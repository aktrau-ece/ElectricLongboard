from pprint import pformat
from time import sleep
import logging
from collections import deque
import threading

import RPi.GPIO as GPIO
import bluetooth

from motorcontrol import MotorControl
from speedsensor import SpeedSensor
from stats import Stats

log = logging.getLogger(__name__)

GPIO.setmode(GPIO.BCM)

REMOTE_CONTROL_MAC_ADDRESS = '48:E7:29:A1:85:86'

MOTOR_THROTTLE_UPDATE_RATE = 20 # Hz

WHEEL_1_MOTOR_THROTTLE_PIN = 12
WHEEL_1_HALL_LATCH_PIN = 17
WHEEL_2_HALL_LATCH_PIN = 27

'''
Controls the longboard by establishing a connection with the remote control, recording sensor data, and sending
throttle signals to the motors. Remote control communication, sensor data collection, and motor control are done
concurrently.
'''
class Controller:

	def __init__(self, **kwargs):

		kwparams = ['enable_traction_control']
		for arg in kwargs:
			if arg not in kwparams: log.error(f'Unknown argument: {arg}')

		self.enable_traction_control = kwargs.get('enable_traction_control', False)

		self.motor_control_1 = MotorControl(motor_throttle_pin=WHEEL_1_MOTOR_THROTTLE_PIN)

		self.remote_control = RemoteControl(
			name = 'controller:remote',
			periph_macaddr = REMOTE_CONTROL_MAC_ADDRESS
		)

		self.drivewheel_speedsensor = SpeedSensor(name='drive', hall_sensor_pin=WHEEL_1_HALL_LATCH_PIN)
		self.freewheel_speedsensor = SpeedSensor(name='free', hall_sensor_pin=WHEEL_2_HALL_LATCH_PIN)

		self.stats = Stats(
			components = [self.remote_control, self.drivewheel_speedsensor, self.freewheel_speedsensor]
		)

	def start(self):

		try:
			self.remote_control.start()
			self.drivewheel_speedsensor.start()
			self.stats.start()

			while True:
				throttle = self.calcThrottle(self.enable_traction_control)
				self.motor_control_1.applyThrottle(throttle)

				sleep(1/MOTOR_THROTTLE_UPDATE_RATE)

		except KeyboardInterrupt:
			self.remote_control.stop()
			self.drivewheel_speedsensor.stop()
			self.stats.stop()

			self.remote_control.join()
			self.drivewheel_speedsensor.join()
			self.stats.join()

			GPIO.cleanup()

	def calcThrottle(self, enable_traction_control):

		joystick_pos = self.remote_control.getAveragedJoystickPos()

		free_wheel_speed = self.freewheel_speedsensor.getCurrentWheelSpeed()
		drive_wheel_speed = self.drivewheel_speedsensor.getCurrentWheelSpeed()

		# If the rotational speed of the free wheel is more than 30 Hz, reduce motor throttle (limits speed)
		if free_wheel_speed > 30: return 0

		if enable_traction_control:

			user_throttle = self.constrainNum(joystick_pos, min_val=0, max_val=100)

			if (drive_wheel_speed + free_wheel_speed) == 0:
				throttle = user_throttle

			elif self.normalizedDifference(drive_wheel_speed, free_wheel_speed) > 1/2:
				throttle = 0

		else: throttle = self.constrainNum(joystick_pos, min_val=0, max_val=100)

		return throttle

	@staticmethod
	def constrainNum(value, min_val, max_val):

		constrained_val = max(min_val, min(max_val, value))
		return constrained_val

	@staticmethod
	def normalizedDifference(val_1, val_2):

		normalized_diff = (val_1 - val_2) / (val_1 + val_2)
		return normalized_diff

'''
This class communicates with the remote control (ESP32 connected to a joystick) via bluetooth classic.
'''
class RemoteControl(threading.Thread):

	'''
	Params:
		`name`: The name of this thread (used for logging) (default is "controller:remote")
		`periph_macaddr`: MAC address of the remote control
		`size`: Bluetooth receive size (default is 1024)
		`log`: Optional logger. If not specified, a logger with the name given in the `name` param will
			be created and used
	'''
	def __init__(self, periph_macaddr, **kwargs):

		threading.Thread.__init__(self)
		self.stop_event = threading.Event()

		self.periph_macaddr = periph_macaddr

		kwparams = ['name', 'size', 'log']
		for arg in kwargs:
			if arg not in kwparams: log.error(f'Unknown argument: {arg}')

		self.name = kwargs.get('name', 'controller:remote')
		self.size = kwargs.get('size', 1024)
		self.log = kwargs.get('log', logging.getLogger(self.name))

		self.joys_pos_buffer = deque([0 for i in range(10)], maxlen=10) # joystick position buffer.
			# circular buffer used to keep a short history of joystick position data - intended 
			# to be used for smoothening any abrupt throttle changes. It can take values from 0 to 100

		# Mutex for managing changes to `joys_pos_buffer`
		self.joys_pos_buffer_lock = threading.Lock()

	def run(self):

		self.log.info('Here!')

		port, name, host = self.findService()
		sock = self.connectToClient(port, name, host)
		self.readMessages(sock)

	def stop(self):

		self.log.info(f'Stopping..')
		self.stop_event.set()

	def scanForDevices(self):

		self.log.info(f'Scanning for bluetooth peripherals..')
		available_devices = bluetooth.discover_devices(lookup_names=True, lookup_class=True)
		devices_unpacked = [f'{name} | {addr} | {_class}' for addr, name, _class in available_devices]
		self.log.info( 'Found devices: ' + pformat(devices_unpacked) )

	def findService(self):

		self.log.info(f'Scanning for bluetooth services..')

		service_matches = bluetooth.find_service(address=self.periph_macaddr)
		self.log.info('Found services: ' + pformat(service_matches) )

		first_match = service_matches[0]
		port = first_match["port"]
		name = first_match["name"]
		host = first_match["host"]

		return port, name, host

	def connectToClient(self, port, name, host):

		self.log.info(f'Connecting to client..')
		sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		sock.connect((host, port))

		return sock

	def readMessages(self, sock):

		self.log.info('Reading messages..')

		try:
			while not self.stop_event.is_set():
				data = sock.recv(self.size)
				joystick_pos = int(data.decode('utf-8'))

				self.pushJoystickBuffer(joystick_pos)
				self.log.debug(f'Joystick position buffer: {self.getJoystickBufferAsList()}')

		finally: sock.close()

	def pushJoystickBuffer(self, pos:int):

		with self.joys_pos_buffer_lock:
			self.joys_pos_buffer.append(pos)

	def getJoystickBufferAsList(self):

		with self.joys_pos_buffer_lock:
			buffer = list(self.joys_pos_buffer)

		return buffer

	def getAveragedJoystickPos(self):

		with self.joys_pos_buffer_lock:
			buffer = list(self.joys_pos_buffer)

		avg = sum(buffer) / len(buffer)
		return avg

	def getCurrentJoystickPos(self):

		with self.joys_pos_buffer_lock:
			current_js_pos = self.joys_pos_buffer[-1]

		return current_js_pos

	def getStats(self):

		stats = f'{__name__} | {self.name} | {str(self.getJoystickBufferAsList())}'
		return stats
from pprint import pformat
from time import sleep
import logging
from collections import deque
import threading

import RPi.GPIO as GPIO
import bluetooth

from motorcontrol import MotorControl
from speedsensor import SpeedSensor

log = logging.getLogger(__name__)

GPIO.setmode(GPIO.BCM)

REMOTE_CONTROL_MAC_ADDRESS = '48:E7:29:A1:85:86'

MOTOR_1_THROTTLE_PIN = 12

MOTOR_THROTTLE_UPDATE_RATE = 20 # Hz

'''
Controls the longboard by establishing a connection with the remote control, recording sensor data, and sending
throttle signals to the motors. Remote control communication, sensor data collection, and motor control are done
concurrently.
'''
class Controller:

	def __init__(self, **kwargs):

		kwparams = ['name', 'size', 'log']
		for arg in kwargs:
			if arg not in kwparams: log.error(f'Unknown argument: {arg}')

		self.enable_traction_control = kwargs.get('enable_traction_control', True)

		self.motor_control_1 = MotorControl(motor_throttle_pin=MOTOR_1_THROTTLE_PIN)

		self.remote_control = RemoteControl(
			name = 'controller:remote',
			periph_macaddr = REMOTE_CONTROL_MAC_ADDRESS
		)

		self.drivewheel_speedsensor = SpeedSensor(hall_sensor_pin=17)

	def start(self):

		try:
			self.remote_control.start()
			self.drivewheel_speedsensor.start()

			while True:
				joystick_pos = self.remote_control.getAverageJoystickPos()
				throttle = self.calcThrottle(joystick_pos, self.enable_traction_control)
				self.motor_control_1.applyThrottle(throttle)

				sleep(1/MOTOR_THROTTLE_UPDATE_RATE)

		except KeyboardInterrupt:
			self.remote_control.stop()
			self.drivewheel_speedsensor.stop()

			self.remote_control.join()
			self.drivewheel_speedsensor.join()

			GPIO.cleanup()

	def calcThrottle(self, joystick_pos, enable_traction_control=self.enable_traction_control):

		if enable_traction_control:
			user_throttle = self.constrainNum(joystick_pos, min_val=0, max_val=100)


		else:
			throttle = self.constrainNum(joystick_pos, min_val=0, max_val=100)

		return throttle

	@staticmethod
	def constrainNum(value, min_val, max_val):

		constrained_val = max(min_val, min(max_val, value))
		return constrained_val

'''
This thread communicates with the remote control (ESP32 connected to a joystick) via bluetooth classic.
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

	def getAverageJoystickPos(self):

		with self.joys_pos_buffer_lock:
			buffer = list(self.joys_pos_buffer)

		avg = sum(buffer) / len(buffer)
		return avg

	def getCurrentJoystickPos(self):

		with self.joys_pos_buffer_lock:
			current_js_pos = self.joys_pos_buffer[-1]

		return current_js_pos
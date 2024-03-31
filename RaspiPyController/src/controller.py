from pprint import pformat
from time import sleep
import logging
from collections import deque
import threading

import RPi.GPIO as GPIO
import bluetooth

log = logging.getLogger(__name__)

GPIO.setmode(GPIO.BCM)

PERIPHERAL_MAC_ADDRESS = '48:E7:29:A1:85:86'

'''
Controls the longboard by establishing a connection with the remote control, recording sensor data, and sending
throttle signals to the motors. Remote control communication, sensor data collection, and motor control are done
concurrently.
'''
class Controller:

	def __init__(self, **kwargs):

		kwparams = ['traction_control']
		for arg in kwargs:
			if arg not in kwparams: log.error(f'Unknown argument: {arg}')

		self.traction_control = kwargs.get('traction_control', True)

	def start(self):
		
		self.joystick_buffer = Queue(maxsize=10) # queue for tracking joystick position reports
		self.joystick_buffer_lock = threading.Lock() # mutex for updating the joystick_buffer

		self.remote_control = RemoteControl(
			joystick_buffer = self.joystick_buffer,
			joystick_buffer_lock = self.joystick_buffer_lock,
			name = 'controller:remote',
			periph_macaddr = PERIPHERAL_MAC_ADDRESS
		)

		self.remote_control.run()
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
	def __init__(self, **kwargs):

		threading.Thread.__init__(self)

		kwparams = ['name', 'periph_macaddr', 'size', 'log']
		for arg in kwargs:
			if arg not in kwparams: log.error(f'Unknown argument: {arg}')

		self.name = kwargs.get('name', 'controller:remote')
		self.periph_macaddr = kwargs.get('periph_macaddr', PERIPHERAL_MAC_ADDRESS)
		self.size = kwargs.get('size', 1024)
		self.log = kwargs.get('log', logging.getLogger(self.name))


		self.joys_pos_buffer = deque([0 for i in range(10)], maxlen=10) # joystick position buffer.
			# circular buffer used to keep a short history of joystick position data - intended 
			# to be used for smoothening any abrupt throttle changes. It can take values from 0 to 100

		self.joys_pos_buffer_lock = threading.Lock() # mutex for managing changes to `joys_pos_buffer`

	def run(self):

		self.log.info('Here!')

		port, name, host = self.findService()
		sock = self.connectToClient(port, name, host)

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

		self.log.info(f'Reading messages..')

		while True:
			data = sock.recv(self.size)
			joystick_pos = int(data.decode('utf-8'))

			self.pushJoystickBuffer(joystick_pos)
			self.log.debug(f'Joystick position buffer: {self.getJoystickBufferAsList()}')

		sock.close()

	def pushJoystickBuffer(self, pos:int):

		with self.joys_pos_buffer_lock:
			self.joys_pos_buffer.append(pos)

	def getJoystickBufferAsList(self):

		return list(self.joys_pos_buffer)
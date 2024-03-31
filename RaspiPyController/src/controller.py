from pprint import pformat
from time import sleep
import logging
from queue import Queue
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
		`joystick_buffer`: Buffer used to keep a short history of joystick position data, intended for
			smoothening any abrupt throttle changes
		`joystick_buffer_lock`: Mutex used for making changes to `joystick_buffer`
		`name`: The name of this thread (used for logging) (default is "controller:remote")
		`periph_macaddr`: MAC address of the remote control
		`size`: Bluetooth receive size (default is 1024)
		`log`: Optional logger. If not specified, a logger with the name given in the `name` param will
			be created and used
	'''
	def __init__(self, joystick_buffer:Queue, joystick_buffer_lock:threading.Lock, **kwargs):

		kwparams = ['name', 'periph_macaddr', 'size', 'log']
		for arg in kwargs:
			if arg not in kwparams: log.error(f'Unknown argument: {arg}')

		threading.Thread.__init__(self)
		self.joystick_buffer = joystick_buffer
		self.joystick_buffer_lock = joystick_buffer_lock
		self.name = kwargs.get('name', 'controller:remote')
		self.periph_macaddr = kwargs.get('periph_macaddr', PERIPHERAL_MAC_ADDRESS)
		self.size = kwargs.get('size', 1024)
		self.log = kwargs.get('log', logging.getLogger(self.name))

	def run(self):

		self.log.info('Here!')

		self.log.info(f'Scanning for bluetooth services..')
		service_matches = bluetooth.find_service(address=self.periph_macaddr)
		self.log.info('Found services: ' + pformat(service_matches) )
		first_match = service_matches[0]
		port = first_match["port"]
		name = first_match["name"]
		host = first_match["host"]

		self.log.info(f'Connecting to client..')
		sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		sock.connect((host, port))

		self.log.info(f'Reading messages..')

		while True:
			raw_data = sock.recv(self.size)
			data = int(raw_data.decode('utf-8'))

			self.joystickBufferForcePush(data)
			self.log.debug(f'Joystick position buffer: {list(self.joystick_buffer.queue)}')

		sock.close()

	'''
	Scan for any nearby bluetooth peripherals
	'''
	def scanForDevices(self):

		self.log.info(f'Scanning for bluetooth peripherals..')
		available_devices = bluetooth.discover_devices(lookup_names=True, lookup_class=True)
		devices_unpacked = [f'{name} | {addr} | {_class}' for addr, name, _class in available_devices]
		self.log.info( 'Found devices: ' + pformat(devices_unpacked) )

	def joystickBufferForcePush(self, item):

		self.joystick_buffer_lock.acquire(blocking=1)

		if self.joystick_buffer.full(): self.joystick_buffer.get()
		self.joystick_buffer.put(item)

		self.joystick_buffer_lock.release()
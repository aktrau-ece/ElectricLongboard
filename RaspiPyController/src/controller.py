from pprint import pformat
from time import sleep
import logging
from queue import Queue
import threading

import bluetooth

log = logging.getLogger(__name__)

PERIPHERAL_MAC_ADDRESS = '48:E7:29:A1:85:86'

class Controller:

	def __init__(self, **kwargs):

		# Check for any bad arguments
		kwparams = []
		for arg in kwargs:
			if arg not in kwparams: log.error(f'Unknown argument: {arg}')

		self.traction_control = kwargs.get('traction_control', True)

	def start(self):
		
		self.joystick_buffer_lock = threading.Lock()
		self.joystick_buffer = Queue(maxsize=10)
		self.remote_control = RemoteControl(
			joystick_buffer = self.joystick_buffer,
			joystick_buffer_lock = self.joystick_buffer_lock,
			name = 'controller:remote',
			slave_macaddr = PERIPHERAL_MAC_ADDRESS
		)

		self.remote_control.run()

class RemoteControl(threading.Thread):

	def __init__(self, joystick_buffer:Queue, joystick_buffer_lock, **kwargs):

		# Check for any bad arguments
		kwparams = ['name', 'slave_macaddr', 'size', 'log']
		for arg in kwargs:
			if arg not in kwparams: log.error(f'Unknown argument: {arg}')

		threading.Thread.__init__(self)
		self.joystick_buffer = joystick_buffer
		self.joystick_buffer_lock = joystick_buffer_lock
		self.name = kwargs.get('name', 'controller:remote')	
		self.slave_macaddr = kwargs.get('slave_macaddr', PERIPHERAL_MAC_ADDRESS)
		self.size = kwargs.get('size', 1024)
		self.log = kwargs.get('log', logging.getLogger(self.name))

	def run(self):

		self.log.info('Here!')

		# self.log.info(f'Scanning for bluetooth peripherals..')
		# available_devices = bluetooth.discover_devices(lookup_names=True, lookup_class=True)
		# devices_unpacked = [f'{name} | {addr} | {_class}' for addr, name, _class in available_devices]
		# self.log.info( 'Found devices: ' + pformat(devices_unpacked) )

		self.log.info(f'Scanning for bluetooth services..')
		service_matches = bluetooth.find_service(address=self.slave_macaddr)
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
			data = repr(raw_data.decode('utf-8'))
			if data:
				self.joystickBufferForcePush(data)
				self.log.debug(f'Joystick position buffer: {list(self.joystick_buffer.queue)}')

		sock.close()

	def joystickBufferForcePush(self, item):

		self.joystick_buffer_lock.acquire(blocking=1)
		if self.joystick_buffer.full(): self.joystick_buffer.get()
		self.joystick_buffer.put(item)
		self.joystick_buffer_lock.release()
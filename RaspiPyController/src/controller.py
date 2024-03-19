from pprint import pformat
from time import sleep
import logging

import bluetooth

log = logging.getLogger(__name__)

PERIPHERAL_MAC_ADDRESS = '48:E7:29:A1:85:84'

class Controller:

	def __init__(self, **kwargs):

		self.traction_control = kwargs.get('traction_control', True)

		# Check for bad arguments in kwargs
		kwparams = []
		for arg in kwargs:
			if arg not in kwparams: log.error(f'Unknown argument: {arg}')
		

	def start(self):
		
		self.connectToRemote()

	def connectToRemote(self, server_addr=PERIPHERAL_MAC_ADDRESS, port=3, backlog=1, size=1024):

		log.debug(f'Scanning for bluetooth peripherals..')
		available_devices = bluetooth.discover_devices(lookup_names=True, lookup_class=True)
		devices_unpacked = [f'{name} | {addr} | {_class}' for addr, name, _class in available_devices]
		log.info( 'Found devices:\n' + pformat(devices_unpacked) )

		log.debug(f'Scanning for bluetooth services..')
		service_matches = bluetooth.find_service()
		log.debug('Found services:\n' pformat(service_matches) )
		# first_match = service_matches[0]
		# port = first_match["port"]
		# name = first_match["name"]
		# host = first_match["host"]


		log.debug(f'Connecting to client..')
		sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		sock.connect((server_addr, port))

		while 1:
			data = sock.recv(size)
			if data: print(data)
			else: print('No data')
			sleep(1)

		sock.close()

from pprint import pformat
from time import sleep
import logging

import bluetooth as bt

log = logging.getLogger(__name__)

PERIPHERAL_MAC_ADDRESS = '24:DC:C3:98:9E:F0'

class Controller:

	def __init__(self, **kwargs):

		self.traction_control = kwargs.get('traction_control', True)

		# Check for bad arguments in kwargs
		kwparams = []
		for arg in kwargs:
			if arg not in kwparams: log.error(f'Unknown argument: {arg}')
		

	def start(self):
		
		self.connectWithRemote()

	def connectWithRemote(self, remote_mac=PERIPHERAL_MAC_ADDRESS):

		service_matches = bt.find_service( address=remote_mac )
		if len(service_matches) == 0: log.error(f'Bluetooth peripheral not found')

		log.debug(f'Available bluetooth peripherals: {pformat(service_matches)}')

		service_match = service_matches[0] # pick the 1st match
		port = service_match['port']
		name = service_match['name']
		host = service_match['host']

		log.debug(f'Connecting to "{name}", on host {host}, through port {port}..')
		sock = bt.BluetoothSocket(bt.RFCOMM)
		connection_result = sock.connect((host, port))
		log.debug(f'{connection_result}')
		
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

	def connectToRemote(self, client_addr=PERIPHERAL_MAC_ADDRESS, port=3, backlog=1, size=1024):

		log.debug(f'Searching for bluetooth peripherals..')
		available_devices = bluetooth.discover_devices(lookup_names=True, lookup_class=True)
		devices_unpacked = [f'{name} | {addr} | {_class}' for addr, name, _class in available_devices]
		log.info( pformat(devices_unpacked) )

		sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		sock.bind((hostMACAddress, port))
		sock.listen(backlog)

		client, client_info = sock.accept()
		while 1:
			data = client.recv(size)
			if data: print(data)

		sock.close()

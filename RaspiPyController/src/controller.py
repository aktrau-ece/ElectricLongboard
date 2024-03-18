from pprint import pformat
from time import sleep
import logging
from enum import Enum

log = logging.getLogger(__name__)

PERIPHERAL_MAC_ADDRESS = ''

class DriveMode(Enum):
	FWD = 0 # front wheel drive
	RWD = 1 # rear wheel drive

class Controller:

	def __init__(self, drive_mode:DriveMode, **kwargs):
		
		self.drive_mode = drive_mode

		# Check for bad arguments
		kwparams = []
		for arg in kwargs:
			if arg not in kwparams: log.error(f'Unknown argument: {arg}')
		

	def start(self):
		
		pass

	def connectWithRemote(self, remote_mac=PERIPHERAL_MAC_ADDRESS):

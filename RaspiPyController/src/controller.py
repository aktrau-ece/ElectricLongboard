from pprint import pformat
from time import sleep
import logging

from motor import tb6612fng

log = logging.getLogger(__name__)

class Controller:

	def __init__(self):
		pass

	def start(self):
		
		log.debug('Starting motor..')
		tb6612fng.runMotor()
		sleep(5)
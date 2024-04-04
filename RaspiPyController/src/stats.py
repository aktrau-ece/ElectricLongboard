from pprint import pformat
from time import sleep
import logging, logging.config
import threading

import numpy as np

log = logging.getLogger(__name__)

STAT_DISPLAY_RATE = 1

class Stats(threading.Thread):

	'''
	Params:
		`components`: list of components which must each have a .getStats() method.
	'''
	def __init__(self, components:list):

		threading.Thread.__init__(self)
		self.stop_event = threading.Event()

		self.components = components

	def run(self):

		log.info(f'Lets fucking do this!!!')
		self.displayStatsContinuous()

	def stop(self):

		log.info(f'Stopping..')
		self.stop_event.set()

	def displayStatsContinuous(self):

		log.info(f'Beginning stats display')

		display_time = 1 / STAT_DISPLAY_RATE

		while not self.stop_event.is_set():

			stats ='\n'.join([component.getStats() for component in self.components])
			log.info(pformat(stats))

			sleep(display_time)
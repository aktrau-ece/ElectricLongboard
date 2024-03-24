from pprint import pformat
from time import sleep
import logging, logging.config

import RPi.GPIO as GPIO

log = logging.getLogger(__name__)

GPIO.setmode(GPIO.BOARD)
HALL_PIN = 23

def testHallSensor():

	log.debug('Hall sensor test start')

	GPIO.setup(HALL_PIN, GPIO.IN)

	coin = True
	while True:

		if coin: indent = ' '
		else: indent = ''

		if GPIO.input(HALL_PIN) == GPIO.HIGH:
			log.debug(f'{indent}+')
		else: log.debug(f'{indent}-')

		sleep(0.5)

	GPIO.cleanup()

if __name__ == '__main__':

	LOGGING_CONFIG = {
		'version': 1,
		'disable_existing_loggers' : False,

		'loggers': {
			'main': {
				'handlers': ['console'],
				'level': 'DEBUG'
			}
		},

		'handlers': {
			'console': {
				'level': 'DEBUG',
				'formatter': 'console',
				'class': 'logging.StreamHandler',
				'stream': 'ext://sys.stdout'
			}
		},

		'formatters': {
			'standard': { 'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s' },
			'console': { 'format': '[%(levelname)s] %(name)s: %(message)s' }
		},
	}

	logging.config.dictConfig(LOGGING_CONFIG)
	log = logging.getLogger('main')

	testHallSensor()
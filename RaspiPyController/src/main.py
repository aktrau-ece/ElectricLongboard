import os
from pprint import pformat
import logging, logging.config

from controller import Controller

CONFIGURATION = CF = {}

LOGGING_CONFIG = {
	'version': 1,
	'disable_existing_loggers' : False,

	'loggers': {
		'main': {
			'handlers': ['console'],
			'level': 'DEBUG'
		},
		'controller': {
			'handlers': ['console'],
			'level': 'DEBUG'
		},
		'controller:remote': {
			'handlers': ['console'],
			'level': 'DEBUG' # DEBUG not recommended for fast remote control report rates
		},
		'motor.TB6612FNG': {
			'handlers': ['console'],
			'level': 'DEBUG'
		},
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

def main():

	log.debug('Beginning of script')

	controller = Controller()
	controller.start()

if __name__ == '__main__':
	main()
	input('End of script, press <ENTER> to quit')
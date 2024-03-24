from pprint import pformat
from time import sleep
import logging, logging.config

import RPi.GPIO as GPIO

log = logging.getLogger(__name__)

PWM_FREQ = 1000 # [Hz]
MOTOR_1_PWM_PIN = 12

def testMotorControl():

	log.debug('Motor control test start')

	GPIO.setup(MOTOR_1_PWM_PIN, GPIO.OUT)

	pwm_1 = GPIO.PWM(MOTOR_1_PWM_PIN, PWM_FREQ)
	pwm_1.start(0)

	while True:

		log.debug('Setting duty cycle to "70%"')
		pwm_1.ChangeDutyCycle(70)
		sleep(2)

		log.debug('Setting duty cycle to "80%"')
		pwm_1.ChangeDutyCycle(80)
		sleep(2)

		log.debug('Setting duty cycle to "90%"')
		pwm_1.ChangeDutyCycle(90)
		sleep(2)

		log.debug('Setting duty cycle to "80%"')
		pwm_1.ChangeDutyCycle(80)
		sleep(2)

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

	GPIO.setmode(GPIO.BCM)

	testMotorControl()
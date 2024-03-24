from pprint import pformat
from time import sleep
import logging

import RPi.GPIO as GPIO

log = logging.getLogger(__name__)

GPIO.setmode(GPIO.BOARD)
HALL_PIN = 23

def testHallSensor():

	log.debug('Hall sensor test start')

	GPIO.setup(HALL_PIN, GPIO.IN)
	while True:
		if GPIO.input(HALL_PIN) == GPIO.HIGH:
			log.debug('+')
		else: log.debug('-')

		sleep(0.5)

	GPIO.cleanup()
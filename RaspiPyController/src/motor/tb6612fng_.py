from pprint import pformat
from time import sleep
import logging

import RPi.GPIO as GPIO

log = logging.getLogger(__name__)

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.OUT) # PWM
GPIO.setup(18, GPIO.OUT) # AIN2
GPIO.setup(16, GPIO.OUT) # AIN1
GPIO.setup(22, GPIO.OUT) # STBY

PWM_FREQ = 100
PWM = GPIO.PWM(12, PWM_FREQ)
PWM.start(PWM_FREQ)

def runMotor():

	# GPIO.output(22, GPIO.HIGH) # enable standby
	GPIO.output(16, GPIO.LOW)
	GPIO.output(18, GPIO.HIGH)

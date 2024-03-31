from pprint import pformat
from time import sleep
import logging, logging.config
import threading

import RPi.GPIO as GPIO

log = logging.getLogger(__name__)

PWM_FREQ = 1000 # [Hz]

class MotorControl(threading.Thread):

	def __init__(self, motor_throttle_pin:int):

		threading.Thread.__init__(self)
		self.motor_throttle_pin = motor_throttle_pin

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

		self.initGPIOPins()

	def initGPIOPins(self):

		GPIO.setup(self.motor_throttle_pin, GPIO.OUT)
		self.motor_pwm = GPIO.PWM(self.motor_throttle_pin, PWM_FREQ)
		self.motor_pwm.start(0)

	'''
	Params:
		`throttle`: amount of throttle to apply to motors (int between 0 and 100)
	'''
	def applyThrottle(self, throttle):

		min_duty_cycle = 30
		max_duty_cycle = 100

		duty_cycle = int(throttle/100 * (max_duty_cycle-min_duty_cycle) + min_duty_cycle)

		self.setPWMDutyCycle(duty_cycle)

	def setPWMDutyCycle(self, duty_cycle):

		self.motor_pwm.ChangeDutyCycle(duty_cycle)
		log.debug(f'Set duty cycle to {duty_cycle}%')
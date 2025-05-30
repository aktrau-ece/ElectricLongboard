from pprint import pformat
from time import sleep
from collections import deque
import logging, logging.config
import threading

import RPi.GPIO as GPIO
import numpy as np

log = logging.getLogger(__name__)

# How often to sample the magnetic latch (Hz)
# Default: 360
HALL_EFFECT_LATCH_SAMPLE_RATE = 360

# How many samples should be taken before reporting the wheel speed
# Larger values will reduce the report rate, but improves report accuracy
# Default: 36
HALL_EFFECT_LATCH_SAMPLES_PER_WHEEL_SPEED_REPORT = 36

# How many magnets are along the perimeter of the wheel.
# It should be an even number, since the magnetic polarity should
# flip between magnets
MAGNETS_PER_WHEEL = 6

class SpeedSensor(threading.Thread):

	def __init__(self, name, hall_sensor_pin:int):

		threading.Thread.__init__(self)
		self.stop_event = threading.Event()

		self.hall_sensor_pin = hall_sensor_pin
		self.name = name

		self.initGPIOPins()
		log.info(f'Initialized speed sensor using pin {self.hall_sensor_pin}')

		# Circular buffer for storing a history of wheel-speed recordings
		self.wheelspeed_buffer = deque([0 for i in range(10)], maxlen=10)

		# Mutex for managing changes to `wheelspeed_buffer`
		self.wheelspeed_buffer_lock = threading.Lock()

	def initGPIOPins(self):

		GPIO.setup(self.hall_sensor_pin, GPIO.IN)

	def run(self):

		log.info(f'Here!!!!!')
		self.recordWheelSpeed()

	def stop(self):

		log.info(f'Stopping..')
		self.stop_event.set()

	def recordWheelSpeed(self):

		sample_rate = HALL_EFFECT_LATCH_SAMPLE_RATE
		samples_per_report = HALL_EFFECT_LATCH_SAMPLES_PER_WHEEL_SPEED_REPORT
		latch_sample_time = 1 / sample_rate
		report_rate = sample_rate / samples_per_report
		report_time = 1 / report_rate

		samples = np.zeros(samples_per_report, dtype=bool)

		while not self.stop_event.is_set():

			'''
			I suspect that this loop might be performance-limiting, so im using numpy where i can,
			although the array sizes are still pretty small
			'''

			for i in range(samples_per_report):

				sample = GPIO.input(self.hall_sensor_pin)
				samples[i] = sample

				sleep(latch_sample_time)

			# Count the amount of times the sample switches from HIGH to LOW or vice versa - how many
			# times it "flips" while iterating through the array
			num_flips = np.sum(samples[:-1] != samples[1:])

			# Wheel spin frequency in Hz
			# Note that each "flip" incident occurs when a magnet passes by the magnetic latch - 
			# each full wheel revolution comprises of a `MAGNETS_PER_WHEEL` amount of flips.
			wheel_spin_freq = num_flips / MAGNETS_PER_WHEEL / report_time

			self.pushWheelSpeedBuffer(wheel_spin_freq)
			log.debug(f'Wheel speed history: {self.getWheelSpeedBufferAsList()}')

	'''
	Params:
		`speed`: wheel rotation frequency in Hz
	'''
	def pushWheelSpeedBuffer(self, speed):

		with self.wheelspeed_buffer_lock:
			self.wheelspeed_buffer.append(speed)

	def getWheelSpeedBufferAsList(self, decimal_places=2):

		with self.wheelspeed_buffer_lock:
			buffer = list(self.wheelspeed_buffer)
		
		rounded_buffer = np.round(buffer, decimal_places)
		return rounded_buffer

	def getCurrentWheelSpeed(self):

		with self.wheelspeed_buffer_lock:
			current_wheelspeed = self.wheelspeed_buffer[-1]

		return current_wheelspeed

	def getStats(self):

		stats = f'{__name__} | {self.name} | {str(self.getWheelSpeedBufferAsList())}'
		return stats
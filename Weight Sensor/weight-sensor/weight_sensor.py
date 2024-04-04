# weight-sensor/weight_sensor.py

import RPi.GPIO as GPIO
from hx711 import HX711

class WeightSensor:
    def __init__(self, dout_pin, pd_sck_pin, target_weight):
        GPIO.setmode(GPIO.BCM)
        self.hx = HX711(dout_pin=dout_pin, pd_sck_pin=pd_sck_pin)
        self.target_weight = target_weight
        self.initialize_scale()

    def initialize_scale(self):
        self.hx.reset()
        err = self.hx.zero()
        if err:
            raise ValueError("Tare is unsuccessful.")
        # The scale ratio should be calibrated beforehand and set here
        self.hx.set_scale_ratio(2280)  # Example scale ratio

    def read_weight(self):
        weight = self.hx.get_weight_mean(5)
        return weight

    def check_weight(self):
        try:
            weight = self.read_weight()
            return 1 if weight > self.target_weight else 0
        except Exception as e:
            print("Error reading HX711.", e)
            self.initialize_scale()

import time
from hx711 import HX711

hx = HX711(dout_pin=23, pd_sck_pin=22)

def initialize_scale():
    """
    Initialize the HX711 scale.
    """
    hx.reset()  
    hx.set_scale_ratio(2280)  # Calibration Value
    hx.tare()  
    print("Scale initialized.")

def read_weight():
    """
    Read and return the weight from the scale.
    """
    try:
        weight = hx.get_weight_mean(5)
        return weight
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception as e:
        print("HX711 not found. Attempting reinitialization.", e)
        initialize_scale()

def main():
    initialize_scale()
    while True:
        weight = read_weight()
        print(f"Reading: | Weight: {weight:.2f} kg")
        
        if weight < 13:  # Checking if the weight is less than 13kg
            print("Weight is less than 13kg pounds. Shutting off motors.")
            # code here to shut off the motors
        
        time.sleep(1)  # Delay before the next read

if __name__ == "__main__":
    main()
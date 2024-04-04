from weight_sensor import WeightSensor
import time  # Import the time module for sleep functionality

def main():
    #GPIO Pin definations
    dout_pin = 23 
    pd_sck_pin = 22
    target_weight = 13

    sensor = WeightSensor(dout_pin, pd_sck_pin, target_weight)

    print("Checking weight...")
    while True:  # Start an infinite loop
        result = sensor.check_weight()
        print("Weight check result:", "Above target" if result == 1 else "Below target")
        time.sleep(1)  # Wait for 1 second before the next check

if __name__ == "__main__":
    main()

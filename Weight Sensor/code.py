# code.py

from weight_sensor import WeightSensor

def main():
    dout_pin = int(input("Enter DOUT pin number: "))
    pd_sck_pin = int(input("Enter PD_SCK pin number: "))
    target_weight = float(input("Enter target weight value (kg): "))

    sensor = WeightSensor(23, 22, 13.0)

    print("Checking weight...")
    result = sensor.check_weight()
    print("Weight check result:", "Above target" if result == 1 else "Below target")

if __name__ == "__main__":
    main()

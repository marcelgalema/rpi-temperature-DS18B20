import os
import glob
import time

# calibration explanation and info can be found on  https://www.instructables.com/Calibration-of-DS18B20-Sensor-With-Arduino-UNO/


class DS18B20:
    device_file: str = ""
    base_dir: str = "/sys/bus/w1/devices/"
    raw_high: float = 100  # the raw temp when the sensor is in boiling water
    raw_low: float = 0  # the raw temp when the sensor is in melting ice
    reference_high: float = 100.19  # in Utrecht, NL on 1 ft altitude
    reference_low: float = 0
    temp_c: int = 0
    temp_format: str = "c"
    precision: float = 2
    debug: bool = False

    def __init__(self, args=None):
        self.temp_format = args.format
        self.precision = args.precision
        self.raw_high = args.raw_high
        self.raw_low = args.raw_low
        self.reference_high = args.reference_high
        self.reference_low = args.reference_low
        self.debug = args.debug

        # 1Wired sensors appear in this folder
        # DS18B20 sensors have an ID starting with 28
        if self.debug:
            self.base_dir = "." + self.base_dir

        globbed = glob.glob(self.base_dir + "28*")
        if len(globbed):

            if self.debug == False:
                os.system("modprobe w1-gpio")
                os.system("modprobe w1-therm")

            self.device_file = globbed[0] + "/w1_slave"
        else:
            print("No sensors found, exiting")
            # exit(1)

    def __repr__(self):
        return f"Sensor ID {self.get_id()}"

    def get_id(self):
        return self.device_file.split("/")[5]

    def raw_range(self):
        return self.raw_high - self.raw_low

    def reference_range(self):
        return self.reference_high - self.reference_low

    def get_temperature(self):
        self.__read_temp()

        calibrated_temp = (
            ((self.temp_c - self.raw_low) * self.reference_range()) / self.raw_range()
        ) + self.reference_low

        if self.temp_format == "c":
            return self.__get_temparature_celsius(calibrated_temp)
        else:
            return self.___get_temparature_fahrenheit(calibrated_temp)

    def __get_temparature_celsius(self, calibrated_temp: float):
        return f"{calibrated_temp:.{self.precision}f} Celsius"

    def ___get_temparature_fahrenheit(self, calibrated_temp: float):
        return f"{calibrated_temp* 9.0 / 5.0 + 32.0:.{self.precision}f} Fahrenheit"

    def __read_temp_raw(self):
        f = open(self.device_file, "r")
        lines = f.readlines()
        f.close()
        return lines

    def __read_temp(self):
        lines = self.__read_temp_raw()
        while lines[0].strip()[-3:] != "YES":
            time.sleep(0.2)
            lines = self.__read_temp_raw()

        equals_pos = lines[1].find("t=")

        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2 :]
            self.temp_c = float(temp_string) / 1000.0

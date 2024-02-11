import os
import glob
import time


class DS18B20:
    device_file = ""
    base_dir = "/sys/bus/w1/devices/"
    temp_c = 0
    temp_format = "c"
    precision = 2

    def __init__(self, args=None):
        self.temp_format = args.format
        self.precision = args.precision

        # 1Wired sensors appear in this folder
        # DS18B20 sensors have an ID starting with 28
        globbed = glob.glob(self.base_dir + "28*")
        if len(globbed):
            os.system("modprobe w1-gpio")
            os.system("modprobe w1-therm")
            self.device_file = globbed[0] + "/w1_slave"
        else:
            print("No sensors found, exiting")
            exit(1)

    def __str__(self):
        return f"Sensor ID {self.get_id()}"

    def get_id(self):
        return self.device_file.split("/")[5]

    def get_temperature(self):
        self.__read_temp()
        if self.temp_format == "c":
            return self.__get_temparature_celsius()
        else:
            return self.___get_temparature_fahrenheit()

    def __get_temparature_celsius(self):
        return f"{self.temp_c:.{self.precision}f} Celsius"

    def ___get_temparature_fahrenheit(self):
        return f"{self.temp_c * 9.0 / 5.0 + 32.0:.{self.precision}f} Fahrenheit"

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

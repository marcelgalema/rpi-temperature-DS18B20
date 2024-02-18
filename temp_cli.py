#!/usr/bin/env python

import time
from ds18b20 import DS18B20
from appargs import AppArgs


if __name__ == "__main__":
    args = AppArgs()
    args.handle_cli_args()

    sensor_ds18b20 = DS18B20(args)
    print(f"{sensor_ds18b20}, refresh every {args.refresh_rate} seconds\n")

    while True:
        print(f"Temperature: {sensor_ds18b20.get_temperature()}")
        time.sleep(args.refresh_rate)

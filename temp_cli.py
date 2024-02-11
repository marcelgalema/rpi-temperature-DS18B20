#!/usr/bin/env python

import argparse
import time
from ds18b20 import DS18B20


def handle_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--precision",
        help="specify the temperature precision",
        type=int,
        default=2,
    )
    parser.add_argument(
        "-r",
        "--refresh_rate",
        help="specify the refresh rate in seconds",
        type=float,
        default=5,
    )
    parser.add_argument(
        "-f",
        "--format",
        help="report in degrees Celsius or Fahrenheit",
        type=str,
        choices=["c", "f"],
        default="c",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = handle_cli_args()

    sensor_ds18b20 = DS18B20(args)
    print(f"{sensor_ds18b20}, refresh every {args.refresh_rate} seconds\n")

    while True:
        print(f"Temperature: {sensor_ds18b20.get_temperature()}")
        time.sleep(args.refresh_rate)

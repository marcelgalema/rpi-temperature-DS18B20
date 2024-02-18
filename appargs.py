from dataclasses import dataclass
from flask import request
import argparse


@dataclass
class AppArgs:
    precision: int = 2
    raw_high: float = 100
    raw_low: float = 0
    reference_high: float = 100
    reference_low: float = 0
    refresh_rate: float = 5
    format: str = "c"
    debug: bool = False

    def handle_url_args(self):
        self.precision = request.args.get("precision", default=2, type=int)
        self.refresh_rate = request.args.get("refresh_rate", default=5, type=float)
        self.raw_high = request.args.get("raw_high", default=100, type=float)
        self.raw_low = request.args.get("raw_low", default=0, type=float)
        self.reference_high = request.args.get(
            "reference_high", default=100, type=float
        )
        self.reference_low = request.args.get("reference_low", default=0, type=float)
        self.format = request.args.get("format", default="c", type=str)
        self.debug = request.args.get("debug", default=False, type=bool)

    def handle_cli_args(self):
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
            "-h1",
            "--raw_high",
            help="specify the raw temperature in boiling water",
            type=float,
            default=100,
        )
        parser.add_argument(
            "-l1",
            "--raw_low",
            help="specify the raw temperature in melting ice",
            type=float,
            default=0,
        )
        parser.add_argument(
            "-h2",
            "--reference_high",
            help="specify the reference temperature in boiling water",
            type=float,
            default=100,
        )
        parser.add_argument(
            "-l2",
            "--reference_low",
            help="specify the reference temperature in melting ice",
            type=float,
            default=0,
        )
        parser.add_argument(
            "-f",
            "--format",
            help="report in degrees Celsius or Fahrenheit",
            type=str,
            choices=["c", "f"],
            default="c",
        )
        parser.add_argument("-d", "--debug", help="debug mode", action="store_true")

        args = parser.parse_args()
        self.precision = args.precision
        self.debug = args.debug
        self.format = args.format
        self.refresh_rate = args.refresh_rate
        self.raw_high = args.raw_high
        self.raw_low = args.raw_low
        self.reference_high = args.reference_high
        self.reference_low = args.reference_low

#!/usr/bin/env python

import argparse
import time
from ds18b20 import DS18B20
from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.serving import WSGIRequestHandler
from appargs import AppArgs

app = Flask(__name__)


@app.route("/")
def home():
    args = AppArgs()
    args.handle_url_args()

    sensor_ds18b20 = DS18B20(args)

    output = f"<h1>{sensor_ds18b20}</h1>"
    output += f"<p>{sensor_ds18b20}, refresh every {args.refresh_rate} seconds with a precision of {args.precision} digits</p>"
    output += f"<p>Temperature: {sensor_ds18b20.get_temperature()}</p>"

    return output


# running the server
if __name__ == "__main__":

    port_number = 5000
    debug_mode = True
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    class CustomWSGIRequestHandler(WSGIRequestHandler):
        protocol_version: str = "HTTP/1.0"

    app.run(
        debug=debug_mode,
        host="0.0.0.0",
        port=port_number,
        request_handler=CustomWSGIRequestHandler,
    )  # to allow for debugging and auto-reload

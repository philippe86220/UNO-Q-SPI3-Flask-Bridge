import struct
import time
from flask import Flask, jsonify
import spidev

app = Flask(__name__)

NUM_BYTES = 66

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
spi.mode = 0


def read_floats_from_spi():
    spi.xfer2([0x0B] + [0x00] * 15)

    for _ in range(10):
        time.sleep(0.05)

        rx = spi.xfer2([0x00] * NUM_BYTES)

        if rx[0] != 0xA5:
            continue

        count = rx[1]

        if count > 16:
            return {
                "ok": False,
                "error": "Invalid count"
            }

        values = []

        for i in range(count):
            start = 2 + i * 4
            value = struct.unpack("<f", bytes(rx[start:start + 4]))[0]
            values.append(value)

        return {
            "ok": True,
            "values": values
        }

    return {
        "ok": False,
        "error": "Invalid frame"
    }


@app.route("/values")
def values():
    return jsonify(read_floats_from_spi())


@app.route("/status")
def status():
    return jsonify({
        "ok": True,
        "message": "SPI3 Flask service running"
    })


print("SPI3 Flask service started on port 9000", flush=True)
app.run(host="0.0.0.0", port=9000)

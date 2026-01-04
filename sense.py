import asyncio
import time
import numpy as np
from bleak import BleakScanner

WINDOW = 10
THRESHOLD = 20.0

rssi_log = []

def detection_callback(device, advertisement_data):
    if advertisement_data.rssi is not None:
        rssi_log.append(advertisement_data.rssi)

async def main():
    print("Bluetooth sensing started...")

    scanner = BleakScanner(detection_callback)

    await scanner.start()
    try:
        while True:
            if len(rssi_log) >= WINDOW:
                window = rssi_log[-WINDOW:]
                var = np.var(window)
                mean = np.mean(window)
                print(f"RSSI var: {var:.2f}")
                print(f"RSSI mean: {mean:.2f}")

                if var > THRESHOLD:
                    print(">>> PRESENCE / MOTION DETECTED")

            await asyncio.sleep(1)
    finally:
        await scanner.stop()

asyncio.run(main())

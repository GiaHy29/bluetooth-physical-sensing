import asyncio
import time
import numpy as np
from bleak import BleakScanner
from collections import deque

WINDOW = 10          # cửa sổ phân tích
LOG_INTERVAL = 1.0   # giây

# giữ log gọn, không phình RAM
rssi_log = deque(maxlen=500)

def detection_callback(device, advertisement_data):
    if advertisement_data.rssi is not None:
        rssi_log.append(advertisement_data.rssi)

async def main():
    print("Bluetooth sensing started...")
    print("MODE: RAW LOGGING (mean / variance only)")
    print("timestamp, mean_rssi, var_rssi")

    scanner = BleakScanner(detection_callback)
    await scanner.start()

    try:
        while True:
            if len(rssi_log) >= WINDOW:
                window = list(rssi_log)[-WINDOW:]
                mean = np.mean(window)
                var = np.var(window)

                ts = time.strftime("%H:%M:%S")
                print(f"{ts}, {mean:.2f}, {var:.2f}")

            await asyncio.sleep(LOG_INTERVAL)

    finally:
        await scanner.stop()

asyncio.run(main())

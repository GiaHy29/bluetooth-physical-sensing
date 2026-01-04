import asyncio
import time
import json
import numpy as np
from bleak import BleakScanner
from collections import deque

with open("profiles.json") as f:
    PROFILES = json.load(f)

profile = PROFILES["quiet_single_person_wooden_table"]

BASELINE_MEAN = profile.get("baseline_mean", -87.8)
MOTION_CONFIRM = 2
EMPTY_CONFIRM = 3

rssi_log = deque(maxlen=500)

current_state = "EMPTY"
motion_count = 0
empty_count = 0

def detection_callback(device, advertisement_data):
    if advertisement_data.rssi is not None:
        rssi_log.append(advertisement_data.rssi)

async def main():
    global current_state, motion_count, empty_count

    print("Bluetooth sensing started...")
    print("Profile: quiet_single_person_wooden_table")
    print(
        f"Hysteresis: MOTION_CONFIRM={MOTION_CONFIRM}, "
        f"EMPTY_CONFIRM={EMPTY_CONFIRM}"
    )
    print("Press Ctrl+C to quit.\n")

    scanner = BleakScanner(detection_callback)
    await scanner.start()

    try:
        while True:
            if len(rssi_log) >= profile["window"]:
                window = list(rssi_log)[-profile["window"]:]
                mean_now = np.mean(window)
                var_now = np.var(window)

                delta_mean = BASELINE_MEAN - mean_now

                soft_motion = (
                    var_now >= profile.get(
                        "var_motion_soft",
                        profile["var_motion_min"]
                    )
                    and abs(delta_mean) >= 1.5
                )

                if var_now >= profile["var_motion_min"] or soft_motion:
                    motion_count += 1
                    empty_count = 0
                else:
                    empty_count += 1
                    motion_count = 0

                prev_state = current_state

                if current_state != "MOTION" and motion_count >= MOTION_CONFIRM:
                    current_state = "MOTION"

                elif current_state == "MOTION" and empty_count >= EMPTY_CONFIRM:
                    if (
                        delta_mean >= profile["mean_block_drop"]
                        and var_now <= profile["var_empty_max"]
                    ):
                        current_state = "BLOCKED"
                    else:
                        current_state = "EMPTY"

                if current_state != prev_state:
                    ts = time.strftime("%H:%M:%S")
                    print(
                        f"{ts} | mean={mean_now:.2f} "
                        f"var={var_now:.2f} "
                        f"Δmean={delta_mean:.2f} "
                        f"{prev_state} → {current_state}"
                    )

            await asyncio.sleep(1)

    except (KeyboardInterrupt, asyncio.CancelledError):
        print("\nStopping Bluetooth sensing...")

    finally:
        await scanner.stop()
        print("Scanner stopped. Bye.")


if __name__ == "__main__":
    asyncio.run(main())

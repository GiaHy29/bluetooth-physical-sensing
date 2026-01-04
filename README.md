# Bluetooth Physical Presence Sensing (Passive)

This project explores **passive physical presence and motion sensing**
using Bluetooth Low Energy (BLE) RSSI statistics on a single laptop.

The system does **not** interact with or identify devices.
It observes changes in the wireless channel itself.

---

## Motivation

The goal is **not** to locate people or devices,
but to infer **physical environment state changes**
through variations in wireless signal behavior.

This project treats the BLE channel as a physical sensor.

---

## What this project does

- Passively observes BLE RSSI advertisements
- Infers coarse environment states:
  - **EMPTY** — stable channel, no obstruction
  - **BLOCKED** — stable attenuation (static obstruction)
  - **MOTION** — dynamic channel disturbance
- Prioritizes **stability and interpretability** over reaction speed

---

## What this project does NOT do

- No localization or ranging
- No device or person identification
- No imaging or reconstruction
- No active probing or packet injection
- No machine learning

---

## Core Idea

Two simple statistical features are used:

- **RSSI mean**
  - Represents long-term signal attenuation
  - Correlates with static absorption or obstruction

- **RSSI variance**
  - Represents short-term channel instability
  - Correlates with physical motion near the receiver

State inference is performed using:
- sliding window statistics
- environment-specific thresholds
- temporal hysteresis for stability

---

## Design Principles

- Passive only (receive-only sensing)
- Profile-based calibration
- Deterministic logic
- Explainable decisions
- Small, controlled scope

Detection latency (≈2–3 seconds) is **intentional**
and used to suppress transient RF noise.

---

## Status

Research prototype (v2)

The system is stable for controlled experiments
within predefined environments,
but is **not intended for general-purpose deployment**.

---

## Environment Profiles

This project uses **calibrated threshold profiles**
derived from empirical measurements in specific environments.

Profiles are **environment-dependent**
and must be recalibrated when conditions change.

---

### Profile: `quiet_single_person_wooden_table`

**Environment**
- Quiet RF background
- Wooden table surface
- Single person present
- Laptop stationary

**Observed characteristics**
- RSSI variance (empty): ~2–6
- RSSI variance (motion): ≥22
- Mean RSSI drop (blocked): ~4 dB

Thresholds were derived from logged data
and are **not expected to generalize**
without recalibration.

---

## Limitations

- Sensitive to RF environment changes
- Requires manual calibration per environment
- Detects motion presence, not identity
- Not suitable for crowded or highly dynamic RF spaces

---

## Ethical Note

This project focuses on **channel behavior**, not individuals.
No identifying information is collected or inferred.

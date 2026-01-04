# Bluetooth Physical Presence Sensing (Passive)

This project explores passive physical presence and motion sensing
using Bluetooth Low Energy (BLE) RSSI statistics on a single laptop.

## Motivation
The goal is NOT to locate devices or people,
but to infer physical environment state changes
through wireless channel behavior.

## What this project does
- Detects environment stability changes
- Distinguishes between:
  - empty space
  - static obstruction
  - motion-induced disturbance

## What this project does NOT do
- No localization
- No identification
- No imaging

## Core idea
We observe:
- RSSI mean → long-term absorption / obstruction
- RSSI variance → short-term channel instability

## Status
Prototype / research exploration

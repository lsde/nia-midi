#!/bin/bash
cd $(dirname "$0")
while true; do
    xvfb-run venv/bin/python3 nia-midi.py
done

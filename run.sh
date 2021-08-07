#!/bin/bash
cd /home/pi/wohnung
/home/pi/wohnung/venv/bin/python3 /home/pi/wohnung/run.py >> /home/pi/wohnung/dataset/log.log 2>&1

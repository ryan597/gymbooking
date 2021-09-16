#!/bin/bash

# Suspend to save state to the disk, wake at local time
echo "PASSWORD" | sudo -S rtcwake -m disk -l -t $(date +%s -d `tomorrow 06:15`)

conda activate gymbooking
python main.py
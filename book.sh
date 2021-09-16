#!/bin/bash

# Suspend to save state to the disk, wake at local time
cat secrets/password.txt | sudo --stdin rtcwake -m disk -l -t $(date +%s -d `tomorrow 06:15`)

conda activate gymbooking
python main.py

sudo rtcwake -m disk -t 30
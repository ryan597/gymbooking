#!/bin/bash

# Suspend to save state to the disk, wake at local time
cat secrets/password.txt | sudo --stdin rtcwake -m mem -l -t $(date +%s --date 'tomorrow 06:15')

conda activate gymbooking
python main.py > logging.txt 2>&1 # log any errors for debugging

cat logging.txt
shutdown
#!/bin/bash

# Suspend to save state to the disk, wake at local time
cat secrets/password.txt | sudo --stdin rtcwake -m disk -l -t $(date +%s --date 'tomorrow 06:15')

conda activate gymbooking
python main.py > errorlog.txt 2>&1 # log any errors for debugging

#shutdown
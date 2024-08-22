#!/bin/bash
# Can run this at startup by running this script in the rc.local file: https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/
source /home/eriksorensen/Github/SmartBeehive/pi_files/venv/bin/activate
nohup python /home/eriksorensen/Github/SmartBeehive/pi_files/datastream/bigquery_data_write_api/stream_bme280.py & > /dev/null 2>&1
#!/bin/bash
cd /home/pi/py-stn
python3 udp.py&
sleep 2
python3  control.py&
sleep 30
python3 mqtt-spider.py&
sleep 2
python3 mqtt-rbn-cw.py&
sleep 2
python3 mqtt-rbn-mgm.py&
sleep 2
./ip.sh
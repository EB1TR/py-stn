#!/bin/bash
cd /home/pi/venv
source bin/activate
cd /home/pi
./ip.sh&
sleep 5
./udp.sh&
sleep 5
./control.sh&
sleep 5
./spider.sh&
sleep 5
./rbncw.sh&
sleep 5
./rbnmgm.sh&

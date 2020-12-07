#!/bin/bash
cd /home/pi/py-stn/scripts
./udp.sh&
sleep 2
./control.sh&
sleep 30
./spider.sh&
sleep 2
./rbncw.sh&
sleep 2
./rbnmgm.sh&
sleep 2
./ip.sh
#!/bin/bash
cd /home/pi/py-stn/scripts
sudo kill -9 $(ps aux | grep '[p]ython3' | awk '{print $2}')
sleep 1
cp /home/pi/py-stn/config.json /home/pi/
cd /home/pi
rm -rf py-stn
git clone https://github.com/EB1TR/py-stn.git
cd /home/pi/py-stn/scripts
chmod +x *.sh
cd /home/pi
cp config.json py-stn/
sudo reboot
sudo apt update && \
sudo apt install -y nginx mosquitto git python3 python3-distutils python3-gpiozero && \
git clone https://github.com/EB1TR/docker-mqtt-ws.git && \
git clone https://github.com/EB1TR/py-stn.git && \
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
sudo python3 get-pip.py && \
sudo python3 -m pip install --upgrade pip && \
sudo pip3 install virtualenv gpiozero && \
sudo cat /home/pi/py-stn/conf-files/mosquitto.conf > /etc/mosquitto/mosquitto.conf && \
virtualenv /home/pi/venv && \
sudo chmod +x /home/pi/pyt-stn/scripts/*.sh && \
sudo reboot

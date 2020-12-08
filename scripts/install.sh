sudo su && \
apt update && \
apt upgrade && \
apt install -y nginx mosquitto git python3 python3-distutils python3-gpiozero gcc libffi-dev libssl-dev python3-dev && \
git clone https://github.com/EB1TR/py-stn.git && \
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
python3 get-pip.py && \
python3 -m pip install --upgrade pip && \
cat /home/pi/py-stn/conf-files/mosquitto.conf > /etc/mosquitto/mosquitto.conf && \
chown -R pi:pi /home/pi && \
cd /home/pi/py-stn/scripts && \
chmod +x *.sh && \
cat /home/pi/py-stn/conf-files/rc.local > /etc/rc.local && \
sed -i 's#/var/www/html#/home/pi/py-stn/static#g' /etc/nginx/sites-enabled/default && \
pip install -r /home/pi/py-stn/requirements.txt && \
pip install gpiozero adafruit-circuitpython-mcp230xx && \
reboot


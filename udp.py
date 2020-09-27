""" Six Pack & Filter Control - UDP to MQTTn"""
#
# Six Pack & Filter Control
#

# pylint: disable=invalid-name;
# pylint: disable=too-few-public-methods;
# pylint: disable=C0301, R0912, R0914, R0915, R1702, W0703

__author__ = 'EB1TR'
__date__ = "12/09/2020"

import settings
import paho.mqtt.client as mqtt
import socket
import xmltodict

try:
    MQTT_HOST = settings.Config.MQTT_HOST
    MQTT_PORT = settings.Config.MQTT_PORT
    STN1 = settings.Config.STN1
    STN2 = settings.Config.STN2
    pass
except Exception as e:
    print('Unexpected: %s' % e)
    exit(1)


def mqtt_connect():
    mqtt_client = mqtt.Client(transport='tcp')
    mqtt_client.connect(MQTT_HOST, MQTT_PORT, 600)
    return mqtt_client


def define_band(qrg):
    if qrg in range(180000, 200000):
        band = 160
    elif qrg in range(350000, 400000):
        band = 80
    elif qrg in range(700000, 720000):
        band = 40
    elif qrg in range(1400000, 1435000):
        band = 20
    elif qrg in range(2100000, 2145000):
        band = 15
    elif qrg in range(2800000, 2970000):
        band = 10
    else:
        band = 0
    return band


def do_udp():
    global STN1
    global STN2
    mqtt_client = mqtt_connect()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 12060))
    while True:
        data, addr = sock.recvfrom(1024)
        data = data.decode('utf-8')
        doc = xmltodict.parse(data)
        if doc["RadioInfo"]['StationName'] == STN1:
            stn = 1
        if doc["RadioInfo"]['StationName'] == STN2:
            stn = 2

        qrg = int(doc["RadioInfo"]['Freq'])
        radio = int(doc["RadioInfo"]['RadioNr'])
        mode = str(doc["RadioInfo"]['Mode'])
        op = str(doc["RadioInfo"]['OpCall'])
        op = op.upper()

        band = define_band(qrg)
        print("STN: " + str(stn) +
              " | Radio: " + str(radio) +
              " | QRG: " + str(qrg/100) +
              " | Mode:" + str(mode) +
              " | OP: " + str(op)
              )

        try:
            if stn == 1:
                if radio == 1:
                    mqtt_client.publish("stn1/radio1/qrg", qrg)
                    mqtt_client.publish("stn1/radio1/band", band)
                    mqtt_client.publish("stn1/radio1/mode", mode)
                    mqtt_client.publish("stn1/radio1/op", op)
                if radio == 2:
                    mqtt_client.publish("stn1/radio2/qrg", qrg)
                    mqtt_client.publish("stn1/radio2/band", band)
                    mqtt_client.publish("stn1/radio2/mode", mode)
                    mqtt_client.publish("stn1/radio2/op", op)
            if stn == 2:
                if radio == 1:
                    mqtt_client.publish("stn2/radio1/qrg", qrg)
                    mqtt_client.publish("stn2/radio1/band", band)
                    mqtt_client.publish("stn2/radio1/mode", mode)
                    mqtt_client.publish("stn2/radio1/op", op)
                if radio == 2:
                    mqtt_client.publish("stn2/radio2/qrg", qrg)
                    mqtt_client.publish("stn2/radio2/band", band)
                    mqtt_client.publish("stn2/radio2/mode", mode)
                    mqtt_client.publish("stn2/radio2/op", op)
        except:
            print("MQTT problem")


if __name__ == '__main__':
    do_udp()

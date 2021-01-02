""" Six Pack & Filter Control - UDP to MQTTn"""
#
# Six Pack & Filter Control
#

# pylint: disable=invalid-name;
# pylint: disable=too-few-public-methods;
# pylint: disable=C0301, R0912, R0914, R0915, R1702, W0703

__author__ = 'EB1TR'
__date__ = "12/09/2020"

import socket
import paho.mqtt.client as mqtt
import xmltodict
import json
import os
import sys
print("Configurando UDP")
try:
    with open('config.json') as json_file:
        data = json.load(json_file)
        CONFIG = dict(data)
        print("Datos de configuracion cargados desde fichero...")
except:
    if os.path.exists('cfg/stacks.json'):
        os.remove('cfg/stacks.json')
        print("Fallo en la carga de fichero de configuracion...")

MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883

STN1 = CONFIG['netbios-stn1']
STN2 = CONFIG['netbios-stn2']

def mqtt_connect():
    mqtt_c = mqtt.Client(transport='tcp')
    mqtt_c.connect(MQTT_HOST, MQTT_PORT, 600)
    return mqtt_c


def define_band(qrg):
    if qrg in range(175000, 205000):
        band = 160
    elif qrg in range(345000, 405000):
        band = 80
    elif qrg in range(525000, 545000):
        band = 60
    elif qrg in range(695000, 730000):
        band = 40
    elif qrg in range(1005000, 1020000):
        band = 30
    elif qrg in range(1395000, 1440000):
        band = 20
    elif qrg in range(1805000, 1820000):
        band = 17
    elif qrg in range(2095000, 2150000):
        band = 15
    elif qrg in range(2485000, 2500000):
        band = 12
    elif qrg in range(2795000, 3000000):
        band = 10
    elif qrg in range(4995000, 5050000):
        band = 6
    else:
        band = 0
    return band


def publish_data(mqtt_c, radio_i):
    if radio_i[0] == 1:
        if radio_i[1] == 1:
            mqtt_c.publish("stn1/radio1/qrg", radio_i[3])
            mqtt_c.publish("stn1/radio1/band", radio_i[2])
            mqtt_c.publish("stn1/radio1/mode", radio_i[4])
            mqtt_c.publish("stn1/radio1/op", radio_i[5])
        if radio_i[1] == 2:
            mqtt_c.publish("stn2/radio1/qrg", radio_i[3])
            mqtt_c.publish("stn2/radio1/band", radio_i[2])
            mqtt_c.publish("stn2/radio1/mode", radio_i[4])
            mqtt_c.publish("stn2/radio1/op", radio_i[5])
    if radio_i[0] == 2:
        if radio_i[1] == 1:
            mqtt_c.publish("stn2/radio1/qrg", radio_i[3])
            mqtt_c.publish("stn2/radio1/band", radio_i[2])
            mqtt_c.publish("stn2/radio1/mode", radio_i[4])
            mqtt_c.publish("stn2/radio1/op", radio_i[5])
        if radio_i[1] == 2:
            mqtt_c.publish("stn1/radio1/qrg", radio_i[3])
            mqtt_c.publish("stn1/radio1/band", radio_i[2])
            mqtt_c.publish("stn1/radio1/mode", radio_i[4])
            mqtt_c.publish("stn1/radio1/op", radio_i[5])


def process_xml(xml_data):
    data = []
    data.append(0)
    data.append(int(xml_data["RadioInfo"]['RadioNr']))
    data.append(define_band(int(xml_data["RadioInfo"]['Freq'])))
    data.append(int(xml_data["RadioInfo"]['Freq']))
    data.append(str(xml_data["RadioInfo"]['Mode']))
    data.append(str(xml_data["RadioInfo"]['OpCall']).upper())
    if xml_data["RadioInfo"]['StationName'] == STN1:
        data[0] = 1
    if xml_data["RadioInfo"]['StationName'] == STN2:
        data[0] = 2
    print("UDP " + str(data))
    return data


def do_udp():
    try:
        print("UDP a la escucha para %s y %s en puerto 12060" % (STN1, STN2))
        mqtt_c = mqtt_connect()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", 12060))
        while True:
            data = sock.recvfrom(1024)
            data = data.decode('utf-8')
            data = xmltodict.parse(data)
            data = process_xml(data)
            publish_data(mqtt_c, data)
    except KeyboardInterrupt:
        print('\n** User exited.')
        mqtt_c.disconnect()
        sys.exit(0)
    except Exception as e:
        print('ERR: %s' % str(e))


if __name__ == '__main__':
    do_udp()


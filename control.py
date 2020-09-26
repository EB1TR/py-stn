""" Six Pack & Filter Control """
#
# Six Pack & Filter Control
#

# pylint: disable=invalid-name;
# pylint: disable=too-few-public-methods;
# pylint: disable=C0301, R0912, R0914, R0915, R1702, W0703

__author__ = 'EB1TR'
__date__ = "12/09/2020"

import settings
import json
import paho.mqtt.client as mqtt
from gpiozero import LED

try:
    MQTT = settings.Config.MQTT
    MQTT_HOST = settings.Config.MQTT_HOST
    MQTT_PORT = settings.Config.MQTT_PORT
    pass
except Exception as e:
    print('Unexpected: %s' % e)
    exit(1)

STN1 = {
    'auto': True,
    'ant': 0,
    'antname': "--",
    'fil': 0,
    'bpf': True
}

STN2 = {
    'auto': True,
    'ant': 0,
    'antname': "--",
    'fil': 0,
    'bpf': True
}

OUTS = {
    0: "N",
    1: "N",
    2: "N",
    3: "N",
    4: "N",
    5: "N",
    6: "N"
}

FIL = {
    10: 6,
    15: 5,
    20: 4,
    40: 3,
    80: 2,
    160: 1
}

ANT = {
    6: "MomoBeam MB-6",
    5: "MomoBeam MB-7",
    4: "ND",
    3: "Dipolo 40",
    2: "Dipolo 80",
    1: "Dipolo 160",
    0: "Sin antena"
}

SP = {
    10: [5, 6],
    15: [6, 5],
    20: [5, 6],
    40: [3],
    80: [2],
    160: [1]
}

gpio_pin1 = LED(1)
gpio_pin2 = LED(2)
gpio_pin3 = LED(3)
gpio_pin4 = LED(4)
gpio_pin5 = LED(5)
gpio_pin6 = LED(6)
gpio_pin7 = LED(7)
gpio_pin8 = LED(8)
gpio_pin9 = LED(9)
gpio_pin10 = LED(10)
gpio_pin11 = LED(11)
gpio_pin12 = LED(12)
gpio_pin13 = LED(13)
gpio_pin14 = LED(14)
gpio_pin15 = LED(15)
gpio_pin16 = LED(16)
gpio_pin17 = LED(17)
gpio_pin18 = LED(18)
gpio_pin19 = LED(19)
gpio_pin20 = LED(20)
gpio_pin21 = LED(21)
gpio_pin22 = LED(22)
gpio_pin23 = LED(23)
gpio_pin24 = LED(24)

SO2R = "0"


def activate_ant_gpio(stn, old, new):
    if stn == 1:
        gpio_pin1.off()
        gpio_pin2.off()
        gpio_pin3.off()
        gpio_pin4.off()
        gpio_pin5.off()
        gpio_pin6.off()
        if not new == 0:
            if new == 1: gpio_pin1.on()
            if new == 2: gpio_pin2.on()
            if new == 3: gpio_pin3.on()
            if new == 4: gpio_pin4.on()
            if new == 5: gpio_pin5.on()
            if new == 6: gpio_pin6.on()
    if stn == 2:
        gpio_pin7.off()
        gpio_pin8.off()
        gpio_pin9.off()
        gpio_pin10.off()
        gpio_pin11.off()
        gpio_pin12.off()
        if not new == 0:
            if new == 1: gpio_pin7.on()
            if new == 2: gpio_pin8.on()
            if new == 3: gpio_pin9.on()
            if new == 4: gpio_pin10.on()
            if new == 5: gpio_pin11.on()
            if new == 6: gpio_pin12.on()


def activate_fil_gpio(stn, old, new):
    if stn == 1:
        gpio_pin13.off()
        gpio_pin14.off()
        gpio_pin15.off()
        gpio_pin16.off()
        gpio_pin17.off()
        gpio_pin18.off()
        if not new == 0:
            if new == 1: gpio_pin13.on()
            if new == 2: gpio_pin14.on()
            if new == 3: gpio_pin15.on()
            if new == 4: gpio_pin16.on()
            if new == 5: gpio_pin17.on()
            if new == 6: gpio_pin18.on()
    if stn == 2:
        gpio_pin19.off()
        gpio_pin20.off()
        gpio_pin21.off()
        gpio_pin22.off()
        gpio_pin23.off()
        gpio_pin24.off()
        if not new == 0:
            if new == 1: gpio_pin19.on()
            if new == 2: gpio_pin20.on()
            if new == 3: gpio_pin21.on()
            if new == 4: gpio_pin22.on()
            if new == 5: gpio_pin23.on()
            if new == 6: gpio_pin24.on()


def assign_stn1(band):
    global STN1
    global OUTS
    global SP
    if band != STN1['band']:
        if band in SP:
            for e in SP[band]:
                if OUTS[e] == "N":
                    activate_ant_gpio(1, STN1['ant'], e)
                    OUTS[e] = "1"
                    OUTS[STN1['ant']] = "N"
                    STN1['ant'] = e
                    STN1['antname'] = ANT[e]
                    break
                elif OUTS[e] == 1:
                    break
                else:
                    pass
        else:
            OUTS[STN1['ant']] = "N"
            STN1['ant'] = 0

        if STN1['bpf']:
            assign_filter_stn1(band)


def assign_stn2(band):
    global STN2
    global OUTS
    global SP
    if band != STN2[band]:
        if band in SP:
            for e in SP[band]:
                if OUTS[e] == "N":
                    activate_ant_gpio(2, STN2['ant'], e)
                    OUTS[e] = "2"
                    OUTS[STN2['ant']] = "N"
                    STN2['ant'] = e
                    STN2['antname'] = ANT[e]
                    break
                elif OUTS[e] == 2:
                    break
                else:
                    pass
        else:
            OUTS[STN2['ant']] = "N"
            STN2['ant'] = 0

        if STN2['bpf']:
            assign_filter_stn2(band)


def assign_filter_stn1(band):
    global STN1
    global FIL
    if band != 99:
        activate_fil_gpio(1, STN1['fil'], FIL[band])
        STN1['fil'] = FIL[band]
    else:
        activate_fil_gpio(1, STN1['fil'], FIL[band])
        STN1['fil'] = 0


def assign_filter_stn2(band):
    global STN2
    global FIL
    if band != 99:
        activate_fil_gpio(2, STN2['fil'], FIL[band])
        STN2['fil'] = FIL[band]
    else:
        activate_fil_gpio(2, STN2['fil'], FIL[band])
        STN2['fil'] = 0


def status():
    data_json = json.dumps(
        {
            'so2r': SO2R,
            'stn1': STN1,
            'stn2': STN2
        }, sort_keys=False
    )
    print(data_json)
    #  MQTT broker -------------------------------------------------------------------------------------
    #
    mqtt_client.publish("pytofront", data_json)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe([
        ("stn1/radio1/banda", 0),
        ("stn1/radio2/banda", 0),
        ("stn2/radio1/banda", 0),
        ("stn2/radio2/banda", 0),
        ("set/stn1/ant", 0),
        ("set/stn1/fil", 0),
        ("set/stn2/ant", 0),
        ("set/stn2/fil", 0),
        ("set/stn1/antm", 0),
        ("set/stn1/film", 0),
        ("set/stn2/antm", 0),
        ("set/stn2/film", 0),
        ("set/stn1/so2r", 0),
        ("set/stn2/so2r", 0),
        ("refrescar", 0)

    ])


def on_message(client, userdata, msg):
    global STN1
    global STN2
    global OUTS
    global FIL
    global SP
    global SO2R

    dato = msg.payload.decode('utf-8')

    if msg.topic == "stn1/radio1/banda":
        if SO2R == "2":
            pass
        else:
            if STN1['auto']:
                assign_stn1(int(dato))

    if msg.topic == "stn1/radio2/banda":
        if SO2R in ["2", "0"]:
            pass
        else:
            if STN2['auto']:
                assign_stn2(int(dato))

    if msg.topic == "stn2/radio1/banda":
        if SO2R == "1":
            pass
        elif SO2R == "0":
            if STN2['auto']:
                assign_stn2(int(dato))
        else:
            if STN1['auto']:
                assign_stn1(int(dato))

    if msg.topic == "stn2/radio2/banda":
        if SO2R in ["1", "0"]:
            pass
        else:
            if STN2['auto']:
                assign_stn2(int(dato))

    if not STN1['auto'] and msg.topic == "set/stn1/ant":
        dato = int(dato)
        if OUTS[dato] == "N" or dato == 0:
            if not dato == 0:
                activate_ant_gpio(1, STN1['ant'], dato)
            OUTS[dato] = "1"
            OUTS[STN1['ant']] = "N"
            STN1['ant'] = dato
            STN1['antname'] = ANT[dato]
        else:
            pass

    if not STN2['auto'] and msg.topic == "set/stn2/ant":
        dato = int(dato)
        if OUTS[dato] == "N" or dato == 0:
            if not dato == 0:
                activate_ant_gpio(2, STN2['ant'], dato)
            OUTS[dato] = "2"
            OUTS[STN2['ant']] = "N"
            STN2['ant'] = dato
            STN2['antname'] = ANT[dato]
        else:
            pass

    if not STN1['bpf'] and msg.topic == "set/stn1/fil":
        dato = int(dato)
        activate_fil_gpio(1, STN1['fil'], dato)
        STN1['fil'] = dato

    if not STN2['bpf'] and msg.topic == "set/stn2/fil":
        dato = int(dato)
        activate_fil_gpio(2, STN2['fil'], dato)
        STN2['fil'] = dato

    if msg.topic == "set/stn1/film":
        if STN1['bpf']:
            STN1['bpf'] = False
            SO2R = "0"
        else:
            STN1['bpf'] = True

    if msg.topic == "set/stn2/film":
        if STN2['bpf']:
            STN2['bpf'] = False
            SO2R = "0"
        else:
            STN2['bpf'] = True

    if msg.topic == "set/stn1/antm":
        if STN1['auto']:
            STN1['auto'] = False
            SO2R = "0"
        else:
            STN1['auto'] = True

    if msg.topic == "set/stn2/antm":
        if STN2['auto']:
            STN2['auto'] = False
            SO2R = "0"
        else:
            STN2['auto'] = True

    if msg.topic == "set/stn1/so2r":
        if SO2R == "1":
            SO2R = "0"
        else:
            SO2R = "1"
            STN1['auto'] = True
            STN1['bpf'] = True
            STN2['auto'] = True
            STN2['bpf'] = True

    if msg.topic == "set/stn2/so2r":
        if SO2R == "2":
            SO2R = "0"
        else:
            SO2R = "2"
            STN1['auto'] = True
            STN1['bpf'] = True
            STN2['auto'] = True
            STN2['bpf'] = True

    status()


mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 600)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.loop_forever()

""" Six Pack & Filter Control """
#
# Six Pack & Filter Control
#

# pylint: disable=invalid-name;
# pylint: disable=too-few-public-methods;
# pylint: disable=C0301, R0912, R0914, R0915, R1702, W0703

__author__ = 'EB1TR'
__date__ = "12/09/2020"

import json
import paho.mqtt.client as mqtt
from gpiozero import LED

MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883

STN1 = {
    'auto': True,
    'ant': 0,
    'antname': "--",
    'fil': 0,
    'bpf': True,
    'band': 0
}

STN2 = {
    'auto': True,
    'ant': 0,
    'antname': "--",
    'fil': 0,
    'bpf': True,
    'band': 0
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
    0: 0,
    10: 6,
    15: 5,
    20: 4,
    40: 3,
    80: 2,
    160: 1
}

ANT = {
    6: "MB6",
    5: "MB7",
    4: "ND",
    3: "ROT",
    2: "DIP",
    1: "DIP",
    0: "N/A"
}

SP = {
    10: [5, 6],
    15: [6, 5],
    20: [5, 6],
    40: [3],
    80: [2],
    160: [1],
    0: [0]
}
# GPIOs al SixPack A
gpio_pin1 = LED(2)
gpio_pin2 = LED(3)
gpio_pin3 = LED(4)
gpio_pin4 = LED(17)
gpio_pin5 = LED(27)
gpio_pin6 = LED(22)
# GPIOs al SixPack B
gpio_pin7 = LED(10)
gpio_pin8 = LED(9)
gpio_pin9 = LED(11)
gpio_pin10 = LED(5)
gpio_pin11 = LED(6)
gpio_pin12 = LED(13)
# GPIOs a Filtros A
gpio_pin13 = LED(14)
gpio_pin14 = LED(15)
gpio_pin15 = LED(18)
gpio_pin16 = LED(23)
gpio_pin17 = LED(24)
gpio_pin18 = LED(25)
# GPIOs a Filtros B
gpio_pin19 = LED(8)
gpio_pin20 = LED(7)
gpio_pin21 = LED(12)
gpio_pin22 = LED(16)
gpio_pin23 = LED(20)
gpio_pin24 = LED(21)


def activate_ant_gpio(stn, new):
    if stn == 1:
        gpio_pin1.off()
        gpio_pin2.off()
        gpio_pin3.off()
        gpio_pin4.off()
        gpio_pin5.off()
        gpio_pin6.off()
        if new == 1:
            gpio_pin1.on()
        if new == 2:
            gpio_pin2.on()
        if new == 3:
            gpio_pin3.on()
        if new == 4:
            gpio_pin4.on()
        if new == 5:
            gpio_pin5.on()
        if new == 6:
            gpio_pin6.on()
    if stn == 2:
        gpio_pin7.off()
        gpio_pin8.off()
        gpio_pin9.off()
        gpio_pin10.off()
        gpio_pin11.off()
        gpio_pin12.off()
        if new == 1:
            gpio_pin7.on()
        if new == 2:
            gpio_pin8.on()
        if new == 3:
            gpio_pin9.on()
        if new == 4:
            gpio_pin10.on()
        if new == 5:
            gpio_pin11.on()
        if new == 6:
            gpio_pin12.on()


def activate_fil_gpio(stn, new):
    if stn == 1:
        gpio_pin13.off()
        gpio_pin14.off()
        gpio_pin15.off()
        gpio_pin16.off()
        gpio_pin17.off()
        gpio_pin18.off()
        if new == 1:
            gpio_pin13.on()
        if new == 2:
            gpio_pin14.on()
        if new == 3:
            gpio_pin15.on()
        if new == 4:
            gpio_pin16.on()
        if new == 5:
            gpio_pin17.on()
        if new == 6:
            gpio_pin18.on()
    if stn == 2:
        gpio_pin19.off()
        gpio_pin20.off()
        gpio_pin21.off()
        gpio_pin22.off()
        gpio_pin23.off()
        gpio_pin24.off()
        if new == 1:
            gpio_pin19.on()
        if new == 2:
            gpio_pin20.on()
        if new == 3:
            gpio_pin21.on()
        if new == 4:
            gpio_pin22.on()
        if new == 5:
            gpio_pin23.on()
        if new == 6:
            gpio_pin24.on()


def swap(stn):
    global STN1
    global STN2
    global OUTS
    global SP

    stn1_pre_swap = STN1['ant']
    stn2_pre_swap = STN2['ant']

    if STN1['ant'] in SP[STN2['band']] and STN2['ant'] in SP[STN1['band']]:
        STN1['ant'] = stn2_pre_swap
        activate_ant_gpio(1, stn2_pre_swap)
        OUTS[stn2_pre_swap] = "1"
        STN2['ant'] = stn1_pre_swap
        OUTS[stn1_pre_swap] = "2"
        activate_ant_gpio(2, stn1_pre_swap)

    elif int(stn) == 1 and len(SP[STN1['band']]) == 2 and int(STN2['ant']) not in SP[STN1['band']]:
        if STN1['ant'] == SP[STN1['band']][0]:
            STN1['ant'] = SP[STN1['band']][1]
            OUTS[SP[STN1['band']][0]] = "N"
            OUTS[SP[STN1['band']][1]] = "1"
            activate_ant_gpio(stn, SP[STN1['band']][1])
        elif STN1['ant'] == SP[STN1['band']][1]:
            STN1['ant'] = SP[STN1['band']][0]
            OUTS[SP[STN1['band']][1]] = "N"
            OUTS[SP[STN1['band']][0]] = "1"
            activate_ant_gpio(stn, SP[STN1['band']][0])

    elif int(stn) == 2 and len(SP[STN2['band']]) == 2 and int(STN1['ant']) not in SP[STN2['band']]:
        if STN2['ant'] == SP[STN2['band']][0]:
            STN2['ant'] = SP[STN2['band']][1]
            OUTS[SP[STN2['band']][0]] = "N"
            OUTS[SP[STN2['band']][1]] = "2"
            activate_ant_gpio(stn, SP[STN2['band']][1])
        elif STN2['ant'] == SP[STN2['band']][1]:
            STN2['ant'] = SP[STN2['band']][0]
            OUTS[SP[STN2['band']][1]] = "N"
            OUTS[SP[STN2['band']][0]] = "2"
            activate_ant_gpio(stn, SP[STN2['band']][0])


def assign_stn(stn, band):
    global STN1
    global STN2
    global OUTS
    global SP
    if stn == 1:
        STNX = STN1
        STNY = STN2
    if stn == 2:
        STNX = STN2
        STNY = STN1
    if band in SP and band != STNY['band']:
        if not STNX['ant'] in SP[band] or STNX['band'] != band:
            for e in SP[band]:
                if OUTS[e] == "N":
                    if STNX['band'] != band:
                        activate_ant_gpio(stn, e)
                    OUTS[e] = str(stn)
                    OUTS[STNX['ant']] = "N"
                    STNX['ant'] = e
                    STNX['antname'] = ANT[e]
                    STNX['band'] = band
                    break
                elif OUTS[e] == str(stn):
                    STNX['band'] = band
                    break
    else:
        activate_ant_gpio(stn, 0)
        OUTS[STNX['ant']] = "N"
        STNX['ant'] = 0
        STNX['antname'] = "--"
        STNX['band'] = 0

    if stn == 1:
        STN1 = STNX
    if stn == 2:
        STN2 = STNX


def assign_filter(stn, band):
    global STN1
    global STN2
    global FIL
    if stn == 1:
        STNX = STN1
    if stn == 2:
        STNX = STN2
    if band in FIL:
        if STNX['fil'] != FIL[band]:
            activate_fil_gpio(stn, FIL[band])
            STNX['fil'] = FIL[band]
    else:
        activate_fil_gpio(stn, FIL[band])
        STNX['fil'] = 0
    if stn == 1:
        STN1 = STNX
    if stn == 2:
        STN2 = STNX


def status():
    data_json = json.dumps(
        {
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
        ("stn1/radio1/band", 0),
        ("stn2/radio1/band", 0),
        ("set/stn1/ant", 0),
        ("set/stn1/fil", 0),
        ("set/stn2/ant", 0),
        ("set/stn2/fil", 0),
        ("set/stn1/antm", 0),
        ("set/stn2/antm", 0),
        ("set/stn1/film", 0),
        ("set/stn2/film", 0),
        ("set/stn1/band", 0),
        ("set/stn2/band", 0),
        ("set/stn1/swap", 0),
        ("set/stn2/swap", 0),
        ("update", 0)
    ])


def on_message(client, userdata, msg):
    global STN1
    global STN2
    global OUTS
    global FIL
    global SP

    dato = msg.payload.decode('utf-8')

    try:
        dato = int(dato)
    except:
        pass

    if msg.topic == "stn1/radio1/band":
        if STN1['auto']:
            assign_stn(1, dato)
        if STN1['bpf']:
            assign_filter(1, dato)

    if msg.topic == "stn2/radio1/band":
        if STN2['auto']:
            assign_stn(2, dato)
        if STN2['bpf']:
            assign_filter(2, dato)

    if not STN1['auto'] and msg.topic == "set/stn1/ant":
        if OUTS[dato] == "N" or dato == 0:
            activate_ant_gpio(1, dato)
            OUTS[dato] = "1"
            OUTS[STN1['ant']] = "N"
            STN1['ant'] = dato
            STN1['antname'] = ANT[dato]
            STN1['band'] = 0

    if not STN2['auto'] and msg.topic == "set/stn2/ant":
        if OUTS[dato] == "N" or dato == 0:
            activate_ant_gpio(2, dato)
            OUTS[dato] = "2"
            OUTS[STN2['ant']] = "N"
            STN2['ant'] = dato
            STN2['antname'] = ANT[dato]
            STN2['band'] = 0

    if not STN1['auto'] and msg.topic == "set/stn1/band":
        assign_stn(1, dato)

    if not STN2['auto'] and msg.topic == "set/stn2/band":
        assign_stn(2, dato)

    if not STN1['bpf'] and msg.topic == "set/stn1/fil":
        assign_filter(1, dato)

    if not STN2['bpf'] and msg.topic == "set/stn2/fil":
        assign_filter(2, dato)

    if msg.topic == "set/stn1/antm":
        if STN1['auto']:
            STN1['auto'] = False
        else:
            STN1['auto'] = True

    if msg.topic == "set/stn2/antm":
        if STN2['auto']:
            STN2['auto'] = False
        else:
            STN2['auto'] = True

    if msg.topic == "set/stn1/film":
        if STN1['bpf']:
            STN1['bpf'] = False
        else:
            STN1['bpf'] = True

    if msg.topic == "set/stn2/film":
        if STN2['bpf']:
            STN2['bpf'] = False
        else:
            STN2['bpf'] = True

    if msg.topic == "set/stn1/swap":
        swap(1)

    if msg.topic == "set/stn2/swap":
        swap(2)

    status()


mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 600)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.loop_forever()

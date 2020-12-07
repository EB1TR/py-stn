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
import os

import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017

i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)



MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883

try:
    with open('config.json') as json_file:
        data = json.load(json_file)
        CONFIG = dict(data)
        print("Datos de configuración cargados desde fichero...")
except:
    if os.path.exists('cfg/stacks.json'):
        os.remove('cfg/stacks.json')
        print("Fallo en la carga de fichero de configuración...")

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
    6: CONFIG["nombre-antena6"],
    5: CONFIG["nombre-antena5"],
    4: CONFIG["nombre-antena4"],
    3: CONFIG["nombre-antena3"],
    2: CONFIG["nombre-antena2"],
    1: CONFIG["nombre-antena1"],
    0: "N/A"
}

ants10 = []
ants15 = []
ants20 = []
ants40 = []
ants80 = []
ants160 = []
for e in CONFIG["sp-10"]:
    ants10.append(e)
for e in CONFIG["sp-15"]:
    ants15.append(e)
for e in CONFIG["sp-20"]:
    ants20.append(e)
for e in CONFIG["sp-40"]:
    ants40.append(e)
for e in CONFIG["sp-80"]:
    ants80.append(e)
for e in CONFIG["sp-160"]:
    ants160.append(e)
SP = {
    10: ants10,
    15: ants15,
    20: ants20,
    40: ants40,
    80: ants80,
    160: ants160,
    0: [0]
}

# GPIOs al SixPack A
rpi_gpio1 = LED(4)
rpi_gpio2 = LED(17)
rpi_gpio3 = LED(27)
rpi_gpio4 = LED(22)
rpi_gpio5 = LED(10)
rpi_gpio6 = LED(9)
# GPIOs al SixPack B
rpi_gpio7 = LED(11)
rpi_gpio8 = LED(5)
rpi_gpio9 = LED(6)
rpi_gpio10 = LED(13)
rpi_gpio11 = LED(19)
rpi_gpio12 = LED(26)
# GPIOs a Filtros A
rpi_gpio13 = LED(14)
rpi_gpio14 = LED(15)
rpi_gpio15 = LED(18)
rpi_gpio16 = LED(23)
rpi_gpio17 = LED(24)
rpi_gpio18 = LED(25)
# GPIOs a Filtros B
rpi_gpio19 = LED(8)
rpi_gpio20 = LED(7)
rpi_gpio21 = LED(12)
rpi_gpio22 = LED(16)
rpi_gpio23 = LED(20)
rpi_gpio24 = LED(21)

# GPIOS expansion
ext_gpio0 = mcp.get_pin(0)
ext_gpio1 = mcp.get_pin(1)
ext_gpio2 = mcp.get_pin(2)
ext_gpio3 = mcp.get_pin(3)
ext_gpio4 = mcp.get_pin(4)
ext_gpio5 = mcp.get_pin(5)
ext_gpio6 = mcp.get_pin(6)
ext_gpio7 = mcp.get_pin(7)
ext_gpio8 = mcp.get_pin(8)
ext_gpio9 = mcp.get_pin(9)
ext_gpio10 = mcp.get_pin(10)
ext_gpio11 = mcp.get_pin(11)
ext_gpio12 = mcp.get_pin(12)
ext_gpio13 = mcp.get_pin(13)
ext_gpio14 = mcp.get_pin(14)
ext_gpio15 = mcp.get_pin(15)
ext_gpio0.switch_to_output(value=False)
ext_gpio1.switch_to_output(value=False)
ext_gpio2.switch_to_output(value=False)
ext_gpio3.switch_to_output(value=False)
ext_gpio4.switch_to_output(value=False)
ext_gpio5.switch_to_output(value=False)
ext_gpio6.switch_to_output(value=False)
ext_gpio7.switch_to_output(value=False)
ext_gpio8.switch_to_output(value=False)
ext_gpio9.switch_to_output(value=False)
ext_gpio10.switch_to_output(value=False)
ext_gpio11.switch_to_output(value=False)
ext_gpio12.switch_to_output(value=False)
ext_gpio13.switch_to_output(value=False)
ext_gpio14.switch_to_output(value=False)
ext_gpio15.switch_to_output(value=False)


def activate_ant_gpio(stn, new):
    if stn == 1:
        rpi_gpio1.off()
        rpi_gpio2.off()
        rpi_gpio3.off()
        rpi_gpio4.off()
        rpi_gpio5.off()
        rpi_gpio6.off()
        if new == 1:
            rpi_gpio1.on()
        if new == 2:
            rpi_gpio2.on()
        if new == 3:
            rpi_gpio3.on()
        if new == 4:
            rpi_gpio4.on()
        if new == 5:
            rpi_gpio5.on()
        if new == 6:
            rpi_gpio6.on()
    if stn == 2:
        rpi_gpio7.off()
        rpi_gpio8.off()
        rpi_gpio9.off()
        rpi_gpio10.off()
        rpi_gpio11.off()
        rpi_gpio12.off()
        if new == 1:
            rpi_gpio7.on()
        if new == 2:
            rpi_gpio8.on()
        if new == 3:
            rpi_gpio9.on()
        if new == 4:
            rpi_gpio10.on()
        if new == 5:
            rpi_gpio11.on()
        if new == 6:
            rpi_gpio12.on()


def activate_fil_gpio(stn, new):
    if stn == 1:
        rpi_gpio13.off()
        rpi_gpio14.off()
        rpi_gpio15.off()
        rpi_gpio16.off()
        rpi_gpio17.off()
        rpi_gpio18.off()
        if new == 1:
            rpi_gpio13.on()
        if new == 2:
            rpi_gpio14.on()
        if new == 3:
            rpi_gpio15.on()
        if new == 4:
            rpi_gpio16.on()
        if new == 5:
            rpi_gpio17.on()
        if new == 6:
            rpi_gpio18.on()
    if stn == 2:
        rpi_gpio19.off()
        rpi_gpio20.off()
        rpi_gpio21.off()
        rpi_gpio22.off()
        rpi_gpio23.off()
        rpi_gpio24.off()
        if new == 1:
            rpi_gpio19.on()
        if new == 2:
            rpi_gpio20.on()
        if new == 3:
            rpi_gpio21.on()
        if new == 4:
            rpi_gpio22.on()
        if new == 5:
            rpi_gpio23.on()
        if new == 6:
            rpi_gpio24.on()


def rpi(cmd):
    if cmd == "reboot":
        os.system('sudo shutdown -r now')
        print("Reiniciando")
    elif cmd == "shutdown":
        os.system('sudo shutdown -h now')
        print("Apagando")

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
            STNX['band'] = band
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
    print("CONTROL -> " + str(data_json))
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
        ("set/rpi", 0),
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
            assign_filter(1, 0)
        else:
            STN1['bpf'] = True

    if msg.topic == "set/stn2/film":
        if STN2['bpf']:
            STN2['bpf'] = False
            assign_filter(2, 0)
        else:
            STN2['bpf'] = True

    if msg.topic == "set/stn1/swap":
        swap(1)

    if msg.topic == "set/stn2/swap":
        swap(2)
    
    if msg.topic == "set/reboot":
        rebootpi()

    status()


mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 600)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.loop_forever()

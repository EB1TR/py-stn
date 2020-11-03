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
#from gpiozero import LED

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
    'band': 0
}

STN2 = {
    'auto': True,
    'ant': 0,
    'band': 0
}

OUTS = {
    0: "N",
    160: "N",
    80: "N",
    40: "N",
    20: "N",
    15: "N",
    10: "N"
}

STACKS = {
    0: {
        'salidas': 0,
        1: {
            'estado': False,
            'nombre': "N/A"
        },
        2: {
            'estado': False,
            'nombre': "N/A"
        },
        3: {
            'estado': False,
            'nombre': "N/A"
        }
    },
    160: {
        'salidas': 1,
        1: {
            'estado': True,
            'nombre': "DIP"
        },
        2: {
            'estado': False,
            'nombre': "N/A"
        },
        3: {
            'estado': False,
            'nombre': "N/A"
        }
    },
    80: {
        'salidas': 1,
        1: {
            'estado': True,
            'nombre': "DIP"
        },
        2: {
            'estado': False,
            'nombre': "N/A"
        },
        3: {
            'estado': False,
            'nombre': "N/A"
        }
    },
    40: {
        'salidas': 1,
        1: {
            'estado': True,
            'nombre': "ROT"
        },
        2: {
            'estado': False,
            'nombre': "N/A"
        },
        3: {
            'estado': False,
            'nombre': "N/A"
        }
    },
    20: {
        'salidas': 2,
        1: {
            'estado': True,
            'nombre': "MB6E"
        },
        2: {
            'estado': False,
            'nombre': "MB7N"
        },
        3: {
            'estado': False,
            'nombre': "N/A"
        }
    },
    15: {
        'salidas': 2,
        1: {
            'estado': True,
            'nombre': "MB6E"
        },
        2: {
            'estado': False,
            'nombre': "MB7N"
        },
        3: {
            'estado': False,
            'nombre': "N/A"
        }
    },
    10: {
        'salidas': 2,
        1: {
            'estado': True,
            'nombre': "MB6E"
        },
        2: {
            'estado': False,
            'nombre': "MB7N"
        },
        3: {
            'estado': False,
            'nombre': "N/A"
        }
    }
}


def assign_stn(stn, band):
    global STN1
    global STN2
    global OUTS
    if stn == 1:
        STNX = STN1
        STNY = STN2
    if stn == 2:
        STNX = STN2
        STNY = STN1
    if band != STNY['band']:
        if OUTS[band] == "N":
            #activate_ant_gpio(stn, band)
            OUTS[band] = str(stn)
            OUTS[STNX['ant']] = "N"
            STNX['ant'] = band
            STNX['band'] = band
    else:
        #activate_ant_gpio(stn, 0)
        OUTS[int(STNX['ant'])] = "N"
        STNX['ant'] = 0
        STNX['band'] = 0

    if stn == 1:
        STN1 = STNX
    if stn == 2:
        STN2 = STNX


def status():
    data_json = json.dumps(
        {
            'stn1': STN1,
            'stn2': STN2,
            'stacks': STACKS
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
        ("set/stn1/antm", 0),
        ("set/stn2/antm", 0),
        ("set/stn1/band", 0),
        ("set/stn2/band", 0),
        ("set/stn1/stack", 0),
        ("set/stn2/stack", 0),
        ("update", 0)
    ])


def on_message(client, userdata, msg):
    global STN1
    global STN2

    dato = msg.payload.decode('utf-8')

    # Mensajes recibidos desde UDP

    if msg.topic == "stn1/radio1/band":
        if STN1['auto'] and STN1['band'] != int(dato):
            assign_stn(1, int(dato))

    if msg.topic == "stn1/radio2/band":
        if STN2['auto'] and STN2['band'] != int(dato):
            assign_stn(2, int(dato))

    # Mensajes recibidos desde FRONT

    if not STN1['auto'] and msg.topic == "set/stn1/band":
        dato = int(dato)
        assign_stn(1, dato)

    if not STN2['auto'] and msg.topic == "set/stn2/band":
        dato = int(dato)
        assign_stn(2, dato)

    if msg.topic == "set/stn1/antm":
        if STN1['auto']:
            STN1['auto'] = False
        else:
            STN1['auto'] = True
            assign_stn(1, 0)

    if msg.topic == "set/stn2/antm":
        if STN2['auto']:
            STN2['auto'] = False
        else:
            STN2['auto'] = True
            assign_stn(2, 0)

    if msg.topic == "set/stn1/stack" and int(STN1['band']) != 0:
        cc = 0
        if STACKS[int(STN1['band'])][1]['estado']: cc = cc + 1
        if STACKS[int(STN1['band'])][2]['estado']: cc = cc + 1
        if STACKS[int(STN1['band'])][3]['estado']: cc = cc + 1
        if STACKS[int(STN1['band'])][int(dato)]['estado'] and cc > 1:
            STACKS[int(STN1['band'])][int(dato)]['estado'] = False
        else:
            STACKS[int(STN1['band'])][int(dato)]['estado'] = True

    if msg.topic == "set/stn2/stack" and int(STN2['band']) != 0:
        cc = 0
        if STACKS[int(STN2['band'])][1]['estado']: cc = cc + 1
        if STACKS[int(STN2['band'])][2]['estado']: cc = cc + 1
        if STACKS[int(STN2['band'])][3]['estado']: cc = cc + 1
        if STACKS[int(STN2['band'])][int(dato)]['estado'] and cc > 1:
            STACKS[int(STN2['band'])][int(dato)]['estado'] = False
        else:
            STACKS[int(STN2['band'])][int(dato)]['estado'] = True

    status()


mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 600)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.loop_forever()

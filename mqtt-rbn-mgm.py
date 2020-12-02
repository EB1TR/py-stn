__author__ = 'EB1TR'

import sys
import json
import telnetlib
import time
from time import sleep
import paho.mqtt.client as mqtt
import frequency
import os
print("Configurando RBN MGM")
try:
    with open('config.json') as json_file:
        data = json.load(json_file)
        CONFIG = dict(data)
        print("Datos de configuración cargados desde fichero...")
except:
    if os.path.exists('cfg/stacks.json'):
        os.remove('cfg/stacks.json')
        print("Fallo en la carga de fichero de configuración...")

CALL = CONFIG['rbnmgm-call']
HOST = CONFIG['rbnmgm-host']
PORT = CONFIG['rbnmgm-port']
MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "spots/rbn/mgm"


def is_spot(data, mqtt_client):
    #comment = ""
    #for e in range(5, (len(data) - 1)):
    #    comment = comment + data[e] + " "
    #comment = comment[:-1]
    comment = data[5] + " " + data[6] + data[7] + " " + data[8]
    src = data[2].split("-")
    src = src[0]
    qrg = '%.1f' % float(data[3])
    qrg_info = frequency.qrgband(float(qrg))
    processed_data = json.dumps(
        {
            'tstamp': int(time.time()),
            'dx': data[4],
            'qrg': float(qrg),
            'band': qrg_info['band'],
            'src': src,
            'cmt': comment,
            'db': int(data[6])

        }, sort_keys=False
    )
    mqtt_client.publish(MQTT_TOPIC, str(processed_data))
    print(processed_data)


def do_telnet():
    try:
        print('+ Conectando a RBN MGM %s:%s' % (HOST, PORT))
        print('|-> Usando CALL: ' + CALL)
        t = telnetlib.Telnet(HOST, PORT, 10)
        # t.set_debuglevel(100)
    except Exception as e:
        print('|- No es posible conectar a RBN CW %s: %s' % HOST, e)
        return
    t.read_until(b'Please enter your call: ', 10)
    sleep(2)
    t.write(CALL.encode('ascii') + b"\r\n")
    mqtt_client = mqtt.Client(transport='tcp')
    try:
        print('+ Conectando con MQTT...')
        mqtt_client.connect(MQTT_HOST, MQTT_PORT, 600)
        print('|-> Conectado.')
    except Exception as e:
        print('\n** Cerrando conexión con MQTT por un error: %s' % e)
        sys.exit(1)
    while True:
        try:
            rawdata = t.read_until(b'\r\n').decode('ISO-8859-1')
            data = rawdata.split()
            if not data:
                pass
            else:
                if data[0] == 'DX':
                    try:
                        is_spot(data, mqtt_client)
                    except:
                        print("############### UNHANDLED ###############")
                        print(data)
                        print("#########################################")
        except KeyboardInterrupt:
            print('\n** User exited.')
            mqtt_client.disconnect()
            sys.exit(0)
        except EOFError:
            print('\n** Closing connection due to EOFError: %s' % EOFError)
            mqtt_client.disconnect()
            sys.exit(1)
        except OSError:
            print('\n** Closing connection due to OSError: %s' % OSError)
            mqtt_client.disconnect()
            sys.exit(1)
        except Exception as e:
            print('\n** Closing connection due to an exception: %s' % str(e))
            mqtt_client.disconnect()
            sys.exit()


if __name__ == '__main__':
    do_telnet()

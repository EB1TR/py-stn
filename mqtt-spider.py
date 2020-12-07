__author__ = 'EB1TR'

import sys
import json
import telnetlib
import time
import paho.mqtt.client as mqtt
import frequency
from time import sleep
import os
print("Configurando SPIDER")
try:
    with open('config.json') as json_file:
        data = json.load(json_file)
        CONFIG = dict(data)
        print("Datos de configuracion cargados desde fichero...")
except:
    if os.path.exists('cfg/stacks.json'):
        os.remove('cfg/stacks.json')
        print("Fallo en la carga de fichero de configuracion...")

try:
    CALL = CONFIG['spider-call']
    HOST = CONFIG['spider-host']
    PORT = CONFIG['spider-port']
    MQTT_HOST = "127.0.0.1"
    MQTT_PORT = 1883
    MQTT_TOPIC = "spots/spider/spots"
except Exception as e:
    print('Unexpected: %s' % e)
    exit(1)


def telnet_connect():
    try:
        print('+ Conectando a SPIDER %s:%s' % (HOST, PORT))
        print('|-> Usando CALL: ' + CALL)
        t = telnetlib.Telnet(HOST, PORT, 10)
    except Exception as e:
        print('|- No es posible conectar a SPIDER %s: %s' % HOST, e)
        return
    t.read_until(b'login: ', 10)
    print("Enviando CALL...")
    sleep(1)
    t.write(CALL.encode('ascii') + b'\n')
    print('Habilitando WCY...')
    sleep(1)
    t.write(b'set/wcy\n')
    sleep(1)
    t.write(b'clear/wcy\n')
    print('Deshabilitando WWV...')
    sleep(1)
    t.write(b'unset/wwv\n')
    print('Deshabilitando filtros...')
    sleep(1)
    t.write(b'clear/spots all\n')
    print('Deshabilitando beeps...')
    sleep(1)
    t.write(b'set/nobeep\n')
    print('Deshabilitando anuncios...')
    sleep(1)
    t.write(b'unset/announce\n')
    sleep(1)
    t.write(b'clear/ann all\n')
    print('Reject WX...')
    sleep(1)
    t.write(b'unset/wx\n')
    print('Deshabilitando talk...')
    sleep(1)
    t.write(b'unset/talk\n')
    print('Habilitando modo CC11...')
    sleep(1)
    t.write(b'set/ve7cc\n')
    print('Deshabilitando Skimmers...')
    sleep(1)
    t.write(b'unset/skimmer\n')
    print('Deshabilitando Estados USA...')
    sleep(1)
    t.write(b'unset/usstates\n')
    return t


def mqtt_connect():
    mqtt_client = mqtt.Client(transport='tcp')
    try:
        print('+ Conectando con MQTT...')
        mqtt_client.connect(MQTT_HOST, MQTT_PORT, 600)
        print('|-> Conectado.')
    except Exception as e:
        print('\n** Cerrando conexion con MQTT por un error: %s' % e)
        sys.exit(1)
    return mqtt_client


def is_wcy(data, mqtt_client):
    k = data[5][2:]
    ek = data[6][5:]
    a = data[7][2:]
    ssn = data[8][2:]
    sfi = data[9][4:]
    sa = data[10][3:]
    gmf = data[11][4:]
    au = data[12][3:]
    processed_data = json.dumps(
        {
            'tstamp': int(time.time()),
            'k': k,
            'ek': ek,
            'a': a,
            'ssn': ssn,
            'sfi': sfi,
            'sa': sa,
            'gmf': gmf,
            'au': au
        }, sort_keys=False

    )
    mqtt_client.publish('solar/wcy', str(processed_data))
    print("WCY " + str(processed_data))


def is_spot(data, mqtt_client):
    qrg = '%.1f' % float(data[1])
    qrg_info = frequency.qrgband(float(qrg))
    band = qrg_info['band']
    processed_data = json.dumps(
        {
            'tstamp': int(time.time()),
            'dx': data[2],
            'qrg': float(qrg),
            'band': band,
            'src': data[6],
            'cmt': data[5]
        }, sort_keys=False
    )
    mqtt_client.publish(MQTT_TOPIC, str(processed_data))
    print("SPR " + str(processed_data))


def do_telnet():
    t = telnet_connect()
    mqtt_client = mqtt_connect()
    while True:
        try:
            rawdata = t.read_until(b'\r\n').decode('ISO-8859-1')
            data = rawdata.split("^")
            if not data:
                pass
            else:
                if data[0] == 'CC11':
                    try:
                        is_spot(data, mqtt_client)
                    except:
                        print("############## NO MANEJADO ##############")
                        print(data)
                        print("#########################################")
                else:
                    data = rawdata.split()
                    if data[0] == 'WCY':
                        try:
                            is_wcy(data, mqtt_client)
                        except:
                            print("############## NO MANEJADO ##############")
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
            print('\n** Closing connection due to an exception: %s' % e)
            mqtt_client.disconnect()
            sys.exit()


if __name__ == '__main__':
    do_telnet()

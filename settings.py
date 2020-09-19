# -*- coding: utf-8 -*-
# pylint: disable=locally-disabled, multiple-statements
# pylint: disable=fixme, line-too-long, invalid-name
# pylint: disable=W0703

""" Six Pack & Filter Control """

__author__ = 'EB1TR'
__date__ = "12/09/2020"

import sys
from os import environ, path
from environs import Env


ENV_FILE = path.join(path.abspath(path.dirname(__file__)), '.env')

try:
    ENVIR = Env()
    ENVIR.read_env()
except Exception as e:
    print('Error: .env file not found: %s' % e)
    sys.exit(1)


class Config:
    """
    This is the generic loader that sets common attributes

    :param: "UNK"
    :return: "UNK"
    """
    if environ.get('MQTT'):
        MQTT = ENVIR('MQTT')

    if environ.get('MQTT_HOST'):
        MQTT_HOST = ENVIR('MQTT_HOST')

    if environ.get('MQTT_PORT'):
        MQTT_PORT = int(ENVIR('MQTT_PORT'))

    if environ.get('STN1'):
        STN1 = ENVIR('STN1')

    if environ.get('STN2'):
        STN2 = ENVIR('STN2')




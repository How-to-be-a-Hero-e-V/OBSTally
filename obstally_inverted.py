#!/usr/bin/env python
# -*- coding: utf-8 -*-

#################################
#  Tally Lights for OBS-Studio  #
#  Using OBS-Websockets         #
#   Rewritten Version           #
#  (c) 2023 Deniz K. HTBAH e.V. #
#################################

import time
import xml.etree.ElementTree as ET
import logging
import RPi.GPIO as GPIO
from gpiozero import LED
from obswebsocket import obsws, events, requests

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()

LOG_LEVEL = logging.INFO
logging.basicConfig(level=LOG_LEVEL)

XML_FILE = 'tally.xml'

GPIO_PINS = {
    'pv_tally_1': 17,
    'pgm_tally_1': 18,
    'pv_tally_2': 19,
    'pgm_tally_2': 20,
    'pv_tally_3': 21,
    'pgm_tally_3': 22,
    'pv_tally_4': 23,
    'pgm_tally_4': 24,
}

def setup_gpio_pins():
    for pin in GPIO_PINS.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, True)

def set_tally_leds(state):
    for pin in GPIO_PINS.values():
        GPIO.output(pin, not state)

def parse_xml_file(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    return {
        'host': root[0].text,
        'port': root[1].text,
        'password': root[2].text,
        'scenes': [root[i].text for i in range(3, 7)],
        'gpio_pins': [root[i].text for i in range(7, 15)],
    }

def on_switch(message, scene_configs):
    obsscene = message.getSceneName()
    try:
        scene_index = scene_configs['scenes'].index(obsscene)
    except ValueError:
        logging.debug('Scene without tally: %s', obsscene)
        return
    logging.debug('Camera %d active', scene_index + 1)
    pgm_tally_on(scene_configs, scene_index)

def on_preview(message, scene_configs):
    pv_scene = message.getSceneName()
    try:
        scene_index = scene_configs['scenes'].index(pv_scene)
    except ValueError:
        logging.debug('Scene without tally: %s', pv_scene)
        return
    logging.debug('Camera %d preview', scene_index + 1)
    pv_tally_on(scene_configs, scene_index)

def pgm_tally_on(scene_configs, index):
    logging.debug('PGM Tally on for camera %d', index + 1)
    GPIO.output(int(scene_configs['gpio_pins'][index * 2 + 1]), False)

def pv_tally_on(scene_configs, index):
    logging.debug('PV Tally on for camera %d', index + 1)
    GPIO.output(int(scene_configs['gpio_pins'][index * 2]), False)

def start_tally():
    setup_gpio_pins()
    scene_configs = parse_xml_file(XML_FILE)
    try:
        ws = obsws(scene_configs['host'], int(scene_configs['port']), scene_configs['password'])
        ws.connect()
        logging.debug('Connected to OBS')
        for scene in scene_configs['scenes']:
            ws.register(callback=on_switch, event=events.SwitchScenes)
            ws.register(callback=on_preview, event=events.PreviewSceneChanged)
            logging.debug('Registered events for %s', scene)
        set_tally_leds(True)
        logging.debug('Tally LEDs set to off')
        ws.run_forever()
    except KeyboardInterrupt:
        logging.debug('Interrupted by user')
    finally:
        set_tally_leds(False)
        logging.debug('Tally LEDs set to on')
        GPIO.cleanup()
        logging.debug('Cleaned up GPIO')
        ws.disconnect()
        logging.debug('Disconnected from OBS')

if __name__ == '__main__':
    start_tally()

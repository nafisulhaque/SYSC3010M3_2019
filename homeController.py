import serial
import globals
import json
from datetime import datetime

import socket, sys, time

host = sys.argv[1]
textport = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = (host, port)

ser = serial.Serial('COM10', 9600)

globals.initialize()


def parse_op_code(op_code_rec):
    globals.pirActive = int(op_code_rec[0])
    globals.lightsActive = int(op_code_rec[1])
    globals.blindsActive = int(op_code_rec[2])

    globals.lightsOn = int(op_code_rec[3])
    globals.blindsOn = int(op_code_rec[4])
    globals.temp = int(op_code_rec[5:7])
    globals.hum = int(op_code_rec[7:9])
    globals.temp_hum_rec = int(op_code_rec[9:])


def json_gen_send():
    if globals.temp_hum_rec == 1:
        temp_hum_dict = {
            "commandtype": "insert",
            "temp": globals.temp,
            "hum": globals.hum,
            "timeSent": str(datetime.now())
        }

    temp_hum_json = json.dumps(temp_hum_dict)

    return temp_hum_json


def comm_code_send():
    ser.write("10110".encode('UTF-8'))


def check_lights_active():
    return globals.lightsActive


def check_lights_on():
    return globals.lightsOn


def check_blinds_active():
    return globals.blindsActive


def check_blinds_on():
    return globals.blindsOn


def check_pir_active():
    return globals.pirActive


def check_hum_temp():
    return globals.temp, globals.hum


while True:
    data = ser.readline().decode('UTF-8')
    parse_op_code(data)
    if globals.temp_hum_rec == 1:
        json_gen = str(json_gen_send())
        print(json_gen)
        s.sendto(json_gen.encode('UTF-8'), server_address)

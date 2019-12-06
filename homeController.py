import serial
import socket, sys, time
import json
from datetime import datetime

host = sys.argv[1]
textport = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = (host, port)

ser = serial.Serial('COM10', 9600)

pirActive = 1
blindsActive = 1
lightsActive = 1

lightsOn = 0
blindsOn = 0

temp = 0
hum = 40

opCodeSen = 11011023


def parse_op_code(opCodeRec):
    global pirActive
    global blindsActive
    global lightsActive
    global lightsOn
    global blindsOn
    global temp
    global hum

    pirActive = opCodeRec[0]
    blindsActive = opCodeRec[1]
    lightsActive = opCodeRec[2]
    lightsOn = opCodeRec[3]
    blindsOn = opCodeRec[4]
    temp = opCodeRec[5:7]
    hum = opCodeRec[7:9]


def send_op_code():
    ser.write(opCodeSen.encode())


def json_gen_send():
    tempHumDict = {
        "command_type": "insert",
        "temp": temp,
        "hum": hum,
        "table": "readings",
        "timeSent": str(datetime.timestamp())
    }

    tempHumJSON = json.dumps(tempHumDict)

    return tempHumJSON


def check_lights_active():
    return lightsActive


def check_lights_on():
    return lightsOn


def check_blinds_active():
    return blindsActive


def check_blinds_on():
    return blindsOn


def check_pir_active():
    return pirActive


while True:
    opCodeRec = ser.readline().decode('UTF-8')
    parse_op_code(opCodeRec)
    tempHumJSON = json_gen_send()
    print(tempHumJSON)

    if not len(tempHumJSON):
        break

    s.sendto(tempHumJSON.encode('UTF-8'), server_address)

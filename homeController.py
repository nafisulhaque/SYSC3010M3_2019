import socket
import sys

import serial
import time

#host = sys.argv[1]
#textport = sys.argv[2]

motion_act = 1
#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#port = int(textport)
ser = serial.Serial('COM10', 9600)

motion_detect = 1


def read_motion():
    a = int(ser.readline().decode('UTF-8'))
    global motion_detect
    if a == 1:
        motion_detect = 1
    elif a == 0:
        motion_detect = 0

def toggle_lights():
    global motion_detect
    if motion_detect == 1:
        ser.write("Lights off".encode())
        motion_detect = 0
    elif motion_detect == 0:
        ser.write("Lights on".encode())

while True:
    time.sleep(2)
    toggle_lights()
    read = ser.readline()
    print(read.decode())
    toggle_lights()


import serial

ser = serial.Serial('COM10', 9600)

while True:
    ser.write(100)
    read_serial = ser.readline()
    print(read_serial.decode('UTF-8'))
import unittest
import serial
import homeController
import globals

ser = serial.Serial('COM10', 9600)
j = 1
success = 0
failed = 0
test_state = True


def test(i):
    switcher = {
        1: homeController.check_pir_active() == 0,
        2: homeController.check_pir_active() == 1,
        3: homeController.check_lights_active() == 1,
        4: homeController.check_lights_active() == 1,
        5: homeController.check_lights_on() == 0,
        6: homeController.check_lights_on() == 1,
        7: homeController.check_blinds_active() == 0,
        8: homeController.check_blinds_active() == 1,
        9: homeController.check_blinds_on() == 0,
        10: homeController.check_blinds_on() == 1,
        11: homeController.check_hum_temp() == (45, 63),
        12: homeController.check_hum_temp() == (25, 50),
        13: homeController.check_hum_temp() == (27, 18)

    }

    return switcher.get(i)


while test_state:
    data = ser.readline().decode('UTF-8')
    homeController.parse_op_code(data)

    result = test(j)
    if result:
        success += 1

    elif not result:
        failed += 1
        print("test " + str(j) + " failed")
    j += 1
    if j > 13:
        ser.close()
        test_state = False

print("Test successful: " + str(success))
print("Test failed: " + str(failed))

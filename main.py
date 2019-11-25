import logging
import sys
import time
import json
import databaseManager
import random

random.seed()

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.CRITICAL)
else:
    print("Running under other")

log = logging.getLogger(__name__)
counter = 0


def readinggenerator():
    global counter
    reading = dict()
    reading["tablename"] = "readings"
    reading["timesent"] = int(time.time()) + counter
    reading["temp"] = random.randint(-400, 400)
    reading["hum"] = random.randint(0, 800)
    reading["motion"] = random.randint(0, 1)
    reading["commandtype"] = "insert"
    reading["timereceived"] = int(time.time()) + counter
    counter += 1

    return reading

# parsejsonintocommand testing

invalidinput = list()
invalidinput.append(databaseManager.parsejsonintocommand(147174771.8383) is None)
invalidinput.append(databaseManager.parsejsonintocommand(json.dumps(["RAW", "PRAGMA table_info(readings);"])) is None)
invalidinput.append(databaseManager.parsejsonintocommand("foaiwehofhaosuhdfisuhidfhsdilhafsudhflsaiudhfaiuhsidufh") is None)





a = readinggenerator()
del a["tablename"]
b = readinggenerator()
del b["tablename"]
del b["temp"]
c = readinggenerator()
del c["tablename"]
c["test"] = "testtest"
testarray = [a, b, c]

jsonwithouttableinput = list()

for item in testarray:
    jsonwithouttableinput.append(databaseManager.parsejsonintocommand(json.dumps(item)) is None)

for i in range(len(jsonwithouttableinput)):
    if jsonwithouttableinput[i] is False:
        print("Failure in invalid json input test")
        print("Test failed with input: " + str(testarray[i]))



testarray = [readinggenerator(), readinggenerator(), readinggenerator()]
del testarray[1]["temp"]
fulljsoninput = list()

for item in testarray:
    fulljsoninput.append(databaseManager.parsejsonintocommand(json.dumps(item)) is not None)

for i in range(len(fulljsoninput)):
    if fulljsoninput[i] is False:
        print("Failure in valid json input test")
        print("Test failed with input: " + str(testarray[i]))


print("Testing for invalid json inputs: " + str(invalidinput))
print("Testing for valid json without table inputs: " + str(jsonwithouttableinput))
print("Testing for valid json inputs: " + str(fulljsoninput))





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

print("hello!")
invalidinput = list()
invalidinput.append(databaseManager.parsejsonintocommand(147174771.8383) is None)
invalidinput.append(databaseManager.parsejsonintocommand(json.dumps(["RAW", "PRAGMA table_info(readings);"])) is None)
invalidinput.append(databaseManager.parsejsonintocommand("foaiwehofhaosuhdfisuhidfhsdilhafsudhflsaiudhfaiuhsidufh") is None)

print("Testing for invalid json inputs: " + str(invalidinput))

#a = databaseManager.parsejsonintocommand(json.dumps({"commandtype": "RAW", "command": "PRAGMA table_info(readings);"}))
#c = [item[1] for item in a]
#print(c)

#assert databaseManager.parsejsonintocommand(json.dumps({"command": "PRAGMA table_info(readings);"})) is None

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

print("Testing for valid json without table inputs: " + str(jsonwithouttableinput))

testarray = [readinggenerator(), readinggenerator(), readinggenerator()]
del testarray[1]["temp"]
fulljsoninput = list()

for item in testarray:
    fulljsoninput.append(databaseManager.parsejsonintocommand(json.dumps(item)) is not None)

print("Testing for valid json inputs: " + str(fulljsoninput))





import logging
import sys
import datetime
import json
import databaseManager

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
else:
    print("Running under other")

log = logging.getLogger(__name__)

# parsejsonintocommand testing

print("hello!")
assert databaseManager.parsejsonintocommand("") is None
assert databaseManager.parsejsonintocommand(dict()) is None
databaseManager.parsejsonintocommand(json.dumps({"commandtype": "RAW", "command": "PRAGMA table_info(readings);"}))

assert databaseManager.parsejsonintocommand(json.dumps({"command": "PRAGMA table_info(readings);"})) is not None

json.dumps({"a": 4, "b":"asdf", "c":3.3})
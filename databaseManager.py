import math
import sys
import sqlite3
import re
import string
import json
import logging
import datetime

# https://stackoverflow.com/questions/15727420/using-python-logging-in-multiple-modules
if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

# testing and debug variables
db1name = "C:/SQLite/example.db"  # change to relative path later, include ability to have more database files

# Constants
VALID_CHARACTERS = string.ascii_letters + string.digits + '_'
DB1 = sqlite3.connect(db1name)
TIMEZONE = None  # maybe change later


def parsejsonintocommand(jsoninput):
    try:
        # parse json here
        readout = json.loads(jsoninput)
    except:
        log.error("json input could not be parsed")
        return None

    try:
        tablename = readout['tablename']
        assert(tablenamechecker(tablename))
        assert(isinstance(tablename, str))
    except AssertionError:
        log.error("tablename in received json input is not acceptable")
        return None
    except KeyError:
        log.error("tablename not found in json input")
        return None

    readout["time_received"] = datetime.datetime.now(tz = TIMEZONE)
    fieldnames = getschema(DB1, tablename)
    inputs = []
    for name in fieldnames:
        try:
            inputs += [readout[name]]
        except KeyError:
            inputs += [None]

    insertintotable(DB1, tablename, inputs, len(fieldnames))


# This does not accept all valid table names, but will keep most conventional ones and all the ones we use.
# The first character must be either a letter or an underscore.
# All other characters must be letters, numbers or underscore
def tablenamechecker(tablename):
    if len(tablename) == 0:
        log.debug("Failure due to empty table name.")
        return False
    if tablename[0] in string.ascii_letters or tablename[0] == '_':
        for c in tablename:
            if c not in VALID_CHARACTERS:
                log.debug("Failure due to table name containing non-alphanumeric characters.")
                return False
        log.debug("Success in checking table name")
        return True
    log.debug("Failure due to table name starting with invalid character")
    return False


def getschema(tableobj, tablename):
    cursor = tableobj.cursor()

    if tablenamechecker(tablename):
        command = "PRAGMA table_info(" + tablename + ");"
        cursor.execute(command)
        fieldnames = [x[1] for x in cursor.fetchall()]
        print(fieldnames)
        return fieldnames
    log.error("tablename is incorrect in getschema()")
    return None


def insertintotable(tableobj, tablename, inputs, tablewidth):

    tablename = tablename.strip()
    if tablenamechecker(tablename) is False:
        raise ValueError
    if tablewidth == 0:
        raise IndexError
    if len(inputs) != tablewidth:
        raise IndexError  # number of inputs is too small or large

    command = "insert into " + tablename + "(" + str(getschema(tableobj, tablename))[1:-1] + ") values(" + "?, " * tablewidth
    command = command[:-2] + ");"

    cursor = tableobj.cursor()
    cursor.execute(command, inputs)
    tableobj.commit()


# reading more lines than there are lines in the table will return only the number of lines in the table.
def readlastnlines(tableobj, tablename, n):
    if n < 1:
        return None  # reading less than one line
    tablename = tablename.strip()
    if tablenamechecker(tablename) is False:
        raise ValueError
    command = "SELECT * FROM " + tablename + " ORDER BY time DESC LIMIT "
    command = command + str(n) + ";"

    cursor = tableobj.cursor()
    cursor.execute(command)  # Select last n lines, up to max number.

    # https://stackoverflow.com/questions/10195139/how-to-retrieve-sql-result-column-value-using-column-name-in-python
    # ty stack overflow
    fieldnames = [field[0] for field in cursor.description]
    print (fieldnames)
    values = cursor.fetchone()
    rows = []
    while values is not None:
        row = dict(zip(fieldnames, values))
        values = cursor.fetchone()
        rows = rows + [row]

    print(rows)

    return rows



getschema(DB1, "testing")
readlastnlines(DB1, "testing", 4)
asdf = json.dumps({"a": 3, "b": 4, "c": 5, "tablename": "testing", "time": 1234, "id": 123, "name": "qwer"})
parsejsonintocommand(asdf)

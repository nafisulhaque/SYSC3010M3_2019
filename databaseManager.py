"""
This file handles all database commands.

The important function is parsejsonintocommand().
It takes a jsonified (python dictionary) as a string, and attempts to run the contained command.


Written by Dorian Wang
"""

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
db1name = "./main.db"  # file in local directory

# Constants
VALID_CHARACTERS = string.ascii_letters + string.digits + '_'
DB1 = sqlite3.connect(db1name)
TIMEZONE = None  # maybe change later, set to local timezone


# The input must include the table the command is affecting if it is not a raw SQL command.
# Raw SQL commands are run without other checking.
# No security or feedback is provided for such commands as it is not within the scope of this project.
def parsejsonintocommand(jsoninput):
    """

    :param jsoninput: string from a call from json.dumps(dict). The dict() must contain element 'commandtype'.
    'commandtype' dictates the command run. 'insert' makes it add all elements with the same
    :return:
    """
    try:
        # parse json string here
        readout = json.loads(jsoninput)
        assert (isinstance(readout, dict))
        assert (isinstance(readout['commandtype'], str))
    except AssertionError:
        log.error("received jsoninput could not be parsed into a dictionary")
        return None
    except:
        log.error("json input could not be parsed")
        return None

    if readout['commandtype'] == "RAW":
        cursor = DB1.cursor()
        log.info("This is not safe, and may not exist in the final version")
        returnvalue = cursor.execute(readout['command']).fetchall()
        DB1.commit()
        return returnvalue

    elif "insert" == readout['commandtype'].strip().lower():
        log.debug("Inserting into database")

        try:
            tablename = readout['tablename']
            assert (tablenamechecker(tablename))
            assert (isinstance(tablename, str))
        except AssertionError:
            log.error("tablename in received json input is not a string")
            return None
        except KeyError:
            log.error("tablename not found in json input")
            return None

        readout["time_received"] = datetime.datetime.now(tz=TIMEZONE)
        fieldnames = getschema(DB1, tablename)
        inputs = []
        for name in fieldnames:
            try:
                inputs += [readout[name]]
            except KeyError:
                inputs += [None]
        try:
            return insertintotable(DB1, tablename, inputs, len(fieldnames))
        except ValueError:
            log.error("Value error when attempting to insert into table")
            return None
        except IndexError:
            log.error("Index error when attempting to insert into table")
            return None
        except sqlite3.IntegrityError:
            log.error("Integrity error when attempting to insert into table")
            return None

    elif "read" == readout['commandtype'].strip().lower():

        try:
            tablename = readout['tablename']
            assert (tablenamechecker(tablename))
            assert (isinstance(tablename, str))
        except AssertionError:
            log.error("tablename in received json input is not a string")
            return None
        except KeyError:
            log.error("tablename not found in json input")
            return None

        try:
            numlines = readout['numlines']
            numlines = int(numlines)
        except KeyError:
            log.error("numlines not found in json input")
            return None
        except ValueError:
            log.error("numlines is not an integer, or is not properly formatted")
            return None

        return readlastnlines(DB1, tablename, numlines)

    else:
        log.info("No command read, skipping")
        return None


# This does not accept all valid table names, but will keep most conventional ones and all the ones we use.
# The first character must be either a letter or an underscore.
# All other characters must be letters, numbers or underscore
def tablenamechecker(tablename):
    if len(tablename) == 0:
        log.error("Failure in tablenamechecker() due to empty table name.")
        return False
    if tablename[0] in string.ascii_letters or tablename[0] == '_':
        for c in tablename:
            if c not in VALID_CHARACTERS:
                log.error("Failure in tablenamechecker() due to table name containing non-alphanumeric characters.")
                return False
        log.debug("Success in checking table name")
        return True
    log.error("Failure in tablenamechecker() due to table name starting with invalid character")
    return False


# returns the schema of the specified table in a list.
def getschema(tableobj, tablename):
    cursor = tableobj.cursor()

    if tablenamechecker(tablename):
        command = "PRAGMA table_info(" + tablename + ");"
        cursor.execute(command)
        fieldnames = [x[1] for x in cursor.fetchall()]
        return fieldnames
    log.error("tablename is incorrect in getschema()")
    return None


# inserts the inputs dictionary into the table. If inputs are missing it will rely on SQLite defaults.
def insertintotable(tableobj, tablename, inputs, tablewidth):
    tablename = tablename.strip()
    if tablenamechecker(tablename) is False:
        raise ValueError
    if tablewidth == 0:
        raise IndexError
    if len(inputs) != tablewidth:
        raise IndexError  # number of inputs is too small or large

    command = "insert into " + tablename + "(" + str(getschema(tableobj, tablename))[
                                                 1:-1] + ") values(" + "?, " * tablewidth
    command = command[:-2] + ");"

    cursor = tableobj.cursor()
    try:
        cursor.execute(command, inputs)
    except sqlite3.IntegrityError:
        raise sqlite3.IntegrityError
        return
    tableobj.commit()
    return True


# Reads n number or lines from the specified table.
# Reading more lines than there are lines in the table will return only the number of lines in the table.
def readlastnlines(tableobj, tablename, n):
    if n < 1:
        return None  # reading less than one line
    tablename = tablename.strip()
    if tablenamechecker(tablename) is False:
        raise ValueError
    command = "SELECT * FROM " + tablename + " ORDER BY timesent DESC LIMIT "
    command = command + str(n) + ";"

    cursor = tableobj.cursor()
    cursor.execute(command)  # Select last n lines, up to max number.

    # https://stackoverflow.com/questions/10195139/how-to-retrieve-sql-result-column-value-using-column-name-in-python
    # ty stack overflow
    fieldnames = [field[0] for field in cursor.description]
    values = cursor.fetchone()
    rows = []
    while values is not None:
        row = dict(zip(fieldnames, values))
        values = cursor.fetchone()
        rows = rows + [row]

    return rows

# value = readlastnlines(DB1, "readings", 4)
# value = json.dumps(value)
# value = json.loads(value)
# print(value)
# print(value[1]['timesent'])
# asdf = json.dumps({"commandtype": "RAW", "tablename": "testing", "time": 1234, "id": 123, "name": "qwer", \
# "command": "SELECT Count(*) FROM testing"})
# print(parsejsonintocommand(asdf))

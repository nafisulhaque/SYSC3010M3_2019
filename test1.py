import math
import sqlite3
import re
import string

# testing and debug variables
db1name = "C:/SQLite/example.db"  # change to relative path later, include ability to have more database files


# Constants
VALID_CHARACTERS = string.ascii_letters + string.digits + '_'
DB1 = sqlite3.connect(db1name)

# This does not accept all valid table names, but will keep most conventional ones and all the ones we use.
# The first character must be either a letter or an underscore.
# All other characters must be letters, numbers or underscore
def tablenamechecker(tablename):
    if len(tablename) == 0:
        return false
    if tablename[0] in string.ascii_letters or tablename[0] == '_':
        for c in tablename:
            if c not in VALID_CHARACTERS:
                return false
    return true


def insertintotable(tableobj, tablename, inputs, tablewidth):

    tablename = tablename.strip()
    if tablenamechecker(tablename) == false:
        raise ValueError
    if tablewidth == 0:
        raise IndexError
    if inputs.size() != tablewidth:
        raise IndexError  # number of inputs is too small or large

    command = "insert into " + tablename + " values(" + "%s, " * tablewidth
    command = command[:-2] + ");"
    command = command % db1.literal(inputs)

    cursor = tableobj.cursor()
    cursor.execute(command)


# reading more lines than there are lines in the table will return only the number of lines in the table.
def readlastnlines(tableobj, tablename, n):
    if n < 1:
        return None  # reading less than one line
    tablename = tablename.strip()
    if tablenamechecker(tablename) == false:
        raise ValueError
    command = "SELECT * FROM " + tablename + " ORDER BY time DESC LIMIT "
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

    print(rows)

    return rows


readlastnlines(DB1, "testings", 4)


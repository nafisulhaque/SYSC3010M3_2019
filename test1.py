import math
import sqlite3



db1name = "C:/SQLite/example.db"
db1 = sqlite3.connect(db1name)


def insertintotable(tableobj, inputs, tablewidth):
    if tablewidth == 0:
        raise IndexError
    if inputs.size() != tablewidth:
        raise IndexError  # number of inputs is too small or large
    command = "insert into table values(" + "%s, " * tablewidth
    command = command[:-2] + ");"
    command = command % db1.literal(inputs)
    cursor = tableobj.cursor()

def readlastnlines(tableobj, n):
    if n == 0:
        return None
    command = "SELECT * FROM testing ORDER BY time DESC LIMIT "
    command = command + str(n) + ";"
    cursor = tableobj.cursor()

    cursor.execute(command)  # Select last n lines, up to max number.

    # https://stackoverflow.com/questions/10195139/how-to-retrieve-sql-result-column-value-using-column-name-in-python
    # ty stack overflow

    fieldnames = [field[0] for field in cursor.description]
    values = cursor.fetchone()
    rows = []
    while values != None:
        row = dict(zip(fieldnames, values))
        values = cursor.fetchone()
        rows = rows + [row]

    print(rows)

    return rows

readlastnlines(db1, 4)


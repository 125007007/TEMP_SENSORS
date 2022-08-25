import sqlite3, sys, json

with open('locations.json') as json_file:
    data = json.load(json_file)

names = data['names']

if len(sys.argv) < 2:
    print('Usage: readDatabase.py <database name>')
    sys.exit()

database = sys.argv[1]



def readData():
    conn = sqlite3.connect(sys.argv[1])
    curs = conn.cursor()
    print ("\nEntire database contents:\n")
    for key, value in names.items():
        for row in curs.execute("SELECT * FROM {}".format(value)):
            print(row)

readData()
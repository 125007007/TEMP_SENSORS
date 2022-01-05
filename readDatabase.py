import sqlite3, sys


if len(sys.argv) < 2:
    print('Usage: readDatabase.py <database name>')
    sys.exit()

if sys.argv[1] == 'sensor1Data.db':
    conn = sqlite3.connect('sensor1Data.db')
elif sys.argv[1] == 'sensor2Data.db':
    conn=sqlite3.connect('sensor2Data.db')
else:
    print('Usage: readDatabase.py <database name>')
    sys.exit()

curs = conn.cursor()
print ("\nEntire database contents:\n")
for row in curs.execute("SELECT * FROM DHT_data"):
    print(row)
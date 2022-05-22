import sqlite3, sys


if len(sys.argv) < 2:
    print('Usage: readDatabase.py <database name>')
    sys.exit()

if sys.argv[1] == 'sensor1Data.db' or sys.argv[1] == 'sensor2Data.db':
    conn = sqlite3.connect(sys.argv[1])
    curs = conn.cursor()
    print ("\nEntire database contents:\n")
    for row in curs.execute("SELECT * FROM DHT_data"):
        print(row)
elif sys.argv[1] == 'serverCPU.db':
    conn=sqlite3.connect(sys.argv[1])
    curs = conn.cursor()
    print ("\nEntire database contents:\n")
    for row in curs.execute("SELECT * FROM CPU_temps"):
        print(row)
else:
    print('Usage: readDatabase.py <database name>')
    sys.exit()


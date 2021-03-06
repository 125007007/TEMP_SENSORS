import sqlite3, sys
from datetime import datetime


if len(sys.argv) < 2:
    print('Usage: readDatabase.py <database name>')
    sys.exit()

conn = sqlite3.connect(sys.argv[1])
curs = conn.cursor()
print ("\nEntire database contents:\n")
for row in curs.execute("SELECT * FROM DHT_data WHERE date(timestamp, 'unixepoch') = " + str(datetime.today().strftime('%Y-%m-%d'))):
    print(row)
import sqlite3, sys
from datetime import datetime


if len(sys.argv) < 2:
    print('Usage: dateSelector.py <database name>')
    sys.exit()

conn = sqlite3.connect(sys.argv[1])
curs = conn.cursor()
tdate = str(datetime.today().strftime('%Y-%m-%d'))
print ("\nEntire database contents:\n")
for row in curs.execute("SELECT * FROM CPU_temps WHERE timestamp >= datetime('now', '-12 hours')"):
    print(row)
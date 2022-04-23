import sqlite3 as lite
import sys


con = lite.connect('sensor1Data.db')
with con:
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS DHT_data")
	cur.execute("CREATE TABLE DHT_data(name TEXT, timestamp DATETIME, temp NUMERIC, hum NUMERIC)")

print('Created Table 1')

con = lite.connect('sensor2Data.db')
with con:
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS DHT_data")
	cur.execute("CREATE TABLE DHT_data(name TEXT, temp NUMERIC, hum NUMERIC, date TEXT, time TEXT)")

print('Created Table 2')
print('Done!')
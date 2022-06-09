import sqlite3 as lite
import sys


con = lite.connect('serverCPU.db')
with con:
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS CPU_temps")
	cur.execute("CREATE TABLE CPU_temps(temp NUMERIC, date TEXT, time TEXT, timestamp DATETIME)")

print('Created Table 1')


con = lite.connect('sensor1Data.db')
with con:
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS DHT_data")
	cur.execute("CREATE TABLE DHT_data(name TEXT, temp NUMERIC, hum NUMERIC, timestamp DATETIME)")

print('Created Table 2')

con = lite.connect('sensor2Data.db')
with con:
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS DHT_data")
	cur.execute("CREATE TABLE DHT_data(name TEXT, temp NUMERIC, hum NUMERIC, timestamp DATETIME)")

print('Created Table 3')
print('Done!')
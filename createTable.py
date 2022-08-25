import sqlite3 as lite
import sys
import json

 
# Opening JSON file
with open('locations.json') as json_file:
    data = json.load(json_file)

names = data['names']

con = lite.connect('loggedData.db')
with con:
	cur = con.cursor()
	cur.execute('DROP TABLE IF EXISTS CPU_temps')
	cur.execute('CREATE TABLE CPU_temps(temp NUMERIC, date TEXT, time TEXT, timestamp DATETIME)')
	print('Created Table CPU_temps')

	for key, value in names.items():
		cur.execute('DROP TABLE IF EXISTS {}'.format(value))
		cur.execute('CREATE TABLE {}(name TEXT, temp NUMERIC, hum NUMERIC, timestamp DATETIME)'.format(value))
		print('Created table {}'.format(value))
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  appDhtWebHist_v2.py
#  
#  Created by MJRoBot.org 
#  10Jan18

'''
	RPi WEb Server for DHT captured data with Gage and Graph plot  
'''

from datetime import datetime
from gpiozero import CPUTemperature
import os, sqlite3, io
from flask import Flask, render_template, send_file, make_response, request, Response


app = Flask(__name__)


# Retrieve LAST data from database
def getLastData():
	conn = sqlite3.connect('../sensor1Data.db', check_same_thread=False)
	curs = conn.cursor()
	for row in curs.execute("SELECT * FROM DHT_data ORDER BY data DESC LIMIT 1"):
		name = str(row[0])
		temp = row[1]
		hum = row[2]
		date = str(row[3])
		time = str(row[4])

	conn.close()
	return name, temp, hum, date, time

# Get Max number of rows (table size)
def maxRowsTable():
	conn = sqlite3.connect('../sensor1Data.db', check_same_thread=False)
	curs = conn.cursor()
	for row in curs.execute("select COUNT(temp) from  DHT_data"):
		maxNumberRows=row[0]
	conn.close()
	return maxNumberRows

# define and initialize global variables
global numSamples
numSamples = maxRowsTable()
if (numSamples > 145):
        numSamples = 100

# Get 'x' samples of historical data
def getHistData (numSamples):
	conn = sqlite3.connect('../sensor1Data.db', check_same_thread=False)
	curs = conn.cursor()
	curs.execute("SELECT * FROM DHT_data ORDER BY data DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	names = []
	temps = []
	hums = []
	dates = []
	times = []

	for row in reversed(data):
		names.append(row[0])
		temps.append(row[1])
		hums.append(row[2])
		dates.append(row[3])
		times.append(row[4])
	conn.close()
	return names, temps, hums, dates, times

# Retrieve LAST data from database
def getLastData2():
	conn = sqlite3.connect('../sensor2Data.db', check_same_thread=False)
	curs = conn.cursor()
	for row in curs.execute("SELECT * FROM DHT_data ORDER BY data DESC LIMIT 1"):
		name = str(row[0])
		temp = row[1]
		hum = row[2]
		date = str(row[3])
		time = str(row[4])

	conn.close()
	return name, temp, hum, date, time

# Get 'x' samples of historical data
def getHistData2(numSamples):
	conn = sqlite3.connect('../sensor2Data.db', check_same_thread=False)
	curs = conn.cursor()
	curs.execute("SELECT * FROM DHT_data ORDER BY date DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	names = []
	temps = []
	hums = []
	dates = []
	times = []
	for row in reversed(data):
		names.append(row[0])
		temps.append(row[1])
		hums.append(row[2])
		dates.append(row[3])
		times.append(row[4])
	conn.close()
	return names, temps, hums, dates, times

def getCurrentDayData1():
	conn = sqlite3.connect('../sensor1Data.db', check_same_thread=False)
	curs = conn.cursor()
	curs.execute("SELECT * FROM DHT_data WHERE date(date, 'unixepoch') = " + str(datetime.today().strftime('%Y-%m-%d')))
	data = curs.fetchall()
	names = []
	temps = []
	hums = []
	dates = []
	times = []
	for row in reversed(data):
		names.append(row[0])
		temps.append(row[1])
		hums.append(row[2])
		dates.append(row[3])
		times.append(row[4])
	conn.close()
	return names, temps, hums, dates, times


global rangeTime
rangeTime = 100


#main route 
@app.route("/")
def index():

	templateData = {'CPU_temp': CPUTemperature().temperature}

	return render_template('index.html', **templateData)

@app.route("/sensor1")
def sensor1():
	name, temp, hum, date, time = getHistData(numSamples)
	name_last, temp_last, hum_last, date_last, time_last, = getLastData()
	templateData = {'name':name,
					'temp':temp,
					'hum':hum,
					'date':date,
					'time':time,
					'name_last':name_last,
					'temp_last':temp_last,
					'hum_last':hum_last,
					'date_last':date_last,
					'time_last':time_last}

	return render_template('sensor1.html', **templateData)

@app.route("/sensor1/dayTemp")
def sensor1_dayTemp():
	name, temp, hum, date, time = getCurrentDayData1()
	name_last, temp_last, hum_last, date_last, time_last = getLastData()
	templateData = {'name':name,
					'temp':temp,
					'hum':hum,
					'date':date,
					'time':time,
					'name_last':name_last,
					'temp_last':temp_last,
					'hum_last':hum_last,
					'date_last':date_last,
					'time_last':time_last}

	return render_template('sensor1_day.html', **templateData)

@app.route("/sensor2")
def sensor2():
	name, temp, hum, date, time = getHistData2(numSamples)
	name_last, temp_last, hum_last, date_last, time_last = getLastData2()
	templateData = {'name':name,
					'temp':temp,
					'hum':hum,
					'date':date,
					'time':time,
					'name_last':name_last,
					'temp_last':temp_last,
					'hum_last':hum_last,
					'date_last':date_last,
					'time_last':time_last}

	return render_template('sensor2.html', **templateData)


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)

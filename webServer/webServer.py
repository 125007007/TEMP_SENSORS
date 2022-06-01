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
import sqlite3, time, threading
from flask import Flask, render_template, send_file, make_response, request, Response


app = Flask(__name__)


# Retrieve LAST data from database
def getLastData():
	conn = sqlite3.connect('../sensor1Data.db', check_same_thread=False)
	curs = conn.cursor()
	for row in curs.execute("SELECT * FROM DHT_data ORDER BY date DESC LIMIT 1"):
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
def getHistData(numSamples):
	conn = sqlite3.connect('../sensor1Data.db', check_same_thread=False)
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

# Retrieve LAST data from database
def getLastData2():
	conn = sqlite3.connect('../sensor2Data.db', check_same_thread=False)
	curs = conn.cursor()
	for row in curs.execute("SELECT * FROM DHT_data ORDER BY date DESC LIMIT 1"):
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

global rangeTime
rangeTime = 100



def cpuTempLog():

	while True:

		temp = round(CPUTemperature().temperature, 1)
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		current_date = now.strftime('%Y-%m-%d')
		rounded_timestamp = now.replace(microsecond=0)
		conn=sqlite3.connect('../serverCPU.db')
		curs=conn.cursor()
		curs.execute("INSERT INTO CPU_temps values((?), (?), (?), (?))", (temp, current_date, current_time, rounded_timestamp)) 
		conn.commit()
		conn.close()
		time.sleep(300)

def getHistDataCPU(numSamples):
	conn = sqlite3.connect('../serverCPU.db', check_same_thread=False)
	curs = conn.cursor()
	curs.execute("SELECT * FROM CPU_temps ORDER BY date ASC")
	data = curs.fetchall()
	temps = []
	dates = []
	times = []
	timestamps = []

	for row in reversed(data):
		temps.append(row[0])
		dates.append(row[1])
		times.append(row[2])
		timestamps.append(row[3])

	conn.close()
	return temps, dates, times, timestamps

def getDayCPU(selectDate):
	conn = sqlite3.connect('../serverCPU.db', check_same_thread=False)
	curs = conn.cursor()
	curs.execute("SELECT * FROM CPU_temps WHERE date = '{}'".format(selectDate))
	data = curs.fetchall()
	temps = []
	dates = []
	times = []
	timestamps = []

	for row in reversed(data):
		temps.append(row[0])
		dates.append(row[1])
		times.append(row[2])
		timestamps.append(row[3])

	conn.close()
	return temps, dates, times, timestamps

#main route 
@app.route("/", methods=['GET', 'POST'])
def index():

	temps, dates, times, timestamps = getHistDataCPU(numSamples)

	templateData = {'temp':temps,
					'date':dates,
					'time':times,
					'timestamps':timestamps,
					'CPU_temp_now': CPUTemperature().temperature}

	if request.method == 'POST':
		selectedDate = request.form.get("Sdate")

		temps, dates, times, timestamps = getDayCPU(str(selectedDate))

		templateData = {'temp':temps,
						'date':dates,
						'time':times,
						'timestamps':timestamps}

		return render_template('sensor1_day.html', **templateData)

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

@app.route("/Sday")
def sensor1_dayTemp():
	
	temps, dates, times, timestamps = getDayCPU(str(datetime.today().strftime('%Y-%m-%d')))

	templateData = {'temp':temps,
					'date':dates,
					'time':times,
					'timestamps':timestamps}

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
	t1 = threading.Thread(target=cpuTempLog)
	t1.start()
	app.run(host='0.0.0.0', port=80, debug=True)

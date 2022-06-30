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
	conn = sqlite3.connect('../sensor1.db', check_same_thread=False)
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
	conn = sqlite3.connect('../sensor1.db', check_same_thread=False)
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
	conn = sqlite3.connect('../sensor1.db', check_same_thread=False)
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
	conn = sqlite3.connect('../sensor2.db', check_same_thread=False)
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
	conn = sqlite3.connect('../sensor2.db', check_same_thread=False)
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


#-------------------------------------------------------CPU temp stuff-----------------------------------------------------------------------------

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

def last12HoursCPU():
	conn = sqlite3.connect('../serverCPU.db', check_same_thread=False)
	curs = conn.cursor()
	#curs.execute("SELECT * FROM CPU_temps ORDER BY date ASC")
	curs.execute("SELECT * FROM CPU_temps WHERE timestamp >= datetime('now', '-1 hours')")
	data = curs.fetchall()
	temps = []
	dates = []
	times = []
	timestamps = []

	for row in data:
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

	for row in data:
		temps.append(row[0])
		dates.append(row[1])
		times.append(row[2])
		timestamps.append(row[3])

	conn.close()
	return temps, dates, times, timestamps

#-----------------------------------------------------------end-------------------------------------------------------------------------------------



def last12hours(database):
	conn = sqlite3.connect(database, check_same_thread=False)
	curs = conn.cursor()
	curs.execute("SELECT * FROM DHT_data WHERE timestamp >= datetime('now', '-1 hours')")
	data = curs.fetchall()
	names = []
	temps = []
	hums = []
	timestamps = []

	for row in data:
		names.append(row[0])
		temps.append(row[1])
		hums.append(row[2])
		timestamps.append(row[3])
	conn.close()
	return names, temps, hums, timestamps

def lastReading(database):
	conn = sqlite3.connect(database, check_same_thread=False)
	curs = conn.cursor()
	for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"):
		name = str(row[0])
		temp = row[1]
		hum = row[2]
		timestamp = str(row[3])

	conn.close()
	return name, temp, hum, timestamp

def selectDay(database, selectDate):
	conn = sqlite3.connect(database, check_same_thread=False)
	curs = conn.cursor()
	curs.execute("SELECT * FROM DHT_data WHERE timestamp like '{}%'".format(selectDate))
	data = curs.fetchall()
	names = []
	temps = []
	hums = []
	timestamps = []

	for row in data:
		names.append(row[0])
		temps.append(row[1])
		hums.append(row[2])
		timestamps.append(row[3])

	conn.close()
	return names, temps, hums, timestamps




#main route 
@app.route("/", methods=['GET', 'POST'])
def index():

	temps, dates, times, timestamps = last12HoursCPU()

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

		return render_template('fullDayCPU.html', **templateData)

	return render_template('index.html', **templateData)

@app.route("/ServerCPU/entireDay")
def sensor1_dayTemp():
	
	temps, dates, times, timestamps = getDayCPU(str(datetime.today().strftime('%Y-%m-%d')))

	templateData = {'temp':temps,
					'date':dates,
					'time':times,
					'timestamps':timestamps}

	return render_template('fullDayCPU.html', **templateData)

@app.route("/sensor1")
def sensor1():
	name_last, temp_last, hum_last, timestamp_last, = lastReading('../sensor1.db')
	templateData = {'name_last':name_last,
					'temp_last':temp_last,
					'hum_last':hum_last,
					'timestamp_last':timestamp_last}

	return render_template('sensor1.html', **templateData)

@app.route("/sensor1/temperature", methods=['GET', 'POST'])
def sensor1Temp():
	names, temps, hums, timestamps = last12hours('../sensor1.db')
	#name_last, temp_last, hum_last, timestamp_last, = lastReading('../sensor1.db')

	templateData = {'names':names,
					'temps':temps,
					'hums':hums,
					'timestamps':timestamps,
					'name_last':names[-1],
					'temp_last':temps[-1],
					'hum_last':hums[-1],
					'timestamp_last':timestamps[-1]}

	
	if request.method == 'POST':
		selectedDate = request.form.get("Sdate")

		names, temps, hums, timestamps = selectDay('../sensor1.db', str(selectedDate))

		templateData = {'names':names,
						'temps':temps,
						'hums':hums,
						'timestamps':timestamps,
						'selectedDate':selectedDate,
						'name_last':names[-1]}

		return render_template('fullDayTemp.html', **templateData)

	return render_template('sensor1Temp.html', **templateData)


@app.route("/sensor1/humidity", methods=['GET', 'POST'])
def sensor1Hum():
	names, temps, hums, timestamps = last12hours('../sensor1.db')
	#name_last, temp_last, hum_last, timestamp_last, = lastReading('../sensor1.db')

	templateData = {'names':names,
					'temps':temps,
					'hums':hums,
					'timestamps':timestamps,
					'name_last':names[-1],
					'temp_last':temps[-1],
					'hum_last':hums[-1],
					'timestamp_last':timestamps[-1]}

	
	if request.method == 'POST':
		selectedDate = request.form.get("Sdate")

		names, temps, hums, timestamps = selectDay('../sensor1.db', str(selectedDate))

		templateData = {'names':names,
						'temps':temps,
						'hums':hums,
						'timestamps':timestamps,
						'selectedDate':selectedDate,
						'name_last':names[-1]}

		return render_template('fullDayHum.html', **templateData)

	return render_template('sensor1Hum.html', **templateData)




@app.route("/sensor2")
def sensor2():
	name_last, temp_last, hum_last, timestamp_last, = lastReading('../sensor2.db')
	templateData = {'name_last':name_last,
					'temp_last':temp_last,
					'hum_last':hum_last,
					'timestamp_last':timestamp_last}

	return render_template('sensor2.html', **templateData)

@app.route("/sensor2/temperature", methods=['GET', 'POST'])
def sensor2Temp():
	names, temps, hums, timestamps = last12hours('../sensor2.db')
	#name_last, temp_last, hum_last, timestamp_last, = lastReading('../sensor2.db')

	templateData = {'names':names,
					'temps':temps,
					'hums':hums,
					'timestamps':timestamps,
					'name_last':names[-1],
					'temp_last':temps[-1],
					'hum_last':hums[-1],
					'timestamp_last':timestamps[-1]}

	
	if request.method == 'POST':
		selectedDate = request.form.get("Sdate")

		names, temps, hums, timestamps = selectDay('../sensor2.db', str(selectedDate))

		templateData = {'names':names,
						'temps':temps,
						'hums':hums,
						'timestamps':timestamps,
						'selectedDate':selectedDate,
						'name_last':names[-1]}

		return render_template('fullDayTemp.html', **templateData)

	return render_template('sensor2Temp.html', **templateData)


@app.route("/sensor2/humidity", methods=['GET', 'POST'])
def sensor2Hum():
	names, temps, hums, timestamps = last12hours('../sensor2.db')
	#name_last, temp_last, hum_last, timestamp_last, = lastReading('../sensor2.db')

	templateData = {'names':names,
					'temps':temps,
					'hums':hums,
					'timestamps':timestamps,
					'name_last':names[-1],
					'temp_last':temps[-1],
					'hum_last':hums[-1],
					'timestamp_last':timestamps[-1]}

	
	if request.method == 'POST':
		selectedDate = request.form.get("Sdate")

		names, temps, hums, timestamps = selectDay('../sensor2.db', str(selectedDate))

		templateData = {'names':names,
						'temps':temps,
						'hums':hums,
						'timestamps':timestamps,
						'selectedDate':selectedDate,
						'name_last':names[-1]}

		return render_template('fullDayHum.html', **templateData)

	return render_template('sensor2Hum.html', **templateData)



if __name__ == "__main__":
	t1 = threading.Thread(target=cpuTempLog)
	t1.start()
	app.run(host='0.0.0.0', port=80, debug=True)

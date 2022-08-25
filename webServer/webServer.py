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

from platform import platform

# set to false to not use the pi CPU temp logging
rpi = False

if rpi is True:
	from gpiozero import CPUTemperature

from datetime import datetime
import sqlite3, time, threading
from flask import Flask, render_template, send_file, make_response, request, Response


app = Flask(__name__)

global database
database = '../loggedData.db'

#-------------------------------------------------------CPU temp stuff-----------------------------------------------------------------------------

def cpuTempLog():

	while True:

		temp = round(CPUTemperature().temperature, 1)
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		current_date = now.strftime('%Y-%m-%d')
		rounded_timestamp = now.replace(microsecond=0)
		conn=sqlite3.connect(database)
		curs=conn.cursor()
		curs.execute("INSERT INTO CPU_temps values((?), (?), (?), (?))", (temp, current_date, current_time, rounded_timestamp)) 
		conn.commit()
		conn.close()
		time.sleep(300)

def last12HoursCPU():
	conn = sqlite3.connect(database, check_same_thread=False)
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
	conn = sqlite3.connect(database, check_same_thread=False)
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



def last12hours(table):
	conn = sqlite3.connect(database, check_same_thread=False)
	curs = conn.cursor()
	curs.execute("SELECT * FROM {} WHERE timestamp >= datetime('now', '-1 hours')".format(table))
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

def lastReading(table):
	conn = sqlite3.connect(database, check_same_thread=False)
	curs = conn.cursor()
	for row in curs.execute("SELECT * FROM {} ORDER BY timestamp DESC LIMIT 1".format(table)):
		name = str(row[0])
		temp = row[1]
		hum = row[2]
		timestamp = str(row[3])

	conn.close()
	return name, temp, hum, timestamp

def selectDay(table, selectDate):
	conn = sqlite3.connect(database, check_same_thread=False)
	curs = conn.cursor()
	curs.execute("SELECT * FROM {} WHERE timestamp like '{}%'".format(table, selectDate))
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
@app.route("/")
def index():

	return render_template('index.html')

# server cpu temp route 
@app.route("/serverCPU", methods=['GET', 'POST'])
def serverCPU():

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

	return render_template('serverCPU.html', **templateData)

@app.route("/serverCPU/entireDay")
def sensor1_dayTemp():
	
	temps, dates, times, timestamps = getDayCPU(str(datetime.today().strftime('%Y-%m-%d')))

	templateData = {'temp':temps,
					'date':dates,
					'time':times,
					'timestamps':timestamps}

	return render_template('fullDayCPU.html', **templateData)

@app.route("/sensor1")
def sensor1():
	name_last, temp_last, hum_last, timestamp_last, = lastReading('sensor1')
	templateData = {'name_last':name_last,
					'temp_last':temp_last,
					'hum_last':hum_last,
					'timestamp_last':timestamp_last}

	return render_template('sensor1.html', **templateData)

@app.route("/sensor1/temperature", methods=['GET', 'POST'])
def sensor1Temp():
	names, temps, hums, timestamps = last12hours('sensor1')
	#name_last, temp_last, hum_last, timestamp_last, = lastReading()

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

		names, temps, hums, timestamps = selectDay('sensor1', str(selectedDate))

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
	names, temps, hums, timestamps = last12hours('sensor1')
	#name_last, temp_last, hum_last, timestamp_last, = lastReading()

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

		names, temps, hums, timestamps = selectDay('sensor1', str(selectedDate))

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
	name_last, temp_last, hum_last, timestamp_last, = lastReading('sensor2')
	templateData = {'name_last':name_last,
					'temp_last':temp_last,
					'hum_last':hum_last,
					'timestamp_last':timestamp_last}

	return render_template('sensor2.html', **templateData)

@app.route("/sensor2/temperature", methods=['GET', 'POST'])
def sensor2Temp():
	names, temps, hums, timestamps = last12hours('sensor2')
	#name_last, temp_last, hum_last, timestamp_last, = lastReading()

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

		names, temps, hums, timestamps = selectDay('sensor2', str(selectedDate))

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
	names, temps, hums, timestamps = last12hours('sensor2')
	#name_last, temp_last, hum_last, timestamp_last, = lastReading()

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

		names, temps, hums, timestamps = selectDay('sensor2', str(selectedDate))

		templateData = {'names':names,
						'temps':temps,
						'hums':hums,
						'timestamps':timestamps,
						'selectedDate':selectedDate,
						'name_last':names[-1]}

		return render_template('fullDayHum.html', **templateData)

	return render_template('sensor2Hum.html', **templateData)


@app.route("/sensor3")
def sensor3():
	name_last, temp_last, hum_last, timestamp_last, = lastReading('sensor3')
	templateData = {'name_last':name_last,
					'temp_last':temp_last,
					'hum_last':hum_last,
					'timestamp_last':timestamp_last}

	return render_template('sensor3.html', **templateData)

@app.route("/sensor3/temperature", methods=['GET', 'POST'])
def sensor3Temp():
	names, temps, hums, timestamps = last12hours('sensor3')
	#name_last, temp_last, hum_last, timestamp_last, = lastReading()

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

		names, temps, hums, timestamps = selectDay('sensor3', str(selectedDate))

		templateData = {'names':names,
						'temps':temps,
						'hums':hums,
						'timestamps':timestamps,
						'selectedDate':selectedDate,
						'name_last':names[-1]}

		return render_template('fullDayTemp.html', **templateData)

	return render_template('sensor3Temp.html', **templateData)


@app.route("/sensor3/humidity", methods=['GET', 'POST'])
def sensor3Hum():
	names, temps, hums, timestamps = last12hours('sensor3')
	#name_last, temp_last, hum_last, timestamp_last, = lastReading()

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

		names, temps, hums, timestamps = selectDay('sensor3', str(selectedDate))

		templateData = {'names':names,
						'temps':temps,
						'hums':hums,
						'timestamps':timestamps,
						'selectedDate':selectedDate,
						'name_last':names[-1]}

		return render_template('fullDayHum.html', **templateData)

	return render_template('sensor3Hum.html', **templateData)


@app.route("/sensor4")
def sensor4():
	name_last, temp_last, hum_last, timestamp_last, = lastReading('sensor4')
	templateData = {'name_last':name_last,
					'temp_last':temp_last,
					'hum_last':hum_last,
					'timestamp_last':timestamp_last}

	return render_template('sensor4.html', **templateData)

@app.route("/sensor4/temperature", methods=['GET', 'POST'])
def sensor4Temp():
	names, temps, hums, timestamps = last12hours('sensor4')
	#name_last, temp_last, hum_last, timestamp_last, = lastReading()

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

		names, temps, hums, timestamps = selectDay('sensor4', str(selectedDate))

		templateData = {'names':names,
						'temps':temps,
						'hums':hums,
						'timestamps':timestamps,
						'selectedDate':selectedDate,
						'name_last':names[-1]}

		return render_template('fullDayTemp.html', **templateData)

	return render_template('sensor4Temp.html', **templateData)


@app.route("/sensor4/humidity", methods=['GET', 'POST'])
def sensor4Hum():
	names, temps, hums, timestamps = last12hours('sensor4')
	#name_last, temp_last, hum_last, timestamp_last, = lastReading()

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

		names, temps, hums, timestamps = selectDay('sensor4', str(selectedDate))

		templateData = {'names':names,
						'temps':temps,
						'hums':hums,
						'timestamps':timestamps,
						'selectedDate':selectedDate,
						'name_last':names[-1]}

		return render_template('fullDayHum.html', **templateData)

	return render_template('sensor4Hum.html', **templateData)


@app.route("/sensor5")
def sensor5():
	name_last, temp_last, hum_last, timestamp_last, = lastReading('sensor5')
	templateData = {'name_last':name_last,
					'temp_last':temp_last,
					'hum_last':hum_last,
					'timestamp_last':timestamp_last}

	return render_template('sensor5.html', **templateData)

@app.route("/sensor5/temperature", methods=['GET', 'POST'])
def sensor5Temp():
	names, temps, hums, timestamps = last12hours('sensor5')
	#name_last, temp_last, hum_last, timestamp_last, = lastReading()

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

		names, temps, hums, timestamps = selectDay('sensor5', str(selectedDate))

		templateData = {'names':names,
						'temps':temps,
						'hums':hums,
						'timestamps':timestamps,
						'selectedDate':selectedDate,
						'name_last':names[-1]}

		return render_template('fullDayTemp.html', **templateData)

	return render_template('sensor5Temp.html', **templateData)


@app.route("/sensor5/humidity", methods=['GET', 'POST'])
def sensor5Hum():
	names, temps, hums, timestamps = last12hours('sensor5')
	#name_last, temp_last, hum_last, timestamp_last, = lastReading()

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

		names, temps, hums, timestamps = selectDay('sensor5', str(selectedDate))

		templateData = {'names':names,
						'temps':temps,
						'hums':hums,
						'timestamps':timestamps,
						'selectedDate':selectedDate,
						'name_last':names[-1]}

		return render_template('fullDayHum.html', **templateData)

	return render_template('sensor5Hum.html', **templateData)

if __name__ == "__main__":
	if rpi is True:
		t1 = threading.Thread(target=cpuTempLog)
		t1.start()
	app.run(host='0.0.0.0', port=80, debug=True)

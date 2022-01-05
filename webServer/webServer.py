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
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import os, sqlite3, io
from flask import Flask, render_template, send_file, make_response, request, Response


app = Flask(__name__)


# Retrieve LAST data from database
def getLastData():
	conn = sqlite3.connect('../sensor1Data.db', check_same_thread=False)
	curs = conn.cursor()
	for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"):
		name = str(row[0])
		time = str(row[1])
		temp = row[2]
		hum = row[3]
	conn.close()
	return name, time, temp, hum

# Get Max number of rows (table size)
def maxRowsTable():
	conn = sqlite3.connect('../sensor1Data.db', check_same_thread=False)
	curs = conn.cursor()
	for row in curs.execute("select COUNT(temp) from  DHT_data"):
		maxNumberRows=row[0]
	conn.close()
	return maxNumberRows

# Get 'x' samples of historical data
def getHistData (numSamples):
	conn = sqlite3.connect('../sensor1Data.db', check_same_thread=False)
	curs = conn.cursor()
	curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	names = []
	dates = []
	temps = []
	hums = []
	for row in reversed(data):
		names.append(row[0])
		dates.append(row[1])
		temps.append(row[2])
		hums.append(row[3])
	conn.close()
	return names, dates, temps, hums

# Retrieve LAST data from database
def getLastData2():
	conn = sqlite3.connect('../sensor2Data.db', check_same_thread=False)
	curs = conn.cursor()
	for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"):
		name = str(row[0])
		time = str(row[1])
		temp = row[2]
		hum = row[3]
	conn.close()
	return name, time, temp, hum

# Get 'x' samples of historical data
def getHistData2(numSamples):
	conn = sqlite3.connect('../sensor2Data.db', check_same_thread=False)
	curs = conn.cursor()
	curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	names = []
	dates = []
	temps = []
	hums = []
	for row in reversed(data):
		names.append(row[0])
		dates.append(row[1])
		temps.append(row[2])
		hums.append(row[3])
	conn.close()
	return names, dates, temps, hums

# define and initialize global variables
global numSamples
numSamples = maxRowsTable()
if (numSamples > 145):
        numSamples = 144

global rangeTime
rangeTime = 100


# main route 
@app.route("/")
def index():
	return render_template('index.html')
	

@app.route("/sensor1")
def sensor1():
	name, time, temp, hum = getLastData()
	templateData = {'name':name, 'time':time, 'temp':temp, 'hum':hum}

	return render_template('sensor1.html', **templateData)
	
@app.route("/sensor2")
def sensor2():
	name, time, temp, hum = getLastData2()
	templateData = {'name':name, 'time':time, 'temp':temp, 'hum':hum}

	return render_template('sensor2.html', **templateData)

@app.route('/sensor1/plot/hum')
def plot_hum():
	name, times, temps, hums = getHistData(numSamples)
	ys = hums
	xs = range(numSamples)
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_ylabel('Humidity')
	axis.set_xlabel('Samples')
	axis.plot(xs, ys)
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')

@app.route('/sensor1/plot/temp')
def plot_temp():
	name, times, temps, hums = getHistData(numSamples)
	ys = temps
	xs = range(numSamples)
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_ylabel('Temperature')
	axis.set_xlabel('Samples')
	axis.plot(xs, ys)
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')

@app.route('/sensor2/plot/hum')
def plot_hum2():
	name, times, temps, hums = getHistData2(numSamples)
	ys = hums
	xs = range(numSamples)
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_ylabel('Humidity')
	axis.set_xlabel('Samples')
	axis.plot(xs, ys)
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')

@app.route('/sensor2/plot/temp')
def plot_temp2():
	name, times, temps, hums = getHistData2(numSamples)
	ys = temps
	xs = range(numSamples)
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_ylabel('Temperature')
	axis.set_xlabel('Samples')
	axis.plot(xs, ys)
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)

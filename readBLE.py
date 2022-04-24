#!/usr/bin/env python3
from datetime import datetime
import time, logging, threading, sqlite3, sys
import bluetooth._bluetooth as bluez
from py_bluetooth_utils.bluetooth_utils import (toggle_device, enable_le_scan, parse_le_advertising_events, disable_le_scan, raw_packet_to_str)


# Use 0 for hci0
dev_id = 0
toggle_device(dev_id, True)
sensor1_db = 'sensor1Data.db'
sensor2_db = 'sensor2Data.db'
sampleFreq = 150 # time in seconds ==> Sample every 10 min
name = None
temp = None
hum = None
last = None
cache = [None, None]
print(time.time())
try:
    sock = bluez.hci_open_dev(dev_id)
except:
    print("Cannot open bluetooth device %i" % dev_id)
    raise

# Set filter to "True" to see only one packet per device
enable_le_scan(sock, filter_duplicates=False)

def temp_1_handler(mac, adv_type, data, rssi):
	global dbname, sampleFreq, name, temp, hum
	data_str = raw_packet_to_str(data)
	# Check for ATC preamble
	if data_str[6:10] == '1a18':
		temp = int(data_str[22:26], 16) / 10
		hum = int(data_str[26:28], 16)
		batt = int(data_str[28:30], 16)
		if mac == "A4:C1:38:19:B4:32":
			name = "In Portacom"
			getData_1()

def temp_2_handler(mac, adv_type, data, rssi):
	global dbname, sampleFreq, name2, temp2, hum2
	data_str = raw_packet_to_str(data)
	# Check for ATC preamble
	if data_str[6:10] == '1a18':
		temp2 = int(data_str[22:26], 16) / 10
		hum2 = int(data_str[26:28], 16)
		batt2 = int(data_str[28:30], 16)
		if mac == "A4:C1:38:A4:8C:2C":
			name2 = "Under Portacom"
			getData_2()

def getData_1():
	global name, temp, hum
	# Called on new LE packet
	print(datetime.now(), "Device: In Portacom - Saving into {}".format(sensor1_db))
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	current_date = now.strftime('%Y-%m-%d')
	conn=sqlite3.connect(sensor1_db)
	curs=conn.cursor()
	timestamp = datetime.now()
	curs.execute("INSERT INTO DHT_data values((?), (?), (?), (?), (?))", (name, temp, hum, current_time, current_date)) 
	conn.commit()
	conn.close()
	time.sleep(sampleFreq)
	
def getData_2():
	global name2, temp2, hum2
	# Called on new LE packet
	print(datetime.now(), "Device: Under Portacom - Saving into {}".format(sensor2_db))
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	current_date = now.strftime('%Y-%m-%d')
	conn=sqlite3.connect(sensor2_db)
	curs=conn.cursor()
	timestamp = datetime.now()
	curs.execute("INSERT INTO DHT_data values((?), (?), (?), (?), (?))", (name, temp, hum, current_time, current_date)) 
	conn.commit()
	conn.close()
	time.sleep(sampleFreq)

def temp_1():
	global sock
	parse_le_advertising_events(sock, handler=temp_1_handler, debug=False)
	
def temp_2():
	global sock
	parse_le_advertising_events(sock, handler=temp_2_handler, debug=False)
	

if __name__ == "__main__":
	t1 = threading.Thread(target=temp_1)
	t2 = threading.Thread(target=temp_2)
	t1.start()
	t2.start()
	#parse_le_advertising_events(sock, handler=le_advertise_packet_handler, debug=False)

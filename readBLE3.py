#!/usr/bin/env python3
import sys, sqlite3, time, json
import bluetooth._bluetooth as bluez
from datetime import datetime
from py_bluetooth_utils.bluetooth_utils import (toggle_device, enable_le_scan,
                             parse_le_advertising_events,
                             disable_le_scan, raw_packet_to_str)



 
# Opening JSON file
with open('locations.json') as json_file:
    data = json.load(json_file)

macs = data['macs']
tables = data['names']

# Use 0 for hci0
dev_id = 0
toggle_device(dev_id, True)
sampleFreq = 75 # time in seconds ==> Sample every 10 min
database = 'loggedData.db'
 
try:
    sock = bluez.hci_open_dev(dev_id)
except:
    print("Cannot open bluetooth device %i" % dev_id)
    raise

# Set filter to "True" to see only one packet per device
enable_le_scan(sock, filter_duplicates=False)
 
try:

    def saveDB(name, temp, hum, table):
        # Saves gathered data into database
        #print(datetime.now(), "Device:", name, "- Saving into {}".format(database))
        now = datetime.now()
        rounded_timestamp = now.replace(microsecond=0)
        conn=sqlite3.connect(database)
        curs=conn.cursor()
        curs.execute("INSERT INTO {} values((?), (?), (?), (?))".format(table), (name, temp, hum, rounded_timestamp)) 
        conn.commit()
        conn.close()
        time.sleep(sampleFreq)


    def le_advertise_packet_handler(mac, adv_type, data, rssi):
        data_str = raw_packet_to_str(data)
        # Check for ATC preamble
        if data_str[6:10] == '1a18':
            temp = int(data_str[22:26], 16) / 10
            hum = int(data_str[26:28], 16)
            batt = int(data_str[28:30], 16)
            for key, value in macs.items():

                if mac == key:
                    name = value
                    for key, value in tables.items():
                        if mac == key:
                            table = value
                    saveDB(name, temp, hum, table)
            #print(name, temp, hum, batt)
            print("%s - Device: %s Temp: %sc Humidity: %s%% Batt: %s%%" % \
                 (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, temp, hum, batt))


 
    # Called on new LE packet
    parse_le_advertising_events(sock,
                                handler=le_advertise_packet_handler,
                                debug=False)
# Scan until Ctrl-C
except KeyboardInterrupt:
    disable_le_scan(sock)

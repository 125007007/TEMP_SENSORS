#!/usr/bin/env python3
import sys, sqlite3
from datetime import datetime
import bluetooth._bluetooth as bluez
 
from bluetooth_utils import (toggle_device, enable_le_scan,
                             parse_le_advertising_events,
                             disable_le_scan, raw_packet_to_str)
 
# Use 0 for hci0
dev_id = 0
toggle_device(dev_id, True)
sensor1_db = 'sensor1.db'
sensor2_db = 'sensor2.db'
 
try:
    sock = bluez.hci_open_dev(dev_id)
except:
    print("Cannot open bluetooth device %i" % dev_id)
    raise

# Set filter to "True" to see only one packet per device
enable_le_scan(sock, filter_duplicates=False)
 
try:

    def saveDB(name, temp, hum, database):
        # Called on new LE packet
        print(datetime.now(), "Device:", name, "- Saving into {}".format(database))
        now = datetime.now()
        rounded_timestamp = now.replace(microsecond=0)
        conn=sqlite3.connect(database)
        curs=conn.cursor()
        curs.execute("INSERT INTO DHT_data values((?), (?), (?), (?))", (name, temp, hum, rounded_timestamp)) 
        conn.commit()
        conn.close()

    def le_advertise_packet_handler(mac, adv_type, data, rssi):
        data_str = raw_packet_to_str(data)
        # Check for ATC preamble
        if data_str[6:10] == '1a18':
            temp = int(data_str[22:26], 16) / 10
            hum = int(data_str[26:28], 16)
            batt = int(data_str[28:30], 16)
            if mac == "A4:C1:38:19:B4:32":
                name = "In Portacom"
                saveDB(name, temp, hum, sensor1_db)
            elif mac == "A4:C1:38:A4:8C:2C":
                name = "Under Portacom"
                saveDB(name, temp, hum, sensor2_db)
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

#!/usr/bin/env python3
import sys, sqlite3, time, json, time
import bluetooth._bluetooth as bluez
from datetime import datetime
from py_bluetooth_utils.bluetooth_utils import (toggle_device, enable_le_scan,
                             parse_le_advertising_events,
                             disable_le_scan, raw_packet_to_str)


# Opening JSON file
with open('locations.json') as json_file:
    data = json.load(json_file)

macs = data['macs']

# Use 0 for hci0
dev_id = 0
toggle_device(dev_id, True)
 
try:
    sock = bluez.hci_open_dev(dev_id)
except:
    print("Cannot open bluetooth device %i" % dev_id)
    raise

# Set filter to "True" to see only one packet per device
enable_le_scan(sock, filter_duplicates=False)
 
try:

    def le_advertise_packet_handler(mac, adv_type, data, rssi):
        data_str = raw_packet_to_str(data)
        # Check for ATC preamble
        if data_str[6:10] == '1a18':
            temp = int(data_str[22:26], 16) / 10
            hum = int(data_str[26:28], 16)
            batt = int(data_str[28:30], 16)
            for key, value in macs.items():

                if mac == key:
    
                    print("%s - Device: %s Temp: %sc Humidity: %s%% Batt: %s%%" % \
                        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), value, temp, hum, batt))
                else:
                    #print(name, temp, hum, batt)
                    print("%s - Device: %s Temp: %sc Humidity: %s%% Batt: %s%%" % \
                    (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), mac, temp, hum, batt))
        


 
    # Called on new LE packet
    parse_le_advertising_events(sock,
                                handler=le_advertise_packet_handler,
                                debug=False)
# Scan until Ctrl-C
except KeyboardInterrupt:
    disable_le_scan(sock)

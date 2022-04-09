# TEMP_SENSORS

## Installation Instructions


```bash
sudo apt install python3-gpiozero
sudo apt-get install python3-dev python3-rpi.gpio
git clone https://github.com/125007007/TEMP_SENSORS.git
cd TEMP_SENSORS
sudo python3 installer.py
```

To run the Bluetooth reader
```bash
sudo python3 readBLE.py
```

To run server
```bash
cd webServer
sudo python3 webServer.py
```

## Create service for BLE reader.

Create file for the service and include the code below.

```bash
sudo nano /etc/systemd/system/readBLE.service
```

```ini
[Unit]
Description= read ble data and stores in a database

[Service]
User=root
WorkingDirectory=/home/ubuntu/TEMP_SENSORS/
ExecStart=python3 readBLE.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then run these commands
```bash
sudo systemctl daemon-reload
sudo systemctl enable readBLE.service
sudo systemctl start readBLE.service
sudo systemctl status readBLE.service
```

## Create service for web server.

Create file for the service and include the code below.
```bash
sudo nano /etc/systemd/system/webServer.service
```

```ini
[Unit]
Wants=network-online.target
After=network-online.target
Description= web server for displaying temp data from database

[Service]
User=root
WorkingDirectory=/home/ubuntu/TEMP_SENSORS/webServer/
ExecStart=python3 webServer.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then run these commands
```bash
sudo systemctl daemon-reload
sudo systemctl enable webServer.service
sudo systemctl start webServer.service
sudo systemctl status webServer.service
```

import os
from time import sleep

os.system('sudo apt-get install bluetooth libbluetooth-dev sqlite3')
os.system('sudo pip3 install -r requirements.txt')
sleep(0.5)
print('Creating Databases')
os.system('python3 createDatabases.py')
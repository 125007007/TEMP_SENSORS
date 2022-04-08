import sqlite3
conn=sqlite3.connect('sensorData.db')
curs=conn.cursor()

print ("\nLast raw Data logged on database:\n")
for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"):
    print ("Name = "+str(row[0]), str(row[1])+ " ==> Temp = "+str(row[2])+"	Hum ="+str(row[3]))

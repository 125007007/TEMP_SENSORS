import sqlite3, os, time
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_connection('serverCPU.db')
    create_connection('sensor1.db')
    create_connection('sensor2.db')
    time.sleep(0.5)
    os.system('python3 createTable.py')
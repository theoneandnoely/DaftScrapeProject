import sqlite3
from os.path import exists

def initialise_db():
    if exists('daft_data.db'):
        raise RuntimeError('Tried to Initialise Database which already exists.')
    conn = sqlite3.connect('daft_data.db')
    curs = conn.cursor()
    curs.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT);")
    curs.execute("CREATE TABLE properties (daft_id TEXT, sent_to TEXT, num_beds INTEGER, price REAL, latitude REAL, longitude REAL, applied INTEGER);")
    conn.close()

if __name__ == "__main__":
    initialise_db()
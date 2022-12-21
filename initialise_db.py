import sqlite3
from os.path import exists

def initialise_db():
    '''
    Initialises the daft_data.db database with the properties and users tables and correct columns

    INPUT:
    None

    OUTPUT:
    None
    '''
    # Raise error if database already exists
    if exists('daft_data.db'):
        raise RuntimeError('Tried to Initialise Database which already exists.')
    # Connect to database. Creates a database if none exist.
    conn = sqlite3.connect('daft_data.db')
    
    #Initialise cursor to execute SQL queries
    curs = conn.cursor()
    
    # Create users table with id, name, and email columns
    curs.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT);")

    # Create properties table with daft_id, sent_to, num_beds, price, latitude, longitude, and applied columns
    curs.execute("CREATE TABLE properties (daft_id TEXT, sent_to TEXT, num_beds INTEGER, price REAL, latitude REAL, longitude REAL, applied INTEGER);")
    
    # Close connection
    conn.close()

if __name__ == "__main__":
    initialise_db()
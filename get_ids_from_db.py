import sqlite3
import pandas as pd

def get_ids_from_db() -> list[str]:
    '''
    Returns a list of the daft IDs which have already been scraped.

    INPUT:
    None

    OUTPUT:
    - ids (list): List of daft_ids which have already been scraped.
    '''
    # Connect to daft_data.db
    conn = sqlite3.connect('daft_data.db')

    # Pull daft_id data from properties table and save in a pandas DataFrame
    df = pd.read_sql_query("SELECT daft_id FROM properties;", conn)

    # Close connection
    conn.close()

    # Return the values of daft_id as a list
    return df['daft_id'].to_list()

if __name__ == "__main__":
    ids = get_ids_from_db()
    print(ids)
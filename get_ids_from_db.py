import sqlite3
import pandas as pd

def get_ids_from_db():
    conn = sqlite3.connect('daft_data.db')
    df = pd.read_sql_query("SELECT daft_id FROM properties;", conn)
    conn.close()
    return df['daft_id'].to_list()

if __name__ == "__main__":
    ids = get_ids_from_db()
    print(ids)
import sqlite3

class DataBaseError(Exception):
    pass

def get_template_response(user: str) -> str:
    '''
    Get the template which is saved for user in the users table of the database and return as a string.

    INPUT:
    - user (str): The user who's template should be returned. Can be id, name, or email.

    OUTPUT:
    - template (str): The template store in the database for user.
    '''
    # Check if the user string is an id, name, or user
    if '@' in user:
        user_type = 'email'
    elif user.isdigit():
        user_type = 'id'
    else:
        user_type = 'name'
    
    # Connect to daft_data.db database and set up cursor
    conn = sqlite3.connect('daft_data.db')
    curs = sqlite3.Cursor(conn)

    # Check if template column exists in users table
    curs.execute('PRAGMA table_info(users)')
    users_cols = curs.fetchall()
    if any(row[1]=='template' for row in users_cols) == False:
        raise DataBaseError("No 'template' column found in users table.")

    # Return the template from users table
    query = f'SELECT template FROM users WHERE {user_type}="{user}"'

    curs.execute(query)
    template = curs.fetchone()[0]

    # Close curson and connection
    curs.close()
    conn.close()

    return template

if __name__ == "__main__":
    get_template_response('test')
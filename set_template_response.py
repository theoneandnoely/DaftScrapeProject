import sqlite3
import pandas as pd
from initialise_db import initialise_db
from os.path import exists
import argparse
import urllib.parse

class FileTypeError(Exception):
    pass

class UserExistenceError(Exception):
    pass

def set_template_response(user: str, filepath: str):
    '''
    Set the default template response, which can be dynamically populated with relevant property details to be copied and pasted into application, from txt file. Store response in users table of database.

    INPUT:
    - user (str): The user who should be populated. This can be their email, username, or user id.
    - filepath (str): The filepath for the txt file containing the template.

    OUTPUT:
    None
    '''


    # Check if filepath is a .txt file
    if ".txt" in filepath == False:
        raise FileTypeError("Input file must be a .txt file")
    else:
        with open(filepath, 'r', encoding='utf-8') as f:
            contents = f.read()
            print(f'File Contents:\n{contents}\n\n')
    
    url_encoded_contents = urllib.parse.quote(contents)
    formatted_contents = url_encoded_contents.replace('%7B', '{').replace('%7D', '}')
    print(f'Parsed contents:\n{formatted_contents}\n\n')
    
    # Initialise database if this doesn't already exist
    if exists('daft_data.db') == False:
        initialise_db()
        print('Database initialised')
    
    # Connect to database and set the cursor
    conn = sqlite3.connect('daft_data.db')
    curs = sqlite3.Cursor(conn)

    # Pull data from users table
    users_df = pd.read_sql_query("SELECT * FROM users", conn)
    print(f'Old users_df:\n{users_df[users_df["email"] == user]["template"][0]}\n\n')
    
    # Check if user exists in users table
    if user in users_df['id'] == False and user in users_df['name'] == False and user in users_df['email'] == False:
        raise UserExistenceError("User Does not already exist in database. Please run add_user_db.py --email <your email address> to add the user before running this file.")

    # Check if template column exists in users table, add it to DataFram if not, and update the template value for the relevant user with the contents of filepath
    if 'template' in users_df.columns:
        if '@' in user:
            users_df.loc[users_df['email'] == user, 'template'] = formatted_contents
        elif user.isdigit():
            users_df.loc[users_df['id'] == user, 'template'] = formatted_contents
        else:
            users_df.loc[users_df['name'] == user, 'template'] = formatted_contents
    else:
        users_df = users_df.assign({'template':''})
        if '@' in user:
            users_df.loc[users_df['email'] == user, 'template'] = formatted_contents
        elif user.isdigit():
            users_df.loc[users_df['id'] == user, 'template'] = formatted_contents
        else:
            users_df.loc[users_df['name'] == user, 'template'] = formatted_contents

    print(f'Updated users_df:\n{users_df[users_df["email"] == user]["template"][0]}\n\n')

    # Replace the users table with the data in users_df
    users_df.to_sql('users', conn, if_exists='replace', index=False)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    # Initialise Argument Parser to accept command line arguments
    parser = argparse.ArgumentParser()

    # Add the arguments for user and file
    parser.add_argument("--user", type=str, required=True, help="The user to set the template for. This can be the username, email, or user id")
    parser.add_argument("--file", type=str, required=True, help="Filepath of the .txt file containing the template to be added")

    args = parser.parse_args()

    # Set the variables using the command line specified arguments
    user = args.user
    file = args.file

    # Run the set_template function and log once completed
    set_template_response(user, file)
    print(f"Template has been updated for {user}")
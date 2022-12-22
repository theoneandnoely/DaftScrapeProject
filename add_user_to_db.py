import sqlite3
import pandas as pd
import argparse
from os.path import exists
from initialise_db import initialise_db
from set_template_response import FileTypeError

def add_user_to_db(email:str, file:str="") -> None:
    '''
    Adds user to users table of database

    INPUT:
    email (str): email address of user to add to db

    OUTPUT:
    None
    '''
    if file == "":
        template = ""
    elif '.txt' in file == False:
        raise FileTypeError("Template file must be a .txt file")
    else:
        with open(file, 'r', encoding='utf-8') as f:
            template = f.read()

    # Check if database exists. If not, initialise db.
    if exists('daft_data.db') == False:
        initialise_db()
        print('Database Initialised.')

    # Connect to sql database
    conn = sqlite3.connect('daft_data.db')

    # Pull all data from users table
    users_df = pd.read_sql_query("SELECT * FROM users;", conn)

    # Get the maximum value of 'id' from the table or set to 0
    if len(users_df['id']) == 0:
        max_id = 0
    else:
        max_id = users_df['id'].max()

    if len(users_df['id']) == 0:
        users_df = pd.DataFrame([[max_id+1, email.split('@')[0], email, template]], columns=['id', 'name', 'email', 'template'])
    elif email in list(users_df['email']) == False:
        users_df = pd.concat([users_df, pd.DataFrame([max_id+1, email.split('@')[0], email, template], columns=['id', 'name', 'email', 'template'])], ignore_index=True)
    else:
        print(f'{email} is already in database.\nID:\t{users_df[users_df["email"]==email]["id"]}\nName:\t{users_df[users_df["email"]==email]["name"]}')

    # Replace users table with updated users table
    users_df.to_sql('users', conn, if_exists='replace', index=False)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    # Initialise Argument Parser
    parser = argparse.ArgumentParser()

    # Add the --email argument
    parser.add_argument("--email", type=str, required=True, help="Email Address of user to add")
    parser.add_argument("--template", type=str, required=False, default="", help="(Optional) Filepath of .txt file containing template for applications")

    # Parse the Arguments
    args = parser.parse_args()

    # Set the email variable to the specified argument and run add_user_to_db function
    email = args.email
    if hasattr(args, 'template'):
        add_user_to_db(email, args.template)
    else:
        add_user_to_db(email)
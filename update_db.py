import sqlite3
import pandas as pd

def update_db(properties: list, sent_to: list, num_beds: str):
    '''
    Connects to the daft_data.db database and udpates the properties and users tables with new data.

    INPUT:
    - properties (list): List of dictionaries for each property to add to the database. Each dictionary contains the daft_id, link, address, price, latitude, and longitude for the property.
    - sent_to (list): List of recipient email addresses the property ads were sent to.
    - num_beds (str): Number of beds in the properties.

    OUTPUT:
    None
    '''

    # Connect to the SQLite database
    conn = sqlite3.connect('daft_data.db')

    # Pull all of the current data from properties into a Pandas DataFrame
    old_properties_df = pd.read_sql_query("SELECT * FROM properties;", conn)

    # Initialise list for the new properties
    new_properties_list = []

    # Iterate through all properties in properties and append the values from each to new_properties_list to create a list of lists
    for property in properties:
        # Convert the string of €x per month (week) to a numerical float value. If price given weekly, obtain monthly equivalent
        if 'week' in property['price']:
            price = (float(property['price'].split('€')[1].split[' '][0].replace(',',''))*52)/12
        else:
            price = float(property['price'].split('€')[1].split(' ')[0].replace(',',''))
        
        for email in sent_to:
            new_properties_list.append([property['id'], email, num_beds, price, property['latitude'], property['longitude'], 0])
    
    # Convert list of lists to DataFrame with same columns as properties table
    new_properties_df = pd.DataFrame(new_properties_list, columns=['daft_id', 'sent_to', 'num_beds', 'price', 'latitude', 'longitude', 'applied'])
    
    # Concatenate the new values and the old values into a single DataFrame and replace the table with the updated version
    updated_properties_df = pd.concat([old_properties_df, new_properties_df], ignore_index=True)
    updated_properties_df.to_sql('properties', conn, if_exists = 'replace', index = False)

    # Pull all data from users table
    users_df = pd.read_sql_query("SELECT * FROM users;", conn)

    # Get the maximum value of 'id' from the table or set to 0
    if len(users_df['id']) == 0:
        max_id = 0
    else:
        max_id = users_df['id'].max()

    # Iterate through each email in the sent_to list and append the user if they don't already exist in the table, with the id as the maximum id + 1
    for email in sent_to:
        if len(users_df['id']) == 0:
            users_df = pd.DataFrame([[max_id+1, email.split('@')[0], email]], columns=['id', 'name', 'email'])
            max_id += 1
        elif email in list(users_df['email']) == False:
            users_df = pd.concat([users_df, pd.DataFrame([max_id+1, email.split('@')[0], email], columns=['id', 'name', 'email'])], ignore_index=True)
            max_id += 1
    
    # Replace users table with updated users table
    users_df.to_sql('users', conn, if_exists='replace', index=False)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    # Test for debugging
    update_db([{'id':'test-delete-from-db', 'price':'€2,200 per month', 'latitude':69.42069, 'longitude':-3.25108}], ['test@example.com'], '2')
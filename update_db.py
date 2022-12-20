import sqlite3
import pandas as pd

def update_db(properties, sent_to, num_beds):
    conn = sqlite3.connect('daft_data.db')
    old_properties_df = pd.read_sql_query("SELECT * FROM properties;", conn)
    new_properties_list = []
    for property in properties:
        if 'week' in property['price']:
            price = (float(property['price'].split('€')[1].split[' '][0].replace(',',''))*52)/12
        else:
            price = float(property['price'].split('€')[1].split(' ')[0].replace(',',''))
        for email in sent_to:
            new_properties_list.append([property['id'], email, num_beds, price, property['latitude'], property['longitude'], 0])
    new_properties_df = pd.DataFrame(new_properties_list, columns=['daft_id', 'sent_to', 'num_beds', 'price', 'latitude', 'longitude', 'applied'])
    updated_properties_df = pd.concat([old_properties_df, new_properties_df], ignore_index=True)
    updated_properties_df.to_sql('properties', conn, if_exists = 'replace', index = False)

    users_df = pd.read_sql_query("SELECT * FROM users;", conn)
    if len(users_df['id']) == 0:
        max_id = 0
    else:
        max_id = users_df['id'].max()
    for email in sent_to:
        if len(users_df['id']) == 0:
            users_df = pd.DataFrame([[max_id+1, email.split('@')[0], email]], columns=['id', 'name', 'email'])
            max_id += 1
        elif email in list(users_df['email']) == False:
            users_df = pd.concat([users_df, pd.DataFrame([max_id+1, email.split('@')[0], email], columns=['id', 'name', 'email'])], ignore_index=True)
            max_id += 1
    users_df.to_sql('users', conn, if_exists='replace', index=False)

    conn.close()

if __name__ == "__main__":
    update_db([{'id':'test-delete-from-db', 'price':'€2,200 per month', 'latitude':69.42069, 'longitude':-3.25108}], ['test@example.com'], '2')
from bs4 import BeautifulSoup
import requests
import time
import argparse
from get_coords import get_coords
from send_daft_email import send_daft_email
from os.path import exists
from initialise_db import initialise_db
from get_ids_from_db import get_ids_from_db
from update_db import update_db
import ast
import datetime


def scrape_daft(num_beds: str, max_price: str) -> list[dict]:
    '''
    Function to connect to daft.ie, scrape the most recent properties with a specified max price and number of beds, and return the details in a list of dictionaries

    INPUT:
    - num_beds (str): The number of beds required for the property.
    - max_price (str): The maximum rental price for the property. String must be in the form of numeric digits with no commas (i.e. '2000' and not '2,000')

    OUTPUT:
    - properties (list): List of dictionaries relating to each property scraped. Each dictionary contains the daft_id, link, address, price, latitude, and longitude for the property.
    '''

    # Construct URL from the base url, max_price, and num_beds
    url = 'https://www.daft.ie/property-for-rent/dublin-city?rentalPrice_to='+max_price+'&numBeds_from='+num_beds+'&numBeds_to='+num_beds+'&sort=publishDateDesc'
    
    # Request and Parse the page
    with requests.get(url) as page:
        soup = BeautifulSoup(page.text, "html.parser")

    # Find list of all property ads on the page
    results = soup.find('ul', attrs={"data-testid":"results"})

    # If the daft_data.db database does not yet exist, initialise this first
    if exists('daft_data.db') == False:
        initialise_db()
        print('Database Intitialised')

    # Get list of ids which have already been scraped and an email notification sent for
    sent_ids = get_ids_from_db()

    # initialise properties list and counter
    properties = []
    counter = 0

    # iterate through all property ads scraped
    for list_item in results.find_all('li'):

        id = list_item['data-testid']
        link = list_item.find('a').get('href')
        address = list_item.find('p', attrs={"data-testid":"address"}).text
        price = list_item.find('div', attrs={"data-testid":"price"}).span.text

        # If an id has previously been scraped or the counter reaches 10, stop iterating and return properties. Otherwise, append the values to properties and continue iterating
        if id in sent_ids or counter == 10:
            return properties
        else:
            lat, lon = get_coords(address)
            properties.append({'id':id, 'link':'https://www.daft.ie'+link, 'address':address, 'price':price, 'latitude':lat, 'longitude':lon})
            counter += 1
    return properties



if __name__ == '__main__':

    # Initialise Argument Parser for command line
    parser = argparse.ArgumentParser()

    # Add arguments for user to specify the number of beds, max_price, and email recipients from the command line
    parser.add_argument('--beds', type=str, required=True, help='The number of beds in the properties to scrape for')
    parser.add_argument('--max_price', type=str, required=True, help='The maximum price of the properties to scrape for')
    parser.add_argument('--email', type=str, required=True, help='List of the email addresses to notify eg. ["myemail@example.com","youremail@example.com"]')

    args = parser.parse_args()
    
    # set variables to the user specified arguments
    num_beds = args.beds
    max_price = args.max_price
    to = args.email

    # Change 'to' variable to a list of strings
    to = ast.literal_eval(to)

    # Command will run continuously until interrupted
    while True:
        # Call scrape_daft for the user specified values
        links = scrape_daft(num_beds, max_price)
        
        # Log number of properties found at each loop to the screen
        print(f'{str(len(links))} Properties found for {max_price} or less with {num_beds} beds @ {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.')
        
        # If scrape_daft returns new properties in the correct range, send an email notification and update the database tables
        if len(links) > 0:
            send_daft_email(links, to, num_beds)
            update_db(links, to, num_beds)

        # Wait 5 minutes
        time.sleep(300)
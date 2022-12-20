from bs4 import BeautifulSoup
import requests
import time
import argparse
from get_coords import get_coords
from send_daft_email import sendDaftEmail
from os.path import exists
from initialise_db import initialise_db
from get_ids_from_db import get_ids_from_db
from update_db import update_db
import ast


def scrape_daft(num_beds, max_price):
    url = 'https://www.daft.ie/property-for-rent/dublin-city?rentalPrice_to='+max_price+'&numBeds_from='+num_beds+'&numBeds_to='+num_beds+'&sort=publishDateDesc'
    with requests.get(url) as page:
        soup = BeautifulSoup(page.text, "html.parser")
    results = soup.find('ul', attrs={"data-testid":"results"})
    if exists('daft_data.db') == False:
        print('Database to be Initialised')
        initialise_db()
        print('Database Intitialised')
    else:
        print(f'Database exists = {exists("daft_data.db")}')
    sent_ids = get_ids_from_db()
    properties = []
    counter = 0
    for list_item in results.find_all('li'):
        id = list_item['data-testid']
        link = list_item.find('a').get('href')
        address = list_item.find('p', attrs={"data-testid":"address"}).text
        price = list_item.find('div', attrs={"data-testid":"price"}).span.text
        if id in sent_ids or counter == 10:
            return properties
        else:
            lat, lon = get_coords(address)
            properties.append({'id':id, 'link':'https://www.daft.ie'+link, 'address':address, 'price':price, 'latitude':lat, 'longitude':lon})
            counter += 1
    return properties



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--beds', type=str, required=True, help='The number of beds in the properties to scrape for')
    parser.add_argument('--max_price', type=str, required=True, help='The maximum price of the properties to scrape for')
    parser.add_argument('--email', type=str, required=True, help='List of the email addresses to notify eg. ["myemail@example.com","youremail@example.com"]')

    args = parser.parse_args()
    
    num_beds = args.beds
    max_price = args.max_price
    to = args.email
    to = ast.literal_eval(to)

    print(f'Args:\nnum_beds - {num_beds}\nmax_price - {max_price}\nemail - {to}')

    #while True:
    links = scrape_daft(num_beds, max_price)
    print(f'{str(len(links))} Properties found for {max_price} or less with {num_beds} beds.')
    if len(links) > 0:
        sendDaftEmail(links, to, num_beds)
        update_db(links, to, num_beds)


        # Wait 5 minutes
        #time.sleep(300)
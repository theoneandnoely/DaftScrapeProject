from os import getenv
import requests
import json

def get_coords(address: str):
    '''
    Uses positionstack.com API to determine latitude and longitude coordinates based on the address in the daft ad.

    INPUT:
    - address (str): Address to query as a string

    OUTPUT:
    - latitude (float): Degrees North of the equator as a float (negative numbers equal south of equator)
    - longitude (float): Degrees East of Prime Meridian as float (negative numebers equal west of Prime Meridian)
    '''
    # Get API key which has been saved to environment variable POS_STACK_KEY and construct URL with this, the base url, and the address
    api_key = getenv('POS_STACK_KEY')
    url = f'http://api.positionstack.com/v1/forward?access_key={api_key}&query={address}&country=IE&region=Dublin&fields=results.latitude,results.longitude'
    
    with requests.get(url) as response:
        data = json.loads(response.text)

    # Check to see if the response has actually provided coordinates for the address
    if len(data["data"]) == 0:
        print(f'No Coordinates for {address}.')
        # Make attempt with neighbourhood instead of full address
        altered_address = address.split(',')[1]
        url = f'http://api.positionstack.com/v1/forward?access_key={api_key}&query={altered_address}&country=IE&region=Dublin&fields=results.latitude,results.longitude'
        with requests.get(url) as response:
            data = json.loads(response.text)
        if len(data["data"]) == 0:
            print(f'No Coordinates for {altered_address} either.')
            return (0,0)
        else:
            return data["data"][0]["latitude"], data["data"][0]["longitude"]
    else:    
        return data["data"][0]["latitude"], data["data"][0]["longitude"]

if __name__ == "__main__":
    lat, lon = get_coords('71 Milltown Hall, Mount St Annes, Milltown, Dublin 6')
    print(lat)
    print(lon)
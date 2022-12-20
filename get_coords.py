from os import getenv
import requests
import json

def get_coords(address):
    api_key = getenv('POS_STACK_KEY')
    url = f'http://api.positionstack.com/v1/forward?access_key={api_key}&query={address}&country=IE&region=Dublin&fields=results.latitude,results.longitude'
    
    with requests.get(url) as response:
        data = json.loads(response.text)

    if len(data["data"]) == 0:
        print(f'No Coordinates for {address}.')
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
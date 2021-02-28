# Class responsible for pulling destination data from an existing google sheet.

import requests
import os
SHEETY_URL = os.getenv("SHEETY_URL")

class DataManager:
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_URL)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

# Update the IATA code in the google sheet if not already present
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_URL}/{city['id']}",
                json=new_data
            )
            print(response.text)



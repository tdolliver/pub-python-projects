# Class is responsible for talking to the Flight Search API.
import requests
from flight_data import FlightData
import os

class FlightSearch:
    def __init__(self):
        self.LOCATION_API_ENDPOINT = "https://tequila-api.kiwi.com"
        self.TEQUILA_API_KEY = os.getenv("TEQUILA_API_KEY")
        self.TEQUILA_SEARCH_API_KEY = os.getenv("TEQUILA_SEARCH_API_KEY")

    def get_iata_code(self, city_name):
        uri = "/locations/query"
        headers = {
            "apikey": self.TEQUILA_API_KEY
        }
        params = {
            "term": city_name,
            "limit": 1
        }

        response = requests.get(url=f"{self.LOCATION_API_ENDPOINT}{uri}", headers=headers, params=params)
        print(response)
        return response.json()['locations'][0]


    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {
            "apikey": self.TEQUILA_SEARCH_API_KEY
        }

        params = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD"

        }
        response = requests.get(url="https://tequila-api.kiwi.com/v2/search", headers=headers, params=params)
        data = response.json()["data"][0]

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data

# This program will pull information from an existing google sheet using sheety
# and check current flight prices compared to threshold set in the google sheet
# it will send an SMS with Twilio if current prices are lower then threshold

# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager
# classes to achieve the program requirements.


import data_manager
import flight_search
from datetime import datetime, timedelta
from notification_manager import NotificationManager

# Create new objects of each class
dm = data_manager.DataManager()
fs = flight_search.FlightSearch()
sheet_data = dm.get_destination_data()
notification_manager = NotificationManager()
print(sheet_data)

# Update the IATA code in the spreadsheet if not already present
for city in sheet_data:
    if city["iataCode"] == "":
        #print(f"No code for {city['city']}")
        city_details = fs.get_iata_code(city['city'])
        print(city_details['code'])
        city['iataCode'] = city_details['code']

        dm.destination_data = sheet_data
        dm.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

# Check each destination in the sheet and send an SMS if any flights are within budget
for destination in sheet_data:
    flight = fs.check_flights(
        "LON",
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    if flight.price < destination["lowestPrice"]:
        notification_manager.send_sms(
            message=f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        )

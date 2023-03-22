#!/usr/bin/env python

import requests
from datetime import datetime

# Prompt the user to enter the latitude and longitude of the location to check
latitude = input("Enter latitude: ")
longitude = input("Enter longitude: ")

# for testing
# latitude = 39.7456
# longitude = -97.0892

# todo: add check to make sure that latitude and longitude is in US
# todo: add an additional user input to request when to retrieve the forecast for
# todo: add an additional user input for user to request different parts of the forecast


# Send a request to the /points/{latitude},{longitude} endpoint to get the grid coordinates and office
url = f"https://api.weather.gov/points/{latitude},{longitude}"
headers = {"User-Agent": "WeatherForecastApp/1.0 (+https://example.com/)"}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Extract the grid coordinates URL, office, and grid X and Y coordinates from the JSON response
    data = response.json()
    grid_coords_url = data["properties"]["forecastGridData"]
    # office = data["properties"]["gridId"]
    # grid_x, grid = grid_coords_url.split("/")[-2:]

    # Send a request to the /gridpoints/{office}/{grid X},{grid Y}/forecast endpoint to get the forecast
    # forecast_url = f"https://api.weather.gov/gridpoints/{office}/{grid_x},{grid_y}/forecast"
    forecast_url = f"{grid_coords_url}/forecast"
    forecast_response = requests.get(forecast_url, headers=headers)

    # troubleshooting
    # print("Grid Coord:" + grid_coords_url)
    # print("Office:" + office)
    # print("Grid X:" + grid_x)
    # print("Grid Y:" + grid_y)
    # print(forecast_url)

    if forecast_response.status_code == 200:
        # Extract the forecast data from the JSON response for Wednesday night
        forecast_data = forecast_response.json()
        periods = forecast_data["properties"]["periods"]
        # Use str
        if datetime.now().strftime("%A") == "Wednesday":
            tonight = next((p for p in periods if "Tonight" in p["name"]), None)
            if tonight:
                print("Weather forecast for tonight (Wednesday night):", tonight["detailedForecast"])
            else:
                print("Failed to find weather forecast for tonight (Wednesday night).")
        else:
            wed_night = next((p for p in periods if "Wednesday Night" in p["name"]), None)
            if wed_night:
                print("Weather forecast for Wednesday night:", wed_night["detailedForecast"])
            else:
                print("Failed to find weather forecast for Wednesday night.")
    else:
        # Display an error message if the request to the /gridpoints/{office}/{grid X},{grid Y}/forecast endpoint fails
        print("Failed to get weather forecast:", forecast_response.status_code)
else:
    # Display an error message if the request to the /points/{latitude},{longitude} endpoint fails
    print("Failed to get grid coordinates and office:", response.status_code)


# todo: add logging
# todo: add gui
    # todo: add additional methods of location input, ie. map interaction, gps, etc.
# todo: improve error handling and proactive error checking
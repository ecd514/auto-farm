# Title:  Weather API Script
# Author: Aidan Kapuschinsky
# Description:
# This script documents a basic example of calling the Weather.gov api.
########################
import requests

api_urn = "https://api.weather.gov"  # Base location to access the weather api
weather_station = "BGM"  # Weather forecasting station 3 letter code
weather_station_xlocation = "63"  # X location in local WFO grid
weather_station_ylocation = "60"  # Y location in local WFO grid
api_url_forecast = "/gridpoints/"+weather_station+"/" + \
    weather_station_xlocation+","+weather_station_ylocation + \
    "/forecast"  # API location to call

api_forecast_results = requests.get(
    api_urn+api_url_forecast).json()  # Make API call

tomorrow_forecast_list = [api_forecast_results["properties"]["periods"] for api_forecast_results["properties"]["periods"]
                          # Search for results 12 hours from now
                          in api_forecast_results["properties"]["periods"] if api_forecast_results["properties"]["periods"]["number"] == 2]
# Since its a list of dicts, pull out the only dict entry
tomorrow_forecast = tomorrow_forecast_list[0]

print([tomorrow_forecast["probabilityOfPrecipitation"]["value"],
      tomorrow_forecast["temperature"], tomorrow_forecast["shortForecast"], tomorrow_forecast["startTime"]])

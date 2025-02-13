# Title:  Weather API Script
# Author: Aidan Kapuschinsky
# Description:
# This script documents a basic example of calling the Weather.gov api.
########################
import requests


class weather_forecast_data:

    def __init__(self, temp: float = 0, pcor: str = "empty-value", df: str = 'empty-value', i_url: str = 'empty-value', gen_time: str = 'empty-value', exp_time: str = 'empty-value'):
        self.temperature = temp
        self.chance_of_rain = pcor
        self.detailed_forecast = df
        self.icon_url = i_url
        self.generation_time = gen_time
        self.expiration_time = exp_time

    def getData(self):
        return [self.temperature, self.chance_of_rain, self.detailed_forecast]


def reqweather(api_urn="https://api.weather.gov", weather_station="BGM",
               weather_station_xlocation="63", weather_station_ylocation="60"):
    api_url_forecast = "/gridpoints/"+weather_station+"/" + \
        weather_station_xlocation+","+weather_station_ylocation+"/forecast"
    api_forecast_results = requests.get(
        api_urn+api_url_forecast).json()  # Make API call

    tomorrow_forecast_list = [api_forecast_results["properties"]["periods"]
                              for api_forecast_results["properties"]["periods"]
                              in api_forecast_results["properties"]["periods"]
                              if api_forecast_results["properties"]["periods"]
                              ["number"] == 2]

# Since its a list of dicts, pull out the only dict entry
    tomorrow_forecast = tomorrow_forecast_list[0]
#    if tomorrow_forecast["probabilityOfPrecipitation"]["value"] == ' None':
#        tomorrow_forecast["probabilityOfPrecipitation"]["value"] = '0'

    return weather_forecast_data(temp=tomorrow_forecast["temperature"],
                                 pcor=tomorrow_forecast["probabilityOfPrecipitation"]["value"],
                                 df=tomorrow_forecast["detailedForecast"],
                                 i_url=tomorrow_forecast["icon"],
                                 gen_time=tomorrow_forecast["generatedAt"],
                                 exp_time=tomorrow_forecast["updateTime"])

import requests


class weather_forecast_data:
    def __init__(self, temp: float = 0, pcor: int = 0, df: str = 'empty-value',
                 i_url: str = 'empty-value', gen_time: str = 'empty-value',
                 exp_time: str = 'empty-value'):
        self.temperature: float = temp
        self.chance_of_rain: int = int(pcor)  # Ensured input is already valid
        self.detailed_forecast: str = df
        self.icon_url = i_url
        self.generation_time = gen_time
        self.expiration_time = exp_time

    def getData(self):
        return {
            'temperature': self.temperature,
            'rain': self.chance_of_rain,
            'detailed_forecast': self.detailed_forecast
        }


def reqweather(api_urn="https://api.weather.gov", weather_station="BGM",
               weather_station_xlocation="63", weather_station_ylocation="60"):
    api_url_forecast = f"/gridpoints/{weather_station}/{
        weather_station_xlocation},{weather_station_ylocation}/forecast"
    api_forecast_results = requests.get(api_urn + api_url_forecast).json()

    # Fixed list comprehension to properly iterate through periods
    tomorrow_forecast_list = [
        period for period in api_forecast_results["properties"]["periods"]
        if period["number"] == 2
    ]

    # Handle case where no matching period found
    if not tomorrow_forecast_list:
        return weather_forecast_data()  # Return default values

    tomorrow_forecast = tomorrow_forecast_list[0]

    # Handle potential null values from API
    temp = tomorrow_forecast.get("temperature", 0)
    po_precip = tomorrow_forecast.get(
        "probabilityOfPrecipitation", {}).get("value", 0) or 0
    detailed_forecast = tomorrow_forecast.get(
        "detailedForecast", "No forecast available")

    return weather_forecast_data(
        temp=float(temp),
        pcor=int(po_precip),
        df=detailed_forecast,
        i_url=tomorrow_forecast.get("icon", ""),
        gen_time=api_forecast_results['properties'].get('generatedAt', '')
    ).getData()

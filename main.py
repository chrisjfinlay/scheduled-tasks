import requests, datetime, os
from twilio.rest import Client

# OpenWeather weather codes: https://openweathermap.org/api/weather-conditions#Weather-Condition-Codes-2

# OpenWeather setup
OPENWEATHER_API_KEY = os.environ.get("OWM_API_KEY")
lat=54.154331
lon=-4.480060
# endpoint = "https://api.openweathermap.org/data/2.5/weather"
openweather_api_endpoint = "https://api.openweathermap.org/data/2.5/forecast"
params = {
    "lat": lat,
    "lon": lon,
    "appid": OPENWEATHER_API_KEY,
    "cnt": 4,
}
date_format = "%Y-%m-%d %H:%M:%S"
# 2026-07-28 03:00:00

# Twilio Setup
account_sid = os.environ.get("TWILIO_ACC_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

will_rain = False
rain_times = []


weather_response = requests.get(openweather_api_endpoint, params)
weather_response.raise_for_status()
weather_data = weather_response.json()
weather_list = weather_data["list"]
for forecast in weather_list:
    condition_code = forecast["weather"][0]["id"]
    if 200 <= condition_code < 700:
        rain_date = datetime.datetime.strptime(forecast["dt_txt"], date_format)
        rain_times.append(str(f"{rain_date.hour:02d}:{rain_date.minute:02d}"))
        will_rain = True

if will_rain:
    # print(f"Bring an umbrella. It is expected to rain at {", ".join(rain_times)}")
    message = client.messages.create(
        body=f"☔ Bring an umbrella. It is expected to rain at {", ".join(rain_times)}",
        from_=os.environ.get("FROM_NUMBER"),
        to=os.environ.get("TO_NUMBER"),
    )
    print(message.status)
else:
    print("You will not need an umbrella in the next 12 hours.")

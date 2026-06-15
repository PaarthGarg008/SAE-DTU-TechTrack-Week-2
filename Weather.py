import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

HISTORY_FILE = "history.json"


def load_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def add_to_history(record):
    history = load_history()

    history.append(record)

    if len(history) > 5:
        history.pop(0)

    save_history(history)


def show_history():
    history = load_history()

    if not history:
        print("\nNo history available.\n")
        return

    print("\n===== LAST 5 SEARCHES =====\n")

    for item in history:

        if item["status"] == "success":

            print(f"City: {item['city']}")
            print(f"Temperature: {item['temperature']}°C")
            print(f"Humidity: {item['humidity']}%")
            print(f"Wind Speed: {item['wind_speed']} km/h")
            print(f"Condition: {item['condition']}")
            print(f"AQI: {item['aqi']}")
            print("-" * 30)

        else:

            print(f"City: {item['city']}")
            print(f"Error: {item['error']}")
            print("-" * 30)


def get_weather(city):

    weather_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(weather_url, params=params, timeout=10)

        if response.status_code == 404:

            add_to_history({
                "city": city,
                "status": "failed",
                "error": "City not found"
            })

            print("\nCity not found.\n")
            return

        if response.status_code != 200:
            print(f"\nAPI Error: {response.status_code}\n")
            return

        data = response.json()

        temperature = data.get("main", {}).get("temp", "N/A")
        feels_like = data.get("main", {}).get("feels_like", "N/A")
        humidity = data.get("main", {}).get("humidity", "N/A")

        wind_speed = data.get("wind", {}).get("speed", 0)
        wind_speed = round(wind_speed * 3.6, 2)

        condition = data.get("weather", [{}])[0].get(
            "description",
            "N/A"
        )

        lat = data.get("coord", {}).get("lat")
        lon = data.get("coord", {}).get("lon")

        get_aqi(
            city,
            temperature,
            feels_like,
            humidity,
            wind_speed,
            condition,
            lat,
            lon
        )

    except requests.exceptions.ConnectionError:
        print("\nNo internet connection.\n")

    except requests.exceptions.Timeout:
        print("\nRequest timed out.\n")

    except Exception as e:
        print("\nUnexpected error:", e)


def get_aqi(
        city,
        temperature,
        feels_like,
        humidity,
        wind_speed,
        condition,
        lat,
        lon
):

    aqi_url = (
        "https://api.openweathermap.org/data/2.5/air_pollution"
    )

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY
    }

    response = requests.get(aqi_url, params=params)

    aqi_data = response.json()

    aqi = (
        aqi_data.get("list", [{}])[0]
        .get("main", {})
        .get("aqi", "N/A")
    )

    advisory = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }

    print("\n===== WEATHER REPORT =====\n")

    print(f"City         : {city}")
    print(f"Temperature  : {temperature}°C")
    print(f"Feels Like   : {feels_like}°C")
    print(f"Humidity     : {humidity}%")
    print(f"Wind Speed   : {wind_speed} km/h")
    print(f"Condition    : {condition}")
    print(f"AQI          : {aqi}")
    print(f"Advisory     : {advisory.get(aqi)}")

    add_to_history({
        "city": city,
        "status": "success",
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "condition": condition,
        "aqi": aqi
    })


def main():

    history = load_history()

    if history:
        print("\nLast Search:")
        print(history[-1]["city"])

    while True:

        city = input(
            "\nEnter city name "
            "(history/exit): "
        ).strip()

        if city.lower() == "exit":
            break

        if city.lower() == "history":
            show_history()
            continue

        get_weather(city)


if __name__ == "__main__":
    main()
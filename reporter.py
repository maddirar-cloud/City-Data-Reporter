
import requests
import json
import csv


def get_city():
    """Ask the user for a non-empty city name."""
    while True:
        city = input("Enter a city name: ").strip()

        if city:
            return city

        print("City name cannot be empty. Please try again.")


def get_weather(city):
    """Retrieve weather data from OpenWeatherMap API."""
    api_key = "INSERT_API"

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )

    try:
        response = requests.get(url)
        data = json.loads(response.text)

        if response.status_code == 404:
            print("Error: City not found.")
            return None

        if response.status_code == 401:
            print("Error: Invalid API key.")
            return None

        response.raise_for_status()

        weather = {
            "City": data["name"],
            "Country": data["sys"]["country"],
            "Temperature (C)": data["main"]["temp"],
            "Humidity (%)": data["main"]["humidity"],
            "Description": data["weather"][0]["description"]
        }

        return weather

    except requests.exceptions.RequestException:
        print("Error: Unable to retrieve weather data.")
        return None


def display_weather(weather):
    """Display the weather information."""
    print("\nCity Weather Report")
    print(f"City: {weather['City']}")
    print(f"Country: {weather['Country']}")
    print(f"Temperature: {weather['Temperature (C)']} °C")
    print(f"Humidity: {weather['Humidity (%)']}%")
    print(f"Description: {weather['Description']}")


def save_to_csv(weather):
    """Write weather information to city_data.csv."""
    with open("city_data.csv", "a", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "City",
                "Country",
                "Temperature (C)",
                "Humidity (%)",
                "Description"
            ]
        )

        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(weather)


def read_csv():
    """Read and report information from city_data.csv."""
    try:
        with open("city_data.csv", "r", newline="") as file:
            reader = csv.DictReader(file)
            cities = list(reader)

        print("\nSaved City Report")
        print("-----------------")
        print(f"Number of cities: {len(cities)}")

        for city in cities:
            print(
                f"{city['City']}: "
                f"{city['Temperature (C)']} °C"
            )

    except FileNotFoundError:
        print("No city data file found.")


def main():
    """Run the City Data Reporter program."""
    city = get_city()

    weather = get_weather(city)

    if weather:
        display_weather(weather)
        save_to_csv(weather)
        read_csv()


if __name__ == "__main__":
    main()
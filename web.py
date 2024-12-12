import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_weather_data(city, api_key):
    """Fetch weather data from OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None

def process_weather_data(data):
    """Process and clean the weather data for analysis."""
    forecast_list = data['list']
    processed_data = []
    for forecast in forecast_list:
        processed_data.append({
            "datetime": forecast["dt_txt"],
            "temperature": forecast["main"]["temp"],
            "humidity": forecast["main"]["humidity"],
            "wind_speed": forecast["wind"]["speed"],
            "weather": forecast["weather"][0]["description"]
        })
    return pd.DataFrame(processed_data)

def visualize_weather_data(df):
    """Visualize weather data using matplotlib and seaborn."""
    plt.figure(figsize=(12, 6))

    # Temperature Trend
    plt.subplot(2, 1, 1)
    sns.lineplot(x=pd.to_datetime(df["datetime"]), y=df["temperature"], marker="o", label="Temperature (°C)")
    plt.title("Temperature Trend")
    plt.xlabel("Datetime")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)

    # Humidity Trend
    plt.subplot(2, 1, 2)
    sns.lineplot(x=pd.to_datetime(df["datetime"]), y=df["humidity"], marker="o", color="orange", label="Humidity (%)")
    plt.title("Humidity Trend")
    plt.xlabel("Datetime")
    plt.ylabel("Humidity (%)")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

def alert_system(df):
    """Notify users of severe weather conditions."""
    alerts = []
    for index, row in df.iterrows():
        if row["temperature"] < 0:
            alerts.append(f"Alert: Freezing temperatures on {row['datetime']} ({row['temperature']}°C)")
        if "rain" in row["weather"].lower() or "storm" in row["weather"].lower():
            alerts.append(f"Alert: Rain or storm expected on {row['datetime']} ({row['weather']})")
    return alerts

def main():
    print("Weather Forecasting Application")
    api_key = "975f8c3c634b2d153ddaa6102733d5f1"  # Replace with your OpenWeatherMap API key

    city = input("Enter the city name: ").strip()
    weather_data = get_weather_data(city, api_key)

    if weather_data:
        df = process_weather_data(weather_data)
        print("\nWeather Data:")
        print(df.head())

        print("\nVisualizing Weather Data...")
        visualize_weather_data(df)

        print("\nWeather Alerts:")
        alerts = alert_system(df)
        for alert in alerts:
            print(alert)
    else:
        print("Failed to retrieve weather data. Please check the city name or API key.")

if __name__ == "__main__":
    main()

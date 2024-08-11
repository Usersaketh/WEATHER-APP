import requests

def get_weather(api_key, location):
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        'key': api_key,
        'q': location
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def display_weather(data):
    if data:
        location = data.get('location', {})
        current = data.get('current', {})
        city = location.get('name')
        temp_c = current.get('temp_c')
        humidity = current.get('humidity')
        weather_desc = current.get('condition', {}).get('text')

        print(f"\nWeather in {city}:")
        print(f"Temperature: {temp_c}°C")
        print(f"Humidity: {humidity}%")
        print(f"Conditions: {weather_desc}\n")
    else:
        print("\nUnable to retrieve weather data.\nCheck your location name.\n")

def main():
    api_key = '2db17cf6bc6a41a39e8101930241008' 
    print("<----------- Basic Weather App ----------->\n")
    
    while True:
        location = input("Enter the location (city): ").strip()
        
        if location:
            weather_data = get_weather(api_key, location)
            display_weather(weather_data)
        else:
            print("Enter valid Location name")
        
        check_again = input("Do you want to check another location? (yes/no): ").strip().lower()
        if check_again != 'yes':
            print("\nExiting the Weather App. Have a great day!")
            break

if __name__ == "__main__":
    main()

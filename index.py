import requests
import os
from flask import Flask, render_template, request, jsonify
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def get_weather(api_key, location):
    """
    Fetch weather data from WeatherAPI with improved error handling
    """
    if not api_key or not location:
        return {"error": "API key and location are required"}
    
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        'key': api_key,
        'q': location.strip(),
        'aqi': 'yes'  # Include air quality data
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Successfully fetched weather data for {location}")
            return data
        elif response.status_code == 400:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Invalid location')
            logger.warning(f"Invalid location: {location}")
            return {"error": error_msg}
        elif response.status_code == 401:
            logger.error("Invalid API key")
            return {"error": "Invalid API key"}
        elif response.status_code == 403:
            logger.error("API key quota exceeded")
            return {"error": "API quota exceeded"}
        else:
            logger.error(f"API request failed with status code: {response.status_code}")
            return {"error": f"Weather service unavailable (Status: {response.status_code})"}
            
    except requests.exceptions.Timeout:
        logger.error("Request timeout")
        return {"error": "Request timeout - please try again"}
    except requests.exceptions.ConnectionError:
        logger.error("Connection error")
        return {"error": "Connection error - check your internet connection"}
    except requests.exceptions.RequestException as e:
        logger.error(f"Request exception: {str(e)}")
        return {"error": "Failed to fetch weather data"}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {"error": "An unexpected error occurred"}

def format_weather_data(data):
    """
    Format weather data for display
    """
    if 'error' in data:
        return data
    
    try:
        location = data.get('location', {})
        current = data.get('current', {})
        
        formatted_data = {
            'city': location.get('name', 'Unknown'),
            'country': location.get('country', 'Unknown'),
            'region': location.get('region', ''),
            'temp_c': current.get('temp_c', 0),
            'temp_f': current.get('temp_f', 0),
            'humidity': current.get('humidity', 0),
            'wind_kph': current.get('wind_kph', 0),
            'wind_dir': current.get('wind_dir', 'N/A'),
            'pressure_mb': current.get('pressure_mb', 0),
            'visibility_km': current.get('vis_km', 0),
            'uv': current.get('uv', 0),
            'weather_desc': current.get('condition', {}).get('text', 'Unknown'),
            'weather_icon': current.get('condition', {}).get('icon', ''),
            'feels_like_c': current.get('feelslike_c', 0),
            'feels_like_f': current.get('feelslike_f', 0),
            'last_updated': current.get('last_updated', ''),
            'local_time': location.get('localtime', ''),
        }
        
        # Add air quality data if available
        if 'air_quality' in current:
            air_quality = current['air_quality']
            formatted_data['air_quality'] = {
                'co': air_quality.get('co', 0),
                'no2': air_quality.get('no2', 0),
                'o3': air_quality.get('o3', 0),
                'pm2_5': air_quality.get('pm2_5', 0),
                'pm10': air_quality.get('pm10', 0),
                'us_epa_index': air_quality.get('us-epa-index', 0),
                'gb_defra_index': air_quality.get('gb-defra-index', 0)
            }
        
        return formatted_data
        
    except Exception as e:
        logger.error(f"Error formatting weather data: {str(e)}")
        return {"error": "Error processing weather data"}

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather_data():
    """API endpoint to get weather data"""
    try:
        data = request.get_json()
        location = data.get('location', '').strip()
        
        if not location:
            return jsonify({"error": "Please enter a location"})
        
        api_key = os.getenv('WEATHER_API_KEY', '2db17cf6bc6a41a39e8101930241008')
        
        weather_data = get_weather(api_key, location)
        formatted_data = format_weather_data(weather_data)
        
        return jsonify(formatted_data)
        
    except Exception as e:
        logger.error(f"Error in weather endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"})

def display_weather(data):
    """
    Console display function (kept for backward compatibility)
    """
    if 'error' in data:
        print(f"\nError: {data['error']}\n")
        return
    
    formatted_data = format_weather_data(data)
    if 'error' in formatted_data:
        print(f"\nError: {formatted_data['error']}\n")
        return
    
    print(f"\nWeather in {formatted_data['city']}, {formatted_data['country']}:")
    print(f"Temperature: {formatted_data['temp_c']}°C ({formatted_data['temp_f']}°F)")
    print(f"Feels like: {formatted_data['feels_like_c']}°C ({formatted_data['feels_like_f']}°F)")
    print(f"Humidity: {formatted_data['humidity']}%")
    print(f"Conditions: {formatted_data['weather_desc']}")
    print(f"Wind: {formatted_data['wind_kph']} km/h {formatted_data['wind_dir']}")
    print(f"Pressure: {formatted_data['pressure_mb']} mb")
    print(f"Visibility: {formatted_data['visibility_km']} km")
    print(f"UV Index: {formatted_data['uv']}")
    print(f"Last Updated: {formatted_data['last_updated']}\n")

def main():
    """Console version of the weather app"""
    api_key = os.getenv('WEATHER_API_KEY', '2db17cf6bc6a41a39e8101930241008')
    print("<----------- Enhanced Weather App ----------->\n")
    
    while True:
        location = input("Enter the location (city, country): ").strip()
        
        if location:
            weather_data = get_weather(api_key, location)
            display_weather(weather_data)
        else:
            print("Please enter a valid location name")
        
        check_again = input("Do you want to check another location? (yes/no): ").strip().lower()
        if check_again not in ['yes', 'y']:
            print("\nExiting the Weather App. Have a great day!")
            break

def run_web_app():
    """Run the Flask web application"""
    print("Starting Weather App Web Server...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'web':
        run_web_app()
    else:
        print("Weather App - Choose mode:")
        print("1. Console mode")
        print("2. Web interface")
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == '2':
            run_web_app()
        else:
            main()
    main()

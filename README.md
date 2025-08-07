# Enhanced Weather App

A robust weather application with both console and web interface modes, featuring detailed weather information including air quality data.

## Features

### Robust Error Handling
- Network timeout handling
- API rate limit management
- Invalid location detection
- Connection error recovery
- Detailed error messages

### Enhanced Weather Data
- Current temperature (Celsius and Fahrenheit)
- Feels like temperature
- Humidity, wind speed and direction
- Atmospheric pressure
- Visibility and UV index
- Air quality measurements (PM2.5, PM10, CO, NO2, O3)
- Last updated timestamp
- Local time for the location

### Two Interface Modes
1. **Console Mode**: Traditional command-line interface
2. **Web Interface**: Modern, responsive HTML interface

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. (Optional) Set your WeatherAPI key as an environment variable:
```bash
# Windows PowerShell
$env:WEATHER_API_KEY="your_api_key_here"

# Windows Command Prompt
set WEATHER_API_KEY=your_api_key_here
```

## Usage

### Running the Application

#### Option 1: Interactive Mode Selection
```bash
python index.py
```
Choose between console mode (1) or web interface (2).

#### Option 2: Direct Web Mode
```bash
python index.py web
```

#### Option 3: Console Mode (Default)
Just press Enter or select option 1 when prompted.

### Web Interface
- Open your browser to `http://localhost:5000`
- Enter any city name (e.g., "London", "Paris", "New York")
- View detailed weather information with a beautiful, responsive design
- Works on desktop and mobile devices

### Console Interface
- Enter city names when prompted
- View detailed weather information in the terminal
- Option to check multiple locations
- Type 'no' or 'n' to exit

## API Key

The application comes with a demo API key, but for production use, you should:

1. Get your free API key from [WeatherAPI.com](https://www.weatherapi.com/)
2. Set it as an environment variable `WEATHER_API_KEY`
3. Or replace the default key in the code

## Error Handling

The application handles various error scenarios:
- **Invalid locations**: Clear error messages for misspelled cities
- **Network issues**: Timeout and connection error handling
- **API limits**: Quota exceeded notifications
- **Service unavailable**: Graceful degradation when API is down

## Technical Details

### Dependencies
- `requests`: HTTP library for API calls
- `Flask`: Web framework for the UI
- `logging`: Error tracking and debugging

### API Used
- [WeatherAPI.com](https://www.weatherapi.com/) for current weather and air quality data

### File Structure
```
WEATHER-APP/
├── index.py              # Main application file
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── templates/
    └── index.html       # Web interface template
```

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError"**: Install requirements with `pip install -r requirements.txt`
2. **"Connection Error"**: Check your internet connection
3. **"Invalid API Key"**: Verify your API key is correct
4. **"Location not found"**: Try different spelling or include country name

### Getting Help
- Check the console output for detailed error messages
- Verify your internet connection
- Ensure the API key is valid and has remaining quota

## License

This project is open source and available under the MIT License.

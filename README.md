# SAE-DTU-TechTrack-Week-2
# Weather + Air Quality CLI Dashboard

A Python command-line application that fetches real-time weather and air quality information using the OpenWeatherMap API.

## Features

- Get current weather information for any city
- Displays:
  - Temperature (°C)
  - Feels Like Temperature
  - Humidity (%)
  - Wind Speed (km/h)
  - Weather Condition
  - Air Quality Index (AQI)
- Saves the last 5 searches in a JSON file
- Stores both successful and failed (invalid city) searches
- View search history using the `history` command
- Handles invalid city names gracefully
- Handles network and API errors without crashing

## Technologies Used

- Python
- Requests
- JSON
- python-dotenv
- OpenWeatherMap API

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd WeatherDashboard
```

### 2. Install Dependencies

```bash
pip install requests python-dotenv
```

### 3. Create a .env File

Create a `.env` file from `.env.example`.

Contents of `.env.example`:

```text
OPENWEATHER_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual OpenWeatherMap API key.

### 4. Run the Application

```bash
python weather.py
```

## Usage

Enter a city name when prompted.

Example:

```text
Enter city name (history/exit): Delhi
```

### Special Commands

To view the last 5 searches:

```text
history
```

To exit the application:

```text
exit
```

## Example Output

```text
===== WEATHER REPORT =====

City         : Delhi
Temperature  : 35°C
Feels Like   : 39°C
Humidity     : 45%
Wind Speed   : 12 km/h
Condition    : Clear Sky
AQI          : 2
Advisory     : Fair
```

## Project Structure

```text
WeatherDashboard/
│
├── weather.py
├── history.json
├── .env
├── .gitignore
└── README.md
```

## Files

### weather.py
Main application file containing:
- Weather API integration
- AQI API integration
- Error handling
- Search history management

### history.json
Stores the last 5 searches.

### .env
Stores the OpenWeatherMap API key.

### .env.example
Template for creating the `.env` file.

### .gitignore
Prevents sensitive files from being uploaded to GitHub.

## Error Handling

The application handles:

- Invalid city names
- Network connection errors
- API request failures
- Missing history file
- JSON file errors

## API Used

OpenWeatherMap APIs:

- Current Weather API
- Air Pollution API

## Notes

- Never upload your `.env` file to GitHub.
- Keep your API key private.
- Search history is stored locally in `history.json`.

## Author

Paarth Garg

FORGETRACK 2026 - Week 02 Project

const axios = require('axios');

class WeatherService {
  constructor() {
    this.apiKey = process.env.OPENWEATHER_API_KEY;
    this.baseUrl = 'https://api.openweathermap.org/data/2.5';

    console.log('🔑 API Key exists:', !!this.apiKey);
    console.log('🔑 API Key length:', this.apiKey?.length);
  }

  // Fallback data for Parliament House, New Delhi
  getFallbackWeatherData() {
    const currentDate = new Date();
    
    return {
      current: {
        main: {
          temp: 32, // Typical Delhi temperature
          humidity: 65
        },
        wind: {
          speed: 2.5 // m/s
        },
        weather: [{
          icon: '01d', // Clear sky
          main: 'Clear',
          description: 'clear sky'
        }],
        name: 'New Delhi'
      },
      forecast: {
        list: [
          {
            dt: currentDate.getTime() / 1000,
            main: { temp_max: 34, temp_min: 26 },
            weather: [{ icon: '01d', main: 'Clear' }],
            pop: 0.1
          },
          {
            dt: (currentDate.getTime() + 86400000) / 1000, // +1 day
            main: { temp_max: 33, temp_min: 25 },
            weather: [{ icon: '02d', main: 'Partly Cloudy' }],
            pop: 0.2
          },
          {
            dt: (currentDate.getTime() + 172800000) / 1000, // +2 days
            main: { temp_max: 31, temp_min: 24 },
            weather: [{ icon: '03d', main: 'Cloudy' }],
            pop: 0.3
          },
          {
            dt: (currentDate.getTime() + 259200000) / 1000, // +3 days
            main: { temp_max: 29, temp_min: 23 },
            weather: [{ icon: '10d', main: 'Rain' }],
            pop: 0.7
          },
          {
            dt: (currentDate.getTime() + 345600000) / 1000, // +4 days
            main: { temp_max: 32, temp_min: 25 },
            weather: [{ icon: '02d', main: 'Partly Cloudy' }],
            pop: 0.2
          }
        ]
      },
      location: {
        city: 'New Delhi',
        country: 'India'
      }
    };
  }

  async getCurrentWeather(lat, lon) {
    try {
      const url = `${this.baseUrl}/weather?lat=${lat}&lon=${lon}&appid=${this.apiKey}&units=metric`;
      console.log('🌐 Making current weather request to:', url.replace(this.apiKey, 'HIDDEN_KEY'));

      const response = await axios.get(`${this.baseUrl}/weather`, {
        params: {
          lat,
          lon,
          appid: this.apiKey,
          units: 'metric'
        }
      });
      return response.data;
    } catch (error) {
      console.warn('⚠️ Current Weather API failed, using fallback data for Parliament House');
      return this.getFallbackWeatherData().current;
    }
  }

  async getFiveDayForecast(lat, lon) {
    try {
      const response = await axios.get(`${this.baseUrl}/forecast`, {
        params: {
          lat,
          lon,
          appid: this.apiKey,
          units: 'metric'
        }
      });
      return response.data;
    } catch (error) {
      console.warn('⚠️ Forecast API failed, using fallback data for Parliament House');
      return this.getFallbackWeatherData().forecast;
    }
  }

  // Get location info from coordinates
  async getLocationInfo(lat, lon) {
    try {
      const response = await axios.get(`${this.baseUrl}/weather`, {
        params: {
          lat,
          lon,
          appid: this.apiKey,
          units: 'metric'
        }
      });
      return {
        city: response.data.name,
        country: response.data.sys.country
      };
    } catch (error) {
      console.warn('⚠️ Location API failed, using fallback location');
      return this.getFallbackWeatherData().location;
    }
  }

  formatWeatherData(currentWeather, forecast, location) {
    // Get weather icon mapping
    const getWeatherEmoji = (iconCode) => {
      const iconMap = {
        '01d': '☀️', '01n': '🌙',
        '02d': '⛅', '02n': '☁️',
        '03d': '☁️', '03n': '☁️',
        '04d': '☁️', '04n': '☁️',
        '09d': '🌧️', '09n': '🌧️',
        '10d': '🌦️', '10n': '🌧️',
        '11d': '⛈️', '11n': '⛈️',
        '13d': '🌨️', '13n': '🌨️',
        '50d': '🌫️', '50n': '🌫️'
      };
      return iconMap[iconCode] || '☀️';
    };

    // Format 5-day forecast
    const dailyForecasts = [];
    const processedDates = new Set();
    
    forecast.list.forEach(item => {
      const date = new Date(item.dt * 1000);
      const dateKey = date.toDateString();
      const hour = date.getHours();
      
      // Take the forecast around noon (12:00) for each day, max 5 days
      // For fallback data, we don't have hour restrictions
      if (!processedDates.has(dateKey) && dailyForecasts.length < 5) {
        // For real API data, prefer noon readings; for fallback, take any
        const isGoodTime = hour >= 12 && hour <= 15;
        const isFallbackData = !forecast.city; // Fallback data doesn't have city property
        
        if (isFallbackData || isGoodTime || processedDates.size === 0) {
          processedDates.add(dateKey);
          dailyForecasts.push({
            day: date.toLocaleDateString('en-US', { weekday: 'short' }),
            icon: getWeatherEmoji(item.weather[0].icon),
            high: Math.round(item.main.temp_max),
            low: Math.round(item.main.temp_min),
            precipitation: Math.round(item.pop * 100) // Convert to percentage
          });
        }
      }
    });

    // Ensure we have exactly 5 days for the forecast
    while (dailyForecasts.length < 5) {
      const lastDay = dailyForecasts[dailyForecasts.length - 1];
      const nextDate = new Date();
      nextDate.setDate(nextDate.getDate() + dailyForecasts.length);
      
      dailyForecasts.push({
        day: nextDate.toLocaleDateString('en-US', { weekday: 'short' }),
        icon: lastDay?.icon || '☀️',
        high: lastDay?.high || 30,
        low: lastDay?.low || 25,
        precipitation: 20
      });
    }

    return {
      success: true,
      data: {
        icon: getWeatherEmoji(currentWeather.weather[0].icon),
        temperature: Math.round(currentWeather.main.temp),
        humidity: currentWeather.main.humidity,
        windSpeed: Math.round(currentWeather.wind.speed * 3.6), // Convert m/s to km/h
        forecast5Days: dailyForecasts
      },
      location: location || {
        city: currentWeather.name || 'New Delhi',
        country: currentWeather.sys?.country || 'India'
      }
    };
  }

  // Main method that combines all data
  async getCompleteWeatherData(lat, lon) {
    try {
      console.log(`🌍 Fetching weather data for coordinates: ${lat}, ${lon}`);
      
      // Fetch all data (with fallback handling in each method)
      const [currentWeather, forecast] = await Promise.all([
        this.getCurrentWeather(lat, lon),
        this.getFiveDayForecast(lat, lon)
      ]);

      // Get location info
      const location = await this.getLocationInfo(lat, lon);

      // Format and return the complete weather data
      return this.formatWeatherData(currentWeather, forecast, location);
      
    } catch (error) {
      console.error('❌ Complete weather data fetch failed:', error.message);
      
      // Return fallback data with proper formatting
      const fallbackData = this.getFallbackWeatherData();
      return this.formatWeatherData(
        fallbackData.current,
        fallbackData.forecast,
        fallbackData.location
      );
    }
  }
}

module.exports = new WeatherService();

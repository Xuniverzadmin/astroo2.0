# Frontend Components

This directory contains React components for the Astrooverz frontend application.

## Components

### TodayCard.jsx

A comprehensive component that displays today's panchangam information including:

- **Location-based data**: Automatically detects user location or allows manual override
- **Panchangam elements**: Tithi, Nakshatra, Yoga, Karana with progress indicators
- **Timing information**: Sunrise/sunset times with proper timezone handling
- **Inauspicious periods**: Rahu Kalam, Yama Gandam, Gulikai Kalam with countdown timers
- **Gowri Panchangam**: Auspicious and inauspicious time periods
- **Calendar integration**: Download .ics file for calendar applications
- **Real-time updates**: Auto-refreshes countdown timers every minute

#### Features:
- Responsive design with Tailwind CSS
- Error handling for location and API failures
- Loading states and user feedback
- Automatic location detection with fallback
- Manual location override capability
- Calendar export functionality

#### Usage:
```jsx
import TodayCard from './components/TodayCard';

function App() {
  return (
    <div>
      <TodayCard />
    </div>
  );
}
```

## Hooks

### useLocation.js

A custom React hook for handling geolocation and location management:

#### Features:
- Browser geolocation API integration
- Reverse geocoding for city/country names
- Manual location override
- Local storage persistence
- Error handling and permission management
- Timezone detection

#### Usage:
```jsx
import { useLocation } from '../hooks/useLocation';

function MyComponent() {
  const { 
    location, 
    loading, 
    error, 
    hasLocation,
    getCurrentPosition,
    setManualLocation 
  } = useLocation();

  return (
    <div>
      {hasLocation ? (
        <p>Location: {location.latitude}, {location.longitude}</p>
      ) : (
        <button onClick={getCurrentPosition}>Get Location</button>
      )}
    </div>
  );
}
```

## API Integration

The components integrate with the backend API endpoints:

- `GET /api/panchangam/{date}?lat={lat}&lon={lon}&tz={tz}` - Fetch panchangam data
- Location services for reverse geocoding
- Calendar export functionality (.ics format)

## Dependencies

- React 18+
- Lucide React (icons)
- Tailwind CSS (styling)
- Browser Geolocation API
- Fetch API for HTTP requests

## Browser Support

- Modern browsers with ES6+ support
- Geolocation API support
- Local Storage support
- Fetch API support

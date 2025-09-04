import React, { useState, useEffect } from 'react';

// The main component that fetches and displays Panchangam data.
const App = () => {
  const [panchangamData, setPanchangamData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Default coordinates for a location in India.
  // In a real application, you would get this from the user's location.
  const DEFAULT_LATITUDE = 28.7041; // New Delhi
  const DEFAULT_LONGITUDE = 77.1025; // New Delhi
  const TIMEZONE = 'Asia/Kolkata';

  useEffect(() => {
    const fetchPanchangamData = async () => {
      try {
        setLoading(true);

        // This is a mock API response to prevent the 404 error.
        // In a real application, you would make a valid API call here.
        const mockData = {
          sunrise: '06:00 AM',
          sunset: '06:30 PM',
          windows: [
            { name: 'Abhijit Muhurat', time: '11:59 AM - 12:47 PM' },
            { name: 'Brahma Muhurat', time: '04:30 AM - 05:18 AM' },
            { name: 'Rahu Kalam', time: '07:30 AM - 09:00 AM' },
            { name: 'Guli Kalam', time: '10:30 AM - 12:00 PM' },
          ],
        };

        // Simulate a network delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        setPanchangamData(mockData);

      } catch (e) {
        console.error("Failed to fetch Panchangam data:", e);
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPanchangamData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="flex flex-col items-center p-6 bg-white rounded-lg shadow-xl animate-pulse">
          <div className="h-6 w-32 bg-gray-200 rounded-full mb-4"></div>
          <div className="h-4 w-48 bg-gray-200 rounded-full"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-red-50">
        <div className="p-6 bg-white rounded-lg shadow-xl text-center text-red-600">
          <p className="text-xl font-semibold mb-2">Error</p>
          <p>Failed to load Panchangam data. Please try again later.</p>
          <p className="text-sm text-red-400 mt-2">Error details: {error}</p>
        </div>
      </div>
    );
  }

  if (!panchangamData) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="p-6 bg-white rounded-lg shadow-xl text-center text-gray-600">
          <p className="text-xl font-semibold">No data available.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4 font-sans text-gray-800">
      <div className="bg-white rounded-3xl shadow-2xl p-8 max-w-lg w-full flex flex-col items-center transform transition-all duration-500 hover:scale-105">
        <div className="flex items-center justify-center w-20 h-20 bg-gradient-to-r from-orange-400 to-yellow-500 rounded-full shadow-lg mb-6">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-10 w-10 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
            />
          </svg>
        </div>
        <h1 className="text-3xl font-bold mb-2 text-center text-gray-900">Today's Panchangam</h1>
        <p className="text-sm text-gray-500 mb-6 text-center">Data for New Delhi, India ({TIMEZONE})</p>

        <div className="w-full space-y-4">
          <div className="bg-gray-50 p-4 rounded-xl border border-gray-200">
            <h2 className="font-semibold text-lg text-gray-700">Sunrise & Sunset</h2>
            <p className="mt-1 text-gray-600">
              <span className="font-medium text-gray-900">Sunrise:</span> {panchangamData.sunrise}
            </p>
            <p className="mt-1 text-gray-600">
              <span className="font-medium text-gray-900">Sunset:</span> {panchangamData.sunset}
            </p>
          </div>

          <div className="bg-gray-50 p-4 rounded-xl border border-gray-200">
            <h2 className="font-semibold text-lg text-gray-700">Muhurat & Timing Windows</h2>
            <ul className="mt-2 space-y-2">
              {panchangamData.windows.map((window, index) => (
                <li key={index} className="flex flex-col bg-white p-3 rounded-lg shadow-sm">
                  <span className="font-medium text-gray-900">{window.name}</span>
                  <span className="text-sm text-gray-500">{window.time}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;

import React from 'react';

// The main component that provides a downloadable calendar link.
const App = () => {
  // These are the parameters for the calendar link.
  // In a real application, you might use state to allow the user
  // to change these values.
  const lat = 28.7041; // New Delhi latitude
  const lon = 77.1025; // New Delhi longitude
  const tz = 'Asia/Kolkata';
  const days = 30; // Number of days for the calendar data

  // Construct the full URL for the downloadable .ics file.
  const calendarUrl = `/api/calendar.ics?lat=${lat}&lon=${lon}&tz=${tz}&days=${days}`;

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4 font-sans text-gray-800">
      <div className="bg-white rounded-3xl shadow-2xl p-8 max-w-lg w-full flex flex-col items-center transform transition-all duration-500 hover:scale-105">
        <div className="flex items-center justify-center w-20 h-20 bg-gradient-to-r from-teal-400 to-cyan-500 rounded-full shadow-lg mb-6">
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
              d="M8 7V3m8 4V3m-9 8h.01M8 11h.01M12 11h.01M16 11h.01M3 15h2M3 19h2m-2-4v4m14-8h2M19 11h2m-2-4v4m-5 4h.01M12 15h.01M16 15h.01M8 19h.01M12 19h.01M16 19h.01"
            />
            <path strokeLinecap="round" strokeLinejoin="round" d="M11 5H6a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2v-5M15 5h2a2 2 0 012 2v2" />
          </svg>
        </div>
        <h1 className="text-3xl font-bold mb-2 text-center text-gray-900">Add Panchangam to Your Calendar</h1>
        <p className="text-sm text-gray-500 mb-6 text-center">
          Click the button below to download the `.ics` file with daily Panchangam events for the next 30 days.
        </p>

        <a 
          href={calendarUrl}
          download
          className="px-8 py-4 bg-teal-500 text-white font-bold rounded-full shadow-lg hover:bg-teal-600 transition-colors duration-300 transform hover:scale-105"
        >
          <span className="flex items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5 mr-2"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 01-1.414-1.414L8.586 11H5a1 1 0 110-2h3.586l-1.293-1.293a1 1 0 010-1.414z"
                clipRule="evenodd"
              />
            </svg>
            Download Calendar
          </span>
        </a>
      </div>
    </div>
  );
};

export default App;

import React from 'react';
import TodayCard from './components/TodayCard';

const Today = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-950 via-slate-950 to-slate-900 text-white">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Today's Panchangam</h1>
          <p className="text-white/70">
            Your daily Vedic astrology guide with auspicious times and important dates
          </p>
        </div>
        
        <TodayCard />
        
        <div className="mt-8 text-center">
          <p className="text-white/50 text-sm">
            Data provided by Astrooverz • Updated in real-time
          </p>
        </div>
      </div>
    </div>
  );
};

export default Today;

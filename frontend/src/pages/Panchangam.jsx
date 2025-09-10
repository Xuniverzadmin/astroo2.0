import React from 'react';
import { Sparkles, Sun, Moon, Clock, Calendar, MapPin, Star } from 'lucide-react';

const Panchangam = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-950 via-slate-950 to-slate-900 text-white">
      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Header */}
        <header className="text-center mb-12">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="p-1.5 rounded-xl bg-white/10">
              <Sparkles className="w-5 h-5" />
            </div>
            <span className="text-lg font-semibold">Astrooverz</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Understanding Panchangam
          </h1>
          <p className="text-white/80 text-lg max-w-2xl mx-auto">
            Learn about the ancient Vedic calendar system that guides auspicious timing for all life activities.
          </p>
        </header>

        {/* Main Content */}
        <main>
          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6">What is Panchangam?</h2>
            <div className="prose prose-invert max-w-none">
              <p className="text-white/80 leading-relaxed mb-4">
                Panchangam is a traditional Hindu calendar system that provides detailed information about the five essential elements of time: Tithi (lunar day), Vara (weekday), Nakshatra (lunar mansion), Yoga (auspicious combination), and Karana (half of a tithi). This ancient system helps determine the most auspicious times for various activities.
              </p>
              <p className="text-white/80 leading-relaxed mb-4">
                The word "Panchangam" literally means "five limbs" in Sanskrit, referring to these five components that together form a complete picture of the cosmic time. It's been used for thousands of years to guide everything from daily routines to major life events.
              </p>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6">The Five Components of Panchangam</h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 rounded-xl bg-white/10">
                    <Moon className="w-5 h-5" />
                  </div>
                  <h3 className="text-lg font-semibold">Tithi (Lunar Day)</h3>
                </div>
                <p className="text-white/80 text-sm leading-relaxed">
                  The lunar day based on the Moon's position relative to the Sun. There are 15 tithis in each lunar fortnight, each with specific characteristics and auspiciousness for different activities.
                </p>
              </div>

              <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 rounded-xl bg-white/10">
                    <Sun className="w-5 h-5" />
                  </div>
                  <h3 className="text-lg font-semibold">Vara (Weekday)</h3>
                </div>
                <p className="text-white/80 text-sm leading-relaxed">
                  The day of the week, each ruled by a specific planet. Each day has its own energy and is suitable for different types of activities and spiritual practices.
                </p>
              </div>

              <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 rounded-xl bg-white/10">
                    <Star className="w-5 h-5" />
                  </div>
                  <h3 className="text-lg font-semibold">Nakshatra (Lunar Mansion)</h3>
                </div>
                <p className="text-white/80 text-sm leading-relaxed">
                  The 27 lunar mansions that the Moon passes through. Each nakshatra has unique qualities and influences, affecting the nature of activities performed during its period.
                </p>
              </div>

              <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 rounded-xl bg-white/10">
                    <Clock className="w-5 h-5" />
                  </div>
                  <h3 className="text-lg font-semibold">Yoga & Karana</h3>
                </div>
                <p className="text-white/80 text-sm leading-relaxed">
                  Yoga represents auspicious combinations of Sun and Moon, while Karana is half of a tithi. These provide additional timing insights for specific activities.
                </p>
              </div>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6">Auspicious and Inauspicious Times</h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-2xl p-6">
                <h3 className="text-lg font-semibold text-emerald-400 mb-4">Auspicious Times (Shubh Muhurat)</h3>
                <ul className="text-white/80 space-y-2 text-sm">
                  <li>• Abhijit Muhurat - Most auspicious time of the day</li>
                  <li>• Brahma Muhurat - Early morning spiritual time</li>
                  <li>• Godhuli Muhurat - Evening twilight period</li>
                  <li>• Amrit Kalam - Nectar time for new beginnings</li>
                  <li>• Vijaya Muhurat - Victory time for important decisions</li>
                </ul>
              </div>

              <div className="bg-red-500/10 border border-red-500/20 rounded-2xl p-6">
                <h3 className="text-lg font-semibold text-red-400 mb-4">Inauspicious Times (Ashubh Muhurat)</h3>
                <ul className="text-white/80 space-y-2 text-sm">
                  <li>• Rahu Kalam - Avoid new ventures</li>
                  <li>• Yamaganda - Avoid important activities</li>
                  <li>• Gulikai Kalam - Avoid financial transactions</li>
                  <li>• Varjyam - Avoid auspicious ceremonies</li>
                  <li>• Bhadra - Avoid travel and new projects</li>
                </ul>
              </div>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6">Daily Panchangam Information</h2>
            <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
              <h3 className="text-lg font-semibold mb-4">What You'll Find in Daily Panchangam:</h3>
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium text-emerald-400 mb-2">Sun & Moon Times</h4>
                  <ul className="text-white/80 text-sm space-y-1">
                    <li>• Sunrise and sunset times</li>
                    <li>• Moonrise and moonset times</li>
                    <li>• Duration of day and night</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-emerald-400 mb-2">Auspicious Periods</h4>
                  <ul className="text-white/80 text-sm space-y-1">
                    <li>• Best times for prayers</li>
                    <li>• Favorable hours for business</li>
                    <li>• Good times for travel</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-emerald-400 mb-2">Festivals & Observances</h4>
                  <ul className="text-white/80 text-sm space-y-1">
                    <li>• Religious festivals</li>
                    <li>• Fasting days</li>
                    <li>• Special observances</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-emerald-400 mb-2">Planetary Positions</h4>
                  <ul className="text-white/80 text-sm space-y-1">
                    <li>• Current planetary transits</li>
                    <li>• Retrograde periods</li>
                    <li>• Planetary aspects</li>
                  </ul>
                </div>
              </div>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6">How Astrooverz Provides Panchangam</h2>
            <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
              <p className="text-white/80 leading-relaxed mb-4">
                Our advanced panchangam system provides personalized daily guidance based on your location and timezone:
              </p>
              <ul className="text-white/80 space-y-2">
                <li>• Location-specific sunrise/sunset times</li>
                <li>• Personalized auspicious timings</li>
                <li>• Daily nakshatra and tithi information</li>
                <li>• Inauspicious periods to avoid</li>
                <li>• Festival and observance reminders</li>
                <li>• Planetary transit alerts</li>
                <li>• Customized recommendations for your activities</li>
              </ul>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6">Benefits of Following Panchangam</h2>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-emerald-400 mb-2">Timing</div>
                <p className="text-white/70 text-sm">Choose the best times for important activities</p>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-emerald-400 mb-2">Harmony</div>
                <p className="text-white/70 text-sm">Align with natural cosmic rhythms</p>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-emerald-400 mb-2">Success</div>
                <p className="text-white/70 text-sm">Increase chances of favorable outcomes</p>
              </div>
            </div>
          </section>
        </main>

        {/* CTA Section */}
        <section className="text-center bg-white/5 border border-white/10 rounded-2xl p-8">
          <h2 className="text-2xl font-bold mb-4">Get Your Daily Panchangam</h2>
          <p className="text-white/80 mb-6">
            Access personalized panchangam information tailored to your location and receive daily guidance for optimal timing.
          </p>
          <button className="bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-3 rounded-xl font-medium">
            View Today's Panchangam
          </button>
        </section>
      </div>
    </div>
  );
};

export default Panchangam;

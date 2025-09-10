import React from 'react';
import { Sparkles, Sun, Moon, Star, Calendar, Users, Globe2 } from 'lucide-react';

const VedicAstrology = () => {
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
            Understanding Vedic Astrology
          </h1>
          <p className="text-white/80 text-lg max-w-2xl mx-auto">
            Discover the ancient wisdom of Vedic astrology and how it can guide your life decisions with precision and insight.
          </p>
        </header>

        {/* Main Content */}
        <main>
          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6">What is Vedic Astrology?</h2>
            <div className="prose prose-invert max-w-none">
              <p className="text-white/80 leading-relaxed mb-4">
                Vedic astrology, also known as Jyotish (the science of light), is an ancient Indian system of astrology that has been practiced for over 5,000 years. Unlike Western astrology, Vedic astrology uses the sidereal zodiac, which accounts for the precession of the equinoxes, making it more astronomically accurate.
              </p>
              <p className="text-white/80 leading-relaxed mb-4">
                The foundation of Vedic astrology lies in the belief that the positions of celestial bodies at the time of birth influence an individual's personality, life events, and destiny. This system provides detailed insights into various aspects of life including career, relationships, health, and spiritual growth.
              </p>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6">Key Components of Vedic Astrology</h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 rounded-xl bg-white/10">
                    <Sun className="w-5 h-5" />
                  </div>
                  <h3 className="text-lg font-semibold">Birth Chart (Kundli)</h3>
                </div>
                <p className="text-white/80 text-sm leading-relaxed">
                  A detailed map of the sky at the exact moment of birth, showing the positions of planets, signs, and houses. This forms the foundation for all astrological predictions and guidance.
                </p>
              </div>

              <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 rounded-xl bg-white/10">
                    <Moon className="w-5 h-5" />
                  </div>
                  <h3 className="text-lg font-semibold">Nakshatras (Lunar Mansions)</h3>
                </div>
                <p className="text-white/80 text-sm leading-relaxed">
                  The 27 lunar mansions that provide deeper insights into personality traits, life purpose, and compatibility. Each nakshatra has unique characteristics and ruling deities.
                </p>
              </div>

              <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 rounded-xl bg-white/10">
                    <Calendar className="w-5 h-5" />
                  </div>
                  <h3 className="text-lg font-semibold">Dasha Periods</h3>
                </div>
                <p className="text-white/80 text-sm leading-relaxed">
                  Planetary periods that determine the timing of life events. Understanding dasha periods helps in making important life decisions and planning for the future.
                </p>
              </div>

              <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 rounded-xl bg-white/10">
                    <Star className="w-5 h-5" />
                  </div>
                  <h3 className="text-lg font-semibold">Yogas (Planetary Combinations)</h3>
                </div>
                <p className="text-white/80 text-sm leading-relaxed">
                  Special combinations of planets that create specific effects in life. These yogas can indicate wealth, fame, health issues, or spiritual inclinations.
                </p>
              </div>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6">How Astrooverz Uses Vedic Astrology</h2>
            <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
              <p className="text-white/80 leading-relaxed mb-4">
                At Astrooverz, we combine traditional Vedic wisdom with modern technology to provide personalized guidance. Our digital jothidar analyzes your birth chart and provides:
              </p>
              <ul className="text-white/80 space-y-2">
                <li>• Daily panchangam with auspicious timings</li>
                <li>• Personalized numerology insights</li>
                <li>• Compatibility analysis for relationships</li>
                <li>• Career and life guidance based on planetary positions</li>
                <li>• Timing recommendations for important decisions</li>
              </ul>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6">Benefits of Vedic Astrology</h2>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-emerald-400 mb-2">Self-Awareness</div>
                <p className="text-white/70 text-sm">Understand your strengths, weaknesses, and life purpose</p>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-emerald-400 mb-2">Timing</div>
                <p className="text-white/70 text-sm">Make decisions at the most auspicious moments</p>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-emerald-400 mb-2">Guidance</div>
                <p className="text-white/70 text-sm">Navigate life's challenges with cosmic wisdom</p>
              </div>
            </div>
          </section>
        </main>

        {/* CTA Section */}
        <section className="text-center bg-white/5 border border-white/10 rounded-2xl p-8">
          <h2 className="text-2xl font-bold mb-4">Ready to Explore Your Vedic Chart?</h2>
          <p className="text-white/80 mb-6">
            Get your personalized Vedic astrology reading and discover the cosmic influences shaping your life.
          </p>
          <button className="bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-3 rounded-xl font-medium">
            Get Your Free Reading
          </button>
        </section>
      </div>
    </div>
  );
};

export default VedicAstrology;

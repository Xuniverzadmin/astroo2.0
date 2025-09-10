import React from 'react';
import { Sparkles, Calculator, Heart, Briefcase, Home, Users } from 'lucide-react';

const Numerology = () => {
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
            The Power of Numerology
          </h1>
          <p className="text-white/80 text-lg max-w-2xl mx-auto">
            Discover how numbers influence your life path, personality, and destiny through the ancient science of numerology.
          </p>
        </header>

        {/* Main Content */}
        <main>
          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6">What is Numerology?</h2>
            <div className="prose prose-invert max-w-none">
              <p className="text-white/80 leading-relaxed mb-4">
                Numerology is the mystical study of numbers and their influence on human life. Based on the belief that numbers have vibrational frequencies that affect our lives, numerology uses your birth date and name to reveal insights about your personality, life purpose, and future possibilities.
              </p>
              <p className="text-white/80 leading-relaxed mb-4">
                The practice of numerology dates back thousands of years and has been used by ancient civilizations including the Babylonians, Egyptians, and Greeks. Today, it continues to provide valuable insights for personal growth and decision-making.
              </p>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6">Core Numbers in Numerology</h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 rounded-xl bg-white/10">
                    <Calculator className="w-5 h-5" />
                  </div>
                  <h3 className="text-lg font-semibold">Life Path Number</h3>
                </div>
                <p className="text-white/80 text-sm leading-relaxed">
                  Calculated from your birth date, this is the most important number in numerology. It reveals your life's purpose, natural talents, and the lessons you're here to learn.
                </p>
              </div>

              <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 rounded-xl bg-white/10">
                    <Heart className="w-5 h-5" />
                  </div>
                  <h3 className="text-lg font-semibold">Expression Number</h3>
                </div>
                <p className="text-white/80 text-sm leading-relaxed">
                  Derived from your full name, this number reveals your natural abilities, talents, and how you express yourself to the world.
                </p>
              </div>

              <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 rounded-xl bg-white/10">
                    <Briefcase className="w-5 h-5" />
                  </div>
                  <h3 className="text-lg font-semibold">Destiny Number</h3>
                </div>
                <p className="text-white/80 text-sm leading-relaxed">
                  Also calculated from your name, this number indicates your life's mission and what you're destined to achieve in this lifetime.
                </p>
              </div>

              <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 rounded-xl bg-white/10">
                    <Home className="w-5 h-5" />
                  </div>
                  <h3 className="text-lg font-semibold">Soul Urge Number</h3>
                </div>
                <p className="text-white/80 text-sm leading-relaxed">
                  Based on the vowels in your name, this number reveals your inner desires, motivations, and what truly drives you from within.
                </p>
              </div>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6">How to Calculate Your Numbers</h2>
            <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
              <h3 className="text-lg font-semibold mb-4">Life Path Number Example:</h3>
              <div className="text-white/80 space-y-2 mb-4">
                <p>Birth Date: March 15, 1990</p>
                <p>Step 1: 3 + 15 + 1990 = 2008</p>
                <p>Step 2: 2 + 0 + 0 + 8 = 10</p>
                <p>Step 3: 1 + 0 = 1</p>
                <p><strong>Life Path Number: 1</strong></p>
              </div>
              <p className="text-white/80 text-sm">
                Continue reducing until you get a single digit (1-9) or master numbers (11, 22, 33).
              </p>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6">Number Meanings (1-9)</h2>
            <div className="grid md:grid-cols-3 gap-4">
              <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                <div className="text-2xl font-bold text-emerald-400 mb-2">1</div>
                <h4 className="font-semibold mb-2">The Leader</h4>
                <p className="text-white/70 text-sm">Independent, ambitious, pioneering spirit</p>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                <div className="text-2xl font-bold text-emerald-400 mb-2">2</div>
                <h4 className="font-semibold mb-2">The Diplomat</h4>
                <p className="text-white/70 text-sm">Cooperative, intuitive, peace-loving</p>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                <div className="text-2xl font-bold text-emerald-400 mb-2">3</div>
                <h4 className="font-semibold mb-2">The Creative</h4>
                <p className="text-white/70 text-sm">Expressive, optimistic, artistic</p>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                <div className="text-2xl font-bold text-emerald-400 mb-2">4</div>
                <h4 className="font-semibold mb-2">The Builder</h4>
                <p className="text-white/70 text-sm">Practical, organized, hardworking</p>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                <div className="text-2xl font-bold text-emerald-400 mb-2">5</div>
                <h4 className="font-semibold mb-2">The Explorer</h4>
                <p className="text-white/70 text-sm">Adventurous, freedom-loving, versatile</p>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                <div className="text-2xl font-bold text-emerald-400 mb-2">6</div>
                <h4 className="font-semibold mb-2">The Nurturer</h4>
                <p className="text-white/70 text-sm">Caring, responsible, family-oriented</p>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                <div className="text-2xl font-bold text-emerald-400 mb-2">7</div>
                <h4 className="font-semibold mb-2">The Seeker</h4>
                <p className="text-white/70 text-sm">Spiritual, analytical, introspective</p>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                <div className="text-2xl font-bold text-emerald-400 mb-2">8</div>
                <h4 className="font-semibold mb-2">The Achiever</h4>
                <p className="text-white/70 text-sm">Ambitious, material success, authoritative</p>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                <div className="text-2xl font-bold text-emerald-400 mb-2">9</div>
                <h4 className="font-semibold mb-2">The Humanitarian</h4>
                <p className="text-white/70 text-sm">Compassionate, generous, wise</p>
              </div>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-bold mb-6">How Astrooverz Uses Numerology</h2>
            <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
              <p className="text-white/80 leading-relaxed mb-4">
                Our AI-powered numerology analysis combines traditional calculations with modern insights to provide:
              </p>
              <ul className="text-white/80 space-y-2">
                <li>• Comprehensive life path analysis</li>
                <li>• Personality trait insights</li>
                <li>• Career and relationship compatibility</li>
                <li>• Lucky numbers and dates</li>
                <li>• Personal growth recommendations</li>
                <li>• Name change suggestions for better vibrations</li>
              </ul>
            </div>
          </section>
        </main>

        {/* CTA Section */}
        <section className="text-center bg-white/5 border border-white/10 rounded-2xl p-8">
          <h2 className="text-2xl font-bold mb-4">Discover Your Numerological Profile</h2>
          <p className="text-white/80 mb-6">
            Get detailed insights into your personality, life path, and destiny through our advanced numerology analysis.
          </p>
          <button className="bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-3 rounded-xl font-medium">
            Calculate My Numbers
          </button>
        </section>
      </div>
    </div>
  );
};

export default Numerology;

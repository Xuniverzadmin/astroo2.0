// Simple DashaWidget stub as per your scaffold
import React from 'react';
import { motion } from 'framer-motion';
import { Clock, X } from 'lucide-react';

export default function DashaWidget({ data, onClose }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
    >
      <div className="bg-slate-900 rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-700">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-fuchsia-600">
              <Clock size={24} className="text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white">Dasha Timeline</h2>
              <p className="text-gray-400">Planetary periods</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
          >
            <X size={24} className="text-gray-400" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          <div className="text-center py-12">
            <Clock size={64} className="text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-white mb-2">Dasha Timeline</h3>
            <p className="text-gray-400 mb-6">Connect to backend API to load real dasha data</p>
            {data && (
              <div className="bg-slate-800 rounded-lg p-4 text-left">
                <pre className="text-xs text-gray-300 overflow-auto">
                  {JSON.stringify(data, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
}

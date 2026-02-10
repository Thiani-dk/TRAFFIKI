/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      colors: {
        'road-black': '#1a1a1a',
        'road-yellow': '#fbbf24', // Amber-400
        'digital-red': '#ef4444',
        'digital-green': '#22c55e',
        'digital-amber': '#f59e0b',
      },
      fontFamily: {
        'digital': ['Courier New', 'Courier', 'monospace'], // Fallback for digital look
      }
    },
  },
  plugins: [],
}
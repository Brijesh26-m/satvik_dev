/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        obsidian: '#080808',
        'deep-black': '#0C0C0C',
        charcoal: '#151515',
        graphite: '#242424',
        'metallic-grey': '#3B3B3B',
        'champagne-gold': '#C6A15B',
        'molten-gold': '#E9D39A',
        'antique-gold': '#806234',
        'warm-ivory': '#F4EFE5',
        'muted-text': '#AAA49A',
        veg: '#22C55E',
      },
      fontFamily: {
        brand: ['Cinzel', '"Cormorant Garamond"', 'Playfair Display', 'serif'],
        editorial: ['Cinzel', '"Cormorant Garamond"', 'Playfair Display', 'serif'],
        cormorant: ['"Cormorant Garamond"', 'Cinzel', 'serif'],
        serif: ['Cinzel', '"Cormorant Garamond"', 'Playfair Display', 'serif'],
        haas: ['"Neue Haas Grotesk Display Pro"', '"Neue Haas Grotesk"', '"Helvetica Neue"', 'Helvetica', 'Inter', '"Plus Jakarta Sans"', 'sans-serif'],
        sans: ['"Neue Haas Grotesk Text Pro"', '"Neue Haas Grotesk"', '"Helvetica Neue"', 'Helvetica', '"Plus Jakarta Sans"', 'Inter', 'sans-serif'],
      },
      boxShadow: {
        'liquid-chrome': '0 8px 24px -4px rgba(0, 0, 0, 0.8), inset 0 1px 1px 0 rgba(233, 211, 154, 0.45), inset 0 -2px 4px 0 rgba(0, 0, 0, 0.9)',
        'liquid-gold-glow': '0 0 24px -2px rgba(198, 161, 91, 0.35)',
        'card-dark': '0 12px 32px -8px rgba(0, 0, 0, 0.75)',
      },
      animation: {
        'liquid-flow': 'liquidFlow 4s ease-in-out infinite alternate',
      },
      keyframes: {
        liquidFlow: {
          '0%': { backgroundPosition: '0% 50%' },
          '100%': { backgroundPosition: '100% 50%' },
        },
      },
    },
  },
  plugins: [],
};

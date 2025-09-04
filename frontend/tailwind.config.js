/** @type {import('tailwindcss').Config} */
export default {
content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
theme: {
extend: {
colors: {
brand: {
50: '#ECF6FF', 100: '#D9EEFF', 200: '#B2DCFF', 300: '#8AC9FF',
400: '#63B7FF', 500: '#3CA4FF', 600: '#2387E6', 700: '#1B69B4',
800: '#124B81', 900: '#0A2D4F'
}
},
backgroundImage: {
'grid': 'radial-gradient(circle at 1px 1px, rgba(255,255,255,0.12) 1px, transparent 0)',
'glow': 'radial-gradient(60% 60% at 50% 30%, rgba(60,164,255,0.25), rgba(10,45,79,0))'
}
}
},
plugins: []
}
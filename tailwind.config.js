/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "sunburst":'#F8C617',
        'midnight':'#252C37'
      },fontFamily: {
        montserrat: ['Montserrat', 'sans-serif'],
        playfair: ['Playfair Display', 'serif'],
        oswald: ['Oswald', 'sans-serif'],
        lora: ['Lora', 'serif'],
        bebas: ['Bebas Neue', 'sans-serif'],
        raleway: ['Raleway', 'sans-serif'],
        poppins: ['Poppins', 'sans-serif'],
        anton: ['Anton', 'sans-serif'],
        merriweather: ['Merriweather', 'serif'],
        abril: ['Abril Fatface', 'serif'],
      }
    },
  },
  plugins: [],
}
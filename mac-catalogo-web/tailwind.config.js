  /** @type {import('tailwindcss').Config} */
 export default {
    content: ["./src/**/*.{html,js}"],  
    theme: {
      extend: {},
    },
    plugins: [],
  }
  module.exports = {
  theme: {
    extend: {
      fontFamily: {
        'archivo-black': ['Archivo Black', 'sans-serif'],
        'archivo-regular': ['Archivo', 'sans-serif'],
        'archivo': ['Archivo', 'sans-serif'], // Por defecto
      },
    },
  },
}
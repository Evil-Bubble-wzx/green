/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: "#0ea5e9", dark: "#0284c7", light: "#38bdf8" },
        accent: { DEFAULT: "#10b981", dark: "#059669" },
        dark: { DEFAULT: "#0f172a", card: "#1e293b", lighter: "#334155" },
        warning: "#f59e0b",
        danger: "#ef4444",
      },
    },
  },
  plugins: [],
};

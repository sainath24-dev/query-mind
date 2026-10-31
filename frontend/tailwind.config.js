/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#0066cc",
          focus: "#0071e3",
          dark: "#0055b3",
          "on-dark": "#2997ff",
        },
        canvas: {
          DEFAULT: "#ffffff",
          parchment: "#f5f5f7",
        },
        surface: {
          pearl: "#fafafc",
          "tile-1": "#272729",
          "tile-2": "#2a2a2c",
          "tile-3": "#252527",
          black: "#000000",
        },
        ink: {
          DEFAULT: "#1d1d1f",
          "muted-80": "#333333",
          "muted-48": "#7a7a7a",
        },
        hairline: "#e0e0e0",
        "divider-soft": "#f0f0f0",
      },
      borderRadius: {
        sm: "8px",
        md: "11px",
        lg: "18px",
        pill: "9999px",
      },
      fontFamily: {
        sans: [
          "-apple-system",
          "BlinkMacSystemFont",
          '"SF Pro Text"',
          '"SF Pro Display"',
          '"Helvetica Neue"',
          "Helvetica",
          "Arial",
          "sans-serif",
        ],
        display: [
          "-apple-system",
          "BlinkMacSystemFont",
          '"SF Pro Display"',
          '"SF Pro Text"',
          '"Helvetica Neue"',
          "Helvetica",
          "Arial",
          "sans-serif",
        ],
        mono: [
          "SFMono-Regular",
          "Menlo",
          "Monaco",
          "Consolas",
          '"Liberation Mono"',
          '"Courier New"',
          "monospace",
        ],
      },
      letterSpacing: {
        "apple-tight": "-0.025em",
        "apple-body": "-0.022em",
      },
    },
  },
  plugins: [],
};

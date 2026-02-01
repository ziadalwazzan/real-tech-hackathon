import forms from "@tailwindcss/forms";

export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["'Fraunces'", "serif"],
        body: ["'Space Grotesk'", "sans-serif"],
      },
      colors: {
        ink: "#0f172a",
        mist: "#f8fafc",
        ocean: "#0ea5e9",
        lime: "#84cc16",
        amber: "#f59e0b",
        rose: "#f43f5e",
      },
      boxShadow: {
        glow: "0 24px 80px rgba(15, 23, 42, 0.18)",
      },
      keyframes: {
        floatIn: {
          "0%": { opacity: 0, transform: "translateY(16px)" },
          "100%": { opacity: 1, transform: "translateY(0)" },
        },
      },
      animation: {
        floatIn: "floatIn 0.6s ease-out both",
      },
    },
  },
  plugins: [forms],
};

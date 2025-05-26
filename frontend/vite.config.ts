import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
          mui: ["@mui/material", "@mui/x-data-grid"],
        },
      },
    },
  },
  server: {
    host: "0.0.0.0",
    port: 3000,
  },
});

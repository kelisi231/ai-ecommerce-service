import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      "/agent": "http://127.0.0.1:8000",
      "/login": "http://127.0.0.1:8000",
      "/knowledge": "http://127.0.0.1:8000",
      "/rag": "http://127.0.0.1:8000",
    },
  },
})
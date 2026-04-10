import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,
    port: 3000,
    allowedHosts: [
      'predly-api.onrender.com',
      'all'],
    proxy: {
      // Dev only: proxies /api → local Flask on 5001
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true,
      },
    },
  },
  // In production (Render), VITE_API_BASE_URL is set to the backend service URL.
  // In dev, it is empty so the proxy above handles /api calls.
  define: {
    __API_BASE__: JSON.stringify(process.env.VITE_API_BASE_URL || ''),
  },
})
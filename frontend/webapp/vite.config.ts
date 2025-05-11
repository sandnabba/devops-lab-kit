import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api/docs': {
        target: 'http://backend-dev-container:5000',
        changeOrigin: true,
        // Don't rewrite /api/docs paths, pass them through as-is
      },
      '/api/swagger.json': {
        target: 'http://backend-dev-container:5000',
        changeOrigin: true,
        // Don't rewrite /api/swagger.json, pass it through as-is
      },
      '/api': {
        target: 'http://backend-dev-container:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})

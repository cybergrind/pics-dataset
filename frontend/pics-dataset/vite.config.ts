import { sveltekit } from '@sveltejs/kit/vite'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    proxy: {
      '/api': 'http://localhost:8009',
      '/api/ws': {
        target: 'ws://localhost:8009',
        ws: true
      }
    }
  }
})

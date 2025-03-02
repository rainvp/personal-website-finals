import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    historyApiFallback: true // Fixes 404 on refresh in development
  }
});

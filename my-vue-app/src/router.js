import { createRouter, createWebHistory } from 'vue-router';
import Home from './components/NavbarBanner.vue';  // Home page
import Resume from './components/Resume.vue';
import Gallery from './components/Gallery.vue';
import Contact from './components/Contact.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/resume', component: Resume },
  { path: '/gallery', component: Gallery },
  { path: '/contact', component: Contact }
];

const router = createRouter({
  history: createWebHistory(),  // Ensure it's using Web History mode
  routes
});

export default router;

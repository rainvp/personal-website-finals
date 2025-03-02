import { createRouter, createWebHashHistory } from 'vue-router';  // Use Hash Mode
import NavbarBanner from './components/NavbarBanner.vue';
import Resume from './components/Resume.vue';
import Gallery from './components/Gallery.vue';
import Contact from './components/Contact.vue';

const routes = [
  { path: '/', component: NavbarBanner },
  { path: '/resume', component: Resume },
  { path: '/gallery', component: Gallery },
  { path: '/contact', component: Contact }
];

const router = createRouter({
  history: createWebHashHistory(),  // Use Hash Mode
  routes,
  scrollBehavior(to, from, savedPosition) {
    return { top: 0, behavior: 'smooth' }; // Ensures scrolling to top on navigation
  }
});

export default router;

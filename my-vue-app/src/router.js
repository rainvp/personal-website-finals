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
  routes
});

export default router;

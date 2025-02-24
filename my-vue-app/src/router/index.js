import { createRouter, createWebHistory } from 'vue-router';
import Resume from '../components/Resume.vue';  // Use relative path

const routes = [
  { path: '/resume', component: Resume }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

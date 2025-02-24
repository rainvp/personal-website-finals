import { createApp } from 'vue';
import Resume from './components/Resume.vue';

import './resume.css';

import AOS from 'aos';
import 'aos/dist/aos.css';

AOS.init();

const app = createApp(Resume);
app.mount('#resume-app');

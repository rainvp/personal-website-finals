import { createApp } from 'vue';
import Resources from './components/Resources.vue';

import './resources.css';

import AOS from 'aos';
import 'aos/dist/aos.css';

AOS.init();

const app = createApp(Resources);
app.mount('#resources-app');

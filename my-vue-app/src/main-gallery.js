import { createApp } from 'vue';
import Gallery from './components/Gallery.vue';

import './gallery.css';

import AOS from 'aos';
import 'aos/dist/aos.css';

AOS.init();

const app = createApp(Gallery);
app.mount('#gallery-app');

import { createApp } from 'vue';
import Contact from './components/Contact.vue';

import './contact.css';

import AOS from 'aos';
import 'aos/dist/aos.css';

AOS.init();

const app = createApp(Contact);
app.mount('#contact-app');

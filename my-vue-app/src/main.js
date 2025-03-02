import { createApp } from 'vue';
import App from './App.vue';

import NavbarBanner from './components/NavbarBanner.vue';
import Footer from './components/Footer.vue'; // Import Footer
import router from './router';

import './main.css';

import AOS from 'aos';
import 'aos/dist/aos.css';

const app = createApp(App);

AOS.init();

app.component('NavbarBanner', NavbarBanner);
app.component('Footer', Footer); // Register Footer component
app.use(router)

app.mount('#app');

import { createApp } from 'vue';
import App from './App.vue';

import CommentSection from './components/CommentSection.vue';
import NavbarBanner from './components/NavbarBanner.vue';
import Guestbook from './components/Guestbook.vue'
import Footer from './components/Footer.vue'; // Import Footer

import './main.css';

import AOS from 'aos';
import 'aos/dist/aos.css';

const app = createApp(App);

AOS.init();

app.component('CommentSection', CommentSection);
app.component('NavbarBanner', NavbarBanner);
app.component('Guestbook', Guestbook);
app.component('Footer', Footer); // Register Footer component

app.mount('#app');

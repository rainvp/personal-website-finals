<template>
  <div>
    <NavbarBanner />
    <Guestbook/>
    <router-view />
    <Footer />  <!-- Footer is used here -->
    
    
  </div>
</template>

<script setup>
import NavbarBanner from './components/NavbarBanner.vue';
import Guestbook from './components/Guestbook.vue';
import Footer from './components/Footer.vue'; 
</script>

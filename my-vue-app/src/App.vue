<template>
  <div>
    <router-view />
    <Guestbook/>
    <Footer />  <!-- Footer is used here -->
    
    
  </div>
</template>

<script setup>
import Guestbook from './components/Guestbook.vue';
import Footer from './components/Footer.vue'; 
</script>

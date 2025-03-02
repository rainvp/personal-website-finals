<template>
  <nav class="navbar">
    <div class="logo">
      <img 
        src="https://scontent.fmnl33-1.fna.fbcdn.net/v/t1.15752-9/474667107_1150394953328908_453092773794161443_n.png?_nc_cat=100&ccb=1-7&_nc_sid=9f807c&_nc_eui2=AeFtTV2Y3K0jKg0_2qV1Ho2xsF94E5Xqu6ewX3gTleq7pyQODnFyHMmvOYxLBKQlWA6rilKeyHQG2zaatLODHo2A&_nc_ohc=rpQ5djOAujEQ7kNvgHIFAZB&_nc_zt=23&_nc_ht=scontent.fmnl33-1.fna&oh=03_Q7cD1gF1ICi8zBFjshzJ24XNdz3oZT7SBQdxXjfFdQZv9Wfp3w&oe=67BFD3DF"
        alt="Rain's Cafe Logo">
    </div>   
  
    <div class="nav-links">
      <router-link to="/" class="nav-link"><b>Home</b></router-link>
      <router-link to="/resume" class="nav-link"><b>More</b></router-link>
      <router-link to="/gallery" class="nav-link"><b>Gallery</b></router-link>
      <router-link to="/contact" class="nav-link"><b>Contact</b></router-link>
        <div class="dropdown">
            <button class="dropbtn">
                <span class="dropdown-icon">&#x25BC;</span>
            </button>
            <div class="dropdown-content">
                <div class="dropdown-section">
                  <h4 class="dropdown-title">Menu</h4>
                  <a href="#menu1">Coffees</a>
                  <a href="#menu2">Pastries</a>
                  <a href="#menu3">Specials</a>
                </div>
                <div class="dropdown-section">
                  <h4 class="dropdown-title">Contact Us</h4>
                  <a href="#location">Our Location</a>
                  <a href="#support">Customer Support</a>
                </div>
                <div class="dropdown-section">
                  <h4 class="dropdown-title">Social</h4>
                  <a href="#facebook">Facebook</a>
                  <a href="#instagram">Instagram</a>
                  <a href="#twitter">Twitter</a>
                </div>
            </div>
        </div>
    </div> 
  </nav>

  <!-- Banner Section -->
  <header id="banner">
      <div id="banner-content" class="row clearfix">
          <div class="col-38">
              <div class="section-heading">
                  <h1>Steamed & Skilled</h1>
              </div>
          </div>
      </div>
  </header>

  <div class="contact-container">
    <h2 class="contact-title">Let's Connect! ☕</h2>
    <p class="contact-subtitle">Drop me a message and I'll get back to you soon!</p>
    
    <form @submit.prevent="submitForm" class="contact-form">
      <input v-model="name" type="text" placeholder="Your Name" required />
      <input v-model="email" type="email" placeholder="Your Email" required />
      <input v-model="subject" type="text" placeholder="Subject (optional)" />
      <textarea v-model="message" placeholder="Your Message" required></textarea>
      <button type="submit">Send Message ✉️</button>
    </form>
    
    <p v-if="confirmationMessage" class="confirmation-message">{{ confirmationMessage }}</p>
    
    <div class="contact-links">
      <p>Or reach me here:</p>
      <a href="mailto:your@email.com"><i class="fas fa-envelope"></i></a>
      <a href="https://twitter.com/yourprofile" target="_blank"><i class="fab fa-twitter"></i></a>
      <a href="https://instagram.com/yourprofile" target="_blank"><i class="fab fa-instagram"></i></a>
    </div>
  </div>

</template>

<script>
import { createClient } from '@supabase/supabase-js';
import { onMounted, ref, computed } from 'vue';

const supabaseUrl = 'https://kbhnxlrhbxamkgwyqpjn.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtiaG54bHJoYnhhbWtnd3lxcGpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg0Njc3NzEsImV4cCI6MjA1NDA0Mzc3MX0.lCXlrIXQaw3BvkzR9SBLGuxXnDAIscdkzcUpnn0KR-8';
const supabase = createClient(supabaseUrl, supabaseKey);
export default {
  data() {
    return {
      name: '',
      email: '',
      subject: '',
      message: '',
      confirmationMessage: ''
    };
  },
  methods: {
    async submitForm() {
      const { error } = await supabase.from('contact_messages').insert([
        { name: this.name, email: this.email, subject: this.subject, message: this.message }
      ]);
      
      if (!error) {
        this.confirmationMessage = '☕ Your message has been brewed and sent!';
        this.name = this.email = this.subject = this.message = '';
      } else {
        this.confirmationMessage = '⚠️ Oops! Something went wrong. Please try again.';
      }
    }
  }
};

</script>
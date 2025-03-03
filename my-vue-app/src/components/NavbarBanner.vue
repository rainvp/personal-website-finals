<template> 
    <nav class="navbar">
      <div class="logo">
        <img 
          src="https://github.com/rainvp/Personal-Profile-Webpage/blob/main/images/logo.png?raw=true"
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
    
 <!------------------------------------------ Banner Section --------------------------------------------------------------------->
        <header id="banner">
          <div id="banner-content" class="row clearfix">
            <div class="col-38">
              <div class="section-heading">
                <h1>Rain's Digital Café</h1>
              </div>
              <a href="#owner" class="button" @click.prevent="scrollToOwner">Get to know me!</a>
            </div>
          </div>
        </header>


<!-- About The Page Section -->
<div class="w3-container" id="about" data-aos="fade-up">
  <div class="w3-content">
    <h5 class="tag">ABOUT THE CAFE</h5>
    <p class="welcome-text"><b>Welcome to my personal profile webpage!</b></p>
    <p class="justified-text">
      This is my very first step into the world of web development. 
      I created this page to explore and learn the basics of building a website 
      while expressing my style through a cozy café-inspired theme. 
      It’s a small but meaningful project that represents the beginning of 
      my journey in web design and development.
    </p>
  </div>
</div>

<!-- About The Owner Section -->
<div class="w3-container" id="owner" data-aos="fade-up">
  <div class="w3-content owner-content">
    
    <!-- Title -->
    <div class="full-width">
      <h5 class="tag">ABOUT THE OWNER</h5>
    </div>

    <div class="owner-wrapper">
      <!-- Left Side: Text Content -->
      <div class="owner-text" data-aos="fade-right">
        <p><b> 🍵 Welcome to My Little Corner of the Internet Café! 🍵</b></p>
        <p>
          Just like a <span style="color: rgb(17, 71, 17)">well-whisked matcha</span>, I’m blending my passions into something smooth and vibrant. 
          I’m a <b>second-year Computer Science student specializing in Cybersecurity and Forensics</b>, 
          always striving to learn more and keep things secure—both online and in my dream café plans! 
          My goal? To brew a successful tech career in <b>Singapore</b>, but if a fulfilling path unfolds in the <b>Philippines</b>, 
          that would be just as refreshing.
        </p>
        <p>
          I’m also a <b>starting content creator</b> on TikTok, serving up beauty and 
          makeup content with the same care as crafting the <span style="color: rgb(17, 71, 17)">perfect iced matcha</span>. 
          One day, I hope to bring <b>SummerRain Café</b> to life—a cozy café featuring a library, boutique, and of course, delicious drinks and pastries!
        </p>

        <div class="w3-panel w3-leftbar w3-light-beige">
          <p><i>Life motto: "The sun will rise and we will try again"</i></p>
          <p><b>Founder: Rain Cel-Anne Sophia V. Presa</b></p> 
        </div>

        <!-- Interest List -->
        <h4 class="interest-title">🍵 A Few Things That Catch My Interest:</h4>
        <ul class="interest-list">
          <li>📺 Watching movies & series</li>
          <li>🎀 Collecting anything I find cute</li>
          <li>🎧 Listening to music</li>
          <li>💄 Makeup magic</li>
          <li>📖 Reading my heart out</li>
          <li>🍪 Baking sweet delights</li>
          <li>🎨 Exploring new hobbies (even if I struggle to finish them!)</li>
        </ul>

        <p>So, whether you're here for the matcha vibes, tech talk, or beauty content—stay a while, sip, and enjoy! ✨</p>
      </div>

      <!-- Right Side: Owner's Photos (Vertical) -->
      <div class="owner-gallery" data-aos="fade-left">
       <img src="https://github.com/rainvp/Personal-Profile-Webpage/blob/feature/4_rvp_finalswebsite/images/prof1.jpg?raw=true" alt="Owner's Photo">
       <img src="https://github.com/rainvp/Personal-Profile-Webpage/blob/feature/4_rvp_finalswebsite/images/prof2.jpg?raw=true" alt="Photo 1">
       <img src="https://github.com/rainvp/Personal-Profile-Webpage/blob/feature/4_rvp_finalswebsite/images/prof3.jpg?raw=true" alt="Photo 2">
       <img src="https://github.com/rainvp/Personal-Profile-Webpage/blob/feature/4_rvp_finalswebsite/images/prof4.jpg?raw=true" alt="Photo 3">
    </div>

    </div>

  </div>
</div>



<br>
<br>
<div class="guest-section" data-aos="zoom-in">
        <h2 class="tag">Leave a little trace of yourself, like coffee rings on a well-loved table.☕✨</h2>
        <div class="guest-container">
            <div class="guest-form">
                <h2>Sign the Guestbook</h2>
                <form @submit.prevent="addGuest">
                  <input v-model="name" type="text" placeholder="Your Name" required />
                  <input v-model="email" type="email" placeholder="Your Email (optional)">
                  <textarea v-model="message" placeholder="Say something (optional)"></textarea>
                  <button type="submit">Submit</button>
                </form>
            </div>


            <div class="guest-box" ref="guestListRef"> 
                <h2>Guestbook</h2>
                <ul ref="guestListRef">
  <li 
    v-for="(guest, index) in guests" 
    :key="index" 
    class="guest-entry" 
    :class="{'sparkle': guest.sparkle}"
  >
    <strong>{{ guest.name }}</strong>
    <p v-if="guest.message">{{ guest.message }}</p>
  </li>
</ul>

            </div>
        </div>
    </div>
        
    </template>



<script>
import { ref, onMounted, nextTick } from 'vue';
import supabase from '../lib/supabaseClient';
import AOS from 'aos';
import 'aos/dist/aos.css';

export default {
  setup() {
    const name = ref('');
    const email = ref('');
    const message = ref('');
    const guests = ref([]);
    const guestListRef = ref(null); // Reference to the guest list container

    const scrollToOwner = () => {
  const ownerSection = document.getElementById("owner");
  if (ownerSection) {
    ownerSection.scrollIntoView({ behavior: "smooth" });
  }
}

    const fetchGuests = async () => {
      try {
        const { data, error } = await supabase
          .from('guestbook')
          .select('name, message'); // Exclude email for privacy

        if (error) throw error;

        console.log('Fetched guests from Supabase:', data); // Debugging
        guests.value = [...data]; // Force reactivity update

      } catch (err) {
        console.error('Error fetching guests:', err.message);
      }
    };

    const addGuest = async () => {
      if (!name.value.trim()) return; // Only require a name

      try {
        const { data, error } = await supabase.from('guestbook').insert([
          {
            name: name.value,
            email: email.value.trim() || null, // Stores null if empty
            message: message.value
          }
        ]).select('*'); // Fetch the inserted row

        if (error) throw error;

        if (data.length > 0) {
          guests.value.push({ name: data[0].name, message: data[0].message, sparkle: true });

          // Store the email in localStorage if provided
          if (data[0].email) {
            localStorage.setItem("user_email", data[0].email);
          }
        }

        await nextTick(); // Wait for DOM update

        // Auto-scroll only within guest-box
        const guestList = guestListRef.value;
        if (guestList) {
          guestList.scrollTop = guestList.scrollHeight; // Scroll to the bottom of guest-box
        }

        // Remove sparkle effect after 1s
        setTimeout(() => {
          guests.value[guests.value.length - 1].sparkle = false;
        }, 1000);

        name.value = '';
        email.value = ''; // Reset email field
        message.value = '';
      } catch (err) {
        console.error('Error adding guest:', err.message);
      }
    };

    const login = async (email, password) => {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password
      });

      if (data.user) {
        localStorage.setItem("user_email", data.user.email); // Store email in localStorage
      }
    };

    const signUp = async (email, password) => {
      const { data, error } = await supabase.auth.signUp({
        email,
        password
      });

      if (data.user) {
        localStorage.setItem("user_email", data.user.email); // Store email in localStorage
      }
    };

    // Fetch guests when the component is mounted
    onMounted(() => {
      AOS.init(); // Initialize AOS animations properly
      fetchGuests(); // Ensure guestbook entries load correctly
    });

    return { name, email, message, guests, addGuest, guestListRef, scrollToOwner};
  }
};


</script>
    
    <style>


    </style>
    
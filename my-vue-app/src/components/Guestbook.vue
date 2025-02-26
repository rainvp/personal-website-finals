<template>

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
    ]);
    if (error) throw error;

    guests.value.push({ name: name.value, message: message.value, sparkle: true });

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

    // Fetch guests when the component is mounted
    onMounted(() => {
      AOS.init(); // Initialize AOS animations properly
      fetchGuests(); // Ensure guestbook entries load correctly
    });

    return { name, email, message, guests, addGuest, guestListRef };
  }
};


</script>

  
<style scoped>
/* --- 1. Overall Guest Section --- */
.guest-section {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  margin-bottom: 35px;
  padding: 15px;
  background: #f4e4d7;
  font-family: 'Press Start 2P', cursive;
  border: 8px solid #8b5e3c;
  box-shadow: 8px 8px 0px #5e3d2b;
  text-align: center;
}

h2 {
  font-size: 16px;
  font-family: 'Press Start 2P', cursive;
}
.tag {
  font-size: 16px;
  font-family: 'Press Start 2P', cursive;
}

.guest-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

/* --- 2. Guest Form & Guest Box Styling (Pixel Art Look) --- */
.guest-form{
  width: 50%;
  margin: 20px;
  background: #d2b48c;
  padding: 15px;
  border-radius: 0px;
  border: 4px solid #8b5e3c;
  box-shadow: 6px 6px 0px #5e3d2b;
  position: relative;
}

.guest-box {
  width: 50%;
  margin: 20px;
  background: #d2b48c;
  padding: 15px;
  border: 4px solid #8b5e3c;
  box-shadow: 6px 6px 0px #5e3d2b;
  position: relative;
  max-height: 350px; /* Adjust height as needed */
  overflow-y: auto; /* Enables scrolling inside the box */
}

/* Hide scrollbar in WebKit browsers but still allow scrolling */
.guest-box::-webkit-scrollbar {
  width: 8px;
}

.guest-box::-webkit-scrollbar-thumb {
  background-color: #8b5e3c;
  border-radius: 4px;
}

.guest-box::-webkit-scrollbar-track {
  background: #d2b48c;
}

/* --- 3. Input & Textarea with Pixel Borders --- */
input, textarea {
  width: 100%;
  padding: 12px;
  margin-bottom: 10px;
  font-family: inherit;
  border: 3px solid #8b5e3c;
  background: #fff8dc;
  outline: none;
  box-shadow: 4px 4px 0px #5e3d2b;
}

/* Push-up effect */
input:focus {
  outline: none;
  transform: translateY(-3px);
  box-shadow: 2px 2px 0px #5e3d2b;
  margin-bottom: 16px; /* Slightly increases spacing below */
}

textarea:focus {
  outline: none;
  transform: translateY(-3px);
  box-shadow: 2px 2px 0px #5e3d2b;
  margin-bottom: 16px; /* Slightly increases spacing below */
}
/* Adjust margin of the next sibling to push it back */
input:focus + textarea {
  margin-top: -8px;
}

textarea:focus + button {
  margin-top: -8px;
}

/* --- 4. Pixel-Style Button --- */
button {
  background: #8b5e3c;
  color: white;
  border: 3px solid #5e3d2b;
  padding: 12px;
  width: 100%;
  cursor: pointer;
  font-size: 14px;
  text-transform: uppercase;
  box-shadow: 4px 4px 0px #5e3d2b;
  transition: transform 0.1s;
}

/* Retro Button Click Effect */
button:active {
  transform: translate(3px, 3px);
  box-shadow: 2px 2px 0px #5e3d2b;
}

/* --- 5. Guest Entries with Pixel Edges & Glow --- */
.guest-box ul {
  list-style: none;
  padding: 0;
}

.guest-entry {
  background: #fff8dc; /* Warm background */
  padding: 10px; /* Slightly more padding for overall content */
  margin: 8px 0;
  border: 3px solid #8b5e3c; /* Brown border */
  box-shadow: 4px 4px 0px #5e3d2b; /* Vintage-style shadow */
  font-size: 16px; 
  position: relative;
  display: flex;
  flex-direction: column; /* Stack content vertically */
  gap: 5px; /* Space between elements */
}

.guest-entry strong {
  font-size: 14px; /* Slightly larger for names */
  font-weight: bold;
  padding: 0; /* Remove excess padding */
  margin: 0; /* Reset margins */
}

.guest-entry p {
  font-size: 15px; /* A little smaller for messages */
  font-family: cursive; /* Stylish handwriting effect */
  color: #555;
  margin: 0; /* Reset margin */
}



/* --- 6. Sparkle Animation (More Pixelated Look) --- */
.sparkle {
  position: relative;
}

.sparkle::after,
.sparkle::before {
  content: '✨';
  position: absolute;
  font-size: 55px;
  text-shadow: 2px 2px 0px #ffdf70;
  animation: sparkle 1s infinite alternate;
}

.sparkle::after {
  top: -12px;
  right: -12px; /* Top right corner */
}

.sparkle::before {
  bottom: -12px;
  left: -12px; /* Bottom left corner */
}


/* --- 7. Responsive Tweaks --- */
@media (max-width: 768px) {
  .guest-container {
    flex-direction: column;
    align-items: center;
  }

  .guest-form, .guest-box {
    width: 90%;
    margin: 20px;
  }
}

  </style>
  
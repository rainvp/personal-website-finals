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
                    <textarea v-model="message" placeholder="Say something (optional)"></textarea>
                    <button type="submit">Submit</button>
                </form>
            </div>
            <div class="guest-box">
                <h2>Guestbook</h2>
                <ul>
                    <li v-for="(guest, index) in guests" :key="index" class="guest-entry" :class="{'sparkle': guest.sparkle}">
                        <strong>{{ guest.name }}</strong>
                        <p v-if="guest.message">{{ guest.message }}</p>
                    </li>
                </ul>
            </div>
        </div>
    </div>
  </template>
  
  <script>
import { ref, onMounted } from 'vue';
import { createClient } from '@supabase/supabase-js';

// Supabase setup
const supabase = createClient('https://your-project.supabase.co', 'your-anon-key');

export default {
  setup() {
    const name = ref('');
    const message = ref('');
    const guests = ref([]);

    // Fetch guests from Supabase
    const fetchGuests = async () => {
      try {
        const { data, error } = await supabase.from('guestbook').select('*');
        if (error) throw error;
        guests.value = data;
      } catch (err) {
        console.error('Error fetching guests:', err.message);
      }
    };

    // Add a new guest entry
    const addGuest = async () => {
      if (!name.value.trim() || !message.value.trim()) return; // Prevent empty entries

      try {
        const { data, error } = await supabase.from('guestbook').insert([
          { name: name.value, message: message.value }
        ]);
        if (error) throw error;

        guests.value.push({ name: name.value, message: message.value, sparkle: true });

        // Remove sparkle effect after animation
        setTimeout(() => {
          guests.value[guests.value.length - 1].sparkle = false;
        }, 1000);

        // Clear input fields
        name.value = '';
        message.value = '';
      } catch (err) {
        console.error('Error adding guest:', err.message);
      }
    };

    // Fetch guests when the component is mounted
    onMounted(() => {
      AOS.init(); // Initialize AOS animations
      document.querySelector('.guest-section')?.classList.add('pixel-bounce');
      fetchGuests();
    });

    return { name, message, guests, addGuest };
  }
};
</script>

  
<style scoped>
/* --- 1. Overall Guest Section --- */
.guest-section {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  margin-bottom: 50px;
  padding: 20px;
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
  width: 48%;
  margin: 20px;
  background: #d2b48c;
  padding: 15px;
  border-radius: 0px;
  border: 4px solid #8b5e3c;
  box-shadow: 6px 6px 0px #5e3d2b;
  position: relative;
}

.guest-box {
  width: 48%;
  margin: 20px;
  background: #d2b48c;
  padding: 15px;
  border: 4px solid #8b5e3c;
  box-shadow: 6px 6px 0px #5e3d2b;
  position: relative;
  max-height: 300px; /* Adjust height as needed */
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

/* Retro Button Click Effect */
input:active {
  transform: translate(3px, 3px);
  box-shadow: 2px 2px 0px #5e3d2b;
}

/* Retro Button Click Effect */
textarea:active {
  transform: translate(3px, 3px);
  box-shadow: 2px 2px 0px #5e3d2b;
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
  background: #fff8dc;
  padding: 12px;
  margin: 5px 0;
  border: 3px solid #8b5e3c;
  box-shadow: 4px 4px 0px #5e3d2b;
  font-size: 14px;
  position: relative;
}

/* --- 6. Sparkle Animation (More Pixelated Look) --- */
.sparkle::after {
  content: '✨';
  position: absolute;
  top: -12px;
  right: -12px;
  animation: sparkle 1s infinite alternate;
  font-size: 16px;
  text-shadow: 2px 2px 0px #ffdf70;
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

@keyframes pixel-jump {
  0% { transform: translateY(0); }
  25% { transform: translateY(-5px); }
  50% { transform: translateY(0); }
  75% { transform: translateY(-3px); }
  100% { transform: translateY(0); }
}

[data-aos="pixel-bounce"] {
  animation: pixelBounce 0.5s ease-in-out;
}



  </style>
  
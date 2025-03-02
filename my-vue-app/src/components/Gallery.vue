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

    <br>
  
    <!-- Banner Section -->
    <header id="banner">
        <div id="banner-content" class="row clearfix">
            <div class="col-38">
                <div class="section-heading">
                    <h1>Capture & Connect</h1>
                </div>
            </div>
        </div>
    </header>

<!-- Section Title (Properly Positioned) -->

<!-- Gallery Container -->
<div class="gallery-container" data-aos="fade-up">
  <h5 class="tag">Camera Crumbs 📸🍪</h5>
  <div class="gallery-slider">
    <button class="slider-nav left-arrow" @click="prevSlide">&#10094;</button>
    <div class="slider-images-wrapper">
      <div v-for="image in currentImages" :key="image.id" class="slider-image">
        <img :src="image.src" class="gallery-img" />
      </div>
    </div>
    <button class="slider-nav right-arrow" @click="nextSlide">&#10095;</button>
  </div>

  <!-- Caption Below the Slider -->
  <div class="slider-caption">
    <p>{{ currentCaption }}</p>
  </div>
</div>

<br>
<br>

<div id="app">
    <div id="app-comments" class="comments-section" data-aos="zoom-in-up">
      <h2 class="section-title">Share your thoughts!💬</h2>

      <!-- Comment Form -->
      <form @submit.prevent="addComment" class="comment-form">
        <input v-model="newComment.name" type="text" placeholder="Your Name" required />
        <textarea v-model="newComment.comment" placeholder="Write a comment..." required></textarea>
        <button type="submit">Post Comment</button>
      </form>

      <!-- Comments List -->
      <div class="comments-list">
        <div v-for="comment in comments" :key="comment.id" class="comment-box">
          <p><strong>{{ comment.name }}</strong>: {{ comment.comment }}</p>
          <span>{{ formatTimestamp(comment.created_at) }}</span>

          <!-- Reactions -->
          <div class="reactions">
            <button @click="toggleReaction(comment.id, 'laughs')">
              😂 <span>{{ comment.reactions.laughs }}</span>
            </button>
            <button @click="toggleReaction(comment.id, 'loves')">
              ❤️ <span>{{ comment.reactions.loves }}</span>
            </button>
            <button @click="toggleReaction(comment.id, 'dislikes')">
              👎 <span>{{ comment.reactions.dislikes }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>


</template>

<script>
import { ref, onMounted, computed } from 'vue';
import supabase from '../lib/supabaseClient';

export default {
  setup() {
    // Comment Section
    const comments = ref([]);
    const newComment = ref({ name: '', comment: '' });

    // Retrieve stored user email from guestbook
    const storedEmail = localStorage.getItem("user_email") || null;

    const fetchComments = async () => {
      try {
        let { data, error } = await supabase
          .from('comments')
          .select('*')
          .order('created_at', { ascending: false });

        if (error) throw error;

        comments.value = data.map(comment => ({
          ...comment,
          reactions: { laughs: 0, loves: 0, dislikes: 0 }, // Default state
        }));

        // Batch fetch reactions for efficiency
        await Promise.all(comments.value.map(comment => fetchReactions(comment.id)));

      } catch (err) {
        console.error("Error fetching comments:", err);
      }
    };

    const fetchReactions = async (commentId) => {
      try {
        const response = await fetch(`http://localhost:5001/get_reactions?comment_id=${commentId}`);
        const data = await response.json();

        if (data.reactions) {
          comments.value = comments.value.map(comment =>
            comment.id === commentId ? { ...comment, reactions: data.reactions } : comment
          );
        }
      } catch (error) {
        console.error("Error fetching reactions:", error);
      }
    };

    const addComment = async () => {
      if (!newComment.value.name || !newComment.value.comment) return;

      try {
        let { data, error } = await supabase
          .from('comments')
          .insert([
            {
              name: newComment.value.name,
              comment: newComment.value.comment,
              email: storedEmail, // Attach stored email if available
              created_at: new Date().toISOString(),
            }
          ])
          .select('*');

        if (!error && data.length > 0) {
          let newCommentData = {
            ...data[0],
            reactions: { laughs: 0, loves: 0, dislikes: 0 }
          };
          comments.value.unshift(newCommentData);
          newComment.value = { name: newComment.value.name, comment: '' }; // Retain name
        }
      } catch (error) {
        console.error("Error adding comment:", error);
      }
    };

    const toggleReaction = async (commentId, reactionType) => {
      if (!storedEmail) {
        console.error("User not recognized (not in guestbook)");
        return;
      }

      try {
        const response = await fetch("http://localhost:5001/toggle_reaction", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            comment_id: commentId,
            reaction_type: reactionType,
            user_email: storedEmail // Use stored email instead of auth
          }),
        });

        const result = await response.json();
        console.log(result.message);

        // Fetch updated reactions
        fetchReactions(commentId);
      } catch (error) {
        console.error("Error toggling reaction:", error);
      }
    };

    const formatTimestamp = (timestamp) => {
      return timestamp ? new Date(timestamp).toLocaleString() : "Unknown time";
    };

    onMounted(() => {
      fetchComments();

      // Subscribe to real-time updates for new comments
      supabase
        .channel('comments')
        .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'comments' }, (payload) => {
          let newComment = { ...payload.new, reactions: { laughs: 0, loves: 0, dislikes: 0 } };
          comments.value.unshift(newComment);
        })
        .subscribe();

      // Subscribe to real-time updates for reactions
      supabase
        .channel('reactions')
        .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'reactions' }, (payload) => {
          fetchReactions(payload.new.comment_id);
        })
        .subscribe();
    });

    // Auto-fill name if user already signed guestbook
    const storedName = localStorage.getItem("user_name") || '';
    newComment.value.name = storedName;

    // Gallery Section
    const images = ref([
      { id: 1, src: 'https://github.com/rainvp/Personal-Profile-Webpage/blob/main/images/460961978_967543388415623_4541161538742405339_n.jpg?raw=true' },
      { id: 2, src: 'https://github.com/rainvp/Personal-Profile-Webpage/blob/main/images/472789858_1157284476015373_4532978188250656890_n.jpg?raw=true' },
      { id: 3, src: 'https://github.com/rainvp/Personal-Profile-Webpage/blob/main/images/472478541_1393676961599516_8296656406198264170_n.jpg?raw=true' },
      { id: 4, src: 'https://github.com/rainvp/Personal-Profile-Webpage/blob/main/images/363829702_970044974249532_9015369949003698015_n.jpg?raw=true' },
      { id: 5, src: 'https://raw.githubusercontent.com/rainvp/Personal-Profile-Webpage/refs/heads/main/images/4ebab79f-86d0-41ab-b557-e37c20843d4b.jfif' },
      { id: 6, src: 'https://github.com/rainvp/Personal-Profile-Webpage/blob/main/images/472699294_466149492989920_1496860658682248426_n.jpg?raw=true' },
      { id: 7, src: 'https://github.com/rainvp/Personal-Profile-Webpage/blob/main/images/8DD1B940-891E-44AA-BFCC-A3BE20992CDB.jpg?raw=true' },
      { id: 8, src: 'https://github.com/rainvp/Personal-Profile-Webpage/blob/main/images/af29de30-95ab-420c-90d6-6d6e91d783d3.jpg?raw=true' },
      { id: 9, src: 'https://github.com/rainvp/Personal-Profile-Webpage/blob/main/images/IMG_3543%20(2).JPG?raw=true' },
    ]);

    const captions = ref([
      'Slide 1: Welcome to the gallery!',
      'Slide 2: Highlights of the journey.',
      'Slide 3: Moments captured in time.',
    ]);

    const currentIndex = ref(0);
    const itemsPerSlide = 3;

    const currentImages = computed(() => {
      const start = currentIndex.value * itemsPerSlide;
      return images.value.slice(start, start + itemsPerSlide);
    });

    const currentCaption = computed(() => captions.value[currentIndex.value] || '');

    const prevSlide = () => {
      currentIndex.value = (currentIndex.value === 0) 
        ? Math.floor(images.value.length / itemsPerSlide) 
        : currentIndex.value - 1;
    };

    const nextSlide = () => {
      currentIndex.value = ((currentIndex.value + 1) * itemsPerSlide >= images.value.length) 
        ? 0 
        : currentIndex.value + 1;
    };

    return {
      // Comments
      comments,
      newComment,
      addComment,
      toggleReaction,
      formatTimestamp,

      // Gallery
      images,
      captions,
      currentIndex,
      currentImages,
      currentCaption,
      prevSlide,
      nextSlide,
    };
  }
};

</script>

<style scoped>
body, html {
    height: 100%;
    font-family: 'Poppins', sans-serif;
    margin: 0;
    color: #4a3b2b;
    background-color: #fcf5e8;
}

 .menu {
    display: none;
 }

 a {
    text-decoration: none;
    color: inherit;
    transition: color 0.3s;
}

p {
   font-size: 18px;
}

.tag {
  width: 100%;
  font-size: 28px;
  font-weight: bold;
  color: #5a391f;
  margin-bottom: 2px;
  text-transform: uppercase;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 50px;
  margin-bottom: 50px;
  font-weight: bold;
  letter-spacing: 2px; /* Add some spacing between letters */
  position: relative; /* For positioning the lines */
}

.tag::before {
  content: "";
  flex: 1; 
  height: 3px; 
  flex-grow: 5; /* Makes the lines expand further */
  background: linear-gradient(to right, #d4b59b, #502917);
  margin: 0 15px;
}
.tag::after {
  content: "";
  flex: 1; 
  flex-grow: 5; /* Makes the lines expand further */
  height: 3px; 
  background: linear-gradient(to left, #d4b59b, #502917); /* Gradient effect */
  margin: 0 15px;
}


/*--------------------------------------------- Custom Styles------------------------------------------- */

/* ---------------------------------------- Navigation Bar ---------------------------------------------- */
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    background-color: #f7e7d1; 
    color: #4a3b2b;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    z-index: 1000;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1); 
}

.navbar .logo img {
    height: 65px; /* Adjust the height of the logo */
    width: auto; /* Maintain aspect ratio */
    display: block; /* Ensure proper spacing around the image */
}


.nav-links {
  display: flex;
  align-items: center;
}

/* Ensure both <a> and <router-link> look the same */
.navbar a, 
.navbar .nav-link {
  color: #4a3b2b;
  font-size: 20px;
  text-decoration: none;
  padding: 10px 25px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.navbar a:hover, 
.navbar .nav-link:hover {
  background-color: #d4b59b;
  color: #fff;
  border-radius: 5px;
}

/* Dropdown styling */
.dropdown {
    position: relative;
    display: inline-block;
}

.dropbtn {
    background-color: transparent;
    border: none;
    cursor: pointer;
    font-size: 16px;
    color: #4a3b2b;
    padding: 10px 15px;
    transition: color 0.3s ease;

      /* Remove unwanted shadows */
  box-shadow: none;
  text-shadow: none;
}

.dropbtn:hover {
    color: #d4b59b;
}

/* Dropdown icon */
.dropdown-icon {
    font-size: 16px;
    margin-left: 5px;
    transition: transform 0.3s ease; /* Animation for rotation */
}

/* Dropdown content */
.dropdown-content {
    display: none;
    position: absolute;
    right: 0; /* Align dropdown below the icon */
    background-color: #fff;
    box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
    z-index: 1;
    min-width: 250px;
    border-radius: 5px;
    opacity: 0;
    visibility: hidden;
    transform: translateY(10px); /* Start with a slight downward position */
    transition: opacity 0.3s ease, visibility 0.3s ease, transform 0.3s ease; /* Smooth fade-in and slide-up */
}

/* Dropdown sections */
.dropdown-section {
    padding: 15px;
    border-bottom: 1px solid #f7e7d1;
}

.dropdown-title {
    font-size: 16px;
    font-weight: bold;
    color: #4a3b2b;
    margin-bottom: 10px;
    text-transform: uppercase; /* Optional: Make titles uppercase for a neat look */
}

/* Dropdown items */
.dropdown-content a {
    color: #4a3b2b;
    padding: 8px 15px;
    text-decoration: none;
    display: block;
    transition: background-color 0.3s ease;
}

.dropdown-content a:hover {
    background-color: #f7e7d1;
}

/* Show dropdown on hover */
.dropdown:hover .dropdown-content {
    display: block;
    opacity: 1;
    visibility: visible;
    transform: translateY(0); /* Slide to the original position */
}

/* Rotate the arrow when dropdown is open */
.dropdown:hover .dropdown-icon {
    transform: rotate(180deg); /* Rotate arrow */
}

/* Responsive Design */
@media screen and (max-width: 768px) {
    .nav-links a {
        font-size: 16px;  /* Decrease font size for small screens */
        padding: 8px 12px;
    }

    .dropdown-content a {
        font-size: 14px;  /* Make dropdown text smaller */
    }

    .dropbtn {
        font-size: 14px;  /* Adjust dropdown button size */
        padding: 8px 10px;
    }

    /* Reduce logo size for small screens */
    .navbar .logo img {
        height: 50px;
    }

    /* Reduce padding of navbar */
    .navbar {
        padding: 8px 15px;
    }
}
/* ------------------------------------------------ Banner & Header ---------------------------*/
#banner {
    height: 100vh;
    display: flex;
    justify-content: flex-start; 
    align-items: center; 
    padding-left: 90px;
    padding-top: 20px;  
    position: relative;
    overflow: hidden;
    background-position: center;
    background-size: cover;
    background-image: url("https://i.pinimg.com/originals/07/91/1f/07911f8ccbaa7f0462acd7ac534f020f.gif");
    min-height: 75%;
}

/* Optional Gradient Overlay for a softer look */
#banner:before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(rgba(241, 179, 121, 0.39), rgba(255, 255, 255, 0.5));
}

/* Banner content section */
#banner-content {
    animation: fadeInLeft 1.5s ease-out;
    max-width: 50%; /* Restrict the content width */
    z-index: 2; /* Ensures content is above the background */
    position: relative;
    text-align: left;
}

/* Header styling */
#banner h1 {
    font-size: 5em;
    color:#fffaf5;
    margin-bottom: 15px;
    animation: fadeInLeft 1.5s ease-out;
    font-family: 'Poppins', sans-serif;
    letter-spacing: 2px; 
    font-weight: bold;
    line-height: 1.2;
}

/* Subheading styling */
#banner h2 {
    font-size: 1.8em;
    margin-bottom: 30px;
    animation: fadeInLeft 1.5s ease-out;
    font-style: italic;
    letter-spacing: 1px;
    font-family: 'Arial', sans-serif;
    line-height: 1.5;
}

/* Button styling */
#banner .button {
    background-color: #502917;
    color: #fff;
    margin-top: 15px;
    padding: 22px;
    text-decoration: none;
    border-radius: 30px;
    font-size: 20px;
    transition: background-color 0.3s, transform 0.3s;
    position: relative;
    display: inline-block; 
    text-align: center;
}

/* Add hover effect */
#banner .button:hover {
    background-color: #6a3d22;
    transform: scale(1.05); 
}

/* Responsive adjustments */
@media (max-width: 768px) {
    #banner .button {
        padding: 0.8em 1.5em; /* Adjust padding for smaller screens */
        font-size: 1rem; /* Adjust font size */
    }
}

@media (max-width: 480px) {
    #banner .button {
        padding: 0.6em 1em; /* Further adjust for very small screens */
        font-size: 0.9rem;
        margin: 0.5em;
    }
}

/* Fade-in left animation */
@keyframes fadeInLeft {
    0% {
        opacity: 0;
        transform: translateX(-50px);
    }
    100% {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Centering and limiting gallery size */
.gallery-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 1500px;
  margin: auto;
  padding: 10px;
}

/* Gallery slider layout */
.gallery-slider {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  width: 100%;
  max-width: 1200px;
  height: auto;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  background-color: #f7e7d1;
}

/* Image wrapper */
.slider-images-wrapper {
  display: flex;
  transition: transform 0.5s ease-in-out;
  width: 100%;
}

/* Individual image */
.slider-image {
  flex: 0 0 calc(100% / 3);
  max-width: calc(100% / 3);
  padding: 5px;
  box-sizing: border-box;
}

.gallery-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.slider-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  font-size: 24px;  /* Adjust arrow size */
  color: white;
  background-color: rgba(0, 0, 0, 0.6);  /* Less opacity */
  border: none;
  border-radius: 50%;  /* Ensures it's circular */
  padding: 10px;  /* Adjust padding */
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;  /* Fixed size */
  height: 40px;  /* Fixed size */

    /* Remove unwanted shadows */
  box-shadow: none;
  text-shadow: none;
}

.slider-nav:hover {
  background-color: rgba(0, 0, 0, 0.8);
}


.left-arrow {
  left: 15px;  /* Adjusted for equal spacing */
}

.right-arrow {
  right: 15px; /* Adjusted for equal spacing */
}


/* Caption styling */
.slider-caption {
  text-align: center;
  font-size: 14px;
  color: #551f18;
  font-family: "Inconsolata", sans-serif;
  margin-top: 10px;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .gallery-slider {
    max-width: 900px;
  }
  .slider-image {
    flex: 0 0 calc(100% / 2);
    max-width: calc(100% / 2);
  }
}

@media (max-width: 768px) {
  .gallery-slider {
    max-width: 600px;
  }
  .slider-image {
    flex: 0 0 100%;
    max-width: 100%;
  }
  .slider-nav {
    font-size: 24px;
    padding: 6px 10px;
  }
}

@media (max-width: 480px) {
  .gallery-slider {
    max-width: 100%;
  }
  .slider-nav {
    font-size: 20px;
    padding: 5px 8px;
  }
}
  /* Comments Section */
  .comments-section {
    max-width: 1000px;
    width: 100%;
    margin: 2rem auto;
    margin-bottom: 85px;
    padding: 20px;
    background: #f4e4d7;
    font-family: cursive;
    border: 4px solid #c99f82;
    box-shadow: 8px 8px 0px #5e3d2b;
    text-align: center;
  }
  
  /* Title Styling */
  .comments-section h2 {
    font-size: 24px;
    color: #755049;
    margin-bottom: 1rem;
    font-weight: bold;
    font-family: 'Press Start 2P';
  }
  
  /* Comment Form */
  .comment-form {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 1.2rem;
  }
  
  .comment-form input,
  .comment-form textarea {
    width: 100%;
    padding: 12px;
    font-family: inherit;
    border: 2px solid #c98b72;
    border-radius: 3px;
    font-size: 1rem;
    background: #fffaf5;
    color: #4a3f35;
    box-shadow: 4px 4px 0px #5e3d2b;
  }
  

  .comment-form textarea {
    resize: none;
    min-height: 100px;
  }
  
  .comment-form button {
    padding: 12px;
    background: #c48d74;
    color: white;
    font-size: 12px;
    font-family: 'Press Start 2P';
    letter-spacing: 2px;
    border: none;
    text-transform: uppercase;
    border-radius: 3px;
    cursor: pointer;
    transition: 0.3s;
    cursor: pointer;
    font-weight: bold;
    transition: transform 0.1s;
    box-shadow: 4px 4px 0px #5e3d2b;
  }

/* Push-up effect */
.comment-form input:focus,
.comment-form textarea:focus {
  outline: none;
  transform: translateY(-3px);
  box-shadow: 2px 2px 0px #5e3d2b;
  margin-bottom: 16px; /* Slightly increases spacing below */
}

/* Adjust margin of the next sibling to push it back */
.comment-form input:focus + textarea,
.comment-form textarea:focus + button {
  margin-top: -8px;
}
/* Retro Button Click Effect */
.comment-form button:active {
  transform: translate(3px, 3px);
  box-shadow: 2px 2px 0px #5e3d2b;
}

  /* Comments List */
  .comments-list {
    margin-top: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 15px;
    padding: 0 10px;
  }
  
  /* Comment Box */
  .comment-box {
    background: #ffeadd;
    padding: 14px;
    border-radius: 12px;
    box-shadow: 2px 3px 10px rgba(0, 0, 0, 0.08);
    text-align: left;
    border-left: 4px solid #d3a484;
    position: relative;
    transition: transform 0.2s ease-in-out, box-shadow 0.2s;
    display: flex;
    flex-direction: column;
    width: 100%;

    
  }
  
  .comment-box:hover {
    transform: translateY(-3px);
    box-shadow: 4px 5px 15px rgba(0, 0, 0, 0.12);
  }
  
  .comment-box p {
    font-size: 1rem;
    margin: 0;
  }
  
  .comment-box span {
    font-size: 0.85rem;
    color: #e08c8c;
    display: block;
    margin-top: 6px;
  }
  
  /* Reactions */
  .reactions {
  display: flex;
  align-items: center;
  gap: 13px; /* Small gap */
  margin-top: 8px;
  justify-content: flex-start;
  flex-wrap: nowrap; /* Prevents wrapping */
  width: max-content; /* Ensures only necessary width */
  white-space: nowrap; /* Prevents line breaks */
}

  
  .reactions button {
  background: none;
  border: none;
  cursor: pointer;
  box-shadow: none;
  text-shadow: none;
  flex: 0 1 auto; /* Prevent shrinking */
  padding: 1px 3px;
  border-radius: 6px;
  display: inline-flex;
  align-items: center;
  font-size: 14px;
  
  }
  
  .reactions button:hover {
    background: #ffdfdf;
    color: #d9534f;
    transform: scale(1);
  }
</style>
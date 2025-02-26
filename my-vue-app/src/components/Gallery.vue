<template>
    <nav class="navbar">
      <div class="logo">
        <img 
          src="https://scontent.fmnl33-1.fna.fbcdn.net/v/t1.15752-9/474667107_1150394953328908_453092773794161443_n.png?_nc_cat=100&ccb=1-7&_nc_sid=9f807c&_nc_eui2=AeFtTV2Y3K0jKg0_2qV1Ho2xsF94E5Xqu6ewX3gTleq7pyQODnFyHMmvOYxLBKQlWA6rilKeyHQG2zaatLODHo2A&_nc_ohc=rpQ5djOAujEQ7kNvgHIFAZB&_nc_zt=23&_nc_ht=scontent.fmnl33-1.fna&oh=03_Q7cD1gF1ICi8zBFjshzJ24XNdz3oZT7SBQdxXjfFdQZv9Wfp3w&oe=67BFD3DF"
          alt="Rain's Cafe Logo">
      </div>   
    
      <div class="nav-links">
          <a href="/navbarbanner"><b>Home</b></a>
          <a href="/resume"><b>More</b></a>
          <a href="#banner"><b>Gallery</b></a>
          <a href="/contact"><b>Contact</b></a>
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

  <footer class="footer">
  <div class="footer-content">
    <p> 2025 Rain's Café. All rights reserved.</p>
    <div class="social-icons">
      <a href="#"><i class="fab fa-facebook"></i></a>
      <a href="#"><i class="fab fa-instagram"></i></a>
      <a href="#"><i class="fab fa-twitter"></i></a>
    </div>
  </div>
</footer>

</template>

<script>
import { ref, onMounted } from 'vue';
import supabase from '../lib/supabaseClient';
export default {
  setup() {
    // Comment Section
    const comments = ref([]);
    const newComment = ref({ name: '', comment: '' });

    const fetchComments = async () => {
      let { data, error } = await supabase
        .from('comments')
        .select('*')
        .order('created_at', { ascending: false });

      if (!error) {
        comments.value = data.map(comment => ({
          ...comment,
          reactions: loadReactions(comment.id),
        }));
      }
    };

    const addComment = async () => {
      if (!newComment.value.name || !newComment.value.comment) return;

      let { data, error } = await supabase
        .from('comments')
        .insert([
          {
            name: newComment.value.name,
            comment: newComment.value.comment,
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
        newComment.value = { name: '', comment: '' };
      }
    };

    const loadReactions = (commentId) => {
      return {
        laughs: parseInt(localStorage.getItem(`reaction_${commentId}_laughs`)) || 0,
        loves: parseInt(localStorage.getItem(`reaction_${commentId}_loves`)) || 0,
        dislikes: parseInt(localStorage.getItem(`reaction_${commentId}_dislikes`)) || 0,
      };
    };

    const toggleReaction = (commentId, reactionType) => {
      const key = `reaction_${commentId}_${reactionType}`;
      const hasReacted = localStorage.getItem(key);

      comments.value = comments.value.map(comment => {
        if (comment.id === commentId) {
          if (hasReacted) {
            comment.reactions[reactionType] = Math.max(0, comment.reactions[reactionType] - 1);
            localStorage.removeItem(key);
          } else {
            comment.reactions[reactionType] += 1;
            localStorage.setItem(key, 'true');
          }
        }
        return comment;
      });
    };

    const formatTimestamp = (timestamp) => {
      return timestamp ? new Date(timestamp).toLocaleString() : "Unknown time";
    };

    onMounted(() => {
      fetchComments();

      supabase
        .channel('comments')
        .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'comments' }, (payload) => {
          let newComment = { ...payload.new, reactions: { laughs: 0, loves: 0, dislikes: 0 } };
          comments.value.unshift(newComment);
        })
        .subscribe();
    });

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
        ? Math.floor(images.value.length / itemsPerSlide) - 1
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
<template>
  <div id="app">
    <div id="app-comments" class="comments-section">
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
import { createClient } from '@supabase/supabase-js';
import { onMounted, ref } from 'vue';

const supabaseUrl = 'https://kbhnxlrhbxamkgwyqpjn.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtiaG54bHJoYnhhbWtnd3lxcGpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg0Njc3NzEsImV4cCI6MjA1NDA0Mzc3MX0.lCXlrIXQaw3BvkzR9SBLGuxXnDAIscdkzcUpnn0KR-8'
const supabase = createClient(supabaseUrl, supabaseKey);

export default {
  setup() {
    const comments = ref([]);
    const newComment = ref({ name: '', comment: '' });

    // Fetch comments
    const fetchComments = async () => {
      let { data, error } = await supabase
        .from('comments')
        .select('*')
        .order('created_at', { ascending: false });

      if (!error) {
        comments.value = data.map(comment => ({
          ...comment,
          reactions: loadReactions(comment.id)
        }));
      }
    };

    // Add a new comment
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

    // Load reactions from localStorage
    const loadReactions = (commentId) => {
      return {
        laughs: parseInt(localStorage.getItem(`reaction_${commentId}_laughs`)) || 0,
        loves: parseInt(localStorage.getItem(`reaction_${commentId}_loves`)) || 0,
        dislikes: parseInt(localStorage.getItem(`reaction_${commentId}_dislikes`)) || 0
      };
    };

    // Toggle reactions (No Supabase)
    const toggleReaction = (commentId, reactionType) => {
      const key = `reaction_${commentId}_${reactionType}`;
      const hasReacted = localStorage.getItem(key);

      comments.value = comments.value.map(comment => {
        if (comment.id === commentId) {
          if (hasReacted) {
            // Undo reaction
            comment.reactions[reactionType] = Math.max(0, comment.reactions[reactionType] - 1);
            localStorage.removeItem(key);
          } else {
            // Add reaction
            comment.reactions[reactionType] += 1;
            localStorage.setItem(key, 'true');
          }
        }
        return comment;
      });
    };

    // Format timestamp
    const formatTimestamp = (timestamp) => {
      if (!timestamp) return "Unknown time";
      return new Date(timestamp).toLocaleString();
    };

    // Fetch comments when component loads
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

    return { comments, newComment, toggleReaction, addComment, formatTimestamp };
  }
};
</script>


<style scoped>
/* General Styles */
body {
  background-color: #f7e6d6;
  color: #4a3f35;
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
}

/* Comments Section */
.comments-section {
  max-width: 1500px;
  background: #fff4e6;
  margin: 2rem auto;
  padding: 1.5rem;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
  text-align: center;
  transition: transform 0.2s ease-in-out;
}

/* Title Styling */
.comments-section h2 {
  font-size: 24px;
  color: #b36a6a;
  margin-bottom: 1rem;
  font-weight: bold;
}

/* Comment Form */
.comment-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: #fae2cf;
  padding: 1.2rem;
  border-radius: 12px;
  border: 2px solid #e0a899;
}

.comment-form input,
.comment-form textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #c98b72;
  border-radius: 8px;
  font-size: 1rem;
  background: #fffaf5;
  color: #4a3f35;
}

.comment-form textarea {
  resize: none;
  min-height: 100px;
}

.comment-form button {
  padding: 12px;
  background: #c47474;
  color: white;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s;
  font-weight: bold;
}

.comment-form button:hover {
  background: #ea9c9c;
  transform: scale(1.01);
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
  gap: 8px;
  margin-top: 8px;
}

.reactions button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 8px;
  border-radius: 8px;
}

.reactions button:hover {
  background: #ffdfdf;
  color: #d9534f;
  transform: scale(1.1);
}
</style>

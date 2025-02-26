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

</style>

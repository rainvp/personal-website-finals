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
import { ref, onMounted } from 'vue';
import supabase from '../lib/supabaseClient';

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

    const toggleReaction = async (commentId, reactionType) => {
  const user = supabase.auth.user();
  if (!user) {
    console.error("User is not authenticated");
    return;
  }

  try {
    const response = await fetch("http://localhost:5000/toggle_reaction", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        comment_id: commentId, 
        reaction_type: reactionType, 
        user_email: user.email 
      }),
    });

    const result = await response.json();
    console.log(result.message);

    // Fetch updated reactions
    fetchReactions(commentId);  // ✅ Removed `await` to avoid setup() error
  } catch (error) {
    console.error("Error toggling reaction:", error);
  }
};

// Fetch reactions
const fetchReactions = async (commentId) => {
  const updatedReactions = await getReactionsFromBackend(commentId);
  comments.value = comments.value.map(comment =>
    comment.id === commentId ? { ...comment, reactions: updatedReactions } : comment
  );
};

// Function to fetch reactions from backend
const getReactionsFromBackend = async (commentId) => {
  try {
    const response = await fetch(`http://localhost:5000/get_reactions?comment_id=${commentId}`);
    const data = await response.json();
    return data.reactions || { laughs: 0, loves: 0, dislikes: 0 };
  } catch (error) {
    console.error("Error fetching reactions:", error);
    return { laughs: 0, loves: 0, dislikes: 0 };
  }
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

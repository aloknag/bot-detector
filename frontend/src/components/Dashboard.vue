<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">
      Bot Detection Dashboard
    </h1>

    <!-- Current Session -->
    <section class="mb-10">
      <h2 class="text-xl font-semibold mb-2 text-gray-700">Current Detection</h2>
      <BotDetector />
    </section>

    <!-- Session History -->
    <section>
      <h2 class="text-xl font-semibold mb-4 text-gray-700">Previous Sessions</h2>
      <div v-if="loading" class="text-gray-500">Loading sessions...</div>
      <div v-else-if="sessions.length === 0" class="text-gray-500">No sessions recorded yet.</div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div
          v-for="session in sessions"
          :key="session.id"
          class="bg-white shadow rounded-lg p-4 border cursor-pointer hover:bg-gray-50"
          @click="goToSession(session.id)"
        >
          <router-link
            :to="{ name: 'session-detail', params: { id: session.id } }"
            class="block text-blue-600 hover:underline mb-1"
            @click.stop
          >
            View Session #{{ session.id.slice(0, 8) }}
          </router-link>
          <p class="text-sm text-gray-600">Time: {{ formatTime(session.timestamp) }}</p>
          <p class="text-sm text-gray-600 truncate" title="Environment">{{ session.environment || 'No Data' }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import BotDetector from "./BotDetector.vue";

export default {
  name: "Dashboard",
  components: {
    BotDetector
  },
  data() {
    return {
      sessions: [],
      loading: true,
      sessionId: null,
    };
  },
  mounted() {
    this.initSession();
  },

  methods: {
    async initSession() {
      // Request a new session_id from backend
      try {
        console.log("Fetching session ID from backend...");
        const res = await fetch('/api/session');
        const data = await res.json();
        this.sessionId = data.session_id;
        localStorage.setItem('session_id', this.sessionId);
        console.log("Session ID set:", this.sessionId);
      } catch (e) {
        console.error("Failed to fetch session ID:", e);
        this.sessionId = null;
      }
      this.fetchSessions();
    },
    async fetchSessions() {
      try {
        const response = await fetch("/api/sessions");
        const data = await response.json();
        this.sessions = data.reverse(); // latest first
      } catch (err) {
        console.error("Failed to load sessions:", err);
      } finally {
        this.loading = false;
      }
    },
    formatTime(ts) {
      return new Date(ts).toLocaleString();
    },
    scoreColor(score) {
      if (score < 30) return "text-green-600";
      if (score < 60) return "text-yellow-600";
      return "text-red-600";
    }
  }
};
</script>

<style scoped>
</style>

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
          class="bg-white shadow rounded-lg p-4 border"
        >
          <p class="text-sm text-gray-600">Time: {{ formatTime(session.timestamp) }}</p>
          <p class="text-sm text-gray-600">Env: {{ session.environment }}</p>
          <p class="text-sm font-semibold" :class="scoreColor(session.score)">
            Score: {{ session.score }}/100
          </p>
          <ul class="mt-2 list-disc list-inside text-sm text-gray-700">
            <li v-for="(issue, i) in session.issues" :key="i">{{ issue }}</li>
          </ul>
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
      loading: true
    };
  },
  mounted() {
    this.fetchSessions();
  },
  methods: {
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

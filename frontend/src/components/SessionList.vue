<template>
  <div>
    <div v-if="loading" class="text-gray-500">Loading sessions...</div>
    <div v-else-if="sessions.length === 0" class="text-gray-500">No sessions recorded yet.</div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div
        v-for="session in sessions"
        :key="session.id"
        class="bg-white shadow rounded-lg p-4 border"
      >
        <p class="text-sm text-gray-600">Time: {{ formatTime(session.timestamp) }}</p>
        <p class="text-sm text-gray-600 truncate" title="Environment">{{ session.environment }}</p>
        <p
          class="text-sm font-semibold"
          :class="scoreColor(session.score)"
        >
          Score: {{ session.score }}/100
        </p>
        <ul class="mt-2 list-disc list-inside text-sm text-gray-700 max-h-32 overflow-auto">
          <li v-for="(issue, i) in session.issues" :key="i">{{ issue }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SessionList",
  data() {
    return {
      sessions: [],
      loading: true,
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
        this.sessions = data.reverse(); // show latest first
      } catch (error) {
        console.error("Error fetching sessions:", error);
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
    },
  },
};
</script>

<style scoped>
/* Optional: add scrollbar styling */
</style>

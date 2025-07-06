<template>
  <div>
    <div class="flex items-center mb-2">
      <button
        @click="clearSessions"
        class="ml-auto px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-sm"
      >
        Clear All Sessions
      </button>
    </div>
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
        // Only id and timestamp are available now
        this.sessions = data;
      } catch (error) {
        console.error("Error fetching sessions:", error);
      } finally {
        this.loading = false;
      }
    },
    async clearSessions() {
      if (!confirm('Are you sure you want to clear all sessions?')) return;
      try {
        await fetch('/api/sessions', { method: 'DELETE' });
        this.sessions = [];
      } catch (e) {
        alert('Failed to clear sessions');
      }
    },
    formatTime(ts) {
      if (!ts) return 'No Data';
      return new Date(ts).toLocaleString();
    },
    goToSession(id) {
      this.$router.push({ name: 'session-detail', params: { id } });
    },
  },
};
</script>

<style scoped>
/* Optional: add scrollbar styling */
</style>

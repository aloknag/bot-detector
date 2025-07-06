<template>
  <div v-if="loading" class="text-gray-500">Loading session...</div>
  <div v-else-if="!session" class="text-gray-500">Session not found.</div>
  <div v-else class="max-w-xl mx-auto bg-white shadow rounded-lg p-6 border">
    <h2 class="text-lg font-bold mb-2">Session #{{ sessionId.slice(0, 8) }}</h2>
    <p class="text-sm text-gray-600 mb-1">Time: {{ formatTime(session.timestamp) }}</p>
    <div v-if="!session.environment && (!session.issues || session.issues.length === 0)">
      <div class="text-gray-500">No Data</div>
    </div>
    <div v-else>
      <p class="text-sm text-gray-600 mb-1">Environment: {{ session.environment }}</p>
      <h4 class="font-semibold mt-4 mb-1">Issues</h4>
      <ul v-if="session.issues && session.issues.length" class="list-disc list-inside text-sm text-gray-700 mb-2">
        <li v-for="(issue, i) in session.issues" :key="i">{{ issue }}</li>
      </ul>
      <div v-else class="text-green-600 text-sm mb-2">No issues detected.</div>
      <h4 class="font-semibold mt-4 mb-1">Details</h4>
      <pre class="bg-gray-100 rounded p-2 text-xs overflow-x-auto">{{ JSON.stringify(session.details, null, 2) }}</pre>
    </div>
    <router-link to="/" class="inline-block mt-4 text-blue-600 hover:underline">← Back to sessions</router-link>
  </div>
</template>

<script>
export default {
  name: "SessionDetail",
  data() {
    return {
      session: null,
      loading: true,
    };
  },
  computed: {
    sessionId() {
      return this.$route.params.id;
    },
  },
  mounted() {
    this.fetchSession();
  },
  methods: {
    async fetchSession() {
      this.loading = true;
      try {
        const response = await fetch(`/api/sessions/${this.sessionId}`);
        if (!response.ok) throw new Error("Not found");
        this.session = await response.json();
      } catch (error) {
        this.session = null;
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
pre {
  max-height: 300px;
}
</style>

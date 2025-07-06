<template>
  <div class="container mx-auto p-4">
    <!-- Navigation -->
    <nav class="mb-6">
      <div class="flex space-x-4">
        <router-link to="/" class="btn btn-outline-primary">🏠 Home (Our Tests)</router-link>
        <router-link to="/creepjs" class="btn btn-outline-primary">CreepJS Fingerprint</router-link>
      </div>
    </nav>

    <!-- Our Bot Tests -->
    <BotDetector />
    <section>
      <h2 class="text-xl font-semibold mb-4 text-gray-700">Previous Sessions</h2>
      <SessionList />
    </section>
  </div>
</template>

<script>
import BotDetector from '@/components/BotDetector.vue'
import SessionList from '@/components/SessionList.vue'

export default {
  name: 'DashboardView',
  components: { BotDetector, SessionList }
}
</script>


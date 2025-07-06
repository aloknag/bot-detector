<template>
  <div class="card shadow-sm mb-3">
    <div class="card-body">
      <h5 class="card-title mb-3">🧠 CreepJS Fingerprint</h5>

      <div v-if="loading" class="text-muted">Running fingerprint test...</div>

      <div v-else>
        <table class="table table-sm">
          <thead>
            <tr class="table-light">
              <th>Key</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(value, key) in results" :key="key">
              <td>{{ key }}</td>
              <td>
                <span v-if="typeof value === 'object'">{{ JSON.stringify(value) }}</span>
                <span v-else>{{ value }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { fingerprint } from 'creepjs'

export default {
  name: 'CreepJSTest',
  data() {
    return {
      loading: true,
      results: {},
    }
  },
  mounted() {
    this.runFingerprint()
  },
  methods: {
    async runFingerprint() {
      try {
        const result = await fingerprint()
        this.results = result
        this.loading = false

        // Optional: emit score or issues
        this.$emit('result', {
          source: 'CreepJSTest',
          issues: [], // You can evaluate `result` to add issues if needed
          scoreImpact: 0,
        })
      } catch (error) {
        this.results = { error: error.message }
        this.loading = false
      }
    },
  },
}
</script>

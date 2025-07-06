<template>
  <div class="card shadow-sm p-3">
    <h5 class="mb-3">Incoming Request Headers</h5>
    <table class="table table-sm table-borderless mb-0" style="font-size: 0.9rem;">
      <thead>
        <tr>
          <th class="py-1 px-2">Header</th>
          <th class="py-1 px-2">Value</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(value, key) in headers" :key="key">
          <td class="py-1 px-2">{{ key }}</td>
          <td class="py-1 px-2">{{ value }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "HeadersTest",
  data() {
    return {
      headers: {},
    };
  },
  mounted() {
    fetch("/api/headers")
      .then((res) => res.json())
      .then((data) => {
        this.headers = data;
      })
      .catch((err) => {
        console.error("Failed to fetch headers:", err);
      });
  },
};
</script>

<style scoped>
table {
  word-break: break-all;
}
</style>

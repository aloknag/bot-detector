<template>
  <router-view />
</template>


<script>
import DashboardView from "@/views/DashboardView.vue";

export default {
  name: "App",
  components: {
    DashboardView,
  },
};
</script>

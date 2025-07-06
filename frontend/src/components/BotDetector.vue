<template>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <HeadersTest />
    <UserActivityTest />
    <HeadlessBrowserTest />
    <FingerprintTest />
    <RenderingTests />
    <AudioPerformanceTest />
    <EnvironmentTest />
    <!-- add more tests as cards -->
  </div>
</template>

<script>
import UserActivityTest from './UserActivityTest.vue'
import HeadlessBrowserTest from './HeadlessBrowserTest.vue'
import FingerprintTest from './FingerprintTest.vue'
import RenderingTests from './RenderingTest.vue'
import AudioPerformanceTest from './AudioPerformanceTest.vue'
import EnvironmentTest from './EnvironmentTest.vue'
import HeadersTest from './HeadersTest.vue'

export default {
  components: {
    UserActivityTest,
    HeadlessBrowserTest,
    FingerprintTest,
    RenderingTests,
    AudioPerformanceTest,
    EnvironmentTest,
    HeadersTest,
  }
}
</script>

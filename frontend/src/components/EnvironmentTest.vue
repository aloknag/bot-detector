<template>
  <div class="card shadow-sm mb-3">
    <div class="card-body">
      <h3 class="card-title mb-3">Environment Test</h3>
      <h6 class="mb-2">Tests Performed</h6>
      <ul class="list-group mb-3">
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <span><strong>Platform/User-Agent (Windows):</strong> Platform and UA match</span>
          <span :class="['badge', results.platformWindows ? 'bg-danger' : 'bg-success']">
            {{ results.platformWindows ? 'Mismatch' : 'OK' }}
          </span>
        </li>
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <span><strong>Platform/User-Agent (Mac):</strong> Platform and UA match</span>
          <span :class="['badge', results.platformMac ? 'bg-danger' : 'bg-success']">
            {{ results.platformMac ? 'Mismatch' : 'OK' }}
          </span>
        </li>
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <span><strong>Screen Color Depth:</strong> At least 24</span>
          <span :class="['badge', results.colorDepth ? 'bg-danger' : 'bg-success']">
            {{ results.colorDepth ? 'Low' : 'OK' }}
          </span>
        </li>
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <span><strong>Screen Resolution:</strong> At least 800x600</span>
          <span :class="['badge', results.screenResolution ? 'bg-danger' : 'bg-success']">
            {{ results.screenResolution ? 'Small' : 'OK' }}
          </span>
        </li>
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <span><strong>Suspicious User-Agent:</strong> Headless/Automation detected</span>
          <span :class="['badge', results.suspiciousUA ? 'bg-danger' : 'bg-success']">
            {{ results.suspiciousUA ? 'Yes' : 'No' }}
          </span>
        </li>
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <span><strong>Touch on Desktop UA:</strong> Touch events on desktop</span>
          <span :class="['badge', results.touchOnDesktop ? 'bg-danger' : 'bg-success']">
            {{ results.touchOnDesktop ? 'Yes' : 'No' }}
          </span>
        </li>
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <span><strong>eval() Enabled:</strong> eval() is not disabled</span>
          <span :class="['badge', results.evalDisabled ? 'bg-danger' : 'bg-success']">
            {{ results.evalDisabled ? 'Disabled' : 'Enabled' }}
          </span>
        </li>
      </ul>
      <h6 class="mb-2">Detected Issues</h6>
      <ul class="list-group mb-3" v-if="issues.length">
        <li class="list-group-item text-danger" v-for="(issue, i) in issues" :key="i">{{ issue }}</li>
      </ul>
      <div v-else class="alert alert-success p-2 mb-3">
        No environment anomalies detected.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "EnvironmentTest",
  emits: ["complete"],
  data() {
    return {
      results: {
        platformWindows: false,
        platformMac: false,
        colorDepth: false,
        screenResolution: false,
        suspiciousUA: false,
        touchOnDesktop: false,
        evalDisabled: false
      },
      issues: []
    };
  },
  mounted() {
    const issues = [];
    const ua = navigator.userAgent;
    const platform = navigator.platform;

    // 1. Platform and User-Agent mismatch
    this.results.platformWindows = /Win/.test(platform) && !/Windows/.test(ua);
    if (this.results.platformWindows) issues.push("Platform/UA mismatch (Windows)");

    this.results.platformMac = /Mac/.test(platform) && !/Macintosh/.test(ua);
    if (this.results.platformMac) issues.push("Platform/UA mismatch (Mac)");

    // 2. Inconsistent screen properties
    this.results.colorDepth = screen.colorDepth < 24;
    if (this.results.colorDepth) issues.push("Low screen color depth");

    this.results.screenResolution = screen.width < 800 || screen.height < 600;
    if (this.results.screenResolution) issues.push("Unusually small screen resolution");

    // 3. User-Agent anomalies
    const suspiciousUA = [
      "HeadlessChrome",
      "PhantomJS",
      "Selenium",
      "Puppeteer",
      "Node.js"
    ];
    this.results.suspiciousUA = suspiciousUA.some(keyword => ua.includes(keyword));
    if (this.results.suspiciousUA) issues.push("Suspicious User-Agent string");

    // 4. Check if touch is enabled on desktop UA
    const hasTouch = "ontouchstart" in window;
    this.results.touchOnDesktop = hasTouch && /Windows NT|Macintosh|X11/.test(ua);
    if (this.results.touchOnDesktop) issues.push("Touch support on desktop UA");

    // 5. Check eval behavior (some anti-bot setups disable it)
    try {
      eval("1+1");
      this.results.evalDisabled = false;
    } catch (e) {
      this.results.evalDisabled = true;
      issues.push("eval() is disabled");
    }

    this.issues = issues;
    const score = issues.length * 10;
    this.$emit("complete", {
      component: "EnvironmentTest",
      score,
      issues
    });
  }
};
</script>

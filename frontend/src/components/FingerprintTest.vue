<template>
  <div class="card shadow-sm mb-3">
    <div class="card-body">
      <h3 class="card-title mb-3">Fingerprint Test</h3>

      <h6 class="mb-2">Tests Performed</h6>
      <ul class="list-group mb-3">
        <li class="list-group-item d-flex justify-content-between align-items-center" v-for="(test, i) in testResults" :key="i">
          <span>
            <strong>{{ test.name }}:</strong> {{ test.description }}
          </span>
          <span :class="['badge', test.passed ? 'bg-success' : 'bg-danger']">
            {{ test.passed ? 'Pass' : 'Fail' }}
          </span>
        </li>
      </ul>

      <h6 class="mb-2">Detected Issues</h6>
      <ul class="list-group mb-3" v-if="issues.length">
        <li class="list-group-item text-danger" v-for="(issue, i) in issues" :key="i">{{ issue }}</li>
      </ul>
      <div v-else class="alert alert-success p-2 mb-3">
        No fingerprint anomalies detected.
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: "FingerprintTest",
  data() {
    return {
      issues: [],
      screenSize: "",
      timezoneOffset: 0,
      systemTimeZone: "",
      language: "",
      uaOS: "",
      platform: "",
      testResults: [],
    };
  },
  mounted() {
    const issues = [];
    let scoreImpact = 0;
    const testResults = [];

    try {
      this.screenSize = `${window.screen.width}x${window.screen.height}`;
      this.timezoneOffset = new Date().getTimezoneOffset();
      this.language = navigator.language || "unknown";
      this.platform = navigator.platform || "";
      this.systemTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone || "";

      // Extract OS from userAgent string
      const ua = navigator.userAgent || "";
      this.uaOS = this.extractOSFromUA(ua);

      // OS mismatch test
      const actualPlatform = navigator.userAgentData?.platform || this.platform;
      const osMatch = this.uaOS && actualPlatform && this.uaOS.toLowerCase().includes(actualPlatform.toLowerCase());
      testResults.push({
        name: "OS Consistency",
        description: `UA OS (${this.uaOS}) vs Platform (${actualPlatform})`,
        passed: !!osMatch,
      });
      if (!osMatch) {
        issues.push(`Mismatch between UA OS (${this.uaOS}) and platform (${actualPlatform})`);
        scoreImpact += 10;
      }

      // Timezone offset vs system timezone offset
      const systemDate = new Date().toLocaleString("en-US", { timeZone: this.systemTimeZone });
      const systemOffset = new Date(systemDate).getTimezoneOffset();
      const tzMatch = this.timezoneOffset === systemOffset;
      testResults.push({
        name: "Timezone Consistency",
        description: `Browser TZ offset (${this.timezoneOffset}) vs System TZ offset (${systemOffset})`,
        passed: tzMatch,
      });
      if (!tzMatch) {
        issues.push(`Mismatch between browser TZ offset (${this.timezoneOffset}) and system TZ (${this.systemTimeZone})`);
        scoreImpact += 10;
      } else if (this.timezoneOffset === 0) {
        issues.push("Timezone is UTC (bots often use UTC)");
        scoreImpact += 5;
      }

      // Language check
      const langValid = !!navigator.language && navigator.language.length >= 2;
      testResults.push({
        name: "Language Presence",
        description: `Browser language: ${navigator.language || "unknown"}`,
        passed: langValid,
      });
      if (!langValid) {
        issues.push("Suspicious or missing browser language");
        scoreImpact += 5;
      }

      // Platform empty check
      const platformPresent = !!this.platform;
      testResults.push({
        name: "Platform Presence",
        description: `Platform: ${this.platform || "empty"}`,
        passed: platformPresent,
      });
      if (!platformPresent) {
        issues.push("Platform is empty");
        scoreImpact += 5;
      }

      // Hardware concurrency check
      const hwConcurrency = navigator.hardwareConcurrency || 0;
      const hwConcurrencyOk = hwConcurrency >= 2;
      testResults.push({
        name: "Hardware Concurrency",
        description: `Cores: ${hwConcurrency}`,
        passed: hwConcurrencyOk,
      });
      if (navigator.hardwareConcurrency && !hwConcurrencyOk) {
        issues.push("Low hardware concurrency (virtual or emulated environment)");
        scoreImpact += 5;
      }

      // Screen size check
      const screenOk = window.screen.width >= 800 && window.screen.height >= 600;
      testResults.push({
        name: "Screen Size",
        description: `Screen: ${this.screenSize}`,
        passed: screenOk,
      });
      if (!screenOk) {
        issues.push(`Unusually small screen size: ${this.screenSize}`);
        scoreImpact += 5;
      }

      this.issues = issues;
      this.testResults = testResults;
      this.$emit("result", {
        source: "FingerprintTest",
        issues,
        scoreImpact,
      });
    } catch (e) {
      this.issues = ["Fingerprinting error: " + e.message];
      this.testResults = [];
      this.$emit("result", {
        source: "FingerprintTest",
        issues: this.issues,
        scoreImpact: 10,
      });
    }
  },
  methods: {
    extractOSFromUA(ua) {
      if (!ua) return "";
      if (ua.indexOf("Windows NT 10.0") !== -1) return "Windows 10";
      if (ua.indexOf("Windows NT 6.3") !== -1) return "Windows 8.1";
      if (ua.indexOf("Windows NT 6.2") !== -1) return "Windows 8";
      if (ua.indexOf("Windows NT 6.1") !== -1) return "Windows 7";
      if (ua.indexOf("Macintosh") !== -1) return "Mac OS";
      if (ua.indexOf("Linux") !== -1) return "Linux";
      if (ua.indexOf("Android") !== -1) return "Android";
      if (ua.indexOf("like Mac OS X") !== -1) return "iOS";
      return "Unknown";
    },
  },
};
</script>

<template>
  <div class="card shadow-sm mb-3">
    <div class="card-body">
      <h5 class="card-title mb-3">Automated Browser Check</h5>

      <table class="table table-sm mb-3">
        <thead>
          <tr class="table-light">
            <th scope="col">Test</th>
            <th scope="col">Result</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(test, i) in testResults" :key="i">
            <td>{{ test.name }}</td>
            <td>
              <span :class="test.passed ? 'text-success' : 'text-danger'">
                {{ test.passed ? 'Passed' : 'Failed' }}
              </span>
              <span v-if="test.detail" class="text-muted ms-2">({{ test.detail }})</span>
            </td>
          </tr>
        </tbody>
      </table>

      <h6 class="mb-2">Detected Issues</h6>
      <ul class="list-group mb-3" v-if="issues.length">
        <li class="list-group-item text-danger" v-for="(issue, i) in issues" :key="i">{{ issue }}</li>
      </ul>
      <div v-else class="alert alert-success p-2 mb-3">
        No headless traits detected.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HeadlessBrowserTest",
  data() {
    return {
      issues: [],
      testResults: [
        { name: "navigator.webdriver", passed: true, detail: "" },
        { name: "Browser plugins present", passed: true, detail: "" },
        { name: "window.chrome defined", passed: true, detail: "" },
        { name: "Notifications permission", passed: true, detail: "" },
        { name: "DevTools open detection", passed: true, detail: "" },
      ],
      devToolsOpen: false,
    };
  },
  mounted() {
    this.runTests();
  },
  methods: {
    async runTests() {
      const issues = [];
      let scoreImpact = 0;
      const testResults = [...this.testResults];

      // navigator.webdriver check
      if (navigator.webdriver) {
        issues.push("navigator.webdriver is true (likely headless)");
        scoreImpact += 20;
        testResults[0].passed = false;
        testResults[0].detail = "navigator.webdriver = true";
      } else {
        testResults[0].detail = "navigator.webdriver = false";
      }

      // Browser plugins check
      if (navigator.plugins.length === 0) {
        issues.push("No browser plugins detected");
        scoreImpact += 10;
        testResults[1].passed = false;
        testResults[1].detail = "No plugins";
      } else {
        testResults[1].detail = `${navigator.plugins.length} plugins`;
      }

      // window.chrome check
      if (!window.chrome) {
        issues.push("window.chrome is undefined (suspicious in Chrome-based browsers)");
        scoreImpact += 10;
        testResults[2].passed = false;
        testResults[2].detail = "window.chrome is undefined";
      } else {
        testResults[2].detail = "window.chrome is defined";
      }

      // Notifications permission check
      if (navigator.permissions && navigator.permissions.query) {
        try {
          const res = await navigator.permissions.query({ name: "notifications" });
          if (res.state === "denied") {
            issues.push("Notifications permission denied (common in headless/automated)");
            scoreImpact += 5;
            testResults[3].passed = false;
            testResults[3].detail = "denied";
          } else {
            testResults[3].detail = res.state;
          }
        } catch {
          issues.push("Permissions API query failed");
          scoreImpact += 5;
          testResults[3].passed = false;
          testResults[3].detail = "query failed";
        }
      } else {
        testResults[3].passed = false;
        testResults[3].detail = "Not supported";
      }

      // DevTools detection check
      const devtools = this.isDevToolsOpen();
      if (devtools) {
        issues.push("DevTools detected as open");
        scoreImpact += 15;
        testResults[4].passed = false;
        testResults[4].detail = "DevTools open";
      } else {
        testResults[4].detail = "DevTools closed";
      }

      this.issues = issues;
      this.testResults = testResults;
      this.$emit("result", {
        source: "HeadlessBrowserTest",
        issues,
        scoreImpact,
      });
    },

    isDevToolsOpen() {
      // Simple heuristic: measure difference between window.outerWidth and innerWidth, and detect devtools panel on sides
      const threshold = 160; // pixels difference threshold
      const widthDiff = window.outerWidth - window.innerWidth;
      const heightDiff = window.outerHeight - window.innerHeight;

      // If differences are large, devtools likely open on any side
      return widthDiff > threshold || heightDiff > threshold;
    },
  },
};
</script>

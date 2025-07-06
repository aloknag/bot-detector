<template>
  <div class="card shadow-sm mb-3">
    <div class="card-body">
      <h5 class="card-title mb-3">Rendering Fingerprint Tests</h5>

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
        No suspicious rendering fingerprints detected.
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: "RenderingTests",
  data() {
    return {
      issues: [],
      testResults: [
        { name: "Canvas fingerprint consistency", passed: true, detail: "" },
        { name: "WebGL renderer info presence", passed: true, detail: "" },
        { name: "WebGL debug info consistency", passed: true, detail: "" },
      ],
    };
  },
  mounted() {
    this.runTests();
  },
  methods: {
    runTests() {
      const issues = [];
      let scoreImpact = 0;
      const testResults = [...this.testResults];

      // Canvas fingerprint test
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      if (ctx) {
        ctx.textBaseline = "top";
        ctx.font = "14px 'Arial'";
        ctx.fillStyle = "#f60";
        ctx.fillRect(125, 1, 62, 20);
        ctx.fillStyle = "#069";
        ctx.fillText("Cwm fjordbank glyphs vext quiz, 😃", 2, 15);

        const dataUrl = canvas.toDataURL();
        // Some known bad patterns or empty canvas check (simplified)
        if (!dataUrl || dataUrl.length < 1000) {
          issues.push("Canvas fingerprint appears suspicious or empty");
          scoreImpact += 10;
          testResults[0].passed = false;
          testResults[0].detail = "Suspicious canvas output";
        } else {
          testResults[0].detail = `Fingerprint length ${dataUrl.length}`;
        }
      } else {
        issues.push("Canvas not supported");
        scoreImpact += 10;
        testResults[0].passed = false;
        testResults[0].detail = "No canvas context";
      }

      // WebGL tests
      const gl = this.getWebGLContext();
      if (!gl) {
        issues.push("WebGL not supported");
        scoreImpact += 10;
        testResults[1].passed = false;
        testResults[1].detail = "No WebGL context";
        testResults[2].passed = false;
        testResults[2].detail = "No WebGL context";
      } else {
        // Renderer info
        const debugInfo = gl.getExtension("WEBGL_debug_renderer_info");
        if (debugInfo) {
          const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
          const vendor = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);
          if (renderer && vendor) {
            testResults[1].detail = `${vendor} / ${renderer}`;
            testResults[2].detail = `Debug info available`;
          } else {
            issues.push("WebGL debug info incomplete");
            scoreImpact += 5;
            testResults[1].passed = false;
            testResults[1].detail = "Incomplete debug info";
            testResults[2].passed = false;
            testResults[2].detail = "Incomplete debug info";
          }
        } else {
          issues.push("WebGL debug extension not available");
          scoreImpact += 5;
          testResults[1].passed = false;
          testResults[1].detail = "No debug extension";
          testResults[2].passed = false;
          testResults[2].detail = "No debug extension";
        }
      }

      this.issues = issues;
      this.testResults = testResults;
      this.$emit("result", {
        source: "RenderingFingerprintTests",
        issues,
        scoreImpact,
      });
    },

    getWebGLContext() {
      const canvas = document.createElement("canvas");
      let gl = null;
      try {
        gl =
          canvas.getContext("webgl") ||
          canvas.getContext("experimental-webgl");
      } catch {
        return null;
      }
      return gl;
    },
  },
};
</script>

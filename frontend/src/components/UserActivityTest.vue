<template>
  <div class="border p-4 rounded-lg shadow bg-white">
    <h3 class="font-semibold text-gray-800 mb-2">User Activity Test</h3>

    <div class="mt-2 text-xs text-gray-500">
      <table class="table table-bordered table-sm mb-0">
        <tbody>
          <tr>
            <th>Keystrokes</th>
            <td>{{ keystrokes }}</td>
          </tr>
          <tr>
            <th>Mouse Moves</th>
            <td>{{ mouseMoves }}</td>
          </tr>
          <tr>
            <th>Touches</th>
            <td>{{ touches }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- New table for test results -->
    <div class="mt-4 text-xs">
      <table class="table table-bordered table-sm w-full">
        <thead>
          <tr>
            <th>Test</th>
            <th>Result</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Keystroke count &ge; 2</td>
            <td>{{ keystrokes }}</td>
            <td>
              <span :class="keystrokes >= 2 ? 'text-green-600' : 'text-red-600'">
                {{ keystrokes >= 2 ? 'Passed' : 'Failed' }}
              </span>
            </td>
          </tr>
          <tr>
            <td>Mouse moves &ge; 5</td>
            <td>{{ mouseMoves }}</td>
            <td>
              <span :class="mouseMoves >= 5 ? 'text-green-600' : 'text-red-600'">
                {{ mouseMoves >= 5 ? 'Passed' : 'Failed' }}
              </span>
            </td>
          </tr>
          <tr v-if="hasTouch">
            <td>At least 1 touch event</td>
            <td>{{ touches }}</td>
            <td>
              <span :class="touches > 0 ? 'text-green-600' : 'text-red-600'">
                {{ touches > 0 ? 'Passed' : 'Failed' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <h6 class="mb-2">Detected Issues</h6>
    <ul class="list-group mb-3" v-if="issues.length">
      <li class="list-group-item text-danger" v-for="(issue, i) in issues" :key="i">{{ issue }}</li>
    </ul>
    <div v-else class="alert alert-success p-2 mb-3">
      Normal human interaction detected.
    </div>
  </div>

</template>

<script>
export default {
  name: "UserActivityTest",
  data() {
    return {
      keystrokes: 0,
      mouseMoves: 0,
      touches: 0,
      issues: [],
    };
  },
  mounted() {
    window.addEventListener("keydown", this.handleKey);
    window.addEventListener("mousemove", this.handleMouse);
    window.addEventListener("touchstart", this.handleTouch);
    setTimeout(this.evaluateUserActivity, 5000);
  },
  beforeDestroy() {
    window.removeEventListener("keydown", this.handleKey);
    window.removeEventListener("mousemove", this.handleMouse);
    window.removeEventListener("touchstart", this.handleTouch);
  },
  computed: {
    hasTouch() {
      return typeof window !== "undefined" && "ontouchstart" in window;
    }
  },
  methods: {
    handleKey() {
      this.keystrokes++;
    },
    handleMouse() {
      this.mouseMoves++;
    },
    handleTouch() {
      this.touches++;
    },
    evaluateUserActivity() {
      const issues = [];
      let scoreImpact = 0;

      if (this.keystrokes < 2) {
        issues.push("Low keystroke count");
        scoreImpact += 10;
      }

      if (this.touches === 0 && this.hasTouch) {
        issues.push("No touch events");
        scoreImpact += 5;
      }

      if (this.touches === 0 && "ontouchstart" in window) {
        issues.push("No touch events");
        scoreImpact += 5;
      }

      this.issues = issues;

      this.$emit("result", {
        source: "UserActivityTest",
        issues,
        scoreImpact,
      });
    },
  },
};
</script>

<template>
    <div class="card shadow-sm mb-3">
        <div class="card-body">
            <h5 class="card-title mb-3">Audio & Performance Tests</h5>

            <table class="table table-sm mb-3">
                <thead>
                    <tr class="table-light">
                        <th scope="col">Test</th>
                        <th scope="col">Confidence Level</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(test, i) in testResults" :key="i">
                        <td>{{ test.name }}</td>
                        <td>
                            <span :class="confidenceClass(test.confidence)">
                                {{ test.confidence }}
                            </span>
                            <span v-if="test.detail" class="text-muted ms-2">({{ test.detail }})</span>
                        </td>
                    </tr>
                </tbody>
            </table>

            <ul class="list-group list-group-flush mb-0" v-if="issues.length">
                <li v-for="(issue, i) in issues" :key="i" class="list-group-item px-0 py-1">
                    {{ issue }}
                </li>
            </ul>
            <p v-else class="text-success mb-0">
                No suspicious audio or performance anomalies detected.
            </p>
        </div>
    </div>
</template>

<script>
export default {
    name: "AudioPerformanceTest",
    data() {
        return {
            issues: [],
            testResults: [
                { name: "AudioContext entropy", confidence: "Safe", detail: "" },
                { name: "Event loop lag (ms)", confidence: "Safe", detail: "" },
            ],
        };
    },
    mounted() {
        const resumeAudioContext = () => {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            context.resume().then(() => {
                this.runTests();
            });
        };
        // this.runTests();
        window.addEventListener("click", resumeAudioContext, { once: true });
    },
    methods: {
        confidenceClass(level) {
            switch (level) {
                case "Safe":
                    return "text-success";
                case "Caution":
                    return "text-warning";
                case "Likely Bot":
                    return "text-danger";
                default:
                    return "";
            }
        },
        async runTests() {
            const issues = [];
            let scoreImpact = 0;
            const testResults = [...this.testResults];
            const entropyThresholdBot = 0.01;    // Likely Bot
            const entropyThresholdCaution = 0.05; // Caution
            const lagThresholdBot = 300;         // Likely Bot
            const lagThresholdCaution = 100;     // Caution

            // AudioContext fingerprint entropy
            try {
                const entropy = await this.getAudioContextEntropy();
                if (entropy < entropyThresholdBot) {
                    issues.push("AudioContext entropy is very low");
                    scoreImpact += 10;
                    testResults[0].confidence = "Likely Bot";
                    testResults[0].detail = `Low entropy: ${entropy.toFixed(4)}`;
                } else if (entropy < entropyThresholdCaution) {
                    issues.push("AudioContext entropy is lower than normal");
                    scoreImpact += 5;
                    testResults[0].confidence = "Caution";
                    testResults[0].detail = `Entropy: ${entropy.toFixed(4)}`;
                } else {
                    testResults[0].confidence = "Safe";
                    testResults[0].detail = `Entropy: ${entropy.toFixed(4)}`;
                }
            } catch (err) {
                issues.push("AudioContext test failed: " + err.message);
                scoreImpact += 10;
                testResults[0].confidence = "Likely Bot";
                testResults[0].detail = "Test error";
            }

            // Event loop lag measurement
            try {
                const lag = await this.measureEventLoopLag();
                if (lag > lagThresholdBot) {
                    issues.push(`High event loop lag detected (${lag.toFixed(1)} ms)`);
                    scoreImpact += 15;
                    testResults[1].confidence = "Likely Bot";
                    testResults[1].detail = `${lag.toFixed(1)} ms (High)`;
                } else if (lag > lagThresholdCaution) {
                    issues.push(`Moderate event loop lag detected (${lag.toFixed(1)} ms)`);
                    scoreImpact += 5;
                    testResults[1].confidence = "Caution";
                    testResults[1].detail = `${lag.toFixed(1)} ms (Moderate)`;
                } else {
                    testResults[1].confidence = "Safe";
                    testResults[1].detail = `${lag.toFixed(1)} ms (Normal)`;
                }
            } catch (err) {
                issues.push("Event loop lag test failed: " + err.message);
                scoreImpact += 10;
                testResults[1].confidence = "Likely Bot";
                testResults[1].detail = "Test error";
            }

            this.issues = issues;
            this.testResults = testResults;
            this.$emit("result", {
                source: "AudioAndPerformanceTest",
                issues,
                scoreImpact,
            });
        },

        getAudioContextEntropy() {
            return new Promise((resolve, reject) => {
                try {
                    const AudioContext = window.AudioContext || window.webkitAudioContext;
                    if (!AudioContext) return reject(new Error("AudioContext not supported"));

                    const context = new AudioContext();
                    const oscillator = context.createOscillator();
                    const analyser = context.createAnalyser();
                    const gainNode = context.createGain();

                    gainNode.gain.value = 0; // mute audio
                    oscillator.type = "triangle";
                    oscillator.connect(analyser);
                    analyser.connect(gainNode);
                    gainNode.connect(context.destination);

                    oscillator.start(0);

                    // Wait for audio context to process
                    setTimeout(() => {
                        const frequencyData = new Uint8Array(analyser.frequencyBinCount);
                        analyser.getByteFrequencyData(frequencyData);

                        // Simple entropy estimation by counting unique frequency values ratio
                        const uniqueValues = new Set(frequencyData).size;
                        const entropy = uniqueValues / frequencyData.length;

                        oscillator.stop();
                        context.close();

                        resolve(entropy);
                    }, 100);
                } catch (e) {
                    reject(e);
                }
            });
        },

        measureEventLoopLag() {
            return new Promise((resolve) => {
                const iterations = 10;
                const delays = [];
                function measure(iteration) {
                    if (iteration === 0) {
                        const avgDelay = delays.reduce((a, b) => a + b, 0) / delays.length;
                        resolve(avgDelay);
                        return;
                    }
                    const start = performance.now();
                    setTimeout(() => {
                        const end = performance.now();
                        delays.push(end - start);
                        measure(iteration - 1);
                    }, 0);
                }
                measure(iterations);
            });
        },
    },
};
</script>

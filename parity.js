// Node parity check: mirrors index.html calc() using model.json weights.
const fs = require("fs");
const m = JSON.parse(fs.readFileSync("model.json", "utf8"));
const samples = JSON.parse(fs.readFileSync("parity_samples.json", "utf8"));
let maxDiff = 0;
for (const s of samples) {
  let v = m.intercept;
  for (let j = 0; j < 5; j++) v += ((s.inputs[j] - m.means[j]) / m.stds[j]) * m.coef[j];
  const p = Math.min(100, Math.max(0, v));
  const diff = Math.abs(p - s.score);
  maxDiff = Math.max(maxDiff, diff);
  console.log(JSON.stringify(s.inputs), p.toFixed(2), "vs python", s.score.toFixed(2), "diff", diff.toFixed(6));
}
console.log("max diff:", maxDiff, maxDiff < 0.01 ? "PASS" : "FAIL");

// Computes real per-label statistics from a .jtl file: count, error rate,
// elapsed-time percentiles, throughput, and average response size. Used to
// ground both the first-pass analysis and the misinterpretation-hunt pass in
// actual numbers rather than estimates. Run: node compute_stats.js <file.jtl>
const fs = require("fs");

const file = process.argv[2];
const lines = fs.readFileSync(file, "utf8").trim().split("\n");
const header = lines[0].split(",");
const idx = (name) => header.indexOf(name);
const iTs = idx("timeStamp"),
  iElapsed = idx("elapsed"),
  iLabel = idx("label"),
  iCode = idx("responseCode"),
  iSuccess = idx("success"),
  iBytes = idx("bytes");

const rows = lines.slice(1).map((l) => {
  const c = l.split(",");
  return {
    ts: Number(c[iTs]),
    elapsed: Number(c[iElapsed]),
    label: c[iLabel],
    code: c[iCode],
    success: c[iSuccess] === "true",
    bytes: Number(c[iBytes]),
  };
});

function pct(arr, p) {
  const sorted = [...arr].sort((a, b) => a - b);
  const idx = Math.min(sorted.length - 1, Math.ceil((p / 100) * sorted.length) - 1);
  return sorted[Math.max(0, idx)];
}

function summarize(name, rs) {
  const elapsed = rs.map((r) => r.elapsed);
  const fails = rs.filter((r) => !r.success);
  const codeCounts = {};
  for (const r of rs) codeCounts[r.code] = (codeCounts[r.code] || 0) + 1;
  const tsMin = Math.min(...rs.map((r) => r.ts));
  const tsMax = Math.max(...rs.map((r) => r.ts));
  const durationSec = (tsMax - tsMin) / 1000 || 1;
  const avgBytes = rs.reduce((a, r) => a + r.bytes, 0) / rs.length;
  console.log(`\n--- ${name} (n=${rs.length}) ---`);
  console.log(`  codes: ${JSON.stringify(codeCounts)}`);
  console.log(`  success=false count: ${fails.length} (${((fails.length / rs.length) * 100).toFixed(2)}%)`);
  console.log(`  elapsed ms -> min:${Math.min(...elapsed)} avg:${(elapsed.reduce((a, b) => a + b, 0) / elapsed.length).toFixed(1)} median:${pct(elapsed, 50)} p90:${pct(elapsed, 90)} p95:${pct(elapsed, 95)} p99:${pct(elapsed, 99)} max:${Math.max(...elapsed)}`);
  console.log(`  throughput: ${(rs.length / durationSec).toFixed(2)} req/s over ${durationSec.toFixed(1)}s window`);
  console.log(`  avg response bytes: ${avgBytes.toFixed(0)}`);
}

console.log(`=== ${file} ===`);
summarize("OVERALL", rows);
const labels = [...new Set(rows.map((r) => r.label))];
for (const label of labels) {
  summarize(label, rows.filter((r) => r.label === label));
}

// Bytes-over-time trend for GET /api/admin/orders specifically (checking for
// unbounded response growth as more orders accumulate - no pagination).
const getOrders = rows.filter((r) => r.label === "GET /api/admin/orders");
if (getOrders.length > 5) {
  const first5 = getOrders.slice(0, 5).map((r) => r.bytes);
  const last5 = getOrders.slice(-5).map((r) => r.bytes);
  console.log(`\n  GET /api/admin/orders response bytes - first 5: ${first5.join(",")} | last 5: ${last5.join(",")}`);
}

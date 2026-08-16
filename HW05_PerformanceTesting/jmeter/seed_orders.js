// Seeds `orders` with a large pool of status='pending' rows so the admin
// order-management workflow (GET /api/admin/orders, PUT .../status) has real
// data to read and transition during Load/Stress/Spike/Soak runs, without
// paying HTTP/register/login/checkout cost for every seed row.
//
// Usage: node seed_orders.js [count]   (default 3000)
// Writes: data/order_ids.csv (order_id,status) sized to `count`, target
// status is always "confirmed" (the valid next step from "pending").
//
// Run this fresh before every OFFICIAL Load/Stress/Spike/Soak execution.

const path = require("path");
const fs = require("fs");

const sqlite3 = require(
  path.join(__dirname, "..", "..", "backend", "node_modules", "sqlite3"),
).verbose();

const count = parseInt(process.argv[2], 10) || 3000;
const dbPath = path.join(__dirname, "..", "..", "backend", "database.sqlite");
const csvPath = path.join(__dirname, "data", "order_ids.csv");

const db = new sqlite3.Database(dbPath);

const BUYER_USER_ID = 2; // "Test User" seeded by backend/database.js

db.serialize(() => {
  db.run("DELETE FROM orders");
  db.run("DELETE FROM sqlite_sequence WHERE name='orders'");

  const stmt = db.prepare(
    "INSERT INTO orders (user_id, total_amount, status, shipping_address) VALUES (?, ?, 'pending', ?)",
  );

  db.run("BEGIN TRANSACTION");
  for (let i = 0; i < count; i++) {
    const amount = 100000 + Math.floor(Math.random() * 49900000);
    stmt.run(BUYER_USER_ID, amount, "Seeded by HW05 perf test");
  }
  db.run("COMMIT", (err) => {
    if (err) {
      console.error("Seed failed:", err.message);
      process.exit(1);
    }
    stmt.finalize(() => {
      db.get("SELECT COUNT(*) as n FROM orders", [], (e, row) => {
        console.log(`Seeded ${row.n} pending orders (requested ${count}).`);

        const lines = ["order_id,status"];
        for (let id = 1; id <= row.n; id++) {
          lines.push(`${id},confirmed`);
        }
        fs.writeFileSync(csvPath, lines.join("\n") + "\n", "utf8");
        console.log(`Wrote ${csvPath} (${row.n} rows).`);
        db.close();
      });
    });
  });
});

// Resets the admin account's lockout state so Stress/Spike runs can be
// repeated without waiting out the real 180s lock. Run after any run that
// deliberately triggers lockout (Stress's lockout sub-test).
const path = require("path");
const sqlite3 = require(
  path.join(__dirname, "..", "..", "backend", "node_modules", "sqlite3"),
).verbose();
const dbPath = path.join(__dirname, "..", "..", "backend", "database.sqlite");
const db = new sqlite3.Database(dbPath);
db.run(
  "UPDATE users SET login_attempts = 0, locked_until = NULL WHERE email = 'admin@eshop.com'",
  function (err) {
    if (err) { console.error(err.message); process.exit(1); }
    console.log(`Lockout reset for admin@eshop.com (rows changed: ${this.changes}).`);
    db.close();
  },
);

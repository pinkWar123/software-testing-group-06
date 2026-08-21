import fs from 'node:fs';

const dir = new URL('./', import.meta.url);
const csv = fs.readFileSync(new URL('api1_login_test_cases.csv', dir), 'utf8');
const out = new URL('api1_login.postman_collection.json', dir);

function parseCsv(text) {
  const rows = [], row = [];
  let current = '', quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    if (ch === '"') { quoted = !quoted; continue; }
    if (!quoted && ch === ',') { row.push(current); current = ''; continue; }
    if (!quoted && (ch === '\n' || ch === '\r')) {
      if (ch === '\r' && text[i + 1] === '\n') i += 1;
      row.push(current); current = '';
      if (row.length) rows.push(row.splice(0));
      continue;
    }
    current += ch;
  }
  if (current || row.length) { row.push(current); rows.push(row); }
  const headers = rows.shift();
  return rows.map(values => Object.fromEntries(headers.map((h, i) => [h, values[i] ?? ''])));
}

const cases = parseCsv(csv);
const pre = [
  "const sid = pm.environment.get('studentId');",
  "pm.request.headers.upsert({key: 'X-Student-Id', value: sid});",
  "console.log('X-Student-Id:', sid, '|', pm.info.requestName);"
];

function expectedTests(id) {
  const lines = [
    "pm.test('Student-ID header is present', () => pm.expect(pm.request.headers.get('X-Student-Id')).to.eql(pm.environment.get('studentId')));",
    "pm.test('Response is not a server crash', () => pm.expect(pm.response.code).to.be.below(500));"
  ];
  const success = ['LOGIN-001','LOGIN-002','LOGIN-030','LOGIN-031','LOGIN-032','LOGIN-033','LOGIN-038','LOGIN-039','SLOGIN-001','SLOGIN-002','SLOGIN-003'];
  if (success.includes(id)) {
    lines.push("pm.test('Expected successful login', () => pm.expect(pm.response.code).to.eql(200));");
    lines.push("pm.test('Success response has JWT', () => pm.expect(pm.response.json().token).to.be.a('string').and.not.empty);");
    lines.push("pm.test('Success response has user object', () => pm.expect(pm.response.json()).to.have.property('user'));");
  } else if (id === 'LOGIN-028') {
    lines.push("pm.test('Locked account is rejected with 403', () => pm.expect(pm.response.code).to.eql(403));");
  } else if (id === 'SLOGIN-004') {
    lines.push("pm.test('Locked account is indistinguishable from unknown account', () => pm.expect(pm.response.code).to.eql(401));");
  } else if (['LOGIN-025','LOGIN-026','LOGIN-027'].includes(id)) {
    lines.push("pm.test('Failed login follows documented 401 oracle', () => pm.expect(pm.response.code).to.eql(401));");
  } else {
    lines.push("pm.test('Negative case returns 4xx', () => pm.expect(pm.response.code).to.be.within(400, 499));");
  }
  if (['LOGIN-039','SLOGIN-003'].includes(id)) {
    lines.push("const forbidden = ['password','reset_token','login_attempts','locked_until','shipping_address','phone'];");
    lines.push("pm.test('No sensitive user fields are disclosed', () => { const u = pm.response.json().user; forbidden.forEach(k => pm.expect(u, k + ' must not be disclosed').not.have.property(k)); });");
  }
  return lines;
}

function variable(name) { return `{{${name}}}`; }
function requestData(c) {
  const id = c.TestCaseID;
  let method = 'POST', type = 'application/json';
  let email = variable(id === 'LOGIN-002' || ['LOGIN-032','LOGIN-033','SLOGIN-003','SLOGIN-004'].includes(id) ? 'adminEmail' : 'caseUnknownEmail');
  let password = variable(id === 'LOGIN-002' || ['LOGIN-032','LOGIN-033','SLOGIN-003','SLOGIN-004'].includes(id) ? 'adminPassword' : 'wrongPassword');
  let body = { email, password };
  if (['LOGIN-001','LOGIN-030','LOGIN-031','LOGIN-038','SLOGIN-002'].includes(id)) body = { email: variable('successEmail'), password: variable('successPassword') };
  if (['LOGIN-025','LOGIN-026','LOGIN-027','LOGIN-029'].includes(id)) body = { email: variable('disposableEmail'), password: variable('wrongPassword') };
  if (id === 'LOGIN-006') body = {};
  if (['LOGIN-007','LOGIN-009'].includes(id)) body = { password: 'wrong' };
  if (['LOGIN-008','LOGIN-010'].includes(id)) body = { email: 'case@example.invalid' };
  if (id === 'LOGIN-011') body = { email: '', password: 'wrong' };
  if (id === 'LOGIN-012') body = { email: '   ', password: '   ' };
  if (id === 'LOGIN-013') body = { email: 'userdomain.com', password: 'wrong' };
  if (id === 'LOGIN-014') body = { email: 'user@@domain.com', password: 'wrong' };
  if (id === 'LOGIN-015') body = { email: 'x'.repeat(300), password: 'wrong' };
  if (['LOGIN-016','LOGIN-017','LOGIN-018'].includes(id)) body = { email: "' OR '1'='1<script>", password: 'wrong' };
  if (['LOGIN-019','LOGIN-020','LOGIN-021','LOGIN-022','LOGIN-023','LOGIN-024'].includes(id)) body = { email: 'case@example.invalid', password: 'x' };
  if (['LOGIN-028','SLOGIN-001','SLOGIN-004'].includes(id)) body = { email: variable('disposableEmail'), password: variable('disposablePassword') };
  if (id === 'LOGIN-034') { type = 'text/plain'; body = '{"email":"x","password":"y"}'; }
  if (id === 'LOGIN-035') body = '{"email":';
  if (id === 'LOGIN-036') body = { email: 'x'.repeat(100000), password: 'x'.repeat(100000) };
  if (id === 'LOGIN-037') method = 'GET';
  if (id === 'LOGIN-039' || id === 'SLOGIN-003') body = { email: variable('adminEmail'), password: variable('adminPassword') };
  if (id === 'SLOGIN-005') { method = 'PUT'; body = {}; }
  if (id === 'SLOGIN-006') body = [];
  return { method, type, body };
}

function caseItem(c) {
  const id = c.TestCaseID, d = requestData(c);
  const raw = typeof d.body === 'string' ? d.body : JSON.stringify(d.body, null, 2);
  return {
    name: id,
    request: { method: d.method, header: [{ key: 'Content-Type', value: d.type }], body: { mode: 'raw', raw }, url: { raw: '{{baseUrl}}/api/login', host: ['{{baseUrl}}'], path: ['api','login'] } },
    event: [{ listen: 'prerequest', script: { type: 'text/javascript', exec: pre } }, { listen: 'test', script: { type: 'text/javascript', exec: expectedTests(id) } }]
  };
}

const setup = {
  name: 'SETUP - create disposable execution user',
  request: { method: 'POST', header: [{ key: 'Content-Type', value: 'application/json' }], body: { mode: 'raw', raw: JSON.stringify({ name: 'Newman API1 User', email: variable('disposableEmail'), password: variable('disposablePassword') }) }, url: { raw: '{{baseUrl}}/api/register', host: ['{{baseUrl}}'], path: ['api','register'] } },
  event: [{ listen: 'prerequest', script: { type: 'text/javascript', exec: pre } }, { listen: 'test', script: { type: 'text/javascript', exec: ["pm.test('Setup returns a controlled result', () => pm.expect(pm.response.code).to.be.oneOf([200, 400]));"] } }]
};

const setupSuccess = {
  name: 'SETUP - create independent success user',
  request: { method: 'POST', header: [{ key: 'Content-Type', value: 'application/json' }], body: { mode: 'raw', raw: JSON.stringify({ name: 'Newman API1 Success User', email: variable('successEmail'), password: variable('successPassword') }) }, url: { raw: '{{baseUrl}}/api/register', host: ['{{baseUrl}}'], path: ['api','register'] } },
  event: [{ listen: 'prerequest', script: { type: 'text/javascript', exec: pre } }, { listen: 'test', script: { type: 'text/javascript', exec: ["pm.test('Independent user setup returns a controlled result', () => pm.expect(pm.response.code).to.be.oneOf([200, 400]));"] } }]
};

const collection = { info: { name: 'HW06 API 1 - Login Execution', schema: 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json' }, variable: [{ key: 'baseUrl', value: 'http://localhost:3000' }, { key: 'studentId', value: '22127345' }], item: [setup, setupSuccess, ...cases.map(caseItem)] };
fs.writeFileSync(out, JSON.stringify(collection, null, 2) + '\n');
console.log(`Generated ${cases.length} API cases plus setup: ${out.pathname}`);

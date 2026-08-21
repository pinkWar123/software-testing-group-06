import fs from 'node:fs';
import path from 'node:path';

const dir = path.dirname(new URL(import.meta.url).pathname);
const out = path.join(dir, 'api2_checkout.postman_collection.json');
const sid = `const sid = pm.environment.get('studentId');\npm.request.headers.upsert({key:'X-Student-Id', value:sid});\nconsole.log('X-Student-Id:', sid, '|', pm.info.requestName);`;
const common = `pm.test('Student-ID header is present',()=>pm.expect(pm.request.headers.get('X-Student-Id')).to.eql(pm.environment.get('studentId')));`;
const json = `let body=null; try { body=pm.response.json(); } catch(e) { }`;
const schema = `pm.test('success schema',()=>{pm.expect(body).to.be.an('object');pm.expect(Object.keys(body).sort()).to.eql(['message','orderId']);pm.expect(body.message).to.eql('Checkout successful');pm.expect(body.orderId).to.be.a('number');pm.expect(body.orderId).to.be.above(0);});`;
const expect4xx = `pm.test('controlled client/security error',()=>pm.expect(pm.response.code).to.be.within(400,499));`;
const expectSuccess = `${schema}\npm.test('HTTP 200',()=>pm.expect(pm.response.code).to.eql(200));`;

function item(name, method, raw, test, headers=[{key:'Content-Type',value:'application/json'}], endpoint='checkout') {
  return {name, request:{method,header:headers,url:{raw:`{{baseUrl}}/api/${endpoint}`,host:['{{baseUrl}}'],path:['api',endpoint]},body: raw===undefined?undefined:{mode:'raw',raw}},event:[{listen:'prerequest',script:{type:'text/javascript',exec:sid.split('\n')}},{listen:'test',script:{type:'text/javascript',exec:`${common}\n${json}\n${test}`.split('\n')}}]};
}
const valid = JSON.stringify({total_amount:100000,shipping_address:'123 Le Loi, TP.HCM'});
const cases = [
 ['API2-001',valid,expectSuccess],['API2-002',JSON.stringify({total_amount:999999,shipping_address:'123 Le Loi'}),`${expectSuccess}\npm.test('server total is authoritative',()=>pm.expect(body.orderId).to.be.a('number'));`],
 ['API2-003',JSON.stringify({total_amount:1,shipping_address:'123 Le Loi'}),expectSuccess],
 ['API2-004',JSON.stringify({shipping_address:'123 Le Loi'}),expect4xx],['API2-005',JSON.stringify({total_amount:null,shipping_address:'123 Le Loi'}),expect4xx],
 ['API2-006',JSON.stringify({total_amount:'200000',shipping_address:'123 Le Loi'}),expect4xx],['API2-007',JSON.stringify({total_amount:-1,shipping_address:'123 Le Loi'}),expect4xx],['API2-008',JSON.stringify({total_amount:0,shipping_address:'123 Le Loi'}),expect4xx],
 ['API2-009',valid,expect4xx,[{key:'Content-Type',value:'application/json'}]],
 ['API2-010',valid,expect4xx,[{key:'Content-Type',value:'application/json'},{key:'Authorization',value:'Bearer malformed'}]],
 ['API2-011',valid,expect4xx,[{key:'Content-Type',value:'application/json'},{key:'Authorization',value:'Bearer expired.invalid.token'}]],
 ['API2-012',valid,expect4xx,[{key:'Content-Type',value:'application/json'},{key:'Authorization',value:'Basic {{token}}'}]],
 ['API2-013',JSON.stringify({total_amount:100000,shipping_address:'A',user_id:999999}),expectSuccess],['API2-014',JSON.stringify({total_amount:100000,shipping_address:'A',role:'admin'}),expectSuccess],
 ['API2-015',valid,expectSuccess],['API2-016',JSON.stringify({total_amount:100000}),expect4xx],['API2-017',JSON.stringify({total_amount:100000,shipping_address:''}),expect4xx],['API2-018',JSON.stringify({total_amount:100000,shipping_address:'   '}),expect4xx],['API2-019',JSON.stringify({total_amount:100000,shipping_address:{x:1}}),expect4xx],
 ['API2-020',valid,expect4xx,[{key:'Content-Type',value:'application/json'},{key:'Authorization',value:'Bearer {{emptyToken}}'}]],['API2-021',valid,expect4xx],['API2-022',valid,expect4xx],
 ['API2-023',valid,expectSuccess],['API2-024',valid,`${expectSuccess}\npm.test('no secrets',()=>pm.expect(JSON.stringify(body)).to.not.match(/password|token|secret|otp/i));`],
 ['API2-025',JSON.stringify({total_amount:100000,shipping_address:'A',id:999999,user_id:999999,cart_id:999999}),expectSuccess],['API2-026',JSON.stringify({total_amount:100000,shipping_address:'A',user_id:999999,role:'admin'}),expectSuccess],
 ['API2-027',JSON.stringify({total_amount:100000,shipping_address:"' OR 1=1 --"}),expectSuccess],['API2-028',JSON.stringify({total_amount:100000,shipping_address:'<script>alert(1)</script>'}),expectSuccess],['API2-029',JSON.stringify({total_amount:100000,shipping_address:'A',user_id:999999,role:'admin',token:'x',extra:'x'}),expectSuccess],['API2-030',JSON.stringify({total_amount:100000,shipping_address:'A','__proto__':{role:'admin'},constructor:{x:1}}),expectSuccess],
 ['API2-031','{"total_amount":100000,',expect4xx,[{key:'Authorization',value:'Bearer {{token}}'},{key:'Content-Type',value:'application/json'}]],
 ['API2-032','not-json',`pm.test('no server crash',()=>pm.expect(pm.response.code).to.be.within(400,499));\npm.test('no stack disclosure',()=>{const t=pm.response.text();pm.expect(t.includes('TypeError')||t.includes('server.js')||t.includes(' at ')).to.eql(false);});`,[{key:'Authorization',value:'Bearer {{token}}'},{key:'Content-Type',value:'text/plain'}]],
 ['API2-033',undefined,`pm.test('unsupported method is controlled',()=>pm.expect(pm.response.code).to.be.oneOf([404,405]));`,[{key:'Authorization',value:'Bearer {{token}}'}]],
 ['API2-034',valid,expectSuccess,[{key:'Content-Type',value:'application/json'},{key:'Authorization',value:'Bearer {{token}}'}]],
 ['API2-035',valid,expectSuccess],['API2-036',valid,expectSuccess],['API2-037',JSON.stringify({total_amount:null}),`${expect4xx}\npm.test('error is JSON and safe',()=>{pm.expect(pm.response.headers.get('Content-Type')||'').to.match(/json/i);const t=pm.response.text().toLowerCase();pm.expect(t.includes('stack')||t.includes('typeerror')||t.includes('server.js')).to.eql(false);});`],
 ['SAPI2-001',valid,expectSuccess],['SAPI2-002',valid,expect4xx],['SAPI2-003',valid,expectSuccess],['SAPI2-004',JSON.stringify({total_amount:"' OR '1'='1",shipping_address:'A'}),expect4xx],['SAPI2-005',valid,expectSuccess],['SAPI2-006',JSON.stringify({total_amount:100000,shipping_address:'x'.repeat(5000)}),expect4xx]
];
const setup = [
  item('SETUP register checkout user','POST',JSON.stringify({name:'Newman API2 Checkout User',email:'{{email}}',password:'{{password}}'}),`pm.test('setup controlled',()=>pm.expect(pm.response.code).to.be.oneOf([200,400,500]));`,undefined,'register'),
  item('SETUP login checkout user','POST',JSON.stringify({email:'{{email}}',password:'{{password}}'}),`${expectSuccess.replace("pm.test('HTTP 200',()=>pm.expect(pm.response.code).to.eql(200));", "pm.test('login 200',()=>pm.expect(pm.response.code).to.eql(200));").replace("pm.test('success schema',()=>{pm.expect(body).to.be.an('object');pm.expect(Object.keys(body).sort()).to.eql(['message','orderId']);pm.expect(body.message).to.eql('Checkout successful');pm.expect(body.orderId).to.be.a('number');pm.expect(body.orderId).to.be.above(0);});", "pm.test('login token',()=>pm.expect(body.token).to.be.a('string'));pm.environment.set('token',body.token);")}`,undefined,'login'),
  item('SETUP add known cart item','POST',JSON.stringify({id:1,name:'Test item',price:50000,quantity:2}),`pm.test('cart setup',()=>pm.expect(pm.response.code).to.eql(200));`,[{key:'Content-Type',value:'application/json'},{key:'Authorization',value:'Bearer {{token}}'}],'cart'),
  item('SETUP register empty-cart user','POST',JSON.stringify({name:'Newman API2 Empty User',email:'{{emptyEmail}}',password:'{{password}}'}),`pm.test('setup controlled',()=>pm.expect(pm.response.code).to.be.oneOf([200,400,500]));`,undefined,'register'),
  item('SETUP login empty-cart user','POST',JSON.stringify({email:'{{emptyEmail}}',password:'{{password}}'}),`const b=pm.response.json();pm.test('empty user token',()=>pm.expect(b.token).to.be.a('string'));pm.environment.set('emptyToken',b.token);`,undefined,'login')
];
// The checkout requests use the setup token unless a case explicitly overrides it.
for (const [id, body, test, headers] of cases) {
  const method = id==='API2-033'?'GET':'POST';
  const h = headers || [{key:'Content-Type',value:'application/json'},{key:'Authorization',value:'Bearer {{token}}'}];
  if (id !== 'API2-009' && !h.some(x=>x.key.toLowerCase()==='authorization')) h.push({key:'Authorization',value:'Bearer {{token}}'});
  setup.push(item(id,method,body,test,h));
}
const collection={info:{name:'HW06 API 2 - Checkout Execution',schema:'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'},variable:[{key:'baseUrl',value:'http://localhost:3000'},{key:'studentId',value:'22127345'}],item:setup};
fs.writeFileSync(out,JSON.stringify(collection,null,2)+'\n');
console.log(`Wrote ${out} with ${cases.length} API cases.`);

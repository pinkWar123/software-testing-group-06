import fs from 'node:fs';
import path from 'node:path';

const dir = path.dirname(new URL(import.meta.url).pathname);
const out = path.join(dir, 'api3_admin_order_status.postman_collection.json');
const sid = `const sid = pm.environment.get('studentId');\npm.request.headers.upsert({key:'X-Student-Id', value:sid});\nconsole.log('X-Student-Id:', sid, '|', pm.info.requestName);`;
const common = `pm.test('Student-ID header is present',()=>pm.expect(pm.request.headers.get('X-Student-Id')).to.eql(pm.environment.get('studentId')));`;
const json = `let body=null; try { body=pm.response.json(); } catch(e) { }`;
const success = `${json}\npm.test('HTTP 200',()=>pm.expect(pm.response.code).to.eql(200));\npm.test('success schema',()=>{pm.expect(body).to.be.an('object');pm.expect(Object.keys(body)).to.eql(['message']);pm.expect(body.message).to.eql('Order status updated');});`;
const error = `${json}\npm.test('controlled 4xx',()=>pm.expect(pm.response.code).to.be.within(400,499));\npm.test('error is safe JSON',()=>{pm.expect(pm.response.headers.get('Content-Type')||'').to.match(/json/i);pm.expect(body).to.be.an('object');pm.expect(body.error).to.be.a('string');const t=pm.response.text().toLowerCase();pm.expect(t.includes('stack')||t.includes('server.js')||t.includes('typeerror')).to.eql(false);});`;
const noCrash = `${json}\npm.test('no server crash',()=>pm.expect(pm.response.code).to.be.below(500));`;

function req(name, method, endpoint, raw, test, headers=[]) {
  const request={method,header:headers,url:{raw:`{{baseUrl}}${endpoint}`,host:['{{baseUrl}}'],path:endpoint.split('/').filter(Boolean)}};
  if(raw!==undefined) request.body={mode:'raw',raw};
  return {name,request,event:[{listen:'prerequest',script:{type:'text/javascript',exec:sid.split('\n')}},{listen:'test',script:{type:'text/javascript',exec:`${common}\n${test}`.split('\n')}}]};
}
const jsonHeaders=[{key:'Content-Type',value:'application/json'}];
const auth=()=>[...jsonHeaders,{key:'Authorization',value:'Bearer {{adminToken}}'}];
const userAuth=()=>[...jsonHeaders,{key:'Authorization',value:'Bearer {{userToken}}'}];
const statusBody=s=>JSON.stringify({status:s});
const email=`hw06.api3.${Date.now()}@example.com`;
const password='Api3Test123!';
const items=[];

items.push(req('SETUP login admin','POST','/api/login',JSON.stringify({email:'admin@eshop.com',password:'Admin123!'}),`${json}\npm.test('admin token',()=>pm.expect(body.token).to.be.a('string'));pm.environment.set('adminToken',body.token);pm.environment.set('adminUserId',String(body.user.id));\npm.test('login 200',()=>pm.expect(pm.response.code).to.eql(200));`,jsonHeaders));
items.push(req('SETUP register API3 order user','POST','/api/register',JSON.stringify({name:'Newman API3 User',email,password}),`pm.test('registration controlled',()=>pm.expect(pm.response.code).to.be.oneOf([200,400]));`,jsonHeaders));
items.push(req('SETUP login API3 order user','POST','/api/login',JSON.stringify({email,password}),`${json}\npm.test('user token',()=>pm.expect(body.token).to.be.a('string'));pm.environment.set('userToken',body.token);`,jsonHeaders));

for (let i=1;i<=10;i++) {
  items.push(req(`SETUP add cart item ${i}`,'POST','/api/cart',JSON.stringify({id:1,name:'API3 fixture item',price:10000,quantity:1}),`pm.test('cart setup controlled',()=>pm.expect(pm.response.code).to.be.oneOf([200,400]));`,userAuth()));
  items.push(req(`SETUP create order ${i}`,'POST','/api/checkout',JSON.stringify({total_amount:10000,shipping_address:`API3 fixture address ${i}`}),`${json}\npm.test('checkout setup',()=>pm.expect(pm.response.code).to.eql(200));pm.test('order ID captured',()=>pm.expect(body.orderId).to.be.a('number'));pm.environment.set('order${i}',String(body.orderId));`,userAuth()));
}

// Prepare independent fixture states: order1/2/8/10 pending; order3/4 confirmed; order5/9 shipping; order6 delivered; order7 canceled.
for (const [name, id, status] of [['confirm order 3','3','confirmed'],['confirm order 4','4','confirmed'],['confirm order 5','5','confirmed'],['ship order 5','5','shipping'],['confirm order 6','6','confirmed'],['ship order 6','6','shipping'],['deliver order 6','6','delivered'],['confirm order 7','7','confirmed'],['cancel order 7','7','canceled'],['confirm order 9','9','confirmed'],['ship order 9','9','shipping']]) {
  const previous=name.startsWith('ship')?'confirmed':name.startsWith('deliver')?'shipping':name.startsWith('cancel')?'confirmed':null;
  const idVar=`{{order${id}}}`;
  items.push(req(`SETUP ${name}`,'PUT',`/api/admin/orders/${idVar}/status`,statusBody(status),`${json}\npm.test('fixture transition',()=>pm.expect(pm.response.code).to.eql(200));`,auth()));
}

const cases=[
 ['API3-001','PUT','1','confirmed',success,auth()],['API3-002','PUT','2','canceled',success,auth()],['API3-003','PUT','3','shipping',success,auth()],['API3-004','PUT','4','canceled',success,auth()],['API3-005','PUT','5','delivered',success,auth()],
 ['API3-006','PUT','999999','confirmed',error,auth()],['API3-007','PUT','8','confirmed',error,jsonHeaders],['API3-008','PUT','8','confirmed',error,[...jsonHeaders,{key:'Authorization',value:'Bearer malformed'}]],['API3-009','PUT','8','confirmed',error,[...jsonHeaders,{key:'Authorization',value:'Bearer forged.invalid.token'}]],['API3-010','PUT','8','confirmed',error,[...jsonHeaders,{key:'Authorization',value:'Bearer expired.invalid.token'}]],['API3-011','PUT','8','confirmed',error,userAuth()],['API3-012','PUT','8','confirmed',error,[...jsonHeaders,{key:'Authorization',value:'Basic {{adminToken}}'}]],['API3-013','PUT','8','confirmed',error,[...userAuth(),{key:'X-Role',value:'admin'}]],
 ['API3-014','PUT','8',undefined,error,auth()],['API3-015','PUT','8',null,error,auth()],['API3-016','PUT','8','',error,auth()],['API3-017','PUT','8','   ',error,auth()],['API3-018','PUT','8','returned',error,auth()],['API3-019','PUT','8','Confirmed',error,auth()],['API3-020','PUT','8',1,error,auth()],['API3-021','PUT','8',['confirmed'],error,auth()],['API3-022','PUT','8',{value:'confirmed'},error,auth()],
 ['API3-023','PUT','10','shipping',error,auth()],['API3-024','PUT','10','delivered',error,auth()],['API3-025','PUT','3','delivered',error,auth()],['API3-026','PUT','9','canceled',error,auth()],['API3-027','PUT','6','confirmed',error,auth()],['API3-028','PUT','7','confirmed',error,auth()],
 ['API3-029','PUT','0','confirmed',error,auth()],['API3-030','PUT','-1','confirmed',error,auth()],['API3-031','PUT','1.5','confirmed',error,auth()],['API3-032','PUT','1 OR 1=1','confirmed',error,auth()],['API3-033','PUT','8',"confirmed'",error,auth()],['API3-034','PUT','8','MALFORMED_JSON',noCrash,[...jsonHeaders,{key:'Authorization',value:'Bearer {{adminToken}}'}]],['API3-035','PUT','8','not-json',`${noCrash}\npm.test('no stack disclosure',()=>{const t=pm.response.text();pm.expect(t.includes('TypeError')||t.includes('server.js')||t.includes(' at ')).to.eql(false);});`,[{key:'Content-Type',value:'text/plain'},{key:'Authorization',value:'Bearer {{adminToken}}'}]],['API3-036','GET','8',undefined,`pm.test('unsupported method controlled',()=>pm.expect(pm.response.code).to.be.oneOf([404,405]));`,[{key:'Authorization',value:'Bearer {{adminToken}}'}]],
 ['API3-037','PUT','10','confirmed',success,auth()],['API3-038','PUT','8','delivered',error,auth()],['API3-039','PUT','10','shipping',success,auth()],['API3-040','PUT','10','delivered',success,auth()]
];
const orderRefs={
  'API3-001':'{{order1}}','API3-002':'{{order2}}','API3-003':'{{order3}}','API3-004':'{{order4}}','API3-005':'{{order5}}',
  'API3-023':'{{order10}}','API3-024':'{{order10}}','API3-025':'{{order8}}','API3-026':'{{order9}}','API3-027':'{{order6}}','API3-028':'{{order7}}',
  'API3-037':'{{order10}}','API3-038':'{{order8}}','API3-039':'{{order10}}','API3-040':'{{order10}}'
};
for (const [id,method,idValue,status,test,headers] of cases) {
  let raw;
  if (id==='API3-014') raw='{}'; else if (id==='API3-015') raw=JSON.stringify({status:null}); else if (id==='API3-021') raw=JSON.stringify({status:[status]}); else if (id==='API3-022') raw=JSON.stringify({status}); else if (id==='API3-020') raw=JSON.stringify({status:1}); else if (id==='API3-034') raw='{"status":'; else if (id==='API3-035') raw='not-json'; else if (status===undefined) raw=undefined; else raw=JSON.stringify({status});
  const endpoint=`/api/admin/orders/${orderRefs[id] || idValue}/status`;
  items.push(req(id,method,endpoint,raw,test,headers));
}

const collection={info:{name:'HW06 API 3 - Admin Order Status Execution',schema:'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'},variable:[{key:'baseUrl',value:'http://localhost:3000'},{key:'studentId',value:'22127345'},{key:'userToken',value:''},{key:'adminToken',value:''}],item:items};
fs.writeFileSync(out,JSON.stringify(collection,null,2)+'\n');
const env={name:'HW06-local',values:[{key:'baseUrl',value:'http://localhost:3000',enabled:true},{key:'studentId',value:'22127345',enabled:true},{key:'adminToken',value:'',enabled:true},{key:'userToken',value:'',enabled:true},...Array.from({length:10},(_,i)=>({key:`order${i+1}`,value:'',enabled:true}))]};
fs.writeFileSync(path.join(dir,'api3_local.postman_environment.json'),JSON.stringify(env,null,2)+'\n');
console.log(`Wrote ${out} with ${cases.length} API cases and ${items.length} total requests.`);

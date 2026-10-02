const assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');
const path = require('node:path');
const root = path.resolve(__dirname,'..');
const dir = path.join(root,'sdks/generated/typescript');
execFileSync(process.execPath,[path.join(root,'node_modules/typescript/bin/tsc'),'-p',path.join(dir,'tsconfig.json')],{stdio:'inherit'});
const {Supadata} = require(path.join(dir,'dist/index.js'));
let seen;
global.fetch = async (input,init) => {
 const request = new Request(input,init); seen=request.url;
 return new Response(JSON.stringify({platform:'tiktok',type:'video',id:'demo-123'}),{status:200,headers:{'Content-Type':'application/json'}});
};
(async()=>{
 const result = await new Supadata({baseUrl:'https://api.supadata.ai/v1',auth:{apiKeyAuth:'demo-not-a-secret'},retry:{maxAttempts:1}}).metadata.get({url:'https://www.tiktok.com/@demo/video/123'});
 assert.equal(result.id,'demo-123'); assert.equal(result.url,undefined);
 console.log(JSON.stringify({mode:'synthetic fixture, offline HTTP mock; no live API calls',octri_typescript_client:'accepted response with optional url absent',requests_intercepted:[seen]},null,2));
})().catch(e=>{console.error(e);process.exitCode=1;});

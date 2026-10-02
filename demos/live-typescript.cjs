const assert = require('node:assert/strict');
const path = require('node:path');
const {execFileSync} = require('node:child_process');
const root = path.resolve(__dirname, '..');
const target = root.endsWith('scrapeninja') ? 'scrapeninja' : 'supadata';
const authOnly = process.argv.includes('--auth-only');
const envName = target === 'scrapeninja' ? 'SCRAPENINJA_API_KEY' : 'SUPADATA_API_KEY';
const key = authOnly ? 'octri-demo-invalid-key' : process.env[envName];
if (!key) {console.error(`Set ${envName} to a provider key before running the live success test.`); process.exit(2);}
const dir = path.join(root, 'sdks', target === 'scrapeninja' ? 'apiroad' : 'generated', 'typescript');
execFileSync(process.execPath, [path.join(root, 'node_modules/typescript/bin/tsc'), '-p', path.join(dir, 'tsconfig.json')], {stdio: 'inherit'});
const sdk = require(path.join(dir, 'dist/index.js'));
(async () => {
  const responses = [];
  const config = {baseUrl: target === 'scrapeninja' ? 'https://scrapeninja.apiroad.net' : 'https://api.supadata.ai/v1', auth: {apiKeyAuth: key}, retry: {maxAttempts: 1}, idempotency: {enabled: false}, timeoutMs: 20000, onResponse: response => responses.push(response.statusCode)};
  const report = {tested_at: new Date().toISOString(), target, language: 'TypeScript', mode: authOnly ? 'live authentication response' : 'live successful operation'};
  let passed = false;
  try {
    if (target === 'scrapeninja') {
      const result = await new sdk.ScrapeNinjaAPIRoadUnofficialOctriDemo(config).scrape.scrape({url: 'https://example.com'});
      assert.ok(typeof result.body === 'string' && result.body.length > 0);
      Object.assign(report, {operation: 'POST /scrape', html_characters: result.body.length});
    } else {
      const result = await new sdk.Supadata(config).metadata.get({url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'});
      assert.equal(result.id, 'dQw4w9WgXcQ'); assert.equal(result.platform, 'youtube');
      Object.assign(report, {operation: 'GET /metadata', platform: result.platform, media_id: result.id});
    }
    Object.assign(report, {status: authOnly ? 'unexpected success with invalid key' : 'passed', http_status: responses.at(-1) ?? null});
    passed = !authOnly;
  } catch (error) {
    passed = authOnly && error.statusCode === (target === 'scrapeninja' ? 403 : 401);
    Object.assign(report, {status: passed ? 'passed' : 'failed', http_status: error.statusCode ?? null, error_type: error.constructor.name});
  }
  console.log(JSON.stringify(report, null, 2));
  process.exitCode = passed ? 0 : 1;
})().catch(error => {console.error(error.constructor.name); process.exitCode = 1;});

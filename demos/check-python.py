"""Contract/model reproduction using a synthetic response, never a live API."""
import asyncio, importlib.util, json, sys
from pathlib import Path
import httpx
from jsonschema import Draft202012Validator
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'sdks/generated/python/src'))
from supadata import Supadata
from supadata.client import ClientConfig, ClientAuthConfig, RetryConfig, NOT_GIVEN
payload = {'platform':'tiktok','type':'video','id':'demo-123'}
schema = json.loads((ROOT/'specs/upstream.json').read_text())
Draft202012Validator({'$ref':'#/components/schemas/Metadata','components':schema['components']}).validate(payload)
spec = importlib.util.spec_from_file_location('upstream_supadata_types',ROOT/'vendor/supadata-python/types.py')
upstream = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = upstream
spec.loader.exec_module(upstream)
try:
    upstream.Metadata(**payload)
except TypeError as exc:
    assert "'url'" in str(exc)
    original_error = str(exc)
else:
    raise AssertionError('Expected upstream model to require url')
async def main():
    seen = []
    def handler(req):
        seen.append(str(req.url))
        return httpx.Response(200,json=payload)
    cfg = ClientConfig(base_url='https://api.supadata.ai/v1',auth=ClientAuthConfig(api_key_auth='demo-not-a-secret'),retry=RetryConfig(max_attempts=1))
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        cfg._client = http
        result = await Supadata(cfg).metadata.get(url='https://www.tiktok.com/@demo/video/123')
        assert result.id == 'demo-123'
        assert result.url is NOT_GIVEN
    assert len(seen) == 1
    print(json.dumps({'mode':'synthetic fixture, offline HTTP mock; no live API calls','schema_validation':'passed','official_python_model':original_error,'octri_python_client':'accepted the schema-valid response','requests_intercepted':seen},indent=2))
asyncio.run(main())

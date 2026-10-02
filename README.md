# Supadata SDK demo with Octri

[![Demo validation](https://github.com/octri-dev/octri-demo-supadata/actions/workflows/demo-validation.yml/badge.svg)](https://github.com/octri-dev/octri-demo-supadata/actions/workflows/demo-validation.yml)

Python and TypeScript SDKs generated with [Octri](https://octri.dev) from Supadata's public OpenAPI specification, covering 21 operations for media metadata, transcripts, web content, and account information.

The clients provide typed requests and responses, resource namespaces, HTTP error classes, configurable retries, and timeouts. The SDK `src/` files match the original Octri-generated artifacts.

Independent demonstration; not an official Supadata package.

## Run the example

Requires Python 3.10+ and Node.js 22.12+.

```sh
git clone https://github.com/octri-dev/octri-demo-supadata.git
cd octri-demo-supadata
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm ci --ignore-scripts
.venv/bin/python demos/check-python.py
npm run check:typescript
```

These offline examples exercise the generated metadata method and its typed response handling, including fields declared optional in the API schema. No provider credentials are needed.

## Call the live API

Set `SUPADATA_API_KEY` to your provider key in your environment, then run:

```sh
.venv/bin/python demos/live-python.py
node demos/live-typescript.cjs
```

Each command requests metadata for the public video `dQw4w9WgXcQ`, checks its platform and media ID, and reports the real HTTP status. API usage follows your provider plan. Keys stay in the environment and are not included in the result.

To test the real authentication/error response without a key:

```sh
.venv/bin/python demos/live-python.py --auth-only
node demos/live-typescript.cjs --auth-only
```

[Live test status](evidence/VALIDATION.md): authentication responses checked in both languages; successful authenticated calls await a valid provider key.

## SDK usage

```python
import asyncio
import os
from supadata import Supadata
from supadata.client import ClientConfig, ClientAuthConfig

async def main():
    config = ClientConfig(
        base_url="https://api.supadata.ai/v1",
        auth=ClientAuthConfig(api_key_auth=os.environ["SUPADATA_API_KEY"]),
    )
    try:
        metadata = await Supadata(config).metadata.get(
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        print(metadata.id)
    finally:
        await config.aclose()

asyncio.run(main())
```

Install the Python SDK locally from `sdks/generated/python`, or build the TypeScript package in `sdks/generated/typescript`. These demo distributions are not published to npm or PyPI. Use a separate environment if you already have the official `supadata` Python package installed.

## Checks and source

```sh
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python demos/verify.py
```

The verification command covers SDK tests, formatting, lint, type checks, package builds, and the offline examples. Live calls are separate and never run automatically in CI.

- [Python SDK](sdks/generated/python)
- [TypeScript SDK](sdks/generated/typescript)
- [Public OpenAPI snapshot](specs/upstream.json)
- [Original public specification](https://docs.supadata.ai/api-reference/v1-openapi.json)
- [Generation provenance](evidence/provenance.json)

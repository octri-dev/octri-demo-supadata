"""Run a real API call. --auth-only uses an invalid placeholder without credentials."""
import argparse
import asyncio
import importlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = 'scrapeninja' if ROOT.name.endswith('scrapeninja') else 'supadata'
ENV_NAME = 'SCRAPENINJA_API_KEY' if TARGET == 'scrapeninja' else 'SUPADATA_API_KEY'
PARSER = argparse.ArgumentParser()
PARSER.add_argument('--auth-only', action='store_true')
ARGS = PARSER.parse_args()
KEY = 'octri-demo-invalid-key' if ARGS.auth_only else os.environ.get(ENV_NAME, '')
if not KEY:
    print(f'Set {ENV_NAME} to a provider key before running the live success test.', file=sys.stderr)
    raise SystemExit(2)
VARIANT = 'apiroad' if TARGET == 'scrapeninja' else 'generated'
sys.path.insert(0, str(ROOT / 'sdks' / VARIANT / 'python' / 'src'))
PACKAGE = 'sdk' if TARGET == 'scrapeninja' else 'supadata'
SDK = importlib.import_module(PACKAGE)
CLIENT = importlib.import_module(PACKAGE + '.client')

async def main():
    responses = []
    config = CLIENT.ClientConfig(
        base_url='https://scrapeninja.apiroad.net' if TARGET == 'scrapeninja' else 'https://api.supadata.ai/v1',
        auth=CLIENT.ClientAuthConfig(api_key_auth=KEY),
        retry=CLIENT.RetryConfig(max_attempts=1),
        idempotency=CLIENT.IdempotencyConfig(enabled=False),
        timeout_s=20,
        on_response=lambda response: responses.append(response.status_code),
    )
    report = {'tested_at': datetime.now(timezone.utc).isoformat(), 'target': TARGET, 'language': 'Python', 'mode': 'live authentication response' if ARGS.auth_only else 'live successful operation'}
    try:
        if TARGET == 'scrapeninja':
            result = await SDK.ScrapeNinjaAPIRoadUnofficialOctriDemo(config).scrape.scrape(url='https://example.com')
            assert isinstance(result.body, str) and len(result.body) > 0
            report.update(operation='POST /scrape', html_characters=len(result.body))
        else:
            result = await SDK.Supadata(config).metadata.get(url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
            assert result.id == 'dQw4w9WgXcQ' and result.platform == 'youtube'
            report.update(operation='GET /metadata', platform=result.platform, media_id=result.id)
        report.update(status='passed' if not ARGS.auth_only else 'unexpected success with invalid key', http_status=responses[-1] if responses else None)
        passed = not ARGS.auth_only
    except Exception as error:
        status = getattr(error, 'status_code', None)
        passed = ARGS.auth_only and status == (403 if TARGET == 'scrapeninja' else 401)
        report.update(status='passed' if passed else 'failed', http_status=status, error_type=type(error).__name__)
    finally:
        await config.aclose()
    print(json.dumps(report, indent=2))
    return 0 if passed else 1

raise SystemExit(asyncio.run(main()))

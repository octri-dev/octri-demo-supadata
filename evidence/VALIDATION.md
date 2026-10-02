# Demo checks

The demo uses the Octri-generated Python and TypeScript SDK source files. Run `demos/verify.py` for the full local checks, or inspect the [automated validation](https://github.com/octri-dev/octri-demo-supadata/actions/workflows/demo-validation.yml).

## Live API checks — October 2, 2026

| Language | Real authentication response | SDK handling |
|---|---|---|
| Python | 401 | SdkUnauthorizedError |
| TypeScript | 401 | SdkUnauthorizedError |

These requests used a deliberately invalid placeholder key against the real API endpoint. They verify connectivity and HTTP error handling. Successful authenticated metadata retrieval remains pending a valid provider key.

The `demos/live-python.py` and `demos/live-typescript.cjs` commands perform that success check when the key is provided in the environment. No live calls run in CI.

Recorded responses: [Python](live-python-authentication.json), [TypeScript](live-typescript-authentication.json).

# Supadata: an unofficial Octri SDK demonstration

[![Demo validation](https://github.com/octri-dev/octri-demo-supadata/actions/workflows/demo-validation.yml/badge.svg)](https://github.com/octri-dev/octri-demo-supadata/actions/workflows/demo-validation.yml)

**A reproducible optional-field contract example, with generated Python and TypeScript SDKs.** Created by Octri for evaluation. Not an official Supadata SDK, not endorsed by Supadata, and not published to a package registry.

## The observation

In the [public OpenAPI spec](https://docs.supadata.ai/api-reference/v1-openapi.json) captured October 2, 2026, `Metadata` requires `platform`, `type`, and `id`; `url` is optional. The [official Python SDK's `Metadata` dataclass at the reviewed commit](https://github.com/supadata-ai/py/blob/35b369f30ad8c9de10957a922265e51c586b9cc6/supadata/types.py) requires `url`. The [client constructs that model directly from the response](https://github.com/supadata-ai/py/blob/35b369f30ad8c9de10957a922265e51c586b9cc6/supadata/client.py).

This synthetic payload validates against the published `Metadata` schema:

```json
{"platform":"tiktok","type":"video","id":"demo-123"}
```

| Check | Observed result |
|---|---|
| JSON Schema validation against the captured public contract | Pass |
| Official Python model, reviewed repository version 1.7.0 | `Metadata.__init__() missing 1 required positional argument: 'url'` |
| Octri-generated Python client receiving mock HTTP 200 | Accepts the response; absent `url` is `NOT_GIVEN` |
| Octri-generated TypeScript client receiving mock HTTP 200 | Accepts the response; absent `url` is `undefined` |

**This is a contract/model mismatch reproduced with a synthetic fixture, not proof of a current production outage.** No live API was called. The team's intended contract needs confirmation: either the SDK should tolerate an absent `url`, or the OpenAPI schema should make it required if the API guarantees it. The demo follows the currently published schema.

A [public report describes the same missing-argument error](https://supadata.featurebase.app/en/p/bug-metadatainit-missing-required-url-argument-when-calling-supadataclientmetadata). Its historical report is context; our results above come from the pinned source and synthetic fixture, not a replay of the reporter's live API call.

## Try it locally

Requires Python 3.10+ and Node.js 22.12+.

```sh
git clone https://github.com/octri-dev/octri-demo-supadata.git
cd octri-demo-supadata
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python demos/check-python.py
npm ci --ignore-scripts
npm run check:typescript
```

The Python demo validates the fixture against the source schema, loads the pinned upstream model in isolation, then intercepts the actual generated client's request with `httpx.MockTransport`. The TypeScript demo compiles the complete generated SDK and intercepts its request with a fetch stub. Neither calls the live API or needs credentials.

Client classes in these builds require an explicit base URL in their constructor config. The examples set `https://api.supadata.ai/v1`. These are local demos: distribution names explicitly identify them as Octri demos; the npm package is marked private. Both official and generated Python clients use the import name `supadata`; keep them in separate environments.

## What is included

- [`specs/upstream.json`](specs/upstream.json): unchanged public spec snapshot, version 1.3.0, containing 21 operations.
- [`sdks/generated`](sdks/generated): Octri Python and TypeScript output, with documented local demo repairs.
- [`vendor/supadata-python`](vendor/supadata-python): only the upstream `types.py` source needed for reproduction, with its original license. Commit `35b369f30ad8c9de10957a922265e51c586b9cc6`; repository package version 1.7.0.
- [`evidence`](evidence): recorded results and source provenance.

## A useful conversation with the team

“I reproduced a small difference between the published Metadata schema and the Python response model: the spec permits an absent URL, while the model requires it. I made a runnable example and generated clients that follow the spec. Is URL intended to be guaranteed? Would keeping SDK models and schema changes aligned reduce work for your team?”

A useful pilot would establish the intended contract, test one real customer workflow with the team's help, then regenerate after a schema change. This demo validates one behavior, not every endpoint or production compatibility.

[Octri](https://octri.dev) · [Public source API](https://supadata.ai) · [Provenance](evidence/provenance.json)

## Demo readiness

The complete SDK suites, lint, format, type checks, builds, package creation, and clean-install smoke tests were checked before sharing. See [the validation report](evidence/VALIDATION.md) for exact counts, commands, local repairs, and limits. The current source includes those repairs; original Octri ZIP hashes remain in provenance for comparison.

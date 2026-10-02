# Demo validation — October 2, 2026

**Ready for a technical evaluation demo using the current repository files.** Verification used local mocks and synthetic fixtures. No live API calls, real API keys, or production-compatibility claims.

## Complete SDK checks

| Package | Language | SDK tests | Lint | Format | Types | Package creation |
|---|---|---|---|---|---|---|
| supadata | python | 42 passed; 0 skipped | Pass | Pass | Pass | Pass |
| supadata | typescript | 58 passed; 0 skipped | Pass | Pass | Pass | Pass |

The SDK suite exercised all 21 operations in each language against local HTTP servers. Mock contract probes reported 126 checks across 25 success/error response modes per contract run. Generated tests include synthetic errors; they do not establish the live service's behavior.

The original targeted demo also passes in Python and TypeScript. Built wheel and npm archives were installed in fresh environments. Each installed client passed import, a high-level call, authentication-header capture, 401 error/request-ID handling, a 429 retry followed by success, and timeout handling. See `installed-python-results.json` and `installed-typescript-results.json`.

## Repairs made after the broader test run

- The Python response test compared Pydantic's normalized timestamp strings with the original wire spelling. It now compares timezone-aware date-times as instants. A regression test also verifies that different instants and different ordinary strings still fail comparison. The SDK's datetime parsing behavior is unchanged.
- Fetch transport and contract probes now omit a body for GET/HEAD, resolving lint findings and making that constraint explicit.
- Test/mock scripts are executable in the checkout.
- SDK README installation commands use these local files rather than unrelated registry packages. Distribution names explicitly identify the Octri demos, and npm packages are private.
- Dependency lockfiles and a repeatable verification command are included. Formatting was applied to changed source and test files.

These are local demo repairs to Octri output. The original spec snapshots and original ZIP hashes remain in provenance. Regenerating in Octri may require reapplying these repairs until the generator itself incorporates them. **Use the current repository or demo ZIP when sharing; the earlier CDN ZIPs do not contain these repairs.**

## Reproduce the full checks

Requires Node.js 22.12+ and Python 3.10+. Local verification used Node 24.19.0 and Python 3.14.4 on macOS; GitHub Actions uses Python 3.12 and Node 24 on Ubuntu.

From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python demos/verify.py
```

The verifier installs locked JavaScript development dependencies, runs all SDK checks and the focused demos, and exits unsuccessfully if any check fails. Dependency setup requires registry access; SDK requests go to mocks only. The [GitHub validation workflow](https://github.com/octri-dev/octri-demo-supadata/actions/workflows/demo-validation.yml) repeats this from a clean checkout.

## Scope of confidence

This supports sending a clearly unofficial, runnable demonstration. It does not certify all API combinations, live authentication, service-specific retry/idempotency rules, latency, or production use. A live integration test with credentials provided by the target team is the next validation step.

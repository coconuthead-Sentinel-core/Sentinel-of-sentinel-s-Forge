# Interdepartmental Memo To VR Studios Assistant

**Date:** 2026-03-24  
**From:** Engineering  
**To:** Assistant Working In VR Studios  
**Subject:** Verbatim closeout instructions for final fact-check, SDLC reconciliation, and acceptance readiness

Please follow these instructions verbatim. Review the current Sentinel Forge repository state as a thorough fact checker, use the latest AQA results as aggregated data rather than starting from stale assumptions, and close the remaining gap between repository-state completion and environment-state confirmation. Do not expand scope. Do not reopen settled code paths without evidence. Do verify, reconcile, and finalize.

## Aggregated Data Inputs

Use these files as the primary handoff packet:

- `docs/INTERDEPARTMENTAL_COMPLETION_MEMO.md`
- `docs/VR_STUDIOS_DATA_NODE.md`
- `docs/sdlc/`

The `docs/VR_STUDIOS_DATA_NODE.md` file is the central data node. Treat each child node in that document as a smaller evidence package that must either be confirmed, partially confirmed, or not confirmed.

## Current AQA Baseline

The latest AQA review materially confirmed the repository-state completion claims for items 7 through 9:

1. Item 7 confirmed at repository level: compose wiring, `.env.example`, and `tests/test_billing.py` all exist and billing tests passed.
2. Item 8 confirmed at repository level: nginx TLS paths match, PEM files exist, certificate parsing succeeded, and the key pair matched.
3. Item 9 confirmed at repository level: `release.yml` is no longer a stub, release docs exist, and the full test suite passed.
4. Remaining partial confirmations are environment-related only: Docker unavailable, nginx unavailable, and GitHub Actions not executed live in the AQA sandbox.
5. No direct contradiction was found against `docs/INTERDEPARTMENTAL_COMPLETION_MEMO.md`.

## Review Standard Requested

Please be meticulous.

1. Verify claims directly from the repository and runtime behavior where your environment permits
2. Prefer disconfirming checks over trust-based acceptance
3. Call out any mismatch between documentation, code, generated artifacts, and actual behavior
4. If a claim is only partially true, mark it partial rather than complete
5. If you find a blocker, identify the exact file, line, and runtime impact

## Engineering Claims To Confirm

### Item 7: Stripe live runtime wiring is complete

Claimed evidence:

- `docker-compose.yml` now injects `JWT_SECRET_KEY` and all required `STRIPE_*` variables into the `app` container runtime
- `.env.example` documents the required runtime keys without embedding real secrets
- `tests/test_billing.py` verifies the Stripe checkout path in both mock and configured modes

Files to inspect:

- `docker-compose.yml`
- `.env.example`
- `tests/test_billing.py`
- `backend/routes/billing_routes.py`
- `backend/core/config.py`

Suggested checks:

1. Confirm the compose file fails fast if `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, and the three plan price IDs are missing
2. Confirm the backend code actually consumes those variables and leaves mock mode when configured
3. Run the billing tests and confirm they pass in your environment
4. If possible, verify the container receives the variables at runtime rather than only at build time

### Item 8: TLS certificate placement is complete

Claimed evidence:

- `nginx/ssl/fullchain.pem` and `nginx/ssl/privkey.pem` exist
- The certificate parses as valid X.509 and matches the private key
- `scripts/generate_dev_tls_cert.py` can regenerate the pair

Files to inspect:

- `nginx/nginx.conf`
- `nginx/ssl/fullchain.pem`
- `nginx/ssl/privkey.pem`
- `nginx/ssl/README.md`
- `scripts/generate_dev_tls_cert.py`

Suggested checks:

1. Confirm the filenames exactly match the paths nginx expects
2. Confirm the certificate and key match cryptographically
3. Confirm nginx can load the files in your environment
4. Note clearly that the current certificate is bootstrap/self-signed unless you confirm otherwise

### Item 9: Release pipeline and secrets contract are complete

Claimed evidence:

- `.github/workflows/release.yml` is no longer a stub
- The workflow runs tests, builds the Docker image, pushes to GHCR by default, and supports alternate registries
- `docs/RELEASE_PIPELINE.md` documents required variables, registry secrets, and deploy-time runtime secrets

Files to inspect:

- `.github/workflows/release.yml`
- `Dockerfile`
- `docs/RELEASE_PIPELINE.md`

Suggested checks:

1. Parse and review the workflow YAML for valid structure and trigger behavior
2. Confirm the workflow has a real test job and a real build/publish job
3. Confirm the registry login paths make sense for GHCR and non-GHCR registries
4. Confirm the documented secrets match what the workflow and runtime actually need
5. If your environment supports it, run or simulate the workflow logic far enough to verify there is no obvious release blocker

## Existing Engineering Verification Results

Engineering already observed the following in this workspace:

1. `tests/test_billing.py` passed locally
2. The full repository test suite passed locally with `47 passed`
3. The generated TLS certificate parsed successfully and matched the private key
4. The release workflow YAML parsed successfully
5. Runtime env wiring and secrets documentation were programmatically checked

Please treat those as claims to validate, not as final truth.

## Requested Output

## Additional SDLC Instruction

Use the SDLC suite under `docs/sdlc/` as the repository implementation baseline, and compare it against the software development life cycle source-of-truth structure provided in the handoff conversation. The repo already contains filled SDLC documents, so your job is to reconcile and validate them, not to replace them blindly.

For each SDLC document that is still in scope for closure or acceptance:

1. Confirm the document is filled and internally consistent.
2. Add or identify three verifiable proofs that the document remains accurate and current.
3. Mark any field that cannot be proved from repo state or your environment as `Pending External Verification` with the reason.
4. Update stale evidence references if you find them.
5. Do not invent approvals, signatures, dates, budgets, or legal attestations that are not present or cannot be supported.

Suggested priority order:

1. `docs/sdlc/P9-CLOSE-075.md`
2. `docs/sdlc/P9-ACCEPT-076.md`
3. `docs/sdlc/P9-TRANS-077.md`
4. `docs/sdlc/P9-MAINT-078.md`
5. `docs/sdlc/P9-PIR-079.md`
6. `docs/sdlc/P9-DRP-080.md`
7. Remaining Phase 1 initiation documents only where evidence or wording is now stale

## Required Runtime Follow-Up

If your environment supports these tools, run them in this order:

1. `docker compose config` for `docker-compose.yml`
2. `docker compose up --build` or equivalent dry-run validation if safe
3. `nginx -t` against the current nginx config and PEM files
4. Any GitHub Actions workflow validation or release simulation available to you

If your environment does not support one of those checks, classify it as an environment limitation, not as a repository defect.

## Required Output

Please return a concise review with:

1. `Confirmed`
2. `Partially Confirmed`
3. `Not Confirmed`

Under each section, list the exact evidence and any file references. If everything is confirmed, say so explicitly. If anything is not confirmed, identify whether it is a documentation issue, code issue, runtime issue, or environment limitation.

Then provide:

1. An SDLC delta list naming any documents you updated
2. A proof ledger listing the three proofs used for each updated document
3. A final release-readiness statement that says either `Ready for acceptance review` or `Blocked`, with exact blockers if blocked

## Review Target

The current engineering completion memo is here:

- `docs/INTERDEPARTMENTAL_COMPLETION_MEMO.md`

Please compare your findings against that memo and either validate it or annotate where it overstates completion.

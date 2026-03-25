# Partner Environment Execution Checklist

Purpose: clear all external verification blockers in one execution pass and convert project state from Blocked to Ready for acceptance review.

Owner: VR Studios assistant environment reviewer
Target duration: 45 to 90 minutes

## Preflight

1. Open repository root and pull latest main branch.
2. Confirm Docker is installed and running.
3. Confirm nginx is installed locally, or confirm Docker nginx image validation will be used.
4. Confirm GitHub CLI is authenticated to the repository.
5. Confirm environment file exists at project root with required runtime keys populated.

Required runtime keys:
- API_KEY
- JWT_SECRET_KEY
- CORS_ORIGINS
- STRIPE_SECRET_KEY
- STRIPE_WEBHOOK_SECRET
- STRIPE_PRICE_ID_STARTER
- STRIPE_PRICE_ID_PRO
- STRIPE_PRICE_ID_ENTERPRISE
- AOAI_ENDPOINT
- AOAI_KEY
- COSMOS_ENDPOINT
- COSMOS_KEY

Reference files:
- [docker-compose.yml](docker-compose.yml)
- [.env.example](.env.example)
- [backend/routes/billing_routes.py](backend/routes/billing_routes.py)
- [nginx/nginx.conf](nginx/nginx.conf)
- [.github/workflows/release.yml](.github/workflows/release.yml)
- [docs/RELEASE_PIPELINE.md](docs/RELEASE_PIPELINE.md)

## Single-Pass Validation Sequence

### Step 1: Compose contract validation

Run: docker compose config

Pass criteria:
- Command succeeds with exit code 0.
- No missing-variable error for Stripe or JWT keys.

Evidence to capture:
- Terminal output showing resolved services.
- Any warning lines, if present.

### Step 2: Build and startup validation

Run: docker compose up --build -d

Pass criteria:
- app and nginx containers both start.
- app healthcheck passes.

Evidence to capture:
- docker compose ps output.
- docker compose logs app last 50 lines.
- docker compose logs nginx last 50 lines.

### Step 3: Nginx TLS load test

Run: nginx -t using current nginx config and TLS files.
If local nginx is unavailable, validate with container logs after compose startup.

Pass criteria:
- Syntax OK and test successful, or nginx container boots cleanly without cert/key load errors.

Evidence to capture:
- nginx -t output or nginx container startup logs.

### Step 4: Billing runtime verification

Run billing tests:
- python -m pytest tests/test_billing.py -q

Run full suite:
- python -m pytest tests -q

Pass criteria:
- Billing tests pass.
- Full suite passes.

Evidence to capture:
- Test summary lines for billing and full suite.

### Step 5: Runtime endpoint verification

Verify API health and readiness:
- GET /api/healthz
- GET /api/readyz

Verify billing behavior with configured runtime:
- exercise /api/billing/plans
- create or use an authenticated user and obtain a Bearer token
- exercise /api/billing/checkout in configured mode with Authorization header
- confirm the checkout response is not the mock `https://checkout.stripe.com/mock?...` path when Stripe secrets are configured

Pass criteria:
- health and ready endpoints are healthy.
- billing endpoints respond and authenticated checkout does not return mock mode when secrets are configured.

Evidence to capture:
- HTTP responses for health, ready, signup or login, billing plans, and billing checkout calls.

### Step 6: GitHub Actions release workflow verification

Run manual workflow dispatch for Release workflow, then inspect jobs.

Pass criteria:
- Test Suite job passes.
- Build And Publish Container job passes.
- Release manifest artifact is produced.

Evidence to capture:
- Workflow run URL.
- Job status screenshots or logs.
- Artifact name and contents summary.

### Step 7: SDLC acceptance closure updates

Update these docs with environment-verified results:
- [docs/sdlc/P9-CLOSE-075.md](docs/sdlc/P9-CLOSE-075.md)
- [docs/sdlc/P9-ACCEPT-076.md](docs/sdlc/P9-ACCEPT-076.md)
- [docs/sdlc/P9-TRANS-077.md](docs/sdlc/P9-TRANS-077.md)
- [docs/sdlc/P9-MAINT-078.md](docs/sdlc/P9-MAINT-078.md)
- [docs/sdlc/P9-PIR-079.md](docs/sdlc/P9-PIR-079.md)
- [docs/sdlc/P9-DRP-080.md](docs/sdlc/P9-DRP-080.md)

Required updates:
- Replace Pending External Verification for runtime tool checks that were completed.
- Keep legal/signature approvals as pending unless actually signed.
- Preserve factual boundary: no invented approvals or dates.

### Step 8: Acceptance decision

Mark final status:
- Ready for acceptance review only if Steps 1 to 7 pass.
- Blocked if any required step fails.

If blocked, record exact blocker type:
- Documentation issue
- Code issue
- Runtime issue
- Environment limitation

## Final Deliverables To Return

1. Confirmed / Partially Confirmed / Not Confirmed matrix with evidence.
2. Proof ledger with three proofs per updated SDLC document.
3. Final statement: Ready for acceptance review or Blocked, with exact blockers.
4. Updated interdepartmental memo if status changes.

Primary memo references:
- [docs/MEMO_TO_VR_STUDIOS_ASSISTANT.md](docs/MEMO_TO_VR_STUDIOS_ASSISTANT.md)
- [docs/INTERDEPARTMENTAL_COMPLETION_MEMO.md](docs/INTERDEPARTMENTAL_COMPLETION_MEMO.md)
- [docs/VR_STUDIOS_DATA_NODE.md](docs/VR_STUDIOS_DATA_NODE.md)

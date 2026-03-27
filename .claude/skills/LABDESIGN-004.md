# LABDESIGN-004 — Laboratory Design & Testing Framework

## Purpose
Defines the testing strategy, quality gates, and experimental framework for Sentinel Forge. Ensures all components meet production standards before deployment.

## Test Infrastructure

### Unit Tests
- `tests/test_service.py` — QNFService core operations
- `tests/test_api.py` — API endpoint responses
- `tests/test_billing.py` — Stripe billing flow
- `tests/test_config_security.py` — JWT security validation
- `tests/test_api_integration.py` — HTTP-level integration tests (11 tests)

### Integration Test Coverage
| Area | Tests | Status |
|------|-------|--------|
| Health Check | 1 | Passing |
| Auth Flow | 7 | Passing |
| Billing Flow | 3 | Passing |
| Config Security | 3 | Passing |
| Service Core | ~46 | Passing |
| **Total** | **60** | **All passing** |

### Frontend Build Verification
- TypeScript compilation: `npx tsc -b`
- Vite production build: `npm run build`
- Output: 192KB JS, 11KB CSS
- CI Job: `.github/workflows/ci.yml` → `frontend-build`

## Quality Gates
1. All 60 tests must pass
2. TypeScript must compile with zero errors
3. Vite build must produce valid output
4. JWT security validation must reject weak secrets
5. No secrets in committed code

## Integration Points
- **CI**: `.github/workflows/ci.yml` — runs `pytest` and frontend build
- **Docker**: `Dockerfile` — multi-stage build validates both frontend and backend
- **Config**: `backend/core/config.py` — `validate_security_configuration()` as startup gate

## QNF Ecosystem Layer
**FORGE** (Mind/Software) — Quality assurance

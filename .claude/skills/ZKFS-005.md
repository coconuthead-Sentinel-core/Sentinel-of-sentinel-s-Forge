# ZKFS-005 — Zero-Knowledge File System & Privacy Architecture

## Purpose
Privacy-first data architecture ensuring user data is stored securely with minimal exposure. Defines the security boundaries, authentication flow, and data isolation patterns.

## Security Architecture

### Authentication Flow
```
Signup → bcrypt hash → SQLite/Cosmos storage
Login → bcrypt verify → JWT access + refresh tokens
Request → Bearer token → JWT decode → user_id extraction
Protected Route → RBAC check → authorize or 401
```

### JWT Security
- **Enforcement**: `backend/core/config.py` — `validate_security_configuration()`
- Rejects known weak secrets (empty, "secret", "changeme", etc.)
- Requires 32+ character minimum in production
- Access token expiry: configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`
- Refresh token rotation supported

### RBAC Role Hierarchy
- `user` — standard access
- `admin` — elevated access via `admin_guard` dependency
- API key guard for service-to-service calls

### Data Isolation
- User data scoped by `user_id` in all repositories
- Notes isolated per user in Cosmos DB partitions
- SQLite with WAL mode for concurrent read safety
- No cross-user data leakage in query patterns

## Integration Points
- **Auth Routes**: `backend/routes/auth_routes.py` — signup, login, refresh, profile
- **Security Guards**: `backend/core/security.py` — `api_key_guard`, `admin_guard`
- **User Storage**: `backend/infrastructure/user_repository.py` — Cosmos → SQLite → memory fallback
- **Frontend**: `AuthContext.tsx` — localStorage token management with auto-refresh
- **Frontend**: `ProtectedRoute` component in `App.tsx`

## Privacy Principles
1. Passwords never stored in plaintext (bcrypt)
2. JWT tokens have bounded lifetimes
3. API routes require explicit authentication
4. Sensitive config rejected at startup if insecure
5. `.gitignore` excludes `*.db`, `.env`, credentials

## QNF Ecosystem Layer
**FORGE** (Mind/Software) — Security infrastructure

# SESSION-WRAP-001 — Session Persistence & Context Wrapping

## Purpose
Ensures session context persists across page refreshes, browser closes, and reconnections. Wraps session state so users never lose their place — critical for ADHD-friendly UX where interruptions are expected.

## Integration Points
- **Frontend Auth**: `AuthContext.tsx` — already persists JWT tokens in localStorage
  - On mount: restores `access_token` and `refresh_token` from localStorage
  - Validates via `getProfile()` call
  - Auto-clears on 401 response
- **Backend Sessions**: `backend/schemas.py` — `SyncSnapshot` with `session_id` field
- **Backend Sync**: `sentinel_sync.py` — sync coordinator with session handling
- **Chat History**: `ChatPage.tsx` — message history lives in component state (volatile)

## Current State
- Auth session persistence: **DONE** (localStorage tokens)
- Chat history persistence: **NOT YET** (messages lost on navigation)
- Cognition results persistence: **NOT YET**
- Notes: **DONE** (server-side via Cosmos DB / SQLite)
- Dashboard state: **DONE** (fetched fresh each visit)

## Recommended Implementation
1. Persist chat history to localStorage or IndexedDB with a session key
2. Restore chat history on ChatPage mount
3. Add a "session wrap" summary when user leaves chat (POST to `/api/cog/process`)
4. Store session metadata in backend via sync coordinator
5. Surface session history in InsightsPage under "Recent Sessions"

## QNF Ecosystem Layer
**Avatar** (Body/Interface) — User experience continuity

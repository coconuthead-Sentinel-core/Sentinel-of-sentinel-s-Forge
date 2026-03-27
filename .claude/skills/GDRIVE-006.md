# GDRIVE-006 — External Storage & Sync Integration

## Purpose
Manages external storage integration patterns for Sentinel Forge — synchronization between local state, cloud databases, and external file systems.

## Current Storage Stack

### Primary: Azure Cosmos DB
- Notes repository: `infrastructure/cosmos_repo.py`
- User repository: `infrastructure/user_repository.py` (Cosmos path)
- Partition-based isolation per user

### Fallback: SQLite
- User repository: `infrastructure/user_repository.py` (SQLite path)
- WAL mode for concurrent read performance
- Thread-safe with `check_same_thread=False`
- Auto-creates `data/users.db` on first run

### Tertiary: In-Memory
- Final fallback if both Cosmos and SQLite unavailable
- Volatile — data lost on restart

### Local Persistence
- `backend/storage.py` — `JSONStore` for QNF service state
- `data/glyphs_pack.sample.json` — glyph definitions
- Session state in browser localStorage

## Sync Coordinator
- `sentinel_sync.py` — orchestrates state sync across storage tiers
- `SyncSnapshot` schema with `session_id` for tracking sync operations
- Glyphic signature verification for data integrity

## Integration Points
- **Config**: `COSMOS_ENDPOINT`, `COSMOS_KEY`, `COSMOS_DATABASE` env vars
- **Fallback Logic**: Repository classes auto-detect available storage
- **Docker**: `user-data` volume for SQLite persistence across container restarts
- **Frontend**: `api.ts` — all data access through typed HTTP client

## Future: External Drive Sync
- Google Drive / OneDrive integration for user file import
- Skill file sync from external sources
- Backup/restore workflows

## QNF Ecosystem Layer
**MAU-1** (Brain/Hardware) — Storage infrastructure

API Routes (key endpoints)

- GET /api/healthz → 204
- GET /api/readyz → 200 with summary
- GET /api/status → system status (pools, processors, latency)
- GET /api/metrics → compact JSON metrics
- GET /api/metrics/prom → Prometheus text; includes qnf_bus_*, qnf_intent_count, qnf_topic_count, qnf_threads_total, qnf_resonance_*
- POST /api/stress {iterations:int, concurrent:bool, async_mode:bool} → StressResult
- GET /api/jobs/{job_id} → async stress job status

Cognition

- POST /api/cog/process {data:any} → {input, output, processing_time, metadata}
- GET /api/cog/status → orchestrator status
- GET /api/cog/rules | PUT /api/cog/rules {rules: {pattern: tag}}
- GET /api/cog/memory | DELETE /api/cog/memory
- GET /api/cog/prime → prime metrics
- GET /api/cog/suggest?limit=5 → suggested rules

Threads / Seeds / Glyphs

- GET /api/cog/threads[?topic=x] → list threads
- GET /api/cog/threads/{id}[?limit=50] → thread detail
- GET /api/cog/stats → {intents, topics}
- GET /api/cog/seeds → {seeds:[...]}
- POST /api/cog/seeds {items:[...]} → upsert seeds
- GET /api/cog/matrix[?top_k=20] → token matrix per topic
- GET /api/glyphs/aliases → alias map
- POST /api/glyphs/pack {shapes:{...}} → bulk seeds/rules/aliases
- POST /api/glyphs/interpret {sequence:"APEX->CORE->EMIT"} → {tokens, topics, route}

Sync / Glyphic protocol

- POST /api/sync/update {agent, state:{...}} → updates tri-node state
- GET /api/sync/snapshot → session snapshot
- GET /api/sync/trinode → roles/presence
- POST /api/glyphs/validate {sequence:[...]} → validity
- GET /api/glyphs/boot → boot steps

WebSocket

- /ws/sync → NDJSON‑like stream; payloads include {type:"cog.intent"|"sync.update", data:{...}}

Notes

- Include header X-API-Key if QNF_API_KEY is set.

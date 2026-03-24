# Sentinel Forge — User Guide

Welcome to **Sentinel Forge**, an enterprise-grade cognitive AI orchestration platform.

---

## Getting Started

### 1. Obtain Your API Key

After signing up, you'll receive an API key. Include it in all requests:

```
X-API-Key: your-api-key-here
```

Or set it in the web UI by storing it in your browser's localStorage:
```javascript
localStorage.setItem('QNF_API_KEY', 'your-api-key-here');
```

### 2. Access the Platform

| Interface | URL | Description |
|-----------|-----|-------------|
| Web UI | `/ui/` | Interactive control panel |
| Dashboard | `/ui/dashboard.html` | Real-time metrics & monitoring |
| API Docs | `/docs` | Interactive Swagger/OpenAPI documentation |
| Ops Panel | `/api/ops` | Operations overview |

---

## Core Features

### AI Chat

Send messages to the cognitive AI pipeline:

```bash
curl -X POST https://your-domain/api/ai/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{"messages": [{"role": "user", "content": "Analyze this pattern"}]}'
```

### Cognition Pipeline

Process data through the cognitive engine:

```bash
curl -X POST https://your-domain/api/cog/process \
  -H "Content-Type: application/json" \
  -d '{"data": "Your input text here"}'
```

### Notes (Memory System)

Save and retrieve notes in the persistent memory lattice:

```bash
# Save a note
curl -X POST https://your-domain/api/notes/upsert \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{"text": "Important finding", "tag": "research"}'

# List all notes
curl https://your-domain/api/notes
```

### Embeddings

Generate vector embeddings for semantic analysis:

```bash
curl -X POST https://your-domain/api/ai/embeddings \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{"input": ["text to embed"], "dimensions": 1536}'
```

### Symbolic Rules

Configure pattern-matching rules for the cognition engine:

```bash
# Get current rules
curl https://your-domain/api/cog/rules

# Update rules
curl -X PUT https://your-domain/api/cog/rules \
  -H "Content-Type: application/json" \
  -d '{"rules": {"pattern": "tag-name"}}'
```

### Glyphic Protocol

Validate symbolic glyph sequences:

```bash
curl -X POST https://your-domain/api/glyphs/validate \
  -H "Content-Type: application/json" \
  -d '{"sequence": ["structure","logic","emotion","transform","unity"]}'
```

---

## Real-Time Features

### WebSocket Connections

Connect to live data streams:

| Endpoint | Purpose |
|----------|---------|
| `ws://your-domain/ws/sync` | Live sync updates & events |
| `ws://your-domain/ws/metrics` | Real-time performance metrics (2s interval) |
| `ws://your-domain/ws/events` | Real-time event stream (1s interval) |

**JavaScript example:**
```javascript
const ws = new WebSocket('wss://your-domain/ws/metrics?api_key=your-key');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Metrics:', data);
};
```

---

## Monitoring & Health

| Endpoint | Purpose |
|----------|---------|
| `GET /api/healthz` | Liveness check (returns 204) |
| `GET /api/readyz` | Readiness check (returns JSON) |
| `GET /api/status` | System status overview |
| `GET /api/metrics` | Detailed metrics snapshot |
| `GET /api/metrics/prom` | Prometheus-format metrics |

---

## User Roles

| Role | Access Level |
|------|-------------|
| **Viewer** | Read-only: status, metrics, rules |
| **User** | Standard: AI chat, notes, cognition processing |
| **Operator** | Management: pools, stress tests, state inspection |
| **Admin** | Full: teardown, rebuild, upgrade, profile reset |

---

## Rate Limits

API calls are subject to rate limiting to ensure fair usage:

- Default: **600 requests per minute** per API key
- Burst: Up to **120 requests** in rapid succession
- Exceeding limits returns `429 Too Many Requests`

---

## Error Codes

| Code | Meaning |
|------|---------|
| `200` | Success |
| `204` | Success (no content) |
| `400` | Bad request (check your input) |
| `401` | Invalid or missing API key |
| `403` | Insufficient permissions for your role |
| `404` | Resource not found |
| `413` | Request body too large (max 10MB) |
| `429` | Rate limit exceeded |
| `500` | Internal server error |
| `502` | Upstream AI service error |
| `503` | Service temporarily unavailable |

---

## FAQ

**Q: How do I reset my cognitive memory?**
A: Use `DELETE /api/cog/memory` (requires admin role).

**Q: Can I use multiple AI providers?**
A: Yes. Configure via environment variables: `AZURE_OPENAI_ENDPOINT`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GOOGLE_API_KEY`.

**Q: How do I export my data?**
A: Use `GET /api/notes` to retrieve all saved notes, and `GET /api/state` to export system state.

**Q: Is my data encrypted?**
A: Yes. All data is encrypted in transit (TLS 1.2+) and at rest (Azure Cosmos DB encryption).

---

## Support

- **API Reference:** Visit `/docs` on your deployment for interactive API documentation
- **Troubleshooting:** See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- **Issues:** Report bugs at the project repository

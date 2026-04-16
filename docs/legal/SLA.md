# Service Level Agreement (SLA)
## The Forge Trilogy â€” [YOUR LLC NAME]

**Effective:** April 10, 2026
**Applies to:** Pro and Enterprise subscription tiers

---

## 1. SLA Coverage

This SLA applies to:

| Platform | Endpoints Covered |
|----------|------------------|
| Sentinel-of-sentinel-s-Forge | All `/api/*` endpoints; Flask server availability |
| Sentinel-of-sentinel-s-Forge | All `/api/*` and `/api/ai/*` REST endpoints; WebSocket `/ws/*` |
| Sentinel-of-sentinel-s-Forge | All REST endpoints; WebSocket endpoints; Voice processing pipeline |

---

## 2. Uptime Commitments

| Tier | Monthly Uptime Target | Max Allowed Downtime / Month |
|------|----------------------|------------------------------|
| Developer | Best effort (no SLA) | â€” |
| Starter | Best effort (no SLA) | â€” |
| Pro | **99.0%** | 7.2 hours / month |
| Enterprise | **99.5%** | 3.6 hours / month |

**Uptime is calculated as:**
```
Uptime % = (Total minutes in month âˆ’ Downtime minutes) / Total minutes in month Ã— 100
```

---

## 3. What Counts as Downtime

| Event | Counts as Downtime? |
|-------|-------------------|
| Service unavailable (5xx errors on all requests) | âœ… Yes |
| API response time > 30 seconds consistently | âœ… Yes |
| Partial degradation (some endpoints down) | âœ… Pro-rated |
| Slow responses (< 30 seconds) | âŒ No â€” performance degradation, not outage |
| Azure OpenAI model-side delays | âŒ No â€” third-party, outside our control |
| Scheduled maintenance (notified 24 hours prior) | âŒ No â€” excluded |
| Force majeure | âŒ No â€” excluded |
| Customer-caused failure | âŒ No â€” excluded |

---

## 4. Latency Targets

| Metric | Target | Measured By |
|--------|--------|-------------|
| API Response Time (p50) | < 500ms | `/api/status` health probe |
| API Response Time (p95) | < 2,000ms | Monthly log analysis |
| AI Response Time (p50) | < 5,000ms | End-to-end API call |
| WebSocket Connection | < 1,000ms | Connection establishment |
| ComputeNodeRouter (Sentinel-of-sentinel-s-Forge) | < 20ms internal | Automated threshold detection |

*Note: AI response time depends on Azure OpenAI model response â€” not fully within our control.*

---

## 5. SLA Credits

If uptime falls below the committed target, Customer receives a credit on the next invoice:

| Uptime Achieved | Pro Credit | Enterprise Credit |
|----------------|-----------|------------------|
| 98.0%â€“98.9% | 10% of monthly fee | 15% of monthly fee |
| 97.0%â€“97.9% | 20% of monthly fee | 25% of monthly fee |
| 96.0%â€“96.9% | 30% of monthly fee | 40% of monthly fee |
| Below 96.0% | 50% of monthly fee | 50% of monthly fee |

**Maximum credit:** 50% of the monthly fee for the affected month.
**Credits are applied to next invoice** â€” not paid as cash refunds.

### How to Claim
Email [YOUR EMAIL] with subject "SLA Credit Request â€” [Month Year]" within 30 days of the end of the affected month. Include your account email and a description of the outage.

---

## 6. Monitoring

### How We Monitor
- **Health probe:** `GET /api/healthz` checked every 60 seconds
- **Alerting:** Automated alerts to [YOUR EMAIL] when health probe fails 3 consecutive times
- **Azure monitoring:** Azure service health dashboard for infrastructure-level events

### Transparency
- Incident reports are filed in `docs/compliance/INCIDENT_LOG.md`
- Customers may request uptime reports for any billing month

---

## 7. Incident Response Times

| Severity | Definition | Initial Response | Resolution Target |
|----------|-----------|-----------------|------------------|
| **P1 â€” Critical** | Complete outage; all API calls failing | 1 hour | 4 hours |
| **P2 â€” High** | Major feature unavailable; >50% error rate | 4 hours | 24 hours |
| **P3 â€” Medium** | Degraded performance; some features affected | 1 business day | 3 business days |
| **P4 â€” Low** | Minor issue; workaround available | 3 business days | Next sprint |

*Business hours: Mondayâ€“Friday 09:00â€“18:00 Central Time (CT)*
*P1 incidents: responded to 24/7 via [YOUR EMAIL]*

---

## 8. Scheduled Maintenance

- **Window:** Sunday 02:00â€“06:00 CT (preferred)
- **Notice:** Minimum 24 hours via email for standard maintenance; 72 hours for extended maintenance
- **Emergency maintenance:** May occur without advance notice; communicated via email as soon as possible
- Scheduled maintenance does **not** count toward downtime for SLA purposes

---

## 9. Support Channels

| Channel | Tiers | Response Time |
|---------|-------|--------------|
| Email ([YOUR EMAIL]) | All | 1 business day (Pro), 4 hours (Enterprise) |
| GitHub Issues | Developer, Starter | 3 business days |
| Dedicated contact (Enterprise) | Enterprise only | Per agreement |

---

## 10. Exclusions

This SLA does not apply to:
- Developer and Starter tier subscriptions
- Service disruptions caused by Customer (e.g., API key misuse, DDoS from Customer)
- Disruptions caused by Azure OpenAI model outages (outside Provider's control)
- Disruptions from Customer's own infrastructure (client-side)
- Beta or preview features (clearly labeled)
- Force majeure events

---

## 11. Term

This SLA applies for the duration of the Pro or Enterprise subscription. SLA terms may be updated with 30 days' notice; updates do not reduce committed uptime during an existing term.

---

*Contact: [YOUR EMAIL]*
*[YOUR LLC NAME] | [YOUR TEXAS ADDRESS] | Texas, United States*


# Register of Processing Activities
## Sentinel-of-sentinel-s-Forge v5.2.0

**Template source:** ICT Institute — Register of Processing Activities (CC Attribution License)
**Standard:** GDPR Article 30
**Prepared by:** Shannon Bryan Kelly (Data Controller)
**Date:** April 2026
**Review Date:** April 2027

---

## Controller Details

| Field | Details |
|-------|---------|
| Controller name | Shannon Bryan Kelly |
| Organization | Sentinel-of-sentinel-s-Forge (sole proprietorship) |
| Contact | [Add before multi-user deployment] |
| Data Protection Officer | Not required at current scale |

---

## ⚠️ Special Category Data Notice

This platform serves neurodivergent users and may incidentally process data relating to **cognitive and neurodevelopmental conditions** (ADHD, Autism Spectrum, Dyslexia). Under GDPR Article 9, this may constitute **special category health data**. This register reflects heightened controls accordingly.

---

## Processing Activity 1: Cognitive Lens Processing

| Field | Details |
|-------|---------|
| **Activity name** | User input processing through neurodivergent cognitive lenses |
| **Purpose** | Generate cognitively-styled AI responses adapted to user's selected processing style |
| **Legal basis** | Legitimate interest (cognitive exploration tool) |
| **Data subjects** | Users (currently: owner only) |
| **Personal data** | Free-text and emoji/glyph inputs (may incidentally contain personal data) |
| **Special category data** | Not intentionally collected; user may disclose neurodivergent status or health conditions |
| **Art. 9 basis (if special cat.)** | Explicit consent — NOT YET IMPLEMENTED for persistent storage |
| **Source** | Directly from data subject |
| **Recipients** | Microsoft Azure OpenAI (processor) |
| **International transfers** | USA/EU — Microsoft Standard Contractual Clauses |
| **Retention period** | Session only — deleted when server session ends |
| **Security measures** | No persistent storage; HTTPS to Azure; API key in `.env` |
| **Processor** | Microsoft Azure (DPA via subscription) |

---

## Processing Activity 2: Lens Selection

| Field | Details |
|-------|---------|
| **Activity name** | Cognitive lens selection and configuration |
| **Purpose** | Configure processing style for user session |
| **Legal basis** | Legitimate interest |
| **Data subjects** | Users |
| **Personal data** | Lens selection (ADHD/Autism/Dyslexia/Neurotypical) — may imply neurodivergent status |
| **Special category data** | Potentially — lens choice may constitute implicit health disclosure |
| **Retention period** | Session only — not stored |
| **Security measures** | Not recorded; session-only state |
| **Notes** | Lenses framed as processing style choices, not diagnoses |

---

## Processing Activity 3: Three-Zone Memory Classification

| Field | Details |
|-------|---------|
| **Activity name** | Entropy-based zone classification (GREEN / YELLOW / RED) |
| **Purpose** | Organize cognitive processing outputs |
| **Data subjects** | None — processed outputs, not personal data |
| **Personal data** | None — entropy values and zone labels only |
| **Retention period** | Session only — reset when server restarts |
| **Security measures** | In-memory only |

---

## Processing Activity 4: System Metrics

| Field | Details |
|-------|---------|
| **Activity name** | Performance and usage metrics |
| **Purpose** | System health monitoring |
| **Personal data** | None — aggregated system counts only |
| **Retention period** | Session only |

---

## Processing Activity 5: CI/CD Pipeline Logs

| Field | Details |
|-------|---------|
| **Activity name** | Automated test and build logging |
| **Purpose** | Code quality assurance |
| **Data subjects** | Developer (commit author metadata) |
| **Personal data** | GitHub username, commit metadata |
| **Retention period** | GitHub Actions default (90 days) |
| **Processor** | GitHub (Microsoft) |

---

## Future Processing Activities (Not Yet Active)

| Activity | Status | Required Before Activation |
|----------|--------|--------------------------|
| Cosmos DB conversation persistence | Not active | Updated DPIA; explicit consent (Art. 9 for health data); privacy notice; retention policy |
| Multi-user accounts and sessions | Not active | Privacy notice; consent mechanism; DPIA update; Art. 9 safeguards |
| Cognitive profile storage | Not active | Explicit Art. 9 consent; encryption at rest; access controls; full DPIA review |
| Research data collection | Not active | Research ethics review; institutional agreement; explicit consent |

---

*Template adapted from ICT Institute Register of Processing Activities under Creative Commons Attribution License.*
*Source: https://github.com/swzaken/freetemplates*

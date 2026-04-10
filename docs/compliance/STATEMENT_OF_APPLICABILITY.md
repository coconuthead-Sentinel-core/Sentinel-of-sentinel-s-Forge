# Statement of Applicability (SoA)
## Sentinel-of-sentinel-s-Forge v5.2.0

**Template source:** ICT Institute — Statement of Applicability ISO 27001-2022 (CC Attribution License)
**Standard:** ISO/IEC 27001:2022 — Annex A Controls
**Prepared by:** Shannon Bryan Kelly
**Date:** April 2026
**Review Date:** April 2027

---

## Purpose

This Statement of Applicability documents which ISO 27001:2022 Annex A controls are applicable to Sentinel-of-sentinel-s-Forge, how each is implemented, and the justification for any controls excluded.

**Legend:**
- ✅ Applicable and implemented
- ⚠️ Applicable — partially implemented or planned
- ➖ Not applicable (justification provided)

---

## 5. Organizational Controls

| Control | Title | Status | Implementation / Justification |
|---------|-------|--------|-------------------------------|
| 5.1 | Policies for information security | ✅ | `INFORMATION_SECURITY_POLICY.md` — this document suite |
| 5.2 | Information security roles and responsibilities | ✅ | Single owner: Shannon Bryan Kelly |
| 5.3 | Segregation of duties | ➖ | Not applicable — single-person operation |
| 5.4 | Management responsibilities | ✅ | Owner is sole decision-maker |
| 5.7 | Threat intelligence | ⚠️ | Azure Security Center monitors infrastructure |
| 5.8 | Information security in project management | ✅ | SDLC documentation; security reviewed per release; accessibility in Definition of Done |
| 5.9 | Inventory of information and other assets | ✅ | Asset inventory in ASSET_RISK_REGISTER.md |
| 5.10 | Acceptable use of information | ✅ | AI Policy §4 — includes neurodivergent-specific rules |
| 5.12 | Classification of information | ✅ | Classified in Information Security Policy §5 |
| 5.14 | Information transfer | ✅ | Transfers only to Azure (DPA in place) |
| 5.15 | Access control | ✅ | Owner-only access; GitHub repo control |
| 5.17 | Authentication information | ✅ | API keys in `.env`; excluded from GitHub |
| 5.19 | Information security in supplier relationships | ✅ | Azure, GitHub — ISO 27001 certified suppliers |
| 5.20 | Addressing security in supplier agreements | ✅ | Azure subscription DPA; GitHub ToS |
| 5.23 | Information security for cloud services | ✅ | Azure OpenAI — Microsoft ISO 27001 certified |
| 5.24 | Incident management planning | ✅ | INCIDENT_LOG.md; IS Policy §10 |
| 5.26 | Response to information security incidents | ✅ | IS Policy §10 — neurodivergent data breach escalation included |
| 5.29 | Business continuity planning | ✅ | Mock mode fallback; GitHub code backup; accessibility maintained in degraded mode |
| 5.31 | Legal, statutory, regulatory, and contractual requirements | ✅ | GDPR Art. 9 (DPIA.md); AI Act (FRIA.md) |
| 5.34 | Privacy and data protection | ✅ | DPIA.md — elevated for neurodivergent special category data |

---

## 6. People Controls

| Control | Title | Status | Implementation / Justification |
|---------|-------|--------|-------------------------------|
| 6.1 | Screening | ➖ | Not applicable — no employees currently |
| 6.3 | Information security awareness | ✅ | Owner maintains awareness; AI Policy §9 |
| 6.7 | Remote working | ✅ | All work remote; `.env` local protection |
| 6.8 | Information security event reporting | ✅ | INCIDENT_LOG.md process defined |

---

## 7. Physical Controls

| Control | Title | Status | Implementation / Justification |
|---------|-------|--------|-------------------------------|
| 7.1 | Physical security perimeters | ⚠️ | Home office — standard residential security |
| 7.7 | Clear desk and clear screen | ✅ | Best practice; screen locked when away |
| 7.10 | Storage media | ⚠️ | `.env` backed up on encrypted storage |
| 7.14 | Secure disposal or re-use of equipment | ⚠️ | `.env` wiped before device disposal |

---

## 8. Technological Controls

| Control | Title | Status | Implementation / Justification |
|---------|-------|--------|-------------------------------|
| 8.1 | User endpoint devices | ✅ | Owner's Windows laptop — standard security |
| 8.2 | Privileged access rights | ✅ | Azure portal access — owner only |
| 8.3 | Information access restriction | ✅ | GitHub access control; `.env` local only |
| 8.5 | Secure authentication | ✅ | GitHub MFA; Azure MFA recommended |
| 8.7 | Protection against malware | ✅ | Windows Defender / standard AV |
| 8.9 | Configuration management | ✅ | `.env` config; `requirements.txt` |
| 8.10 | Information deletion | ✅ | No persistent user data; session-only processing |
| 8.11 | Data masking | ⚠️ | Special attention required for neurodivergent health data if storage enabled |
| 8.12 | Data leakage prevention | ✅ | `.gitignore` prevents credential leakage |
| 8.13 | Information backup | ✅ | GitHub is full code backup |
| 8.14 | Redundancy | ✅ | Mock mode fallback for Azure outages |
| 8.20 | Networks security | ⚠️ | HTTPS to Azure; localhost API only |
| 8.21 | Security of network services | ✅ | Azure OpenAI — TLS encrypted |
| 8.24 | Use of cryptography | ✅ | HTTPS for all Azure communications |
| 8.25 | Secure development lifecycle | ✅ | Full SDLC documentation; CI pipeline; accessibility in DoD |
| 8.26 | Application security requirements | ✅ | API contracts documented; error standards defined |
| 8.28 | Secure coding | ✅ | No hardcoded secrets; input validation |
| 8.29 | Security testing | ✅ | Unit tests; CI pipeline; 80-prompt evaluation |
| 8.32 | Change management | ✅ | Git commits; version history |
| 8.33 | Test information | ✅ | Evaluation uses synthetic prompts — no real user data |

---

## Special Controls — Neurodivergent User Data (GDPR Article 9)

These controls go beyond standard ISO 27001 and are required due to the potential for special category data:

| Control | Requirement | Status |
|---------|-------------|--------|
| Art. 9 processing prohibition | No storage of health/disability data without explicit consent | ✅ No storage by default |
| Explicit consent mechanism | Required before Cosmos DB activation | ⚠️ Not yet built |
| Data minimization | Process only what the lens function requires | ✅ Session-only processing |
| Purpose limitation | Cognitive synthesis only — no profiling | ✅ Design principle |
| Heightened breach response | 72-hour GDPR notification if health data breached | ✅ Documented in IS Policy |

---

*Template adapted from ICT Institute Statement of Applicability ISO 27001-2022 under Creative Commons Attribution License.*
*Source: https://github.com/swzaken/freetemplates*

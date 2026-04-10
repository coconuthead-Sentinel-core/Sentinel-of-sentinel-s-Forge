# Asset Inventory and Risk Register
## Sentinel-of-sentinel-s-Forge v5.2.0

**Template source:** ICT Institute — Assets-and-risks-ISO-27001 (CC Attribution License)
**Standard:** ISO/IEC 27001:2022
**Prepared by:** Shannon Bryan Kelly
**Date:** April 2026
**Review Date:** April 2027

---

## Asset Inventory

| ID | Asset | Type | Owner | Classification | Location |
|----|-------|------|-------|----------------|---------|
| A-001 | Azure OpenAI API Key | Credential | Shannon Bryan Kelly | 🔴 Confidential | `.env` file (local) |
| A-002 | Azure Endpoint URL | Credential | Shannon Bryan Kelly | 🔴 Confidential | `.env` file (local) |
| A-003 | `.env` file | Credential | Shannon Bryan Kelly | 🔴 Confidential | Local only |
| A-004 | `quantum_nexus_forge_v5_2_enhanced.py` — Main engine | Source code | Shannon Bryan Kelly | 🟡 Internal | GitHub / local |
| A-005 | `backend/` — FastAPI backend module | Source code | Shannon Bryan Kelly | 🟡 Internal | GitHub / local |
| A-006 | `frontend/` — Web dashboard | Source code | Shannon Bryan Kelly | 🟢 Public | GitHub / local |
| A-007 | `evaluation/` — Evaluation pipeline | Source code | Shannon Bryan Kelly | 🟢 Public | GitHub / local |
| A-008 | `tests/` — Unit test suite | Source code | Shannon Bryan Kelly | 🟢 Public | GitHub / local |
| A-009 | Cognitive lens logic (ADHD, Autism, Dyslexia, Neurotypical) | Intellectual property | Shannon Bryan Kelly | 🟡 Internal | GitHub / local |
| A-010 | `.github/workflows/` — CI pipeline | Configuration | Shannon Bryan Kelly | 🟢 Public | GitHub |
| A-011 | `requirements.txt` | Configuration | Shannon Bryan Kelly | 🟢 Public | GitHub / local |
| A-012 | SDLC documentation suite | Documentation | Shannon Bryan Kelly | 🟢 Public | GitHub / local |
| A-013 | Compliance documentation suite | Documentation | Shannon Bryan Kelly | 🟢 Public | GitHub / local |
| A-014 | GitHub repository | Platform | Shannon Bryan Kelly | 🟢 Public | GitHub (Microsoft) |
| A-015 | Azure OpenAI resource | Platform | Shannon Bryan Kelly | 🔴 Confidential | Azure cloud |
| A-016 | Developer laptop | Hardware | Shannon Bryan Kelly | 🟡 Internal | Home office |
| A-017 | Neurodivergent lens design (proprietary cognitive model) | Intellectual property | Shannon Bryan Kelly | 🟡 Internal | GitHub / local |

---

## Risk Register

### Risk Assessment Scale

| Likelihood | Score | Severity | Score | Risk = L × S |
|-----------|-------|---------|-------|--------------|
| Very Low | 1 | Negligible | 1 | 1–4: LOW |
| Low | 2 | Low | 2 | 5–9: MEDIUM |
| Medium | 3 | Medium | 3 | 10–16: HIGH |
| High | 4 | High | 4 | 17–25: CRITICAL |
| Very High | 5 | Critical | 5 | |

---

| ID | Risk | Assets | Likelihood | Severity | Score | Level | Controls | Residual |
|----|------|--------|-----------|---------|-------|-------|---------|---------|
| R-001 | API key committed to GitHub | A-001, A-002, A-003 | 2 | 5 | 10 | 🟡 HIGH | `.gitignore`; pre-commit review; GitHub secret scanning | 🟢 LOW |
| R-002 | Azure account compromised | A-015 | 2 | 5 | 10 | 🟡 HIGH | Azure MFA; strong password; limited access | 🟢 LOW |
| R-003 | Cognitive lens outputs stigmatize neurodivergent users | A-004, A-009, A-017 | 2 | 5 | 10 | 🟡 HIGH | Lens designed as strength-based; 80-prompt evaluation; accessibility review in DoD | 🟢 LOW |
| R-004 | User enters neurodivergent health data in prompts | A-004, A-005 | 4 | 4 | 16 | 🟡 HIGH | No persistent storage; user guidance; Azure data processing terms; DPIA completed | 🟡 MEDIUM |
| R-005 | Developer laptop lost or stolen | A-001–A-017 | 2 | 4 | 8 | 🟡 MEDIUM | Full disk encryption; GitHub backup; `.env` local only | 🟡 MEDIUM |
| R-006 | Azure OpenAI outage | A-015 | 3 | 2 | 6 | 🟡 MEDIUM | Mock mode fallback | 🟢 LOW |
| R-007 | Cosmos DB activated storing health data without consent | A-015 | 1 | 5 | 5 | 🟡 MEDIUM | Not activated; DPIA update + consent required before activation | 🟢 LOW |
| R-008 | Platform misused for clinical diagnosis | A-004, A-009 | 2 | 5 | 10 | 🟡 HIGH | AI Policy §4; FRIA; "not a diagnostic tool" statement required in UI | 🟡 MEDIUM |
| R-009 | Accessibility failure — platform unusable by neurodivergent users | A-006 | 2 | 4 | 8 | 🟡 MEDIUM | Accessibility review in Definition of Done; chunked responses; color + label zones | 🟢 LOW |
| R-010 | Malicious dependency | A-004–A-008 | 2 | 3 | 6 | 🟡 MEDIUM | Dependabot alerts; pinned versions; CI testing | 🟡 MEDIUM |

---

## Treatment Plan

| Risk ID | Treatment | Owner | Target Date |
|---------|-----------|-------|------------|
| R-001 | Maintain `.gitignore`; run pre-commit secret scan | Shannon Bryan Kelly | Ongoing |
| R-002 | Enable Azure MFA; quarterly access review | Shannon Bryan Kelly | April 2026 |
| R-003 | Maintain strength-based lens framing; re-evaluate per release | Shannon Bryan Kelly | Per release |
| R-004 | Add "do not enter health data" guidance to UI | Shannon Bryan Kelly | Next sprint |
| R-005 | Enable full disk encryption on laptop | Shannon Bryan Kelly | April 2026 |
| R-008 | Add "not a diagnostic tool" disclaimer to all UI screens | Shannon Bryan Kelly | Next sprint |

---

*Template adapted from ICT Institute Assets-and-risks-ISO-27001 under Creative Commons Attribution License.*
*Source: https://github.com/swzaken/freetemplates*

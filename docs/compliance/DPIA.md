# Data Protection Impact Assessment (DPIA)
## Sentinel-of-sentinel-s-Forge v5.2.0

**Template source:** ICT Institute — DPIA Template (CC Attribution License)
**Prepared by:** Shannon Bryan Kelly
**Date:** April 2026
**Review Date:** April 2027

---

## 1. Introduction

This DPIA identifies, assesses, and documents privacy risks for the Sentinel-of-sentinel-s-Forge platform — a neurodivergent cognitive processing system. It is conducted in accordance with GDPR Article 35.

### Is a DPIA Required?

| Criterion | Present? |
|-----------|---------|
| Processing of special category data (health/disability) | Potentially — users may disclose neurodivergent status |
| Innovative technology with privacy implications | Yes — AI cognitive processing |
| Vulnerable individuals (neurodivergent users) | Yes |
| Systematic monitoring of individuals | No |
| Automated decision-making with legal/significant effects | No |

**DPIA Decision: REQUIRED** — The combination of AI processing, neurodivergent user group, and potential special category data makes this DPIA mandatory under GDPR Article 35.

---

## 2. System Description

**Sentinel-of-sentinel-s-Forge** accepts user text and emoji inputs, processes them through neurodivergent cognitive lenses (ADHD, Autism, Dyslexia, Neurotypical) powered by Azure OpenAI, and returns cognitively-styled AI responses. Outputs are classified into a three-zone memory system (GREEN/YELLOW/RED). In default configuration, no data is stored after the session ends.

### Data Flow

```
User types text or emoji glyph input
              ↓
CognitiveLensProcessor — selects lens (adhd/autism/dyslexia/neurotypical)
              ↓
Azure OpenAI API (Microsoft cloud — USA/EU)
              ↓
GlyphProcessor + SpatialCognition — in-memory processing
              ↓
ThreeZoneMemory — in-memory classification only
              ↓
Response returned to user
              ↓
[Optional] Cosmos DB persistence — NOT active by default
```

---

## 3. Personal Data Inventory

| Data Element | Source | Purpose | Legal Basis | Stored? |
|-------------|--------|---------|-------------|---------|
| User prompt text | User input | Cognitive processing | Legitimate interest / consent | No — in memory only |
| Selected cognitive lens | User selection | Processing configuration | Legitimate interest | No — session only |
| Emoji/glyph sequences | User input | Symbolic interpretation | Legitimate interest | No — in memory only |
| Processing results (zone, entropy) | System output | Memory classification | Legitimate interest | No — in memory only |
| IP address | HTTP request | Server operation | Legitimate interest | No — not logged by default |

**Special Category Data Concern (GDPR Art. 9):**

Neurodivergent status (ADHD, Autism, Dyslexia) is **special category health data** under GDPR Article 9. Risks include:
- Users selecting the "ADHD lens" may implicitly disclose their own neurodivergent status
- Users may include explicit health disclosures in prompts
- **Current mitigation:** Lens selection is a processing choice, not a data storage event; no data is stored by default

---

## 4. Privacy Risk Assessment

### Risk 1: Special Category Data in Prompts

| Field | Detail |
|-------|--------|
| Description | User includes neurodivergent diagnosis, health information, or disability status in a prompt |
| Likelihood | High — by design, users may discuss their cognitive experience |
| Severity | High — special category data |
| Risk Level | 🔴 HIGH |
| Mitigation | No persistent storage; UI guidance; Azure data processing terms; users advised not to enter identifiable health data |
| Residual Risk | 🟡 MEDIUM |

---

### Risk 2: Lens Selection as Implicit Health Disclosure

| Field | Detail |
|-------|--------|
| Description | A user selecting "ADHD" or "Autism" lens implicitly discloses neurodivergent status |
| Likelihood | Medium |
| Severity | Medium |
| Risk Level | 🟡 MEDIUM |
| Mitigation | Lens selection is not stored; framing lenses as "cognitive processing styles" rather than diagnostic categories |
| Residual Risk | 🟢 LOW |

---

### Risk 3: Azure OpenAI Processing Sensitive Prompts

| Field | Detail |
|-------|--------|
| Description | Microsoft processes neurodivergent-related user prompts through Azure OpenAI |
| Likelihood | High (by design) |
| Severity | Medium |
| Risk Level | 🟡 MEDIUM |
| Mitigation | Microsoft Azure data processing terms apply; Azure does not train on customer data; Standard Contractual Clauses cover international transfers |
| Residual Risk | 🟢 LOW |

---

### Risk 4: Cosmos DB Storing Sensitive Cognitive Data

| Field | Detail |
|-------|--------|
| Description | If Cosmos DB enabled, all cognitive processing results (including implied health data) would be stored |
| Likelihood | Low (not yet enabled) |
| Severity | Very High |
| Risk Level | 🔴 HIGH |
| Mitigation | NOT activated; explicit DPIA update, privacy notice, and explicit user consent required before activation |
| Residual Risk | 🟢 LOW (while disabled) |

---

### Risk 5: Unauthorized Credential Access

| Field | Detail |
|-------|--------|
| Description | Azure API credentials compromised, allowing access to processing infrastructure |
| Likelihood | Low |
| Severity | High |
| Risk Level | 🟡 MEDIUM |
| Mitigation | `.env` excluded from GitHub; credentials not shared; single-owner access |
| Residual Risk | 🟢 LOW |

---

## 5. Overall Privacy Risk Summary

| Risk | Residual Level |
|------|----------------|
| Special category data in prompts | 🟡 MEDIUM |
| Lens selection as health disclosure | 🟢 LOW |
| Azure OpenAI processing | 🟢 LOW |
| Cosmos DB persistence | 🟢 LOW (while disabled) |
| Credential exposure | 🟢 LOW |

**Overall DPIA Result: LOW–MEDIUM RISK**

Deployable in current single-user configuration with active controls. **Must not** enable Cosmos DB or multi-user access without full updated DPIA and privacy notice.

---

## 6. Measures in Place and Required

| Measure | Status |
|---------|--------|
| No persistent data storage by default | ✅ Built-in |
| Azure OpenAI data processing terms accepted | ✅ Via Azure subscription |
| `.env` credentials excluded from version control | ✅ `.gitignore` configured |
| Lenses framed as processing styles, not diagnoses | ✅ Design principle |
| UI disclaimer: "not a diagnostic tool" | ⚠️ Recommended addition to UI |
| User guidance not to enter health data | ⚠️ Add to UI and README |
| Privacy notice | ⚠️ Required before multi-user deployment |
| Explicit consent mechanism for health data | ⚠️ Required if Cosmos DB activated |
| Data breach response plan | ✅ See INCIDENT_LOG.md |

---

## 7. Data Subject Rights

| Right | How Handled |
|-------|-------------|
| Right of access | No personal data stored — nothing to access |
| Right to erasure | No personal data stored — nothing to erase |
| Right to object to automated decisions | No automated decisions about individuals |
| Right to portability | Not applicable |
| Rights regarding health data (Art. 9) | No health data stored; lens selection not recorded |

---

## 8. International Data Transfers

| Transfer | Safeguard |
|----------|-----------|
| Prompts → Azure OpenAI (USA/EU) | Microsoft Azure Standard Contractual Clauses |

---

## 9. Consultation

Given the focus on neurodivergent users, consultation with neurodivergent community representatives is recommended before any multi-user public deployment.

---

## 10. DPIA Conclusion

**Processing may proceed** in current configuration. This DPIA must be updated before:
- Enabling Cosmos DB persistence
- Deploying to multiple users
- Adding user accounts or authentication
- Expanding to healthcare, education, or employment contexts
- Storing any lens selection or cognitive processing history

---

## 11. Sign-Off

| Role | Name | Date |
|------|------|------|
| Data Controller / Architect | Shannon Bryan Kelly | April 2026 |

---

*Template adapted from ICT Institute DPIA Template under Creative Commons Attribution License.*
*Source: https://github.com/swzaken/freetemplates*

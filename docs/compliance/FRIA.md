# Fundamental Rights Impact Assessment (FRIA)
## Sentinel-of-sentinel-s-Forge v5.2.0

**Template source:** ICT Institute — FRIA Assessment Template V2.0 (CC Attribution License)
**Prepared by:** Shannon Bryan Kelly
**Date:** April 2026
**Review Date:** April 2027

---

## 1. System Description

| Field | Details |
|-------|---------|
| System name | Sentinel-of-sentinel-s-Forge |
| Version | 5.2.0 |
| Purpose | Neurodivergent cognitive processing and knowledge synthesis |
| Deployer | Shannon Bryan Kelly |
| AI Provider | Microsoft Azure OpenAI |
| Deployment context | Local / private — portfolio, research, and personal use |
| Target users | General public with emphasis on neurodivergent individuals |
| Geographic scope | United States (primarily) |

---

## 2. AI Act Risk Classification

| Question | Answer |
|----------|--------|
| Is this system listed in Annex III (High-Risk AI) as currently deployed? | No |
| Does it make consequential decisions about natural persons? | No |
| Does it affect employment, education, credit, or safety decisions? | No (as currently deployed) |
| Does it process biometric data? | No |
| Does it provide medical or therapeutic services? | No — exploratory tool only |
| Does it use prohibited techniques (manipulation, social scoring)? | No |

**Current Classification: General-Purpose / Limited-Risk AI System**

⚠️ **Escalation Trigger:** If platform is used in healthcare, employment screening, education assessment, or clinical contexts — RECLASSIFY as High-Risk under Annex III, Category 1 (biometric categorization) or Category 5 (employment/education). Full conformity assessment would then be required.

---

## 3. Fundamental Rights Assessment

### 3.1 Right to Human Dignity (Article 1, EU Charter)

| Risk | Likelihood | Severity | Mitigation |
|------|-----------|---------|------------|
| Cognitive lens outputs pathologize or demean neurodivergent cognition | Medium | High | Lens design explicitly frames ADHD/Autism/Dyslexia as cognitive strengths — reviewed in development |
| System used to produce stigmatizing content about neurodivergent people | Low | High | Acceptable use policy prohibits this explicitly |
| Users mistake AI cognitive modeling for clinical assessment | Medium | High | UI must clearly state: not a diagnostic tool |

**Residual Risk: LOW–MEDIUM** — Active monitoring required given target user group.

---

### 3.2 Right to Privacy and Data Protection (Articles 7 & 8, EU Charter)

| Risk | Likelihood | Severity | Mitigation |
|------|-----------|---------|------------|
| Users disclose neurodivergent status in prompts (special category data) | High | High | Users advised not to enter health data; no persistent storage by default |
| Azure OpenAI processing neurodivergent-related prompts | Medium | Medium | Microsoft data processing terms apply; no training on user data |
| Cosmos DB storing sensitive prompt data | Low (not yet enabled) | High | Full DPIA required before Cosmos DB activation |

**Residual Risk: MEDIUM** — Elevated due to nature of user group and sensitivity of cognitive data.

---

### 3.3 Right to Non-Discrimination (Article 21, EU Charter)

| Risk | Likelihood | Severity | Mitigation |
|------|-----------|---------|------------|
| Cognitive lens produces systematically different quality responses for different groups | Low | High | All lenses evaluated against 80-prompt benchmark (3.94–3.99/5.0 — equivalent performance) |
| System reinforces stereotypes about neurodivergent processing styles | Low | Medium | Lens design reviewed; outputs are exploratory not prescriptive |
| Users in healthcare/employment contexts use outputs to discriminate | Low | High | Acceptable use policy explicitly prohibits this |

**Residual Risk: LOW**

---

### 3.4 Rights of Persons with Disabilities (Article 26, EU Charter)

| Risk | Likelihood | Severity | Mitigation |
|------|-----------|---------|------------|
| Platform is inaccessible to the neurodivergent users it serves | Low | High | Accessibility review required in Definition of Done for all stories |
| Color-only zone coding (GREEN/YELLOW/RED) inaccessible to colorblind users | Medium | Medium | Labels shown alongside colors; planned improvement |
| Text responses not chunked — overwhelming for ADHD users | Low | Medium | Response chunking is a design requirement |

**Residual Risk: LOW–MEDIUM** — Accessibility is a core design commitment; ongoing review required.

---

### 3.5 Right to Non-Discrimination Based on Health Status (GDPR Article 9)

| Risk | Likelihood | Severity | Mitigation |
|------|-----------|---------|------------|
| Neurodivergent diagnosis data stored without explicit consent | Low (not stored by default) | High | No persistent storage in default mode; explicit DPIA required before enabling |
| Third-party access to cognitive profile data | Very Low | High | No multi-user access currently; single-user local deployment |

**Residual Risk: LOW** (current deployment) / **HIGH** (if persistent storage enabled without review)

---

### 3.6 Right to an Effective Remedy (Article 47, EU Charter)

| Risk | Likelihood | Severity | Mitigation |
|------|-----------|---------|------------|
| User harmed by AI output with no recourse | Medium | Medium | Incident reporting process defined in AI Policy |
| No audit trail of cognitive processing decisions | Medium | Low | Metrics endpoint provides partial audit; zone assignments logged |

**Residual Risk: LOW–MEDIUM**

---

## 4. Overall Risk Summary

| Rights Area | Residual Risk Level |
|-------------|---------------------|
| Human Dignity | 🟡 LOW–MEDIUM |
| Privacy & Data Protection | 🟡 MEDIUM |
| Non-Discrimination | 🟢 LOW |
| Rights of Persons with Disabilities | 🟡 LOW–MEDIUM |
| Health Data (GDPR Art. 9) | 🟢 LOW (current scope) |
| Effective Remedy | 🟡 LOW–MEDIUM |

**Overall FRIA Result: LOW–MEDIUM RISK**

Deployable at current scope with active monitoring. Re-assess before any expansion to multi-user, healthcare, or employment contexts.

---

## 5. Required Mitigation Measures

| Measure | Owner | Status |
|---------|-------|--------|
| AI Policy published with neurodivergent-specific protections | Shannon Bryan Kelly | ✅ Complete |
| Lenses evaluated for equivalent performance (80-prompt benchmark) | Evaluation pipeline | ✅ Complete — 3.94–3.99/5.0 |
| UI clearly states "not a diagnostic tool" | Frontend | ⚠️ Recommended — add to UI |
| Accessibility review in Definition of Done | SDLC process | ✅ Documented |
| No persistent storage by default | Platform design | ✅ Built-in |
| DPIA completed | DPIA.md | ✅ Complete |
| Incident reporting process | AI Policy §10 | ✅ Complete |
| Colorblind-accessible zone labeling | Frontend | ⚠️ Planned improvement |

---

## 6. Monitoring Plan

| Activity | Frequency | Owner |
|---------|-----------|-------|
| Review lens outputs for dignity and non-discrimination | Per release | Shannon Bryan Kelly |
| Accessibility audit of UI | Per release | Shannon Bryan Kelly |
| Update FRIA when features or deployment scope change | Per release | Shannon Bryan Kelly |
| Review EU AI Act implementing rules | Annually | Shannon Bryan Kelly |
| FRIA re-assessment if multi-user or clinical deployment planned | Before expansion | Shannon Bryan Kelly |

---

## 7. Sign-Off

| Role | Name | Date |
|------|------|------|
| System Architect / Owner | Shannon Bryan Kelly | April 2026 |

---

*Template adapted from ICT Institute FRIA Assessment Template V2.0 under Creative Commons Attribution License.*
*Source: https://github.com/swzaken/freetemplates*

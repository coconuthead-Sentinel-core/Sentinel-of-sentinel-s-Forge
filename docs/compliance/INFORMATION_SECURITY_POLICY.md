# Information Security Policy
## Sentinel-of-sentinel-s-Forge v5.2.0

**Template source:** ICT Institute — Information Security Policy Template (CC Attribution License)
**Standard:** ISO/IEC 27001:2022
**Prepared by:** Shannon Bryan Kelly
**Effective Date:** April 2026
**Review Date:** April 2027

---

## 1. Purpose

This policy establishes the information security objectives, principles, and commitments for **Sentinel-of-sentinel-s-Forge**. It protects the confidentiality, integrity, and availability of all information assets associated with the platform — with heightened attention to the privacy of neurodivergent users.

---

## 2. Scope

This policy applies to:
- All source code, configuration files, and documentation
- Azure OpenAI API credentials and `.env` configuration
- GitHub repositories and CI/CD pipeline
- All cognitive lens processing outputs
- Any future user data or conversation logs

---

## 3. Information Security Objectives

| Objective | Target |
|-----------|--------|
| No credentials committed to version control | Zero incidents |
| CI pipeline passes before any deployment | 100% of releases |
| Azure API keys rotated if suspected compromise | Within 24 hours |
| Security incidents logged and reviewed | 100% of incidents |
| No unauthorized storage of neurodivergent user data | Zero incidents |
| Accessibility review passed on every release | 100% of stories |

---

## 4. Principles

### 4.1 Confidentiality
- All API keys, endpoints, and credentials stored in `.env` files only
- `.env` files excluded from Git via `.gitignore` — never committed to GitHub
- Source code reviewed for hardcoded secrets before any commit
- Heightened protection for any data that could reveal neurodivergent status (GDPR Art. 9)

### 4.2 Integrity
- All changes committed to GitHub with meaningful commit messages
- CI pipeline validates code on every push
- Version history maintained in project log

### 4.3 Availability
- Mock mode (`MOCK_AI=true`) ensures platform remains operational if Azure is unavailable
- System designed for accessibility — must remain usable by neurodivergent users at all times

---

## 5. Asset Classification

| Asset | Classification | Owner |
|-------|---------------|-------|
| Azure OpenAI API key | 🔴 Confidential | Shannon Bryan Kelly |
| Azure endpoint URL | 🔴 Confidential | Shannon Bryan Kelly |
| `.env` file | 🔴 Confidential | Shannon Bryan Kelly |
| Cognitive lens processing logic | 🟡 Internal | Shannon Bryan Kelly |
| Source code (main engine, backend) | 🟡 Internal | Shannon Bryan Kelly |
| GitHub repository (public) | 🟢 Public | Shannon Bryan Kelly |
| SDLC documentation | 🟢 Public | Shannon Bryan Kelly |
| Compliance documentation | 🟢 Public | Shannon Bryan Kelly |

---

## 6. Access Control

| Resource | Access | Authorization |
|----------|--------|---------------|
| GitHub repository | Read: public; Write: owner only | GitHub account control |
| Azure OpenAI resource | Owner only | Azure portal credentials |
| `.env` file | Owner machine only | Local file system |
| REST API endpoints | Localhost only | No authentication yet |

**Note:** Before any multi-user deployment, authentication is mandatory. Any deployment handling neurodivergent user data requires consent management and GDPR Article 9 safeguards.

---

## 7. Acceptable Use

- Platform used for cognitive research, portfolio demonstration, and personal productivity
- No credential sharing with third parties
- No storage of neurodivergent user data without consent and updated DPIA
- All contributors must read and acknowledge this policy before working on the platform

---

## 8. Special Security Controls — Neurodivergent User Data

Because this platform serves neurodivergent users and may process health-related information:

| Control | Requirement |
|---------|-------------|
| GDPR Art. 9 safeguards | Applied to any health/disability data |
| Data minimization | No more data processed than necessary for lens function |
| Storage limitation | No user data stored by default |
| Purpose limitation | Data processed only for cognitive synthesis — not profiling |
| Consent | Explicit consent required before any persistent storage of cognitive data |

---

## 9. Supplier Security

| Supplier | Service | Security Assessment |
|----------|---------|---------------------|
| Microsoft Azure | OpenAI API, Cosmos DB | ISO 27001 certified; SOC 2 Type II; DPA via subscription |
| GitHub (Microsoft) | Version control, CI/CD | ISO 27001 certified; SOC 2 Type II |
| Anthropic | Claude AI (development) | Enterprise privacy terms accepted |

---

## 10. Incident Response

| Step | Action | Timeframe |
|------|--------|-----------|
| 1 | Detect and identify incident | Immediate |
| 2 | Log in INCIDENT_LOG.md | Within 1 hour |
| 3 | Contain — disable live AI if needed | Within 1 hour |
| 4 | If neurodivergent user data involved — assess GDPR breach notification requirement (72-hour rule) | Within 24 hours |
| 5 | Rotate any compromised credentials via Azure portal | Within 24 hours |
| 6 | Review root cause | Within 48 hours |
| 7 | Update controls | Within 1 week |

---

## 11. Business Continuity

- Mock mode fallback ensures cognitive processing remains operational during Azure outages
- GitHub repository serves as full source code backup
- `.env` credentials backed up securely offline by owner
- Accessibility must be maintained even in degraded/mock mode

---

## 12. Compliance

| Regulation / Standard | Applicability |
|----------------------|---------------|
| GDPR (incl. Art. 9 special category) | Applicable — see DPIA.md |
| EU AI Act | Applicable — see AI_POLICY.md and FRIA.md |
| ISO 27001:2022 | Framework adopted — see STATEMENT_OF_APPLICABILITY.md |
| Microsoft Azure DPA | Applicable — accepted via Azure subscription |

---

## 13. Roles and Responsibilities

| Role | Responsibility |
|------|---------------|
| Shannon Bryan Kelly (Data Controller / Architect) | Owns all security decisions, credential management, incident response, accessibility review, policy review |

---

## 14. Policy Review

This policy is reviewed:
- Annually (April each year)
- Following any security or privacy incident
- Before any multi-user deployment or clinical/healthcare context expansion

---

*Template adapted from ICT Institute Information Security Policy Template under Creative Commons Attribution License.*
*Source: https://github.com/swzaken/freetemplates*

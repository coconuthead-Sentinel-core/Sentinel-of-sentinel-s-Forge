# AI Policy
## Sentinel-of-sentinel-s-Forge v5.2.0

**Template source:** ICT Institute — AI Policy Template V1.0 (CC Attribution License)
**Adapted by:** Shannon Bryan Kelly
**Implementation:** Claude AI (Anthropic)
**Effective Date:** April 2026
**Review Date:** April 2027

---

## 1. Purpose and Scope

This policy governs the design, development, operation, and use of artificial intelligence within the **Sentinel-of-sentinel-s-Forge** platform. It applies to:

- Shannon Bryan Kelly (Architect / Owner)
- Any contractors, consultants, or contributors working on the platform
- Any end users interacting with the cognitive processing system

---

## 2. What Sentinel-of-sentinel-s-Forge Is

Sentinel-of-sentinel-s-Forge is an AI-powered **neurodivergent cognitive processing platform**. It processes user inputs through four specialized cognitive lenses powered by **Azure OpenAI**:

| Lens | Processing Style |
|------|-----------------|
| ADHD | Rapid burst processing, dynamic context-switching |
| Autism | Precision pattern recognition, systematic analysis |
| Dyslexia | Multi-dimensional spatial interpretation, symbol reasoning |
| Neurotypical | Standard baseline linear processing |

The system is specifically designed to support neurodivergent users and researchers. It processes text and emoji/glyph sequences and maps outputs to a three-zone memory system (GREEN / YELLOW / RED).

---

## 3. Special Considerations — Neurodivergent Users

This platform is designed **for and with** neurodivergent users. The following principles apply above and beyond standard AI policy:

- **Dignity:** All cognitive lens outputs must preserve the dignity of neurodivergent individuals
- **No pathologizing:** ADHD, Autism, and Dyslexia lenses represent cognitive strengths — not deficits
- **Accessibility-first:** UI must remain usable by users with ADHD, dyslexia, and screen reader needs
- **No harm:** The system must not produce outputs that stigmatize or demean neurodivergent cognition
- **Informed use:** Users must be aware they are interacting with an AI system modeled on cognitive styles — not receiving clinical assessment

---

## 4. Acceptable Use Principles

### ✅ Acceptable Use
- Cognitive exploration and self-understanding support
- Research into neurodivergent cognitive styles
- Creative ideation and concept mapping
- Educational demonstrations
- Personal productivity and knowledge organization

### ❌ Unacceptable Use
- Clinical diagnosis or medical advice — this platform is NOT a diagnostic tool
- Producing content that stereotypes, demeans, or discriminates against neurodivergent individuals
- Processing sensitive health or disability data without explicit consent and DPIA review
- Using cognitive lens outputs to make employment, educational, or legal decisions about individuals
- Impersonating or misrepresenting neurodivergent experiences without appropriate context

---

## 5. AI Act Compliance

### Risk Classification
Under the EU AI Act, Sentinel-of-sentinel-s-Forge requires careful classification due to its neurodivergent-focused design.

**Current Classification: Limited-Risk / General-Purpose AI**

**Rationale:**
- The system does not make medical or diagnostic determinations
- Lens outputs are clearly framed as cognitive processing styles, not clinical assessments
- No consequential decisions about individuals are automated

**Important Boundary:** If the platform is ever used to:
- Assess individuals for employment or education suitability
- Provide clinical recommendations
- Be deployed in healthcare contexts

...it would be reclassified as **High-Risk AI** under Annex III and require full conformity assessment.

### Obligations
- **Transparency:** Users are clearly informed they interact with AI cognitive models — not licensed clinicians
- **Human oversight:** All outputs are exploratory — no clinical or legal weight
- **Non-discrimination:** Lens design must not produce outputs that demean any cognitive style
- **Documentation:** This policy and the FRIA serve as primary AI governance documentation

---

## 6. Privacy and GDPR Compliance

- **No personal data is collected** by default — no login or registration required
- User prompts processed in memory only — not stored persistently unless Cosmos DB is enabled
- If a user enters health or disability information in a prompt, that data is processed by Azure OpenAI under Microsoft's data processing terms
- **Heightened sensitivity:** Neurodivergent status may constitute **special category data** under GDPR Article 9 — additional protections apply if stored
- Users must not enter identifiable health information into prompts
- Full DPIA review required before any persistent storage of user interaction data

---

## 7. Approved AI Services

| Service | Provider | Purpose | Status |
|---------|----------|---------|--------|
| Azure OpenAI (GPT-5.4-nano) | Microsoft | Core cognitive responses | ✅ Approved |
| Claude AI (Anthropic) | Anthropic | Development assistance | ✅ Approved |
| GitHub Copilot | Microsoft/GitHub | Code assistance | ✅ Approved (no proprietary code) |
| ChatGPT (OpenAI) | OpenAI | Research only | ⚠️ Approved — no confidential/health data |
| Gemini | Google | Research only | ⚠️ Approved — no confidential/health data |

**Critical Rule:** No user health information, disability disclosures, or personal data may be entered into public AI tools.

---

## 8. Transparency Requirements

- All responses are clearly identified as AI-generated cognitive processing
- The active cognitive lens is always displayed to the user
- Mock mode vs. live AI mode is declared in system status
- The system does not claim to provide clinical, medical, or therapeutic services

---

## 9. Security and Confidentiality

- Azure API keys stored in `.env` — never committed to GitHub
- `.gitignore` excludes all `.env` files
- Future multi-user deployment requires full authentication and consent management review
- Any storage of neurodivergent user data requires elevated security controls per GDPR Article 9

---

## 10. Incident Reporting

If an AI output stigmatizes neurodivergent cognition, causes harm, or behaves unexpectedly:
1. Document the prompt and output immediately
2. Log in `docs/compliance/INCIDENT_LOG.md`
3. Disable live AI (`MOCK_AI=true`) if needed
4. Mandatory review before re-enabling

---

## 11. Policy Review

This policy is reviewed annually or when:
- A new AI service or cognitive lens is added
- EU AI Act implementing rules are updated
- Platform is deployed to healthcare, education, or employment contexts
- A significant incident occurs

---

*Template adapted from ICT Institute AI Policy Template V1.0 under Creative Commons Attribution License.*
*Source: https://github.com/swzaken/freetemplates*

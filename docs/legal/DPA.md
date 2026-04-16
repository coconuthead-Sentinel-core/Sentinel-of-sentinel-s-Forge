# Data Processing Agreement (DPA)
## The Forge Trilogy â€” [YOUR LLC NAME]

**GDPR Article 28 â€” Controller-to-Processor Agreement**
**Template Source:** Adapted from Common Paper DPA Standard (CC Attribution)
**Version:** 1.0

> Required for any customer in the EU/UK, and best practice for all B2B customers.

---

## PARTIES

| Role | Party | Details |
|------|-------|---------|
| **Data Controller** | Customer | The entity using the Forge Trilogy platforms |
| **Data Processor** | [YOUR LLC NAME] | Shannon Bryan Kelly, [YOUR TEXAS ADDRESS], Texas, USA |

---

## 1. Definitions

| Term | Meaning |
|------|---------|
| **Personal Data** | Any information relating to an identified or identifiable natural person submitted to the Services |
| **Processing** | Any operation performed on Personal Data (collection, storage, transmission, analysis) |
| **Sub-processor** | A third party engaged by Processor to process Personal Data on Controller's behalf |
| **Data Breach** | A confirmed breach of security leading to unauthorized access, disclosure, or loss of Personal Data |
| **GDPR** | EU General Data Protection Regulation 2016/679 |
| **Services** | The Forge Trilogy platforms as defined in the associated SaaS Agreement |

---

## 2. Scope of Processing

### 2.1 Subject Matter
Processor will process Personal Data submitted by Controller through the Services for the purpose of delivering AI cognitive processing outputs.

### 2.2 Nature of Processing
| Activity | Description |
|----------|-------------|
| Transit processing | Personal Data transmitted through API endpoints for AI response generation |
| Temporary storage | Session-only storage in memory during processing |
| Persistent storage | Notes/conversation history if Controller enables Cosmos DB feature |

### 2.3 Types of Personal Data
Depending on Controller's use:
- Text prompts (may contain names, descriptions of persons, contact details)
- Voice transcripts (Sentinel-of-sentinel-s-Forge â€” session only, browser-side)
- User account data (name, email, organization)
- API usage logs (IP address, timestamps, endpoint)

### 2.4 Categories of Data Subjects
- Controller's employees, contractors, or agents using the Services
- Third parties whose information Controller submits via API
- End users of Controller's applications built on the Services

### 2.5 Duration
Processing continues for the duration of the SaaS Agreement. Upon termination, Processor deletes Personal Data within 30 days of Controller's written request.

---

## 3. Processor Obligations

### 3.1 Instructions
Processor shall process Personal Data only on Controller's documented instructions. The SaaS Agreement and this DPA constitute the primary documented instructions.

### 3.2 Confidentiality
Processor ensures that persons authorized to process Personal Data are subject to confidentiality obligations.

### 3.3 Security Measures
Processor implements appropriate technical and organizational measures (TOMs) including:

| Measure | Implementation |
|---------|---------------|
| Encryption in transit | TLS 1.2+ for all API communications |
| Encryption at rest | AES-256 (Azure Cosmos DB) |
| Access control | API key authentication; role-based access |
| Credential management | No hardcoded secrets; `.env` file excluded from version control |
| Incident monitoring | Azure security monitoring; application error logging |
| Staff access | Owner-only access to production credentials |

### 3.4 Sub-processors
Controller provides general authorization for Processor to engage sub-processors. Current approved sub-processors:

| Sub-processor | Role | Location | Safeguard |
|--------------|------|----------|-----------|
| **Microsoft Azure** | AI inference (OpenAI o4-mini), Cosmos DB storage, hosting | USA / EU | Microsoft DPA; EU SCCs |
| **Stripe** | Payment processing (billing data only) | USA | Stripe DPA; EU SCCs |
| **GitHub** (Microsoft) | Source code hosting (no customer data) | USA | GitHub DPA |

Processor will notify Controller at least 30 days before adding a new sub-processor that processes Personal Data. Controller may object within 14 days; if unresolved, Controller may terminate the Agreement.

### 3.5 Data Subject Rights Assistance
Processor will provide Controller with reasonable assistance in responding to data subject rights requests (access, erasure, portability, restriction) within 30 days of Controller's request.

### 3.6 DPIA Assistance
Processor will provide reasonable assistance if Controller is required to conduct a Data Protection Impact Assessment (DPIA) related to the Services. Processor's own DPIAs are maintained per platform in `docs/compliance/DPIA.md`.

### 3.7 Breach Notification
Processor will notify Controller without undue delay â€” and in any event within **72 hours** â€” of becoming aware of a Personal Data Breach affecting Customer Data. Notification will include:
- Nature of the breach (if known)
- Categories and approximate number of data subjects affected
- Likely consequences of the breach
- Measures taken or proposed to address the breach

### 3.8 Audit Rights
Upon Controller's written request (no more than once per year), Processor will provide documentation confirming compliance with this DPA, or permit an audit by a mutually agreed third-party auditor subject to a confidentiality agreement.

### 3.9 Deletion or Return
Upon termination of the SaaS Agreement, Processor will (at Controller's election):
- Delete all Personal Data and certify deletion in writing; or
- Return a machine-readable export of Controller Data within 30 days

Processor may retain data required by law, in which case access is restricted to legally required purposes.

---

## 4. Controller Obligations

Controller warrants that:
- It has a valid legal basis for processing the Personal Data it submits
- It has provided required notices to data subjects
- It will provide Processor only with Personal Data that is necessary for the Services
- It complies with all applicable data protection laws

---

## 5. International Data Transfers

Processor transfers Personal Data to Microsoft Azure (USA) under Standard Contractual Clauses (EU Commission Decision 2021/914, Module 3 â€” Processor to Sub-processor). Copies of applicable SCCs available upon request.

---

## 6. Governing Law

This DPA is governed by the laws of the **State of Texas, United States**, without prejudice to GDPR requirements applicable to EU Personal Data.

---

## 7. Order of Precedence

In case of conflict, the order of precedence is:
1. This DPA (for data processing matters)
2. The SaaS Agreement (for commercial matters)
3. The Privacy Policy
4. The Terms of Service

---

## 8. Signatures

| Data Controller (Customer) | Data Processor ([YOUR LLC NAME]) |
|---------------------------|----------------------------------|
| Signed: _________________________ | Signed: _________________________ |
| Name: _________________________ | Name: Shannon Bryan Kelly |
| Title: _________________________ | Title: Founder & Architect |
| Date: _________________________ | Date: _________________________ |
| Email: _________________________ | Email: [YOUR EMAIL] |

---

*Adapted from Common Paper DPA Standard v1.0 (CC Attribution)*
*Source: https://commonpaper.com/standards/data-processing-agreement/*


# Cloud / SaaS Service Agreement
## The Forge Trilogy â€” [YOUR LLC NAME]

**Agreement Type:** Standard B2B Cloud Service Agreement
**Template Source:** Adapted from Common Paper Cloud Service Agreement (CC Attribution)
**Effective:** Upon countersignature or electronic acceptance
**Version:** 1.0

> **For B2B / Enterprise customers.** Individual/consumer customers are covered by the Terms of Service.
> Fill in `[YOUR LLC NAME]`, `[YOUR EMAIL]`, `[YOUR TEXAS ADDRESS]` before use.

---

## PARTIES

| Party | Information |
|-------|------------|
| **Provider** | [YOUR LLC NAME], operated by Shannon Bryan Kelly, [YOUR TEXAS ADDRESS], Texas, United States |
| **Customer** | [CUSTOMER LEGAL NAME], [CUSTOMER ADDRESS] |

---

## 1. Services

### 1.1 Platforms Covered

Provider will make available the following platforms ("Services") as selected in the Order Form:

| Platform | Base URL | Primary Feature |
|----------|----------|----------------|
| Sentinel-of-sentinel-s-Forge | TBD (hosted) | Multi-agent AI orchestration |
| Sentinel-of-sentinel-s-Forge | TBD (hosted) | Neurodivergent cognitive AI |
| Sentinel-of-sentinel-s-Forge | TBD (hosted) | Self-optimizing cognitive AI OS |

### 1.2 Service Scope

Services include:
- REST API access per subscription tier
- WebSocket real-time event streaming (Sentinel, Sentinel-of-sentinel-s-Forge)
- AI processing via Azure OpenAI o4-mini model
- Dashboard access
- Cognitive lens processing (ADHD, Autism, Dyslexia, Dyscalculia, Neurotypical modes)
- Standard email support

Services do **not** include:
- On-premise deployment
- Custom model fine-tuning
- Guaranteed AI response accuracy
- Professional consulting services (available separately)

### 1.3 API Specifications

API documentation is maintained at:
- Sentinel-of-sentinel-s-Forge: `docs/sdlc/API_CONTRACTS.md`
- Sentinel-of-sentinel-s-Forge: `docs/sdlc/API_CONTRACTS.md`
- Sentinel-of-sentinel-s-Forge: `docs/sdlc/API_CONTRACTS.md`

Current API version: defined per platform in respective documentation.

---

## 2. Order Form

To be completed per agreement:

| Field | Value |
|-------|-------|
| Customer | [CUSTOMER NAME] |
| Service(s) Selected | [QNF / Sentinel / Sovereign / All Three] |
| Subscription Tier | [Starter / Pro / Enterprise] |
| Monthly Fee | $[AMOUNT] |
| Start Date | [DATE] |
| Initial Term | 12 months (or Month-to-Month) |
| API Call Limit/Month | [NUMBER] |
| SLA Tier | [None / Pro / Enterprise] |
| Renewal | Auto-renews unless cancelled 30 days before term end |

---

## 3. Payment Terms

### 3.1 Fees
Customer shall pay Provider the fees specified in the Order Form.

### 3.2 Billing
- Monthly subscriptions: billed monthly in advance on the subscription anniversary date
- Annual subscriptions: billed annually in advance
- All fees in USD

### 3.3 Payment Method
Payment via Stripe (credit card, ACH, or wire transfer for Enterprise). Invoices issued within 2 business days of each billing date. Payment due within **Net 30** of invoice date.

### 3.4 Late Payment
Invoices unpaid after 30 days accrue interest at 1.5% per month (18% annual) or the maximum permitted by Texas law, whichever is less. Provider may suspend Service access after 45 days of non-payment with 5 business days' written notice.

### 3.5 Taxes
Customer is responsible for all applicable taxes (sales tax, VAT, GST) except for taxes on Provider's net income. Provider will collect Texas sales tax as required by the Texas Comptroller.

---

## 4. API Usage and Rate Limits

### 4.1 API Limits
Customer's API usage is limited to the tier specified in the Order Form.

### 4.2 Overage
| Tier | Overage Handling |
|------|-----------------|
| Starter | API calls blocked after limit; upgrade to continue |
| Pro | API calls blocked after limit; upgrade or purchase add-on credits |
| Enterprise | Custom overage rate per Order Form |

### 4.3 Rate Limiting
Provider may apply per-minute and per-day rate limits to maintain service quality for all customers. Current limits are documented in the API Contracts.

---

## 5. Uptime and SLA

### 5.1 Uptime Commitment

| Tier | Monthly Uptime Target | Credit for Breach |
|------|----------------------|-------------------|
| Starter | Best effort | None |
| Pro | 99.0% | 10% of monthly fee per 1% below target |
| Enterprise | 99.5% | 15% of monthly fee per 1% below target, up to 50% of monthly fee |

### 5.2 Measurement
Uptime is measured monthly, excluding:
- Scheduled maintenance (notified 24 hours in advance)
- Force majeure events
- Customer-caused failures
- Azure OpenAI or third-party outages beyond Provider's control

### 5.3 SLA Credits
Credits are applied to the next invoice. Credits do not accumulate as cash refunds.

### 5.4 Maintenance
Provider will schedule maintenance during off-peak hours (Sunday 02:00â€“06:00 CT) where possible. Emergency maintenance may occur without advance notice.

---

## 6. Data and Privacy

### 6.1 Customer Data
Customer retains ownership of all data submitted to the Services ("Customer Data"). Provider processes Customer Data solely to deliver the Services.

### 6.2 Provider's Data Processing
Provider processes Customer Data on Azure infrastructure (Microsoft). Azure does not use customer data for model training. Transfers are protected by Standard Contractual Clauses.

### 6.3 Data Processing Agreement
For GDPR Article 28 compliance, a separate Data Processing Agreement ("DPA") is required. Provider's standard DPA is available at `docs/legal/DPA.md`. Enterprise customers may negotiate a custom DPA.

### 6.4 Data Retention
Customer Data is retained per the Privacy Policy. Upon contract termination, Provider will delete Customer Data within 30 days upon written request.

### 6.5 Security
Provider implements the security controls documented in `docs/compliance/INFORMATION_SECURITY_POLICY.md`, including:
- TLS 1.2+ encryption in transit
- AES-256 encryption at rest (Azure Cosmos DB)
- API key authentication
- Access control and audit logging

### 6.6 Breach Notification
Provider will notify Customer within 72 hours of discovering a confirmed data breach affecting Customer Data, per GDPR Article 33 requirements.

---

## 7. Intellectual Property

### 7.1 Provider IP
Provider retains all intellectual property rights in the Platforms, AI architecture, cognitive frameworks, and documentation. Customer's subscription grants a limited, non-exclusive, non-transferable license to access and use the Services.

### 7.2 Customer IP
Customer retains all intellectual property rights in Customer Data. AI-generated outputs derived from Customer Data are owned by Customer, subject to applicable law.

### 7.3 Feedback
If Customer provides feedback on the Services, Customer grants Provider a royalty-free license to use such feedback to improve the Services.

---

## 8. Confidentiality

### 8.1 Definition
"Confidential Information" means any non-public information disclosed by one party to the other that is designated as confidential or should reasonably be understood to be confidential.

### 8.2 Obligations
Each party will: (a) keep Confidential Information strictly confidential; (b) not disclose to third parties without prior written consent; (c) use only for the purposes of this Agreement.

### 8.3 Exceptions
Confidentiality obligations do not apply to information that is: (a) publicly known; (b) independently developed; (c) received from a third party without restriction; (d) required to be disclosed by law (with reasonable notice to allow the other party to seek a protective order).

---

## 9. Warranties and Disclaimers

### 9.1 Provider Warranties
Provider warrants that:
- The Services will perform materially as described in the documentation during the subscription term
- Provider has the right to enter this Agreement and grant the licenses herein
- Provider will maintain industry-standard security controls

### 9.2 Disclaimers
**THE SERVICES ARE PROVIDED "AS IS" WITH RESPECT TO AI OUTPUT ACCURACY. PROVIDER DOES NOT WARRANT THAT AI-GENERATED OUTPUTS ARE ACCURATE, COMPLETE, OR FIT FOR ANY PARTICULAR PURPOSE. AI OUTPUTS SHOULD BE VALIDATED BEFORE USE IN CRITICAL APPLICATIONS.**

Provider does not warrant that the Services will be error-free or uninterrupted beyond the SLA commitments above.

---

## 10. Limitation of Liability

### 10.1 Mutual Limitation
NEITHER PARTY SHALL BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING LOST PROFITS OR LOST DATA, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

### 10.2 Cap
EACH PARTY'S TOTAL LIABILITY UNDER THIS AGREEMENT SHALL NOT EXCEED THE GREATER OF: (A) THE TOTAL FEES PAID BY CUSTOMER TO PROVIDER IN THE 12 MONTHS PRECEDING THE CLAIM, OR (B) $10,000.

### 10.3 Exceptions
The limitation above does not apply to: (a) indemnification obligations; (b) either party's confidentiality obligations; (c) Customer's payment obligations; (d) damages caused by willful misconduct.

---

## 11. Indemnification

### 11.1 Provider Indemnification
Provider will defend, indemnify, and hold harmless Customer from third-party claims that the Services infringe a third party's intellectual property rights, provided Customer (a) notifies Provider promptly, (b) gives Provider control of the defense, and (c) cooperates with Provider.

### 11.2 Customer Indemnification
Customer will defend, indemnify, and hold harmless Provider from third-party claims arising from Customer's: (a) use of Services in violation of these Terms; (b) Customer Data; (c) violation of applicable law.

---

## 12. Term and Termination

### 12.1 Term
This Agreement begins on the Start Date and continues for the Initial Term specified in the Order Form, then auto-renews monthly/annually unless cancelled.

### 12.2 Cancellation
Either party may cancel renewal with 30 days' written notice before the renewal date. No early termination fee for month-to-month. Annual plans: see Order Form for early termination terms.

### 12.3 Termination for Cause
Either party may terminate immediately if the other party: (a) materially breaches this Agreement and fails to cure within 30 days of written notice; (b) becomes insolvent or files for bankruptcy.

### 12.4 Effect of Termination
Upon termination: (a) Customer's API access is revoked; (b) Customer Data is deleted within 30 days upon written request; (c) all unpaid fees become immediately due.

---

## 13. General

### 13.1 Governing Law
This Agreement is governed by the laws of the **State of Texas, United States**.

### 13.2 Disputes
Disputes shall be resolved first by good-faith negotiation (30 days), then by binding arbitration in Texas under AAA Commercial Arbitration Rules.

### 13.3 Entire Agreement
This Agreement, the Order Form, Privacy Policy, DPA (if executed), and SLA constitute the entire agreement and supersede all prior negotiations.

### 13.4 Amendments
Amendments must be in writing and signed by both parties.

### 13.5 Force Majeure
Neither party is liable for delays caused by events beyond their reasonable control, including natural disasters, pandemic, cyber-attacks, government actions, or third-party service outages.

---

## 14. Signatures

| Provider | Customer |
|---------|---------|
| **[YOUR LLC NAME]** | **[CUSTOMER LEGAL NAME]** |
| Signed: _________________________ | Signed: _________________________ |
| Name: Shannon Bryan Kelly | Name: _________________________ |
| Title: Founder & Architect | Title: _________________________ |
| Date: _________________________ | Date: _________________________ |
| Email: [YOUR EMAIL] | Email: _________________________ |

---

*Adapted from Common Paper Cloud Service Agreement Standard v2.0 (CC Attribution)*
*Source: https://commonpaper.com/standards/cloud-service-agreement/*


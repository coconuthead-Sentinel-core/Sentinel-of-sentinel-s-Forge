# Commercial Launch & Payments Compliance Checklist
## The Forge Trilogy — Shannon Bryan Kelly

**Date:** April 2026
**Jurisdiction:** State of Texas, United States
**Business Model:** SaaS / AI Platform (subscription + API access)

---

## Status Legend
- 🔴 **REQUIRED BEFORE FIRST PAYMENT** — Cannot legally take money without this
- 🟡 **REQUIRED WITHIN 90 DAYS** — Legally required but grace period applies
- 🟢 **STRONGLY RECOMMENDED** — Enterprise/B2B expected; builds credibility
- ✅ **COMPLETE** — Already done

---

## BUNDLE 1 — Business Formation & Tax Packet

### Step 1: Choose and reserve your LLC name 🔴

**What:** Decide the official legal entity name. Must be unique in Texas.
**Options:**
- "Forge Trilogy LLC" (covers all three platforms under one entity)
- "Shannon Bryan Kelly AI LLC"
- "Cognitive Forge Labs LLC"

**Action:** Search the Texas SoS name database before filing:
- URL: https://www.sos.state.tx.us/corp/sosda/index.shtml
- Name must include "LLC", "L.L.C.", "Limited Liability Company", or equivalent

---

### Step 2: File Texas LLC — Form 205 🔴

**What:** Certificate of Formation — Limited Liability Company
**Form:** Form 205 (Chapter 101, Texas Business Organizations Code)
**Fee:** $300 (one-time filing fee)
**Where:** Texas Secretary of State — SOSDirect online portal
- URL: https://www.sos.state.tx.us/corp/forms/205_boc.pdf
- Online filing: https://direct.sos.state.tx.us/

**What you need to file:**
- [ ] LLC name (must be available)
- [ ] Registered Agent name and Texas street address (can be you, can't be a P.O. Box)
- [ ] Organizer name and address (you — Shannon Bryan Kelly)
- [ ] Purpose statement ("AI software platform services")
- [ ] Member-managed or manager-managed structure
- [ ] Payment of $300 filing fee

**Processing time:** 3–5 business days (expedited: same day for extra fee)

**After filing, you will receive:**
- Certificate of Formation (keep permanently — you'll need it for bank accounts and Stripe)

---

### Step 3: Get your EIN from the IRS 🔴

**What:** Employer Identification Number — your LLC's federal tax ID
**Cost:** FREE
**Where:** IRS online EIN application (instant)
- URL: https://www.irs.gov/businesses/small-businesses-self-employed/get-an-employer-identification-number
- Form: SS-4 (online application takes 10 minutes, EIN issued immediately)

**What you need:**
- [ ] Responsible party name: Shannon Bryan Kelly
- [ ] Your Social Security Number (SSN) — not stored by IRS after issuance
- [ ] LLC name (must match SoS filing exactly)
- [ ] Business address in Texas
- [ ] Entity type: LLC
- [ ] Number of members: 1 (single-member LLC)

**After EIN:**
- You'll receive a CP575 letter (keep permanently)
- Use EIN for all tax filings, bank accounts, and Stripe

---

### Step 4: Texas Comptroller — Sales Tax Permit 🔴

**What:** Required if you sell taxable services/software in Texas
**Cost:** FREE
**Where:** Texas Comptroller Online Tax Registration
- URL: https://comptroller.texas.gov/taxes/permit/

**Texas SaaS Tax Note:** Texas taxes "data processing services" — which includes cloud-based AI processing. A Texas sales tax permit is required if you have Texas customers.

**What you need:**
- [ ] EIN (from Step 3)
- [ ] LLC name
- [ ] Texas business address
- [ ] Description of services offered

---

### Step 5: Open a Business Bank Account 🔴

**What:** Separate business checking account (required for LLC integrity and Stripe)
**Requirements:**
- [ ] Certificate of Formation (from Step 2)
- [ ] EIN letter (from Step 3)
- [ ] Two forms of ID (driver's license + one other)
- [ ] Initial deposit (varies by bank — often $25–$100)

**Recommended:** Chase Business Complete Checking, Bank of America Business Advantage, or local Texas credit union (often lower fees)

---

## BUNDLE 2 — Payments / Merchant Onboarding Packet

### Step 6: Stripe Business Account Setup 🔴

**What:** Payment processor KYC/KYB verification — must complete before charging customers
**Where:** https://stripe.com/

**Stripe requires (KYB — Know Your Business):**
- [ ] Legal business name (LLC name, must match SoS filing)
- [ ] Business type: LLC / Software & Technology
- [ ] EIN
- [ ] Business address (Texas)
- [ ] Business phone number
- [ ] Business website URL (must be live and include Terms, Privacy Policy, Refund Policy)
- [ ] Business description ("AI SaaS platform — cognitive processing and AI orchestration")
- [ ] Beneficial owner info: Shannon Bryan Kelly (name, address, DOB, SSN last 4)
- [ ] Government-issued ID photo (driver's license or passport)
- [ ] Bank account (routing + account number for payouts)
- [ ] Business bank statement (sometimes requested)

**Stripe payout schedule:** 2 business days after first payment (standard)

---

### Step 7: Publish Legal Pages Before Enabling Payments 🔴

Stripe **requires** these to be publicly accessible before they will enable your account:
- [ ] Privacy Policy — URL must be live
- [ ] Terms of Service — URL must be live
- [ ] Refund / Cancellation Policy — URL must be live
- [ ] Contact information — must be visible on website

**Status:** These documents are drafted (see `docs/legal/` folder) — needs deployment.

---

## BUNDLE 3 — Customer-Facing Legal Policies Packet

All documents drafted and saved to `docs/legal/`:

| Document | File | Status |
|----------|------|--------|
| Privacy Policy | `PRIVACY_POLICY.md` + `privacy.html` | ✅ Drafted — needs your address/email filled in |
| Terms of Service | `TERMS_OF_SERVICE.md` + `terms.html` | ✅ Drafted — needs your address/email/pricing filled in |
| Refund & Cancellation Policy | `REFUND_CANCELLATION_POLICY.md` | ✅ Drafted |
| SaaS/Cloud Service Agreement | `SAAS_AGREEMENT.md` | ✅ Drafted |
| Data Processing Agreement | `DPA.md` | ✅ Drafted |
| Service Level Agreement | `SLA.md` | ✅ Drafted |

**What you need to fill in:**
- `[YOUR LLC NAME]` — your Texas LLC name
- `[YOUR EMAIL]` — one real email (e.g., legal@yourllcname.com or your personal email)
- `[YOUR TEXAS ADDRESS]` — registered agent address or home address
- `[PRICING TIERS]` — decide: free tier? $X/month subscription? per-API-call?

---

## BUNDLE 4 — Commercial Contract / Enterprise Packet

| Document | File | Status |
|----------|------|--------|
| Cloud/SaaS Service Agreement | `SAAS_AGREEMENT.md` | ✅ Drafted |
| Data Processing Agreement (DPA) | `DPA.md` | ✅ Drafted |
| Service Level Agreement (SLA) | `SLA.md` | ✅ Drafted |

These are needed when you sell B2B / enterprise. Present these when a company asks "what are your terms?"

---

## BUNDLE 5 — Compliance & Operations Packet

Already complete across all three platforms:

| Document | Status |
|----------|--------|
| SDLC Documentation Suite (PRD, System Design, API Contracts, Backlog, Test Strategy) | ✅ Complete — all 3 platforms |
| GDPR DPIA | ✅ Complete — all 3 platforms |
| ISO 27001 Statement of Applicability | ✅ Complete — all 3 platforms |
| ISO 27001 Asset & Risk Register | ✅ Complete — all 3 platforms |
| Information Security Policy | ✅ Complete — all 3 platforms |
| AI Act FRIA | ✅ Complete — all 3 platforms |
| GDPR Processing Activities Register | ✅ Complete — all 3 platforms |
| Incident Log | ✅ Complete — all 3 platforms |

---

## Minimum "Ready to Accept First Payment" Checklist

Before sending your first invoice or enabling Stripe:

- [ ] **1.** Texas LLC filed and Certificate of Formation received
- [ ] **2.** EIN obtained from IRS
- [ ] **3.** Business bank account opened
- [ ] **4.** Legal policy pages live on website (Privacy, Terms, Refund)
- [ ] **5.** Stripe KYB verification complete
- [ ] **6.** Pricing decided and published
- [ ] **7.** Contact email live and monitored

**Estimated total cost to launch:**
- Texas LLC filing: $300
- EIN: $0 (free)
- Texas sales tax permit: $0 (free)
- Business bank account: $0–$100 (first deposit)
- Stripe: $0 (2.9% + $0.30 per transaction — no monthly fee)
- **Total fixed cost: ~$300**

---

## Pricing Model Recommendation

For SaaS AI platforms at your stage:

| Tier | Price | What's Included | Recommended For |
|------|-------|-----------------|-----------------|
| Developer (Free) | $0 | Limited API calls (e.g., 100/month), mock mode only | Portfolio demos, GitHub visitors |
| Starter | $29/month | 1,000 API calls, live Azure AI, all cognitive lenses | Individuals, small teams |
| Pro | $99/month | 10,000 API calls, priority support, SLA | Small businesses, researchers |
| Enterprise | Custom | Unlimited, DPA, SLA, dedicated support | B2B, enterprise contracts |

**Stripe product to use:** Stripe Billing (subscriptions) — integrates with FastAPI via webhook

---

*This checklist covers the Forge Trilogy: Quantum Nexus Forge, Sentinel-of-sentinel-s-Forge, Sovereign Forge.*
*All three platforms operate under one LLC. Separate Stripe products can be created per platform under one account.*

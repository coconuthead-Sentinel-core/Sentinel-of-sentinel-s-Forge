# Product Requirements Document (PRD)
## Sentinel-of-sentinel-s-Forge v5.2.0

**Architect:** Shannon Bryan Kelly
**Implementation:** Claude AI (Anthropic)
**Date:** November 2025 — April 2026
**Status:** Production

---

## 1. Purpose

Sentinel-of-sentinel-s-Forge is a neurodivergent-aware cognitive AI orchestration platform. It processes information through specialized cognitive lenses designed for ADHD, autism, dyslexia, and neurotypical thinking patterns — making AI accessible to all cognitive styles instead of assuming everyone thinks the same way.

---

## 2. Users

| User Type | Description |
|-----------|-------------|
| **Primary — Shannon Bryan Kelly** | Architect and operator. Neurodivergent thinker building AI that reflects his own cognitive architecture |
| **Secondary — Neurodivergent users** | People with ADHD, autism, dyslexia who benefit from AI adapted to their thinking style |
| **Tertiary — Enterprise teams** | Organizations with cognitively diverse teams who need AI tools that adapt |
| **Quaternary — Researchers** | Cognitive science researchers studying computational models of diverse thinking |

---

## 3. Problem Statement

Most AI tools are built around a single model of thinking — linear, neurotypical, text-first. This creates accessibility barriers for neurodivergent users who process information differently. Shannon Bryan Kelly, a neurodivergent architect (ADHD, dyslexia, dysgraphia), built this platform to prove that AI can be designed inclusively from the ground up — adapting to how the user thinks, not the other way around.

---

## 4. Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Cognitive lenses implemented | 5 | 5 ✅ (ADHD, Autism, Dyslexia, Dyscalculia, Neurotypical) |
| Three-zone memory system | Active | Active ✅ |
| Glyph processing engine | Active | Active ✅ |
| Evaluation score (Relevance) | ≥ 3.8 / 5.0 | **3.97** ✅ |
| Evaluation score (Coherence) | ≥ 3.8 / 5.0 | **3.94** ✅ |
| Evaluation score (Groundedness) | ≥ 3.8 / 5.0 | **3.96** ✅ |
| Evaluation score (Overall) | ≥ 3.9 / 5.0 | **3.96** ✅ |
| Evaluation prompts | 80 queries | 80 ✅ (20 per lens) |
| CI pipeline passing | Yes | Yes ✅ |
| Azure OpenAI o4-mini connected | Yes | Yes ✅ (sbryank1234-7203-resource) |
| Unit tests passing | Yes | Yes ✅ (14 tests) |
| API endpoints (REST) | ≥ 10 | 40+ ✅ |
| Cognitive orchestration latency | < 2,000ms | avg 91.4ms ✅ |

---

## 5. Non-Goals (Out of Scope — Current Version)

- This version does NOT include voice interface (planned)
- This version does NOT include mobile application (planned)
- This version does NOT include community lens contributions (future)
- This version does NOT include enterprise multi-tenant deployment (future)
- This version does NOT include research partnership integrations (future)

---

## 6. Constraints

| Constraint | Detail |
|------------|--------|
| **Runtime** | Python 3.11+ required |
| **AI Model** | Azure OpenAI o4-mini — `sbryank1234-7203-resource` — API version 2025-01-01-preview |
| **Architecture** | FastAPI backend (`backend/`) + 5 cognitive lens services + 3 AI sub-protocols (EventMind, Onset, VoidLogic) |
| **Memory** | Three-zone in-memory system (resets on restart) |
| **Platform** | Windows and Chromebook compatible |
| **Accessibility** | Must remain accessible to non-technical users |

---

## 7. Core User Stories

- As a user with ADHD, I can process information through rapid context-switching bursts
- As a user with autism, I can use precision pattern recognition for detail-focused analysis
- As a user with dyslexia, I can use multi-dimensional symbol interpretation
- As a developer, I can run the platform with one command
- As a reviewer, I can read the README and understand the full system in under 5 minutes
- As an AI system, I can call the API and receive cognitively-adapted responses

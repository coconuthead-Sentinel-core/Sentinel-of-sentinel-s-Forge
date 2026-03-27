# NISCOB-001 — Neurodivergent-Inclusive Structured Cognitive Operations Blueprint

## Purpose
Design patterns and UX principles ensuring Sentinel Forge is accessible and effective for neurodivergent users — particularly those with ADHD, autism, and executive function differences.

## Core Principles
1. **Mode Switching**: Two distinct modes (Conversation / Work) — users aren't forced to context-switch between UI paradigms
2. **Minimal Cognitive Load**: Each page does one thing well
3. **Visual Hierarchy**: Clear headings, status indicators (health dots), progress feedback
4. **Interruption Tolerance**: Session persistence (SESSION-WRAP) so users can leave and return
5. **Structured Input**: Tag-based notes, form validation with clear feedback
6. **Quick Actions**: Dashboard cards for immediate navigation to common tasks

## Integration Points in Existing Code

### ChatPage (Conversation Mode)
- Single-purpose: talk to the AI
- Auto-scroll keeps focus on latest message
- Typing indicator provides processing feedback
- Clear visual distinction between user/assistant messages

### DashboardPage (Work Mode Hub)
- Quick-action cards: 4 primary actions, no decision fatigue
- System health at a glance (color-coded dot)
- KV-grid layout: scannable, not overwhelming

### CognitionPage (Structured Processing)
- Form with clear labels and placeholders
- Processing time shown after completion
- Results displayed in structured format

### NotesPage (External Memory Aid)
- Tag-based organization (externalized categorization)
- Filter pills for quick narrowing
- "Create your first note" empty-state guidance

### InsightsPage (Pattern Recognition Aid)
- Aggregated view of memory, rules, threads
- Usage percentage helps gauge system capacity
- AI suggestions surfaced automatically

## Target Use Cases (from QNF Dashboard)
1. **Neurodivergent professionals** — primary audience
2. **CNA/Healthcare workers** — structured task management under pressure
3. **Solo entrepreneurs** — AI-assisted cognitive offloading
4. **Students** — study aid with memory lattice
5. **Automotive/Trades** — reference lookup, procedure notes
6. **Elder care** — simplified interface, routine support

## QNF Ecosystem Layer
**Avatar** (Body/Interface) — Accessibility and inclusion

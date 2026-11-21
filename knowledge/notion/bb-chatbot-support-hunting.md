# SKILL: Chatbot & Live Support Security Hunting

**Name:** `bb-chatbot-support-hunting`  
**Version:** 1.0  
**Source:** Notion — *Chatbot & Live Support Security — Specialized Hunting Methodology*  
**Purpose:** Execution-ready hunting module for classic live chat, support widgets, AI support agents, RAG-backed chat, and real-time/API integrations.

> Module inside the Universal Adaptive Hunting Methodology — **not** a second methodology and not a writeup library. Do not default to prompt injection; many chat surfaces are ordinary web apps with identity, authz, state, parser, storage, and integration boundaries.

## When to use

Target exposes any of: chat bubble, support widget, AI assistant, helpdesk agent, transcript/email bridge, MQTT/WebSocket chat backend, agent inbox/console.

## Position in Methodology OS

Follow the universal loop:  
Scope → Discover → Model → Map → Orient → Property → Hypothesis → Baseline → One Mutation → Observe → Discriminate → Validate → Impact → Chain → Update → Stop/Report

## 1. Classify the surface first

| Type | Typical contents | Primary questions |
| --- | --- | --- |
| Classic live chat | Visitor ↔ human agent, sessions, attachments | Can visitor A affect/read visitor B? |
| Third-party widget | External script, tenant/app ID, browser token | Integration config secure? Who owns the bug? |
| AI chatbot | Model conversation, history, renderer | User content into privileged context / unsafe render? |
| AI support agent | CRM, tickets, tools, refunds, lookup | Influence identity, tools, approvals, actions? |
| RAG assistant | Docs, chunks, embeddings | Ingestion/retrieval/tenant/provenance secure? |
| Real-time backend | WS / Socket.IO / MQTT | Connection, topic, event, resource authz? |
| Agent/admin console | Staff inbox, previews, moderation | Attacker content execute or alter operator view? |

Do not infer architecture from the UI alone. Map the data path.

## 2. Architecture graph (replace nodes with observations)

```text
Visitor Browser
  ├── Widget JS / Public Config
  ├── REST / GraphQL API
  └── WebSocket / Socket.IO / MQTT-over-WS
          ↓
     Chat Backend / Broker
          ├── Session & Conversation Store
          ├── Attachments
          ├── Human Agent Inbox / Admin Console
          ├── Ticketing / CRM / Identity APIs
          └── AI Orchestrator
                 ├── System / Developer Context
                 ├── History / Memory
                 ├── RAG / Vector Store
                 ├── Tools / Function Calls
                 ├── Email / External APIs
                 └── Action / Approval Workflow
```

For each component record: host/protocol/product, who can reach it, auth artifact, objects (conversation/thread/visitor/ticket/attachment/doc IDs), state, inputs, decision point, consumer, side effects. Label confidence: confirmed / inferred / unknown.

## 3. Actors (model separately)

Anonymous guest · Customer A · Customer B · Support agent · Supervisor · App admin · Internal AI/service principal · Third-party integration · Tenant admin · Background worker/ingestion

## 4. Trust boundaries (invariants)

- Browser → widget provider: public config ≠ privileged credential
- Guest → authenticated: no promotion via client metadata
- Customer A → B: conversation/attachment/profile remain owner-bound
- Customer → agent console: untrusted messages stay data, not operator instructions or executable markup
- WS connection → message: every sensitive event authorized for principal/resource/context
- MQTT client → topic: only authorized topics/scopes
- Tenant A → B: no cross-tenant retrieval/subscription/action
- Email parser → AI agent: identity bound to authenticated/normalized data
- RAG ingestion → retrieval: permissions + provenance + tenant preserved
- AI agent → tool/API: tool independently enforces caller scope
- AI output → UI: treat as untrusted data; safe rendering
- Third-party provider → target app: ownership vs program scope distinguished

## 5. Recon tracks

### Visible feature
Launchers, login gating, which pages load the widget, when session/token is created.

### Frontend artifacts
apiUrl, chatHost, socketUrl, mqttUrl, tenant/app IDs, conversation create endpoints, guest registration, WS paths/events, upload/transcript routes, agent preview, KB/ingestion endpoints, CRM/refund tools.

Public hostname/config/token is a **discovery signal**, not automatically a vulnerability.

### Endpoint inventory fields
Interface · Method/event/topic · Auth · Principal · Resource · Tenant · Operation · State dependency · Response/effect · Evidence

Prioritize surfaces that expose/modify another user’s data, reach staff, invoke tools, change financial/account state, or cross tenants.

## 6. Universal chat testing loop

1. Context (component, interface, principal, tenant, object, state)
2. Invariant
3. Hypothesis
4. Baseline (account/resource you control)
5. **One mutation**
6. Observation
7. Discriminator (benign explanations)
8. Validation (unauthorized data/capability/state with controlled test data)
9. Impact (actual, not theoretical max)
10. Negative knowledge
11. Next experiment

**Do not promote** 200 / exposed config / hidden event / model claim of success without proving a boundary was crossed.

## 7. Hunting tracks (summary)

### A — Identity / guest / session binding
Invariant: identity established server-side; client metadata must not grant privileged identity.  
Variants: spoofable forwarding headers, mutable guest secrets, stale tokens, widget token confused with account session.  
Validate only on owned test conversations.

### B — Conversation IDOR / BOLA / tenant isolation
Objects: conversation/thread/chat/session IDs, visitor/customer/agent IDs, ticket/order IDs, attachment/file/doc IDs, tenant/workspace IDs.  
Method: two owned customers A/B; baseline A→A; substitute only B’s ID; test read **and** write; compare REST/GraphQL/WS; nested objects; alternate transcript/export endpoints; search leakage; deleted/closed objects; cache leakage.

### C — WebSocket / Socket.IO / MQTT authorization
Handshake success ≠ unrestricted authority. Re-check auth after role/tenant/session changes. Map events, subscriptions, recipients.

### D — AI agent / tools / RAG / output XSS
Treat agent-rendered HTML as XSS sink until proven sanitized. Tool calls must re-check authz. conversationID history BOLA (incl. unauthenticated). Prompt injection only as LEAD toward evidence of unauthorized action on owned accounts.

### E — Attachments / uploads
Ownership on download; content-type vs magic bytes; staff preview sinks.

## Agent output contract

1. Surface classification table
2. Target Graph (chat-specific nodes)
3. Active hunting track + invariant
4. Baseline + single mutation
5. Discriminator
6. Evidence class: LEAD until validated on owned objects
7. Explicit stop if real customer data appears

## Strong reference patterns (research only)

- Guest registration trusting client `X-Real-IP` → internal bot identity (Better Messages style identity confusion)
- Zero-click stored XSS in chat rendered in agent console
- MQTT/WebSocket topic authorization failures
- Third-party widget object IDOR (Intercom-style)

Always re-validate on the **current** in-scope target; historical CVEs are patterns, not automatic findings.

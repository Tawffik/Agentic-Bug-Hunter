# Chat, Support Widgets & Real-Time Backends

> A support widget is an ordinary web app with identity, authorization, state, storage and integration
> boundaries. Do not default to prompt injection. Map the data path first, then test the boundary that
> carries the most sensitive data.

Use when the target exposes: chat bubble, support widget, AI assistant, helpdesk agent, transcript/email
bridge, MQTT/WebSocket chat backend, or an agent/admin console. Pair with `agentic-app-audit` (deployed
agent actions), `llm-redteam` (model behavior) and `web2-vuln-classes` (authz).

---

## 1. Classify the surface

| Type | Contents | Primary question |
|---|---|---|
| Classic live chat | visitor ↔ human agent, sessions, attachments | can visitor A read/affect visitor B? |
| Third-party widget | external script, tenant/app ID, browser token | is integration config secure? who owns the bug? |
| AI chatbot | conversation, history, renderer | does user content reach a privileged context or unsafe sink? |
| AI support agent | CRM, tickets, tools, refunds, lookup | can you influence identity, tools, approvals, actions? |
| RAG assistant | docs, chunks, embeddings | ingestion/retrieval/tenant/provenance isolation? |
| Real-time backend | WS / Socket.IO / MQTT | connection, topic, event and resource authorization? |
| Agent/admin console | staff inbox, previews, moderation | can attacker content execute or alter operator view? |

Do not infer architecture from the UI. Map the data path.

## 2. Architecture graph

```
Visitor Browser
  ├── Widget JS / public config
  ├── REST / GraphQL API
  └── WebSocket / Socket.IO / MQTT-over-WS
          ↓
     Chat backend / broker
          ├── session & conversation store
          ├── attachments
          ├── human agent inbox / admin console
          ├── ticketing / CRM / identity APIs
          └── AI orchestrator
                 ├── system/developer context
                 ├── history / memory
                 ├── RAG / vector store
                 ├── tools / function calls
                 ├── email / external APIs
                 └── action / approval workflow
```

For each node record: host/protocol/product, who can reach it, auth artifact, objects
(conversation/thread/visitor/ticket/attachment/doc IDs), state, inputs, decision point, consumer,
side effects, confidence (confirmed/inferred/unknown).

## 3. Actors

Anonymous guest · Customer A · Customer B · Support agent · Supervisor · App admin · Internal AI/service
principal · Third-party integration · Tenant admin · Background worker/ingestion.

## 4. Trust boundaries (invariants)

- Browser → widget provider: public config is not a privileged credential.
- Guest → authenticated: client metadata must not promote identity.
- Customer A → B: conversations, attachments and profiles stay owner-bound.
- Customer → agent console: untrusted messages stay data, not operator instructions or executable HTML.
- WS connection → message: every sensitive event is authorized for principal/resource/context.
- MQTT client → topic: only authorized topics/scopes.
- Tenant A → B: no cross-tenant retrieval, subscription or action.
- Email parser → AI agent: identity bound to authenticated/normalized data.
- RAG ingestion → retrieval: permissions, provenance and tenant preserved.
- AI agent → tool/API: the tool independently enforces caller scope.
- AI output → UI: treated as untrusted data, safely rendered.
- Third-party provider → target app: ownership vs program scope distinguished.

## 5. Hunting tracks

### A. Identity / guest / session binding
Variants: spoofable forwarding headers (`X-Real-IP`, `X-Forwarded-For`) used to mint an internal bot/guest
identity; mutable guest secrets; stale tokens; widget token mistaken for an account session.
Validate only on owned test conversations.

### B. Conversation IDOR / BOLA / tenant isolation
Objects: conversation/thread/chat/session IDs, visitor/customer/agent IDs, ticket/order IDs,
attachment/file/doc IDs, tenant/workspace IDs.
Method: two owned customers A/B; baseline A→A; substitute only B's ID; test read **and** write; compare
REST/GraphQL/WS; nested objects; alternate transcript/export endpoints; search leakage; deleted/closed
objects; cache leakage; unauthenticated history endpoint.

High-value pattern: `conversationID` / `sessionUUID` accepted without an auth check on a history or
`messages` resolver. Try it with no token and with another user's UUID.

### C. WebSocket / Socket.IO / MQTT authorization
Handshake success is not unrestricted authority. Re-check auth after role/tenant/session changes.
Map events, subscriptions and recipients. Test topic wildcards (`#`, `+`), cross-tenant topic names,
retained messages, and MQTT-over-WS credentials exposed in `env_app.js` / config.
Subscribing broadly to collect real customer messages is out of bounds; prove session mixing between
two owned test sessions.

### D. AI agent / tools / RAG / output XSS
Treat agent-rendered HTML/markdown as an XSS sink until proven sanitized. Test encoded payloads
(base64, HTML entities, markdown→HTML) through the chat and confirm DOM execution in the console.
Tool calls must re-check authz; prompt injection is only a lead until it produces an unauthorized action
on an owned account. See `agentic-app-audit` for tool/memory/confused-deputy tests.

### E. Attachments / uploads
Ownership on download; content-type vs magic bytes; staff preview sinks; filename/path handling.
A deleted attachment may still be reachable through an export, CDN URL or email copy.

## 6. Third-party widget checks

- Intercom-style identity verification: is a signed `user_hash`/JWT required, or can you set an arbitrary
  `user_id`/`email` and read the full support history?
- Is the widget token scoped to a tenant, or usable against another tenant's API?
- `POST /backend/widget/contact/upsert` or similar: does changing the email return another person's
  name/phone/role/internal IDs?
- Do widget APIs accept `conversation_id`/`visitor_id` with no ownership check?
- Who owns the finding: the target tenant or the widget provider? Check program scope before reporting.

## 7. Evidence gate

- Use two owned accounts and a canary conversation/attachment.
- Prove the boundary crossing with the foreign object's content (name/email/message text), not just 200.
- A rendered model string is not XSS until it executes in a real DOM context.
- A WS subscription is not a finding until another session's message is received.
- Stop immediately if real customer data appears; retain only minimal redacted proof.

## 8. Output contract

1. Surface classification table.
2. Chat-specific Target Graph.
3. Active track + invariant.
4. Baseline + single mutation.
5. Discriminator.
6. Evidence class (`LEAD` until validated on owned objects).
7. Explicit stop reason if third-party data appears.
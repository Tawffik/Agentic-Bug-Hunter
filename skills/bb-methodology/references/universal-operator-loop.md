# Universal Operator Loop

> One methodology, any target. Technology changes the **content** of the path, never the **shape** of the
> method. The agent's job is to convert "what should I test?" into a concrete action, one variable, and a
> decision rule.

Use at the start of an engagement, after every finding, and whenever the next step is unclear.

---

## 1. The loop

```
Scope -> Discover -> Model -> Map -> Orient -> Security Property -> Hypothesize
-> Baseline -> Mutate -> Observe -> Discriminate -> Validate -> Impact
-> Chain/Pivot -> Update Model -> Select Next -> Stop/Report
```

Escalate to depth only when the target graph supports it. Never skip scope or validation.

## 2. Operator mode (directive, not questionnaire)

| Stage | DO | Produce |
|---|---|---|
| SCOPE | confirm authorization, limits, identities, allowed impact | testing envelope |
| DISCOVER | enumerate reachable components and alternate interfaces | target inventory |
| MODEL | map components, actors, objects, states, boundaries, consumers | Target Graph |
| MAP | connect features to inputs, decisions, side effects | attack-surface map |
| ORIENT | locate component/interface/identity/object/state | context statement |
| PROPERTY | state the invariant that must hold | security invariant |
| HYPOTHESIZE | pick the highest-value failure mode supported by the model | testable hypothesis |
| BASELINE | perform the normal authorized operation | baseline evidence |
| MUTATE | change ONE meaningful variable | controlled experiment |
| OBSERVE | capture the differential signal | observation |
| DISCRIMINATE | eliminate the cheapest benign explanation | discriminator result |
| VALIDATE | prove boundary crossing + unauthorized consequence | validation evidence |
| IMPACT | measure actual gained capability/data/state | impact evidence |
| CHAIN | follow only evidence-backed new boundaries | chain evidence |
| UPDATE | write known / disproven / unknown | updated Target Graph |
| NEXT | choose the highest-information safe experiment | next experiment |
| STOP | stop low-value/unsafe branches; preserve proof | report package |

Decision rule: never stop at "what should I test?" Ask:
*Given the current Target Graph, what exact action do I take next, what one variable changes, what should
happen securely, and what observation decides the hypothesis?*

---

## 3. Target Graph

```
Organization -> Product -> Domain -> Subdomain -> DNS -> IP/ASN -> Host
-> Technology -> URL -> JS -> API -> Object -> Identity/Tenant -> Cloud/Third-party
```

For each important node record: purpose, reachability, identity/auth, inputs, objects, states, parsers,
where security decisions are made, downstream consumers, evidence, confidence, known/disproven/unknown.

Technology adaptations (same loop):

- WordPress: Core -> Plugin -> REST/AJAX/XML-RPC -> capability -> content object
- GraphQL: Schema -> Query/Mutation -> Resolver -> Object/Field -> identity/tenant
- OAuth/OIDC: Client -> AS -> redirect -> code/token -> identity binding -> session
- Cloud: Principal -> role -> resource -> policy -> service boundary
- AI app: User -> model/agent -> prompt/context -> tool boundary -> delegated identity -> external system
- Chat/support: Visitor -> widget/API/WebSocket -> backend -> agent console -> CRM/tools

Maintain three separate states: **Target State** (what exists), **Knowledge State** (what you know),
**Experiment State** (what you ran and observed).

---

## 4. Security property, not vuln name

Start from what must remain true, then test the failure:

- Identity: the caller is who the session says, established server-side.
- Authentication: the session proved the required factor.
- Authorization: the caller may perform this operation on **this** object/tenant.
- State: lifecycle transitions happen in the allowed order and are not replayable.
- Representation: every serializer enforces the same visibility.
- Parser: the path/value authorized is the path/value executed.
- Disclosure: data is visible only to its intended audience.
- Capability: credentials/tools do not exceed the caller's authority.
- Delegation: an agent acts only with the user's scope and consent.
- Isolation: tenant A cannot read/write/listen to tenant B.
- Business constraint: price/quota/entitlement/limits are enforced server-side.
- Execution safety: user input cannot reach an interpreter or native parser unsafely.

---

## 5. Mutation dimensions

Change one at a time:

- **Actor**: anon, user A, user B, low role, admin, service principal.
- **Object**: own -> sibling -> foreign -> non-existent -> special value (`*`, `0`, `-1`, `null`).
- **Context**: tenant, workspace, org, project.
- **State**: draft, pending, active, archived, deleted, exported, expired.
- **Representation**: HTML, JSON, XML, CSV, PDF, export, download, mobile, GraphQL.
- **Parser**: encoding, case, path form, duplicate keys/params, content-type, body size.
- **Capability**: read vs write vs delete vs export vs share vs delegate.
- **Boundary**: browser -> server, service -> service, agent -> tool, tenant -> tenant.
- **Discovery**: historical copy, alternate host, old API version, derived sibling path.

A mutation is a controlled question, not a payload dump.

---

## 6. Observation vs vulnerability

Signal is not a finding. Always ask: *what benign explanation could produce this?* Run the cheapest
discriminator (public-by-design, your own data, cache, SPA shell, generic error, fixture, intended behavior).

Promotion gate:

```
Observation -> Security Boundary Crossed -> Invariant Violated
-> Unauthorized Capability/Data/State Change -> Reproducible Evidence
```

Classification:

- `LEAD` — plausible, unvalidated.
- `CONFIRMED` — reproducible boundary crossing with an owned account/object.
- `KILLED` — discriminated as benign/out-of-scope/not reproducible. Record why.

Never label `CONFIRMED` without reproducible unauthorized consequence inside the testing envelope.

---

## 7. Prioritization

```
Information Gain x Security Impact x Target Applicability x Evidence Value x Coverage Value
------------------------------------------------------------------------------------------
                              Cost / Risk
```

Prefer what changes the next decision: new trust boundary, privileged function, object identifier,
tenant boundary, auth state, legacy component, unusual parser, management surface, cross-component link.

Coverage track per node: `UNKNOWN -> DISCOVERED -> MAPPED -> BASELINED -> TESTED -> VALIDATED / REJECTED / BLOCKED / N/A`.

---

## 8. Fast path (time-limited)

```
SCOPE -> DISCOVER -> MODEL HIGH-VALUE -> ORIENT -> PROPERTY -> BASELINE
-> ONE HIGH-INFO MUTATION -> DISCRIMINATE -> VALIDATE -> IMPACT -> UPDATE -> NEXT/STOP
```

Use when a program is crowded or a target looks thin. Still record negative evidence.

## 9. Agent output contract

When this loop is active, emit:

1. Envelope status (scope/limits clear?)
2. Target Graph summary (or gaps)
3. Orient answers (component/interface/identity/tenant/object/state)
4. Invariant under test
5. Hypothesis + the single mutation
6. Expected secure behavior vs observed
7. Discriminator plan
8. Evidence class (`LEAD` until validated)
9. Next experiment or stop reason

## 10. Routing

| Signal | Skill |
|---|---|
| New/unknown assets, JS, historical URLs | `web2-recon` |
| Exposure/file/debug/archive artifact | `web2-exposure` |
| Search-engine/code-search/infrastructure pivot | `dorking-osint` |
| Object/tenant/role authorization | `web2-vuln-classes` + `johnwick/references/authz-idor.md` |
| URL fetch/webhook/render | `web2-vuln-classes` (SSRF ref) + `/oob` |
| GraphQL endpoint | `graphql-audit` |
| Auth/OAuth/JWT/session | `web2-vuln-classes` + `argus` |
| Chat/support/AI agent | `agentic-app-audit`, `llm-redteam` |
| CI/CD or public build metadata | `cicd-security` |
| Cloud credential/bucket | `cloud-pentest` |
| Chain a low/medium finding | `bug-chaining` |
| Validate or write | `triage-validation`, `report-writing` |
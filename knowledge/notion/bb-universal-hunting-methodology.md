# SKILL: Universal Adaptive Hunting Methodology

**Name:** `bb-universal-hunting-methodology`  
**Version:** 1.0  
**Source of truth:** Notion — *00 — Universal Adaptive Hunting Methodology v1*  
**Purpose:** Single canonical execution methodology for authorized bug bounty / security research. One methodology, any target.

> **Authorized testing only.** Never leave the program scope. Never auto-confirm vulnerabilities. Every claim needs evidence.

## When to use this skill

- Starting any new authorized engagement
- Orienting an agent before choosing the next experiment
- Converting "what should I test?" into a concrete action + variable + expected observation
- After any finding: update the Target Graph and pick the next high-information experiment

## Core invariant workflow

```text
Scope → Discover → Model → Map → Orient → Security Property → Hypothesize
→ Baseline → Mutate → Observe → Discriminate → Validate → Impact
→ Chain/Pivot → Update Model → Select Next → Stop/Report
```

Technology (WordPress, GraphQL, OAuth, Cloud, AI) changes the **content of the path**, never the methodology.

## Operator mode — directive, not questionnaire

At every stage, **do an action** and **produce an artifact**:

| Stage | DO | Produce |
| --- | --- | --- |
| SCOPE | confirm authorization, limits, identities, allowed impact | testing envelope |
| DISCOVER | enumerate reachable components and alternate interfaces | target inventory |
| MODEL | map components, actors, objects, states, boundaries, consumers | Target Graph |
| MAP | connect features to inputs, decisions, side effects | attack-surface map |
| ORIENT | locate component / interface / identity / object / state | current context |
| SECURITY PROPERTY | state the invariant that must hold | security invariant |
| HYPOTHESIZE | select highest-value failure mode supported by the model | testable hypothesis |
| BASELINE | perform the normal authorized operation | baseline evidence |
| MUTATE | change ONE meaningful variable | controlled experiment |
| OBSERVE | capture the relevant differential signal | observation |
| DISCRIMINATE | eliminate the cheapest benign explanation | discriminator result |
| VALIDATE | prove boundary crossing + unauthorized consequence | validation evidence |
| IMPACT | measure actual gained capability / data / state | impact evidence |
| CHAIN/PIVOT | follow only evidence-backed new boundaries | chain evidence |
| UPDATE | write known / disproven / still unknown | updated Target Graph |
| NEXT | choose highest-information safe experiment | next experiment |
| STOP/REPORT | stop low-value/unsafe branches; preserve proof | report package |

**Decision rule:** Never stop at "what should I test?" Convert to:  
*Given the current Target Graph, what exact action do I perform next, what variable do I change, what should happen securely, and what observation will decide the hypothesis?*

## Mental models

**System model:**  
Target → Components → Interfaces → Trust Boundaries → Actors → Objects → States → Inputs → Representations/Parsers → Security Decisions → Downstream Consumers

**Security model:**  
Actor + Context + Capability + Object + State + Operation → Expected Security Decision

**Research model:**  
Observation → Invariant → Hypothesis → Baseline → Controlled Mutation → Signal → Competing Explanations → Discriminator → Safe Validation → Evidence → Impact

## Phase cards (agent execution)

### 1. Scope (pre-flight gate)

Do not begin active experimentation until known or explicitly marked unknown:

- Scope → Authorization → Identities → Allowed Actions → Forbidden Actions
- Rate/Safety Limits → Evidence Limits → Stop/Escalation Rules

Output: **testing envelope** that constrains every later experiment.

### 2. Discover

Discover the target as a **system**, not a list of URLs.

Collect: domains/hosts/environments, apps/services, clients, APIs, alternate interfaces, auth/IdP, tech clues, plugins, storage, integrations, async processing, cloud boundaries, historical/legacy/debug surfaces, CDN/WAF/cache.

Prefer passive first. Output: **target inventory** with confidence and unknowns.

### 3. Model

Decompose: Target → Components → Interfaces → Trust Boundaries → Actors → Objects → States → Representations → Configuration → Integrations → Deployment → Historical/Legacy

For each important component record: purpose, reachability, identity, inputs, objects, states, parsers, where security decisions occur, downstream consumers, known vs unknown, evidence, confidence.

Output: **Target Graph**.

Technology adaptation examples (same phases always):
- WordPress: Core → Plugin → REST/AJAX/XML-RPC → capability → content object
- GraphQL: Schema → Query/Mutation → Resolver → Object/Field → identity/tenant
- OAuth/OIDC: Client → AS → redirect → code/token → identity binding → session
- Cloud: Principal → role → resource → policy → service boundary
- AI app: User → model/agent → prompt/context → tool boundary → delegated identity → external system

### 4. Map attack surface

Rank by:  
`Security Impact × Exposure × Privilege/Trust × Object/Data Value × State/Integration Complexity × Unknown/Coverage Value ÷ Cost/Risk`

For each feature: Feature → Actor → Object → State → Input → Representation → Interface → Security Decision → Side Effect → Response → Downstream Consumer

Classify operations: read / create / modify / delete / execute / approve / export / delegate / invoke / change security state / create capability / trigger interpreter.

### 5. Orient ("Where am I?")

Answer before testing:
1. Component?
2. Interface?
3. Who am I?
4. Tenant/site/account?
5. Object/capability?
6. State?
7. Controlled input/representation?
8. Who should make the security decision?
9. Downstream consumer?
10. Critical unknown?

If unclear: **STOP TESTING → gather context**.

### 6. Security property (invariant)

Do not start with a vuln name. State what must remain true, e.g.:
Identity, Authentication, Authorization, State, Representation, Input/Parser, Disclosure, Capability, Delegation, Isolation, Business constraint, Execution safety.

### 7–9. Hypothesize → Baseline → Mutate

High-value dimensions: actor substitution, object/context substitution, state mutation, representation mutation, capability mutation, boundary mutation, discovery mutation.

Baseline the legitimate operation first. Then change **one** meaningful variable. Mutation is a controlled question, not a payload dump.

### 10–12. Observe → Discriminate → Validate

Signal ≠ vulnerability. Always ask: *What benign explanation could produce this?* Run the cheapest safe discriminator.

Promotion gate:  
`Observation → Security Boundary Crossed → Invariant Violated → Unauthorized Capability/Data/State Change → Reproducible Evidence`

### 13–15. Impact → Chain → Update

Measure actual gained capability. Represent chains as:  
`Primitive → Boundary Crossing → Capability → … → Impact`  
Every edge needs evidence.

Maintain three separate states: Target State, Knowledge State, Experiment State.

### 16–17. Next / Stop

Priority:  
`Information Gain × Security Impact × Target Applicability × Evidence Value × Coverage Value ÷ Cost/Risk`

Coverage track: UNKNOWN → DISCOVERED → MAPPED → BASELINED → TESTED → VALIDATED / REJECTED / BLOCKED / N/A

**Fast Path** (time-limited):  
SCOPE → DISCOVER → MODEL HIGH-VALUE → ORIENT → PROPERTY → BASELINE → ONE HIGH-INFO MUTATION → DISCRIMINATE → VALIDATE → IMPACT → UPDATE → NEXT/STOP

## Agent output contract

When this skill is active, the agent should emit:

1. **Envelope status** (scope/limits clear?)
2. **Current Target Graph summary** (or gaps)
3. **Current context** (orient answers)
4. **Invariant under test**
5. **Hypothesis + single mutation**
6. **Expected secure behavior vs observed**
7. **Discriminator plan**
8. **Evidence status** (LEAD only until validated)
9. **Next experiment** or **stop reason**

Never label CONFIRMED without reproducible unauthorized consequence inside the testing envelope.

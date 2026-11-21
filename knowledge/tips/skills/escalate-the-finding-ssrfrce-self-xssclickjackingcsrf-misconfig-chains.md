# SKILL: Escalate the finding: SSRF→RCE, Self-XSS→Clickjacking/CSRF, misconfig chains

**Skill id:** `tip/escalate-the-finding-ssrfrce-self-xssclickjackingcsrf-misconfig-chains`  
**Category:** General  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/41ddac31e8808141bcf2d4867ea40ebe  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

البلاغ بـP3 ضعيف غالبًا لأن السلسلة توقفت مبكرًا. فكّر في التصعيد داخل النطاق فقط: SSRF قد يصل لـmetadata/internal admin؛ Self-XSS قد يصبح قابل للاستغلال عبر clickjacking أو CSRF إذا وُجدت نقطة إقناع الضحية؛ Directory listing → configs → internal hosts → SSRF → path traversal → admin API → secrets. وثّق كل حلقة بدليل منفصل ووقف عند الحد المصرّح.

## Payload / Code

```
Chain checklist (authorized scope only):
Directory Listing → Exposed Configs → Internal Host Discovery → SSRF → Path Traversal → Internal Admin API → Secrets
Don't report SSRF alone if internal RCE/metadata is reachable
Don't report Self-XSS alone if clickjacking/CSRF can deliver it
Don't report Self-Stored XSS alone if CSRF can trigger it
```

## Source

Abhishek + Youssef Mohamed tips (X)

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

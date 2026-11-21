# SKILL: حيلة Burp لاكتشاف Blind SSRF عبر Bruteforce للـ Headers

**Skill id:** `tip/حيلة-burp-لاكتشاف-blind-ssrf-عبر-bruteforce-للـ-headers`  
**Category:** SSRF  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dddac31e88081ffa282e270a9db12bd  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **SSRF**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

بدل ما تدور على كل header يدوي، استخدم Intruder عشان تبروت فورس قائمة headers معروفة بتسبب SSRF (X-Forwarded-For, X-Real-IP...) وتحط قيمتها Burp Collaborator ID مع بريفكس رقمي ميز. Pitchfork بتربط كل header برقمه، وTarborator بيراقب أي hit يرجع من اللي target.

## Payload / Code

```
Step 1: استخدم Intruder لـ Bruteforce Headers
Step 2: ضيف Burp collaborator ID كـ value
Step 3: ضيف prefix numerical payload (Pitchfork attack type)
Step 4: استخدم Tarborator Extension لمراقبة الـ hits
```

## Source

kjulius @ethical\_h4ck3r\_

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

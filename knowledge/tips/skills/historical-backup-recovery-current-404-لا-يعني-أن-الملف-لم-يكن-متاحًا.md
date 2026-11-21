# SKILL: 📜 Historical Backup Recovery — Current 404 لا يعني أن الملف لم يكن متاحًا

**Skill id:** `tip/historical-backup-recovery-current-404-لا-يعني-أن-الملف-لم-يكن-متاحًا`  
**Category:** Recon  
**Rating:** 🔥 قوية  
**Status:** Done  
**Notion:** https://app.notion.com/p/3efdac31e8808193a0f3c766e484cae1  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

الفكرة: إذا وجدت URL أو file pattern والـcurrent response = 404/410، افحص التاريخ قبل إسقاطه.

workflow:
known URL/file → current status → Wayback/other historical source → historical 200/content → extract metadata/URLs/hosts → current validation.

الأهم: لا تبحث فقط عن .bak; استخدم files ظهرت فعلًا في target history مثل PDF/CSV/JSON/ZIP/log/config/database artifacts.

Archived copy ≠ vulnerability. ابحث عن sensitive content + relation بالـcurrent target.

## Payload / Code

```
current = 404
      ↓
historical source
      ↓
200 snapshot
      ↓
content extraction
      ↓
current relation
```

## Source

Wayback/archival bug bounty research; historical deleted-file recovery patterns

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

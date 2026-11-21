# SKILL: 🔔 Bug Bounty Tip — File/Folder Delete Endpoints Need Separate Authorization Checks

**Skill id:** `tip/bug-bounty-tip-filefolder-delete-endpoints-need-separate-authorization-checks`  
**Category:** IDOR, API Hacking, Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3e5dac31e880814da602f889900143db  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **IDOR, API Hacking, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

Type: Bug Pattern
Use when: the product supports file storage, folders, notes, attachments, or collaborative documents.

Where to look → DELETE /files/\{id\}, /folders/\{id\}, bulk-delete endpoints, restore/trash APIs, and UI actions that send a resource ID.

What to test → With two authorized test accounts, compare read, update, move, delete, and restore behavior for the same object. Do not assume that because viewing is protected, destructive actions are protected too.

Primitive / bypass → Function-level authorization gap or IDOR on a destructive endpoint.

Validation / impact → Use a harmless test file/folder you own. Prove whether the second account can delete or modify it, then stop. Record the exact endpoint, authorization context, object ownership, and whether the action is reversible.

## Payload / Code

```
Use two owned accounts and one disposable test object. Test one request at a time; avoid bulk actions or production data.
```

## Source

[https://www.bugbountydirectory.com/blogs/unauthorized-user-can-delete-any-file-folder](https://www.bugbountydirectory.com/blogs/unauthorized-user-can-delete-any-file-folder)

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

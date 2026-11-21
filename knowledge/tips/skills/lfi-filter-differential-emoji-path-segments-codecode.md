# SKILL: LFI Filter Differential: Emoji Path Segments (<code>⬅️/</code>)

**Skill id:** `tip/lfi-filter-differential-emoji-path-segments-codecode`  
**Category:** Fuzzing, WAF Bypass  
**Rating:** 📌 للمراجعة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e8808167af48dc7cf431d300  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Fuzzing, WAF Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

A recent researcher tip showed a file-download endpoint returning 404 for a conventional traversal string but 200 for an emoji-based path variant such as ⬅️/⬅️/⬅️/etc/passwd. Treat this as an application-specific normalization/filter differential, not a universal traversal payload: the emoji may be interpreted, mapped, or handled specially by the target's processing chain. The useful signal is a reproducible response/content difference when a blocked path representation is replaced with a nonstandard Unicode/emoji representation.

## Payload / Code

```
Only on an explicitly authorized file-view/download endpoint, start with a harmless file within the allowed test area and compare response status, length, content type, and body:
- Baseline blocked traversal pattern: ../../../known-test-file
- Unicode/emoji variant to investigate: ⬅️/⬅️/⬅️/known-test-file

Do not jump straight to reading /etc/passwd on a live target. First determine whether the application actually maps or normalizes the emoji and whether access crosses the intended directory boundary. A 200 alone is not proof; confirm the returned file and demonstrate only the minimum authorized impact.
```

## Source

Researcher X post by @0xConda, surfaced in Intigriti Bug Bytes #240 (Sep 2026): [https://x.com/0xConda](https://x.com/0xConda) ; roundup: [https://www.intigriti.com/researchers/blog/bug-bytes/intigriti-bug-bytes-240-september-2026](https://www.intigriti.com/researchers/blog/bug-bytes/intigriti-bug-bytes-240-september-2026)

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

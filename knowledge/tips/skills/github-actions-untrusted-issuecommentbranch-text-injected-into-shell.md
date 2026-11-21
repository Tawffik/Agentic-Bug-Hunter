# SKILL: GitHub Actions: untrusted issue/comment/branch text injected into shell

**Skill id:** `tip/github-actions-untrusted-issuecommentbranch-text-injected-into-shell`  
**Category:** RCE, Recon  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/401dac31e88081c6b89ff70a4c90e947  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **RCE, Recon**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

لو workflow بيحط نصًا يتحكم فيه المستخدم (issue title/body، comment، branch name أو PR metadata) مباشرة داخل run: shell، ممكن يتحول النص إلى أوامر بدل ما يظل بيانات. راجع التعبيرات ${{ ... }} داخل shell scripts، وانقل المدخلات إلى environment variables مع quoting آمن أو استخدم action/لغة تتعامل معها كبيانات. لا تختبر بحقن أوامر في workflow حي؛ أثبت المسار بمراجعة YAML أو في نسخة تملكها.

## Payload / Code

_No specific payload — use the methodology in How It Works._

## Source

GitHub Docs — Script injections: [https://docs.github.com/en/actions/concepts/security/script-injections](https://docs.github.com/en/actions/concepts/security/script-injections) ; GitHub Advisory GHSA-6p2j-742g-835f: [https://github.com/advisories/GHSA-6p2j-742g-835f](https://github.com/advisories/GHSA-6p2j-742g-835f) ; GitHub Advisory GHSA-c3xh-98xp-6qhf: [https://github.com/advisories/GHSA-c3xh-98xp-6qhf](https://github.com/advisories/GHSA-c3xh-98xp-6qhf)

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

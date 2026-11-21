# SKILL: npm Remote Dependency URLs → CI/CD Secret Theft

**Skill id:** `tip/npm-remote-dependency-urls-cicd-secret-theft`  
**Category:** Recon, API Hacking, General  
**Rating:** 🔥 قوية  
**Status:** Not started  
**Notion:** https://app.notion.com/p/3e3dac31e88081a88ae5e918762469a7  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, API Hacking, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

A September 2026 campaign analysis described malicious npm packages that kept the obvious payload outside the registry by declaring dependencies through attacker-controlled remote URLs. That makes the package look smaller and can move the real execution path into install-time dependency resolution. For hunting, inspect package manifests, lockfiles, lifecycle scripts, and CI build logs for remote dependency URLs, unexpected install-time network access, and secret exposure in build environments. Study Tab: package/registry usage → inspect dependency sources and install hooks → remote dependency execution + CI secret access → validate with isolated test projects and redacted proof. Use when: a target publishes or consumes npm packages, runs automated builds, or exposes package metadata and CI/CD artifacts.

## Payload / Code

_No specific payload — use the methodology in How It Works._

## Source

Noze / CrowdStrike PhantomRaven analysis — 22 Sep 2026 — [https://www.noze.it/en/insights/phantomraven-npm-bug-bounty-en/](https://www.noze.it/en/insights/phantomraven-npm-bug-bounty-en/)

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

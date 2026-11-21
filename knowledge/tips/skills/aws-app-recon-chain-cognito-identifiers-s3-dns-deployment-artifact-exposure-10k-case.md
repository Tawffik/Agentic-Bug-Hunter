# SKILL: AWS App Recon Chain → Cognito Identifiers, S3 / DNS / Deployment Artifact Exposure (\$10K Case)

**Skill id:** `tip/aws-app-recon-chain-cognito-identifiers-s3-dns-deployment-artifact-exposure-10k-case`  
**Category:** Recon, General  
**Rating:** ⭐ جيدة  
**Status:** Not started  
**Notion:** https://app.notion.com/p/402dac31e88081769f82dc7920d56dbb  

> **Authorized testing only.** LEAD until validated on accounts/objects you own. Never auto-confirm.

## When the agent should use this skill

- Hunting track involves: **Recon, General**
- Target signals match this technique
- Scope and testing envelope confirmed

## How It Works

A 2025 Medium writeup reports a \$10,000 bounty for an AWS configuration issue found while reviewing app client code and auth/file-management traffic. A Cognito pool identifier led to correlation of publicly readable cloud resources and deployment artifacts, exposing S3, DNS ranges and infrastructure metadata. The writeup says the researcher used passive discovery and read-only checks; payout is self-reported. The value is the correlation chain, not treating a public identifier as a secret.

## Payload / Code

```
On in-scope assets only: inspect public JS/config and observed auth/file flows for AWS region, Cognito User Pool or Identity Pool identifiers, bucket names, API base URLs and deployment references. Follow only resources linked from the authorized target and verify access with minimal read-only requests. Do not enumerate unrelated buckets, download sensitive artifacts, authenticate with discovered credentials, or modify cloud resources. Report the exact exposed resource and data category with redacted evidence.
```

## Source

[https://medium.com/%40ethan\_hunt/how-i-won-10k-by-finding-an-aws-misconfiguration-in-an-app-and-what-you-can-learn-990ee90b4f05](https://medium.com/%40ethan_hunt/how-i-won-10k-by-finding-an-aws-misconfiguration-in-an-app-and-what-you-can-learn-990ee90b4f05) ; [https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html) ; [https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)

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

# Test Security ITW

| Field | Value |
|-------|-------|
| **Issue ID** | [335222589](https://issues.chromium.org/issues/335222589) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows |
| **Reporter** | ph...@google.com |
| **Assignee** | pg...@google.com |
| **Created** | 2024-04-16 |
| **Bounty** | $1.00 |

## Description

This is a test bug to test the Security-ITW automation

## Timeline

### ma...@google.com (2024-04-17)

Does this bug need to remain open? Do we need to keep it untriaged, or can we set a random assignee/severity/found-in so that it doesn't appear as untriaged in our dashboard?

### ph...@google.com (2024-04-25)

Reopening for a day to test a blintz rule.

### th...@chromium.org (2024-04-30)

Is this bug still needed?

### am...@chromium.org (2024-05-01)

phao@ is OOO this week. I believe this issue was being used to test some blintz automation for security-notify-itw; it looks like the automation work is still underway. So I'm going to triage this issue in such a way as to ensure it isn't sitting on top of the dashboard.

### am...@chromium.org (2024-05-01)

As an aside, @phao -- can you please ensure the Security ITW hotlist ACLs are updated to include our chromium accounts. I can only see and access this hotlist from my Google account.

Thank you!

### ch...@chromium.org (2024-05-03)

Setting severity to kick from queue(?)

### ph...@chromium.org (2024-05-07)

amyressler@: I added your, Ade and Grace's chromium accounts to the hotlist ACL. Also I think the automation has worked. security-notify-itw@ has been added as collaborators.

### pe...@google.com (2024-08-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ph...@google.com (2024-08-22)

Setting it to fixed to test some automation. If this affects any metrics, feel free to change it back.

### pg...@google.com (2024-08-22)

I've updated the shepherd dashboard to permanently remove this from the query (: so feel free to use this however you need @phao!

### pe...@google.com (2024-08-27)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security> Thanks for your time!

### pe...@google.com (2024-09-05)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/335222589)*

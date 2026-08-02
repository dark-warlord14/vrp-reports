# Missing origin check in FileSystemAccessObserverHost::Observe() allows cross-origin file observation

| Field | Value |
|-------|-------|
| **Issue ID** | [499917177](https://issues.chromium.org/issues/499917177) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 147.0.0.0 |
| **Reporter** | er...@paloaltonetworks.com |
| **Assignee** | fe...@chromium.org |
| **Created** | 2026-04-06 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Apply the attached patch from the root of the Chromium src tree:
   git apply fsa\_observer\_xorigin\_bypass.patch
2. Build:
   autoninja -C out/Default content\_browsertests
3. Run:
   out/Default/content\_browsertests   
   
   --gtest\_filter='*ObserverCrossOriginTokenBypass*'
4. Observe the output:
   
   - "ObserveAcceptsCrossOriginToken" PASSES with log:
     "VULNERABILITY CONFIRMED: Observe() accepted a transfer token from
     <https://victim.example> on an ObserverHost bound to
     <https://attacker.example>"
   - "ResolveTransferTokenRejectsCrossOriginToken" PASSES, confirming
     origin validation works on other code paths and is only missing
     from Observe().

# Problem Description

FileSystemAccessObserverHost::DidResolveTransferTokenToObserve() does not validate the transfer token's origin against the binding context's origin before using the token.

A compromised renderer for origin B can call Observe() with a transfer token belonging to origin A, gaining the ability to observe file system changes on directories granted exclusively to origin A. The observation is backed by origin A's permission grants, meaning handles delivered through change notifications carry origin A's read/write permissions.

Root Cause:
In file\_system\_access\_observer\_host.cc, DidResolveTransferTokenToObserve() checks:

1. Whether the resolved token is non-null
2. Whether the read grant has GRANTED status

But it doesn't check whether resolved\_token->origin() matches binding\_context().storage\_key.origin().

All other transfer token redemption paths perform this check:

- DidResolveTransferTokenForFileHandle (manager\_impl.cc:1442) calls IsValidTransferToken()
- DidResolveTransferTokenForDirectoryHandle (manager\_impl.cc:1467) calls IsValidTransferToken()

The IsValidTransferToken() function (manager\_impl.cc:302) compares token->origin() against the expected origin from the binding context. This
check is simply missing from the Observe() path.

Impact:

- Cross-origin file observation: attacker monitors file changes in directories granted to another origin
- Permission grant leakage: directory handles created from the token carry victim origin's read/write grants

# Summary

Missing origin check in FileSystemAccessObserverHost::Observe() allows cross-origin file observation

# Custom Questions

#### Reporter credit:

Eran Rom of Palo Alto Networks

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A \

## Attachments

- [fsa_observer_xorigin_bypass.patch](attachments/fsa_observer_xorigin_bypass.patch) (text/x-diff, 12.8 KB)

## Timeline

### za...@google.com (2026-04-07)

[security shepherd] There is a missing token origin check issue in FileSystemAccessObserverHost::DidResolveTransferTokenToObserve(). This allows an attacker origin to use a victim origin's transfer token to observe files, inheriting the user's permissions. Hi fergal@, can you please take a look at this and see if we should add origin validation to DidResolveTransferTokenToObserve(), similar to other paths? Thanks.

### ch...@google.com (2026-04-08)

Setting milestone because of s2 severity.

### dx...@google.com (2026-04-23)

Project: chromium/src  

Branch:  main  

Author:  Fergal Daly [fergal@chromium.org](mailto:fergal@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7784855>

Fix a cross-site leak of file-monitoring capability.

---


Expand for full commit details
```
     
    If site-A has permission to monitor a file or directory then a 
    compromised renderer on site-B can also monitor it. 
     
    The fix is to check that the site associated with the final resolved 
    token is the current site before granting access. 
     
    Fixed: 499917177 
    Change-Id: I815a1a3dbf382b71758565b8ca035a3da5547eb0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7784855 
    Commit-Queue: Fergal Daly <fergal@chromium.org> 
    Reviewed-by: Ming-Ying Chung <mych@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1619316}

```

---

Files:

- M `content/browser/file_system_access/file_system_access_observer_browsertest.cc`
- M `content/browser/file_system_access/file_system_access_observer_host.cc`

---

Hash: [12f2a15d6550acdb736b12c5a394002c1dcd1e80](https://chromiumdash.appspot.com/commit/12f2a15d6550acdb736b12c5a394002c1dcd1e80)  

Date: Thu Apr 23 04:16:34 2026


---

### sp...@google.com (2026-06-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Low impact. Web platform privilege escalation.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-15)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ch...@google.com (2026-07-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/499917177)*

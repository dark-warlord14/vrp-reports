# Heap buffer overflow write in renderer via crafted font in HarfBuzz apply_stch()

| Field | Value |
|-------|-------|
| **Issue ID** | [492209815](https://issues.chromium.org/issues/492209815) |
| **Status** | Verified |
| **Severity** | Unknown |
| **Priority** | P4 |
| **Component** | Unknown |
| **Reporter** | ma...@gmail.com |
| **Created** | 2026-03-12 |
| **Bounty** | $5,000.00 |

## Description

Dear Google team,
I would like to kindly request reconsideration of previous issue (<https://issues.chromium.org/issues/490815163>) being marked as not reproducible.

While the report may indeed be difficult to reproduce on 64bit builds, the underlying reason is probably that the OOB write extends far beyond the ASAN detectable zone, which results in a SIGSEGV because process has no allocated memory on that high adress. However, on 32bit builds, the issue **reproduces normally** and the OOB write can be observed as expected.

I collaborated with the maintainer on a fix, which has already been **merged into Chromium.**

- Please see here:
  <https://chromium.googlesource.com/chromium/src/+/4151e38fc8c91f9cacab2026e44e80720f9f779f>
- Upstream fixes: <https://github.com/harfbuzz/harfbuzz/pull/5823>, <https://github.com/harfbuzz/harfbuzz/pull/5808>

Given that the issue results in a confirmed OOB write, a fix has been implemented and merged, and the behavior is atleast somehow reproducible.

I would appreciate if the issue status could be reconsidered. Even if exploitation may be less likely on 64bit architectures, it still represents a high severity memory corruption.

Thank you for taking another look.

**Original summary of the bug:**

An unsigned integer wraparound in HarfBuzz's apply\_stch() function causes a heap out-of-bounds write that crashes the Chrome renderer process. A malicious webpage can trigger this by serving a crafted OpenType font (which passes OTS) and rendering Arabic text on a canvas. No user interaction is required beyond navigating to the page.

## Timeline

### ch...@google.com (2026-03-16)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ke...@chromium.org (2026-03-16)

We do support 32-bit builds on at least some platforms so this is valid. Since the fix has been rolled already then there is nothing to do, but this bug will serve for VRP panel consideration.

### ma...@gmail.com (2026-03-16)

Thank you for the consideration.

### ch...@google.com (2026-03-17)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-17)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [146, 147].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ma...@gmail.com (2026-03-17)

# Bisect

**Introduced:** `6e6f82b6f3dde0fc6c3c7d991d9ec6cfff57823d` — 2015-11-05 — Behdad Esfahbod
"Implement SYRIAC ABBREVIATION MARK with 'stch' feature"

**Fixed:** `44331f173330671cfb6b1500e23844ceccd12687` — 2026-03-11 — Behdad Esfahbod
"[arabic] Cap stch expansion per run" (PR #5823)

**File:** `src/hb-ot-shaper-arabic.cc`, function `apply_stch()`
**Vulnerable range:** 2015-11-05 to 2026-03-11

### ke...@chromium.org (2026-03-17)

This was fixed in an upstream dependency. The roll does not need to be merged.

### ma...@gmail.com (2026-04-27)

Hi, is there any update on this issue? It has been fixed for some time now.

### sp...@google.com (2026-05-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Baseline. RCE / Memory Corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Baseline. RCE / Memory Corruption in a sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492209815)*

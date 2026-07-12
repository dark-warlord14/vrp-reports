# ANGLE Metal Shadow Buffer Stale Size causes GPU OOB WRITE

| Field | Value |
|-------|-------|
| **Issue ID** | [492249619](https://issues.chromium.org/issues/492249619) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Mac |
| **Reporter** | ci...@gmail.com |
| **Assignee** | gm...@chromium.org |
| **Created** | 2026-03-12 |
| **Bounty** | $18,000.00 |

## Description

---

### Report description

ANGLE Metal Shadow Buffer Stale Size causes GPU OOB WRITE

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/angle/angle/+/refs/heads/main/src/libANGLE/renderer/metal/BufferMtl.mm>

---

### The problem

#### Please describe the technical details of the vulnerability

Heap buffer overflow in ANGLE's Metal backend shadow copy sync. BufferMtl.mm:342 calls memcpy(mShadowCopy.data(), ptr, size()) where size() returns a stale large value after a buffer resize, while the shadow allocation is small.

Buffer.cpp:237-238 calls setDataWithUsageFlags (which runs setDataImpl) before updating mState.mSize at line 244. An inflate-then-shrink sequence leaves size() returning the old large value during the shrink. The Metal buffer pool (mtl\_buffer\_manager.mm) returns buffers without clearing cpuReadMemDirty, so the stale-size memcpy fires on the reused dirty buffer.

Affected OS: macOS Intel with ANGLE Metal backend

### Steps to Reproduce

**ASan** (Chromium 146.0.7676.0, macOS 15.7.2 x64, Intel UHD Graphics 630):

```
./Chromium.app/Contents/MacOS/Chromium poc.html

```

Full ASan trace attached as asan\_full.txt:

```
==22427==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x61900051da80
WRITE of size 524288 at 0x61900051da80 thread T0

```

**Stable** (Chrome 145.0.7632.160, macOS 15.7.2 x64, Intel UHD Graphics 630):

```
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome poc.html

```

GPU process crashes. Crashpad dump:

```
EXC_BAD_ACCESS (code=2, address=0x10c013eb000)
_platform_memmove$VARIANT$Haswell + 41
rdx = 0x80000 (512KB memcpy size)

```
### Proposed Fix

Use mShadowCopy.size() instead of size() at BufferMtl.mm:342:

```
  memcpy(mShadowCopy.data(), ptr, mShadowCopy.size());

```

Or set mState.mSize before calling setDataWithUsageFlags in Buffer.cpp.

### Bisect

Introduced in <https://chromium.googlesource.com/angle/angle/+/968041b54770af8917001d8fe9b52a881cfed0b2> (2022-08-19, "Metal: Optimized BufferSubData per device"). This commit added the buffer pool manager whose returnBuffer/getBuffer recycles buffers without clearing cpuReadMemDirty, making the pre-existing stale-size memcpy in ensureShadowCopySyncedFromGPU reachable.

#### Impact analysis

- Web reachable, no compromised renderer required
- Default WebGL2 config, no flags
- macOS Intel with ANGLE Metal backend
- GPU process heap overflow: up to 512KB past allocation

---

### The cause

#### What version of Chrome have you found the security issue in?

145.0.7632.160 Stable, 146.0.7676.0 Dev

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

cinzinga

## Attachments

- [poc.html](attachments/poc.html) (text/html, 4.6 KB)
- [asan_full.txt](attachments/asan_full.txt) (text/plain, 28.1 KB)
- [asan_out_symbolized.txt](attachments/asan_out_symbolized.txt) (text/plain, 25.5 KB)

## Timeline

### th...@chromium.org (2026-03-13)

[security shepherd] I don't have the hardware to repro this. Speculatively setting found in to extended stable based on description. Also speculative OSes.

gman@ - could you please triage this as relevant?

### ch...@google.com (2026-03-14)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-14)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ci...@gmail.com (2026-03-24)

Looks like the original ASan output did not fully symbolize with the error "invalid path to external symbolizer". I've attached the fixed output.

### gm...@chromium.org (2026-04-02)

This appers to be fixed by <https://chromium-review.googlesource.com/c/angle/angle/+/7703916> The poc doesn't repo.

### ch...@google.com (2026-04-02)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-04-03)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-04-03)

No crashes in Canary after 24 hours, approved to merge to M147.

### ch...@google.com (2026-04-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-04-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2026-05-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $18000.00 for this report.

Rationale for this decision:
Baseline with renderer and bisect bonus. Memory Corruption / RCE in a highly privileged process (e.g. GPU or network)


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492249619)*

# V8 Sandbox Bypass: AAR/W via table set OOB SBXCHECK_LT() bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [349502157](https://issues.chromium.org/issues/349502157) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | se...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2024-06-26 |
| **Bounty** | $5,000.00 |

## Description

### VULNERABILITY DETAILS

V8 sandbox bypass, arbitrary address read/write via table set OOB check bypass using in-sandbox exploit primitives.

As `WasmTableObject`'s `current_length` and `maximum_length` fields can be overwritten, `WasmDispatchTable::Set()` employs a [`SBXCHECK_LT(index, length());`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/wasm-objects.cc;l=1883) to guard against OOB writes in the dispatch table.

However, **both `index` and `length()` are `int`**, and all code paths in:

```
WebAssemblyTableSetImpl()
-> WasmTableObject::Set()
-> WasmTableObject::SetFunctionTableEntry()
-> WasmTableObject::UpdateDispatchTables()

```

...uses a very specific mix of `int` and `uint32_t` which results in negative indices to pass all the checks when `current_length` and `maximum_length` is modified to `0xfffffffe` (`-1` in `smi`). This causes out-of-bounds write with a negative index. This allows us to overwrite another table's dispatch table and cause function type confusion, leading to AAR/W outside of the sandbox.

### VERSION

Chrome Version: ~latest (tested on v8 commit a832ff96bd41b40b9cfee90a314fa816802cf9ae)  

Operating System: all

### REPRODUCTION CASE

Repro added as `table_set_oob.js`.

### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Sandbox violation

### CREDIT INFORMATION

Reporter credit: Seunghyun Lee (@0x10n)

## Attachments

- [table_set_oob.js](attachments/table_set_oob.js) (text/javascript, 71.7 KB)

## Timeline

### el...@chromium.org (2024-06-26)

Security shepherd: thanks for the report. Over to the v8 shepherd (cffsmith@) with provisional Pri-2 Sev-2 & FoundIn, since this is a v8 heap sandbox escape but not an RCE.

### pe...@google.com (2024-06-27)

Setting milestone because of s2 severity.

### cf...@google.com (2024-07-02)

jkummerow@, could you PTAL?

### ap...@google.com (2024-07-12)

Project: v8/v8
Branch: main

commit 2f16c5f7b56c40c1faeca4c14e897ac453d6b5ba
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Fri Jul 12 17:11:30 2024

    [wasm][sandbox] Introduce CHECK_BOUNDS / SBXCHECK_BOUNDS
    
    And use them where appropriate. These new helpers cast their
    arguments to unsigned types, to check with a single unsigned
    comparison that the value in question is both positive and
    less than the provided limit.
    
    Bug: 336507783
    Change-Id: Id08eae110dfde1e8423114d88c6f3fa07957b52c
    Fixed: 349502157
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5701137
    Reviewed-by: Patrick Thier <pthier@chromium.org>
    Reviewed-by: Toon Verwaest <verwaest@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95005}

M       src/base/logging.h
M       src/execution/arguments.h
M       src/regexp/experimental/experimental-interpreter.cc
M       src/sandbox/check.h
M       src/wasm/wasm-objects.cc
M       test/mjsunit/mjsunit.status
A       test/mjsunit/sandbox/regress/regress-349502157.js

https://chromium-review.googlesource.com/5701137


### jk...@chromium.org (2024-07-12)

Another excellent catch, Seunghyun! Thanks for the report.

I think fixing the existing SBXCHECKs (as the patch in #5 does) should be enough. It would certainly be nice to clean up some of the (implicit and explicit) `int`/`uint32_t` casts, but ultimately that would only lead to a fix by virtue of having the eventual consequence of making the SBXCHECKs do unsigned comparisons, so enforcing that directly is both quicker and more robust towards future code changes.

### se...@gmail.com (2024-07-13)

Re #6: Agreed, the signed/unsigned casts were unfortunately making this bypass quite easily reachable but in the end what matters in terms of v8sbx is the corresponding SBXCHECK. Fix looks good to me too :)

### pe...@google.com (2024-07-13)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M127. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
**Merge rejected:** M127 is already shipping to beta and this issue is marked as a Priority:P2,P3 or Type:feature request.

Please contact the milestone owner if you have questions.

**Owners:** eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### jk...@chromium.org (2024-07-15)

#8: That's cool, we don't currently backmerge fixes for V8 Sandbox escapes.

### sp...@google.com (2024-07-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
V8 heap sandbox bypass reward


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2024-10-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/349502157)*

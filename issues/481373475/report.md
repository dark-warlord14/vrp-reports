# Security DCHECK failure: i < length() in 201

| Field | Value |
|-------|-------|
| **Issue ID** | [481373475](https://issues.chromium.org/issues/481373475) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>SVG |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | je...@jvfam.ca |
| **Assignee** | tk...@chromium.org |
| **Created** | 2026-02-03 |
| **Bounty** | $9,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5709310059282432

Fuzzer: jesse_avalanche
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  i < length() in 201
  blink::SVGAElement::DefaultEventHandler
  blink::EventDispatcher::DispatchEventPostProcess
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1578608:1578610

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5709310059282432

Additional requirements: Requires Gestures

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### 24...@project.gserviceaccount.com (2026-02-03)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### ch...@google.com (2026-02-04)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2026-02-04)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### xi...@chromium.org (2026-02-04)

Assigning to tkent@ who is actively working on string view.

### tk...@chromium.org (2026-02-05)

This is a regression by <https://chromium-review.googlesource.com/c/chromium/src/+/7533096> .

I found that `String::operator[]` and `StringView::operator[]` had different behaviors.

### dx...@google.com (2026-02-05)

Project: chromium/src  

Branch:  main  

Author:  Kent Tamura [tkent@chromium.org](mailto:tkent@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7547177>

SVG: Fix a crash in SVGAElement::DefaultEventHandler()

---


Expand for full commit details
```
     
    This CL fixes a regression caused by https://crrev.com/c/7533096 . 
    StringView::operator[] is stricter than String::operator[]. 
     
    Bug: 481373475 
    Change-Id: I2ede74281c5ca754075ebdf40a21b1600d43ce06 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7547177 
    Auto-Submit: Kent Tamura <tkent@chromium.org> 
    Reviewed-by: Fredrik Söderquist <fs@opera.com> 
    Commit-Queue: Fredrik Söderquist <fs@opera.com> 
    Cr-Commit-Position: refs/heads/main@{#1579953}

```

---

Files:

- M `third_party/blink/renderer/core/svg/build.gni`
- M `third_party/blink/renderer/core/svg/svg_a_element.cc`
- A `third_party/blink/renderer/core/svg/svg_a_element_test.cc`
- M `third_party/blink/renderer/platform/wtf/text/string_view.h`
- M `third_party/blink/renderer/platform/wtf/text/wtf_string.h`

---

Hash: [72a3631366f2fe736acae215a62f734ca44093e1](https://chromiumdash.appspot.com/commit/72a3631366f2fe736acae215a62f734ca44093e1)  

Date: Thu Feb 5 09:18:09 2026


---

### ch...@google.com (2026-02-11)

Security Merge Request Consideration: Not requesting merge to dev (M146) because latest trunk commit (1579953) appears to be prior to dev branch point (1582197). If this is incorrect please remove NA-146 from the 'Merge' field and add 146 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### sp...@google.com (2026-03-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $9000.00 for this report.

Rationale for this decision:
memory corruption in a sandboxed process with a fuzzer bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/481373475)*

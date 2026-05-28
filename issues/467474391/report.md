# Use-after-poison in base::MemoryConsumer::UpdateMemoryLimit

| Field | Value |
|-------|-------|
| **Issue ID** | [467474391](https://issues.chromium.org/issues/467474391) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>MemoryCoordinator |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | pm...@chromium.org |
| **Created** | 2025-12-10 |
| **Bounty** | $9,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=6257461686108160

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Use-after-poison WRITE 4
Crash Address: 0x7ecc005d1c38
Crash State:
  base::MemoryConsumer::UpdateMemoryLimit
  content::ChildMemoryConsumerRegistry::ConsumerGroup::OnUpdateMemoryLimit
  base::MemoryConsumer::UpdateMemoryLimit
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=1554957:1554960

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6257461686108160

Additional requirements: Requires Gestures

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### 24...@project.gserviceaccount.com (2025-12-10)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-12-10)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/3408a49637917700b2bd304ce5a47297fb186839 (Fix config for MemoryCoordinatorLastResortGC

Also add missing OWNERS file.

Bug: 447352454
Change-Id: Ie27fd9f01992ab70978149a46c1d25ddf783a355
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7229062
Commit-Queue: Nate Chapin <japhet@chromium.org>
Auto-Submit: Patrick Monette <pmonette@chromium.org>
Reviewed-by: Francois Pierre Doray <fdoray@chromium.org>
Reviewed-by: Nate Chapin <japhet@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1554960}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### ch...@google.com (2025-12-10)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-12-10)

Setting Priority to P0 to match Severity s0. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### li...@chromium.org (2025-12-10)

This looks like it's in the renderer process so it should be high sev instead of critical. This may also be more of a v8 bug but not 100% sure yet so CCing the v8 shepherd to take a look

### dx...@google.com (2025-12-11)

Project: chromium/src  

Branch:  main  

Author:  Patrick Monette [pmonette@chromium.org](mailto:pmonette@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7248069>

[NGShapeCache] Clean up MemoryPressureListener registration in finalizer

---


Expand for full commit details
```
     
    This ensures the registration is cleared up, avoiding calls to the 
    object after it has been GC'ed. 
     
    Bug: 467474391 
    Change-Id: I250e15dc6cf362ab4d234999f0c6b9b8ffbc3791 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7248069 
    Reviewed-by: Kouhei Ueno <kouhei@chromium.org> 
    Commit-Queue: Patrick Monette <pmonette@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1557132}

```

---

Files:

- M `third_party/blink/renderer/platform/fonts/shaping/ng_shape_cache.h`

---

Hash: [92c94c4c0e4815d6dfd13a667282a6e953ff7ef5](https://chromiumdash.appspot.com/commit/92c94c4c0e4815d6dfd13a667282a6e953ff7ef5)  

Date: Thu Dec 11 06:00:54 2025


---

### 24...@project.gserviceaccount.com (2025-12-11)

ClusterFuzz testcase 6257461686108160 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=1557130:1557132

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### wf...@chromium.org (2025-12-16)

b0ring\_webidl\_fuzzer seems to be owned by inferno@ I'm not sure this is VRP eligible. m.cooolie is this one of yours?

### m....@gmail.com (2025-12-17)

Yes, this is my fuzzer run on CF through chrome-fuzzer-program

<https://bughunters.google.com/about/rules/chrome-friends/5745167867576320/chrome-vulnerability-reward-program-rules#chrome-fuzzer-program>

### sp...@google.com (2025-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $9000.00 for this report.

Rationale for this decision:
baseline memory corruption in a sandboxed process + fuzzer program bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-01-14)

Security Merge Request Consideration: Not requesting merge to dev (M145) because latest trunk commit (1557132) appears to be prior to dev branch point (1568190). If this is incorrect please remove NA-145 from the 'Merge' field and add 145 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-03-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/467474391)*

# Stack-buffer-overflow in spv::Builder::createMatrixConstructor

| Field | Value |
|-------|-------|
| **Issue ID** | [40769704](https://issues.chromium.org/issues/40769704) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P4 |
| **Component** | Internals>GPU>ANGLE, Internals>GPU>Internals |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | cl...@chromium.org |
| **Assignee** | sy...@chromium.org |
| **Created** | 2021-06-01 |
| **Bounty** | $6,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=6215979714281472

Fuzzer: aohelin_ni
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Stack-buffer-overflow WRITE 4
Crash Address: 0x7f4caaada160
Crash State:
  spv::Builder::createMatrixConstructor
  TGlslangToSpvTraverser::visitAggregate
  glslang::TIntermAggregate::traverse
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=849492:849506

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6215979714281472

Issue filed automatically.

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6215979714281472 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### [Deleted User] (2021-06-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-06-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-06-01)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>GPU>Internals]

### [Deleted User] (2021-06-01)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bd...@chromium.org (2021-06-02)

Can someone from the ANGLE component take a look at this?

[Monorail components: Internals>GPU>ANGLE]

### bd...@chromium.org (2021-06-02)

Assigning to @sugoi. @sugoi are you able to triage or take a look at this?

### su...@chromium.org (2021-06-02)

[Empty comment from Monorail migration]

### su...@chromium.org (2021-06-02)

Sending to Geoff for triage.

### su...@chromium.org (2021-06-02)

This isn't launched yet, but might be in 92, so pushing the deadline to M92.

### su...@chromium.org (2021-06-02)

Shabi, could you have a look?

### jm...@chromium.org (2021-06-02)

[Empty comment from Monorail migration]

### jm...@chromium.org (2021-06-02)

Unfortunately I don't think we have anyone left at Google who works on glslang. Maybe we can make a small repro and share upstream.

### sy...@chromium.org (2021-06-03)

FYI: https://github.com/KhronosGroup/glslang/pull/2656

### sy...@chromium.org (2021-06-05)

Fix landed in glslang. Clusterfuzz should be happy when glslang rolls.

### [Deleted User] (2021-06-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-06-05)

ClusterFuzz testcase 6215979714281472 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=889521:889527

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### am...@google.com (2021-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-04)

Congratulations, the VRP Panel has decided to award you $6,000 for this report. $5,000 for the issue + $1,000 fuzzer bonus. Thank you for your efforts in supporting Chrome Fuzzing! 

### ao...@gmail.com (2021-08-05)

Awesome! Thanks :)

### am...@google.com (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-06)

Fighting with sheriffbot because it re-added topanel because I added the wrong label in https://crbug.com/chromium/1215053#c20; for some reason automation didn't work for processing payment (conflict with email address) for this issue. But it has been manually processed and submitted to finance. Adding correct label accordingly. 

### [Deleted User] (2021-09-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1215053?no_tracker_redirect=1

[Multiple monorail components: Internals>GPU>ANGLE, Internals>GPU>Internals]
[Monorail blocking: crbug.com/angleproject/4659]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40769704)*

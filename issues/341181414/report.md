# Container-overflow in blink::QualifiedName::ToString

| Field | Value |
|-------|-------|
| **Issue ID** | [341181414](https://issues.chromium.org/issues/341181414) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>DOM, Blink>SecurityFeature>SanitizerAPI |
| **Platforms** | Linux |
| **Reporter** | m....@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2024-05-18 |
| **Bounty** | $9,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5650292977631232

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_content_shell_drt
Platform Id: linux

Crash Type: Container-overflow READ 8
Crash Address: 0x5040000c1b70
Crash State:
  blink::QualifiedName::ToString
  blink::Sanitizer::KeepElement
  blink::Sanitizer::DoSanitizing
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_content_shell_drt&range=1302889:1302902

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5650292977631232

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### 24...@project.gserviceaccount.com (2024-05-18)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-05-18)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/317e389e62807305b8225431880043343643c7c6 (Avoid materializing an array in Element::getAttributeNames).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### pe...@google.com (2024-05-18)

Setting milestone because of s2 severity.

### pe...@google.com (2024-05-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-05-18)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-05-21)

Project: chromium/src
Branch: main

commit c379df13dae21e899123a26584bb271dd97db809
Author: Andrey Kosyakov <caseq@chromium.org>
Date:   Tue May 21 20:24:17 2024

    Only return TransformedView of element attributes to bindings
    
    ... to avoid surprising callers that may be modifying the underlying
    collection while iterating.
    
    Bug: 341181414
    Change-Id: I0cc5d2f00a8899257d1ba92c2941df47eb0f9689
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5551575
    Reviewed-by: Nate Chapin <japhet@chromium.org>
    Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1304013}

M       third_party/blink/renderer/core/dom/element.cc
M       third_party/blink/renderer/core/dom/element.h
M       third_party/blink/renderer/core/dom/element.idl
M       third_party/blink/renderer/modules/sanitizer_api/sanitizer.cc

https://chromium-review.googlesource.com/5551575


### 24...@project.gserviceaccount.com (2024-05-22)

ClusterFuzz testcase 5650292977631232 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_content_shell_drt&range=1304009:1304024

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### pe...@google.com (2024-05-23)

Requesting merge to beta (M126) because latest trunk commit (1304013) appears to be after beta branch point (1300313).
Merge review required: M126 is already shipping to beta.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pg...@google.com (2024-05-23)

the suspected regression changelist of comment 3 also landed in M127 - updating foundin and labels accordingly

### pe...@google.com (2024-05-24)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M126, which branched on 2024-05-13 (Chromium branch: 6478, Chromium branch position: 1300313)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove TBD-## from the Merge field and replace it with NA-## (where ## corresponds to the milestone under evaluation). If a merge is necessary, the requested milestone(s) to the Merge-Request field. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

### ca...@google.com (2024-05-24)

Removing M126 as the milestone and associated merge TBD-## label, as the culprit of regression [never made its way into M126](https://chromiumdash.appspot.com/commit/317e389e62807305b8225431880043343643c7c6) in the first place.

### m....@gmail.com (2024-06-25)

Can we add VRP-related personnel to this? It seems like the VRP-related flag might not be set correctly.

### am...@chromium.org (2024-06-27)

the flag is correctly set, we've just had a lot of VRP bugs to review lately so we are just getting to this today

### sp...@google.com (2024-06-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $9000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in the renderer / sandboxed process + $2,000 fuzzer bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-28)

Congratulations! Thank you for your efforts and reporting this issue to us, and for your patience as we hacked through the bug queue. 

### pe...@google.com (2024-08-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/341181414)*

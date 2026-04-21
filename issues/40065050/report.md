# CHECK failure: !v8::internal::v8_flags.enable_slow_asserts.value() || (IsSeqOneByteString_NonIn

| Field | Value |
|-------|-------|
| **Issue ID** | [40065050](https://issues.chromium.org/issues/40065050) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 5n...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2023-05-31 |
| **Bounty** | $5,000.00 |

## Description

version:
d8 dev channel:10.4.132.20

build flags:
gn gen out/partinst --args='is_debug=false dcheck_always_on=true v8_static_library=true v8_enable_slow_dchecks=true v8_enable_v8_checks=true v8_enable_verify_heap=true v8_enable_verify_csa=true target_cpu="x64"'

run with:
./d8 2.js

crash info:
#
# Fatal error in gen/torque-generated/src/objects/string-tq-inl.inc, line 375
# Check failed: !v8::internal::v8_flags.enable_slow_asserts.value() || (IsSeqOneByteString_NonInline(*this)).
#
#
#
#FailureMessage Object: 0x7ffcde86c1a0
==== C stack trace ===============================

    /home/r00t/v8_build/partinst/d8(+0x66ca63) [0x5614738e5a63]
    /home/r00t/v8_build/partinst/d8(+0x66c16b) [0x5614738e516b]
    /home/r00t/v8_build/partinst/d8(+0x664859) [0x5614738dd859]
    /home/r00t/v8_build/partinst/d8(+0x7080b0) [0x5614739810b0]
    /home/r00t/v8_build/partinst/d8(+0x18c862e) [0x561474b4162e]
    /home/r00t/v8_build/partinst/d8(+0xed2554) [0x56147414b554]
    /home/r00t/v8_build/partinst/d8(+0xecd28d) [0x56147414628d]
    /home/r00t/v8_build/partinst/d8(+0xecbda3) [0x561474144da3]
    /home/r00t/v8_build/partinst/d8(+0xecf345) [0x561474148345]
    /home/r00t/v8_build/partinst/d8(+0xec88c8) [0x5614741418c8]
    /home/r00t/v8_build/partinst/d8(+0xec875a) [0x56147414175a]
    /home/r00t/v8_build/partinst/d8(+0x7c8dfa) [0x561473a41dfa]
    /home/r00t/v8_build/partinst/d8(+0x29dff36) [0x561475c58f36]

Found by fuzzilli guided fuzzing.

## Attachments

- [2.js](attachments/2.js) (text/plain, 148 B)

## Timeline

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-06-01)

Detailed Report: https://clusterfuzz.com/testcase?key=4973429479112704

Fuzzer: None
Job Type: linux_d8_dbg
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  !v8::internal::v8_flags.enable_slow_asserts.value() || (IsSeqOneByteString_NonIn
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_d8_dbg&revision=88009

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4973429479112704

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### am...@chromium.org (2023-06-01)

renderer memory corruption == sev-high 
hopefully clusterfuzz will soon update with FoundIn- 
assigning to sroettger@ as current V8 security shepherd 

[Monorail components: Blink>JavaScript]

### sr...@google.com (2023-06-02)

CF bisected this to:
6925385d6d38f8a1a5a166ae749bb9adde20786b
"[json-parse-with-source] Ship the proposal"

### [Deleted User] (2023-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-02)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2023-06-05)

While my CL surfaced the bug, it looks like it was introduced by https://chromium-review.googlesource.com/c/v8/v8/+/1647696

### sy...@chromium.org (2023-06-05)

[Empty comment from Monorail migration]

### jg...@chromium.org (2023-06-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/a7e2bef27b72f187a7dcdf95714df686f56d9e0b

commit a7e2bef27b72f187a7dcdf95714df686f56d9e0b
Author: Shu-yu Guo <syg@chromium.org>
Date: Mon Jun 05 23:05:52 2023

Check for encoding when appending in string builder

Fixed: chromium:1450114
Change-Id: I6d1a790b213d24d2737f4b268e8c35ba999f8adf
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4591495
Reviewed-by: Jakob Linke <jgruber@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Commit-Queue: Shu-yu Guo <syg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#88091}

[modify] https://crrev.com/a7e2bef27b72f187a7dcdf95714df686f56d9e0b/src/strings/string-builder.cc


### [Deleted User] (2023-06-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-06)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### 5n...@gmail.com (2023-06-07)

Hi,reporter credit as:

5n1p3r0010

Thanks

### [Deleted User] (2023-06-07)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1450114&entry.364066060=External&entry.958145677=Android&entry.958145677=Chrome&entry.958145677=Fuchsia&entry.958145677=Linux&entry.958145677=Mac&entry.958145677=Windows&entry.958145677=Lacros&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript&entry.975983575=syg@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-07)

Merge review required: M114 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-07)

Merge review required: M115 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-06-07)

ClusterFuzz testcase 4973429479112704 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=88090:88091

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### sy...@chromium.org (2023-06-07)

> 1. Why does your merge fit within the merge criteria for these milestones?
> - Chrome Browser: https://chromiumdash.appspot.com/branches
> - Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

Security issue.

> 2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/v8/v8/+/4591495

> 3. Have the changes been released and tested on canary?

Yes

> 4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No

> 5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A

> 6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No manual testing needed

### am...@chromium.org (2023-06-08)

114 and 115 merges approved for https://chromium-review.googlesource.com/c/v8/v8/+/4591495
please merge this fix to 11.4-lkgr and 11.5-lkgr by EOD tomorrow (Friday 9 June) so this fix can be included in next M114/Stable and M115/Beta -- thank you! 

### gi...@appspot.gserviceaccount.com (2023-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/06955cb7e856f0a45cfaa8bc7b482bcdf3a0a624

commit 06955cb7e856f0a45cfaa8bc7b482bcdf3a0a624
Author: Shu-yu Guo <syg@chromium.org>
Date: Mon Jun 05 23:05:52 2023

Merged: Check for encoding when appending in string builder

Fixed: chromium:1450114
(cherry picked from commit a7e2bef27b72f187a7dcdf95714df686f56d9e0b)

Change-Id: I2c692c385def56a2ee07e5ae902200249e00d470
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4604097
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.5@{#8}
Cr-Branched-From: 0c4044b7336787781646e48b2f98f0c7d1b400a5-refs/heads/11.5.150@{#1}
Cr-Branched-From: b71d3038a7d99c79e1c21239e8ae07da5fc8c90b-refs/heads/main@{#87781}

[modify] https://crrev.com/06955cb7e856f0a45cfaa8bc7b482bcdf3a0a624/src/strings/string-builder.cc


### gi...@appspot.gserviceaccount.com (2023-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/2e76270cf65e13348f8705fc95d6a7580c6174b2

commit 2e76270cf65e13348f8705fc95d6a7580c6174b2
Author: Shu-yu Guo <syg@chromium.org>
Date: Mon Jun 05 23:05:52 2023

Merged: Check for encoding when appending in string builder

Fixed: chromium:1450114
(cherry picked from commit a7e2bef27b72f187a7dcdf95714df686f56d9e0b)

Change-Id: I5838383b6b12d137e84c8a36863ef88000e85c76
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4604652
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.4@{#41}
Cr-Branched-From: 8a8a1e7086dacc426965d3875914efa66663c431-refs/heads/11.4.183@{#1}
Cr-Branched-From: 5483d8e816e0bbce865cbbc3fa0ab357e6330bab-refs/heads/main@{#87241}

[modify] https://crrev.com/2e76270cf65e13348f8705fc95d6a7580c6174b2/src/strings/string-builder.cc


### jk...@chromium.org (2023-06-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-06-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-13)

[Empty comment from Monorail migration]

### sa...@google.com (2023-06-13)

Thanks for using Fuzzilli!

### pg...@google.com (2023-06-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-16)

Congratulations  5n1p3r0010! The VRP Panel has decided to award you $5,000 for this report. The reward amount was decided based on the potential for memory corruption in the renderer, however this report was lacking a full stack trace and any analysis of the issue being reported. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-17)

[Empty comment from Monorail migration]

### gm...@google.com (2023-07-19)

[Empty comment from Monorail migration]

### rz...@google.com (2023-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-20)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-07-20)

1. Just https://crrev.com/c/4701649
2. Low, no conflicts
3. 114, 115
4. Yes

### gm...@google.com (2023-07-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/beb241e62e5b09c0067cac50fc91afa0fd9d7d3c

commit beb241e62e5b09c0067cac50fc91afa0fd9d7d3c
Author: Shu-yu Guo <syg@chromium.org>
Date: Mon Jun 05 23:05:52 2023

[M108-LTS] Check for encoding when appending in string builder

(cherry picked from commit a7e2bef27b72f187a7dcdf95714df686f56d9e0b)

Fixed: chromium:1450114
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Change-Id: I6d1a790b213d24d2737f4b268e8c35ba999f8adf
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4591495
Commit-Queue: Shu-yu Guo <syg@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#88091}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4701649
Reviewed-by: Shu-yu Guo <syg@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/10.8@{#80}
Cr-Branched-From: f1bc03fd6b4c201abd9f0fd9d51fb989150f97b9-refs/heads/10.8.168@{#1}
Cr-Branched-From: 237de893e1c0a0628a57d0f5797483d3add7f005-refs/heads/main@{#83672}

[modify] https://crrev.com/beb241e62e5b09c0067cac50fc91afa0fd9d7d3c/src/strings/string-builder.cc


### rz...@google.com (2023-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1450114?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065050)*

# use-after-poison local_frame_view.cc:816 in blink::LocalFrameView::PerformLayout

| Field | Value |
|-------|-------|
| **Issue ID** | [40060643](https://issues.chromium.org/issues/40060643) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Internals>Frames |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | sz...@chromium.org |
| **Created** | 2022-08-22 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

#TestOn  

asan-win32-release\_x64-1037582

#Reproduce  

chrome --no-sandbox --user-data-dir=test --enable-logging=stderr poc.html

**Problem Description:**  

#Type of crash  

render tab

#Analysis  

Coming soon

# **Additional Comments:** #asan

==8700==ERROR: AddressSanitizer: use-after-poison on address 0x7edf801d7c88 at pc 0x7ffa227b9aaa bp 0x00855c5fd3a0 sp 0x00855c5fd3e8  

READ of size 4 at 0x7edf801d7c88 thread T0  

==8700==WARNING: Failed to use and restart external symbolizer!  

==8700==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==8700==\*\*\* Most likely this means that the app is already \*\*\*  

==8700==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==8700==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==8700==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ffa227b9aa9 in blink::LocalFrameView::PerformLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:816  

#1 0x7ffa227bad4c in blink::LocalFrameView::UpdateLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:910  

#2 0x7ffa227dd885 in blink::LocalFrameView::UpdateStyleAndLayoutInternal C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3288  

#3 0x7ffa227c4a6c in blink::LocalFrameView::UpdateStyleAndLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3224  

#4 0x7ffa2289fdcb in blink::Document::UpdateStyleAndLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2612  

#5 0x7ffa228a62ec in blink::Document::EnsurePaintLocationDataValidForNode C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2711  

#6 0x7ffa22f5bf61 in blink::HTMLElement::offsetTopForBinding C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\html\_element.cc:1846  

#7 0x7ffa2ebf4b92 in blink::`anonymous namespace'::v8\_html\_element::OffsetTopAttributeGetCallback C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\renderer\bindings\modules\v8\v8\_html\_element.cc:625  

#8 0x7ff9bfe4d46c (<unknown module>)

Address 0x7edf801d7c88 is a wild pointer inside of access range of size 0x000000000004.  

SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:816 in blink::LocalFrameView::PerformLayout  

Shadow bytes around the buggy address:  

0x123f9e33af40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x123f9e33af50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x123f9e33af60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x123f9e33af70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x123f9e33af80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x123f9e33af90: 00[f7]00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x123f9e33afa0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x123f9e33afb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x123f9e33afc0: 00 00 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x123f9e33afd0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x123f9e33afe0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==8700==ABORTING

\*\*Chrome version: \*\* asan-win32-release\_x64-1037582 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- asan.txt (text/plain, 3.6 KB)
- [poc.html](attachments/poc.html) (text/plain, 4.1 KB)

## Timeline

### [Deleted User] (2022-08-22)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-08-22)

Detailed Report: https://clusterfuzz.com/testcase?key=5255856751050752

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Use-after-poison READ 4
Crash Address: 0x7ea080154e20
Crash State:
...see report...
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1037664

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5255856751050752

### sr...@google.com (2022-08-23)

[Empty comment from Monorail migration]

### sr...@google.com (2022-08-23)

The minimized testcase from clusterfuzz reproduces on 105.0.5195.37 for me.
szager@, assigning to you since you touched blink::LocalFrameView::PerformLayout last and I hope you're familiar with the code. Could you take a look at this?


[Monorail components: Blink>Internals>Frames]

### [Deleted User] (2022-08-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-23)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sz...@chromium.org (2022-08-23)

m.coolie@ -- I can't access the clusterfuzz issue, is there a separate bug report for it?

### m....@gmail.com (2022-08-24)

re https://crbug.com/chromium/1355237#c09 No, I just want to do Bisect (identification of the commit or commit range that introduced the bug) by CF.



### [Deleted User] (2022-08-30)

[Empty comment from Monorail migration]

### sz...@chromium.org (2022-09-01)

I have a fix in review:

https://chromium-review.googlesource.com/c/chromium/src/+/3864877

### gi...@appspot.gserviceaccount.com (2022-09-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/815aa5ca03ab4ecc619b2d2ad7650531bd3892a8

commit 815aa5ca03ab4ecc619b2d2ad7650531bd3892a8
Author: Stefan Zager <szager@chromium.org>
Date: Thu Sep 01 04:28:49 2022

Fix for reference to invalid iterator

Evidently, LocalFrameView::layout_subtree_root_list_ can be modified
during LayoutFromRootObject, leaving the loop variable in an invalid
state. I don't know the exact sequence, but the test case crashes for
me without this patch, and doesn't crash with the patch.

Bug: 1355237
Change-Id: Ib17b1fac5b2ec060eda39be76305db18075802fa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3864877
Reviewed-by: Ian Kilpatrick <ikilpatrick@chromium.org>
Commit-Queue: Stefan Zager <szager@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1041903}

[modify] https://crrev.com/815aa5ca03ab4ecc619b2d2ad7650531bd3892a8/third_party/blink/renderer/core/frame/local_frame_view.cc


### sz...@chromium.org (2022-09-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

Requesting merge to stable M105 because latest trunk commit (1041903) appears to be after stable branch point (1027018).

Requesting merge to beta M106 because latest trunk commit (1041903) appears to be after beta branch point (1036826).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-07)

Merge review required: M106 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-07)

Merge review required: M105 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2022-09-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-09-08)

AFAICT, this fix should also be backmerged to M104/extended as well as M105/stable, please merge this fix to 104 (branch 5112) and 105 (branch 5195) ASAP - by 10am PDT tomorrow, Friday, 9 September so this fix can be included in the next stable and extended stable security respins 

merge also approved to M106/beta, please merge to branch 5249 at your earliest convenience 

thanks! 

### pb...@google.com (2022-09-08)

This merge has been approved for M105, please help complete your merges asap (before 4pm PST) today, so the change can be included in next weeks RC build for Stable releases.

### sr...@google.com (2022-09-08)

I have created the CP's for M104/M105/M106 here  and running through dry-run CQ

104-https://chromium-review.googlesource.com/c/chromium/src/+/3884238
105-https://chromium-review.googlesource.com/c/chromium/src/+/3884119
106- https://chromium-review.googlesource.com/c/chromium/src/+/3883961

Please +1 the CL's and help them land. 

### gi...@appspot.gserviceaccount.com (2022-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cc9b711e779f102804df3e500cd5272e838ed632

commit cc9b711e779f102804df3e500cd5272e838ed632
Author: Stefan Zager <szager@chromium.org>
Date: Thu Sep 08 20:58:17 2022

Fix for reference to invalid iterator

Evidently, LocalFrameView::layout_subtree_root_list_ can be modified
during LayoutFromRootObject, leaving the loop variable in an invalid
state. I don't know the exact sequence, but the test case crashes for
me without this patch, and doesn't crash with the patch.

(cherry picked from commit 815aa5ca03ab4ecc619b2d2ad7650531bd3892a8)

Bug: 1355237
Change-Id: Ib17b1fac5b2ec060eda39be76305db18075802fa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3864877
Reviewed-by: Ian Kilpatrick <ikilpatrick@chromium.org>
Commit-Queue: Stefan Zager <szager@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1041903}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3884119
Auto-Submit: Srinivas Sista <srinivassista@chromium.org>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Reviewed-by: Stefan Zager <szager@chromium.org>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5195@{#1087}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[modify] https://crrev.com/cc9b711e779f102804df3e500cd5272e838ed632/third_party/blink/renderer/core/frame/local_frame_view.cc


### gi...@appspot.gserviceaccount.com (2022-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/eb4d31309df7e555e928388778fe8a0801b4ede6

commit eb4d31309df7e555e928388778fe8a0801b4ede6
Author: Stefan Zager <szager@chromium.org>
Date: Fri Sep 09 01:56:46 2022

Fix for reference to invalid iterator

Evidently, LocalFrameView::layout_subtree_root_list_ can be modified
during LayoutFromRootObject, leaving the loop variable in an invalid
state. I don't know the exact sequence, but the test case crashes for
me without this patch, and doesn't crash with the patch.

(cherry picked from commit 815aa5ca03ab4ecc619b2d2ad7650531bd3892a8)

Bug: 1355237
Change-Id: Ib17b1fac5b2ec060eda39be76305db18075802fa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3864877
Reviewed-by: Ian Kilpatrick <ikilpatrick@chromium.org>
Commit-Queue: Stefan Zager <szager@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1041903}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3884238
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Auto-Submit: Srinivas Sista <srinivassista@chromium.org>
Reviewed-by: Stefan Zager <szager@chromium.org>
Cr-Commit-Position: refs/branch-heads/5112@{#1566}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/eb4d31309df7e555e928388778fe8a0801b4ede6/third_party/blink/renderer/core/frame/local_frame_view.cc


### sr...@google.com (2022-09-12)

Merge for M106 is approved, Please complete your merges asap so these changes can be included in this weeks beta release. Beta RC will be cut on Sept 13 (tuesday) at 3pm PST. 

Next week is M106 stable RC, so I would like to ensure all these CL's have good coverage before RC cut

If the merge is compelete and not linked to this bug, please drop the merge-approved-106 label 

### [Deleted User] (2022-09-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-09-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a92c31e5a8c6da324d8226358b6038d8d6b6845b

commit a92c31e5a8c6da324d8226358b6038d8d6b6845b
Author: Stefan Zager <szager@chromium.org>
Date: Tue Sep 13 19:53:48 2022

Fix for reference to invalid iterator

Evidently, LocalFrameView::layout_subtree_root_list_ can be modified
during LayoutFromRootObject, leaving the loop variable in an invalid
state. I don't know the exact sequence, but the test case crashes for
me without this patch, and doesn't crash with the patch.

(cherry picked from commit 815aa5ca03ab4ecc619b2d2ad7650531bd3892a8)

Bug: 1355237
Change-Id: Ib17b1fac5b2ec060eda39be76305db18075802fa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3864877
Reviewed-by: Ian Kilpatrick <ikilpatrick@chromium.org>
Commit-Queue: Stefan Zager <szager@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1041903}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3883961
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Reviewed-by: Stefan Zager <szager@chromium.org>
Auto-Submit: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5249@{#434}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/a92c31e5a8c6da324d8226358b6038d8d6b6845b/third_party/blink/renderer/core/frame/local_frame_view.cc


### am...@google.com (2022-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-22)

Congratulations! The VRP Panel has decided to award you $7,000 for this report + $2,000 fuzzer bonus (as your fuzzer did find this issue in tandem to your manual report) for a total of $9,000 reward. Thank you for your efforts toward Chrome Fuzzing and great work! 

### am...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1355237?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1355512]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060643)*

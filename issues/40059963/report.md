# Security DCHECK failure: IsA<Derived>(from) in casting.h

| Field | Value |
|-------|-------|
| **Issue ID** | [40059963](https://issues.chromium.org/issues/40059963) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Linux, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | fu...@chromium.org |
| **Created** | 2022-06-14 |
| **Bounty** | $5,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=6396966137430016

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  IsA<Derived>(from) in casting.h
  blink::LayoutListMarker::ListItem
  blink::LayoutListMarker::IsInside
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1013857

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6396966137430016

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Attachments

- [clusterfuzz-testcase-minimized-6396966137430016.html](attachments/clusterfuzz-testcase-minimized-6396966137430016.html) (text/plain, 203 B)
- [tc.html](attachments/tc.html) (text/plain, 121 B)

## Timeline

### [Deleted User] (2022-06-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-06-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-15)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-06-21)

[Empty comment from Monorail migration]

### aj...@google.com (2022-06-21)

CC some owners in Blink>Layout.

[Monorail components: Blink>Layout]

### tk...@chromium.org (2022-06-21)

obrufau@, can you take a look at this?



### ms...@chromium.org (2022-06-22)

Issue with legacy fallback with container queries.
Attaching cleaned up test.

### fu...@chromium.org (2022-06-22)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-06-22)

This requires an experimental flag to be enabled for impact in M104, but not behind a flag in M105.


### ob...@chromium.org (2022-06-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a3a4da874d6ffe5fd5e53749850a10e251209c60

commit a3a4da874d6ffe5fd5e53749850a10e251209c60
Author: Rune Lillesveen <futhark@chromium.org>
Date: Wed Jun 22 13:01:54 2022

[@container] Ensure list-item and marker are NG or legacy

Legacy fallback for table inside multicol may mark size container
list-items for legacy fallback without re-attaching. Check the list-item
box type when creating the marker object as they need to be both either
NG or legacy.

Bug: 1336334
Change-Id: I8959b490d3dcaa498a91d3dd288676f8d714b370
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3718030
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Reviewed-by: Morten Stenshorne <mstensho@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1016674}

[add] https://crrev.com/a3a4da874d6ffe5fd5e53749850a10e251209c60/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/crashtests/table-in-columns-005-crash.html
[modify] https://crrev.com/a3a4da874d6ffe5fd5e53749850a10e251209c60/third_party/blink/renderer/core/layout/layout_object_factory.cc


### fu...@chromium.org (2022-06-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-22)

Requesting merge to dev M104 because latest trunk commit (1016674) appears to be after dev branch point (1012729).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2022-06-22)

ClusterFuzz testcase 6396966137430016 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1016670:1016675

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-06-23)

Merge review required: M104 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fu...@chromium.org (2022-06-23)

No need for merging to M104 since it is behind a flag in that release.

### sr...@google.com (2022-06-27)

dropping review label per https://crbug.com/chromium/1336334#c18

### am...@google.com (2022-07-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-06)

Congratulations! The VRP Panel has decided to award you $5,000 for this report + $1,000 fuzzer bonus. Thank you for your efforts in Chrome Fuzzing and nice work! 

### am...@chromium.org (2022-07-08)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1336334?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059963)*

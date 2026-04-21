# Heap-use-after-free in ui::AXTreeSerializer<blink::AXObject*>::AnyDescendantWasReparented

| Field | Value |
|-------|-------|
| **Issue ID** | [40065256](https://issues.chromium.org/issues/40065256) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Accessibility, Internals>Accessibility |
| **Platforms** | Linux |
| **Reporter** | m....@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2023-06-03 |
| **Bounty** | $7,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5405225089957888

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_content_shell_drt
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x506000208f48
Crash State:
  ui::AXTreeSerializer<blink::AXObject*>::AnyDescendantWasReparented
  ui::AXTreeSerializer<blink::AXObject*>::AnyDescendantWasReparented
  ui::AXTreeSerializer<blink::AXObject*>::SerializeChanges
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_content_shell_drt&range=1152210:1152215

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5405225089957888

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Attachments

- [test3.html](attachments/test3.html) (text/plain, 87 B)

## Timeline

### [Deleted User] (2023-06-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-04)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2023-06-06)

[Comment Deleted]

### ca...@chromium.org (2023-06-06)

[Empty comment from Monorail migration]

### ca...@chromium.org (2023-06-06)

chrishtr: Can you PTAL? This looks like it might be related to crrev.com/c/4568365 in the regression range. Thanks

### ca...@chromium.org (2023-06-06)

[Empty comment from Monorail migration]

[Monorail components: Blink>Accessibility]

### cl...@chromium.org (2023-06-06)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Accessibility]

### ch...@chromium.org (2023-06-07)

[Empty comment from Monorail migration]

### ch...@chromium.org (2023-06-07)

Reduced testcase attached.

### ch...@chromium.org (2023-06-07)

Debugging CL: https://chromium-review.googlesource.com/c/chromium/src/+/4599813

### ch...@chromium.org (2023-06-07)

[Empty comment from Monorail migration]

### ch...@chromium.org (2023-06-09)

The root cause is that we are failing to invalidate the AX subtree in when nodes edit the flat tree, here:

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/dom/node.cc;l=3406

### al...@chromium.org (2023-06-11)

WIP:https://chromium-review.googlesource.com/c/chromium/src/+/4605033

### gi...@appspot.gserviceaccount.com (2023-06-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/317e9ba1b1d83d1b5d454ae236c1a0feaf1ffd0e

commit 317e9ba1b1d83d1b5d454ae236c1a0feaf1ffd0e
Author: Aaron Leventhal <aleventhal@google.com>
Date: Mon Jun 12 23:42:01 2023

[A11y] Remove subtrees of nodes removed from flat tree.

Create a method called RemoveSubtreeWhenSafe() that removes subtrees as
soon as it is safe to traverse the flat tree, so that there can be no
orphaned objects left in the cache.

Specifically, "when safe" means:
1) If CanSafelyUseFlatTraversal() returns true, do it now (flat
traversal is not forbidden and there are no pending slot assignments
2) Otherwise, do it towards the beginning of a11y's clean layout
processing. This may be later than necessary -- we may consider having
a special callback that occurs as soon as flat traversal is safe.

Bug: none
Cq-Include-Trybots: luci.chrome.try:chromeos-eve-chrome;luci.chromium.try:linux-rel;luci.chromium.try:linux-lacros-rel,fuchsia-x64-accessibility-rel,fuchsia-x64-rel,linux-bfcache-rel,linux-rel

Bug: 1451115
Change-Id: Ifeef4a50213b41e9598645bca2b8cc8a356a5c46
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4605033
Commit-Queue: Chris Harrelson <chrishtr@chromium.org>
Reviewed-by: Mason Freed <masonf@chromium.org>
Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
Auto-Submit: Aaron Leventhal <aleventhal@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1156556}

[modify] https://crrev.com/317e9ba1b1d83d1b5d454ae236c1a0feaf1ffd0e/third_party/blink/renderer/modules/accessibility/ax_object_cache_impl.h
[modify] https://crrev.com/317e9ba1b1d83d1b5d454ae236c1a0feaf1ffd0e/third_party/blink/renderer/core/accessibility/ax_object_cache.h
[add] https://crrev.com/317e9ba1b1d83d1b5d454ae236c1a0feaf1ffd0e/third_party/blink/web_tests/virtual/force-renderer-accessibility-parser-yield-and-delay-often/README.md
[modify] https://crrev.com/317e9ba1b1d83d1b5d454ae236c1a0feaf1ffd0e/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/317e9ba1b1d83d1b5d454ae236c1a0feaf1ffd0e/third_party/blink/renderer/modules/accessibility/ax_object_cache_impl.cc
[modify] https://crrev.com/317e9ba1b1d83d1b5d454ae236c1a0feaf1ffd0e/third_party/blink/web_tests/VirtualTestSuites
[modify] https://crrev.com/317e9ba1b1d83d1b5d454ae236c1a0feaf1ffd0e/third_party/blink/renderer/modules/accessibility/ax_object.cc
[add] https://crrev.com/317e9ba1b1d83d1b5d454ae236c1a0feaf1ffd0e/third_party/blink/web_tests/external/wpt/accessibility/crashtests/removed-from-flat-tree.html
[modify] https://crrev.com/317e9ba1b1d83d1b5d454ae236c1a0feaf1ffd0e/third_party/blink/renderer/core/dom/node.cc


### ch...@chromium.org (2023-06-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-06-21)

ClusterFuzz testcase 5405225089957888 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the ClusterFuzz-Wrong label.

### [Deleted User] (2023-06-23)

Not requesting merge to dev (M116) because latest trunk commit (1156556) appears to be prior to dev branch point (1160321). If this is incorrect, please replace the Merge-NA-116 label with Merge-Request-116. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge approved: your change passed merge requirements and is auto-approved for M116. Please go ahead and merge the CL to branch 5845 (refs/branch-heads/5845) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-24)

Congratulations! The VRP Panel has decided to award you $7,000 for this report + $2,000 fuzzer bonus. Thank you for your efforts toward fuzzing Chrome that resulted in this finding! 

### am...@chromium.org (2023-06-26)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-27)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-03)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@google.com (2023-07-12)

Removing Merge-Approval label given c#19 message that it should already be included in branch.

### [Deleted User] (2023-09-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1451115?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Accessibility, Internals>Accessibility]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065256)*

# Heap-use-after-free in blink::LayoutListItem::UpdateMarkerLocation

| Field | Value |
|-------|-------|
| **Issue ID** | [40052201](https://issues.chromium.org/issues/40052201) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ob...@igalia.com |
| **Created** | 2020-05-05 |
| **Bounty** | $6,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5733377792081920

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0xe289ce4c
Crash State:
  blink::LayoutListItem::UpdateMarkerLocation
  blink::LayoutListItem::SubtreeDidChange
  blink::LayoutObject::HandleSubtreeModifications
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_v8_arm&range=745011:745012

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5733377792081920

Issue filed automatically.

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5733377792081920 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### oc...@google.com (2020-05-06)

Regression range points directly to https://chromium-review.googlesource.com/c/chromium/src/+/2066747.

obrufau, could you please take a look?

[Monorail components: Blink>Layout]

### ob...@igalia.com (2020-05-06)

I can reproduce the heap-use-after-free when compiling content_shell with

    enable_ipc_fuzzer = true
    enable_nacl = false
    ffmpeg_branding = "Chrome"
    is_asan = true
    is_component_build = false
    is_debug = false
    proprietary_codecs = true
    use_goma = true
    v8_enable_verify_heap = true

and loading this testcase with --disable-blink-features=LayoutNG

    <!DOCTYPE html>
    <style>
    #target::before {
      content: "";
      display: list-item;
      list-style-position: inside;
    }
    #target.foo::before {
      column-width: 100px;
    }
    </style>
    <div id="target"></div>
    <script>
    document.body.offsetLeft;
    target.classList.add("foo");
    </script>

### [Deleted User] (2020-05-06)

Setting milestone and target because of Security_Impact=Beta and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-06)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-06)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ob...@igalia.com (2020-05-06)

I have found the cause, will fix soon.

### sr...@google.com (2020-05-06)

obrufau@ thank you, please help get the fix landed on master soon and verify so that we can get the merge to M83 by next monday. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c2a2b61a37a28c0c9c750bf0c26600192edac946

commit c2a2b61a37a28c0c9c750bf0c26600192edac946
Author: Oriol Brufau <obrufau@igalia.com>
Date: Thu May 07 11:50:44 2020

[css-pseudo] Fix legacy ::marker originated by pseudo-element multicol

This patch fixes a heap-use-after-free in legacy layout when having a
an inside ::marker originated by a ::before or ::after pseudo-element
which is dynamically converted into a multicol container.

The problem was caused by some code that was aiming to prevent the
::marker from being placed after the generated contents of the ::before
or ::after. To do so, it reinserted the ::marker as the first child of
the originating list item. The problem was that, in the multicol case,
the LayoutInsideListMarker is a descendant (not a child) of the
LayoutListItem, since there are a LayoutMultiColumnFlowThread and a
LayoutBlockFlow between them.

Therefore, this patch reinserts the ::marker as the first child of its
parent, instead of as the first child of the list item.

BUG=1078236

TEST=third_party/blink/web_tests/external/wpt/css/css-multicol/multicol-list-item-002.html

Change-Id: I580e4730d6e8ec6d41e423d0d027f67de4d48fa5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2185030
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Commit-Queue: Oriol Brufau <obrufau@igalia.com>
Cr-Commit-Position: refs/heads/master@{#766374}

[modify] https://crrev.com/c2a2b61a37a28c0c9c750bf0c26600192edac946/third_party/blink/renderer/core/layout/layout_list_item.cc
[add] https://crrev.com/c2a2b61a37a28c0c9c750bf0c26600192edac946/third_party/blink/web_tests/external/wpt/css/css-multicol/multicol-list-item-002-ref.html
[add] https://crrev.com/c2a2b61a37a28c0c9c750bf0c26600192edac946/third_party/blink/web_tests/external/wpt/css/css-multicol/multicol-list-item-002.html


### ob...@igalia.com (2020-05-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-07)

[Empty comment from Monorail migration]

### sr...@google.com (2020-05-07)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-07)

This bug requires manual review: To minimize risk and increase branch stability, all merge requests are being reviewed manually by the release team.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-05-07)

ClusterFuzz testcase 5142373900812288 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_ubsan_vptr_chrome&range=766373:766374

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### ob...@igalia.com (2020-05-08)

1. Does your merge fit within the Merge Decision Guidelines?
Yes, I think M83 is in phase 2, and "The bug is considered either release blocking or considered a high-impact regression" applies.

Full automated unit test coverage: tested by external/wpt/css/css-multicol/multicol-list-item-002.html
Deployed in Canary for at least 24 hours: yes
Safe Merge: yes

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/2187574

3. Has the change landed and been verified on master/ToT?
Yes, see https://crbug.com/chromium/1078236#c14.

4. Why are these changes required in this milestone after branch?
To fix a heap-use-after-free when you have a ::before or ::after which is a list item with an inside marker, and after being laid out it's dynamically turned into a multicol container.

5. Is this a new feature?
No, it's a heap-use-after-free fix.

6. If it is a new feature, is it behind a flag using finch?
-

### sr...@google.com (2020-05-08)

Merge approved for M-83 branch:4103 please merge your changes asap

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4c46391b425a35f70b75d45990a27aba0e10dd60

commit 4c46391b425a35f70b75d45990a27aba0e10dd60
Author: Oriol Brufau <obrufau@igalia.com>
Date: Fri May 08 19:26:48 2020

[css-pseudo] Fix legacy ::marker originated by pseudo-element multicol

This patch fixes a heap-use-after-free in legacy layout when having a
an inside ::marker originated by a ::before or ::after pseudo-element
which is dynamically converted into a multicol container.

The problem was caused by some code that was aiming to prevent the
::marker from being placed after the generated contents of the ::before
or ::after. To do so, it reinserted the ::marker as the first child of
the originating list item. The problem was that, in the multicol case,
the LayoutInsideListMarker is a descendant (not a child) of the
LayoutListItem, since there are a LayoutMultiColumnFlowThread and a
LayoutBlockFlow between them.

Therefore, this patch reinserts the ::marker as the first child of its
parent, instead of as the first child of the list item.

BUG=1078236

TEST=third_party/blink/web_tests/external/wpt/css/css-multicol/multicol-list-item-002.html

(cherry picked from commit c2a2b61a37a28c0c9c750bf0c26600192edac946)

Change-Id: I580e4730d6e8ec6d41e423d0d027f67de4d48fa5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2185030
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Commit-Queue: Oriol Brufau <obrufau@igalia.com>
Cr-Original-Commit-Position: refs/heads/master@{#766374}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2187574
Cr-Commit-Position: refs/branch-heads/4103@{#490}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/4c46391b425a35f70b75d45990a27aba0e10dd60/third_party/blink/renderer/core/layout/layout_list_item.cc
[modify] https://crrev.com/4c46391b425a35f70b75d45990a27aba0e10dd60/third_party/blink/web_tests/TestExpectations
[add] https://crrev.com/4c46391b425a35f70b75d45990a27aba0e10dd60/third_party/blink/web_tests/external/wpt/css/css-multicol/multicol-list-item-002-ref.html
[add] https://crrev.com/4c46391b425a35f70b75d45990a27aba0e10dd60/third_party/blink/web_tests/external/wpt/css/css-multicol/multicol-list-item-002.html


### na...@google.com (2020-05-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-05-14)

Congrats! The Panel decided to award $6,000 for this report. 

### na...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1078236?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/457718]
[Monorail mergedwith: crbug.com/chromium/1079195]
[Monorail components added to Component Tags custom field.]

### rb...@chromium.org (2024-03-12)

Bulk editing assignee to correct for crbug.com/324827398

### ja...@chromium.org (2024-03-12)

Updating the status on this bug to Fixed (Verified) as this looks like it was reopened unintentionally.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052201)*

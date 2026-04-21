# Heap-buffer-overflow in blink::LayoutTable::AddColumn

| Field | Value |
|-------|-------|
| **Issue ID** | [40054845](https://issues.chromium.org/issues/40054845) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>Layout>Table |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | cl...@chromium.org |
| **Assignee** | at...@chromium.org |
| **Created** | 2021-02-14 |
| **Bounty** | $5,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5201403786887168

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0xf1509278
Crash State:
  blink::LayoutTable::AddColumn
  blink::LayoutTableCol::InsertedIntoTree
  blink::LayoutObjectChildList::InsertChildNode
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_v8_arm&range=853600:853618

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5201403786887168

Issue filed automatically.

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5201403786887168 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Attachments

- [tc.html](attachments/tc.html) (text/plain, 217 B)
- [tc2.html](attachments/tc2.html) (text/plain, 244 B)

## Timeline

### cl...@chromium.org (2021-02-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-02-14)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Layout]

### cl...@chromium.org (2021-02-14)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/ba2b0737788e60e133cbd4b17cf653eb3f9e9b9e ([GridNG] Resolve both min-length & max-length for auto repetitions.).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### [Deleted User] (2021-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-14)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-02-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ik...@chromium.org (2021-02-14)

[Empty comment from Monorail migration]

### at...@chromium.org (2021-02-14)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Layout Blink>Layout>Table]

### at...@chromium.org (2021-02-14)

Root cause is violation of "Only NG table parts inside NG Tables".
LayoutTableColumn gets created inside LayoutNGTable.
Lots of tricky stuff going on with forcing/unforcing legacy layout inside element.cc, this might take a while to unpack.

### ms...@chromium.org (2021-02-15)

I get this instead:

Received signal 11 SEGV_MAPERR 0000000002e0
#0 0x7f4411d95a49 base::debug::CollectStackTrace()
#1 0x7f4411c95ae3 base::debug::StackTrace::StackTrace()
#2 0x7f4411d955a1 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#3 0x7f4406c5b140 (/lib/x86_64-linux-gnu/libpthread-2.31.so+0x1413f)
#4 0x7f440d2965fb blink::LayoutObject::MarkContainerChainForOverflowRecalcIfNeeded()
#5 0x7f440d2964ed blink::LayoutObject::SetNeedsOverflowRecalc()
#6 0x7f440cae192e blink::LayoutObject::SetNeedsLayout()
#7 0x7f440d2a25ec blink::LayoutObjectChildList::InsertChildNode()
#8 0x7f440d28d7c0 blink::LayoutObject::AddChild()
#9 0x7f440d4510c9 blink::LayoutNGTable::AddChild()
#10 0x7f440cb9c33d blink::LayoutTreeBuilderForElement::CreateLayoutObject()
#11 0x7f440cb5f0d6 blink::Element::AttachLayoutTree()

But that's probably because I'm not using an asan build, and hopefully it's the same issue.

Introduced by https://chromium-review.googlesource.com/c/chromium/src/+/2687617

### ms...@chromium.org (2021-02-15)

[Empty comment from Monorail migration]

### at...@chromium.org (2021-02-15)

https://chromium-review.googlesource.com/c/chromium/src/+/2692390

### at...@chromium.org (2021-02-15)

The fix in my CL does not fix your test case. Investigating...

### ms...@chromium.org (2021-02-15)

The problem here is that initially both the table and colgroup require legacy fallback, because of the "columns" declaration. When removing the "columns" declaration from the table, the table no longer requires legacy fallback, but the colgroup child still does (but we don't check, since nothing changed there), and since they make up the same table, we cannot start using NG for the table. But we do.

One observation is that "columns" don't really apply to table or table-column-group at all [1], so forcing legacy in the first place isn't really necessary. Then again, "columns" is allowed for table-cell, so I'm not sure if it can be fixed this way.

[1] https://www.w3.org/TR/css-multicol-1/#cc

### ms...@chromium.org (2021-02-15)

> One observation is that "columns" don't really apply to table or table-column-group at all [1], so forcing legacy in the first place isn't really necessary. Then again, "columns" is allowed for table-cell, so I'm not sure if it can be fixed this way.

Nope. Seems problematic. Adding new test.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dcd7b566693c8dbbe9f04b5754a6ea6d73c5dcec

commit dcd7b566693c8dbbe9f04b5754a6ea6d73c5dcec
Author: Aleks Totic <atotic@chromium.org>
Date: Tue Feb 16 00:10:50 2021

[TablesNG] clusterfuzz multicol causes illegal table layout trees

The cause of the crash is legacy LayoutTableColumn inside
LayoutNGTable. This triggers bad typecast, wrong methods get called...

The fix is to propagate SetShouldForceLegacyLayoutForChild
correctly. It was only propagating until it found parent
with legacy layout.

Note: SetShouldForceLegacyLayoutForChild flag never gets cleared.

Also added DCHECKs to detect mixed table trees earlier.

Bug: 1178263
Change-Id: Ifebaaccbad4006819ca66fed8310ddeb59e1aa64
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2692390
Commit-Queue: Aleks Totic <atotic@chromium.org>
Reviewed-by: Morten Stenshorne <mstensho@chromium.org>
Cr-Commit-Position: refs/heads/master@{#854106}

[modify] https://crrev.com/dcd7b566693c8dbbe9f04b5754a6ea6d73c5dcec/third_party/blink/renderer/core/layout/ng/table/layout_ng_table.cc
[add] https://crrev.com/dcd7b566693c8dbbe9f04b5754a6ea6d73c5dcec/third_party/blink/web_tests/external/wpt/css/css-tables/crashtests/legacy_ng_mix_crash.html
[modify] https://crrev.com/dcd7b566693c8dbbe9f04b5754a6ea6d73c5dcec/third_party/blink/renderer/core/dom/element.cc
[modify] https://crrev.com/dcd7b566693c8dbbe9f04b5754a6ea6d73c5dcec/third_party/blink/renderer/core/layout/layout_table_section.h
[modify] https://crrev.com/dcd7b566693c8dbbe9f04b5754a6ea6d73c5dcec/third_party/blink/renderer/core/layout/layout_table_row.h
[modify] https://crrev.com/dcd7b566693c8dbbe9f04b5754a6ea6d73c5dcec/third_party/blink/renderer/core/layout/layout_table.h


### at...@chromium.org (2021-02-16)

[Empty comment from Monorail migration]

### at...@chromium.org (2021-02-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-02-16)

ClusterFuzz testcase 6145276621160448 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=854100:854124

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### am...@google.com (2021-03-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-11)

Congratulations, attekett@! The VRP Panel has decided to award you $5,000 for this issue + $1000 fuzzer bonus, since your fuzzer discover this issue, for a total reward of $6,000. Thank you for your contributions to Chrome Fuzzing and nice work! 


### am...@google.com (2021-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1178263?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1178440]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054845)*

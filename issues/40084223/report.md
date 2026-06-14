# Heap-use-after-free in blink::LayoutObject::containingBlock

| Field | Value |
|-------|-------|
| **Issue ID** | [40084223](https://issues.chromium.org/issues/40084223) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Editing>Selection, Blink>HTML>Meter |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2016-05-03 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6516471743643648

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000045de0
Crash State:
  blink::LayoutObject::containingBlock
  blink::CaretBase::invalidateLocalCaretRect
  blink::FrameSelection::nodeWillBeRemoved
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=390316:390338

Minimized Testcase (0.57 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96LcBCWrW__6eLF2JDpCkRqR9C1uB8whADDZy4rjCJiTO9Wp7WQSBvOfkMckfO__vE_X6c9ZNYQ7fu9e9IvkAx0BaXl0Rd2voMz1DSzudx0OxUm1tIivC22wvS-5OSFecG-oqoMTg0X8fWoeqWsNnGcw3zaBA

Filer: ochang

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### sh...@chromium.org (2016-05-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-04)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-05-04)

[Empty comment from Monorail migration]

### fe...@chromium.org (2016-05-06)

tkent@, could you please take a look? Could this have been caused by https://chromium.googlesource.com/chromium/src//+/5bfffca95444ba872b0a7faeaf956e92ab18639f?

[Monorail components: Blink>Layout]

### tk...@chromium.org (2016-05-06)

It seems HTMLMeterElement::canContainRangeEndPoint() triggers this issue.


[Monorail components: -Blink>Layout Blink>HTML>Meter Blink>TextSelection]

### tk...@chromium.org (2016-05-06)

Cleaner repro:

<style></style>
<div id="d" contenteditable=""></div>
<script>
var test0 = document.getElementById("d")
test0.focus();
test0.appendChild(document.createElement("meter"))
setTimeout(function() {
  document.styleSheets[0].insertRule('#d {content: counter(c, katakana);}');
  test0.textContent = "PASS";
})
</script>


### tk...@chromium.org (2016-05-09)

In CaretBase::caretLayoutObject(Node* node).
 - |node| is being detached from the document tree, and it has an obsolete LayoutObject.
 - caretRendersInsideNode(node) in this function calls HTMLMeterElement::canContainRangeEndPoint(), and it updates the layout tree.  It means LayoutObject for the METER is deleted.
 - Local variable |layoutObject| becomes a stale pointer.

I think we may remove updateLayoutTreeForForNode() in HTMLMeterElement::canContainRangeEndPoint().


### tk...@chromium.org (2016-05-09)

[Empty comment from Monorail migration]

### tk...@chromium.org (2016-05-09)

yosin@ takes this over.


### yo...@chromium.org (2016-05-09)

We should keep LayoutObject in CaretBase to avoid calling caretLayoutObject() with updating layout object at recalc style, and layout change.

### yo...@chromium.org (2016-05-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-18)

yoichio: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2016-05-23)

yoichio@, do you have any updates on this? Thanks!

### yo...@chromium.org (2016-05-24)

This is Heap-use-after-free security bug. 
Sanity of the script and usage in wild is important index to prioritize?
Other such bugs from clusterfuzz have been fixed quickly.
https://bugs.chromium.org/p/chromium/issues/list?can=1&q=Heap-use-after-free+clusterfuzz&colspec=ID+Pri+M+Stars+ReleaseBlock+Component+Status+Owner+Summary+OS+Modified&x=m&y=releaseblock&cells=ids

WDYK, yosin@?

### es...@chromium.org (2016-05-24)

We're doing a security fix-it right now; would it be possible to get this fixed this week?

### yo...@chromium.org (2016-05-25)

I'm working on this issue.

### bu...@chromium.org (2016-05-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e4edfb63d1b068c5ab5dc6b91edf75c108ebc433

commit e4edfb63d1b068c5ab5dc6b91edf75c108ebc433
Author: yoichio <yoichio@chromium.org>
Date: Wed May 25 07:23:06 2016

Check node->layoutObject in CaretBase::caretLayoutObject

In CaretBase::caretLayoutObject(Node* node),
if caretRendersInsideNode(node) calls HTMLMeterElement::canContainRangeEndPoint,
 it updates the layout tree.  It means LayoutObject for the METER can be deleted.
This is bad design. We should make caret painting algorithm clean.

BUG=608817

Review-Url: https://codereview.chromium.org/1972523002
Cr-Commit-Position: refs/heads/master@{#395822}

[modify] https://crrev.com/e4edfb63d1b068c5ab5dc6b91edf75c108ebc433/third_party/WebKit/Source/core/editing/CaretBase.cpp


### yo...@chromium.org (2016-05-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-05-25)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Request-XX label, where XX is the Chrome milestone.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-05-25)

[Empty comment from Monorail migration]

### es...@chromium.org (2016-05-25)

Thanks yoichio!

### tk...@chromium.org (2016-06-06)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-06)

Your change meets the bar and is auto-approved for M52 (branch: 2743)

### go...@chromium.org (2016-06-06)

Please merge your change to M52 branch 2743 before 3:00 PM PST tomorrow, Tuesday (06/07) so we can take it for this week beta release. Thank you.

### bu...@chromium.org (2016-06-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/59c23e7f2a1eeeafa8040eb50a193f2e3a29a02f

commit 59c23e7f2a1eeeafa8040eb50a193f2e3a29a02f
Author: Yoichi Osato <yoichio@chromium.org>
Date: Tue Jun 07 02:17:39 2016

Check node->layoutObject in CaretBase::caretLayoutObject

In CaretBase::caretLayoutObject(Node* node),
if caretRendersInsideNode(node) calls HTMLMeterElement::canContainRangeEndPoint,
 it updates the layout tree.  It means LayoutObject for the METER can be deleted.
This is bad design. We should make caret painting algorithm clean.

BUG=608817

Review-Url: https://codereview.chromium.org/1972523002
Cr-Commit-Position: refs/heads/master@{#395822}
(cherry picked from commit e4edfb63d1b068c5ab5dc6b91edf75c108ebc433)

Review URL: https://codereview.chromium.org/2042153002 .

Cr-Commit-Position: refs/branch-heads/2743@{#256}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/59c23e7f2a1eeeafa8040eb50a193f2e3a29a02f/third_party/WebKit/Source/core/editing/CaretBase.cpp


### cl...@chromium.org (2016-06-09)

ClusterFuzz has detected this issue as fixed in range 395786:395828.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6516471743643648

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000045de0
Crash State:
  blink::LayoutObject::containingBlock
  blink::CaretBase::invalidateLocalCaretRect
  blink::FrameSelection::nodeWillBeRemoved
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=390316:390338
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=395786:395828

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94_DGoNp8fVMd_haDgN_JwnuqFwPLdptMj-On8JzzwoIHQhKKVVFFsq6to-ulZIM7beD3c_0wvmRbz-hVqURKSZ50yS6oAZg93uvhqRgAmse4ai5ZeCsD649OKJMOm6rB0U0Il7wMvrz4uPYUkXUGGo2ZR3U1OZScEvabEhiy0dOjGGuFg


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### yo...@chromium.org (2016-06-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/59c23e7f2a1eeeafa8040eb50a193f2e3a29a02f

commit 59c23e7f2a1eeeafa8040eb50a193f2e3a29a02f
Author: Yoichi Osato <yoichio@chromium.org>
Date: Tue Jun 07 02:17:39 2016

Check node->layoutObject in CaretBase::caretLayoutObject

In CaretBase::caretLayoutObject(Node* node),
if caretRendersInsideNode(node) calls HTMLMeterElement::canContainRangeEndPoint,
 it updates the layout tree.  It means LayoutObject for the METER can be deleted.
This is bad design. We should make caret painting algorithm clean.

BUG=608817

Review-Url: https://codereview.chromium.org/1972523002
Cr-Commit-Position: refs/heads/master@{#395822}
(cherry picked from commit e4edfb63d1b068c5ab5dc6b91edf75c108ebc433)

Review URL: https://codereview.chromium.org/2042153002 .

Cr-Commit-Position: refs/branch-heads/2743@{#256}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/59c23e7f2a1eeeafa8040eb50a193f2e3a29a02f/third_party/WebKit/Source/core/editing/CaretBase.cpp


### aw...@chromium.org (2016-07-20)

Groovy - $3,500 for this one!

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### tk...@chromium.org (2016-10-12)

[Empty comment from Monorail migration]

[Monorail components: -Blink>TextSelection Blink>Editing>Selection]

### is...@google.com (2016-10-12)

This issue was migrated from crbug.com/chromium/608817?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Editing>Selection, Blink>HTML>Meter]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084223)*

# Heap-buffer-overflow in blink::BidiResolver<blink::InlineIterator, blink::BidiRun>::applyL1Rule

| Field | Value |
|-------|-------|
| **Issue ID** | [40080919](https://issues.chromium.org/issues/40080919) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | at...@gmail.com |
| **Assignee** | ea...@chromium.org |
| **Created** | 2014-11-28 |
| **Bounty** | $500.00 |

## Description



Tested on:

OS: Ubuntu 14.04


Chromium	41.0.2233.0 (Developer Build) 
Revision	222b9c08723a0acd0327b8ff7a11f1254d241a99-refs/heads/master@{#305981}

ASAN-trace:

==15720==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200004421e at pc 0x7fdc0c38c5e8 bp 0x7fffe76e88e0 sp 0x7fffe76e88d8
READ of size 2 at 0x60200004421e thread T0 (chrome)
    #0 0x7fdc0c38c5e7 in int blink::findFirstTrailingSpace<unsigned short>(blink::RenderText*, unsigned short const*, int, int) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/InlineIterator.h:469:9
    #1 0x7fdc0c38bc3d in blink::BidiResolver<blink::InlineIterator, blink::BidiRun>::applyL1Rule(blink::BidiRunList<blink::BidiRun>&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/text/BidiResolver.h:465:22
    #2 0x7fdc0c38a3fa in blink::BidiResolver<blink::InlineIterator, blink::BidiRun>::createBidiRunsForLine(blink::InlineIterator const&, blink::VisualDirectionOverride, bool, bool) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/text/BidiResolver.h:1068:9
    #3 0x7fdc0c3880df in blink::constructBidiRunsForLine(blink::BidiResolver<blink::InlineIterator, blink::BidiRun>&, blink::BidiRunList<blink::BidiRun>&, blink::InlineIterator const&, blink::VisualDirectionOverride, bool, bool) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/BidiRunForLine.cpp:141:5
    #4 0x7fdc0c106564 in blink::RenderBlockFlow::layoutRunsAndFloatsInRange(blink::LineLayoutState&, blink::BidiResolver<blink::InlineIterator, blink::BidiRun>&, blink::InlineIterator const&, blink::BidiStatus const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderBlockLineLayout.cpp:850:13
    #5 0x7fdc0c1047c7 in blink::RenderBlockFlow::layoutRunsAndFloats(blink::LineLayoutState&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderBlockLineLayout.cpp:773:5
    #6 0x7fdc0c10eac4 in blink::RenderBlockFlow::layoutInlineChildren(bool, blink::LayoutUnit&, blink::LayoutUnit&, blink::LayoutUnit) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderBlockLineLayout.cpp:1590:9
.
.
.
0x60200004421e is located 0 bytes to the right of 14-byte region [0x602000044210,0x60200004421e)
allocated by thread T0 (chrome) here:
    #0 0x7fdc076f010b in __interceptor_malloc ??:0:0
    #1 0x7fdc0a633c92 in partitionAllocGenericFlags /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/PartitionAlloc.h:541:20
    #2 0x7fdc0a633c92 in partitionAllocGeneric /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/PartitionAlloc.h:557:0
    #3 0x7fdc0a633c92 in WTF::StringImpl::createUninitialized(unsigned int, unsigned short*&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/text/StringImpl.cpp:315:0
    #4 0x7fdc0a634df1 in WTF::StringImpl::create(unsigned short const*, unsigned int) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/text/StringImpl.cpp:407:33
    #5 0x7fdc0a6536ea in WTF::String::String(unsigned short const*, unsigned int) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/text/WTFString.cpp:48:27
    #6 0x7fdc0c16c75f in blink::RenderCombineText::combineText() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderCombineText.cpp:141:9
.
.
.


## Attachments

- [chrome-heap-buffer-overflow-int9-min.html](attachments/chrome-heap-buffer-overflow-int9-min.html) (text/html, 337 B)

## Timeline

### cl...@chromium.org (2014-11-28)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6664436101152768

### in...@chromium.org (2014-11-28)

I am suspecting this is also a regression similar to https://code.google.com/p/chromium/issues/detail?id=437458

Uploading to CF to verify.

### cl...@chromium.org (2014-11-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6664436101152768

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x60900014fbde
Crash State:
  blink::BidiResolver<blink::InlineIterator, blink::BidiRun>::applyL1Rule
  blink::BidiResolver<blink::InlineIterator, blink::BidiRun>::createBidiRunsF
  blink::constructBidiRunsForLine
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=265035:265102

Minimized Testcase (0.18 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95BklcuCRWNCA_SxxAGLJqkJIQIw1OB0TGPczmxEhuifmky0CuYhhDcAeB8qkj8S-7KOWx61DANlaskLF_ara7j2lwTtDvG5bUGzS5UAtRmXdt43Ojo7ap6G2LiUTtTJ5RaRU5bai3SaqrfrAjjbu76Ns9Y1g
<style>
div {
  -webkit-writing-mode: vertical-lr;
  -webkit-text-combine: horizontal;
  height: 7px;
  white-space: pre-wrap;
</style>
<div>
foo
  <script></script>
  </script><textarea>




### cl...@chromium.org (2014-11-28)

[Empty comment from Monorail migration]

### ke...@chromium.org (2014-11-28)

[Empty comment from Monorail migration]

### pa...@google.com (2014-12-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-06)

dw.im@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-13)

dw.im@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-12-16)

Author: igor.o@sisa.samsung.com
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/38ca532f101fa1f1c8a04b18ec5c44f1cb99ab11
Time: Tue Jan 07 10:01:44 2014
The CL last changed line 469 of file InlineIterator.h, which is stack frame 0.

### js...@chromium.org (2014-12-17)

leviw@, eae@, it looks like you guys reviewed the CL that we suspect and I can't assign the bug directly to igor.o. So, I'm being a jerk and assigning to one of you based on a coin flip and hoping you can help get it fixed.

### ea...@chromium.org (2014-12-17)

Well, levi is on vacation so I guess it falls on me.


### ea...@chromium.org (2014-12-18)

[Empty comment from Monorail migration]

### ea...@chromium.org (2014-12-18)

Turns out that the patch in r164557 assumes that the last node has at least two characters, which is an incorrect assumption. The obvious fix didn't quite work [1] so I'll revert r164557.


### ea...@chromium.org (2014-12-18)

Turns out it is not quite that easy given that it was added 11 months ago and the code has changed a lot since.
I'm guessing trying to get the fix in https://codereview.chromium.org/813133002/ working will be easier.

### ea...@chromium.org (2014-12-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-09)

eae@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-02-02)

eae@: Uh oh! This issue is still open and hasn't been updated in the last 45 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-02-08)

ClusterFuzz has detected this issue as fixed in range 314621:315214.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6664436101152768

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x60900014fbde
Crash State:
  blink::BidiResolver<blink::InlineIterator, blink::BidiRun>::applyL1Rule
  blink::BidiResolver<blink::InlineIterator, blink::BidiRun>::createBidiRunsF
  blink::constructBidiRunsForLine
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=262830:262871
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=314621:315214

Minimized Testcase (0.18 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95BklcuCRWNCA_SxxAGLJqkJIQIw1OB0TGPczmxEhuifmky0CuYhhDcAeB8qkj8S-7KOWx61DANlaskLF_ara7j2lwTtDvG5bUGzS5UAtRmXdt43Ojo7ap6G2LiUTtTJ5RaRU5bai3SaqrfrAjjbu76Ns9Y1g
<style>
div {
  -webkit-writing-mode: vertical-lr;
  -webkit-text-combine: horizontal;
  height: 7px;
  white-space: pre-wrap;
</style>
<div>
foo
  <script></script>
  </script><textarea>

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### me...@chromium.org (2015-02-23)

Clusterfuzz says this is fixed. eae@: Could you please confirm?

### cl...@chromium.org (2015-02-23)

ClusterFuzz has detected this issue as fixed in range 314621:315214.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6664436101152768

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x60900014fbde
Crash State:
  blink::BidiResolver<blink::InlineIterator, blink::BidiRun>::applyL1Rule
  blink::BidiResolver<blink::InlineIterator, blink::BidiRun>::createBidiRunsF
  blink::constructBidiRunsForLine
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=262830:262871
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=314621:315214

Minimized Testcase (0.18 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95BklcuCRWNCA_SxxAGLJqkJIQIw1OB0TGPczmxEhuifmky0CuYhhDcAeB8qkj8S-7KOWx61DANlaskLF_ara7j2lwTtDvG5bUGzS5UAtRmXdt43Ojo7ap6G2LiUTtTJ5RaRU5bai3SaqrfrAjjbu76Ns9Y1g
<style>
div {
  -webkit-writing-mode: vertical-lr;
  -webkit-text-combine: horizontal;
  height: 7px;
  white-space: pre-wrap;
</style>
<div>
foo
  <script></script>
  </script><textarea>

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2015-02-23)

no idea what fixed this.

### cl...@chromium.org (2015-02-23)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-14)

Congrats - $500 for this report. I'll add it to your tab :)

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-01)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-03)

Processing via our *new* e-payment system should only take a 7-10 days and the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/437399?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080919)*

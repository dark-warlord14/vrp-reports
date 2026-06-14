# Security: Universal XSS using late widget updates

| Field | Value |
|-------|-------|
| **Issue ID** | [40086195](https://issues.chromium.org/issues/40086195) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Internals |
| **Reporter** | ma...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2016-12-11 |
| **Bounty** | $8,000.00 |

## Description

**VULNERABILITY DETAILS**  

Among the things that Document::shutdown() does, |view()->dispose()| is called:

## From /third\_party/WebKit/Source/core/frame/FrameView.cpp:

## void FrameView::dispose() { (...) // FIXME: Do we need to do something here for OOPI? HTMLFrameOwnerElement\* ownerElement = m\_frame->deprecatedLocalOwner(); // TODO(dcheng): It seems buggy that we can have an owner element that // points to another Widget. if (ownerElement && ownerElement->ownedWidget() == this) ownerElement->setWidget(nullptr); (...) }

In addition to what Daniel said, not clearing the owner's widget when it doesn't match the document's view is dangerous -- this logic means there are 2 cases:

1. ownerElement->ownedWidget() == document\_in\_shutdown->view()  
   
   The frame element's widget is cleared during Document::shutdown(). The widget update is suspended and executed in a safe state.
2. ownerElement->ownedWidget() != document\_in\_shutdown->view()  
   
   The frame element's widget is left intact during Document::shutdown(). Instead, it's cleared in LocalFrame::createView when a new view is created for the navigated frame shortly thereafter. This is unsafe because clearing the widget may destroy a plugin and run script, allowing an attacker to violate invariants.

**VERSION**  

The attached exploit works in:  

Chrome 56.0.2924.21 (Beta)  

Chrome 56.0.2924.18 (Dev)  

Chromium 57.0.2948.0 + Pepper Flash (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 2.5 KB)
- [exploit-55.zip](attachments/exploit-55.zip) (application/octet-stream, 2.6 KB)

## Timeline

### ma...@gmail.com (2016-12-11)

Here's a patch ensuring that the widget is always cleared soon enough: https://codereview.chromium.org/2563313002

Please note that although the exploit doesn't work in the stable channel, the bug seems to affect that branch as well. The plugin element loading logic is somehow different in stable and I have yet to see if I can adjust the PoC to it.

### wr...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

### ma...@gmail.com (2016-12-13)

Okay, so it turns out embed elements are a tiny bit broken in stable, ie. setting src works only once. Please find attached an example that should work in Chrome 55.0.2883.87 as well, the Security_Impact flag can be updated accordingly.

### dc...@chromium.org (2016-12-13)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-12-13)

Unmergable, but I'm going to attempt (again) to just remove deferred widget updates altogether (https://crbug.com/chromium/561683)

In the meanwhile, we'll need a short-term fix for this to stop the bleeding though.

### sh...@chromium.org (2016-12-13)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-12-14)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-12-15)

Looks like the patch from c#1 is in the CQ now, but setting an owner just in case any follow-up is needed. Feel free to reassign if someone else makes more sense.

Thanks for the report and fix, Marius!

### bu...@chromium.org (2016-12-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/71b91a424a00dce5ff5ff4cf2e7b52fc70136f36

commit 71b91a424a00dce5ff5ff4cf2e7b52fc70136f36
Author: marius.mlynski <marius.mlynski@gmail.com>
Date: Fri Dec 16 01:48:01 2016

Clear the owner element's widget in Document::shutdown().

FrameView::dispose() doesn't guarantee that the owner's widget is cleared
and this could be problematic when it's overwritten in
LocalFrame::createView() a short time later.

BUG=673170

Review-Url: https://codereview.chromium.org/2563313002
Cr-Commit-Position: refs/heads/master@{#438977}

[modify] https://crrev.com/71b91a424a00dce5ff5ff4cf2e7b52fc70136f36/third_party/WebKit/Source/core/dom/Document.cpp
[modify] https://crrev.com/71b91a424a00dce5ff5ff4cf2e7b52fc70136f36/third_party/WebKit/Source/core/frame/FrameView.cpp


### sh...@chromium.org (2016-12-16)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-19)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-12-19)

Your change meets the bar and is auto-approved for M56 (branch: 2924)

### bu...@chromium.org (2016-12-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a7a51f270ce442c7292abb84e2e4941f1c9c6199

commit a7a51f270ce442c7292abb84e2e4941f1c9c6199
Author: Daniel Cheng <dcheng@chromium.org>
Date: Mon Dec 19 18:25:33 2016

Clear the owner element's widget in Document::shutdown().

FrameView::dispose() doesn't guarantee that the owner's widget is cleared
and this could be problematic when it's overwritten in
LocalFrame::createView() a short time later.

BUG=673170

Review-Url: https://codereview.chromium.org/2563313002
Cr-Commit-Position: refs/heads/master@{#438977}
(cherry picked from commit 71b91a424a00dce5ff5ff4cf2e7b52fc70136f36)

Review-Url: https://codereview.chromium.org/2589913002 .
Cr-Commit-Position: refs/branch-heads/2924@{#551}
Cr-Branched-From: 3a87aecc31cd1ffe751dd72c04e5a96a1fc8108a-refs/heads/master@{#433059}

[modify] https://crrev.com/a7a51f270ce442c7292abb84e2e4941f1c9c6199/third_party/WebKit/Source/core/dom/Document.cpp
[modify] https://crrev.com/a7a51f270ce442c7292abb84e2e4941f1c9c6199/third_party/WebKit/Source/core/frame/FrameView.cpp


### mb...@chromium.org (2016-12-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>Internals]

### sh...@chromium.org (2016-12-20)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2016-12-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-09)

[Empty comment from Monorail migration]

### aw...@google.com (2017-01-10)

Many thanks as ever - $8,000 for this one!

### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### ha...@chromium.org (2017-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-02-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/73fedd040c60dbae15d97bf93926b7d577750821

commit 73fedd040c60dbae15d97bf93926b7d577750821
Author: Ehsan Karamad <ekaramad@chromium.org>
Date: Tue Feb 06 21:23:01 2018

Fix an issue with speculative frame cleanup in OOPIFs

When the beforeunload handler is ACKed by the OOPIF process with "do not
proceed", the corresponding speculative frame is cleaned up. When the
speculative frame is in the parent frame's process it will set the
EmbeddedContentView of the owner element to nullptr. This is incorrect
as the navigation has been canceled.

This CL will avoid setting the EmbeddedContentView to nullptr when the
ContentFrame() is not equal to Document::GetFrame() (i.e., speculative)
and also the EmbeddedContentView is a RemoteFrameView.

Bug: 578349, 673170, 807772
Change-Id: Ic6f5a16ae6f02bfbe11238851936ee323472a407
Reviewed-on: https://chromium-review.googlesource.com/898028
Commit-Queue: Ehsan Karamad <ekaramad@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Ehsan Karamad <ekaramad@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/heads/master@{#534795}
[modify] https://crrev.com/73fedd040c60dbae15d97bf93926b7d577750821/content/browser/site_per_process_browsertest.cc
[modify] https://crrev.com/73fedd040c60dbae15d97bf93926b7d577750821/third_party/WebKit/Source/core/dom/Document.cpp
[modify] https://crrev.com/73fedd040c60dbae15d97bf93926b7d577750821/third_party/WebKit/Source/core/exported/WebFrame.cpp
[modify] https://crrev.com/73fedd040c60dbae15d97bf93926b7d577750821/third_party/WebKit/Source/core/frame/LocalFrame.h
[modify] https://crrev.com/73fedd040c60dbae15d97bf93926b7d577750821/third_party/WebKit/Source/core/frame/WebLocalFrameImpl.cpp


### bu...@chromium.org (2018-02-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/36e80ec89c398f2832a252fe47d2f50c50ef38e6

commit 36e80ec89c398f2832a252fe47d2f50c50ef38e6
Author: Ehsan Karamad <ekaramad@chromium.org>
Date: Thu Feb 08 20:20:42 2018

Fix an issue with speculative frame cleanup in OOPIFs

When the beforeunload handler is ACKed by the OOPIF process with "do not
proceed", the corresponding speculative frame is cleaned up. When the
speculative frame is in the parent frame's process it will set the
EmbeddedContentView of the owner element to nullptr. This is incorrect
as the navigation has been canceled.

This CL will avoid setting the EmbeddedContentView to nullptr when the
ContentFrame() is not equal to Document::GetFrame() (i.e., speculative)
and also the EmbeddedContentView is a RemoteFrameView.

TBR=ekaramad@chromium.org

(cherry picked from commit 73fedd040c60dbae15d97bf93926b7d577750821)

Bug: 578349, 673170, 807772
Change-Id: Ic6f5a16ae6f02bfbe11238851936ee323472a407
Reviewed-on: https://chromium-review.googlesource.com/898028
Commit-Queue: Ehsan Karamad <ekaramad@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Ehsan Karamad <ekaramad@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#534795}
Reviewed-on: https://chromium-review.googlesource.com/909297
Cr-Commit-Position: refs/branch-heads/3325@{#390}
Cr-Branched-From: bc084a8b5afa3744a74927344e304c02ae54189f-refs/heads/master@{#530369}
[modify] https://crrev.com/36e80ec89c398f2832a252fe47d2f50c50ef38e6/content/browser/site_per_process_browsertest.cc
[modify] https://crrev.com/36e80ec89c398f2832a252fe47d2f50c50ef38e6/third_party/WebKit/Source/core/dom/Document.cpp
[modify] https://crrev.com/36e80ec89c398f2832a252fe47d2f50c50ef38e6/third_party/WebKit/Source/core/exported/WebFrame.cpp
[modify] https://crrev.com/36e80ec89c398f2832a252fe47d2f50c50ef38e6/third_party/WebKit/Source/core/frame/LocalFrame.h
[modify] https://crrev.com/36e80ec89c398f2832a252fe47d2f50c50ef38e6/third_party/WebKit/Source/core/frame/WebLocalFrameImpl.cpp


### aw...@google.com (2018-03-20)

[Comment Deleted]

### aw...@google.com (2018-03-20)

[Comment Deleted]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/673170?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/674203]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086195)*

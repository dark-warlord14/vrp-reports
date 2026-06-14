# Part 1 of Pwnium Bug: UXSS

| Field | Value |
|-------|-------|
| **Issue ID** | [40054620](https://issues.chromium.org/issues/40054620) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | in...@chromium.org |
| **Assignee** | mo...@google.com |
| **Created** | 2012-03-07 |
| **Bounty** | $60,000.00 |

## Description

1. UXSS using iframe elements

When the src attribute of an iframe element is set to a javascript: URI, a security check is performed.
This check uses a stack of JS contexts and is considered to be passed when there is no JS context on 
the stack (i.e. when the DOM tree is modified by native code). An attacker can force the XML parser to
insert the iframe element into the document tree by intercepting mutation events during generation of 
an XML parsing error message (see uxss.svg and XMLErrors.cpp).

The bug requires an iframe to be attached to a Frame object with a vicim page loaded while the iframe
itself is not inserted into the tree. This also can be achieved with setting the proper mutation event
handler (see uxss.html).

## Timeline

### in...@chromium.org (2012-03-07)

Upstreamed in https://bugs.webkit.org/show_bug.cgi?id=80530

Merged to branch 963

### jo...@chromium.org (2012-03-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-08)

Merged to 963 Adam's patch in
http://trac.webkit.org/changeset/110140

My patch was merged in http://trac.webkit.org/changeset/110111

### in...@chromium.org (2012-03-08)

Need to evaluate that if my part of the fix needs to go into trunk. mutation events shouldnt be fired at all during movement of nodes while generating error blocks. moving to parser* functions was breaking tests, so need to look more closely what appendChild, insertBefore is doing different from parser* functions. Basically, using parser* prevent mutation events to fire at all.

### sc...@gmail.com (2012-03-08)

[Empty comment from Monorail migration]

### [Deleted User] (2012-03-08)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-12)

For the containernode iteration fix on M18: http://trac.webkit.org/changeset/110473

### sc...@gmail.com (2012-03-12)

Ok, so also merged M17-specific workaround to M18 as: http://trac.webkit.org/changeset/110479

I'm going to leave this as Merge=Approved with Mstone=19 so that we know to either re-merge this branch-specific CL, or call it done if https://bugs.webkit.org/show_bug.cgi?id=80765 gets fixed instead.

### sc...@gmail.com (2012-03-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-24)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-25)

Ok, https://bugs.webkit.org/show_bug.cgi?id=80765 was resolved on trunk by:
http://trac.webkit.org/changeset/112023

No more merges to track from this bug.

### sc...@gmail.com (2012-05-03)

Payment of Pwnium reward in system -- along with $2k top-up for the other UXSS :)

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-12-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/783e19486cab2b7485b4a19c02a2eb0369f3b350

commit 783e19486cab2b7485b4a19c02a2eb0369f3b350
Author: marius.mlynski <marius.mlynski@gmail.com>
Date: Mon Dec 05 23:31:27 2016

Don't skip security checks for javascript: URLs when the JS stack is empty.

Before this patch, HTMLFrameElementBase::isURLAllowed would skip the security
check if there were no JavaScript frames on the stack. This could lead to UXSS
bugs if an attacker managed to trick the parser into attaching a frame element
with a cross-origin document and the src attribute set to a javascript: URL.

After this patch, the security context of the frame's containing document
is used to verify if the URL is allowed. Nothing else (expect for some other
same-origin context) could've set the src attribute, so we assume it's the most
logical choice in the absence of the current JavaScript context.

BUG=117226

Review-Url: https://codereview.chromium.org/2502783004
Cr-Commit-Position: refs/heads/master@{#436449}

[modify] https://crrev.com/783e19486cab2b7485b4a19c02a2eb0369f3b350/third_party/WebKit/Source/bindings/core/v8/ScriptController.cpp
[modify] https://crrev.com/783e19486cab2b7485b4a19c02a2eb0369f3b350/third_party/WebKit/Source/bindings/core/v8/ScriptController.h
[modify] https://crrev.com/783e19486cab2b7485b4a19c02a2eb0369f3b350/third_party/WebKit/Source/core/html/HTMLFrameElementBase.cpp


### bu...@chromium.org (2016-12-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6a2bb4e40356e5a96ff3395ee5ba8c1b48736f9d

commit 6a2bb4e40356e5a96ff3395ee5ba8c1b48736f9d
Author: Daniel Cheng <dcheng@chromium.org>
Date: Fri Dec 16 09:29:36 2016

Don't skip security checks for javascript: URLs when the JS stack is empty.

Before this patch, HTMLFrameElementBase::isURLAllowed would skip the security
check if there were no JavaScript frames on the stack. This could lead to UXSS
bugs if an attacker managed to trick the parser into attaching a frame element
with a cross-origin document and the src attribute set to a javascript: URL.

After this patch, the security context of the frame's containing document
is used to verify if the URL is allowed. Nothing else (expect for some other
same-origin context) could've set the src attribute, so we assume it's the most
logical choice in the absence of the current JavaScript context.

BUG=117226

Review-Url: https://codereview.chromium.org/2502783004
Cr-Commit-Position: refs/heads/master@{#436449}
(cherry picked from commit 783e19486cab2b7485b4a19c02a2eb0369f3b350)

R=esprehn@chromium.org, haraken@chromium.org, jochen@chromium.org

Review-Url: https://codereview.chromium.org/2579213002 .
Cr-Commit-Position: refs/branch-heads/2924@{#524}
Cr-Branched-From: 3a87aecc31cd1ffe751dd72c04e5a96a1fc8108a-refs/heads/master@{#433059}

[modify] https://crrev.com/6a2bb4e40356e5a96ff3395ee5ba8c1b48736f9d/third_party/WebKit/Source/bindings/core/v8/ScriptController.cpp
[modify] https://crrev.com/6a2bb4e40356e5a96ff3395ee5ba8c1b48736f9d/third_party/WebKit/Source/bindings/core/v8/ScriptController.h
[modify] https://crrev.com/6a2bb4e40356e5a96ff3395ee5ba8c1b48736f9d/third_party/WebKit/Source/core/html/HTMLFrameElementBase.cpp


### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### is...@google.com (2020-11-03)

This issue was migrated from crbug.com/chromium/117226?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054620)*

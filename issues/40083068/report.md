# Security: Universal XSS using plugin objects

| Field | Value |
|-------|-------|
| **Issue ID** | [40083068](https://issues.chromium.org/issues/40083068) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>HTML |
| **Reporter** | ma...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2015-10-22 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

This is a regression from <https://crbug.com/chromium/524120>. Now that widget updates are deferred until after the frame is detached from the document (and beyond the lifetime of ScriptForbiddenScope, too), it is possible to attach another document to the frame before a new document is installed. The attached document can then be used to bypass the same-origin policy.

**VERSION**  

Chrome 47.0.2526.27 (Beta)  

Chrome 48.0.2540.0 (Dev)  

Chromium 48.0.2544.0 + Pepper Flash 19.0.0.207 (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/zip, 267.2 KB)

## Timeline

### dc...@chromium.org (2015-10-22)

[Empty comment from Monorail migration]

### ke...@chromium.org (2015-10-22)

Thanks for taking this dcheng@.

### cl...@chromium.org (2015-10-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-22)

[Empty comment from Monorail migration]

### ss...@google.com (2015-10-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-05)

dcheng@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@google.com (2015-11-10)

@dcheng - do you still have this on your radar?


### dc...@chromium.org (2015-11-10)

Yes, I'm still working on this. The fix I'm attempting is somewhat tricky and currently crashes a lot =/

### cl...@chromium.org (2015-11-13)

[Empty comment from Monorail migration]

### ss...@google.com (2015-11-15)

Any update on this? M47 stable cut is fast approaching and this is marked as ReleaseBlock-Stable.

### dc...@chromium.org (2015-11-16)

So the root cause of this issue is that running nested message loops that invoke script in Document::detach() generally results in broken invariants.

My original patch tries to change the timing of running deferred widget updates to the message loop, to avoid re-entrancy. However, that hit a lot of crashes and didn't look like something that would be easy to merge to M47.

I tried making a simpler patch yesterday: https://codereview.chromium.org/1444183003

It /almost/ works... but it turns out that it can leave a dangling Document/FrameView. The invariant being violated here is that Frame has no FrameView at the end of Document::detach(). I can try to pile on some more bandaid fixes... but ugh.

### bu...@chromium.org (2015-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/66ad73d642b9cf824f4b1f300811ed1ee6963da7

commit 66ad73d642b9cf824f4b1f300811ed1ee6963da7
Author: dcheng <dcheng@chromium.org>
Date: Tue Nov 17 23:06:50 2015

Don't allow navigations in Document::detach.

When navigating to a javascript: URL, Blink detaches the original
Document. This process may detach plugin elements, causing a nested
message loop to run.

Document::detach() creates a ScriptForbiddenScope to prevent script from
breaking invariants. Since plugins were detached synchronously, any
script trying to execute in the nested message loop would be blocked.

However, the fix for https://crbug.com/524120 defers plugin updates to
happen outside the ScriptForbiddenScope. Thus, it is now possible to
attach a *new* Document with a synchronous navigation while the old
Document is being detached.

BUG=546545

Review URL: https://codereview.chromium.org/1444183003

Cr-Commit-Position: refs/heads/master@{#360190}

[modify] http://crrev.com/66ad73d642b9cf824f4b1f300811ed1ee6963da7/third_party/WebKit/Source/core/dom/Document.cpp
[modify] http://crrev.com/66ad73d642b9cf824f4b1f300811ed1ee6963da7/third_party/WebKit/Source/core/frame/LocalFrame.cpp
[modify] http://crrev.com/66ad73d642b9cf824f4b1f300811ed1ee6963da7/third_party/WebKit/Source/core/frame/LocalFrame.h
[modify] http://crrev.com/66ad73d642b9cf824f4b1f300811ed1ee6963da7/third_party/WebKit/Source/core/loader/FrameLoader.cpp
[modify] http://crrev.com/66ad73d642b9cf824f4b1f300811ed1ee6963da7/third_party/WebKit/Source/core/loader/NavigationScheduler.cpp
[modify] http://crrev.com/66ad73d642b9cf824f4b1f300811ed1ee6963da7/third_party/WebKit/Source/core/loader/NavigationScheduler.h


### dc...@chromium.org (2015-11-17)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-11-17)

Note that the change looks large, but it's really just moving FrameNavigationDisabler from NavigationScheduler into LocalFrame.

The core change in the patch is just adding one line to Document::detach to disable navigations:
FrameNavigationDisabler navigationDisabler(*m_frame);

Which is really low risk because prior to r350972, these sorts of navigations couldn't be triggered anyway.

### ss...@google.com (2015-11-17)

Merge approved for M47 (branch 2526)

### cl...@chromium.org (2015-11-17)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8148a1e48eeba4215886d8ceab7e989a367ae117

commit 8148a1e48eeba4215886d8ceab7e989a367ae117
Author: Daniel Cheng <dcheng@chromium.org>
Date: Tue Nov 17 23:45:17 2015

Don't allow navigations in Document::detach.

When navigating to a javascript: URL, Blink detaches the original
Document. This process may detach plugin elements, causing a nested
message loop to run.

Document::detach() creates a ScriptForbiddenScope to prevent script from
breaking invariants. Since plugins were detached synchronously, any
script trying to execute in the nested message loop would be blocked.

However, the fix for https://crbug.com/524120 defers plugin updates to
happen outside the ScriptForbiddenScope. Thus, it is now possible to
attach a *new* Document with a synchronous navigation while the old
Document is being detached.

BUG=546545

Review URL: https://codereview.chromium.org/1444183003

Cr-Commit-Position: refs/heads/master@{#360190}
(cherry picked from commit 66ad73d642b9cf824f4b1f300811ed1ee6963da7)

Review URL: https://codereview.chromium.org/1458643003 .

Cr-Commit-Position: refs/branch-heads/2526@{#443}
Cr-Branched-From: cb947c0153db0ec02a8abbcb3ca086d88bf6006f-refs/heads/master@{#352221}

[modify] http://crrev.com/8148a1e48eeba4215886d8ceab7e989a367ae117/third_party/WebKit/Source/core/dom/Document.cpp
[modify] http://crrev.com/8148a1e48eeba4215886d8ceab7e989a367ae117/third_party/WebKit/Source/core/frame/LocalFrame.cpp
[modify] http://crrev.com/8148a1e48eeba4215886d8ceab7e989a367ae117/third_party/WebKit/Source/core/frame/LocalFrame.h
[modify] http://crrev.com/8148a1e48eeba4215886d8ceab7e989a367ae117/third_party/WebKit/Source/core/loader/FrameLoader.cpp
[modify] http://crrev.com/8148a1e48eeba4215886d8ceab7e989a367ae117/third_party/WebKit/Source/core/loader/NavigationScheduler.cpp
[modify] http://crrev.com/8148a1e48eeba4215886d8ceab7e989a367ae117/third_party/WebKit/Source/core/loader/NavigationScheduler.h


### bu...@chromium.org (2015-11-18)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/8148a1e48eeba4215886d8ceab7e989a367ae117

commit 8148a1e48eeba4215886d8ceab7e989a367ae117
Author: Daniel Cheng <dcheng@chromium.org>
Date: Tue Nov 17 23:45:17 2015


### cl...@chromium.org (2015-11-18)

[Empty comment from Monorail migration]

### ti...@google.com (2015-11-18)

Congrats your change is auto-approved for M48 (branch: 2564)

### bu...@chromium.org (2015-11-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/89e7aca2d8bb1e3cb5e9e7b5a9167e4b5e0f66b0

commit 89e7aca2d8bb1e3cb5e9e7b5a9167e4b5e0f66b0
Author: Daniel Cheng <dcheng@chromium.org>
Date: Thu Nov 19 03:24:37 2015

Don't allow navigations in Document::detach.

When navigating to a javascript: URL, Blink detaches the original
Document. This process may detach plugin elements, causing a nested
message loop to run.

Document::detach() creates a ScriptForbiddenScope to prevent script from
breaking invariants. Since plugins were detached synchronously, any
script trying to execute in the nested message loop would be blocked.

However, the fix for https://crbug.com/524120 defers plugin updates to
happen outside the ScriptForbiddenScope. Thus, it is now possible to
attach a *new* Document with a synchronous navigation while the old
Document is being detached.

BUG=546545

Review URL: https://codereview.chromium.org/1444183003

Cr-Commit-Position: refs/heads/master@{#360190}
(cherry picked from commit 66ad73d642b9cf824f4b1f300811ed1ee6963da7)

Review URL: https://codereview.chromium.org/1460973002 .

Cr-Commit-Position: refs/branch-heads/2564@{#55}
Cr-Branched-From: 1283eca15bd9f772387f75241576cde7bdec7f54-refs/heads/master@{#359700}

[modify] http://crrev.com/89e7aca2d8bb1e3cb5e9e7b5a9167e4b5e0f66b0/third_party/WebKit/Source/core/dom/Document.cpp
[modify] http://crrev.com/89e7aca2d8bb1e3cb5e9e7b5a9167e4b5e0f66b0/third_party/WebKit/Source/core/frame/LocalFrame.cpp
[modify] http://crrev.com/89e7aca2d8bb1e3cb5e9e7b5a9167e4b5e0f66b0/third_party/WebKit/Source/core/frame/LocalFrame.h
[modify] http://crrev.com/89e7aca2d8bb1e3cb5e9e7b5a9167e4b5e0f66b0/third_party/WebKit/Source/core/loader/FrameLoader.cpp
[modify] http://crrev.com/89e7aca2d8bb1e3cb5e9e7b5a9167e4b5e0f66b0/third_party/WebKit/Source/core/loader/NavigationScheduler.cpp
[modify] http://crrev.com/89e7aca2d8bb1e3cb5e9e7b5a9167e4b5e0f66b0/third_party/WebKit/Source/core/loader/NavigationScheduler.h


### bu...@chromium.org (2015-11-20)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/89e7aca2d8bb1e3cb5e9e7b5a9167e4b5e0f66b0

commit 89e7aca2d8bb1e3cb5e9e7b5a9167e4b5e0f66b0
Author: Daniel Cheng <dcheng@chromium.org>
Date: Thu Nov 19 03:24:37 2015


### ti...@google.com (2015-11-28)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-01)

Thanks again, and here's another $7,500 to show our appreciation for your research!

### cl...@chromium.org (2016-03-02)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

- Your friendly Sheriffbot

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/546545?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083068)*

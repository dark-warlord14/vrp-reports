# Security: Universal XSS by circumventing the unload event

| Field | Value |
|-------|-------|
| **Issue ID** | [40083520](https://issues.chromium.org/issues/40083520) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM |
| **Reporter** | ma...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2016-01-13 |
| **Bounty** | $7,500.00 |

## Description

## **VULNERABILITY DETAILS** From /third\_party/WebKit/Source/core/dom/Document.cpp:

void Document::dispatchUnloadEvents()  

{  

PluginScriptForbiddenScope forbidPluginDestructorScripting;  

RefPtrWillBeRawPtr<Document> protect(this);  

if (m\_parser)  

m\_parser->stopParsing();

```
if (m_loadEventProgress == LoadEventNotRun)  
    return;  

if (m_loadEventProgress <= UnloadEventInProgress) {  
    (...)  
    if (m_loadEventProgress < PageHideInProgress) {  
        (...)  
    }  
    m_loadEventProgress = UnloadEventHandled;  
}  

```
## (...) }

If this method is called while the document's |m\_loadEventProgress| is still at |LoadEventNotRun| then it returns without advancing |m\_loadEventProgress|. It is possible to take this branch by calling document.open() (which sets |m\_loadEventProgress| to LoadEventNotRun), and then navigating the document without the body element (the presence of which would allow |m\_loadEventProgress| to change to BeforeUnloadEventCompleted before Document::dispatchUnloadEvents is called).

Since FrameLoader::prepareForCommit relies on Document::dispatchUnloadEvents to advance |m\_loadEventProgress| to block the creation of new frames, this allows an attacker to attach subframes that will persist in the frame tree of a cross-origin document.

**VERSION**  

Chrome 47.0.2526.106 (Stable)  

Chrome 48.0.2564.71 (Beta)  

Chrome 49.0.2618.8.0 (Dev)  

Chromium 49.0.2621.0 (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/zip, 1.7 KB)
- [patch.diff](attachments/patch.diff) (application/octet-stream, 660 B)

## Timeline

### ma...@gmail.com (2016-01-13)

This patch changes m_loadEventProgress to a state disallowing any further creation of subframes even if the unload event isn't actually dispatched. I'm not sure if it's the desired fix, especially that it's unclear to me why it's necessary to skip the unload event dispatch in the first place.

### dc...@chromium.org (2016-01-13)

[Empty comment from Monorail migration]

### ri...@chromium.org (2016-01-13)

Thanks for yet another great report!

### dc...@chromium.org (2016-01-25)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-02-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-02-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a4bcdcb1f8df4f7427e208201501a9d8e41e386b

commit a4bcdcb1f8df4f7427e208201501a9d8e41e386b
Author: dcheng <dcheng@chromium.org>
Date: Thu Feb 04 19:17:21 2016

Disable sub frame loads more reliably in frame detach.

Previously, guarding against attaching a new frame in frame detach
was done by inspecting LoadEventProgress. There are certain
operations, such as document.open(), that can cause LoadEventProgress
to never advance, causing the guard to get skipped.

BUG=577105

Review URL: https://codereview.chromium.org/1659013003

Cr-Commit-Position: refs/heads/master@{#373581}

[add] http://crrev.com/a4bcdcb1f8df4f7427e208201501a9d8e41e386b/third_party/WebKit/LayoutTests/fast/frames/open-then-unload-expected.txt
[add] http://crrev.com/a4bcdcb1f8df4f7427e208201501a9d8e41e386b/third_party/WebKit/LayoutTests/fast/frames/open-then-unload.html
[modify] http://crrev.com/a4bcdcb1f8df4f7427e208201501a9d8e41e386b/third_party/WebKit/Source/core/frame/LocalFrame.cpp
[modify] http://crrev.com/a4bcdcb1f8df4f7427e208201501a9d8e41e386b/third_party/WebKit/Source/core/html/HTMLFrameOwnerElement.h
[modify] http://crrev.com/a4bcdcb1f8df4f7427e208201501a9d8e41e386b/third_party/WebKit/Source/core/loader/FrameLoader.cpp
[modify] http://crrev.com/a4bcdcb1f8df4f7427e208201501a9d8e41e386b/third_party/WebKit/Source/web/WebLocalFrameImpl.cpp


### dc...@chromium.org (2016-02-04)

Let's try to get this in the M48 respin.

### cl...@chromium.org (2016-02-04)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-02-04)

We're planning M48 stable refresh candidate cut tomorrow @ 4:00 PM for release on Tuesday (02/09) so please merge as soon as Merge is approved.


### ti...@google.com (2016-02-04)

hey dcheng@, has this baked through canary and safe?

### dc...@chromium.org (2016-02-04)

This hasn't been through canary yet, but I believe this change is safe.

### bu...@chromium.org (2016-02-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4c8b008f055f79e622344627fed7f820375a4f01

commit 4c8b008f055f79e622344627fed7f820375a4f01
Author: dcheng <dcheng@chromium.org>
Date: Thu Feb 04 22:45:59 2016

Change Document::detach() to RELEASE_ASSERT all subframes are gone.

BUG=556724,577105

Review URL: https://codereview.chromium.org/1667573002

Cr-Commit-Position: refs/heads/master@{#373642}

[modify] http://crrev.com/4c8b008f055f79e622344627fed7f820375a4f01/third_party/WebKit/Source/core/dom/Document.cpp


### dc...@chromium.org (2016-02-04)

To be clear, the merge request is only for commit https://chromium.googlesource.com/chromium/src.git/+/a4bcdcb1f8df4f7427e208201501a9d8e41e386b: the commit in https://crbug.com/chromium/577105#c12 is not mergeable (as it will cause a bunch of renderer crashes by itself)

### ti...@google.com (2016-02-05)

Merge approved for M48 (branch 2564). Pls merge asap - by 4pm this Fri to catch up with next stable refresh. Thanks.

### bu...@chromium.org (2016-02-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1f7c706b9c343d11d0011f3ede6843c8d91c7b31

commit 1f7c706b9c343d11d0011f3ede6843c8d91c7b31
Author: Daniel Cheng <dcheng@chromium.org>
Date: Fri Feb 05 06:48:21 2016

Disable sub frame loads more reliably in frame detach.

Previously, guarding against attaching a new frame in frame detach
was done by inspecting LoadEventProgress. There are certain
operations, such as document.open(), that can cause LoadEventProgress
to never advance, causing the guard to get skipped.

BUG=577105

Review URL: https://codereview.chromium.org/1659013003

Cr-Commit-Position: refs/heads/master@{#373581}
(cherry picked from commit a4bcdcb1f8df4f7427e208201501a9d8e41e386b)

Review URL: https://codereview.chromium.org/1675513003 .

Cr-Commit-Position: refs/branch-heads/2564@{#671}
Cr-Branched-From: 1283eca15bd9f772387f75241576cde7bdec7f54-refs/heads/master@{#359700}

[add] http://crrev.com/1f7c706b9c343d11d0011f3ede6843c8d91c7b31/third_party/WebKit/LayoutTests/fast/frames/open-then-unload-expected.txt
[add] http://crrev.com/1f7c706b9c343d11d0011f3ede6843c8d91c7b31/third_party/WebKit/LayoutTests/fast/frames/open-then-unload.html
[modify] http://crrev.com/1f7c706b9c343d11d0011f3ede6843c8d91c7b31/third_party/WebKit/Source/core/frame/LocalFrame.cpp
[modify] http://crrev.com/1f7c706b9c343d11d0011f3ede6843c8d91c7b31/third_party/WebKit/Source/core/html/HTMLFrameOwnerElement.h
[modify] http://crrev.com/1f7c706b9c343d11d0011f3ede6843c8d91c7b31/third_party/WebKit/Source/core/loader/FrameLoader.cpp
[modify] http://crrev.com/1f7c706b9c343d11d0011f3ede6843c8d91c7b31/third_party/WebKit/Source/web/WebLocalFrameImpl.cpp


### dc...@chromium.org (2016-02-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-02-05)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/1f7c706b9c343d11d0011f3ede6843c8d91c7b31

commit 1f7c706b9c343d11d0011f3ede6843c8d91c7b31
Author: Daniel Cheng <dcheng@chromium.org>
Date: Fri Feb 05 06:48:21 2016


### ti...@google.com (2016-02-08)

Thanks again Daniel for the fast work here!

@sshruthi - please also approve for M49.

### ss...@google.com (2016-02-08)

Merge approved for M49 (branch 2623)

### go...@chromium.org (2016-02-08)

Please merge your change to M49 (branch: 2623) before 5:00 PM PST tomorrow,Tuesday [02/09] if order to make it to M49 Beta push on Wednesday [02/10].

### bu...@chromium.org (2016-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/55ca2716d9e29fa2b50eb3b15cdf98651ac8eb55

commit 55ca2716d9e29fa2b50eb3b15cdf98651ac8eb55
Author: Daniel Cheng <dcheng@chromium.org>
Date: Tue Feb 09 00:49:36 2016

Disable sub frame loads more reliably in frame detach.

Previously, guarding against attaching a new frame in frame detach
was done by inspecting LoadEventProgress. There are certain
operations, such as document.open(), that can cause LoadEventProgress
to never advance, causing the guard to get skipped.

BUG=577105

Review URL: https://codereview.chromium.org/1659013003

Cr-Commit-Position: refs/heads/master@{#373581}
(cherry picked from commit a4bcdcb1f8df4f7427e208201501a9d8e41e386b)

Review URL: https://codereview.chromium.org/1678343003 .

Cr-Commit-Position: refs/branch-heads/2623@{#314}
Cr-Branched-From: 92d77538a86529ca35f9220bd3cd512cbea1f086-refs/heads/master@{#369907}

[add] http://crrev.com/55ca2716d9e29fa2b50eb3b15cdf98651ac8eb55/third_party/WebKit/LayoutTests/fast/frames/open-then-unload-expected.txt
[add] http://crrev.com/55ca2716d9e29fa2b50eb3b15cdf98651ac8eb55/third_party/WebKit/LayoutTests/fast/frames/open-then-unload.html
[modify] http://crrev.com/55ca2716d9e29fa2b50eb3b15cdf98651ac8eb55/third_party/WebKit/Source/core/frame/LocalFrame.cpp
[modify] http://crrev.com/55ca2716d9e29fa2b50eb3b15cdf98651ac8eb55/third_party/WebKit/Source/core/html/HTMLFrameOwnerElement.h
[modify] http://crrev.com/55ca2716d9e29fa2b50eb3b15cdf98651ac8eb55/third_party/WebKit/Source/core/loader/FrameLoader.cpp
[modify] http://crrev.com/55ca2716d9e29fa2b50eb3b15cdf98651ac8eb55/third_party/WebKit/Source/web/WebLocalFrameImpl.cpp


### bu...@chromium.org (2016-02-09)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/55ca2716d9e29fa2b50eb3b15cdf98651ac8eb55

commit 55ca2716d9e29fa2b50eb3b15cdf98651ac8eb55
Author: Daniel Cheng <dcheng@chromium.org>
Date: Tue Feb 09 00:49:36 2016


### ti...@google.com (2016-02-09)

Congratulations - $7,500 for this great report!

Panel notes: $7500 for the report. Unfortunately, the fix ended up being significantly different from the patch provided so no additional patch bonus this time around.

We'll start payment shortly - thanks again.

### sh...@chromium.org (2016-05-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

This issue was migrated from crbug.com/chromium/577105?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083520)*

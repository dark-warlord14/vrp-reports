# Security: Universal XSS via persistence of subframes

| Field | Value |
|-------|-------|
| **Issue ID** | [40083201](https://issues.chromium.org/issues/40083201) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Loader |
| **Reporter** | ma...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2015-11-16 |
| **Bounty** | $8,000.00 |

## Description

## **VULNERABILITY DETAILS** From /third\_party/WebKit/Source/core/dom/Document.cpp:

bool FrameLoader::prepareForCommit()  

{  

PluginScriptForbiddenScope forbidPluginDestructorScripting;  

RefPtrWillBeRawPtr<DocumentLoader> pdl = m\_provisionalDocumentLoader;  

(...)  

if (m\_documentLoader) {  

client()->dispatchWillClose();  

dispatchUnloadEvent();  

}  

m\_frame->detachChildren();  

// The previous calls to dispatchUnloadEvent() and detachChildren() can  

// execute arbitrary script via things like unload events. If the executed  

// script intiates a new load or causes the current frame to be detached,  

// we need to abandon the current load.  

if (pdl != m\_provisionalDocumentLoader)  

return false;  

(...)  

if (m\_frame->document())  

m\_frame->document()->detach();  

m\_documentLoader = m\_provisionalDocumentLoader.release();  

m\_frame->updateFrameSecurityOrigin();

```
return true;  

```
## }

This logic depends on the assumption that dispatching the unload event will advance the navigated document's |LoadEventProgress| state to UnloadEventHandled, such that creation of subframes will be suppressed. The frame's document may change through synchronous loads, though. Normally, this is okay because the load will detach the provisional loader from the frame, and the |(pdl != m\_provisionalDocumentLoader)| check will catch this. However, if the replacement occurs through loading a javascript: URI during a page dismissal event, which suppresses detaching loaders, the provisional loader will remain attached. As a result, an attacker will be able to attach subframes that will persist in the frame tree of a cross-origin document.

**VERSION**  

Chrome 46.0.2490.86 (Stable)  

Chrome 47.0.2526.58 (Beta)  

Chrome 48.0.2560.0 (Dev)  

Chromium 49.0.2566.0 (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/zip, 1.8 KB)

## Timeline

### ma...@gmail.com (2015-11-16)

I've taken a stab at writing a patch for this. Please see https://codereview.chromium.org/1451123002

### dc...@chromium.org (2015-11-16)

Sigh.

### ji...@chromium.org (2015-11-16)

Thanks for reporting this issue and contributing your fix, marius.mlynski!

+dcheng@, could you update this issue with appropriate Cr component, security_severity, and security_impact labels? 

Thanks! 

### dc...@chromium.org (2015-11-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-17)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-11-17)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-11-17)

[Empty comment from Monorail migration]

### ss...@google.com (2015-11-17)

Marking as all OS, please change if not appropriate.

### bu...@chromium.org (2015-11-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e6fabc430b0f6a52dacc47860d66da09c79c310b

commit e6fabc430b0f6a52dacc47860d66da09c79c310b
Author: marius.mlynski <marius.mlynski@gmail.com>
Date: Wed Nov 18 01:00:59 2015

Block javascript: document navigations during page dismissal events.

This basically reflects the logic from FrameLoader::startLoad. Before this patch, javascript: document navigations could be performed during page dismissal events. This could be problematic, especially that dismissal events prevent loaders from being stopped or detached.

This patch adds a bail-out condition to FrameLoader::replaceDocumentWhileExecutingJavaScriptURL.

BUG=556724

Review URL: https://codereview.chromium.org/1451123002

Cr-Commit-Position: refs/heads/master@{#360242}

[modify] http://crrev.com/e6fabc430b0f6a52dacc47860d66da09c79c310b/AUTHORS
[add] http://crrev.com/e6fabc430b0f6a52dacc47860d66da09c79c310b/third_party/WebKit/LayoutTests/fast/events/javascript-uri-navigation-blocked-in-unload-handler-expected.txt
[add] http://crrev.com/e6fabc430b0f6a52dacc47860d66da09c79c310b/third_party/WebKit/LayoutTests/fast/events/javascript-uri-navigation-blocked-in-unload-handler.html
[modify] http://crrev.com/e6fabc430b0f6a52dacc47860d66da09c79c310b/third_party/WebKit/Source/core/loader/FrameLoader.cpp


### dc...@chromium.org (2015-11-18)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-11-18)

[Empty comment from Monorail migration]

### ss...@google.com (2015-11-18)

Approved for M47 (branch 2526)

### bu...@chromium.org (2015-11-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7f18334a16565705c53743dfb3c394f60d020a00

commit 7f18334a16565705c53743dfb3c394f60d020a00
Author: Daniel Cheng <dcheng@chromium.org>
Date: Wed Nov 18 03:05:06 2015

Block javascript: document navigations during page dismissal events.

This basically reflects the logic from FrameLoader::startLoad. Before this patch, javascript: document navigations could be performed during page dismissal events. This could be problematic, especially that dismissal events prevent loaders from being stopped or detached.

This patch adds a bail-out condition to FrameLoader::replaceDocumentWhileExecutingJavaScriptURL.

BUG=556724

Review URL: https://codereview.chromium.org/1451123002

Cr-Commit-Position: refs/heads/master@{#360242}
(cherry picked from commit e6fabc430b0f6a52dacc47860d66da09c79c310b)

Review URL: https://codereview.chromium.org/1461503002 .

Cr-Commit-Position: refs/branch-heads/2526@{#448}
Cr-Branched-From: cb947c0153db0ec02a8abbcb3ca086d88bf6006f-refs/heads/master@{#352221}

[modify] http://crrev.com/7f18334a16565705c53743dfb3c394f60d020a00/AUTHORS
[add] http://crrev.com/7f18334a16565705c53743dfb3c394f60d020a00/third_party/WebKit/LayoutTests/fast/events/javascript-uri-navigation-blocked-in-unload-handler-expected.txt
[add] http://crrev.com/7f18334a16565705c53743dfb3c394f60d020a00/third_party/WebKit/LayoutTests/fast/events/javascript-uri-navigation-blocked-in-unload-handler.html
[modify] http://crrev.com/7f18334a16565705c53743dfb3c394f60d020a00/third_party/WebKit/Source/core/loader/FrameLoader.cpp


### cl...@chromium.org (2015-11-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-11-18)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/7f18334a16565705c53743dfb3c394f60d020a00

commit 7f18334a16565705c53743dfb3c394f60d020a00
Author: Daniel Cheng <dcheng@chromium.org>
Date: Wed Nov 18 03:05:06 2015


### ti...@google.com (2015-11-23)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-01)

Maruisz - $8,000 for this report ($7500 for the report + $500 for the patch). Thanks again as always for the excellent report :)

### dc...@chromium.org (2016-01-25)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/556724?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083201)*

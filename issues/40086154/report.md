# Security: Universal XSS through bypassing ScopedPageSuspender with closing windows

| Field | Value |
|-------|-------|
| **Issue ID** | [40086154](https://issues.chromium.org/issues/40086154) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ma...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2016-12-05 |
| **Bounty** | $8,837.00 |

## Description

**VULNERABILITY DETAILS**  

ScopedPageSuspender works by taking pages from Page::ordinaryPages() and marking them as suspended. When window.close() is called, the following operations are performed:

## From /third\_party/WebKit/Source/web/ChromeClientImpl.cpp:

void ChromeClientImpl::closeWindowSoon() {  

// Make sure this Page can no longer be found by JS.  

m\_webView->page()->willBeClosed();

// Make sure that all loading is stopped. Ensures that JS stops executing!  

m\_webView->mainFrame()->stopLoading();

## if (m\_webView->client()) m\_webView->client()->closeWidgetSoon(); }

|m\_webView->page()->willBeClosed()| removes the associated page from the ordinaryPages set. Therefore, suspenders instantiated later, for example during |m\_webView->mainFrame()->stopLoading()|, won't include the closing page. This allows an attacker to circumvent the suspender and perform synchronous loads in unexpected circumstances.

**VERSION**  

Chrome 55.0.2883.75 (Stable)  

Chrome 55.0.2883.75 (Beta)  

Chrome 56.0.2924.14 (Dev)  

Chromium 57.0.2943.0 + Pepper Flash (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 3.0 KB)

## Timeline

### oc...@chromium.org (2016-12-05)

dcheng, would you mind helping with finding the right owner for this? Thanks.

[Monorail components: Blink]

### dc...@chromium.org (2016-12-05)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-12-05)

Meh. I was hoping to avoid maintaining two sets after https://codereview.chromium.org/2174263002, but it appears to be unavoidable.

### sh...@chromium.org (2016-12-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-06)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-12-14)

[Empty comment from Monorail migration]

### mm...@chromium.org (2016-12-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-12-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0879cb1c4d5e7a53d060bfb7cf7cf9ea05aced72

commit 0879cb1c4d5e7a53d060bfb7cf7cf9ea05aced72
Author: dcheng <dcheng@chromium.org>
Date: Thu Dec 22 10:36:49 2016

Make sure pages that are closing but not yet closed are still suspended.

BUG=671102

Review-Url: https://codereview.chromium.org/2580703003
Cr-Commit-Position: refs/heads/master@{#440376}

[modify] https://crrev.com/0879cb1c4d5e7a53d060bfb7cf7cf9ea05aced72/third_party/WebKit/Source/core/frame/DOMWindow.cpp
[modify] https://crrev.com/0879cb1c4d5e7a53d060bfb7cf7cf9ea05aced72/third_party/WebKit/Source/core/page/FrameTree.cpp
[modify] https://crrev.com/0879cb1c4d5e7a53d060bfb7cf7cf9ea05aced72/third_party/WebKit/Source/core/page/Page.cpp
[modify] https://crrev.com/0879cb1c4d5e7a53d060bfb7cf7cf9ea05aced72/third_party/WebKit/Source/core/page/Page.h
[modify] https://crrev.com/0879cb1c4d5e7a53d060bfb7cf7cf9ea05aced72/third_party/WebKit/Source/core/page/ScopedPageSuspender.cpp
[modify] https://crrev.com/0879cb1c4d5e7a53d060bfb7cf7cf9ea05aced72/third_party/WebKit/Source/core/page/ScopedPageSuspender.h
[modify] https://crrev.com/0879cb1c4d5e7a53d060bfb7cf7cf9ea05aced72/third_party/WebKit/Source/web/ChromeClientImpl.cpp
[modify] https://crrev.com/0879cb1c4d5e7a53d060bfb7cf7cf9ea05aced72/third_party/WebKit/Source/web/tests/ChromeClientImplTest.cpp
[modify] https://crrev.com/0879cb1c4d5e7a53d060bfb7cf7cf9ea05aced72/third_party/WebKit/Source/web/tests/WebViewTest.cpp


### dc...@chromium.org (2016-12-27)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-12-27)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-12-27)

Note that we already merged a generic fix for these class of UXSS in https://crbug.com/chromium/674203, but this is still a potential correctness issue.

### di...@chromium.org (2016-12-27)

Your change meets the bar and is auto-approved for M56 (branch: 2924)

### sh...@chromium.org (2016-12-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-30)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-01-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-01-02)

[Empty comment from Monorail migration]

### dc...@chromium.org (2017-01-03)

So there's a lot of conflicts; resolving them manually is tricky.

The simplest path forward is to merge https://codereview.chromium.org/2526163002, and then this CL, but I'm not sure if that's still considered OK.

### bu...@google.com (2017-01-03)

That sounds fine to me, approving both changes for merge into M56

### bu...@chromium.org (2017-01-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fad76601729f6b957274071fb0f1d33072ab72c1

commit fad76601729f6b957274071fb0f1d33072ab72c1
Author: Daniel Cheng <dcheng@chromium.org>
Date: Tue Jan 03 21:35:21 2017

Rename blink::Page's load deferral to suspension

This CL renames:
 * ScopedPageLoadDeferrer to ScopedPageSuspender,
 * blink::Page::defersLoading() to suspended(), and
 * blink::Page::setDefersLoading() to setSuspended().

blink::setDefersLoading does not only defer loadings, but also suspends
all associated ExecutionContext and ActiveDOMObjects.

Review-Url: https://codereview.chromium.org/2526163002
Cr-Commit-Position: refs/heads/master@{#434378}
(cherry picked from commit 5ad6641ca96fc131e8268f649bc6db71170ad736)

BUG=671102

Review-Url: https://codereview.chromium.org/2611753003 .
Cr-Commit-Position: refs/branch-heads/2924@{#655}
Cr-Branched-From: 3a87aecc31cd1ffe751dd72c04e5a96a1fc8108a-refs/heads/master@{#433059}

[modify] https://crrev.com/fad76601729f6b957274071fb0f1d33072ab72c1/third_party/WebKit/Source/core/dom/Document.cpp
[modify] https://crrev.com/fad76601729f6b957274071fb0f1d33072ab72c1/third_party/WebKit/Source/core/loader/DocumentLoader.cpp
[modify] https://crrev.com/fad76601729f6b957274071fb0f1d33072ab72c1/third_party/WebKit/Source/core/loader/FrameFetchContext.cpp
[modify] https://crrev.com/fad76601729f6b957274071fb0f1d33072ab72c1/third_party/WebKit/Source/core/loader/FrameLoader.cpp
[modify] https://crrev.com/fad76601729f6b957274071fb0f1d33072ab72c1/third_party/WebKit/Source/core/loader/NavigationScheduler.cpp
[modify] https://crrev.com/fad76601729f6b957274071fb0f1d33072ab72c1/third_party/WebKit/Source/core/page/BUILD.gn
[modify] https://crrev.com/fad76601729f6b957274071fb0f1d33072ab72c1/third_party/WebKit/Source/core/page/ChromeClient.cpp
[modify] https://crrev.com/fad76601729f6b957274071fb0f1d33072ab72c1/third_party/WebKit/Source/core/page/FocusController.cpp
[modify] https://crrev.com/fad76601729f6b957274071fb0f1d33072ab72c1/third_party/WebKit/Source/core/page/Page.cpp
[modify] https://crrev.com/fad76601729f6b957274071fb0f1d33072ab72c1/third_party/WebKit/Source/core/page/Page.h
[rename] https://crrev.com/fad76601729f6b957274071fb0f1d33072ab72c1/third_party/WebKit/Source/core/page/ScopedPageSuspender.cpp
[rename] https://crrev.com/fad76601729f6b957274071fb0f1d33072ab72c1/third_party/WebKit/Source/core/page/ScopedPageSuspender.h
[modify] https://crrev.com/fad76601729f6b957274071fb0f1d33072ab72c1/third_party/WebKit/Source/web/ChromeClientImpl.cpp
[modify] https://crrev.com/fad76601729f6b957274071fb0f1d33072ab72c1/third_party/WebKit/Source/web/WebViewImpl.cpp
[modify] https://crrev.com/fad76601729f6b957274071fb0f1d33072ab72c1/third_party/WebKit/Source/web/tests/ChromeClientImplTest.cpp
[modify] https://crrev.com/fad76601729f6b957274071fb0f1d33072ab72c1/third_party/WebKit/Source/web/tests/WebFrameTest.cpp
[modify] https://crrev.com/fad76601729f6b957274071fb0f1d33072ab72c1/third_party/WebKit/Source/web/tests/WebViewTest.cpp


### bu...@chromium.org (2017-01-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dc3f2823c1485ab302a2144ec1fcfe37f0e5af50

commit dc3f2823c1485ab302a2144ec1fcfe37f0e5af50
Author: Daniel Cheng <dcheng@chromium.org>
Date: Tue Jan 03 21:44:44 2017

Make sure pages that are closing but not yet closed are still suspended.

BUG=671102

Review-Url: https://codereview.chromium.org/2580703003
Cr-Commit-Position: refs/heads/master@{#440376}
(cherry picked from commit 0879cb1c4d5e7a53d060bfb7cf7cf9ea05aced72)

Review-Url: https://codereview.chromium.org/2616513002 .
Cr-Commit-Position: refs/branch-heads/2924@{#656}
Cr-Branched-From: 3a87aecc31cd1ffe751dd72c04e5a96a1fc8108a-refs/heads/master@{#433059}

[modify] https://crrev.com/dc3f2823c1485ab302a2144ec1fcfe37f0e5af50/third_party/WebKit/Source/core/frame/DOMWindow.cpp
[modify] https://crrev.com/dc3f2823c1485ab302a2144ec1fcfe37f0e5af50/third_party/WebKit/Source/core/page/FrameTree.cpp
[modify] https://crrev.com/dc3f2823c1485ab302a2144ec1fcfe37f0e5af50/third_party/WebKit/Source/core/page/Page.cpp
[modify] https://crrev.com/dc3f2823c1485ab302a2144ec1fcfe37f0e5af50/third_party/WebKit/Source/core/page/Page.h
[modify] https://crrev.com/dc3f2823c1485ab302a2144ec1fcfe37f0e5af50/third_party/WebKit/Source/core/page/ScopedPageSuspender.cpp
[modify] https://crrev.com/dc3f2823c1485ab302a2144ec1fcfe37f0e5af50/third_party/WebKit/Source/core/page/ScopedPageSuspender.h
[modify] https://crrev.com/dc3f2823c1485ab302a2144ec1fcfe37f0e5af50/third_party/WebKit/Source/web/ChromeClientImpl.cpp
[modify] https://crrev.com/dc3f2823c1485ab302a2144ec1fcfe37f0e5af50/third_party/WebKit/Source/web/tests/ChromeClientImplTest.cpp
[modify] https://crrev.com/dc3f2823c1485ab302a2144ec1fcfe37f0e5af50/third_party/WebKit/Source/web/tests/WebViewTest.cpp


### aw...@chromium.org (2017-01-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-12)

Hi!  The panel decided to reward $7,500 for this bug, and a $1337 bonus for the fix in https://chromium.googlesource.com/chromium/src/+/783e19486c

### aw...@chromium.org (2017-01-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/671102?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/674203]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086154)*

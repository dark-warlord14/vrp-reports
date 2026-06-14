# Heap-use-after-free in WebCore::ResourceFetcher::frame()

| Field | Value |
|-------|-------|
| **Issue ID** | [40078668](https://issues.chromium.org/issues/40078668) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | at...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2014-01-10 |
| **Bounty** | $1,000.00 |

## Description


Tested on:

OS: Ubuntu 12.04

Chromium: 34.0.1777.0 (Developer Build 243865)


To reproduce this issue you need both attached files in same folder. run.html is just a wrapper-file that loads the actual repro-file inside an iframe to reproduce the crash.

This issue feels like a race condition and I don't think that CF will be able to reproduce it reliably. 

You have to have high CPU load when executing the repro-file. With the attached minimized test case the best way to reproduce the issue was the following command:

chrome --no-sandbox --incognito run.html run.html run.html run.html run.html run.html run.html run.html run.html run.html run.html run.html run.html run.html

With that command at least one tab crashed every time. If the tab doesn't crash within few refreshes after startup it won't crash. I would guess that has something to do with caching, but I was unable to make the crashing more reliable with any of the cache disabling flags I know about.

If required I can give the original repro-file, but its size is over 560Kb. 

ASAN-report:

==12427==ERROR: AddressSanitizer: heap-use-after-free on address 0x61100003a288 at pc 0x7fe49b1eb8d4 bp 0x7fffd648f8c0 sp 0x7fffd648f8b8
READ of size 8 at 0x61100003a288 thread T0 (chrome)
    #0 0x7fe49b1eb8d3 in WebCore::ResourceFetcher::frame() const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/fetch/ResourceFetcher.cpp:253:0
    #1 0x7fe49b1dc48d in WebCore::Resource::load(WebCore::ResourceFetcher*, WebCore::ResourceLoaderOptions const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/fetch/Resource.cpp:167:0
    #2 0x7fe49b1ca5e2 in WebCore::FontResource::beginLoadIfNeeded(WebCore::ResourceFetcher*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/fetch/FontResource.cpp:76:0
    #3 0x7fe49b055d0f in WebCore::FontLoader::loadPendingFonts() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/css/CSSFontSelector.cpp:84:0
    #4 0x7fe49a3c9c71 in WebCore::ThreadTimers::sharedTimerFiredInternal() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/ThreadTimers.cpp:134:0
    #5 0x7fe49a3c96c4 in WebCore::ThreadTimers::sharedTimerFired() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/ThreadTimers.cpp:108:0
.
.
.
0x61100003a3c8 is located 72 bytes inside of 240-byte region [0x61100003a380,0x61100003a470)
freed by thread T0 (chrome) here:
    #0 0x7fe496d61309 in __interceptor_free _asan_rtl_:0
    #1 0x7fe49a005d17 in WebCore::Document::~Document() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:536:0
    #2 0x7fe49acff10d in WebCore::HTMLDocument::~HTMLDocument() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/html/HTMLDocument.cpp:79:0
    #3 0x7fe49a0fddc6 in derefIfNotNull<WebCore::Document> /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/PassRefPtr.h:56:0
    #4 0x7fe49a0fddc6 in ~RefPtr /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/RefPtr.h:49:0
    #5 0x7fe49a0fddc6 in ~RefPtr /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/RefPtr.h:49:0
    #6 0x7fe49a0fddc6 in WTF::RefPtr<WebCore::Document>::operator=(WebCore::Document*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/RefPtr.h:113:0
    #7 0x7fe49b22f9e0 in WebCore::DOMWindow::clearDocument() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/frame/DOMWindow.cpp:361:0
    #8 0x7fe49b2322d4 in WebCore::DOMWindow::~DOMWindow() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/frame/DOMWindow.cpp:513:0
.
.
.


## Attachments

- [chrome-heap-use-after-free-WebCoreResourceFetcherframe.html](attachments/chrome-heap-use-after-free-WebCoreResourceFetcherframe.html) (text/html, 1.5 KB)
- [run.html](attachments/run.html) (text/html, 177 B)

## Timeline

### jl...@chromium.org (2014-01-10)

morrita@, japhet@, you both seem to have worked in this area, could one of you take a look ?

### jl...@chromium.org (2014-01-10)

[Empty comment from Monorail migration]

### ja...@chromium.org (2014-01-10)

Looks like we're UAFing the ResourceFetcher? If so, FontLoader::loadPendingFonts() should probably protect the ResourceFetcher or the Document.

### cl...@chromium.org (2014-01-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-13)

[Empty comment from Monorail migration]

### ja...@chromium.org (2014-01-14)

morrita@, any chance you'd be willing to look at this one? I'm feeling a bit overwhelmed by my bug backlog at the moment.

### [Deleted User] (2014-01-15)

Sure, let me take a look.

### cl...@chromium.org (2014-01-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-23)

morrita@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-01-25)

[Empty comment from Monorail migration]

### me...@chromium.org (2014-01-27)

Doesn't reproduce on M32, reproduces on M33 beta.

### cl...@chromium.org (2014-01-27)

[Empty comment from Monorail migration]

### [Deleted User] (2014-01-30)

Sorry, on my plate.


### [Deleted User] (2014-02-06)

[Empty comment from Monorail migration]

### [Deleted User] (2014-02-07)

According to git blame, this should be same as crbug.com/336921 (I cannot see it)
and should've been fixed at https://src.chromium.org/viewvc/blink?revision=165824&view=revision




### bu...@chromium.org (2014-02-07)

Is there a merge required here?

### [Deleted User] (2014-02-07)

No need to merge.

### ks...@chromium.org (2014-02-07)

Yes, should be the same as https://crbug.com/chromium/336921.

### in...@chromium.org (2014-02-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-02-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-09)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-03-04)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-14)

My apologies for the delay here - $1000 for this one. I'll start the payment process today.

### ti...@chromium.org (2014-04-15)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-30)

Processing via our e-payment system can take up to 30 days, but the reward should be on its way to you.


### cl...@chromium.org (2014-05-16)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2014-05-16)

This bug is a regression and does not impact stable. Removing incorrectly added Release-0-M33 label.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/333378?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/336921]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078668)*

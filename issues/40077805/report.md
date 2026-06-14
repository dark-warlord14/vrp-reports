# Heap-use-after-free in WebCore::Document::detach

| Field | Value |
|-------|-------|
| **Issue ID** | [40077805](https://issues.chromium.org/issues/40077805) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | cl...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2013-07-18 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes chrome's ASAN build. A frame object seems to be used after it was freed.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-211418  

Operating System: Linux 64-bit

**REPRODUCTION CASE**  

The testcase is attached as crash.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: see log.txt for ASAN output

## Attachments

- [log.txt](attachments/log.txt) (text/plain; charset=us-ascii, 11.8 KB)
- [crash.html](attachments/crash.html) (text/html; charset=us-ascii, 1.6 KB)

## Timeline

### cl...@chromium.org (2013-07-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4873821647536128

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61700000d9a0
Crash State:
  - crash stack -
  WebCore::Document::detach
  WebCore::DOMWindow::setDocument
  - free stack -
  WebCore::FrameView::~FrameView
  WebCore::FrameView::~FrameView
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=204670:204818

Minimized Testcase (1.46 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95CDIKr3hGjXJ7XbJJRtKefzqvJ75T114vna6DsD3P5UK2Du9Va5qJxRPZB8havSu7qN_gwxrbm2VwFyVzPmZxKPjbfAyzSfQEAHB2bZhjHzbeeLdAj2WuLzLIlMs1DyFNXQOKXQP_JYCQ5sHfjviYaLs7-QA



### in...@chromium.org (2013-07-19)

From regression range, looks like another fallout from http://src.chromium.org/viewvc/blink?view=rev&revision=151960. :( Daniel, can you please take a look.

### in...@chromium.org (2013-07-23)

We can't leave a high severity regression in the tree. If you didn't get a chance to look, can you please revert soon.

### dc...@chromium.org (2013-07-23)

I've been looking at the bug this past weekend. I'm trying to understand the best way to fix it. Reverting it will be tricky since there are at least two or three other patches that would have to be reverted as well.

### dc...@chromium.org (2013-07-24)

Here's a basic explanation of the bug and why it occurs after http://src.chromium.org/viewvc/blink?view=rev&revision=151960.

Before: In DocumentLoader::createWriterFor()--formerly known as DocumentWriter::begin()--we used to call Frame::setDocument() to transition. This would detach the old Document immediately.

After: DocumentLoader::createWriterFor() now invokes Frame::setDOMWindow() followed by DOMWindow::setDocument(). However, if someone (such as JS) has a reference to the old DOMWindow (call it x), then x will not be destroyed at this point. This means that Document::attached() is still true for x->document().
At some later point, the original Frame associated with x is destroyed (for example, by a navigation). At some pointer after that, V8 garbage collects DOM objects and destroys DOMWindow x. ~DOMWindow() tries to detach the Document in its destructor and explosions, since Document's m_frame pointers points to a destroyed object.

The fix I'm working on consists of several parts:
- Moving detach() out of the DOMWindow dtor and asserting that the Document is always detached there.
- Making sure the Document is correctly detached elsewhere. I'm trying to make sure that this is handled correctly.

One other thing I want to verify is that FrameLoader::clear() is working as expected. I'm not sure if having javascript: URLs is causing the majority of the work in FrameLoader::clear() to be skipped, since if FrameLoader::begin() is not invoked for javascript: URLs, then FrameLoader::clear() will be a no-op.

### in...@chromium.org (2013-07-24)

[Empty comment from Monorail migration]

### dc...@chromium.org (2013-07-31)

[Empty comment from Monorail migration]

### jl...@chromium.org (2013-08-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-08-02)

friendly ping!

### dc...@chromium.org (2013-08-02)

Sorry, today's my last day as Blink sheriff. It's been rather... interesting.

### bu...@chromium.org (2013-08-21)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=156496

------------------------------------------------------------------------
r156496 | dcheng@chromium.org | 2013-08-21T20:14:46.815351Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/frames/navigation-in-pagehide.html?r1=156496&r2=156495&pathrev=156496
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/loader/DocumentLoader.cpp?r1=156496&r2=156495&pathrev=156496
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/loader/FrameLoader.h?r1=156496&r2=156495&pathrev=156496
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/testing/Internals.cpp?r1=156496&r2=156495&pathrev=156496
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Document.cpp?r1=156496&r2=156495&pathrev=156496
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/loader/FrameLoaderTypes.h?r1=156496&r2=156495&pathrev=156496
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/page/DOMWindow.cpp?r1=156496&r2=156495&pathrev=156496
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/frames/navigation-in-pagehide-expected.txt?r1=156496&r2=156495&pathrev=156496
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/page/Frame.cpp?r1=156496&r2=156495&pathrev=156496
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/loader/FrameLoader.cpp?r1=156496&r2=156495&pathrev=156496

Make sure the Document is always detached before it's too late.

During a navigation, FrameLoader::clear() typically detaches the
Document before DocumentLoader::createWriterFor() replaces the
DOMWindow and cancels all pending navigations.

However, synchronous navigations during a pagehide event can cause
FrameLoader::clear() to be re-entered, causing it to skip the detach.
This wasn't a problem before r151960, since the Frame::setDocument()
call would detach the Document if it was still attached.

Now, we manually check if the original Document is still attached
before replacing the DOMWindow. If it's still attached, then we
detach it anyway. As a bonus, this fix revealed an older bug where
AXObjectCache's timer can fire for destroyed Documents. To fix that,
FrameLoader::clear() uses prepareForDestruction() instead of detach().

BUG=261836, 268642

Review URL: https://chromiumcodereview.appspot.com/21109008
------------------------------------------------------------------------

### in...@chromium.org (2013-08-21)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-08-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-08-23)

ClusterFuzz has detected this issue as fixed in range 218939:218946.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4873821647536128

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61700000d9a0
Crash State:
  - crash stack -
  WebCore::Document::detach
  WebCore::DOMWindow::setDocument
  - free stack -
  WebCore::FrameView::~FrameView
  WebCore::FrameView::~FrameView
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=204670:204818
Fixed: https://cluster-fuzz.appspot.com/revisions?range=218939:218946

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95CDIKr3hGjXJ7XbJJRtKefzqvJ75T114vna6DsD3P5UK2Du9Va5qJxRPZB8havSu7qN_gwxrbm2VwFyVzPmZxKPjbfAyzSfQEAHB2bZhjHzbeeLdAj2WuLzLIlMs1DyFNXQOKXQP_JYCQ5sHfjviYaLs7-QA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-09-12)

Please merge your change to the m30 branch (1599) by early next week [using drover]. We have m30 beta coming next week and we want all the security changes in by that time. 

### bu...@chromium.org (2013-09-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157701

------------------------------------------------------------------------
r157701 | dcheng@chromium.org | 2013-09-12T21:03:51.286234Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/page/DOMWindow.cpp?r1=157701&r2=157700&pathrev=157701
   A http://src.chromium.org/viewvc/blink/branches/chromium/1599/LayoutTests/fast/frames/navigation-in-pagehide-expected.txt?r1=157701&r2=157700&pathrev=157701
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/loader/FrameLoader.cpp?r1=157701&r2=157700&pathrev=157701
   A http://src.chromium.org/viewvc/blink/branches/chromium/1599/LayoutTests/fast/frames/navigation-in-pagehide.html?r1=157701&r2=157700&pathrev=157701
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/loader/DocumentLoader.cpp?r1=157701&r2=157700&pathrev=157701
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/loader/FrameLoader.h?r1=157701&r2=157700&pathrev=157701
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/testing/Internals.cpp?r1=157701&r2=157700&pathrev=157701
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/dom/Document.cpp?r1=157701&r2=157700&pathrev=157701
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/loader/FrameLoaderTypes.h?r1=157701&r2=157700&pathrev=157701

Merge 156496 "Make sure the Document is always detached before i..."

> Make sure the Document is always detached before it's too late.
> 
> During a navigation, FrameLoader::clear() typically detaches the
> Document before DocumentLoader::createWriterFor() replaces the
> DOMWindow and cancels all pending navigations.
> 
> However, synchronous navigations during a pagehide event can cause
> FrameLoader::clear() to be re-entered, causing it to skip the detach.
> This wasn't a problem before r151960, since the Frame::setDocument()
> call would detach the Document if it was still attached.
> 
> Now, we manually check if the original Document is still attached
> before replacing the DOMWindow. If it's still attached, then we
> detach it anyway. As a bonus, this fix revealed an older bug where
> AXObjectCache's timer can fire for destroyed Documents. To fix that,
> FrameLoader::clear() uses prepareForDestruction() instead of detach().
> 
> BUG=261836, 268642
> 
> Review URL: https://chromiumcodereview.appspot.com/21109008

TBR=dcheng@chromium.org

Review URL: https://codereview.chromium.org/23523057
------------------------------------------------------------------------

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### in...@chromium.org (2013-09-26)

Removing incorrect Release-0 which is reserved for bugs impacting stable.

### sc...@gmail.com (2013-09-28)

Congrats @cloudfuzzer, a $3000 reward for this one. This is our largest reward in our first batch of rewards under our new raised rewards.

The ASAN stack clearly shows JS control between the free and the use, and the used object (Frame) is not yet in any of our heap partitions; furthmore the "use" appears to be a pointer, etc.

To get to $5000 you'd need to provide a similar simple analysis yourself, and perhaps provide a repro that faults at a 0x4141414141414141 pointer?

### pa...@chromium.org (2013-10-18)

OK, kicked off payment for this one (and the rest). Expect something in a few weeks. Thanks again cloudfuzzer :)

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/261836?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/268642]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077805)*

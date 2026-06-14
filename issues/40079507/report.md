# WebCore::SVGUseElement::updateContainerOffsets ExecAV@Arbitrary (1dc75f12fe3750aa1828ea20506a5d54)

| Field | Value |
|-------|-------|
| **Issue ID** | [40079507](https://issues.chromium.org/issues/40079507) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ao...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2010-03-01 |
| **Bounty** | $500.00 |

## Description

Opening the attached SVG file or a page containing it causes a segmentation
fault in WebCore::SVGUseElement::setHrefBaseValue in 32-bit Ubuntu 9.10.
Builds 36515 up to the current 40259 appear to be affected. In 64-bit
Fedora 12 the issue manifests as the tab getting stuck in loading, sad tab
or a browser crash (segmentation fault after a possible double-free or
memory corruption) when using Google Chrome  5.0.307.9 (Official Build
39052) beta or Chromium 5.0.339.0 (Developer Build 40152).

I have no proof that this is exploitable. Reported as a security issue to
be on the safe side.

## Attachments

- [bad2.svg](attachments/bad2.svg) (text/plain; charset=us-ascii, 133 B)
- [svg2-gdb.txt](attachments/svg2-gdb.txt) (text/plain, English; charset=us-ascii, 6.4 KB)
- [WebCore..SVGUseElement..updateContainerOffsets ExecAV@Arbitrary (1dc75f12fe3750aa1828ea20506a5d54).html](attachments/WebCore..SVGUseElement..updateContainerOffsets ExecAV@Arbitrary (1dc75f12fe3750aa1828ea20506a5d54).html) (exported SGML document text, 452.9 KB)

## Timeline

### sk...@chromium.org (2010-03-01)

Using 5.0.339.0 (40179), I see evidence of an exploitable vulnerability. I tried three times and always got this exception:

Id:          WebCore::SVGUseElement::updateContainerOffsets ExecAV@Arbitrary (1dc75f12fe3750aa1828ea20506a5d54)
Description: Attempt to execute non-executable arbitrary memory @ 0x02895030 in WebCore::SVGUseElement::updateContainerOffsets
Stack:
  [Missing symbols]
  WebCore::SVGUseElement::updateContainerOffsets
  WebCore::SVGUseElement::buildShadowAndInstanceTree
  WebCore::RenderSVGShadowTreeRootContainer::updateFromElement
  WebCore::ContainerNode::dispatchPostAttachCallbacks
  WebCore::ContainerNode::resumePostAttachCallbacks
  WebCore::ContainerNode::appendChild
  WebCore::XMLTokenizer::insertErrorMessageBlock
  WebCore::XMLTokenizer::finish
  WebCore::FrameLoader::endIfNotLoadingMainResource
  WebCore::FrameLoader::finishedLoading
  WebCore::MainResourceLoader::didFinishLoading
  WebCore::ResourceLoader::didFinishLoading
  webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest
  ResourceDispatcher::OnRequestComplete
  IPC::MessageWithTuple<...><...><...><...><...>::Dispatch<...><...><...><...>
  ResourceDispatcher::DispatchMessageW
  ResourceDispatcher::OnMessageReceived
  ChildThread::OnMessageReceived
  RunnableMethod<...><...>::Run
  MessageLoop::RunTask
  MessageLoop::DoWork
  base::MessagePumpDefault::Run
  MessageLoop::RunInternal
  MessageLoop::Run
  RendererMain

Attached are details grabbed from the debugger.

The repro contains this:

<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<g id="foo"><use/></g>
<use xlink:href="#foo"/> 

It seems to be that the <use/> tag is the linkely culprit: we are already aware of problems in the code that implements it and a mayor 
rewrite is in progress. I'll try to find the bug for that and mark this as a duplicate if appropriate.

### sc...@gmail.com (2010-03-02)

Ugh, affects 4.1.249.1021 but not 4.0.249.89
http://crash/reportdetail?reportid=87fbaea255d7f8eb
(In this instance, it's a wild read, but the result of that is clearly used as the 
basis of a wild write so, exploitable.... probably a use after free)
  mov ecx,dword ptr [ecx+4]    (ecx wild!!! 0xabcd1204)
  mov dword ptr <addr>[ecx+esi], <addr>

This is very welcome report. Thank you, Aki.

### sc...@gmail.com (2010-03-02)

[Empty comment from Monorail migration]

### ma...@gmail.com (2010-03-02)

Has anyone tried this with Safari and a WebKit nightly?

It looks like something that would need to get fixed upstream.

### sc...@gmail.com (2010-03-02)

https://bugs.webkit.org/show_bug.cgi?id=35603

### [Deleted User] (2010-03-03)

I can't see the WebKit bug. Is it assigned already and expected to be fixed in the next 
few days...?

### sk...@chromium.org (2010-03-04)

It's fixed: https://crbug.com/chromium/37061#c9 From Oliver Hunt 2010-03-04 00:58:33 PST (-) [reply] 
Committed r55511
http://trac.webkit.org/changeset/55511

I tried to add you to the webkit bug as oritm@chromium.org, but apparently you're not 
registered there under that email address, so I can't.

### ia...@gmail.com (2010-03-04)

Dimitry,

Can you merge this on to the 249 branch?

### ia...@gmail.com (2010-03-04)

Dave, I think you're sheriff today, so assigning over to you?

Context: There's a bad security bug that we know about, and we're trying to get a 4.1 
update out today. We would really like to get this patch in the update. Sadly, it 
looks like this patch is causing crashes on the buildbots - dglazkov wasn't sure if 
it was an assert() in the code that was no longer correct, or what.

Is there any chance you can look into this one? Really would like to get this patch 
merged to the 249 branch if possible.

### le...@chromium.org (2010-03-05)

First, it looks like it should be safe to pick up this fix as is. If you need to run debug, then remove the " 
ASSERT(frameCount());" in  ImageSource::frameIsCompleteAtIndex in 
chromium/src/third_party/WebKit/WebCore/platform/graphics/cg/ImageSourceCG.cpp.

Details:

Next, here's how to repro the current issue, run test_shell with full paths to 
  chromium/src/third_party/WebKit/LayoutTests/svg/custom/tiling-regular-hexagonal-crash.svg
  chromium/src/third_party/WebKit/LayoutTests/svg/custom/transform-ignore-after-invalid.svg
The second one crashes. For some reason running the second one alone didn't seem to cause the assert.

The assert occurs is this one:
  bool ImageSource::frameIsCompleteAtIndex(size_t index)
  {
      ASSERT(frameCount());

This happens because the m_decoder is 0 (because the image that was attempted to be created was 156 X 0.

Regardless, the rest of the code in this function handles this nicely and there are no problems. I need to do 
more investigation to understand if the assert can be removed. (When the assert fires, it doesn't seem to be 
harmful, but it does seem to be an unexpected occurrence so in that sense it may be valid.)



### le...@chromium.org (2010-03-05)

Update: WebKit r55169 (which was on Feb 23, 2010) added this assert. Previously very similar code would run 
without doing this assert, so I think the assert was added incorrectly.

Investigation still ongoing.


### bu...@gmail.com (2010-03-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=40827 

------------------------------------------------------------------------
r40827 | mal@chromium.org | 2010-03-05 23:16:00 -0800 (Fri, 05 Mar 2010) | 5 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/use-empty-reference-expected.txt?r1=40827&r2=40826
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/use-nested-disallowed-target-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/use-nested-disallowed-target.svg
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/use-nested-missing-target-added-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/use-nested-missing-target-added.svg
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/use-nested-missing-target-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/use-nested-missing-target-removed-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/use-nested-missing-target-removed.svg
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/use-nested-missing-target.svg
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/use-nested-notarget-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/use-nested-notarget.svg

Check in test changes for Webkit https://crbug.com/chromium/35603.

BUG= 37061
TEST= yes
Review URL: http://codereview.chromium.org/669236
------------------------------------------------------------------------


### bu...@gmail.com (2010-03-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=40828 

------------------------------------------------------------------------
r40828 | mal@chromium.org | 2010-03-05 23:17:44 -0800 (Fri, 05 Mar 2010) | 5 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/svg/SVGUseElement.cpp?r1=40828&r2=40827

Merge WebKit r55511

BUG= 37061
TEST= see LayoutTests
Review URL: http://codereview.chromium.org/669237
------------------------------------------------------------------------


### bu...@gmail.com (2010-03-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=40829 

------------------------------------------------------------------------
r40829 | mal@chromium.org | 2010-03-05 23:23:42 -0800 (Fri, 05 Mar 2010) | 5 lines
Changed paths:
   A http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/relative-sized-deep-shadow-tree-content-expected.checksum
   A http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/relative-sized-deep-shadow-tree-content-expected.png
   A http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/relative-sized-deep-shadow-tree-content-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/relative-sized-shadow-tree-content-expected.checksum
   A http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/relative-sized-shadow-tree-content-expected.png
   A http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/relative-sized-shadow-tree-content-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win-vista/LayoutTests/svg/custom/use-empty-reference-expected.checksum
   A http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win-vista/LayoutTests/svg/custom/use-empty-reference-expected.png
   A http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win-vista/LayoutTests/svg/custom/use-empty-reference-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win-vista/LayoutTests/svg/custom/use-nested-missing-target-removed-expected.txt

Update expectations for WebKit r55511

BUG= 37061
TEST= yes
Review URL: http://codereview.chromium.org/669239
------------------------------------------------------------------------


### ma...@gmail.com (2010-03-06)

Merged r55511, which turns the originally attached svg file from a sad tab into a happy 
tab. (Verified on a local 249.1026 build.)

No new crashes running layout tests.

### sc...@gmail.com (2010-03-09)

@aohelin: congrats! Subject to the usual continued responsible disclosure, we wish to 
offer you a $500 reward. You can e-mail me at cevans@chromium.org to let me know if 
you accept or not.

@mal: is there a dedicated graphic we use for a "happy tab"? :D

### sc...@gmail.com (2010-03-23)

Releasing due to fix in 4.1.249.1036.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/37061?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079507)*

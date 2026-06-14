# Heap-use-after-free in WebCore::SVGUseElement::expandSymbolElementsInShadowTree

| Field | Value |
|-------|-------|
| **Issue ID** | [40053222](https://issues.chromium.org/issues/40053222) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>SVG |
| **Reporter** | ao...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2012-02-02 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

ASan reports a heap use after free when the attached SVG is opened.

**VERSION**  

Chrome Version: Chromium 18.0.1027.0 (Developer Build 0[sic])  

Operating System: Linux (Debian 6.0.4, x86\_64)

**REPRODUCTION CASE**  

$ chrome-asan tree.svg

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

==8052== ERROR: AddressSanitizer heap-use-after-free on address 0x7f9af76830a4 at pc 0x7f9b0831de84 bp 0x7fffbca1dc30 sp 0x7fffbca1dc28  

READ of size 4 at 0x7f9af76830a4 thread T0  

#0 0x7f9b0831de84 in WebCore::SVGUseElement::expandSymbolElementsInShadowTree(WebCore::Node\*) ???:0  

#1 0x7f9b0831dffe in WebCore::SVGUseElement::expandSymbolElementsInShadowTree(WebCore::Node\*) ???:0  

#2 0x7f9b0831b5d8 in WebCore::SVGUseElement::buildShadowAndInstanceTree(WebCore::SVGShadowTreeRootElement\*) ???:0  

#3 0x7f9b08390b9f in WebCore::RenderSVGShadowTreeRootContainer::updateFromElement() ???:0  

#4 0x7f9b0831e55e in WebCore::SVGUseElement::attach() ???:0  

#5 0x7f9b06366a69 in WebCore::ContainerNode::attach() ???:0  

#6 0x7f9b063e3166 in WebCore::Element::attach() ???:0  

#7 0x7f9b082cb45e in WebCore::SVGStyledElement::attach() ???:0  

#8 0x7f9b06366a69 in WebCore::ContainerNode::attach() ???:0  

#9 0x7f9b063e3166 in WebCore::Element::attach() ???:0  

#10 0x7f9b06366a69 in WebCore::ContainerNode::attach() ???:0  

#11 0x7f9b063e3166 in WebCore::Element::attach() ???:0  

#12 0x7f9b0635fb81 in WebCore::ContainerNode::appendChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), int&, bool) ???:0  

#13 0x7f9b07268907 in WebCore::XMLErrors::insertErrorMessageBlock() ???:0  

#14 0x7f9b07251786 in WebCore::XMLDocumentParser::end() ???:0  

#15 0x7f9b06ff1024 in WebCore::DocumentWriter::endIfNotLoadingMainResource() ???:0  

#16 0x7f9b07027c29 in WebCore::FrameLoader::finishedLoading() ???:0  

#17 0x7f9b0704e3f1 in WebCore::MainResourceLoader::didFinishLoading(double) ???:0  

#18 0x7f9b086ff1c2 in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) ???:0  

#19 0x7f9b05d0e80a in ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) ???:0  

#20 0x7f9b05d0f9fb in bool ResourceMsg\_RequestComplete::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)>(IPC::Message const\*, ResourceDispatcher\*, ResourceDispatcher\*, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)) ???:0  

#21 0x7f9b05d0bfcc in ResourceDispatcher::DispatchMessage(IPC::Message const&) ???:0  

#22 0x7f9b05d09f50 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) ???:0  

#23 0x7f9b05c1589f in ChildThread::OnMessageReceived(IPC::Message const&) ???:0  

#24 0x7f9b05d61429 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ???:0  

#25 0x7f9b045e7e66 in MessageLoop::RunTask(base::PendingTask const&) ???:0  

#26 0x7f9b045e86c6 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0  

#27 0x7f9b045e99ab in MessageLoop::DoWork() ???:0  

#28 0x7f9b045f43e7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ???:0  

#29 0x7f9b045e6a2e in MessageLoop::RunInternal() ???:0  

#30 0x7f9b045e4c1f in MessageLoop::Run() ???:0  

#31 0x7f9b0927f6ea in RendererMain(content::MainFunctionParams const&) ???:0  

#32 0x7f9b045444e8 in (anonymous namespace)::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main.cc:0  

#33 0x7f9b045439b4 in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) ???:0  

#34 0x7f9b02d705e7 in ChromeMain ??:0  

#35 0x7f9b02d704eb in main ???:0  

#36 0x7f9afc259c8d in \_\_libc\_start\_main /tmp/buildd/eglibc-2.11.3/csu/libc-start.c:260  

0x7f9af76830a4 is located 36 bytes inside of 448-byte region [0x7f9af7683080,0x7f9af7683240)  

freed by thread T0 here:  

#0 0x7f9b0a3f4362 in operator delete(void\*) ??:0  

#1 0x7f9b0831df63 in WebCore::SVGUseElement::expandSymbolElementsInShadowTree(WebCore::Node\*) ???:0  

#2 0x7f9b0831dffe in WebCore::SVGUseElement::expandSymbolElementsInShadowTree(WebCore::Node\*) ???:0  

#3 0x7f9b0831b5d8 in WebCore::SVGUseElement::buildShadowAndInstanceTree(WebCore::SVGShadowTreeRootElement\*) ???:0  

#4 0x7f9b08390b9f in WebCore::RenderSVGShadowTreeRootContainer::updateFromElement() ???:0  

#5 0x7f9b0831e55e in WebCore::SVGUseElement::attach() ???:0  

#6 0x7f9b06366a69 in WebCore::ContainerNode::attach() ???:0  

#7 0x7f9b063e3166 in WebCore::Element::attach() ???:0  

#8 0x7f9b082cb45e in WebCore::SVGStyledElement::attach() ???:0  

#9 0x7f9b06366a69 in WebCore::ContainerNode::attach() ???:0  

#10 0x7f9b063e3166 in WebCore::Element::attach() ???:0  

#11 0x7f9b06366a69 in WebCore::ContainerNode::attach() ???:0  

#12 0x7f9b063e3166 in WebCore::Element::attach() ???:0  

#13 0x7f9b0635fb81 in WebCore::ContainerNode::appendChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), int&, bool) ???:0  

#14 0x7f9b07268907 in WebCore::XMLErrors::insertErrorMessageBlock() ???:0  

#15 0x7f9b07251786 in WebCore::XMLDocumentParser::end() ???:0  

#16 0x7f9b06ff1024 in WebCore::DocumentWriter::endIfNotLoadingMainResource() ???:0  

#17 0x7f9b07027c29 in WebCore::FrameLoader::finishedLoading() ???:0  

#18 0x7f9b0704e3f1 in WebCore::MainResourceLoader::didFinishLoading(double) ???:0  

#19 0x7f9b086ff1c2 in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) ???:0  

#20 0x7f9b05d0e80a in ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) ???:0  

#21 0x7f9b05d0f9fb in bool ResourceMsg\_RequestComplete::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)>(IPC::Message const\*, ResourceDispatcher\*, ResourceDispatcher\*, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)) ???:0  

#22 0x7f9b05d0bfcc in ResourceDispatcher::DispatchMessage(IPC::Message const&) ???:0  

#23 0x7f9b05d09f50 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) ???:0  

#24 0x7f9b05c1589f in ChildThread::OnMessageReceived(IPC::Message const&) ???:0  

#25 0x7f9b05d61429 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ???:0  

#26 0x7f9b045e7e66 in MessageLoop::RunTask(base::PendingTask const&) ???:0  

#27 0x7f9b045e86c6 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0  

#28 0x7f9b045e99ab in MessageLoop::DoWork() ???:0  

#29 0x7f9b045f43e7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ???:0  

previously allocated by thread T0 here:  

#0 0x7f9b0a3f41e2 in operator new(unsigned long) ??:0  

#1 0x7f9b082a17ce in WebCore::SVGSVGElement::create(WebCore::QualifiedName const&, WebCore::Document\*) ???:0  

#2 0x7f9b0831d8c8 in WebCore::SVGUseElement::expandSymbolElementsInShadowTree(WebCore::Node\*) ???:0  

#3 0x7f9b0831dffe in WebCore::SVGUseElement::expandSymbolElementsInShadowTree(WebCore::Node\*) ???:0  

#4 0x7f9b0831b5d8 in WebCore::SVGUseElement::buildShadowAndInstanceTree(WebCore::SVGShadowTreeRootElement\*) ???:0  

#5 0x7f9b08390b9f in WebCore::RenderSVGShadowTreeRootContainer::updateFromElement() ???:0  

#6 0x7f9b0831e55e in WebCore::SVGUseElement::attach() ???:0  

#7 0x7f9b06366a69 in WebCore::ContainerNode::attach() ???:0  

#8 0x7f9b063e3166 in WebCore::Element::attach() ???:0  

#9 0x7f9b082cb45e in WebCore::SVGStyledElement::attach() ???:0  

#10 0x7f9b06366a69 in WebCore::ContainerNode::attach() ???:0  

#11 0x7f9b063e3166 in WebCore::Element::attach() ???:0  

#12 0x7f9b06366a69 in WebCore::ContainerNode::attach() ???:0  

#13 0x7f9b063e3166 in WebCore::Element::attach() ???:0  

#14 0x7f9b0635fb81 in WebCore::ContainerNode::appendChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), int&, bool) ???:0  

#15 0x7f9b07268907 in WebCore::XMLErrors::insertErrorMessageBlock() ???:0  

#16 0x7f9b07251786 in WebCore::XMLDocumentParser::end() ???:0  

#17 0x7f9b06ff1024 in WebCore::DocumentWriter::endIfNotLoadingMainResource() ???:0  

#18 0x7f9b07027c29 in WebCore::FrameLoader::finishedLoading() ???:0  

#19 0x7f9b0704e3f1 in WebCore::MainResourceLoader::didFinishLoading(double) ???:0  

#20 0x7f9b086ff1c2 in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) ???:0  

#21 0x7f9b05d0e80a in ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) ???:0  

#22 0x7f9b05d0f9fb in bool ResourceMsg\_RequestComplete::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)>(IPC::Message const\*, ResourceDispatcher\*, ResourceDispatcher\*, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)) ???:0  

==8052== ABORTING  

Stats: 2M malloced (4M for red zones) by 15467 calls  

Stats: 0M realloced by 44 calls  

Stats: 1M freed by 7063 calls  

Stats: 0M really freed by 0 calls  

Stats: 40M (10246 full pages) mmaped in 10 calls  

mmaps by size class: 8:16383; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32;  

mallocs by size class: 8:13064; 9:1121; 10:891; 11:244; 12:52; 13:31; 14:49; 15:5; 16:9; 17:1;  

frees by size class: 8:5333; 9:739; 10:762; 11:136; 12:27; 13:19; 14:41; 15:3; 16:3;  

rfrees by size class:  

Stats: malloc large: 1 small slow: 70  

Shadow byte and word:  

0x1ff35eed0614: fd  

0x1ff35eed0610: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1ff35eed05f0: fa fa fa fa fa fa fa fa  

0x1ff35eed05f8: fa fa fa fa fa fa fa fa  

0x1ff35eed0600: fa fa fa fa fa fa fa fa  

0x1ff35eed0608: fa fa fa fa fa fa fa fa  

=>0x1ff35eed0610: fd fd fd fd fd fd fd fd  

0x1ff35eed0618: fd fd fd fd fd fd fd fd  

0x1ff35eed0620: fd fd fd fd fd fd fd fd  

0x1ff35eed0628: fd fd fd fd fd fd fd fd  

0x1ff35eed0630: fd fd fd fd fd fd fd fd

## Attachments

- [tree.svg](attachments/tree.svg) (text/plain; charset=us-ascii, 135 B)

## Timeline

### sk...@chromium.org (2012-02-02)

https://cluster-fuzz.appspot.com/testcase?key=17706360

### sk...@chromium.org (2012-02-02)

Crash type	Heap-use-after-free READ 4
Crash address	0x7f1116c488a4
Crash state	- crash stack -
WebCore::SVGUseElement::expandSymbolElementsInShadowTree
WebCore::SVGUseElement::expandSymbolElementsInShadowTree
- free stack -
WebCore::SVGUseElement::expandSymbolElementsInShadowTree
WebCore::SVGUseElement::expandSymbolElementsInShadowTree


### sk...@chromium.org (2012-02-02)

Upstream: https://bugs.webkit.org/show_bug.cgi?id=77639

### in...@chromium.org (2012-02-02)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=17706360

Uploader: skylined@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7f25e9846ca4
Crash State:
  - crash stack -
  WebCore::SVGUseElement::expandSymbolElementsInShadowTree
  WebCore::SVGUseElement::expandSymbolElementsInShadowTree
  - free stack -
  WebCore::SVGUseElement::expandSymbolElementsInShadowTree
  WebCore::SVGUseElement::expandSymbolElementsInShadowTree
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=116390:116434

Minimized Testcase (0.13 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv962bCUE6LrtYS5ipMyKGwx8MzPgFEAcsaKfsmBJkLuGbRLAiOQWBj_XHoG8YX6B_k3kngHS6WPwg2lu_LWqnU5OwYocMtcnjABUjNWWEMgv1fCdNidAO9InzBmpeAYNrT6oiDe7Iw_239QDK0OSAP5L-teXow
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<use xlink:href="#foo"/>
<symbol id="foo">
<style>

### in...@chromium.org (2012-02-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-02)

We should always wait for regression range before upstreaming. also, we should always try to find regresse and assign/cc him/her from the short regression range. we want the bugs to move forward quickly.

https://trac.webkit.org/log/?verbose=on&stop_rev=104046&rev=104074&limit=1000, seems to coming from https://trac.webkit.org/changeset/104060/.

### sc...@chromium.org (2012-02-02)

I'll look at it this afternoon.

### sc...@chromium.org (2012-02-03)

The bug is due to the error processing code (it is an error to have missing closing tags for SVG elements). The code that adds an error message tries to re-parent the root SVG document into an HTML document, and in doing so causes the layout to happen for the SVG content before it is ready, or something like that. Removing the error reporting code removes the crash, although that is insufficient as a fix.

### sc...@chromium.org (2012-02-03)

The underlying issue is bad SVG error checking on the use of <style> tags inside <use> elements.

https://bugs.webkit.org/show_bug.cgi?id=77764

### js...@chromium.org (2012-02-04)

Thanks for taking this, but I'm dubious that the error handling is the real problem. I've fixed many similar bugs in SVG, and the root cause was always an object lifetime issue. The error handling is one trigger, the resolution has always been something like adding a RefPtr, implementing a weak pointer idiom, or fixing a bug in element removal.

### sc...@chromium.org (2012-02-05)

Yes, I recognize that the error is probably due to bad management of ref-counted pointers when a particular method is accessed recursively. I'm not yet certain which one, but it has to do with the code protected by an assert in style calculation. I assume that I need to make the code robust to the call stack as currently seen, so that the problem will not arise even if someone screws up calling code in the future. Then I can fix the calling code.


### in...@chromium.org (2012-02-14)

Aki, did yu try to reproduce this on Chrome Stable?

### ao...@gmail.com (2012-02-14)

@inferno: IIRC this didn't crash in official stable. Don't know about ASan.

### sc...@chromium.org (2012-02-15)

Patch up: https://bugs.webkit.org/show_bug.cgi?id=77639

### sc...@gmail.com (2012-02-17)

w00t!
Committed r108084: <http://trac.webkit.org/changeset/108084>

We will take care of the merge.

### sc...@gmail.com (2012-03-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-08)

@aohelin: congrats, a great SVG regression catch.
An obvious $1000

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2012-03-12)

M18: http://trac.webkit.org/changeset/110452

### sc...@gmail.com (2012-03-20)

[Empty comment from Monorail migration]

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

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/112411?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053222)*

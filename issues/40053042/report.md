# Heap-buffer-overflow in WebCore::SVGSVGElement::currentViewBoxRect

| Field | Value |
|-------|-------|
| **Issue ID** | [40053042](https://issues.chromium.org/issues/40053042) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | at...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-01-26 |
| **Bounty** | $1,000.00 |

## Description

Repro-file as attachment.

**VERSION**  

WinDBG analysis: Chrome Version: 18.0.1018.0 canary, Windows 7 x64

Type of crash: tab-crash

Crash State:

WinDBG dump-analysis:

0:000> !load winext\msec.dll  

0:000> !analyze -v

FAULTING\_IP:  

chrome\_5ce50000!WebCore::SVGSVGElement::currentViewBoxRect+21 [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\svg\svgsvgelement.cpp @ 533]  

5e367181 8b4e10 mov ecx,dword ptr [esi+10h]

EXCEPTION\_RECORD: ffffffff -- (.exr 0xffffffffffffffff)  

ExceptionAddress: 5e367181 (chrome\_5ce50000!WebCore::SVGSVGElement::currentViewBoxRect+0x00000021)  

ExceptionCode: c0000005 (Access violation)  

ExceptionFlags: 00000000  

NumberParameters: 2  

Parameter[0]: 00000000  

Parameter[1]: 6e617271  

Attempt to read from address 6e617271

DEFAULT\_BUCKET\_ID: STRING\_DEREFERENCE

PROCESS\_NAME: chrome.exe

EXCEPTION\_PARAMETER1: 00000000

EXCEPTION\_PARAMETER2: 6e617271

READ\_ADDRESS: 6e617271

FOLLOWUP\_IP:  

chrome\_5ce50000!WebCore::SVGSVGElement::currentViewBoxRect+21 [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\svg\svgsvgelement.cpp @ 533]  

5e367181 8b4e10 mov ecx,dword ptr [esi+10h]

MOD\_LIST: <ANALYSIS/>

NTGLOBALFLAG: 400

PRIMARY\_PROBLEM\_CLASS: STRING\_DEREFERENCE

BUGCHECK\_STR: APPLICATION\_FAULT\_STRING\_DEREFERENCE\_INVALID\_POINTER\_READ

STACK\_TEXT:  

002feafc 5e36ca00 002feb14 002feb60 01f67570 chrome\_5ce50000!WebCore::SVGSVGElement::currentViewBoxRect+0x21 [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\svg\svgsvgelement.cpp @ 533]  

002feb20 5e36cb55 002feb34 002feb30 00000000 chrome\_5ce50000!WebCore::SVGLengthContext::determineViewport+0x66 [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\svg\svglengthcontext.cpp @ 291]  

002feb34 5e36ce62 40000000 00000000 002feb60 chrome\_5ce50000!WebCore::SVGLengthContext::convertValueFromPercentageToUserUnits+0x1b [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\svg\svglengthcontext.cpp @ 188]  

002feb44 5e360b48 40000000 00000000 00000002 chrome\_5ce50000!WebCore::SVGLengthContext::convertValueToUserUnits+0x98 [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\svg\svglengthcontext.cpp @ 128]  

002feb60 5e3949f2 002feb88 00000001 01f8219c chrome\_5ce50000!WebCore::SVGLength::value+0x2b [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\svg\svglength.cpp @ 192]  

002feb98 5e3868c3 00000000 00000000 01f8219c chrome\_5ce50000!WebCore::SVGAnimatedLengthAnimator::calculateAnimatedValue+0x145 [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\svg\svganimatedlength.cpp @ 108]  

002febb4 5e371f80 00000000 00000000 01f82030 chrome\_5ce50000!WebCore::SVGAnimateElement::calculateAnimatedValue+0x6c [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\svg\svganimateelement.cpp @ 186]  

002febd4 5e35fd9a 00000000 00000000 01f82030 chrome\_5ce50000!WebCore::SVGAnimationElement::updateAnimation+0x227 [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\svg\svganimationelement.cpp @ 624]  

002fec04 5e36383d 00000000 00000000 01f82030 chrome\_5ce50000!WebCore::SVGSMILElement::progress+0x141 [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\svg\animation\svgsmilelement.cpp @ 968]  

002fec94 5e363a0c 00000000 00000000 00000000 chrome\_5ce50000!WebCore::SMILTimeContainer::updateAnimations+0x28a [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\svg\animation\smiltimecontainer.cpp @ 306]  

002fecbc 5e35abc5 01f58a00 01f58a40 00000000 chrome\_5ce50000!WebCore::SMILTimeContainer::begin+0x39 [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\svg\animation\smiltimecontainer.cpp @ 97]  

002fece0 5d0e204f 01f94d20 01f45f90 5d33b8a8 chrome\_5ce50000!WebCore::SVGDocumentExtensions::startAnimations+0x6d [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\svg\svgdocumentextensions.cpp @ 103]  

002fecec 5d33b8a8 01f70188 01fa0a88 5d33b801 chrome\_5ce50000!WebCore::FrameLoader::checkCompleted+0x90 [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\loader\frameloader.cpp @ 744]  

002fecf8 5d33b801 01fa0728 01fa0a88 5e6b8757 chrome\_5ce50000!WebCore::CachedResourceLoader::loadDone+0x2b [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\loader\cache\cachedresourceloader.cpp @ 659]  

002fed04 5e6b8757 01fa0a88 5e71e6c0 002fed44 chrome\_5ce50000!WebCore::SubresourceLoader::releaseResources+0x46 [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\loader\subresourceloader.cpp @ 318]  

002fed0c 5e71e6c0 002fed44 002fed44 01fa0a88 chrome\_5ce50000!WebCore::ResourceLoader::didFail+0x5b [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\loader\resourceloader.cpp @ 346]  

002fed20 5e6b8673 002fed44 002fee0c 01fa0f60 chrome\_5ce50000!WebCore::SubresourceLoader::didFail+0x6e [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\loader\subresourceloader.cpp @ 296]  

002fed30 5de6bfe3 01fcbe00 002fed44 01f883c8 chrome\_5ce50000!WebCore::ResourceLoader::didFail+0x51 [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webcore\loader\resourceloader.cpp @ 462]  

002fed54 5d2b9497 01fcbe18 002fed78 00f75900 chrome\_5ce50000!WebCore::ResourceHandleInternal::didFail+0x37 [d:\b\build\slave\chrome-unofficial\build\src\third\_party\webkit\source\webkit\chromium\src\resourcehandle.cpp @ 165]  

002fee54 5d2b9156 002feea8 002feeb0 002fee78 chrome\_5ce50000!webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest+0x1a8 [d:\b\build\slave\chrome-unofficial\build\src\webkit\glue\weburlloader\_impl.cc @ 645]  

002fee84 5d2b8f73 00000001 002feea8 002feeb0 chrome\_5ce50000!ResourceDispatcher::OnRequestComplete+0x7f [d:\b\build\slave\chrome-unofficial\build\src\content\common\resource\_dispatcher.cc @ 488]  

002feed4 5d14eb14 01f8876c 00f75900 00f75900 chrome\_5ce50000!ResourceMsg\_RequestComplete::Dispatch<ResourceDispatcher,ResourceDispatcher,void (\_\_thiscall ResourceDispatcher::\*)(int,net::URLRequestStatus const &,std::basic\_string<char,std::char\_traits<char>,std::allocator<char> > const &,base::TimeTicks const &)>+0x68 [d:\b\build\slave\chrome-unofficial\build\src\content\common\resource\_messages.h @ 172]  

002fef68 5cfd3042 01f8876c 01f8876c 00f73984 chrome\_5ce50000!ResourceDispatcher::DispatchMessageW+0x22a [d:\b\build\slave\chrome-unofficial\build\src\content\common\resource\_dispatcher.cc @ 559]  

002ff02c 5cfd2c0a 01f8876c 002ff68c 00000000 chrome\_5ce50000!ResourceDispatcher::OnMessageReceived+0x237 [d:\b\build\slave\chrome-unofficial\build\src\content\common\resource\_dispatcher.cc @ 326]  

002ff084 5ce94717 01f8876c 002ff184 5ce8e654 chrome\_5ce50000!ChildThread::OnMessageReceived+0x21 [d:\b\build\slave\chrome-unofficial\build\src\content\common\child\_thread.cc @ 171]  

002ff090 5ce8e654 01f88758 00000000 00f66940 chrome\_5ce50000!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (\_\_thiscall history::TopSitesBackend::\*)(FilePath const &)>,void \_\_cdecl(history::TopSitesBackend \*,FilePath const &),void \_\_cdecl(history::TopSitesBackend \*,FilePath)>,void \_\_cdecl(history::TopSitesBackend \*,FilePath const &)>::Run+0x16 [d:\b\build\slave\chrome-unofficial\build\src\base\bind\_internal.h @ 1254]  

002ff168 5ce8e30f 002ff184 00f62f78 002ff57c chrome\_5ce50000!MessageLoop::RunTask+0x203 [d:\b\build\slave\chrome-unofficial\build\src\base\message\_loop.cc @ 460]  

002ff1b8 5ce91096 00f662c0 002ff57c 00000000 chrome\_5ce50000!MessageLoop::DoWork+0x22c [d:\b\build\slave\chrome-unofficial\build\src\base\message\_loop.cc @ 661]  

002ff27c 5ce8df14 002ff57c 00f59be8 002ff2a0 chrome\_5ce50000!base::MessagePumpDefault::Run+0x122 [d:\b\build\slave\chrome-unofficial\build\src\base\message\_pump\_default.cc @ 55]  

002ff324 5ce8de64 00000001 5ce74800 00000000 chrome\_5ce50000!MessageLoop::RunInternal+0x9e [d:\b\build\slave\chrome-unofficial\build\src\base\message\_loop.cc @ 417]  

002ff33c 5cfb2c00 00000008 00000008 002ff8c0 chrome\_5ce50000!MessageLoop::Run+0x5b [d:\b\build\slave\chrome-unofficial\build\src\base\message\_loop.cc @ 301]  

002ff6b4 5ce72eeb 002ff7c8 002ff8f4 00f59be8 chrome\_5ce50000!RendererMain+0x38a [d:\b\build\slave\chrome-unofficial\build\src\content\renderer\renderer\_main.cc @ 242]  

002ff768 5ce64f90 002ff8c0 002ff7c8 002ff8f4 chrome\_5ce50000!`anonymous namespace'::RunNamedProcessTypeMain+0xbb [d:\b\build\slave\chrome-unofficial\build\src\content\app\content\_main.cc @ 264]  

002ff8dc 5ce64a9f 012f0000 002ff9a0 002ff8f4 chrome\_5ce50000!content::ContentMain+0x49f [d:\b\build\slave\chrome-unofficial\build\src\content\app\content\_main.cc @ 455]  

002ff90c 012f57ff 012f0000 002ff9a0 fffffffe chrome\_5ce50000!ChromeMain+0x21 [d:\b\build\slave\chrome-unofficial\build\src\chrome\app\chrome\_main.cc @ 28]  

002ff984 012f1074 012f0000 002ff9a0 fffffffe chrome!MainDllLoader::Launch+0x18f [d:\b\build\slave\chrome-unofficial\build\src\chrome\app\client\_util.cc @ 343]  

002ff9e0 0133fecf 012f0000 00000000 00502920 chrome!wWinMain+0x74 [d:\b\build\slave\chrome-unofficial\build\src\chrome\app\chrome\_exe\_main\_win.cc @ 37]  

002ffa70 74da339a 7efde000 002ffabc 77349ef2 chrome!\_\_tmainCRTStartup+0x112 [f:\dd\vctools\crt\_bld\self\_x86\crt\src\crt0.c @ 263]  

002ffa7c 77349ef2 7efde000 77320f6d 00000000 kernel32!BaseThreadInitThunk+0xe  

002ffabc 77349ec5 0133ff3a 7efde000 00000000 ntdll!\_\_RtlUserThreadStart+0x70  

002ffad4 00000000 0133ff3a 7efde000 00000000 ntdll!\_RtlUserThreadStart+0x1b

STACK\_COMMAND: ~0s; .ecxr ; kb

SYMBOL\_STACK\_INDEX: 0

SYMBOL\_NAME: chrome!WebCore::SVGSVGElement::currentViewBoxRect+21

MODULE\_NAME: chrome\_5ce50000

IMAGE\_NAME: chrome.dll

FAILURE\_BUCKET\_ID: STRING\_DEREFERENCE\_c0000005\_chrome.dll!WebCore::SVGSVGElement::currentViewBoxRect

BUCKET\_ID: APPLICATION\_FAULT\_STRING\_DEREFERENCE\_INVALID\_POINTER\_READ\_chrome!WebCore::SVGSVGElement::currentViewBoxRect+21

---

0:000> !exploitable  

Exploitability Classification: UNKNOWN  

Recommended Bug Title: Data from Faulting Address may be used as a return value starting at chrome\_5ce50000!WebCore::SVGSVGElement::currentViewBoxRect+0x0000000000000021 (Hash=0x17101315.0x412d6a73)

The data from the faulting address may later be used as a return value from this function.

ASAN report:

=================================================================  

==3375== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f629360a418 at pc 0x7f62a456ec68 bp 0x7fff494a2510 sp 0x7fff494a2508  

READ of size 1 at 0x7f629360a418 thread T0  

#0 0x7f62a456ec68 (/home/ouspg/chrome/src/out/Release/chrome+0x61c8c68)  

#1 0x7f62a44c8bd6 (/home/ouspg/chrome/src/out/Release/chrome+0x6122bd6)  

#2 0x7f62a44c30c5 (/home/ouspg/chrome/src/out/Release/chrome+0x611d0c5)  

#3 0x7f62a4677143 (/home/ouspg/chrome/src/out/Release/chrome+0x62d1143)  

.  

.  

.  

#34 0x7f629841deff (/lib/x86\_64-linux-gnu/libc.so.6+0x1eeff)  

0x7f629360a418 is located 104 bytes to the left of 200-byte region [0x7f629360a480,0x7f629360a548)  

allocated by thread T0 here:  

#0 0x7f62a65b12b2 (/home/ouspg/chrome/src/out/Release/chrome+0x820b2b2)  

#1 0x7f62a219dd9b (/home/ouspg/chrome/src/out/Release/chrome+0x3df7d9b)  

#2 0x7f62a2eed7fd (/home/ouspg/chrome/src/out/Release/chrome+0x4b477fd)  

.  

.  

.  

#22 0x7f62a2002bb9 (/home/ouspg/chrome/src/out/Release/chrome+0x3c5cbb9)  

==3375== ABORTING  

Stats: 4M malloced (6M for red zones) by 20910 calls  

Stats: 0M realloced by 116 calls  

Stats: 2M freed by 9007 calls  

Stats: 0M really freed by 0 calls  

Stats: 44M (11270 full pages) mmaped in 11 calls  

mmaps by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32;  

mallocs by size class: 8:17924; 9:1359; 10:995; 11:392; 12:93; 13:37; 14:86; 15:8; 16:12; 17:4;  

frees by size class: 8:6872; 9:903; 10:833; 11:244; 12:47; 13:20; 14:78; 15:4; 16:6;  

rfrees by size class:  

Stats: malloc large: 4 small slow: 93  

Shadow byte and word:  

0x1fec526c1483: fa  

0x1fec526c1480: fa fa fa fa fa fa fa fa  

More shadow bytes:  

0x1fec526c1460: 00 00 00 00 00 00 00 00  

0x1fec526c1468: 00 00 00 00 00 fb fb fb  

0x1fec526c1470: fa fa fa fa fa fa fa fa  

0x1fec526c1478: fa fa fa fa fa fa fa fa  

=>0x1fec526c1480: fa fa fa fa fa fa fa fa  

0x1fec526c1488: fa fa fa fa fa fa fa fa  

0x1fec526c1490: 00 00 00 00 00 00 00 00  

0x1fec526c1498: 00 00 00 00 00 00 00 00  

0x1fec526c14a0: 00 00 00 00 00 00 00 00

## Attachments

- [heap-buffer-overflow-1327569970.svg](attachments/heap-buffer-overflow-1327569970.svg) (text/plain; charset=us-ascii, 579 B)

## Timeline

### in...@chromium.org (2012-01-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=15780941

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7f6624082e18
Crash State:
  - crash stack -
  WebCore::SVGSVGElement::currentViewBoxRect
  WebCore::SVGLengthContext::convertValueToUserUnits
  WebCore::SVGLength::value
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=118466:118516

Minimized Testcase (0.25 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95UpAyT_Sy6SS2kLgQu6koRKdPN-MoF_J1QNAa2lqlUmPnRUnfowXz_CKaUDdrt3LvElbVwVqt-gqRw03mvH7Z09u4FDeaMLInvTU-T_rksTUbJ8SyXadN-3C2J89Z8UKc-Pydq5lUH0nSM8pA1f9t87EqXAA
<svg xmlns="http://www.w3.org/2000/svg" 
     xmlns:xlink="http://www.w3.org/1999/xlink"
    >
  
  <script xlink:href="smil-util.js" type="text/javascript"/>

  <symbol>
      <symbol>
      <rect>
    <animate attributeName="width"
     to="0%"
    >
  </use>

### in...@chromium.org (2012-01-26)

filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=77121. it is a bad cast

### at...@gmail.com (2012-01-26)

Is there some way for me to follow the progress of the bug filed for the webkit?

### in...@chromium.org (2012-01-26)

Fixed in http://trac.webkit.org/changeset/106036

### sc...@gmail.com (2012-01-27)

How's that for progress? :)
Adding reward-topanel

### at...@gmail.com (2012-01-27)

That is great progress. :) Again I'm impressed with the speed. :)

### sc...@gmail.com (2012-02-05)

Nice regression catch and good report. We like catching things nice and early before they go to Beta or Stable :D
$1000

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

### sc...@gmail.com (2012-03-27)

[Empty comment from Monorail migration]

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

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-06-13)

ClusterFuzz has detected this issue as fixed in range 119408:119410.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=15780941

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7f6624082e18
Crash State:
  - crash stack -
  WebCore::SVGSVGElement::currentViewBoxRect
  WebCore::SVGLengthContext::convertValueToUserUnits
  WebCore::SVGLength::value
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=119408:119410

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95UpAyT_Sy6SS2kLgQu6koRKdPN-MoF_J1QNAa2lqlUmPnRUnfowXz_CKaUDdrt3LvElbVwVqt-gqRw03mvH7Z09u4FDeaMLInvTU-T_rksTUbJ8SyXadN-3C2J89Z8UKc-Pydq5lUH0nSM8pA1f9t87EqXAA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/111467?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053042)*

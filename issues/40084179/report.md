# chrome_55000000!WebCore::FEBlend::apply+0x1a5

| Field | Value |
|-------|-------|
| **Issue ID** | [40084179](https://issues.chromium.org/issues/40084179) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | wo...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2010-10-26 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

eax=fc5f9e66 ebx=007308a0 ecx=00733b10 edx=00000000 esi=0070fc70 edi=00000000  

eip=55b85f1b esp=0030e990 ebp=0030e9fc iopl=0 nv up ei pl nz na pe nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010206  

chrome\_55000000!WebCore::FEBlend::apply+0x1a5:  

55b85f1b ff1485fcec0d56 call dword ptr chrome\_55000000!callEffect (560decfc)[eax\*4] ds:0023:478c6694=????????  

2:024> u  

chrome\_55000000!WebCore::FEBlend::apply+0x1a5 [d:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\platform\graphics\filters\feblend.cpp @ 134]:  

55b85f1b ff1485fcec0d56 call dword ptr chrome\_55000000!callEffect (560decfc)[eax\*4]  

55b85f22 8b4c2428 mov ecx,dword ptr [esp+28h]  

55b85f26 8b490c mov ecx,dword ptr [ecx+0Ch]  

55b85f29 8b542420 mov edx,dword ptr [esp+20h]  

55b85f2d 8b4904 mov ecx,dword ptr [ecx+4]  

55b85f30 8d343a lea esi,[edx+edi]  

55b85f33 83c410 add esp,10h  

55b85f36 3b7104 cmp esi,dword ptr [ecx+4]  

2:024> kv  

ChildEBP RetAddr Args to Child  

0030e9fc 559fdcde 0072a980 006c35b0 007309c0 chrome\_55000000!WebCore::FEBlend::apply+0x1a5 (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\platform\graphics\filters\feblend.cpp @ 134]  

0030ea54 559f6b63 006c35b0 0030eac8 00000001 chrome\_55000000!WebCore::RenderSVGResourceFilter::postApplyResource+0xed (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\rendering\rendersvgresourcefilter.cpp @ 266]  

0030ea78 559f838b 0030eac8 0030f148 0030eb40 chrome\_55000000!WebCore::SVGRenderSupport::finishRenderSVGContent+0x3b (CONV: cdecl) [d:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\rendering\svgrendersupport.cpp @ 152]  

0030eaf4 5556448a 0030eb18 00000000 00000000 chrome\_55000000!WebCore::RenderSVGContainer::paint+0x12f (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\rendering\rendersvgcontainer.cpp @ 123]  

0030eb44 559f0696 0030eb78 00000000 00000000 chrome\_55000000!WebCore::RenderBox::paint+0x5e (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\rendering\renderbox.cpp @ 584]  

0030ebf4 554f50c5 0030ec58 00000000 00000000 chrome\_55000000!WebCore::RenderSVGRoot::paint+0x152 (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\rendering\rendersvgroot.cpp @ 192]  

0030eda4 554f52de 006c31ec 0030f148 0030f048 chrome\_55000000!WebCore::RenderLayer::paintLayer+0x569 (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\rendering\renderlayer.cpp @ 2463]  

0030edd0 554f51cb 006c31ec 006c31ec 0030f148 chrome\_55000000!WebCore::RenderLayer::paintList+0x38 (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\rendering\renderlayer.cpp @ 2515]  

0030ef94 554f49c3 006c31ec 0030f148 0030f048 chrome\_55000000!WebCore::RenderLayer::paintLayer+0x66f (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\rendering\renderlayer.cpp @ 2484]  

0030efe0 554fd6e8 0030f148 0030f048 00000000 chrome\_55000000!WebCore::RenderLayer::paint+0x3a (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\rendering\renderlayer.cpp @ 2268]  

0030f010 554b3af5 0030f148 0030f048 0030f148 chrome\_55000000!WebCore::FrameView::paintContents+0x105 (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\page\frameview.cpp @ 2004]  

0030f078 556b23db 0030f148 0030f0a8 0030f0e8 chrome\_55000000!WebCore::ScrollView::paint+0x131 (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\platform\scrollview.cpp @ 818]  

0030f0c8 556b2458 006b9480 0030f148 00000000 chrome\_55000000!WebKit::WebFrameImpl::paintWithContext+0x77 (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third\_party\webkit\webkit\chromium\src\webframeimpl.cpp @ 1829]  

0030f154 556aca30 006b9480 006810e0 0030f210 chrome\_55000000!WebKit::WebFrameImpl::paint+0x3c (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third\_party\webkit\webkit\chromium\src\webframeimpl.cpp @ 1851]  

0030f1b8 55126419 006810e0 0030f210 00000000 chrome\_55000000!WebKit::WebViewImpl::paint+0x32 (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third\_party\webkit\webkit\chromium\src\webviewimpl.cpp @ 957]  

0030f224 55126797 006f4000 007336c0 00000000 chrome\_55000000!RenderWidget::PaintRect+0xb7 (CONV: thiscall) [d:\b\slave\chrome-official\build\src\chrome\renderer\render\_widget.cc @ 422]  

0030f348 55126527 006f4000 0071a834 5512850d chrome\_55000000!RenderWidget::DoDeferredUpdate+0x255 (CONV: thiscall) [d:\b\slave\chrome-official\build\src\chrome\renderer\render\_widget.cc @ 531]  

0030f354 5512850d 0030f394 0030f5dc 5512651e chrome\_55000000!RenderWidget::CallDoDeferredUpdate+0x9 (FPO: [0,0,1]) (CONV: thiscall) [d:\b\slave\chrome-official\build\src\chrome\renderer\render\_widget.cc @ 458]  

0030f370 550c2a8c 0030f3e0 0071a818 0030f4e8 chrome\_55000000!RunnableMethod<RenderWidget,void (\_\_thiscall RenderWidget::\*)(void),Tuple0>::Run+0x2b (CONV: thiscall) [d:\b\slave\chrome-official\build\src\base\task.h @ 327]  

0030f3a0 550c2b18 0030f4e8 0071a820 0030f4e8 chrome\_55000000!MessageLoop::RunTask+0x97 (CONV: thiscall) [d:\b\slave\chrome-official\build\src\base\message\_loop.cc @ 409]  

**VERSION**  

Chrome Version: 7.0.517.41 + stable  

Operating System: windows 7  

**REPRODUCTION CASE**  

open the attached file using chrome.  

Type of crash: tab

## Attachments

- [test0.xhtml](attachments/test0.xhtml) (text/plain; charset=us-ascii, 742 B)

## Timeline

### js...@chromium.org (2010-10-26)

Thanks for the detailed report wooshi. The SVG use element and animation are a bit of an unholy nexus. I'll look at it later today.

### js...@chromium.org (2010-10-26)

Okay, this is an awesome bug. The FEBlend::apply() method has a static array of function pointers for the different filter operations, and the current operation index is stored in FEBlend::m_mode. So, you can set the mode to any value via JavaScript and (barring ASLR) call any address you want when painting occurs. Fortunately, it should be a really easy fix. 

I'll reduce the repro and report upstream.

### sc...@gmail.com (2010-10-26)

Whoa. I did think the faulting instruction of call [eax*4] was a little weird :)

### js...@chromium.org (2010-10-27)

Patched upstream: http://trac.webkit.org/changeset/70652

I'll merge this today so we can make the next stable refresh.


### js...@chromium.org (2010-10-27)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-10-28)

Merged to 517 as r70727 and 552 as r70729.

### sc...@gmail.com (2010-10-28)

@wooshi: congratulations! This bug provisionally qualifies for a $1000 Chromium Security Reward.
The reward was increased beyond the base amount because it's a great quality report:
- Simplified and reliable repro file.
- Excellent stack trace (with symbols, cool!) and good register capture.
Thank you.

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

### js...@chromium.org (2010-11-04)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-11-12)

Payment is in electronic system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

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

This issue was migrated from crbug.com/chromium/60688?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084179)*

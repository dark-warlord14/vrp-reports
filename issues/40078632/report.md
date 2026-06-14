# Security: use-after-free in content::WebContentsImpl::~WebContentsImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40078632](https://issues.chromium.org/issues/40078632) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2014-01-06 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. Please use a different**  

**template for other types of bug reports.**

**Please see the following link for instructions on filing security bugs:**  

**<http://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**VULNERABILITY DETAILS**

**VERSION**  

Chrome Version: [stable 31.0.1650.63 m]  

Operating System: [Window 7]

**REPRODUCTION CASE**  

Actually is not easy to repro this crash cause can take several tries to repro, so you should click on page many clicks and faster as much as possible (you can see the screenshot).

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]  

Client ID (if relevant): 2d7d33b5cdde3482, 82e09d0806a93a6d  

Crash State:

eax=f5105786 ebx=00000000 ecx=0ae00650 edx=00011d3f esi=0b436000 edi=00000001  

eip=60fd6eb4 esp=0026ed50 ebp=0026ed78 iopl=0 nv up ei pl nz na pe nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00210206  

chrome\_60c90000!content::WebContentsImpl::~WebContentsImpl+0x1bd:  

60fd6eb4 ff10 call dword ptr [eax] ds:0023:f5105786=????????  

0:000> k  

ChildEBP RetAddr  

0026ed78 60fd6ce3 chrome\_60c90000!content::WebContentsImpl::~WebContentsImpl+0x1bd [c:\b\build\slave\win\build\src\content\browser\web\_contents\web\_contents\_impl.cc @ 422]  

0026ed84 60fd678f chrome\_60c90000!content::WebContentsImpl::`scalar deleting destructor'+0xb  

0026eda8 60fd65db chrome\_60c90000!TabStripModel::InternalCloseTab+0x63 [c:\b\build\slave\win\build\src\chrome\browser\ui\tabs\tab\_strip\_model.cc @ 1160]  

0026edfc 6184a83a chrome\_60c90000!TabStripModel::InternalCloseTabs+0x139 [c:\b\build\slave\win\build\src\chrome\browser\ui\tabs\tab\_strip\_model.cc @ 1144]  

0026ee28 6184998a chrome\_60c90000!TabStripModel::CloseWebContentsAt+0x32 [c:\b\build\slave\win\build\src\chrome\browser\ui\tabs\tab\_strip\_model.cc @ 427]  

0026ee40 618486e5 chrome\_60c90000!chrome::CloseWebContents+0x37 [c:\b\build\slave\win\build\src\chrome\browser\ui\browser\_tabstrip.cc @ 82]  

0026ee58 61958f3e chrome\_60c90000!Browser::CloseContents+0x3c [c:\b\build\slave\win\build\src\chrome\browser\ui\browser.cc @ 1386]  

0026ee6c 61954645 chrome\_60c90000!content::WebContentsImpl::Close+0x25 [c:\b\build\slave\win\build\src\content\browser\web\_contents\web\_contents\_impl.cc @ 3242]  

0026ee78 60f2d70d chrome\_60c90000!content::RenderViewHostImpl::ClosePageIgnoringUnloadEvents+0x27 [c:\b\build\slave\win\build\src\content\browser\renderer\_host\render\_view\_host\_impl.cc @ 554]  

0026f22c 60f2d578 chrome\_60c90000!content::RenderViewHostImpl::OnMessageReceived+0x18a [c:\b\build\slave\win\build\src\content\browser\renderer\_host\render\_view\_host\_impl.cc @ 949]  

0026f354 60f2d2c5 chrome\_60c90000!content::RenderProcessHostImpl::OnMessageReceived+0x29f [c:\b\build\slave\win\build\src\content\browser\renderer\_host\render\_process\_host\_impl.cc @ 1282]  

0026f384 60d49fba chrome\_60c90000!IPC::ChannelProxy::Context::OnDispatchMessage+0x93 [c:\b\build\slave\win\build\src\ipc\ipc\_channel\_proxy.cc @ 270]  

0026f394 60ce13e9 chrome\_60c90000!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (\_\_thiscall predictors::LoggedInPredictorTable::\*)(GURL const &)>,void \_\_cdecl(predictors::LoggedInPredictorTable \*,GURL const &),void \_\_cdecl(scoped\_refptr[predictors::LoggedInPredictorTable](javascript:void(0);),GURL)>,void \_\_cdecl(predictors::LoggedInPredictorTable \*,GURL const &)>::Run+0x16 [c:\b\build\slave\win\build\src\base\bind\_internal.h @ 1253]  

0026f408 60ce0dd9 chrome\_60c90000!base::MessageLoop::RunTask+0x223 [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 493]  

0026f558 60d5d1cd chrome\_60c90000!base::MessageLoop::DoWork+0x301 [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 618]  

0026f588 60ce08cc chrome\_60c90000!base::MessagePumpForUI::DoRunLoop+0x5c [c:\b\build\slave\win\build\src\base\message\_loop\message\_pump\_win.cc @ 243]  

0026f5a8 60ce0837 chrome\_60c90000!base::MessageLoop::RunInternal+0x5f [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 436]  

0026f5b8 60f149b5 chrome\_60c90000!base::RunLoop::Run+0x59 [c:\b\build\slave\win\build\src\base\run\_loop.cc @ 48]  

0026f630 60f1489e chrome\_60c90000!ChromeBrowserMainParts::MainMessageLoopRun+0xfa [c:\b\build\slave\win\build\src\chrome\browser\chrome\_browser\_main.cc @ 1588]  

0026f644 60f14868 chrome\_60c90000!content::BrowserMainLoop::RunMainMessageLoopParts+0x2d [c:\b\build\slave\win\build\src\content\browser\browser\_main\_loop.cc @ 695]

## Attachments

- [screenshot.png](attachments/screenshot.png) (image/png, 699.5 KB)
- [how to repro.avi](attachments/how to repro.avi) (application/octet-stream, 3.4 MB)
- [repro.html](attachments/repro.html) (text/html, 967 B)
- [Chrome-last.dmp](attachments/Chrome-last.dmp) (application/octet-stream, 443.1 KB)

## Timeline

### ch...@gmail.com (2014-01-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-07)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=6264081749114880

### ia...@chromium.org (2014-01-07)

I can't repro this on OS X, cc'ing people from past similar bugs.

### jl...@chromium.org (2014-01-07)

I'm unable to reproduce so far.

It looks like it would be a use-after-free of the color chooser, triggered by the following snippets in the WebContentsImpl() destructor:

  if (color_chooser_)
    color_chooser_->End();

The vtable pointer looks like garbage.

Ownership of the ColorChooser object seems unclear by quickly glancing at 
ColorChooserWin::OnColorChooserDialogClosed()

Keishi, can you please take a look ?

Tentatively marking a "High" security impact.



### cl...@chromium.org (2014-01-07)

[Empty comment from Monorail migration]

### ke...@chromium.org (2014-01-08)

I couldn't reproduce the issue, but I put a CL up for review to fix the probable cause.
https://codereview.chromium.org/128053002/

### cl...@chromium.org (2014-01-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-01-14)

------------------------------------------------------------------------
r244710 | keishi@chromium.org | 2014-01-14T14:56:30.122384Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/public/browser/web_contents_delegate.h?r1=244710&r2=244709&pathrev=244710
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/web_contents/web_contents_impl.cc?r1=244710&r2=244709&pathrev=244710
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/views/color_chooser_win.cc?r1=244710&r2=244709&pathrev=244710

Make WebContentsDelegate::OpenColorChooser return NULL on failure

Changing WebContentsDelegate::OpenColorChooser to return NULL on failure so we don't put the same ColorChooser into two scoped_ptrs(WebContentsImpl::color_chooser_)

BUG=331790

Review URL: https://codereview.chromium.org/128053002
------------------------------------------------------------------------

### in...@chromium.org (2014-01-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-01-14)

Is there a merge required here?

### ka...@google.com (2014-01-14)

ping? do we want to merge this? adding just in case.

### cl...@chromium.org (2014-01-14)

[Empty comment from Monorail migration]

### ke...@chromium.org (2014-01-15)

Fix confirmed. Requesting permission to merge to M33 and M32.

### la...@google.com (2014-01-15)

[Empty comment from Monorail migration]

### ch...@gmail.com (2014-01-15)

Is this report qualified for a reward ?

### ka...@google.com (2014-01-15)

please don't merge to m32 yet. laforge approved just for m33. once it's there merge-request for m32 again

### ke...@chromium.org (2014-01-15)

chromium.khalil: It show go to the panel to decide, certainly. It looks like this is very difficult to reproduce but a browser process use-after-free is serious business.

### bu...@chromium.org (2014-01-16)

------------------------------------------------------------------------
r245061 | keishi@chromium.org | 2014-01-16T02:06:44.799688Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/content/public/browser/web_contents_delegate.h?r1=245061&r2=245060&pathrev=245061
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/content/browser/web_contents/web_contents_impl.cc?r1=245061&r2=245060&pathrev=245061
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/chrome/browser/ui/views/color_chooser_win.cc?r1=245061&r2=245060&pathrev=245061

Merge 244710 "Make WebContentsDelegate::OpenColorChooser return ..."

> Make WebContentsDelegate::OpenColorChooser return NULL on failure
> 
> Changing WebContentsDelegate::OpenColorChooser to return NULL on failure so we don't put the same ColorChooser into two scoped_ptrs(WebContentsImpl::color_chooser_)
> 
> BUG=331790
> 
> Review URL: https://codereview.chromium.org/128053002

TBR=keishi@chromium.org

Review URL: https://codereview.chromium.org/131333005
------------------------------------------------------------------------

### ke...@chromium.org (2014-01-16)

Merged to M33.

### dh...@google.com (2014-01-16)

[Empty comment from Monorail migration]

### ka...@google.com (2014-01-17)

this hasn't gone out in m33 yet, i think this needs more baking.

### ka...@google.com (2014-02-05)

there will be no more 32s, please make sure to request merge to M33 instead

### in...@chromium.org (2014-02-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-02-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-02-19)

[Empty comment from Monorail migration]

### dh...@google.com (2014-02-19)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-03-04)

Thanks for the report! This one qualifies for a $1000 reward. It did not qualify at a higher reward level because of the amount of user interaction required to trigger the use after free.

### ti...@chromium.org (2014-04-15)

Starting payment process.

### cl...@chromium.org (2014-04-22)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-06-17)

Processing via our e-payment system can take up to 6-8 weeks, but the reward should be on its way to you. Thanks again for your help!


### ch...@gmail.com (2014-06-24)

[Comment Deleted]

### cl...@chromium.org (2016-02-02)

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

This issue was migrated from crbug.com/chromium/331790?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/343629]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078632)*

# use-after-free in SpeechRecognitionBubbleView::GetAnchorRect

| Field | Value |
|-------|-------|
| **Issue ID** | [40078600](https://issues.chromium.org/issues/40078600) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Speech |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2013-12-25 |
| **Bounty** | $500.00 |

## Description

**This template is ONLY for reporting security bugs. Please use a different**  

**template for other types of bug reports.**

**Please see the following link for instructions on filing security bugs:**  

**<http://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

Chrome Version: 34.0.1760.0 canary  

Operating System: Window 7

**REPRODUCTION CASE**

Just keep clicking somewhere on the page until the crash.(it can take several tries to repro the crash)

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: Browser  

Crash State:

eax=f7abcc0e ebx=078d8e00 ecx=07847700 edx=002ff4b0 esi=078d8e00 edi=00000003  

eip=61333361 esp=002ff488 ebp=002ff4b4 iopl=0 nv up ei pl zr na pe nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010246  

chrome\_604e0000!`anonymous namespace'::SpeechRecognitionBubbleView::GetAnchorRect+0x23:  

61333361 ff5054 call dword ptr [eax+54h] ds:0023:f7abcc62=????????

002ff4b4 61725339 chrome\_604e0000!`anonymous namespace'::SpeechRecognitionBubbleView::GetAnchorRect+0x23 [c:\b\build\slave\win\build\src\chrome\browser\ui\views\speech_recognition_bubble_views.cc @ 125] 002ff4e8 617252ce chrome_604e0000!views::BubbleDelegateView::GetBubbleBounds+0x30 [c:\b\build\slave\win\build\src\ui\views\bubble\bubble_delegate.cc @ 325] 002ff508 6133303f chrome_604e0000!views::BubbleDelegateView::SizeToContents+0x17 [c:\b\build\slave\win\build\src\ui\views\bubble\bubble_delegate.cc @ 312] 002ff520 613331db chrome_604e0000!`anonymous namespace'::SpeechRecognitionBubbleView::UpdateLayout+0x126 [c:\b\build\slave\win\build\src\chrome\browser\ui\views\speech\_recognition\_bubble\_views.cc @ 206]  

002ff540 60c24f40 chrome\_604e0000!`anonymous namespace'::SpeechRecognitionBubbleImpl::UpdateLayout+0x28 [c:\b\build\slave\win\build\src\chrome\browser\ui\views\speech\_recognition\_bubble\_views.cc @ 392]  

002ff550 60b8d3e8 chrome\_604e0000!SpeechRecognitionBubbleBase::SetMessage+0x30 [c:\b\build\slave\win\build\src\chrome\browser\speech\speech\_recognition\_bubble.cc @ 219]  

002ff58c 60574608 chrome\_604e0000!speech::SpeechRecognitionBubbleController::ProcessRequestInUiThread+0xd8 [c:\b\build\slave\win\build\src\chrome\browser\speech\speech\_recognition\_bubble\_controller.cc @ 195]  

002ff59c 6053aaf1 chrome\_604e0000!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (\_\_thiscall invalidation::InvalidationClientImpl::\*)(std::vector<invalidation::ObjectId,std::allocator[invalidation::ObjectId](javascript:void(0);) > const &)>,void \_\_cdecl(invalidation::InvalidationClientImpl \*,std::vector<invalidation::ObjectId,std::allocator[invalidation::ObjectId](javascript:void(0);) > const &),void \_\_cdecl(base::internal::UnretainedWrapper[invalidation::InvalidationClientImpl](javascript:void(0);),std::vector<invalidation::ObjectId,std::allocator[invalidation::ObjectId](javascript:void(0);) >)>,void \_\_cdecl(invalidation::InvalidationClientImpl \*,std::vector<invalidation::ObjectId,std::allocator[invalidation::ObjectId](javascript:void(0);) > const &)>::Run+0x16 [c:\b\build\slave\win\build\src\base\bind\_internal.h @ 1253]  

002ff668 6053a193 chrome\_604e0000!base::MessageLoop::RunTask+0x56d [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 513]  

002ff7b8 605a5b5b chrome\_604e0000!base::MessageLoop::DoWork+0x301 [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 638]  

002ff7e4 60552806 chrome\_604e0000!base::MessagePumpForUI::DoRunLoop+0x5c [c:\b\build\slave\win\build\src\base\message\_loop\message\_pump\_win.cc @ 219]  

002ff888 607725b7 chrome\_604e0000!PrefService::SetUserPrefValue+0xd9 [c:\b\build\slave\win\build\src\base\prefs\pref\_service.cc @ 455]  

002ff89c 60772581 chrome\_604e0000!content::BrowserMainLoop::RunMainMessageLoopParts+0x2d [c:\b\build\slave\win\build\src\content\browser\browser\_main\_loop.cc @ 730]  

002ff8ac 604fe8ee chrome\_604e0000!content::BrowserMainRunnerImpl::Run+0x13 [c:\b\build\slave\win\build\src\content\browser\browser\_main\_runner.cc @ 123]  

002ff8e4 604fe6c6 chrome\_604e0000!content::BrowserMain+0x99 [c:\b\build\slave\win\build\src\content\browser\browser\_main.cc @ 26]  

002ff8f8 604fe648 chrome\_604e0000!content::RunNamedProcessTypeMain+0x5d [c:\b\build\slave\win\build\src\content\app\content\_main\_runner.cc @ 472]  

002ff964 604ea943 chrome\_604e0000!content::ContentMainRunnerImpl::Run+0x85 [c:\b\build\slave\win\build\src\content\app\content\_main\_runner.cc @ 791]  

002ff974 604ea388 chrome\_604e0000!content::ContentMain+0x29 [c:\b\build\slave\win\build\src\content\app\content\_main.cc @ 35]  

002ff9ac 01388928 chrome\_604e0000!ChromeMain+0x2b [c:\b\build\slave\win\build\src\chrome\app\chrome\_main.cc @ 34]  

002ffa4c 01388b84 chrome!MainDllLoader::Launch+0x161 [c:\b\build\slave\win\build\src\chrome\app\client\_util.cc @ 302]

## Attachments

- [crash.html](attachments/crash.html) (text/html, 856 B)
- [crash.html](attachments/crash_53183425.html) (text/html, 552 B)

## Timeline

### mb...@chromium.org (2013-12-26)

I'm having some trouble reproducing this one, but it looks very similar to https://crbug.com/chromium/262606. primiano@, could you take a look at this when you get a chance? Adding a few ccs from that bug as well in case anyone has some input on this.

I'm holding off on setting impact for this until I can reproduce it. chromium.khalil, are you seeing this crash on stable or beta as well, or just on canary?

### ch...@gmail.com (2013-12-26)

[Comment Deleted]

### ch...@gmail.com (2013-12-26)

[Comment Deleted]

### ch...@gmail.com (2013-12-26)

https://crbug.com/chromium/262606 is already fixed on canary (previous version), but in effect the bug still exits on canary (latest version) that's why I used a different PoC to repro it again on canary .

### mb...@chromium.org (2013-12-26)

Thanks for the reply. I meant to ask if you were able to reproduce in previous versions with this PoC, or if this PoC is only reproducing against the latest canary.

### ch...@gmail.com (2013-12-26)

Yes, I was able to reproduce the crash in all previous versions.

### mb...@chromium.org (2013-12-26)

Thanks again for the quick response. Updating severity based on this. I'll try to reproduce it later today to confirm.

### mb...@chromium.org (2013-12-26)

I meant to say updating impact labels instead of severity in the previous comment.

### cl...@chromium.org (2013-12-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-01-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-04)

primiano@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### pr...@chromium.org (2014-01-06)

Assigning to tommi@ as his team is the right owner.

### [Deleted User] (2014-01-07)

I am probably the correct owner but I am still waiting for a Windows machine... This and the other referenced bug seems to only happen on Win because I have not been able to reproduce them on Mac/Linux/

### ch...@gmail.com (2014-01-07)

As you said Tommy, I can repro this bug only on the Windows.

### cl...@chromium.org (2014-01-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-09)

[Empty comment from Monorail migration]

### to...@chromium.org (2014-01-09)

[Empty comment from Monorail migration]

### dh...@google.com (2014-01-15)

tommyw: any updates on this bug?

### cl...@chromium.org (2014-01-18)

tommyw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### me...@chromium.org (2014-01-24)

Setting OS label per https://crbug.com/chromium/330660#c13.

### cl...@chromium.org (2014-01-26)

tommyw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-01-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-03)

tommyw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ch...@gmail.com (2014-02-05)

tommyw@: Could you please assign someone else to own this bug if you're busy?


### [Deleted User] (2014-02-06)

[Empty comment from Monorail migration]

### [Deleted User] (2014-02-06)

I was not able to reproduce this today on HEAD (using Windows 8. The behavior or the input fields have changed so I had to slightly rewrite the HTML code as well.

Will do some code inspection tomorrow.

### [Deleted User] (2014-02-10)

I think I have a fix for this issue (thanks to Tommi for introducing me to WinDbg) but since I can't repro this on a self-built binary I'll have to get it submitted and then wait for a bit.

https://codereview.chromium.org/148343008

### cl...@chromium.org (2014-02-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-19)

tommyw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### [Deleted User] (2014-02-19)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-02-20)

------------------------------------------------------------------------
r252269 | tommyw@chromium.org | 2014-02-20T16:56:52.654249Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/speech/speech_recognition_bubble_browsertest.cc?r1=252269&r2=252268&pathrev=252269
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/speech/speech_recognition_bubble_controller.cc?r1=252269&r2=252268&pathrev=252269
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/speech/speech_recognition_bubble.cc?r1=252269&r2=252268&pathrev=252269
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/gtk/speech_recognition_bubble_gtk.cc?r1=252269&r2=252268&pathrev=252269
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/views/speech_recognition_bubble_views.cc?r1=252269&r2=252268&pathrev=252269
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/speech/speech_recognition_bubble.h?r1=252269&r2=252268&pathrev=252269
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/speech/speech_recognition_bubble_controller_unittest.cc?r1=252269&r2=252268&pathrev=252269
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/cocoa/speech_recognition_bubble_cocoa.mm?r1=252269&r2=252268&pathrev=252269

It can happen that when a page with an Speech Recognition enabled input goes away directly after pressing the speech icon that the bubble is using a stale pointer; so instead of cashing a WebContents pointer I look it up every time instead.

BUG=330660

Review URL: https://codereview.chromium.org/148343008
------------------------------------------------------------------------

### in...@chromium.org (2014-02-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-20)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-02-20)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-02-25)

Merge-Requested for both m33 and m34. We want this to go in m33 patch 1 (before Pwnium)

### bu...@chromium.org (2014-02-25)

------------------------------------------------------------------------
r253113 | tommyw@chromium.org | 2014-02-25T10:06:59.686305Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/chrome/browser/speech/speech_recognition_bubble.cc?r1=253113&r2=253112&pathrev=253113
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/chrome/browser/ui/gtk/speech_recognition_bubble_gtk.cc?r1=253113&r2=253112&pathrev=253113
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/chrome/browser/ui/views/speech_recognition_bubble_views.cc?r1=253113&r2=253112&pathrev=253113
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/chrome/browser/speech/speech_recognition_bubble.h?r1=253113&r2=253112&pathrev=253113
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/chrome/browser/speech/speech_recognition_bubble_controller_unittest.cc?r1=253113&r2=253112&pathrev=253113
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/chrome/browser/ui/cocoa/speech_recognition_bubble_cocoa.mm?r1=253113&r2=253112&pathrev=253113
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/chrome/browser/speech/speech_recognition_bubble_browsertest.cc?r1=253113&r2=253112&pathrev=253113
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/chrome/browser/speech/speech_recognition_bubble_controller.cc?r1=253113&r2=253112&pathrev=253113

Merge 252269 "It can happen that when a page with an Speech Reco..."

> It can happen that when a page with an Speech Recognition enabled input goes away directly after pressing the speech icon that the bubble is using a stale pointer; so instead of cashing a WebContents pointer I look it up every time instead.
> 
> BUG=330660
> 
> Review URL: https://codereview.chromium.org/148343008

TBR=inferno@chromium.org

Review URL: https://codereview.chromium.org/176873011
------------------------------------------------------------------------

### bu...@chromium.org (2014-02-25)

------------------------------------------------------------------------
r253126 | tommyw@chromium.org | 2014-02-25T10:29:25.913616Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/chrome/browser/speech/speech_recognition_bubble.cc?r1=253126&r2=253125&pathrev=253126
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/chrome/browser/ui/gtk/speech_recognition_bubble_gtk.cc?r1=253126&r2=253125&pathrev=253126
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/chrome/browser/ui/views/speech_recognition_bubble_views.cc?r1=253126&r2=253125&pathrev=253126
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/chrome/browser/speech/speech_recognition_bubble.h?r1=253126&r2=253125&pathrev=253126
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/chrome/browser/speech/speech_recognition_bubble_controller_unittest.cc?r1=253126&r2=253125&pathrev=253126
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/chrome/browser/ui/cocoa/speech_recognition_bubble_cocoa.mm?r1=253126&r2=253125&pathrev=253126
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/chrome/browser/speech/speech_recognition_bubble_browsertest.cc?r1=253126&r2=253125&pathrev=253126
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/chrome/browser/speech/speech_recognition_bubble_controller.cc?r1=253126&r2=253125&pathrev=253126

Merge 252269 "It can happen that when a page with an Speech Reco..."

> It can happen that when a page with an Speech Recognition enabled input goes away directly after pressing the speech icon that the bubble is using a stale pointer; so instead of cashing a WebContents pointer I look it up every time instead.
> 
> BUG=330660
> 
> Review URL: https://codereview.chromium.org/148343008

TBR=inferno@chromium.org

Review URL: https://codereview.chromium.org/176963011
------------------------------------------------------------------------

### la...@google.com (2014-02-25)

Retrospective Approval.  In the future please wait for the Merge-Approved before landing on an official release branch.

### dh...@chromium.org (2014-02-25)

[Empty comment from Monorail migration]

### [Deleted User] (2014-02-26)

I'm really sorry. I got confused when inferno added the merge-requested label.

### mb...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### ka...@google.com (2014-03-03)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-03-04)

Thanks for the report! This one qualifies for a $500 reward. It did not qualify at a higher reward level because of the amount of user interaction required to trigger the use after free.

### ti...@chromium.org (2014-04-15)

Starting payment process.

### cl...@chromium.org (2014-05-29)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-06-17)

Processing via our e-payment system can take up to 6-8 weeks, but the reward should be on its way to you. Thanks again for your help!


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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/330660?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078600)*

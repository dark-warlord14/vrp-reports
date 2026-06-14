# use-after-free - speech API and window.close() ::SpeechRecognitionBubbleView::GetAnchorRect+0x23

| Field | Value |
|-------|-------|
| **Issue ID** | [40077820](https://issues.chromium.org/issues/40077820) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Speech, Internals>Media>UI |
| **Platforms** | Linux, Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | pr...@chromium.org |
| **Created** | 2013-07-20 |
| **Bounty** | $1,000.00 |

## Description

Hi again Chromium Security Team !

Actually I've found another issue in Speech API again but this time I used window.close()

Crash ID :
60a432a4801a79bd
76fa3b85b260ecbf
0ec010bc289ba9a1
f92f06bc5a8499b6
450b06813a4085bc

Tested on : [windows 7 32bit - Chrome Stable]

Crash type : [Browser]

Steps  to reporting : 

1. Open testcase.html

2. Click double-click on the page.

3.Boom !! the crash 

Stack Info :

(8a8.10f8): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=f85b4626 ebx=0a91e380 ecx=07a63500 edx=002ff3a8 esi=0a91e380 edi=00000003
eip=5497e9ae esp=002ff380 ebp=002ff3ac iopl=0         nv up ei pl zr na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010246
chrome_533b0000!`anonymous namespace'::SpeechRecognitionBubbleView::GetAnchorRect+0x23:
5497e9ae ff503c          call    dword ptr [eax+3Ch]  ds:0023:f85b4662=????????
0:000> k
ChildEBP RetAddr  
002ff3ac 5397f5ff chrome_533b0000!`anonymous namespace'::SpeechRecognitionBubbleView::GetAnchorRect+0x23 [c:\b\build\slave\win\build\src\chrome\browser\ui\views\speech_recognition_bubble_views.cc @ 128]
002ff3e0 5397f577 chrome_533b0000!views::BubbleDelegateView::GetBubbleBounds+0x30 [c:\b\build\slave\win\build\src\ui\views\bubble\bubble_delegate.cc @ 340]
002ff408 5497e68c chrome_533b0000!views::BubbleDelegateView::SizeToContents+0x19 [c:\b\build\slave\win\build\src\ui\views\bubble\bubble_delegate.cc @ 318]
002ff420 5497e828 chrome_533b0000!`anonymous namespace'::SpeechRecognitionBubbleView::UpdateLayout+0x123 [c:\b\build\slave\win\build\src\chrome\browser\ui\views\speech_recognition_bubble_views.cc @ 209]
002ff440 543e3a2c chrome_533b0000!`anonymous namespace'::SpeechRecognitionBubbleImpl::UpdateLayout+0x28 [c:\b\build\slave\win\build\src\chrome\browser\ui\views\speech_recognition_bubble_views.cc @ 395]
002ff450 5436c56f chrome_533b0000!SpeechRecognitionBubbleBase::SetMessage+0x30 [c:\b\build\slave\win\build\src\chrome\browser\speech\speech_recognition_bubble.cc @ 220]
002ff48c 533f1d1d chrome_533b0000!speech::SpeechRecognitionBubbleController::ProcessRequestInUiThread+0xcb [c:\b\build\slave\win\build\src\chrome\browser\speech\speech_recognition_bubble_controller.cc @ 177]
002ff49c 533e7dbf chrome_533b0000!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall history::HistoryBackend::*)(std::vector<history::ExpireHistoryArgs,std::allocator<history::ExpireHistoryArgs> > const &)>,void __cdecl(history::HistoryBackend *,std::vector<history::ExpireHistoryArgs,std::allocator<history::ExpireHistoryArgs> > const &),void __cdecl(scoped_refptr<history::HistoryBackend>,std::vector<history::ExpireHistoryArgs,std::allocator<history::ExpireHistoryArgs> >)>,void __cdecl(history::HistoryBackend *,std::vector<history::ExpireHistoryArgs,std::allocator<history::ExpireHistoryArgs> > const &)>::Run+0x16 [c:\b\build\slave\win\build\src\base\bind_internal.h @ 1257]
002ff530 533e6d07 chrome_533b0000!base::MessageLoop::RunTask+0x34e [c:\b\build\slave\win\build\src\base\message_loop.cc @ 486]
002ff680 535a586c chrome_533b0000!base::MessageLoop::DoWork+0x2ec [c:\b\build\slave\win\build\src\base\message_loop.cc @ 689]
002ff6b0 533e6954 chrome_533b0000!base::MessagePumpForUI::DoRunLoop+0x5b [c:\b\build\slave\win\build\src\base\message_pump_win.cc @ 241]
002ff6d0 533e6872 chrome_533b0000!base::MessageLoop::RunInternal+0x5f [c:\b\build\slave\win\build\src\base\message_loop.cc @ 436]
002ff6e4 538ffd22 chrome_533b0000!base::RunLoop::Run+0x59 [c:\b\build\slave\win\build\src\base\run_loop.cc @ 46]
002ff75c 538ffc04 chrome_533b0000!ChromeBrowserMainParts::MainMessageLoopRun+0x101 [c:\b\build\slave\win\build\src\chrome\browser\chrome_browser_main.cc @ 1647]
002ff770 538ffbce chrome_533b0000!content::BrowserMainLoop::RunMainMessageLoopParts+0x2d [c:\b\build\slave\win\build\src\content\browser\browser_main_loop.cc @ 554]
002ff780 5343ddd3 chrome_533b0000!content::BrowserMainRunnerImpl::Run+0x13 [c:\b\build\slave\win\build\src\content\browser\browser_main_runner.cc @ 126]
002ff794 533cb315 chrome_533b0000!content::BrowserMain+0x3c [c:\b\build\slave\win\build\src\content\browser\browser_main.cc @ 22]
002ff7a8 533cb29c chrome_533b0000!content::RunNamedProcessTypeMain+0x58 [c:\b\build\slave\win\build\src\content\app\content_main_runner.cc @ 431]
002ff814 533babe1 chrome_533b0000!content::ContentMainRunnerImpl::Run+0x85 [c:\b\build\slave\win\build\src\content\app\content_main_runner.cc @ 754]
002ff824 533ba8d3 chrome_533b0000!content::ContentMain+0x29 [c:\b\build\slave\win\build\src\content\app\content_main.cc @ 35]


Thanks,
Khalil Zhani

## Attachments

- [crash.png](attachments/crash.png) (image/png; charset=binary, 100.7 KB)
- [testcase.html](attachments/testcase.html) (text/html; charset=us-ascii, 538 B)
- [crash.txt](attachments/crash.txt) (text/x-c++; charset=us-ascii, 4.5 KB)
- [ee.png](attachments/ee.png) (image/png; charset=binary, 128.5 KB)
- [uaf_stack.txt](attachments/uaf_stack.txt) (text/plain; charset=us-ascii, 11.2 KB)
- [repro.patch](attachments/repro.patch) (text/x-diff; charset=us-ascii, 2.1 KB)
- [speech_recognition_repro.patch](attachments/speech_recognition_repro.patch) (text/x-diff; charset=us-ascii, 4.3 KB)

## Timeline

### ts...@chromium.org (2013-07-24)

Thanks. khalil, when reporting, be sure to include the exact chrome version number.
Repro'd on chrome 30.0.1575.0 linux.

### ae...@chromium.org (2013-07-24)

Repro'd here as well, 30.0.1574.0 linux. Hits a NULL deref.

### ts...@chromium.org (2013-07-24)

Browser DoS are a minor nuisance and hence severity low.

### ts...@chromium.org (2013-07-24)

DNR on 29.0.1547.15, recent regression.

### ae...@chromium.org (2013-07-24)

The windows crash looks fairly interesting though:

call    dword ptr [eax+3Ch]  ds:0023:f85b4662=????????
eax=f85b4626

### ts...@chromium.org (2013-07-24)

Crash server shows this at V28.0.1500.72.  Hmmm.

### ch...@gmail.com (2013-07-24)

Yep, that's what I see 

### ae...@chromium.org (2013-07-24)

Well, the NULL deref on linux is certainly uninteresting.

Before dereferencing, bubble_ is assigned NULL here, because the view is gone:

      bubble_.reset(SpeechRecognitionBubble::Create(
          tab_util::GetWebContentsByID(request.render_process_id,
                                       request.render_view_id),
          this, request.element_rect));

Wonder what happens on win32 though.

### ch...@gmail.com (2013-07-25)

I got this on Ubuntu 12.04.

Program received signal SIGSEGV, Segmentation fault.
0x80355d46 in ?? ()
(gdb) bt
#0  0x80355d46 in ?? ()
#1  0x80355410 in ?? ()
Backtrace stopped: previous frame inner to this frame (corrupt stack?)
(gdb) info r
eax            0x0	0
ecx            0x0	0
edx            0x1	1
ebx            0x84c5f6b8	-2067401032
esp            0xbfffefa0	0xbfffefa0
ebp            0xbffff180	0xbffff180
esi            0x859fd858	-2053121960
edi            0x85d2d7c0	-2049779776
eip            0x80355d46	0x80355d46
eflags         0x210282	[ SF IF RF ID ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x33	51

### ch...@gmail.com (2013-07-25)

[Comment Deleted]

### ae...@chromium.org (2013-07-29)

Thanks for the Ubuntu crash dump. Could you do another round and also output the crashing instruction:

x/1i $eip

Symbolized stack trace would also be nice, but that's somewhat more work.

I'll try to test if the crash on windows is more interesting.

### ch...@gmail.com (2013-07-29)

(gdb) x/1i $eip
=> 0x80355d46:	mov    (%eax),%edx
(gdb) i r
eax            0x0	0
ecx            0x0	0
edx            0x1	1
ebx            0x84c5f6b8	-2067401032
esp            0xbfffefa0	0xbfffefa0
ebp            0xbffff180	0xbffff180
esi            0x855374d8	-2058128168
edi            0x85471d40	-2058937024
eip            0x80355d46	0x80355d46
eflags         0x210286	[ PF SF IF RF ID ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x33	51


### ch...@gmail.com (2013-07-29)

Seems a NULL deref, but on the windows it's more interesting.

### ch...@gmail.com (2013-07-29)

[Comment Deleted]

### ch...@gmail.com (2013-07-29)

[Comment Deleted]

### ch...@gmail.com (2013-07-29)

I guess on the screenshot (the bubble) makes on the windows more interesting before the crash.


### ae...@chromium.org (2013-07-29)

The original dump actually looks a lot like a UaF. It crashes here:

  web_contents_->GetView()->GetContainerBounds(&container_rect);

The vtable pointer of web_contents_ is invalid 0xf85b4626. And web_contents_ is a raw pointer to WebContents, which is freed on window.close().

Still haven't been able to reproduce it though.

### ae...@chromium.org (2013-07-30)

Probably doesn't trigger on linux, because it has a different SpeechRecognitionBubble implementation, which doesn't try to use web_contents_.

### ae...@chromium.org (2013-07-30)

Still trying to repro, but setting the flags to what they'll likely be.

I think it would be critical severity, but since it requires user interaction, I'll set it to high severity.

### in...@chromium.org (2013-07-31)

Tommi, can you please take a look or help with an owner.

### ch...@gmail.com (2013-08-02)

After analyzing I couldn't repro it on the Linux, and this bug looks clearly a Use-
After-Free.

### ae...@chromium.org (2013-08-02)

I reproduced it on Windows ASAN build. Couldn't get UaF dump though, probably because the WebContents slot is re-allocated before use.

I do get a UaF dump on linux, if I add code to do what Windows does - access WebContents from set message request. Apply repro.patch to reproduce on linux.

As a fix, I'm not sure. Can the bubble just take a reference to WebContents instead of a raw pointer?

@jam, you're probably familiar with this code, could you please take a look?

### [Deleted User] (2013-08-02)


Sorry for the late response, I am busy with some other tasks until now.

That code was very old and I don't understand why the problems pops up now, and I feel we'd better figure out what has been changed and why GetContainerBounds(&container_rect) needs to be called there.

Mike, the code looks relevant to https://codereview.chromium.org/8565003, do you know why the bubble can outlive the webcontent?

SX

### ms...@chromium.org (2013-08-02)

SpeechRecognitionBubbleView::GetAnchorRect() calls web_contents_->GetView()->GetContainerBounds(&container_rect); to align the bubble with the icon in the web contents, or return some reasonable value if the icon is offscreen.

If the bubble is outliving the WebContents, that clearly seems bad.
Most other bubbles close with their parent or anchor widget automatically.
Sadly, I wasn't able to use set_close_on_deactivate() for this bubble, because:
// The bubble lifetime is managed by its controller; closing on escape or
// explicitly closing on deactivation will cause unexpected behavior.
https://code.google.com/p/chromium/codesearch#chromium/src/chrome/browser/ui/views/speech_recognition_bubble_views.cc&l=116
(set_notify_delegate_on_activation_change might also be of interest)

I'm not familiar with SpeechRecognitionBubble[Base] or SpeechRecognitionBubbleController. Since this is a cross platform issue (comments #1 and #2 mention repro on Linux), it's likely a defect in those cross-platform classes, and not the Views-specific (Win and CrOS) impl. If the owners of those bubble/controller classes can't help, I can take a look.

### ha...@chromium.org (2013-08-02)

[Empty comment from Monorail migration]

### ae...@chromium.org (2013-08-04)

Crashes #1 and #2 were a bit different issues. Bubble was created after WebContents was already gone, so bubble creation failed, which caused bubble_ NULL deref.

#22 shows that bubble can outlive WebContents on linux as well. But it looks like linux bubble implementation can't be made to use WebContents after it has been freed. So the root cause is cross platform and high severity is only for windows.

### ch...@gmail.com (2013-08-09)

Is he Tommi on vacation ? 

### to...@chromium.org (2013-08-09)

I'm back from my vacation but those that might actually know this code are still on vacation!  I'll take a look.

### ch...@gmail.com (2013-08-13)

[Comment Deleted]

### to...@chromium.org (2013-08-21)

mcasas - can you look at this please?

### mc...@chromium.org (2013-08-23)

Had a quick look and try - didn't crash in my Win7, and I'm won't be away for a week so I'll bounce it back to tommi to reassign.

### to...@chromium.org (2013-08-23)

Tommy - can you take a look at this one?

### ch...@gmail.com (2013-08-26)

minimize report :

<input type="search" onclick="window.close()" x-webkit-speech/>

### [Deleted User] (2013-08-26)

I started looking at this and while I can't repro this exact crash due to not having a Windows machine I have found several other problems which might well be the underlying issues.

### ch...@gmail.com (2013-09-01)

For repro this crash you should have a fresh browsing session.

### bu...@chromium.org (2013-09-03)

------------------------------------------------------------------------
r220936 | tommyw@chromium.org | 2013-09-03T13:39:33.641123Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/speech/speech_recognition_bubble_controller.cc?r1=220936&r2=220935&pathrev=220936

WebSpeech: Protect the thread switching code from bubble changes
Changing two DCHECKs to just if cases. These DCHECKs will be hit
if the user very quickly opens and then closes the bubble.

BUG=262606

Review URL: https://chromiumcodereview.appspot.com/23403005
------------------------------------------------------------------------

### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### [Deleted User] (2013-09-03)

I am not certain that my patch fixes the complete issue so closing it before the issue is verified is likely wrong. None of the dev team have been able to repro the issue on Win but I managed to easily find and fix a related issue on Linux.

### in...@chromium.org (2013-09-03)

[Comment Deleted]

### in...@chromium.org (2013-09-03)

Bulk move. M29 is released.

### in...@chromium.org (2013-09-03)

Fix labels.

### pr...@chromium.org (2013-09-06)

Is it possible to have more details about the issue experienced in Linux?
I tried to repro reverting r220936 but can't hit any dcheck on Linux.

Many Thanks.


### ae...@chromium.org (2013-09-20)

I can hit a DCHECK in InvokeDelegateFocusChanged() after reverting r220936. I double click on the repro page.

If I do a linux release build and apply the patch from #22, I get a UaF stack after ~10 tries.

### in...@chromium.org (2013-09-21)

Aedla@, do you mean to say that r200936 fixes the bug ? If yes, please close the close as fixed.

### pr...@chromium.org (2013-09-25)

Correct me if I am wrong, but I think that nobody here as looked at the windows bug yet, which is the one originally reported in this bug.
The discussion about r200936 seems somehow independent, as the original bug was affecting views ui and AFAIK we're still using GTK on desktop Linux.


### ch...@gmail.com (2013-09-25)

Note : primiano@, inferno@, it's r220936, not r200936.

### ch...@gmail.com (2013-09-25)

[Comment Deleted]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### cl...@chromium.org (2013-09-27)

tommyw@: you haven't provided any bug update or come up with a fix for this issue in the last 7 days. Please note that this is a medium+ severity security vulnerability that needs your immediate response. If you have a patch in progress and don't want future nags, please add a codereview link and a WIP label. If the issue is already fixed or you can't reproduce it, please close the bug.

### ch...@gmail.com (2013-09-28)

inferno@, Is this issue fixed or not yet?

### in...@chromium.org (2013-09-28)

Chromium.khalil@, it does not look like the issue is fixed. i closed it wrong before, by seeing the linux fix. but it looks like windows fix is still pending.

### [Deleted User] (2013-09-30)

chromium.khalil@: As in the other bug can you download the latest canary and check if the issue is fixed? For some reason we have had zero success to repro this issue on Windows.

### ch...@gmail.com (2013-09-30)

tommyw@, It's fixed.

### in...@chromium.org (2013-09-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-30)

Adding Merge-Requested label.

Please do not merge your patch without first checking with the release manager. Once the merge is approved by the release manager, make sure to merge the fix to all the affected branches, i.e stable, beta and trunk (near branch point). Look for the branch information on omahaproxy.appspot.com.

If this fix is not applicable for merge, change this label to Merge-NA.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-10-02)

Migrating old milestone labels.

### ae...@chromium.org (2013-10-03)

Sorry guys, but this still reproduces for me on Windows trunk build. I don't have an ASAN build, but I added some printf's like this:

diff --git a/chrome/browser/ui/views/speech_recognition_bubble_views.cc b/chrome/browser/ui/views/sp
index 2434c1d..ef68353 100644
--- a/chrome/browser/ui/views/speech_recognition_bubble_views.cc
+++ b/chrome/browser/ui/views/speech_recognition_bubble_views.cc
@@ -125,6 +125,8 @@ void SpeechRecognitionBubbleView::OnWidgetActivationChanged(

 gfx::Rect SpeechRecognitionBubbleView::GetAnchorRect() {
   gfx::Rect container_rect;
+  printf("use %016lx\n", (unsigned long)web_contents_);
+  fflush(stdout);
   web_contents_->GetView()->GetContainerBounds(&container_rect);
   gfx::Rect anchor(element_rect_);
   anchor.Offset(container_rect.OffsetFromOrigin());
diff --git a/content/browser/web_contents/web_contents_impl.cc b/content/browser/web_contents/web_co
index cf74d27..7848db1 100644
--- a/content/browser/web_contents/web_contents_impl.cc
+++ b/content/browser/web_contents/web_contents_impl.cc
@@ -378,6 +378,8 @@ WebContentsImpl::WebContentsImpl(
 }

 WebContentsImpl::~WebContentsImpl() {
+  printf("free %016lx\n", (unsigned long)this);
+  fflush(stdout);
   is_being_destroyed_ = true;

   ClearAllPowerSaveBlockers();

which prints out:

...
free 00000000066ef2e0
use 00000000066ef2e0
Segmentation fault

So clearly there is still a use-after-free.

### ae...@chromium.org (2013-10-03)

I looked into what happens. It is an interaction between UI and IO thread tasks.

Free tasks
----------
Renderer sends ViewHostMsg_Close, which starts a task on UI thread, I'll call this task FREE_UI, because it frees WebContentsImpl. FREE_UI also posts ChromeSpeechRecognitionManagerDelegateBubbleUI::TabClosedCallback on IO thread, I'll call this task FREE_IO. FREE_IO closes the bubble by setting current_bubble_session_id_ = kInvalidSessionId.

Use tasks
---------
Channel to the renderer closes, which triggers a chain of IO tasks to abort recognition. Last task in this chain runs SpeechRecognizerImpl::Abort, I'll call this task USE_IO, because it will cause WebContentsImpl to be used. If bubble hasn't been closed yet, USE_IO calls SpeechRecognitionBubbleController::SetBubbleMessage to set the bubble text to "Speech recognition was aborted.". SetBubbleMessage then posts a UI task, which I'll call USE_UI and which will actually cause bubble_ to use web_contents_.

So let's say FREE_UI is running. At some point it posts FREE_IO. USE_IO could be posted either before or after that point. UaF happens when USE_IO is posted before FREE_IO. This means USE_IO also runs before FREE_IO. Since FREE_IO hasn't yet run, bubble is still open and USE_IO attempts to set bubble message by posting USE_UI. Once FREE_UI is finished and has deleted WebContentsImpl, USE_UI runs and uses WebContentsImpl.

### ae...@chromium.org (2013-10-03)

The bug reproduces pretty reliably for me on windows, but not so well on linux. I made it reliable on linux by adding a delay before posting FREE_IO so it will be posted after USE_IO. Attached is a patch with the delay and some printf's for debugging. If you still can't reproduce the bug with this patch, please copy the debug output to this issue.

### pr...@chromium.org (2013-10-03)

Many thanks aedla@ for all the investigation. I extremely appreciated it. Your analysis is correct and you saved me many time! I owe you a beer ;)

There was a race during the tab closing path due to the call to the CloseBubble being posted.
It should be fixed by https://codereview.chromium.org/25948002/

Khalil: Can you try to see if it repros again applying the CL crrev.com/25948002.

Thanks

### ae...@chromium.org (2013-10-04)

Thank you for the fix. I think that should do it.

### ch...@gmail.com (2013-10-04)

primiano@, I couldn't repro it, Thanks for the fix.

### bu...@chromium.org (2013-10-04)

------------------------------------------------------------------------
r227023 | primiano@chromium.org | 2013-10-04T17:01:26.435708Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/speech/chrome_speech_recognition_manager_delegate_bubble_ui.cc?r1=227023&r2=227022&pathrev=227023
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/speech/chrome_speech_recognition_manager_delegate_bubble_ui.h?r1=227023&r2=227022&pathrev=227023
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/speech/speech_recognition_bubble_controller.cc?r1=227023&r2=227022&pathrev=227023
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/speech/speech_recognition_bubble_controller.h?r1=227023&r2=227022&pathrev=227023
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/speech/chrome_speech_recognition_manager_delegate.cc?r1=227023&r2=227022&pathrev=227023

[Input element speech API] Close the bubble synchronously on tab closure.

When a tab is closed while an <input x-webkit-speech> element is
performing speech recognition and showing the corresponding bubble,
the bubble must be closed.
The previous implementation was doing that asyncrhonously by means of
(a couple of) PostTask. It turned out this is not correct and the
bubble must be closed synchronously, because the underlying
WebContents are going to be disposed immediately after the call.
This CL makes this action synchronous.

BUG=262606

Review URL: https://codereview.chromium.org/25948002
------------------------------------------------------------------------

### pr...@chromium.org (2013-10-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

[Comment Deleted]

### pr...@chromium.org (2013-10-15)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-10-22)

Thanks for the report! This one qualifies for a $1000 reward. It did not qualify for a higher reward because there does not seem to be control between the free and use.

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

Hey there, just kicked off payment on this one and 268565. Thanks again for your help!

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/262606?no_tracker_redirect=1

[Multiple monorail components: Blink>Speech, Internals>Media>UI]
[Monorail mergedwith: crbug.com/chromium/265505]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077820)*

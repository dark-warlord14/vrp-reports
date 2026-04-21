# Aww snap crash when editing canvas text

| Field | Value |
|-------|-------|
| **Issue ID** | [40055253](https://issues.chromium.org/issues/40055253) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Canvas |
| **Platforms** | Mac |
| **Reporter** | [Deleted User] |
| **Assignee** | li...@chromium.org |
| **Created** | 2021-03-19 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36

Steps to reproduce the problem:
1. Have chrome Hardware Acceleration setting OFF
2. Relaunch page
3. Sign into Seesaw account as a teacher
4. Go to Activities tab and select activity with a template (https://help.seesaw.me/hc/en-us/articles/115005282803-How-do-I-customize-activities-in-Seesaw-)
5. Click ‘Edit Activity’ 
6. Click on Template and see that canvas opens
7. Add a page and use drawing tool then try adding a label
8. Repeat step 7 several times, the page crashes with 'Aw Snap error code

What is the expected behavior?
Browser does not crash

What went wrong?
Browser crashes

Crashed report ID: dc9042194c0f3d83

How much crashed? Just one tab

Is it a problem with a plugin? N/A 

Did this work before? Yes No reports of a crash with these steps in Chrome 88

Chrome version: 89.0.4389.90  Channel: stable
OS Version: OS X 10.15.7
Flash Version: 

Many Seesaw Users are reporting this crash on Chrome 89 on Macs. 

Crash report IDs from two other users: 
487308fb29e7eabe
4e113afb300c099b

## Attachments

- [1189926.mp4](attachments/1189926.mp4) (video/mp4, 1.3 MB)
- [chrome_crash.mov](attachments/chrome_crash.mov) (video/quicktime, 3.3 MB)
- [Screen Shot 2021-03-19 at 9.21.31 AM.png](attachments/Screen Shot 2021-03-19 at 9.21.31 AM.png) (image/png, 1.3 MB)
- [Screen Shot 2021-03-23 at 12.52.09 PM.png](attachments/Screen Shot 2021-03-23 at 12.52.09 PM.png) (image/png, 95.2 KB)
- [gpu.txt](attachments/gpu.txt) (text/plain, 5.8 KB)

## Timeline

### va...@chromium.org (2021-03-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>Canvas]

### sa...@chromium.org (2021-03-19)

Tried testing the issue on reported chrome version #89.0.4389.90 using Mac 10.12.6 as per https://crbug.com/chromium/1189926#c0 and didn't see option 'Edit Activity' to open the canvas.

@Reporter: Could you please review attached screencast and let us know if anything is being missed here.

Thanks..

### [Deleted User] (2021-03-19)

After you press the heart button, a "Copy and Edit Activity" option will be available under the three dots. 

### [Deleted User] (2021-03-19)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-19)

In case it's helpful, I've attached a screenshot with the buttons to click to edit the activity, and a screen recording of encountering the crash while editing text.


### sa...@chromium.org (2021-03-22)

Retried the issue on chrome stable as per https://crbug.com/chromium/1189926#c3 & https://crbug.com/chromium/1189926#c5 and unable to reproduce the issue, hence removing Needs-Bisect label, feel free to add back if required. Also marking status to untriaged so that dev can have a look and  provide further updates.

Thanks..

### [Deleted User] (2021-03-23)

Since the browser does not crash every time text is edited on the canvas, we tried memory profiling while reproducing the crash. Here is a video with the Performance Monitor Chrome dev tool open through the crash: https://drive.google.com/file/d/1uRiW5WBP-qkOqL_hax-TbGuz4A35egpZ/view?usp=sharing. Heap size starts ~40MB and ends ~60MB. DOM Nodes start ~13,000 and end ~21,000. 

In comparison, the same profiling when opening a Google Sheet on the same computer shows JS Heap Size in the 70-80MB range and DOM Nodes ~30,000, and that tab does not crash.

I've also attached About this Mac and chrome://gpu information from the same computer. 

We also wanted to download the crash logs from this Mac, but did not find files at locations listed in either of these instructions: https://support.google.com/chrome/a/answer/6271282?hl=en#zippy=%2Cmac, https://www.chromium.org/for-testers/bug-reporting-guidelines/reporting-crash-bug. Are there other instructions on how we can get more information about these crashes?

Is there any other information I could gather that would be helpful?  

### [Deleted User] (2021-03-24)

We made a Seesaw account with activities users have reported this problem while editing, please feel free to use it for testing if that would be helpful. At https://app.seesaw.me/#/login, hit "I'm a Teacher", login as emily+teacher@seesaw.me with password seesaw2020. Follow the same steps as in the crash video (https://drive.google.com/file/d/1uRiW5WBP-qkOqL_hax-TbGuz4A35egpZ/view?usp=sharing):
- Switch to the Activities tab in the right pane
- Hit the three dots more options button on any of these activities, then Edit Activity
- Type into labels on the canvas (along with various other interactions) until the tab crashes

With these steps (on the Mac that I posted info for in the previous comment), our QA engineer reliably reproduces the crash. We would all be happy to hop on a call and/or have her run any steps that would help us get to the bottom of this problem. We have 50+ users reporting this crash, and for now we can only advise them to please use Seesaw on another browser.

### aj...@chromium.org (2021-03-24)

[Empty comment from Monorail migration]

### aj...@chromium.org (2021-03-24)

Stack trace of the crash id: dc9042194c0f3d83 from C#0

Thread 0  (id: 0x0034bc22) CRASHED [EXC_BAD_ACCESS / EXC_I386_GPFLT @ 0x0000000110ea9174 ] MAGIC SIGNATURE THREADShow exception record
0x0000000110ea9174(Google Chrome Framework -scrollbar.cc:800)blink::Scrollbar::SetNeedsPaintInvalidation(blink::ScrollbarPart)
0x0000000116164d4a(Google Chrome Framework -scroll_animator_mac.mm:330)blink::BlinkScrollbarPartAnimationTimer::TimerFired(blink::TimerBase*)
0x00000001110306d5(Google Chrome Framework -timer.cc:152)blink::TimerBase::RunInternal()
0x000000010f8d2368(Google Chrome Framework -callback.h:101)base::TaskAnnotator::RunTask(char const*, base::PendingTask*)
0x000000010f8e09ad(Google Chrome Framework -thread_controller_with_message_pump_impl.cc:351)base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*)
0x000000010f8e04cd(Google Chrome Framework -thread_controller_with_message_pump_impl.cc:264)base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
0x000000010f9177b2(Google Chrome Framework -message_pump_mac.mm:358)base::MessagePumpCFRunLoopBase::RunWork()
0x000000010f914059(Google Chrome Framework + 0x00000000010cc059)base::mac::CallWithEHFrame(void () block_pointer)
0x000000010f91712d(Google Chrome Framework -message_pump_mac.mm:325)base::MessagePumpCFRunLoopBase::RunDelayedWorkTimer(__CFRunLoopTimer*, void*)
0x00007fff3051c7f8(CoreFoundation + 0x0009e7f8)__CFRUNLOOP_IS_CALLING_OUT_TO_A_TIMER_CALLBACK_FUNCTION__
0x00007fff3051c35e(CoreFoundation + 0x0009e35e)__CFRunLoopDoTimer
0x00007fff3051be46(CoreFoundation + 0x0009de46)__CFRunLoopDoTimers
0x00007fff30500be9(CoreFoundation + 0x00082be9)__CFRunLoopRun
0x00007fff304ffe3d(CoreFoundation + 0x00081e3d)CFRunLoopRunSpecific
0x00007fff32b9b1d7(Foundation + 0x000601d7)-[NSRunLoop(NSRunLoop) runMode:beforeDate:]
0x000000010f917cc3(Google Chrome Framework -message_pump_mac.mm:604)base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)
0x000000010f916d0a(Google Chrome Framework -message_pump_mac.mm:149)base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)
0x000000010f8e140e(Google Chrome Framework -thread_controller_with_message_pump_impl.cc:460)base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)
0x000000010f8be1f8(Google Chrome Framework -run_loop.cc:131)base::RunLoop::Run()
0x00000001113214e7(Google Chrome Framework -renderer_main.cc:260)content::RendererMain(content::MainFunctionParams const&)
0x000000010f881199(Google Chrome Framework -content_main_runner_impl.cc:937)content::ContentMainRunnerImpl::Run(bool)
0x000000010f87fe6f(Google Chrome Framework -content_main.cc:372)content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*)
0x000000010f880331(Google Chrome Framework -content_main.cc:398)content::ContentMain(content::ContentMainParams const&)
0x000000010e84eba7(Google Chrome Framework -chrome_main.cc:141)ChromeMain
0x00000001077eb523(Google Chrome Helper (Renderer) -chrome_exe_main_mac.cc:114)main
0x00007fff6a5a1cc8(libdyld.dylib + 0x0001acc8)start

Stack trace matches with https://crbug.com/chromium/1183276(unable to access but was pinged by maguschen@). As per update, this crash should already be fixed on the latest canary and next/upcoming beta and stable, possibly very soon.

Based on stack trace comparison, looks same as https://crbug.com/chromium/1183276(unable to dupe due to permission issue)

@reporter: Could you please check this on the latest canary(https://www.google.com/intl/en_in/chrome/canary/) and confirm if its fixed for you as well?

### li...@chromium.org (2021-03-24)

[Empty comment from Monorail migration]

### li...@chromium.org (2021-03-24)

I was able to reproduce on Canary 91.0.4457.0.
Also, I was able to reproduce locally on ToT. The stack trace looks like this:

2021-03-24 12:04:44.257 Chromium Helper (Renderer)[18689:7602542] CoreText note: Client requested name ".AppleSymbolsFB", it will get Times-Roman rather than the intended font. All system UI font access should be through proper APIs such as CTFontCreateUIFontForLanguage() or +[NSFont systemFontOfSize:].
2021-03-24 12:04:44.257 Chromium Helper (Renderer)[18689:7602542] CoreText note: Set a breakpoint on CTFontLogSystemFontNameRequest to debug.
Received signal 10 BUS_ADRERR 60c00007b640
0   libbase.dylib                       0x000000012682f889 base::debug::CollectStackTrace(void**, unsigned long) + 9
1   libbase.dylib                       0x000000012643df73 base::debug::StackTrace::StackTrace() + 19
2   libbase.dylib                       0x000000012682f14b base::debug::(anonymous namespace)::StackDumpSignalHandler(int, __siginfo*, void*) + 2875
3   libsystem_platform.dylib            0x00007fff203bad7d _sigtramp + 29
4   ???                                 0x0000000000000000 0x0 + 0
5   libblink_core.dylib                 0x000000014f7d40ff -[BlinkScrollbarPartAnimation setCurrentProgress:] + 559
6   libblink_core.dylib                 0x000000014f7dc539 blink::BlinkScrollbarPartAnimationTimer::TimerFired(blink::TimerBase*) + 633
7   libblink_platform.dylib             0x00000001576d4d9c blink::TimerBase::RunInternal() + 348
8   libblink_core.dylib                 0x000000014d2bb99f base::internal::Invoker<base::internal::BindState<void (blink::TimerBase::*)(), base::WeakPtr<blink::TimerBase> >, void ()>::RunOnce(base::internal::BindStateBase*) + 479
9   libblink_core.dylib                 0x000000014bdfc0ff WTF::ThreadCheckingCallbackWrapper<base::OnceCallback<void ()>, void ()>::Run() + 383
10  libbase.dylib                       0x0000000126699d78 base::TaskAnnotator::RunTask(char const*, base::PendingTask*) + 1224
11  libbase.dylib                       0x0000000126710fc8 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) + 2584
12  libbase.dylib                       0x000000012670fdad base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() + 349
13  libbase.dylib                       0x00000001268a2b29 base::MessagePumpCFRunLoopBase::RunWork() + 393
14  libbase.dylib                       0x00000001268777da base::mac::CallWithEHFrame(void () block_pointer) + 10
15  libbase.dylib                       0x00000001268a1146 base::MessagePumpCFRunLoopBase::RunDelayedWorkTimer(__CFRunLoopTimer*, void*) + 374
16  CoreFoundation                      0x00007fff2048790d __CFRUNLOOP_IS_CALLING_OUT_TO_A_TIMER_CALLBACK_FUNCTION__ + 20
17  CoreFoundation                      0x00007fff204873e8 __CFRunLoopDoTimer + 922
18  CoreFoundation                      0x00007fff20486f42 __CFRunLoopDoTimers + 307
19  CoreFoundation                      0x00007fff2046d57f __CFRunLoopRun + 2008
20  CoreFoundation                      0x00007fff2046c6ce CFRunLoopRunSpecific + 563
21  Foundation                          0x00007fff211f9fa1 -[NSRunLoop(NSRunLoop) runMode:beforeDate:] + 212
22  libbase.dylib                       0x00000001268a4971 base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*) + 257
23  libbase.dylib                       0x000000012689fa79 base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*) + 521
24  libbase.dylib                       0x0000000126712d86 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) + 1526
25  libbase.dylib                       0x00000001265e1e14 base::RunLoop::Run(base::Location const&) + 2292
26  libcontent.dylib                    0x0000000135fc4268 content::RendererMain(content::MainFunctionParams const&) + 3320
27  libcontent.dylib                    0x00000001363bc0cf content::ContentMainRunnerImpl::Run(bool) + 1327
28  libcontent.dylib                    0x00000001363b8757 content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) + 5879
29  libcontent.dylib                    0x00000001363b8d2d content::ContentMain(content::ContentMainParams const&) + 29
30  libchrome_dll.dylib                 0x0000000111ae5b41 ChromeMain + 545
31  Chromium Helper (Renderer)          0x0000000107c1b7a9 main + 697
32  libdyld.dylib                       0x00007fff20391621 start + 1
33  ???                                 0x000000000000000d 0x0 + 13
[end of stack trace]
 

### ad...@google.com (2021-03-24)

Flipping to security bug, since this is believed to be the root cause behind https://crbug.com/chromium/1183276.

### [Deleted User] (2021-03-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-24)

Thank you for looking into this! Just confirming that our QA engineer is still reproducing the issue on latest Canary (still the same device as https://crbug.com/chromium/1189926#c7).

### [Deleted User] (2021-03-24)

Crash report ID from repro on Canary: c4abf92bc1ce29eb

### li...@chromium.org (2021-03-29)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/19207bea6bd8472aa4203db328fc7f51826956d4

commit 19207bea6bd8472aa4203db328fc7f51826956d4
Author: Liviu Tinta <liviutinta@chromium.org>
Date: Tue Mar 30 13:44:40 2021

Fix Mac crash due to use after free of BlinkScrollbarPartAnimation

What is happening is that the BlinkScrollbarPartAnimation instance
passed to BlinkScrollbarPartAnimationTimer is released while
the BlinkScrollbarPartAnimationTimer::TimerFired method runs as
part of BlinkScrollbarPartAnimation::setCurrentProgress call,
during the execution of ScrollbarPainter::setKnobAlpha which ends
up calling BlinkScrollbarPainterDelegate::setUpAlphaAnimation
through a chain of observers.
BlinkScrollbarPainterDelegate::setUpAlphaAnimation releases the
BlinkScrollbarPartAnimation instance which gets deallocated.
BlinkScrollbarPartAnimation::setCurrentProgress continues execution
after ScrollbarPainter::setKnobAlpha returns, but the _scrollbar
pointer is overwritten with garbage and when SetNeedsPaintInvalidation
is called the crash happens.

I believe that BlinkScrollbarPartAnimationTimer::TimerFired should
retain the animation_ while it runs and release animation_ before
it exits. By retaining Objective C runtime won't free animation_
while BlinkScrollbarPartAnimationTimer is running and the crash
should be avoided.

Bug: 1183276, 1189926
Change-Id: Ibd5092a1dbae53bc21940c43883536624d1b03f3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2787572
Commit-Queue: Robert Flack <flackr@chromium.org>
Reviewed-by: Robert Flack <flackr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#867587}

[modify] https://crrev.com/19207bea6bd8472aa4203db328fc7f51826956d4/third_party/blink/renderer/core/scroll/mac_scrollbar_animator_impl.mm


### li...@chromium.org (2021-03-30)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-30)

Pretty sure Sheriffbot would add a merge request later this morning anyway, so just shortcutting the process in case I'm wrong. We'll wait for some Canary coverage before approving the merge request.

### [Deleted User] (2021-03-30)

This bug requires manual review: We are only 13 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-30)

[Empty comment from Monorail migration]

### sa...@chromium.org (2021-03-31)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-31)

Approving merge to M90; please merge to branch 4430.

### gi...@appspot.gserviceaccount.com (2021-04-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3e2009952e2e9a7b27de18a3d393662269b827e7

commit 3e2009952e2e9a7b27de18a3d393662269b827e7
Author: Liviu Tinta <liviutinta@chromium.org>
Date: Thu Apr 01 18:07:07 2021

Fix Mac crash due to use after free of BlinkScrollbarPartAnimation

What is happening is that the BlinkScrollbarPartAnimation instance
passed to BlinkScrollbarPartAnimationTimer is released while
the BlinkScrollbarPartAnimationTimer::TimerFired method runs as
part of BlinkScrollbarPartAnimation::setCurrentProgress call,
during the execution of ScrollbarPainter::setKnobAlpha which ends
up calling BlinkScrollbarPainterDelegate::setUpAlphaAnimation
through a chain of observers.
BlinkScrollbarPainterDelegate::setUpAlphaAnimation releases the
BlinkScrollbarPartAnimation instance which gets deallocated.
BlinkScrollbarPartAnimation::setCurrentProgress continues execution
after ScrollbarPainter::setKnobAlpha returns, but the _scrollbar
pointer is overwritten with garbage and when SetNeedsPaintInvalidation
is called the crash happens.

We retain self in BlinkScrollbarPartAnimation::setCurrentProgress
while it runs and release self before exit. By retaining self
Objective C runtime won't free BlinkScrollbarPartAnimation
while BlinkScrollbarPartAnimationTimer is running and the crash
should be avoided.

(cherry picked from commit 19207bea6bd8472aa4203db328fc7f51826956d4)

Bug: 1183276, 1189926, 1193025
Change-Id: Ibd5092a1dbae53bc21940c43883536624d1b03f3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2787572
Commit-Queue: Robert Flack <flackr@chromium.org>
Reviewed-by: Robert Flack <flackr@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#867587}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2799973
Commit-Queue: Liviu Tinta <liviutinta@chromium.org>
Cr-Commit-Position: refs/branch-heads/4430@{#979}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/3e2009952e2e9a7b27de18a3d393662269b827e7/third_party/blink/renderer/core/scroll/scroll_animator_mac.mm


### ad...@google.com (2021-04-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-07)

Hi, chelse@ - the VRP Panel has decided to award you $1000 as a thank you for reporting this issue! A member of our finance team will be in touch soon to arrange payment. In the meantime, please let me know whom we should credit (and name/handle to be used) for this issue. Thanks again for reporting it to us and helping us with reproduction!

### [Deleted User] (2021-04-08)

Thank you! Please credit: Chelse Tsai-Simek, Jeanette Ulloa, and Emily Voigtlander of Seesaw.

### am...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### ja...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### as...@google.com (2021-04-22)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1189926?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1194276]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055253)*

# Security: stack-buffer-overflow in views::ScrollView::OnMouseWheel(ui::MouseWheelEvent const&) in the browser process

| Field | Value |
|-------|-------|
| **Issue ID** | [40058181](https://issues.chromium.org/issues/40058181) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Mobile>TabStrip |
| **Platforms** | Mac |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2021-12-09 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

Enable chrome://flags/#scrollable-tabstrip && chrome://flags/#scrollable-tabstrip-buttons  

Two fingers move on the touchpad(Macbook pro) in the omnibox result box will triger the stack-buffer-overflow in views::ScrollView::OnMouseWheel

**VERSION**  

Chrome Version: Version 98.0.4757.0 (Developer Build) (x86\_64 translated)  

Operating System:macOS Monterey Version 12.0.1 Chip Apple M1 Pro

**REPRODUCTION CASE**

download: gs://chromium-browser-asan/mac-release/asan-mac-release-950004.zip

1. Enable the two flags:chrome://flags/#scrollable-tabstrip && chrome://flags/#scrollable-tabstrip-buttons
2. Input some easy words in the omnibox and the chrome will popup the result window.
3. Two fingers move on the touchpad(Macbook pro) in the omnibox result window.
4. It will triger the stack-buffer-overflow

PS:I try to use the mouse to reproduce this issue and it failed. However the touchbar will triger this issue relatively stably

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser.]  

Asan log:  

==3651==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x00030d76f708 at pc 0x00015fd20b68 bp 0x00030d76ee10 sp 0x00030d76ee08  

READ of size 4 at 0x00030d76f708 thread T0

#0 0x15fd20b67 in views::ScrollView::OnMouseWheel(ui::MouseWheelEvent const&) scroll\_view.cc:717  

#1 0x15fd6b9b7 in views::View::OnMouseEvent(ui::MouseEvent\*) view.cc:1457  

#2 0x158ce921e in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:139  

#3 0x158ce8acb in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:55  

#4 0x15fda6aff in views::internal::RootView::OnMouseWheel(ui::MouseWheelEvent const&) root\_view.cc:636  

#5 0x161247be7 in BrowserRootView::OnMouseWheel(ui::MouseWheelEvent const&) browser\_root\_view.cc:296  

#6 0x15fdc30c0 in views::Widget::OnMouseEvent(ui::MouseEvent\*) widget.cc:1578  

#7 0x16160ee39 in non-virtual thunk to RoundedOmniboxResultsFrame::OnMouseEvent(ui::MouseEvent\*) rounded\_omnibox\_results\_frame.cc:283  

#8 0x158ce921e in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:139  

#9 0x158ce8acb in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:55  

#10 0x15fda6aff in views::internal::RootView::OnMouseWheel(ui::MouseWheelEvent const&) root\_view.cc:636  

#11 0x15fdc30c0 in views::Widget::OnMouseEvent(ui::MouseEvent\*) widget.cc:1578  

#12 0x15fdc3d2b in views::Widget::OnScrollEvent(ui::ScrollEvent\*) widget.cc:1605  

#13 0x15fe6c48b in non-virtual thunk to views::NativeWidgetMacNSWindowHost::OnScrollEvent(std::\_\_1::unique\_ptr<ui::Event, std::\_\_1::default\_delete[ui::Event](javascript:void(0);) >) native\_widget\_mac\_ns\_window\_host.mm:845  

#14 0x15c23c95b in -[BridgedContentView scrollWheel:] bridged\_content\_view.mm:828  

#15 0x7ff813cbb27b in -[NSWindow(NSEventRouting) \_reallySendEvent:isDelayedEvent:]+0x1bed (AppKit:x86\_64+0x1b227b)  

#16 0x7ff813cb946d in -[NSWindow(NSEventRouting) sendEvent:]+0x15f (AppKit:x86\_64+0x1b046d)  

#17 0x15c24635d in -[NativeWidgetMacNSWindow sendEvent:] native\_widget\_mac\_nswindow.mm:298  

#18 0x7ff813cb80f3 in -[NSApplication(NSEvent) sendEvent:]+0xa17 (AppKit:x86\_64+0x1af0f3)  

#19 0x1557c599c in \_\_34-[BrowserCrApplication sendEvent:]\_block\_invoke chrome\_browser\_application\_mac.mm:344  

#20 0x156a72259 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xd781259)  

#21 0x1557c49b1 in -[BrowserCrApplication sendEvent:] chrome\_browser\_application\_mac.mm:321  

#22 0x7ff813f7080a in -[NSApplication \_handleEvent:]+0x40 (AppKit:x86\_64+0x46780a)  

#23 0x7ff813b3837d in -[NSApplication run]+0x26e (AppKit:x86\_64+0x2f37d)  

#24 0x156a869ea in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate\*) message\_pump\_mac.mm:743  

#25 0x156a82728 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*) message\_pump\_mac.mm:161  

#26 0x1569a3e96 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread\_controller\_with\_message\_pump\_impl.cc:468  

#27 0x1568d539c in base::RunLoop::Run(base::Location const&) run\_loop.cc:140  

#28 0x14da83576 in content::BrowserMainLoop::RunMainMessageLoop() browser\_main\_loop.cc:1038  

#29 0x14da87bc1 in content::BrowserMainRunnerImpl::Run() browser\_main\_runner\_impl.cc:153  

#30 0x14da7cf85 in content::BrowserMain(content::MainFunctionParams) browser\_main.cc:30  

#31 0x1556182ea in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content\_main\_runner\_impl.cc:646  

#32 0x15561af83 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content\_main\_runner\_impl.cc:1160  

#33 0x15561a1f6 in content::ContentMainRunnerImpl::Run() content\_main\_runner\_impl.cc:1026  

#34 0x1556154b2 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content\_main.cc:398  

#35 0x1556173b1 in content::ContentMain(content::ContentMainParams) content\_main.cc:426  

#36 0x1492f5be4 in ChromeMain chrome\_main.cc:177  

#37 0x1048fcbb5 in main chrome\_exe\_main\_mac.cc:117  

#38 0x204dcc4fd in start+0x1cd (dyld:x86\_64+0x54fd)  

#39 0x204dc6fff (<unknown module>)  

#40 0x1048fbfff (/Users/asnine/fuzz/chromium\_version/asan-mac-release-950004/Chromium.app/Contents/MacOS/Chromium:x86\_64+0xffffffff)

Address 0x00030d76f708 is located in stack of thread T0 at offset 264 in frame  

#0 0x16160ecdf in non-virtual thunk to RoundedOmniboxResultsFrame::OnMouseEvent(ui::MouseEvent\*)+0xf (/Users/asnine/fuzz/chromium\_version/asan-mac-release-950004/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4757.0/Chromium Framework:x86\_64+0x1831dcdf)

This frame has 1 object(s):  

[32, 264) 'pair.i' (line 281) <== Memory access at offset 264 overflows this variable  

HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork  

(longjmp and C++ exceptions \*are\* supported)  

SUMMARY: AddressSanitizer: stack-buffer-overflow (/Users/asnine/fuzz/chromium\_version/asan-mac-release-950004/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4757.0/Chromium Framework:x86\_64+0x16a2fb67) in views::ScrollView::OnMouseWheel(ui::MouseWheelEvent const&)+0x407  

Shadow bytes around the buggy address:  

0x100061aede90: 00 00 00 00 00 00 00 00 00 00 00 00 f1 f1 f1 f1  

0x100061aedea0: f8 f8 f8 f8 f3 f3 f3 f3 00 00 00 00 00 00 00 00  

0x100061aedeb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x100061aedec0: f1 f1 f1 f1 00 00 00 00 00 00 00 00 00 00 00 00  

0x100061aeded0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x100061aedee0: 00[f3]f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 00 00 00 00  

0x100061aedef0: 00 00 00 00 00 00 00 00 00 00 00 00 f1 f1 f1 f1  

0x100061aedf00: f8 f3 f3 f3 00 00 00 00 00 00 00 00 00 00 00 00  

0x100061aedf10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x100061aedf20: f1 f1 f1 f1 00 00 00 00 00 00 f2 f2 f2 f2 f8 f3  

0x100061aedf30: f3 f3 f3 f3 00 00 00 00 00 00 00 00 00 00 00 00  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==3651==ABORTING  

Received signal 6  

[0x000156a4c589]  

[0x0001567f3cb3]  

[0x000156a4c30b]  

[0x7ff811146e2d]  

[0x000134efee00]  

[0x7ff81107dd10]  

[0x00010d347546]  

[0x00010d346cc4]  

[0x00010d32adb7]  

[0x00010d32a04f]  

[0x00010d32b2d8]  

[0x00015fd20b68]  

[0x00015fd6b9b8]  

[0x000158ce921f]  

[0x000158ce8acc]  

[0x00015fda6b00]  

[0x000161247be8]  

[0x00015fdc30c1]  

[0x00016160ee3a]  

[0x000158ce921f]  

[0x000158ce8acc]  

[0x00015fda6b00]  

[0x00015fdc30c1]  

[0x00015fdc3d2c]  

[0x00015fe6c48c]  

[0x00015c23c95c]  

[0x7ff813cbb27c]  

[0x7ff813cb946e]  

[0x00015c24635e]  

[0x7ff813cb80f4]  

[0x0001557c599d]  

[0x000156a7225a]  

[0x0001557c49b2]  

[0x7ff813f7080b]  

[0x7ff813b3837e]  

[0x000156a869eb]  

[0x000156a82729]  

[0x0001569a3e97]  

[0x0001568d539d]  

[0x00014da83577]  

[0x00014da87bc2]  

[0x00014da7cf86]  

[0x0001556182eb]  

[0x00015561af84]  

[0x00015561a1f7]  

[0x0001556154b3]  

[0x0001556173b2]  

[0x0001492f5be5]  

[0x0001048fcbb6]  

[0x000204dcc4fe]  

[0x000204dc7000]  

[0x0001048fc000]  

[end of stack trace]

## Attachments

- [poc.mp4](attachments/poc.mp4) (video/mp4, 7.1 MB)
- [Screen Recording 2022-01-06 at 10.41.49 PM.mov](attachments/Screen Recording 2022-01-06 at 10.41.49 PM.mov) (video/quicktime, 14.1 MB)
- [Screen Shot 2022-01-12 at 3.05.58 PM.png](attachments/Screen Shot 2022-01-12 at 3.05.58 PM.png) (image/png, 36.6 KB)

## Timeline

### [Deleted User] (2021-12-09)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-12-10)

Browser process use after free from a very reasonable chain of user actions. That's critical severity, but in a disabled feature, which means Impact=None for now.

TabStrip folks, can you please look at this?

[Monorail components: UI>Browser>Mobile>TabStrip]

### do...@chromium.org (2021-12-10)

[Empty comment from Monorail migration]

### 0x...@gmail.com (2021-12-12)

It seems that the mouse can also triger this issue in MAC. I use the mouse logitech master 3 with the left & right scroll function.


### do...@chromium.org (2021-12-14)

Owners: can someone please take a look and follow up on this? Especially if this actually can be triggered without needing a flag, that would mark it as P0.

### wf...@chromium.org (2021-12-22)

I agree with the triage here. Can someone from the tab strip team look at this as a matter of urgency? dfried touched this code last, so gets the potato.

### df...@chromium.org (2022-01-06)

This appears to be a Mac-only bug, as it goes through Mac-specific code; if it is not it needs to be updated. (I can't repro on Windows fyi)

I suspect what is happening is that something in the scrolling tabstrip is scooping the event, causing the omnibox to close in the middle of event dispatch, resulting in what is really some sort of bad pointer dereference or UAF but which is showing up as a stack overflow (even though we're not in an infinite recursion or anything).

If this is the case, the behavior of the tabstrip might not even be wrong; I'm going to hand this to the Mac team for triage to see if they can't make more sense of what is going on. The fact that it is touch-only and does not repro on mousewheel suggests that it has something to do with how touchpad events are handled on the platform, but I could be completely wrong.

### df...@chromium.org (2022-01-06)

[Empty comment from Monorail migration]

### av...@chromium.org (2022-01-06)

As much as I want Elly’s past on the Mac team to haunt her forever, she left the Mac team. Unassigning.

This is crashing in MacViews, apparently due to something special about trackpad scrolling? Sending to kerenzhu for a first analysis, but happy to consult/answer questions/take over if it turns out to be a non-View Mac thing.

### ke...@google.com (2022-01-06)

[Empty comment from Monorail migration]

### ke...@google.com (2022-01-07)

I can't reproduce the memory bug reported in c#1. But there're things I didn't expect.

I turned on chrome://flags/#scrollable-tabstrip && chrome://flags/#scrollable-tabstrip-buttons, but the tab strip was not scrollable. I've tried 96.0 stable and 99.0 canary, on windows and mac. None of them worked. 

On the other hand, when I scrolled by moving two figures on touchpad, a DCHECK was triggered on my dev build. 

[67845:259:0106/220757.549686:FATAL:threaded_input_handler.cc(311)] Check failed: scroll_status.main_thread_scrolling_reasons == MainThreadScrollingReason::kNotScrollingOnMain (1024 vs. 0)
0   libbase.dylib                       0x00000001064d542f base::debug::CollectStackTrace(void**, unsigned long) + 31
1   libbase.dylib                       0x00000001061a7d58 base::debug::StackTrace::StackTrace(unsigned long) + 72
2   libbase.dylib                       0x00000001061a7ddd base::debug::StackTrace::StackTrace(unsigned long) + 29
3   libbase.dylib                       0x00000001061a7db5 base::debug::StackTrace::StackTrace() + 37
4   libbase.dylib                       0x0000000106203763 logging::LogMessage::~LogMessage() + 179
5   libbase.dylib                       0x0000000106204705 logging::LogMessage::~LogMessage() + 21
6   libbase.dylib                       0x0000000106204729 logging::LogMessage::~LogMessage() + 25
7   libbase.dylib                       0x000000010616306b logging::CheckError::~CheckError() + 43
8   libbase.dylib                       0x0000000106162b25 logging::CheckError::~CheckError() + 21
9   libcc.dylib                         0x0000000116bd0157 cc::ThreadedInputHandler::ScrollBegin(cc::ScrollState*, ui::ScrollInputType) + 4423
10  libcompositor.dylib                 0x000000012c337128 ui::ScrollInputHandler::OnScrollEvent(ui::ScrollEvent const&, ui::Layer*) + 296
11  libviews.dylib                      0x00000001b88a9f19 views::ScrollView::OnScrollEvent(ui::ScrollEvent*) + 745
12  libevents.dylib                     0x000000010a64fc56 ui::EventHandler::OnEvent(ui::Event*) + 166
13  libevents.dylib                     0x000000010a64c2c2 ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) + 178
14  libevents.dylib                     0x000000010a64b829 ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) + 473
15  libevents.dylib                     0x000000010a64b3ab ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) + 219
16  libevents.dylib                     0x000000010a64b181 ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) + 321
17  libevents.dylib                     0x000000010a650cae ui::EventProcessor::OnEventFromSource(ui::Event*) + 974
18  libevents.dylib                     0x000000010a6510bf non-virtual thunk to ui::EventProcessor::OnEventFromSource(ui::Event*) + 47
19  libevents.dylib                     0x000000010a6530cf ui::EventSource::DeliverEventToSink(ui::Event*) + 175
20  libevents.dylib                     0x000000010a652edd ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) + 573
21  libevents.dylib                     0x000000010a652c3f ui::EventSource::SendEventToSink(ui::Event const*) + 47
22  libviews.dylib                      0x00000001b8a883ce views::Widget::OnScrollEvent(ui::ScrollEvent*) + 126
23  libviews.dylib                      0x00000001b8acb5f6 views::NativeWidgetMacNSWindowHost::OnScrollEvent(std::__1::unique_ptr<ui::Event, std::__1::default_delete<ui::Event> >) + 70
24  libapp_shim.dylib                   0x00000001c91cb93b -[BridgedContentView scrollWheel:] + 283
25  AppKit                              0x00007ff817b63328 -[NSWindow(NSEventRouting) _reallySendEvent:isDelayedEvent:] + 7150
26  AppKit                              0x00007ff817b6151a -[NSWindow(NSEventRouting) sendEvent:] + 352
27  libapp_shim.dylib                   0x00000001c91d7911 -[NativeWidgetMacNSWindow sendEvent:] + 1553
28  AppKit                              0x00007ff817b601a0 -[NSApplication(NSEvent) sendEvent:] + 2584
29  libchrome_dll.dylib                 0x0000000146828abc __34-[BrowserCrApplication sendEvent:]_block_invoke + 716
30  libbase.dylib                       0x000000010650bf82 base::mac::CallWithEHFrame(void () block_pointer) + 10
31  libchrome_dll.dylib                 0x0000000146827ee6 -[BrowserCrApplication sendEvent:] + 806
32  AppKit                              0x00007ff817e1889f -[NSApplication _handleEvent:] + 65
33  AppKit                              0x00007ff8179e05ce -[NSApplication run] + 623
34  libbase.dylib                       0x00000001065272ab base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate*) + 251
35  libbase.dylib                       0x000000010652489a base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*) + 170
36  libbase.dylib                       0x00000001063fa339 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) + 633
37  libbase.dylib                       0x000000010630ecc1 base::RunLoop::Run(base::Location const&) + 769
38  libcontent.dylib                    0x000000019b4608a9 content::BrowserMainLoop::RunMainMessageLoop() + 361
39  libcontent.dylib                    0x000000019b46f68d content::BrowserMainRunnerImpl::Run() + 253
40  libcontent.dylib                    0x000000019b45adf4 content::BrowserMain(content::MainFunctionParams) + 388
41  libcontent.dylib                    0x000000019e012f95 content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) + 453
42  libcontent.dylib                    0x000000019e015282 content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) + 1874
43  libcontent.dylib                    0x000000019e014a3c content::ContentMainRunnerImpl::Run() + 924
44  libcontent.dylib                    0x000000019e010a7a content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) + 890
45  libcontent.dylib                    0x000000019e01172a content::ContentMain(content::ContentMainParams) + 74
46  libchrome_dll.dylib                 0x00000001423bb9a8 ChromeMain + 456
47  Chromium                            0x00000001035c8959 main + 569
48  dyld                                0x00000001060a24fe start + 462
Crash keys:
  "nsevent" = "NSEvent type=22 modifierFlags=0x0 locationInWindow=(192.884,752.198)"
  "ui_scheduler_async_stack" = "0x103D903C3 0x0"
  "extension-2" = "jdifiehgphoohjljmacgppcfnmdehgmf"
  "extension-1" = "felcaaldnbdncclmgdcncolpebgiejap"
  "num-extensions" = "2"
  "switch-3" = "--origin-trial-disabled-features=CaptureHandle"
  "switch-2" = "--enable-features=ScrollableTabStrip,ScrollableTabStripButtons"
  "switch-1" = "--disable-threaded-scrolling"
  "io_scheduler_async_stack" = "0x103D903C3 0x0"
  "num-switches" = "5"
  "osarch" = "x86_64"
  "pid" = "67845"
  "ptype" = "browser"

tbergquist@, do you know why tab scrolling was not working? Am I under a wrong configuration? See attached screen recording.

### 0x...@gmail.com (2022-01-07)

I can reproduce this issue in th latest gs://chromium-browser-asan/mac-release/asan-mac-release-956465.zip version in the macbook pro M1.
And find only the chrome://flags/#scrollable-tabstrip flag is needed.
It is a little hard to reproduce this issue sometimes.
It need enough patience to slide freely on the touchpad with two fingers😅

=================================================================
==22112==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x0003094b1740 at pc 0x00015da4b214 bp 0x0003094b0e50 sp 0x0003094b0e48
READ of size 4 at 0x0003094b1740 thread T0
 #0 0x15da4b213 in views::ScrollView::OnMouseWheel(ui::MouseWheelEvent const&) scroll_view.cc:721
 #1 0x15da96157 in views::View::OnMouseEvent(ui::MouseEvent*) view.cc:1457
 #2 0x156a67062 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) event_dispatcher.cc:139
 #3 0x156a66912 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) event_dispatcher.cc:55
 #4 0x15dad166f in views::internal::RootView::OnMouseWheel(ui::MouseWheelEvent const&) root_view.cc:636
 #5 0x15ef7faa7 in BrowserRootView::OnMouseWheel(ui::MouseWheelEvent const&) browser_root_view.cc:300
 #6 0x15daedc40 in views::Widget::OnMouseEvent(ui::MouseEvent*) widget.cc:1571
 #7 0x15f33f7ec in non-virtual thunk to RoundedOmniboxResultsFrame::OnMouseEvent(ui::MouseEvent*) rounded_omnibox_results_frame.cc:283
 #8 0x156a67062 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) event_dispatcher.cc:139

### tb...@chromium.org (2022-01-07)

The kNotScrollingOnMain thing is likely at least somewhat related to some ScrollView weirdness that I haven't been able to get to the bottom of. See my notes / scratch space here: https://docs.google.com/document/d/1Zf3PSzpwYGUCqfUA8x-5BREWK4LL-NfK2K_sokPqTz8/edit?usp=sharing&resourcekey=0-p5QvTTaDQxA34fnRR75h-g

It's an important thing that needs fixing, but I had to back-burner it because I was just too stuck. If the DCHECK is blocking you, try flipping the #scroll-unification flag and see if that affects it.

### ke...@chromium.org (2022-01-07)

Thanks for the notes. I haven't read it through, but this bug seems to be related to the kUiCompositorScrollWithLayers flag. Right now, only mac uses cc scrolling for ScrollView. 

### tb...@chromium.org (2022-01-07)

Which bug is related to that flag? This buffer overflow or the DCHECK? Or both? Both would make sense.

Just to clarify, the repro for the overflow involves scrolling the omnibox suggestion window, not the tabstrip, but with the #scrollable-tabstrip flag enabled? And the repro for the DCHECK involves scrolling on the tabstrip, but when it doesn't have tabs open enough for scrolling to actually take place?

### ke...@chromium.org (2022-01-10)

re c#15: I suspect that kUiCompositorScrollWithLayers causes both bugs. That's the only difference between mac and other platforms I know that has something to do with scrolling. 

> overflow involves scrolling the omnibox suggestion window, not the tabstrip, but with the #scrollable-tabstrip flag enabled? 
Yes.

> DCHECK involves scrolling on the tabstrip, but when it doesn't have tabs open enough for scrolling to actually take place?
Yes.

I filed a separate bug for the DCHECK, crbug.com/1285895

### ke...@chromium.org (2022-01-12)

0xasnine@ I got the same stack track log as you posted in c#1, not by scrolling on omnibox popup, by scrolling on tab strip. I can reproduce it consistently. 
In your screen recording, the crash happened right after your cursor stayed on the tab strip, so I suspect your reproduce steps were wrong. 

Here's my crash log:

=================================================================
==81087==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ff7b70b9a20 at pc 0x00016017c9d4 bp 0x7ff7b70b9130 sp 0x7ff7b70b9128
READ of size 4 at 0x7ff7b70b9a20 thread T0

    #0 0x16017c9d3 in views::ScrollView::OnMouseWheel(ui::MouseWheelEvent const&) scroll_view.cc:721
    #1 0x1601c7717 in views::View::OnMouseEvent(ui::MouseEvent*) view.cc:1457
    #2 0x159137692 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) event_dispatcher.cc:139
    #3 0x159136f42 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) event_dispatcher.cc:55
    #4 0x16020283f in views::internal::RootView::OnMouseWheel(ui::MouseWheelEvent const&) root_view.cc:636
    #5 0x1616b6917 in BrowserRootView::OnMouseWheel(ui::MouseWheelEvent const&) browser_root_view.cc:300
    #6 0x16021ee10 in views::Widget::OnMouseEvent(ui::MouseEvent*) widget.cc:1571
    #7 0x161a752dc in non-virtual thunk to RoundedOmniboxResultsFrame::OnMouseEvent(ui::MouseEvent*) rounded_omnibox_results_frame.cc:283
    #8 0x159137692 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) event_dispatcher.cc:139
    #9 0x159136f42 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) event_dispatcher.cc:55
    #10 0x16020283f in views::internal::RootView::OnMouseWheel(ui::MouseWheelEvent const&) root_view.cc:636
    #11 0x16021ee10 in views::Widget::OnMouseEvent(ui::MouseEvent*) widget.cc:1571
    #12 0x16021fa87 in views::Widget::OnScrollEvent(ui::ScrollEvent*) widget.cc:1598
/* The rest frames are the same as c#1, omit them here */

Address 0x7ff7b70b9a20 is located in stack of thread T0 at offset 256 in frame
    #0 0x161a7518f in non-virtual thunk to RoundedOmniboxResultsFrame::OnMouseEvent(ui::MouseEvent*) rounded_omnibox_results_frame.cc

  This frame has 1 object(s):
    [32, 256) 'pair.i' (line 281) <== Memory access at offset 256 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow scroll_view.cc:721 in views::ScrollView::OnMouseWheel(ui::MouseWheelEvent const&)
Shadow bytes around the buggy address:
  0x1ffef6e172f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1ffef6e17300: f1 f1 f1 f1 f8 f8 f8 f8 f3 f3 f3 f3 00 00 00 00
  0x1ffef6e17310: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1ffef6e17320: 00 00 00 00 f1 f1 f1 f1 00 00 00 00 00 00 00 00
  0x1ffef6e17330: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x1ffef6e17340: 00 00 00 00[f3]f3 f3 f3 f3 f3 f3 f3 00 00 00 00
  0x1ffef6e17350: 00 00 00 00 00 00 00 00 00 00 00 00 f1 f1 f1 f1
  0x1ffef6e17360: f8 f3 f3 f3 00 00 00 00 00 00 00 00 00 00 00 00
  0x1ffef6e17370: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1ffef6e17380: f1 f1 f1 f1 00 00 00 00 00 00 f2 f2 f2 f2 f8 f3
  0x1ffef6e17390: f3 f3 f3 f3 00 00 00 00 00 00 00 00 00 00 00 00

### ke...@chromium.org (2022-01-12)

I missed a critical detail in the reproduce steps, the REAL reproduce steps are:

1. Turn on #scrollable-tabstrip flag.
2. Type something in omnibox, so that the omnibox suggestion popup shows up.
3. Omnibox popup has a faint shadow over tab strip. Scroll on the tab strip WITHIN the omnibox shadow.

### ke...@chromium.org (2022-01-12)

OK I think I've found the root cause. A MouseEvent* is casted to a MouseWheelEvent*, but the instance under the hood is a MouseEvent. 

The MouseEvent is defined here on stack, https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/omnibox/rounded_omnibox_results_frame.cc;drc=0e45c020c43b1a9f6d2870ff7f92b30a2f03a458;l=281. 

The casting is in widget.cc, https://source.chromium.org/chromium/chromium/src/+/main:ui/views/widget/widget.cc;drc=56d5a0912735ab5609e2f5e360583910bd47fad9;l=1572

The reading of MouseWheelEvent is at the bottom of stack, https://source.chromium.org/chromium/chromium/src/+/main:ui/views/controls/scroll_view.cc;drc=bff7fcba732aa420926466bf53dbd1d9504ba22f;l=721. Note that `offset` is a member of MouseWheelEvent but not MouseEvent. This is a read violation. 

avi@, we should banned copy constructor of ui::Event. It's a source of wrong downcasting, WDYT? As a rule of thumb, always use Event::Clone().

### av...@chromium.org (2022-01-12)

I would be happy to =delete the copy constructor if it causes issues like this.

### av...@chromium.org (2022-01-12)

Going further:

The copy constructor is dangerous for a subclassed type like this because of slicing, which leads to the failure you found. The copy constructor is already protected, but apparently that was not enough protection. I hope that =deleting the copy constructor will lead to the code that is doing the improper copying (which is yielding a ui::ET_MOUSEWHEEL event type that’s not from a ui::MouseWheelEvent).

### ke...@chromium.org (2022-01-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3b0c8fbb83567082d332b6f94921608870c48291

commit 3b0c8fbb83567082d332b6f94921608870c48291
Author: Keren Zhu <kerenzhu@chromium.org>
Date: Thu Jan 13 02:17:28 2022

Fix stack overflow in scrollable tab strip

A MouseWheelEvent is sliced into a MouseEvent and later down-casted back
to a MouseWheelEvent*, resulting in a memory access violation. This CL
fixes the issue.

Bug: 1278375
Change-Id: I768b886c48045c963537d3ef828ba0e87202c7ad
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3383692
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Keren Zhu <kerenzhu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#958403}

[modify] https://crrev.com/3b0c8fbb83567082d332b6f94921608870c48291/chrome/browser/ui/views/omnibox/rounded_omnibox_results_frame.cc


### ke...@chromium.org (2022-01-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-20)

Based on further analysis, the exploitation potential and attacker control appears to be quite minimal and this seems like an ASLR bypass; adjusting severity accordingly 

### am...@google.com (2022-01-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-20)

Congratulations - the VRP Panel has decided to award you $3000 for this report. Thank you for this report and your efforts! 

### am...@google.com (2022-01-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-04-22)

This issue was migrated from crbug.com/chromium/1278375?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/1286893, crbug.com/chromium/873923]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058181)*

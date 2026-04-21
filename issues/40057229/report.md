# Security: heap-use-after-free in app_controller_mac.mm

| Field | Value |
|-------|-------|
| **Issue ID** | [40057229](https://issues.chromium.org/issues/40057229) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Incognito |
| **Platforms** | Mac |
| **Reporter** | me...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2021-09-11 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36

Steps to reproduce the problem:
1. download asan-mac-release-920191.zip and unzip
2. start a web server in the folder of poc.html
3. ./Chromium --incognito http://127.0.0.1:8605/poc.html
4. after poc.hmlt is closed, click the icon of Chromium in dock

What is the expected behavior?

What went wrong?
Here is an UAF in app_controller_mac.mm

=================================================================
==4888==ERROR: AddressSanitizer: heap-use-after-free on address 0x6110001a2240 at pc 0x00011846b4c8 bp 0x0003088bc2d0 sp 0x0003088bc2c8
READ of size 8 at 0x6110001a2240 thread T0
    #0 0x11846b4c7 in -[AppController applicationShouldHandleReopen:hasVisibleWindows:] app_controller_mac.mm:1461
    #1 0x7fff22d97a7b in -[NSApplication(NSAppleEventHandling) _handleAEReopen:]+0x108 (AppKit:x86_64+0x207a7b)
    #2 0x7fff22bd4f86 in -[NSApplication(NSAppleEventHandling) _handleCoreEvent:withReplyEvent:]+0x298 (AppKit:x86_64+0x44f86)
    #3 0x7fff2112c305 in -[NSAppleEventManager dispatchRawAppleEvent:withRawReply:handlerRefCon:]+0x133 (Foundation:x86_64+0x35305)
    #4 0x7fff2112c175 in _NSAppleEventManagerGenericHandler+0x4f (Foundation:x86_64+0x35175)
    #5 0x7fff261dc7f2  (AE:x86_64+0xc7f2)
    #6 0x7fff261dbf0d  (AE:x86_64+0xbf0d)
    #7 0x7fff261d4c22 in aeProcessAppleEvent+0x1bf (AE:x86_64+0x4c22)
    #8 0x7fff289578a1 in AEProcessAppleEvent+0x35 (HIToolbox:x86_64+0x428a1)
    #9 0x7fff22bcf60f in _DPSNextEvent+0x7fd (AppKit:x86_64+0x3f60f)
    #10 0x7fff22bcd944 in -[NSApplication(NSEvent) _nextEventMatchingEventMask:untilDate:inMode:dequeue:]+0x553 (AppKit:x86_64+0x3d944)
    #11 0x118479ba2 in __71-[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]_block_invoke chrome_browser_application_mac.mm:237
    #12 0x1196b34c9 in base::mac::CallWithEHFrame(void () block_pointer)+0x9 (Chromium Framework:x86_64+0xd3b34c9)
    #13 0x11847974d in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:] chrome_browser_application_mac.mm:236
    #14 0x7fff22bbfc68 in -[NSApplication run]+0x249 (AppKit:x86_64+0x2fc68)
    #15 0x1196c7fda in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate*) message_pump_mac.mm:739
    #16 0x1196c3d58 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*) message_pump_mac.mm:157
    #17 0x1195e7903 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread_controller_with_message_pump_impl.cc:467
    #18 0x119522168 in base::RunLoop::Run(base::Location const&) run_loop.cc:134
    #19 0x110a43b63 in content::BrowserMainLoop::RunMainMessageLoop() browser_main_loop.cc:988
    #20 0x110a480d1 in content::BrowserMainRunnerImpl::Run() browser_main_runner_impl.cc:152
    #21 0x110a3d5cc in content::BrowserMain(content::MainFunctionParams const&) browser_main.cc:49
    #22 0x1182c1eda in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content_main_runner_impl.cc:1104
    #23 0x1182c0fc5 in content::ContentMainRunnerImpl::Run(bool) content_main_runner_impl.cc:971
    #24 0x1182bce30 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content_main.cc:390
    #25 0x1182becfa in content::ContentMain(content::ContentMainParams const&) content_main.cc:418
    #26 0x10c304ba4 in ChromeMain chrome_main.cc:172
    #27 0x102231bff in main chrome_exe_main_mac.cc:115
    #28 0x7fff203c1f3c in start+0x0 (libdyld.dylib:x86_64+0x15f3c)

0x6110001a2240 is located 0 bytes inside of 248-byte region [0x6110001a2240,0x6110001a2338)
freed by thread T0 here:
    #0 0x10a9dd8b9  (libclang_rt.asan_osx_dynamic.dylib:x86_64+0x478b9)
    #1 0x118a4c69e in std::__1::__tree<std::__1::__value_type<Profile::OTRProfileID, std::__1::unique_ptr<Profile, std::__1::default_delete<Profile> > >, std::__1::__map_value_compare<Profile::OTRProfileID, std::__1::__value_type<Profile::OTRProfileID, std::__1::unique_ptr<Profile, std::__1::default_delete<Profile> > >, std::__1::less<Profile::OTRProfileID>, true>, std::__1::allocator<std::__1::__value_type<Profile::OTRProfileID, std::__1::unique_ptr<Profile, std::__1::default_delete<Profile> > > > >::erase(std::__1::__tree_const_iterator<std::__1::__value_type<Profile::OTRProfileID, std::__1::unique_ptr<Profile, std::__1::default_delete<Profile> > >, std::__1::__tree_node<std::__1::__value_type<Profile::OTRProfileID, std::__1::unique_ptr<Profile, std::__1::default_delete<Profile> > >, void*>*, long>) __tree:2422
    #2 0x118a46c19 in ProfileImpl::DestroyOffTheRecordProfile(Profile*) profile_impl.cc:1043
    #3 0x118a03f46 in ProfileDestroyer::DestroyOffTheRecordProfileNow(Profile*) profile_destroyer.cc:98
    #4 0x118a01961 in ProfileDestroyer::DestroyProfileWhenAppropriate(Profile*) profile_destroyer.cc:70
    #5 0x1232379ca in Browser::~Browser() browser.cc:641
    #6 0x123238b2d in Browser::~Browser() browser.cc:562
    #7 0x123c0d04e in BrowserView::~BrowserView() browser_view.cc:769
    #8 0x123c0d697 in non-virtual thunk to BrowserView::~BrowserView() browser_view.cc:734
    #9 0x1227480a0 in views::View::~View() view.cc:242
    #10 0x123a8341d in BrowserNonClientFrameViewMac::~BrowserNonClientFrameViewMac() browser_non_client_frame_view_mac.mm:101
    #11 0x122842b42 in views::NonClientView::~NonClientView() non_client_view.cc:164
    #12 0x12274bc96 in views::View::DoRemoveChildView(views::View*, bool, bool, views::View*) view.cc:2623
    #13 0x12274c11a in views::View::RemoveAllChildViews() view.cc:317
    #14 0x1227a5e0d in views::Widget::~Widget() widget.cc:208
    #15 0x123a8813d in BrowserFrame::~BrowserFrame() browser_frame.cc:86
    #16 0x122885b1d in views::NativeWidgetMac::~NativeWidgetMac() native_widget_mac.mm:125
    #17 0x122f97b09 in BrowserFrameMac::~BrowserFrameMac() browser_frame_mac.mm:111
    #18 0x11ed7f83a in -[ViewsNSWindowDelegate windowWillClose:] views_nswindow_delegate.mm:181
    #19 0x7fff20494d08 in __CFNOTIFICATIONCENTER_IS_CALLING_OUT_TO_AN_OBSERVER__+0xb (CoreFoundation:x86_64+0x76d08)
    #20 0x7fff205306f7 in ___CFXRegistrationPost_block_invoke+0x30 (CoreFoundation:x86_64+0x1126f7)
    #21 0x7fff20530674 in _CFXRegistrationPost+0x1c5 (CoreFoundation:x86_64+0x112674)
    #22 0x7fff20465fb3 in _CFXNotificationPost+0x31a (CoreFoundation:x86_64+0x47fb3)
    #23 0x7fff21100bb7 in -[NSNotificationCenter postNotificationName:object:userInfo:]+0x3a (Foundation:x86_64+0x9bb7)
    #24 0x7fff23483bea in -[NSWindow _finishClosingWindow]+0x7b (AppKit:x86_64+0x8f3bea)
    #25 0x7fff22f1332f in -[NSWindow _close]+0x15a (AppKit:x86_64+0x38332f)
    #26 0x11c8ee0d0 in base::internal::Invoker<base::internal::BindState<base::ScopedTypeRef<void () block_pointer, base::mac::internal::ScopedBlockTraits<void () block_pointer> > >, void ()>::RunOnce(base::internal::BindStateBase*) bind_internal.h:690
    #27 0x1195abbec in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) task_annotator.cc:178
    #28 0x1195e67f0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) thread_controller_with_message_pump_impl.cc:360
    #29 0x1195e5f47 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread_controller_with_message_pump_impl.cc:260

previously allocated by thread T0 here:
    #0 0x10a9dd770  (libclang_rt.asan_osx_dynamic.dylib:x86_64+0x47770)
    #1 0x10c3024e7 in operator new(unsigned long) new.cpp:67
    #2 0x118a3aa49 in Profile::CreateOffTheRecordProfile(Profile*, Profile::OTRProfileID const&) off_the_record_profile_impl.cc:638
    #3 0x118a464a0 in ProfileImpl::GetOffTheRecordProfile(Profile::OTRProfileID const&, bool) profile_impl.cc:1022
    #4 0x1135a985b in Profile::GetPrimaryOTRProfile(bool) profile.cc:506
    #5 0x12339b548 in StartupBrowserCreator::GetPrivateProfileIfRequested(base::CommandLine const&, Profile*) startup_browser_creator.cc
    #6 0x12339a02a in StartupBrowserCreator::ProcessCmdLineImpl(base::CommandLine const&, base::FilePath const&, bool, Profile*, std::__1::vector<Profile*, std::__1::allocator<Profile*> > const&) startup_browser_creator.cc:899
    #7 0x123399c19 in StartupBrowserCreator::Start(base::CommandLine const&, base::FilePath const&, Profile*, std::__1::vector<Profile*, std::__1::allocator<Profile*> > const&) startup_browser_creator.cc:570
    #8 0x1184b17b6 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() chrome_browser_main.cc:1691
    #9 0x1184afc2d in ChromeBrowserMainParts::PreMainMessageLoopRun() chrome_browser_main.cc:1075
    #10 0x110a41661 in content::BrowserMainLoop::PreMainMessageLoopRun() browser_main_loop.cc:938
    #11 0x111bb14e4 in content::StartupTaskRunner::RunAllTasksNow() startup_task_runner.cc:41
    #12 0x110a40c02 in content::BrowserMainLoop::CreateStartupTasks() browser_main_loop.cc:846
    #13 0x110a4780d in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams const&) browser_main_runner_impl.cc:131
    #14 0x110a3d591 in content::BrowserMain(content::MainFunctionParams const&) browser_main.cc:45
    #15 0x1182c1eda in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content_main_runner_impl.cc:1104
    #16 0x1182c0fc5 in content::ContentMainRunnerImpl::Run(bool) content_main_runner_impl.cc:971
    #17 0x1182bce30 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content_main.cc:390
    #18 0x1182becfa in content::ContentMain(content::ContentMainParams const&) content_main.cc:418
    #19 0x10c304ba4 in ChromeMain chrome_main.cc:172
    #20 0x102231bff in main chrome_exe_main_mac.cc:115
    #21 0x7fff203c1f3c in start+0x0 (libdyld.dylib:x86_64+0x15f3c)

SUMMARY: AddressSanitizer: heap-use-after-free app_controller_mac.mm:1461 in -[AppController applicationShouldHandleReopen:hasVisibleWindows:]
Shadow bytes around the buggy address:
  0x1c22000343f0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x1c2200034400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c2200034410: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c2200034420: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc
  0x1c2200034430: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc
=>0x1c2200034440: fa fa fa fa fa fa fa fa[fd]fd fd fd fd fd fd fd
  0x1c2200034450: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c2200034460: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x1c2200034470: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c2200034480: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x1c2200034490: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==4888==ABORTING
Received signal 6
 [0x00011968dd09]
 [0x00011943f833]
 [0x00011968da8b]
 [0x7fff203ebd7d]
 [0x3a656c69666f7250]
 [0x7fff202fb406]
 [0x00010aa01356]
 [0x00010aa00a84]
 [0x00010a9e59f7]
 [0x00010a9e4c97]
 [0x00010a9e5fa8]
 [0x00011846b4c8]
 [0x7fff22d97a7c]
 [0x7fff22bd4f87]
 [0x7fff2112c306]
 [0x7fff2112c176]
 [0x7fff261dc7f3]
 [0x7fff261dbf0e]
 [0x7fff261d4c23]
 [0x7fff289578a2]
 [0x7fff22bcf610]
 [0x7fff22bcd945]
 [0x000118479ba3]
 [0x0001196b34ca]
 [0x00011847974e]
 [0x7fff22bbfc69]
 [0x0001196c7fdb]
 [0x0001196c3d59]
 [0x0001195e7904]
 [0x000119522169]
 [0x000110a43b64]
 [0x000110a480d2]
 [0x000110a3d5cd]
 [0x0001182c1edb]
 [0x0001182c0fc6]
 [0x0001182bce31]
 [0x0001182becfb]
 [0x00010c304ba5]
 [0x000102231c00]
 [0x7fff203c1f3d]
 [0x000000000003]
[end of stack trace]

Did this work before? N/A 

Chrome version: 93.0.4577.63  Channel: stable
OS Version: OS X 10.15.7

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 172 B)

## Timeline

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### ad...@google.com (2021-09-12)

Reproduced exactly as described.

Security severity: browser process UaF => critical. Mitigated to high by the need for user interaction/inability of web pages to close themselves in normal circumstances.

rhalavati@, please will you route this to the best person?

(I will now figure out the correct FoundIn label by trying to reproduce on older versions).

[Monorail components: UI>Browser>Incognito]

### ad...@google.com (2021-09-12)

Does not reproduce with 881922.

### ad...@google.com (2021-09-12)

Does reproduce with 903649.

There's an annoying gap in ASAN builds so I'll have to see if I can build my own to figure out whether this impacts the current stable branch.

### [Deleted User] (2021-09-12)

[Empty comment from Monorail migration]

### ad...@google.com (2021-09-12)

Yep. I got the same when I built my own Mac ASAN debug against r902210, which is 93 branch point.

### [Deleted User] (2021-09-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-12)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rh...@chromium.org (2021-09-14)

droger@,

I don't have a Mac device (and any experience with it). Do you have the bandwidth to take a look?

### dr...@chromium.org (2021-09-14)

Sure, I will try to repro.

### dr...@chromium.org (2021-09-14)

I can repro the bug on ToT.

Right clicking on the Dock icon instead of left-clicking also crashes, with a different stack, but it's probably the same root cause.


### dr...@chromium.org (2021-09-14)

I found the root cause. It seems the bug only happens if the experiment UpdateHistoryEntryPointsInIncognito is enabled, which seems to be currently at 1% stable.
We may want to disable this experiment on Mac (although the volume of crashes is probably very low).

### dr...@chromium.org (2021-09-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bc872c1dbed0bfddf48b4a58b1399121eec4fd16

commit bc872c1dbed0bfddf48b4a58b1399121eec4fd16
Author: David Roger <droger@chromium.org>
Date: Thu Sep 16 13:42:33 2021

[Mac] Fix UAF after closing incognito profile created from command line

In its constructor, AppControllerProfileObserver was not observing
pre-existing incognito profiles.
Only profiles created after the AppControllerProfileObserver were
observed correctly.

This bug only happens if the experiment
UpdateHistoryEntryPointsInIncognito is enabled.

The CL also adds a test, and performs some cleanup by merging
ProfileDestructionWaiter and ProfileDestroyedData.

Fixed: 1248661
Change-Id: I3f0c115154cf3086c2dd971b6c36ab5747394540
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3160211
Commit-Queue: David Roger <droger@chromium.org>
Reviewed-by: Side YILMAZ <sideyilmaz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#922114}

[modify] https://crrev.com/bc872c1dbed0bfddf48b4a58b1399121eec4fd16/chrome/browser/app_controller_mac.mm
[modify] https://crrev.com/bc872c1dbed0bfddf48b4a58b1399121eec4fd16/chrome/browser/app_controller_mac_browsertest.mm
[modify] https://crrev.com/bc872c1dbed0bfddf48b4a58b1399121eec4fd16/chrome/browser/profiles/profile_manager.h


### dr...@chromium.org (2021-09-16)

Requesting merge to M-95 for this stability fix, although I am not 100% sure we want it, I will let TPM weigh on this.

Note that:
- this is not a regression, as the crash was already existing in M94 at least (and probably before)
- it only happens with the UpdateHistoryEntryPointsInIncognito experiment is enabled (which is enabled at 1% on stable). We can fix the crash by disabling this experiment, but cherry picking the fix would unblock that experiment.
- the merge is not clean, but the conflict can be fixed manually without too much risk (here's a CL with the conflict markers: https://chromium-review.googlesource.com/c/chromium/src/+/3165236)

### [Deleted User] (2021-09-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-17)

Your change meets the bar and is auto-approved for M95. Please go ahead and merge the CL to branch 4638 (refs/branch-heads/4638) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), harrysouders@(iOS), None@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-09-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/45d44b48832dcee034def070e1a4f35e7b2c51b4

commit 45d44b48832dcee034def070e1a4f35e7b2c51b4
Author: David Roger <droger@chromium.org>
Date: Fri Sep 17 18:58:13 2021

[Mac] Fix UAF after closing incognito profile created from command line

In its constructor, AppControllerProfileObserver was not observing
pre-existing incognito profiles.
Only profiles created after the AppControllerProfileObserver were
observed correctly.

This bug only happens if the experiment
UpdateHistoryEntryPointsInIncognito is enabled.

The CL also adds a test, and performs some cleanup by merging
ProfileDestructionWaiter and ProfileDestroyedData.

(cherry picked from commit bc872c1dbed0bfddf48b4a58b1399121eec4fd16)

Fixed: 1248661
Change-Id: I3f0c115154cf3086c2dd971b6c36ab5747394540
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3160211
Commit-Queue: David Roger <droger@chromium.org>
Reviewed-by: Side YILMAZ <sideyilmaz@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#922114}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3165236
Commit-Queue: Side YILMAZ <sideyilmaz@chromium.org>
Auto-Submit: David Roger <droger@chromium.org>
Cr-Commit-Position: refs/branch-heads/4638@{#117}
Cr-Branched-From: 159257cab5585bc8421abf347984bb32fdfe9eb9-refs/heads/main@{#920003}

[modify] https://crrev.com/45d44b48832dcee034def070e1a4f35e7b2c51b4/chrome/browser/app_controller_mac.mm
[modify] https://crrev.com/45d44b48832dcee034def070e1a4f35e7b2c51b4/chrome/browser/app_controller_mac_browsertest.mm
[modify] https://crrev.com/45d44b48832dcee034def070e1a4f35e7b2c51b4/chrome/browser/profiles/profile_manager.h


### am...@google.com (2021-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-30)

Congratulations on another one! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts and nice finding! 

### me...@gmail.com (2021-09-30)

Thank you:)

### am...@google.com (2021-10-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-19)

[Empty comment from Monorail migration]

### rz...@google.com (2021-10-20)

[Empty comment from Monorail migration]

### rz...@google.com (2021-10-20)

Labelled as not applicable for M90 as it affects only Mac 

### am...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1248661?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1248929]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057229)*

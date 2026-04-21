# Security: Heap-use-after-free in lens::OpenLensRegionSearchInstructions

| Field | Value |
|-------|-------|
| **Issue ID** | [40075359](https://issues.chromium.org/issues/40075359) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>SearchSidePanel |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ju...@google.com |
| **Created** | 2023-10-21 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: 120.0.6079.0 (Official Build) canary (64-bit) (cohort: Clang-64)  

Operating System: windows 11

**REPRODUCTION CASE**

1. Open two chrome windows
2. On each window open Google Search Side Panel and try to seach by "Select any page area" option.
3. Move one window to the other
4. Try again to seach by "Select any page area" option

rax=0000c9dcfaed2ea7 rbx=00005acc06163100 rcx=efefefefefefefef  

rdx=00000076841fd0c8 rsi=00005acc0018c700 rdi=00000076841fd0c8  

rip=00007ffaceef0bc8 rsp=00000076841fd000 rbp=0000000000000000  

r8=00000076841fd0d0 r9=0000000000000030 r10=00000fff5a612c34  

r11=0010000000000000 r12=00005acc096fea00 r13=aaaaaaaaaaaaaaab  

r14=fffffffc00000000 r15=00005acc00000000  

iopl=0 nv up ei ng nz na pe nc  

cs=0033 ss=0000 ds=0000 es=0000 fs=0053 gs=002b efl=00010282  

chrome!BrowserView::GetBrowserViewForBrowser+0x18:  

00007ffa`ceef0bc8 488b01 mov rax,qword ptr [rcx] ds:efefefef`efefefef=????????????????  

0:000> k  

\*\*\* Stack trace for last set context - .thread/.cxr resets it

# Child-SP RetAddr Call Site

00 00000076`841fd000 00007ffa`d8839013 chrome!BrowserView::GetBrowserViewForBrowser+0x18 [C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser\_view.cc @ 1136]  

01 00000076`841fd030 00007ffa`d8825fbb chrome!lens::OpenLensRegionSearchInstructions+0x23 [C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\lens\lens\_side\_panel\_helper.cc @ 54]  

02 00000076`841fd0a0 00007ffa`d7d385ac chrome!lens::LensRegionSearchController::Start+0x1cb [C:\b\s\w\ir\cache\builder\src\chrome\browser\lens\region\_search\lens\_region\_search\_controller.cc @ 71]  

03 00000076`841fd120 00007ffa`d7b7308d chrome!companion::CompanionTabHelper::StartRegionSearch+0x6c [C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\side\_panel\companion\companion\_tab\_helper.cc @ 202]  

04 00000076`841fd180 00007ffa`d65907e0 chrome!companion::CompanionPageHandler::OnRegionSearchClicked+0x5d [C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\webui\side\_panel\companion\companion\_page\_handler.cc @ 385]  

05 00000076`841fd1e0 00007ffa`d3a2f02c chrome!side\_panel::mojom::CompanionPageHandlerStubDispatch::Accept+0x90 [C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\chrome\browser\companion\core\mojom\companion.mojom.cc @ 1343]  

06 (Inline Function) --------`-------- chrome!mojo::InterfaceEndpointClient::HandleValidatedMessage+0xac2 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 1016] 07 00000076`841fd2d0 00007ffa`d39518ad chrome!mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept+0xafc [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 363] 08 (Inline Function) --------`-------- chrome!mojo::MessageDispatcher::Accept+0x28b [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc @ 43]  

09 (Inline Function) --------`-------- chrome!mojo::InterfaceEndpointClient::HandleIncomingMessage+0x314 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 701] 0a (Inline Function) --------`-------- chrome!mojo::internal::MultiplexRouter::ProcessIncomingMessage+0x682 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc @ 1095]  

0b 00000076`841fd4b0 00007ffa`d36ee92a chrome!mojo::internal::MultiplexRouter::Accept+0x92d [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc @ 708]  

0c 00000076`841fd8a0 00007ffa`d6c8b475 chrome!mojo::MessageDispatcher::Accept+0x29a [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc @ 43]  

0d (Inline Function) --------`-------- chrome!mojo::Connector::DispatchMessageW+0x1ce [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc @ 560] 0e (Inline Function) --------`-------- chrome!mojo::Connector::ReadAllAvailableMessages+0x418 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc @ 618]  

0f (Inline Function) --------`-------- chrome!mojo::Connector::OnHandleReadyInternal+0x420 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc @ 451] 10 (Inline Function) --------`-------- chrome!mojo::Connector::OnWatcherHandleReady+0x42d [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc @ 417]  

11 (Inline Function) --------`-------- chrome!base::internal::FunctorTraits<void (mojo::Connector::\*)(const char \*, unsigned int),void>::Invoke+0x43d [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 713] 12 (Inline Function) --------`-------- chrome!base::internal::InvokeHelper<0,void,0,1>::MakeItSo+0x45b [C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h @ 868]  

13 (Inline Function) --------`-------- chrome!base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(const char \*, unsigned int),base::internal::UnretainedWrapper<mojo::Connector,base::unretained_traits::MayNotDangle,0>,base::internal::UnretainedWrapper<const char,base::unretained_traits::MayNotDangle,0> >,void (unsigned int)>::RunImpl+0x45b [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 968] 14 00000076`841fd9a0 00007ffa`d412b9e5 chrome!base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(const char \*, unsigned int),base::internal::UnretainedWrapper<mojo::Connector,base::unretained_traits::MayNotDangle,0>,base::internal::UnretainedWrapper<const char,base::unretained_traits::MayNotDangle,0> >,void (unsigned int)>::Run+0x495 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 932] 15 (Inline Function) --------`-------- chrome!base::RepeatingCallback<void (unsigned int)>::Run+0x2c [C:\b\s\w\ir\cache\builder\src\base\functional\callback.h @ 337]  

16 (Inline Function) --------`-------- chrome!mojo::SimpleWatcher::DiscardReadyState+0x2c [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.h @ 192] 17 (Inline Function) --------`-------- chrome!base::internal::FunctorTraits<void (\*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),void>::Invoke+0x40 [C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h @ 631]  

18 (Inline Function) --------`-------- chrome!base::internal::InvokeHelper<0,void,0>::MakeItSo+0x40 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 868] 19 (Inline Function) --------`-------- chrome!base::internal::Invoker<base::internal::BindState<void (\*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::RunImpl+0x40 [C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h @ 968]  

1a 00000076`841fdbb0 00007ffa`d1d35bc8 chrome!base::internal::Invoker<base::internal::BindState<void (\*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run+0x45 [C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h @ 932]  

1b (Inline Function) --------`-------- chrome!base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run+0x2e [C:\b\s\w\ir\cache\builder\src\base\functional\callback.h @ 337] 1c 00000076`841fdbe0 00007ffa`d32bf825 chrome!mojo::SimpleWatcher::OnHandleReady+0x168 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc @ 278] 1d (Inline Function) --------`-------- chrome!base::internal::FunctorTraits<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &),void>::Invoke+0x2a [C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h @ 713]  

1e (Inline Function) --------`-------- chrome!base::internal::InvokeHelper<1,void,0,1,2,3>::MakeItSo+0x56 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 896] 1f (Inline Function) --------`-------- chrome!base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);),int,unsigned int,mojo::HandleSignalsState>,void ()>::RunImpl+0x56 [C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h @ 968]  

20 (Inline Function) --------`-------- chrome!base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState>,void ()>::RunOnce+0x56 [C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h @ 919] 21 (Inline Function) --------`-------- chrome!base::OnceCallback<void ()>::Run+0x1a0c [C:\b\s\w\ir\cache\builder\src\base\functional\callback.h @ 154]  

22 (Inline Function) --------`-------- chrome!base::TaskAnnotator::RunTaskImpl+0x1b06 [C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc @ 201] 23 (Inline Function) --------`-------- chrome!base::TaskAnnotator::RunTask+0x21d1 [C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.h @ 89]  

24 (Inline Function) --------`-------- chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x26b6 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 461] 25 00000076`841fdd00 00007ffa`d2f2e14b chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x27b5 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 326] 26 00000076`841fe610 00007ffa`cea810f9 chrome!base::MessagePumpForUI::DoRunLoop+0xdfb [C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc @ 213] 27 00000076`841fe7f0 00007ffa`cf35cefa chrome!base::MessagePumpWin::Run+0x79 [C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc @ 79] 28 00000076`841fe850 00007ffa`cf36e59e chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x1aa [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 629] 29 00000076`841fe900 00007ffa`cffab37b chrome!base::RunLoop::Run+0x1ce [C:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 136] 2a 00000076`841fea40 00007ffa`cffaafda chrome!content::BrowserMainLoop::RunMainMessageLoop+0x13b [C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc @ 1088] 2b (Inline Function) --------`-------- chrome!content::BrowserMainRunnerImpl::Run+0xc [C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc @ 158]  

2c 00000076`841feab0 00007ffa`cffa9dac chrome!content::BrowserMain+0x16a [C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc @ 34]  

2d (Inline Function) --------`-------- chrome!content::RunBrowserProcessMain+0x113 [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 707] 2e 00000076`841feb80 00007ffa`cf741e94 chrome!content::ContentMainRunnerImpl::RunBrowser+0x76c [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 1298] 2f 00000076`841fedb0 00007ffa`cf74134c chrome!content::ContentMainRunnerImpl::Run+0x3c4 [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 1142] 30 (Inline Function) --------`-------- chrome!content::RunContentProcess+0x498 [C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc @ 334]  

31 00000076`841fef30 00007ffa`cf73f092 chrome!content::ContentMain+0x50c [C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc @ 347]  

32 00000076`841ff160 00007ff6`6761716a chrome!ChromeMain+0x282 [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc @ 192]  

33 00000076`841ff410 00007ff6`676162b7 chrome\_exe!MainDllLoader::Launch+0x35a [C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc @ 169]  

34 00000076`841ff6a0 00007ff6`676bf1c2 chrome\_exe!wWinMain+0x647 [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc @ 390]  

35 (Inline Function) --------`-------- chrome_exe!invoke_main+0x21 [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 118] 36 00000076`841ffae0 00007ffb`635a257d chrome_exe!__scrt_common_main_seh+0x106 [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288] 37 00000076`841ffb20 00007ffb`64c4aa78 KERNEL32!BaseThreadInitThunk+0x1d 38 00000076`841ffb50 00000000`00000000 ntdll!RtlUserThreadStart+0x28

## Attachments

- [Recording #1.mp4](attachments/Recording #1.mp4) (video/mp4, 1.0 MB)

## Timeline

### [Deleted User] (2023-10-21)

[Empty comment from Monorail migration]

### ch...@gmail.com (2023-10-21)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-10-23)

I was unable to repro this, though the behavior of my browser was a bit different when clicking the "select any page area" button, I didn't actually get the "select an area to search with lens" bubble. Are you running with any non-standard flags / settings?

[Monorail components: UI>Browser>SearchSidePanel]

### ch...@gmail.com (2023-10-23)

I don't repro this on ASAN build. I can only repro this on Canary and Dev builds.

>> Are you running with any non-standard flags / settings?

No.



### [Deleted User] (2023-10-23)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ju...@google.com (2023-10-24)

I am able to reproduce this on Chrome Canary 120.0.6086.0 on MacOS. I think this has to do with how the browser is fetched by the region search tool. I am investigating now.

### ju...@google.com (2023-10-24)

This feature is currently only enabled by experiment or by chrome flag. The flag is chrome://flags/#csc.

### gi...@appspot.gserviceaccount.com (2023-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/444f737100c497f9ba3433b3a474b3c0f2cac23a

commit 444f737100c497f9ba3433b3a474b3c0f2cac23a
Author: Juan Mojica <juanmojica@google.com>
Date: Wed Oct 25 00:47:21 2023

Fix region search controller using dangling browser pointer.

Gets the browser on every start instead of storing it as a raw_ptr.

Cq-Include-Trybots: luci.chrome.try:linux-chromeos-chrome,mac-chrome
Bug: 1494565, b:307537320
Change-Id: I1844ecaa0a66e439d49c8dd4c1c64ad28d796f7b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4973698
Commit-Queue: Juan Mojica <juanmojica@google.com>
Reviewed-by: Duncan Mercer <mercerd@google.com>
Reviewed-by: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1214562}

[modify] https://crrev.com/444f737100c497f9ba3433b3a474b3c0f2cac23a/chrome/browser/ui/side_panel/companion/companion_tab_helper.cc
[modify] https://crrev.com/444f737100c497f9ba3433b3a474b3c0f2cac23a/chrome/browser/lens/region_search/lens_region_search_controller.h
[modify] https://crrev.com/444f737100c497f9ba3433b3a474b3c0f2cac23a/chrome/browser/ui/views/lens/lens_side_panel_helper.cc
[modify] https://crrev.com/444f737100c497f9ba3433b3a474b3c0f2cac23a/chrome/browser/lens/region_search/lens_region_search_controller.cc
[modify] https://crrev.com/444f737100c497f9ba3433b3a474b3c0f2cac23a/chrome/browser/ui/views/lens/lens_static_page_controller.cc
[modify] https://crrev.com/444f737100c497f9ba3433b3a474b3c0f2cac23a/chrome/browser/renderer_context_menu/render_view_context_menu.cc
[modify] https://crrev.com/444f737100c497f9ba3433b3a474b3c0f2cac23a/chrome/browser/ui/browser_commands.cc
[modify] https://crrev.com/444f737100c497f9ba3433b3a474b3c0f2cac23a/chrome/browser/ui/views/lens/lens_region_search_controller_unittest.cc


### ma...@chromium.org (2023-10-25)

Setting foundin-118 as it looks like the experiment has been running since 117.
Setting desktop platforms based on experiment config.
Setting high severity as this is a UAF in browser process, but mitigated by requiring user actions.

### [Deleted User] (2023-10-25)

[Empty comment from Monorail migration]

### ch...@gmail.com (2023-10-26)

I am not able to repro this on 120.0.6089.3 Canary. Fixed.

### [Deleted User] (2023-10-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ju...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-30)

Requesting merge to extended stable M118 because latest trunk commit (1214562) appears to be after extended stable branch point (1192594).

Requesting merge to stable M119 because latest trunk commit (1214562) appears to be after stable branch point (1204232).

Merge review required: M118 is already shipping to stable.

Merge review required: M119 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [118, 119].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ju...@google.com (2023-10-30)

1. https://chromium-review.googlesource.com/c/chromium/src/+/4973698
2. Yes.
3. It does not pose potential stability risks. It's been in Canary a few days now.
4. No.
5. No.

### [Deleted User] (2023-10-31)

Requesting merge to extended stable M118 because latest trunk commit (1214562) appears to be after extended stable branch point (1192594).

Requesting merge to stable M119 because latest trunk commit (1214562) appears to be after stable branch point (1204232).

Merge review required: M118 is already shipping to stable.

Merge review required: M119 is already shipping to stable.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [118, 119].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-01)

While FoundIn-118 has been applied here, it is unclear if this issue actually goes back as far as 118 or was introduced more recently. 
From https://crbug.com/chromium/1494565#c9 it looks like FoundIn was derived based on the active experimentation beginning in 117 rather than repro of this issue. 
But in https://crbug.com/chromium/1494565#c4 OP conveys, " I can only repro this on Canary and Dev builds." it appears only repros were done on 120 or earlier builds. 


### [Deleted User] (2023-11-01)

Requesting merge to extended stable M118 because latest trunk commit (1214562) appears to be after extended stable branch point (1192594).

Requesting merge to stable M119 because latest trunk commit (1214562) appears to be after stable branch point (1204232).

Not requesting merge to dev (M120) because latest trunk commit (1214562) appears to be prior to dev branch point (1217362). If this is incorrect, please replace the Merge-NA-120 label with Merge-Request-120. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge review required: M118 is already shipping to stable.

Merge review required: M119 is already shipping to stable.

Merge review required: M120 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [118, 119, 120].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ju...@google.com (2023-11-01)

This fix is already merged into M120. https://chromiumdash.appspot.com/commit/444f737100c497f9ba3433b3a474b3c0f2cac23a

### am...@chromium.org (2023-11-01)

Thanks, my concern here is the merge requests for 119 and 120 as per https://crbug.com/chromium/1494565#c19. 
If this was recently introduced and only impacts 120, then merge to 118 and 119 is not needed here. 


### am...@chromium.org (2023-11-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-11-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-02)

Congratulations Khalil! The Chrome VRP Panel has decided to award you $1,000 for this report of a highly mitigated security bug, mitigated by significant user gesture and not being remote exploitable and this pointer being BRP / MiraclePtr protected. Thank you for your efforts and reporting this issue to us! 

### am...@chromium.org (2023-11-03)

Since there is no clear answer here and it doesn't appear this issue goes as far back as 118, combined with the mitigating factors here (significant UI gesture + BRP protection). I am going to decline merges for this fix to 119 and 118. 

### am...@google.com (2023-11-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-12-06)

[Empty comment from Monorail migration]

### pg...@google.com (2023-12-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### gm...@google.com (2024-01-16)

[Empty comment from Monorail migration]

### rz...@google.com (2024-01-17)

[Empty comment from Monorail migration]

### rz...@google.com (2024-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-18)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2024-01-18)

1. Just https://crrev.com/c/5207785
2. Low, no conflicts
3. 120, 121, 122
4. Yes

### na...@google.com (2024-01-22)

Merge approved for LTS-114

### gi...@appspot.gserviceaccount.com (2024-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9f8bea8be72e92e13b8cc5f9c637a2b16dc58b3e

commit 9f8bea8be72e92e13b8cc5f9c637a2b16dc58b3e
Author: Juan Mojica <juanmojica@google.com>
Date: Wed Jan 24 15:50:19 2024

[M114-LTS] Fix region search controller using dangling browser pointer.

Gets the browser on every start instead of storing it as a raw_ptr.

(cherry picked from commit 444f737100c497f9ba3433b3a474b3c0f2cac23a)

Bug: 1494565, b:307537320
Change-Id: I1844ecaa0a66e439d49c8dd4c1c64ad28d796f7b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4973698
Commit-Queue: Juan Mojica <juanmojica@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1214562}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5207785
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Michael Ershov <miersh@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Reviewed-by: Victor Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1672}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/9f8bea8be72e92e13b8cc5f9c637a2b16dc58b3e/chrome/browser/ui/side_panel/companion/companion_tab_helper.cc
[modify] https://crrev.com/9f8bea8be72e92e13b8cc5f9c637a2b16dc58b3e/chrome/browser/lens/region_search/lens_region_search_controller.h
[modify] https://crrev.com/9f8bea8be72e92e13b8cc5f9c637a2b16dc58b3e/chrome/browser/ui/views/lens/lens_side_panel_helper.cc
[modify] https://crrev.com/9f8bea8be72e92e13b8cc5f9c637a2b16dc58b3e/chrome/browser/lens/region_search/lens_region_search_controller.cc
[modify] https://crrev.com/9f8bea8be72e92e13b8cc5f9c637a2b16dc58b3e/chrome/browser/renderer_context_menu/render_view_context_menu.cc
[modify] https://crrev.com/9f8bea8be72e92e13b8cc5f9c637a2b16dc58b3e/chrome/browser/ui/views/lens/lens_static_page_controller.cc
[modify] https://crrev.com/9f8bea8be72e92e13b8cc5f9c637a2b16dc58b3e/chrome/browser/ui/browser_commands.cc
[modify] https://crrev.com/9f8bea8be72e92e13b8cc5f9c637a2b16dc58b3e/chrome/browser/ui/views/lens/lens_region_search_controller_unittest.cc


### rz...@google.com (2024-01-24)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-24)

This issue was migrated from crbug.com/chromium/1494565?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40075359)*

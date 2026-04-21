# Type confusion in blink::StyleBuilderConverterBase::ConvertFontSize Security DCHECK failed: IsA<Derived>(from). 

| Field | Value |
|-------|-------|
| **Issue ID** | [40056683](https://issues.chromium.org/issues/40056683) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2021-07-27 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4582.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-905113.zip

#Reproduce
1. python -m http.server 8000
2. chrome.exe --no-sandbox --user-data-dir=0727 http://localhost:8000/poc.html

Type of crash
render tab

What is the expected behavior?

What went wrong?

#asan
[10552:8776:0727/151835.996:FATAL:casting.h(115)] Security DCHECK failed: IsA<Derived>(from). 
Backtrace:
	base::debug::CollectStackTrace [0x00007FFCF354FB82+18] (C:\b\s\w\ir\cache\builder\src\base\debug\stack_trace_win.cc:303)
	base::debug::StackTrace::StackTrace [0x00007FFCF337C64A+26] (C:\b\s\w\ir\cache\builder\src\base\debug\stack_trace.cc:197)
	logging::LogMessage::~LogMessage [0x00007FFCF33B066C+860] (C:\b\s\w\ir\cache\builder\src\base\logging.cc:589)
	blink::StyleBuilderConverterBase::ConvertFontSize [0x00007FFCFF5B3575+1525] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_builder_converter.cc:421)
	blink::FontStyleResolver::ComputeFont [0x00007FFCFE75E661+929] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\font_style_resolver.cc:30)
	blink::OffscreenCanvasRenderingContext2D::setFont [0x00007FFD01905E98+2426] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\canvas\offscreencanvas2d\offscreen_canvas_rendering_context_2d.cc:427)
	blink::`anonymous namespace'::v8_offscreen_canvas_rendering_context_2d::FontAttributeSetCallback [0x00007FFD02BACC65+813] (C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_offscreen_canvas_rendering_context_2d.cc:923)
	v8::internal::FunctionCallbackArguments::Call [0x00007FFCEF4334DB+1755] (C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:155)
	v8::internal::`anonymous namespace'::HandleApiCallHelper<0> [0x00007FFCEF43059E+2430] (C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:112)
	v8::internal::Builtins::InvokeApiFunction [0x00007FFCEF42E68A+2474] (C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:226)
	v8::internal::Object::SetPropertyWithAccessor [0x00007FFCF00D9C5D+2381] (C:\b\s\w\ir\cache\builder\src\v8\src\objects\objects.cc:1561)
	v8::internal::Object::SetPropertyInternal [0x00007FFCF00EA48E+2206] (C:\b\s\w\ir\cache\builder\src\v8\src\objects\objects.cc:2527)
	v8::internal::Object::SetProperty [0x00007FFCF00E9AB1+289] (C:\b\s\w\ir\cache\builder\src\v8\src\objects\objects.cc:2610)
	v8::internal::StoreIC::Store [0x00007FFCEFB32549+3977] (C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:1759)
	v8::internal::Runtime_StoreIC_Miss [0x00007FFCEFB4AA01+1169] (C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:2640)
	(No symbol) [0x00007EDE000BD3DC]
Task trace:
Backtrace:
	blink::ImageLoader::ImageNotifyFinished [0x00007FFCFB5F29F1+3105] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\image_loader.cc:845)
	blink::Document::DecrementLoadEventDelayCount [0x00007FFCF7E04C70+384] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:7147)
	media::PipelineImpl::RendererWrapper::OnPipelineError [0x00007FFCEB28D968+584] (C:\b\s\w\ir\cache\builder\src\media\base\pipeline_impl.cc:908)
	media::RunOnTaskRunner [0x00007FFCEB2A6861+383] (C:\b\s\w\ir\cache\builder\src\media\base\serial_runner.cc:38)
	media::FFmpegDemuxer::OnOpenContextDone [0x00007FFCEB467996+1084] (C:\b\s\w\ir\cache\builder\src\media\filters\ffmpeg_demuxer.cc:1286)
Task trace buffer limit hit, update PendingTask::kTaskBacktraceLength to increase.

=================================================================
==10552==ERROR: AddressSanitizer: breakpoint on unknown address 0x7ffcf354e56d (pc 0x7ffcf354e56d bp 0x001e551fc020 sp 0x001e551fbf50 T37)
==10552==*** WARNING: Failed to initialize DbgHelp!              ***
==10552==*** Most likely this means that the app is already      ***
==10552==*** using DbgHelp, possibly with incompatible flags.    ***
==10552==*** Due to technical reasons, symbolization might crash ***
==10552==*** or produce wrong results.                           ***
==10552==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffcf354e56c in base::debug::BreakDebugger C:\b\s\w\ir\cache\builder\src\base\debug\debugger_win.cc:28
    #1 0x7ffcf33b0f69 in logging::LogMessage::~LogMessage C:\b\s\w\ir\cache\builder\src\base\logging.cc:891
    #2 0x7ffcff5b3574 in blink::StyleBuilderConverterBase::ConvertFontSize C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_builder_converter.cc:421
    #3 0x7ffcfe75e660 in blink::FontStyleResolver::ComputeFont C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\font_style_resolver.cc:30
    #4 0x7ffd01905e97 in blink::OffscreenCanvasRenderingContext2D::setFont C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\canvas\offscreencanvas2d\offscreen_canvas_rendering_context_2d.cc:427
    #5 0x7ffd02bacc64 in blink::`anonymous namespace'::v8_offscreen_canvas_rendering_context_2d::FontAttributeSetCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_offscreen_canvas_rendering_context_2d.cc:923
    #6 0x7ffcef4334da in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:155
    #7 0x7ffcef43059d in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:112
    #8 0x7ffcef42e689 in v8::internal::Builtins::InvokeApiFunction C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:226
    #9 0x7ffcf00d9c5c in v8::internal::Object::SetPropertyWithAccessor C:\b\s\w\ir\cache\builder\src\v8\src\objects\objects.cc:1561
    #10 0x7ffcf00ea48d in v8::internal::Object::SetPropertyInternal C:\b\s\w\ir\cache\builder\src\v8\src\objects\objects.cc:2527
    #11 0x7ffcf00e9ab0 in v8::internal::Object::SetProperty C:\b\s\w\ir\cache\builder\src\v8\src\objects\objects.cc:2610
    #12 0x7ffcefb32548 in v8::internal::StoreIC::Store C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:1759
    #13 0x7ffcefb4aa00 in v8::internal::Runtime_StoreIC_Miss C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:2640

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: breakpoint C:\b\s\w\ir\cache\builder\src\base\debug\debugger_win.cc:28 in base::debug::BreakDebugger
Thread T37 created by T0 here:
    #0 0x7ff6dc8806d2 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
    #1 0x7ffcf3588eee in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:185
    #2 0x7ffcf350627d in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:216
    #3 0x7ffced5790f1 in content::RenderProcessHostImpl::Init C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_process_host_impl.cc:1997
    #4 0x7ffced55c298 in content::RenderFrameHostManager::InitRenderView C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:2913
    #5 0x7ffced5530df in content::RenderFrameHostManager::ReinitializeMainRenderFrame C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:3149
    #6 0x7ffced5508b1 in content::RenderFrameHostManager::GetFrameHostForNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:1120
    #7 0x7ffced54f448 in content::RenderFrameHostManager::DidCreateNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:875
    #8 0x7ffced2cbfc9 in content::FrameTreeNode::CreatedNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\frame_tree_node.cc:536
    #9 0x7ffced486f9d in content::Navigator::Navigate C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigator.cc:603
    #10 0x7ffced3f9995 in content::NavigationControllerImpl::NavigateWithoutEntry C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:3244
    #11 0x7ffced3f8ad0 in content::NavigationControllerImpl::LoadURLWithParams C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:1091
    #12 0x7ffcf56575ea in `anonymous namespace'::LoadURLInContents C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:387
    #13 0x7ffcf56549ac in Navigate C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:659
    #14 0x7ffcfcaee435 in StartupBrowserCreatorImpl::OpenTabsInBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:316
    #15 0x7ffcfcaf043e in StartupBrowserCreatorImpl::RestoreOrCreateBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:592
    #16 0x7ffcfcaed605 in StartupBrowserCreatorImpl::DetermineURLsAndLaunch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:430
    #17 0x7ffcfcaeccac in StartupBrowserCreatorImpl::Launch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:220
    #18 0x7ffcf8a2c948 in StartupBrowserCreator::LaunchBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:617
    #19 0x7ffcf8a2f80a in StartupBrowserCreator::ProcessLastOpenedProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1225
    #20 0x7ffcf8a2e9ad in StartupBrowserCreator::LaunchBrowserForLastProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:708
    #21 0x7ffcf8a32632 in StartupBrowserCreator::StartupLaunchAfterProtocolHandler C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1178
    #22 0x7ffcf8a2be04 in StartupBrowserCreator::ProcessCmdLineImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1138
    #23 0x7ffcf8a2a339 in StartupBrowserCreator::Start C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:553
    #24 0x7ffcf5b66085 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1676
    #25 0x7ffcf5b63c86 in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1051
    #26 0x7ffceca3904e in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:937
    #27 0x7ffced828f5b in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup_task_runner.cc:41
    #28 0x7ffceca38555 in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:845
    #29 0x7ffceca3ff75 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:131
    #30 0x7ffceca34d24 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:45
    #31 0x7ffcef2a0980 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:608
    #32 0x7ffcef2a321c in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1104
    #33 0x7ffcef2a2403 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:971
    #34 0x7ffcef29ee86 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:390
    #35 0x7ffcef29fec8 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:418
    #36 0x7ffce8cd145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:164
    #37 0x7ff6dc7d5b74 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #38 0x7ff6dc7d2be8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #39 0x7ff6dcbc136f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #40 0x7ffd712b7033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #41 0x7ffd71c82650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

==10552==ABORTING

Did this work before? N/A 

Chrome version: 94.0.4582.0  Channel: n/a
OS Version: 10.0

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 367 B)
- [asan.txt](attachments/asan.txt) (text/plain, 22.1 KB)

## Timeline

### [Deleted User] (2021-07-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-07-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5932411794554880.

### cl...@chromium.org (2021-07-27)

ClusterFuzz testcase 5932411794554880 is closed as invalid, so closing issue.

### cl...@chromium.org (2021-07-27)

Testcase 5932411794554880 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5932411794554880.

### m....@gmail.com (2021-07-28)

I think ClusterFuzz was wrong, does anyone test it locally?

### me...@chromium.org (2021-07-28)

Reopening.

### me...@chromium.org (2021-07-28)

I can repro. andruud, could you PTAL?

[Monorail components: Blink>CSS]

### [Deleted User] (2021-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-28)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-28)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-28)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2021-07-28)

Looks like the offscreen canvas context incorrectly allows values with "var()" through its API.

### an...@chromium.org (2021-07-28)

Fix coming: https://chromium-review.googlesource.com/c/chromium/src/+/3058649

I don't think it's a recent regressions.

### gi...@appspot.gserviceaccount.com (2021-07-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1583beafd72f80ff8cae84cff4d85749220ae699

commit 1583beafd72f80ff8cae84cff4d85749220ae699
Author: Anders Hartvoll Ruud <andruud@chromium.org>
Date: Thu Jul 29 07:05:38 2021

Handle font values that contain "var()" for OffscreenCanvas

This is an offscreen equivalent to https://crbug.com/chromium/1131922. The fix for that
bug introduced CSSParser::ParseFont, which handles var() and CSS-wide
keywords correctly.

Use CSSParser::ParseFont for OffscreenCanvasRenderingContext2D as well.

Fixed: 1233430
Change-Id: Ic2119c64dec428f3b34f7fc0c15c86b6bcfe9195
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3058649
Reviewed-by: Aaron Krajeski <aaronhk@chromium.org>
Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Commit-Position: refs/heads/master@{#906604}

[modify] https://crrev.com/1583beafd72f80ff8cae84cff4d85749220ae699/third_party/blink/renderer/modules/canvas/offscreencanvas2d/offscreen_canvas_rendering_context_2d.cc
[modify] https://crrev.com/1583beafd72f80ff8cae84cff4d85749220ae699/third_party/blink/web_tests/external/wpt/html/canvas/offscreen/text/2d.text.font.parse.invalid.html
[modify] https://crrev.com/1583beafd72f80ff8cae84cff4d85749220ae699/third_party/blink/web_tests/external/wpt/html/canvas/offscreen/text/2d.text.font.parse.invalid.worker.js
[modify] https://crrev.com/1583beafd72f80ff8cae84cff4d85749220ae699/third_party/blink/web_tests/external/wpt/html/canvas/tools/yaml/offscreen/text.yaml


### [Deleted User] (2021-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-04)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. Nice work! 

### m....@gmail.com (2021-08-06)

[Comment Deleted]

### am...@google.com (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-14)

Not requesting merge to dev (M94) because latest trunk commit (906604) appears to be prior to dev branch point (911515). If this is incorrect, please replace the Merge-na label with Merge-Request-94. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1233430?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056683)*

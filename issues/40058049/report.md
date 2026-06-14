# Application crashes on Safety warning page when returning to page

| Field | Value |
|-------|-------|
| **Issue ID** | [40058049](https://issues.chromium.org/issues/40058049) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | UI>Browser>Interstitials, UI>Browser>Navigation>BFCache |
| **Platforms** | Windows |
| **Reporter** | re...@gmail.com |
| **Assignee** | fe...@chromium.org |
| **Created** | 2021-11-28 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36

Steps to reproduce the problem:
1. Open the attached “PoC.html” HTML document.
2. Click “Click me” in the web page.
3. When the Safety warning page is displayed, enter “https://www.google.com/” in the address bar to access it. * It is an example and does not need to be google.com.
4. When the Google page is fully open, press the back button on your browser.
5. There is no reaction. Please press it again. * In rare cases, the RESULT_CODE_KILLED_BAD_MESSAGE error page may appear. Continue to the next step.
6. Press the browser's back button again.
7. As a result, Chrome crashes.

What is the expected behavior?
The browser is expected to display the previously displayed page without crashing.

What went wrong?
When the Safety warning page is displayed as a mitigation for the IDN homograph attack, access any website to the address bar of that page. Then, when I tried to return to the Safety warning page with the browser's back button, the RESULT_CODE_KILLED_BAD_MESSAGE error code was thrown and the application crashed.
Everyone doesn't want web browsers to crash.
It's unclear if it's practically possible, but it could hinder the use of web browsers through a specially crafted HTML document that exploits this bug.

Did this work before? N/A 

Chrome version: 96.0.4664.45  Channel: stable
OS Version: 10.0

I tried to submit the report promptly.
With the reproducibility I presented, there were some cases where the cause was unknown but it didn't work.
In that case, it was reproducible by clearing the browser's cache and history altogether.
I have confirmed the reproducibility of the following products of Windows 10 and macOS Big Sur.
Google Chrome (Stable)
Google Chrome Canary
We're sorry, but we haven't investigated the other combinations in detail.

Also, the URL of the link “IDN homograph attack on * .office365.com” in the PoC HTML document was created by me for cybersecurity research purposes. It's blocked by Chrome in the first place, but we promise that the content is harmless.

## Attachments

- [PoC.html](attachments/PoC.html) (text/plain, 318 B)
- [Chromium_Crash_Bug.mp4](attachments/Chromium_Crash_Bug.mp4) (video/mp4, 12.5 MB)
- [Chromium_RESULT_CODE_KILLED_BAD_MESSAGE.png](attachments/Chromium_RESULT_CODE_KILLED_BAD_MESSAGE.png) (image/png, 329.4 KB)
- [1274308 - No issue.mp4](attachments/1274308 - No issue.mp4) (video/mp4, 2.0 MB)
- [Chromium_Crash_Bug_2.mp4](attachments/Chromium_Crash_Bug_2.mp4) (video/mp4, 13.5 MB)
- [1274308-96.mp4](attachments/1274308-96.mp4) (video/mp4, 9.9 MB)
- [1274308-101.mp4](attachments/1274308-101.mp4) (video/mp4, 4.8 MB)
- [1274308-100.mp4](attachments/1274308-100.mp4) (video/mp4, 4.5 MB)

## Timeline

### sa...@chromium.org (2021-11-29)

[Empty comment from Monorail migration]

### sa...@chromium.org (2021-11-29)

[Empty comment from Monorail migration]

[Monorail components: UI]

### ka...@google.com (2021-11-29)

[Comment Deleted]

[Monorail components: Blink]

### ka...@google.com (2021-11-29)

[Empty comment from Monorail migration]

[Monorail components: -Blink]

### po...@chromium.org (2021-11-30)

Unable to reproduce the issue with reported chrome version #96.0.4664.45 on Windows 10 as per steps mentioned in the C#0

@Reporter: Could you please provide 16 digit crash id from chrome://crashes for furthur triaging the issue.Check the attached screencast and let us know if anything is missed.The safety warning page is not displayed while trying to reproduce. please let us know how this safety warning page can be reproduced. Also  could you please let us know if you are able to reproduce this crash consistently in a fresh profile without any apps and extensions on latest chrome versions.


Thanks..!

### re...@gmail.com (2021-12-01)

Thank you for your cooperation in reproducing the issue.
I investigated what was the cause.
Again, the issue was reproducible only when the Safety warning page was displayed.
Certainly the reproducibility was unstable.
I found the cause of this. The cause was whether the Chromium component "Safety Tips" were updated.
Chrome components are not updated immediately after installation or launching with a new profile.
This means that you won't see the "Safety warning" page because you don't have a Phishing database.
Either the "Safety Tips" component was automatically updated or manually updated.
When I verified it with multiple Chrome (Chromium) builds, it was definitely reproducible with Chrome (Stable), Chrome Dev, Chrome Canary and the latest Chromium build 98.0.4740.0.
The reproduction procedure is described below.

New reproduction procedure
1. Go to chrome://components/
2. Press the "Check for Update" button in the "Safety Tips" component at the bottom of the page.
3. Make sure the "Safety Tips" component has been updated. The numbers will be updated from "Version: 0.0.0.0".
4. Open the attached “PoC.html” HTML document.
5. Click “Click me” in the web page.
6. When the Safety warning page is displayed, enter “google.com” in the address bar to access it.
7. When the Google page is fully open, press the back button on your browser.
8. There is no response, but proceed to the next step.
9. Press the browser back button again.
10. As a result, Chrome crashes.


And I will tell you the Crash report ID.

Crash from Wednesday, December 1, 2021 at 9:55:44 AM
Status: Uploaded
Uploaded Crash Report ID: e9f610aa1d6c5e53
Upload Time: Wednesday, December 1, 2021 at 9:55:46 AM

### [Deleted User] (2021-12-01)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dh...@chromium.org (2021-12-02)

Please find the magic signature & stack trace for the crash id#e9f610aa1d6c5e53

Magic Signature >> [Renderer kill 205] content::RenderFrameHostImpl::DidCommitNavigationInternal

Stack Trace >>
Thread 0  (id: 0x00004384) CRASHED [Simulated Exception @ 0x00007ffd2d6d2c57 ] MAGIC SIGNATURE THREADShow exception record
0x00007ffd2d6d2c57(chrome_elf.dll -crashpad.cc:275)crash_reporter::DumpWithoutCrashing()
0x00007ffcd163d970(chrome.dll -dump_without_crashing.cc:25)base::debug::DumpWithoutCrashing()
0x00007ffcd21918f5(chrome.dll -render_process_host_impl.cc:3049)content::RenderProcessHostImpl::ShutdownForBadMessage(content::RenderProcessHost::CrashReportMode)
0x00007ffccddaf8cc(chrome.dll -render_frame_host_impl.cc:10224)content::RenderFrameHostImpl::DidCommitNavigationInternal
0x00007ffcd2177335(chrome.dll -render_frame_host_impl.cc:4094)content::RenderFrameHostImpl::DidCommitPageActivation(content::NavigationRequest *,mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>)
0x00007ffcd2176e8c(chrome.dll -navigation_request.cc:4480)content::NavigationRequest::CommitPageActivation
0x00007ffcce661aa0(chrome.dll -navigation_request.cc:4230)content::NavigationRequest::CommitNavigation
0x00007ffccdef7d9b(chrome.dll -commit_deferring_condition_runner.cc:149)content::CommitDeferringConditionRunner::ProcessConditions()
0x00007ffcd213a859(chrome.dll -bind_internal.h:690)base::internal::Invoker<base::internal::BindState<`lambda at ../../content/browser/renderer_host/back_forward_cache_impl.cc:1257:11',base::TimeTicks,base::OnceCallback<void ()> >,void ()>::RunOnce
0x00007ffccf122c12(chrome.dll -barrier_closure.cc:35)base::`anonymous namespace'::BarrierInfo::Run
0x00007ffcd159e13c(chrome.dll -page_lifecycle_state_manager.cc:245)content::PageLifecycleStateManager::OnPageLifecycleChangedAck
0x00007ffcd15a80a6(chrome.dll -bind_internal.h:509)base::internal::FunctorTraits<void (content::PageLifecycleStateManager::*)(mojo::StructPtr<blink::mojom::PageLifecycleState>, base::OnceCallback<void ()>),void>::Invoke<void (content::PageLifecycleStateManager::*)(mojo::StructPtr<blink::mojom::PageLifecycleState>, base::OnceCallback<void ()>),base::WeakPtr<content::PageLifecycleStateManager>,mojo::StructPtr<blink::mojom::PageLifecycleState>,base::OnceCallback<void ()> >
0x00007ffcd16bc47b(chrome.dll -net_benchmarking.mojom.cc:544)blink::mojom::BlobRegistry_GetBlobFromUUID_ForwardToCallback::Accept(mojo::Message *)
0x00007ffcd0946061(chrome.dll -interface_endpoint_client.cc:331)mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept(mojo::Message *)
0x00007ffcd07eaee8(chrome.dll -message_dispatcher.cc:43)mojo::MessageDispatcher::Accept(mojo::Message *)
0x00007ffcd1246302(chrome.dll -bind_internal.h:690)base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce
0x00007ffcd06b0774(chrome.dll -task_annotator.cc:178)base::TaskAnnotator::RunTask(char const *,base::PendingTask *)
0x00007ffcd06aee40(chrome.dll -thread_controller_with_message_pump_impl.cc:260)base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
0x00007ffcd0f383e6(chrome.dll -message_pump_win.cc:220)base::MessagePumpForUI::DoRunLoop()
0x00007ffccd88a153(chrome.dll -message_pump_win.cc:78)base::MessagePumpWin::Run(base::MessagePump::Delegate *)
0x00007ffccde07eb2(chrome.dll -thread_controller_with_message_pump_impl.cc:462)base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool,base::TimeDelta)
0x00007ffcce034ee5(chrome.dll -run_loop.cc:140)base::RunLoop::Run(base::Location const &)
0x00007ffcce54170a(chrome.dll -browser_main_loop.cc:989)content::BrowserMainLoop::RunMainMessageLoop()
0x00007ffcce09d490(chrome.dll -browser_main.cc:49)content::BrowserMain(content::MainFunctionParams const &)
0x00007ffcce09b53d(chrome.dll -content_main_runner_impl.cc:1116)content::ContentMainRunnerImpl::RunBrowser
0x00007ffcce091009(chrome.dll -content_main_runner_impl.cc:983)content::ContentMainRunnerImpl::Run(bool)
0x00007ffccdd37f81(chrome.dll -content_main.cc:418)content::ContentMain(content::ContentMainParams const &)
0x00007ffccdd36e49(chrome.dll -chrome_main.cc:172)ChromeMain
0x00007ff6fa096f2f(chrome.exe -main_dll_loader_win.cc:169)MainDllLoader::Launch(HINSTANCE__ *,base::TimeTicks)
0x00007ff6fa096ac9(chrome.exe -chrome_exe_main_win.cc:382)wWinMain
0x00007ff6fa0fb9d1(chrome.exe -exe_common.inl:288)__scrt_common_main_seh
0x00007ffd4d4a7033(KERNEL32.DLL + 0x00017033)BaseThreadInitThunk
0x00007ffd4f0a2650(ntdll.dll + 0x00052650)RtlUserThreadStart

Using Code Search for the file, "render_frame_host_impl.cc" suspecting the below Cl might have caused this issue

Suspect CL: https://chromium.googlesource.com/chromium/src/+/87696ae524748b1bd0781d57045fb89c3e4ad44f

dtapuska@ -- Could you please check whether this is caused with respect to your change, if not please help us in assigning it to the right owner.

Thanks!

[Monorail components: -UI Internals>Core]

### dt...@chromium.org (2021-12-02)

No this is not due to my change. My change landed in M98 and this is actually in Stable M96.

I debugged the issue and it appears the interstitial is being served from bfcache I believe. As it is failing at:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=6052;drc=93a1f4f7b9d4d7893fa643c4955be0a4b8db7480

Full stack trace is:
[40855:40855:1202/111957.765664:ERROR:navigation_request.cc(4464)] Served from bfcache 1
[40855:40855:1202/111957.766489:FATAL:navigation_request.cc(6065)] Check failed: params->url_is_unreachable == false (1 vs. 0)
#0 0x7febf280b0a9 base::debug::CollectStackTrace()
#1 0x7febf2705ab3 base::debug::StackTrace::StackTrace()
#2 0x7febf27264b4 logging::LogMessage::~LogMessage()
#3 0x7febf2726f2e base::internal::LoggerWithAllowedAllocations::~LoggerWithAllowedAllocations()
#4 0x7febef6ea37f content::NavigationRequest::MakeDidCommitProvisionalLoadParamsForActivation()
#5 0x7febef6e3329 content::NavigationRequest::MakeDidCommitProvisionalLoadParamsForBFCacheRestore()
#6 0x7febef6e30a7 content::NavigationRequest::CommitPageActivation()
#7 0x7febef6d3692 content::NavigationRequest::CommitNavigation()
#8 0x7febef6e095b content::NavigationRequest::OnCommitDeferringConditionChecksComplete()
#9 0x7febef60becc content::CommitDeferringConditionRunner::ProcessConditions()
#10 0x7febef60c08e content::CommitDeferringConditionRunner::ResumeProcessing()
#11 0x7febeee13014 base::internal::Invoker<>::RunOnce()
#12 0x7febef602173 base::internal::Invoker<>::RunOnce()
#13 0x7febf26f012f base::(anonymous namespace)::BarrierInfo::Run()
#14 0x7febef6fd5a2 content::PageLifecycleStateManager::OnPageLifecycleChangedAck()
#15 0x7febef6fd92b base::internal::FunctorTraits<>::Invoke<>()
#16 0x7febec15ca95 blink::mojom::PageBroadcast_SetPageLifecycleState_ForwardToCallback::Accept()
#17 0x7febf20378d1 mojo::InterfaceEndpointClient::HandleValidatedMessage()
#18 0x7febf203d8ef mojo::MessageDispatcher::Accept()
#19 0x7febf20391bd mojo::InterfaceEndpointClient::HandleIncomingMessage()
#20 0x7febf0cd4a1d IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread()
#21 0x7febf0cd117c base::internal::Invoker<>::RunOnce()
#22 0x7febf279bee9 base::TaskAnnotator::RunTaskImpl()

Assigning to fergal@ as this seems to be a BF Cache Bug.


[Monorail components: -Internals>Core UI>Browser>Navigation>BFCache]

### dt...@chromium.org (2021-12-02)

Sorry code search line numbers don't match the stack trace since my local branch didn't match ToT version I was searching on code search.

### fe...@google.com (2021-12-03)

Thanks. I can reproduce and it's easy to stop this happening by just checking url_is_unreachable before and not BFCaching the interstitial.

I'm not sure though if that's the correct thing to do. I think we should not cache any interstitials. In devtools this interstitial has a URL of chrome-error://chromewebdata/ ​but

GetLastCommittedURL

is returning 

https://outlook.xn--offce365-41a.com

What is the correct way to detect interstitials?

### fe...@google.com (2021-12-03)

last_document_url_in_renderer() seems to have the correct (chrome://) URL, so I wonder if we should

-  if (!rfh->GetLastCommittedURL().SchemeIsHTTPOrHTTPS()) {
+  if (!rfh->last_document_url_in_renderer().SchemeIsHTTPOrHTTPS()) {
     result.No(
         BackForwardCacheMetrics::NotRestoredReason::kSchemeNotHTTPOrHTTPS);
   }

rakina@, looks like you added RendererURLInfo, which should we use for BFCache?

### ra...@chromium.org (2021-12-03)

Do we want to know if the RFH is on an error page? Then we should just use IsErrorDocument() instead of checking the URL.

### fe...@google.com (2021-12-03)

IsErrorDocument() seems reasonable but it ​seems to be populated from a very different code-path. 

It feels like there could be other times when GetLastCommittedURL() != last_document_url_in_renderer().

What's the argument for not using last_document_url_in_renderer() when thinking about whether the page can be cached?

### ra...@chromium.org (2021-12-03)

Last document URL can only be different from GetLastCommittedURL() in case of error pages, WebView cases which BFCache doesn't care about, and when the URL is updated due to document.open() being called on it by another frame. That can only happen when the other frame is same-origin, but can involve about:blank etc.

last_document_url_in_renderer is not used by anything in the browser. The URL in the NavigationEntry will equal GetLastCommittedURL(), and I think it should be what is used for BFCache decisions. Using last_document_url_in_renderer to detect if a page is an error page sounds like an indirect way that might lead to confusions and maybe bugs.

### fe...@google.com (2021-12-06)

I think the reason why we don't see more of these is that the other interstitial error pages don't have a 200 status code, this one does. That seems odd.

### fe...@google.com (2021-12-06)

Adding some look-alikes folks.

Should the lookalike interstitial be showing up with a 200 status code? I suspect not given that we consider it an error page.

[Monorail components: UI>Browser>Interstitials]

### gi...@appspot.gserviceaccount.com (2022-03-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7a05b426c6c51254a08de9a8dee8db9c1911b9c9

commit 7a05b426c6c51254a08de9a8dee8db9c1911b9c9
Author: Fergal Daly <fergal@chromium.org>
Date: Tue Mar 15 09:18:40 2022

Use IsErrorDocument() to prevent BFCacheing of interstitials and errors.

In the bug, a crash occurs because we try to cache an interstitial. We
catch some error documents via status codes etc but interstitials do
not consistently set those. Checking IsErrorDocument() is more reliable.

Bug: 1274308,1287996
Change-Id: Ifec662c169c77e33ca5dc4d56b0e42c8d71f1d97
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3319862
Commit-Queue: Fergal Daly <fergal@chromium.org>
Reviewed-by: Rakina Zata Amni <rakina@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Alexander Timin <altimin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#981026}

[modify] https://crrev.com/7a05b426c6c51254a08de9a8dee8db9c1911b9c9/content/browser/back_forward_cache_browsertest.cc
[modify] https://crrev.com/7a05b426c6c51254a08de9a8dee8db9c1911b9c9/third_party/blink/public/devtools_protocol/browser_protocol.pdl
[modify] https://crrev.com/7a05b426c6c51254a08de9a8dee8db9c1911b9c9/content/browser/devtools/protocol/page_handler.cc
[modify] https://crrev.com/7a05b426c6c51254a08de9a8dee8db9c1911b9c9/content/browser/renderer_host/back_forward_cache_can_store_document_result.cc
[modify] https://crrev.com/7a05b426c6c51254a08de9a8dee8db9c1911b9c9/content/browser/back_forward_cache_basics_browsertest.cc
[modify] https://crrev.com/7a05b426c6c51254a08de9a8dee8db9c1911b9c9/content/browser/back_forward_cache_internal_browsertest.cc
[modify] https://crrev.com/7a05b426c6c51254a08de9a8dee8db9c1911b9c9/content/browser/renderer_host/back_forward_cache_impl.cc
[modify] https://crrev.com/7a05b426c6c51254a08de9a8dee8db9c1911b9c9/content/browser/renderer_host/back_forward_cache_metrics.h
[modify] https://crrev.com/7a05b426c6c51254a08de9a8dee8db9c1911b9c9/content/browser/back_forward_cache_browsertest.h
[modify] https://crrev.com/7a05b426c6c51254a08de9a8dee8db9c1911b9c9/base/tracing/protos/chrome_track_event.proto


### fe...@google.com (2022-03-15)

Closing this, that change should have fixed it. If not, please let me know.

### fe...@google.com (2022-03-15)

[Empty comment from Monorail migration]

### ka...@chromium.org (2022-03-16)

Able to reproduce the issue on reported chrome version #96.0.4664.45 using Win 10  as per https://crbug.com/chromium/1274308#c6 Observed the crash 
Verified the fix on Win10  on the latest M101 #101.0.4947.0 Observed no crash 
Attaching screencasts for reference.

Hence, the fix is working as expected and adding verified labels

### gi...@appspot.gserviceaccount.com (2022-03-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/21cc9b98d6187e6a9e5cf2c26d3519cd5e525f1d

commit 21cc9b98d6187e6a9e5cf2c26d3519cd5e525f1d
Author: Changhao Han <changhaohan@chromium.org>
Date: Fri Mar 18 09:25:30 2022

Roll CDP and css_properties updates into DevTools

DISABLE_THIRD_PARTY_CHECK=add missing BFCache not restored reason

Bug: 1274308,1287996
Change-Id: If0795ce0d051901ddc686230ca2de60a63fed7a7
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3535880
Reviewed-by: Alex Rudenko <alexrudenko@chromium.org>
Commit-Queue: Changhao Han <changhaohan@chromium.org>
Auto-Submit: Changhao Han <changhaohan@chromium.org>

[modify] https://crrev.com/21cc9b98d6187e6a9e5cf2c26d3519cd5e525f1d/front_end/generated/InspectorBackendCommands.js
[modify] https://crrev.com/21cc9b98d6187e6a9e5cf2c26d3519cd5e525f1d/third_party/blink/public/devtools_protocol/browser_protocol.pdl
[modify] https://crrev.com/21cc9b98d6187e6a9e5cf2c26d3519cd5e525f1d/third_party/blink/public/devtools_protocol/browser_protocol.json
[modify] https://crrev.com/21cc9b98d6187e6a9e5cf2c26d3519cd5e525f1d/front_end/generated/SupportedCSSProperties.js
[modify] https://crrev.com/21cc9b98d6187e6a9e5cf2c26d3519cd5e525f1d/front_end/core/i18n/locales/en-US.json
[modify] https://crrev.com/21cc9b98d6187e6a9e5cf2c26d3519cd5e525f1d/front_end/panels/application/components/BackForwardCacheStrings.ts
[modify] https://crrev.com/21cc9b98d6187e6a9e5cf2c26d3519cd5e525f1d/third_party/blink/renderer/core/css/css_properties.json5
[modify] https://crrev.com/21cc9b98d6187e6a9e5cf2c26d3519cd5e525f1d/front_end/core/i18n/locales/en-XL.json
[modify] https://crrev.com/21cc9b98d6187e6a9e5cf2c26d3519cd5e525f1d/front_end/generated/protocol.ts


### gi...@appspot.gserviceaccount.com (2022-03-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3fa5b727580d9c357a4c78519897a27fe156950d

commit 3fa5b727580d9c357a4c78519897a27fe156950d
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Mar 18 11:25:50 2022

Roll DevTools Frontend from a77c27dff5be to 21cc9b98d618 (1 revision)

https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/a77c27dff5be..21cc9b98d618

2022-03-18 changhaohan@chromium.org Roll CDP and css_properties updates into DevTools

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/devtools-frontend-chromium
Please CC devtools-waterfall-sheriff-onduty@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1274308,chromium:1287996
Tbr: devtools-waterfall-sheriff-onduty@grotations.appspotmail.com
Change-Id: I5d6fe78870a45bb741be162c4422bdc5f816e321
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3535922
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#982662}

[modify] https://crrev.com/3fa5b727580d9c357a4c78519897a27fe156950d/DEPS


### gi...@appspot.gserviceaccount.com (2022-04-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/57bdd90d8c81168e8f055e5663967854068b7f05

commit 57bdd90d8c81168e8f055e5663967854068b7f05
Author: Fergal Daly <fergal@chromium.org>
Date: Thu Apr 07 02:16:11 2022

Use IsErrorDocument() to prevent BFCacheing of interstitials and errors.

In the bug, a crash occurs because we try to cache an interstitial. We
catch some error documents via status codes etc but interstitials do
not consistently set those. Checking IsErrorDocument() is more reliable.

(cherry picked from commit 7a05b426c6c51254a08de9a8dee8db9c1911b9c9)

Bug: 1274308,1287996,1283050
Change-Id: Ifec662c169c77e33ca5dc4d56b0e42c8d71f1d97
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3319862
Commit-Queue: Fergal Daly <fergal@chromium.org>
Reviewed-by: Rakina Zata Amni <rakina@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Alexander Timin <altimin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#981026}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3559271
Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org>
Owners-Override: Hiroki Nakagawa <nhiroki@chromium.org>
Commit-Queue: Rakina Zata Amni <rakina@chromium.org>
Cr-Commit-Position: refs/branch-heads/4896@{#1065}
Cr-Branched-From: 1f63ff4bc27570761b35ffbc7f938f6586f7bee8-refs/heads/main@{#972766}

[modify] https://crrev.com/57bdd90d8c81168e8f055e5663967854068b7f05/content/browser/back_forward_cache_browsertest.cc
[modify] https://crrev.com/57bdd90d8c81168e8f055e5663967854068b7f05/third_party/blink/public/devtools_protocol/browser_protocol.pdl
[modify] https://crrev.com/57bdd90d8c81168e8f055e5663967854068b7f05/content/browser/devtools/protocol/page_handler.cc
[modify] https://crrev.com/57bdd90d8c81168e8f055e5663967854068b7f05/content/browser/back_forward_cache_basics_browsertest.cc
[modify] https://crrev.com/57bdd90d8c81168e8f055e5663967854068b7f05/content/browser/renderer_host/back_forward_cache_can_store_document_result.cc
[modify] https://crrev.com/57bdd90d8c81168e8f055e5663967854068b7f05/content/browser/back_forward_cache_browsertest.h
[modify] https://crrev.com/57bdd90d8c81168e8f055e5663967854068b7f05/content/browser/back_forward_cache_internal_browsertest.cc
[modify] https://crrev.com/57bdd90d8c81168e8f055e5663967854068b7f05/content/browser/renderer_host/back_forward_cache_impl.cc
[modify] https://crrev.com/57bdd90d8c81168e8f055e5663967854068b7f05/content/browser/renderer_host/back_forward_cache_metrics.h
[modify] https://crrev.com/57bdd90d8c81168e8f055e5663967854068b7f05/base/tracing/protos/chrome_track_event.proto


### ka...@chromium.org (2022-04-11)

Verified the fix on Win10  on the latest M100 #100.0.4896.88 Observed no crash 
Attaching screencasts for reference.

Hence, the fix is working as expected and adding verified labels

### am...@chromium.org (2022-04-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-04-11)

Hello, reinforchu@ -- as your issue was the original reporting of an issue that turned out to be a security bug, the Chrome VRP would like to extend to you a $1,000 reward to thank you for your report and your detailed reproduction which helped get the issue reproduced and assisted in the root cause analysis. A member of our finance team will be in touch to arrange payment. Thank you for your reporting this issue to us. 

(note for Chromium teams-- temporarily adding RV-SN as this issue alludes to a security bug, will remove this label for this to be publicly disclosed in 14 weeks from fix in accordance with Chrome Security disclosure policy; added Next Action date of 21 June 2022 for public disclosure) 

### am...@google.com (2022-04-13)

[Empty comment from Monorail migration]

### re...@gmail.com (2022-04-14)

Hello Chromium developers.
It's a great honor to receive the Google VRP bugbounty.
And I'm glad that the internet is safer!
I have just asked the P2P VRP Team to start the procedure for receiving rewards.

And I have a question. I have submitted a report of an application crash, but I think the crash is an attack vector that can be a vulnerability. So will a CVE number be assigned to this bug?

I look forward to working with you.

### am...@chromium.org (2022-04-14)

Hello, thank you for reaching out. 
You do not need to reach out to the p2p-vrp@ as they will not yet have the information to process a payment to you until they reach out to you to begin the enrollment process. There are processes on the Google side that will allow that to move forward. 

Also, please do note that this reward was a thank you for your report. There was another reporter who demonstrated the security consequences of this issue,  so acknowledgement and CVE should be provided to them. Without their report, this likely would have been handled solely as a functional issue rather than a security one. 

### gi...@appspot.gserviceaccount.com (2022-04-19)

https://crbug.com/chromium/1283050 has been un-merged from this issue.


### gi...@appspot.gserviceaccount.com (2022-04-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/38ab9c5b06a472fcb5105458b2b4037749c50766

commit 38ab9c5b06a472fcb5105458b2b4037749c50766
Author: Fergal Daly <fergal@chromium.org>
Date: Tue Apr 19 15:25:29 2022

[M96-LTS] Use IsErrorDocument() to prevent BFCacheing of interstitials and errors.

M96 merge issues:
  Tests not present on M96:
  - back_forward_cache_basics_browsertest.cc
  - back_forward_cache_browsertest.h
  - back_forward_cache_internal_browsertest.cc
  chrome_track_event.proto:
  - changed code (tracing) doesn't exist on M96, discarded
    all changes
  back_forward_cache_browsertest.cc:
  - conflicting includes
  - removed NavigateAndBlock, which would be called on
    on back_forward_cache_browsertest.cc (not present in M96)
  page_handler.cc:
  - conflicting case statements on NotRestoredReasonToProtocol
  back_forward_cache_can_store_document_result.cc:
  - NotRestoredReasonToTraceEnum not present on M96
  - conflicting case statements on NotRestoredReasonToString
  back_forward_cache_metrics.h:
  - conflicting entries for NotRestoredReason enum

In the bug, a crash occurs because we try to cache an interstitial. We
catch some error documents via status codes etc but interstitials do
not consistently set those. Checking IsErrorDocument() is more reliable.

(cherry picked from commit 7a05b426c6c51254a08de9a8dee8db9c1911b9c9)

Bug: 1274308,1287996,1283050
Change-Id: Ifec662c169c77e33ca5dc4d56b0e42c8d71f1d97
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3319862
Commit-Queue: Fergal Daly <fergal@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#981026}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3577265
Reviewed-by: Fergal Daly <fergal@chromium.org>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1592}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/38ab9c5b06a472fcb5105458b2b4037749c50766/content/browser/back_forward_cache_browsertest.cc
[modify] https://crrev.com/38ab9c5b06a472fcb5105458b2b4037749c50766/third_party/blink/public/devtools_protocol/browser_protocol.pdl
[modify] https://crrev.com/38ab9c5b06a472fcb5105458b2b4037749c50766/content/browser/devtools/protocol/page_handler.cc
[modify] https://crrev.com/38ab9c5b06a472fcb5105458b2b4037749c50766/content/browser/renderer_host/back_forward_cache_can_store_document_result.cc
[modify] https://crrev.com/38ab9c5b06a472fcb5105458b2b4037749c50766/content/browser/renderer_host/back_forward_cache_impl.cc
[modify] https://crrev.com/38ab9c5b06a472fcb5105458b2b4037749c50766/content/browser/renderer_host/back_forward_cache_metrics.h


### [Deleted User] (2022-06-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-06-21)

This issue was migrated from crbug.com/chromium/1274308?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Interstitials, UI>Browser>Navigation>BFCache]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058049)*

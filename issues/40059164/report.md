# Security: UAF in SyncConfirmation

| Field | Value |
|-------|-------|
| **Issue ID** | [40059164](https://issues.chromium.org/issues/40059164) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Sandbox>SiteIsolation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2022-03-21 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

Since the flag `--isolation-by-default` (will enable `CrossOriginOpenerPolicyByDefault`[1]) is turned on, COOP's default will shift from `unsafe-none` to `same-origin-allow-popups`, finally lead the mismatch of `initiator_coop` and `destination_coop`[2] (`unsafe-none` vs `same-origin-allow-popups`).

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/features.cc;l=99;drc=c11809b8c0b9fe16955456110c9ec3723b5ff7b5>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/cross_origin_opener_policy_status.cc;l=34;drc=d400fcfcccd5d1fc636d8758fcfa3c9490f37ca5>

The mismatch will eventually lead to `current_site_instance != dest_site_instance`[3], and thus create a WebUI[4] for current pending frame.

`bool use_current_rfh = current_site_instance == dest_site_instance;`

=> use\_current\_rfh = 0

=> branch:

```
if (WebUIControllerFactoryRegistry::GetInstance()->UseWebUIForURL(  
        browser_context, request->common_params().url) &&  
    request->state() < NavigationRequest::CANCELING) {  
  bool created_web_ui = speculative_render_frame_host_->CreateWebUI(  
      request->common_params().url, request->bindings());  
  notify_webui_of_rf_creation =  
      created_web_ui && speculative_render_frame_host_->web_ui();  
}  

```

Turning on sync will construct a SyncConfirmationUI and create a SyncConfirmationHandler[5].  

=> SyncConfirmationUI::InitializeMessageHandlerWithBrowser

[3]. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_manager.cc;l=984;drc=992e3216b7f4b26aef91a2b0d324d59110504781>  

[4]. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_manager.cc;l=1097;drc=992e3216b7f4b26aef91a2b0d324d59110504781>  

[5]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/signin/sync_confirmation_ui.cc;l=101;drc=19de77a492c7ec851885070ecf5142d2a03f9358>

Then CommitPending will unload the current pending frame, and OnUnloaded get called.

```
void RenderFrameHostImpl::OnUnloaded() {  
  DCHECK(is_waiting_for_unload_ack_);  
  
  TRACE_EVENT_NESTABLE_ASYNC_END0("navigation", "RenderFrameHostImpl::Unload",  
                                  TRACE_ID_LOCAL(this));  
  if (unload_event_monitor_timeout_)  
    unload_event_monitor_timeout_->Stop();  
  
  ClearWebUI();  <<<=======================  
  
  bool deleted =  
      frame_tree_node_->render_manager()->DeleteFromPendingList(this);  
  CHECK(deleted);  
}  

```

OnUnloaded will clear the WebUI, destroy the SyncConfirmationHandler and close the SigninViewControllerDelegateViews dialog. Thus destroy current WebContents, and also the current RFH.  

=> ClearWebUI  

=> ~SyncConfirmationHandler  

=> CloseModalSigninWindow [6]  

=> OnSyncConfirmationUIClosed  

=> CloseModalSignin  

=> dialog\_.reset(); [7]  

=> ~SigninViewControllerDelegateViews [8]  

=> ~WebContentsImpl  

=> ~RenderFrameHostImpl -> the speculative frame

Then after the ClearWebUI call completes, return to the next line of code[9] to continue execution:

```
bool deleted =  
      frame_tree_node_->render_manager()->DeleteFromPendingList(this);  

```

Accessing the member variable of the RenderFrameHostImpl will trigger the UAF.

[6]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/signin/sync_confirmation_handler.cc;l=60;drc=91148c1c1e318eb5e5a4b9340fe59e036a3ed15f>  

[7]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/signin_view_controller.cc;l=304;drc=f5401f1b7f4c8b07ac219134888ed05a8a2d8106>  

[8]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/profiles/signin_view_controller_delegate_views.cc;l=379;drc=9cf6cbe7313144f0ec1bf7958104f1204ed5dcd4>  

[9]. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=4814;drc=80fb7252b99d4478d1c2e940d3ccba81fcc14995>

**VERSION**  

Chrome Version: stable with feature flag: CrossOriginOpenerPolicyByDefault  

Operating System: test in linux & win

**REPRODUCTION CASE**

out/asan/chrome --user-data-dir=/tmp/xxxx --isolation-by-default "<http://localhost:8000/poc.html>"

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [asan](attachments/asan) (text/plain, 34.4 KB)
- [poc.html](attachments/poc.html) (text/plain, 21.8 KB)

## Timeline

### [Deleted User] (2022-03-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-03-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6210164499480576.

### cl...@chromium.org (2022-03-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5740511302057984.

### cl...@chromium.org (2022-03-22)

ClusterFuzz testcase 5740511302057984 is closed as invalid, so closing issue.

### le...@gmail.com (2022-03-22)

Since triggering this issue requires account login, I don't think ClusterFuzz will catch it

### le...@gmail.com (2022-03-23)

The WontFix tag seems to be a mistake by ClusterFuzz, can someone reopen this issue?

### am...@chromium.org (2022-03-26)

UAF in the browser process = Critical, but mitigated by account signin, so high severity 

[Monorail components: Services>SignIn]

### am...@chromium.org (2022-03-26)

for signin 

### am...@chromium.org (2022-03-26)

reopening this as it was auto-closed by clusterfuzz as was unable to reproduce since the issue is predicated on account signin; did not attempt to reproduce as of yet but wanted to get some initial triage done on it before the weekend but it *appears* this issue has existed for sometime (so setting to FoundIn-98, since that is current extended stable) 

[Monorail components: Services>Sync]

### am...@chromium.org (2022-03-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2022-03-29)

Note that this UAF requires manually setting the --isolation-by-default flag, so it doesn't affect the general user population. With --isolation-by-default flag enabled, I can reproduce the crash just by enabling Chrome Sync. Chrome crashes even before showing the sync confirmation dialog.

An important detail here is that ~SyncConfrimationHandler() triggers [1] the destruction of a modal dialog that hosts the sync confirmation UI. In other words, Sync Confirmation webUI destruction leads to a synchronous destruction of WebContents that contains the webUI.

The issue is that with --isolation-by-default flag enabled, Chrome hits the RenderFrameHostImpl::OnUnloaded() method [2] which calls ClearWebUI() and then expects the WebContents to be still alive. I'm not sure this is a safe assumption to make. Also, it's weird that the webUI handler gets destroyed before even showing the UI to the user. This behavior will mess with our metrics too. 

Since this is a bug activated by the --isolation-by-default flag, reassigning to the flag owners for evaluation.

[1] https://source.chromium.org/chromium/chromium/src/+/2f3cc1c87bd587a1d065235d661f5a51cbea6f79:chrome/browser/ui/webui/signin/sync_confirmation_handler.cc;l=60
[2] https://source.chromium.org/chromium/chromium/src/+/2f3cc1c87bd587a1d065235d661f5a51cbea6f79:content/browser/renderer_host/render_frame_host_impl.cc;drc=3ed5d3ca63b4c3b397547e931bad196608e6b0a6;l=4825

[Monorail components: Internals>Sandbox>SiteIsolation]

### cl...@chromium.org (2022-03-30)

Thanks! Since this require manually enabling a flag that likely breaks a lot of the internet, the impacted population is probably very low.

That said, synchronously destroying a WebContents is a source of lots of memory bugs in general and should be avoided if possible. Is there a way to postTask the destruction of the WeContents from ~SyncConfirmationHandler()? I think we can add a guard after the ClearWebUI() call in RenderFrameHostImpl::OnUnloaded(), but if we could avoid the synchronous destruction of WebContents that would be good as well, as other bugs may appear.

Assigning to arthursonzogni who has been looking at memory safety issues lately.

### ar...@chromium.org (2022-03-30)

Thanks for the bug report! I will take a look.

We probably should add some logic to prevent Chrome developers to delete WebContents synchronously and instead force them to post a task. This might prevent similar bugs to happen.

I will let amyressler@ adjust the flags if needed, but since this is behind a flag for a feature, this should impact no users: Security_Impact-None


### le...@gmail.com (2022-03-30)

Thanks for the handling. Yes, the Security_Impact should be None, but according to the Severity Guidelines:

> Conversely, we do not consider it a mitigating factor if a vulnerability applies only to a particular group of users. For instance, a Critical vulnerability is still considered Critical even if it applies only to Linux or to those users running with accessibility features enabled.

The Security_Severity may keep High.

### ar...@chromium.org (2022-03-30)

[Comment Deleted]

### ar...@chromium.org (2022-03-30)

I can reproduce, after login in with some google credentials.

Thanks for providing this great reproducer and your analysis!

### ar...@chromium.org (2022-03-30)

[Comment Deleted]

### al...@chromium.org (2022-03-30)

I'm pretty sure it should be possible to avoid destroying WebContents from ~SyncConfirmationHandler() synchronously, if that is discouraged. Should we avoid destroying WebContents synchronously in other cases, like in a button click handler? 

Enforcing these restrictions is a good idea if we want to prevent similar bugs from happening in the future.

Arthur, could you explain to me why RenderFrameHostImpl attempts to destroy WebUI that has never been shown to the user? Is it because Chrome tries to move the webUI into another process? Why is this codepath never hit without the --isolation-by-default flag? At least I don't see any crashes like this in our crash reports.


### ar...@chromium.org (2022-03-30)

> I'm pretty sure it should be possible to avoid destroying WebContents from ~SyncConfirmationHandler() synchronously, if that is discouraged. Should we avoid destroying WebContents synchronously in other cases, like in a button click handler? 

A WebContents owns everything. Destroying a WebContent inside a deep stack might have a lot side effects and the various function callers might not expect "everything" to disappear. We can't reasonably expect everyone to check "Am I still alive?" everytime they call unsuspicious function.

> Arthur, could you explain to me why RenderFrameHostImpl attempts to destroy WebUI that has never been shown to the user? Is it because Chrome tries to move the webUI into another process? Why is this codepath never hit without the --isolation-by-default flag? At least I don't see any crashes like this in our crash reports.

I don't really understand exactly why.


What happens here:

RenderFrameHostImpl::ClearWebUI() releases:
WebUiImpl, which owns:
WebUiMessageHandler, which is implemented by:
SyncConfirmationHandler, which calls:
CloseModalSigninWindow(), which calls:
LoginUIService::SyncConfirmationUIClosed(), which is observed by:
TurnSyncOnHelperDelegateImpl::OnSyncConfirmationUIClosed(), which calls:
SigninViewController::CloseModalSignin(), which calls:
SigninModalDiaglog::CloseModalDialog(), which is implemented by:
SigninReauthViewController::CloseModalDialog(), which causes:
SigninViewControllerDelegateViews::CloseModalSignin() to call "delete this" :-( 
As a views::view, it owned childs which are views::WebViews.


The full stacktrace:
```
0x6220000ab220 is located 288 bytes inside of 4904-byte region [0x6220000ab100,0x6220000ac428)
freed by thread T0 (chrome) here:
    #0 0x559d7466583d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x559d7c6e056d in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #2 0x559d7c6e056d in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #3 0x559d7c6e056d in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #4 0x559d7c6e056d in destroy<std::__1::unique_ptr<content::RenderFrameHostImpl, std::__1::default_delete<content::RenderFrameHostImpl> >, void, void> buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:318:15
    #5 0x559d7c6e056d in std::__1::__tree<std::__1::unique_ptr<content::RenderFrameHostImpl, std::__1::default_delete<content::RenderFrameHostImpl> >, base::UniquePtrComparator, std::__1::allocator<std::__1::unique_ptr<content::RenderFrameHostImpl, std::__1::default_delete<content::RenderFrameHostImpl> > > >::destroy(std::__1::__tree_node<std::__1::unique_ptr<content::RenderFrameHostImpl, std::__1::default_delete<content::RenderFrameHostImpl> >, void*>*) buildtools/third_party/libc++/trunk/include/__tree:1801:9
    #6 0x559d7c6c9953 in clear buildtools/third_party/libc++/trunk/include/__tree:1838:5
    #7 0x559d7c6c9953 in clear buildtools/third_party/libc++/trunk/include/set:707:37
    #8 0x559d7c6c9953 in content::RenderFrameHostManager::ClearRFHsPendingShutdown() content/browser/renderer_host/render_frame_host_manager.cc:886:25
    #9 0x559d7c298ab1 in content::FrameTree::Shutdown() content/browser/renderer_host/frame_tree.cc:843:29
    #10 0x559d7ccab681 in content::WebContentsImpl::~WebContentsImpl() content/browser/web_contents/web_contents_impl.cc:1070:23
    #11 0x559d7ccae1bd in content::WebContentsImpl::~WebContentsImpl() content/browser/web_contents/web_contents_impl.cc:1016:37
    #12 0x559d95bd4aa0 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #13 0x559d95bd4aa0 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #14 0x559d95bd4aa0 in views::WebView::SetWebContents(content::WebContents*) ui/views/controls/webview/webview.cc:106:15
    #15 0x559d95bd46b7 in views::WebView::~WebView() ui/views/controls/webview/webview.cc:74:3
    #16 0x559d95bd4e9d in views::WebView::~WebView() ui/views/controls/webview/webview.cc:72:21
    #17 0x559d935f02ae in views::View::~View() ui/views/view.cc:254:9
    #18 0x559d935f13fd in views::View::~View() ui/views/view.cc:227:15
    #19 0x559d935f02ae in views::View::~View() ui/views/view.cc:254:9
    #20 0x559d936935f4 in views::DialogDelegateView::~DialogDelegateView() ui/views/window/dialog_delegate.cc:475:41
    #21 0x559d94b1b2fa in ~SigninViewControllerDelegateViews chrome/browser/ui/views/profiles/signin_view_controller_delegate_views.cc:302:71
    #22 0x559d94b1b2fa in SigninViewControllerDelegateViews::~SigninViewControllerDelegateViews() chrome/browser/ui/views/profiles/signin_view_controller_delegate_views.cc:302:71
    #23 0x559d94ae6f4d in SigninViewController::CloseModalSignin() chrome/browser/ui/signin_view_controller.cc:292:14
    #24 0x559d94c273e2 in TurnSyncOnHelperDelegateImpl::OnSyncConfirmationUIClosed(LoginUIService::SyncConfirmationUIClosedResult) chrome/browser/ui/webui/signin/turn_sync_on_helper_delegate_impl.cc:185:41
    #25 0x559d94a8b611 in LoginUIService::SyncConfirmationUIClosed(LoginUIService::SyncConfirmationUIClosedResult) chrome/browser/ui/webui/signin/login_ui_service.cc:53:14
    #26 0x559d94b56a1e in CloseModalSigninWindow chrome/browser/ui/webui/signin/sync_confirmation_handler.cc:216:51
    #27 0x559d94b56a1e in SyncConfirmationHandler::~SyncConfirmationHandler() chrome/browser/ui/webui/signin/sync_confirmation_handler.cc:60:5
    #28 0x559d94b56bdd in SyncConfirmationHandler::~SyncConfirmationHandler() chrome/browser/ui/webui/signin/sync_confirmation_handler.cc:53:53
    #29 0x559d7cee0272 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #30 0x559d7cee0272 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #31 0x559d7cee0272 in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #32 0x559d7cee0272 in destroy buildtools/third_party/libc++/trunk/include/__memory/allocator.h:133:15
    #33 0x559d7cee0272 in destroy<std::__1::unique_ptr<content::WebUIMessageHandler, std::__1::default_delete<content::WebUIMessageHandler> >, void> buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:308:13
    #34 0x559d7cee0272 in __destruct_at_end buildtools/third_party/libc++/trunk/include/vector:429:9
    #35 0x559d7cee0272 in clear buildtools/third_party/libc++/trunk/include/vector:372:29
    #36 0x559d7cee0272 in ~__vector_base buildtools/third_party/libc++/trunk/include/vector:466:9
    #37 0x559d7cee0272 in ~vector buildtools/third_party/libc++/trunk/include/vector:558:5
    #38 0x559d7cee0272 in content::WebUIImpl::~WebUIImpl() content/browser/webui/web_ui_impl.cc:85:1
    #39 0x559d7cee064d in content::WebUIImpl::~WebUIImpl() content/browser/webui/web_ui_impl.cc:79:25
    #40 0x559d7c5c333d in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #41 0x559d7c5c333d in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #42 0x559d7c5c333d in ClearWebUI content/browser/renderer_host/render_frame_host_impl.cc:9042:11
    #43 0x559d7c5c333d in content::RenderFrameHostImpl::OnUnloaded() content/browser/renderer_host/render_frame_host_impl.cc:4833:3
    #44 0x559d7c601815 in PendingDeletionCheckCompleted content/browser/renderer_host/render_frame_host_impl.cc:8078:7
    #45 0x559d7c601815 in content::RenderFrameHostImpl::OnUnloadACK() content/browser/renderer_host/render_frame_host_impl.cc:4822:3

```

### ar...@chromium.org (2022-03-30)

I have a fix. In views::Webview, defer deleteing the Webview:

-  if (wc_owner_.get() != replacement)
-    wc_owner_.reset();

+  if (wc_owner_.get() != replacement) {
+    // A WebContent must be deleted in its own task, because this task's stack
+    // might be deep. There are many callers who are likely owned by this
+    // WebContents that might not expect everything to disappear.
+    base::ThreadTaskRunnerHandle::Get()->DeleteSoon(FROM_HERE,
+                                                    std::move(wc_owner_));
+  }
+

We should probably make some logic to disallow folks from deleting WebContent directly. I will take a look how to achieve this. This will likely not be possible immediately, given the current usages.

### ar...@chromium.org (2022-03-31)

Fix:https://chromium-review.googlesource.com/c/chromium/src/+/3560577

+CC reviewer sadrul@ for the context. 

### ar...@chromium.org (2022-04-08)

Hello @alexilin or @droger.

I would need your help about the ProfileDestroyer.

I get this error:
```
[FATAL:browser_context_impl.cc(98)] Check failed: false. rph_with_bc_reference : {  pl='{ chrome://signin-dice-web-intercept/ }' lsn=2[RFHI:LoadInitialURL@ui/views/controls/webview/webview.cc:136] }
#0 0x5597061983b9 base::debug::CollectStackTrace()
#1 0x559706095ca3 base::debug::StackTrace::StackTrace()
#2 0x5597060b0150 logging::LogMessage::~LogMessage()
#3 0x5597060b0c1e logging::LogMessage::~LogMessage()
#4 0x55970322fde3 content::BrowserContextImpl::~BrowserContextImpl()
#5 0x55970322dd13 content::BrowserContext::~BrowserContext()
#6 0x5597040dd246 Profile::~Profile()
#7 0x559706473bc3 ProfileImpl::~ProfileImpl()
#8 0x559706473c1e ProfileImpl::~ProfileImpl()
#9 0x55970646f261 ProfileDestroyer::DestroyOriginalProfileNow()
#10 0x55970646eee3 ProfileDestroyer::DestroyProfileWhenAppropriate()
```


The ProfileDestroyer destroy the Profile. The profil is a BrowserContextImpl. It checks there are no RenderProcessHost referencing this BrowserContext.
The profileDestroyer normally waits for every RenderProcessHost to be destroyed, but only for off_the_profile ones. See:
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/profiles/profile_destroyer.cc;l=63-66?q=DestroyProfileWhenAppropriate&ss=chromium

This looks incorrect to me, so I tried making the ProfileDestroyer to consistently wait for every RendererProcessHost to be released before releasing the Profile:
https://chromium-review.googlesource.com/c/chromium/src/+/3560577/8

But this makes even more tests to fail.

Would you have some context about why the ProfileDestroyer is working this way?

### al...@chromium.org (2022-04-08)

+nicolaso@ for https://crbug.com/chromium/1308391#c24

### ni...@chromium.org (2022-04-08)

> The profileDestroyer normally waits for every RenderProcessHost to be destroyed, but only for off_the_profile ones.

ProfileDestroyer was implemented like this back when we didn't destroy non-OTR profiles prior to shutdown. We only added a wait for OTR profiles, because they can be destroyed earlier than regular profiles (and dangling RPHs can cause other bugs).

So we added the up-to-1-second wait to work around issues. See crbug.com/112383 (10-year-old bug).

With DestroyProfileOnBrowserClose, it's not true that *only* OTR profiles are destroyed prior to shutdown. So, it makes sense to add the up-to-1-second wait for those as well.

> This looks incorrect to me, so I tried making the ProfileDestroyer to consistently wait for every RendererProcessHost to be released before releasing the Profile

I agree that unifying the OTR/non-OTR codepaths is a good goal. This is especially important if we delete WebContents in a task, as suggested in crbug.com/1311962.

TBH I *think* this could cause race conditions, so we should be extra careful. Specifically, calling ProfileManager::LoadProfile() after ProfileDestroyer::DestroyProfileWhenAppropriate(). We could end up with 2 Profile objects active at the same time, for the same profile dir. Those will be hard to repro, debug, and fix. What happens if e.g. the new Profile tries to acquire a lock on the Preferences file?

> But this makes even more tests to fail.

Those stack traces in the failing tests look a bit weird. They're jumping all over the place: why does calling ObserverList::AddObserver() trigger a DCHECK in ~ObserverList, for instance? Maybe the cause will be clearer if you run those tests locally with a debug build.

### gi...@appspot.gserviceaccount.com (2022-04-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/139dd2fbf56a30009b4009be48735b878e5e7413

commit 139dd2fbf56a30009b4009be48735b878e5e7413
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Mon Apr 11 09:04:31 2022

ProfileDestroyer refactor [1/N]

While I am failing to make progress on:
https://chromium-review.googlesource.com/c/chromium/src/+/3560577 there
are still some refactoring I would be happy to preserve, so let's start
branch a small refactoring. Maybe this will make it easier

[1/N]: Turn the global |pending_destroyers_| pointer into a function
with a static base::Nodestructor. This is the recommended way to create
global singleton. This also avoid caring about whether the pointer is
null or not.

Bug: 1308391
Change-Id: I4b4a7250bd8f4aaaec7d3dfc9dbaafd0fbce49cb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3574653
Reviewed-by: Alex Ilin <alexilin@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/main@{#990932}

[modify] https://crrev.com/139dd2fbf56a30009b4009be48735b878e5e7413/chrome/browser/profiles/profile_destroyer.cc
[modify] https://crrev.com/139dd2fbf56a30009b4009be48735b878e5e7413/chrome/browser/profiles/profile_destroyer.h


### ar...@chromium.org (2022-04-11)

> Those stack traces in the failing tests look a bit weird. They're jumping all over the place: why does calling ObserverList::AddObserver() trigger a DCHECK in ~ObserverList, for instance? Maybe the cause will be clearer if you run those tests locally with a debug build.

Here are two stacktraces.
They correspond:
1. When the observer (SchemaRegistryTrackingPolicyProvider) starts observing (ConfigurationPolicyProvider).
2. When the observed is deleted, prior to its observer.

You can see the ProfileImpl is the cause of the observation. Unfortunately it hasn't been deleted yet when the BrowserProcessImpl shutdown.

#1 0x55ec6d52b3f3 base::debug::StackTrace::StackTrace()
#2 0x55ec671c4ec8 base::ObserverList<>::AddObserver()
#3 0x55ec6a395326 policy::SchemaRegistryTrackingPolicyProvider::SchemaRegistryTrackingPolicyProvider()
#4 0x55ec6d88822f policy::ProfilePolicyConnector::AppendPolicyProviderWithSchemaTracking()
#5 0x55ec6d887eed policy::ProfilePolicyConnector::Init()
#6 0x55ec6d888952 policy::CreateAndInitProfilePolicyConnector()
#7 0x55ec6d907bcb ProfileImpl::LoadPrefsForNormalStartup()
#8 0x55ec6d907727 ProfileImpl::ProfileImpl()
#9 0x55ec6d906b96 Profile::CreateProfile()
#10 0x55ec6d91357f ProfileManager::CreateProfileAsync()
#11 0x55ec6a66a9fe base::internal::Invoker<>::RunOnce()
#12 0x55ec6d5b43e9 base::TaskAnnotator::RunTaskImpl()
#13 0x55ec6d5e1df0 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()
#14 0x55ec6d5e13be base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#15 0x55ec6d5e28e2 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#16 0x55ec6d55feb3 base::MessagePumpGlib::Run()
#17 0x55ec6d5e30d0 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#18 0x55ec6d591fee base::RunLoop::Run()
#19 0x55ec6825ddc0 DiceWebSigninInterceptionBubbleBrowserTest_ProfileKeepAlive_Test::RunTestOnMainThread()
#20 0x55ec6e04aa6e content::BrowserTestBase::ProxyRunTestOnMainThreadLoop()
#21 0x55ec6a6968e0 content::BrowserMainLoop::RunMainMessageLoop()
#22 0x55ec6a6986e2 content::BrowserMainRunnerImpl::Run()
#23 0x55ec6a693e4b content::BrowserMain()
#24 0x55ec6b88ec55 content::RunBrowserProcessMain()
#25 0x55ec6b89105f content::ContentMainRunnerImpl::RunBrowser()
#26 0x55ec6b89077b content::ContentMainRunnerImpl::Run()
#27 0x55ec6b88d1a7 content::RunContentProcess()
#28 0x55ec6b88d28e content::ContentMain()
#29 0x55ec6e049e3b content::BrowserTestBase::SetUp()
#30 0x55ec6d505738 InProcessBrowserTest::SetUp()
#31 0x55ec68c90100 testing::Test::Run()
#32 0x55ec68c9169f testing::TestInfo::Run()
#33 0x55ec68c92407 testing::TestSuite::Run()
#34 0x55ec68ca5007 testing::internal::UnitTestImpl::RunAllTests()
#35 0x55ec68ca499e testing::UnitTest::Run()
#36 0x55ec6d6ab07c base::TestSuite::Run()
#37 0x55ec6d4b68e2 ChromeTestSuiteRunner::RunTestSuite()
#38 0x55ec6d4b6baa ChromeTestLauncherDelegate::RunTestSuite()
#39 0x55ec6e0c2b4a content::LaunchTests()
#40 0x55ec6d4b6ec4 LaunchChromeTests()
#41 0x55ec6d4b0a25 main
#42 0x7fcde9d767fd __libc_start_main
#43 0x55ec664b21ea _start


#0 0x55ec6d62c739 base::debug::CollectStackTrace()
#1 0x55ec6d52b3f3 base::debug::StackTrace::StackTrace()
#2 0x55ec6d5451f0 logging::LogMessage::~LogMessage()
#3 0x55ec6d545cbe logging::LogMessage::~LogMessage()
#4 0x55ec6865ba10 base::ObserverList<>::~ObserverList()
#5 0x55ec6a372be8 policy::ConfigurationPolicyProvider::~ConfigurationPolicyProvider()
#6 0x55ec6a382c7c policy::ProxyPolicyProvider::~ProxyPolicyProvider()
#7 0x55ec6a382cee policy::ProxyPolicyProvider::~ProxyPolicyProvider()
#8 0x55ec6a326f40 policy::BrowserPolicyConnectorBase::~BrowserPolicyConnectorBase()
#9 0x55ec6d882786 policy::ChromeBrowserPolicyConnector::~ChromeBrowserPolicyConnector()
#10 0x55ec6d88283e policy::ChromeBrowserPolicyConnector::~ChromeBrowserPolicyConnector()
#11 0x55ec6d713051 BrowserProcessImpl::~BrowserProcessImpl()
#12 0x55ec6d71314e BrowserProcessImpl::~BrowserProcessImpl()
#13 0x55ec6d79b01c browser_shutdown::ShutdownPostThreadsStop()
#14 0x55ec6d711d18 ChromeBrowserMainParts::PostDestroyThreads()
#15 0x55ec6a697001 content::BrowserMainLoop::ShutdownThreadsAndCleanUp()
#16 0x55ec6a698809 content::BrowserMainRunnerImpl::Shutdown()
#17 0x55ec6a693e57 content::BrowserMain()
#18 0x55ec6b88ec55 content::RunBrowserProcessMain()
#19 0x55ec6b89105f content::ContentMainRunnerImpl::RunBrowser()
#20 0x55ec6b89077b content::ContentMainRunnerImpl::Run()
#21 0x55ec6b88d1a7 content::RunContentProcess()
#22 0x55ec6b88d28e content::ContentMain()
#23 0x55ec6e049e3b content::BrowserTestBase::SetUp()
#24 0x55ec6d505738 InProcessBrowserTest::SetUp()
#25 0x55ec68c90100 testing::Test::Run()
#26 0x55ec68c9169f testing::TestInfo::Run()
#27 0x55ec68c92407 testing::TestSuite::Run()
#28 0x55ec68ca5007 testing::internal::UnitTestImpl::RunAllTests()
#29 0x55ec68ca499e testing::UnitTest::Run()
#30 0x55ec6d6ab07c base::TestSuite::Run()
#31 0x55ec6d4b68e2 ChromeTestSuiteRunner::RunTestSuite()
#32 0x55ec6d4b6baa ChromeTestLauncherDelegate::RunTestSuite()
#33 0x55ec6e0c2b4a content::LaunchTests()
#34 0x55ec6d4b6ec4 LaunchChromeTests()
#35 0x55ec6d4b0a25 main
#36 0x7fcde9d767fd __libc_start_main
#37 0x55ec664b21ea _start


### ar...@chromium.org (2022-04-12)

@nicolaso, I found the problem. FYI.

### ni...@chromium.org (2022-04-12)

Ah, I see now. So the problem is that profile destruction can happen during shutdown, and adding the delay causes other objects to get deleted first.'

This isn't a problem w/ Incognito currently, because we do DestroyOffTheRecordProfileNow() in ~ProfileImpl [1], rather than ...WhenAppropriate().

We would need DestroyProfileWhenAppropriate to skip the 1-second wait if it's called during shutdown. I think we can check BrowserProcess::IsShuttingDown().

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/profiles/profile_impl.cc;l=892-893;drc=14b836593fe9608129fd06679467c8b43e6df944

### ar...@google.com (2022-04-14)

Thanks nicolaso@!

Yes. Also, I believe I would also have to force delete all the profile pending destruction during shutdown.

I will try..

### gi...@appspot.gserviceaccount.com (2022-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/976353b521bbff373b1699fbac1456cca52a4918

commit 976353b521bbff373b1699fbac1456cca52a4918
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Fri Apr 29 14:51:34 2022

ProfileDestroyer refactor [2/N]

Due to multiple issues in chrome/ I am failing to make progress on:
https://chromium-review.googlesource.com/c/chromium/src/+/3560577

On issue I got: the TestingProfile is running the IO loop in its
own destructor. This is a bad practice, because it causes complex call
stack to appear. In my case, I was deleting the profile, while deleting
the profile.

This patch:
- Removes running the loop in the destructor.
- Adapt tests relying on this delay.
- Remove unused field "extensions_cookie_store"
- Adapt test relying on removed transitive inclusions.

Bug: 1308391
Change-Id: I2c008bdd87cfce37d5d0e549d10cadf941200563
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3599175
Reviewed-by: David Roger <droger@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/main@{#997705}

[modify] https://crrev.com/976353b521bbff373b1699fbac1456cca52a4918/chrome/browser/ash/plugin_vm/plugin_vm_util_unittest.cc
[modify] https://crrev.com/976353b521bbff373b1699fbac1456cca52a4918/chrome/browser/browsing_data/cookies_tree_model_unittest.cc
[modify] https://crrev.com/976353b521bbff373b1699fbac1456cca52a4918/chrome/test/base/testing_profile.h
[modify] https://crrev.com/976353b521bbff373b1699fbac1456cca52a4918/chrome/test/base/testing_profile.cc
[modify] https://crrev.com/976353b521bbff373b1699fbac1456cca52a4918/chrome/browser/download/download_prefs_unittest.cc


### an...@chromium.org (2022-05-06)

Issue has both Severity-High and Low labels attached. Removing the latter as this still a browser UAF with admittedly mitigating factors (requires flag to be enabled).

### gi...@appspot.gserviceaccount.com (2022-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0838c1133261472b0ad4ba5a7ac8acabab8fc9dd

commit 0838c1133261472b0ad4ba5a7ac8acabab8fc9dd
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Mon May 09 13:09:50 2022

Cleanup ~Browser() weakptr invalidation.

Running a loop in TestingProfile is a bad practise, with complex and
unpredictable side effects. I removed it previously:
https://chromium-review.googlesource.com/c/chromium/src/+/3599175

I just found in ~Browser() some code to mitigate the previous issue, by
invalidating weakptr. Since the primary cause is gone, it should be in
theory possible to remove the mitigation.

Bug: 1308391,1311962
Change-Id: Ide0a02395353ce7edc54150140689c524e35dbd1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3634380
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: David Roger <droger@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1000973}

[modify] https://crrev.com/0838c1133261472b0ad4ba5a7ac8acabab8fc9dd/chrome/browser/ui/browser.cc


### gi...@appspot.gserviceaccount.com (2022-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ca1f263790291eaffe0b99cabe56e0217a642dac

commit ca1f263790291eaffe0b99cabe56e0217a642dac
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Mon May 09 15:16:21 2022

Close ExtensionsHosts directly in test.

In order to close the ExtensionHosts as a side effect, this test was
deleting its profile instead.

Why not going straight to the point? That's what this patch does.

[Motivation]:
This is a prerequisite to patch:
https://chromium-review.googlesource.com/c/chromium/src/+/3560577
Here, destroying the profile might now happen in a different task and be
delayed. We need either to apply this patch, or to manually add some
logic to exhaust pending tasks for the deletion to happens.

Bug: 1308391
Change-Id: Ic8b928a798adcf5243bde60b9b0f2a8c4dd8da44
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3634377
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1001018}

[modify] https://crrev.com/ca1f263790291eaffe0b99cabe56e0217a642dac/chrome/browser/ash/power/extension_event_observer_unittest.cc


### ar...@chromium.org (2022-05-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-05-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/300c3dba1de899fc32a29cd6edb005720956bbb9

commit 300c3dba1de899fc32a29cd6edb005720956bbb9
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Fri May 13 16:17:39 2022

Fix dangling raw_ptr in TabStripPageHandler / WebuiTabStrip.

The |browser_| and |embedder_| attributes from the TabStripPageHandler
might become dangling. This may results in UAF.

This patch resets the borrowed references and clear the objects
depending on them when they go out of scope.

[Motivation]
This is a dependency of:
https://chromium-review.googlesource.com/c/chromium/src/+/3620393
This deletes WebContents in its own task, which causes the dangling
raw_ptr to become real UAF and one test to fail.

Bug: 1308391,1311962
Change-Id: I1c56052069de76e304502bf76108d79e2236b2c1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3634520
Reviewed-by: Thomas Lukaszewicz <tluk@chromium.org>
Reviewed-by: Collin Baker <collinbaker@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: John Lee <johntlee@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1003148}

[modify] https://crrev.com/300c3dba1de899fc32a29cd6edb005720956bbb9/chrome/browser/ui/views/frame/webui_tab_strip_container_view.cc
[modify] https://crrev.com/300c3dba1de899fc32a29cd6edb005720956bbb9/chrome/browser/ui/webui/tab_strip/tab_strip_ui.cc
[modify] https://crrev.com/300c3dba1de899fc32a29cd6edb005720956bbb9/chrome/browser/ui/webui/tab_strip/tab_strip_ui.h
[modify] https://crrev.com/300c3dba1de899fc32a29cd6edb005720956bbb9/chrome/browser/ui/views/frame/webui_tab_strip_container_view.h


### ma...@google.com (2022-06-01)

Friendly security marshal ping. Does the above commit fix this issue? If so, could you please mark the bug as fixed? Thanks!

### th...@chromium.org (2022-06-09)

Security marshal here. arthursonzogni@, is there any work remaining here, or can this ticket be closed? (will ping as well)

### ar...@chromium.org (2022-06-09)

No, this bug has not been fixed at all.

We can "hide" pretty easily this particular bug by checking whether or not we have "mysteriously" been deleted when calling this function. However this would just fix this occurrence of the bug, not the root cause. That would be quite useless.

I am trying to fix the root cause, by making this branch of patches:
- https://chromium-review.googlesource.com/c/chromium/src/+/3599175 [Landed]
- https://chromium-review.googlesource.com/c/chromium/src/+/3634380 [Landed]
- https://chromium-review.googlesource.com/c/chromium/src/+/3634377 [Landed]
- https://chromium-review.googlesource.com/c/chromium/src/+/3634520 [Landed]
- https://chromium-review.googlesource.com/c/chromium/src/+/3560577 [Waiting for branch cut]
- https://chromium-review.googlesource.com/c/chromium/src/+/3620393 [WIP]

Chrome looks quite fragile when this is about the lifetime of Profile and WebContents.
The last two patches are improving the situation, but they might as well impact the stability. I am waiting for branch cut before landing them, to give us some time to revert them if needed.

### gi...@appspot.gserviceaccount.com (2022-06-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8fe068c8aba38d7a7cd64f010723a704ac893147

commit 8fe068c8aba38d7a7cd64f010723a704ac893147
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Fri Jun 10 08:56:38 2022

Unify/Correct ProfileDestroyer implementation.

This patch is a dependency of:
https://chromium-review.googlesource.com/c/chromium/src/+/3620393/1
were WebContents destruction are going to be deferred into a new task.

The ProfileDestroyer currently has several problems:
1. Depending on whether the profile is an incognito one or not,
   the profile is either destroyed immediately or we wait for the
   associated RenderProcessHost to shutdown first.
2. The ProfileDestroyer assert there are no remaining RenderProcessHost
   associated with a Profile. However, (1) do not provide this
   guarantee for non-incognito profiles.
3. The implementation doesn't wait for RenderProcess Shutdown when they
   have been added in between calling the ProfileDestroyer and
   destroying the profile.

This patch unify the Incognito/Normal profile destruction. It also make
the ProfileDestroyer to take into account new RenderProcessHost.

Change-Id: Ia28f384502bfd57466fca94a0234e325984139ef
Bug: 1308391,1311962
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3560577
Reviewed-by: David Roger <droger@chromium.org>
Reviewed-by: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1012863}

[modify] https://crrev.com/8fe068c8aba38d7a7cd64f010723a704ac893147/chrome/browser/profiles/profile_destroyer.cc
[modify] https://crrev.com/8fe068c8aba38d7a7cd64f010723a704ac893147/chrome/browser/profiles/profile_manager.cc
[modify] https://crrev.com/8fe068c8aba38d7a7cd64f010723a704ac893147/chrome/test/base/testing_profile_manager.cc
[modify] https://crrev.com/8fe068c8aba38d7a7cd64f010723a704ac893147/chrome/browser/ui/views/bubble/webui_bubble_manager_unittest.cc
[modify] https://crrev.com/8fe068c8aba38d7a7cd64f010723a704ac893147/chrome/browser/browser_process_impl.h
[modify] https://crrev.com/8fe068c8aba38d7a7cd64f010723a704ac893147/chrome/browser/profiles/profile_destroyer.h
[modify] https://crrev.com/8fe068c8aba38d7a7cd64f010723a704ac893147/chrome/browser/profiles/profile_destroyer_unittest.cc


### gi...@appspot.gserviceaccount.com (2022-06-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9a238378e74253bae14b97efc76e7c6df1ec3c3b

commit 9a238378e74253bae14b97efc76e7c6df1ec3c3b
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Tue Jun 21 11:25:07 2022

Revert "Unify/Correct ProfileDestroyer implementation."

This reverts commit 8fe068c8aba38d7a7cd64f010723a704ac893147.

Reason for revert: We believe it might be the cause of:
https://crbug.com/1337388

Original change's description:
> Unify/Correct ProfileDestroyer implementation.
>
> This patch is a dependency of:
> https://chromium-review.googlesource.com/c/chromium/src/+/3620393/1
> were WebContents destruction are going to be deferred into a new task.
>
> The ProfileDestroyer currently has several problems:
> 1. Depending on whether the profile is an incognito one or not,
>    the profile is either destroyed immediately or we wait for the
>    associated RenderProcessHost to shutdown first.
> 2. The ProfileDestroyer assert there are no remaining RenderProcessHost
>    associated with a Profile. However, (1) do not provide this
>    guarantee for non-incognito profiles.
> 3. The implementation doesn't wait for RenderProcess Shutdown when they
>    have been added in between calling the ProfileDestroyer and
>    destroying the profile.
>
> This patch unify the Incognito/Normal profile destruction. It also make
> the ProfileDestroyer to take into account new RenderProcessHost.
>
> Change-Id: Ia28f384502bfd57466fca94a0234e325984139ef
> Bug: 1308391,1311962
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3560577
> Reviewed-by: David Roger <droger@chromium.org>
> Reviewed-by: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
> Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1012863}

Bug: 1308391,1311962
Change-Id: I299d0a98b1ff3e3fe542933cee347dc45679f62c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3714253
Reviewed-by: David Roger <droger@chromium.org>
Reviewed-by: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Auto-Submit: Arthur Sonzogni <arthursonzogni@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1016128}

[modify] https://crrev.com/9a238378e74253bae14b97efc76e7c6df1ec3c3b/chrome/browser/profiles/profile_destroyer.cc
[modify] https://crrev.com/9a238378e74253bae14b97efc76e7c6df1ec3c3b/chrome/browser/profiles/profile_manager.cc
[modify] https://crrev.com/9a238378e74253bae14b97efc76e7c6df1ec3c3b/chrome/test/base/testing_profile_manager.cc
[modify] https://crrev.com/9a238378e74253bae14b97efc76e7c6df1ec3c3b/chrome/browser/ui/views/bubble/webui_bubble_manager_unittest.cc
[modify] https://crrev.com/9a238378e74253bae14b97efc76e7c6df1ec3c3b/chrome/browser/profiles/profile_destroyer.h
[modify] https://crrev.com/9a238378e74253bae14b97efc76e7c6df1ec3c3b/chrome/browser/browser_process_impl.h
[modify] https://crrev.com/9a238378e74253bae14b97efc76e7c6df1ec3c3b/chrome/browser/profiles/profile_destroyer_unittest.cc


### gi...@appspot.gserviceaccount.com (2022-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cf2ba42acf6977eb009c5d93625d343e6dce6eed

commit cf2ba42acf6977eb009c5d93625d343e6dce6eed
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Thu Jun 23 14:11:33 2022

Reland "Unify/Correct ProfileDestroyer implementation."

It got reverted in:
https://chromium-review.googlesource.com/c/chromium/src/+/3714253

The problem was that an OTR profile destruction is requested from two
locations:
-PresentationReceiverWindowController::~PresentationReceiverWindowController
- ProfileManager::~ProfileManager()

To solve this, we follow @nicolaso advice:
https://bugs.chromium.org/p/chromium/issues/detail?id=1337388#c12

We allow two requests to destroy the same profile. The first request
is canceled and replaced by the new one.

See the diff in between patchset 1 and N for what has been added in the reland:
https://chromium-review.googlesource.com/c/chromium/src/+/3714294/1..2

> Unify/Correct ProfileDestroyer implementation.
>
> This patch is a dependency of:
> https://chromium-review.googlesource.com/c/chromium/src/+/3620393/1
> were WebContents destruction are going to be deferred into a new task.
>
> The ProfileDestroyer currently has several problems:
> 1. Depending on whether the profile is an incognito one or not,
>    the profile is either destroyed immediately or we wait for the
>    associated RenderProcessHost to shutdown first.
> 2. The ProfileDestroyer assert there are no remaining RenderProcessHost
>    associated with a Profile. However, (1) do not provide this
>    guarantee for non-incognito profiles.
> 3. The implementation doesn't wait for RenderProcess Shutdown when they
>    have been added in between calling the ProfileDestroyer and
>    destroying the profile.
>
> This patch unify the Incognito/Normal profile destruction. It also make
> the ProfileDestroyer to take into account new RenderProcessHost.
>
> Change-Id: Ia28f384502bfd57466fca94a0234e325984139ef
> Bug: 1308391,1311962
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3560577


Bug: 1308391,1311962,1337388
Change-Id: I4963c99b47ac125a5a30dcbcabe096dc3718cae6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3714294
Reviewed-by: David Roger <droger@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1017147}

[modify] https://crrev.com/cf2ba42acf6977eb009c5d93625d343e6dce6eed/chrome/browser/profiles/profile_destroyer.cc
[modify] https://crrev.com/cf2ba42acf6977eb009c5d93625d343e6dce6eed/chrome/browser/profiles/profile_manager.cc
[modify] https://crrev.com/cf2ba42acf6977eb009c5d93625d343e6dce6eed/chrome/test/base/testing_profile_manager.cc
[modify] https://crrev.com/cf2ba42acf6977eb009c5d93625d343e6dce6eed/chrome/browser/ui/views/bubble/webui_bubble_manager_unittest.cc
[modify] https://crrev.com/cf2ba42acf6977eb009c5d93625d343e6dce6eed/chrome/browser/browser_process_impl.h
[modify] https://crrev.com/cf2ba42acf6977eb009c5d93625d343e6dce6eed/chrome/browser/profiles/profile_destroyer.h
[modify] https://crrev.com/cf2ba42acf6977eb009c5d93625d343e6dce6eed/chrome/browser/profiles/profile_destroyer_unittest.cc


### ar...@google.com (2022-06-25)

[Empty comment from Monorail migration]

### ar...@chromium.org (2022-07-04)

Update: I am just waiting for a code review: https://chromium-review.googlesource.com/c/chromium/src/+/3726457

### gi...@appspot.gserviceaccount.com (2022-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/56fbd269ba6ad5387aa58ca75bc230f0be7250e0

commit 56fbd269ba6ad5387aa58ca75bc230f0be7250e0
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Thu Jul 07 10:24:32 2022

Guard against ClearWebUI() side effect.

ClearWebUI() delete some objects owned by content's embedders. This may
indirectly cause the deletion of the WebContent and |this|.

An alternative considered was to protect against content embedder
deleting synchronously the WebContent.
https://chromium-review.googlesource.com/c/chromium/src/+/3620393

Change-Id: I77f457ef9e9e2da95040e0a2304bcb5caaf4e204
Bug: 1308391
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3726457
Reviewed-by: Camille Lamy <clamy@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1021599}

[modify] https://crrev.com/56fbd269ba6ad5387aa58ca75bc230f0be7250e0/content/browser/renderer_host/render_frame_host_impl.h
[modify] https://crrev.com/56fbd269ba6ad5387aa58ca75bc230f0be7250e0/content/browser/webui/web_ui_browsertest.cc
[modify] https://crrev.com/56fbd269ba6ad5387aa58ca75bc230f0be7250e0/content/browser/renderer_host/render_frame_host_impl.cc


### ar...@google.com (2022-07-07)

It has been fixed.

The only reproducer we know requires enabling a feature flag. So, I believe we can wait for a standard (canary->dev->beta->stable) progression without asking for cherry-picking.

### [Deleted User] (2022-07-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-07)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-13)

Congratulations, Leecraso and Guang Gong! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts and great work on another one! 

### am...@google.com (2022-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1308391?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, Services>SignIn, Services>Sync]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059164)*

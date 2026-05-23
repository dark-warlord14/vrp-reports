# Regression: Chrome crashes when "No thanks" link is dropped in any text-boxes on Chrome sign-in page.

| Field | Value |
|-------|-------|
| **Issue ID** | [40081470](https://issues.chromium.org/issues/40081470) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | js...@etouch.net |
| **Assignee** | no...@chromium.org |
| **Created** | 2015-02-20 |
| **Bounty** | Confirmed (amount unknown) |

## Description

Chrome Version: 42.0.2309.2 (Official Build) canary (64-bit)bb00754a11e3beaea6dbf887dd52b255eaca88d1-refs/branch-heads/2309@{#5}-32/64-bit.  

OS: All (Win 7 - Aero enabled)

**What steps will reproduce the problem?**

1. Launch chrome, go to chrome sign-in page i.e. chrome://chrome-signin/?source=0
2. Now drag "No thanks" link and drop it in 'Email' or 'Password' text-box
3. Observe

Chrome browser crashes. Crash id: 42499cb87bd80b65 (Chrome).

Browser should not crash.

This is an regression issue, broken in M-42 series and below is the narrow bisect info:  

<https://chromium.googlesource.com/chromium/src/+log/a7dc2b4e44a79d4cdb5cb81fa14b44b63a5ac3ea..fb08a0fa2c10544e102bcadeadd08c6815055752?pretty=fuller&n=100>

Suspecting - r316600

## Attachments

- [Actual_Crash.m4v](attachments/Actual_Crash.m4v) (application/octet-stream, 3.0 MB)
- [Expected_No_Crash.m4v](attachments/Expected_No_Crash.m4v) (application/octet-stream, 1.1 MB)

## Timeline

### [Deleted User] (2015-02-20)

Stack Traces:
===============

Thread 0 CRASHED [EXC_BAD_ACCESS / KERN_INVALID_ADDRESS @ 0x00000048] MAGIC SIGNATURE THREAD
0x000000010ad0ebfd	[Google Chrome Framework -navigation_controller_impl.cc:783 ]	content::NavigationControllerImpl::RendererDidNavigate(content::RenderFrameHost*, FrameHostMsg_DidCommitProvisionalLoad_Params const&, content::LoadCommittedDetails*)
0x000000010ad16c4f	[Google Chrome Framework -navigator_impl.cc:520 ]	content::NavigatorImpl::DidNavigate(content::RenderFrameHostImpl*, FrameHostMsg_DidCommitProvisionalLoad_Params const&)
0x000000010ad1c489	[Google Chrome Framework -render_frame_host_impl.cc:830 ]	content::RenderFrameHostImpl::OnDidCommitProvisionalLoad(IPC::Message const&)
0x000000010ad1adb8	[Google Chrome Framework -render_frame_host_impl.cc:347 ]	content::RenderFrameHostImpl::OnMessageReceived(IPC::Message const&)
0x000000010ae4df3d	[Google Chrome Framework -render_process_host_impl.cc:1539 ]	content::RenderProcessHostImpl::OnMessageReceived(IPC::Message const&)
0x0000000108a240c7	[Google Chrome Framework -ipc_channel_proxy.cc:282 ]	IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&)
0x00000001082bc617	[Google Chrome Framework -callback.h:396 ]	base::debug::TaskAnnotator::RunTask(char const*, char const*, base::PendingTask const&)
0x00000001082de0ee	[Google Chrome Framework -message_loop.cc:448 ]	base::MessageLoop::RunTask(base::PendingTask const&)
0x00000001082de4ca	[Google Chrome Framework -message_loop.cc:458 ]	base::MessageLoop::DoWork()
0x00000001082b2f40	[Google Chrome Framework -message_pump_mac.mm:325 ]	base::MessagePumpCFRunLoopBase::RunWork()
0x00007fff91973b30	[CoreFoundation + 0x00012b30 ]	__CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__
0x00007fff91973454	[CoreFoundation + 0x00012454 ]	__CFRunLoopDoSources0
0x00007fff919967f4	[CoreFoundation + 0x000357f4 ]	__CFRunLoopRun
0x00007fff919960e1	[CoreFoundation + 0x000350e1 ]	CFRunLoopRunSpecific
0x00007fff949c5eb3	[HIToolbox + 0x0005feb3 ]	RunCurrentEventLoopInMode
0x00007fff949c5c51	[HIToolbox + 0x0005fc51 ]	ReceiveNextEventCommon
0x00007fff949c5ae2	[HIToolbox + 0x0005fae2 ]	BlockUntilNextEventMatchingListInMode
0x00007fff90e19532	[AppKit + 0x00155532 ]	_DPSNextEvent
0x00007fff90e18df1	[AppKit + 0x00154df1 ]	-[NSApplication nextEventMatchingMask:untilDate:inMode:dequeue:]
0x00007fff90e101a2	[AppKit + 0x0014c1a2 ]	-[NSApplication run]
0x00000001082b358d	[Google Chrome Framework -message_pump_mac.mm:649 ]	base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate*)
0x00000001082b2dab	[Google Chrome Framework -message_pump_mac.mm:235 ]	base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)
0x00000001082f14e2	[Google Chrome Framework -run_loop.cc:55 ]	base::RunLoop::Run()
0x0000000107ca9390	[Google Chrome Framework -chrome_browser_main.cc:1650 ]	ChromeBrowserMainParts::MainMessageLoopRun(int*)
0x000000010ac8c028	[Google Chrome Framework -browser_main_loop.cc:805 ]	content::BrowserMainLoop::RunMainMessageLoopParts()
0x000000010ac8e561	[Google Chrome Framework -browser_main_runner.cc:200 ]	content::BrowserMainRunnerImpl::Run()
0x000000010ac886f6	[Google Chrome Framework -browser_main.cc:26 ]	content::BrowserMain(content::MainFunctionParams const&)
0x000000010825dd13	[Google Chrome Framework -content_main_runner.cc:763 ]	content::ContentMainRunnerImpl::Run()
0x000000010825d455	[Google Chrome Framework -content_main.cc:19 ]	content::ContentMain(content::ContentMainParams const&)
0x0000000107c136f1	[Google Chrome Framework -chrome_main.cc:66 ]	ChromeMain
0x0000000107c08f38	[Google Chrome -chrome_exe_main_mac.cc:16 ]	main
0x0000000107c08f23	[Google Chrome + 0x00000f23 ]	start

### fs...@chromium.org (2015-02-20)

There are two bugs here:

1. Dragging a link from the signin page should not navigate the signin page. I'll take care of that.

2. This stack trace feels like a use-after-free bug that creis@ or nasko@ would be better able to diagnose than I. CC'ing them.

### cr...@chromium.org (2015-02-20)

Wow, that's a nice find, and a nasty crash.

In a debugger, it looks like something is deleting the RenderFrameHost that receives the DidCommit IPC for the "No thanks" chrome://extension URL.

### no...@chromium.org (2015-02-20)

crbug.com/455083 is a related crash (the link gets dropped on the bookmarks bar). Should I mark it as a duplicate of this? (I hadn't started working on it)

### cr...@chromium.org (2015-02-20)

And here's the stack from where the RFH is deleted, while its commit handler is still on the stack.

This stack says that the WebContents is being closed/deleted by  Browser::OnExtensionUnloaded (frame #16) thanks to UnloadGaiaAuthExtension (frame #24), which happens when the WebUI object gets reset in RenderFrameHostManager::CommitPending (frame #37).

That sounds like fundamentally wrong behavior in the signin code.

#0  content::RenderFrameHostImpl::~RenderFrameHostImpl (this=0x1024160273a0)
    at ../../content/browser/frame_host/render_frame_host_impl.cc:183
#1  0x00007f66706a7909 in content::RenderFrameHostImpl::~RenderFrameHostImpl (
    this=0x1024160273a0)
    at ../../content/browser/frame_host/render_frame_host_impl.cc:182
#2  0x00007f667066fe42 in base::DefaultDeleter<content::RenderFrameHostImpl>::operator() (this=0x7fff16593850, ptr=0x1024160273a0)
    at ../../base/memory/scoped_ptr.h:128
#3  0x00007f667066fe04 in base::internal::scoped_ptr_impl<content::RenderFrameHostImpl, base::DefaultDeleter<content::RenderFrameHostImpl> >::~scoped_ptr_impl
    (this=0x7fff16593850) at ../../base/memory/scoped_ptr.h:222
#4  0x00007f66706636e5 in scoped_ptr<content::RenderFrameHostImpl, base::DefaultDeleter<content::RenderFrameHostImpl> >::~scoped_ptr (this=0x7fff16593850)
    at ../../base/memory/scoped_ptr.h:312
#5  0x00007f66706cc527 in content::RenderFrameHostManager::~RenderFrameHostManager (this=0x1024143c5370)
    at ../../content/browser/frame_host/render_frame_host_manager.cc:72
#6  0x00007f66706704db in content::FrameTreeNode::~FrameTreeNode (
    this=0x1024143c5360)
    at ../../content/browser/frame_host/frame_tree_node.cc:46
#7  0x00007f66706702ae in base::DefaultDeleter<content::FrameTreeNode>::operator() (this=0x1024143ebca0, ptr=0x1024143c5360)
    at ../../base/memory/scoped_ptr.h:128
#8  0x00007f6670670274 in base::internal::scoped_ptr_impl<content::FrameTreeNode---Type <return> to continue, or q <return> to quit---
, base::DefaultDeleter<content::FrameTreeNode> >::~scoped_ptr_impl (
    this=0x1024143ebca0) at ../../base/memory/scoped_ptr.h:222
#9  0x00007f6670662f95 in scoped_ptr<content::FrameTreeNode, base::DefaultDeleter<content::FrameTreeNode> >::~scoped_ptr (this=0x1024143ebca0)
    at ../../base/memory/scoped_ptr.h:312
#10 0x00007f6670661389 in content::FrameTree::~FrameTree (this=0x1024143ebbf0)
    at ../../content/browser/frame_host/frame_tree.cc:84
#11 0x00007f6670e5c905 in content::WebContentsImpl::~WebContentsImpl (
    this=0x1024143eb820)
    at ../../content/browser/web_contents/web_contents_impl.cc:440
#12 0x00007f6670e5cd69 in content::WebContentsImpl::~WebContentsImpl (
    this=0x1024143eb820)
    at ../../content/browser/web_contents/web_contents_impl.cc:372
#13 0x00007f667797ef37 in TabStripModel::InternalCloseTab (
    this=0x1024141327a0, contents=0x1024143eb820, index=0, 
    create_historical_tabs=false)
    at ../../chrome/browser/ui/tabs/tab_strip_model.cc:1304
#14 0x00007f667797a866 in TabStripModel::InternalCloseTabs (
    this=0x1024141327a0, indices=..., close_types=0)
    at ../../chrome/browser/ui/tabs/tab_strip_model.cc:1279
#15 0x00007f667797ab08 in TabStripModel::CloseWebContentsAt (
    this=0x1024141327a0, index=0, close_types=0)
    at ../../chrome/browser/ui/tabs/tab_strip_model.cc:554
#16 0x00007f6677914941 in Browser::OnExtensionUnloaded (this=0x1024134fc020, 
---Type <return> to continue, or q <return> to quit---
    browser_context=0x10241357d220, extension=0x102416b61d60, 
    reason=extensions::UnloadedExtensionInfo::REASON_UNINSTALL)
    at ../../chrome/browser/ui/browser.cc:2066
#17 0x00007f66779149ad in non-virtual thunk to Browser::OnExtensionUnloaded(content::BrowserContext*, extensions::Extension const*, extensions::UnloadedExtensionInfo::Reason) () at ../../chrome/browser/ui/browser.cc:2070
#18 0x00007f66784b1bb1 in extensions::ExtensionRegistry::TriggerOnUnloaded (
    this=0x102413a9d7a0, extension=0x102416b61d60, 
    reason=extensions::UnloadedExtensionInfo::REASON_UNINSTALL)
    at ../../extensions/browser/extension_registry.cc:64
#19 0x00007f6678917aa0 in ExtensionService::NotifyExtensionUnloaded (
    this=0x102413d69220, extension=0x102416b61d60, 
    reason=extensions::UnloadedExtensionInfo::REASON_UNINSTALL)
    at ../../chrome/browser/extensions/extension_service.cc:1102
#20 0x00007f6678919c6b in ExtensionService::UnloadExtension (
    this=0x102413d69220, extension_id=..., 
    reason=extensions::UnloadedExtensionInfo::REASON_UNINSTALL)
    at ../../chrome/browser/extensions/extension_service.cc:1378
#21 0x00007f6678919d8e in ExtensionService::RemoveComponentExtension (
    this=0x102413d69220, extension_id=...)
    at ../../chrome/browser/extensions/extension_service.cc:1391
#22 0x00007f66788a527a in extensions::ComponentLoader::UnloadComponent (
    this=0x102413a4a020, component=0x102414495620)
    at ../../chrome/browser/extensions/component_loader.cc:657
---Type <return> to continue, or q <return> to quit---
#23 0x00007f66788a4f4d in extensions::ComponentLoader::Remove (
    this=0x102413a4a020, id=...)
    at ../../chrome/browser/extensions/component_loader.cc:272
#24 0x00007f66789b12cf in (anonymous namespace)::UnloadGaiaAuthExtension (
    context=0x10241357d220)
    at ../../chrome/browser/extensions/signin/gaia_auth_extension_loader.cc:81
#25 0x00007f66789b0fe9 in extensions::GaiaAuthExtensionLoader::UnloadIfNeeded (
    this=0x102413d2b480)
    at ../../chrome/browser/extensions/signin/gaia_auth_extension_loader.cc:104
#26 0x00007f66789b1bd3 in ScopedGaiaAuthExtension::~ScopedGaiaAuthExtension (
    this=0x10241452bd00)
    at ../../chrome/browser/extensions/signin/scoped_gaia_auth_extension.cc:23
#27 0x00007f6677a4b7d5 in InlineLoginUI::~InlineLoginUI (this=0x10241452bcf0)
    at ../../chrome/browser/ui/webui/signin/inline_login_ui.cc:91
#28 0x00007f6677a4b809 in InlineLoginUI::~InlineLoginUI (this=0x10241452bcf0)
    at ../../chrome/browser/ui/webui/signin/inline_login_ui.cc:91
#29 0x00007f6670ed11b2 in base::DefaultDeleter<content::WebUIController>::operator() (this=0x102416b0a6d8, ptr=0x10241452bcf0)
    at ../../base/memory/scoped_ptr.h:128
#30 0x00007f6670ed116b in base::internal::scoped_ptr_impl<content::WebUIController, base::DefaultDeleter<content::WebUIController> >::reset (
    this=0x102416b0a6d8, p=0x0) at ../../base/memory/scoped_ptr.h:248
#31 0x00007f6670ecc2fd in scoped_ptr<content::WebUIController, base::DefaultDeleter<content::WebUIController> >::reset (this=0x102416b0a6d8, p=0x0)
---Type <return> to continue, or q <return> to quit---
    at ../../base/memory/scoped_ptr.h:377
#32 0x00007f6670eca409 in content::WebUIImpl::~WebUIImpl (this=0x102416b0a620)
    at ../../content/browser/webui/web_ui_impl.cc:56
#33 0x00007f6670eca4e9 in content::WebUIImpl::~WebUIImpl (this=0x102416b0a620)
    at ../../content/browser/webui/web_ui_impl.cc:53
#34 0x00007f66706da152 in base::DefaultDeleter<content::WebUIImpl>::operator()
    (this=0x1024143c53b0, ptr=0x102416b0a620)
    at ../../base/memory/scoped_ptr.h:128
#35 0x00007f66706da10b in base::internal::scoped_ptr_impl<content::WebUIImpl, base::DefaultDeleter<content::WebUIImpl> >::reset (this=0x1024143c53b0, 
    p=0x10241382e520) at ../../base/memory/scoped_ptr.h:248
#36 0x00007f66706d8cad in scoped_ptr<content::WebUIImpl, base::DefaultDeleter<content::WebUIImpl> >::reset (this=0x1024143c53b0, p=0x10241382e520)
    at ../../base/memory/scoped_ptr.h:377
#37 0x00007f66706d0867 in content::RenderFrameHostManager::CommitPending (
    this=0x1024143c5370)
    at ../../content/browser/frame_host/render_frame_host_manager.cc:1566
#38 0x00007f66706d0339 in content::RenderFrameHostManager::DidNavigateFrame (
    this=0x1024143c5370, render_frame_host=0x1024160273a0, 
    was_caused_by_user_gesture=false)
    at ../../content/browser/frame_host/render_frame_host_manager.cc:462
#39 0x00007f667069d236 in content::NavigatorImpl::DidNavigate (
    this=0x1024141e29e0, render_frame_host=0x1024160273a0, input_params=...)
    at ../../content/browser/frame_host/navigator_impl.cc:468
---Type <return> to continue, or q <return> to quit---
#40 0x00007f66706aab2b in content::RenderFrameHostImpl::OnDidCommitProvisionalLoad (this=0x1024160273a0, msg=...)
    at ../../content/browser/frame_host/render_frame_host_impl.cc:830
#41 0x00007f66706a8c56 in content::RenderFrameHostImpl::OnMessageReceived (
    this=0x1024160273a0, msg=...)
    at ../../content/browser/frame_host/render_frame_host_impl.cc:347
#42 0x00007f6670b61256 in content::RenderProcessHostImpl::OnMessageReceived (
    this=0x102416b8a920, msg=...)
    at ../../content/browser/renderer_host/render_process_host_impl.cc:1539
#43 0x00007f6670b6165f in non-virtual thunk to content::RenderProcessHostImpl::OnMessageReceived(IPC::Message const&) ()
    at ../../content/browser/renderer_host/render_process_host_impl.cc:1540
#44 0x00007f666676bcad in IPC::ChannelProxy::Context::OnDispatchMessage (
    this=0x1024141317a0, message=...) at ../../ipc/ipc_channel_proxy.cc:282
#45 0x00007f66667749ea in base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>::Run (this=0x7fff16598920, 
    object=0x1024141317a0, args=...) at ../../base/bind_internal.h:176

### cr...@chromium.org (2015-02-20)

Note: drag and drop is only one way to cause this crash.  Simpler repro steps:

1) Navigate to chrome://chrome-signin/?source=0
2) Paste the following URL in the omnibox: chrome-extension://mfffpogegjflfpflabcdkioaeobkgjik/success.html?source=0&ntp=1
3) Crash.

Definitely a sign-in bug.

### cr...@chromium.org (2015-02-20)

@noms: Yes, https://crbug.com/chromium/455083 is the same crash.  Please mark it as a duplicate of this.

Also, this is a use-after-free in the browser process, which may have security implications.  Please do treat this as a Stable Blocker.  I'll assign it to you for triage, since Fady's CL just added another way for this existing issue to happen.  We should aim to get this fixed soon if we can.  Thanks!

@inferno: Can you help triage the security flags for this?

### in...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### no...@chromium.org (2015-02-25)

(adding xiyuan who has worked on this before)

### no...@chromium.org (2015-02-25)

I have a fix ready for this at https://codereview.chromium.org/961443003/. Now we just close the tab when we're in this situation (because the extension is being unloaded asynchronously), which is strictly better than crashing. 

### bu...@chromium.org (2015-02-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1805c4c5c4b5292cca51a54f379cde498db7238b

commit 1805c4c5c4b5292cca51a54f379cde498db7238b
Author: noms <noms@chromium.org>
Date: Wed Feb 25 23:24:25 2015

Unload the ScopedGaiaAuthExtension asynchronously.

If we don't do this, then we have a race condition between unloading
this extension, and trying to use it because we have manually
navigated to it.

BUG=460431

Review URL: https://codereview.chromium.org/961443003

Cr-Commit-Position: refs/heads/master@{#318140}

[modify] http://crrev.com/1805c4c5c4b5292cca51a54f379cde498db7238b/chrome/browser/extensions/signin/scoped_gaia_auth_extension.cc


### bu...@chromium.org (2015-02-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7f4aed4ac87717e339303e2c494be4855cab738d

commit 7f4aed4ac87717e339303e2c494be4855cab738d
Author: sammc <sammc@chromium.org>
Date: Thu Feb 26 02:58:35 2015

Revert of Unload the ScopedGaiaAuthExtension asynchronously. (patchset #2 id:20001 of https://codereview.chromium.org/961443003/)

Reason for revert:
Broke BookmarkSyncPromoControllerTest.SignInLink on Mac ASan 64: https://build.chromium.org/p/chromium.memory/builders/Mac%20ASan%2064%20Tests%20%281%29/builds/7363

Original issue's description:
> Unload the ScopedGaiaAuthExtension asynchronously.
>
> If we don't do this, then we have a race condition between unloading
> this extension, and trying to use it because we have manually
> navigated to it.
>
> BUG=460431
>
> Committed: https://crrev.com/1805c4c5c4b5292cca51a54f379cde498db7238b
> Cr-Commit-Position: refs/heads/master@{#318140}

TBR=xiyuan@chromium.org,noms@google.com,noms@chromium.org
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=460431

Review URL: https://codereview.chromium.org/944923007

Cr-Commit-Position: refs/heads/master@{#318176}

[modify] http://crrev.com/7f4aed4ac87717e339303e2c494be4855cab738d/chrome/browser/extensions/signin/scoped_gaia_auth_extension.cc


### no...@chromium.org (2015-02-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-13)

noms@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@google.com (2015-03-16)

@noms - what's the latest after the revert?

### no...@chromium.org (2015-03-16)

The CL is going through the CQ as we speak: https://codereview.chromium.org/961443003/

### bu...@chromium.org (2015-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c37009c34bc9c7921cabf5f9cfee96430511be97

commit c37009c34bc9c7921cabf5f9cfee96430511be97
Author: noms <noms@chromium.org>
Date: Tue Mar 17 17:47:08 2015

Unload the ScopedGaiaAuthExtension asynchronously.

If we don't do this, then we have a race condition between unloading
this extension, and trying to use it because we have manually
navigated to it.

BUG=460431

Committed: https://crrev.com/1805c4c5c4b5292cca51a54f379cde498db7238b
Cr-Commit-Position: refs/heads/master@{#318140}

Review URL: https://codereview.chromium.org/961443003

Cr-Commit-Position: refs/heads/master@{#320937}

[modify] http://crrev.com/c37009c34bc9c7921cabf5f9cfee96430511be97/chrome/browser/extensions/signin/gaia_auth_extension_loader.cc
[modify] http://crrev.com/c37009c34bc9c7921cabf5f9cfee96430511be97/chrome/browser/extensions/signin/gaia_auth_extension_loader.h
[modify] http://crrev.com/c37009c34bc9c7921cabf5f9cfee96430511be97/chrome/browser/extensions/signin/scoped_gaia_auth_extension.cc


### no...@chromium.org (2015-03-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2015-03-18)

Is there a merge required here?

### cl...@chromium.org (2015-03-18)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### am...@chromium.org (2015-03-23)

merge approved for m42

### bu...@chromium.org (2015-03-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ce546fa035ec9473ab8f39068d891b2f2883c834

commit ce546fa035ec9473ab8f39068d891b2f2883c834
Author: Alex Mineer <amineer@chromium.org>
Date: Mon Mar 23 19:53:37 2015

Unload the ScopedGaiaAuthExtension asynchronously.

If we don't do this, then we have a race condition between unloading
this extension, and trying to use it because we have manually
navigated to it.

BUG=460431

Committed: https://crrev.com/1805c4c5c4b5292cca51a54f379cde498db7238b
Cr-Commit-Position: refs/heads/master@{#318140}

Review URL: https://codereview.chromium.org/961443003

(cherry picked from commit c37009c34bc9c7921cabf5f9cfee96430511be97)

Cr-Original-Commit-Position: refs/heads/master@{#320937}
Cr-Commit-Position: refs/branch-heads/2311@{#321}
Cr-Branched-From: 09b7de5dd7254947cd4306de907274fa63373d48-refs/heads/master@{#317474}

[modify] http://crrev.com/ce546fa035ec9473ab8f39068d891b2f2883c834/chrome/browser/extensions/signin/gaia_auth_extension_loader.cc
[modify] http://crrev.com/ce546fa035ec9473ab8f39068d891b2f2883c834/chrome/browser/extensions/signin/gaia_auth_extension_loader.h
[modify] http://crrev.com/ce546fa035ec9473ab8f39068d891b2f2883c834/chrome/browser/extensions/signin/scoped_gaia_auth_extension.cc


### bu...@chromium.org (2015-03-31)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/experimental/chrome-radiance.git/+/c37009c34bc9c7921cabf5f9cfee96430511be97

commit c37009c34bc9c7921cabf5f9cfee96430511be97
Author: noms <noms@chromium.org>
Date: Tue Mar 17 17:47:08 2015


### ti...@google.com (2015-04-08)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-12)

Thanks for this report - our reward panel determined to reward you with $1,000 for this report. Congratulations!

A member of our finance team should reach out with details to collect payment in two weeks. After that information is collected, payment takes about 3-4 weeks.

### ti...@google.com (2015-06-12)

@jshanbal - note that if you found this bug as a contracted tester (i.e. you were being paid by Google to do this), you can't claim the reward. Let me know!

### [Deleted User] (2015-06-15)

+ Anantha.

### cl...@chromium.org (2015-06-24)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-25)

Marking as reward ineligible per #28 - found by a contracted tester.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/460431?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/455083]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081470)*

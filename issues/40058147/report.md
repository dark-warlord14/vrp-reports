# Security: heap-use-after-free in ui::AXTree::NotifyNodeWillBeReparentedOrDeleted 

| Field | Value |
|-------|-------|
| **Issue ID** | [40058147](https://issues.chromium.org/issues/40058147) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Internals>Accessibility |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | dl...@gmail.com |
| **Created** | 2021-12-07 |
| **Bounty** | $7,000.00 |

## Description

This vulnerability is similar to the triggering method of <https://crbug.com/chromium/1277327>, but it has a fundamentally different cause. It seems to be a new UAF, wait for me to have time to analyze it in detail.

=================================================================  

==13220==ERROR: AddressSanitizer: heap-use-after-free on address 0x12772dea1950 at pc 0x7ffcb0f9779d bp 0x007d281fac60 sp 0x007d281faca8  

READ of size 4 at 0x12772dea1950 thread T0  

#0 0x7ffcb0f9779c in ui::AXTree::NotifyNodeWillBeReparentedOrDeleted E:\src\chromium\src\ui\accessibility\ax\_tree.cc:1725  

#1 0x7ffcb0f9235a in ui::AXTree::Unserialize E:\src\chromium\src\ui\accessibility\ax\_tree.cc:1052  

#2 0x7ffcba5f956a in content::BrowserAccessibilityManager::Unserialize E:\src\chromium\src\content\browser\accessibility\browser\_accessibility\_manager.cc:225  

#3 0x7ffcba5faf7c in content::BrowserAccessibilityManager::OnAccessibilityEvents E:\src\chromium\src\content\browser\accessibility\browser\_accessibility\_manager.cc:460  

#4 0x7ffcbb50f5f8 in content::RenderFrameHostImpl::HandleAXEvents E:\src\chromium\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:7180  

#5 0x7ffcba620e11 in base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::\*)(const ui::AXTreeID &, mojo::StructPtr[content::mojom::AXUpdatesAndEvents](javascript:void(0);), int),base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);),ui::AXTreeID,mojo::StructPtr[content::mojom::AXUpdatesAndEvents](javascript:void(0);),int>,void ()>::RunOnce E:\src\chromium\src\base\bind\_internal.h:741  

#6 0x7ffcd2cdb3df in base::`anonymous namespace'::PostTaskAndReplyRelay::RunTaskAndPostReply E:\src\chromium\src\base\threading\post\_task\_and\_reply\_impl.cc:100  

#7 0x7ffcd2cdbc23 in base::internal::Invoker<base::internal::BindState<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce E:\src\chromium\src\base\bind\_internal.h:741  

#8 0x7ffcd2c27474 in base::TaskAnnotator::RunTaskImpl E:\src\chromium\src\base\task\common\task\_annotator.cc:135  

#9 0x7ffcd2c74789 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#10 0x7ffcd2c73e58 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#11 0x7ffcd2d70216 in base::MessagePumpForUI::DoRunLoop E:\src\chromium\src\base\message\_loop\message\_pump\_win.cc:220  

#12 0x7ffcd2d6dccf in base::MessagePumpWin::Run E:\src\chromium\src\base\message\_loop\message\_pump\_win.cc:78  

#13 0x7ffcd2c75f03 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#14 0x7ffcd2b71e03 in base::RunLoop::Run E:\src\chromium\src\base\run\_loop.cc:140  

#15 0x7ffcba8972a1 in content::BrowserMainLoop::RunMainMessageLoop E:\src\chromium\src\content\browser\browser\_main\_loop.cc:1038  

#16 0x7ffcba89d0a3 in content::BrowserMainRunnerImpl::Run E:\src\chromium\src\content\browser\browser\_main\_runner\_impl.cc:153  

#17 0x7ffcba89072f in content::BrowserMain E:\src\chromium\src\content\browser\browser\_main.cc:30  

#18 0x7ffcbc9db22e in content::RunBrowserProcessMain E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:646  

#19 0x7ffcbc9de3e3 in content::ContentMainRunnerImpl::RunBrowser E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:1160  

#20 0x7ffcbc9dd511 in content::ContentMainRunnerImpl::Run E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:1026  

#21 0x7ffcbc9d92bf in content::RunContentProcess E:\src\chromium\src\content\app\content\_main.cc:398  

#22 0x7ffcbc9da327 in content::ContentMain E:\src\chromium\src\content\app\content\_main.cc:426  

#23 0x7ffcbff214a5 in ChromeMain E:\src\chromium\src\chrome\app\chrome\_main.cc:172  

#24 0x7ff7903d5554 in MainDllLoader::Launch E:\src\chromium\src\chrome\app\main\_dll\_loader\_win.cc:169  

#25 0x7ff7903d2a02 in main E:\src\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#26 0x7ff7905aee4b in \_\_scrt\_common\_main\_seh D:\agent\_work\13\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#27 0x7ffd30497033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#28 0x7ffd32402650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x12772dea1950 is located 80 bytes inside of 472-byte region [0x12772dea1900,0x12772dea1ad8)  

freed by thread T0 here:  

#0 0x7ffcf404070b in operator delete+0x8b (E:\src\chromium\src\out\Default\clang\_rt.asan\_dynamic-x86\_64.dll+0x18004070b)  

#1 0x7ffcb0f8f01a in ui::AXTree::DestroyNodeAndSubtree E:\src\chromium\src\ui\accessibility\ax\_tree.cc:2088  

#2 0x7ffcb0f8dcb0 in ui::AXTree::Destroy E:\src\chromium\src\ui\accessibility\ax\_tree.cc:794  

#3 0x7ffcba5f8b3b in content::BrowserAccessibilityManager::~BrowserAccessibilityManager E:\src\chromium\src\content\browser\accessibility\browser\_accessibility\_manager.cc:211  

#4 0x7ffcbbbdf02b in content::BrowserAccessibilityManagerWin::~BrowserAccessibilityManagerWin E:\src\chromium\src\content\browser\accessibility\browser\_accessibility\_manager\_win.cc:86  

#5 0x7ffcbb4c956e in content::RenderFrameHostImpl::~RenderFrameHostImpl E:\src\chromium\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:1649  

#6 0x7ffcbb54d889 in content::RenderFrameHostImpl::~RenderFrameHostImpl E:\src\chromium\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:1511  

#7 0x7ffcbb58711a in content::RenderFrameHostManager::~RenderFrameHostManager E:\src\chromium\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:312  

#8 0x7ffcbb2a872a in content::FrameTreeNode::~FrameTreeNode E:\src\chromium\src\content\browser\renderer\_host\frame\_tree\_node.cc:243  

#9 0x7ffcbb29700e in content::FrameTree::~FrameTree E:\src\chromium\src\content\browser\renderer\_host\frame\_tree.cc:295  

#10 0x7ffcbb9a349d in content::WebContentsImpl::~WebContentsImpl E:\src\chromium\src\content\browser\web\_contents\web\_contents\_impl.cc:1070  

#11 0x7ffcbba2e49b in content::WebContentsImpl::~WebContentsImpl E:\src\chromium\src\content\browser\web\_contents\web\_contents\_impl.cc:972  

#12 0x7ffc8ed688c9 in views::WebView::SetWebContents E:\src\chromium\src\ui\views\controls\webview\webview.cc:106  

#13 0x7ffc8ed68699 in views::WebView::~WebView E:\src\chromium\src\ui\views\controls\webview\webview.cc:74  

#14 0x7ffc8ed6c849 in views::WebView::~WebView E:\src\chromium\src\ui\views\controls\webview\webview.cc:72  

#15 0x7ffcbfb4cffd in views::View::~View E:\src\chromium\src\ui\views\view.cc:253  

#16 0x7ffcc791149f in WebUITabStripContainerView::~WebUITabStripContainerView E:\src\chromium\src\chrome\browser\ui\views\frame\webui\_tab\_strip\_container\_view.cc:494  

#17 0x7ffcc5de0188 in BrowserView::MaybeInitializeWebUITabStrip E:\src\chromium\src\chrome\browser\ui\views\frame\browser\_view.cc:3441  

#18 0x7ffcb0fdf1ed in ui::AXPlatformNode::NotifyAddAXModeFlags E:\src\chromium\src\ui\accessibility\platform\ax\_platform\_node.cc:105  

#19 0x7ffcb10823a4 in ui::AXPlatformNodeWin::get\_states E:\src\chromium\src\ui\accessibility\platform\ax\_platform\_node\_win.cc:1270  

#20 0x7ffcbbb9e4be in content::AccessibilityEventRecorderWin::OnWinEventHook E:\src\chromium\src\content\browser\accessibility\accessibility\_event\_recorder\_win.cc:248  

#21 0x7ffcbbb9cd08 in content::AccessibilityEventRecorderWin::WinEventHookThunk E:\src\chromium\src\content\browser\accessibility\accessibility\_event\_recorder\_win.cc:98  

#22 0x7ffd3056671b in GetMenuItemCount+0xeb (C:\Windows\System32\USER32.dll+0x18002671b)  

#23 0x7ffd32450ba3 in KiUserCallbackDispatcher+0x23 (C:\Windows\SYSTEM32\ntdll.dll+0x1800a0ba3)  

#24 0x7ffd2fdf15e3 in NtUserNotifyWinEvent+0x13 (C:\Windows\System32\win32u.dll+0x1800015e3)  

#25 0x7ffcbbbdcfee in content::BrowserAccessibilityManagerWin::OnSubtreeWillBeDeleted E:\src\chromium\src\content\browser\accessibility\browser\_accessibility\_manager\_win.cc:716  

#26 0x7ffcb0f9724f in ui::AXTree::NotifySubtreeWillBeReparentedOrDeleted E:\src\chromium\src\ui\accessibility\ax\_tree.cc:1711  

#27 0x7ffcb0f92318 in ui::AXTree::Unserialize E:\src\chromium\src\ui\accessibility\ax\_tree.cc:1050

previously allocated by thread T0 here:  

#0 0x7ffcf404041b in operator new+0x8b (E:\src\chromium\src\out\Default\clang\_rt.asan\_dynamic-x86\_64.dll+0x18004041b)  

#1 0x7ffcb0fa1e93 in ui::AXTree::CreateNode E:\src\chromium\src\ui\accessibility\ax\_tree.cc:1377  

#2 0x7ffcb0f98331 in ui::AXTree::UpdateNode E:\src\chromium\src\ui\accessibility\ax\_tree.cc:1669  

#3 0x7ffcb0f92dbf in ui::AXTree::Unserialize E:\src\chromium\src\ui\accessibility\ax\_tree.cc:1151  

#4 0x7ffcba5f956a in content::BrowserAccessibilityManager::Unserialize E:\src\chromium\src\content\browser\accessibility\browser\_accessibility\_manager.cc:225  

#5 0x7ffcba5f87ed in content::BrowserAccessibilityManager::Initialize E:\src\chromium\src\content\browser\accessibility\browser\_accessibility\_manager.cc:247  

#6 0x7ffcbbbd8d79 in content::BrowserAccessibilityManagerWin::BrowserAccessibilityManagerWin E:\src\chromium\src\content\browser\accessibility\browser\_accessibility\_manager\_win.cc:83  

#7 0x7ffcbbbd8f51 in content::BrowserAccessibilityManager::Create E:\src\chromium\src\content\browser\accessibility\browser\_accessibility\_manager\_win.cc:69  

#8 0x7ffcbb4ff01c in content::RenderFrameHostImpl::GetOrCreateBrowserAccessibilityManager E:\src\chromium\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:8742  

#9 0x7ffcbb50e755 in content::RenderFrameHostImpl::HandleAXEvents E:\src\chromium\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:7148  

#10 0x7ffcba620e11 in base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::\*)(const ui::AXTreeID &, mojo::StructPtr[content::mojom::AXUpdatesAndEvents](javascript:void(0);), int),base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);),ui::AXTreeID,mojo::StructPtr[content::mojom::AXUpdatesAndEvents](javascript:void(0);),int>,void ()>::RunOnce E:\src\chromium\src\base\bind\_internal.h:741  

#11 0x7ffcd2cdb3df in base::`anonymous namespace'::PostTaskAndReplyRelay::RunTaskAndPostReply E:\src\chromium\src\base\threading\post\_task\_and\_reply\_impl.cc:100  

#12 0x7ffcd2cdbc23 in base::internal::Invoker<base::internal::BindState<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce E:\src\chromium\src\base\bind\_internal.h:741  

#13 0x7ffcd2c27474 in base::TaskAnnotator::RunTaskImpl E:\src\chromium\src\base\task\common\task\_annotator.cc:135  

#14 0x7ffcd2c74789 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#15 0x7ffcd2c73e58 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#16 0x7ffcd2d70216 in base::MessagePumpForUI::DoRunLoop E:\src\chromium\src\base\message\_loop\message\_pump\_win.cc:220  

#17 0x7ffcd2d6dccf in base::MessagePumpWin::Run E:\src\chromium\src\base\message\_loop\message\_pump\_win.cc:78  

#18 0x7ffcd2c75f03 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#19 0x7ffcd2b71e03 in base::RunLoop::Run E:\src\chromium\src\base\run\_loop.cc:140  

#20 0x7ffcba8972a1 in content::BrowserMainLoop::RunMainMessageLoop E:\src\chromium\src\content\browser\browser\_main\_loop.cc:1038  

#21 0x7ffcba89d0a3 in content::BrowserMainRunnerImpl::Run E:\src\chromium\src\content\browser\browser\_main\_runner\_impl.cc:153  

#22 0x7ffcba89072f in content::BrowserMain E:\src\chromium\src\content\browser\browser\_main.cc:30  

#23 0x7ffcbc9db22e in content::RunBrowserProcessMain E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:646  

#24 0x7ffcbc9de3e3 in content::ContentMainRunnerImpl::RunBrowser E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:1160  

#25 0x7ffcbc9dd511 in content::ContentMainRunnerImpl::Run E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:1026  

#26 0x7ffcbc9d92bf in content::RunContentProcess E:\src\chromium\src\content\app\content\_main.cc:398  

#27 0x7ffcbc9da327 in content::ContentMain E:\src\chromium\src\content\app\content\_main.cc:426

SUMMARY: AddressSanitizer: heap-use-after-free E:\src\chromium\src\ui\accessibility\ax\_tree.cc:1725 in ui::AXTree::NotifyNodeWillBeReparentedOrDeleted  

Shadow bytes around the buggy address:  

0x049c12fd42d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x049c12fd42e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x049c12fd42f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x049c12fd4300: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x049c12fd4310: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x049c12fd4320: fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd  

0x049c12fd4330: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x049c12fd4340: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x049c12fd4350: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa  

0x049c12fd4360: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x049c12fd4370: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==13220==ABORTING

**VERSION**  

Chrome Version: 98.0.4750.0 x64  

Operating System: windows 10 21h1  

credit information:

Zhihua Yao of KunLun Lab

## Timeline

### [Deleted User] (2021-12-07)

[Empty comment from Monorail migration]

### ha...@gmail.com (2021-12-07)

[0]https://source.chromium.org/chromium/chromium/src/+/main:ui/accessibility/ax_node.cc;drc=58b0f88e7fedf85501d3fd605e69928965571387;l=696

void AXNode::Destroy() {
  delete this;   //destory the AXNode object
}

[1]https://source.chromium.org/chromium/chromium/src/+/main:ui/accessibility/ax_tree.cc;l=1725
void AXTree::NotifyNodeWillBeReparentedOrDeleted(
    AXNode* node,
    const AXTreeUpdateState* update_state) {
  DCHECK(!GetTreeUpdateInProgressState());

  AXNodeID id = node->id();  //UAF here
......

### do...@chromium.org (2021-12-07)

Is this the same as https://crbug.com/chromium/1277324?

Please provide a POC or video to help triage, thanks.

### ha...@gmail.com (2021-12-07)

This vulnerability is very unstable to reproduce the crash in win11, but here are the steps to reproduce 

1.open the chrome://accessibility with Touch UI Layout
2.click tab search and refresh
3.click "chrome://tab-search.top-chrome/" start recording button
4.choose Web accessibility options and then choose Native accessibility API support options
5.UAF occurs

### do...@chromium.org (2021-12-07)

Given the similarity of steps, I'm inclined to think this is a duplicate of https://crbug.com/chromium/1277327. Even though the stack is slightly different, the underlying reason for the UaF may be identical.

### ha...@gmail.com (2021-12-07)

The root cause I have analyzed above, it is caused by different reasons 

### do...@chromium.org (2021-12-08)

aleventhal: I suspect the same fix for https://crbug.com/chromium/1277327 may fix this bug as well. If so, that would make them duplicates. Do you mind taking a look?

[Monorail components: Internals>Accessibility]

### al...@chromium.org (2021-12-08)

SInce it's marked as "not time critical", does that mean it can wait a bit?

### do...@chromium.org (2021-12-08)

No, I have simply not added the usual security labels on this bug yet. All security issues should be treated as urgent.

### do...@chromium.org (2021-12-14)

Sheriff ping: can owners please take a look at this issue and help triage, thanks

### me...@chromium.org (2021-12-16)

I'm the current security sheriff  and triaging this and similar issues from the same reporter.These reports have the following in common:
1. They require Touch UI Layout to be enabled. This feature is disabled by default.
2. The UAFs are on chrome://accessibility pages. Websites and extensions can't script chrome:// pages.
3. The bugs require non-trivial user input.
4. The UAFs are in the browser process.

Browser process UAFs are normally critical, but given the triple mitigating factors above, there is argument to be made that these are Low severity. However, I'm going to go with the precedent set by https://bugs.chromium.org/p/chromium/issues/detail?id=1270095#c24 and mark this one as Medium to be consistent.

Tentatively adding labels, though I wasn't able to repro in 96, 97 or 98.

### [Deleted User] (2021-12-16)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-12-16)

Digging a bit more: The touch UI layout is never intended for production, it's only for QA and testers: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/flag-metadata.json;l=5370?q=%22top-chrome-touch-ui%22&ss=chromium

If this bug doesn't trigger without the Touch UI Layout being enabled, this would be Security_Impact-None.

hackyzh002: Can you please confirm if Touch UI Layout is necessary for this bug?

### ha...@gmail.com (2021-12-16)

Yep,enable  Touch UI Layout

### me...@chromium.org (2021-12-16)

Can you say more? If the touch layout is disabled, is there any chance of reproducing this? (e.g. on mobile)

### [Deleted User] (2021-12-16)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-16)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2021-12-16)

This is on an internal debug page that's not user facing so I'm lowering the severity once again. There are several mitigating factors to make this a practical bug for exploitation.

### ha...@gmail.com (2021-12-20)

This UAF point seems to be fixed by other bugs.https://chromium.googlesource.com/chromium/src.git/+/043a1ffbd9dee09ddc6d48eb4772cc0ceae79cdc%5E%21/#F0

### me...@chromium.org (2021-12-20)

+dlibby@microsoft.com who landed that CL

dlibby: Was there a bug that prompted you to land the CL? Thanks.

### dl...@gmail.com (2021-12-20)

There was not, it was general cleanup that I noticed in preparation for moving some AXNodeID usage to use WeakPtr<AXNode> instead for performance reasons.

Whether or not to complete the conversion is still an open question, but in retrospect, I should have tied it to a bug.

Reporter - I don't think that change should have modified the lifetimes of AXNode, can you confirm that this bug is fixed in latest Chromium builds? 

Overall between this bug and https://crbug.com/chromium/1277327, we probably don't want BrowserView::AccessibilityModeObserver::OnAXModeAdded to trigger synchronous destruction of WebContents, but I'm not very familiar with that code. +dfried@ as author of crrev.com/c/2459056 which added that code.

### me...@chromium.org (2021-12-20)

Thanks for the explanation!

I discussed this in the security chat and there is a preference to bump this back to Medium: While chrome://accessibility is a developer facing page, webui bugs have been used as part of exploit chains in the past. So I'm readjusting the severity again, sorry for the noise.

### al...@chromium.org (2021-12-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-22)

asurkov: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@igalia.com (2021-12-22)

It looks a duplication of https://crbug.com/chromium/1277324, which has a patch attached (https://chromium-review.googlesource.com/c/chromium/src/+/3353757), so let's wait and see if it helps.

### ha...@gmail.com (2021-12-22)

[Comment Deleted]

### dl...@gmail.com (2021-12-22)

The unique_ptr local in ui::AXTree::DestroyNodeAndSubtree will invoke `delete` and free the memory (instead of directly invoking Destroy/delete). So the AXNode object should still be getting deleted.

### ha...@gmail.com (2021-12-27)

Yep,y ou are right, I can still reproduce in  99.0.4790.0

### dl...@gmail.com (2022-01-05)

[Empty comment from Monorail migration]

### dl...@gmail.com (2022-01-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c1ce12c32b780b2dafe1e4c27a0d2e4db179030c

commit c1ce12c32b780b2dafe1e4c27a0d2e4db179030c
Author: Daniel Libby <dlibby@microsoft.com>
Date: Thu Jan 06 18:32:02 2022

Don't initialize webui tab strip synchronously during AXMode changes

MaybeInitializeWebUITabStrip will destroy Views or WebContents
associated with the WebUI tab strip. Currently, the accessibility code
has a model where AXMode is checked on API calls or tree updates.
Synchronously destroying the WebUI tab strip can lead to UAF so post a
task to do this work when the AXMode changes.

Bug: 1277328
Change-Id: Ic1391c93c95af1c936d6b55b93668207de5d6598
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3368621
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Daniel Libby <dlibby@microsoft.com>
Cr-Commit-Position: refs/heads/main@{#956181}

[modify] https://crrev.com/c1ce12c32b780b2dafe1e4c27a0d2e4db179030c/chrome/browser/ui/views/frame/browser_view.cc


### dl...@gmail.com (2022-01-07)

[Empty comment from Monorail migration]

### dl...@gmail.com (2022-01-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-07)

Requesting merge to dev M98 because latest trunk commit (956181) appears to be after dev branch point (950365).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-07)

Merge review required: M98 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2022-01-10)

pls answer https://crbug.com/chromium/1277328#c40 for merge review. 

### dl...@gmail.com (2022-01-10)

1. Why does your merge fit within the merge criteria for these milestones?
P1 security issue
2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3368621
3. Have the changes been released and tested on canary?
Yes
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No

### am...@chromium.org (2022-01-11)

merge approved for M98, please merge to branch 4758 ASAP (before 12pm PST tomorrow, Tuesday 11 January) so this fix can be included in tomorrow's beta cut for release on Wednesday -- thanks! 

### gi...@appspot.gserviceaccount.com (2022-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cf7bc9c38a6bf7e062772678f660697cfe8bca32

commit cf7bc9c38a6bf7e062772678f660697cfe8bca32
Author: Daniel Libby <dlibby@microsoft.com>
Date: Tue Jan 11 02:20:47 2022

Don't initialize webui tab strip synchronously during AXMode changes

MaybeInitializeWebUITabStrip will destroy Views or WebContents
associated with the WebUI tab strip. Currently, the accessibility code
has a model where AXMode is checked on API calls or tree updates.
Synchronously destroying the WebUI tab strip can lead to UAF so post a
task to do this work when the AXMode changes.

(cherry picked from commit c1ce12c32b780b2dafe1e4c27a0d2e4db179030c)

Bug: 1277328
Change-Id: Ic1391c93c95af1c936d6b55b93668207de5d6598
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3368621
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Daniel Libby <dlibby@microsoft.com>
Cr-Original-Commit-Position: refs/heads/main@{#956181}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3379727
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#485}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/cf7bc9c38a6bf7e062772678f660697cfe8bca32/chrome/browser/ui/views/frame/browser_view.cc


### [Deleted User] (2022-01-13)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dl...@gmail.com (2022-01-18)

RE: LTS candidate:
1. No
2. No

### ha...@gmail.com (2022-01-19)

I found this issue #1237069 is Critical,from my inference maybe this can be triggered by controlling the html content, maybe my level should also be raised to high? The same is true in accessiblity.

### ha...@gmail.com (2022-01-27)

Any reward update?

### am...@chromium.org (2022-01-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-27)

Hello, thanks for your patience as we working through this VRP queue. The queue is prioritized from critical to low, so while we endeavor to evaluate this issue as soon as possible, it may be a bit more time until we get to this one. Thanks again for your patience. 

### [Deleted User] (2022-01-28)

The older reward-topanel https://crbug.com/chromium/1277324 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### rz...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-03)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-02-03)

1. Number of CLs needed for this fix and links to them.
1 CL, https://crrev.com/c/3427975

2. Level of complexity (High, Medium, Low - Explain)
Low, no conflicts

3. Has this been merged to a stable release? beta release?
98

4. Overall Recommendation (Yes, No)
Yes

### gm...@google.com (2022-02-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-03)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-02-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6e0153b5f3db457f23a9ee11af42547fb4d72f2c

commit 6e0153b5f3db457f23a9ee11af42547fb4d72f2c
Author: Daniel Libby <dlibby@microsoft.com>
Date: Fri Feb 04 10:53:48 2022

[M96-LTS] Don't initialize webui tab strip synchronously during AXMode changes

MaybeInitializeWebUITabStrip will destroy Views or WebContents
associated with the WebUI tab strip. Currently, the accessibility code
has a model where AXMode is checked on API calls or tree updates.
Synchronously destroying the WebUI tab strip can lead to UAF so post a
task to do this work when the AXMode changes.

(cherry picked from commit c1ce12c32b780b2dafe1e4c27a0d2e4db179030c)

Bug: 1277328
Change-Id: Ic1391c93c95af1c936d6b55b93668207de5d6598
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3368621
Commit-Queue: Daniel Libby <dlibby@microsoft.com>
Cr-Original-Commit-Position: refs/heads/main@{#956181}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3427975
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1447}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/6e0153b5f3db457f23a9ee11af42547fb4d72f2c/chrome/browser/ui/views/frame/browser_view.cc


### rz...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-11)

Congratulations - the VRP Panel has decided to award you $7,000 for this report. Thanks for your efforts and reporting this issue to us! 

### am...@google.com (2022-02-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2022-09-26)

Crash no longer being reported. Issue presumed fixed

### am...@chromium.org (2022-12-13)

This issue is a duplicate of a previously reported https://crbug.com/chromium/1262902; could not be merged at the time as the fix was landed on this issue.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1277328?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1277324, crbug.com/chromium/1282852, crbug.com/chromium/1282988, crbug.com/chromium/1282992, crbug.com/chromium/1283211]
[Monorail mergedinto: crbug.com/chromium/1262902]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058147)*

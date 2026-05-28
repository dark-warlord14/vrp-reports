# Security: heap-use-after-free in blink::PropertyTreeManager::EnsureCompositorTransformNode

| Field | Value |
|-------|-------|
| **Issue ID** | [40062206](https://issues.chromium.org/issues/40062206) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Compositing |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | xi...@chromium.org |
| **Created** | 2022-12-13 |
| **Bounty** | $8,000.00 |

## Description

**VULNERABILITY DETAILS**  

A portal adopting a portal predecessor selected in a nested <selectmenu> causes UaF.

**VERSION**  

Chrome Version: 110.0.5475.0  

Operating System: Windows

**REPRODUCTION CASE**

1. python3 -m http.server 9000
2. chrome --enable-features=Portals --enable-experimental-web-platform-features
3. Open DevTools
4. Open <http://localhost:9000/poc.html>

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: tab Crash State:

==34456==ERROR: AddressSanitizer: heap-use-after-free on address 0x11f738905aa0 at pc 0x7ff877fe5e69 bp 0x0020f9bfdb40 sp 0x0020f9bfdb88  

WRITE of size 8 at 0x11f738905aa0 thread T0  

==34456==WARNING: Failed to use and restart external symbolizer!  

==34456==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==34456==\*\*\* Most likely this means that the app is already \*\*\*  

==34456==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==34456==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==34456==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ff877fe5e68 in blink::PropertyTreeManager::EnsureCompositorTransformNode C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\graphics\compositing\property\_tree\_manager.cc:469  

#1 0x7ff877fe47d6 in blink::PropertyTreeManager::EnsureCompositorTransformNode C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\graphics\compositing\property\_tree\_manager.cc:390  

#2 0x7ff877fe3fc0 in blink::PropertyTreeManager::EnsureCompositorScrollNodes C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\graphics\compositing\property\_tree\_manager.cc:222  

#3 0x7ff873c1ab50 in blink::PaintArtifactCompositor::Update C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\graphics\compositing\paint\_artifact\_compositor.cc:684  

#4 0x7ff8704f8df3 in blink::LocalFrameView::PushPaintArtifactToCompositor C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3123  

#5 0x7ff8704f3e63 in blink::LocalFrameView::RunPaintLifecyclePhase C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2790  

#6 0x7ff8704f0799 in blink::LocalFrameView::UpdateLifecyclePhasesInternal C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2521  

#7 0x7ff8704ed27e in blink::LocalFrameView::UpdateLifecyclePhases C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2324  

#8 0x7ff8704ec6c4 in blink::LocalFrameView::UpdateAllLifecyclePhases C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2087  

#9 0x7ff87386244f in blink::PageAnimator::UpdateAllLifecyclePhases C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\page\page\_animator.cc:159  

#10 0x7ff87049aabd in blink::WebFrameWidgetImpl::UpdateLifecycle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\web\_frame\_widget\_impl.cc:1394  

#11 0x7ff873a9ebcb in blink::WidgetBase::UpdateVisualState C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\widget\_base.cc:892  

#12 0x7ff86e02e733 in cc::LayerTreeHost::RequestMainFrameUpdate C:\b\s\w\ir\cache\builder\src\cc\trees\layer\_tree\_host.cc:376  

#13 0x7ff871657c5d in cc::ProxyMain::BeginMainFrame C:\b\s\w\ir\cache\builder\src\cc\trees\proxy\_main.cc:280  

#14 0x7ff8762013cc in base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState,std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >),base::WeakPtr[cc::ProxyMain](javascript:void(0);),std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState,std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:924  

#15 0x7ff86b299e70 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:157  

#16 0x7ff86e43c2ba in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:484  

#17 0x7ff86e43aecb in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:335  

#18 0x7ff86e40e433 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:48  

#19 0x7ff86e43e853 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:644  

#20 0x7ff86b22937e in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#21 0x7ff86de4c59e in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:330  

#22 0x7ff86addace7 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:746  

#23 0x7ff86addd518 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1100  

#24 0x7ff86add8666 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:344  

#25 0x7ff86add94c1 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:372  

#26 0x7ff85e8814a5 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:174  

#27 0x7ff7fa6062f8 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#28 0x7ff7fa602c26 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:391  

#29 0x7ff7faa3464b in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#30 0x7ff947a8247c in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x18001247c)  

#31 0x7ff94918dfb7 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005dfb7)

0x11f738905aa0 is located 2592 bytes inside of 2944-byte region [0x11f738905080,0x11f738905c00)  

freed by thread T0 here:  

#0 0x7ff7fa6aecdd in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ff86e09378a in std::Cr::vector<cc::TransformNode,std::Cr::allocator[cc::TransformNode](javascript:void(0);) >::\_\_push\_back\_slow\_path[cc::TransformNode](javascript:void(0);) C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:1534  

#2 0x7ff86e06bc17 in cc::PropertyTree[cc::TransformNode](javascript:void(0);)::Insert C:\b\s\w\ir\cache\builder\src\cc\trees\property\_tree.cc:79  

#3 0x7ff86e06fc2c in cc::TransformTree::Insert C:\b\s\w\ir\cache\builder\src\cc\trees\property\_tree.cc:126  

#4 0x7ff877fe483e in blink::PropertyTreeManager::EnsureCompositorTransformNode C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\graphics\compositing\property\_tree\_manager.cc:391  

#5 0x7ff877fe47d6 in blink::PropertyTreeManager::EnsureCompositorTransformNode C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\graphics\compositing\property\_tree\_manager.cc:390  

#6 0x7ff877fe51ba in blink::PropertyTreeManager::EnsureCompositorTransformNode C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\graphics\compositing\property\_tree\_manager.cc:458  

#7 0x7ff877fe47d6 in blink::PropertyTreeManager::EnsureCompositorTransformNode C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\graphics\compositing\property\_tree\_manager.cc:390  

#8 0x7ff877fe3fc0 in blink::PropertyTreeManager::EnsureCompositorScrollNodes C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\graphics\compositing\property\_tree\_manager.cc:222  

#9 0x7ff873c1ab50 in blink::PaintArtifactCompositor::Update C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\graphics\compositing\paint\_artifact\_compositor.cc:684  

#10 0x7ff8704f8df3 in blink::LocalFrameView::PushPaintArtifactToCompositor C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3123  

#11 0x7ff8704f3e63 in blink::LocalFrameView::RunPaintLifecyclePhase C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2790  

#12 0x7ff8704f0799 in blink::LocalFrameView::UpdateLifecyclePhasesInternal C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2521  

#13 0x7ff8704ed27e in blink::LocalFrameView::UpdateLifecyclePhases C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2324  

#14 0x7ff8704ec6c4 in blink::LocalFrameView::UpdateAllLifecyclePhases C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2087  

#15 0x7ff87386244f in blink::PageAnimator::UpdateAllLifecyclePhases C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\page\page\_animator.cc:159  

#16 0x7ff87049aabd in blink::WebFrameWidgetImpl::UpdateLifecycle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\web\_frame\_widget\_impl.cc:1394  

#17 0x7ff873a9ebcb in blink::WidgetBase::UpdateVisualState C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\widget\_base.cc:892  

#18 0x7ff86e02e733 in cc::LayerTreeHost::RequestMainFrameUpdate C:\b\s\w\ir\cache\builder\src\cc\trees\layer\_tree\_host.cc:376  

#19 0x7ff871657c5d in cc::ProxyMain::BeginMainFrame C:\b\s\w\ir\cache\builder\src\cc\trees\proxy\_main.cc:280  

#20 0x7ff8762013cc in base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState,std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >),base::WeakPtr[cc::ProxyMain](javascript:void(0);),std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState,std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:924  

#21 0x7ff86b299e70 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:157  

#22 0x7ff86e43c2ba in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:484  

#23 0x7ff86e43aecb in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:335  

#24 0x7ff86e40e433 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:48  

#25 0x7ff86e43e853 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:644  

#26 0x7ff86b22937e in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#27 0x7ff86de4c59e in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:330

previously allocated by thread T0 here:  

#0 0x7ff7fa6aeddd in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff87fa2b81e in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ff86e093629 in std::Cr::vector<cc::TransformNode,std::Cr::allocator[cc::TransformNode](javascript:void(0);) >::\_\_push\_back\_slow\_path[cc::TransformNode](javascript:void(0);) C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:1529  

#3 0x7ff86e06bc17 in cc::PropertyTree[cc::TransformNode](javascript:void(0);)::Insert C:\b\s\w\ir\cache\builder\src\cc\trees\property\_tree.cc:79  

#4 0x7ff86e06fc2c in cc::TransformTree::Insert C:\b\s\w\ir\cache\builder\src\cc\trees\property\_tree.cc:126  

#5 0x7ff877fe483e in blink::PropertyTreeManager::EnsureCompositorTransformNode C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\graphics\compositing\property\_tree\_manager.cc:391  

#6 0x7ff877fe733d in blink::PropertyTreeManager::EnsureCompositorClipNode C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\graphics\compositing\property\_tree\_manager.cc:532  

#7 0x7ff873c1aaa2 in blink::PaintArtifactCompositor::Update C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\graphics\compositing\paint\_artifact\_compositor.cc:678  

#8 0x7ff8704f8df3 in blink::LocalFrameView::PushPaintArtifactToCompositor C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3123  

#9 0x7ff8704f3e63 in blink::LocalFrameView::RunPaintLifecyclePhase C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2790  

#10 0x7ff8704f0799 in blink::LocalFrameView::UpdateLifecyclePhasesInternal C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2521  

#11 0x7ff8704ed27e in blink::LocalFrameView::UpdateLifecyclePhases C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2324  

#12 0x7ff8704ec6c4 in blink::LocalFrameView::UpdateAllLifecyclePhases C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2087  

#13 0x7ff87386244f in blink::PageAnimator::UpdateAllLifecyclePhases C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\page\page\_animator.cc:159  

#14 0x7ff87049aabd in blink::WebFrameWidgetImpl::UpdateLifecycle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\web\_frame\_widget\_impl.cc:1394  

#15 0x7ff873a9ebcb in blink::WidgetBase::UpdateVisualState C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\widget\_base.cc:892  

#16 0x7ff86e02e733 in cc::LayerTreeHost::RequestMainFrameUpdate C:\b\s\w\ir\cache\builder\src\cc\trees\layer\_tree\_host.cc:376  

#17 0x7ff871657c5d in cc::ProxyMain::BeginMainFrame C:\b\s\w\ir\cache\builder\src\cc\trees\proxy\_main.cc:280  

#18 0x7ff8762013cc in base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState,std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >),base::WeakPtr[cc::ProxyMain](javascript:void(0);),std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState,std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:924  

#19 0x7ff86b299e70 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:157  

#20 0x7ff86e43c2ba in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:484  

#21 0x7ff86e43aecb in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:335  

#22 0x7ff86e40e433 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:48  

#23 0x7ff86e43e853 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:644  

#24 0x7ff86b22937e in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#25 0x7ff86de4c59e in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:330  

#26 0x7ff86addace7 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:746  

#27 0x7ff86addd518 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1100

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\graphics\compositing\property\_tree\_manager.cc:469 in blink::PropertyTreeManager::EnsureCompositorTransformNode  

Shadow bytes around the buggy address:  

0x11f738905800: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11f738905880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11f738905900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11f738905980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11f738905a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x11f738905a80: fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd  

0x11f738905b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11f738905b80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11f738905c00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x11f738905c80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11f738905d00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==34456==ABORTING

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 643 B)
- [portal.html](attachments/portal.html) (text/plain, 147 B)
- [poc.webm](attachments/poc.webm) (video/webm, 1.3 MB)
- [new-poc.html](attachments/new-poc.html) (text/plain, 763 B)
- [new-poc.webm](attachments/new-poc.webm) (video/webm, 700.8 KB)
- [asan.log](attachments/asan.log) (text/plain, 26.2 KB)

## Timeline

### [Deleted User] (2022-12-13)

[Empty comment from Monorail migration]

### st...@gmail.com (2022-12-13)

Update: I found an easier way to repro this without DevTools and Portals. ASan backtrace is the same.

./chrome --enable-experimental-web-platform-features http://localhost:9000/new-poc.html

### aj...@google.com (2022-12-13)

Thanks this reproduces on HEAD at 5463693. Attached log with the first poc.

### aj...@google.com (2022-12-13)

The second poc weirdly does gets a STATUS_ACCESS_VIOLATION but not an asan stack trace.

-> xiaochengh from git blame around EnsureAnchorScrollContainersData (https://chromium-review.googlesource.com/c/chromium/src/+/3774762)
-> High (renderer RCE)
-> None (--enable-experimental-web-platform-features)

Please investigate and fix this security issue - if the code is reachable in shipped versions of Chrome please let me know so I can adjust the impact.



[Monorail components: Internals>Compositing]

### st...@gmail.com (2022-12-13)

Bisect:

Reproducible since commit 7b60f9a0bbaa5536887a1e23689d5cef52f0a48c
Affected Chrome releases: Canary 110.0.5468.0 and newer

### aj...@google.com (2022-12-13)

Thanks for the bisect in https://crbug.com/chromium/1400522#c5 - adjusting FoundIn - as the crashing code has been around longer it's possible there are other ways to reach this.

### xi...@chromium.org (2022-12-13)

I actually hit a DCHECK:

[21495:1:1213/140358.784255:FATAL:paint_property_tree_builder.cc(806)] Check failed: inner_most_scroll_container.

This occurs if:
- In the previous frame, the AnchorScrollData object has a scroller
- In the next frame, the scroller is gone, and there's something else triggering a paint update on the anchor-positioned element

Not sure if this is the root cause of this UaF, but I'll fix the DCHECK hit first anyways.

Repro:

<div id="scroller">
  <div id="spacer"></div>
  <div id="anchor">anchor</div>
</div>
<div id="target">target</div>

<style>
#scroller {
  margin-top: 200px;
  height: 200px;
  overflow-y: scroll;
}

#anchor {
  anchor-name: --a;
}

#spacer {
  height: 400px;
}

#target {
  position: fixed;
  top: anchor(--a bottom);
  left: anchor(--a left);
  anchor-scroll: --a;
}
</style>

<script>
setTimeout(() => {
  spacer.style.height = '0';
  target.style.transform = 'scale(1)';
}, 200);
</script>


### xi...@chromium.org (2022-12-13)

CL: crrev.com/c/4104980

The uaf also seems gone after this patch.

### xi...@chromium.org (2022-12-16)

I figured it out.

The uaf object is created and freed at property_tree.cc:79:

```
template <typename T>
int PropertyTree<T>::Insert(const T& tree_node, int parent_id) {
  DCHECK_GT(nodes_.size(), 0u);
  nodes_.push_back(tree_node);  <---
  T& node = nodes_.back();
  node.parent_id = parent_id;
  node.id = static_cast<int>(nodes_.size()) - 1;
  return node.id;
}
```

And the use-after-free is at compositing/property_tree_manager.cc:469
```
  auto compositor_element_id = transform_node.GetCompositorElementId();
  if (compositor_element_id) {
    transform_tree_.SetElementIdForNodeId(id, compositor_element_id);
    compositor_node.element_id = compositor_element_id;  <---
  }
```

Here we are holding |compositor_node| as a reference to a vector entry, but the vector can be reallocated in the previous EnsureCompositorScrollNode call at L458/460, leaving |compositor_node| reference invalid.

Sticky positioning does the same but is safe from this issue, because it only calls EnsureCompositorScrollNode for an ancestor node, so at this time the scroll node should have already been created.

Anchor positioning does that for a node in a different subtree, and causes this issue.

So the uaf bug is unrelated to this patch, and the right fix should be to change |compositor_node| into a ptr and revalidate it after EnsureCompositorScrollNode calls.


### xi...@chromium.org (2022-12-16)

Filed https://crbug.com/chromium/1401827 for the DCHECK hit, which has a different cause.

### st...@gmail.com (2022-12-16)

xiaochengh@, you might want to add visibility protections (Restrict-View-...) to the issue in https://crbug.com/chromium/1400522#c10 as it contains a repro for the UaF.

### xi...@chromium.org (2022-12-16)

The other issue should be fine. It's not a repro for this UaF, but a DCHECK hit, or a nullptr deref in a production build.

### gi...@appspot.gserviceaccount.com (2023-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c9ec3e13113e061313cbf534eb55f8c7cdd17400

commit c9ec3e13113e061313cbf534eb55f8c7cdd17400
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Tue Jan 10 02:33:12 2023

[anchor-position] Always use compositor scroller ids for composited scrolling

The existing implementation for composited scrolling is problematic
because if scrollers have changed in a style update, then it might
access data that is stale or already gone in the subsequent paint
property tree building.

This patch basically follows the outline in crbug.com/1401827#c2:
- It changes Blink::AnchorScrollData to store CompositorElementId instead
of PaintLayer for the relevant scroll containers, so that we don't
need to access the snapshotted PaintLayer/PaintLayerScrollableArea in
PrePaint and Paint, at which time they may have been stale
- This also moves the job of scroller validation (i.e., whether there
is a ScrollNode on cc side) completely to cc, which is much saner
compared to the previous heuristic of checking HasOverflow() on the
Blink side
- This also fixes crbug.com/1400522, as we no longer create one cc
TransformNode in the middle of creating another

Note that unlike the outline, there's no AnchorScrollData validation
at PrePaint on the Blink side. Since everything we pass to cc are just
scroller ids, and scroller id validation is done completely by cc, further validation in Blink is unnecessary.

Fixed: 1400522, 1401827
Change-Id: Ief68d18e4484cfbe8d4f1037f5d5cb6c6de9687f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4137178
Reviewed-by: Xianzhu Wang <wangxianzhu@chromium.org>
Reviewed-by: Philip Rogers <pdr@chromium.org>
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1090660}

[modify] https://crrev.com/c9ec3e13113e061313cbf534eb55f8c7cdd17400/cc/trees/draw_properties_unittest.cc
[add] https://crrev.com/c9ec3e13113e061313cbf534eb55f8c7cdd17400/third_party/blink/web_tests/external/wpt/css/css-anchor-position/anchor-scroll-composited-scrolling-002-crash.html
[modify] https://crrev.com/c9ec3e13113e061313cbf534eb55f8c7cdd17400/third_party/blink/renderer/core/layout/anchor_scroll_data.cc
[add] https://crrev.com/c9ec3e13113e061313cbf534eb55f8c7cdd17400/third_party/blink/web_tests/external/wpt/css/css-anchor-position/anchor-scroll-composited-scrolling-004-crash.html
[modify] https://crrev.com/c9ec3e13113e061313cbf534eb55f8c7cdd17400/third_party/blink/renderer/platform/graphics/compositing/property_tree_manager.cc
[add] https://crrev.com/c9ec3e13113e061313cbf534eb55f8c7cdd17400/third_party/blink/web_tests/external/wpt/css/css-anchor-position/anchor-scroll-composited-scrolling-005-crash.html
[modify] https://crrev.com/c9ec3e13113e061313cbf534eb55f8c7cdd17400/cc/trees/property_tree.h
[add] https://crrev.com/c9ec3e13113e061313cbf534eb55f8c7cdd17400/third_party/blink/web_tests/external/wpt/html/semantics/forms/the-selectmenu-element/selectmenu-listbox-fallback-change-crash.tentative.html
[modify] https://crrev.com/c9ec3e13113e061313cbf534eb55f8c7cdd17400/cc/trees/property_tree.cc
[add] https://crrev.com/c9ec3e13113e061313cbf534eb55f8c7cdd17400/third_party/blink/web_tests/external/wpt/css/css-anchor-position/anchor-scroll-composited-scrolling-003-crash.html
[rename] https://crrev.com/c9ec3e13113e061313cbf534eb55f8c7cdd17400/third_party/blink/web_tests/external/wpt/css/css-anchor-position/anchor-scroll-composited-scrolling-001-crash.html
[modify] https://crrev.com/c9ec3e13113e061313cbf534eb55f8c7cdd17400/third_party/blink/renderer/core/paint/paint_property_tree_builder.cc
[modify] https://crrev.com/c9ec3e13113e061313cbf534eb55f8c7cdd17400/third_party/blink/renderer/platform/graphics/paint/transform_paint_property_node.h
[modify] https://crrev.com/c9ec3e13113e061313cbf534eb55f8c7cdd17400/third_party/blink/renderer/core/layout/anchor_scroll_data.h


### [Deleted User] (2023-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-10)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-18)

Congratulations, Thomas! The VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### am...@google.com (2023-01-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-04-18)

This issue was migrated from crbug.com/chromium/1400522?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1309178]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062206)*

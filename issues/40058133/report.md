# AddressSanitizer: use-after-poison ng_physical_fragment.h:316 in blink::NGPhysicalFragment::HasSelfPaintingLayer

| Field | Value |
|-------|-------|
| **Issue ID** | [40058133](https://issues.chromium.org/issues/40058133) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | fu...@chromium.org |
| **Created** | 2021-12-06 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4676.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-948429.zip

#Reproduce
1. unzip poc.zip
2. python -m http.server 80
3. chrome --js-flags='--expose_gc --allow-natives-syntax' --no-sandbox --enable-blink-test-features --user-data-dir=notexits http://localhost/poc.html
4. If it does not reproduce, ctrl+f5 refresh

What is the expected behavior?

What went wrong?
Type of crash
render tab

#Analysis
Come soon

#Patch
Not yet

#asan
=================================================================
==7464==ERROR: AddressSanitizer: use-after-poison on address 0x7eb000a031e8 at pc 0x7ff95ddbd2d0 bp 0x006f3b3fd280 sp 0x006f3b3fd2c8
READ of size 4 at 0x7eb000a031e8 thread T0
==7464==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff95ddbd2cf in blink::NGPhysicalFragment::HasSelfPaintingLayer C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_physical_fragment.h:316
    #1 0x7ff95ddc7ad1 in blink::NGBoxFragmentPainter::PaintBlockChildren C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\ng\ng_box_fragment_painter.cc:744
    #2 0x7ff95ddc1ddb in blink::NGBoxFragmentPainter::PaintObject C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\ng\ng_box_fragment_painter.cc:616
    #3 0x7ff95ddbe7b7 in blink::NGBoxFragmentPainter::PaintInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\ng\ng_box_fragment_painter.cc:467
    #4 0x7ff95a538120 in blink::PaintLayerPainter::PaintFragmentWithPhase C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\paint_layer_painter.cc:812
    #5 0x7ff95a53702c in blink::PaintLayerPainter::PaintForegroundForFragmentsWithPhase C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\paint_layer_painter.cc:891
    #6 0x7ff95a537424 in blink::PaintLayerPainter::PaintForegroundForFragments C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\paint_layer_painter.cc:856
    #7 0x7ff95a5336d3 in blink::PaintLayerPainter::PaintLayerContents C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\paint_layer_painter.cc:625
    #8 0x7ff95a530e40 in blink::PaintLayerPainter::Paint C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\paint_layer_painter.cc:147
    #9 0x7ff95a536a63 in blink::PaintLayerPainter::PaintChildren C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\paint_layer_painter.cc:743
    #10 0x7ff95a5337f7 in blink::PaintLayerPainter::PaintLayerContents C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\paint_layer_painter.cc:637
    #11 0x7ff95a530e40 in blink::PaintLayerPainter::Paint C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\paint_layer_painter.cc:147
    #12 0x7ff95a5309e8 in blink::PaintLayerPainter::Paint C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\paint_layer_painter.cc:42
    #13 0x7ff95a53927a in blink::FramePainter::PaintContents C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\frame_painter.cc:114
    #14 0x7ff95a538c35 in blink::FramePainter::Paint C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\frame_painter.cc:56
    #15 0x7ff957173199 in blink::LocalFrameView::PaintTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3007
    #16 0x7ff95716dd09 in blink::LocalFrameView::RunPaintLifecyclePhase C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2806
    #17 0x7ff95716a1da in blink::LocalFrameView::UpdateLifecyclePhasesInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2541
    #18 0x7ff957167200 in blink::LocalFrameView::UpdateLifecyclePhases C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2370
    #19 0x7ff957166d7e in blink::LocalFrameView::UpdateAllLifecyclePhases C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2114
    #20 0x7ff95a0f0e28 in blink::PageAnimator::UpdateAllLifecyclePhases C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\page\page_animator.cc:153
    #21 0x7ff95711f07d in blink::WebFrameWidgetImpl::UpdateLifecycle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\web_frame_widget_impl.cc:1296
    #22 0x7ff95a1c66a3 in blink::WidgetBase::UpdateVisualState C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\widget\widget_base.cc:808
    #23 0x7ff954d9731a in cc::LayerTreeHost::RequestMainFrameUpdate C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host.cc:346
    #24 0x7ff957d934bf in cc::ProxyMain::BeginMainFrame C:\b\s\w\ir\cache\builder\src\cc\trees\proxy_main.cc:257
    #25 0x7ff95be1f652 in base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::*)(std::__1::unique_ptr<cc::BeginMainFrameAndCommitState,std::__1::default_delete<cc::BeginMainFrameAndCommitState> >),base::WeakPtr<cc::ProxyMain>,std::__1::unique_ptr<cc::BeginMainFrameAndCommitState,std::__1::default_delete<cc::BeginMainFrameAndCommitState> > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:741
    #26 0x7ff9525f6684 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #27 0x7ff9551545e5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356
    #28 0x7ff955153cb8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #29 0x7ff95512ca57 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:38
    #30 0x7ff955155cb1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468
    #31 0x7ff9525762a3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
    #32 0x7ff954c1387e in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:278
    #33 0x7ff94e221b31 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:678
    #34 0x7ff94e223797 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1028
    #35 0x7ff94e21f8f9 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398
    #36 0x7ff94e220984 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:426
    #37 0x7ff947ae148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:172
    #38 0x7ff7f8af5b65 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #39 0x7ff7f8af2c31 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #40 0x7ff7f8ef4cbf in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #41 0x7ff9d40e7033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #42 0x7ff9d51e2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

Address 0x7eb000a031e8 is a wild pointer inside of access range of size 0x000000000004.
SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_physical_fragment.h:316 in blink::NGPhysicalFragment::HasSelfPaintingLayer
Shadow bytes around the buggy address:
  0x1157c21c05e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1157c21c05f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1157c21c0600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1157c21c0610: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1157c21c0620: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x1157c21c0630: 00 00 00 00 00 00 00 00 00 f7 f7 f7 f7[f7]f7 f7
  0x1157c21c0640: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x1157c21c0650: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 f7 f7 f7
  0x1157c21c0660: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x1157c21c0670: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 f7 f7 f7
  0x1157c21c0680: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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
==7464==ABORTING

Did this work before? N/A 

Chrome version: 100.0.4676.0  Channel: n/a
OS Version: 10.0

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 8.5 KB)
- [poc.zip](attachments/poc.zip) (application/octet-stream, 66.0 KB)
- [cl_1276898.zip](attachments/cl_1276898.zip) (application/octet-stream, 66.0 KB)

## Timeline

### [Deleted User] (2021-12-06)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-12-06)

Can you please provide the PoC?

### m....@gmail.com (2021-12-06)

re https://crbug.com/chromium/1276898#c2 Sorry for the delay, because the casereduce has not been completed before~

### cl...@chromium.org (2021-12-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6395591166590976.

### do...@chromium.org (2021-12-07)

ClusterFuzz can't reproduce this one, but there's a Ctrl-Refresh interaction that it might not be simulating. +kojii, can you take a look?

I'll mark this as Medium severity since ClusterFuzz can't reproduce (indicating the user action of a refresh might be needed to help make this happen reliably).[1]

The code doesn't look like it's changed very recently; tentatively marking this as appearing in Stable for now.

1. https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#toc-medium-severity

[Monorail components: Blink>Layout]

### m....@gmail.com (2021-12-07)

This issue not require user action.

ClusterFuzz cannot reproduce this, because many of the paths and ports in it are hard-coded(http://localhost/h1.js). The ClusterFuzz environment is inconsistent with the test environment I provided, resulting in many dependencies that cannot be loaded.

### [Deleted User] (2021-12-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-12-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4575746913533952.

### do...@chromium.org (2021-12-07)

Possibly the test case wasn't formatted correctly the first time round. I'll try uploading it again to see if that fixes it.

### do...@chromium.org (2021-12-07)

#6 ah, thanks for clarifying. If that's the case, I will update this to High for now.

### m....@gmail.com (2021-12-07)

I changed some absolute address references to relative addresses, which is friendly to ClusterFuzz.
ClusterFuzz does not allow me to modify the command line parameters, otherwise I can test it myself.

### cl...@chromium.org (2021-12-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5352415446237184.

### do...@chromium.org (2021-12-07)

Thanks, I'll upload that.

FYI, I think Clusterfuzz prefers the poc file to be called "index.html" rather than "poc.html" in the zip file.

### do...@chromium.org (2021-12-07)

Looks to me that ClusterFuzz thinks this, https://crbug.com/chromium/1277359, and https://crbug.com/chromium/1277004 are all duplicates of each other.

### m....@gmail.com (2021-12-07)

re https://crbug.com/chromium/1276898#c14 It seems that the latest chromium version causes these use cases to crash in one place, can you use the 948429 version to test？

### [Deleted User] (2021-12-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ko...@chromium.org (2021-12-07)

The stack is under `RuntimeEnabledFeatures::CSSContainerQueriesEnabled`. Rune, can you take a look?

[Monorail components: -Blink>Layout Blink>CSS]

### do...@chromium.org (2021-12-07)

#15: ClusterFuzz's regression testing rolled through that range and looks like it didn't crash (I'd be a bit surprised if a different crash happened and Clusterfuzz just kept on going. Though maybe that happens?):

[2021-12-07 17:09:18 UTC] clusterfuzz-linux-sdxb: Regression task in-progress: Testing r941180 (current range 933402:948915).
[2021-12-07 17:35:15 UTC] clusterfuzz-linux-sdxb: Regression task in-progress: Testing r945153 (current range 941180:948915).
[2021-12-07 18:01:50 UTC] clusterfuzz-linux-sdxb: Regression task in-progress: Testing r946934 (current range 945153:948915).
[2021-12-07 18:03:59 UTC] clusterfuzz-linux-d8b6: Progression task started: r949014.
[2021-12-07 18:28:44 UTC] clusterfuzz-linux-sdxb: Regression task in-progress: Testing r948081 (current range 946934:948915).
[2021-12-07 18:54:47 UTC] clusterfuzz-linux-sdxb: Regression task in-progress: Testing r948437 (current range 948081:948915).
[2021-12-07 18:55:45 UTC] clusterfuzz-linux-d8b6: Progression task finished: still crashes on latest revision r949014.
[2021-12-07 19:20:29 UTC] clusterfuzz-linux-sdxb: Regression task in-progress: Testing r948660 (current range 948437:948915).
[2021-12-07 19:42:09 UTC] clusterfuzz-linux-sdxb: Regression task in-progress: Testing r948504 (current range 948437:948660).
[2021-12-07 20:12:04 UTC] clusterfuzz-linux-sdxb: Regression task in-progress: Testing r948554 (current range 948504:948660).

### do...@chromium.org (2021-12-07)

Looks like this is from https://chromium.googlesource.com/chromium/src/+/200d27d3de29a7ac5aa0249b98676790f29f9c30.

### do...@chromium.org (2021-12-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-07)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-12-07)

Reporter: it may be there are a couple of issues here. We'll focus on the one ClusterFuzz narrowed down first, and once that's fixed, if we can still repro a different one, we can reopen another issue for that.

### [Deleted User] (2021-12-08)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-08)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-08)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fu...@chromium.org (2021-12-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-12-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f27a54c99b20971d9732d8fa05183a38ad1d9a49

commit f27a54c99b20971d9732d8fa05183a38ad1d9a49
Author: Morten Stenshorne <mstensho@chromium.org>
Date: Thu Dec 09 08:54:17 2021

Disallow container queries at or inside multicol containers.

Container queries will remain disallowed until we have full NG block
fragmentation support, for all layout types, including printing.

The reason is that, with container queries, style is recalculated during
layout. We cannot risk that we switch between legacy and NG layout while
we're there, since we may have started NG layout on ancestors that style
recalc suddenly wants to be legacy.

Had to improve the multicol detection mechanism that's run during style
recalc because of this, to ensure that we only trigger legacy fallback
when an element is actually going to become a multicol container (which
isn't the case for e.g. <span style="columns:2;">). Otherwise we may
trigger unnecessary legacy layout fallback on ancestors all the way up
to the block formatting context root, which may already be in the middle
of NG layout, if we're evaluating container queries.

Regarding the tests included: The inline-with-columns-* ones would only
crash without LayoutNGBlockFragmentation enabled, while all the others
would only crash *with* LayoutNGBlockFragmentation enabled.

Had to update a couple of unit tests that no longer get legacy fallback
(because there aren't actually any multicols there).

Bug: 1276898
AX-Relnotes: n/a
Change-Id: Ia75fe86d91966233ffeea43a3940113b6a431075
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3320292
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Reviewed-by: Aaron Leventhal <aleventhal@chromium.org>
Commit-Queue: Morten Stenshorne <mstensho@chromium.org>
Cr-Commit-Position: refs/heads/main@{#949990}

[delete] https://crrev.com/999cd2a17a5b1c70c5294ab5e4990dc2a129a429/content/test/data/accessibility/css/marker-crash-without-layout-ng-block-frag.html
[add] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/table-in-columns-002-crash.html
[add] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/flex-in-columns-001-crash.html
[add] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/inline-with-columns-000-crash.html
[add] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/flex-in-columns-003-crash.html
[modify] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/renderer/core/style/computed_style_extra_fields.json5
[modify] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/renderer/core/layout/layout_block_flow_test.cc
[add] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/grid-in-columns-003-crash.html
[modify] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/renderer/core/dom/element.cc
[add] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/grid-in-columns-001-crash.html
[add] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/table-in-columns-003-crash.html
[modify] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/content/browser/accessibility/dump_accessibility_tree_browsertest.cc
[delete] https://crrev.com/999cd2a17a5b1c70c5294ab5e4990dc2a129a429/content/test/data/accessibility/css/marker-crash-without-layout-ng-block-frag-expected-blink.txt
[add] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/flex-in-columns-002-crash.html
[add] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/table-in-columns-001-crash.html
[add] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/flex-in-columns-000-crash.html
[add] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/table-in-columns-000-crash.html
[modify] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/renderer/core/style/computed_style.h
[modify] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/renderer/core/css/resolver/style_adjuster.cc
[add] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/grid-in-columns-002-crash.html
[add] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/grid-in-columns-000-crash.html
[add] https://crrev.com/f27a54c99b20971d9732d8fa05183a38ad1d9a49/third_party/blink/web_tests/external/wpt/css/css-contain/container-queries/inline-with-columns-001-crash.html


### am...@chromium.org (2022-01-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-12)

reversed the merge of this into 1276933 and merged https://crbug.com/chromium/1276933 into this issue, as this is the earlier report and the fix CL was landed on this issue 

### [Deleted User] (2022-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-12)

Not requesting merge to beta (M98) because latest trunk commit (949990) appears to be prior to beta branch point (950365). If this is incorrect, please replace the Merge-NA-98 label with Merge-Request-98. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-01-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-13)

Congratulations! The VRP Panel has decided to award you $5000 for this report. Thank you for this report and great work! 

### am...@google.com (2022-01-14)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1276898?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1276933, crbug.com/chromium/1277359]
[Monorail mergedinto: crbug.com/chromium/1276933]
[Monorail components added to Component Tags custom field.]

### ch...@google.com (2025-07-18)

futhark: Uh oh! This issue still open and hasn't been updated in the last 1317 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-18)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### ms...@chromium.org (2025-07-18)

Amy, I think the robots messed up here. Close?

### ch...@google.com (2025-07-21)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### fu...@chromium.org (2025-07-21)

I don't know how to close this so that is not re-opened. This was fixed years ago.


### ch...@google.com (2025-10-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058133)*

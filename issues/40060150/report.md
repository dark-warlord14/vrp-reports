# heap-overflow in blink::TableLayoutAlgorithmAuto::InsertSpanCell table_layout_algorithm_auto.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40060150](https://issues.chromium.org/issues/40060150) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | bi...@chromium.org |
| **Created** | 2022-07-03 |
| **Bounty** | $7,500.00 |

## Description

**Steps to reproduce the problem:**  

#TestOn  

asan-win32-release\_x64-1020412

#Reproduce

1. chrome --no-sandbox --user-data-dir=test poc.html

**Problem Description:**  

ype of crash  

render tab

#Analysis  

The root cause of the problem is that the sizeof(Member<LayoutTableCell>) is not the same as the sizeof(LayoutTableCell\*) due to CPPGC\_POINTER\_COMPRESSION  

Using the test patch I provided, the log shows that the value of sizeof(Member<LayoutTableCell>) is 4 and the value of sizeof(LayoutTableCell\*) is 8

```
#https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/layout/table_layout_algorithm_auto.h;drc=a9ff21200983d63b5cffc4d5b56b5024af314a44;l=96  
HeapVector<Member<LayoutTableCell>, 4> span_cells_;						<<--[1]  
  
#https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/layout/table_layout_algorithm_auto.cc;drc=a9ff21200983d63b5cffc4d5b56b5024af314a44;l=654  
void TableLayoutAlgorithmAuto::InsertSpanCell(LayoutTableCell\* cell) {  
  DCHECK(cell);  
  DCHECK_NE(cell->ColSpan(), 1u);  
  if (!cell || cell->ColSpan() == 1)  
    return;  
...CUT...  
  unsigned pos = 0;  
  unsigned span = cell->ColSpan();  
  while (pos < span_cells_.size() && span_cells_[pos] &&  
         span > span_cells_[pos]->ColSpan())  
    pos++;  
  memmove(span_cells_.data() + pos + 1, span_cells_.data() + pos,  
          (size - pos - 1) \* sizeof(LayoutTableCell\*));					<<--[2]  
  span_cells_[pos] = cell;  
}  
  
#test patch  
--- a/third_party/blink/renderer/core/layout/table_layout_algorithm_auto.cc  
+++ b/third_party/blink/renderer/core/layout/table_layout_algorithm_auto.cc  
@@ -672,6 +672,12 @@ void TableLayoutAlgorithmAuto::InsertSpanCell(LayoutTableCell\* cell) {  
   while (pos < span_cells_.size() && span_cells_[pos] &&  
          span > span_cells_[pos]->ColSpan())  
     pos++;  
+  
+  LOG(WARNING) << "pos-> " << pos << "  size-> " << span_cells_.size()  
+               << " data->" << span_cells_.data() << "  data+1-> "  
+               << span_cells_.data() + 1 << " sizeof(LayoutTableCell\*)-> "  
+               << sizeof(LayoutTableCell\*) << " member-> "  
+               << sizeof(Member<LayoutTableCell>);  
   memmove(span_cells_.data() + pos + 1, span_cells_.data() + pos,  
           (size - pos - 1) \* sizeof(LayoutTableCell\*));  
   span_cells_[pos] = cell;  
  

```

#FixPatch

```
diff --git a/third_party/blink/renderer/core/layout/table_layout_algorithm_auto.cc b/third_party/blink/renderer/core/layout/table_layout_algorithm_auto.cc  
index 1e1575cf47..3a43d3220d 100644  
--- a/third_party/blink/renderer/core/layout/table_layout_algorithm_auto.cc  
+++ b/third_party/blink/renderer/core/layout/table_layout_algorithm_auto.cc  
@@ -673,7 +673,7 @@ void TableLayoutAlgorithmAuto::InsertSpanCell(LayoutTableCell\* cell) {  
          span > span_cells_[pos]->ColSpan())  
     pos++;  
   memmove(span_cells_.data() + pos + 1, span_cells_.data() + pos,  
-          (size - pos - 1) \* sizeof(LayoutTableCell\*));  
+          (size - pos - 1) \* sizeof(Member<LayoutTableCell>));  
   span_cells_[pos] = cell;  
 }  
   

```
# **Additional Comments:**

==12644==ERROR: AddressSanitizer: use-after-poison on address 0x7ecd00cee030 at pc 0x7ff668a09ed7 bp 0x0062fd5fb4f0 sp 0x0062fd5fb530  

READ of size 72 at 0x7ecd00cee030 thread T0  

==12644==WARNING: Failed to use and restart external symbolizer!  

==12644==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==12644==\*\*\* Most likely this means that the app is already \*\*\*  

==12644==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==12644==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==12644==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ff668a09ed6 in \_\_asan\_memmove C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_interceptors\_memintrinsics.cpp:30  

#1 0x7ffa5c45f03a in blink::TableLayoutAlgorithmAuto::InsertSpanCell C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\table\_layout\_algorithm\_auto.cc:675  

#2 0x7ffa5c45ccef in blink::TableLayoutAlgorithmAuto::RecalcColumn C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\table\_layout\_algorithm\_auto.cc:154  

#3 0x7ffa5c46058d in blink::TableLayoutAlgorithmAuto::FullRecalc C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\table\_layout\_algorithm\_auto.cc:219  

#4 0x7ffa5c460d0b in blink::TableLayoutAlgorithmAuto::ComputeIntrinsicLogicalWidths C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\table\_layout\_algorithm\_auto.cc:298  

#5 0x7ffa593ca321 in blink::LayoutTable::ComputeIntrinsicLogicalWidths C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_table.cc:1162  

#6 0x7ffa55912c1f in blink::LayoutBox::UpdateCachedIntrinsicLogicalWidthsIfNeeded C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_box.cc:2168  

#7 0x7ffa593b8fe8 in blink::LayoutTable::UpdateLogicalWidth C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_table.cc:353  

#8 0x7ffa593c0ed2 in blink::LayoutTable::UpdateLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_table.cc:735  

#9 0x7ffa55d090b2 in blink::LayoutBlockFlow::PositionAndLayoutOnceIfNeeded C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block\_flow.cc:832  

#10 0x7ffa55d0b39e in blink::LayoutBlockFlow::LayoutBlockChild C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block\_flow.cc:947  

#11 0x7ffa55d05b3d in blink::LayoutBlockFlow::LayoutBlockChildren C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block\_flow.cc:1644  

#12 0x7ffa55cffaa6 in blink::LayoutBlockFlow::LayoutChildren C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block\_flow.cc:617  

#13 0x7ffa55cfe693 in blink::LayoutBlockFlow::UpdateBlockLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block\_flow.cc:478  

#14 0x7ffa55b925b3 in blink::LayoutBlock::UpdateLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block.cc:444  

#15 0x7ffa55d090b2 in blink::LayoutBlockFlow::PositionAndLayoutOnceIfNeeded C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block\_flow.cc:832  

#16 0x7ffa55d0b39e in blink::LayoutBlockFlow::LayoutBlockChild C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block\_flow.cc:947  

#17 0x7ffa55d05b3d in blink::LayoutBlockFlow::LayoutBlockChildren C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block\_flow.cc:1644  

#18 0x7ffa55cffaa6 in blink::LayoutBlockFlow::LayoutChildren C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block\_flow.cc:617  

#19 0x7ffa55cfe693 in blink::LayoutBlockFlow::UpdateBlockLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block\_flow.cc:478  

#20 0x7ffa55b925b3 in blink::LayoutBlock::UpdateLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block.cc:444  

#21 0x7ffa55d090b2 in blink::LayoutBlockFlow::PositionAndLayoutOnceIfNeeded C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block\_flow.cc:832  

#22 0x7ffa55d0b39e in blink::LayoutBlockFlow::LayoutBlockChild C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block\_flow.cc:947  

#23 0x7ffa55d05b3d in blink::LayoutBlockFlow::LayoutBlockChildren C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block\_flow.cc:1644  

#24 0x7ffa55cffaa6 in blink::LayoutBlockFlow::LayoutChildren C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block\_flow.cc:617  

#25 0x7ffa55cfe693 in blink::LayoutBlockFlow::UpdateBlockLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block\_flow.cc:478  

#26 0x7ffa526c957c in blink::LayoutView::UpdateBlockLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_view.cc:336  

#27 0x7ffa55b925b3 in blink::LayoutBlock::UpdateLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_block.cc:444  

#28 0x7ffa526ca00a in blink::LayoutView::UpdateLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_view.cc:377  

#29 0x7ffa5252da7c in blink::LocalFrameView::PerformLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:880  

#30 0x7ffa525310c1 in blink::LocalFrameView::UpdateLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:942  

#31 0x7ffa5255c0fa in blink::LocalFrameView::UpdateStyleAndLayoutInternal C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3262  

#32 0x7ffa5253c366 in blink::LocalFrameView::UpdateStyleAndLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3199  

#33 0x7ffa5255014c in blink::LocalFrameView::UpdateStyleAndLayoutIfNeededRecursive C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3119  

#34 0x7ffa5254b96f in blink::LocalFrameView::RunStyleAndLayoutLifecyclePhases C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2563  

#35 0x7ffa5254985f in blink::LocalFrameView::UpdateLifecyclePhasesInternal C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2386  

#36 0x7ffa525467ca in blink::LocalFrameView::UpdateLifecyclePhases C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2323  

#37 0x7ffa52546034 in blink::LocalFrameView::UpdateAllLifecyclePhases C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2081  

#38 0x7ffa55812143 in blink::PageAnimator::UpdateAllLifecyclePhases C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\page\page\_animator.cc:161  

#39 0x7ffa524f6a94 in blink::WebFrameWidgetImpl::UpdateLifecycle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\web\_frame\_widget\_impl.cc:1320  

#40 0x7ffa559cbe49 in blink::WidgetBase::UpdateVisualState C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\widget\_base.cc:857  

#41 0x7ffa4ffa1766 in cc::LayerTreeHost::RequestMainFrameUpdate C:\b\s\w\ir\cache\builder\src\cc\trees\layer\_tree\_host.cc:376  

#42 0x7ffa53144181 in cc::ProxyMain::BeginMainFrame C:\b\s\w\ir\cache\builder\src\cc\trees\proxy\_main.cc:277  

#43 0x7ffa57668f95 in base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState,std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >),base::WeakPtr[cc::ProxyMain](javascript:void(0);),std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState,std::Cr::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:768  

#44 0x7ffa4d61eaa4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#45 0x7ffa5034e111 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:406  

#46 0x7ffa5034d2ee in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:284  

#47 0x7ffa5032ba1a in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#48 0x7ffa5034fd1a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:551  

#49 0x7ffa4d59272f in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#50 0x7ffa4fe1216d in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:290  

#51 0x7ffa4d14b83e in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:720  

#52 0x7ffa4d14d7d3 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1063  

#53 0x7ffa4d149eab in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407  

#54 0x7ffa4d14a615 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435  

#55 0x7ffa41b814ac in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:182  

#56 0x7ff6689656fe in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:162  

#57 0x7ff668962ae4 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:395  

#58 0x7ff668d6a1df in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#59 0x7ffb2c507033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#60 0x7ffb2e102650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

Address 0x7ecd00cee030 is a wild pointer inside of access range of size 0x000000000048.  

SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_interceptors\_memintrinsics.cpp:30 in \_\_asan\_memmove  

Shadow bytes around the buggy address:  

0x114ce819dbb0: 00 00 00 00 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x114ce819dbc0: f7 f7 f7 f7 00 00 00 00 00 00 00 00 00 00 00 00  

0x114ce819dbd0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00  

0x114ce819dbe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x114ce819dbf0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x114ce819dc00: 00 00 00 00 00 00[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x114ce819dc10: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x114ce819dc20: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x114ce819dc30: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x114ce819dc40: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x114ce819dc50: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

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

==12644==ABORTING

\*\*Chrome version: \*\* 103.0.5060.53 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 11.6 KB)
- [fixpatch.diff](attachments/fixpatch.diff) (text/plain, 713 B)
- [poc.html](attachments/poc.html) (text/plain, 474 B)

## Timeline

### [Deleted User] (2022-07-03)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-07-03)

#NOTE
This was found by my fuzzer running on CF (https://clusterfuzz.com/testcase-detail/5467088881909760), but CF incorrectly classified it as a non-security issue, so I manually submitted a report.

### da...@chromium.org (2022-07-05)

This was changed to a Member<> field in

Commit 7ac2f2d : yukiy@chromium.org @ 2021-09-01 1:38 AM
Layout: Convert TableLayoutAlgorithm to GCed



[Monorail components: Blink>Layout]

### da...@chromium.org (2022-07-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-05)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sz...@chromium.org (2022-07-06)

I'm OOO until next week, assigning to ikilpatrick for layout triage.

### ik...@chromium.org (2022-07-06)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-07-07)

@ping Anyone take a look at this issue?

### da...@chromium.org (2022-07-07)

Why was this changed to unowned?

### ik...@chromium.org (2022-07-07)

I'm OOO - Someone on the GC team should look at this as related to pointer compression.

[Monorail components: -Blink>Layout Blink>GarbageCollection]

### da...@chromium.org (2022-07-07)

[Empty comment from Monorail migration]

### ml...@chromium.org (2022-07-07)

Anton, cany ou have a look before relanding?

CPPGC_POINTER_COMPRESSION was only enabled in M105 for a single Canary [1]. It's currently disabled and was definitely not enabled on M102/M103.

danakj: Can you help us with the labels? I am not sure how you want to track this.

[1] https://chromiumdash.appspot.com/commit/111d20bb7c1909a645353b56ec40fa52805809e0

### da...@chromium.org (2022-07-07)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-07-07)

None for not shipping code (yet)

### bi...@chromium.org (2022-07-08)

Thanks m.cooolie@, that's a great find! This code has been broken even without pointer compression on builds with dchecks (since sizeof(Member<>) is bigger than sizeof(void*) on dcheck builds).  I've prepared a CL, but please let me know if you want to prepare yourself or already have your own:  https://chromium-review.googlesource.com/c/chromium/src/+/3751138

### gi...@appspot.gserviceaccount.com (2022-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2083e894852cfd18bd913a91eea23f59046e6c39

commit 2083e894852cfd18bd913a91eea23f59046e6c39
Author: Anton Bikineev <bikineev@chromium.org>
Date: Sun Jul 10 22:17:03 2022

Fix heap-overflow in blink::TableLayoutAlgorithmAuto::InsertSpanCell

The CL fixes size confusion between Member<> and raw pointers.

The bug was found (and the fix was proposed) by m.cooolie@gmail.com.

Bug: 1341539
Change-Id: I99d524fd65c2d6305693d09ad274c23178271269
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3751138
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Anton Bikineev <bikineev@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1022529}

[modify] https://crrev.com/2083e894852cfd18bd913a91eea23f59046e6c39/third_party/blink/renderer/core/layout/table_layout_algorithm_auto.cc


### jd...@chromium.org (2022-07-12)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-07-14)

@bikineev Thanks for your quick response, the issue can be set as fixed.

### bi...@chromium.org (2022-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-15)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1341539&entry.364066060=External&entry.958145677=Windows&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>GarbageCollection&entry.975983575=bikineev@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bi...@chromium.org (2022-07-15)

Didn't hit stable (or beta/dev), removing postmortem label.

### m....@gmail.com (2022-07-15)

re https://crbug.com/chromium/1341539#c24
Even it does not affect the stable(or beta/dev) version, it is still a security issue, so the Type=BugSecurity Security_Severity-High tag is required.


### bi...@chromium.org (2022-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-18)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1341539&entry.364066060=External&entry.958145677=Windows&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>GarbageCollection&entry.975983575=bikineev@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-21)

Congratulations! The VRP Panel has decided to award you $7500 for this report + $1000 fuzzer bonus + $500 patch bonus for a total of $9,000. Thank you for your efforts and excellent work! 

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### ml...@chromium.org (2022-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-10-20)

This issue was migrated from crbug.com/chromium/1341539?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1341524]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060150)*

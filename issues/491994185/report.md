# Iterator Invalidation in LayoutSubtreeRootList During Container Query Interleaved Style Recalc Leads to Use-After-Free

| Field | Value |
|-------|-------|
| **Issue ID** | [491994185](https://issues.chromium.org/issues/491994185) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2026-03-12 |
| **Bounty** | $11,000.00 |

## Description

# Iterator Invalidation in LayoutSubtreeRootList During Container Query Interleaved Style Recalc Leads to Use-After-Free

## Summary

A use-after-free vulnerability exists in the Blink layout engine where `LocalFrameView::PerformLayout()` iterates over a `HeapVector` of subtree layout roots using a live range-for loop. During this iteration, an interleaved style recalculation triggered by a CSS container query can destroy a queued `LayoutObject`, causing `DepthOrderedLayoutObjectList::Remove()` to call `ordered_objects_.clear()`. This immediately frees the backing store of the vector being iterated, leaving the loop's iterators dangling. The subsequent iteration dereferences poisoned memory. The bug is platform-independent and is triggered entirely from JavaScript via standard DOM and CSSOM APIs. No special hardware or GPU is required.

## Bisect

Introducing Commit: CL 2627411 (2021-01-15, <https://chromium-review.googlesource.com/c/chromium/src/+/2627411>)

This commit wired `UpdateStyleAndLayoutTreeForSizeContainer()` into `BlockNode::Layout()`, creating the interleaved style recalc path that runs during layout. Once this path exists, a container query result change during `PerformLayout()` can trigger `RebuildLayoutTree()`, destroy a queued `LayoutObject`, and call `DepthOrderedLayoutObjectList::Remove()` while the range-for loop is iterating the internal vector.

## Root Cause

`LocalFrameView::PerformLayout()` processes pending subtree layout roots by iterating directly over the internal `HeapVector` returned by `DepthOrderedLayoutObjectList::Ordered()`:

```
// third_party/blink/renderer/core/frame/local_frame_view.cc:756-780
for (auto& root : layout_subtree_root_list_.Ordered()) {
    bool should_rebuild_fragments = false;
    LayoutObject& root_layout_object = *root;
    LayoutBox* container_box = root->ContainingNGBox();
    // ...
    if (!LayoutFromRootObject(*root))
      continue;
    // ...
}
layout_subtree_root_list_.Clear();

```

The `Ordered()` method returns a const reference to `ordered_objects_`, an internal cached `HeapVector<LayoutObjectWithDepth>`. The range-for loop captures `begin()` and `end()` iterators that point directly into this vector's backing store.

During `LayoutFromRootObject()`, the layout engine may enter a container query interleaved style recalc via `BlockNode::Layout()` calling `StyleEngine::UpdateStyleAndLayoutTreeForSizeContainer()`. If the container query result changes, this triggers `RecalcStyleForSizeContainer()` followed by `RebuildLayoutTree()`, which can change an element's computed `display` to `none` and destroy its `LayoutObject`. The destruction chain is:

```
// third_party/blink/renderer/core/layout/layout_object.cc:3965-4011
void LayoutObject::WillBeDestroyed() {
  // ...
  Remove();
  // ...
  if (LocalFrameView* view = GetFrameView()) {
    view->ClearLayoutSubtreeRoot(*this);   // calls into Remove() below
    // ...
  }
}

```

`ClearLayoutSubtreeRoot()` delegates to `DepthOrderedLayoutObjectList::Remove()`, which erases the object from the hash set and unconditionally clears the ordered vector:

```
// third_party/blink/renderer/core/layout/depth_ordered_layout_object_list.cc:70-77
void DepthOrderedLayoutObjectList::Remove(LayoutObject& object) {
  auto it = data_->objects().find(&object);
  if (it == data_->objects().end())
    return;
  DCHECK(ListModificationAllowedFor(object));
  data_->objects().erase(it);
  data_->ordered_objects().clear();   // frees the HeapVector backing store
}

```

The `clear()` call chains through `ShrinkCapacity(0)`, `HeapAllocator::FreeVectorBacking()`, and ultimately `cppgc::subtle::FreeUnreferencedObject()`, which zeroes the memory and calls `ASAN_POISON_MEMORY_REGION()`. This is not a deferred garbage collection; the backing store is immediately freed and poisoned. The range-for loop's captured iterators now point into freed memory, and the next iteration performs a read from the poisoned region.

The only guard is `ListModificationAllowedFor()`, which is a DCHECK that evaluates to a no-op in Release builds. In Release, the interleaved style recalc sets `InInterleavedStyleRecalc()` to true, so the DCHECK would pass even in Debug, making this reachable on all build configurations.

There is a telling asymmetry in the code. `UpdateLayout()`, which calls `PerformLayout()`, copies the ordered list into a local variable for tracing purposes just before entering layout:

```
// third_party/blink/renderer/core/frame/local_frame_view.cc:830-839
HeapVector<LayoutObjectWithDepth> layout_roots;
// ...
layout_roots = layout_subtree_root_list_.Ordered();  // copy

```

Yet `PerformLayout()` itself iterates the live internal reference, not a snapshot. Had it iterated a copy, the `clear()` inside `Remove()` would invalidate only the internal cache, not the iteration.

## Reproduce

This issue was tested on Chromium commit `f51a685e768b6` on Linux (x86\_64). No source modifications are required; the bug reproduces on a stock ASAN build. All platforms are affected.

To prepare the build, check out the commit and configure an ASAN release build. A minimal `args.gn` for `out/asan-release` is shown below.

```
is_asan = true
is_debug = false
is_component_build = true
symbol_level = 1

```

Compile with `autoninja -C out/asan-release chrome`. Launch Chrome with the attached PoC. The renderer process will crash within a few seconds.

```
ASAN_OPTIONS=detect_odr_violation=0 \
  ~/chromium/src/out/asan-release/chrome \
  --no-sandbox --disable-gpu \
  --user-data-dir=/tmp/poc-$(date +%s) \
  poc.html

```
### ASAN output

```
==2242985==ERROR: AddressSanitizer: use-after-poison on address 0x7aec00409898 at pc 0x7f035e77569c bp 0x7fff37f44d30 sp 0x7fff37f44d28
READ of size 4 at 0x7aec00409898 thread T0 (chrome)
    #0 0x7f035e77569b in blink::LocalFrameView::PerformLayout() v8/include/cppgc/internal/member-storage.h:92:58
    #1 0x7f035e776c2b in blink::LocalFrameView::UpdateLayout() third_party/blink/renderer/core/frame/local_frame_view.cc:848:3
    #2 0x7f035e796036 in blink::LocalFrameView::UpdateStyleAndLayoutInternal() third_party/blink/renderer/core/frame/local_frame_view.cc:3427:7
    #3 0x7f035e780463 in blink::LocalFrameView::UpdateStyleAndLayout() third_party/blink/renderer/core/frame/local_frame_view.cc:3353:18
    #4 0x7f036100b411 in blink::Document::UpdateStyleAndLayout(blink::DocumentUpdateReason) third_party/blink/renderer/core/dom/document.cc:3091:17
    #5 0x7f036100e1b3 in blink::Document::UpdateStyleAndLayoutForNode(blink::Node const*, blink::DocumentUpdateReason) third_party/blink/renderer/core/dom/document.cc:2914:3
    #6 0x7f035ed97b7b in blink::HTMLElement::offsetWidthForBinding() third_party/blink/renderer/core/html/html_element.cc:3555:17
    #7 0x7f03466d96c7 in blink::(anonymous namespace)::v8_html_element::OffsetWidthAttributeGetCallback(v8::FunctionCallbackInfo<v8::Value> const&) gen/third_party/blink/renderer/bindings/modules/v8/v8_html_element.cc:684:39
    #8 0x7b03140106a3  (<unknown module>)
    #9 0x7b0314021274  (<unknown module>)
    #10 0x7b03141bcf4c  (<unknown module>)
    #11 0x7b031400e83b  (<unknown module>)
    #12 0x7b031400b5db  (<unknown module>)
    #13 0x7b031400b32a  (<unknown module>)
    #14 0x7f034e72246e in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/simulator.h:216:12
    #15 0x7f034e71ffde in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::Object>, v8::internal::DirectHandle<v8::internal::Object>, v8::base::Vector<v8::internal::DirectHandle<v8::internal::Object> const>) v8/src/execution/execution.cc:532:10
    #16 0x7f034e2f807a in v8::Function::Call(v8::Isolate*, v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) v8/src/api/api.cc:5573:27
    #17 0x7f035d0f6350 in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:855:48
    #18 0x7f035cf4977b in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionWithTaskAttributionBase, (blink::bindings::CallbackInvokeHelperMode)0, (blink::bindings::CallbackReturnTypeIsPromise)0>::Call(int, v8::Local<v8::Value>*) third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:126:12
    #19 0x7f0361758b22 in blink::V8FrameRequestCallback::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, double) gen/third_party/blink/renderer/bindings/core/v8/v8_frame_request_callback.cc:62:13
    #20 0x7f0361759cc1 in blink::V8FrameRequestCallback::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, double) gen/third_party/blink/renderer/bindings/core/v8/v8_frame_request_callback.cc:111:15
    #21 0x7f035deae1a8 in blink::FrameRequestCallbackCollection::ExecuteFrameCallbacks(double, double) third_party/blink/renderer/core/dom/frame_request_callback_collection.cc
    #22 0x7f0360256e39 in blink::PageAnimator::ServiceScriptedAnimations(base::TimeTicks, ...) third_party/blink/renderer/core/page/page_animator.cc:292:28
    #23 0x7f0360253c79 in blink::PageAnimator::ServiceScriptedAnimations(base::TimeTicks) third_party/blink/renderer/core/page/page_animator.cc:110:3
    #24 0x7f0360246c11 in blink::Page::Animate(base::TimeTicks) third_party/blink/renderer/core/page/page.cc:1542:14
    #25 0x7f035e9094c6 in blink::WebFrameWidgetImpl::BeginMainFrame(viz::BeginFrameArgs const&) third_party/blink/renderer/core/frame/web_frame_widget_impl.cc:2665:14
    #26 0x7f0355e85904 in blink::WidgetBase::BeginMainFrame(viz::BeginFrameArgs const&) third_party/blink/renderer/platform/widget/widget_base.cc:1071:12
    #27 0x7f039f477982 in cc::ProxyMain::BeginMainFrame(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>) cc/trees/proxy_main.cc:318:21
    #28 0x7f039f46eba2 in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #29 0x7f03b1760c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #30 0x7f03b17e216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #31 0x7f03b17e1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #32 0x7f03b16033f1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #33 0x7f03b17e37e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #34 0x7f03b16cb002 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #35 0x7f03a740de85 in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:364:16
    #36 0x7f03a7860bb7 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #37 0x7f03a7861d7e in content::RunOtherNamedProcessTypeMain(...) content/app/content_main_runner_impl.cc:771:12
    #38 0x7f03a78642da in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1150:10
    #39 0x7f03a785ea63 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #40 0x7f03a785edea in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #41 0x55f0556d1c15 in ChromeMain chrome/app/chrome_main.cc:191:12
    #42 0x7f0340229d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

Address 0x7aec00409898 is a wild pointer inside of access range of size 0x000000000004.
SUMMARY: AddressSanitizer: use-after-poison v8/include/cppgc/internal/member-storage.h:92:58 in blink::LocalFrameView::PerformLayout()
Shadow bytes around the buggy address:
  0x7aec00409780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7aec00409800: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7aec00409880: 00 00 f7[f7]00 00 00 00 00 00 00 00 00 00 00 00
  0x7aec00409900: 00 00 f7 f7 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte f7 = Poisoned by user

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 9.3 KB)
- [poc.html](attachments/poc.html) (text/html, 1.8 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6327819944624128.

### th...@chromium.org (2026-03-13)

[security shepherd] CF can repro but it's really taking its time... I'll triage the rest manually since it has confirmed a repro. Setting FoundIn to extended stable based on bisect.

andruud@: Could you PTAL?

### 24...@project.gserviceaccount.com (2026-03-13)

Detailed Report: https://clusterfuzz.com/testcase?key=6327819944624128

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Use-after-poison READ 4
Crash Address: 0x7ef4004094f0
Crash State:
  blink::LocalFrameView::PerformLayout
  blink::LocalFrameView::UpdateLayout
  blink::LocalFrameView::UpdateStyleAndLayoutInternal
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1598715

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6327819944624128

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ch...@google.com (2026-03-14)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-14)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-03-18)

Project: chromium/src  

Branch:  main  

Author:  Anders Hartvoll Ruud [andruud@chromium.org](mailto:andruud@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7669842>

Iterate on copy of layout subtree roots during LFV::PerformLayout()

---


Expand for full commit details
```
     
    During iteration of LocalFrameView::layout_subtree_root_list_ 
    in PerformLayout(), we can do interleaved style and layout tree 
    building due to e.g. container queries. Such layout tree rebuilds 
    can destroy the LayoutObjects being subtree roots, 
    and call LocalFrameView::ClearLayoutSubtreeRoot() in the process, 
    modifying layout_subtree_root_list_ during the iteration. 
     
    To fix this, iterate on a copy of the layout subtree roots instead. 
    Note that even though we do clear layout_subtree_root_list_ immediately 
    after iteration, we can not just std::move the list to a local, 
    since we need to discover (and skip) the roots that were removed 
    during previous iterations. 
     
    Fixed: 491994185 
    Change-Id: I729e3df6e938533467ff4d45e66c666fe27a83c0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7669842 
    Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org> 
    Reviewed-by: Morten Stenshorne <mstensho@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1600948}

```

---

Files:

- M `third_party/blink/renderer/core/frame/local_frame_view.cc`
- M `third_party/blink/renderer/core/layout/depth_ordered_layout_object_list.cc`
- M `third_party/blink/renderer/core/layout/depth_ordered_layout_object_list.h`
- A `third_party/blink/web_tests/external/wpt/css/css-conditional/container-queries/crashtests/chrome-bug-491994185-crash.html`

---

Hash: [c215f8e6f0492ef6840b43ab2657be2eafbeda1f](https://chromiumdash.appspot.com/commit/c215f8e6f0492ef6840b43ab2657be2eafbeda1f)  

Date: Wed Mar 18 01:43:46 2026


---

### ch...@google.com (2026-03-18)

Security Merge Request Consideration: Requesting merge to stable (M146) because latest trunk commit (1600948) appears to be after stable branch point (1582197).
Security Merge Request Consideration: Requesting merge to beta (M147) because latest trunk commit (1600948) appears to be after beta branch point (1596535).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### 24...@project.gserviceaccount.com (2026-03-18)

ClusterFuzz testcase 6327819944624128 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1600947:1600948

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-03-19)

Merge review required: M147 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-19)

Merge review required: M146 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### dr...@chromium.org (2026-03-20)

Okay this now has it's bake time in Canary and there's still no crashes. Approved to merge to M146 and M147.

### dr...@chromium.org (2026-03-24)

andruud@ - friendly ping to merge this!

### ch...@google.com (2026-03-25)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dr...@chromium.org (2026-03-30)

Ah, looks like andruud@ is OOO. mstensho@ - you did the review of the fix CL, can you handle the merges?

### ms...@chromium.org (2026-03-30)

I'm OOO in the same period.

### ch...@google.com (2026-03-31)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sr...@chromium.org (2026-03-31)

We are cutting M147 RC today around 12pm PST, if your merge is critical to be incliuded in the RC build and is not able to make that cut off, please reach out to me , ( i can give some buffer for critical fixes that needs to included in RC) 

### wf...@chromium.org (2026-04-01)

renderer memory corruption is sev high.

### dx...@google.com (2026-04-07)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Anders Hartvoll Ruud [andruud@chromium.org](mailto:andruud@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7735721>

Iterate on copy of layout subtree roots during LFV::PerformLayout()

---


Expand for full commit details
```
     
    During iteration of LocalFrameView::layout_subtree_root_list_ 
    in PerformLayout(), we can do interleaved style and layout tree 
    building due to e.g. container queries. Such layout tree rebuilds 
    can destroy the LayoutObjects being subtree roots, 
    and call LocalFrameView::ClearLayoutSubtreeRoot() in the process, 
    modifying layout_subtree_root_list_ during the iteration. 
     
    To fix this, iterate on a copy of the layout subtree roots instead. 
    Note that even though we do clear layout_subtree_root_list_ immediately 
    after iteration, we can not just std::move the list to a local, 
    since we need to discover (and skip) the roots that were removed 
    during previous iterations. 
     
    (cherry picked from commit c215f8e6f0492ef6840b43ab2657be2eafbeda1f) 
     
    Fixed: 491994185 
    Change-Id: I729e3df6e938533467ff4d45e66c666fe27a83c0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7669842 
    Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org> 
    Reviewed-by: Morten Stenshorne <mstensho@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1600948} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7735721 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#2417} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `third_party/blink/renderer/core/frame/local_frame_view.cc`
- M `third_party/blink/renderer/core/layout/depth_ordered_layout_object_list.cc`
- M `third_party/blink/renderer/core/layout/depth_ordered_layout_object_list.h`
- A `third_party/blink/web_tests/external/wpt/css/css-conditional/container-queries/crashtests/chrome-bug-491994185-crash.html`

---

Hash: [c34df82e64962b44e0ee604c099422ef9a1732fa](https://chromiumdash.appspot.com/commit/c34df82e64962b44e0ee604c099422ef9a1732fa)  

Date: Tue Apr 7 20:44:49 2026


---

### pe...@google.com (2026-04-07)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-04-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-27)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7790541
2. Low - There was no conflict
3. 147
4. Yes, the bug was an old bug that was introduced in 2021.

### sp...@google.com (2026-05-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
High-quality report of demonstrated memory corruption with bisect. RCE / Memory Corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/491994185)*

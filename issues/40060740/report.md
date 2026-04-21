# heap-use-after-free html_element.cc:1850 in blink::HTMLElement::offsetTopForBinding

| Field | Value |
|-------|-------|
| **Issue ID** | [40060740](https://issues.chromium.org/issues/40060740) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>DOM |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | db...@chromium.org |
| **Created** | 2022-08-31 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

#Reproduce

1. chrome --js-flags="-expose-gc --allow-natives-syntax" --no-sandbox --enable-blink-test-features --user-data-dir=test --enable-logging=stderr poc.html
2. click any where

poc.htmlStable reproducible but not minimal sample  

poc1.html is a minimal sample but not stable to reproduce

**Problem Description:**  

#Type of crash  

render tab

#Analysis  

Coming soon

# **Additional Comments:** #asan

==16288==ERROR: AddressSanitizer: heap-use-after-free on address 0x11463f9f6368 at pc 0x7ff979b1dc44 bp 0x0020d69fdc00 sp 0x0020d69fdc48  

READ of size 8 at 0x11463f9f6368 thread T0  

==16288==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ff979b1dc43 in blink::HTMLElement::offsetTopForBinding C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\html\_element.cc:1850  

#1 0x7ff98580cd9e in blink::`anonymous namespace'::v8\_html\_element::OffsetTopAttributeGetCallback C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\renderer\bindings\modules\v8\v8\_html\_element.cc:625  

#2 0x7ff91fe4d2dd (<unknown module>)

0x11463f9f6368 is located 8 bytes inside of 112-byte region [0x11463f9f6360,0x11463f9f63d0)  

freed by thread T0 here:  

#0 0x7ff6bb72e26c in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ff9797ed49a in blink::Element::RecalcOwnStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:4521  

#2 0x7ff9797e7d7c in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:3959  

#3 0x7ff979b99144 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\container\_node.cc:1386  

#4 0x7ff9797e8bb2 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:4062  

#5 0x7ff979aad44a in blink::StyleEngine::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2848  

#6 0x7ff979aae9a8 in blink::StyleEngine::UpdateStyleAndLayoutTreeForContainer C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2808  

#7 0x7ff97d55325f in blink::NGBlockNode::Layout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:473  

#8 0x7ff98147d689 in blink::NGBlockLayoutAlgorithm::LayoutNewFormattingContext C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1586  

#9 0x7ff981479bd7 in blink::NGBlockLayoutAlgorithm::HandleNewFormattingContext C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1369  

#10 0x7ff98146b0a1 in blink::NGBlockLayoutAlgorithm::Layout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:719  

#11 0x7ff98146908f in blink::NGBlockLayoutAlgorithm::Layout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:464  

#12 0x7ff97d57927b in blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm,`lambda at ../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:216:28'> C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:124  

#13 0x7ff97d553b52 in blink::NGBlockNode::Layout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:535  

#14 0x7ff98147d689 in blink::NGBlockLayoutAlgorithm::LayoutNewFormattingContext C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1586  

#15 0x7ff981479bd7 in blink::NGBlockLayoutAlgorithm::HandleNewFormattingContext C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1369  

#16 0x7ff98146b0a1 in blink::NGBlockLayoutAlgorithm::Layout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:719  

#17 0x7ff98146908f in blink::NGBlockLayoutAlgorithm::Layout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:464  

#18 0x7ff97d57927b in blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm,`lambda at ../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:216:28'> C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:124  

#19 0x7ff97d553b52 in blink::NGBlockNode::Layout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:535  

#20 0x7ff98147d689 in blink::NGBlockLayoutAlgorithm::LayoutNewFormattingContext C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1586  

#21 0x7ff981479bd7 in blink::NGBlockLayoutAlgorithm::HandleNewFormattingContext C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1369  

#22 0x7ff98146b0a1 in blink::NGBlockLayoutAlgorithm::Layout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:719  

#23 0x7ff98146908f in blink::NGBlockLayoutAlgorithm::Layout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:464  

#24 0x7ff97d57927b in blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm,`lambda at ../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:216:28'> C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:124  

#25 0x7ff97d553b52 in blink::NGBlockNode::Layout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:535  

#26 0x7ff981489bcd in blink::`anonymous namespace'::LayoutInflow C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:129  

#27 0x7ff9814889ec in blink::NGBlockLayoutAlgorithm::HandleInflow C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1737

previously allocated by thread T0 here:  

#0 0x7ff6bb72e36c in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff9749545ed in partition\_alloc::PartitionRoot<1>::Alloc C:\b\s\w\ir\cache\builder\src\base\allocator\partition\_allocator\partition\_root.h:1980  

#2 0x7ff97c8c59e6 in blink::ComputedStyle::Clone C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\style\computed\_style.cc:207  

#3 0x7ff97cd1f82b in blink::StyleResolver::ApplyInheritance C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_resolver.cc:989  

#4 0x7ff97cd204f6 in blink::StyleResolver::InitStyleAndApplyInheritance C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_resolver.cc:1013  

#5 0x7ff97cd22efe in blink::StyleResolver::ApplyBaseStyleNoCache C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_resolver.cc:1211  

#6 0x7ff97cd1d381 in blink::StyleResolver::ApplyBaseStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_resolver.cc:1418  

#7 0x7ff97cd1ba7e in blink::StyleResolver::ResolveStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_resolver.cc:907  

#8 0x7ff9797e63cb in blink::Element::OriginalStyleForLayoutObject C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:3842  

#9 0x7ff9797e5828 in blink::Element::StyleForLayoutObject C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:3814  

#10 0x7ff9797eabaa in blink::Element::RecalcOwnStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:4274  

#11 0x7ff9797e7d7c in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:3959  

#12 0x7ff979b99144 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\container\_node.cc:1386  

#13 0x7ff9797e8bb2 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:4062  

#14 0x7ff979aad44a in blink::StyleEngine::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2848  

#15 0x7ff979aae9a8 in blink::StyleEngine::UpdateStyleAndLayoutTreeForContainer C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2808  

#16 0x7ff97d55325f in blink::NGBlockNode::Layout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:473  

#17 0x7ff98147d689 in blink::NGBlockLayoutAlgorithm::LayoutNewFormattingContext C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1586  

#18 0x7ff981479bd7 in blink::NGBlockLayoutAlgorithm::HandleNewFormattingContext C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1369  

#19 0x7ff98146b0a1 in blink::NGBlockLayoutAlgorithm::Layout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:719  

#20 0x7ff98146908f in blink::NGBlockLayoutAlgorithm::Layout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:464  

#21 0x7ff97d57927b in blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm,`lambda at ../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:216:28'> C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:124  

#22 0x7ff97d553b52 in blink::NGBlockNode::Layout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:535  

#23 0x7ff98147d689 in blink::NGBlockLayoutAlgorithm::LayoutNewFormattingContext C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1586  

#24 0x7ff981479bd7 in blink::NGBlockLayoutAlgorithm::HandleNewFormattingContext C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:1369  

#25 0x7ff98146b0a1 in blink::NGBlockLayoutAlgorithm::Layout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:719  

#26 0x7ff98146908f in blink::NGBlockLayoutAlgorithm::Layout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_layout\_algorithm.cc:464  

#27 0x7ff97d57927b in blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm,`lambda at ../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:216:28'> C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\ng\ng\_block\_node.cc:124

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\html\_element.cc:1850 in blink::HTMLElement::offsetTopForBinding  

Shadow bytes around the buggy address:  

0x0359078bec10: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00  

0x0359078bec20: 00 fa fa fa fa fa fa fa fa fa fd fd fd fd fd fd  

0x0359078bec30: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  

0x0359078bec40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa  

0x0359078bec50: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd  

=>0x0359078bec60: fd fd fd fd fa fa fa fa fa fa fa fa fd[fd]fd fd  

0x0359078bec70: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x0359078bec80: fa fa 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0359078bec90: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0359078beca0: 00 00 00 00 00 00 fa fa fa fa fa fa fa fa 00 00  

0x0359078becb0: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa  

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

==16288==ABORTING

\*\*Chrome version: \*\* asan-win32-release\_x64-1040122 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 11.9 KB)
- [h1.js](attachments/h1.js) (text/plain, 8.2 KB)
- [poc.html](attachments/poc.html) (text/plain, 81.0 KB)
- [poc2.html](attachments/poc2.html) (text/plain, 2.4 KB)
- [testharness.js](attachments/testharness.js) (text/plain, 155.7 KB)
- deleted (application/octet-stream, 0 B)
- [poc2.html](attachments/poc2.html) (text/plain, 2.4 KB)
- deleted (application/octet-stream, 0 B)
- [poc.html](attachments/poc.html) (text/plain, 81.0 KB)

## Timeline

### [Deleted User] (2022-08-31)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-08-31)

The POC provided earlier is missing some dependencies, please use the samples provided this time for testing.

### bo...@chromium.org (2022-08-31)

I am unable to reproduce a crash (ASAN or otherwise) using either poc_fix/poc.html or poc_fix/poc2.html on either Windows or Linux on 105 (Stable) and 107 (Canary). 

I regard this as unactionable based on the information currently available, but I am looping in the owners of the Blink DOM features involved for visibility of any future updates. 

### bo...@chromium.org (2022-08-31)

[Empty comment from Monorail migration]

### db...@chromium.org (2022-08-31)

Given that the addresses look like 64-bit, I think it's saying that the bad access is a dereference of ComputedStyleBase::rare_inherited_usage_less_than_64_percent_data_.

I wish I could see a more complete stack for the "freed by thread T0 here:" part of the ASAN report above.  I suspect it may be *inside* of offsetTopForBinding, which could explain the bug.

I think offsetTopForBinding seems somewhat suspicious.  It calls unclosedOffsetParent(), which calls GetDocument().UpdateStyleAndLayoutForNode(), which could, I think, change the layout_object pointer that offsetTopForBinding has been holding on to since before calling unclosedOffsetParent.

The report is consistent with AdjustLayoutUnit() being inlined, and the dereference being part of its call to style.EffectiveZoom().

If this is the case, it looks like it regressed in https://crrev.com/c/3541546 which shipped in M101 (by being backported to M101).

[Monorail components: Blink>DOM]

### db...@chromium.org (2022-08-31)

(I can try to patch this tomorrow, but need to head out for the day right now.  Others could feel free to take as well.)

### ja...@chromium.org (2022-08-31)

poc2.html has a details element so it could be DisplayLocking related, but it's still quite large of a file and there is non DisplayLocking stuff in the stack trace so I'm definitely not sure.
Reporter, if you can make the repro html file even smaller that would be very helpful.

### db...@chromium.org (2022-09-01)

Oh -- one further note -- I think there's a clear *correctness* bug as a result of the above changes, but I think whether there's a use-after-free depends on compiler optimizations since it's depending on undefined behavior.  In particular, the code is:

  if (const auto* layout_object = GetLayoutBoxModelObject()) {
    return AdjustForAbsoluteZoom::AdjustLayoutUnit(
               layout_object->OffsetTop(unclosedOffsetParent()),
               layout_object->StyleRef())
        .Round();
  }

Since layout_object is under oilpan, layout_object itself should be fine across the whole thing.  However, it's possible for the result of layout_object->StyleRef() to change across the call to unclosedOffsetParent(), and I believe the relative order of the unclosedOffsetParent() call and the layout_object->StyleRef() call is undefined.  So if my theory is correct, this may only reproduce in optimized builds, and then only some of them, depending on the optimizer and maybe its inputs.

### db...@chromium.org (2022-09-01)

Oh, never mind about the correctness bug being clearer than the UAF -- both depend on the undefined behavior.

(On the other hand, I think it should be easy to write a test that fails in the bad case, by moving the layout_object->StyleRef() call into its own statement, thus creating a sequence point.  So I should be able to write tests that test the fix even if I can't observe it with the optimizer in my compiler setup.)

### m....@gmail.com (2022-09-01)

re https://crbug.com/chromium/1358597#c03, I'm very sorry, the reproduction steps I gave are not accurate, please use http server to load the webpage
I modified the poc2.html sample, and now it can be reproduced stably.

#Reproduce
1. python -m http.server 1337
2. chrome --js-flags="-expose-gc --allow-natives-syntax" --no-sandbox --enable-blink-test-features --user-data-dir=test --enable-logging=stderr http://localhost:1337/poc2.html
3. click any where


### ma...@chromium.org (2022-09-01)

dbaron, mind if I move this to you, since it looks like you’re  most of the way to fixing it?

### bo...@chromium.org (2022-09-01)

@dbaron, thanks for looking in to this. I'm glad to see you have an idea of where things could be going wrong. 

FYI @m.coolie, I am still unable to repro using the updated POC served from an HTTP server on Chrome 105/stable on either Windows or Linux. 

### m....@gmail.com (2022-09-01)

re https://crbug.com/chromium/1358597#c12 upload poc and reproduce video

### gi...@appspot.gserviceaccount.com (2022-09-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f3795059fd59890f263a41f30c5c282741d0a28f

commit f3795059fd59890f263a41f30c5c282741d0a28f
Author: L. David Baron <dbaron@chromium.org>
Date: Fri Sep 02 15:59:20 2022

Avoid updating layout/style at undefined time.

This reverts a small refactoring in https://crrev.com/c/3541546 so that
the ordering of unclosedOffsetParent() and the other code is clearly
defined.

This is important since unclosedOffsetParent() can update style and
layout.  But since EnsurePaintLocationDataValidForNode also updates
style and layout, this is likely only relevant in cases where a single
style/layout update doesn't stabilize.  Such cases should be rare, but
it seems like they may be possible (though I haven't yet figured out how
to construct a testcase showing that they are).  (I think we currently
generally handle features that need iterations to stabilize in
LocalFrameView::UpdateLifecyclePhasesInternal rather than in
style/layout update.)

Bug: 1358597
Change-Id: Iaf85000a373b76c7c52f5bda8296858b2850b69b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3869251
Auto-Submit: David Baron <dbaron@chromium.org>
Reviewed-by: Vladimir Levin <vmpstr@chromium.org>
Commit-Queue: Vladimir Levin <vmpstr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1042593}

[modify] https://crrev.com/f3795059fd59890f263a41f30c5c282741d0a28f/third_party/blink/renderer/core/html/html_element.cc


### db...@chromium.org (2022-09-02)

@m.cooolie, I'm curious if you're able to confirm whether the above change fixes the problem that you're seeing.  I think it should be straightforward to apply the patch to M105 if that's where you're able to reproduce the bug.  (I'm guessing you're doing your own ASAN build?)

### m....@gmail.com (2022-09-02)

I will test after the asan precompiled version is generated.

### m....@gmail.com (2022-09-02)

No longer reproduce on asan-win32-release_x64-1042605, so I think the patch works fine.

### ja...@chromium.org (2022-09-02)

[Empty comment from Monorail migration]

### db...@chromium.org (2022-09-02)

[Empty comment from Monorail migration]

### bo...@chromium.org (2022-09-02)

Thanks for the fix and verification. I'm setting security flags so sheriff bot can ensure the fix is queued for merge accordingly. 

I was never able to repro even with the updated POC in c#13. However, I'm going to assume the issue impacts M102 since the affected functions hadn't been changed since March.

### db...@chromium.org (2022-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

Merge rejected: M106 is already shipping to beta and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-07)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-09-19)

Hello, dbaron@ thank you for fixing this issue. In the future, please refrain from manually updated security fixes with merge labels and simply just updated the bug as fixed as soon as the resolving CLs are landed. This issue did not make it to a merge review queue due to the bot being confused. At the time this was fixed, this fix would have been a candidate to backmerge to 105/stable and 104/extended. We aim to keep the patch gap (especially for high severity issues) as small as possible to reduce the potential for n-day exploitation.

Please go ahead and merge to branch 5249 ASAP so this fix can be included in tomorrow's 106 stable cut for stable channel release next week. Thank you. 

### db...@chromium.org (2022-09-19)

Cherry-pick at https://chromium-review.googlesource.com/c/chromium/src/+/3904668 .

### gi...@appspot.gserviceaccount.com (2022-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cf3dfd91bbd72746aa3500b1a68c177ebf4ffece

commit cf3dfd91bbd72746aa3500b1a68c177ebf4ffece
Author: L. David Baron <dbaron@chromium.org>
Date: Tue Sep 20 00:07:12 2022

Avoid updating layout/style at undefined time.

This reverts a small refactoring in https://crrev.com/c/3541546 so that
the ordering of unclosedOffsetParent() and the other code is clearly
defined.

This is important since unclosedOffsetParent() can update style and
layout.  But since EnsurePaintLocationDataValidForNode also updates
style and layout, this is likely only relevant in cases where a single
style/layout update doesn't stabilize.  Such cases should be rare, but
it seems like they may be possible (though I haven't yet figured out how
to construct a testcase showing that they are).  (I think we currently
generally handle features that need iterations to stabilize in
LocalFrameView::UpdateLifecyclePhasesInternal rather than in
style/layout update.)

(cherry picked from commit f3795059fd59890f263a41f30c5c282741d0a28f)

Bug: 1358597
Change-Id: Iaf85000a373b76c7c52f5bda8296858b2850b69b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3869251
Auto-Submit: David Baron <dbaron@chromium.org>
Reviewed-by: Vladimir Levin <vmpstr@chromium.org>
Commit-Queue: Vladimir Levin <vmpstr@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1042593}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3904668
Cr-Commit-Position: refs/branch-heads/5249@{#504}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/cf3dfd91bbd72746aa3500b1a68c177ebf4ffece/third_party/blink/renderer/core/html/html_element.cc


### am...@google.com (2022-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-22)

Congratulations on another one x3! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts in reporting this issue to us -- nice work! 

### am...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1358597?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060740)*

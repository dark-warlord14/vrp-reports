# AddressSanitizer: heap-use-after-free html_element.cc:1802 in blink::HTMLElement::offsetTopForBindin

| Field | Value |
|-------|-------|
| **Issue ID** | [40060030](https://issues.chromium.org/issues/40060030) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2022-06-21 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**  

#TestOn  

asan-win32-release\_x64-1016102

#Reproduce

1. chrome --no-sandbox --user-data-dir=test poc.html
2. Click any where

**Problem Description:**  

Type of crash  

render tab

#Analysis  

Coming soon

# **Additional Comments:** #asan

==7604==ERROR: AddressSanitizer: heap-use-after-free on address 0x11f200dfacf8 at pc 0x7ffd92d3ccb3 bp 0x000fec9fda00 sp 0x000fec9fda48  

READ of size 8 at 0x11f200dfacf8 thread T0  

==7604==WARNING: Failed to use and restart external symbolizer!  

==7604==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==7604==\*\*\* Most likely this means that the app is already \*\*\*  

==7604==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==7604==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==7604==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ffd92d3ccb2 in blink::HTMLElement::offsetTopForBinding C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\html\_element.cc:1802  

#1 0x7ffd9b2c4e96 in blink::`anonymous namespace'::v8_html_element::OffsetTopAttributeGetCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_html_element.cc:623 #2 0x7ffd85b656b6 in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:147 #3 0x7ffd85b62b01 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:114  

#4 0x7ffd85b6079a in v8::internal::Builtins::InvokeApiFunction C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:228  

#5 0x7ffd86b63876 in v8::internal::Object::GetPropertyWithAccessor C:\b\s\w\ir\cache\builder\src\v8\src\objects\objects.cc:1461  

#6 0x7ffd86b60c07 in v8::internal::Object::GetProperty C:\b\s\w\ir\cache\builder\src\v8\src\objects\objects.cc:1180  

#7 0x7ffd8647ceb8 in v8::internal::LoadIC::Load C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:512  

#8 0x7ffd8648f611 in v8::internal::KeyedLoadIC::Load C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:1574  

#9 0x7ffd864ae327 in v8::internal::Runtime\_KeyedLoadIC\_Miss C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:2803  

#10 0x7ffd1fecf1bb (<unknown module>)

0x11f200dfacf8 is located 8 bytes inside of 112-byte region [0x11f200dfacf0,0x11f200dfad60)  

freed by thread T0 here:  

#0 0x7ff694cbc01b in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffd9274a9eb in blink::LayoutObject::SetStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_object.cc:2591  

#2 0x7ffd92f2a5e5 in blink::Text::RecalcTextStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\text.cc:409  

#3 0x7ffd8fcdc95d in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\container\_node.cc:1381  

#4 0x7ffd8f99460a in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:3847  

#5 0x7ffd8fcdca55 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\container\_node.cc:1384  

#6 0x7ffd8f99460a in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:3847  

#7 0x7ffd8fcdca55 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\container\_node.cc:1384  

#8 0x7ffd8f99460a in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:3847  

#9 0x7ffd8fc2d6aa in blink::StyleEngine::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2805  

#10 0x7ffd8fc30267 in blink::StyleEngine::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2828  

#11 0x7ffd8fc30d90 in blink::StyleEngine::UpdateStyleAndLayoutTree C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2935  

#12 0x7ffd8f641f1f in blink::Document::UpdateStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2253  

#13 0x7ffd8f63fe4b in blink::Document::UpdateStyleAndLayoutTreeForThisDocument C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2202  

#14 0x7ffd8f58f134 in blink::LocalFrameView::UpdateStyleAndLayoutInternal C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3269  

#15 0x7ffd8f57306f in blink::LocalFrameView::UpdateStyleAndLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3221  

#16 0x7ffd8f640871 in blink::Document::UpdateStyleAndLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2579  

#17 0x7ffd8f644217 in blink::Document::UpdateStyleAndLayoutForNode C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2435  

#18 0x7ffd92d3ca10 in blink::HTMLElement::offsetTopForBinding C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\html\_element.cc:1802  

#19 0x7ffd9b2c4e96 in blink::`anonymous namespace'::v8_html_element::OffsetTopAttributeGetCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_html_element.cc:623 #20 0x7ffd85b656b6 in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:147 #21 0x7ffd85b62b01 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:114  

#22 0x7ffd85b6079a in v8::internal::Builtins::InvokeApiFunction C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:228  

#23 0x7ffd86b63876 in v8::internal::Object::GetPropertyWithAccessor C:\b\s\w\ir\cache\builder\src\v8\src\objects\objects.cc:1461  

#24 0x7ffd86b60c07 in v8::internal::Object::GetProperty C:\b\s\w\ir\cache\builder\src\v8\src\objects\objects.cc:1180  

#25 0x7ffd8647ceb8 in v8::internal::LoadIC::Load C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:512  

#26 0x7ffd8648f611 in v8::internal::KeyedLoadIC::Load C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:1574  

#27 0x7ffd864ae327 in v8::internal::Runtime\_KeyedLoadIC\_Miss C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:2803

previously allocated by thread T0 here:  

#0 0x7ff694cbc11b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffd7eb401cd in partition\_alloc::PartitionRoot<1>::Alloc C:\b\s\w\ir\cache\builder\src\base\allocator\partition\_allocator\partition\_root.h:1997  

#2 0x7ffd92bd3d66 in blink::ComputedStyle::Clone C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\style\computed\_style.cc:207  

#3 0x7ffd92fa7f77 in blink::StyleResolver::ApplyInheritance C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_resolver.cc:972  

#4 0x7ffd92fa8eb5 in blink::StyleResolver::InitStyleAndApplyInheritance C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_resolver.cc:996  

#5 0x7ffd92fab27e in blink::StyleResolver::ApplyBaseStyleNoCache C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_resolver.cc:1183  

#6 0x7ffd92fa5ddc in blink::StyleResolver::ApplyBaseStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_resolver.cc:1385  

#7 0x7ffd92fa4792 in blink::StyleResolver::ResolveStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_resolver.cc:885  

#8 0x7ffd8f99199e in blink::Element::OriginalStyleForLayoutObject C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:3640  

#9 0x7ffd8f990d20 in blink::Element::StyleForLayoutObject C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:3602  

#10 0x7ffd8f9961ae in blink::Element::RecalcOwnStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:4052  

#11 0x7ffd8f993a02 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:3756  

#12 0x7ffd8fcdca55 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\container\_node.cc:1384  

#13 0x7ffd8f99460a in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:3847  

#14 0x7ffd8fcdca55 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\container\_node.cc:1384  

#15 0x7ffd8f99460a in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:3847  

#16 0x7ffd8fc2d6aa in blink::StyleEngine::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2805  

#17 0x7ffd8fc30267 in blink::StyleEngine::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2828  

#18 0x7ffd8fc30d90 in blink::StyleEngine::UpdateStyleAndLayoutTree C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2935  

#19 0x7ffd8f641f1f in blink::Document::UpdateStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2253  

#20 0x7ffd8f63fe4b in blink::Document::UpdateStyleAndLayoutTreeForThisDocument C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2202  

#21 0x7ffd8f58f134 in blink::LocalFrameView::UpdateStyleAndLayoutInternal C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3269  

#22 0x7ffd8f57306f in blink::LocalFrameView::UpdateStyleAndLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3221  

#23 0x7ffd8f640871 in blink::Document::UpdateStyleAndLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2579  

#24 0x7ffd8f645bcd in blink::Document::EnsurePaintLocationDataValidForNode C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2675  

#25 0x7ffd92d3c9a6 in blink::HTMLElement::offsetTopForBinding C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\html\_element.cc:1798  

#26 0x7ffd9b2c4e96 in blink::`anonymous namespace'::v8\_html\_element::OffsetTopAttributeGetCallback C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\renderer\bindings\modules\v8\v8\_html\_element.cc:623  

#27 0x7ffd85b656b6 in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:147

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\html\_element.cc:1802 in blink::HTMLElement::offsetTopForBinding  

Shadow bytes around the buggy address:  

0x041a40f3f540: fa fa fa fa fa fa 00 00 00 00 00 00 00 00 00 00  

0x041a40f3f550: 00 00 00 fa fa fa fa fa fa fa fa fa 00 00 00 00  

0x041a40f3f560: 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa  

0x041a40f3f570: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x041a40f3f580: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

=>0x041a40f3f590: 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fd[fd]  

0x041a40f3f5a0: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x041a40f3f5b0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x041a40f3f5c0: fd fd fa fa fa fa fa fa fa fa fd fd fd fd fd fd  

0x041a40f3f5d0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x041a40f3f5e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa  

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

==7604==ABORTING

\*\*Chrome version: \*\* 100.0.4896.127 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 855 B)
- [asan.txt](attachments/asan.txt) (text/plain, 12.0 KB)

## Timeline

### [Deleted User] (2022-06-21)

[Empty comment from Monorail migration]

### aj...@google.com (2022-06-21)

Hi m.coolie - have you tried on a released chrome version (103+)?

### aj...@chromium.org (2022-06-21)

Note: you have to click in the tab.

On HEAD I hit this DCHECK:- 

third_party\blink\renderer\core\dom\layout_tree_builder_traversal.cc:56
ContainerNode* LayoutTreeBuilderTraversal::Parent(const Node& node) {
  // TODO(hayato): Uncomment this once we can be sure
  // LayoutTreeBuilderTraversal::parent() is used only for a node which is
  // connected.
  // DCHECK(node.isConnected());
  if (auto* element = DynamicTo<PseudoElement>(node)) {
    DCHECK(node.parentNode());
    return node.parentNode();
  }
  return FlatTreeTraversal::Parent(node);
}

I assume in a release build we will pass the dcheck and something bad will happen.

Sev:high - rce
FoundIn-102 as oldest released version.

[Monorail components: Blink>DOM]

### [Deleted User] (2022-06-21)

[Empty comment from Monorail migration]

### ja...@chromium.org (2022-06-21)

It looks like this involves fullscreen (top layer?) and DisplayLocking

### ja...@chromium.org (2022-06-21)

The DCHECK is being hit because there is a ::backdrop pseudo element with no parent.
I'm guessing that pseudo elements are always supposed to have a parent...?

Here is the stack trace for where the ::backdrop is removed from its parent:
#0 0x7fb21f96e469 base::debug::CollectStackTrace()                                                                                                                                                                                             
#1 0x7fb21f85b8c3 base::debug::StackTrace::StackTrace()                                                                                                                                                                                        
#2 0x7fb21423e9b2 blink::PseudoElement::RemovedFrom()                                                                                                                                                                                          
#3 0x7fb21423dade blink::PseudoElement::Dispose()                                                                                                                                                                                              
#4 0x7fb215055732 blink::PseudoElementData::ClearPseudoElements()                                                                                                                                                                              
#5 0x7fb21503d608 blink::Element::DetachLayoutTree()                                                                                                                                                                                           
#6 0x7fb2141b9a6e blink::DisplayLockContext::DetachDescendantTopLayerElements()                                                                                                                                                                
#7 0x7fb2141b96c7 blink::DisplayLockContext::Lock()                                                                                                                                                                                            
#8 0x7fb2141b9341 blink::DisplayLockContext::NotifyRenderAffectingStateChanged()                                                                                                                                                               
#9 0x7fb2141b8fc9 blink::DisplayLockContext::SetRequestedState()                                                                                                                                                                               
#10 0x7fb21503e195 blink::Element::StyleForLayoutObject()                                                                                                                                                                                      
#11 0x7fb21503f679 blink::Element::RecalcOwnStyle()                                                                                                                                                                                            
#12 0x7fb21503eb8b blink::Element::RecalcStyle()                                                                                                                                                                                               
#13 0x7fb214ff2422 blink::ContainerNode::RecalcDescendantStyles()                                                                                                                                                                              
#14 0x7fb21503f194 blink::Element::RecalcStyle()                                                                                                                                                                                               
#15 0x7fb214186977 blink::StyleEngine::RecalcStyle()                                                                                                                                                                                           
#16 0x7fb214187d22 blink::StyleEngine::UpdateStyleAndLayoutTree()                                                                                                                                                                              
#17 0x7fb215000550 blink::Document::UpdateStyle()                                                                                                                                                                                              
#18 0x7fb214fff7f6 blink::Document::UpdateStyleAndLayoutTreeForThisDocument()                                                                                                                                                                  
#19 0x7fb214484b6a blink::LocalFrameView::UpdateStyleAndLayoutInternal()                                                                                                                                                                       
#20 0x7fb2144790ab blink::LocalFrameView::UpdateStyleAndLayout()                                                                                                                                                                               
#21 0x7fb214fffb97 blink::Document::UpdateStyleAndLayout()                                                                                                                                                                                     
#22 0x7fb2150017de blink::Document::UpdateStyleAndLayoutForNode()                                                                                                                                                                              
#23 0x7fb2145e168e blink::HTMLElement::unclosedOffsetParent()     

I tried not removing pseudo elements in DetachDescendantTopLayerElements, but that didn't help.
I tried avoiding creating a ::backdrop on DisplayLocked elements, but it would seem that the problematic ::backdrop is created before the element actually gets DisplayLocked.

### [Deleted User] (2022-06-22)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-22)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2022-06-28)

ping @Owner

### [Deleted User] (2022-07-06)

jarhar: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2022-07-07)

@ping Anyone take a look at this issue?

### ja...@chromium.org (2022-07-07)

I made a fix, hopefully it works: https://chromium-review.googlesource.com/c/chromium/src/+/3751710

### [Deleted User] (2022-07-22)

jarhar: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-07-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ab55fe05c2c37693afe5021aa637fb2d7491eb6d

commit ab55fe05c2c37693afe5021aa637fb2d7491eb6d
Author: Joey Arhar <jarhar@chromium.org>
Date: Tue Jul 26 19:42:57 2022

Don't re-lock DisplayLocks during forced unlock

When a DisplayLock is unlocked via ForceUnlockIfNeeded, subsequent
updates to the DisplayLock can cause it to become locked again which is
problematic.

This patch prevents the DisplayLock from being locked again until the
next frame.

Fixed: 1338135
Change-Id: I07790658e25ea9fe2f4e8de154e3a58e7e08892b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3751710
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Reviewed-by: Vladimir Levin <vmpstr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1028405}

[add] https://crrev.com/ab55fe05c2c37693afe5021aa637fb2d7491eb6d/third_party/blink/web_tests/external/wpt/fullscreen/crashtests/content-visibility-crash.html
[modify] https://crrev.com/ab55fe05c2c37693afe5021aa637fb2d7491eb6d/third_party/blink/renderer/core/display_lock/display_lock_context.cc


### [Deleted User] (2022-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-27)

Requesting merge to extended stable M102 because latest trunk commit (1028405) appears to be after extended stable branch point (992738).

Requesting merge to stable M103 because latest trunk commit (1028405) appears to be after stable branch point (1002911).

Requesting merge to beta M104 because latest trunk commit (1028405) appears to be after beta branch point (1012729).

Requesting merge to dev M105 because latest trunk commit (1028405) appears to be after dev branch point (1027018).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-27)

Merge approved: your change passed merge requirements and is auto-approved for M105. Please go ahead and merge the CL to branch 5195 (refs/branch-heads/5195) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-27)

Merge review required: M104 has already been cut for stable release.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-27)

Merge review required: M103 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-27)

Merge review required: M102 is already shipping to stable.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3dbd64384ceafe88142424c0d877b749a1cc0616

commit 3dbd64384ceafe88142424c0d877b749a1cc0616
Author: Joey Arhar <jarhar@chromium.org>
Date: Thu Jul 28 14:26:27 2022

Don't re-lock DisplayLocks during forced unlock

When a DisplayLock is unlocked via ForceUnlockIfNeeded, subsequent
updates to the DisplayLock can cause it to become locked again which is
problematic.

This patch prevents the DisplayLock from being locked again until the
next frame.

(cherry picked from commit ab55fe05c2c37693afe5021aa637fb2d7491eb6d)

Fixed: 1338135
Change-Id: I07790658e25ea9fe2f4e8de154e3a58e7e08892b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3751710
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Reviewed-by: Vladimir Levin <vmpstr@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1028405}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3790229
Commit-Queue: Vladimir Levin <vmpstr@chromium.org>
Auto-Submit: Joey Arhar <jarhar@chromium.org>
Cr-Commit-Position: refs/branch-heads/5195@{#90}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[add] https://crrev.com/3dbd64384ceafe88142424c0d877b749a1cc0616/third_party/blink/web_tests/external/wpt/fullscreen/crashtests/content-visibility-crash.html
[modify] https://crrev.com/3dbd64384ceafe88142424c0d877b749a1cc0616/third_party/blink/renderer/core/display_lock/display_lock_context.cc


### [Deleted User] (2022-07-28)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### rz...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-29)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-07-29)

1. https://crrev.com/c/3791907
2. Low, no conflicts
3. 105
4. Yes

### am...@chromium.org (2022-08-04)

m104 merge approved, please merge this fix to branch 5112 at your earliest convenience - thanks! 

### am...@google.com (2022-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-05)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2022-08-08)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-09)

1. Just https://crrev.com/c/3817524
2. Low, no conflicts
3. 105
4. Yes

### gm...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b937ed2c29ef897a844d88783cb2abf3b9f2dcd3

commit b937ed2c29ef897a844d88783cb2abf3b9f2dcd3
Author: Joey Arhar <jarhar@chromium.org>
Date: Thu Aug 11 19:29:32 2022

Don't re-lock DisplayLocks during forced unlock

When a DisplayLock is unlocked via ForceUnlockIfNeeded, subsequent
updates to the DisplayLock can cause it to become locked again which is
problematic.

This patch prevents the DisplayLock from being locked again until the
next frame.

(cherry picked from commit ab55fe05c2c37693afe5021aa637fb2d7491eb6d)

Fixed: 1338135
Change-Id: I07790658e25ea9fe2f4e8de154e3a58e7e08892b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3751710
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Reviewed-by: Vladimir Levin <vmpstr@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1028405}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3826480
Auto-Submit: Joey Arhar <jarhar@chromium.org>
Commit-Queue: Vladimir Levin <vmpstr@chromium.org>
Cr-Commit-Position: refs/branch-heads/5112@{#1444}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[add] https://crrev.com/b937ed2c29ef897a844d88783cb2abf3b9f2dcd3/third_party/blink/web_tests/external/wpt/fullscreen/crashtests/content-visibility-crash.html
[modify] https://crrev.com/b937ed2c29ef897a844d88783cb2abf3b9f2dcd3/third_party/blink/renderer/core/display_lock/display_lock_context.cc


### am...@chromium.org (2022-08-16)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-16)

[Empty comment from Monorail migration]

### gm...@google.com (2022-08-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/96306321286ad6efb7dff37c30e7034168333f0e

commit 96306321286ad6efb7dff37c30e7034168333f0e
Author: Joey Arhar <jarhar@chromium.org>
Date: Fri Aug 19 10:04:11 2022

[M102-LTS] Don't re-lock DisplayLocks during forced unlock

When a DisplayLock is unlocked via ForceUnlockIfNeeded, subsequent
updates to the DisplayLock can cause it to become locked again which is
problematic.

This patch prevents the DisplayLock from being locked again until the
next frame.

(cherry picked from commit ab55fe05c2c37693afe5021aa637fb2d7491eb6d)

Fixed: 1338135
Change-Id: I07790658e25ea9fe2f4e8de154e3a58e7e08892b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3751710
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1028405}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3817524
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Reviewed-by: Michael Ershov <miersh@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1317}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[add] https://crrev.com/96306321286ad6efb7dff37c30e7034168333f0e/third_party/blink/web_tests/external/wpt/fullscreen/crashtests/content-visibility-crash.html
[modify] https://crrev.com/96306321286ad6efb7dff37c30e7034168333f0e/third_party/blink/renderer/core/display_lock/display_lock_context.cc


### gi...@appspot.gserviceaccount.com (2022-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d7a8043d5ac96dfbb0c54a96df4d17d6e1b8cc36

commit d7a8043d5ac96dfbb0c54a96df4d17d6e1b8cc36
Author: Joey Arhar <jarhar@chromium.org>
Date: Fri Aug 19 11:07:51 2022

[M96-LTS] Don't re-lock DisplayLocks during forced unlock

When a DisplayLock is unlocked via ForceUnlockIfNeeded, subsequent
updates to the DisplayLock can cause it to become locked again which is
problematic.

This patch prevents the DisplayLock from being locked again until the
next frame.

(cherry picked from commit ab55fe05c2c37693afe5021aa637fb2d7491eb6d)

Fixed: 1338135
Change-Id: I07790658e25ea9fe2f4e8de154e3a58e7e08892b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3751710
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1028405}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3791907
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Michael Ershov <miersh@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1689}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[add] https://crrev.com/d7a8043d5ac96dfbb0c54a96df4d17d6e1b8cc36/third_party/blink/web_tests/external/wpt/fullscreen/crashtests/content-visibility-crash.html
[modify] https://crrev.com/d7a8043d5ac96dfbb0c54a96df4d17d6e1b8cc36/third_party/blink/renderer/core/display_lock/display_lock_context.cc


### rz...@google.com (2022-08-19)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-19)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1338135?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060030)*

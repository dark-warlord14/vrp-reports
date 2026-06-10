# [Chrome VRP - bugSWAT] DCHECK failure in id_ != kInvalidNodeId in maglev-ir.h

| Field | Value |
|-------|-------|
| **Issue ID** | [374811614](https://issues.chromium.org/issues/374811614) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | vi...@chromium.org |
| **Created** | 2024-10-22 |
| **Bounty** | $10,000.00 |

## Description

VULNERABILITY DETAILS

## INTRODUCE

After bisect, it was determined that following commit caused this problem.

- Commit Info
  - Version: 96389
  - link: <https://crrev.com/249c89719686e45bb5dbac991ee04fc3786534d2>
- Commit Message

```
commit 249c89719686e45bb5dbac991ee04fc3786534d2
Author: Victor Gomes <victorgomes@chromium.org>
Date:   Wed Oct 2 14:22:56 2024 +0200

    [maglev] Use virtual objects from top frame when re-materializing
    
    ... since these contain the most up-to-date objects to that deopt point.
    
    Fixed: 369652820
    Change-Id: I55ad4772aa33c25046a23fd8c27ec0a0905f5f3f
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5899173
    Auto-Submit: Victor Gomes <victorgomes@chromium.org>
    Reviewed-by: Olivier Flückiger <olivf@chromium.org>
    Commit-Queue: Victor Gomes <victorgomes@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#96389}


```
## CRASH LOG

- Debug output

```
# CMD: /tmp/d8-linux-debug-v8-component-96737/d8 --allow-natives-syntax --jit-fuzzing --optimize-on-next-call-optimizes-to-maglev --expose-gc poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/maglev/maglev-ir.h, line 1810
# Debug check failed: id_ != kInvalidNodeId (0 vs. 0).
#
#
#
#FailureMessage Object: 0x7ffda90e2ab0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-96737/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f366b6fec63]
    /tmp/d8-linux-debug-v8-component-96737/libv8_libplatform.so(+0x1a3fd) [0x7f366b6a73fd]
    /tmp/d8-linux-debug-v8-component-96737/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x194) [0x7f366b6e0494]
    /tmp/d8-linux-debug-v8-component-96737/libv8_libbase.so(+0x2bea5) [0x7f366b6dfea5]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(v8::internal::maglev::ValueNode::record_next_use(unsigned int, v8::internal::maglev::InputLocation*)+0x151) [0x7f3669865ec1]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkUse(v8::internal::maglev::ValueNode*, unsigned int, v8::internal::maglev::InputLocation*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*)+0x39) [0x7f3669865bc9]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(void v8::internal::maglev::detail::DeepForVirtualObject<(v8::internal::maglev::detail::DeoptFrameVisitMode)1, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&>(v8::internal::maglev::VirtualObject*, v8::internal::maglev::InputLocation*&, v8::internal::maglev::VirtualObject::List const&, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&)+0x12c) [0x7f366987796c]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(void v8::internal::maglev::CompactInterpreterFrameState::ForEachLocal<void v8::internal::maglev::detail::DeepForEachInputSingleFrameImpl<(v8::internal::maglev::detail::DeoptFrameVisitMode)1, void v8::internal::maglev::detail::DeepForEachInputAndVirtualObject<(v8::internal::maglev::detail::DeoptFrameVisitMode)1, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&>(std::__Cr::conditional<(v8::internal::maglev::detail::DeoptFrameVisitMode)1 == (v8::internal::maglev::detail::DeoptFrameVisitMode)0, v8::internal::maglev::DeoptFrame const, v8::internal::maglev::DeoptFrame>::type&, v8::internal::maglev::InputLocation*&, v8::internal::maglev::VirtualObject::List const&, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&, std::__Cr::function<bool (v8::internal::interpreter::Register)>)::'lambda'(v8::internal::maglev::ValueNode*&, v8::internal::maglev::InputLocation*&)&>(std::__Cr::conditional<(v8::internal::maglev::detail::DeoptFrameVisitMode)1 == (v8::internal::maglev::detail::DeoptFrameVisitMode)0, v8::internal::maglev::DeoptFrame const, v8::internal::maglev::DeoptFrame>::type&, v8::internal::maglev::InputLocation*&, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&, std::__Cr::function<bool (v8::internal::interpreter::Register)>)::'lambda'(v8::internal::maglev::ValueNode*&, v8::internal::interpreter::Register)&>(v8::internal::maglev::MaglevCompilationUnit const&, void v8::internal::maglev::detail::DeepForEachInputSingleFrameImpl<(v8::internal::maglev::detail::DeoptFrameVisitMode)1, void v8::internal::maglev::detail::DeepForEachInputAndVirtualObject<(v8::internal::maglev::detail::DeoptFrameVisitMode)1, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&>(std::__Cr::conditional<(v8::internal::maglev::detail::DeoptFrameVisitMode)1 == (v8::internal::maglev::detail::DeoptFrameVisitMode)0, v8::internal::maglev::DeoptFrame const, v8::internal::maglev::DeoptFrame>::type&, v8::internal::maglev::InputLocation*&, v8::internal::maglev::VirtualObject::List const&, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&, std::__Cr::function<bool (v8::internal::interpreter::Register)>)::'lambda'(v8::internal::maglev::ValueNode*&, v8::internal::maglev::InputLocation*&)&>(std::__Cr::conditional<(v8::internal::maglev::detail::DeoptFrameVisitMode)1 == (v8::internal::maglev::detail::DeoptFrameVisitMode)0, v8::internal::maglev::DeoptFrame const, v8::internal::maglev::DeoptFrame>::type&, v8::internal::maglev::InputLocation*&, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&, std::__Cr::function<bool (v8::internal::interpreter::Register)>)::'lambda'(v8::internal::maglev::ValueNode*&, v8::internal::interpreter::Register)&) const+0x10b) [0x7f3669877cfb]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(void v8::internal::maglev::CompactInterpreterFrameState::ForEachRegister<void v8::internal::maglev::detail::DeepForEachInputSingleFrameImpl<(v8::internal::maglev::detail::DeoptFrameVisitMode)1, void v8::internal::maglev::detail::DeepForEachInputAndVirtualObject<(v8::internal::maglev::detail::DeoptFrameVisitMode)1, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&>(std::__Cr::conditional<(v8::internal::maglev::detail::DeoptFrameVisitMode)1 == (v8::internal::maglev::detail::DeoptFrameVisitMode)0, v8::internal::maglev::DeoptFrame const, v8::internal::maglev::DeoptFrame>::type&, v8::internal::maglev::InputLocation*&, v8::internal::maglev::VirtualObject::List const&, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&, std::__Cr::function<bool (v8::internal::interpreter::Register)>)::'lambda'(v8::internal::maglev::ValueNode*&, v8::internal::maglev::InputLocation*&)&>(std::__Cr::conditional<(v8::internal::maglev::detail::DeoptFrameVisitMode)1 == (v8::internal::maglev::detail::DeoptFrameVisitMode)0, v8::internal::maglev::DeoptFrame const, v8::internal::maglev::DeoptFrame>::type&, v8::internal::maglev::InputLocation*&, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&, std::__Cr::function<bool (v8::internal::interpreter::Register)>)::'lambda'(v8::internal::maglev::ValueNode*&, v8::internal::interpreter::Register)&>(v8::internal::maglev::MaglevCompilationUnit const&, void v8::internal::maglev::detail::DeepForEachInputSingleFrameImpl<(v8::internal::maglev::detail::DeoptFrameVisitMode)1, void v8::internal::maglev::detail::DeepForEachInputAndVirtualObject<(v8::internal::maglev::detail::DeoptFrameVisitMode)1, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&>(std::__Cr::conditional<(v8::internal::maglev::detail::DeoptFrameVisitMode)1 == (v8::internal::maglev::detail::DeoptFrameVisitMode)0, v8::internal::maglev::DeoptFrame const, v8::internal::maglev::DeoptFrame>::type&, v8::internal::maglev::InputLocation*&, v8::internal::maglev::VirtualObject::List const&, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&, std::__Cr::function<bool (v8::internal::interpreter::Register)>)::'lambda'(v8::internal::maglev::ValueNode*&, v8::internal::maglev::InputLocation*&)&>(std::__Cr::conditional<(v8::internal::maglev::detail::DeoptFrameVisitMode)1 == (v8::internal::maglev::detail::DeoptFrameVisitMode)0, v8::internal::maglev::DeoptFrame const, v8::internal::maglev::DeoptFrame>::type&, v8::internal::maglev::InputLocation*&, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&, std::__Cr::function<bool (v8::internal::interpreter::Register)>)::'lambda'(v8::internal::maglev::ValueNode*&, v8::internal::interpreter::Register)&) const+0xb1) [0x7f3669877be1]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(void v8::internal::maglev::CompactInterpreterFrameState::ForEachValue<void v8::internal::maglev::detail::DeepForEachInputSingleFrameImpl<(v8::internal::maglev::detail::DeoptFrameVisitMode)1, void v8::internal::maglev::detail::DeepForEachInputAndVirtualObject<(v8::internal::maglev::detail::DeoptFrameVisitMode)1, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&>(std::__Cr::conditional<(v8::internal::maglev::detail::DeoptFrameVisitMode)1 == (v8::internal::maglev::detail::DeoptFrameVisitMode)0, v8::internal::maglev::DeoptFrame const, v8::internal::maglev::DeoptFrame>::type&, v8::internal::maglev::InputLocation*&, v8::internal::maglev::VirtualObject::List const&, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&, std::__Cr::function<bool (v8::internal::interpreter::Register)>)::'lambda'(v8::internal::maglev::ValueNode*&, v8::internal::maglev::InputLocation*&)&>(std::__Cr::conditional<(v8::internal::maglev::detail::DeoptFrameVisitMode)1 == (v8::internal::maglev::detail::DeoptFrameVisitMode)0, v8::internal::maglev::DeoptFrame const, v8::internal::maglev::DeoptFrame>::type&, v8::internal::maglev::InputLocation*&, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&, std::__Cr::function<bool (v8::internal::interpreter::Register)>)::'lambda'(v8::internal::maglev::ValueNode*&, v8::internal::interpreter::Register)>(v8::internal::maglev::MaglevCompilationUnit const&, void v8::internal::maglev::detail::DeepForEachInputSingleFrameImpl<(v8::internal::maglev::detail::DeoptFrameVisitMode)1, void v8::internal::maglev::detail::DeepForEachInputAndVirtualObject<(v8::internal::maglev::detail::DeoptFrameVisitMode)1, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&>(std::__Cr::conditional<(v8::internal::maglev::detail::DeoptFrameVisitMode)1 == (v8::internal::maglev::detail::DeoptFrameVisitMode)0, v8::internal::maglev::DeoptFrame const, v8::internal::maglev::DeoptFrame>::type&, v8::internal::maglev::InputLocation*&, v8::internal::maglev::VirtualObject::List const&, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&, std::__Cr::function<bool (v8::internal::interpreter::Register)>)::'lambda'(v8::internal::maglev::ValueNode*&, v8::internal::maglev::InputLocation*&)&>(std::__Cr::conditional<(v8::internal::maglev::detail::DeoptFrameVisitMode)1 == (v8::internal::maglev::detail::DeoptFrameVisitMode)0, v8::internal::maglev::DeoptFrame const, v8::internal::maglev::DeoptFrame>::type&, v8::internal::maglev::InputLocation*&, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&, std::__Cr::function<bool (v8::internal::interpreter::Register)>)::'lambda'(v8::internal::maglev::ValueNode*&, v8::internal::interpreter::Register)&&) const+0x1d) [0x7f366987774d]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(void v8::internal::maglev::detail::DeepForEachInputSingleFrameImpl<(v8::internal::maglev::detail::DeoptFrameVisitMode)1, void v8::internal::maglev::detail::DeepForEachInputAndVirtualObject<(v8::internal::maglev::detail::DeoptFrameVisitMode)1, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&>(std::__Cr::conditional<(v8::internal::maglev::detail::DeoptFrameVisitMode)1 == (v8::internal::maglev::detail::DeoptFrameVisitMode)0, v8::internal::maglev::DeoptFrame const, v8::internal::maglev::DeoptFrame>::type&, v8::internal::maglev::InputLocation*&, v8::internal::maglev::VirtualObject::List const&, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&, std::__Cr::function<bool (v8::internal::interpreter::Register)>)::'lambda'(v8::internal::maglev::ValueNode*&, v8::internal::maglev::InputLocation*&)&>(std::__Cr::conditional<(v8::internal::maglev::detail::DeoptFrameVisitMode)1 == (v8::internal::maglev::detail::DeoptFrameVisitMode)0, v8::internal::maglev::DeoptFrame const, v8::internal::maglev::DeoptFrame>::type&, v8::internal::maglev::InputLocation*&, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&, std::__Cr::function<bool (v8::internal::interpreter::Register)>)+0x83) [0x7f3669877133]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(void v8::internal::maglev::detail::DeepForEachInputImpl<(v8::internal::maglev::detail::DeoptFrameVisitMode)1, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&>(std::__Cr::conditional<(v8::internal::maglev::detail::DeoptFrameVisitMode)1 == (v8::internal::maglev::detail::DeoptFrameVisitMode)0, v8::internal::maglev::DeoptFrame const, v8::internal::maglev::DeoptFrame>::type&, v8::internal::maglev::InputLocation*&, v8::internal::maglev::VirtualObject::List const&, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&)+0x70) [0x7f3669877060]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(void v8::internal::maglev::detail::DeepForEachInputForLazy<(v8::internal::maglev::detail::DeoptFrameVisitMode)1, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&>(std::__Cr::conditional<(v8::internal::maglev::detail::DeoptFrameVisitMode)1 == (v8::internal::maglev::detail::DeoptFrameVisitMode)0, v8::internal::maglev::LazyDeoptInfo const, v8::internal::maglev::LazyDeoptInfo>::type*, v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)::'lambda'(v8::internal::maglev::ValueNode*, v8::internal::maglev::InputLocation*)&)+0xa1) [0x7f3669876f81]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkCheckpointNodes(v8::internal::maglev::NodeBase*, v8::internal::maglev::LazyDeoptInfo*, v8::internal::maglev::LiveRangeAndNextUseProcessor::LoopUsedNodes*, v8::internal::maglev::ProcessingState const&)+0x49) [0x7f3669876c49]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(void v8::internal::maglev::LiveRangeAndNextUseProcessor::MarkInputUses<v8::internal::maglev::CallKnownApiFunction>(v8::internal::maglev::CallKnownApiFunction*, v8::internal::maglev::ProcessingState const&)+0xfa) [0x7f366988375a]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(v8::internal::maglev::ProcessResult v8::internal::maglev::LiveRangeAndNextUseProcessor::Process<v8::internal::maglev::CallKnownApiFunction>(v8::internal::maglev::CallKnownApiFunction*, v8::internal::maglev::ProcessingState const&)+0x83) [0x7f36698835a3]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(v8::internal::maglev::ProcessResult v8::internal::maglev::NodeMultiProcessor<v8::internal::maglev::MaxCallDepthProcessor, v8::internal::maglev::LiveRangeAndNextUseProcessor, v8::internal::maglev::DecompressedUseMarkingProcessor>::Process<v8::internal::maglev::CallKnownApiFunction>(v8::internal::maglev::CallKnownApiFunction*, v8::internal::maglev::ProcessingState const&)+0xbb) [0x7f366988349b]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(v8::internal::maglev::GraphProcessor<v8::internal::maglev::NodeMultiProcessor<v8::internal::maglev::DeadNodeSweepingProcessor, v8::internal::maglev::ValueLocationConstraintProcessor, v8::internal::maglev::MaxCallDepthProcessor, v8::internal::maglev::LiveRangeAndNextUseProcessor, v8::internal::maglev::DecompressedUseMarkingProcessor>, false>::ProcessGraph(v8::internal::maglev::Graph*)+0x15c) [0x7f36697e6dec]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(v8::internal::maglev::MaglevCompiler::Compile(v8::internal::LocalIsolate*, v8::internal::maglev::MaglevCompilationInfo*)+0x122b) [0x7f36697e385b]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(v8::internal::maglev::MaglevCompilationJob::ExecuteJobImpl(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x66) [0x7f36698bb3c6]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(v8::internal::OptimizedCompilationJob::ExecuteJob(v8::internal::RuntimeCallStats*, v8::internal::LocalIsolate*)+0x8d) [0x7f366862f74d]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(+0x2a45405) [0x7f3668645405]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(v8::internal::Compiler::CompileOptimized(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::ConcurrencyMode, v8::internal::CodeKind)+0xc0) [0x7f36686479e0]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(+0x3923957) [0x7f3669523957]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(v8::internal::Runtime_CompileOptimized(int, unsigned long*, v8::internal::Isolate*)+0x90) [0x7f3669523330]
    /tmp/d8-linux-debug-v8-component-96737/libv8.so(+0x1f87c7d) [0x7f3667b87c7d]


```
## Other

Please note to include the flags `--allow-natives-syntax --jit-fuzzing --optimize-on-next-call-optimizes-to-maglev --expose-gc` for clusterfuzz classification.

VERSION
Tested on v8 version: 13.1.0 - 13.2.0

REPRODUCTION CASE

1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-96737.zip
2. Run: `d8 --allow-natives-syntax --jit-fuzzing --optimize-on-next-call-optimizes-to-maglev --expose-gc poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Jerry

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 392 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-10-22)

Detailed Report: https://clusterfuzz.com/testcase?key=6332353597079552

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  id_ != kInvalidNodeId in maglev-ir.h
  v8::internal::maglev::NodeBase::id
  v8::internal::maglev::ValueNode::record_next_use
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=96388:96389

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6332353597079552

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### 24...@project.gserviceaccount.com (2024-10-22)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-10-22)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/249c89719686e45bb5dbac991ee04fc3786534d2 ([maglev] Use virtual objects from top frame when re-materializing

... since these contain the most up-to-date objects to that deopt point.

Fixed: 369652820
Change-Id: I55ad4772aa33c25046a23fd8c27ec0a0905f5f3f
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5899173
Auto-Submit: Victor Gomes <victorgomes@chromium.org>
Reviewed-by: Olivier Flückiger <olivf@chromium.org>
Commit-Queue: Victor Gomes <victorgomes@chromium.org>
Cr-Commit-Position: refs/heads/main@{#96389}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### am...@chromium.org (2024-10-22)

Thanks for the report, Jerry.
This reproduced quickly and cleanly with clusterfuzz so I didn't attempt to manually reproduce.
Over to victorgomes@

### pe...@google.com (2024-10-22)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-10-22)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-10-30)

This issue appears to be blocking an upcoming release and is therefore an **Urgent Release Blocking Issue** as per <http://go/chrome-slo#release-blocking-issues>. Bumping the priority to P0 to better reflect the urgency.

If this is not a release blocking issue, please adjust the release block field. Adjusting the priority will have no affect, P0 will be re-applied whilever this is marked as a release blocking issue.

### vi...@chromium.org (2024-10-31)

I'll need more time to investigate and come up with a good solution for this issue.

The problem is an elided-but-modified virtual object that does not contain an use of the modified field inside an inlined function.

I reverted the object tracking feature on M132: <https://chromium-review.googlesource.com/c/v8/v8/+/5979829>
The feature is already disabled in M130. So we will need to merge that to M131.

### pe...@google.com (2024-10-31)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### vi...@chromium.org (2024-10-31)

1. Vulnerability / Release blocker.
2. <https://chromium-review.googlesource.com/c/v8/v8/+/5979829>
3. Yes. It's a revert of a flag.
4. No.
5. N/A.
6. No.

### pg...@google.com (2024-10-31)

(Marking bug as fixed for other automation to take effect for merges - merge review to follow)

### 24...@project.gserviceaccount.com (2024-11-01)

ClusterFuzz testcase 6332353597079552 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=96913:96914

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### am...@chromium.org (2024-11-04)

131 merge approved; please merge this flag change to 13.1 ASAP, by 10am Pacific tomorrow, so this change can be including in M131 Stable RC (being cut tomorrow)

### ap...@google.com (2024-11-05)

Project: v8/v8  

Branch: refs/branch-heads/13.1  

Author: Victor Gomes <[victorgomes@chromium.org](mailto:victorgomes@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5979711>

Merged: Revert "Reland "[maglev] Enable object tracking""

---


Expand for full commit details
```
Merged: Revert "Reland "[maglev] Enable object tracking"" 
 
This reverts commit f15986d4a89e6fba1daa8d3cd96f78227cd27b06. 
 
Reason for revert: 374811614 
 
Original change's description: 
> Reland "[maglev] Enable object tracking" 
> 
> This is a reland of commit 0654522388d6a3782b9831b5de49b0c0abe0f643 
> 
> Original change's description: 
> > [maglev] Enable object tracking 
> > 
> > Bug: v8:7700 
> > Change-Id: I3ae73b0ae19e3fc5b3d1205c6cdfac24505e517b 
> > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5803785 
> > Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
> > Auto-Submit: Victor Gomes <victorgomes@chromium.org> 
> > Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
> > Cr-Commit-Position: refs/heads/main@{#95758} 
> 
> Bug: v8:7700 
> Change-Id: I47f8346a09872146f044040fe1648bf2ef5acbbe 
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5890514 
> Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
> Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
> Cr-Commit-Position: refs/heads/main@{#96301} 
 
Bug: v8:7700, 374811614 
 
(cherry picked from commit 1dc8d0481b2f4040505cbddcb45970290375e8fa) 
 
Change-Id: I0d418c21c8b362f8b9ce6d154a15fe87784a5a23 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5979711 
Commit-Queue: Marja Hölttä <marja@chromium.org> 
Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
Auto-Submit: Victor Gomes <victorgomes@chromium.org> 
Reviewed-by: Marja Hölttä <marja@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.1@{#12} 
Cr-Branched-From: 7998da66cb2883ef9734743857713b1194212d9a-refs/heads/13.1.201@{#1} 
Cr-Branched-From: 5e9af2a913539cf67091def99b62f49afece6f56-refs/heads/main@{#96554}

```

---

Files:

- M `src/flags/flag-definitions.h`

---

Hash: 29cea0aef8d527556a4bc4ce6f7a26829e02e700  

Date:  Thu Oct 31 07:39:14 2024


---

### pe...@google.com (2024-11-05)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### vi...@chromium.org (2024-11-05)

This flag is disabled on M126.

1. No
2. No

### ha...@google.com (2024-11-05)

Change has landed on M131. Removing `Approved-131` state

### qk...@google.com (2024-11-07)

Labeling as LTS-NotApplicable-120 because the fix[1] was to revert the CL to re-land the original CL[2], and the original CL[2] was not merged into the M126. Thus, we don't need to merge the fix to M126.

[1] https://chromium-review.googlesource.com/c/v8/v8/+/5979711
[2] https://chromium-review.googlesource.com/c/v8/v8/+/5803785

### sp...@google.com (2024-11-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process / the renderer + $1,000 bisect bonus + $2,000 bugSWAT bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-08)

Congratulations Jerry! Thank you for your efforts and reporting this issue to us during the bugSWAT bonus period -- nice work!

### pe...@google.com (2025-02-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/374811614)*

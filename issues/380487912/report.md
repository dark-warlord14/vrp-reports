# Use-After-Free in blink::ClipboardItem::ClipboardItem

| Field | Value |
|-------|-------|
| **Issue ID** | [380487912](https://issues.chromium.org/issues/380487912) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bindings |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2024-11-23 |
| **Bounty** | $11,000.00 |

## Description

**Tested OS:** Ubuntu 22.04  

**Tested Chrome Version:** Chromium 133.0.6847.2

---

**Reproduction Steps:**

Run the following command:

```
./chrome http://localhost:8880/poc.html

```

---

**Bisection:**

The issue appears to have been introduced in this changelist (CL):  

<https://chromium-review.googlesource.com/c/chromium/src/+/6013586>

---

**Analysis:**

In this CL, a new class `MemberScriptPromise` is introduced, which allows automatic conversion from `ScriptPromise` to `MemberScriptPromise` via an overloaded operator. Although I haven't analyzed it in detail yet, the AddressSanitizer (ASan) logs indicate that during the conversion, there's an access to an already freed underlying promise object.

**Relevant Code Snippet from the CL:**

```
diff --git a/third_party/blink/renderer/bindings/core/v8/script_promise.h b/third_party/blink/renderer/bindings/core/v8/script_promise.h
index 2054cae..f56593b2 100644
--- a/third_party/blink/renderer/bindings/core/v8/script_promise.h
+++ b/third_party/blink/renderer/bindings/core/v8/script_promise.h

+  // NOLINTNEXTLINE(google-explicit-constructor)
+  operator MemberScriptPromise<IDLResolvedType>() const {
+    return MemberScriptPromise<IDLResolvedType>(isolate_, V8Promise());
+  }
+

```

**ASan Log Extract:**

```
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x72b37c287460 at pc 0x56d3bba0e81c bp 0x7ffdc9a34ac0 sp 0x7ffdc9a34ab8
READ of size 8 at 0x72b37c287460 thread T0 (chrome)
    #0 0x56d3bba0e81b in ValueAsAddress<v8::Promise> ../../v8/include/v8-internal.h:1692:12
    #1 0x56d3bba0e81b in New ../../v8/include/v8-local-handle.h:215:30
    #2 0x56d3bba0e81b in New ../../v8/include/v8-local-handle.h:431:21
    #3 0x56d3bba0e81b in New ../../v8/include/v8-local-handle.h:357:12
    #4 0x56d3bba0e81b in Get ../../v8/include/v8-traced-handle.h:129:49
    #5 0x56d3bba0e81b in V8Promise ../../third_party/blink/renderer/bindings/core/v8/script_promise.h:251:62
    #6 0x56d3bba0e81b in operator MemberScriptPromise ../../third_party/blink/renderer/bindings/core/v8/script_promise.h:339:59
    #7 0x56d3bba0e81b in pair<const WTF::String &, const blink::ScriptPromise<blink::V8UnionBlobOrString> &, 0> ../../third_party/libc++/src/include/__utility/pair.h:163:48
    #8 0x56d3bba0e81b in Construct<const WTF::String &, const blink::ScriptPromise<blink::V8UnionBlobOrString> &> ../../third_party/blink/renderer/platform/wtf/construct_traits.h:28:9
    #9 0x56d3bba0e81b in std::__Cr::pair<WTF::String, blink::MemberScriptPromise<blink::V8UnionBlobOrString>>* WTF::ConstructTraits<std::__Cr::pair<WTF::String, blink::MemberScriptPromise<blink::V8UnionBlobOrString>>, WTF::VectorTraits<std::__Cr::pair<WTF::String, blink::MemberScriptPromise<blink::V8UnionBlobOrString>>>, blink::HeapAllocator>::ConstructAndNotifyElement<WTF::String const&, blink::ScriptPromise<blink::V8UnionBlobOrString> const&>(void*, WTF::String const&, blink::ScriptPromise<blink::V8UnionBlobOrString> const&) ../../third_party/blink/renderer/platform/wtf/construct_traits.h:39:17
    #10 0x56d3bba0c041 in emplace_back<const WTF::String &, const blink::ScriptPromise<blink::V8UnionBlobOrString> &> ../../third_party/blink/renderer/platform/wtf/vector.h:2174:7
    #11 0x56d3bba0c041 in blink::ClipboardItem::ClipboardItem(WTF::Vector<std::__Cr::pair<WTF::String, blink::ScriptPromise<blink::V8UnionBlobOrString>>, 0u, WTF::PartitionAllocator> const&) ../../third_party/blink/renderer/modules/clipboard/clipboard_item.cc:70:24

0x72b37c287460 is located 64 bytes inside of 80-byte region [0x72b37c287420,0x72b37c287470)
freed by thread T0 (chrome) here:
    #0 0x56d391d089f6 in __interceptor_free _asan_rtl_:3
    #1 0x56d397d35b78 in v8::internal::TracedHandles::DeleteEmptyBlocks() ../../v8/src/handles/traced-handles.cc:308:5
    #2 0x56d397ede800 in v8::internal::Heap::EnsureSweepingCompleted(v8::internal::Heap::SweepingForcedFinalizationMode) ../../v8/src/heap/heap.cc:7409:32
    #3 0x56d397ee0813 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) ../../v8/src/heap/heap.cc
    #4 0x56d397f32e45 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_0::operator()() const ../../v8/src/heap/heap.cc:1742:7
    #5 0x56d397f3264c in void heap::base::Stack::SetMarkerAndCallbackImpl<v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)::$_0>(heap::base::Stack*, void*, void const*) ../../v8/src/heap/base/stack.h:167:5
    #6 0x56d399ed6952 in PushAllRegistersAndIterateStack push_registers_asm.cc
    #7 0x56d397ed5275 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ../../v8/src/heap/heap.cc:1710:11
    #8 0x56d397ef94e3 in v8::internal::Heap::CollectAllGarbage(v8::internal::GarbageCollectionFlags, v8::GarbageCollectionReason, const char*) ../../v8/src/heap/heap.cc:1358:3
    #9 0x56d397ef94e3 in v8::internal::Heap::CollectGarbageOnMemoryPressure() ../../v8/src/heap/heap.cc:4236:7

previously allocated by thread T0 (chrome) here:
    #0 0x56d391d08c94 in __interceptor_malloc _asan_rtl_:3
    #1 0x56d397d3307d in v8::internal::TracedHandles::RefillUsableNodeBlocks() ../../v8/src/handles/traced-handles.cc:107:13
    #2 0x56d397d3477e in v8::internal::TracedHandles::Create(v8::internal::Address) ../../v8/src/handles/traced-handles.cc:196:7
    #3 0x56d3b8c6f6b7 in blink::V8Function::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&) ../../third_party/blink/renderer/bindings/core/v8/v8_function.cc:76:15
    #4 0x56d3b8c6fa47 in blink::V8Function::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&) ../../third_party/blink/renderer/bindings/core/v8/v8_function.cc:133:15

```

## Attachments

- [crash.html](attachments/crash.html) (text/html, 768 B)
- [asan.log](attachments/asan.log) (text/plain, 25.0 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-11-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6331406607122432.

### am...@chromium.org (2024-11-25)

Thank for the report!

Clusterfuzz was not able to reproduce this based on the provided testcase. Interim triage based on the stack track and bisect.
S1/P1 based on unprotected renderer memory corruption.

### ja...@chromium.org (2024-11-26)

This is reliably DCHECKing without asan, so it will hopefully be easy to diagnose. I'll work on it tomorrow.

### ml...@chromium.org (2024-11-26)

Seems like we reclaim the V98 promise as we think it's unreachable. Lmk if you need help here, Nate -- I think this could be an interesting crasher and I couldn't spot anything obvious on first sight.

### pe...@google.com (2024-11-26)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-11-26)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ap...@google.com (2024-11-27)

Project: chromium/src  

Branch: main  

Author: Nate Chapin <[japhet@chromium.org](mailto:japhet@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6052355>

ClipboardItem's constructor should take a HeapVector with MemberScriptPromises

---


Expand for full commit details
```
ClipboardItem's constructor should take a HeapVector with MemberScriptPromises 
 
Fixed: 380487912 
Change-Id: Ia0f9bf6ebfbdd5dfc5eb2b598f6c70f7f3b57f89 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6052355 
Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
Commit-Queue: Nate Chapin <japhet@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1388913}

```

---

Files:

- M `third_party/blink/renderer/bindings/core/v8/idl_types.h`
- M `third_party/blink/renderer/modules/clipboard/clipboard_item.cc`
- M `third_party/blink/renderer/modules/clipboard/clipboard_item.h`
- M `third_party/blink/renderer/modules/clipboard/clipboard_promise.cc`

---

Hash: 0a53b7a33a55ad952eb7b3afc42e7badf77c7468  

Date:  Wed Nov 27 17:41:55 2024


---

### sp...@google.com (2024-12-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 for high-quality report of memory corruption in a sandboxed process / renderer + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-12-05)

Congratulations Cassidy Kim! Thank you for your efforts and reporting this issue to us -- nice work!

### ch...@google.com (2025-03-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/380487912)*

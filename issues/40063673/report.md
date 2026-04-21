# Security: segv in JsonStringifier::SerializeString

| Field | Value |
|-------|-------|
| **Issue ID** | [40063673](https://issues.chromium.org/issues/40063673) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>API, Blink>JavaScript>GarbageCollection, Blink>JavaScript>Runtime |
| **Platforms** | Linux |
| **Reporter** | wh...@gmail.com |
| **Assignee** | di...@chromium.org |
| **Created** | 2023-03-20 |
| **Bounty** | $8,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

JsonStringifier::SerializeString

#0 0x00007f1cd1657c40 in v8::internal::FlatStringReader::Get<unsigned char> (this=0x7f1c441ae890, index=969) at ../../src/objects/string-inl.h:347  

#1 0x00007f1cd1652496 in v8::internal::JsonStringifier::SerializeString\_<unsigned char, unsigned char> (this=0x7f1c441aed48, string=...) at ../../src/json/json-stringifier.cc:1038  

#2 0x00007f1cd164fbe8 in v8::internal::JsonStringifier::SerializeString (this=0x7f1c441aed48, object=...) at ../../src/json/json-stringifier.cc:1132  

#3 0x00007f1cd1653b32 in v8::internal::JsonStringifier::Serialize\_<false> (this=0x7f1c441aed48, object=..., comma=false, key=...) at ../../src/json/json-stringifier.cc:620  

#4 0x00007f1cd1650e71 in v8::internal::JsonStringifier::SerializeObject (this=0x7f1c441aed48, obj=...) at ../../src/json/json-stringifier.cc:46  

#5 0x00007f1cd164d8f0 in v8::internal::JsonStringifier::Stringify (this=0x7f1c441aed48, object=..., replacer=..., gap=...) at ../../src/json/json-stringifier.cc:232  

#6 0x00007f1cd164d7e3 in v8::internal::JsonStringify (isolate=0x7f1c3c000b80, object=..., replacer=..., gap=...) at ../../src/json/json-stringifier.cc:145  

#7 0x00007f1cd0dfb5ff in v8::internal::Builtin\_Impl\_JsonStringify (args=..., isolate=0x7f1c3c000b80) at ../../src/builtins/builtins-json.cc:37  

#8 0x00007f1cd0dfb2a3 in v8::internal::Builtin\_JsonStringify (args\_length=8, args\_object=0x7f1c441aef80, isolate=0x7f1c3c000b80) at ../../src/builtins/builtins-json.cc:32  

#9 0x00007f1cd057d43d in Builtins\_CEntry\_Return1\_ArgvOnStack\_BuiltinExit () from /home/uuu/v8\_src.updated/v8/out/x64.debug/libv8.so  

#10 0x00007f1cd01e33c8 in Builtins\_InterpreterEntryTrampoline () from /home/uuu/v8\_src.updated/v8/out/x64.debug/libv8.so  

#11 0x00000a9c00000251 in ?? ()  

#12 0x00000a9c003859e5 in ?? ()  

#13 0x0000000000000010 in ?? ()

**VERSION**  

v8 11.3.169 and current HEAD

**REPRODUCTION CASE**

please run with debug d8 and following command

for i in {1..999}; do ./d8 --future --harmony --assert-types --maglev-assert --harmony-struct poc.js ; done

[COV] edge counters initialized. Shared memory: (null) with 1187200 edges  

V8 is running with experimental features enabled. Stability and security will suffer.  

Received signal 11 SEGV\_ACCERR 212e001cb069

==== C stack trace ===============================

[0x55ea2b113dc2]  

[0x7fa16fe65420]  

[0x55ea2bc880a9]  

[0x55ea2bc84b2d]  

[0x55ea2bc8a3eb]  

[0x55ea2bc7fece]  

[0x55ea2bc7fc99]  

[0x55ea2b2ad374]  

[0x55ea2b2acd5d]  

[0x55ea2dfdadf6]  

[end of stack trace]

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 1.8 KB)
- [1.png](attachments/1.png) (image/png, 31.3 KB)

## Timeline

### [Deleted User] (2023-03-20)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-03-20)

bisect 
when repro it, only need "--harmony-struct" in loop. 
the bug was introduced in commit 31e17fe62d59968f6f89f5c33eaf8fa75d375b77
    [shared-struct, api] Support shared isolates in API

with need "--harmony-struct", acitive release: M113/dev, M112/beta, M111/stable

bug details 
when `FlatStringReader::Get` try to get a char from heap which saved a string need simplify, the heap seem be clear or freed, then lead to egmentation fault [1]
```
Char FlatStringReader::Get(int index) const {
  DCHECK_EQ(is_one_byte_, sizeof(Char) == 1);
  DCHECK(0 <= index && index < length_);
  if (sizeof(Char) == 1) {
    return static_cast<Char>(static_cast<const uint8_t*>(start_)[index]);    <----------------------
  } else {
    return static_cast<Char>(static_cast<const base::uc16*>(start_)[index]);
  }
}
```


*RAX  0x307a0020aca0 ◂— 0x0
*RBX  0x7feb403d61a0 ◂— push rbp
*RCX  0x1d5
*RDX  0x7feb3ea18ffa ◂— 'is_one_byte_ == sizeof(Char) == 1'
*RDI  0x1
*RSI  0x1
 R8   0x0
*R9   0x19eed9
*R10  0x7ffc747e8090
*R11  0x3293c802
*R12  0x307a0038373d ◂— 0xf100000230003837 /* '78' */
*R13  0x7feaac000c00 —▸ 0x307a00348e55 ◂— 0x1900000f6d00000d /* '\r' */
*R14  0x307a00000000 ◂— 0x40000
*R15  0x7feab3789ab8 —▸ 0x307a00000251 ◂— 0x1
*RBP  0x7feab37893a0 —▸ 0x7feab3789490 —▸ 0x7feab3789500 —▸ 0x7feab37897a0 —▸ 0x7feab37897e0 ◂— ...
*RSP  0x7feab3789370 ◂— 0x100307a002c2b41 /* 'A+,' */
*RIP  0x7feb40c32c40 ◂— movzx eax, byte ptr [rax + rcx]
──────────────────────────────────────[ DISASM / x86-64 / set emulate on ]───────────────────────────────────────
 ► 0x7feb40c32c40    movzx  eax, byte ptr [rax + rcx]
   0x7feb40c32c44    add    rsp, 0x30
   0x7feb40c32c48    pop    rbp
   0x7feb40c32c49    ret  







[1] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/json/json-stringifier.cc;l=1038;drc=d3544ce00be672faabb91316e81272cbf22478e2?q=json-stringifier.cc


### wh...@gmail.com (2023-03-20)

BTW, when need arguments to trigger bug, may I need find active releases or not?

### wh...@gmail.com (2023-03-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-03-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5389649258938368.

### cl...@chromium.org (2023-03-20)

[Empty comment from Monorail migration]

### hc...@google.com (2023-03-22)

V8 issue, verwaest@ I think you're the right person to take a look?

[Monorail components: Blink>JavaScript>API]

### cl...@chromium.org (2023-03-22)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Runtime]

### cl...@chromium.org (2023-03-22)

Detailed Report: https://clusterfuzz.com/testcase?key=5389649258938368

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7e26002056a5
Crash State:
  void v8::internal::JsonStringifier::SerializeString_<unsigned char, unsigned cha
  v8::internal::JsonStringifier::SerializeString
  v8::internal::JsonStringifier::Result v8::internal::JsonStringifier::Serialize_<
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=86573:86574

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5389649258938368

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### wh...@gmail.com (2023-03-23)

sorry,  update bisect 

the bug was introduced in commit f8eebf33656666990ea29e9b788080757e94413a
[heap] Enable --shared-space by default


### wh...@gmail.com (2023-03-23)

and at commit 87707ee76946c742225769d257c9b6fdb17e9c22

    [heap] Remove --shared-space flag
    
    Since --shared-space is now enabled by default, the flag can be
    removed and we can assume it is enabled unconditionally.
    
    This CL removes the command line flag and dead code resulting from
    this. Behavior shouldn't change.
    


### wh...@gmail.com (2023-03-23)

when I'm using  84144 ( https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-84144.zip?generation=1667996261945861&alt=media ) , run d8 with --harmony-struct --shared-space poc.js

will get this
#
# Fatal error in ../../src/heap/scavenger-inl.h, line 186
# Debug check failed: heap()->non_atomic_marking_state()->IsWhite(target).
#
#

#2  0x00007f35e508de65 in v8::base::(anonymous namespace)::DefaultDcheckHandler(char const*, int, char const*) () at ../../src/base/logging.cc:57
#3  0x00007f35e6e8b7b9 in v8::internal::CopyAndForwardResult v8::internal::Scavenger::PromoteObject<v8::internal::FullHeapObjectSlot, (v8::internal::Scavenger::PromotionHeapChoice)1>(v8::internal::Map, v8::internal::FullHeapObjectSlot, v8::internal::HeapObject, int, v8::internal::ObjectFields) () at ../../src/heap/scavenger-inl.h:186
#4  0x00007f35e6e8b076 in heap::base::SlotCallbackResult v8::internal::Scavenger::EvacuateObjectDefault<v8::internal::FullHeapObjectSlot, (v8::internal::Scavenger::PromotionHeapChoice)1>(v8::internal::Map, v8::internal::FullHeapObjectSlot, v8::internal::HeapObject, int, v8::internal::ObjectFields) () at ../../src/heap/scavenger-inl.h:270
#5  0x00007f35e6e8a349 in heap::base::SlotCallbackResult v8::internal::Scavenger::EvacuateObject<v8::internal::FullHeapObjectSlot>(v8::internal::FullHeapObjectSlot, v8::internal::Map, v8::internal::HeapObject) () at ../../src/heap/scavenger-inl.h:393
#6  0x00007f35e6e7748b in heap::base::SlotCallbackResult v8::internal::Scavenger::ScavengeObject<v8::internal::FullHeapObjectSlot>(v8::internal::FullHeapObjectSlot, v8::internal::HeapObject) () at ../../src/heap/scavenger-inl.h:440
#7  0x00007f35e6e773ab in v8::internal::RootScavengeVisitor::VisitRootPointers(v8::internal::Root, char const*, v8::internal::FullObjectSlot, v8::internal::FullObjectSlot) () at ../../src/heap/scavenger.cc:892
#8  0x00007f35e68048c6 in v8::internal::HandleScopeImplementer::IterateThis(v8::internal::RootVisitor*) () at ../../src/api/api.cc:10757
warning: Could not find DWO CU obj/v8_base_without_compiler/heap.dwo(0x2dbce3ec1f856f7e) referenced by CU at offset 0x2318 [in module /home/uuu/tmp/d8-linux-debug-v8-component-84144/libv8.so]
#9  0x00007f35e6d820cd in v8::internal::Heap::IterateRoots(v8::internal::RootVisitor*, v8::base::EnumSet<v8::internal::SkipRoot, int>) () at ../../src/heap/heap.cc:4714
#10 0x00007f35e6e7352f in v8::internal::ScavengerCollector::CollectGarbage() () at ../../src/heap/scavenger.cc:382
#11 0x00007f35e6d7b7f7 in v8::internal::Heap::Scavenge() () at ../../src/heap/heap.cc:2664
#12 0x00007f35e6d77bcb in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*) () at ../../src/heap/heap.cc:2223
#13 0x00007f35e6d751f3 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) () at ../../src/heap/heap.cc:1706
#14 0x00007f35e6d8066f in v8::internal::Heap::AllocateExternalBackingStore(std::Cr::function<void* (unsigned long)> const&, unsigned long) () at ../../src/heap/heap.cc:3097
warning: Could not find DWO CU obj/v8_base_without_compiler/backing-store.dwo(0x20f945b926b75fd1) referenced by CU at offset 0x3200 [in module /home/uuu/tmp/d8-linux-debug-v8-component-84144/libv8.so]
#15 0x00007f35e6ff38ac in v8::internal::BackingStore::Allocate(v8::internal::Isolate*, unsigned long, v8::internal::SharedFlag, v8::internal::InitializedFlag) () at ../../src/objects/backing-store.cc:269
warning: Could not find DWO CU obj/v8_base_without_compiler/builtins-arraybuffer.dwo(0x6bebeac5d5b4da7f) referenced by CU at offset 0x40c [in module /home/uuu/tmp/d8-linux-debug-v8-component-84144/libv8.so]
#16 0x00007f35e68d2898 in v8::internal::(anonymous namespace)::ConstructBuffer(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::JSReceiver>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, v8::internal::InitializedFlag) () at ../../src/builtins/builtins-arraybuffer.cc:70
#17 0x00007f35e68cee18 in v8::internal::Builtin_Impl_ArrayBufferConstructor(v8::internal::BuiltinArguments, v8::internal::Isolate*) () at ../../src/builtins/builtins-arraybuffer.cc:152
#18 0x00007f35e68ce377 in v8::internal::Builtin_ArrayBufferConstructor(int, unsigned long*, v8::internal::Isolate*) () at ../../src/builtins/builtins-arraybuffer.cc:116


more bug details later.

### is...@chromium.org (2023-03-23)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-03-23)

AND more bug details after https://crbug.com/chromium/1425769#c2

when d8 perform gc `Heap::PerformGarbageCollection`,  json object in young generate heap 
```
void RootScavengeVisitor::ScavengePointer(FullObjectSlot p) {
  Object object = *p;
  DCHECK(!HasWeakHeapObjectTag(object));
  DCHECK(!MapWord::IsPacked(object.ptr()));
  if (Heap::InYoungGeneration(object)) {
    scavenger_->ScavengeObject(FullHeapObjectSlot(p), HeapObject::cast(object));      <------- [1]
  }
}
```

```
SlotCallbackResult Scavenger::EvacuateObject(THeapObjectSlot slot, Map map,
                                             HeapObject source) {
  static_assert(std::is_same<THeapObjectSlot, FullHeapObjectSlot>::value ||
                    std::is_same<THeapObjectSlot, HeapObjectSlot>::value,
                "Only FullHeapObjectSlot and HeapObjectSlot are expected here");
...
    case kVisitSeqOneByteString:
    case kVisitSeqTwoByteString:
      DCHECK(String::IsInPlaceInternalizable(map.instance_type()));
      return EvacuateInPlaceInternalizableString(                                 <------------ ]2]
          map, slot, String::unchecked_cast(source), size,
          ObjectFields::kMaybePointers);
...
```

```
template <typename THeapObjectSlot,
          Scavenger::PromotionHeapChoice promotion_heap_choice>
CopyAndForwardResult Scavenger::PromoteObject(Map map, THeapObjectSlot slot,
                                              HeapObject object,
                                              int object_size,
                                              ObjectFields object_fields) {
  static_assert(std::is_same<THeapObjectSlot, FullHeapObjectSlot>::value ||
                    std::is_same<THeapObjectSlot, HeapObjectSlot>::value,
                "Only FullHeapObjectSlot and HeapObjectSlot are expected here");
  DCHECK_GE(object_size, Heap::kMinObjectSizeInTaggedWords * kTaggedSize);
  AllocationAlignment alignment = HeapObject::RequiredAlignment(map);
  AllocationResult allocation;
  switch (promotion_heap_choice) {
    case kPromoteIntoLocalHeap:
      allocation = allocator_.Allocate(OLD_SPACE, object_size,
                                       AllocationOrigin::kGC, alignment);
      break;
    case kPromoteIntoSharedHeap:
      DCHECK_NOT_NULL(shared_old_allocator_);
      allocation = shared_old_allocator_->AllocateRaw(object_size, alignment,         <-------  [3]
                                                      AllocationOrigin::kGC);
      break;
  }

  HeapObject target;
  if (allocation.To(&target)) {
    DCHECK(heap()->non_atomic_marking_state()->IsWhite(target));                <--------
    const bool self_success =
        MigrateObject(map, object, target, object_size, promotion_heap_choice);
    if (!self_success) {
...
```
the allocation heap seems have the mark bit clearer

[1] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/scavenger.cc;l=913?q=heap%2Fscavenger.cc&ss=chromium%2Fchromium%2Fsrc
[2] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:v8/src/heap/scavenger-inl.h;l=396;drc=2450f2f5d0ce0da9b8cf493c533f9528ff17bab6
[3] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:v8/src/heap/scavenger-inl.h;l=175;drc=2450f2f5d0ce0da9b8cf493c533f9528ff17bab6

### is...@chromium.org (2023-03-23)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>GarbageCollection]

### ml...@chromium.org (2023-03-23)

I am not sure this holds anymore. Allocating in a shared space may mean allocating in a space where a different Isolate performs GC at that moment which means black allocation could be enabled.

### di...@chromium.org (2023-03-23)

This feature isn't enabled at that point, so setting security impact to none. I believe the DCHECK failure up there is a red herring as this fails in a commit from November when --shared-space still had multiple bugs with incremental marking.

### di...@chromium.org (2023-03-23)

[Empty comment from Monorail migration]

### di...@chromium.org (2023-03-23)

Not yet sure whether this bug really only affects --harmony-struct, so setting security impact back for now.

### di...@chromium.org (2023-03-23)

[Empty comment from Monorail migration]

### di...@chromium.org (2023-03-23)

This doesn't affect production because this can only ever happen with --harmony-struct.

### wh...@gmail.com (2023-03-24)

Re https://crbug.com/chromium/1425769#c17 

I tested  
- 84721 ( https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-84721.zip?generation=1670496350524525&alt=media)
   result is   
#
# Fatal error in ../../src/heap/scavenger-inl.h, line 186
# Debug check failed: heap()->non_atomic_marking_state()->IsWhite(target).
#

and 84722 ( https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-84722.zip?generation=1670497634188660&alt=media) 
result is SEGV_ACCERR, the stack trace is same to https://crbug.com/chromium/1425769#c0

at 84722 d8 which commit is f5f735b10d64f9fff36600b00ce508eab2c9e64c 
[heap] Disable black allocation in shared heap during client GC

A scavenger GC can run on a client isolate while incremental marking
is enabled in the shared space isolate. While we pause black
allocation in the client's heap, we can't really pause it in the
shared heap isolate.

This CL solves that by marking ConcurrentAllocator instances created
for the GC. Black allocation is never enabled during GC. This will
probably also be useful when moving LABs out of the spaces.


### gi...@appspot.gserviceaccount.com (2023-03-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/71397d60962e094dabcc0710302fd2989e04b1fb

commit 71397d60962e094dabcc0710302fd2989e04b1fb
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Thu Mar 23 16:10:49 2023

[heap] Run relocatable callbacks for client isolates

With shared heap we need to run these callbacks in a shared GC not
only for the main isolate but also the client isolates.

This is e.g. needed when running JsonStringifier on a worker isolate.
FlatStringReader might register a Relocatable callback for a shared
space string on its own isolate. When a shared GC then happens while
the FlatStringReader is still active, the shared GC also needs to
invoke the callback for this particular worker isolate.

Bug: v8:13267, chromium:1425769
Change-Id: I7d88e234139ba8aa2053e05add15351f946badd3
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4365864
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#86678}

[modify] https://crrev.com/71397d60962e094dabcc0710302fd2989e04b1fb/src/heap/heap.cc


### di...@chromium.org (2023-03-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-03-24)

ClusterFuzz testcase 5389649258938368 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=86677:86678

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-03-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-29)

Thank you for the report. This issue is specific to --harmony-struct which is specific to the V8 experimental configuration and is not eligible for a VRP reward. [1]

[1] https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules#scope-of-program



### wh...@gmail.com (2023-03-30)

@amyressler 
Hi, as I know that --harmony-struct which is marked as experimental. However, the issue can also be reproduced with for example --shared-string-table (because --harmony-struct implies --shared-string-table) so the issue also affected non-experimental configurations.

with https://crbug.com/chromium/1425769#c22, I tested 84722 and 84721, please check it and reassess.



### pt...@chromium.org (2023-03-30)

To clarify the non-experimental state of --shared-string-table:
While --harmony-struct implies --shared-string-table and --harmony-struct is considered experimental, --shared-string-table is considered ready and we are happy about external reports.
Bugs that only require --shared-string-table (without --harmony-struct) should be considered for VRP rewards.


### wh...@gmail.com (2023-04-04)

ping ? 

### wh...@gmail.com (2023-04-17)

any update about reward?

### wh...@gmail.com (2023-04-18)

@amyressler
will you reassess it ? 

### le...@chromium.org (2023-04-18)

+amyressler in cc

### am...@google.com (2023-04-18)

[Comment Deleted]

### am...@chromium.org (2023-04-18)

Thanks for cc'ing me leszeks@
Apologies for the delay in response as I was not actively monitoring this issue. 
Yes, we can reassess this issue for a potential VRP reward.

### am...@chromium.org (2023-04-20)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-20)

Congratulations! The VRP Panel has decided to award you $8,000 for this report + bisect bonus. Thank you for your efforts and reporting this issue to us.

### wh...@gmail.com (2023-04-20)

Thanks

### am...@google.com (2023-04-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-12-21)

Hello -- we consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), even when included in comments, so I have undeleted comments. Thank you.

### is...@google.com (2023-12-21)

This issue was migrated from crbug.com/chromium/1425769?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>API, Blink>JavaScript>GarbageCollection, Blink>JavaScript>Runtime]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063673)*

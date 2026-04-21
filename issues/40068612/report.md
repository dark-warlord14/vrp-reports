# Security: Type cast failed in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [40068612](https://issues.chromium.org/issues/40068612) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Runtime |
| **Platforms** | Linux |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2023-08-03 |
| **Bounty** | $7,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 88579
    - link: https://crrev.com/3b71a8a1e98b69f9255665cff5927b8d4de38c80 
- Commit Message

```
commit 3b71a8a1e98b69f9255665cff5927b8d4de38c80
Author: Olivier Flückiger <olivf@chromium.org>
Date:   Fri Jun 30 14:00:26 2023 +0200

    Reland "[maglev-osr] Always do an entry stack check"
    
    This is a reland of commit 0e8865fd08cf3322e8b19e4e283f7faf507d17cc
    
    Issue that caused revert fixed in 4660765
    
    Original change's description:
    > [maglev-osr] Always do an entry stack check
    >
    > Even without growing the frame for OSR the stack check can fail since
    > OSR skipps the stack check that would be done by jump loop.
    >
    > Bug: chromium:1458337
    > Bug: v8:7700
    > Change-Id: Ie94d9fbf5ef978d6535c1545216b346623627284
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4650872
    > Auto-Submit: Olivier Flückiger <olivf@chromium.org>
    > Commit-Queue: Leszek Swirski <leszeks@chromium.org>
    > Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#88579}
    
    Bug: chromium:1458337
    Bug: v8:7700
    Change-Id: I4643a4ddeeeba2121b2a89a30bebd9a010852815
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4660841
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Commit-Queue: Olivier Flückiger <olivf@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#88593}

commit ff52a5936d6374fcc3780bb5a813d1a263429b0c
Author: Leszek Swirski <leszeks@chromium.org>
Date:   Fri Jun 30 10:51:45 2023 +0000

    Revert "[maglev-osr] Always do an entry stack check"
    
    This reverts commit 0e8865fd08cf3322e8b19e4e283f7faf507d17cc.
    
    Reason for revert: Breaks an arm test: https://logs.chromium.org/logs/v8/buildbucket/cr-buildbucket/8776871992585522529/+/u/Check_-_armv8-a/date-parse
    
    Original change's description:
    > [maglev-osr] Always do an entry stack check
    >
    > Even without growing the frame for OSR the stack check can fail since
    > OSR skipps the stack check that would be done by jump loop.
    >
    > Bug: chromium:1458337
    > Bug: v8:7700
    > Change-Id: Ie94d9fbf5ef978d6535c1545216b346623627284
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4650872
    > Auto-Submit: Olivier Flückiger <olivf@chromium.org>
    > Commit-Queue: Leszek Swirski <leszeks@chromium.org>
    > Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#88579}
    
    Bug: chromium:1458337
    Bug: v8:7700
    Change-Id: I24b524620b27c9ad263bfda90625b93c8ae95f2f
    No-Presubmit: true
    No-Tree-Checks: true
    No-Try: true
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4660763
    Auto-Submit: Leszek Swirski <leszeks@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#88584}

commit 0e8865fd08cf3322e8b19e4e283f7faf507d17cc
Author: Olivier Flückiger <olivf@chromium.org>
Date:   Thu Jun 29 17:22:56 2023 +0200

    [maglev-osr] Always do an entry stack check
    
    Even without growing the frame for OSR the stack check can fail since
    OSR skipps the stack check that would be done by jump loop.
    
    Bug: chromium:1458337
    Bug: v8:7700
    Change-Id: Ie94d9fbf5ef978d6535c1545216b346623627284
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4650872
    Auto-Submit: Olivier Flückiger <olivf@chromium.org>
    Commit-Queue: Leszek Swirski <leszeks@chromium.org>
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#88579}

```

## CRASH LOG1
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-89298/d8 --jit-fuzzing --stress-gc-during-compilation --lazy-new-space-shrinking --maglev poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/objects/object-type.cc, line 82
# Type cast failed in CAST(GetAccumulator()) at ../../src/interpreter/interpreter-generator.cc:839
  Expected Context but found 0x25ca00005c89: [Oddball] in ReadOnlySpace: #optimized_out

#
#
#
#FailureMessage Object: 0x7fff566e4c30
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-89298/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f008dff45e3]
    /tmp/d8-linux-debug-v8-component-89298/libv8_libplatform.so(+0x19bcd) [0x7f008df9abcd]
    /tmp/d8-linux-debug-v8-component-89298/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7f008dfd42a4]
    /tmp/d8-linux-debug-v8-component-89298/libv8.so(bool v8::internal::IsHeapObject<(v8::internal::HeapObjectReferenceType)1, unsigned long>(v8::internal::TaggedImpl<(v8::internal::HeapObjectReferenceType)1, unsigned long>)+0) [0x7f0090af4850]
    /tmp/d8-linux-debug-v8-component-89298/libv8.so(+0x1ae5c9c) [0x7f008fae5c9c]

```

## CRASH LOG2
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-89298/d8 --jit-fuzzing --stress-gc-during-compilation --lazy-new-space-shrinking --maglev poc.js
# OUTPUT ==============================================================
Stacktrace:
    ptr1=0x2bc000005c89
    ptr2=(nil)
    ptr3=(nil)
    ptr4=(nil)
    ptr5=(nil)
    ptr6=(nil)
    failure_message_object=0x7ffc9fdbc998

==== JS stack trace =========================================

    0: ExitFrame [pc: 0x7f3a1efa18bd]
    1: StubFrame [pc: 0x7f3a1f52454f]
    2: f0 [0x2bc00099b965] [poc1.js:8] [bytecode=0x2bc00099ba89 offset=122](this=0x2bc000983bd5 <JSGlobalProxy>)
    3: /* anonymous */ [0x2bc00099b8f1] [poc1.js:12] [bytecode=0x2bc00099b8ad offset=15](this=0x2bc000983bd5 <JSGlobalProxy>)
    4: InternalFrame [pc: 0x7f3a1ebc0d5c]
    5: EntryFrame [pc: 0x7f3a1ebc0a87]

==== Details ================================================

[0]: ExitFrame [pc: 0x7f3a1efa18bd]
[1]: StubFrame [pc: 0x7f3a1f52454f]
[2]: f0 [0x2bc00099b965] [poc1.js:8] [bytecode=0x2bc00099ba89 offset=122](this=0x2bc000983bd5 <JSGlobalProxy>) {
  // expression stack (top to bottom)
  [07] : 0x2bc000005c89 <Odd Oddball: optimized_out>
  [06] : 0x2bc000005c89 <Odd Oddball: optimized_out>
  [05] : 0x2bc000005c89 <Odd Oddball: optimized_out>
  [04] : 0x2bc000005c89 <Odd Oddball: optimized_out>
  [03] : 0x2bc000005c89 <Odd Oddball: optimized_out>
  [02] : 0x2bc000005c89 <Odd Oddball: optimized_out>
  [01] : 0x2bc000005c89 <Odd Oddball: optimized_out>
  [00] : 0x2bc000005c89 <Odd Oddball: optimized_out>
--------- s o u r c e   c o d e ---------
function f0() {\x0a  try {\x0a    if (test == 1) Object.defineProperty(random(496670), random1(random(496670), 253242), {\x0a      value: random(613915)\x0a    });\x0a  } catch (v2) { }\x0a  while (true) {\x0a    constructor.prototype = 42;\x0a    new WeakRef([,]);\x0a  }\x0a}
-----------------------------------------
}

[3]: /* anonymous */ [0x2bc00099b8f1] [poc1.js:12] [bytecode=0x2bc00099b8ad offset=15](this=0x2bc000983bd5 <JSGlobalProxy>) {
  // expression stack (top to bottom)
  [03] : 0x2bc000983bd5 <JSGlobalProxy>
  [02] : 0x2bc00099b8f1 <JSFunction (sfi = 0x2bc00099b805)>
  [01] : 0x2bc00099b965 <JSFunction f0 (sfi = 0x2bc00099b861)>
  [00] : 0x2bc000000251 <undefined>
--------- s o u r c e   c o d e ---------
function f0() {\x0a  try {\x0a    if (test == 1) Object.defineProperty(random(496670), random1(random(496670), 253242), {\x0a      value: random(613915)\x0a    });\x0a  } catch (v2) { }\x0a  while (true) {\x0a    constructor.prototype = 42;\x0a    new WeakRef([,]);\x0a  }\x0a}\x0af0();\x0a//flags: --jit-fuzzing --stress-gc-during-comp...

-----------------------------------------
}

[4]: InternalFrame [pc: 0x7f3a1ebc0d5c]
[5]: EntryFrame [pc: 0x7f3a1ebc0a87]
=====================

pwndbg> bt
#0  0x0000555555d3d587 in v8::base::OS::Abort()::$_0::operator()() const (this=<optimized out>) at ./../../src/base/platform/platform-posix.cc:698
#1  v8::base::OS::Abort () at ./../../src/base/platform/platform-posix.cc:698
#2  0x00005555564268a5 in v8::internal::Isolate::PushStackTraceAndDie (this=<optimized out>, ptr1=<optimized out>, ptr2=<optimized out>, ptr3=<optimized out>, ptr4=<optimized out>) at ./../../src/execution/isolate.cc:660
#3  0x00005555570c913b in v8::internal::LookupIterator::GetRootForNonJSReceiver (isolate=isolate@entry=0x55555a249f60, lookup_start_object=..., index=index@entry=18446744073709551615, configuration=configuration@entry=v8::internal::LookupIterator::PROTOTYPE_CHAIN) at ./../../src/objects/lookup.cc:158
#4  0x00005555570c6548 in v8::internal::LookupIterator::GetRoot (isolate=0x55555a249f60, lookup_start_object=..., index=18446744073709551615, configuration=v8::internal::LookupIterator::PROTOTYPE_CHAIN) at ../../src/objects/lookup-inl.h:334
#5  0x00005555570c6953 in v8::internal::LookupIterator::Start<false> (this=0x7fffffffcb50) at ./../../src/objects/lookup.cc:49
#6  0x0000555555dffaec in v8::internal::LookupIterator::LookupIterator (this=0x7fffffffcb50, isolate=0x55555a249f60, receiver=..., name=..., index=<optimized out>, lookup_start_object=..., configuration=v8::internal::LookupIterator::PROTOTYPE_CHAIN) at ../../src/objects/lookup-inl.h:111
#7  0x0000555556e838fb in v8::internal::LookupIterator::LookupIterator (this=0x7fffffffcb50, isolate=0x7fffffff27e0, isolate@entry=0x55555a249f60, receiver=..., receiver@entry=..., key=..., configuration=1511235008) at ../../src/objects/lookup-inl.h:55
#8  v8::internal::StoreIC::Store (this=this@entry=0x7fffffffcc38, object=..., name=..., value=value@entry=..., store_origin=store_origin@entry=v8::internal::StoreOrigin::kNamed) at ./../../src/ic/ic.cc:1779
#9  0x0000555556e9a7ec in v8::internal::__RT_impl_Runtime_StoreIC_Miss (args=..., isolate=isolate@entry=0x55555a249f60) at ./../../src/ic/ic.cc:2818
#10 0x0000555556e999fc in v8::internal::Runtime_StoreIC_Miss (args_length=<optimized out>, args_object=0x7fffffffce00, isolate=0x55555a249f60) at ./../../src/ic/ic.cc:2791
#11 0x0000555559451ab6 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit ()
#12 0x0000555559568549 in Builtins_SetNamedPropertyHandler ()
#13 0x00005555593a4164 in Builtins_InterpreterEntryTrampoline ()
#14 0x0000235700005c89 in ?? ()
#15 0x0000235700005c89 in ?? ()
#16 0x0000235700005c89 in ?? ()
#17 0x0000235700005c89 in ?? ()
#18 0x0000235700005c89 in ?? ()
#19 0x0000235700005c89 in ?? ()
#20 0x0000235700005c89 in ?? ()
#21 0x0000235700005c89 in ?? ()
#22 0x0000000000000132 in ?? ()
#23 0x000023570095ba89 in ?? ()
#24 0x0000000000000001 in ?? ()
#25 0x000023570095b965 in ?? ()
#26 0x0000235700943c0d in ?? ()
#27 0x00007fffffffcef8 in ?? ()
#28 0x00005555593a4164 in Builtins_InterpreterEntryTrampoline ()
#29 0x0000235700943bd5 in ?? ()
#30 0x000023570095b8f1 in ?? ()
#31 0x000023570095b965 in ?? ()
#32 0x0000235700000251 in ?? ()
#33 0x000000000000005c in ?? ()
#34 0x000023570095b8ad in ?? ()
#35 0x0000000000000002 in ?? ()
#36 0x000023570095b8f1 in ?? ()
#37 0x0000235700943c0d in ?? ()
#38 0x00007fffffffcf28 in ?? ()
#39 0x00005555593a179c in Builtins_JSEntryTrampoline ()
#40 0x0000235700943bd5 in ?? ()
#41 0x0000235700985bd9 in ?? ()
#42 0x000023570095b8f1 in ?? ()
#43 0x000000000000002c in ?? ()
#44 0x00007fffffffcf90 in ?? ()
#45 0x00005555593a14c7 in Builtins_JSEntry ()
```

## Other
Please note to include the flags `--jit-fuzzing --stress-gc-during-compilation --lazy-new-space-shrinking --maglev` for clusterfuzz classification.

VERSION
Tested on v8 version: 11.7.0 - 11.7.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-89298.zip
2. Run: `d8 --jit-fuzzing --stress-gc-during-compilation --lazy-new-space-shrinking --maglev poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 357 B)
- [poc1.js](attachments/poc1.js) (text/plain, 343 B)
- [poc.js](attachments/poc.js) (text/plain, 357 B)
- [poc1.js](attachments/poc1.js) (text/plain, 343 B)

## Timeline

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### ki...@gmail.com (2023-08-03)

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 88579
    - link: https://crrev.com/3b71a8a1e98b69f9255665cff5927b8d4de38c80 
- Commit Message

```
commit 3b71a8a1e98b69f9255665cff5927b8d4de38c80
Author: Olivier Flückiger <olivf@chromium.org>
Date:   Fri Jun 30 14:00:26 2023 +0200

    Reland "[maglev-osr] Always do an entry stack check"
    
    This is a reland of commit 0e8865fd08cf3322e8b19e4e283f7faf507d17cc
    
    Issue that caused revert fixed in 4660765
    
    Original change's description:
    > [maglev-osr] Always do an entry stack check
    >
    > Even without growing the frame for OSR the stack check can fail since
    > OSR skipps the stack check that would be done by jump loop.
    >
    > Bug: chromium:1458337
    > Bug: v8:7700
    > Change-Id: Ie94d9fbf5ef978d6535c1545216b346623627284
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4650872
    > Auto-Submit: Olivier Flückiger <olivf@chromium.org>
    > Commit-Queue: Leszek Swirski <leszeks@chromium.org>
    > Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#88579}
    
    Bug: chromium:1458337
    Bug: v8:7700
    Change-Id: I4643a4ddeeeba2121b2a89a30bebd9a010852815
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4660841
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Commit-Queue: Olivier Flückiger <olivf@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#88593}

commit ff52a5936d6374fcc3780bb5a813d1a263429b0c
Author: Leszek Swirski <leszeks@chromium.org>
Date:   Fri Jun 30 10:51:45 2023 +0000

    Revert "[maglev-osr] Always do an entry stack check"
    
    This reverts commit 0e8865fd08cf3322e8b19e4e283f7faf507d17cc.
    
    Reason for revert: Breaks an arm test: https://logs.chromium.org/logs/v8/buildbucket/cr-buildbucket/8776871992585522529/+/u/Check_-_armv8-a/date-parse
    
    Original change's description:
    > [maglev-osr] Always do an entry stack check
    >
    > Even without growing the frame for OSR the stack check can fail since
    > OSR skipps the stack check that would be done by jump loop.
    >
    > Bug: chromium:1458337
    > Bug: v8:7700
    > Change-Id: Ie94d9fbf5ef978d6535c1545216b346623627284
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4650872
    > Auto-Submit: Olivier Flückiger <olivf@chromium.org>
    > Commit-Queue: Leszek Swirski <leszeks@chromium.org>
    > Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#88579}
    
    Bug: chromium:1458337
    Bug: v8:7700
    Change-Id: I24b524620b27c9ad263bfda90625b93c8ae95f2f
    No-Presubmit: true
    No-Tree-Checks: true
    No-Try: true
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4660763
    Auto-Submit: Leszek Swirski <leszeks@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#88584}

commit 0e8865fd08cf3322e8b19e4e283f7faf507d17cc
Author: Olivier Flückiger <olivf@chromium.org>
Date:   Thu Jun 29 17:22:56 2023 +0200

    [maglev-osr] Always do an entry stack check
    
    Even without growing the frame for OSR the stack check can fail since
    OSR skipps the stack check that would be done by jump loop.
    
    Bug: chromium:1458337
    Bug: v8:7700
    Change-Id: Ie94d9fbf5ef978d6535c1545216b346623627284
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4650872
    Auto-Submit: Olivier Flückiger <olivf@chromium.org>
    Commit-Queue: Leszek Swirski <leszeks@chromium.org>
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#88579}

```

## CRASH LOG1
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-89298/d8 --jit-fuzzing --stress-gc-during-compilation --lazy-new-space-shrinking --maglev poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/objects/object-type.cc, line 82
# Type cast failed in CAST(GetAccumulator()) at ../../src/interpreter/interpreter-generator.cc:839
  Expected Context but found 0x25ca00005c89: [Oddball] in ReadOnlySpace: #optimized_out

#
#
#
#FailureMessage Object: 0x7fff566e4c30
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-89298/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f008dff45e3]
    /tmp/d8-linux-debug-v8-component-89298/libv8_libplatform.so(+0x19bcd) [0x7f008df9abcd]
    /tmp/d8-linux-debug-v8-component-89298/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7f008dfd42a4]
    /tmp/d8-linux-debug-v8-component-89298/libv8.so(bool v8::internal::IsHeapObject<(v8::internal::HeapObjectReferenceType)1, unsigned long>(v8::internal::TaggedImpl<(v8::internal::HeapObjectReferenceType)1, unsigned long>)+0) [0x7f0090af4850]
    /tmp/d8-linux-debug-v8-component-89298/libv8.so(+0x1ae5c9c) [0x7f008fae5c9c]

```

## CRASH LOG2
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-89298/d8 --jit-fuzzing --stress-gc-during-compilation --lazy-new-space-shrinking --maglev poc.js
# OUTPUT ==============================================================
Stacktrace:
    ptr1=0x2bc000005c89
    ptr2=(nil)
    ptr3=(nil)
    ptr4=(nil)
    ptr5=(nil)
    ptr6=(nil)
    failure_message_object=0x7ffc9fdbc998

==== JS stack trace =========================================

    0: ExitFrame [pc: 0x7f3a1efa18bd]
    1: StubFrame [pc: 0x7f3a1f52454f]
    2: f0 [0x2bc00099b965] [poc1.js:8] [bytecode=0x2bc00099ba89 offset=122](this=0x2bc000983bd5 <JSGlobalProxy>)
    3: /* anonymous */ [0x2bc00099b8f1] [poc1.js:12] [bytecode=0x2bc00099b8ad offset=15](this=0x2bc000983bd5 <JSGlobalProxy>)
    4: InternalFrame [pc: 0x7f3a1ebc0d5c]
    5: EntryFrame [pc: 0x7f3a1ebc0a87]

==== Details ================================================

[0]: ExitFrame [pc: 0x7f3a1efa18bd]
[1]: StubFrame [pc: 0x7f3a1f52454f]
[2]: f0 [0x2bc00099b965] [poc1.js:8] [bytecode=0x2bc00099ba89 offset=122](this=0x2bc000983bd5 <JSGlobalProxy>) {
  // expression stack (top to bottom)
  [07] : 0x2bc000005c89 <Odd Oddball: optimized_out>
  [06] : 0x2bc000005c89 <Odd Oddball: optimized_out>
  [05] : 0x2bc000005c89 <Odd Oddball: optimized_out>
  [04] : 0x2bc000005c89 <Odd Oddball: optimized_out>
  [03] : 0x2bc000005c89 <Odd Oddball: optimized_out>
  [02] : 0x2bc000005c89 <Odd Oddball: optimized_out>
  [01] : 0x2bc000005c89 <Odd Oddball: optimized_out>
  [00] : 0x2bc000005c89 <Odd Oddball: optimized_out>
--------- s o u r c e   c o d e ---------
function f0() {\x0a  try {\x0a    if (test == 1) Object.defineProperty(random(496670), random1(random(496670), 253242), {\x0a      value: random(613915)\x0a    });\x0a  } catch (v2) { }\x0a  while (true) {\x0a    constructor.prototype = 42;\x0a    new WeakRef([,]);\x0a  }\x0a}
-----------------------------------------
}

[3]: /* anonymous */ [0x2bc00099b8f1] [poc1.js:12] [bytecode=0x2bc00099b8ad offset=15](this=0x2bc000983bd5 <JSGlobalProxy>) {
  // expression stack (top to bottom)
  [03] : 0x2bc000983bd5 <JSGlobalProxy>
  [02] : 0x2bc00099b8f1 <JSFunction (sfi = 0x2bc00099b805)>
  [01] : 0x2bc00099b965 <JSFunction f0 (sfi = 0x2bc00099b861)>
  [00] : 0x2bc000000251 <undefined>
--------- s o u r c e   c o d e ---------
function f0() {\x0a  try {\x0a    if (test == 1) Object.defineProperty(random(496670), random1(random(496670), 253242), {\x0a      value: random(613915)\x0a    });\x0a  } catch (v2) { }\x0a  while (true) {\x0a    constructor.prototype = 42;\x0a    new WeakRef([,]);\x0a  }\x0a}\x0af0();\x0a//flags: --jit-fuzzing --stress-gc-during-comp...

-----------------------------------------
}

[4]: InternalFrame [pc: 0x7f3a1ebc0d5c]
[5]: EntryFrame [pc: 0x7f3a1ebc0a87]
=====================

pwndbg> bt
#0  0x0000555555d3d587 in v8::base::OS::Abort()::$_0::operator()() const (this=<optimized out>) at ./../../src/base/platform/platform-posix.cc:698
#1  v8::base::OS::Abort () at ./../../src/base/platform/platform-posix.cc:698
#2  0x00005555564268a5 in v8::internal::Isolate::PushStackTraceAndDie (this=<optimized out>, ptr1=<optimized out>, ptr2=<optimized out>, ptr3=<optimized out>, ptr4=<optimized out>) at ./../../src/execution/isolate.cc:660
#3  0x00005555570c913b in v8::internal::LookupIterator::GetRootForNonJSReceiver (isolate=isolate@entry=0x55555a249f60, lookup_start_object=..., index=index@entry=18446744073709551615, configuration=configuration@entry=v8::internal::LookupIterator::PROTOTYPE_CHAIN) at ./../../src/objects/lookup.cc:158
#4  0x00005555570c6548 in v8::internal::LookupIterator::GetRoot (isolate=0x55555a249f60, lookup_start_object=..., index=18446744073709551615, configuration=v8::internal::LookupIterator::PROTOTYPE_CHAIN) at ../../src/objects/lookup-inl.h:334
#5  0x00005555570c6953 in v8::internal::LookupIterator::Start<false> (this=0x7fffffffcb50) at ./../../src/objects/lookup.cc:49
#6  0x0000555555dffaec in v8::internal::LookupIterator::LookupIterator (this=0x7fffffffcb50, isolate=0x55555a249f60, receiver=..., name=..., index=<optimized out>, lookup_start_object=..., configuration=v8::internal::LookupIterator::PROTOTYPE_CHAIN) at ../../src/objects/lookup-inl.h:111
#7  0x0000555556e838fb in v8::internal::LookupIterator::LookupIterator (this=0x7fffffffcb50, isolate=0x7fffffff27e0, isolate@entry=0x55555a249f60, receiver=..., receiver@entry=..., key=..., configuration=1511235008) at ../../src/objects/lookup-inl.h:55
#8  v8::internal::StoreIC::Store (this=this@entry=0x7fffffffcc38, object=..., name=..., value=value@entry=..., store_origin=store_origin@entry=v8::internal::StoreOrigin::kNamed) at ./../../src/ic/ic.cc:1779
#9  0x0000555556e9a7ec in v8::internal::__RT_impl_Runtime_StoreIC_Miss (args=..., isolate=isolate@entry=0x55555a249f60) at ./../../src/ic/ic.cc:2818
#10 0x0000555556e999fc in v8::internal::Runtime_StoreIC_Miss (args_length=<optimized out>, args_object=0x7fffffffce00, isolate=0x55555a249f60) at ./../../src/ic/ic.cc:2791
#11 0x0000555559451ab6 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit ()
#12 0x0000555559568549 in Builtins_SetNamedPropertyHandler ()
#13 0x00005555593a4164 in Builtins_InterpreterEntryTrampoline ()
#14 0x0000235700005c89 in ?? ()
#15 0x0000235700005c89 in ?? ()
#16 0x0000235700005c89 in ?? ()
#17 0x0000235700005c89 in ?? ()
#18 0x0000235700005c89 in ?? ()
#19 0x0000235700005c89 in ?? ()
#20 0x0000235700005c89 in ?? ()
#21 0x0000235700005c89 in ?? ()
#22 0x0000000000000132 in ?? ()
#23 0x000023570095ba89 in ?? ()
#24 0x0000000000000001 in ?? ()
#25 0x000023570095b965 in ?? ()
#26 0x0000235700943c0d in ?? ()
#27 0x00007fffffffcef8 in ?? ()
#28 0x00005555593a4164 in Builtins_InterpreterEntryTrampoline ()
#29 0x0000235700943bd5 in ?? ()
#30 0x000023570095b8f1 in ?? ()
#31 0x000023570095b965 in ?? ()
#32 0x0000235700000251 in ?? ()
#33 0x000000000000005c in ?? ()
#34 0x000023570095b8ad in ?? ()
#35 0x0000000000000002 in ?? ()
#36 0x000023570095b8f1 in ?? ()
#37 0x0000235700943c0d in ?? ()
#38 0x00007fffffffcf28 in ?? ()
#39 0x00005555593a179c in Builtins_JSEntryTrampoline ()
#40 0x0000235700943bd5 in ?? ()
#41 0x0000235700985bd9 in ?? ()
#42 0x000023570095b8f1 in ?? ()
#43 0x000000000000002c in ?? ()
#44 0x00007fffffffcf90 in ?? ()
#45 0x00005555593a14c7 in Builtins_JSEntry ()
```

## Other
Please note to include the flags `--jit-fuzzing --stress-gc-during-compilation --lazy-new-space-shrinking --maglev` for clusterfuzz classification.

VERSION
Tested on v8 version: 11.7.0 - 11.7.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-89298.zip
2. Run: `d8 --jit-fuzzing --stress-gc-during-compilation --lazy-new-space-shrinking --maglev poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)

### cl...@chromium.org (2023-08-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5177617206149120.

### ts...@chromium.org (2023-08-03)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2023-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-08-03)

Detailed Report: https://clusterfuzz.com/testcase?key=5177617206149120

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: Fatal error
Crash Address: 
Crash State:
  Type cast failed in CAST(GetAccumulator()) at ../../src/interpreter/interpreter-
  v8::internal::CheckObjectType
  Builtins_PushContextHandler
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=89062:89063

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5177617206149120

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2023-08-03)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Runtime]

### sa...@google.com (2023-08-04)

Clusterfuzz fails at bisecting this since it removes --maglev and then just bisects to the CL that enabled maglev by default. I did a local bisect, and it also identifies 3b71a8a1e98b69f9255665cff5927b8d4de38c80 "Reland "[maglev-osr] Always do an entry stack check"" as the culprit.
The #optimized_out value is probably another internal/magic value that should not behave like an Oddball, similar to the_hole.

### sa...@google.com (2023-08-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-08-04)

ClusterFuzz testcase 5177617206149120 appears to be flaky, updating reproducibility label.

### gi...@appspot.gserviceaccount.com (2023-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/a7bc4d8c613963829e26c9eebcda0fdeeff085fa

commit a7bc4d8c613963829e26c9eebcda0fdeeff085fa
Author: Olivier Flückiger <olivf@chromium.org>
Date: Fri Aug 04 14:29:07 2023

[maglev-osr] Fix stack-check bailout position

Deoptimizer continues with the next bytecode. Thus we need the set the
position of the bailout to the current bytecode when the osr happens,
which is jumpLoop.

Bug: chromium:1469800
Change-Id: Ief8e6472340ca2a089ac856638f4c0d85b2d6f20
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4750267
Commit-Queue: Olivier Flückiger <olivf@chromium.org>
Commit-Queue: Leszek Swirski <leszeks@chromium.org>
Auto-Submit: Olivier Flückiger <olivf@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/heads/main@{#89385}

[modify] https://crrev.com/a7bc4d8c613963829e26c9eebcda0fdeeff085fa/src/maglev/maglev-graph-builder.cc


### ki...@gmail.com (2023-08-05)

Hi, saelo, Can you help determine if this is a security issue and what its security level is?

### ol...@chromium.org (2023-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-05)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-08-05)

ClusterFuzz testcase 4682033143676928 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=89384:89385

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-05)

[Empty comment from Monorail migration]

### sa...@google.com (2023-08-08)

The result of this bug would've been that after a bailout, we continue with the second bytecode of the loop body instead of the first one. This probably can lead to all sorts of badness, so setting security labels accordingly.

### ol...@chromium.org (2023-08-08)

Indeed, thanks for reporting this.

### [Deleted User] (2023-08-08)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-10)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M117. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge approved: your change passed merge requirements and is auto-approved for M117. Please go ahead and merge the CL to branch 5938 (refs/branch-heads/5938) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: harrysouders (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ol...@chromium.org (2023-08-11)

Fix landed in dev 117.0.5938.0. Why sherifbot?

### [Deleted User] (2023-08-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ol...@chromium.org (2023-08-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-14)

[Description Changed]

### wf...@chromium.org (2023-08-16)

Hi, can you complete a lightweight v8 post mortem? I think the script missed this as the sev was set to High after the fix - go/v8-security-bug-postmortem

### am...@google.com (2023-08-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-16)

Congratulations, Zhenghang Xiao! The VRP Panel has decided to award you $7000 for this report + $1000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1469800?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Runtime]
[Monorail mergedwith: crbug.com/chromium/1470267]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068612)*

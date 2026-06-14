# Security: Signal SIGSEGV in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [41493175](https://issues.chromium.org/issues/41493175) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2024-01-20 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91451
    - link: https://crrev.com/92d982471f346255af8a75024dc5f0792392436d
- Commit Message

```
commit 92d982471f346255af8a75024dc5f0792392436d
Author: Olivier Flückiger <olivf@chromium.org>
Date:   Mon Dec 11 14:16:32 2023 +0100

    [maps] Derived map cache

    Cache derived maps for reflect.construct or proxies on the prototype
    info. This ensures we have a re-usable map for every prototype+
    constructor combination.

    Bug: chromium:1492212, v8:13978
    Change-Id: I86caa5bc4277db730bf19fdb31f9092173d27c2b
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4943950
    Reviewed-by: Toon Verwaest <verwaest@chromium.org>
    Commit-Queue: Olivier Flückiger <olivf@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91451}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91931/d8 --allow-natives-syntax --jit-fuzzing --optimize-for-size --stress-concurrent-allocation poc.js
# OUTPUT ==============================================================
Received signal 11 SEGV_ACCERR 0667009c0008

==== C stack trace ===============================

 [0x7fe8739f4a83]
 [0x7fe8739f49d2]
 [0x7fe873042520]
 [0x7fe876b7a91c]
 [0x7fe876a3c073]
 [0x7fe876a3b42d]
 [0x7fe8768d24c7]
 [0x7fe875ec455b]
 [0x7fe875ec408f]
 [0x7fe87556adbd]
[end of stack trace]

```

## Other
Please note to include the flags `--allow-natives-syntax --jit-fuzzing --optimize-for-size --stress-concurrent-allocation` for clusterfuzz classification.
The POC is unstable and need to retry for 50-200 times.

VERSION
Tested on v8 version: 12.2.0 - 12.2.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-91931.zip
2. Run: `d8 --allow-natives-syntax --jit-fuzzing --optimize-for-size --stress-concurrent-allocation poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)

If you cannot reproduce it on the release version, please use the following args.gn to reproduce it. I can reproduce this vulnerability within 300 times by using this args.gn on multiple different machines.

I do not recommend using clusterfuzz, because currently I have not determined the fundamental factors that affect the stability of the recurrence of this vulnerability.

In addition, since this vulnerability was introduced very early, and it should not actually require any real feature flag, it should be a stable memory corruption problem, which may cause rce.

- args.gn
```
is_debug = false
dcheck_always_on = true
v8_static_library = true
v8_enable_slow_dchecks = true
v8_enable_v8_checks = true
v8_enable_verify_heap = true
v8_enable_verify_csa = true
v8_enable_verify_predictable = true
target_cpu = "x64"

- stack trace

```
pwndbg> bt
#0  v8::internal::CheckObjectComparisonAllowed(unsigned long, unsigned long) () at ../../src/heap/heap-write-barrier-inl.h:92
#1  0x00007ffff62c1073 in v8::internal::PrototypeInfo::AddDerivedMap(v8::internal::Handle<v8::internal::PrototypeInfo>, v8::internal::Handle<v8::internal::Map>, v8::internal::Isolate*) () at ../../src/objects/tagged-impl.h:88
#2  0x00007ffff62c042d in v8::internal::Map::GetDerivedMap(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Map>, v8::internal::Handle<v8::internal::JSReceiver>) () at ../../src/objects/map.cc:938
#3  0x00007ffff61574c7 in v8::internal::JSFunction::GetDerivedMap(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::JSReceiver>) () at ../../src/objects/js-function.cc:1110
#4  0x00007ffff574955b in v8::internal::Builtin_Impl_NumberFormatConstructor(v8::internal::BuiltinArguments, v8::internal::Isolate*) () at ../../src/builtins/builtins-intl.cc:239
#5  0x00007ffff574908f in v8::internal::Builtin_NumberFormatConstructor(int, unsigned long*, v8::internal::Isolate*) () at ../../src/builtins/builtins-intl.cc:435
#6  0x00007ffff4defdbd in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit () from /home/kiprey/test/libv8.so
#7  0x00007ffff4a48e21 in Builtins_JSBuiltinsConstructStub () from /home/kiprey/test/libv8.so
#8  0x0000197000a42291 in ?? ()
#9  0x0000197000c921ed in ?? ()
#10 0x000000000000000a in ?? ()
#11 0x00001970000006e9 in ?? ()
#12 0x00001970000006e9 in ?? ()
#13 0x0051515100000002 in ?? ()
#14 0x0000197000c8a245 in ?? ()
#15 0x000000000000002e in ?? ()
#16 0x00007fffffffc958 in ?? ()
#17 0x00007ffff4a5501b in Builtins_InterpreterEntryTrampoline () from /home/kiprey/test/libv8.so
#18 0x0000197000000061 in ?? ()
#19 0x0000197000005bfd in ?? ()
#20 0x0000197000005bfd in ?? ()
#21 0x0000197000005bfd in ?? ()
#22 0x0000197000005bfd in ?? ()
#23 0x0000197000005bfd in ?? ()
#24 0x0000197000a42291 in ?? ()
#25 0x0000197000a422ed in ?? ()
#26 0x0000197000c921ed in ?? ()
#27 0x0000197000c91e9d in ?? ()
#28 0x0000197000c91ef1 in ?? ()
#29 0x0000197000a4221d in ?? ()
#30 0x0000197000a42209 in ?? ()
#31 0x0000197000005bfd in ?? ()
#32 0x0000197000005bfd in ?? ()
#33 0x0000197000005bfd in ?? ()
#34 0x0000197000005bfd in ?? ()
#35 0x0000197000005bfd in ?? ()
#36 0x0000197000ca34c1 in ?? ()
#37 0x00000000000001ac in ?? ()
#38 0x00000ae700042669 in ?? ()
#39 0x0000000000000001 in ?? ()
#40 0x0000197000ca3471 in ?? ()
#41 0x0000197000a4223d in ?? ()
#42 0x00007fffffffc9e0 in ?? ()
#43 0x00007ffff4a5501b in Builtins_InterpreterEntryTrampoline () from /home/kiprey/test/libv8.so
#44 0x0000197000c8a1e9 in ?? ()
#45 0x0000197000c82841 in ?? ()
#46 0x0000197000c82851 in ?? ()
#47 0x0000197000c8a1e9 in ?? ()
#48 0x0000197000c82871 in ?? ()
#49 0x0000197000c8a1e9 in ?? ()
#50 0x0000197000ca3471 in ?? ()
#51 0x0000197000c82841 in ?? ()
#52 0x0000197000000061 in ?? ()
#53 0x0000197000ca24d1 in ?? ()
#54 0x000000000000073e in ?? ()
#55 0x00000ae700042259 in ?? ()
#56 0x0000000000000001 in ?? ()
#57 0x0000197000ca20b5 in ?? ()
#58 0x0000197000ca27f1 in ?? ()
#59 0x00007fffffffca08 in ?? ()
#60 0x00007ffff4a4bfdc in Builtins_JSEntryTrampoline () from /home/kiprey/test/libv8.so
#61 0x0000197000c8a1e9 in ?? ()
#62 0x0000197000ca20b5 in ?? ()
#63 0x000000000000002c in ?? ()
#64 0x00007fffffffca70 in ?? ()
#65 0x00007ffff4a4bd07 in Builtins_JSEntry () from /home/kiprey/test/libv8.so
Backtrace stopped: previous frame inner to this frame (corrupt stack?)


PrototypeInfo::AddDerivedMap will compare *bigger and *derived [0], but since one of them is a stale pointer, this will lead to triggering a segment fault at [2] when performing the SLOW_DCHECK comparison [1]. 

The failure of SLOW_DCHECK can indicate a specific impact, suggesting that there might be some potential UAF (Use After Free) issues here.

void PrototypeInfo::AddDerivedMap(Handle<PrototypeInfo> info, Handle<Map> to,
                                  Isolate* isolate) {
  if (IsUndefined(info->derived_maps())) {
    // Index 0 is the map for object create
    Tagged<WeakArrayList> derived = *isolate->factory()->NewWeakArrayList(2);
    // GetConstructMap assumes a weak pointer.
    derived->Set(0, HeapObjectReference::ClearedValue(isolate));
    derived->Set(1, HeapObjectReference::Weak(*to));
    derived->set_length(2);
    info->set_derived_maps(derived, kReleaseStore);
    return;
  }
  auto derived = Tagged<WeakArrayList>::cast(info->derived_maps());
  // Index 0 is the map for object create
  int i = 1;
  for (; i < derived->length(); ++i) {
    MaybeObject el = derived->Get(i);
    if (el.IsCleared()) {
      derived->Set(i, HeapObjectReference::Weak(*to));
      return;
    }
  }

  auto bigger =
      WeakArrayList::EnsureSpace(isolate, handle(derived, isolate), i + 1);
  bigger->Set(i, HeapObjectReference::Weak(*to));
  bigger->set_length(i + 1);
  if (*bigger != *derived) { //-------> [0]
    info->set_derived_maps(*bigger, kReleaseStore);
  }
}

```
  // Don't use this operator for comparing with stale or invalid pointers
  // because CheckObjectComparisonAllowed() might crash when trying to access
  // the object's page header. Use SafeEquals() instead.
  template <typename U>
  constexpr bool operator!=(TaggedImpl<kRefType, U> other) const {
    static_assert(
        std::is_same<U, Address>::value || std::is_same<U, Tagged_t>::value,
        "U must be either Address or Tagged_t");
#ifdef V8_EXTERNAL_CODE_SPACE
    // When comparing two full pointer values ensure that it's allowed.
    if (std::is_same<StorageType, Address>::value &&
        std::is_same<U, Address>::value) {
      SLOW_DCHECK(CheckObjectComparisonAllowed(ptr_, other.ptr())); //-------> [1]
    }
#endif  // V8_EXTERNAL_CODE_SPACE
    return static_cast<Tagged_t>(ptr_) != static_cast<Tagged_t>(other.ptr());
  }
```


```
#ifdef V8_EXTERNAL_CODE_SPACE
bool CheckObjectComparisonAllowed(Address a, Address b) {
  if (!HAS_STRONG_HEAP_OBJECT_TAG(a) || !HAS_STRONG_HEAP_OBJECT_TAG(b)) {
    return true;
  }
  Tagged<HeapObject> obj_a = HeapObject::unchecked_cast(Tagged<Object>(a));
  Tagged<HeapObject> obj_b = HeapObject::unchecked_cast(Tagged<Object>(b));
  // This check might fail when we try to compare objects in different pointer
  // compression cages (e.g. the one used by code space or trusted space) with
  // each other. The main legitimate case when such "mixed" comparison could
  // happen is comparing two AbstractCode objects. If that's the case one must
  // use AbstractCode's == operator instead of Object's one or SafeEquals().
  CHECK_EQ(IsCodeSpaceObject(obj_a), IsCodeSpaceObject(obj_b));
  CHECK_EQ(IsTrustedSpaceObject(obj_a), IsTrustedSpaceObject(obj_b));
  return true;
}
#endif  // V8_EXTERNAL_CODE_SPACE


V8_INLINE uintptr_t GetFlags() const {
return *reinterpret_cast<const uintptr_t*>(reinterpret_cast<Address>(this) +
                                            kFlagsOffset); //[2]
}
```

[0] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/prototype-info-inl.h;l=124;drc=3cc22c22d7637bc5604e8fef3b0882b51a762901;bpv=1;bpt=1
[1] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/tagged-impl.h;l=88;drc=3cc22c22d7637bc5604e8fef3b0882b51a762901;bpv=1;bpt=1
[2] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/heap-write-barrier-inl.h;l=92;drc=3cc22c22d7637bc5604e8fef3b0882b51a762901;bpv=1;bpt=1

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 1.5 KB)
- [poc.js](attachments/poc_53263912.js) (text/plain, 1.5 KB)

## Timeline

### ki...@gmail.com (2024-01-20)

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91451
    - link: https://crrev.com/92d982471f346255af8a75024dc5f0792392436d
- Commit Message

```
commit 92d982471f346255af8a75024dc5f0792392436d
Author: Olivier Flückiger <olivf@chromium.org>
Date:   Mon Dec 11 14:16:32 2023 +0100

    [maps] Derived map cache

    Cache derived maps for reflect.construct or proxies on the prototype
    info. This ensures we have a re-usable map for every prototype+
    constructor combination.

    Bug: chromium:1492212, v8:13978
    Change-Id: I86caa5bc4277db730bf19fdb31f9092173d27c2b
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4943950
    Reviewed-by: Toon Verwaest <verwaest@chromium.org>
    Commit-Queue: Olivier Flückiger <olivf@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91451}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91931/d8 --allow-natives-syntax --jit-fuzzing --optimize-for-size --stress-concurrent-allocation poc.js
# OUTPUT ==============================================================
Received signal 11 SEGV_ACCERR 0667009c0008

==== C stack trace ===============================

 [0x7fe8739f4a83]
 [0x7fe8739f49d2]
 [0x7fe873042520]
 [0x7fe876b7a91c]
 [0x7fe876a3c073]
 [0x7fe876a3b42d]
 [0x7fe8768d24c7]
 [0x7fe875ec455b]
 [0x7fe875ec408f]
 [0x7fe87556adbd]
[end of stack trace]

```

## Other
Please note to include the flags `--allow-natives-syntax --jit-fuzzing --optimize-for-size --stress-concurrent-allocation` for clusterfuzz classification.
The POC is unstable and need to retry for 50-200 times.

VERSION
Tested on v8 version: 12.2.0 - 12.2.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-91931.zip
2. Run: `d8 --allow-natives-syntax --jit-fuzzing --optimize-for-size --stress-concurrent-allocation poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)

### [Deleted User] (2024-01-20)

[Empty comment from Monorail migration]

### ki...@gmail.com (2024-01-20)

[Comment Deleted]

### ki...@gmail.com (2024-01-20)

- stack trace

```
pwndbg> bt
#0  v8::internal::CheckObjectComparisonAllowed(unsigned long, unsigned long) () at ../../src/heap/heap-write-barrier-inl.h:92
#1  0x00007ffff62c1073 in v8::internal::PrototypeInfo::AddDerivedMap(v8::internal::Handle<v8::internal::PrototypeInfo>, v8::internal::Handle<v8::internal::Map>, v8::internal::Isolate*) () at ../../src/objects/tagged-impl.h:88
#2  0x00007ffff62c042d in v8::internal::Map::GetDerivedMap(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Map>, v8::internal::Handle<v8::internal::JSReceiver>) () at ../../src/objects/map.cc:938
#3  0x00007ffff61574c7 in v8::internal::JSFunction::GetDerivedMap(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::JSReceiver>) () at ../../src/objects/js-function.cc:1110
#4  0x00007ffff574955b in v8::internal::Builtin_Impl_NumberFormatConstructor(v8::internal::BuiltinArguments, v8::internal::Isolate*) () at ../../src/builtins/builtins-intl.cc:239
#5  0x00007ffff574908f in v8::internal::Builtin_NumberFormatConstructor(int, unsigned long*, v8::internal::Isolate*) () at ../../src/builtins/builtins-intl.cc:435
#6  0x00007ffff4defdbd in Builtins_CEntry_Return1_ArgvOnStack_BuiltinExit () from /home/kiprey/test/libv8.so
#7  0x00007ffff4a48e21 in Builtins_JSBuiltinsConstructStub () from /home/kiprey/test/libv8.so
#8  0x0000197000a42291 in ?? ()
#9  0x0000197000c921ed in ?? ()
#10 0x000000000000000a in ?? ()
#11 0x00001970000006e9 in ?? ()
#12 0x00001970000006e9 in ?? ()
#13 0x0051515100000002 in ?? ()
#14 0x0000197000c8a245 in ?? ()
#15 0x000000000000002e in ?? ()
#16 0x00007fffffffc958 in ?? ()
#17 0x00007ffff4a5501b in Builtins_InterpreterEntryTrampoline () from /home/kiprey/test/libv8.so
#18 0x0000197000000061 in ?? ()
#19 0x0000197000005bfd in ?? ()
#20 0x0000197000005bfd in ?? ()
#21 0x0000197000005bfd in ?? ()
#22 0x0000197000005bfd in ?? ()
#23 0x0000197000005bfd in ?? ()
#24 0x0000197000a42291 in ?? ()
#25 0x0000197000a422ed in ?? ()
#26 0x0000197000c921ed in ?? ()
#27 0x0000197000c91e9d in ?? ()
#28 0x0000197000c91ef1 in ?? ()
#29 0x0000197000a4221d in ?? ()
#30 0x0000197000a42209 in ?? ()
#31 0x0000197000005bfd in ?? ()
#32 0x0000197000005bfd in ?? ()
#33 0x0000197000005bfd in ?? ()
#34 0x0000197000005bfd in ?? ()
#35 0x0000197000005bfd in ?? ()
#36 0x0000197000ca34c1 in ?? ()
#37 0x00000000000001ac in ?? ()
#38 0x00000ae700042669 in ?? ()
#39 0x0000000000000001 in ?? ()
#40 0x0000197000ca3471 in ?? ()
#41 0x0000197000a4223d in ?? ()
#42 0x00007fffffffc9e0 in ?? ()
#43 0x00007ffff4a5501b in Builtins_InterpreterEntryTrampoline () from /home/kiprey/test/libv8.so
#44 0x0000197000c8a1e9 in ?? ()
#45 0x0000197000c82841 in ?? ()
#46 0x0000197000c82851 in ?? ()
#47 0x0000197000c8a1e9 in ?? ()
#48 0x0000197000c82871 in ?? ()
#49 0x0000197000c8a1e9 in ?? ()
#50 0x0000197000ca3471 in ?? ()
#51 0x0000197000c82841 in ?? ()
#52 0x0000197000000061 in ?? ()
#53 0x0000197000ca24d1 in ?? ()
#54 0x000000000000073e in ?? ()
#55 0x00000ae700042259 in ?? ()
#56 0x0000000000000001 in ?? ()
#57 0x0000197000ca20b5 in ?? ()
#58 0x0000197000ca27f1 in ?? ()
#59 0x00007fffffffca08 in ?? ()
#60 0x00007ffff4a4bfdc in Builtins_JSEntryTrampoline () from /home/kiprey/test/libv8.so
#61 0x0000197000c8a1e9 in ?? ()
#62 0x0000197000ca20b5 in ?? ()
#63 0x000000000000002c in ?? ()
#64 0x00007fffffffca70 in ?? ()
#65 0x00007ffff4a4bd07 in Builtins_JSEntry () from /home/kiprey/test/libv8.so
Backtrace stopped: previous frame inner to this frame (corrupt stack?)
```

### ki...@gmail.com (2024-01-20)

[Comment Deleted]

### ki...@gmail.com (2024-01-20)

PrototypeInfo::AddDerivedMap will compare *bigger and *derived [0], but since one of them is a stale pointer, this will lead to triggering a segment fault at [2] when performing the SLOW_DCHECK comparison [1]. 

The failure of SLOW_DCHECK can indicate a specific impact, suggesting that there might be some potential UAF (Use After Free) issues here.

void PrototypeInfo::AddDerivedMap(Handle<PrototypeInfo> info, Handle<Map> to,
                                  Isolate* isolate) {
  if (IsUndefined(info->derived_maps())) {
    // Index 0 is the map for object create
    Tagged<WeakArrayList> derived = *isolate->factory()->NewWeakArrayList(2);
    // GetConstructMap assumes a weak pointer.
    derived->Set(0, HeapObjectReference::ClearedValue(isolate));
    derived->Set(1, HeapObjectReference::Weak(*to));
    derived->set_length(2);
    info->set_derived_maps(derived, kReleaseStore);
    return;
  }
  auto derived = Tagged<WeakArrayList>::cast(info->derived_maps());
  // Index 0 is the map for object create
  int i = 1;
  for (; i < derived->length(); ++i) {
    MaybeObject el = derived->Get(i);
    if (el.IsCleared()) {
      derived->Set(i, HeapObjectReference::Weak(*to));
      return;
    }
  }

  auto bigger =
      WeakArrayList::EnsureSpace(isolate, handle(derived, isolate), i + 1);
  bigger->Set(i, HeapObjectReference::Weak(*to));
  bigger->set_length(i + 1);
  if (*bigger != *derived) { //-------> [0]
    info->set_derived_maps(*bigger, kReleaseStore);
  }
}

```
  // Don't use this operator for comparing with stale or invalid pointers
  // because CheckObjectComparisonAllowed() might crash when trying to access
  // the object's page header. Use SafeEquals() instead.
  template <typename U>
  constexpr bool operator!=(TaggedImpl<kRefType, U> other) const {
    static_assert(
        std::is_same<U, Address>::value || std::is_same<U, Tagged_t>::value,
        "U must be either Address or Tagged_t");
#ifdef V8_EXTERNAL_CODE_SPACE
    // When comparing two full pointer values ensure that it's allowed.
    if (std::is_same<StorageType, Address>::value &&
        std::is_same<U, Address>::value) {
      SLOW_DCHECK(CheckObjectComparisonAllowed(ptr_, other.ptr())); //-------> [1]
    }
#endif  // V8_EXTERNAL_CODE_SPACE
    return static_cast<Tagged_t>(ptr_) != static_cast<Tagged_t>(other.ptr());
  }
```


```
#ifdef V8_EXTERNAL_CODE_SPACE
bool CheckObjectComparisonAllowed(Address a, Address b) {
  if (!HAS_STRONG_HEAP_OBJECT_TAG(a) || !HAS_STRONG_HEAP_OBJECT_TAG(b)) {
    return true;
  }
  Tagged<HeapObject> obj_a = HeapObject::unchecked_cast(Tagged<Object>(a));
  Tagged<HeapObject> obj_b = HeapObject::unchecked_cast(Tagged<Object>(b));
  // This check might fail when we try to compare objects in different pointer
  // compression cages (e.g. the one used by code space or trusted space) with
  // each other. The main legitimate case when such "mixed" comparison could
  // happen is comparing two AbstractCode objects. If that's the case one must
  // use AbstractCode's == operator instead of Object's one or SafeEquals().
  CHECK_EQ(IsCodeSpaceObject(obj_a), IsCodeSpaceObject(obj_b));
  CHECK_EQ(IsTrustedSpaceObject(obj_a), IsTrustedSpaceObject(obj_b));
  return true;
}
#endif  // V8_EXTERNAL_CODE_SPACE


V8_INLINE uintptr_t GetFlags() const {
return *reinterpret_cast<const uintptr_t*>(reinterpret_cast<Address>(this) +
                                            kFlagsOffset); //[2]
}
```

[0] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/prototype-info-inl.h;l=124;drc=3cc22c22d7637bc5604e8fef3b0882b51a762901;bpv=1;bpt=1
[1] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/tagged-impl.h;l=88;drc=3cc22c22d7637bc5604e8fef3b0882b51a762901;bpv=1;bpt=1
[2] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/heap-write-barrier-inl.h;l=92;drc=3cc22c22d7637bc5604e8fef3b0882b51a762901;bpv=1;bpt=1

### cl...@chromium.org (2024-01-23)

Detailed Report: https://clusterfuzz.com/testcase?key=5431641943506944

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7ede20500008
Crash State:
  v8::internal::CheckObjectComparisonAllowed
  v8::internal::PrototypeInfo::AddDerivedMap
  v8::internal::Map::GetDerivedMap
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&revision=91931

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5431641943506944

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sa...@google.com (2024-01-23)

Managed to reproduce it on Clusterfuzz but not reliable enough for minimization etc. (as expected). Oli, could you take a look?

[Monorail components: Blink>JavaScript>Runtime]

### [Deleted User] (2024-01-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2024-01-23)

ClusterFuzz testcase 5431641943506944 appears to be flaky, updating reproducibility label.

### ol...@chromium.org (2024-01-23)

[Empty comment from Monorail migration]

### ol...@chromium.org (2024-01-23)

Thank you @Kipreyyy, that is a nice find.

### gi...@appspot.gserviceaccount.com (2024-01-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/ee7825c12c1a4466178d8a68f609c13ffd26a23e

commit ee7825c12c1a4466178d8a68f609c13ffd26a23e
Author: Olivier Flückiger <olivf@chromium.org>
Date: Tue Jan 23 14:29:24 2024

[maps] Keep derived map cache handlified

When adding an entry to the derived map cache we must keep the reference
handlified.

Fixed: chromium:1520200
Change-Id: If93e73f75699b7c4516fc5646da63b66d744ac77
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5225046
Auto-Submit: Olivier Flückiger <olivf@chromium.org>
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91959}

[modify] https://crrev.com/ee7825c12c1a4466178d8a68f609c13ffd26a23e/src/objects/prototype-info-inl.h


### am...@chromium.org (2024-01-23)

[Description Changed]

### [Deleted User] (2024-01-23)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-23)

[Empty comment from Monorail migration]

### ol...@chromium.org (2024-01-23)

[Empty comment from Monorail migration]

### ki...@gmail.com (2024-01-24)

Maybe need add all platform? Not only chromeos.

### ha...@google.com (2024-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-24)

Merge review required: M122 is already shipping to beta.

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
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ol...@chromium.org (2024-01-25)

1. security fix
2. https://chromium-review.googlesource.com/c/v8/v8/+/5225046
3. yes
4. no

### am...@google.com (2024-02-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-02)

Congratulations Zhenghang Xiao! The Chrome VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1520200?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### am...@chromium.org (2024-02-04)

[post migration testing / verified] this is a valid merge request carried over from sheriffbot, will be reviewed by Tuesday 

### am...@chromium.org (2024-02-10)

this was removed from my the security review queue because it was only marked as affecting ChromeOS
reviewing now

### am...@chromium.org (2024-02-10)

<https://crrev.com/c/5225046> approved for merge to M122; please merge this fix to 12.2-lkgr by EOD Monday, 12 February so this fix can be included in the M122 Stable cut

### pe...@google.com (2024-02-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-02-12)

Project: v8/v8
Branch: refs/branch-heads/12.2

commit c671e2d874653eb65d454fcc58d534b62979c927
Author: Olivier Flückiger <olivf@chromium.org>
Date:   Tue Jan 23 15:29:24 2024

    Merged: [maps] Keep derived map cache handlified
    
    When adding an entry to the derived map cache we must keep the reference
    handlified.
    
    Fixed: chromium:1520200
    (cherry picked from commit ee7825c12c1a4466178d8a68f609c13ffd26a23e)
    
    Change-Id: Iebb2b27496891d67896a4316f0b7fc710f14462d
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5280694
    Commit-Queue: Victor Gomes <victorgomes@chromium.org>
    Reviewed-by: Victor Gomes <victorgomes@chromium.org>
    Auto-Submit: Olivier Flückiger <olivf@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.2@{#28}
    Cr-Branched-From: 6eb5a9616aa6f8c705217aeb7c7ab8c037a2f676-refs/heads/12.2.281@{#1}
    Cr-Branched-From: 44cf56d850167c6988522f8981730462abc04bcc-refs/heads/main@{#91934}

M       src/objects/prototype-info-inl.h

https://chromium-review.googlesource.com/5280694


### pe...@google.com (2024-02-12)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### ol...@chromium.org (2024-02-12)

no, this only affects 122

### pb...@google.com (2024-02-13)

Please get the Cl's merged to M122 branch asap, Since we are planning to cut M122 Stable RC around 3PM PST today. 

Please get them cherry picked asap and reach out to me if you need any help.

### pb...@google.com (2024-02-13)

My bad the CL is already merged to m122 branch  as it refered in comment#32

### na...@google.com (2024-02-18)

olivf@chromium.org
Could you help confirm if this fix is needed for LTS-114? If Yes, then pls add the hotlist "LTS-Merge-request-114" to the bug and respond to the questionnaire that gets populated with it. thanks

### ol...@chromium.org (2024-02-19)

This affects M122 only. See comment 34.

### na...@google.com (2024-02-21)

Based on comment#34, this fix is not applicable to LTS-114/ 120

### pe...@google.com (2024-05-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41493175)*

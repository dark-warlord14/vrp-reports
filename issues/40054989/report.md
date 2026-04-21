# Security: Use after free in V8

| Field | Value |
|-------|-------|
| **Issue ID** | [40054989](https://issues.chromium.org/issues/40054989) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler, Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | p4...@gmail.com |
| **Assignee** | ne...@chromium.org |
| **Created** | 2021-02-26 |
| **Bounty** | $15,000.00 |

## Description

**Please provide a brief explanation of the security issue.**  

In optimized function, when something unexpected happens, it will call `TranslatedValue::GetValue` to generate some necessary objects using the information (such as element pointer) stored in register or stack. When an object generated twice, the information was stored twice in old space. If we perform side-effect operations on an object, the other memory wasn't modified, causing a dangling pointer left in old space.

There are two places calling TranslatedValue::GetValue, one is OptimizedFrame::Summarize which in JSError object constructing, the other is Deoptimizer::MaterializeHeapObjects in deoptimize.

When a inlined optimized function hinted a try, it will generate the JSFunction object which cause JSerror.  

The JSfunction has a Context member which will store some related objects, and the JSFunction was stoted in the JSError's keyed element.

This is the first time calling TranslatedValue::GetValue.

```
void OptimizedFrame::Summarize(std::vector<FrameSummary>\* frames) const {  
// [...]  
  bool is_constructor = IsConstructor();  
  for (auto it = translated.begin(); it != translated.end(); it++) {  
    if (it->kind() == TranslatedFrame::kUnoptimizedFunction ||  
        it->kind() == TranslatedFrame::kJavaScriptBuiltinContinuation ||  
        it->kind() ==  
            TranslatedFrame::kJavaScriptBuiltinContinuationWithCatch) {  
      Handle<SharedFunctionInfo> shared_info = it->shared_info();  
  
      // The translation commands are ordered and the function is always  
      // at the first position, and the receiver is next.  
      TranslatedFrame::iterator translated_values = it->begin();  
  
      // Get or materialize the correct function in the optimized frame.  
 [1]     Handle<JSFunction> function =  
          Handle<JSFunction>::cast(translated_values->GetValue());  
      translated_values++;  
  
      // Get or materialize the correct receiver in the optimized frame.  
      Handle<Object> receiver = translated_values->GetValue();  
      translated_values++;  
  
      // Determine the underlying code object and the position within it from  
      // the translation corresponding to the frame type in question.  
      Handle<AbstractCode> abstract_code;  
      unsigned code_offset;  
      if (it->kind() == TranslatedFrame::kJavaScriptBuiltinContinuation ||  
          it->kind() ==  
              TranslatedFrame::kJavaScriptBuiltinContinuationWithCatch) {  
        code_offset = 0;  
        abstract_code = handle(  
            AbstractCode::cast(isolate()->builtins()->builtin(  
                Builtins::GetBuiltinFromBytecodeOffset(it->bytecode_offset()))),  
            isolate());  
      } else {  
        DCHECK_EQ(it->kind(), TranslatedFrame::kUnoptimizedFunction);  
        code_offset = it->bytecode_offset().ToInt();  
        abstract_code =  
            handle(shared_info->abstract_code(isolate()), isolate());  
      }  
  
      // Append full summary of the encountered JS frame.  
      Handle<FixedArray> params = GetParameters();  
      FrameSummary::JavaScriptFrameSummary summary(  
          isolate(), \*receiver, \*function, \*abstract_code, code_offset,  
          is_constructor, \*params);  
      frames->push_back(summary);  
      is_constructor = false;  
    } else if (it->kind() == TranslatedFrame::kConstructStub) {  
      // The next encountered JS frame will be marked as a constructor call.  
      DCHECK(!is_constructor);  
      is_constructor = true;  
    }  
  }  
}  

```

when deoptimizing, it will call `Deoptimizer::MaterializeHeapObjects` to generate objects used by runtime.

this is the second time to call TranslatedValue::GetValue.

```
void Deoptimizer::MaterializeHeapObjects() {  
  translated_state_.Prepare(static_cast<Address>(stack_fp_));  
  if (FLAG_deopt_every_n_times > 0) {  
    // Doing a GC here will find problems with the deoptimized frames.  
    isolate_->heap()->CollectAllGarbage(Heap::kNoGCFlags,  
                                        GarbageCollectionReason::kTesting);  
  }  
  
  for (auto& materialization : values_to_materialize_) {  
    Handle<Object> value = materialization.value_->GetValue();  
  
    if (verbose_tracing_enabled()) {  
      PrintF(trace_scope()->file(),  
             "Materialization [" V8PRIxPTR_FMT "] <- " V8PRIxPTR_FMT " ;  ",  
             static_cast<intptr_t>(materialization.output_slot_address_),  
             value->ptr());  
      value->ShortPrint(trace_scope()->file());  
      PrintF(trace_scope()->file(), "\n");  
    }  
  
    \*(reinterpret_cast<Address\*>(materialization.output_slot_address_)) =  
        value->ptr();  
  }  
  
  translated_state_.VerifyMaterializedObjects();  
  
  bool feedback_updated = translated_state_.DoUpdateFeedback();  
  if (verbose_tracing_enabled() && feedback_updated) {  
    FILE\* file = trace_scope()->file();  
    Deoptimizer::DeoptInfo info =  
        Deoptimizer::GetDeoptInfo(compiled_code_, from_);  
    PrintF(file, "Feedback updated from deoptimization at ");  
    OFStream outstr(file);  
    info.position.Print(outstr, compiled_code_);  
    PrintF(file, ", %s\n", DeoptimizeReasonToString(info.deopt_reason));  
  }  
  
  isolate_->materialized_object_store()->Remove(  
      static_cast<Address>(stack_fp_));  
}  

```

In runtime, when some side-effect called, it will only modified object generated in Deoptimizer::MaterializeHeapObjects. for example Heap::LeftTrimFixedArray.

```
FixedArrayBase Heap::LeftTrimFixedArray(FixedArrayBase object,  
                                        int elements_to_trim) {  
  if (elements_to_trim == 0) {  
    // This simplifies reasoning in the rest of the function.  
    return object;  
  }  
  CHECK(!object.is_null());  
  DCHECK(CanMoveObjectStart(object));  
  // Add custom visitor to concurrent marker if new left-trimmable type  
  // is added.  
  DCHECK(object.IsFixedArray() || object.IsFixedDoubleArray());  
  const int element_size = object.IsFixedArray() ? kTaggedSize : kDoubleSize;  
  const int bytes_to_trim = elements_to_trim \* element_size;  
  Map map = object.map();  
  
  // For now this trick is only applied to fixed arrays which may be in new  
  // space or old space. In a large object space the object's start must  
  // coincide with chunk and thus the trick is just not applicable.  
  DCHECK(!IsLargeObject(object));  
  DCHECK(object.map() != ReadOnlyRoots(this).fixed_cow_array_map());  
  
  STATIC_ASSERT(FixedArrayBase::kMapOffset == 0);  
  STATIC_ASSERT(FixedArrayBase::kLengthOffset == kTaggedSize);  
  STATIC_ASSERT(FixedArrayBase::kHeaderSize == 2 \* kTaggedSize);  
  
  const int len = object.length();  
  DCHECK(elements_to_trim <= len);  
  
  // Calculate location of new array start.  
  Address old_start = object.address();  
  Address new_start = old_start + bytes_to_trim;  
  
  if (incremental_marking()->IsMarking()) {  
    incremental_marking()->NotifyLeftTrimming(  
        object, HeapObject::FromAddress(new_start));  
  }  
  
#ifdef DEBUG  
  if (MayContainRecordedSlots(object)) {  
    MemoryChunk\* chunk = MemoryChunk::FromHeapObject(object);  
    DCHECK(!chunk->RegisteredObjectWithInvalidatedSlots<OLD_TO_OLD>(object));  
    DCHECK(!chunk->RegisteredObjectWithInvalidatedSlots<OLD_TO_NEW>(object));  
  }  
#endif  
  
  // Technically in new space this write might be omitted (except for  
  // debug mode which iterates through the heap), but to play safer  
  // we still do it.  
  CreateFillerObjectAt(old_start, bytes_to_trim,  
                       MayContainRecordedSlots(object)  
                           ? ClearRecordedSlots::kYes  
                           : ClearRecordedSlots::kNo);  
  
  // Initialize header of the trimmed array. Since left trimming is only  
  // performed on pages which are not concurrently swept creating a filler  
  // object does not require synchronization.  
  RELAXED_WRITE_FIELD(object, bytes_to_trim, map);  
  RELAXED_WRITE_FIELD(object, bytes_to_trim + kTaggedSize,  
                      Smi::FromInt(len - elements_to_trim));  
  
  FixedArrayBase new_object =  
      FixedArrayBase::cast(HeapObject::FromAddress(new_start));  
  
  // Notify the heap profiler of change in object layout.  
  OnMoveEvent(new_object, object, new_object.Size());  
  
#ifdef ENABLE_SLOW_DCHECKS  
  if (FLAG_enable_slow_asserts) {  
    // Make sure the stack or other roots (e.g., Handles) don't contain pointers  
    // to the original FixedArray (which is now the filler object).  
    SafepointScope scope(this);  
    LeftTrimmerVerifierRootVisitor root_visitor(object);  
    ReadOnlyRoots(this).Iterate(&root_visitor);  
    IterateRoots(&root_visitor, {});  
  }  
#endif  // ENABLE_SLOW_DCHECKS  
  
  return new_object;  
}  

```

When gc happened ,the pointer in JSError becomes dangling pointer.

**VERSION**  

d8 Version: commit cd2248a280ba4e470a0d9c274c4053370a8dcd58  

Operating System: [win10 64bit / ubuntu 64bit]

**REPRODUCTION CASE**  

\* SEGV\_ACCERR caused by uaf.

1. execute the attach file in d8 version with flag "--allow-natives-syntax --expose-gc ".
2. it will crash cause SEGV\_ACCERR. it also can repro in chrome 88.0.4324.190.

/\*  

$ ~/fuzz/v8/out.gn/x64.debug/d8 --allow-natives-syntax --expose-gc test.js  

Received signal 11 SEGV\_ACCERR 2ca1beadbef6

==== C stack trace ===============================

[0x7fc424e84547]  

[0x7fc424a713c0]  

[0x7fc425fc2453]  

[0x7fc425fc7031]  

[0x7fc425fc67e1]  

[0x7fc425f8c5a9]  

[0x7fc425f897bb]  

[0x7fc425f86bda]  

[0x7fc425f88793]  

[0x7fc425cdfb79]  

[0x7fc425cde406]  

[0x7fc425cdc808]  

[0x7fc425cdc2f8]  

[0x7fc4257048bf]  

[end of stack trace]  

[1] 80387 segmentation fault (core dumped) ~/fuzz/v8/out.gn/x64.debug/d8 --allow-natives-syntax --expose-gc test.js  

\*/

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 1.2 KB)

## Timeline

### p4...@gmail.com (2021-02-26)

I can also provide other crash samples in CHECK or DECHECK failed if need.

### [Deleted User] (2021-02-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-02-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5758465398865920.

### cl...@chromium.org (2021-02-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-02-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-02-26)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/e620ba139bc82ff8021031b525c1b40027c8d224 ([torque] Address remaining usages of @noVerifier in base.tq).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2021-02-26)

Detailed Report: https://clusterfuzz.com/testcase?key=5758465398865920

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  elements__value.IsFixedArrayBase() in class-verifiers.cc
  v8::internal::TorqueGeneratedClassVerifiers::JSObjectVerify
  v8::internal::JSObject::JSObjectVerify
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=62262:62263

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5758465398865920

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5758465398865920 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### se...@microsoft.com (2021-02-26)

The blamed change affected class verifiers (a debug-only feature), so I'm not surprised that it would change the crash signature from a bug that causes heap corruption. I'm pretty confident that it didn't introduce this UAF though.

### ad...@google.com (2021-02-26)

ishell@, as we'e persuaded ClusterFuzz to reproduce this, I hope that means we can pass it over to you as the current V8 ClusterFuzz sheriff :)

Please could you also confirm if this is an actual UaF (in which case set Security_Severity-High) or instead something like a null pointer dereference (in which case, type=Bug unless it's believed to be exploitable somehow).

### p4...@gmail.com (2021-02-27)

[Comment Deleted]

### me...@chromium.org (2021-03-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-03-01)

I ran a bisect locally. It bisect back to 2cb8a6e34980c5b44fe45a741ed560d483fb2445 ([Compile] Avoid flushing code that's marked for optimization in tests). This CL is more than two years old and introduces the "%PrepareFunctionForOptimization" runtime function which is being used in the reproducer.
So this seems to be a really old issue.

Georg, can you find a good owner for this please?

### ne...@chromium.org (2021-03-01)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript Blink>JavaScript>Compiler]

### p4...@gmail.com (2021-03-02)

[Comment Deleted]

### ne...@chromium.org (2021-03-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-03-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5642573558120448.

### [Deleted User] (2021-03-02)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ne...@chromium.org (2021-03-04)

[Empty comment from Monorail migration]

### ne...@chromium.org (2021-03-09)

The way the deoptimizer is used by the exception stack trace mechanism is not compatible with left-trimming. The crash not a use-after-free as such, but the garbage collector gets confused, which can have all kinds of effects and might be exploitable with a lot of effort. I'm working on a fix.

[Monorail components: Blink>JavaScript>GC]

### ne...@chromium.org (2021-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/3353a7d0b017146d543434be4036a81aaf7d25ae

commit 3353a7d0b017146d543434be4036a81aaf7d25ae
Author: Georg Neis <neis@chromium.org>
Date: Wed Mar 10 17:18:44 2021

[deoptimizer] Fix bug in OptimizedFrame::Summarize

OptimizedFrame::Summarize is used by debugger features etc
to inspect the frame of an optimized function (and the virtual frames
of functions that got inlined). It could end up materializing a JSArray
with the same backing store as one that would later get left-trimmed,
resulting in a dangling elements pointer. This CL fixes that by creating
a fresh copy of the elements store instead.

Bug: chromium:1182647
Change-Id: Iaf329464520a927b0ba33166cad2524d3752c450
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2748593
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#73330}

[modify] https://crrev.com/3353a7d0b017146d543434be4036a81aaf7d25ae/src/deoptimizer/translated-state.cc
[modify] https://crrev.com/3353a7d0b017146d543434be4036a81aaf7d25ae/src/deoptimizer/translated-state.h
[add] https://crrev.com/3353a7d0b017146d543434be4036a81aaf7d25ae/test/mjsunit/compiler/regress-1182647.js


### cl...@chromium.org (2021-03-11)

ClusterFuzz testcase 5758465398865920 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=73329:73330

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2021-03-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-12)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M89. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M90. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-12)

This bug requires manual review: M90's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2021-03-15)

pls help answer https://crbug.com/chromium/1182647#c27 for merge review

### ne...@chromium.org (2021-03-16)

Sorry for the delay.

1) Yes
2) https://chromium.googlesource.com/v8/v8/+/3353a7d0b017146d543434be4036a81aaf7d25ae
3) Yes
4) I believe 89 and 99.
5) Bug fix (possibly security issue)
6) No

### sr...@google.com (2021-03-16)

Merge approved for M90 branch:4430

### ne...@chromium.org (2021-03-16)

Oops, of course I meant 89 and 90 in https://crbug.com/chromium/1182647#c29. Will do the merge to 90 (v8 9.0) now.

### gi...@appspot.gserviceaccount.com (2021-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/21b892c549fa26cdb6e816b9acbf5e93a9607558

commit 21b892c549fa26cdb6e816b9acbf5e93a9607558
Author: Georg Neis <neis@chromium.org>
Date: Tue Mar 16 17:29:46 2021

Merged: [deoptimizer] Fix bug in OptimizedFrame::Summarize

Revision: 3353a7d0b017146d543434be4036a81aaf7d25ae

BUG=chromium:1182647
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
TBR=bmeurer@chromium.org

Change-Id: Ifd0770913875e97265fd90b016deee09fe40b1a3
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2764747
Reviewed-by: Georg Neis <neis@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.0@{#24}
Cr-Branched-From: bd0108b4c88e0d6f2350cb79b5f363fbd02f3eb7-refs/heads/9.0.257@{#1}
Cr-Branched-From: 349bcc6a075411f1a7ce2d866c3dfeefc2efa39d-refs/heads/master@{#73001}

[modify] https://crrev.com/21b892c549fa26cdb6e816b9acbf5e93a9607558/src/deoptimizer/translated-state.cc
[modify] https://crrev.com/21b892c549fa26cdb6e816b9acbf5e93a9607558/src/deoptimizer/translated-state.h
[add] https://crrev.com/21b892c549fa26cdb6e816b9acbf5e93a9607558/test/mjsunit/compiler/regress-1182647.js


### ne...@chromium.org (2021-03-16)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-18)

Congratulations, p4nda! The VRP Panel has decided to award you $15,000 for this report. Awesome work! 

### am...@google.com (2021-03-18)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-23)

Approving merge to M89. Please go ahead and merge unless you have any stability concerns.

### ne...@chromium.org (2021-03-23)

Merge CL with autosubmit is here: https://chromium-review.googlesource.com/c/v8/v8/+/2780300
I'll be on vacation until end of the month starting tomorrow.

### gi...@appspot.gserviceaccount.com (2021-03-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/c0c96b768a7d3463b11403874549e6496529740d

commit c0c96b768a7d3463b11403874549e6496529740d
Author: Georg Neis <neis@chromium.org>
Date: Tue Mar 23 16:37:21 2021

Merged: [deoptimizer] Fix bug in OptimizedFrame::Summarize

Revision: 3353a7d0b017146d543434be4036a81aaf7d25ae

BUG=chromium:1182647
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=bmeurer@chromium.org

Change-Id: I86abd6a3f34169be5f99aa9f54bb7bb3706fa85a
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2780300
Reviewed-by: Georg Neis <neis@chromium.org>
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.9@{#49}
Cr-Branched-From: 16b9bbbd581c25391981aa03180b76aa60463a3e-refs/heads/8.9.255@{#1}
Cr-Branched-From: d16a2a688498bd1c3e6a49edb25d8c4ca56232dc-refs/heads/master@{#72039}

[modify] https://crrev.com/c0c96b768a7d3463b11403874549e6496529740d/src/deoptimizer/deoptimizer.cc
[modify] https://crrev.com/c0c96b768a7d3463b11403874549e6496529740d/src/deoptimizer/deoptimizer.h
[add] https://crrev.com/c0c96b768a7d3463b11403874549e6496529740d/test/mjsunit/compiler/regress-1182647.js


### ne...@chromium.org (2021-03-24)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-29)

[Empty comment from Monorail migration]

### p4...@gmail.com (2021-03-30)

Could u please credit to  "Bohan Liu (@P4nda20371774) and Moon Liang of Tencent Security Xuanwu Lab" when the new stable version releases. 

Thanks!


### as...@google.com (2021-03-30)

[Empty comment from Monorail migration]

### su...@chromium.org (2021-03-30)

Merge approved for LTS-86

### gi...@appspot.gserviceaccount.com (2021-03-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/254c7945eea2ee85e2bab98dd802b9d940fc1f4b

commit 254c7945eea2ee85e2bab98dd802b9d940fc1f4b
Author: Georg Neis <neis@chromium.org>
Date: Tue Mar 23 16:37:21 2021

Merged: [deoptimizer] Fix bug in OptimizedFrame::Summarize

Revision: 3353a7d0b017146d543434be4036a81aaf7d25ae

BUG=chromium:1182647
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=​bmeurer@chromium.org

(cherry picked from commit c0c96b768a7d3463b11403874549e6496529740d)

Change-Id: I86abd6a3f34169be5f99aa9f54bb7bb3706fa85a
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2780300
Reviewed-by: Georg Neis <neis@chromium.org>
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/8.9@{#49}
Cr-Original-Branched-From: 16b9bbbd581c25391981aa03180b76aa60463a3e-refs/heads/8.9.255@{#1}
Cr-Original-Branched-From: d16a2a688498bd1c3e6a49edb25d8c4ca56232dc-refs/heads/master@{#72039}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2794427
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/8.6@{#72}
Cr-Branched-From: a64aed2333abf49e494d2a5ce24bbd14fff19f60-refs/heads/8.6.395@{#1}
Cr-Branched-From: a626bc036236c9bf92ac7b87dc40c9e538b087e3-refs/heads/master@{#69472}

[modify] https://crrev.com/254c7945eea2ee85e2bab98dd802b9d940fc1f4b/src/deoptimizer/deoptimizer.cc
[modify] https://crrev.com/254c7945eea2ee85e2bab98dd802b9d940fc1f4b/src/deoptimizer/deoptimizer.h
[add] https://crrev.com/254c7945eea2ee85e2bab98dd802b9d940fc1f4b/test/mjsunit/compiler/regress-1182647.js


### as...@google.com (2021-03-31)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1182647?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>Compiler, Blink>JavaScript>GarbageCollection]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054989)*

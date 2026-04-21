# Security: Memory corrupt in v8, leading to RCE

| Field | Value |
|-------|-------|
| **Issue ID** | [40067712](https://issues.chromium.org/issues/40067712) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2023-07-19 |
| **Bounty** | $23,000.00 |

## Description

VULNERABILITY DETAILS
## BISECT1
Note: The current POC will bisect to https://crrev.com/6c108b36d5861c4186e931793a6d8adbfbc7ab83. 
However, it is not the correct entry point. Here, only modifications to the opcode have been made. Reverting these modifications and continuing the bisect will lead to the actual entry point. So, if you are using ClusterFuzz for classification, please take note of this.

After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 85705
    - link: https://crrev.com/455d38ff8df7303474e8ead05cad659aac0a1bbc 
- Commit Message

```
commit 455d38ff8df7303474e8ead05cad659aac0a1bbc
Author: Manos Koukoutos <manoskouk@chromium.org>
Date:   Mon Feb 6 14:12:58 2023 +0100

    Reland "[wasm-gc] Introduce wasm null object"
    
    This is a reland of commit 2e357c4814954c6d83c336655209e14aa53911d4
    
    Difference compared to original: Initialize wasm-null object's
    payload.
    
    Original change's description:
    > [wasm-gc] Introduce wasm null object
    >
    > We introduce a wasm null object, separate from JS null. Its purpose is
    > to support trapping null accesses for wasm objects.
    > This will be achieved by allocating a large payload for it (larger than
    > any wasm struct) and memory-protecting it (see linked CL). The two null
    > objects get mapped to each other at the wasm-JS boundary.
    > Since externref objects live on the JS side of the boundary,
    > null-related instructions in wasm now need an additional type argument
    > to handle the correct null object.
    >
    > Bug: v8:7748
    > Change-Id: I06da00fcd279cc5376e69ab7858e3782f5b5081e
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4200639
    > Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    > Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    > Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#85648}
    
    Bug: v8:7748
    Change-Id: I46413d05f0213229f1d19277ae98dbb8df5afdf9
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4224011
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#85705}

```

## BISECT2
After testing, it can affect chrome stable, dev and canary through origin trials. The specific version numbers are as follows:
Chrome Stable 115.0.5790.99
Chrome Dev 116.0.5845.42
Chrome Canary 117.0.5897.0

The Origin url I specified is http://localhost:8000
So by using the corresponding browser to visit http://localhost:8000/poc.html, you can verify the vulnerability in chrome.
Please do not modify the URL.

## Root Cause
[0] V8 has introduced the wasm null value in this branch, resulting in two types of null values. One is called 'wasm-null', which is used for the wasm runtime, and the other is called 'null-value', which is applied at the JS layer:

https://chromium.googlesource.com/v8/v8.git/+/455d38ff8df7303474e8ead05cad659aac0a1bbc


[1] Therefore, in future code, when operations such as use, assignment, or non-null judgment are performed on an object reference, it is necessary to first identify whether the object is an internal or external object. This determines whether to load 'wasm-null' or 'null-value'. Just like this:

```
-  void LoadNullValue(Register null, LiftoffRegList pinned) {
-    __ LoadFullPointer(null, kRootRegister,
-                       IsolateData::root_slot_offset(RootIndex::kNullValue));
+  void LoadNullValue(Register null, LiftoffRegList pinned, ValueType type) {
+    __ LoadFullPointer(
+        null, kRootRegister,
+        type == kWasmExternRef || type == kWasmNullExternRef
+            ? IsolateData::root_slot_offset(RootIndex::kNullValue)
+            : IsolateData::root_slot_offset(RootIndex::kWasmNull)); // ---> [1]
```

[2] However, in 'src/wasm/constant-expression-interface.cc', for the default value settings of structures and arrays, it doesn't distinguish between object types and directly assigns all null references as 'null-value' rather than 'wasm-null'.
```
WasmValue DefaultValueForType(ValueType type, Isolate* isolate) {
  switch (type.kind()) {
    case kI32:
    case kI8:
    case kI16:
      return WasmValue(0);
    case kI64:
      return WasmValue(int64_t{0});
    case kF32:
      return WasmValue(0.0f);
    case kF64:
      return WasmValue(0.0);
    case kS128:
      return WasmValue(Simd128());
    case kRefNull:
      return WasmValue(isolate->factory()->null_value(), type); // ---> [2]
    case kVoid:
    case kRtt:
    case kRef:
    case kBottom:
      UNREACHABLE();
  }
}
```

[3] The null pointer of the structure member may later be treated as 'wasm-null', which could cause confusion with the 'null-value' assigned here.


## Exploit
[0] In my tests, the address of 'null-value' is v8_heap_base_addr + 0x235, which we can use as a structure pointer.

[1] By defining structures, we can read data from the v8 heap as new pointers, ultimately achieving arbitrary length read and write within the v8 heap address space.

## Fix
We should keep the data types consistent when assigning and using them, that is, decide 'null' based on the 'type'

```
diff --git a/src/wasm/constant-expression-interface.cc b/src/wasm/constant-expression-interface.cc
index 77e9488bd4d..3750a7e31c7 100644
--- a/src/wasm/constant-expression-interface.cc
+++ b/src/wasm/constant-expression-interface.cc
@@ -197,7 +197,10 @@ WasmValue DefaultValueForType(ValueType type, Isolate* isolate) {
     case kS128:
       return WasmValue(Simd128());
     case kRefNull:
-      return WasmValue(isolate->factory()->null_value(), type);
+      return WasmValue(type == kWasmExternRef || type == kWasmNullExternRef
+                    ? Handle<Object>::cast(isolate->factory()->null_value())
+                    : Handle<Object>::cast(isolate->factory()->wasm_null()),
+                type);
     case kVoid:
     case kRtt:
     case kRef:
```

## REPRODUCE EXPLOIT
I wrote exploit in d8 11.7.100 and Chrome 115.0.5790.98:

### v8 exploit
Build V8 version 11.7.100:
```
git checkout 11.7.100 && gclient sync -D
tools/dev/gm.py x64.release
```
Run the exp:
```
out/x64.release/d8 --experimental-wasm-gc exp.js
```

### Chrome stable exploit
```
google-chrome --user-data-dir=./user http://localhost:8000/exp.html
```

## Other
Please note to include the flags `--experimental-wasm-gc` for clusterfuzz classification.

VERSION
Tested on v8 version: 11.2.0 - 11.7.0

REPRODUCTION CASE
Please note that due to changes in the encoding method of wasm code, the POC will be different. For the latest version of V8, please test with 'poc-new.js'. If you want to test commits prior to https://crrev.com/6c108b36d5861c4186e931793a6d8adbfbc7ab83, please use 'poc-old.js'.

1. Download release v8 from: gs://v8-asan/linux-release/d8-linux-release-v8-component-89042.zip
2. Run: `d8 --experimental-wasm-gc poc-new.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Jerry

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.0 KB)
- [test.js](attachments/test.js) (text/plain, 1.0 KB)
- [rce.png](attachments/rce.png) (image/png, 179.0 KB)
- [poc-old.js](attachments/poc-old.js) (text/plain, 590 B)
- [poc-new.js](attachments/poc-new.js) (text/plain, 593 B)
- [fix.patch](attachments/fix.patch) (text/plain, 780 B)
- [exp.js](attachments/exp.js) (text/plain, 3.6 KB)
- [exp.html](attachments/exp.html) (text/plain, 4.7 KB)
- [exp.html](attachments/exp.html) (text/plain, 4.7 KB)
- [exp.js](attachments/exp.js) (text/plain, 3.6 KB)
- [fix.patch](attachments/fix.patch) (text/plain, 780 B)
- [poc.html](attachments/poc.html) (text/plain, 1.0 KB)
- [poc-new.js](attachments/poc-new.js) (text/plain, 593 B)
- [poc-old.js](attachments/poc-old.js) (text/plain, 590 B)
- [rce.png](attachments/rce.png) (image/png, 179.0 KB)
- [test.js](attachments/test.js) (text/plain, 1.0 KB)

## Timeline

### [Deleted User] (2023-07-19)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-07-19)

Title : Memory corrupt in v8, leading to RCE

VULNERABILITY DETAILS
## BISECT1
Note: The current POC will bisect to https://crrev.com/6c108b36d5861c4186e931793a6d8adbfbc7ab83. 
However, it is not the correct entry point. Here, only modifications to the opcode have been made. Reverting these modifications and continuing the bisect will lead to the actual entry point. So, if you are using ClusterFuzz for classification, please take note of this.

After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 85705
    - link: https://crrev.com/455d38ff8df7303474e8ead05cad659aac0a1bbc 
- Commit Message

```
commit 455d38ff8df7303474e8ead05cad659aac0a1bbc
Author: Manos Koukoutos <manoskouk@chromium.org>
Date:   Mon Feb 6 14:12:58 2023 +0100

    Reland "[wasm-gc] Introduce wasm null object"
    
    This is a reland of commit 2e357c4814954c6d83c336655209e14aa53911d4
    
    Difference compared to original: Initialize wasm-null object's
    payload.
    
    Original change's description:
    > [wasm-gc] Introduce wasm null object
    >
    > We introduce a wasm null object, separate from JS null. Its purpose is
    > to support trapping null accesses for wasm objects.
    > This will be achieved by allocating a large payload for it (larger than
    > any wasm struct) and memory-protecting it (see linked CL). The two null
    > objects get mapped to each other at the wasm-JS boundary.
    > Since externref objects live on the JS side of the boundary,
    > null-related instructions in wasm now need an additional type argument
    > to handle the correct null object.
    >
    > Bug: v8:7748
    > Change-Id: I06da00fcd279cc5376e69ab7858e3782f5b5081e
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4200639
    > Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    > Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    > Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#85648}
    
    Bug: v8:7748
    Change-Id: I46413d05f0213229f1d19277ae98dbb8df5afdf9
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4224011
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#85705}

```

## BISECT2
After testing, it can affect chrome stable, dev and canary through origin trials. The specific version numbers are as follows:
Chrome Stable 115.0.5790.99
Chrome Dev 116.0.5845.42
Chrome Canary 117.0.5897.0

The Origin url I specified is http://localhost:8000
So by using the corresponding browser to visit http://localhost:8000/poc.html, you can verify the vulnerability in chrome.
Please do not modify the URL.

## Root Cause
[0] V8 has introduced the wasm null value in this branch, resulting in two types of null values. One is called 'wasm-null', which is used for the wasm runtime, and the other is called 'null-value', which is applied at the JS layer:

https://chromium.googlesource.com/v8/v8.git/+/455d38ff8df7303474e8ead05cad659aac0a1bbc


[1] Therefore, in future code, when operations such as use, assignment, or non-null judgment are performed on an object reference, it is necessary to first identify whether the object is an internal or external object. This determines whether to load 'wasm-null' or 'null-value'. Just like this:

```
-  void LoadNullValue(Register null, LiftoffRegList pinned) {
-    __ LoadFullPointer(null, kRootRegister,
-                       IsolateData::root_slot_offset(RootIndex::kNullValue));
+  void LoadNullValue(Register null, LiftoffRegList pinned, ValueType type) {
+    __ LoadFullPointer(
+        null, kRootRegister,
+        type == kWasmExternRef || type == kWasmNullExternRef
+            ? IsolateData::root_slot_offset(RootIndex::kNullValue)
+            : IsolateData::root_slot_offset(RootIndex::kWasmNull)); // ---> [1]
```

[2] However, in 'src/wasm/constant-expression-interface.cc', for the default value settings of structures and arrays, it doesn't distinguish between object types and directly assigns all null references as 'null-value' rather than 'wasm-null'.
```
WasmValue DefaultValueForType(ValueType type, Isolate* isolate) {
  switch (type.kind()) {
    case kI32:
    case kI8:
    case kI16:
      return WasmValue(0);
    case kI64:
      return WasmValue(int64_t{0});
    case kF32:
      return WasmValue(0.0f);
    case kF64:
      return WasmValue(0.0);
    case kS128:
      return WasmValue(Simd128());
    case kRefNull:
      return WasmValue(isolate->factory()->null_value(), type); // ---> [2]
    case kVoid:
    case kRtt:
    case kRef:
    case kBottom:
      UNREACHABLE();
  }
}
```

[3] The null pointer of the structure member may later be treated as 'wasm-null', which could cause confusion with the 'null-value' assigned here.


## Exploit
[0] In my tests, the address of 'null-value' is v8_heap_base_addr + 0x235, which we can use as a structure pointer.

[1] By defining structures, we can read data from the v8 heap as new pointers, ultimately achieving arbitrary length read and write within the v8 heap address space.

## Fix
We should keep the data types consistent when assigning and using them, that is, decide 'null' based on the 'type'

```
diff --git a/src/wasm/constant-expression-interface.cc b/src/wasm/constant-expression-interface.cc
index 77e9488bd4d..3750a7e31c7 100644
--- a/src/wasm/constant-expression-interface.cc
+++ b/src/wasm/constant-expression-interface.cc
@@ -197,7 +197,10 @@ WasmValue DefaultValueForType(ValueType type, Isolate* isolate) {
     case kS128:
       return WasmValue(Simd128());
     case kRefNull:
-      return WasmValue(isolate->factory()->null_value(), type);
+      return WasmValue(type == kWasmExternRef || type == kWasmNullExternRef
+                    ? Handle<Object>::cast(isolate->factory()->null_value())
+                    : Handle<Object>::cast(isolate->factory()->wasm_null()),
+                type);
     case kVoid:
     case kRtt:
     case kRef:
```

## REPRODUCE EXPLOIT
I wrote exploit in d8 11.7.100 and Chrome 115.0.5790.98:

### v8 exploit
Build V8 version 11.7.100:
```
git checkout 11.7.100 && gclient sync -D
tools/dev/gm.py x64.release
```
Run the exp:
```
out/x64.release/d8 --experimental-wasm-gc exp.js
```

### Chrome stable exploit
```
google-chrome --user-data-dir=./user http://localhost:8000/exp.html
```

## Other
Please note to include the flags `--experimental-wasm-gc` for clusterfuzz classification.

VERSION
Tested on v8 version: 11.2.0 - 11.7.0

REPRODUCTION CASE
Please note that due to changes in the encoding method of wasm code, the POC will be different. For the latest version of V8, please test with 'poc-new.js'. If you want to test commits prior to https://crrev.com/6c108b36d5861c4186e931793a6d8adbfbc7ab83, please use 'poc-old.js'.

1. Download release v8 from: gs://v8-asan/linux-release/d8-linux-release-v8-component-89042.zip
2. Run: `d8 --experimental-wasm-gc poc-new.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Jerry

### je...@gmail.com (2023-07-19)

Attached test samples that can be used as v8 unit tests.
Please use poc-new.js instead of test.js for clusterfuzz


### je...@gmail.com (2023-07-19)

Please note that this vulnerability is completely different from another issue-1462951(https://bugs.chromium.org/p/chromium/issues/detail?id=1462951). 
The issue-1462951 is caused by incorrect rewriting of registers due to `extern.externalize`, while this vulnerability results from improper assignment of default values to structure members, leading to confusion.

Although the resulting confusion may appear similar, this is not a patch bypass of the previous vulnerability. They have entirely different causes and are issues in different modules.
This issue also has the potential to result in a stable Chrome RCE. Please prioritize its resolution and fix it as soon as possible.

### rs...@chromium.org (2023-07-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5131009164771328.

### cl...@chromium.org (2023-07-19)

[Empty comment from Monorail migration]

### rs...@chromium.org (2023-07-19)

Thank you for the report and writeup. This also appears to repro on the version of V8 shipped in M114:

~/Downloads/v8-114> ./d8-linux-release-v8-component-87241/d8 --experimental-wasm-gc ../poc-new.js 
V8 is running with experimental features enabled. Stability and security will suffer.
Received signal 11 SEGV_ACCERR 0d6908024007

==== C stack trace ===============================

 [0x55852fb7aee7]
 [0x7f24e2b7b420]
 [0x1cc34060775e]
[end of stack trace]
Segmentation fault (core dumped)

[Monorail components: Blink>JavaScript>WebAssembly]

### [Deleted User] (2023-07-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-19)

Detailed Report: https://clusterfuzz.com/testcase?key=5131009164771328

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7ecb02024007
Crash State:
  Builtins_NewGenericJSToWasmWrapper
  Builtins_JSToWasmWrapper
  Builtins_InterpreterEntryTrampoline
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=88200:88201

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5131009164771328

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


The recommended severity (Security_Severity-Medium) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### [Deleted User] (2023-07-19)

[Empty comment from Monorail migration]

### ti...@google.com (2023-07-19)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-07-20)

Please assign this issue to manoskouk@chromium.org and he will know how to fix this bug.

Other than that, If you can, please apply my patch directly.
```
diff --git a/src/wasm/constant-expression-interface.cc b/src/wasm/constant-expression-interface.cc
index 77e9488bd4d..3750a7e31c7 100644
--- a/src/wasm/constant-expression-interface.cc
+++ b/src/wasm/constant-expression-interface.cc
@@ -197,7 +197,10 @@ WasmValue DefaultValueForType(ValueType type, Isolate* isolate) {
     case kS128:
       return WasmValue(Simd128());
     case kRefNull:
-      return WasmValue(isolate->factory()->null_value(), type);
+      return WasmValue(type == kWasmExternRef || type == kWasmNullExternRef
+                    ? Handle<Object>::cast(isolate->factory()->null_value())
+                    : Handle<Object>::cast(isolate->factory()->wasm_null()),
+                type);
     case kVoid:
     case kRtt:
     case kRef:
```

### is...@chromium.org (2023-07-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/b947905d27518b7764607708ec9f74ac3ea94b6b

commit b947905d27518b7764607708ec9f74ac3ea94b6b
Author: Manos Koukoutos <manoskouk@chromium.org>
Date: Thu Jul 20 11:17:23 2023

[wasm-gc] Use wasm-null as default value for wasm reference types

Bug: v8:7748, chromium:1466183
Change-Id: I6d7de33e0cec37747045269f441e65f7a482dd4f
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4701553
Auto-Submit: Manos Koukoutos <manoskouk@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/heads/main@{#89060}

[modify] https://crrev.com/b947905d27518b7764607708ec9f74ac3ea94b6b/src/wasm/constant-expression-interface.cc


### cl...@chromium.org (2023-07-20)

ClusterFuzz testcase 5131009164771328 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=89059:89060

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### ma...@chromium.org (2023-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-20)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-21)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1466183&entry.364066060=External&entry.958145677=Android&entry.958145677=Chrome&entry.958145677=Fuchsia&entry.958145677=Linux&entry.958145677=Mac&entry.958145677=Windows&entry.958145677=Lacros&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript>WebAssembly&entry.975983575=manoskouk@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-21)

Merge review required: M116 is already shipping to beta.

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

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-21)

Merge review required: M115 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-21)

Merge review required: M114 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-24)

merge approved for https://chromium-review.googlesource.com/c/v8/v8/+/4701553 
please merge this fix to 11.6-lkgr, 11.5-lkgr, and 11.4-lkgr at your earliest convenience, before EOD tomorrow (Tuesday 25 July) so this fix can be included in the next M116/beta release and M115/Stable and M114/Extended Stable updates being cut this Friday -- thank you! 

### am...@chromium.org (2023-07-24)

[Description Changed]

### gi...@appspot.gserviceaccount.com (2023-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/44afa696eaa7d8bb605bd3a726710f11e4907e11

commit 44afa696eaa7d8bb605bd3a726710f11e4907e11
Author: Manos Koukoutos <manoskouk@chromium.org>
Date: Thu Jul 20 11:17:23 2023

[wasm-gc] Use wasm-null as default value for wasm reference types

(cherry picked from commit b947905d27518b7764607708ec9f74ac3ea94b6b)

Bug: v8:7748, chromium:1466183
Change-Id: I6d7de33e0cec37747045269f441e65f7a482dd4f
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4701553
Auto-Submit: Manos Koukoutos <manoskouk@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#89060}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4714685
Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.4@{#57}
Cr-Branched-From: 8a8a1e7086dacc426965d3875914efa66663c431-refs/heads/11.4.183@{#1}
Cr-Branched-From: 5483d8e816e0bbce865cbbc3fa0ab357e6330bab-refs/heads/main@{#87241}

[modify] https://crrev.com/44afa696eaa7d8bb605bd3a726710f11e4907e11/src/wasm/constant-expression-interface.cc


### gi...@appspot.gserviceaccount.com (2023-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/356259e2addd9d600568edcf3674546d554f95b3

commit 356259e2addd9d600568edcf3674546d554f95b3
Author: Manos Koukoutos <manoskouk@chromium.org>
Date: Thu Jul 20 11:17:23 2023

[wasm-gc] Use wasm-null as default value for wasm reference types

(cherry picked from commit b947905d27518b7764607708ec9f74ac3ea94b6b)

Bug: v8:7748, chromium:1466183
Change-Id: I6d7de33e0cec37747045269f441e65f7a482dd4f
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4701553
Auto-Submit: Manos Koukoutos <manoskouk@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#89060}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4714687
Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.5@{#39}
Cr-Branched-From: 0c4044b7336787781646e48b2f98f0c7d1b400a5-refs/heads/11.5.150@{#1}
Cr-Branched-From: b71d3038a7d99c79e1c21239e8ae07da5fc8c90b-refs/heads/main@{#87781}

[modify] https://crrev.com/356259e2addd9d600568edcf3674546d554f95b3/src/wasm/constant-expression-interface.cc


### gi...@appspot.gserviceaccount.com (2023-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/8d60b1d3b1bea9a20219628c99d004c179a84151

commit 8d60b1d3b1bea9a20219628c99d004c179a84151
Author: Manos Koukoutos <manoskouk@chromium.org>
Date: Thu Jul 20 11:17:23 2023

[wasm-gc] Use wasm-null as default value for wasm reference types

(cherry picked from commit b947905d27518b7764607708ec9f74ac3ea94b6b)

Bug: v8:7748, chromium:1466183
Change-Id: I6d7de33e0cec37747045269f441e65f7a482dd4f
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4701553
Auto-Submit: Manos Koukoutos <manoskouk@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#89060}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4714606
Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.6@{#22}
Cr-Branched-From: e29c028f391389a7a60ee37097e3ca9e396d6fa4-refs/heads/11.6.189@{#3}
Cr-Branched-From: 95cbef20e2aa556a1ea75431a48b36c4de6b9934-refs/heads/main@{#88340}

[modify] https://crrev.com/8d60b1d3b1bea9a20219628c99d004c179a84151/src/wasm/constant-expression-interface.cc


### gi...@appspot.gserviceaccount.com (2023-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4ab81369449d485868e715543a2423dfb5a7d759

commit 4ab81369449d485868e715543a2423dfb5a7d759
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jul 25 11:29:26 2023

Roll v8 11.6 from dc8603588d80 to 578812b03709 (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/dc8603588d80..578812b03709

2023-07-25 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.6.189.14
2023-07-25 manoskouk@chromium.org [wasm-gc] Use wasm-null as default value for wasm reference types

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-11-6-chromium-m116
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.6: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m116: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1466183
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I4f89550c038721850430823bc5e4555177261e37
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4714270
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5845@{#778}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/4ab81369449d485868e715543a2423dfb5a7d759/DEPS


### gi...@appspot.gserviceaccount.com (2023-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f5b22e073e0f8cb8e39e060cb661630ee8a8c8fa

commit f5b22e073e0f8cb8e39e060cb661630ee8a8c8fa
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jul 25 11:37:55 2023

Roll v8 11.5 from 34340db35ab9 to 4fe6b3c798fa (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/34340db35ab9..4fe6b3c798fa

2023-07-25 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.5.150.20
2023-07-25 manoskouk@chromium.org [wasm-gc] Use wasm-null as default value for wasm reference types

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-11-5-chromium-m115
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.5: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m115: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1466183
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: Id39a9b725d66278b8fa2eb93b56f7c1707a8539b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4714269
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5790@{#1821}
Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

[modify] https://crrev.com/f5b22e073e0f8cb8e39e060cb661630ee8a8c8fa/DEPS


### gi...@appspot.gserviceaccount.com (2023-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1892c860e7979eecb119ff4bda8a92070fa7c5cf

commit 1892c860e7979eecb119ff4bda8a92070fa7c5cf
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jul 25 13:06:37 2023

Roll v8 11.4 from d7561b88d067 to 978934af4a29 (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/d7561b88d067..978934af4a29

2023-07-25 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.4.183.29
2023-07-25 manoskouk@chromium.org [wasm-gc] Use wasm-null as default value for wasm reference types

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-11-4-chromium-m114
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.4: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m114: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1466183
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I600d87ed10b1144478c3e0742f893ed36bc35e13
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4711900
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1517}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/1892c860e7979eecb119ff4bda8a92070fa7c5cf/DEPS


### wf...@chromium.org (2023-07-26)

[vrp panel] This a cool bug and a great report. Thank you from the panel!

### am...@google.com (2023-07-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-27)

Congratulations Jerry! The VRP Panel has decided to aware you $20,000 for this report & V8 exploit bonus + $2,000 bisect bonus + $1,000 patch bonus. Thank you for your efforts in discovering and reporting this issue and exploit to us as well as writing a patch that we used -- excellent work! 

### am...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-02)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-03)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-10-18)

Credit: 5f46f4ee2e17957ba7b39897fb376be8

### [Deleted User] (2023-10-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1466183?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1466187]
[Monorail components added to Component Tags custom field.]

### ap...@google.com (2024-02-23)

Project: v8/v8
Branch: main

commit 1a114815001332b0d7fc7bff179e889fcb58ff99
Author: Manos Koukoutos <manoskouk@chromium.org>
Date:   Fri Feb 23 16:50:59 2024

    [wasm-gc] Add missing test for security bug
    
    Bug: chromium:1466183
    Change-Id: I38a56f75d166fac7d64290c71bf4c0bac5515ca7
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5319507
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
    Commit-Queue: Manos Koukoutos <manoskouk@chromium.org>
    Auto-Submit: Manos Koukoutos <manoskouk@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#92514}

A       test/mjsunit/regress/wasm/regress-1466183.js

https://chromium-review.googlesource.com/5319507


---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067712)*

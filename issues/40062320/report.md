# Debug check failed: value.IsForeign().

| Field | Value |
|-------|-------|
| **Issue ID** | [40062320](https://issues.chromium.org/issues/40062320) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>WebAssembly |
| **Platforms** | Linux, Mac |
| **Reporter** | qp...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2022-12-18 |
| **Bounty** | $7,000.00 |

## Description

Version: 11.0.0 (candidate) bfb41bd6eef20577d3057e8428d753ddd0ce2977  

OS: Linux  

Architecture: x64

poc

```
function __f_0(__v_0) {  
  console.trace(Intl, 138982, "/0/", -9007199254740992, 2147483649);  
}  
  
function __f_1(__v_1, __v_2) {  
  'use asm';  
  
  var __v_3 = __v_2.print_stack;  
  
  function __f_2() {  
    var __v_4 = 0;  
  
    while ((__v_4 | 0) < 10) {  
      __v_3(1);  
    }  
  }  
  
  return __f_2;  
}  
  
__f_1({}, {  
  'print_stack': __f_0  
})();  

```

**What steps will reproduce the problem?**

$ ./out/x64.debug/d8 poc.js

**What is the expected output?**

**What do you see instead?**

# 

# Fatal error in gen/torque-generated/src/objects/js-objects-tq-inl.inc, line 34

# Check failed: !v8::internal::v8\_flags.enable\_slow\_asserts || (IsJSReceiver\_NonInline(\*this)).

# 

# 

# 

#FailureMessage Object: 0x7fffffffb9d0  

==== C stack trace ===============================

```
/home/haein/v8-latest/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7ffff7fdfe4e]  
/home/haein/v8-latest/v8/out/x64.debug/libv8_libplatform.so(+0x4b24d) [0x7ffff7f3524d]  
/home/haein/v8-latest/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const\*, int, char const\*, ...)+0x16f) [0x7ffff7fae91f]  
./out/x64.debug/d8(v8::internal::TorqueGeneratedJSReceiver<v8::internal::JSReceiver, v8::internal::HeapObject>::TorqueGeneratedJSReceiver(unsigned long)+0x97) [0x5555556ac107]  
./out/x64.debug/d8(v8::internal::JSReceiver::JSReceiver(unsigned long)+0x1d) [0x5555556b71fd]  
./out/x64.debug/d8(v8::internal::TorqueGeneratedJSObject<v8::internal::JSObject, v8::internal::JSReceiver>::TorqueGeneratedJSObject(unsigned long)+0x21) [0x5555556abfe1]  
./out/x64.debug/d8(v8::internal::JSObject::JSObject(unsigned long)+0x1d) [0x5555556abfad]  
/home/haein/v8-latest/v8/out/x64.debug/libv8.so(v8::internal::WasmInstanceObject::WasmInstanceObject(unsigned long)+0x21) [0x7ffff59c8901]  
/home/haein/v8-latest/v8/out/x64.debug/libv8.so(v8::internal::WasmInstanceObject::cast(v8::internal::Object)+0x21) [0x7ffff5aa7821]  
/home/haein/v8-latest/v8/out/x64.debug/libv8.so(v8::internal::WasmFrame::wasm_instance() const+0x50) [0x7ffff5b0c0d0]  
/home/haein/v8-latest/v8/out/x64.debug/libv8.so(v8::internal::WasmFrame::module_object() const+0x15) [0x7ffff5b0c065]  
/home/haein/v8-latest/v8/out/x64.debug/libv8.so(v8::internal::WasmFrame::script() const+0x15) [0x7ffff5b0bff5]  
/home/haein/v8-latest/v8/out/x64.debug/libv8.so(v8::internal::WasmFrame::Print(v8::internal::StringStream\*, v8::internal::StackFrame::PrintMode, int) const+0xe9) [0x7ffff5b0bc99]  
/home/haein/v8-latest/v8/out/x64.debug/libv8.so(+0x3211137) [0x7ffff5b27137]  
/home/haein/v8-latest/v8/out/x64.debug/libv8.so(v8::internal::Isolate::PrintStack(v8::internal::StringStream\*, v8::internal::Isolate::PrintStackMode)+0xcd) [0x7ffff5b24c6d]  
/home/haein/v8-latest/v8/out/x64.debug/libv8.so(v8::internal::Isolate::PrintStack(_IO_FILE\*, v8::internal::Isolate::PrintStackMode)+0xb8) [0x7ffff5b26f68]  
./out/x64.debug/d8(v8::D8Console::Trace(v8::debug::ConsoleCallArguments const&, v8::debug::ConsoleContext const&)+0x70) [0x55555562e600]  
/home/haein/v8-latest/v8/out/x64.debug/libv8.so(+0x2e6eae0) [0x7ffff5784ae0]  
/home/haein/v8-latest/v8/out/x64.debug/libv8.so(+0x2e6b84a) [0x7ffff578184a]  
/home/haein/v8-latest/v8/out/x64.debug/libv8.so(v8::internal::Builtin_ConsoleTrace(int, unsigned long\*, v8::internal::Isolate\*)+0x103) [0x7ffff5781573]  
[0x7fff7f96dd7f]  

```

**Please use labels and text to provide additional information.**

## Timeline

### cl...@chromium.org (2022-12-19)

Moved https://crbug.com/v8/13601 to now be https://crbug.com/chromium/1402270.

### cl...@chromium.org (2022-12-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-12-19)

Uploaded to Clusterfuzz as: https://clusterfuzz.com/testcase-detail/4871564538609664

### cl...@chromium.org (2022-12-19)

Detailed Report: https://clusterfuzz.com/testcase?key=4871564538609664

Fuzzer: None
Job Type: linux_d8_dbg
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  !v8::internal::v8_flags.enable_slow_asserts || (IsJSReceiver_NonInline(*this)) i
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_d8_dbg&revision=84940

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4871564538609664

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2022-12-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### [Deleted User] (2022-12-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-12-19)

Detailed Report: https://clusterfuzz.com/testcase?key=4871564538609664

Fuzzer: None
Job Type: linux_d8_dbg
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  !v8::internal::v8_flags.enable_slow_asserts || (IsJSReceiver_NonInline(*this)) i
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=82808:82809

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4871564538609664

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2022-12-19)

Bisects to c9c4908 [cleanup] Iterate WasmFrame and TypedFrame by Victor Gomes · 4 months ago


[Monorail components: Blink>JavaScript>WebAssembly]

### cl...@chromium.org (2022-12-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-12-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-12-19)

This crash occurs very frequently on mac platform and is likely preventing the fuzzer None from making much progress. Fixing this will allow more bugs to be found.

Marking this bug as a blocker for next Beta release.

If this is incorrect, please add the ClusterFuzz-Wrong label and remove the ReleaseBlock-Beta label.

### aj...@google.com (2022-12-19)

This looks like a High severity issue - please adjust if this is safe in release builds. 

### vi...@chromium.org (2022-12-21)

Tentative fix on https://chromium-review.googlesource.com/c/v8/v8/+/4118770

### cl...@chromium.org (2022-12-22)

Thanks for looking into this, Victor!
After some offline discussion, we came up with a more targetted solution: https://crrev.com/c/4116778

### gi...@appspot.gserviceaccount.com (2022-12-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/e17eee4894be67f715a7b2d7f17d8b69724f1cf8

commit e17eee4894be67f715a7b2d7f17d8b69724f1cf8
Author: Clemens Backes <clemensb@chromium.org>
Date: Thu Dec 22 08:43:42 2022

[wasm] Fix printing of wasm-to-js frames

After https://crrev.com/c/3859787 those frames would be printed like
standard Wasm frames, but in the place of the WasmInstanceObject, they
have a WasmApiFunctionRef object instead.
So special-case the {WasmToJsFrame::instance()} to load the instance
properly. Also special-case the {position()} accessor for imported
functions.

R=victorgomes@chromium.org

Bug: chromium:1402270
Change-Id: I39805805a50e7a73d7d8075c63c46bdf5a373a33
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4116778
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Clemens Backes <clemensb@chromium.org>
Reviewed-by: Victor Gomes <victorgomes@chromium.org>
Cr-Commit-Position: refs/heads/main@{#84993}

[modify] https://crrev.com/e17eee4894be67f715a7b2d7f17d8b69724f1cf8/src/compiler/backend/ia32/code-generator-ia32.cc
[modify] https://crrev.com/e17eee4894be67f715a7b2d7f17d8b69724f1cf8/src/diagnostics/objects-printer.cc
[add] https://crrev.com/e17eee4894be67f715a7b2d7f17d8b69724f1cf8/test/mjsunit/regress/asm/regress-1402270.js
[modify] https://crrev.com/e17eee4894be67f715a7b2d7f17d8b69724f1cf8/src/compiler/backend/x64/code-generator-x64.cc
[modify] https://crrev.com/e17eee4894be67f715a7b2d7f17d8b69724f1cf8/src/execution/frames.cc
[modify] https://crrev.com/e17eee4894be67f715a7b2d7f17d8b69724f1cf8/src/execution/frames.h
[modify] https://crrev.com/e17eee4894be67f715a7b2d7f17d8b69724f1cf8/src/compiler/backend/arm/code-generator-arm.cc
[modify] https://crrev.com/e17eee4894be67f715a7b2d7f17d8b69724f1cf8/src/compiler/backend/arm64/code-generator-arm64.cc


### cl...@chromium.org (2022-12-22)

ClusterFuzz testcase 4871564538609664 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=84992:84993

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-12-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-23)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1402270&entry.364066060=External&entry.958145677=Linux&entry.958145677=Mac&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript,Blink>JavaScript>WebAssembly&entry.975983575=clemensb@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-01-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2023-01-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-27)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M111. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge approved: your change passed merge requirements and is auto-approved for M111. Please go ahead and merge the CL to branch 5563 (refs/branch-heads/5563) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-01-27)

The fix landed on December 22, right after the M-110 branch. So it's in M-111 already. Removing merge approval.

We should merge to M-110 instead, which will be the next extended stable.

### [Deleted User] (2023-01-27)

Merge review required: M110 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-01-27)

I'm not sure whey the bot can't see the commit on this, especially as the this bug is linked in the CL. Thank you clemensb@ for tagging this for backmerge to M110 as that is definitely appropriate for this one. 
Please go ahead and merge to 11.0-lkgr at your earliest convenience so this fix can be included in M110/Stable cut on Tuesday. TY! 

### am...@chromium.org (2023-01-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-30)

Prepared merge: https://crrev.com/c/4204087

### gi...@appspot.gserviceaccount.com (2023-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/2231850b6598a2e2d2568b2202c6b845c9d6569e

commit 2231850b6598a2e2d2568b2202c6b845c9d6569e
Author: Clemens Backes <clemensb@chromium.org>
Date: Thu Dec 22 08:43:42 2022

Merged: [wasm] Fix printing of wasm-to-js frames

After https://crrev.com/c/3859787 those frames would be printed like
standard Wasm frames, but in the place of the WasmInstanceObject, they
have a WasmApiFunctionRef object instead.
So special-case the {WasmToJsFrame::instance()} to load the instance
properly. Also special-case the {position()} accessor for imported
functions.

R=victorgomes@chromium.org

(cherry picked from commit e17eee4894be67f715a7b2d7f17d8b69724f1cf8)
Bug: chromium:1402270

Change-Id: I0a287afbf14dd64edb859c6407ce7c0a3d159023
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4204087
Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
Reviewed-by: Victor Gomes <victorgomes@chromium.org>
Commit-Queue: Clemens Backes <clemensb@chromium.org>
Reviewed-by: Maya Lekova <mslekova@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.0@{#24}
Cr-Branched-From: 06097c6f0c5af54fd5d6965d37027efb72decd4f-refs/heads/11.0.226@{#1}
Cr-Branched-From: 6bf3344f5d9940de1ab253f1817dcb99c641c9d3-refs/heads/main@{#84857}

[modify] https://crrev.com/2231850b6598a2e2d2568b2202c6b845c9d6569e/src/compiler/backend/ia32/code-generator-ia32.cc
[modify] https://crrev.com/2231850b6598a2e2d2568b2202c6b845c9d6569e/src/diagnostics/objects-printer.cc
[add] https://crrev.com/2231850b6598a2e2d2568b2202c6b845c9d6569e/test/mjsunit/regress/asm/regress-1402270.js
[modify] https://crrev.com/2231850b6598a2e2d2568b2202c6b845c9d6569e/src/execution/frames.cc
[modify] https://crrev.com/2231850b6598a2e2d2568b2202c6b845c9d6569e/src/compiler/backend/x64/code-generator-x64.cc
[modify] https://crrev.com/2231850b6598a2e2d2568b2202c6b845c9d6569e/src/execution/frames.h
[modify] https://crrev.com/2231850b6598a2e2d2568b2202c6b845c9d6569e/src/compiler/backend/arm/code-generator-arm.cc
[modify] https://crrev.com/2231850b6598a2e2d2568b2202c6b845c9d6569e/src/compiler/backend/arm64/code-generator-arm64.cc


### gi...@appspot.gserviceaccount.com (2023-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/87e2a8350307bd70848628b50d2da4c3c93827e8

commit 87e2a8350307bd70848628b50d2da4c3c93827e8
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Jan 30 18:23:55 2023

Roll v8 11.0 from 264676c3b788 to dc183b6f8195 (3 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/264676c3b788..dc183b6f8195

2023-01-30 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.13
2023-01-30 thibaudm@chromium.org Merged: [gap-resolver] Emit move based on destination representation
2023-01-30 clemensb@chromium.org Merged: [wasm] Fix printing of wasm-to-js frames

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-chromium-release-1
Please CC v8-waterfall-sheriff@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.0: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m110: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1402270,chromium:1407571
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I09c6e366347c0a0bd350199ba259ffb784a2a4cf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4204269
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5481@{#801}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/87e2a8350307bd70848628b50d2da4c3c93827e8/DEPS


### am...@chromium.org (2023-02-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-06)

Hello OP/ reporter! I'm realizing now I did not immediately follow up regarding your VRP reward - apologies for that and very belated congratulations. Finance is already processing your VRP reward, so you should have heard from them already. Thank you again for the report!
This fix will be included in tomorrow's M110 release. Please let me know the name or identifier you would like us to use in acknowledging you for this finding. Thank you! 

### qp...@gmail.com (2023-02-07)

[Comment Deleted]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-03-30)

This issue was migrated from crbug.com/chromium/1402270?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>WebAssembly]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062320)*

# memory corruption in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [40062087](https://issues.chromium.org/issues/40062087) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2022-12-07 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os:  

ubuntu 22.04

tested chrome version:  

Chromium 110.0.5449.0  

Chromium 110.0.5463.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1080161.zip)

./chrome crash.html

**Problem Description:**  

The code in problem has no asan instrumented, and I haven't done a detailed analysis yet.  

Received signal 11 SEGV\_ACCERR 7d9393000020  

#0 0x55b2e5630927 in backtrace /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/../sanitizer\_common/sanitizer\_common\_interceptors.inc:4434:13  

#1 0x55b2f766996c in base::debug::CollectStackTrace(void\*\*, unsigned long) ./../../base/debug/stack\_trace\_posix.cc:894:7  

#2 0x55b2f73b00a2 in StackTrace ./../../base/debug/stack\_trace.cc:221:12  

#3 0x55b2f73b00a2 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack\_trace.cc:218:28  

#4 0x55b2f766830e in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo\_t\*, void\*) ./../../base/debug/stack\_trace\_posix.cc:387:3  

#5 0x7fca22a7c520 in \_\_GI\_\_\_sigaction :?  

#6 0x55b2eb0b56b8 in \_\_cxx\_atomic\_load<int> ./../../buildtools/third\_party/libc++/trunk/include/atomic:948:12  

#7 0x55b2eb0b56b8 in load ./../../buildtools/third\_party/libc++/trunk/include/atomic:1537:17  

#8 0x55b2eb0b56b8 in atomic\_load\_explicit<int> ./../../buildtools/third\_party/libc++/trunk/include/atomic:1916:17  

#9 0x55b2eb0b56b8 in Relaxed\_Load ./../../v8/src/base/atomicops.h:237:10  

#10 0x55b2eb0b56b8 in Relaxed\_Load<unsigned int> ./../../v8/src/base/atomic-utils.h:87:9  

#11 0x55b2eb0b56b8 in Relaxed\_Load\_Map\_Word ./../../v8/src/objects/tagged-field-inl.h:126:26  

#12 0x55b2eb0b56b8 in map\_word ./../../v8/src/objects/objects-inl.h:919:10  

#13 0x55b2eb0b56b8 in map ./../../v8/src/objects/objects-inl.h:809:10  

#14 0x55b2eb0b56b8 in IsFixedArray ./../../v8/src/objects/instance-type-inl.h:134:1  

#15 0x55b2eb0b56b8 in v8::internal::ConstantPoolPointerForwarder::IterateConstantPool(v8::internal::FixedArray) ./../../v8/src/codegen/compiler.cc:1940:20  

#16 0x55b2eb08b8b1 in IterateAndForwardPointers ./../../v8/src/codegen/compiler.cc:1928:7  

#17 0x55b2eb08b8b1 in v8::internal::BackgroundMergeTask::BeginMergeInBackground(v8::internal::LocalIsolate\*, v8::internal::Handle[v8::internal::Script](javascript:void(0);)) ./../../v8/src/codegen/compiler.cc:2079:15  

#18 0x55b2eb08f5e1 in v8::internal::BackgroundCompileTask::FinalizeScript(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::String](javascript:void(0);), v8::internal::ScriptDetails const&, v8::internal::MaybeHandle[v8::internal::Script](javascript:void(0);)) ./../../v8/src/codegen/compiler.cc:2186:11  

#19 0x55b2eb0aace7 in v8::internal::Compiler::GetSharedFunctionInfoForStreamedScript(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::String](javascript:void(0);), v8::internal::ScriptDetails const&, v8::internal::ScriptStreamingData\*) ./../../v8/src/codegen/compiler.cc:3754:26  

#20 0x55b2eacc796f in CompileStreamedSource ./../../v8/src/api/api.cc:2932:10  

#21 0x55b2eacc796f in v8::ScriptCompiler::Compile(v8::Local[v8::Context](javascript:void(0);), v8::ScriptCompiler::StreamedSource\*, v8::Local[v8::String](javascript:void(0);), v8::ScriptOrigin const&) ./../../v8/src/api/api.cc:2948:7  

#22 0x55b3043c38f5 in blink::(anonymous namespace)::CompileScriptInternal(v8::Isolate\*, blink::ScriptState\*, blink::ClassicScript const&, v8::ScriptOrigin, v8::ScriptCompiler::CompileOptions, v8::ScriptCompiler::NoCacheReason, absl::optional[blink::inspector\_compile\_script\_event::V8ConsumeCacheResult](javascript:void(0);)\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:134:14  

#23 0x55b3043c2cf9 in blink::V8ScriptRunner::CompileScript(blink::ScriptState\*, blink::ClassicScript const&, v8::ScriptOrigin, v8::ScriptCompiler::CompileOptions, v8::ScriptCompiler::NoCacheReason) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:249:12  

#24 0x55b3043c907f in blink::V8ScriptRunner::CompileAndRunScript(blink::ScriptState\*, blink::ClassicScript\*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:513:9  

#25 0x55b3066db32b in blink::ClassicScript::RunScriptOnScriptStateAndReturnValue(blink::ScriptState\*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third\_party/blink/renderer/core/script/classic\_script.cc:217:10  

#26 0x55b30672ab03 in blink::Script::RunScriptOnScriptState(blink::ScriptState\*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third\_party/blink/renderer/core/script/script.cc:31:17  

#27 0x55b30672b028 in blink::Script::RunScript(blink::LocalDOMWindow\*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third\_party/blink/renderer/core/script/script.cc:38:3  

#28 0x55b3067453f1 in blink::PendingScript::ExecuteScriptBlockInternal(blink::Script\*, blink::ScriptElementBase\*, bool, bool, bool, base::TimeTicks, bool) ./../../third\_party/blink/renderer/core/script/pending\_script.cc:291:13  

#29 0x55b30674492b in blink::PendingScript::ExecuteScriptBlock() ./../../third\_party/blink/renderer/core/script/pending\_script.cc:188:3  

#30 0x55b306730038 in blink::ScriptLoader::PrepareScript(blink::ScriptLoader::ParserBlockingInline

**Additional Comments:**

\*\*Chrome version: \*\* 110.0.5449.0 \*\*Channel: \*\* Dev

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 332 B)
- [sig11.log](attachments/sig11.log) (text/plain, 28.1 KB)
- [asan-110.txt](attachments/asan-110.txt) (text/plain, 28.5 KB)

## Timeline

### [Deleted User] (2022-12-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-12-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6246853357273088.

### ad...@google.com (2022-12-07)

Reproduced manually on the first try with asan-linux-release-1077380 (M110). Does not reproduce with asan-linux-release-1070086 (M109)

### cl...@chromium.org (2022-12-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5981865820487680.

### ad...@google.com (2022-12-07)

I'll have one more crack at reproducing this on ClusterFuzz, feeding it a precise revision to test, in the hopes that it can reproduce it and bisect it.

[Monorail components: Blink>JavaScript>Compiler]

### [Deleted User] (2022-12-07)

[Empty comment from Monorail migration]

### ad...@google.com (2022-12-07)

ClusterFuzz still unable to reproduce for some reason.

Attached is the symbolized stack trace I get on 110 - for completeness - it seems to be identical to the above.

tebbi@ could you take this from here?

Can this be used to achieve heap corruption in the renderer? Or do we reliably just hit an assertion and kill the renderer? I'm going to assume the former and set Security_Severity=High, but if it's the latter, please flip this to type=Bug.

### cl...@chromium.org (2022-12-07)

ClusterFuzz testcase 5981865820487680 is closed as invalid, so closing issue.

### te...@chromium.org (2022-12-07)

This crashes in BackgroundMergeTask, which is a rather new feature. Seth or Leszek, could you take a look?

### [Deleted User] (2022-12-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-07)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-07)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### se...@microsoft.com (2022-12-07)

Thanks for reporting this failure! I've uploaded a CL with a fix: https://chromium-review.googlesource.com/c/v8/v8/+/4087502 . This is a type confusion bug: AsmWasmData is being treated as InterpreterData. I'm not entirely sure, but I imagine someone might be able to use this to read or write data within the V8 pointer cage.

### le...@chromium.org (2022-12-07)

Thanks for the quick fix Seth!

### gi...@appspot.gserviceaccount.com (2022-12-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/50e1f89faf79d07ae8f893b1678bdf94aa474a4b

commit 50e1f89faf79d07ae8f893b1678bdf94aa474a4b
Author: Seth Brenith <seth.brenith@microsoft.com>
Date: Wed Dec 07 22:51:09 2022

is_compiled doesn't mean HasBytecodeArray

A SharedFunctionInfo might have AsmWasmData instead of BytecodeArray and
it would be considered compiled. Code using GetBytecodeArray should
check specifically for the presence of a bytecode array.

Bug: chromium:1397348
Change-Id: I1e376da8ac59204afdcc012e1cb068766be75eb7
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4087502
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Seth Brenith <seth.brenith@microsoft.com>
Cr-Commit-Position: refs/heads/main@{#84716}

[modify] https://crrev.com/50e1f89faf79d07ae8f893b1678bdf94aa474a4b/src/codegen/compiler.cc


### le...@chromium.org (2022-12-13)

emilykim8708, can you still reproduce with 110.0.5473.0?

### em...@gmail.com (2022-12-13)

I tested it in two ways. The first one is to use the patch above. Second, download the latest version(Chromium 110.0.5476.0 - gs://chromium-browser-asan/linux-release/asan-linux-release-1082318.zip)

After testing, I can confirm that the issue has not reproduced again.

### le...@chromium.org (2022-12-13)

Excellent, thanks for verifying!

### [Deleted User] (2022-12-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-17)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M110. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge approved: your change passed merge requirements and is auto-approved for M110. Please go ahead and merge the CL to branch 5481 (refs/branch-heads/5481) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-21)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-26)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@chromium.org (2023-01-02)

This is already in M110

### am...@google.com (2023-01-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-04)

Congratulations, Cassidy Kim! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1397348?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062087)*

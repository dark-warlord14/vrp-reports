# use-after-poison in blink::CollectChildrenAndRemoveFromOldParent

| Field | Value |
|-------|-------|
| **Issue ID** | [40069958](https://issues.chromium.org/issues/40069958) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2023-08-18 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os: ubuntu 22.04  

tested chrome version:  

(Chromium 118.0.5955.0) gs://chromium-browser-asan/linux-release/asan-linux-release-1185022.zip  

Chromium 118.0.5951.0  

./chrome --enable-blink-test-features --user-data-dir=/tmp/xx9 <http://localhost:8000/poc.html>

Immediately reproduce UAP.  

The poc code is very simple and easy to reproduce. I think it is very likely that it has been discovered internally.  

Because I haven't found the fix for the latest CL, I submitted it.  

Sorry to bother you if it's a known issue.  

Thanks.

**Problem Description:**  

==1060109==ERROR: AddressSanitizer: use-after-poison on address 0x7e9900194410 at pc 0x559a65d5221a bp 0x7ffc7bc0f690 sp 0x7ffc7bc0f688  

WRITE of size 4 at 0x7e9900194410 thread T0 (chrome)  

#0 0x559a65d52219 in \_\_cxx\_atomic\_store<unsigned int> ./../../third\_party/libc++/src/include/\_\_atomic/cxx\_atomic\_impl.h:349:5  

#1 0x559a65d52219 in store ./../../third\_party/libc++/src/include/\_\_atomic/atomic\_base.h:52:7  

#2 0x559a65d52219 in StoreAtomic ./../../v8/include/cppgc/internal/member-storage.h:94:58  

#3 0x559a65d52219 in SetRawAtomic ./../../v8/include/cppgc/member.h:56:57  

#4 0x559a65d52219 in operator= ./../../v8/include/cppgc/member.h:232:11  

#5 0x559a65d52219 in SetCurrentNodeBeingRemoved ./../../third\_party/blink/renderer/core/dom/node\_move\_scope.h:50:33  

#6 0x559a65d52219 in blink::NodeMoveScope::SetCurrentNodeBeingRemoved(blink::Node&) ./../../third\_party/blink/renderer/core/dom/node\_move\_scope.h:134:20  

#7 0x559a65d3d78e in blink::CollectChildrenAndRemoveFromOldParent(blink::Node&, blink::HeapVector<cppgc::internal::BasicMember<blink::Node, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 11u>&, blink::ExceptionState&) ./../../third\_party/blink/renderer/core/dom/container\_node.cc:155:3  

#8 0x559a65d3d177 in blink::ContainerNode::AppendChild(blink::Node\*, blink::ExceptionState&) ./../../third\_party/blink/renderer/core/dom/container\_node.cc:933:8  

#9 0x559a66df63e1 in blink::(anonymous namespace)::v8\_node::AppendChildOperationCallbackForMainWorld(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_node.cc:528:39  

#10 0x559a4c8f2e92 in Builtins\_CallApiCallbackGeneric setup-isolate-deserialize.cc:0:0  

#11 0x559a4c8f0fa3 in Builtins\_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0  

#12 0x559a4c8f0fa3 in Builtins\_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0  

#13 0x559a4c8f0fa3 in Builtins\_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0  

#14 0x559a4c8f0fa3 in Builtins\_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0  

#15 0x559a4c8f0fa3 in Builtins\_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0  

#16 0x559a4c8f0fa3 in Builtins\_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0  

#17 0x559a4c8f0fa3 in Builtins\_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0  

#18 0x559a4c8f0fa3 in Builtins\_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0  

#19 0x559a4c8f1a01 in Builtins\_InterpreterPushArgsThenFastConstructFunction setup-isolate-deserialize.cc:0:0  

#20 0x559a4ca65566 in Builtins\_ConstructHandler setup-isolate-deserialize.cc:0:0  

#21 0x559a4c8f0fa3 in Builtins\_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0  

#22 0x559a4c8f0fa3 in Builtins\_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0  

#23 0x559a4c8eee5b in Builtins\_JSEntryTrampoline setup-isolate-deserialize.cc:0:0  

#24 0x559a4c8eeb86 in Builtins\_JSEntry setup-isolate-deserialize.cc:0:0  

#25 0x559a499b3f1e in Call ./../../v8/src/execution/simulator.h:178:12  

#26 0x559a499b3f1e in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:427:33  

#27 0x559a499b693a in v8::internal::Execution::CallScript(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);)) ./../../v8/src/execution/execution.cc:540:10  

#28 0x559a494f5e30 in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Data](javascript:void(0);)) ./../../v8/src/api/api.cc:2131:7  

#29 0x559a620639c1 in blink::V8ScriptRunner::RunCompiledScript(v8::Isolate\*, v8::Local[v8::Script](javascript:void(0);), v8::Local[v8::Data](javascript:void(0);), blink::ExecutionContext\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:409:22  

#30 0x559a620652d8 in blink::V8ScriptRunner::CompileAndRunScript(blink::ScriptState\*, blink::ClassicScript\*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:522:22  

#31 0x559a64d0ef67 in blink::ClassicScript::RunScriptOnScriptStateAndReturnValue(blink::ScriptState\*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third\_party/blink/renderer/core/script/classic\_script.cc:219:10  

#32 0x559a64d5d8c5 in blink::Script::RunScriptOnScriptState(blink::ScriptState\*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third\_party/blink/renderer/core/script/script.cc:36:17  

#33 0x559a64d5ddac in blink::Script::RunScript(blink::LocalDOMWindow\*, blink::ExecuteScriptPolicy, blink::V8ScriptRunner::RethrowErrorsOption) ./../../third\_party/blink/renderer/core/script/script.cc:43:3  

#34 0x559a64d78651 in blink::PendingScr

**Additional Comments:**

\*\*Chrome version: \*\* 118.0.5951.0 \*\*Channel: \*\* Dev

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 327 B)
- [asan.log](attachments/asan.log) (text/plain, 13.1 KB)

## Timeline

### [Deleted User] (2023-08-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-08-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5974606579695616.

### cl...@chromium.org (2023-08-18)

ClusterFuzz testcase 5974606579695616 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2023-08-18)

Detailed Report: https://clusterfuzz.com/testcase?key=5974606579695616

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Use-after-poison WRITE 4
Crash Address: 0x7e8300186708
Crash State:
  blink::CollectChildrenAndRemoveFromOldParent
  blink::ContainerNode::AppendChild
  blink::v8_node::AppendChildOperationCallbackForMainWorld
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1185232

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5974606579695616

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### [Deleted User] (2023-08-19)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### em...@gmail.com (2023-08-24)

any progress?

### am...@chromium.org (2023-09-05)

Thanks for the report, Cassidy Kim. This looks like Clusterfuzz, while reproducing was unable to triage. So triaging now, thanks for pinging in on this and apologies for the delay in response.
Looks like this was potentially introduced via https://crrev.com/c/4764270, assigning to masonf@ accordingly. 



### [Deleted User] (2023-09-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-05)

[Empty comment from Monorail migration]

[Monorail components: Blink>DOM]

### [Deleted User] (2023-09-06)

masonf: Uh oh! This issue still open and hasn't been updated in the last 19 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-06)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2023-09-11)

Based on the stack trace, this is a dupe of 1476784.

### em...@gmail.com (2023-09-12)

This issue id (1473990) is earlier than 1476784. Why is it dup?

### ma...@chromium.org (2023-09-14)

That's fair - I assume you're asking for bug bounty purposes? If so, I can dupe them the other way. I will definitely say that the POC is easier to understand on this bug than on the other one.

### ma...@chromium.org (2023-09-14)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-09-14)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-09-14)

Per the comments on the other one, I'm going to lower this to P-2 and Security_Severity-Low.

### [Deleted User] (2023-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-12-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3f014a9b1e7a0fd4214f9f1350ff42abf69ff612

commit 3f014a9b1e7a0fd4214f9f1350ff42abf69ff612
Author: Mason Freed <masonf@chromium.org>
Date: Thu Dec 21 23:59:43 2023

Remove Part tracking completely

While there was a flag (DOMPartsAPIActivePartTracking) to enable
or disable this behavior, there was overhead associated with tracking
that setting. This CL removes it entirely.

It also had bugs (see crbug.com/1473990).

Bug: 1453291
Fixed: 1473990
Change-Id: I8a5d7c8d49bbd65e7b85afcf702124e533fa4e6f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4915886
Reviewed-by: Joey Arhar <jarhar@chromium.org>
Auto-Submit: Mason Freed <masonf@chromium.org>
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1240385}

[modify] https://crrev.com/3f014a9b1e7a0fd4214f9f1350ff42abf69ff612/third_party/blink/renderer/platform/runtime_enabled_features.json5
[modify] https://crrev.com/3f014a9b1e7a0fd4214f9f1350ff42abf69ff612/third_party/blink/renderer/core/dom/child_node_part.cc
[delete] https://crrev.com/5b24eb3c6711dd91e3eba2fdf4149984dba61fb2/third_party/blink/renderer/core/dom/node_move_scope.cc
[modify] https://crrev.com/3f014a9b1e7a0fd4214f9f1350ff42abf69ff612/third_party/blink/renderer/core/dom/document_part_root.cc
[modify] https://crrev.com/3f014a9b1e7a0fd4214f9f1350ff42abf69ff612/third_party/blink/renderer/core/dom/part.cc
[modify] https://crrev.com/3f014a9b1e7a0fd4214f9f1350ff42abf69ff612/third_party/blink/renderer/core/dom/document.h
[modify] https://crrev.com/3f014a9b1e7a0fd4214f9f1350ff42abf69ff612/third_party/blink/renderer/core/dom/node.cc
[modify] https://crrev.com/3f014a9b1e7a0fd4214f9f1350ff42abf69ff612/third_party/blink/renderer/core/dom/part_root.cc
[modify] https://crrev.com/3f014a9b1e7a0fd4214f9f1350ff42abf69ff612/third_party/blink/renderer/core/dom/container_node.cc
[modify] https://crrev.com/3f014a9b1e7a0fd4214f9f1350ff42abf69ff612/third_party/blink/renderer/core/dom/build.gni
[modify] https://crrev.com/3f014a9b1e7a0fd4214f9f1350ff42abf69ff612/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/3f014a9b1e7a0fd4214f9f1350ff42abf69ff612/third_party/blink/renderer/core/dom/part.h
[modify] https://crrev.com/3f014a9b1e7a0fd4214f9f1350ff42abf69ff612/third_party/blink/renderer/core/dom/node.h
[delete] https://crrev.com/5b24eb3c6711dd91e3eba2fdf4149984dba61fb2/third_party/blink/renderer/core/dom/node_move_scope.h


### [Deleted User] (2023-12-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-28)

It looks like this issue was downgraded to from high severity based on the repro of the other report. This issue appears to have been reproed fairly easily and does not appear to be mitigated (with the exception of being behind a non-default flag, which does not impact severity) and is a UAF in the renderer, so elevating back to high severity. SI-None, since this code is behind a flag that is not default enabled. 

### am...@google.com (2024-01-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-03)

Congratulations Cassidy Kim! The Chrome VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! Happy New Year!

### am...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1473990?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1476784]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069958)*

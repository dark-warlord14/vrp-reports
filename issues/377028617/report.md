# Debug check failed: Handle<To> v8::internal::Cast(Handle<From>, const v8::SourceLocation &) [To = v8::internal::JSObject, From = v8::internal::Object]. in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [377028617](https://issues.chromium.org/issues/377028617) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | di...@chromium.org |
| **Created** | 2024-11-03 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 96877
    - link: https://crrev.com/4d2d8eecac7a636516c2b597bf3ff53738c80bc8 
- Commit Message

commit 4d2d8eecac7a636516c2b597bf3ff53738c80bc8
Author: Dominik Inführ <dinfuehr@chromium.org>
Date:   Tue Oct 29 12:54:03 2024 +0100

    [heap] Add --shared-heap flag
    
    This CL adds a new flag --shared-heap, which allows us to enable the
    shared heap without also enabling the shared string table or the
    shared structs. This will be useful for investigating
    "time-to-global-safepoint" metrics.
    
    Bug: 372493838
    Change-Id: I023e7ac0565cdff2fcc02adc2bd10e975fe15971
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5975436
    Reviewed-by: Patrick Thier <pthier@chromium.org>
    Reviewed-by: Victor Gomes <victorgomes@chromium.org>
    Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#96877}


## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-96945/d8 --allow-natives-syntax --harmony --shared-heap poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/init/bootstrapper.cc, line 5610
# Debug check failed: Handle<To> v8::internal::Cast(Handle<From>, const v8::SourceLocation &) [To = v8::internal::JSObject, From = v8::internal::Object].
#
#
#
#FailureMessage Object: 0x7ff0e9ffa290
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-96945/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7ff144ba9a73]
    /tmp/d8-linux-debug-v8-component-96945/libv8_libplatform.so(+0x1a05d) [0x7ff144b5305d]
    /tmp/d8-linux-debug-v8-component-96945/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x194) [0x7ff144b8b274]
    /tmp/d8-linux-debug-v8-component-96945/libv8_libbase.so(+0x2bc85) [0x7ff144b8ac85]
    /tmp/d8-linux-debug-v8-component-96945/libv8.so(v8::internal::Genesis::InitializeGlobal_js_atomics_pause()+0x159) [0x7ff1421ab4a9]
    /tmp/d8-linux-debug-v8-component-96945/libv8.so(v8::internal::Genesis::InitializeExperimentalGlobal()+0x2e) [0x7ff1421a930e]
    /tmp/d8-linux-debug-v8-component-96945/libv8.so(v8::internal::Genesis::Genesis(v8::internal::Isolate*, v8::internal::MaybeHandle<v8::internal::JSGlobalProxy>, v8::Local<v8::ObjectTemplate>, unsigned long, v8::internal::DeserializeEmbedderFieldsCallback, v8::MicrotaskQueue*)+0x8d5) [0x7ff1421bba05]
    /tmp/d8-linux-debug-v8-component-96945/libv8.so(v8::internal::Bootstrapper::CreateEnvironment(v8::internal::MaybeHandle<v8::internal::JSGlobalProxy>, v8::Local<v8::ObjectTemplate>, v8::ExtensionConfiguration*, unsigned long, v8::internal::DeserializeEmbedderFieldsCallback, v8::MicrotaskQueue*)+0x8d) [0x7ff14217de9d]
    /tmp/d8-linux-debug-v8-component-96945/libv8.so(v8::NewContext(v8::Isolate*, v8::ExtensionConfiguration*, v8::MaybeLocal<v8::ObjectTemplate>, v8::MaybeLocal<v8::Value>, unsigned long, v8::internal::DeserializeEmbedderFieldsCallback, v8::MicrotaskQueue*)+0xc36) [0x7ff141831106]
    /tmp/d8-linux-debug-v8-component-96945/libv8.so(v8::Context::New(v8::Isolate*, v8::ExtensionConfiguration*, v8::MaybeLocal<v8::ObjectTemplate>, v8::MaybeLocal<v8::Value>, v8::DeserializeInternalFieldsCallback, v8::MicrotaskQueue*, v8::DeserializeContextDataCallback, v8::DeserializeAPIWrapperCallback)+0x49) [0x7ff141831939]
    /tmp/d8-linux-debug-v8-component-96945/d8(v8::Shell::CreateEvaluationContext(v8::Isolate*)+0x1b8) [0x564f4f032148]
    /tmp/d8-linux-debug-v8-component-96945/d8(v8::Worker::ExecuteInThread()+0x291) [0x564f4f0380b1]
    /tmp/d8-linux-debug-v8-component-96945/d8(v8::Worker::WorkerThread::Run()+0x24) [0x564f4f037dd4]
    /tmp/d8-linux-debug-v8-component-96945/libv8_libbase.so(+0x49826) [0x7ff144ba8826]
    /lib/x86_64-linux-gnu/libc.so.6(+0x94ac3) [0x7ff13e894ac3]
    /lib/x86_64-linux-gnu/libc.so.6(+0x126850) [0x7ff13e926850]


## Other
Please note to include the flags --allow-natives-syntax --harmony --shared-heap for clusterfuzz classification.

VERSION
Tested on v8 version: 13.2.0 - 13.2.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-96945.zip
2. Run: d8 --allow-natives-syntax --harmony --shared-heap poc.js

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy) 

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 220 B)
- [poc.js](attachments/poc.js) (text/javascript, 218 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-11-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6668761473941504.

### ki...@gmail.com (2024-11-04)

Sorry, wrong POC. Uploading a fixed one.

### cl...@appspot.gserviceaccount.com (2024-11-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5433613755547648.

### 24...@project.gserviceaccount.com (2024-11-04)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-11-04)

Detailed Report: https://clusterfuzz.com/testcase?key=5433613755547648

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  Handle<To> v8::internal::Cast(Handle<From>, const v8::SourceLocation &) [To = v8
  v8::internal::Genesis::InitializeGlobal_js_atomics_pause
  v8::internal::Genesis::InitializeExperimentalGlobal
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=96876:96877

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5433613755547648

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sa...@google.com (2024-11-04)

Dominik, could you take a look?

### pe...@google.com (2024-11-04)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-11-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-11-04)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### di...@chromium.org (2024-11-04)

This does not affect production because it requires the flag --shared-heap.

### di...@chromium.org (2024-11-04)

It seems like the worker isolate doesn't find the "Atomics" field of the global object because "Atomics" is in the read-only space while the lookup has the "Atomics" string in the old space. For the main isolate the lookup "Atomics" string is also in the read-only space.

### di...@chromium.org (2024-11-07)

I've reverted the CL for now.

### am...@chromium.org (2024-11-08)

If the only issue here is that -shared-heap doesn't ship in production, this should remain at S1, but Security\_Impact-None, which I have added.
If there are other issues that reduce the actual exploitability or severity here, please add a note in that regard to explain the severity change specifically.

### sp...@google.com (2024-11-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process / the renderer + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-14)

Congratulations Zhenghang! Thank you for your efforts and reporting this issue to us -- nice work!

### ph...@google.com (2025-02-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/377028617)*

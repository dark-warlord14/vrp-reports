# V8 type confusion in FulfillPromise via double settlement of chrome.runtime.getPackageDirectoryEntry() Promise

| Field | Value |
|-------|-------|
| **Issue ID** | [513289241](https://issues.chromium.org/issues/513289241) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ga...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2026-05-14 |
| **Bounty** | $1,000.00 |

## Description

## VULNERABILITY DETAILS

`chrome.runtime.getPackageDirectoryEntry()` exposes a promise-returning extension binding path that passes an internal promise callback adaptor into `DirectoryEntry.getDirectory()`. An extension page can obtain a real `DirectoryEntry`, replace `DirectoryEntry.prototype.getDirectory`, and synchronously call the supplied success callback twice before the queued microtasks run.

The first success callback call passes a thenable. V8 queues a `PromiseResolveThenableJobTask`, while the target `JSPromise` is still pending. The second success callback call passes another value and resolves the same raw `v8::Promise::Resolver`. When the queued thenable job later runs, V8 attempts to fulfill the same promise again.

In release V8, `FulfillPromise` relies on a debug-only pending-state invariant before it unsafe-casts `promise.reactions_or_result` to a `PromiseReaction` list. After the second resolve, `reactions_or_result` contains the second resolve value instead of a reaction list. V8 then treats the JavaScript value as internal `PromiseReaction` data and crashes in `Builtins_FulfillPromise`.

The attached PoC demonstrates a renderer memory-safety crash in an official Google Chrome stable release build. The second resolve value is the JavaScript number `0x20a0a0a0`, whose tagged Smi representation is `0x41414140`. The release crash confirms that V8 dereferences `cage_base + 0x41414140 + 0x7` from `Builtins_FulfillPromise`.

This report does not claim a controlled read/write primitive or a V8 Sandbox bypass.

## VERSION

Chrome Version: `Google Chrome 148.0.7778.167` + stable

Chrome Build ID: `23b8fa1ce2d3b3613509b206bdd65be3b3f2f149`

Operating System: Ubuntu 24.04.3 LTS, Linux x64

## REPRODUCTION CASE

The CRX is signed with a fixed test key and has extension ID:

```
nbpgoaaffdflnihomombbeimnpfajhap

```

Official Google Chrome release blocks `--load-extension`, so the release repro uses the standard Linux external extension installation path for a CRX.

Steps:

1. Put the attached `ext.crx` at an absolute path, for example `/tmp/ext.crx`.
2. Register the CRX as an external extension:

```
sudo mkdir -p /usr/share/google-chrome/extensions
sudo tee /usr/share/google-chrome/extensions/nbpgoaaffdflnihomombbeimnpfajhap.json >/dev/null <<EOF
{
  "external_crx": "/tmp/ext.crx",
  "external_version": "0.1"
}
EOF

```

3. Start official stable Google Chrome with a fresh profile:

```
USER_DATA_DIR="$(mktemp -d)"
google-chrome-stable \
  --user-data-dir="$USER_DATA_DIR" \
  --no-first-run \
  --no-default-browser-check \
  --enable-logging=stderr \
  --v=1 \
  about:blank

```

4. The extension service worker opens `test.html` automatically on install.
5. The renderer crashes in `Builtins_FulfillPromise` after the second callback returns and the queued thenable job runs.
6. Cleanup after the test:

```
sudo rm -f /usr/share/google-chrome/extensions/nbpgoaaffdflnihomombbeimnpfajhap.json

```
## FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: renderer / tab

Crash State, symbolized with the public release debug-info package for `Google Chrome 148.0.7778.167`:

```
Crash reason:  SIGSEGV / SEGV_ACCERR
Crash address: 0x169b41414147

Thread 0 (crashed)
 0  chrome!Builtins_FulfillPromise + 0x41
    rdx = 0x0000169b41414140
    r14 = 0x0000169b00000000
    rip = 0x000063d80d26fa81
 1  chrome!Builtins_ResolvePromise + 0x44
 2  chrome!Builtins_PromiseCapabilityDefaultResolve + 0x3e
 3  chrome!Builtins_InterpreterEntryTrampoline + 0x143
 4  chrome!Builtins_PromiseResolveThenableJob + 0x216
 5  chrome!Builtins_RunMicrotasks + 0x459
 6  chrome!Builtins_JSRunMicrotasksEntry + 0xab
 7  chrome!v8::internal::(anonymous namespace)::Invoke(...) + 0x3c0
 8  chrome!v8::internal::(anonymous namespace)::InvokeWithTryCatch(...) + 0x62
 9  chrome!v8::internal::MicrotaskQueue::PerformCheckpointInternal(v8::Isolate*) + 0x23f
10  chrome!blink::V8ScriptRunner::CallFunction(...) + 0x732
11  chrome!blink::V8FunctionExecutor::Execute(...) + 0x164
12  chrome!blink::PausableScriptExecutor::ExecuteAndDestroySelf() + 0xff
13  chrome!blink::PausableScriptExecutor::CreateAndRun(...) + 0x334
14  chrome!blink::WebLocalFrameImpl::RequestExecuteV8Function(...) + 0x3d
15  chrome!extensions::ScriptContext::SafeCallFunction(...) + 0x2a2
16  chrome!extensions::ExtensionJSRunner::RunJSFunction(...) + 0x56
17  chrome!extensions::APIRequestHandler::AsyncResultHandler::CallCustomCallback(...) + 0x234
18  chrome!extensions::APIRequestHandler::AsyncResultHandler::ResolveRequest(...) + 0x2b4
19  chrome!extensions::APIRequestHandler::CompleteRequestImpl(...) + 0x1d3
20  chrome!extensions::APIRequestHandler::CompleteRequest(...) + 0x4d
21  chrome!extensions::APIBindingsSystem::CompleteRequest(...) + 0x29
22  chrome!extensions::NativeExtensionBindingsSystem::HandleResponse(...) + 0x9f
23  chrome!extensions::MainThreadIPCMessageSender::OnResponse(...) + 0x55

```

Fault address analysis:

```
r14 = 0x0000169b00000000   // V8 pointer-compression cage base
rdx = 0x0000169b41414140   // cage_base + tagged Smi 0x41414140
crash address = 0x169b41414147

```

Faulting instruction:

```
661ea81: cmpl $0x0, 0x7(%rdx)
661ea85: jne  0x661eb58
661ea8b: movl 0xf(%rdx), %ecx

```

The crash address is `rdx + 0x7`, matching a confused `PromiseReaction` field access after `promise.reactions_or_result` was overwritten by the second resolve value.

## CREDIT INFORMATION

Reporter credit: ggwhyp

## Attachments

- [loader.js](attachments/loader.js) (text/javascript, 231 B)
- [manifest.json](attachments/manifest.json) (application/json, 369 B)
- [test.html](attachments/test.html) (text/html, 115 B)
- [test.js](attachments/test.js) (text/javascript, 1.1 KB)
- [ext.crx](attachments/ext.crx) (application/octet-stream, 2.0 KB)

## Timeline

### is...@chromium.org (2026-05-18)

Thank you for the report! This is an issue indeed.

### ts...@google.com (2026-05-18)

Setting found-in to match extended stable to clear from our sheet.

### ts...@google.com (2026-05-18)

Setting OS to those that support extensions just to clear from our sheet.

### ch...@google.com (2026-05-19)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ch...@google.com (2026-05-19)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-05-19)

Project: v8/v8  

Branch:  main  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7857889>

[promise] Fix double-settlement issue in v8::Promise::Resolver

---


Expand for full commit details
```
     
    This CL adds JSPromise::is_native_resolver_invoked flag as an anti 
    double-settlement measure for native promises. This flag is never 
    used for JavaScript promises. 
     
    This is a simpler version of "promiseOrEmpty.[[Value]] is EMPTY" 
    related steps from the spec: 
      https://tc39.es/ecma262/#sec-createresolvingfunctions 
    Native promises do not require the full `promiseOrEmpty` capturing 
    machinery because their Api is limited and does not allow providing 
    custom executor for native promises. 
     
    Drive-by: 
     - cleanup definition of JSPromise flags, 
     - cleanup Api tests by moving GetData/MakeData helpers to test-api.h. 
     
    Fixes: 513289241 
     
    TAG=agy 
    CONV=d40e1b59-f716-4800-9f72-429924a60d7f 
     
    Change-Id: Icdff40c58aa7dfdc330e53b6ff8e2e2e1f6619d9 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7857889 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#107410}

```

---

Files:

- M `src/api/api.cc`
- M `src/builtins/promise-misc.tq`
- M `src/objects/js-promise-inl.h`
- M `src/objects/js-promise.h`
- M `src/objects/js-promise.tq`
- M `test/cctest/test-api-interceptors.cc`
- M `test/cctest/test-api.cc`
- M `test/cctest/test-api.h`

---

Hash: [5d91cd2961f8eb284edf3972b38501997fd60025](https://chromiumdash.appspot.com/commit/5d91cd2961f8eb284edf3972b38501997fd60025)  

Date: Mon May 18 22:35:02 2026


---

### is...@chromium.org (2026-05-19)

This is a security issue affecting extensions, thus lowering severity since it's an extensions only.

Speculatively adding merge requests while the fix is still yet to be tested in Canary.

### ch...@google.com (2026-05-19)

**M148** merge request created. **Please update [crbug/514588253](https://crbug.com/514588253) to have this merge reviewed.**

### ch...@google.com (2026-05-19)

**M149** merge request created. **Please update [crbug/514588069](https://crbug.com/514588069) to have this merge reviewed.**

### ml...@google.com (2026-05-19)

Memory corruption that requires a specific extension to be installed: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#medium-severity-s2-memory-safety>

### dx...@google.com (2026-05-26)

Project: v8/v8  

Branch:  refs/branch-heads/14.8  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7871074>

Merged: [promise] Fix double-settlement issue in v8::Promise::Resolver

---


Expand for full commit details
```
     
    This CL adds JSPromise::is_native_resolver_invoked flag as an anti 
    double-settlement measure for native promises. This flag is never 
    used for JavaScript promises. 
     
    This is a simpler version of "promiseOrEmpty.[[Value]] is EMPTY" 
    related steps from the spec: 
      https://tc39.es/ecma262/#sec-createresolvingfunctions 
    Native promises do not require the full `promiseOrEmpty` capturing 
    machinery because their Api is limited and does not allow providing 
    custom executor for native promises. 
     
    Drive-by: 
     - cleanup definition of JSPromise flags, 
     - cleanup Api tests by moving GetData/MakeData helpers to test-api.h. 
     
    Bug: 513289241 
    Fixed: 514588253 
     
    TAG=agy 
    CONV=d40e1b59-f716-4800-9f72-429924a60d7f 
     
    (cherry picked from commit 5d91cd2961f8eb284edf3972b38501997fd60025) 
     
    Change-Id: Icdff40c58aa7dfdc330e53b6ff8e2e2e1f6619d9 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7857889 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#107410} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7871074 
    Auto-Submit: Igor Sheludko <ishell@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.8@{#56} 
    Cr-Branched-From: f9659283a5f8d42b3c09228cf5df606fcaf47a3d-refs/heads/14.8.178@{#1} 
    Cr-Branched-From: 141232520dc4910401240c531db3af36910a0fd1-refs/heads/main@{#106240}

```

---

Files:

- M `src/api/api.cc`
- M `src/builtins/promise-misc.tq`
- M `src/objects/js-promise-inl.h`
- M `src/objects/js-promise.h`
- M `src/objects/js-promise.tq`
- M `test/cctest/test-api-interceptors.cc`
- M `test/cctest/test-api.cc`
- M `test/cctest/test-api.h`

---

Hash: [ed897690f5569a5bcc6a362affba5bb64ea410e2](https://chromiumdash.appspot.com/commit/ed897690f5569a5bcc6a362affba5bb64ea410e2)  

Date: Mon May 18 22:35:02 2026


---

### dx...@google.com (2026-05-26)

Project: v8/v8  

Branch:  refs/branch-heads/14.9  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7870939>

Merged: [promise] Fix double-settlement issue in v8::Promise::Resolver

---


Expand for full commit details
```
     
    This CL adds JSPromise::is_native_resolver_invoked flag as an anti 
    double-settlement measure for native promises. This flag is never 
    used for JavaScript promises. 
     
    This is a simpler version of "promiseOrEmpty.[[Value]] is EMPTY" 
    related steps from the spec: 
      https://tc39.es/ecma262/#sec-createresolvingfunctions 
    Native promises do not require the full `promiseOrEmpty` capturing 
    machinery because their Api is limited and does not allow providing 
    custom executor for native promises. 
     
    Drive-by: 
     - cleanup definition of JSPromise flags, 
     - cleanup Api tests by moving GetData/MakeData helpers to test-api.h. 
     
    Bug: 513289241 
    Fixed: 514588069 
     
    TAG=agy 
    CONV=d40e1b59-f716-4800-9f72-429924a60d7f 
     
    (cherry picked from commit 5d91cd2961f8eb284edf3972b38501997fd60025) 
     
    Change-Id: Icdff40c58aa7dfdc330e53b6ff8e2e2e1f6619d9 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7857889 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#107410} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7870939 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Igor Sheludko <ishell@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.9@{#30} 
    Cr-Branched-From: 8f08364a351ad38a60421137a09ef23953ecdd56-refs/heads/14.9.207@{#1} 
    Cr-Branched-From: 8de67b11924d5e8c0032029165a52d800cf05f1f-refs/heads/main@{#106999}

```

---

Files:

- M `src/api/api.cc`
- M `src/builtins/promise-misc.tq`
- M `src/objects/js-promise-inl.h`
- M `src/objects/js-promise.h`
- M `src/objects/js-promise.tq`
- M `test/cctest/test-api-interceptors.cc`
- M `test/cctest/test-api.cc`
- M `test/cctest/test-api.h`

---

Hash: [5e0db03588bc0387e025e9fc317f6b8c676a748e](https://chromiumdash.appspot.com/commit/5e0db03588bc0387e025e9fc317f6b8c676a748e)  

Date: Mon May 18 22:35:02 2026


---

### pe...@google.com (2026-05-26)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### is...@chromium.org (2026-05-26)

Re M144, this issue has been in V8 since forever.

### sp...@google.com (2026-05-27)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
ASAN Write, UAF. Other Processes - Renderer


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-07-10)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-07-10)

1. https://chromium-review.git.corp.google.com/c/v8/v8/+/8064245
2. Low - There was no conflict.
3. 148 and 149
4. Yes.

### dx...@google.com (2026-07-17)

Project: v8/v8  

Branch:  refs/branch-heads/14.4  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/8064245>

[M144-LTS][promise] Fix double-settlement issue in v8::Promise::Resolver

---


Expand for full commit details
```
[M144-LTS][promise] Fix double-settlement issue in v8::Promise::Resolver 
 
This CL adds JSPromise::is_native_resolver_invoked flag as an anti 
double-settlement measure for native promises. This flag is never 
used for JavaScript promises. 
 
This is a simpler version of "promiseOrEmpty.[[Value]] is EMPTY" 
related steps from the spec: 
  https://tc39.es/ecma262/#sec-createresolvingfunctions 
Native promises do not require the full `promiseOrEmpty` capturing 
machinery because their Api is limited and does not allow providing 
custom executor for native promises. 
 
Drive-by: 
 - cleanup definition of JSPromise flags, 
 - cleanup Api tests by moving GetData/MakeData helpers to test-api.h. 
 
Fixes: 513289241 
 
TAG=agy 
CONV=d40e1b59-f716-4800-9f72-429924a60d7f 
 
(cherry picked from commit 5d91cd2961f8eb284edf3972b38501997fd60025) 
 
Change-Id: Icdff40c58aa7dfdc330e53b6ff8e2e2e1f6619d9 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7857889 
Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
Commit-Queue: Igor Sheludko <ishell@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#107410} 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/8064245 
Reviewed-by: Igor Sheludko <ishell@chromium.org> 
Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
Cr-Commit-Position: refs/branch-heads/14.4@{#105} 
Cr-Branched-From: 80acc26727d5a34e77dabeebe7c9213ec1bd4768-refs/heads/14.4.258@{#1} 
Cr-Branched-From: ce7e597e90f6df3fa4b6df224bc613b80c635450-refs/heads/main@{#104020}

```

---

Files:

- M `src/api/api.cc`
- M `src/builtins/promise-misc.tq`
- M `src/objects/js-promise-inl.h`
- M `src/objects/js-promise.h`
- M `src/objects/js-promise.tq`
- M `test/cctest/test-api-interceptors.cc`
- M `test/cctest/test-api.cc`
- M `test/cctest/test-api.h`

---

Hash: [b2461e0071c88bb27c10ed4a83ef269b2048122b](https://chromiumdash.appspot.com/commit/b2461e0071c88bb27c10ed4a83ef269b2048122b)  

Date: Mon May 18 22:35:02 2026


---

### ch...@google.com (2026-08-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/513289241)*

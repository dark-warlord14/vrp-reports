# heap-use-after-free in blink::IdentityProvider::resolve

| Field | Value |
|-------|-------|
| **Issue ID** | [491869946](https://issues.chromium.org/issues/491869946) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Identity>FedCM |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | cb...@chromium.org |
| **Created** | 2026-03-12 |
| **Bounty** | $10,000.00 |

## Description

```
=================================================================
==62372==ERROR: AddressSanitizer: heap-use-after-free on address 0x12be97ae9630 at pc 0x7ff858f0742e bp 0x00e6035fe160 sp 0x00e6035fe1a8
READ of size 8 at 0x12be97ae9630 thread T0
    #0 0x7ff858f0742d in blink::IdentityProvider::resolve(class blink::ScriptState *, class blink::ScriptValue const &, class blink::IdentityResolveOptions const *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\credentialmanagement\identity_provider.cc:316:12
    #1 0x7ff85671195b in blink::`anonymous namespace'::v8_identity_provider::ResolveStaticOperationCallback C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\renderer\bindings\modules\v8\v8_identity_provider.cc:204:23
    #2 0x7ff85e5f3824 in Builtins_CallApiCallbackGeneric (C:\Users\Admin\Downloads\chrome-asan\chrome.dll+0x1ad4d3824)
    #3 0x7ff85e5f197b in Builtins_InterpreterEntryTrampoline (C:\Users\Admin\Downloads\chrome-asan\chrome.dll+0x1ad4d197b)
    ...
    #35 0x7ff845866613 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346:40
    #36 0x7ff8459d3607 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:42:55
    #37 0x7ff8458694ff in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:650:12
    #38 0x7ff84590ef5c in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:135:14

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\credentialmanagement\identity_provider.cc:316:12 in blink::IdentityProvider::resolve(class blink::ScriptState *, class blink::ScriptValue const &, class blink::IdentityResolveOptions const *)
Shadow bytes around the buggy address:
  0x12be97ae9380: f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa
  0x12be97ae9400: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x12be97ae9480: f7 fa 00 fa f7 fa fd fd f7 fa fd fa f7 fa fd fa
  0x12be97ae9500: f7 fa fd fa f7 fa 00 07 f7 fa fd fa f7 fa fd fa
  0x12be97ae9580: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa 00 fa
=>0x12be97ae9600: f7 fa fd fd f7 fa[fd]fd f7 fa fd fa f7 fa fd fa
  0x12be97ae9680: f7 fa fd fa f7 fa fd fd f7 fa fd fa f7 fa fd fa
  0x12be97ae9700: f7 fa fd fa f7 fa fd fa f7 fa 00 00 f7 fa fd fa
  0x12be97ae9780: f7 fa 00 00 f7 fa 00 00 f7 fa 00 00 f7 fa 00 fa
  0x12be97ae9800: f7 fa fd fd f7 fa fd fa f7 fa fd fa f7 fa fd fd
  0x12be97ae9880: f7 fa 00 fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==62372==ADDITIONAL INFO

==62372==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ff855e7d154 in blink::DOMTimer::DOMTimer(class blink::ExecutionContext &, class blink::ScheduledAction *, class base::TimeDelta, bool) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\scheduler\dom_timer.cc:343:27
    #1 0x7ff849446109 in IPC::ChannelAssociatedGroupController::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1138:13


Command line: `"C:\Users\Admin\Downloads\chrome-asan\chrome.exe" --type=renderer --no-pre-read-main-dll --start-stack-profiler --no-sandbox --file-url-path-alias="/gen=C:\Users\Admin\Downloads\chrome-asan\gen" --video-capture-use-gpu-memory-buffer --lang=en-US --device-scale-factor=1 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1773079218143692 --launch-time-ticks=197939893276 --metrics-shmem-handle=3844,i,15911451909191243047,11158795503653610499,2097152 --field-trial-handle=1940,i,1091808593593248265,3138818943078118960,262144 --variations-seed-version --pseudonymization-salt-handle=2108,i,7123884904703337945,13134237462315843116,4 --trace-process-track-uuid=3190708990997080739 --mojo-platform-channel-handle=3780 /prefetch:1`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==62372==END OF ADDITIONAL INFO

==62372==ABORTING

```
#### VERSION

148.0.7730.0 (Developer Build) (64-bit)

#### REPRODUCTION CASE

Build: [asan-win32-release\_x64-1598047](https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-1598047.zip?generation=1773274798874073&alt=media)

Run: `./chrome.exe --no-sandbox poc.html`

---

Reporter credit: Shaheen Fazim

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 27.7 KB)
- [poc.html](attachments/poc.html) (text/html, 567 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [exploit.md](attachments/exploit.md) (text/markdown, 7.3 KB)
- [poc-controlled-rip.html](attachments/poc-controlled-rip.html) (text/html, 2.8 KB)
- [proof-of-exploit.mp4](attachments/proof-of-exploit.mp4) (video/mp4, 28.9 MB)

## Timeline

### fa...@gmail.com (2026-03-12)

# Root Cause Analysis: Heap Use-After-Free in `blink::IdentityProvider::resolve`

## Summary

A Use-After-Free (UAF) vulnerability is present in `blink::IdentityProvider::resolve` when processing a user-controlled token object during Mojo communication. The underlying issue is that a raw pointer to a Mojo remote object (`FederatedAuthRequestProxy`) is held across an operation that allows arbitrary Javascript execution.

By passing an object with a custom getter, an attacker can detach the execution frame during conversion, triggering the destruction of the Mojo remote while maintaining a dangling pointer to it, resulting in a heap-use-after-free when the pointer is subsequently accessed.

## Problematic Code

The flawed code lies within [third\_party/blink/renderer/modules/credentialmanagement/identity\_provider.cc](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/credentialmanagement/identity_provider.cc;l=230;drc=a899c4fc3604107e663ee1f3de6e2a4b47bfbbe1), inside the `IdentityProvider::resolve` method:

```
ScriptPromise<IDLUndefined> IdentityProvider::resolve(
    ScriptState* script_state,
    const ScriptValue& token_value,
    const IdentityResolveOptions* options) {
  // ... (options parsing step)

  // [1] The C++ function grabs a raw pointer to a Mojo Proxy (`request`)
  // that manages the IPC connection to the browser process. This request proxy
  // is tied to the lifecycle of the Document context.
  auto* request =
      CredentialManagerProxy::From(script_state)->FederatedAuthRequest();

  std::unique_ptr<base::Value> token_base_value;
  if (RuntimeEnabledFeatures::FedCmNonStringTokenEnabled()) {
    std::unique_ptr<WebV8ValueConverter> converter =
        Platform::Current()->CreateWebV8ValueConverter();

    // [2] Synchronous JavaScript gets evaluated here! 
    // `token_value` was passed merely as `ScriptValue` (IDL type: `any`),
    // meaning its true extraction executes here and *inside* `resolve`.
    // The `FromV8Value` method walks the properties of the JS object, eventually 
    // running the malicious "getter" that tears down the iframe.
    token_base_value = converter->FromV8Value(token_value.V8Value(),
                                              script_state->GetContext());
    // ...
  } else {
    // ...
  }

  // [3] CRASH occurs here: the C++ execution assumes `request` is still alive.
  // Because the frame detached, the Mojo proxy is now freed (triggering a heap UAF).
  request->ResolveTokenRequest(
      account_id, std::move(*token_base_value),
      BindOnce(&OnResolveTokenRequest, WrapPersistent(resolver)));

  return promise;
}

```
## Vulnerability Details

The crash relies on a specific sequence of parameter handling, pointer initialization, and context destruction:

- **1. IDL Parameter Handling:** The second parameter in the JavaScript call (`options`) is strictly typed as a Dictionary IDL, meaning its conversion happens *before* reaching the vulnerable C++ routine. However, the first parameter (`token_value`) is specified as [type `any` in IDL](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/credentialmanagement/identity_provider.idl;l=39;drc=a899c4fc3604107e663ee1f3de6e2a4b47bfbbe1). This allows it to be passed untouched into the `resolve` function wrapped in a `ScriptValue`.
- **2. Raw Pointer Initialization:** Inside `IdentityProvider::resolve`, the C++ code fetches a [raw pointer](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/credentialmanagement/identity_provider.cc;l=245;drc=a899c4fc3604107e663ee1f3de6e2a4b47bfbbe1) to `mojom::blink::FederatedAuthRequest` via [`CredentialManagerProxy`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/credentialmanagement/credential_manager_proxy.cc;l=14-22;drc=a899c4fc3604107e663ee1f3de6e2a4b47bfbbe1). This pointer manages the IPC connection to the browser process and is intrinsically tied to the Document context's lifecycle.
- **3. Synchronous JavaScript Execution:** The function attempts to convert the user-provided `token_value` into a `base::Value` using [`WebV8ValueConverter::FromV8Value`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/credentialmanagement/identity_provider.cc;l=253;drc=a899c4fc3604107e663ee1f3de6e2a4b47bfbbe1). Because the object is user-controlled, an attacker can define a custom property getter. When `FromV8Value` enumerates the object's properties synchronously, it inadvertently calls back into this malicious JavaScript getter.
- **4. Context Destruction:** Inside the malicious getter, a call to `frame.remove()` is executed, which detaches the iframe and fires `ContextLifecycleObserver::NotifyContextDestroyed()`. The underlying `HeapMojoRemote` observes this teardown and frees the `FederatedAuthRequestProxy` memory block. At this moment, the locally cached [request pointer](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/credentialmanagement/identity_provider.cc;l=245;drc=a899c4fc3604107e663ee1f3de6e2a4b47bfbbe1) becomes a dangling pointer.
- **5. The Crash (UAF):** When the JavaScript engine yields control back to C++, the execution resumes and unknowingly attempts to use the freed raw pointer. Calling [`request->ResolveTokenRequest`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/credentialmanagement/identity_provider.cc;l=272;drc=a899c4fc3604107e663ee1f3de6e2a4b47bfbbe1) dereferences the dangling pointer, resulting in a heap-use-after-free crash.

## Suggested Fix

- **Re-order operations:** Defer fetching the [FederatedAuthRequest](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/credentialmanagement/credential_manager_proxy.cc;l=86-94;drc=a899c4fc3604107e663ee1f3de6e2a4b47bfbbe1) pointer until *after* the `base::Value` token conversion is strictly finished.
- **Validate Context:** Optionally, once `converter->FromV8Value` completes, explicitly check if the script context is still valid (`!script_state->ContextIsValid()`).
- **Safe failure:** If the context was destroyed and the frame was unloaded, the function should return early without resolving the token.

### dc...@chromium.org (2026-03-12)

Yikes, nice find. Not sure if we can add more warnings or make it clearer than v8 value conversion can have "interesting" side effects.

### ch...@google.com (2026-03-13)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-13)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### cb...@chromium.org (2026-03-13)

<https://chromium-review.googlesource.com/c/chromium/src/+/7665206> fixes this

### dx...@google.com (2026-03-16)

Project: chromium/src  

Branch:  main  

Author:  Christian Biesinger [cbiesinger@chromium.org](mailto:cbiesinger@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7665206>

[FedCM] Get the FederatedAuthRequest right before using it

---


Expand for full commit details
```
     
    And only get it if the context is (still) valid. 
     
    R=npm@chromium.org 
     
    Fixed: 491869946 
    Change-Id: I0552f07f7fbffc743a85f95a7026225987a55147 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7665206 
    Commit-Queue: Christian Biesinger <cbiesinger@chromium.org> 
    Reviewed-by: Nicolás Peña <npm@chromium.org> 
    Auto-Submit: Christian Biesinger <cbiesinger@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1599990}

```

---

Files:

- M `third_party/blink/renderer/modules/credentialmanagement/identity_provider.cc`
- A `third_party/blink/web_tests/external/wpt/fedcm/fedcm-authz/fedcm-resolve-side-effects.https.html`

---

Hash: [392c4d50d407236a3212d654cdea1fca202fd7ad](https://chromiumdash.appspot.com/commit/392c4d50d407236a3212d654cdea1fca202fd7ad)  

Date: Mon Mar 16 17:32:18 2026


---

### fa...@gmail.com (2026-03-17)

deleted

### ch...@google.com (2026-03-17)

Merge review required: M147 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-17)

Merge review required: M146 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### cb...@chromium.org (2026-03-17)

1. fixes a UAF security issue
2. <https://chromium-review.googlesource.com/7665206>
3. yes
4. no
5. n/a
6. no

### fa...@gmail.com (2026-03-18)

### Proof-of-Concept - Control Flow Hijack / RIP Control:

Debug (Pattern: 0x41414141):

```
Microsoft (R) Windows Debugger Version 10.0.29507.1001 AMD64
Copyright (c) Microsoft Corporation. All rights reserved.

CommandLine: "D:\browser\chromium\src\out\Release\chrome.exe" --no-sandbox --js-flags="--expose-gc" --user-data-dir="C:/Users/Admin/AppData/Local/Temp/CHROME-4568-8604" "file:///D:\browser\poc-controlled-rip.html"

...
6:101> sxe av; g
...

(3508.ec4): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
*** WARNING: Unable to verify checksum for D:\browser\chromium\src\out\Release\chrome.dll
00007ffe`d1e07051 4f8b1cd3        mov     r11,qword ptr [r11+r10*8] ds:010582fa`acc60500=????????????????
6:101> r rax
rax=4141414141414141
6:101> r
rax=4141414141414141 rbx=00004d0c006f0080 rcx=00004d0c006f0080
rdx=0000004cb89fc2a8 rsi=0000004cb89fc3f8 rdi=0000004cb89fc278
rip=00007ffed1e07051 rsp=0000004cb89fc228 rbp=0000016b010c8c55
 r8=0000004cb89fc258  r9=0000004cb89fc278 r10=0020a0a0a0a0a0a0
r11=00007df5a7c10000 r12=0000004cb89fc258 r13=00004d0c00538000
r14=00004d0c05f54ec0 r15=0000004cb89fc2c0
iopl=0         nv up ei pl nz na po cy
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010207
00007ffe`d1e07051 4f8b1cd3        mov     r11,qword ptr [r11+r10*8] ds:010582fa`acc60500=????????????????
6:101> db poi(@rbx) L40
0000016c`01581b00  41 41 41 41 41 41 41 41-41 41 41 41 41 41 41 41  AAAAAAAAAAAAAAAA
0000016c`01581b10  41 41 41 41 41 41 41 41-41 41 41 41 41 41 41 41  AAAAAAAAAAAAAAAA
0000016c`01581b20  41 41 41 41 41 41 41 41-41 41 41 41 41 41 41 41  AAAAAAAAAAAAAAAA
0000016c`01581b30  41 41 41 41 41 41 41 41-41 41 41 41 41 41 41 41  AAAAAAAAAAAAAAAA

```

Build (Release/args.gn):

```
is_debug = false
is_component_build = false
symbol_level = 1

```

### dr...@chromium.org (2026-03-18)

No crashes in Canary. Approved to merge to M146 and M147.

### go...@google.com (2026-03-19)

Please merge your change to M147 by 2:00 PM PT today so we can take it in for tomorrow's M147 beta release. Thank you.

### cb...@chromium.org (2026-03-20)

Apologies, I was mostly OOO yesterday

<https://chromium-review.git.corp.google.com/c/chromium/src/+/7686274>
and
<https://chromium-review.git.corp.google.com/c/chromium/src/+/7686841>

are in the CQ now

### dx...@google.com (2026-03-20)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Christian Biesinger [cbiesinger@chromium.org](mailto:cbiesinger@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7686274>

[m147][FedCM] Get the FederatedAuthRequest right before using it

---


Expand for full commit details
```
     
    And only get it if the context is (still) valid. 
     
    R=npm@chromium.org 
     
    (cherry picked from commit 392c4d50d407236a3212d654cdea1fca202fd7ad) 
     
    Fixed: 491869946 
    Change-Id: I0552f07f7fbffc743a85f95a7026225987a55147 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7665206 
    Commit-Queue: Christian Biesinger <cbiesinger@chromium.org> 
    Reviewed-by: Nicolás Peña <npm@chromium.org> 
    Auto-Submit: Christian Biesinger <cbiesinger@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1599990} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7686274 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#967} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `third_party/blink/renderer/modules/credentialmanagement/identity_provider.cc`
- A `third_party/blink/web_tests/external/wpt/fedcm/fedcm-authz/fedcm-resolve-side-effects.https.html`

---

Hash: [ed5a54975586d00237ce2d5a87722f6f38efd974](https://chromiumdash.appspot.com/commit/ed5a54975586d00237ce2d5a87722f6f38efd974)  

Date: Fri Mar 20 16:56:33 2026


---

### pe...@google.com (2026-03-20)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-03-20)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Christian Biesinger [cbiesinger@chromium.org](mailto:cbiesinger@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7686841>

[m146][FedCM] Get the FederatedAuthRequest right before using it

---


Expand for full commit details
```
     
    And only get it if the context is (still) valid. 
     
    R=npm@chromium.org 
     
    (cherry picked from commit 392c4d50d407236a3212d654cdea1fca202fd7ad) 
     
    Fixed: 491869946 
    Change-Id: I0552f07f7fbffc743a85f95a7026225987a55147 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7665206 
    Commit-Queue: Christian Biesinger <cbiesinger@chromium.org> 
    Reviewed-by: Nicolás Peña <npm@chromium.org> 
    Auto-Submit: Christian Biesinger <cbiesinger@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1599990} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7686841 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#2899} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/modules/credentialmanagement/identity_provider.cc`
- A `third_party/blink/web_tests/external/wpt/fedcm/fedcm-authz/fedcm-resolve-side-effects.https.html`

---

Hash: [b3466120102e6fef48afc689e328fbb9f35c9e75](https://chromiumdash.appspot.com/commit/b3466120102e6fef48afc689e328fbb9f35c9e75)  

Date: Fri Mar 20 16:57:51 2026


---

### cb...@chromium.org (2026-03-20)

1. no
2. no

This security issue was introduced in 143 with <https://crrev.com/c/7012967>

### qk...@google.com (2026-03-23)

Labeled `LTS-NotApplicable-138` because the bug was introduced in M143.

### pe...@google.com (2026-04-08)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-08)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7692296
2. Medium - There were a few conflicts.
3. 146 and 147
4. Yes. The bug was introduced in M143.

### an...@google.com (2026-04-10)

Merge approved for LTS-144.

### dx...@google.com (2026-04-16)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Christian Biesinger [cbiesinger@chromium.org](mailto:cbiesinger@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7692296>

[M144-LTS][FedCM] Get the FederatedAuthRequest right before using it

---


Expand for full commit details
```
     
    And only get it if the context is (still) valid. 
     
    R=npm@chromium.org 
     
    (cherry picked from commit 392c4d50d407236a3212d654cdea1fca202fd7ad) 
     
    Fixed: 491869946 
    Change-Id: I0552f07f7fbffc743a85f95a7026225987a55147 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7665206 
    Commit-Queue: Christian Biesinger <cbiesinger@chromium.org> 
    Reviewed-by: Nicolás Peña <npm@chromium.org> 
    Auto-Submit: Christian Biesinger <cbiesinger@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1599990} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7692296 
    Reviewed-by: Christian Biesinger <cbiesinger@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Michael Ershov <miersh@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4818} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `third_party/blink/renderer/modules/credentialmanagement/identity_provider.cc`
- A `third_party/blink/web_tests/external/wpt/fedcm/fedcm-authz/fedcm-resolve-side-effects.https.html`

---

Hash: [d90f79b0e547b845d5f711a2823581e2b1d21570](https://chromiumdash.appspot.com/commit/d90f79b0e547b845d5f711a2823581e2b1d21570)  

Date: Thu Apr 16 04:22:45 2026


---

### sp...@google.com (2026-05-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
High-quality report of demonstrated memory corruption. RCE / Memory Corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### fa...@gmail.com (2026-05-20)

Hi, kindly reevaluate this issue. I have demonstrated RIP control in [#comment12](https://issues.chromium.org/issues/491869946#comment12).

### fa...@gmail.com (2026-05-21)

I hope this can be considered under the older reward scheme (as its reported before the change), with a bounty similar to RIP control issues like <https://issues.chromium.org/issues/379516109> , <https://issues.chromium.org/issues/483569511>.

### jd...@google.com (2026-05-26)

Hi fazim.pentester@gmail.com,

This was awarded under the older reward scheme (as it was before the change).  After review of your reassessment request, the panel has decided that there is no change, reward remains as is.  Thank you for your contributions. 


### fa...@gmail.com (2026-05-26)

Hi, It seems to be a misunderstanding, as the exploit does work correctly. Could you please try again? I noticed that sometimes it lands on `0000000000000000`, but that day I successfully got `4141414141414141` and reported it quickly. Could you please give it a few tries, as I believe the exploit is still working on unpatched version (Windows 11)?

Today i tried again, I were able to land it at `4141414141414141`, One thing I noticed is that leaving the page hanging for a few seconds before switching to the console or debugger seems to help the exploit work, although I’m not entirely sure. Here are a few runs I have done using `cdbx64` on Windows, which makes reproduction easier.

#### Run 1 - `Successful`:

Command: `cdbx64 -c ".childdbg 1; sxn ibp; sxn epr" "D:\browser\chromium\src\out\Release\chrome.exe" --no-sandbox --js-flags="--expose-gc" --user-data-dir="C:/Users/Admin/AppData/Local/Temp/CHROME-4568-8604df" C:\Users\Admin\Downloads\poc-controlled-rip.html`

```
...
0:000> g
...
(98d4.fa70): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
*** WARNING: Unable to verify checksum for D:\browser\chromium\src\out\Release\chrome.dll
00007fff`11a07051 4f8b1cd3        mov     r11,qword ptr [r11+r10*8] ds:010582fa`9eb80500=????????????????
5:105> r
rax=4141414141414141 rbx=0000273c006cc0e0 rcx=0000273c006cc0e0
rdx=0000005a6e5fc1c8 rsi=0000005a6e5fc318 rdi=0000005a6e5fc198
rip=00007fff11a07051 rsp=0000005a6e5fc148 rbp=000001e0010c8c21
 r8=0000005a6e5fc178  r9=0000005a6e5fc198 r10=0020a0a0a0a0a0a0
r11=00007df599b30000 r12=0000005a6e5fc178 r13=0000273c0051c000
r14=0000273c05edf5c0 r15=0000005a6e5fc1e0
iopl=0         nv up ei pl nz na pe cy
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010207
00007fff`11a07051 4f8b1cd3        mov     r11,qword ptr [r11+r10*8] ds:010582fa`9eb80500=????????????????
5:105> db poi(@rbx) L40
000001e4`0157e000  41 41 41 41 41 41 41 41-41 41 41 41 41 41 41 41  AAAAAAAAAAAAAAAA
000001e4`0157e010  41 41 41 41 41 41 41 41-41 41 41 41 41 41 41 41  AAAAAAAAAAAAAAAA
000001e4`0157e020  41 41 41 41 41 41 41 41-41 41 41 41 41 41 41 41  AAAAAAAAAAAAAAAA
000001e4`0157e030  41 41 41 41 41 41 41 41-41 41 41 41 41 41 41 41  AAAAAAAAAAAAAAAA
5:105>
6:103> q

```
#### Run 2 - `Failed`:

Command: `cdbx64 -c ".childdbg 1; sxn ibp; sxn epr" "D:\browser\chromium\src\out\Release\chrome.exe" --no-sandbox --js-flags="--expose-gc" --user-data-dir="C:/Users/Admin/AppData/Local/Temp/CHROME-4568-8604df" C:\Users\Admin\Downloads\poc-controlled-rip.html`

```
...
0:000> g
...
(c748.da38): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
*** WARNING: Unable to verify checksum for D:\browser\chromium\src\out\Release\chrome.dll
chrome!blink::IdentityProvider::resolve+0x3e5:
00007ffd`f4b51e35 488b4020        mov     rax,qword ptr [rax+20h] ds:00000000`00000020=????????????????
6:115> r
rax=0000000000000000 rbx=00004c04006bb840 rcx=00002404a8463649
rdx=00004c0405f3a5c0 rsi=000000779fdfc578 rdi=000000779fdfc3f8
rip=00007ffdf4b51e35 rsp=000000779fdfc3b0 rbp=000001a5010c8c55
 r8=00007ffde7dea3e0  r9=00007ffde7dea3c0 r10=00000fffbc5afb02
r11=0000000000000004 r12=000000779fdfc3d8 r13=00004c040051c000
r14=00004c0405f3a5c0 r15=000000779fdfc440
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202
chrome!blink::IdentityProvider::resolve+0x3e5:
00007ffd`f4b51e35 488b4020        mov     rax,qword ptr [rax+20h] ds:00000000`00000020=????????????????
6:115> q

```
#### Run 3 - `Successful`:

Command: `cdbx64 -c ".childdbg 1; sxn ibp; sxn epr" "D:\browser\chromium\src\out\Release\chrome.exe" --no-sandbox --js-flags="--expose-gc" --user-data-dir="C:/Users/Admin/AppData/Local/Temp/CHROME-4568-8604dfd" C:\Users\Admin\Downloads\poc-controlled-rip.html`

```
...
0:000> g
...
(60a0.c28c): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
*** WARNING: Unable to verify checksum for D:\browser\chromium\src\out\Release\chrome.dll
00007fff`11a07051 4f8b1cd3        mov     r11,qword ptr [r11+r10*8] ds:010582fa`9eb80500=????????????????
6:113> r
rax=4141414141414141 rbx=00006c7c047e86a0 rcx=00006c7c047e86a0
rdx=00000099789fc6b8 rsi=00000099789fc808 rdi=00000099789fc688
rip=00007fff11a07051 rsp=00000099789fc638 rbp=000002f5010c8c21
 r8=00000099789fc668  r9=00000099789fc688 r10=0020a0a0a0a0a0a0
r11=00007df599b30000 r12=00000099789fc668 r13=00006c7c00548000
r14=00006c7c05f86fc0 r15=00000099789fc6d0
iopl=0         nv up ei pl nz na pe cy
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010207
00007fff`11a07051 4f8b1cd3        mov     r11,qword ptr [r11+r10*8] ds:010582fa`9eb80500=????????????????
6:113> q

```

Would it also be possible to give another chance to look into next week’s VRP panel? I have also attached a video as proof of working. Thank you and best regards.

### sp...@google.com (2026-06-08)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

no change, maximum award given for category, not a controlled a write

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-06-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/491869946)*

# V8 Sandbox Bypass: Wasm streaming compilation cache confusion via "double streaming"

| Field | Value |
|-------|-------|
| **Issue ID** | [452605804](https://issues.chromium.org/issues/452605804) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2025-10-16 |
| **Bounty** | $20,000.00 |

## Description

### VULNERABILITY DETAILS

#### Summary

V8 sandbox bypass by "double streaming" a single `v8::WasmStreaming`, breaking its state machine and allowing incompatible wire bytes vs. deserialized native module.

Yet another out-of-V8 V8 sandbox violations in the "consumer" side of the sandbox where V8 may execute consumer-side (in this case, Blink) callbacks multiple times, at unexpected states, or with unexpected values. I've alluded to these type of issues to a few security researchers & Chrome/V8 engineers for a while, and this is a concrete example.

#### Details

Wasm streaming compilation works by exposing to V8 `StreamFromResponseCallback()`, a callback to be called when a response is resolved and ready to be consumed by Blink. Under sandbox corruption V8 can call this function however many times its wants to, but Blink is unaware of this and assumes that this is only callable once - essentially breaking its state machine running under the assumption that `promise resolve -> callback -> ...` transitions only once. This results in a peculiar state where a single `v8::WasmStreaming` is served streaming data by two loaders, **each maintaining its own code caching state and wire bytes digest but piping wire bytes into the same `v8::WasmStreaming`**.

By using an attacker-controlled server to control the streaming of Wasm code, or simply using Service Workers to delay responses, we can realize the following exploit:

1. Create a streaming compilation from a potentially cached HTTP source (possibly served by a Service Worker)
   - Delay the response.
2. Extract its callback from the promise chain, then call it with a `Response` backed by an `ArrayBuffer`
   - We now have two providers that pipe in wire bytes into `WasmStreaming` (and thus its internal `StreamingDecoder`)
   - **Any data inserted by this provider does not affect digest computation of the first provider.**
     - Insert a fake Wasm module ending with a custom section header to ignore everything from HTTP source on Wasm module decoding.
3. Resume streaming compilation from the HTTP source
   - Digest "matches", module deserialized from cache.
   - `NativeModule` and its code is now inconsistent with `wire_bytes` and `WasmModule` (similar to [b/40057640](https://issues.chromium.org/issues/40057640))
     - Exploit with any type inconsistent calls from deserialized code (from cache) -> lazily-compiled code (from wire bytes), call an OOB function index, etc.

### VERSION

Chrome: Tested on `asan-v8-sandbox-testing-linux-release-1530881`.

### REPRODUCTION CASE

Attached as `poc.html` (together with `serviceworker.js` and `wasm-module-builder.js`, required to be at the same top-level path) which exploits this issue to trigger a fully arbitary write outside of the sandbox. Must be executed in trusted context where Service Worker is available. Run with e.g. `./chrome --js-flags=--sandbox-testing http://localhost:8080/poc.html`.

### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Sandbox violation

### CREDIT INFORMATION

Reporter credit: Seunghyun Lee (@0x10n) of CMU CSD / CyLab

## Attachments

- poc.html (text/html, 14.3 KB)
- serviceworker.js (text/javascript, 3.5 KB)
- wasm-module-builder.js (text/javascript, 76.7 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-10-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4958164562673664.

### ja...@chromium.org (2025-10-16)

[security shepherd]

Thanks for the bug report and clear writeup.

I tried this out on Canary-143 and Extended-140 but I think I'm missing something on the setup because I get the Sandbox isn't defined.

But, this seems plausible so I'm going to triage it as a sandbox bypass.

### ja...@google.com (2025-10-17)

[security shepherd]

Provisionally adding desktop platforms. Provisionally setting component to v8

### cl...@appspot.gserviceaccount.com (2025-10-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4916480562888704.

### 24...@project.gserviceaccount.com (2025-10-20)

Testcase 4916480562888704 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4916480562888704.

### cl...@chromium.org (2025-10-23)

The current plan is to change the caching API such that the embedder gets a view on the full wire bytes on `Finish()`, and can then decide to pass the serialized bytes.

The underlying issue that the `WasmStreaming` object can be reused / swapped is not really avoidable at this point, as it's stored on the JS heap via a `Managed`. Changing this would be a significant project, so we will harden against `WasmStreaming` swapping in V8 and Chrome instead.

### dx...@google.com (2025-10-23)

Project: v8/v8  

Branch:  main  

Author:  Clemens Backes [clemensb@chromium.org](mailto:clemensb@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7078551>

[wasm] Refactor caching API

---


Expand for full commit details
```
     
    This refactors the caching API. 
    Previously the serialized module bytes were set very early in streaming 
    compilation, and then a `bool` on the `Finish` calls specified whether 
    they can be considered valid. 
    Now the embedders only mark early that compiled module bytes are 
    available, and when finishing the stream they get access to the full 
    streamed wire bytes and can provide the actual serialized bytes. 
     
    This ensures that the embedder can check the actual wire bytes as V8 
    received them for deciding whether serialized bytes are usable. 
     
    R=jkummerow@chromium.org 
     
    Bug: 452605804 
    Change-Id: I8d77214163290161b2b85cb30c8303819bf278ed 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7078551 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Clemens Backes <clemensb@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#103319}

```

---

Files:

- M `include/v8-wasm.h`
- M `src/api/api.cc`
- M `src/wasm/streaming-decoder.cc`
- M `src/wasm/streaming-decoder.h`
- M `src/wasm/sync-streaming-decoder.cc`
- M `src/wasm/wasm-engine.cc`
- M `src/wasm/wasm-js.cc`
- M `test/cctest/wasm/test-compilation-cache.cc`
- M `test/cctest/wasm/test-streaming-compilation.cc`
- M `test/fuzzer/wasm/streaming.cc`
- M `test/unittests/api/api-wasm-unittest.cc`
- M `test/unittests/wasm/streaming-decoder-unittest.cc`
- M `test/unittests/wasm/wasm-compile-module.h`

---

Hash: [d1834d91d325e447435c06272d1da7cd01884427](https://chromiumdash.appspot.com/commit/d1834d91d325e447435c06272d1da7cd01884427)  

Date: Thu Oct 23 14:28:29 2025


---

### dx...@google.com (2025-10-24)

Project: chromium/src  

Branch:  main  

Author:  Clemens Backes [clemensb@chromium.org](mailto:clemensb@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7079290>

[v8][wasm] Use new caching API

---


Expand for full commit details
```
     
    This switches chromium to the new caching API introduced in 
    https://crrev.com/c/7078551. 
     
    This consolidates digest computation to a single place where the full 
    wire bytes are available, and hence avoid mismatch between the wire 
    bytes seen by V8 and the wire bytes seen by chromium (via swapping the 
    WasmStreaming object via in-sandbox corruption). 
     
    R=jkummerow@chromium.org 
     
    Bug: 452605804 
    Change-Id: I4cdd3538477c859eec38a3340aa96149d7a84c27 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7079290 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Clemens Backes <clemensb@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1534808}

```

---

Files:

- M `third_party/blink/renderer/bindings/core/v8/v8_wasm_response_extensions.cc`

---

Hash: [89a9043dce822e5ecdf7eb0b34adf9a6ebe14935](https://chromiumdash.appspot.com/commit/89a9043dce822e5ecdf7eb0b34adf9a6ebe14935)  

Date: Fri Oct 24 07:47:30 2025


---

### cl...@chromium.org (2025-10-24)

This is fixed by https://crrev.com/c/7079290.

In fact, the reproducer now runs into this FATAL error: `SetHasCompiledModuleBytes has to be called before OnBytesReceived` (because it uses the same `WasmStreaming` object twice).

### cl...@chromium.org (2025-10-24)

And I don't think that we should backmerge this rather big change (including new V8 API). It will be included in the M-143 release.

### ch...@google.com (2025-10-24)

This V8 bug has been marked as a release blocker. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### sp...@google.com (2025-11-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $20000.00 for this report.

Rationale for this decision:
v8 sandbox bypass with controllable write


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-01-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> v8 sandbox bypass with controllable write

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/452605804)*

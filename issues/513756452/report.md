# V8 Sandbox Escape via gin::PerContextData EmbedderDataTypeTag collision with Blink ScriptState

| Field | Value |
|-------|-------|
| **Issue ID** | [513756452](https://issues.chromium.org/issues/513756452) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Bindings |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sm...@gmail.com |
| **Assignee** | ah...@google.com |
| **Created** | 2026-05-16 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

V8 Sandbox Escape via gin::PerContextData EmbedderDataTypeTag collision with Blink ScriptState

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://github.com/chromium/chromium>

---

### The problem

#### Please describe the technical details of the vulnerability

`gin::PerContextData` and `blink::ScriptState` both store native C++ pointers in the same `v8::Context::embedder_data` array, protected by V8's `EmbedderDataTypeTag`. The two types are supposed to use different tags, but gin accidentally uses its slot index (`kGinPerContextDataIndex` = 1) as the tag instead of the dedicated `gin::kGinPerContextData` (= 2). Since Blink `ScriptState` also uses tag 1 (`gin::kBlinkScriptState`), V8's EPT type check cannot distinguish the two pointer types. The tag is checked during `GetAlignedPointerFromEmbedderData()` regardless of slot index, so an in-sandbox write that copies one slot's EPT handle into the other slot passes the tag check and C++ code accepts the confused pointer.

The PoC models the prerequisite in-sandbox corruption with the V8 memory corruption testing API. It locates `NativeContext.embedder_data`, reads the gin slot[1] and Blink slot[2] EPT handles, copies the gin handle into the Blink slot, then triggers `div.textContent` which forces Blink to read the 32-byte `gin::PerContextData` as an 80-byte `blink::ScriptState`. ASAN reports heap-use-after-free at `ScriptState::isolate_` (offset +16), MiraclePtr NOT PROTECTED.

Relevant source:

- <https://chromium.googlesource.com/chromium/src/+/ba94d9f045b88ec4b53cb27f7f21a33303ae4ea3/gin/public/gin_embedders.h#15>
- <https://chromium.googlesource.com/chromium/src/+/ba94d9f045b88ec4b53cb27f7f21a33303ae4ea3/gin/public/gin_embedders.h#25>
- <https://chromium.googlesource.com/chromium/src/+/ba94d9f045b88ec4b53cb27f7f21a33303ae4ea3/gin/per_context_data.cc#15>
- <https://chromium.googlesource.com/chromium/src/+/ba94d9f045b88ec4b53cb27f7f21a33303ae4ea3/gin/per_context_data.cc#22>
- <https://chromium.googlesource.com/chromium/src/+/ba94d9f045b88ec4b53cb27f7f21a33303ae4ea3/gin/per_context_data.cc#32>
- <https://chromium.googlesource.com/chromium/src/+/ba94d9f045b88ec4b53cb27f7f21a33303ae4ea3/third_party/blink/renderer/platform/bindings/script_state.cc#31>

The fix is to use `gin::kGinPerContextData` as the tag instead of `kGinPerContextDataIndex`:

```
// gin/per_context_data.cc — current (broken)
context->SetAlignedPointerInEmbedderData(kGinPerContextDataIndex, this,
                                         kGinPerContextDataIndex);
// fix
context->SetAlignedPointerInEmbedderData(kGinPerContextDataIndex, this,
                                         gin::kGinPerContextData);

```

test os:

```
 x86_64 ubuntu

```

build args:

```
target_cpu="x64"
is_asan=true
is_debug=false
is_component_build=false
symbol_level=1
v8_enable_memory_corruption_api=true
v8_enable_sandbox=true
is_lsan=false
dcheck_always_on=false

```

content\_shell command (produces asan.log):

```
ASAN_OPTIONS="detect_leaks=0:halt_on_error=0:symbolize=1" \
content_shell --no-sandbox --headless --ozone-platform=headless --disable-gpu \
  --js-flags="--sandbox-testing" --single-process --run-web-tests \
  "file:///<poc_directory>/gin_blink_ept_reverse_only.html"

```

gin\_unittests command (produces sandbox\_violation.log, requires per\_context\_data\_unittest.diff applied):

```
gin_unittests \
  --gtest_filter="*CanReachOutsideSandboxWrite*" \
  --gtest_also_run_disabled_tests \
  --single-process-tests

```
#### Impact analysis

After a renderer attacker obtains an in-sandbox V8 memory corruption primitive, the tag collision lets them swap EPT handles between gin `PerContextData` (32 bytes) and Blink `ScriptState` (80 bytes). Two independent proofs:

1. **content\_shell PoC** (`gin_blink_ept_reverse_only.html`): copies the gin handle into the Blink slot, then triggers `div.textContent` which forces Blink to read the 32-byte gin object as an 80-byte ScriptState. ASAN reports heap-use-after-free at offset +16 in a 64-byte freed region (`blink::V8UnionStringOrTrustedScript::DirectToV8`). **MiraclePtr Status: NOT PROTECTED** — the UAF remains exploitable.
2. **gin\_unittests write proof** (`per_context_data_unittest.diff`): demonstrates write at attacker-selected address `0x434343430000` with attacker-selected value `0x5151515151515151` outside the V8 sandbox. CrashFilter confirms: `## V8 sandbox violation detected!` with `erf=0x6` (WRITE).

---

### The cause

#### What version of Chrome have you found the security issue in?

149.0.7781.0 - dev (trunk build at ba94d9f045)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Sandbox Escape

#### How would you like to be publicly acknowledged for your report?

sm1ee, ksw9722

## Attachments

- [sandbox_violation.log](attachments/sandbox_violation.log) (application/octet-stream, 1.8 KB)
- [gin_blink_ept_reverse_only.html](attachments/gin_blink_ept_reverse_only.html) (text/html, 4.6 KB)
- [per_context_data_unittest.diff](attachments/per_context_data_unittest.diff) (application/octet-stream, 8.2 KB)
- [asan.log](attachments/asan.log) (application/octet-stream, 27.0 KB)

## Timeline

### ch...@google.com (2026-05-16)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### is...@chromium.org (2026-05-17)

Thank you for the report! Nice catch!

### dx...@google.com (2026-05-18)

Project: chromium/src  

Branch:  main  

Author:  Andreas Haas [ahaas@chromium.org](mailto:ahaas@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7855343>

[gin] Fix type tag of gin::PerContextData

---


Expand for full commit details
```
     
    Bug: 513756452 
    Change-Id: Iae53724ba8838ce77a8db449bd5aa0eff4f81944 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7855343 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Andreas Haas <ahaas@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1632114}

```

---

Files:

- M `gin/per_context_data.cc`

---

Hash: [7c0a3512236f0b909f903465b801b0b298ec56d8](https://chromiumdash.appspot.com/commit/7c0a3512236f0b909f903465b801b0b298ec56d8)  

Date: Mon May 18 12:58:11 2026


---

### ts...@google.com (2026-05-28)

V8 folks:  There are two test cases for this issue, a html-based one and a unit test.  The html case runs with --sandbox-testing, which means the only valid report is one that produces the "V8 sandbox escape detected" but I just see a standard ASAN report. The unit test does reach this outcome, but launching from a unit test seems out-of scope. Is there a vulnerability that is reachable here from a shipping Chrome?

### ah...@google.com (2026-05-29)

This issue is a type confusion outside the V8 sandbox. Afaict it is possible to have objects of both types in the same renderer process, and with in-sandbox corruption, you can mix them up. So yes, afaict, there is a vulnerability that is reachable from a shipping Chrome.

### sp...@google.com (2026-06-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
v8 controlled sandbox. other processes renderer


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-08-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-08-26)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/513756452)*

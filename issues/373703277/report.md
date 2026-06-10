# DCHECK failure in Handle<To> v8::internal::Cast(Handle<From>, const v8::SourceLocation &) [To = v8

| Field | Value |
|-------|-------|
| **Issue ID** | [373703277](https://issues.chromium.org/issues/373703277) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2024-10-16 |
| **Bounty** | $55,000.00 |

## Description

### VULNERABILITY DETAILS

#### Summary

Simple variant of [b/372285204](https://issues.chromium.org/issues/372285204) and [b/332081797](https://issues.chromium.org/issues/332081797). For (null)exnref table types [`InstanceBuilder::Build()`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/module-instantiate.cc;drc=c658efa26d8eef733fd77263802d57d4efcf3c04;l=1276) uses `WasmNull` as the default value instead of JS null, resulting in type confusion.

#### Details

[`InstanceBuilder::Build()`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/module-instantiate.cc;drc=c658efa26d8eef733fd77263802d57d4efcf3c04;l=1276) does not handle exnref or nullexnref types, resulting in type confusion where `WasmNull` is set as the default element for exnref / nullexnref typed table. This can further be retrieved back to JS-side through `throw_ref` and may be exploited through Turboshaft optimization - see [b/372285204](https://issues.chromium.org/issues/372285204) and [b/372269618](https://issues.chromium.org/issues/372269618).

#### Bisect

Bug introduced by commit [2e357c4](https://chromiumdash.appspot.com/commit/2e357c4814954c6d83c336655209e14aa53911d4) in M112 that introduced wasm null, but `exnref` types are guarded behind a staged WASM feature.

#### Suggested Fix

Use `isolate_->factory()->null_value()` for `IsSubtypeOf(table.type, kWasmExnRef, module_)` too.

### VERSION

See bisect commit release info in Chromium Dash for more info: <https://chromiumdash.appspot.com/commit/2e357c4814954c6d83c336655209e14aa53911d4>

Chrome Version: 112.0.5579.0 ~ latest (requires exnref, a staged WASM feature)  

Operating System: All

### REPRODUCTION CASE

Attached as `poc.js` which exploits the type confusion to retrieve a `WasmNull` back to JS, then accesses a property on it to cause a crash. Run it with `--experimental-wasm-exnref --allow-natives-syntax`, which will yield the following:

```
0x3a8d0000fffd <Other heap object (WASM_NULL_TYPE)>
Stacktrace:
    ptr1=0x3a8d0000fffd
    ptr2=(nil)
    ptr3=(nil)
    ptr4=(nil)
    ptr5=(nil)
    ptr6=(nil)
    failure_message_object=0x7fff8fca6e10

==== JS stack trace =========================================

    0: ExitFrame [pc: 0x5ee6dbabbaf6]
    1: StubFrame [pc: 0x5ee6dbbbdb53]
    2: /* anonymous */ [0x3a8d001a6781] [./poc.js:2391] [bytecode=0x1f7f00040c65 offset=8563](this=0x3a8d00181a25 <JSGlobalProxy>)
    3: InternalFrame [pc: 0x5ee6dba1561c]
    4: EntryFrame [pc: 0x5ee6dba1535f]

==== Details ================================================

[0]: ExitFrame [pc: 0x5ee6dbabbaf6]
[1]: StubFrame [pc: 0x5ee6dbbbdb53]
[2]: /* anonymous */ [0x3a8d001a6781] [./poc.js:2391] [bytecode=0x1f7f00040c65 offset=8563](this=0x3a8d00181a25 <JSGlobalProxy>) {
...

```
### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Renderer  

Crash State: Crashes on invalid property access on a wasm null object

### CREDIT INFORMATION

Reporter credit: Seunghyun Lee (@0x10n) of CMU CyLab

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 73.3 KB)
- [poc.js](attachments/poc.js) (text/javascript, 73.3 KB)
- [exp.js](attachments/exp.js) (text/javascript, 78.8 KB)
- [exp.html](attachments/exp.html) (text/html, 91.4 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-10-16)

Detailed Report: https://clusterfuzz.com/testcase?key=5631359552782336

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  Handle<To> v8::internal::Cast(Handle<From>, const v8::SourceLocation &) [To = v8
  v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNu
  v8::internal::LoadIC::Load
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&revision=96619

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5631359552782336

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@appspot.gserviceaccount.com (2024-10-16)

Detailed Report: https://clusterfuzz.com/testcase?key=6730583954620416

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: Abrt
Crash Address: 0x0539000001d7
Crash State:
  v8::internal::Isolate::PushStackTraceAndDie
  v8::internal::LookupIterator::GetRootForNonJSReceiver
  v8::internal::LookupIterator::GetRoot
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8&revision=96619

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6730583954620416

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### 24...@project.gserviceaccount.com (2024-10-16)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### am...@chromium.org (2024-10-16)

clusterfuzz is hitting on the dcheck failure and believes this to be introduced via <https://crrev.com/c/5904414> in 131; going to tentatively set this as 130 (which is not Stable and next Extended Stable) based instead on the bisect

### se...@gmail.com (2024-10-16)

CF seems to bisect to that commit due to the PoC using `ref null noexn` (`kWasmNullExnRef`), but using plain `ref null exn` (`kWasmExnRef`) also works fine and will probably bisect closer to the root cause.

Attached is a PoC that simply replaces `kWasmNullExnRef` from the original PoC with `kWasmExnRef`.

---

FYI, as exnref was removed pre-WasmNull and re-introduced post-WasmNull, <https://crrev.com/c/4953360> which re-introduces exnref would probably be a more sensible bisect.

### pe...@google.com (2024-10-16)

Setting milestone because of s0/s1 severity.

### 24...@project.gserviceaccount.com (2024-10-19)

ClusterFuzz testcase 5631359552782336 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=96677:96678

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pe...@google.com (2024-10-19)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M130. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M131. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [130, 131].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### th...@chromium.org (2024-10-21)

1. https://chromium-review.googlesource.com/c/v8/v8/+/5942456
2. It is not in canary yet
3. No
4. No
5. No

### ma...@chromium.org (2024-10-21)

deleted

### am...@chromium.org (2024-10-21)

<https://crrev.com/c/5942456> approved for merges; please merge to 13.1 and 13.0 at your earliest convenience so this fix can be in the next 131 Beta and 130 Stable updates -- thanks!

### se...@gmail.com (2024-10-21)

Note that these types of subtle leaks and type confusion in opaque types are still exploitable after the turboshaft-wasm hardening fix in <https://crrev.com/c/5928643>.

Attached `exp.js` which obtains caged write primitive, test this with:

- d8: `--turboshaft-wasm --experimental-wasm-exnref` to crash on caged write
- Chrome: Replace the corresponding primitives part from the full exploit in [b/372269618#comment10](https://issues.chromium.org/issues/372269618#comment10), then test it on Chrome with `--enable-features=WebAssemblyTurboshaft --js-flags=--experimental-wasm-exnref --no-sandbox` to pop `calc`

---

CCing mliedtke@ for context for the related bug [b/372269618](https://issues.chromium.org/issues/372269618) and associated fix <https://crrev.com/c/5928643>:

These types of confusion are still exploitable due to branch type narrowing, where we narrow type information based on conditional branches on `WasmTypeCheck` and `IsNull` predicates. Both the predicates itself receives valid input types and thus do not trap, but the narrowed type on either branch taken / not taken cases may result in uninhabitable (i.e. unreachable) state. This is possible for "null value in non-null type" cases, where a `WasmTypeCast` from `ref T` into `ref null ToNullSentinel(T)` cannot be reduced further due to the current typed optimization reducer implementation ([src](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/turboshaft/wasm-gc-typed-optimization-reducer.h;drc=160612a75397f9048e3824d5177ed702742f22ff;l=220)). However, the "is null" branch now infers that the type is `ref ToNullSentinel(T)` which is uninhabitable, resulting in the same type confusion problem.

One mitigation may be to immediately reduce such type checks into `IsNull()` (which will further get reduced into `Word32Constant(0)`).

### se...@gmail.com (2024-10-21)

I'm guessing that these "full renderer RCEs" are not really that much interesting now as they're technically just copy-pasted templates, but just for bookkeeping so that we know what's demonstrated to be exploitable and what's not ;)

Pops `calc` on Windows x64 Chrome builds on versions before 132.0.6785.0 (exclusive), run with flags `--enable-features=WebAssemblyTurboshaft --js-flags=--experimental-wasm-exnref --no-sandbox`.

### th...@chromium.org (2024-10-22)

+mliedtke@ for comment #13

### th...@chromium.org (2024-10-22)

Oh, and this is still behind the --experimental-wasm-exnref flag so we actually don't need to backmerge.

### pb...@google.com (2024-10-22)

[Bulk update] Your change has been approved to get merged to M131 branch, Pls complete the merges by 3PM PST today Tuesday Oct 22th,2024, so they can be part of tomorrow's Beta release. 


### sp...@google.com (2024-10-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $55000.00 for this report.

Rationale for this decision:
$55,000 for high quality report of demonstrated RCE in a sandboxed process / the renderer


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-10-22)

Congrats on another one this week, Seunghyun! Thanks for your efforts on another great RCE demonstration and just reporting this issue to us over -- excellent work!

### cl...@chromium.org (2024-10-23)

Setting `Security_Impact-None` based on #16.

### ml...@chromium.org (2024-10-23)

Thanks for CCing me. Regarding [comment #13](https://issues.chromium.org/issues/373703277#comment13), I'm following up on this in an internal issue ([issue 375048791](https://issues.chromium.org/issues/375048791)) to see if we can figure out a more systematic approach to prevent the capability of arbitrary "conversions" of different type confusions using the type optimizer.

Thanks a lot for raising these concerns and even providing mitigation ideas!

### ap...@google.com (2024-10-25)

Project: v8/v8  

Branch: main  

Author: Matthias Liedtke <[mliedtke@chromium.org](mailto:mliedtke@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5962124>

[turboshaft][wasm] Optimize always failing ref.test instruction

---


Expand for full commit details
```
[turboshaft][wasm] Optimize always failing ref.test instruction 
 
Bug: 373703277, 375048791, 42204049 
Change-Id: I1c1a24f72514adfc8f9daffb27209587cb0947b7 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5962124 
Commit-Queue: Matthias Liedtke <mliedtke@chromium.org> 
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
Auto-Submit: Matthias Liedtke <mliedtke@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#96824}

```

---

Files:

- M `src/compiler/turboshaft/wasm-gc-typed-optimization-reducer.h`

---

Hash: 918bd974f61ae2288ada53939c3320749b274d38  

Date:  Fri Oct 25 11:36:24 2024


---

### pe...@google.com (2024-10-25)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### th...@chromium.org (2024-10-28)

Removed Approved-* labels, see comment #16.

### se...@gmail.com (2024-10-30)

Hi, seems like I haven't added this for my recent reports so adding it in bulk - I'd like to donate the bounty through Benevity. Thanks!

### pe...@google.com (2025-01-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/373703277)*

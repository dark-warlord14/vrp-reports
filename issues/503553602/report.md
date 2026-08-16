# V8 Sandbox Bypass:LOCAL+frame OOB write in `SetLocalVariableValue`

| Field | Value |
|-------|-------|
| **Issue ID** | [503553602](https://issues.chromium.org/issues/503553602) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | V8 version 14.9.0 (candidate) |
| **Reporter** | gr...@gmail.com |
| **Assignee** | da...@google.com |
| **Created** | 2026-04-17 |
| **Bounty** | $5,000.00 |

## Description

# Steps to reproduce the problem

1. Build d8 (commit 6b7fa0487453a6521f21f8d596acbfcc38f98995 Thu Apr 16)

```
is_component_build = false
is_debug = false
target_cpu = "x64"
v8_enable_sandbox = true
v8_enable_backtrace = true
v8_enable_disassembler = true
v8_enable_object_print = true
v8_enable_verify_heap = true
dcheck_always_on = false
v8_enable_memory_corruption_api = true

```

2. ./d8 --enable-inspector --sandbox-testing poc.js

# Problem Description

## Root Cause

`src/debug/debug-scopes.cc:1135–1141` (post-fix):

```
case VariableLocation::LOCAL:
  if (frame_inspector_ == nullptr) {
    /* generator path — patched by c091c2cbce3 */
  } else {
    JavaScriptFrame* frame = GetFrame();
    if (!frame->is_unoptimized()) return false;
    frame->SetExpression(index, *new_value);   // ← unchecked
  }
  return true;

```

`src/execution/frames-inl.h:305`:

```
inline void CommonFrame::SetExpression(int index, Tagged<Object> value) {
  base::Memory<Address>(GetExpressionAddress(index)) = value.ptr();
}

```

`src/execution/frames.cc:1531`:

```
Address UnoptimizedJSFrame::GetExpressionAddress(int n) const {
  const int offset = UnoptimizedFrameConstants::kExpressionsOffset;
  return fp() + offset - n * kSystemPointerSize;
}

```

Neither helper validates `n` / `index` against the frame's actual register file size.

## BISECT

The fix in commit `c091c2cbce3` ("[debug] Fix OOB write in `SetLocalVariableValue`", `Fixed: 502337304`) added bounds-check `CHECK`s only to the PARAMETER write paths in `v8::internal::ScopeIterator::SetLocalVariableValue`. The LOCAL write path that targets a live JavaScript frame still calls `frame->SetExpression(index, *new_value)` with an attacker-controlled `index` and **no bounds check**, giving an arbitrary tagged-value write at `fp() + kExpressionsOffset − index·8`. This is the same trigger family as the original [bug 502337304](https://issues.chromium.org/issues/502337304), simply moved one switch arm over.

# Summary

V8 Sandbox Bypass:LOCAL+frame OOB write in `SetLocalVariableValue`

# Custom Questions

#### Type of crash:

tab

#### Crash state:

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0xdd900000000,0xed900000000)

## V8 sandbox violation detected!

Received signal 11 SEGV_MAPERR 7ffcfbd72fd0

==== C stack trace ===============================

/mnt/cd7/v8/out/x64.release/d8(_ZN2v84base5debug10StackTraceC1Ev+0x1e)[0x5ef0b4ed27ee]
/mnt/cd7/v8/out/x64.release/d8(+0x3152736)[0x5ef0b4ed2736]
/mnt/cd7/v8/out/x64.release/d8(+0x1f980c5)[0x5ef0b3d180c5]
/lib/x86_64-linux-gnu/libc.so.6(+0x42520)[0x7a044e842520]
/mnt/cd7/v8/out/x64.release/d8(_ZN2v88internal13ScopeIterator21SetLocalVariableValueENS0_12DirectHandleINS0_6StringEEENS2_INS0_6ObjectEEE+0x254)[0x5ef0b36a59f4]
/mnt/cd7/v8/out/x64.release/d8(_ZN2v88internal13ScopeIterator16SetVariableValueENS0_6HandleINS0_6StringEEENS0_12DirectHandleINS0_6ObjectEEE+0xd2)[0x5ef0b36a5662]
/mnt/cd7/v8/out/x64.release/d8(_ZN12v8_inspector19V8DebuggerAgentImpl16setVariableValueEiRKNS_8String16ENSt4__Cr10unique_ptrINS_8protocol7Runtime12CallArgumentENS4_14default_deleteIS8_EEEES3_+0x428)[0x5ef0b4241558]
/mnt/cd7/v8/out/x64.release/d8(_ZN12v8_inspector8protocol8Debugger20DomainDispatcherImpl16setVariableValueERKN8v8_crdtp12DispatchableE+0xc4)[0x5ef0b4201b94]
/mnt/cd7/v8/out/x64.release/d8(_ZN8v8_crdtp14UberDispatcher14DispatchResult3RunEv+0x1f)[0x5ef0b4282d5f]
/mnt/cd7/v8/out/x64.release/d8(_ZN12v8_inspector22V8InspectorSessionImpl23dispatchProtocolMessageENS_10StringViewE+0x238)[0x5ef0b425e318]
/mnt/cd7/v8/out/x64.release/d8(_ZN2v815InspectorClient20SendInspectorMessageERKNS_20FunctionCallbackInfoINS_5ValueEEE+0x193)[0x5ef0b34ecde3]
/mnt/cd7/v8/out/x64.release/d8(+0x2f316e4)[0x5ef0b4cb16e4]
[end of stack trace]

```
#### Reporter credit:

GraVity0 & Wum1ng with HUST

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 1.4 KB)
- deleted (application/octet-stream, 0 B)
- [poc2.js](attachments/poc2.js) (text/javascript, 3.8 KB)
- [fix.patch](attachments/fix.patch) (text/x-diff, 857 B)
- [poc2.js](attachments/poc2_76055448.js) (text/javascript, 1.9 KB)

## Timeline

### gr...@gmail.com (2026-04-17)

What the new PoC demonstrates

- Attacker-controlled write position: target = fp(victim) + kExpressionsOffset − INDEX·8, where INDEX is chosen freely by the attacker through the var vN; count in the reparsed corrupt source.
- Attacker-controlled write value: any 31-bit Smi or anyin-sandbox heap object's tagged pointer (selected via setVariableValue's newValue).

Limitations

- Trigger requires the Inspector channel: path goes through Debugger.setVariableValue (DevTools Protocol).
- Write value constrained by Tagged encoding:
  - Smi: high 32 bits always zero → overwriting saved RIP falls into
    the "first 4 GB" filter.
  - HeapObject: high 32 bits are the sandbox base → RIP lands inside
    the sandbox

```
./d8 --enable-inspector --expose-memory-corruption-api ./poc2.js 
[*] sandbox base  = 0xe4600000000
[*] sandbox size  = 0x10000000000
[*] payload.map overwritten with 0xdead1301
[*] expected fault = sandbox_base + 0xdead1300 + 4
Received signal 11 SEGV_ACCERR 0e46dead1304

==== C stack trace ===============================

/mnt/cd7/v8/out/x64.release/d8(_ZN2v84base5debug10StackTraceC1Ev+0x1e)[0x61a3e2db67ee]
/mnt/cd7/v8/out/x64.release/d8(+0x3152736)[0x61a3e2db6736]
/lib/x86_64-linux-gnu/libc.so.6(+0x42520)[0x737b20442520]
/mnt/cd7/v8/out/x64.release/d8(_ZNK2v88internal10HeapObject11SizeFromMapENS0_6TaggedINS0_3MapEEE+0x0)[0x61a3e1a140b0]
/mnt/cd7/v8/out/x64.release/d8(_ZN2v88internal23SemiSpaceObjectIterator4NextEv+0x58)[0x61a3e17bd188]
/mnt/cd7/v8/out/x64.release/d8(_ZN2v88internal18HeapObjectIterator4NextEv+0xed)[0x61a3e173a7dd]
/mnt/cd7/v8/out/x64.release/d8(_ZN2v88internal7Isolate42CollectSourcePositionsForAllBytecodeArraysEv+0xa8)[0x61a3e1641358]
/mnt/cd7/v8/out/x64.release/d8(_ZN2v88internal5Debug11UpdateStateEv+0x6a)[0x61a3e1597c8a]
/mnt/cd7/v8/out/x64.release/d8(_ZN12v8_inspector10V8Debugger6enableEv+0x4c)[0x61a3e212e3dc]
/mnt/cd7/v8/out/x64.release/d8(_ZN12v8_inspector19V8DebuggerAgentImpl10enableImplEv+0x5d)[0x61a3e2117d1d]
/mnt/cd7/v8/out/x64.release/d8(_ZN12v8_inspector19V8DebuggerAgentImpl6enableENSt4__Cr8optionalIdEEPNS_8String16E+0x1dd)[0x61a3e211adfd]
/mnt/cd7/v8/out/x64.release/d8(_ZN12v8_inspector8protocol8Debugger20DomainDispatcherImpl6enableERKN8v8_crdtp12DispatchableE+0xaa)[0x61a3e20e078a]
/mnt/cd7/v8/out/x64.release/d8(_ZN8v8_crdtp14UberDispatcher14DispatchResult3RunEv+0x1f)[0x61a3e2166d5f]
/mnt/cd7/v8/out/x64.release/d8(_ZN12v8_inspector22V8InspectorSessionImpl23dispatchProtocolMessageENS_10StringViewE+0x238)[0x61a3e2142318]
/mnt/cd7/v8/out/x64.release/d8(_ZN2v815InspectorClient20SendInspectorMessageERKNS_20FunctionCallbackInfoINS_5ValueEEE+0x193)[0x61a3e13d0de3]
/mnt/cd7/v8/out/x64.release/d8(+0x2f316e4)[0x61a3e2b956e4]
[end of stack trace]  

```

### em...@google.com (2026-04-18)

The POC uses `--enable-inspector`, however this is generally not a viable way for demonstrating a vulnerability. Quoting <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/d8/d8.cc;l=6693;drc=9cc3c41e729ee1e8d5cccef845efe09263135deb> :

> // Inspector security bugs must be shown through the embedder (i.e. Chrome,  
> 
> // or content\_shell).

### ch...@google.com (2026-04-18)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-18)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ch...@google.com (2026-04-20)

Per [TaskFloss taxonomy](http://go/taskfloss-taxonomy#backlogs) assigned issues must never sit on backlogs, because backlogs are reserved for issues that aren't currently being worked on - and are therefore in state "New" or "Won't Fix (Inactive)".

### ar...@google.com (2026-04-20)

Severity must be set. Even for Security\_Impact-None. I am restoring S1, assuming it was correct previously.

### sz...@google.com (2026-04-20)

Severity is low as this requires extensive user interaction inside DevTools to trigger.

### ch...@google.com (2026-04-20)

This issue has been identified as a security vulnerability and added to the team goal for addressing such issues (["High-priority and security bugs are promptly fixed"](http://b/483246889)). This helps ensure it receives the necessary attention and tracking.

### gr...@gmail.com (2026-04-20)

Adding a fix patch, hope it helps.

Bound the attacker-controlled index against the live frame's bytecode register count with real CHECKs before
frame->SetExpression(index, ...) writes a tagged value to the native stack.

```
#
# Safely terminating process
# The following harmless error was encountered: Check failed: static_cast<uint32_t>(index) < static_cast<uint32_t>( unoptimized->GetBytecodeArray()->register_count()).
#
#
#
#FailureMessage Object: 0x7ffc73e101b0

```

### gr...@gmail.com (2026-04-23)

Hey there, not trying to stir anything up — just curious: how come this [issue 503553602](https://issues.chromium.org/issues/503553602) got Duplicate of 503649569, when 503649569 actually has a later ID than this one?

### gr...@gmail.com (2026-04-23)

Hi team, I know everyone's got a lot on their plate lately — would anyone be able to take a look at this when you get a chance? Thanks!

### em...@google.com (2026-04-24)

danilsomsikov@: If two issues are the same, we should probably dedupe into the earliest (this one) indeed. Thanks.

### gr...@gmail.com (2026-04-28)

hi,team, I noticed that the fix for this vulnerability (f2b042b389d) appears to be incomplete.

The fix f2b042b389d only added CHECK\_GE/CHECK\_LT guards to two paths inside VisitLocals(): VariableLocation::PARAMETER (around line 941-947) and
VariableLocation::LOCAL (around line 959-975). However, VisitLocalScope() is a separate function (starting at line 1003), and contains another
unguarded call to frame\_inspector\_->GetExpression(closure\_scope\_->arguments()->index()) at line 1056 — the patch never touches it.

Bypass:

1. Place a single eval("") inside the victim function. This forces every var in the closure — including the implicit arguments — into
   VariableLocation::CONTEXT, so VisitLocals() short-circuits at line 993 and the newly added PARAMETER/LOCAL CHECKs are never reached.
2. VisitLocals() returns false, so control flows into VisitLocalScope().
3. Use Sandbox.MemoryView to flip Script::source to a polluted string containing 1.1 M var v0..vN declarations. On reparse arguments\_ is also  
   
   CONTEXT-allocated, with var->index() = num\_heap\_slots\_++ — its index grows linearly with the var count in the polluted source, so  
   
   arguments\_->index() ≈ N ≈ 1.1 M.
4. That huge index flows directly into the unguarded GetExpression(index) at line 1056, computing fp + kExpressionsOffset - index\*8 ≈ fp - 8.8
   MB, past the stack base into unmapped pages → SIGSEGV outside the cage → ## V8 sandbox violation detected! (read access).

Suggested fix: replicate the same is\_unoptimized() + CHECK in [0, ComputeExpressionsCount()) guard at line 1056; alternatively, treat an
out-of-range index as optimized-out so line 1060 FunctionGetArguments becomes the fallback.

```
d8 --enable-inspector --sandbox-testing --allow-natives-syntax poc2.js
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x308800000000,0x318800000000)

## V8 sandbox violation detected!

The sandbox violation was a *read* access which is technically not a sandbox violation. This requires manual investigation.
Received signal 11 SEGV_MAPERR 7ffc64583ef8

==== C stack trace ===============================

/mnt/cd7/v8/out/x64.release/d8(_ZN2v84base5debug10StackTraceC1Ev+0x1e)[0x64f10e69b7ee]
/mnt/cd7/v8/out/x64.release/d8(+0x3017736)[0x64f10e69b736]
/mnt/cd7/v8/out/x64.release/d8(+0x1ea3135)[0x64f10d527135]
/lib/x86_64-linux-gnu/libc.so.6(+0x42520)[0x77b5fbc42520]
/mnt/cd7/v8/out/x64.release/d8(_ZN2v88internal14FrameInspector13GetExpressionEi+0x4c)[0x64f10cf33b5c]
/mnt/cd7/v8/out/x64.release/d8(_ZNK2v88internal13ScopeIterator15VisitLocalScopeERKNSt4__Cr8functionIFbNS0_6HandleINS0_6StringEEENS4_INS0_6ObjectEEENS1_9ScopeTypeEEEENS1_4ModeES9_+0xee)[0x64f10cf3fdce]
/mnt/cd7/v8/out/x64.release/d8(_ZN2v88internal13ScopeIterator11ScopeObjectENS1_4ModeE+0x10d)[0x64f10cf3f18d]
/mnt/cd7/v8/out/x64.release/d8(_ZN2v88internal13DebugEvaluate14ContextBuilderC1EPNS0_7IsolateEPNS0_15JavaScriptFrameEi+0xfd)[0x64f10cf32eed]
/mnt/cd7/v8/out/x64.release/d8(_ZN2v88internal13DebugEvaluate5LocalEPNS0_7IsolateENS0_12StackFrameIdEiNS0_12DirectHandleINS0_6StringEEEb+0x1e8)[0x64f10cf325f8]
/mnt/cd7/v8/out/x64.release/d8(_ZN2v88internal23DebugStackTraceIterator8EvaluateENS_5LocalINS_6StringEEEb+0x5d)[0x64f10cf429cd]
/mnt/cd7/v8/out/x64.release/d8(_ZN12v8_inspector19V8DebuggerAgentImpl19evaluateOnCallFrameERKNS_8String16ES3_NSt4__Cr8optionalIS1_EENS5_IbEES7_S7_S7_S7_NS5_IdEEPNS4_10unique_ptrINS_8protocol7Runtime12RemoteObjectENS4_14default_deleteISC_EEEEPNS9_INSB_16ExceptionDetailsENSD_ISH_EEEE+0x316)[0x64f10d9fc3a6]
/mnt/cd7/v8/out/x64.release/d8(_ZN12v8_inspector8protocol8Debugger20DomainDispatcherImpl19evaluateOnCallFrameERKN8v8_crdtp12DispatchableE+0x19b)[0x64f10d9b9f2b]
/mnt/cd7/v8/out/x64.release/d8(_ZN8v8_crdtp14UberDispatcher14DispatchResult3RunEv+0x1f)[0x64f10da3da8f]
/mnt/cd7/v8/out/x64.release/d8(_ZN12v8_inspector22V8InspectorSessionImpl23dispatchProtocolMessageENS_10StringViewE+0x238)[0x64f10da19918]
/mnt/cd7/v8/out/x64.release/d8(_ZN2v815InspectorClient20SendInspectorMessageERKNS_20FunctionCallbackInfoINS_5ValueEEE+0x1ab)[0x64f10cdb804b]
/mnt/cd7/v8/out/x64.release/d8(+0x2dfd6d4)[0x64f10e4816d4]
[end of stack trace]

```

### da...@google.com (2026-05-05)

@gr...@gmail.com

Thanks! You are correct that the previous fix was incomplete as it missed the arguments object materialization path in VisitLocalScope.

This bypass has been addressed in CL 7800198 (<https://chromium-review.googlesource.com/c/v8/v8/+/7800198>). The fix adds the necessary CHECK guards to validate the expression index against the actual frame bounds and ensures that the variable location is explicitly verified as VariableLocation::LOCAL before attempting a stack read.

### sp...@google.com (2026-05-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### 24...@project.gserviceaccount.com (2026-05-07)

ClusterFuzz testcase 5221724752740352 is still reproducing on the latest available build  r107119.

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the hotlistid:5433040.

### ml...@google.com (2026-05-28)

Sandbox bypasses are S2 by default. With debugger interaction required you probably should lower this even to S3.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/503553602)*

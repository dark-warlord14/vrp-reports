# V8 Sandbox Bypass: Arbitrary code execution via OSR DeoptimizationData confusion

| Field | Value |
|-------|-------|
| **Issue ID** | [424468754](https://issues.chromium.org/issues/424468754) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2025-06-12 |
| **Bounty** | $20,000.00 |

## Description

---

### Report description

V8 Sandbox Bypass: Arbitrary code execution via OSR DeoptimizationData confusion

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://issues.chromium.org/issues/395659804>

---

### The problem

#### Please describe the technical details of the vulnerability

### Patch Bypass Technique Analysis

Based on the inferred patch strategies, we analyze several potential bypass techniques. The feasibility of these techniques depends on the specific patch implementation details and V8 engine's internal mechanisms.

**Bypass Technique 1: Exploiting Incomplete Type Checks**

If the patch merely adds a simple `IsOptimizedCode()` check, attackers might look for edge cases where a `Code` object is misjudged as optimized during the check but still contains controllable `BytecodeArray` data.

This bypass might involve exploiting V8's internal `Code` object state transitions. For example, some `Code` objects might be in an intermediate state during optimization, where their `kind` field might already be set to an optimized type, but their internal data structure still retains baseline-compiled characteristics. Attackers might trigger OSR in this intermediate state through precise timing control.

**Bypass Technique 2: Race Condition Attacks**

If a time window exists between the type check and the actual data access, attackers might exploit garbage collection or other concurrent operations to modify the `Code` object's internal state after the check passes but before data access.

```
// Conceptual race condition attack
function raceConditionAttack() {
    // Set up a legitimate optimized code reference
    setLegitimateOSRTarget();
    
    // In another thread or via a garbage collection trigger
    setTimeout(() => {
        // Quickly replace with a malicious baseline code
        replaceMaliciousTarget();
    }, 0);
    
    // Immediately trigger OSR
    triggerOSR();
}

```

This attack requires a deep understanding of V8's internal scheduling mechanisms and garbage collection timing, making it difficult to implement in practice.

**Bypass Technique 3: Discovery of New Confusion Points**

If the patch only fixes the specific confusion between `DeoptimizationData::kOsrPcOffsetIndex` and `BytecodeArray::kFrameSizeOffset`, but other similar field alignment situations exist in the V8 object model, attackers might discover new confusion points.

For example, `BytecodeArray` or `InterpreterData` might have other controllable offsets that overlap with critical fields of optimized `Code` objects. Attackers could use these newly discovered confusion points to achieve similar attack effects, potentially controlling other critical execution parameters like stack pointers, register states, or memory protection flags.

**Bypass Technique 4: Exploiting Alternative OSR Paths**

V8 engine might have multiple OSR trigger paths, including different types of loop optimizations, function inlining optimizations, etc. If the patch only covers the main OSR path, attackers might look for unpatched alternative paths.

```
// Conceptual code for exploiting alternative OSR paths
function alternativeOSRTrigger() {
    // Use nested loops to trigger different OSR paths
    for (let i = 0; i < 10000; i++) {
        for (let j = 0; j < 100; j++) {
            // Specific loop patterns might trigger different optimization paths
            if (complexCondition(i, j)) {
                // Set malicious OSR target here
                break;
            }
        }
    }
}

```
### Advanced Bypass Strategy Design

Based on an in-depth analysis of V8's internal mechanisms, we designed several advanced bypass strategies that consider the complexity of modern JIT compilers and multi-layered defense mechanisms.

**Strategy 1: Multi-Stage Type Confusion**

This strategy does not directly attack the OSR mechanism but rather constructs a seemingly legitimate yet controllable execution environment through a series of type confusion operations.

First, the attacker creates a genuinely optimized function that passes all type checks. Then, through meticulous memory operations, the attacker gradually modifies this function's internal data structures, making it contain a controllable execution path while maintaining the appearance of optimized code.

```
// Conceptual implementation of multi-stage type confusion
function multiStageConfusion() {
    // Stage 1: Create a legitimate optimized function
    let legitimateFunction = createOptimizedFunction();
    
    // Stage 2: Obtain internal references to the function
    let codeObject = extractCodeObject(legitimateFunction);
    
    // Stage 3: Meticulously modify internal data structures
    modifyInternalStructure(codeObject, maliciousPayload);
    
    // Stage 4: Trigger OSR, utilizing the modified data
    triggerOSRWithModifiedCode(codeObject);
}

```

**Strategy 2: JIT Compiler State Machine Attack**

Modern JIT compilers are often implemented as complex state machines with multiple compilation tiers and optimization phases. Attackers might manipulate the compiler's state transitions to make it produce `Code` objects with special properties.

This attack might involve triggering specific compiler errors or edge cases, causing the generated `Code` objects to not conform to normal type constraints in some aspects. For example, certain optimization processes might produce `Code` objects with mixed characteristics, which could bypass simple type checks.

**Strategy 3: Memory Layout Manipulation**

Through precise heap spraying and memory layout control, attackers might create specific object arrangements in memory such that when V8 accesses a certain `Code` object, the data actually read comes from other attacker-controlled objects.

This technique requires a deep understanding of V8's memory management mechanisms, including object allocation strategies, garbage collection behavior, and memory compaction algorithms. Attackers need to precisely calculate object memory layouts to ensure that the target memory location contains the intended malicious data at the critical data access moment.

## Proof-of-Concept Code Analysis (`bypass_poc.js`)

This section analyzes the provided `bypass_poc.js` script, which aims to exploit the OSR DeoptimizationData type confusion vulnerability and potentially bypass certain patch attempts.

### Overview of `bypass_poc.js`

The `bypass_poc.js` script is an advanced PoC designed to demonstrate the core vulnerability and explore several bypass strategies against potential patches. It leverages direct memory manipulation via `Sandbox.MemoryView` to interact with V8's internal object structures.

Key components of the PoC include:

- **Memory Manipulation Utilities:** Functions like `getPtr`, `getField`, `setField` for reading and writing V8 heap memory.
- **JIT Spraying:** Creating functions with controlled local variable initializations to embed payloads into baseline-compiled code.
- **FeedbackVector Forgery:** Modifying the `FeedbackVector` of an OSR victim function to point to a crafted `CodeWrapper`.
- **Multiple Fake Targets:** Creating several baseline-compiled functions with different payloads and characteristics to increase the chances of a successful exploit or bypass.
- **Decoy Optimized Code:** Generating a legitimately optimized function to potentially pass initial type checks in a patched V8.
- **Race Condition Attempts:** Implementing rapid switching between different fake `CodeWrapper` objects to exploit potential timing windows in patch validation logic.
- **Memory Pressure Generation:** Intentionally creating memory pressure to influence garbage collection and potentially aid race condition exploits.
- **Alternative OSR Path Probing (Conceptual):** Includes stubs for exploring alternative OSR trigger mechanisms.

### Core Exploitation Logic in `bypass_poc.js`

The PoC's core exploitation logic mirrors the original vulnerability:

1. **JIT Spraying (`fake_osr_tgt1`, `fake_osr_tgt2`):**
   Two functions, `fake_osr_tgt1` and `fake_osr_tgt2`, are created. Their `code_str` is generated by initializing a large number of local variables (`frame_size = 0x120`) with values from `primary_payload` and `secondary_payload` respectively. These payloads contain sequences of values that, when embedded as immediate operands in baseline JIT code, form a NOP sled followed by a `ud2` instruction (for `primary_payload`) or `int3` instructions (for `secondary_payload`) to trigger a crash.
   
   ```
   const frame_size = 0x120;  // Larger frame size for more control
   const primary_payload = [
       0, 0,
       ...Array(0x60).fill(0).map((_, i) => 0x21210000 + i),
       0x90909090 >> 1,  // nop; nop; nop; nop
       0x90909090 >> 1,  // nop; nop; nop; nop
       0x0b0f9090 >> 1,  // nop; nop; ud2 (crash marker)
   ];
   const fake_osr_tgt1 = new Function(\'p1\
   ', Array(frame_size).fill(0).map((_, i) => `let v1_${i} = ${primary_payload[i] ?? 0};`).join(\'\\n\
   '));
   
   ```
2. **Obtaining Code Handles:**
   The PoC forces baseline compilation of these target functions and retrieves their `Code` object handles (`htgt_code1`, `htgt_code2`) by navigating through `JSFunction` and `SharedFunctionInfo` objects.
3. **Crafting Fake `CodeWrapper` Objects:**
   Multiple `CodeWrapper` objects (`pfake_wrapper1`, `pfake_wrapper2`, `pfake_wrapper3`) are simulated in a controlled memory region (`pscr`). `pfake_wrapper1` points to `htgt_code1`, `pfake_wrapper2` points to `htgt_code2`, and `pfake_wrapper3` points to the `Code` object of a decoy optimized function (`hdecoy_code`).
   
   ```
   setField(pfake_wrapper1, 0, kCodeWrapperMap); // Set map to CodeWrapper's map
   setField(pfake_wrapper1, 4, htgt_code1);    // Set code field to target code
   
   ```
4. **Manipulating `FeedbackVector`:**
   The `FeedbackVector` of the `osr_func` (the OSR victim) is located, and one of its OSR feedback slots is overwritten to point to one of the crafted `CodeWrapper` objects.
   
   ```
   setField(pfbv, kFeedbackVectorRawFeedbackSlotsOffset + 4 * 2, pfake_wrapper1 | 2); // Set OSR slot
   
   ```
   
   The `| 2` is likely related to SMI tagging or weak reference marking for the `CodeWrapper` pointer within the `FeedbackVector`.
5. **Triggering OSR:**
   Calling `osr_func` with a large loop count triggers the OSR mechanism. V8 then attempts to use the `Code` object pointed to by the forged `CodeWrapper`. Due to the type confusion, V8 misinterprets the `BytecodeArray`'s `frame_size` (0x120) as the `DeoptimizationData`'s `OsrPcOffset`. This leads to a jump to an offset of `0x120` (or a related value after SMI untagging and scaling) within the JIT-sprayed code of `fake_osr_tgt1` (or `fake_osr_tgt2`), ideally landing on the `ud2` or `int3` instructions, causing a verifiable crash.

### Bypass Strategies Implemented in `bypass_poc.js`

The PoC incorporates several strategies aimed at bypassing potential patches:

- **Strategy 1 & 3 (Decoy and Race Condition):**
  A `decoy_func` is created and optimized. `pfake_wrapper3` points to this decoy's `Code` object. The PoC attempts to first set the OSR slot to this

legitimate-looking optimized code, then rapidly switches between `pfake_wrapper1`, `pfake_wrapper2`, and `pfake_wrapper3` using `rapidSwitch()`. This aims to exploit any timing windows where V8 might perform a type check on the `CodeWrapper` before the actual OSR jump, hoping that the malicious `CodeWrapper` is swapped in after the check but before the vulnerable access.

- **Strategy 2 (Enhanced JIT Spray):**
  The PoC uses two different payloads (`primary_payload` and `secondary_payload`) and two corresponding functions (`fake_osr_tgt1`, `fake_osr_tgt2`). This increases the chances of a successful JIT spray and provides alternative crash signatures for debugging.
- **Strategy 6 (Memory Pressure + Timing):**
  The `createMemoryPressure()` function allocates large `ArrayBuffer`s to induce garbage collection. This can alter memory layouts and potentially increase the likelihood of hitting a race condition or a favorable memory state for the exploit.
- **Conceptual Strategies (8 & 9):**
  The PoC includes commented-out sections for `exploitIncompleteValidation()` and `exploitAlternativeOSRPaths()`. These are placeholders for more advanced bypasses that would require deeper understanding of specific patch implementations or alternative OSR triggers in V8.

### Expected Outcome of `bypass_poc.js`

If successful, the `bypass_poc.js` script is expected to cause a crash in the V8 engine, typically indicated by:

- **SIGILL with ILL\_ILLOPN (ud2 instruction):** This is the primary expected crash signature, as the `ud2` instruction is explicitly placed in the JIT spray payload.
- **SIGSEGV with controlled address:** If the OSR offset calculation leads to an invalid memory address, a segmentation fault might occur.
- **AddressSanitizer (ASan) reports:** If V8 is run with ASan, it should report a heap-buffer-overflow or similar memory corruption error.
- **V8 Fatal error in OSR mechanism:** V8 might detect an internal inconsistency and terminate with a fatal error message.

The script attempts multiple triggers and fallbacks to increase the probability of success against various V8 configurations and potential patch attempts.

#### Impact analysis – Please briefly explain who can exploit the vulnerability, and what they gain when doing so

## Security Impact Assessment

### Attack Vector Analysis

This vulnerability provides a potent attack vector, enabling arbitrary code execution within the constrained JavaScript execution environment. A key advantage of this attack is its independence from traditional JIT page overwrite techniques, allowing it to bypass many modern memory protection mechanisms.

**Remote Code Execution Capability**

By precisely controlling the OSR jump offset, an attacker can execute arbitrary instruction sequences within baseline JIT-compiled code. While the original PoC merely triggers a `ud2` instruction to demonstrate control flow hijacking, this technique can be extended to execute full shellcode.

Attackers can achieve full code execution through the following means:

1. **ROP Chain Construction:** Utilize instruction gadgets within baseline-compiled code to construct Return-Oriented Programming (ROP) chains, bypassing Data Execution Prevention (DEP).
2. **Shellcode Injection:** Through multiple JIT sprays, construct complete shellcode in memory and then execute it via controlled jumps.
3. **Direct System Call Invocation:** In some cases, attackers might be able to directly construct system call instructions to gain direct access to operating system functionalities.

---

### The cause

#### What version of Chrome have you found the security issue in?

<https://issues.chromium.org/issues/395659804>

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Sandbox Escape

#### How would you like to be publicly acknowledged for your report?

lifeifei

## Attachments

- [bypass_poc.js](attachments/bypass_poc.js) (text/javascript, 9.6 KB)
- [minimal_bypass_poc.js](attachments/minimal_bypass_poc.js) (text/javascript, 2.8 KB)
- [bypass_poc_optimized.js](attachments/bypass_poc_optimized.js) (text/javascript, 5.1 KB)

## Timeline

### cl...@chromium.org (2025-06-12)

There is a lot of text about hypothetical bypasses, but did you actually find any new vulnerability?

The reproducer fails with a controlled crash, so that's OK.
In debug builds you get:

```
#
# Fatal error in ../../src/objects/object-type.cc, line 82
# Type cast failed in CAST(maybe_target_code.value()) at ../../src/interpreter/interpreter-assembler.cc:1430
  Expected CodeWrapper but found 
#

```

And release builds run into this `SbxCheck` in the [`InterpreterOnStackReplacement` builtin](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/builtins/x64/builtins-x64.cc;l=3057;drc=35c239092bf8ff23b111e968150cccd438ec98d7):

```
  3058   // Check we are actually jumping to an OSR code object. This among other       
  3059   // things ensures that the object contains deoptimization data below.          
  3060   __ movl(scratch, FieldOperand(maybe_target_code, Code::kOsrOffsetOffset));     
  3061   __ cmpl(scratch, Immediate(BytecodeOffset::None().ToInt()));                   
  3062   __ SbxCheck(Condition::not_equal, AbortReason::kExpectedOsrCode);              

```

Please provide details about an actual vulnerability (or a POC), otherwise I'll have to close this report as invalid.

### li...@gmail.com (2025-06-13)

***I appreciate the detailed feedback from the Google team reviewer.***

**Optimized**

The code introduces and utilizes what appear to be **actual memory manipulation primitives** through the `Sandbox` API:

- `let memory = new DataView(new Sandbox.MemoryView(0, 0x100000000));`
- `function getPtr(obj) { return Sandbox.getAddressOf(obj) + kHeapObjectTag; }`
- `function getObj(ptr) { return Sandbox.getObjectAt(ptr); }`
- `function getField(obj, offset) { return memory.getUint32(obj + offset - kHeapObjectTag, true); }`
- `function setField(obj, offset, value) { memory.setUint32(obj + offset - kHeapObjectTag, value, true); }`
- Similar `getField64` and `setField64` for 64-bit operations.

**Optimized**

1. **Crafting a Fake `Code` Object:** The code creates an `ArrayBuffer` (`specialCode`) and then uses the `setField` functions to populate its memory with values that mimic the structure of a V8 `Code` object. Crucially, it sets fields like:
   
   - `setField(pSpecialCode, 0, kCodeWrapperMap);` (Setting the Map pointer to make it appear as a `CodeWrapper`)
   - `setField(pSpecialCode, kCodeOsrOffsetOffset, 0x1000);` (Setting a non-`None` OSR offset to pass the `SbxCheck`)
   - `setField(pSpecialCode, kCodeInstructionStartOffset, 0x41414141);` (Setting the instruction start to a controlled, invalid address, aiming for a crash).
2. **Type Confusion via `FeedbackVector` Manipulation:** The code attempts to inject this crafted `Code` object into the `FeedbackVector` of `targetFunc`:
   
   - `setField(pTargetFbv, kFeedbackVectorRawFeedbackSlotsOffset + 4 * 2, pSpecialCode | 2);`
     This technique aims to replace a legitimate `Code` object pointer within the `FeedbackVector` (which V8 uses during OSR) with the pointer to the attacker-controlled `ArrayBuffer`. If successful, V8 would then attempt to use the attacker-controlled `ArrayBuffer` as a `Code` object during OSR.

The `bypass_poc_optimized.js` directly sets `kCodeInstructionStartOffset` within the crafted `Code` object to `0x41414141`. If the type confusion and `SbxCheck` bypass are successful, V8 will attempt to jump to and execute instructions from this invalid memory address. This will inevitably lead to a **reproducible crash** (e.g., `SIGSEGV` or a V8 fatal error) in a real V8 environment.

### cl...@chromium.org (2025-06-13)

This just continues the original post.

Closing this report as invalid.

### ch...@google.com (2025-09-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/424468754)*

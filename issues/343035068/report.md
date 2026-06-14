# Security: Segv in Builtins_JSToWasmWrapperAsm

| Field | Value |
|-------|-------|
| **Issue ID** | [343035068](https://issues.chromium.org/issues/343035068) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2024-05-28 |
| **Bounty** | $11,000.00 |

## Description

VULNERABILITY DETAILS

## INTRODUCE

After bisect, it was determined that following commit caused this problem.

- Commit Info
  - Version: 93916
  - link: <https://crrev.com/bacbfe2c1f0722025a90c33e2b586ccc16ee8e11>
- Commit Message

```
commit bacbfe2c1f0722025a90c33e2b586ccc16ee8e11
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Tue May 14 17:44:15 2024 +0200

    [turboshaft] Clean up representations.h
    
    Two functions were unused, two were almost duplicates of each other,
    and the recently introduced ProtectedPointer representation was
    handled a bit inconsistently.
    This patch isn't expected to change any observable behavior.
    
    Bug: 42202729
    Change-Id: Ia5c46b7503f4d2bdcceff3fbe92d9592895d7579
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5529247
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#93916}


```
## CRASH LOG

- Debug output

```
# CMD: /tmp/d8-linux-release-v8-component-94116/d8 --future --wasm-staging poc.js
# OUTPUT ==============================================================
Received signal 11 SEGV_MAPERR 451800040220


```
## Other

Please note to include the flags `--future --wasm-staging` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.7.0 - 12.7.0

REPRODUCTION CASE

1. Download release v8 from: gs://v8-asan/linux-release/d8-linux-release-v8-component-94116.zip
2. Run: `d8 --future --wasm-staging poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 2.8 KB)

## Timeline

### je...@gmail.com (2024-05-28)

The debug version will always get stuck, please use release to reproduce.

### je...@gmail.com (2024-05-28)

### **Root Cause Analysis of the Vulnerability**

### **Description**

The root cause of this vulnerability lies in the compiler optimization phase where a **`ProtectedPointer`** is incorrectly treated as a regular compressed pointer. This misinterpretation occurs during the **`turboshaft`** optimization process and involves the recently introduced **`ProtectedPointer`** representation.

### **Detailed Analysis**

1. **Crash Information**:
   
   ```
   Thread 1 "d8" received signal SIGSEGV, Segmentation fault.
   0x000020d32100ba2c in ?? ()
   LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
   ───────────────────────────────────────────────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]───────────────────────────────────────────────────────────────────────────
   *RAX  0x1
   *RBX  0x1
   *RCX  0x1
   *RDX  0x1
   *RDI  0xfca00046ae1 ◂— 0x40000009 /* '\t' */
   *RSI  0xfca00046b15 ◂— 0xe90040760000001f
   *R8   0x555583787de8 ◂— 0x1
    R9   0x0
   *R10  0x1
   *R11  0x246
    R12  0x0
   *R13  0x555583701080 —▸ 0x555582659f80 (Builtins_AdaptorWithBuiltinExitFrame) ◂— mov ecx, dword ptr [rdi + 0xf]
   *R14  0x13c800000000 ◂— 0x40940
   ...
   ────────────────────────────────────────────────────────────────────────────────────[ DISASM / x86-64 / set emulate on ]────────────────────────────────────────────────────────────────────────────────────
    ► 0x20d32100ba2c    mov    rdi, qword ptr [r14 + rdi + 0x1f]
      0x20d32100ba31    sar    rdi, 0x10
      0x20d32100ba35    mov    edi, edi
      0x20d32100ba37    and    edi, 0x1f
      0x20d32100ba3a    mov    ecx, edi
      0x20d32100ba3c    ror    ebx, cl
      0x20d32100ba3e    lzcnt  eax, ebx
      0x20d32100ba42    mov    rbp, qword ptr [rbp]
      0x20d32100ba46    mov    ecx, 1
      0x20d32100ba4b    mov    rdx, rcx
      0x20d32100ba4e    add    rsp, 0x18
   
   pwndbg> bt
   #0  0x000020d32100ba2c in ?? ()
   #1  0x00000fca00046b15 in ?? ()
   #2  0x0000000000000008 in ?? ()
   #3  0x00007ffcb4616f48 in ?? ()
   #4  0x00005555826fef4a in Builtins_JSToWasmWrapperAsm ()
   
   pwndbg> job $rdi
   0xfca00046ae1: [TrustedByteArray]
    - map: 0x13c800000921 <Map(TRUSTED_BYTE_ARRAY_TYPE)>
    - length: 32
    - begin: 0xfca00046ae8
   
   
   ```
2. **Debug Information**:
   
   - In the gdb debugging session, the crash point is identified at the following instruction:
     
     ```
     mov    rdi, qword ptr [r14 + rdi + 0x1f]
     
     ```
   - Further analysis reveals that this instruction attempts to access the address stored in **`rdi`**, but **`rdi`** is mistakenly interpreted as a regular compressed pointer. Therefore, V8 adds **`r14`**, which represents the base address of the V8 heap, but it is actually a **`ProtectedPointer`** with the value 0xfca00046ae1. This results in a type confusion, causing out-of-bounds access and triggering a segmentation fault.
   - The vmmap output shows that **`ProtectedPointer`** and regular compressed pointers are stored at different base address offsets, specifically 0xfca00000000 and 0x13c800000000, respectively. Although both are tagged pointers, due to different pointer compression base addresses, they should be treated as different types.
     
     ```
     pwndbg> vmmap
     LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
                  Start                End Perm     Size Offset File
          0xfca00000000      0xfca00001000 rw-p     1000      0 [anon_fca00000]
          0xfca00001000      0xfca00040000 ---p    3f000      0 [anon_fca00001]
          0xfca00040000      0xfca000c0000 rw-p    80000      0 [anon_fca00040]
          0xfca000c0000      0xfca40000000 ---p 3ff40000      0 [anon_fca000c0]
         0x13c000000000     0x13c800000000 ---p 800000000      0 [anon_13c000000]
         0x13c800000000     0x13c800010000 r--p    10000      0 [anon_13c800000]
         0x13c800010000     0x13c800020000 ---p    10000      0 [anon_13c800010]
         0x13c800020000     0x13c800040000 r--p    20000      0 [anon_13c800020]
         0x13c800040000     0x13c800143000 rw-p   103000      0 [anon_13c800040]
     
     ```
3. **turboshaft Optimization Before and After Code**:
   
   Further analysis of the code before and after optimization:
   
   Instruction [0] **`movq rdi, [rdi + 0x1f]`** clearly shows **`rdi`** being treated as a full **`Protected`** heap tagged pointer without adding the **`Protected`** heap base address, indicating it is an 8-byte pointer.
   
   However, from instruction [1] **`movq rdi, [r14 + rdi*1 + 0x1f]`**, it is evident that the turboshaft wasm optimization mistakenly interprets it as a regular compressed pointer, incorrectly adding the V8 heap base address.
   
   ```
   out/x64.release/d8 poc.js  --turboshaft-wasm --experimental-wasm-imported-strings --print-wasm-code                      
   --- WebAssembly code ---
   name: wasm-function[17]
   index: 17
   kind: wasm function
   compiler: Liftoff
   Body (size = 384 = 332 + 52 padding)
   Instructions (size = 320)
   0x35245b9a7840     0  4531e4               xorl r12,r12
   0x35245b9a7843     3  e828f9ffff           call 0x35245b9a7170  (jump table)
   0x35245b9a7848     8  4881ec18000000       REX.W subq rsp,0x18
   0x35245b9a784f     f  8bc0                 movl rax,rax
   0x35245b9a7851    11  8bd2                 movl rdx,rdx
   0x35245b9a7853    13  8bc9                 movl rcx,rcx
   0x35245b9a7855    15  493b65a0             REX.W cmpq rsp,[r13-0x60]
   0x35245b9a7859    19  0f8601010000         jna 0x35245b9a7960  <+0x120>
   0x35245b9a785f    1f  49ba9a9999999999f13f REX.W movq r10,0x3ff199999999999a
   0x35245b9a7869    29  c4c1f96ec2           vmovq xmm0,r10
   0x35245b9a786e    2e  c463010bf80b         vroundsd xmm15,xmm15,xmm0,0xb
   0x35245b9a7874    34  c4c1fb2cdf           vcvttsd2siq rbx,xmm15
   0x35245b9a7879    39  8bdb                 movl rbx,rbx
   0x35245b9a787b    3b  c461832af3           vcvtqsi2sd xmm14,xmm15,rbx
   0x35245b9a7880    40  c441792ef7           vucomisd xmm14,xmm15
   0x35245b9a7885    45  0f8b07000000         jpo 0x35245b9a7892  <+0x52>
   0x35245b9a788b    4b  33db                 xorl rbx,rbx
   0x35245b9a788d    4d  e925000000           jmp 0x35245b9a78b7  <+0x77>
   0x35245b9a7892    52  0f841f000000         jz 0x35245b9a78b7  <+0x77>
   0x35245b9a7898    58  66450f57ff           xorpd xmm15,xmm15
   0x35245b9a789d    5d  c4c1792ec7           vucomisd xmm0,xmm15
   0x35245b9a78a2    62  0f870a000000         ja 0x35245b9a78b2  <+0x72>
   0x35245b9a78a8    68  bb00000000           movl rbx,(nil)
   0x35245b9a78ad    6d  e905000000           jmp 0x35245b9a78b7  <+0x77>
   0x35245b9a78b2    72  bbffffffff           movl rbx,0xffffffff
   0x35245b9a78b7    77  8b7e77               movl rdi,[rsi+0x77]
   0x35245b9a78ba    7a  490bbde0010000       REX.W orq rdi,[r13+0x1e0]
   0x35245b9a78c1    81  488b7f1f             REX.W movq rdi,[rdi+0x1f]//------>[0]
   0x35245b9a78c5    85  48c1ef10             REX.W shrq rdi, 16
   0x35245b9a78c9    89  8945dc               movl [rbp-0x24],rax
   0x35245b9a78cc    8c  8955d8               movl [rbp-0x28],rdx
   0x35245b9a78cf    8f  894dd4               movl [rbp-0x2c],rcx
   0x35245b9a78d2    92  4989e2               REX.W movq r10,rsp
   0x35245b9a78d5    95  4883ec08             REX.W subq rsp,0x8
   0x35245b9a78d9    99  4883e4f0             REX.W andq rsp,0xf0
   0x35245b9a78dd    9d  4c891424             REX.W movq [rsp],r10
   0x35245b9a78e1    a1  8bf7                 movl rsi,rdi
   0x35245b9a78e3    a3  8bfb                 movl rdi,rbx
   0x35245b9a78e5    a5  48b8708a97ba8f550000 REX.W movq rax,0x558fba978a70
   0x35245b9a78ef    af  4c8d150a000000       REX.W leaq r10,[rip+0xa]
   0x35245b9a78f6    b6  4d895578             REX.W movq [r13+0x78],r10
   0x35245b9a78fa    ba  49896d70             REX.W movq [r13+0x70],rbp
   0x35245b9a78fe    be  ffd0                 call rax
   0x35245b9a7900    c0  49c7457000000000     REX.W movq [r13+0x70],0x0
   0x35245b9a7908    c8  488b2424             REX.W movq rsp,[rsp]
   0x35245b9a790c    cc  8bd8                 movl rbx,rax
   0x35245b9a790e    ce  f30fbddb             lzcntl rbx,rbx
   0x35245b9a7912    d2  4c8b55f0             REX.W movq r10,[rbp-0x10]
   0x35245b9a7916    d6  4d8b526f             REX.W movq r10,[r10+0x6f]
   0x35245b9a791a    da  41812a0e010000       subl [r10],0x10e
   0x35245b9a7921    e1  0f884d000000         js 0x35245b9a7974  <+0x134>
   0x35245b9a7927    e7  488b45e8             REX.W movq rax,[rbp-0x18]
   0x35245b9a792b    eb  83400702             addl [rax+0x7],0x2
   0x35245b9a792f    ef  8bc3                 movl rax,rbx
   0x35245b9a7931    f1  b901000000           movl rcx,0x1
   0x35245b9a7936    f6  ba01000000           movl rdx,0x1
   0x35245b9a793b    fb  488b75f0             REX.W movq rsi,[rbp-0x10]
   0x35245b9a793f    ff  ff7508               push [rbp+0x8]
   0x35245b9a7942   102  ff7500               push [rbp+0x0]
   0x35245b9a7945   105  4c8b542408           REX.W movq r10,[rsp+0x8]
   0x35245b9a794a   10a  4c895508             REX.W movq [rbp+0x8],r10
   0x35245b9a794e   10e  4c8b1424             REX.W movq r10,[rsp]
   0x35245b9a7952   112  4c895500             REX.W movq [rbp+0x0],r10
   0x35245b9a7956   116  488d6500             REX.W leaq rsp,[rbp+0x0]
   0x35245b9a795a   11a  5d                   pop rbp
   0x35245b9a795b   11b  e9a0f6ffff           jmp 0x35245b9a7000  (jump table)
   0x35245b9a7960   120  50                   push rax
   0x35245b9a7961   121  51                   push rcx
   0x35245b9a7962   122  52                   push rdx
   0x35245b9a7963   123  e8a8f9ffff           call 0x35245b9a7310  (jump table)
   0x35245b9a7968   128  5a                   pop rdx
   0x35245b9a7969   129  59                   pop rcx
   0x35245b9a796a   12a  58                   pop rax
   0x35245b9a796b   12b  488b75f0             REX.W movq rsi,[rbp-0x10]
   0x35245b9a796f   12f  e9ebfeffff           jmp 0x35245b9a785f  <+0x1f>
   0x35245b9a7974   134  53                   push rbx
   0x35245b9a7975   135  e8e6f7ffff           call 0x35245b9a7160  (jump table)
   0x35245b9a797a   13a  5b                   pop rbx
   0x35245b9a797b   13b  ebaa                 jmp 0x35245b9a7927  <+0xe7>
   0x35245b9a797d   13d  0f1f00               nop
   
   Source positions:
    pc offset  position
          123         0  statement
          135        22  statement
   
   Safepoints (entries = 1, byte size = 12)
   0x35245b9a7968    128  slots (sp->fp): 0000000000000000
   
   RelocInfo (size = 0)
   
   --- End code ---
   --- WebAssembly code ---
   name: wasm-function[17]
   index: 17
   kind: wasm function
   compiler: TurboFan
   Body (size = 192 = 180 + 12 padding)
   Instructions (size = 172)
   0x35245b9a79c0     0  55                   push rbp
   0x35245b9a79c1     1  4889e5               REX.W movq rbp,rsp
   0x35245b9a79c4     4  6a08                 push 0x8
   0x35245b9a79c6     6  56                   push rsi
   0x35245b9a79c7     7  c5f976c0             vpcmpeqd xmm0,xmm0,xmm0
   0x35245b9a79cb     b  c5f973f036           vpsllq xmm0,xmm0,54
   0x35245b9a79d0    10  c5f973d002           vpsrlq xmm0,xmm0,2
   0x35245b9a79d5    15  c5fb2cd8             vcvttsd2si rbx,xmm0
   0x35245b9a79d9    19  85db                 testl rbx,rbx
   0x35245b9a79db    1b  0f8929000000         jns 0x35245b9a7a0a  <+0x4a>
   0x35245b9a79e1    21  49ba000000000000e0c1 REX.W movq r10,0xc1e0000000000000
   0x35245b9a79eb    2b  c441f96efa           vmovq xmm15,r10
   0x35245b9a79f0    30  c50358f8             vaddsd xmm15,xmm15,xmm0
   0x35245b9a79f4    34  c4c17b2cdf           vcvttsd2si rbx,xmm15
   0x35245b9a79f9    39  85db                 testl rbx,rbx
   0x35245b9a79fb    3b  0f8809000000         js 0x35245b9a7a0a  <+0x4a>
   0x35245b9a7a01    41  41ba00000080         movl r10,0x80000000
   0x35245b9a7a07    47  410bda               orl rbx,r10
   0x35245b9a7a0a    4a  448bd3               movl r10,rbx
   0x35245b9a7a0d    4d  c4c1832aca           vcvtqsi2sd xmm1,xmm15,r10
   0x35245b9a7a12    52  c5f92ec1             vucomisd xmm0,xmm1
   0x35245b9a7a16    56  0f8a3b000000         jpe 0x35245b9a7a57  <+0x97>
   0x35245b9a7a1c    5c  0f8535000000         jnz 0x35245b9a7a57  <+0x97>
   0x35245b9a7a22    62  8b7e77               movl rdi,[rsi+0x77]
   0x35245b9a7a25    65  490bbde0010000       REX.W orq rdi,[r13+0x1e0]
   0x35245b9a7a2c    6c  498b7c3e1f           REX.W movq rdi,[r14+rdi*1+0x1f] //------->[1]
   0x35245b9a7a31    71  48c1ff10             REX.W sarq rdi, 16
   0x35245b9a7a35    75  8bff                 movl rdi,rdi
   0x35245b9a7a37    77  83e71f               andl rdi,0x1f
   0x35245b9a7a3a    7a  8bcf                 movl rcx,rdi
   0x35245b9a7a3c    7c  d3cb                 rorl rbx, cl
   0x35245b9a7a3e    7e  f30fbdc3             lzcntl rax,rbx
   0x35245b9a7a42    82  488b6d00             REX.W movq rbp,[rbp+0x0]
   0x35245b9a7a46    86  b901000000           movl rcx,0x1
   0x35245b9a7a4b    8b  488bd1               REX.W movq rdx,rcx
   0x35245b9a7a4e    8e  4883c418             REX.W addq rsp,0x18
   0x35245b9a7a52    92  e9a9f5ffff           jmp 0x35245b9a7000  (jump table)
   0x35245b9a7a57    97  8b5e77               movl rbx,[rsi+0x77]
   0x35245b9a7a5a    9a  490b9de0010000       REX.W orq rbx,[r13+0x1e0]
   0x35245b9a7a61    a1  488bfb               REX.W movq rdi,rbx
   0x35245b9a7a64    a4  bbffffffff           movl rbx,0xffffffff
   0x35245b9a7a69    a9  ebc1                 jmp 0x35245b9a7a2c  <+0x6c>
   0x35245b9a7a6b    ab  90                   nop
   
   Source positions:
    pc offset  position
           62        14
           6c        14
           97        14
   
   Safepoints (entries = 0, byte size = 8)
   
   RelocInfo (size = 4)
   0x35245b9a7a53  internal wasm call
   
   --- End code ---
   
   
   ```
4. **Specific vulnerability code:**
   
   Based on the entry point ([https://chromium.googlesource.com/v8/v8/+/bacbfe2c1f0722025a90c33e2b586ccc16ee8e11^!/#F0](https://chromium.googlesource.com/v8/v8/+/bacbfe2c1f0722025a90c33e2b586ccc16ee8e11%5E%21/#F0)), we can quickly locate the issue. Due to the recently introduced ProtectedPointer representation being handled somewhat inconsistently, this commit changed ProtectedPointer from a WordPtr to a Tagged representation.
   
   WordPtr is an 8-byte full pointer on a 64-bit operating system, consistent with the pre-optimization state of rdi. However, after this commit, by marking it as a Tagged representation, rdi was treated as a regular V8 compressed heap pointer. Consequently, an incorrect addition of the heap address occurred, leading to an out-of-bounds (OOB) access.

```
   RegisterRepresentation ToRegisterRepresentation() const {
     switch (*this) {
       case Int8():
@@ -732,9 +660,8 @@
       case TaggedPointer():
       case TaggedSigned():
       case IndirectPointer():
-        return RegisterRepresentation::Tagged();
       case ProtectedPointer():
-        return RegisterRepresentation::WordPtr();
+        return RegisterRepresentation::Tagged();

```
```
static constexpr MaybeRegisterRepresentation WordPtr() {
    if constexpr (kSystemPointerSize == 4) {
      return Word32();
    } else {
      DCHECK_EQ(kSystemPointerSize, 8);
      return Word64();
    }
  }
 
static constexpr MaybeRegisterRepresentation Tagged() {
    return MaybeRegisterRepresentation(Enum::kTagged);
  }

```

By confirming that this vulnerability only occurs on 64-bit systems, it further verifies that the issue lies in the improper handling of pointer size.

### am...@chromium.org (2024-05-29)

I'm able to reproduce this on ToT

```

AddressSanitizer:DEADLYSIGNAL
=================================================================
==475==ERROR: AddressSanitizer: SEGV on unknown address (pc 0x7a3de4526a2c bp 0x7fff35209770 sp 0x7fff35209760 T0)
==475==The signal is caused by a READ memory access.
==475==Hint: this fault was caused by a dereference of a high value address (see register values below).  Disassemble the provided pc to learn which register was used.
SCARINESS: 20 (wild-addr-read)
    #0 0x7a3de4526a2c  (<unknown module>)
    #1 0x5c0d0f16a5c9 in Builtins_JSToWasmWrapperAsm setup-isolate-deserialize.cc
    #2 0x5c0d0f242afe in Builtins_JSToWasmWrapper setup-isolate-deserialize.cc
    #3 0x5c0d0f0d4ce6 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #4 0x5c0d0f0d275b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #5 0x5c0d0f0d249e in Builtins_JSEntry setup-isolate-deserialize.cc
    #6 0x5c0d0c555215 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:419:22
    #7 0x5c0d0c555bf7 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>) src/execution/execution.cc:516:10
    #8 0x5c0d0c13e529 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2110:7
    #9 0x5c0d0c0b01af in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) src/d8/d8.cc:969:44
    #10 0x5c0d0c0cf432 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:4499:10
    #11 0x5c0d0c0d64b7 in v8::Shell::RunMainIsolate(v8::Isolate*, bool) src/d8/d8.cc:5364:37
    #12 0x5c0d0c0d5f2c in v8::Shell::RunMain(v8::Isolate*, bool) src/d8/d8.cc:5273:18
    #13 0x5c0d0c0d83aa in v8::Shell::Main(int, char**) src/d8/d8.cc:6164:18
    #14 0x7a3de4d8d082 in __libc_start_main /build/glibc-BHL3KM/glibc-2.31/csu/../csu/libc-start.c:308:16
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV (<unknown module>)
==475==ABORTING


```

### pe...@google.com (2024-05-29)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-29)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### je...@gmail.com (2024-05-30)

hello, any update?

### sa...@google.com (2024-05-30)

Today is a public holiday in Germany and I believe Jakob is out of Friday, so will only be back on Monday. Cc'ing some other Wasm folks in case someone wants to take this.

### ml...@chromium.org (2024-05-31)

Can someone share the `args.gn` that reproduce this and if any specific `ASAN_OPTIONS` have to be set? I can't reproduce it on my asan build using the flags provided in the initial description.
It compiles with turboshaft and then hangs due to the endless "loop" (the `main` function `return_call`s itself unconditionally).

### cl...@appspot.gserviceaccount.com (2024-05-31)

Detailed Report: https://clusterfuzz.com/testcase?key=5163656202354688

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: Segv on unknown address
Crash Address: 
Crash State:
  Builtins_JSToWasmWrapperAsm
  Builtins_JSToWasmWrapper
  Builtins_InterpreterEntryTrampoline
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8&revision=94116

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5163656202354688

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sa...@google.com (2024-05-31)

I managed to reproduce this on Clusterfuzz. The gn args from that job:

```
dcheck_always_on = false
is_asan = true
is_clang = true
is_component_build = false
is_debug = false
is_lsan = true
target_cpu = "x64"
use_remoteexec = true
v8_enable_google_benchmark = true
v8_enable_test_features = true
v8_enable_verify_heap = true
v8_no_inline = true

```

### jk...@chromium.org (2024-06-03)

To repro in Debug mode, this needs `--nodebug-code`. It also needs `--turboshaft-wasm-instruction-selection-staged` (which is implied by `--future` currently).

Hard to say whether this is exploitable. It creates a value whose lower half is a pointer into trusted space, but whose upper half is the regular heap base address. Out of caution, I'll leave it classified as a security vulnerability -- I wouldn't be surprised if a heap spraying attack could use this to cause real havoc.

Fix in flight: <https://chromium-review.googlesource.com/c/v8/v8/+/5592473>

### ap...@google.com (2024-06-03)

Project: v8/v8
Branch: main

commit 8dc0701804b21d4a546b4076677aab31dbb84c12
Author: Jakob Kummerow <jkummerow@chromium.org>
Date:   Mon Jun 03 16:17:18 2024

    [turboshaft] Phis with protected-load inputs can't be compressed
    
    When a Phi has an input that's a load of a ProtectedPointer, we must not
    choose compressed representation for this Phi, because we can't restore
    its uncompressed value by using the heap cage base.
    
    Fixed: 343035068
    Change-Id: I9b6c13f446ec254b426fd905d4aa58436cc2ed74
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5592473
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94213}

M       src/compiler/turboshaft/decompression-optimization.cc
A       test/mjsunit/regress/wasm/regress-343035068.js

https://chromium-review.googlesource.com/5592473


### 24...@project.gserviceaccount.com (2024-06-04)

ClusterFuzz testcase 4790952479621120 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=94212:94213

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### pe...@google.com (2024-06-12)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M127. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge approved: your change passed merge requirements and is auto-approved for M127. Please go ahead and merge the CL to branch 6533 (refs/branch-heads/6533) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### jk...@chromium.org (2024-06-13)

#15: The fix to merge is #13, and that landed in time for 127 anyway.

### sp...@google.com (2024-06-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 for high quality report of memory corruption in the renderer / sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-13)

Congratulations, Jerry! Thank you for your efforts in producing this high quality report and reporting this issue to us -- great work!

### pe...@google.com (2024-09-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/343035068)*

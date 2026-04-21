# Security: CSA_DCHECK failed: Torque assert 'IsConstructor(target)'

| Field | Value |
|-------|-------|
| **Issue ID** | [40064002](https://issues.chromium.org/issues/40064002) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | wh...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2023-04-12 |
| **Bounty** | $10,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**

# 

# Fatal error in ../../src/objects/object-type.cc, line 81

# Type cast failed in Parameter 0 at ../../src/builtins/builtins-constructor-gen.cc:179

Expected SharedFunctionInfo but found 0x22e900000251: [Oddball] in ReadOnlySpace: #undefined

# 

**VERSION**  

only tested at current HEAD

**REPRODUCTION CASE**

It's hard to trigger.  

please run  

for i in {1..999}; do  

./d8 --maglev poc.js  

if [ $? -ne 0 ]; then break; fi;  

done

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- [1.js](attachments/1.js) (text/plain, 925 B)
- [simplescreenrecorder-(4).mp4](attachments/simplescreenrecorder-(4).mp4) (video/mp4, 4.2 MB)
- [simplescreenrecorder-(2).mp4](attachments/simplescreenrecorder-(2).mp4) (video/mp4, 264.1 KB)
- [1.png](attachments/1.png) (image/png, 25.6 KB)

## Timeline

### [Deleted User] (2023-04-12)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-04-12)

bisect 

may this commit https://chromium-review.googlesource.com/c/v8/v8/+/4100708 
[maglev] Share more generic nodes

void FastCreateClosure::GenerateCode(MaglevAssembler* masm,
                                     const ProcessingState& state) {
  using D = CallInterfaceDescriptorFor<Builtin::kFastNewClosure>::type;

  DCHECK_EQ(ToRegister(context()), D::ContextRegister());
  __ Move(D::GetRegisterParameter(D::kSharedFunctionInfo),   <-----
          shared_function_info().object());
  __ Move(D::GetRegisterParameter(D::kFeedbackCell), feedback_cell().object());
  __ CallBuiltin(Builtin::kFastNewClosure);
  masm->DefineExceptionHandlerAndLazyDeoptPoint(this);
}


TF_BUILTIN(FastNewClosure, ConstructorBuiltinsAssembler) {
  auto shared_function_info =
      Parameter<SharedFunctionInfo>(Descriptor::kSharedFunctionInfo);    <-----
  auto feedback_cell = Parameter<FeedbackCell>(Descriptor::kFeedbackCell);
  auto context = Parameter<Context>(Descriptor::kContext);
...

shared_function_info_ object related memory should be freed or cleaned during code generate, also may heap or gc related.

[1] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:v8/src/maglev/maglev-ir.cc;l=2130;bpv=0;bpt=1

### cl...@chromium.org (2023-04-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5169337707724800.

### wh...@gmail.com (2023-04-13)

I still can repro it using https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-87053.zip?generation=1681345270037009&alt=media


### wh...@gmail.com (2023-04-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-04-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4632949576892416.

### jd...@chromium.org (2023-04-13)

I can't reproduce this on trunk, but I can with the d8 build you reference. To me that sounds like trunk churn.

Can you still reproduce this?

### wh...@gmail.com (2023-04-14)

I still can reproduce the bug. 

87079 https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-87079.zip?generation=1681413920230091&alt=media

➜  d8-linux-debug-v8-component-87079 fire.bash ./d8 ~/program_20230411210023_96290E99-CDE3-4C82-9D4E-81B00C5853B9_flaky.js --maglev


#
# Fatal error in ../../src/objects/object-type.cc, line 81
# Type cast failed in Parameter 0 at ../../src/builtins/builtins-constructor-gen.cc:179
  Expected SharedFunctionInfo but found 0x2d7d00000251: [Oddball] in ReadOnlySpace: #undefined

#
#
#
#FailureMessage Object: 0x7ffec760b170
==== C stack trace ===============================

    /home/uuu/tmp/d8-linux-debug-v8-component-87079/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fb5e704b553]
    /home/uuu/tmp/d8-linux-debug-v8-component-87079/libv8_libplatform.so(+0x192dd) [0x7fb5e6ff12dd]
    /home/uuu/tmp/d8-linux-debug-v8-component-87079/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x182) [0x7fb5e702a902]
    /home/uuu/tmp/d8-linux-debug-v8-component-87079/libv8.so(v8::internal::CheckObjectType(unsigned long, unsigned long, unsigned long)+0x3dde) [0x7fb5e977f16e]
    /home/uuu/tmp/d8-linux-debug-v8-component-87079/libv8.so(+0xfa89df) [0x7fb5e7fff9df]
/home/uuu/repo/browser/fire.bash: line 4: 2511186 Trace/breakpoint trap   (core dumped) $@


### [Deleted User] (2023-04-14)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wh...@gmail.com (2023-04-14)

[Empty comment from Monorail migration]

### jd...@chromium.org (2023-04-14)

I still can't reproduce this with a recent build, including the one you've sent, but we'll see what v8 folks have to say. Setting labels tentatively assuming that it's valid.

victorgomes@, would you mind taking a quick look? Feel free to kick it back to me if you have no idea what's happening or if it doesn't seem valid to you. Thanks!

[Monorail components: Blink>JavaScript>Compiler>Maglev]

### wh...@gmail.com (2023-04-15)

Note that using 87104 (https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-87104.zip?generation=1681511871207012&alt=media) still can reproduce

### wh...@gmail.com (2023-04-19)

any update?

### wh...@gmail.com (2023-04-19)

note that at current HEAD still can reproduce and still hard to reproduce. 



### wh...@gmail.com (2023-04-21)

ping ?

### wh...@gmail.com (2023-04-27)

ping

### wh...@gmail.com (2023-04-27)

at current HEAD 
87303 https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-87303.zip?generation=1682590454734411&alt=media
still can stable reproduce in my local.

when you will handle the bug?

#
# Fatal error in ../../src/objects/object-type.cc, line 81
# Type cast failed in Parameter 0 at ../../src/builtins/builtins-constructor-gen.cc:179
  Expected SharedFunctionInfo but found 0xed00000251: [Oddball] in ReadOnlySpace: #undefined

#
#
#
#FailureMessage Object: 0x7ffc72728ca0
==== C stack trace ===============================

    /home/uuu/tmp/d8-linux-debug-v8-component-87303/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fd8ae681f43]
    /home/uuu/tmp/d8-linux-debug-v8-component-87303/libv8_libplatform.so(+0x18b4d) [0x7fd8ae627b4d]
    /home/uuu/tmp/d8-linux-debug-v8-component-87303/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x154) [0x7fd8ae6614d4]
    /home/uuu/tmp/d8-linux-debug-v8-component-87303/libv8.so(+0x272f801) [0x7fd8b0dbc801]
    /home/uuu/tmp/d8-linux-debug-v8-component-87303/libv8.so(+0xf989df) [0x7fd8af6259df]
/home/uuu/repo/browser/fire.bash: line 4: 3742746 Trace/breakpoint trap   (core dumped) $@

+victorgomes in cc

### wh...@gmail.com (2023-04-27)

@victorgomes

### vi...@chromium.org (2023-04-27)

Thank you for the bug issue, I will have a look soon.

### vi...@chromium.org (2023-04-27)

I cannot repro locally, even when running
for i in {1..999}; do 
 ./d8 --maglev poc.js 
 if [ $? -ne 0 ]; then break; fi; 
done

and running using the binary you mentioned:  https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-87303.zip?generation=1682590454734411&alt=media


Nor ClusterFuzz seems to be able to reproduce.

Regarding https://crbug.com/chromium/1432470#c2:
"shared_function_info_ object related memory should be freed or cleaned during code generate, also may heap or gc related."

The shared function is not (and should not) be freed during code generation. This does not look like a memory issue, but wrong parameter to the builtin.



### wh...@gmail.com (2023-05-05)

@victorgomes

Hi, I tested d8-linux-debug-v8-component-87460 ( https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-87460.zip?generation=1683259367098812&alt=media)

the bug still can reproduce, you need try to fix it. 

BTW, it's easy to reproduce by loop 999 times in my local machine. 

#
# Fatal error in ../../src/objects/object-type.cc, line 81
# Type cast failed in Parameter 0 at ../../src/builtins/builtins-constructor-gen.cc:179
  Expected SharedFunctionInfo but found 0x1b4000000251: [Oddball] in ReadOnlySpace: #undefined

#
#
#
#FailureMessage Object: 0x7ffe3c6abc18
==== C stack trace ===============================

    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7fcb21115c6e]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8_libplatform.so(+0x4dfad) [0x7fcb21069fad]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x1ac) [0x7fcb210e3d9c]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::CheckObjectType(unsigned long, unsigned long, unsigned long)+0x8cb3) [0x7fcb25406cf3]
    /home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(+0x2a0e15f) [0x7fcb23b3915f]
/home/uuu/repo/browser/fire.bash: line 4: 1986835 Trace/breakpoint trap   (core dumped) $@



### wh...@gmail.com (2023-05-05)

Or 
using fuzzbuild d8 to reproduce it 
```
gn gen out/fuzzbuild --args='is_debug=false dcheck_always_on=true v8_static_library=true v8_enable_slow_dchecks=true v8_enable_v8_checks=true v8_enable_verify_heap=true v8_enable_verify_csa=true v8_fuzzilli=true sanitizer_coverage_flags="trace-pc-guard" target_cpu="x64"
ninja -C ./out/fuzzbuild d8
```
then 
```
for i in {1..999}; do 
 ./d8 --maglev poc.js 
 if [ $? -ne 0 ]; then break; fi; 
done
```
you will get 
[COV] no shared memory bitmap available, skipping
[COV] edge counters initialized. Shared memory: (null) with 1225432 edges
Received signal 11 SEGV_ACCERR 233973726577

==== C stack trace ===============================

 [0x5627f24643b2]
 [0x7f81be2dc420]
 [0x5627f5408943]
[end of stack trace]
/home/uuu/repo/browser/fire.bash: line 4: 2243169 Segmentation fault 

it's very fast to reproduce in my local.


### wh...@gmail.com (2023-05-05)

 ► 0x555558cd9943 <Builtins_FastNewClosure+131>    movzx  r8d, byte ptr [rcx + 3]
   0x555558cd9948 <Builtins_FastNewClosure+136>    lea    rdx, [r8*4]
   0x555558cd9950 <Builtins_FastNewClosure+144>    lea    r8, [rdx + rdi]
   0x555558cd9954 <Builtins_FastNewClosure+148>    cmp    qword ptr [r13 + 0x48], r8
   0x555558cd9958 <Builtins_FastNewClosure+152>    jbe    Builtins_FastNewClosure+284                <Builtins_FastNewClosure+284>
 
   0x555558cd995e <Builtins_FastNewClosure+158>    mov    qword ptr [r13 + 0x40], r8
   0x555558cd9962 <Builtins_FastNewClosure+162>    add    rdi, 1
   0x555558cd9966 <Builtins_FastNewClosure+166>    mov    dword ptr [rdi - 1], ecx
   0x555558cd9969 <Builtins_FastNewClosure+169>    lea    r8, [rdx - 1]
   0x555558cd996d <Builtins_FastNewClosure+173>    cmp    r8, 0x1f
   0x555558cd9971 <Builtins_FastNewClosure+177>    jle    Builtins_FastNewClosure+219                <Builtins_FastNewClosure+219>

pwndbg> x/20gx $r8d
0xffffffffc317478d:     Cannot access memory at address 0xffffffffc317478d
pwndbg> 


+victorgomes in cc

### wh...@gmail.com (2023-05-08)

at current HEAD still can reproduce, please using fuzzbuild-d8 to reproduce. 

The bug took a lot of time to handle, please handle it as soon as possible.

+victorgomes 

### vi...@chromium.org (2023-05-08)

I managed to reproduce. This seems to be a race, I think.
We don't even compile maglev code:
```
[compiling method 0x2422000daf89 <SharedFunctionInfo> (target BASELINE)]
[completed compiling 0x2422000daf89 <SharedFunctionInfo> (target BASELINE) - took 0.766 ms]
[marking 0x2422000db5d1 <JSFunction (sfi = 0x2422000daf89)> for optimization to MAGLEV, ConcurrencyMode::kConcurrent, reason: hot and stable]
[marking 0x2422000db5d1 <JSFunction (sfi = 0x2422000daf89)> for optimization to TURBOFAN, ConcurrencyMode::kConcurrent, reason: hot and stable]
[compiling method 0x2422000db5d1 <JSFunction (sfi = 0x2422000daf89)> (target TURBOFAN) OSR, mode: ConcurrencyMode::kConcurrent]
[completed compiling 0x2422000db5d1 <JSFunction (sfi = 0x2422000daf89)> (target TURBOFAN) OSR - took 0.088, 50.759, 0.099 ms]
[completed optimizing 0x2422000db5d1 <JSFunction (sfi = 0x2422000daf89)> (target TURBOFAN) OSR]
[marking dependent code 0x2422003fb2c1 <Code TURBOFAN> (0x2422000daf89 <SharedFunctionInfo>) (opt id 0) for deoptimization, reason: weak objects]


#
# Fatal error in ../../src/objects/object-type.cc, line 81
# Type cast failed in Parameter 0 at ../../src/builtins/builtins-constructor-gen.cc:179
  Expected SharedFunctionInfo but found 0x242200000251: [Oddball] in ReadOnlySpace: #undefined
```


### vi...@chromium.org (2023-05-08)

This is the code snippet produced by TF when running with `--print-code --code-comments`:
```
0x7f61b3f44447   407  418970ff             movl [r8-0x1],rsi
0x7f61b3f4444b   40b  41c7400304000000     movl [r8+0x3],0x4
0x7f61b3f44453   413  45894807             movl [r8+0x7],r9
0x7f61b3f44457   417  4189780b             movl [r8+0xb],rdi
0x7f61b3f4445b   41b  4c8985b8feffff       REX.W movq [rbp-0x148],r8
0x7f61b3f44462   422  48b8c1b00d002f3a0000 REX.W movq rax,0x3a2f000db0c1    ;; object: 0x3a2f000db0c1 <SharedFunctionInfo C45>
0x7f61b3f4446c   42c  48bb1db60d002f3a0000 REX.W movq rbx,0x3a2f000db61d    ;; object: 0x3a2f000db61d <FeedbackCell[many closures]>
0x7f61b3f44476   436  498bf0               REX.W movq rsi,r8
                    [ Inlined  Trampoline for call to FastNewClosure
0x7f61b3f44479   439  e8826c00a0           call 0x7f6153f4b100  (FastNewClosure)    ;; near builtin entry
                    ]
0x7f61b3f4447e   43e  49b81db20d002f3a0000 REX.W movq r8,0x3a2f000db21d    ;; object: 0x3a2f000db21d <FixedArray[7]>
```

This is the snippet when printing the code in gdb at the crash point:
```
0x7f61b3f44447   407  418970ff             movl [r8-0x1],rsi
0x7f61b3f4444b   40b  41c7400304000000     movl [r8+0x3],0x4
0x7f61b3f44453   413  45894807             movl [r8+0x7],r9
0x7f61b3f44457   417  4189780b             movl [r8+0xb],rdi
0x7f61b3f4445b   41b  4c8985b8feffff       REX.W movq [rbp-0x148],r8
0x7f61b3f44462   422  48b8510200002f3a0000 REX.W movq rax,0x3a2f00000251    ;; object: 0x3a2f00000251 <undefined>
0x7f61b3f4446c   42c  48bb510200002f3a0000 REX.W movq rbx,0x3a2f00000251    ;; object: 0x3a2f00000251 <undefined>
0x7f61b3f44476   436  498bf0               REX.W movq rsi,r8
                    [ Inlined  Trampoline for call to FastNewClosure
0x7f61b3f44479   439  e8826c00a0           call 0x7f6153f4b100  (FastNewClosure)    ;; near builtin entry
                    ]
0x7f61b3f4447e   43e  49b8510200002f3a0000 REX.W movq r8,0x3a2f00000251    ;; object: 0x3a2f00000251 <undefined>
```

It seems maybe GC has cleared the memory?

### vi...@chromium.org (2023-05-08)

GC is marking the code for deopt in MarkDependentCodeForDeoptimization
Then clearing the embedded objects in `code.ClearEmbeddedObjects(heap_);`
That's the reason why we see an undefined object.

### vi...@chromium.org (2023-05-08)

The issue is that we are keeping OSR code in the cache now, since https://chromium-review.googlesource.com/c/v8/v8/+/3607988, but we do not check if the code should be deoptimized in the OSR entry.

Basically, while running in SP, we trigger an OSR compilation, then a GC that mark the code for deoptimization (and clear the embedded objects), and finally call the bugus OSR code.


### vi...@chromium.org (2023-05-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-05-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/b9a0e4e607e1fab25e7d47b55f9a3c4c263fbfc1

commit b9a0e4e607e1fab25e7d47b55f9a3c4c263fbfc1
Author: Toon Verwaest <verwaest@chromium.org>
Date: Mon May 08 16:14:01 2023

[osr] Check whether the target is deoptimized

Bug: chromium:1432470
Change-Id: I944ae6b6ae73d2755c90fdc2d3d32885f5de65d0
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4513858
Auto-Submit: Toon Verwaest <verwaest@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/main@{#87510}

[modify] https://crrev.com/b9a0e4e607e1fab25e7d47b55f9a3c4c263fbfc1/src/runtime/runtime-compiler.cc


### wh...@gmail.com (2023-05-09)

oh, no, the bug not fixed. 

I can reproduce using 87514 (https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-87514.zip?generation=1683604142715164&alt=media)

#
# Fatal error in ../../src/objects/object-type.cc, line 81
# Type cast failed in Parameter 0 at ../../src/builtins/builtins-constructor-gen.cc:179
  Expected SharedFunctionInfo but found 0x151100000251: [Oddball] in ReadOnlySpace: #undefined

#

please check it. 

### wh...@gmail.com (2023-05-10)

@victorgomes

### jg...@chromium.org (2023-05-10)

#28 we do check the kMarkedForDeoptimizationBit, see [0].

Perhaps that check is missing on some paths, or this is a lazy deopt, or somehow related to the Deoptimizer::DeoptExitIsInsideOsrLoop optimization [1].

[0] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:v8/src/codegen/x64/macro-assembler-x64.cc;l=3264;drc=4936d4eca88a0b7e9cdebc8a65bb860683db822d
[1] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/runtime/runtime-compiler.cc;l=392;drc=b9a0e4e607e1fab25e7d47b55f9a3c4c263fbfc1

[Monorail components: -Blink>JavaScript>Compiler>Maglev Blink>JavaScript>Compiler]

### jg...@chromium.org (2023-05-10)

Repros reliably with --no-sparkplug.

### jg...@chromium.org (2023-05-10)

Indeed in OnStackReplacement we enter this Code obj:

0x3720046ee9d: [Code] in OldSpace
 - map: 0x037200000d9d <Map[60](CODE_TYPE)>
 - kind: TURBOFAN
 - deoptimization_data_or_interpreter_data: 0x03720046e061 <FixedArray[191]>
 - position_table: 0x03720046df7d <ByteArray[218]>
 - instruction_stream: 0x7f53e0004031 <InstructionStream TURBOFAN>
 - instruction_start: 0x7f53e0004040
 - is_turbofanned: 1
 - stack_slots: 50
 - marked_for_deoptimization: 1
 - embedded_objects_cleared: 1
 - can_have_weak_objects: 1
 - instruction_size: 6140
 - metadata_size: 408
 - inlined_bytecode_size: 0
 - osr_offset: 501
 - handler_table_offset: 408
 - unwinding_info_offset: 408
 - code_comments_offset: 408
 - instruction_stream.relocation_info: 0x03720046e8a9 <ByteArray[1516]>
 - instruction_stream.body_size: 6548

.. despite presumably having checked the deopt bit at https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:v8/src/interpreter/interpreter-assembler.cc;l=1379;drc=4936d4eca88a0b7e9cdebc8a65bb860683db822d.

### jg...@chromium.org (2023-05-10)

The culprit is

crrev.com/c/4430993/2/src/interpreter/interpreter-assembler.cc

which adds a call to DecreaseInterruptBudget between 1) having checked the deopt bit and 2) actually doing the OSR. DecreaseInterruptBudget triggers GC finalization which sets the deopt bit.

### jg...@chromium.org (2023-05-10)

Related discussion: crrev.com/c/4399952/9..16/src/interpreter/interpreter-generator.cc#b2224

### jg...@chromium.org (2023-05-10)

[Empty comment from Monorail migration]

### jg...@chromium.org (2023-05-10)

Possibly related: chromium:1442603

### jg...@chromium.org (2023-05-10)

Fix in flight crrev.com/c/4518765

### jg...@chromium.org (2023-05-10)

This will need to be merged to 114 (stable cut on May 23).

### jg...@chromium.org (2023-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-10)

Merge review required: M114 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jg...@chromium.org (2023-05-10)

1. Fixes a security issue.
2. crrev.com/c/4518765 (will be landed in a sec)
3. Not yet, let's wait til tomorrow.
4. No
5. N/A
6. N/A

### jg...@chromium.org (2023-05-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-05-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/33db04dc7e11b9ac13444454e725e12b04dc174c

commit 33db04dc7e11b9ac13444454e725e12b04dc174c
Author: Jakob Linke <jgruber@chromium.org>
Date: Wed May 10 11:13:42 2023

[osr] Avoid handling interrupts in the middle of OSR

.. since interrupts may trigger code deoptimization, which in turn
invalidates assumptions we've already checked at the beginning of
OnStackReplacement.

This CL removes the problematic interrupt budget updates around OSR.

Fixed: chromium:1432470,chromium:1442603
Change-Id: I035acb8f6cc677917e82d3a7ad1082a5c7128904
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4518765
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Auto-Submit: Jakob Linke <jgruber@chromium.org>
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/main@{#87570}

[modify] https://crrev.com/33db04dc7e11b9ac13444454e725e12b04dc174c/src/interpreter/interpreter-assembler.cc
[add] https://crrev.com/33db04dc7e11b9ac13444454e725e12b04dc174c/test/mjsunit/regress/regress-1432470.js
[modify] https://crrev.com/33db04dc7e11b9ac13444454e725e12b04dc174c/src/baseline/baseline-compiler.cc
[add] https://crrev.com/33db04dc7e11b9ac13444454e725e12b04dc174c/test/mjsunit/regress/regress-1442603.js
[modify] https://crrev.com/33db04dc7e11b9ac13444454e725e12b04dc174c/test/mjsunit/mjsunit.status


### [Deleted User] (2023-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-10)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-10)

[Empty comment from Monorail migration]

### jg...@chromium.org (2023-05-11)

Temporarily removing the Merge-Review request since we're still discussing another possible fix (sorry for the noise).

### gi...@appspot.gserviceaccount.com (2023-05-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/5aac3c239786ee5b0cff8fe762598bc4cf77c2c2

commit 5aac3c239786ee5b0cff8fe762598bc4cf77c2c2
Author: Jakob Linke <jgruber@chromium.org>
Date: Thu May 11 09:59:54 2023

Revert "[osr] Avoid handling interrupts in the middle of OSR"

This reverts commit 33db04dc7e11b9ac13444454e725e12b04dc174c.

Reason for revert: Reverting in favor of crrev.com/c/4518604

Original change's description:
> [osr] Avoid handling interrupts in the middle of OSR
>
> .. since interrupts may trigger code deoptimization, which in turn
> invalidates assumptions we've already checked at the beginning of
> OnStackReplacement.
>
> This CL removes the problematic interrupt budget updates around OSR.
>
> Fixed: chromium:1432470,chromium:1442603
> Change-Id: I035acb8f6cc677917e82d3a7ad1082a5c7128904
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4518765
> Reviewed-by: Toon Verwaest <verwaest@chromium.org>
> Auto-Submit: Jakob Linke <jgruber@chromium.org>
> Commit-Queue: Toon Verwaest <verwaest@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#87570}

Change-Id: I0d51aadecdc9371a935d060de8ce1c492edffed5
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4521026
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Auto-Submit: Jakob Linke <jgruber@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/main@{#87588}

[modify] https://crrev.com/5aac3c239786ee5b0cff8fe762598bc4cf77c2c2/src/interpreter/interpreter-assembler.cc
[delete] https://crrev.com/66e4f4b05f744f2d37caae98749384029b118922/test/mjsunit/regress/regress-1432470.js
[modify] https://crrev.com/5aac3c239786ee5b0cff8fe762598bc4cf77c2c2/src/baseline/baseline-compiler.cc
[delete] https://crrev.com/66e4f4b05f744f2d37caae98749384029b118922/test/mjsunit/regress/regress-1442603.js
[modify] https://crrev.com/5aac3c239786ee5b0cff8fe762598bc4cf77c2c2/test/mjsunit/mjsunit.status


### gi...@appspot.gserviceaccount.com (2023-05-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/c2eda65a85d1c85f9037fa89b63ae725b18dbfbe

commit c2eda65a85d1c85f9037fa89b63ae725b18dbfbe
Author: Jakob Linke <jgruber@chromium.org>
Date: Thu May 11 07:20:57 2023

[osr] Avoid handling interrupts in the middle of OSR

.. since interrupts may trigger code deoptimization, which in turn
invalidates assumptions we've already checked at the beginning of
OnStackReplacement.

This CL disables the stack check as part of the bytecode budget
interrupt, i.e. we don't call stack_guard()->HandleInterrupts()
in Runtime_BytecodeBudgetInterrupt_{Ignition,Sparkplug}.

Fixed: chromium:1432470,chromium:1442603
Change-Id: I63dc51812741161cfb2f1cdb67c46e269d37f0f6
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4518604
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Jakob Linke <jgruber@chromium.org>
Cr-Commit-Position: refs/heads/main@{#87590}

[modify] https://crrev.com/c2eda65a85d1c85f9037fa89b63ae725b18dbfbe/src/interpreter/interpreter-assembler.cc
[modify] https://crrev.com/c2eda65a85d1c85f9037fa89b63ae725b18dbfbe/src/interpreter/interpreter-assembler.h
[add] https://crrev.com/c2eda65a85d1c85f9037fa89b63ae725b18dbfbe/test/mjsunit/regress/regress-1432470.js
[modify] https://crrev.com/c2eda65a85d1c85f9037fa89b63ae725b18dbfbe/src/baseline/baseline-compiler.cc
[add] https://crrev.com/c2eda65a85d1c85f9037fa89b63ae725b18dbfbe/test/mjsunit/regress/regress-1442603.js
[modify] https://crrev.com/c2eda65a85d1c85f9037fa89b63ae725b18dbfbe/src/baseline/baseline-compiler.h
[modify] https://crrev.com/c2eda65a85d1c85f9037fa89b63ae725b18dbfbe/test/mjsunit/mjsunit.status


### jg...@chromium.org (2023-05-16)

Requesting merge of crrev.com/c/4518604. Updated survey answers:

1. Fixes a security issue.
2. crrev.com/c/4518604
3. Yes
4. No
5. N/A
6. N/A

### [Deleted User] (2023-05-16)

Merge review required: M114 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-05-16)

[Empty comment from Monorail migration]

### jg...@chromium.org (2023-05-17)

(fyi the merge review questions are already answered in c#53.)

### jg...@chromium.org (2023-05-17)

Merge CL prepared at crrev.com/c/4543623.

### gi...@appspot.gserviceaccount.com (2023-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/0615e6e22c0007382b85bf467c6d8ce01ee636b2

commit 0615e6e22c0007382b85bf467c6d8ce01ee636b2
Author: Jakob Linke <jgruber@chromium.org>
Date: Thu May 11 07:20:57 2023

Merged: [osr] Avoid handling interrupts in the middle of OSR

.. since interrupts may trigger code deoptimization, which in turn
invalidates assumptions we've already checked at the beginning of
OnStackReplacement.

This CL disables the stack check as part of the bytecode budget
interrupt, i.e. we don't call stack_guard()->HandleInterrupts()
in Runtime_BytecodeBudgetInterrupt_{Ignition,Sparkplug}.

(cherry picked from commit c2eda65a85d1c85f9037fa89b63ae725b18dbfbe)

No-Try: true
No-Presubmit: true
No-Treechecks: true
Fixed: chromium:1432470,chromium:1442603
Change-Id: I63dc51812741161cfb2f1cdb67c46e269d37f0f6
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4518604
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Jakob Linke <jgruber@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#87590}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4543623
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.4@{#18}
Cr-Branched-From: 8a8a1e7086dacc426965d3875914efa66663c431-refs/heads/11.4.183@{#1}
Cr-Branched-From: 5483d8e816e0bbce865cbbc3fa0ab357e6330bab-refs/heads/main@{#87241}

[modify] https://crrev.com/0615e6e22c0007382b85bf467c6d8ce01ee636b2/src/interpreter/interpreter-assembler.cc
[modify] https://crrev.com/0615e6e22c0007382b85bf467c6d8ce01ee636b2/src/interpreter/interpreter-assembler.h
[add] https://crrev.com/0615e6e22c0007382b85bf467c6d8ce01ee636b2/test/mjsunit/regress/regress-1432470.js
[modify] https://crrev.com/0615e6e22c0007382b85bf467c6d8ce01ee636b2/src/baseline/baseline-compiler.cc
[add] https://crrev.com/0615e6e22c0007382b85bf467c6d8ce01ee636b2/test/mjsunit/regress/regress-1442603.js
[modify] https://crrev.com/0615e6e22c0007382b85bf467c6d8ce01ee636b2/src/baseline/baseline-compiler.h
[modify] https://crrev.com/0615e6e22c0007382b85bf467c6d8ce01ee636b2/test/mjsunit/mjsunit.status


### gi...@appspot.gserviceaccount.com (2023-05-17)

https://crbug.com/chromium/1442603 has been un-merged from this issue.


### gi...@appspot.gserviceaccount.com (2023-05-17)

[Empty comment from Monorail migration]

### va...@chromium.org (2023-05-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-18)

Congratulations, Ganjiang Zhou! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-05-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-30)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-05-31)

[Empty comment from Monorail migration]

### rz...@google.com (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-05-31)

1. 2 CLs https://chromium-review.googlesource.com/q/topic:%225359_1432470%22
2. Low, conflicts with a few functions that aren't present in 108
3. 114
4. Yes

### gm...@google.com (2023-05-31)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-06-06)

@amyressler

It would be nice if you guys could assign a CVE.

### gm...@google.com (2023-06-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/3bd51acc7fc5328f4728ed2f30f2186f4efb2d5d

commit 3bd51acc7fc5328f4728ed2f30f2186f4efb2d5d
Author: Toon Verwaest <verwaest@chromium.org>
Date: Mon May 08 16:14:01 2023

[M108-LTS][osr] Check whether the target is deoptimized

M108 merge issues:
  runtime/runtime-compiler.cc:
    Conflicting arguments for theCompileOptimizedOS call

(cherry picked from commit b9a0e4e607e1fab25e7d47b55f9a3c4c263fbfc1)

Bug: chromium:1432470
Change-Id: I944ae6b6ae73d2755c90fdc2d3d32885f5de65d0
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4513858
Auto-Submit: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#87510}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4577217
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/branch-heads/10.8@{#70}
Cr-Branched-From: f1bc03fd6b4c201abd9f0fd9d51fb989150f97b9-refs/heads/10.8.168@{#1}
Cr-Branched-From: 237de893e1c0a0628a57d0f5797483d3add7f005-refs/heads/main@{#83672}

[modify] https://crrev.com/3bd51acc7fc5328f4728ed2f30f2186f4efb2d5d/src/runtime/runtime-compiler.cc


### gi...@appspot.gserviceaccount.com (2023-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d43ce18e5b9ebad2ed990714092ea743bb840dfa

commit d43ce18e5b9ebad2ed990714092ea743bb840dfa
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Jun 23 18:12:00 2023

Roll v8 10.8 from 014b8ef0631a to 700f8cb7682b (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/014b8ef0631a..700f8cb7682b

2023-06-23 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 10.8.168.36
2023-06-23 verwaest@chromium.org [M108-LTS][osr] Check whether the target is deoptimized

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-10-8-chromium-m108
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 10.8: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m108: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1432470
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: Ibd2800cfb6b3bd874b81f16be8fb3842e15fbf02
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4638854
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1480}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/d43ce18e5b9ebad2ed990714092ea743bb840dfa/DEPS


### gi...@appspot.gserviceaccount.com (2023-06-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/19e4f185744aeaddfcbf871b45e7b6300277b4c6

commit 19e4f185744aeaddfcbf871b45e7b6300277b4c6
Author: Jakob Linke <jgruber@chromium.org>
Date: Thu May 11 07:20:57 2023

[M108-LTS] [osr] Avoid handling interrupts in the middle of OSR

M108 merge issues:
  src/baseline/baseline-compiler.h:
    JumpIfRoot and JumpIfNotRoot aren't present in 108

  src/baseline/baseline-compiler.cc:
    UpdateInterruptBudgetAndJumpToLabel:
    - There's no DCHECK_LT weight check in 108.
    VisitJumpLoop:
    - The UpdateInterruptBudgetAndJumpToLabel call at the end of the block
    doesn't exist in 108

  src/interpreter/interpreter-assembler.h/cc:
    DecreaseInterruptBudget isn't present in 108

  test/mjsunit/mjsunit.status:
    wasm/simd-lane-memory64 and regress/regress-1320641 aren't skipped in
    108

.. since interrupts may trigger code deoptimization, which in turn
invalidates assumptions we've already checked at the beginning of
OnStackReplacement.

This CL disables the stack check as part of the bytecode budget
interrupt, i.e. we don't call stack_guard()->HandleInterrupts()
in Runtime_BytecodeBudgetInterrupt_{Ignition,Sparkplug}.

(cherry picked from commit c2eda65a85d1c85f9037fa89b63ae725b18dbfbe)

Fixed: chromium:1432470,chromium:1442603
Change-Id: I63dc51812741161cfb2f1cdb67c46e269d37f0f6
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4518604
Commit-Queue: Jakob Linke <jgruber@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#87590}
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4577218
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/10.8@{#72}
Cr-Branched-From: f1bc03fd6b4c201abd9f0fd9d51fb989150f97b9-refs/heads/10.8.168@{#1}
Cr-Branched-From: 237de893e1c0a0628a57d0f5797483d3add7f005-refs/heads/main@{#83672}

[modify] https://crrev.com/19e4f185744aeaddfcbf871b45e7b6300277b4c6/src/interpreter/interpreter-assembler.cc
[add] https://crrev.com/19e4f185744aeaddfcbf871b45e7b6300277b4c6/test/mjsunit/regress/regress-1432470.js
[modify] https://crrev.com/19e4f185744aeaddfcbf871b45e7b6300277b4c6/src/baseline/baseline-compiler.cc
[add] https://crrev.com/19e4f185744aeaddfcbf871b45e7b6300277b4c6/test/mjsunit/regress/regress-1442603.js
[modify] https://crrev.com/19e4f185744aeaddfcbf871b45e7b6300277b4c6/src/baseline/baseline-compiler.h
[modify] https://crrev.com/19e4f185744aeaddfcbf871b45e7b6300277b4c6/test/mjsunit/mjsunit.status


### gi...@appspot.gserviceaccount.com (2023-06-29)

https://crbug.com/chromium/1442603 has been un-merged from this issue.


### gi...@appspot.gserviceaccount.com (2023-06-29)

[Empty comment from Monorail migration]

### rz...@google.com (2023-06-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-06-29)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-06-30)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-12-21)

Hello -- we consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), even when included in comments, so I have undeleted such comments and relevant information. Thank you.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1432470?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1459371]
[Monorail mergedwith: crbug.com/chromium/1442603]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064002)*

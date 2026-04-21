# GPU process crash via WebGPU shader - Stack use-after-return at HLMatrixLowerPass.cpp:63

| Field | Value |
|-------|-------|
| **Issue ID** | [346618785](https://issues.chromium.org/issues/346618785) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Tint |
| **Platforms** | Windows |
| **Reporter** | wg...@gmail.com |
| **Assignee** | dn...@google.com |
| **Created** | 2024-06-12 |
| **Bounty** | $10,000.00 |

## Description

##### VULNERABILITY DETAILS

Chromium translates wgsl shaders via tint to an OS-specific shader format. On Windows, the OS-specific file format is hlsl, processed in dxcompiler.dll. When compiling chrome-generated hlsl files, this triggers an stack use-after-return inside the hlsl compiler.

##### VERSION

Chrome Version: Pre-compiled ASAN Chromium 127.0.6535.0 (Developer Build) (64-bit)   

Operating System: Win10 Build 19045.4291

##### REPRODUCTION CASE

Attached is a .html file containing a WebGPU shader. Opening the html file (on windows with the D3D12 backend) crashes the GPU process.

Reproducing the issue stand-alone on Linux also possible:

1. Compile the standalone.wgsl with tint (commit 236295367f2e20a213d0b80f06d8b32175e54731) to hlsl via `./tint standalone.wgsl -o standalone.hlsl`. I also attached standalone.hlsl, but you should get the very same file when compiling standalone.wgsl yourself
2. Compile the hlsl with dxc (commit 1c7cb4ffb89107ce2aea583b2387f88225a4a634): `./dxc-3.7 standalone.hlsl -T cs_6_2 -opt-disable structurize-loop-exits-for-unroll -HV 2018`. Instead of a use-after-return, this triggers a heap UAF.

##### Attached:

- html that triggers an ASAN violation in chromium
- wgsl for producing the hlsl shader
- the hlsl shader
- asan log file

```
[7500:6748:0612/034217.772:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[7500:7272:0612/034223.767:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[5080:6500:0612/034224.690:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[7500:6748:0612/034233.783:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[5080:2152:0612/034244.714:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[7500:6748:0612/034253.798:WARNING:dns_config_service_win.cc(605)] Failed to read DnsConfig.
[5080:268:0612/034509.922:ERROR:sandbox_win.cc(836)] Sandbox cannot access executable. Check filesystem permissions are valid. See https://bit.ly/31yqMJR.: Access is denied. (0x5)
[5080:8872:0612/034953.671:INFO:CONSOLE(20)] "[object GPUDevice]", source: file://vboxsvr/shared/indexDropAllReferences.html (20)
=================================================================
==10144==ERROR: AddressSanitizer: stack-use-after-return on address 0x1274848db930 at pc 0x7ffd7248b011 bp 0x0026e77f9e50 sp 0x0026e77f9e98
READ of size 4 at 0x1274848db930 thread T0
==10144==WARNING: Failed to use and restart external symbolizer!
==10144==*** WARNING: Failed to initialize DbgHelp!              ***
==10144==*** Most likely this means that the app is already      *** 
==10144==*** using DbgHelp, possibly with incompatible flags.    *** 
==10144==*** Due to technical reasons, symbolization might crash *** 
==10144==*** or produce wrong results.                           ***
    #0 0x7ffd7248b010 in `anonymous namespace'::TempOverloadPool::~TempOverloadPool C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\HLSL\HLMatrixLowerPass.cpp:63
    #1 0x7ffd7248acf7 in `anonymous namespace'::HLMatrixLowerPass::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\HLSL\HLMatrixLowerPass.cpp:258
    #2 0x7ffd70aeffff  (<unknown module>)

Address 0x1274848db930 is located in stack of thread T0 at offset 2352 in frame
    #0 0x7ffd7248622f in `anonymous namespace'::HLMatrixLowerPass::runOnModule C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\HLSL\HLMatrixLowerPass.cpp:213

  This frame has 33 object(s):
    [32, 40) 'agg.tmp.i.i.i23.i.i'
    [64, 120) 'Builder.i.i.i' (line 778)
    [160, 184) 'ref.tmp.i265.i.i.i.i'
    [224, 232) 'agg.tmp.i.i.i.i.i'
    [256, 280) 'ref.tmp.i.i233.i.i.i.i'
    [320, 328) 'agg.tmp.i.i212.i.i.i.i'
    [352, 376) 'ref.tmp.i.i.i.i.i'
    [416, 424) 'agg.tmp.i.i183.i.i.i.i'
    [448, 472) 'ref.tmp.i.i.i.i.i.i'
    [512, 520) 'agg.tmp.i.i.i.i.i.i'
    [544, 600) 'PreCallBuilder.i.i.i.i' (line 815)
    [640, 696) 'agg.tmp.i.i.i122.i' (line 815)
    [736, 760) 'ref.tmp.i.i.i.i' (line 833)
    [800, 816) 'RetMatTy.i.i.i.i' (line 851)
    [832, 888) 'AllocaBuilder.i.i.i.i' (line 863)
    [928, 952) 'ref.tmp63.i.i.i.i' (line 865)
    [992, 1048) 'PostCallBuilder.i.i.i.i' (line 867)
    [1088, 1112) 'ref.tmp74.i.i.i.i' (line 868)
    [1152, 1176) 'ref.tmp82.i.i.i.i' (line 876)
    [1216, 1224) 'tmp.i.i' (line 308)
    [1248, 1272) 'ref.tmp.i.i.i'
    [1312, 1320) 'agg.tmp.i.i.i.i'
    [1344, 1400) 'Builder.i.i' (line 734)
    [1440, 1464) 'ref.tmp.i.i' (line 735)
    [1504, 1520) 'ref.tmp5.i.i' (line 735)
    [1536, 1952) 'DIB.i.i' (line 742)
    [2016, 2040) 'MatAllocas.i' (line 268)
    [2080, 2104) 'MatInsts.i' (line 269)
    [2144, 2168) 'ref.tmp.i' (line 663)
    [2208, 2224) 'ref.tmp14.i' (line 663)
    [2240, 2288) 'matToVecStubs' (line 214)
    [2320, 2368) 'vecToMatStubs' (line 215) <== Memory access at offset 2352 is inside this variable
    [2400, 2424) 'Globals' (line 228)
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp, SEH and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-use-after-return C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\lib\HLSL\HLMatrixLowerPass.cpp:63 in `anonymous namespace'::TempOverloadPool::~TempOverloadPool
Shadow bytes around the buggy address:
  0x1274848db680: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x1274848db700: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x1274848db780: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x1274848db800: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x1274848db880: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
=>0x1274848db900: f5 f5 f5 f5 f5 f5[f5]f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x1274848db980: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x1274848dba00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x1274848dba80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x1274848dbb00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x1274848dbb80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==10144==ADDITIONAL INFO

==10144==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffd37c492b0 in gpu::SchedulerDfs::TryScheduleSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:473


==10144==END OF ADDITIONAL INFO
==10144==ABORTING
[5080:8872:0612/034958.742:ERROR:gpu_process_host.cc(1007)] GPU process exited unexpectedly: exit_code=1
[5080:8872:0612/034958.742:WARNING:gpu_process_host.cc(1443)] The GPU process has crashed 1 time(s)
[5080:8872:0612/034958.777:INFO:CONSOLE(0)] "A valid external Instance reference no longer exists.", source: file://vboxsvr/shared/indexDropAllReferences.html (0)

```

## Attachments

- [asanDropAll](attachments/asanDropAll) (application/octet-stream, 7.3 KB)
- [indexDropAllReferences.html](attachments/indexDropAllReferences.html) (text/html, 2.2 KB)
- [standalone.hlsl](attachments/standalone.hlsl) (application/octet-stream, 179 B)
- [standalone.wgsl](attachments/standalone.wgsl) (application/octet-stream, 205 B)
- [deleted](attachments/deleted) (application/octet-stream, 0 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-06-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6366823992721408.

### pg...@google.com (2024-06-13)

I can repro this on Linux with dxc on dawn branch 6367 - setting foundin to 124, sev to S1 and assigning to amaiorano@ who has worked on similar bugs! Can you take a look and reassign if need be?

### pe...@google.com (2024-06-13)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-06-13)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2024-06-14)

It looks like an assertion is hit in debug builds. Taking a closer look.

```
Temporary function still used during pool destruction.dxc: /usr/local/google/home/chouinard/code/DirectXShaderCompiler/lib/HLSL/HLMatrixLowerPass.cpp:101: void (anonymous namespace)::TempOverloadPool::clear(): Assertion `false && "Temporary function still used during pool destruction."' failed.
[1]    2629319 IOT instruction  ./build-asan/bin/dxc -T cs_6_2 -HV 2018 346618785/standalone.hlsl

```

### ch...@google.com (2024-06-17)

In the following code section: <https://github.com/microsoft/DirectXShaderCompiler/blob/8c3f40c0ae12cbc128832ff546eccc62c9945418/lib/HLSL/HLMatrixLowerPass.cpp#L237-L244>

the first loop that lowers globals is executed, populating `m_vecToMatStubs`, but then the TempOverloadPool destructor is called without ever reaching the second loop to iterate over functions and lower individual instructions. I'm not sure why yet.

### ch...@google.com (2024-06-18)

The destructor is being called earlier due to an exception unwinding the stack (thanks amaiorano@ for the help debugging!). Further details from the investigation so far are summarized in this [doc](https://docs.google.com/document/d/16cpLQoEsYkLnNJyLyIgWK3emsipjgpV9hiRmhcvtMMg/edit?usp=sharing).

### dn...@google.com (2024-06-19)

I have an idea.

Don’t call .clear() from within the TempOverloadPool destructor. Instead call it explicitly before the end of runOnModule. But instead, the destructor can either assert that the Funcs map is empty, or do nothing because the only way the map is non-empty at that point is if we were in the middle of throwing an exception.

If the destructor does nothing, then this test case produces an ordinary compile error from DXC. This is the output from a release build and a debug build (without ASAN):

```
$ dxc -T cs_6_0 -opt-disable structurize-loop-exits-for-unroll -HV 2018 a.hlsl
error: cast<X>() argument of incompatible type!
$ echo $?
5

```

Looks like the error message is coming from an exception thrown here:

```
./lib/Support/ErrorHandling.cpp:144:  throw hlsl::Exception(DXC_E_LLVM_CAST_ERROR, std::string(func) + "<X>() argument of incompatible type!\n");

```

So I think what’s happening is the matrix lowering code is doing a `cast<ty>(...)` where the argument is the wrong type. LLVM ordinarily asserts out for this (it’s a checked cast), but looks like Microsoft has customized it to throw an exception. By neutering the destructor of `TempOverloadPool` we allow that exception to escape and get turned into a regular error. That seems to avoid the security issue. It turns it into an ordinary compile error.

### wg...@gmail.com (2024-06-20)

FWIW: you might be happy to hear that the shader fuzzer hasn't been uncovering new issues in dxc for the last couple of days.

### dn...@google.com (2024-06-20)

I've posted a fix for this issue to <https://github.com/microsoft/DirectXShaderCompiler/pull/6710>

There is still a compiler bug (not handling certain matrix lowering cases) but it shouldn't result in a stack use-after-free.

### dn...@google.com (2024-06-26)

upstream patch was just approved

### dn...@google.com (2024-06-27)

The upstream fix landed, then:

- rolled into Dawn with <https://dawn-review.googlesource.com/c/dawn/+/195955>
- rolled into Chromium with <https://chromium-review.googlesource.com/c/chromium/src/+/5660914>

That is not yet in a Chromium build

### dn...@google.com (2024-06-27)

The fix is in Chrome 128.0.6561.0
Via branch origin/chromium/6561

### dn...@google.com (2024-06-27)

In 128.0.6561.0, we get past the original problem and now the ASAN build detects a heap use after free.
It appears to be in the exception unwinding path.

### dn...@google.com (2024-06-27)

redacted

### dn...@google.com (2024-07-10)

Debugging this is a bit tricky on Linux, with Clang 19+

- to test exceptions (with cmake) you have to use Cmake flag LLVM\_ENABLE\_EH, LLVM\_ENABLE\_RTTI, *and* also add CMAKE\_CXX\_FLAGS `-fexceptions` and `-frtti` because the cmake files in the project are to old for Clang 19?

The cast error ends up throwing hlsl::Exception

That is caught in `tools/clang/lib/CodeGen/BackendUtil.cpp`, and we need to do something like:

```
@@ -782,7 +789,10 @@ void clang::EmitBackendOutput(DiagnosticsEngine &Diags,
   } catch (const ::hlsl::Exception &hlslException) {
     Diags.Report(Diags.getCustomDiagID(DiagnosticsEngine::Error, "%0\n"))
         << StringRef(hlslException.what());
+    fprintf(stdout,"%s\n", hlslException.what()); fflush(stdout);
+    std::abort();
   } // HLSL Change Ends

```

Because we abort the process, the diagnostic is not emitted on its own.

I've asked Chris Bieneman (DXC TL at Microsoft) and he's ok adding a project config to modify this behaviour.

### dn...@google.com (2024-07-10)

I posted <https://github.com/microsoft/DirectXShaderCompiler/pull/6764> upstream.

Would also need a change to the GN build config

### dn...@google.com (2024-07-11)

danakj@ is advising.

I'm reworking the patch, so instead of std::abort, it calls the builtin trap (LLVM\_BUILTIN\_TRAP).
Then update the list of "boring" functions in the crash-processing server so we zero in on the interesting part of the call stack.

It's not where we catch the exception, not where we throw the exception, because that is several layers into the checked-cast machinery.

Here's part of the relevant stack:

```
#0  llvm::llvm_cast_assert_internal (func=0x7fffe4ec8360 <__FUNCTION__._ZN4llvm4castINS_8ConstantEKNS_5ValueEEENS_10cast_rettyIT_PT0_E8ret_typeES7_> "cast")
    at /dxc/lib/Support/ErrorHandling.cpp:144
#1  0x00007fffeafe4d0f in llvm::cast<llvm::CompositeType, llvm::Type> (Val=0x51e0000006a0) at /dxc/include/llvm/Support/Casting.h:239
#2  0x00007fffeb01fec9 in ConstantFoldGetElementPtrImpl<llvm::Value*> (PointeeTy=0x521000017360, C=0x50c000001b58, inBounds=false, Idxs=...)
    at /dxc/lib/IR/ConstantFold.cpp:2172
#3  0x00007fffeb0206ff in llvm::ConstantFoldGetElementPtr (Ty=0x521000017360, C=0x50c000001b58, inBounds=false, Idxs=...)
    at /dxc/lib/IR/ConstantFold.cpp:2263
#4  0x00007fffeafa2ee8 in llvm::ConstantExpr::getGetElementPtr (Ty=0x521000017360, C=0x50c000001b58, Idxs=..., InBounds=false, OnlyIfReducedTy=0x0)
    at /dxc/lib/IR/Constants.cpp:2039
#5  0x00007fffeb572319 in llvm::ConstantFolder::CreateGetElementPtr (this=0x7fffdb294cfc, Ty=0x0, C=0x50c000001b58, IdxList=...)
    at /dxc/include/llvm/IR/ConstantFolder.h:133
#6  0x00007fffeb5720b0 in llvm::IRBuilder<true, llvm::ConstantFolder, llvm::IRBuilderDefaultInserter<true> >::CreateGEP (this=0x7fffdb294cd0, Ty=0x0, Ptr=0x50c000001b58, IdxList=...,
    Name=...) at /dxc/include/llvm/IR/IRBuilder.h:1075
#7  0x00007fffeb55f57f in llvm::IRBuilder<true, llvm::ConstantFolder, llvm::IRBuilderDefaultInserter<true> >::CreateGEP (this=0x7fffdb294cd0, Ptr=0x50c000001b58, IdxList=..., Name=...)
    at /dxc/include/llvm/IR/IRBuilder.h:1063
#8  0x00007fffec125ead in (anonymous namespace)::HLMatrixLowerPass::replaceAllVariableUses (this=0x50b000000930, GEPIdxStack=..., StackTopPtr=0x50e000001938, LoweredPtr=0x50c000001b58)
    at /dxc/lib/HLSL/HLMatrixLowerPass.cpp:648

```

The bug is actually in frame 8 and above.

### dn...@google.com (2024-07-11)

I've updated <https://github.com/microsoft/DirectXShaderCompiler/pull/6764> and marked it ready for review.

It has one approval, needs a second.

### dn...@google.com (2024-07-12)

patch landed upstream, and <https://dawn-review.googlesource.com/c/dawn/+/198274> rolls it into and turns it on in Dawn.

### ap...@google.com (2024-07-12)

Project: dawn
Branch: main

commit 04d3cda89534f1aee918f13f06ac8716e7ee8ba3
Author: David Neto <dneto@google.com>
Date:   Fri Jul 12 19:58:54 2024

    Enable DXC_CODEGEN_EXCEPTIONS_TRAP
    
    When the DXC code generator traps, there is no valid recovery.
    So it should generate a trap, which will generate a crash report,
    instead of trying to continue processing.
    
    Roll DirectX Shader Compiler from ffee5dcbe956 to b18fe87633ee (2 revisions)
    
    https://chromium.googlesource.com/external/github.com/microsoft/DirectXShaderCompiler.git/+log/ffee5dcbe956..b18fe87633ee
    
    2024-07-12 dneto@google.com Add CMake option DXC_CODEGEN_EXCEPTIONS_TRAP (#6764)
    2024-07-11 grroth@microsoft.com Enable Living Release Notes (#6772)
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/directx-shader-compiler-dawn
    Please CC kainino@google.com,webgpu-developers@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in DirectX Shader Compiler: https://github.com/microsoft/DirectXShaderCompiler/issues/new/choose
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Bug: 346618785
    Change-Id: Iad156351282d315def1356d8e1b10b8d50abc7e9
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/198274
    Commit-Queue: David Neto <dneto@google.com>
    Auto-Submit: David Neto <dneto@google.com>
    Reviewed-by: Natalie Chouinard <chouinard@google.com>

M       DEPS
M       third_party/dxc
M       third_party/gn/dxc/BUILD.gn

https://dawn-review.googlesource.com/198274


### ap...@google.com (2024-07-13)

Project: chromium/src
Branch: main

commit 3e9b0f12346fd724cdffc2e406bb04254168ce31
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Sat Jul 13 08:44:54 2024

    Roll Dawn from f6e7213e9fb2 to 5ff88c304de7 (13 revisions)
    
    https://dawn.googlesource.com/dawn.git/+log/f6e7213e9fb2..5ff88c304de7
    
    2024-07-13 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll ANGLE from d89a205d355e to a5161f01b4b4 (4 revisions)
    2024-07-13 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll DirectX Shader Compiler from b18fe87633ee to a54abe841e8f (1 revision)
    2024-07-13 jrprice@google.com [msl] Fix logical boolean operators
    2024-07-13 kainino@chromium.org Fix expectations broken by roller
    2024-07-13 dawn-automated-expectations@chops-service-accounts.iam.gserviceaccount.com Reland "Roll third_party/webgpu-cts/ 45e2ca37a..79c4db9d1 (2 commits)"
    2024-07-13 kainino@chromium.org Revert "Roll third_party/webgpu-cts/ 45e2ca37a..79c4db9d1 (2 commits)"
    2024-07-12 cwallez@chromium.org dawn::wire::client Make Device::Destroy cancel mappings
    2024-07-12 dawn-automated-expectations@chops-service-accounts.iam.gserviceaccount.com Roll third_party/webgpu-cts/ 45e2ca37a..79c4db9d1 (2 commits)
    2024-07-12 jrprice@google.com [msl] Move fmod to new BinaryPolyfill transform
    2024-07-12 chouinard@google.com [Tint] Allow trailing commas in var decl
    2024-07-12 chouinard@google.com [Tint] Remove some unnecessary templating
    2024-07-12 chouinard@google.com [Tint] Cleanup Builtin Value classes
    2024-07-12 dneto@google.com Enable DXC_CODEGEN_EXCEPTIONS_TRAP
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/dawn-chromium-autoroll
    Please CC cwallez@google.com,kainino@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64
    Bug: chromium:344963953,chromium:346618785,chromium:352768986,chromium:352816949,chromium:42251016,chromium:42251275,chromium:42251291
    Tbr: kainino@google.com
    Include-Ci-Only-Tests: true
    Change-Id: I64c995e89033188e565560281fa9bc4cd9c43b14
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5705022
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1327145}

M       DEPS
M       third_party/dawn

https://chromium-review.googlesource.com/5705022


### dn...@google.com (2024-07-15)

Change first appears in Chromium origin/chromium/6594

### dn...@google.com (2024-07-15)

Verified fixed in an asan build of 128.0.6597.0: When opening the reproducer .html file, the tab blanks, but there are no additional messages on the cmd.exe window where I launched chrome.exe

So the fixes are:

- DXC to Dawn:
  - <https://dawn-review.googlesource.com/c/dawn/+/195955>
  - <https://dawn-review.googlesource.com/198274>
- Dawn to Chromium:
  - <https://chromium-review.googlesource.com/5705022>

### pe...@google.com (2024-07-16)

Requesting merge to stable (M126) because latest trunk commit (1327145) appears to be after stable branch point (1300313).
Requesting merge to beta (M127) because latest trunk commit (1327145) appears to be after beta branch point (1313161).
Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### dn...@google.com (2024-07-16)

> Which CLs should be backmerged? (Please include Gerrit links.)

DXC to Dawn:

- <https://dawn-review.googlesource.com/c/dawn/+/195955>
- <https://dawn-review.googlesource.com/198274>

> Has this fix been verified on Canary to not pose any stability regressions?

Yes. I tested shader execution CTS tests on 128.0.6597.0

> Does this fix pose any potential non-verifiable stability risks?

No

> Does this fix pose any known compatibility risks?

No

> Does it require manual verification by the test team? If so, please describe required testing.

Yes. Open IndexDropAllReferences.html attached to the original comment. The tab should flash, but there should be no additional messages on the command line.

### ap...@google.com (2024-07-16)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6478

commit 9463ce9cd8d9b02b98edb746431c0bbcf9654ae4
Author: David Neto <dneto@google.com>
Date:   Tue Jul 16 16:34:52 2024

    Add CMake option DXC_CODEGEN_EXCEPTIONS_TRAP (#6764)
    
    When enabled, any hlsl::Exception thrown during code generation and
    optimization will cause the process to trap.
    
    Bug: 346618785
    Change-Id: I9ac966d339ec3090e3455d51a9d7516cc5a3f153
    
    
    HLMatrixLower: allow exceptions to propagate out (#6710)
    
    If an exception is thrown, don't block it in the TempOverloadPool
    destructor. Allow it to propagate out as a user-visible error.
    
    Explicitly clear the TempOverloadPool before returning from the
    HLMatrixLowerPass::runOnModule. In the normal case, when no exception is
    thrown, that will still verify that all the overloads actually have been
    lowered, and will assert out if they aren't.
    
    Bug: 346618785
    Change-Id: Id421ca324e4d799477a41abb14b966e8f39be482
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5715228
    Reviewed-by: Natalie Chouinard <chouinard@google.com>

M       CMakeLists.txt
M       include/dxc/config.h.cmake
M       lib/HLSL/HLMatrixLowerPass.cpp
M       tools/clang/lib/CodeGen/BackendUtil.cpp
A       tools/clang/test/DXC/Passes/HLMatrixLower/dont_crash_on_invalid_cast.ll

https://chromium-review.googlesource.com/5715228


### ap...@google.com (2024-07-17)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6533

commit ef4b99f2913f42741555e67bbac622ab9fce0c4b
Author: David Neto <dneto@google.com>
Date:   Wed Jun 26 11:57:18 2024

    HLMatrixLower: allow exceptions to propagate out (#6710)
    
    If an exception is thrown, don't block it in the TempOverloadPool
    destructor. Allow it to propagate out as a user-visible error.
    
    Explicitly clear the TempOverloadPool before returning from the
    HLMatrixLowerPass::runOnModule. In the normal case, when no exception is
    thrown, that will still verify that all the overloads actually have been
    lowered, and will assert out if they aren't.
    
    Bug: chromium:346618785
    Change-Id: I7eb724f4b49a1cc85a1e10c7b2f96924f8a04d36
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5715230
    Reviewed-by: Natalie Chouinard <chouinard@google.com>
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>

M       lib/HLSL/HLMatrixLowerPass.cpp
A       tools/clang/test/DXC/Passes/HLMatrixLower/dont_crash_on_invalid_cast.ll

https://chromium-review.googlesource.com/5715230


### ap...@google.com (2024-07-17)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6533

commit 13e684ad06c34db809a195302ac460d18a3771d2
Author: David Neto <dneto@google.com>
Date:   Fri Jul 12 09:41:08 2024

    Add CMake option DXC_CODEGEN_EXCEPTIONS_TRAP (#6764)
    
    When enabled, any hlsl::Exception thrown during code generation and
    optimization will cause the process to trap.
    
    Bug: chromium:346618785
    Change-Id: I8de8268266303f917ab20fbd56cf4d1ac4c03695
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5715231
    Reviewed-by: Natalie Chouinard <chouinard@google.com>
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>

M       CMakeLists.txt
M       include/dxc/config.h.cmake
M       tools/clang/lib/CodeGen/BackendUtil.cpp

https://chromium-review.googlesource.com/5715231


### ap...@google.com (2024-07-17)

Project: dawn
Branch: chromium/6478

commit 5fd60bc03720ebd5a804cd64e8a52ba9e95593f5
Author: David Neto <dneto@google.com>
Date:   Wed Jul 17 14:09:26 2024

    DEPS: Update DXC to patched branch
    
    Also, add DXC_CODEGEN_EXCEPTIONS_TRAP=1 to DXC gn config.
    
    Bug: chromium:346618785, chromium:350696474
    Change-Id: I4c1ac753d824c4790e78d8f36231c8f2fe0e2722
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/198756
    Reviewed-by: Natalie Chouinard <chouinard@google.com>

M       DEPS
M       third_party/dxc
M       third_party/gn/dxc/BUILD.gn

https://dawn-review.googlesource.com/198756


### ap...@google.com (2024-07-17)

Project: dawn
Branch: chromium/6533

commit 6c0b2ce19bac367099a07f102b5e33a4e56620a1
Author: David Neto <dneto@google.com>
Date:   Wed Jul 17 16:31:46 2024

    DEPS: Update DXC to patched branch
    
    Also, add DXC_CODEGEN_EXCEPTIONS_TRAP=1 to DXC gn config.
    
    Bug: chromium:346618785, chromium:350696474
    Change-Id: Ie16795353cc89f551ad42e7761db8a2239c0b589
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/198914
    Auto-Submit: David Neto <dneto@google.com>
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>

M       DEPS
M       third_party/dxc
M       third_party/gn/dxc/BUILD.gn

https://dawn-review.googlesource.com/198914


### am...@chromium.org (2024-07-17)

This appears to have been merged without security merge review and approval.
This looks like it was merged after M127 Stable RC was cut yesterday, meaning that the merge to M126 will need to be reverted as soon as possible.
It should also be confirmed there were no issues in Canary since this fix was rolled into Chromium to ensure there are no risks to performance and stability since we did have the opportunity to assess that or the fix before it was merged.

### am...@chromium.org (2024-07-17)

now the M126 merges are being reverted -- re-adding the review tag so this can stay in the M126 merge review queue; we can approve this for merge after after the initial M126 Extended and M127 Stable releases and before the first M127 Stable respin to ensure the fix has been released in a Stable update first/in concert with M126 Extended

### ap...@google.com (2024-07-17)

Project: dawn
Branch: chromium/6478

commit 54dfb1d939205818aa037b5ec1df01407e2c0372
Author: David Neto <dneto@google.com>
Date:   Wed Jul 17 20:54:03 2024

    Revert "DEPS: Update DXC to patched branch"
    
    This reverts commit 5fd60bc03720ebd5a804cd64e8a52ba9e95593f5.
    
    Reason for revert:  Not approved for backmerge into M126. They would land too early.
    
    
    Original change's description:
    > DEPS: Update DXC to patched branch
    >
    > Also, add DXC_CODEGEN_EXCEPTIONS_TRAP=1 to DXC gn config.
    >
    > Bug: chromium:346618785, chromium:350696474
    > Change-Id: I4c1ac753d824c4790e78d8f36231c8f2fe0e2722
    > Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/198756
    > Reviewed-by: Natalie Chouinard <chouinard@google.com>
    
    TBR=dneto@google.com,amaiorano@google.com,chouinard@google.com
    
    Change-Id: I5e50dcfb6c599ee8e2af173467fd38a77625fbdc
    No-Presubmit: true
    No-Tree-Checks: true
    No-Try: true
    Bug: chromium:346618785, chromium:350696474
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/198935
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>
    Reviewed-by: David Neto <dneto@google.com>
    Commit-Queue: Antonio Maiorano <amaiorano@google.com>

M       DEPS
M       third_party/dxc
M       third_party/gn/dxc/BUILD.gn

https://dawn-review.googlesource.com/198935


### am...@chromium.org (2024-07-17)

I've reviewed canary data since the Dawn->Chromium roll was landed against the upstream fix; there appear to be no issues with performance or stability related to this fix, so the M127 merge seems fine to stay as is to be released in the first respin of M127 Stable on 30 July

### ap...@google.com (2024-07-17)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6478

commit 5a1e4c633633d1a9b2de092171584ebb4f490a44
Author: David Neto <dneto@google.com>
Date:   Wed Jul 17 20:46:42 2024

    Revert "Add CMake option DXC_CODEGEN_EXCEPTIONS_TRAP (#6764)"
    
    This reverts commit 9463ce9cd8d9b02b98edb746431c0bbcf9654ae4.
    
    Reason for revert: Not approved for backmerge into M126. They would land too early.
    
    Original change's description:
    > Add CMake option DXC_CODEGEN_EXCEPTIONS_TRAP (#6764)
    >
    > When enabled, any hlsl::Exception thrown during code generation and
    > optimization will cause the process to trap.
    >
    > Bug: 346618785
    > Change-Id: I9ac966d339ec3090e3455d51a9d7516cc5a3f153
    >
    >
    > HLMatrixLower: allow exceptions to propagate out (#6710)
    >
    > If an exception is thrown, don't block it in the TempOverloadPool
    > destructor. Allow it to propagate out as a user-visible error.
    >
    > Explicitly clear the TempOverloadPool before returning from the
    > HLMatrixLowerPass::runOnModule. In the normal case, when no exception is
    > thrown, that will still verify that all the overloads actually have been
    > lowered, and will assert out if they aren't.
    >
    > Bug: 346618785
    > Change-Id: Id421ca324e4d799477a41abb14b966e8f39be482
    > Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5715228
    > Reviewed-by: Natalie Chouinard <chouinard@google.com>
    
    Bug: 346618785
    Change-Id: I2aa4cbc51dabea51aadea8c4b4bb78c273eb23f8
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5719348
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

M       CMakeLists.txt
M       include/dxc/config.h.cmake
M       lib/HLSL/HLMatrixLowerPass.cpp
M       tools/clang/lib/CodeGen/BackendUtil.cpp
D       tools/clang/test/DXC/Passes/HLMatrixLower/dont_crash_on_invalid_cast.ll

https://chromium-review.googlesource.com/5719348


### am...@chromium.org (2024-07-19)

updating merge labels to reflect the M126 merge revert to ensure this is revisited for merge review for 126 later next week

### sp...@google.com (2024-07-24)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
report of memory corruption in the GPU process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-25)

Nice work on another one -- congratulations and thank you for reporting this issue to us!

### pe...@google.com (2024-07-29)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-07-29)

Project: dawn
Branch: chromium/6478

commit c9815acd5a88ae4853cd25f7cb8f2face7cace28
Author: David Neto <dneto@google.com>
Date:   Mon Jul 29 20:20:18 2024

    Reland "DEPS: Update DXC to patched branch"
    
    This is a reland of commit 5fd60bc03720ebd5a804cd64e8a52ba9e95593f5
    
    Original change's description:
    > DEPS: Update DXC to patched branch
    >
    > Also, add DXC_CODEGEN_EXCEPTIONS_TRAP=1 to DXC gn config.
    >
    > Bug: chromium:346618785, chromium:350696474
    > Change-Id: I4c1ac753d824c4790e78d8f36231c8f2fe0e2722
    > Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/198756
    > Reviewed-by: Natalie Chouinard <chouinard@google.com>
    
    Bug: chromium:346618785, chromium:350696474
    Change-Id: I9205dc9a028654388e09ffb853c64ff2010b793f
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/200494
    Reviewed-by: David Neto <dneto@google.com>
    Reviewed-by: Natalie Chouinard <chouinard@google.com>

M       DEPS
M       third_party/dxc
M       third_party/gn/dxc/BUILD.gn

https://dawn-review.googlesource.com/200494


### pe...@google.com (2024-10-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of memory corruption in the GPU process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/346618785)*

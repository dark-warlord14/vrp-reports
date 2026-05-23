# GPU process crash via WebGPU shader - dynamic_cast exception in DXC

| Field | Value |
|-------|-------|
| **Issue ID** | [333420620](https://issues.chromium.org/issues/333420620) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU, Internals>GPU>Dawn, Internals>GPU>Tint |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | wg...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2024-04-09 |
| **Bounty** | $10,000.00 |

## Description

VULNERABILITY DETAILS

Chromium translates wgsl shaders via tint to an OS-specific shader format. On Windows, the OS-specific file format is hlsl, processed in dxcompiler.dll. When compiling chrome-generated hlsl files, this might trigger a heap UAF insider the hlsl compiler.

VERSION Chrome Version: Pre-compiled ASAN Chromium 125.0.6406.0 (Developer Build) (64-bit) Operating System: Win10 Build 19045

REPRODUCTION CASE Attached is a .html file containing a WebGPU shader. Opening the html file (on windows with the D3D12 backend) crashes the GPU process. On a linux dxc build, ASAN terminates with a UAF in DeadBlockDeleter in DxilRemoveDeadBlocks.cpp, when running Chrome the crash is a stack-use-after-return.
The problematic wgsl shader (for standalone compilation) is:

```
fn f() {
    var l_1: array<i32, 10>;
    var l_2: array<i32, 10>;
    var l_7: i32;
    var l_12: i32;
    var l_20: i32;
    var l_29: f32;

    let x_68_ = l_2;
    l_2 = x_68_;
    let _e75 = true;
    l_12 = -2147483648;
    loop {
        if l_12 > 9 {
            break;
        }
        let x_120_ = (l_12 + 264912789);
        loop {
            if (!_e75) {
                return;
            }
            loop {
                continuing {
                    break if l_12 < 9;
                }
            }
            if (x_120_ == 0) {
                return;
            }
            if (l_20 > 1) {
                break;
            }
            continuing {
                l_2[l_20] = l_1[l_20];
                l_20 = (l_20 + 1);
            }
        }
        continuing {
            l_12 = x_120_;
        }
    }
}

@fragment
fn main() -> @location(0) vec4<f32> {
    loop {
        continuing {
            f();
            break if (i32() > i32());
        }
    }
    return vec4<f32>();
}

```
```
==4544==ERROR: AddressSanitizer: stack-use-after-return on address 0x11fce74378f8 at pc 0x7ffaf6d9058d bp 0x0011301fa3a0 sp 0x0011301fa3e8
READ of size 8 at 0x11fce74378f8 thread T0
==4544==WARNING: Failed to use and restart external symbolizer!
==4544==*** WARNING: Failed to initialize DbgHelp!              ***
==4544==*** Most likely this means that the app is already      *** 
==4544==*** using DbgHelp, possibly with incompatible flags.    *** 
==4544==*** Due to technical reasons, symbolization might crash *** 
==4544==*** or produce wrong results.                           ***
    #0 0x7ffaf6d9058c in `anonymous namespace'::EmitAssemblyHelper::~EmitAssemblyHelper C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:159
    #1 0x7ffaf6d9026f in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:797
    #2 0x7ffaf661ffff  (<unknown module>)

Address 0x11fce74378f8 is located in stack of thread T0 at offset 2296 in frame
    #0 0x7ffaf6d8b03f in clang::EmitBackendOutput C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:770

  This frame has 35 object(s):
    [32, 48) 'agg.tmp.i94'
    [64, 80) 'agg.tmp.i77'
    [96, 136) 'agg.tmp.i.i203.i' (line 84) 
    [176, 224) 'TargetTriple.i204.i' (line 648)
    [256, 280) 'ref.tmp.i205.i' (line 648)
    [320, 344) 'DL.i.i.i' (line 308)
    [384, 385) 'MapParser.i.i.i' (line 310)
    [400, 440) 'agg.tmp.i.i173.i' (line 109)
    [480, 584) 'PMBuilder.i.i' (line 332)
    [624, 648) 'agg.tmp.i.i64' (line 318)
    [688, 712) 'agg.tmp63.i.i' (line 318)
    [752, 776) 'agg.tmp67.i.i' (line 318)
    [816, 840) 'agg.tmp71.i.i' (line 318)
    [880, 904) 'agg.tmp77.i.i' (line 318)
    [944, 968) 'agg.tmp82.i.i' (line 318)
    [1008, 1056) 'TargetTriple.i.i' (line 443)
    [1088, 1112) 'ref.tmp.i174.i' (line 443)
    [1152, 1176) 'Error.i.i' (line 507)
    [1216, 1240) 'Triple.i.i' (line 508)
    [1280, 1304) 'FeaturesStr.i.i' (line 545)
    [1344, 1432) 'Options.i.i' (line 573)
    [1472, 1496) 'ref.tmp69.i.i' (line 576)
    [1536, 1540) 'ref.tmp85.i.i' (line 578)
    [1552, 1556) 'ref.tmp88.i.i' (line 578)
    [1568, 1584) 'agg.tmp294.i.i' (line 507)
    [1600, 1624) 'ref.tmp.i' (line 708)
    [1664, 1688) 'CrashInfo.i' (line 745)
    [1728, 1752) 'CrashInfo122.i' (line 755)
    [1792, 1816) 'CrashInfo135.i' (line 760)
    [1856, 1872) 'agg.tmp.i'
    [1888, 1904) 'agg.tmp2.i'
    [1920, 1936) 'agg.tmp.i.i'
    [1952, 2328) 'AsmHelper' (line 771) <== Memory access at offset 2296 is inside this variable
    [2400, 2408) 'hlslException'
    [2432, 2456) 'DLDesc' (line 788)
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp, SEH and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-use-after-return C:\b\s\w\ir\cache\builder\src\third_party\dawn\third_party\dxc\tools\clang\lib\CodeGen\BackendUtil.cpp:159 in `anonymous namespace'::EmitAssemblyHelper::~EmitAssemblyHelper
Shadow bytes around the buggy address:
  0x11fce7437600: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x11fce7437680: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x11fce7437700: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x11fce7437780: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x11fce7437800: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
=>0x11fce7437880: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5[f5]
  0x11fce7437900: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x11fce7437980: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x11fce7437a00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x11fce7437a80: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x11fce7437b00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
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

==4544==ADDITIONAL INFO

==4544==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffa9e65398e in gpu::SchedulerDfs::RunNextTask C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:681
    #1 0x7ffa9e64c8e5 in gpu::SchedulerDfs::TryScheduleSequence C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler_dfs.cc:480


==4544==END OF ADDITIONAL INFO
==4544==ABORTING
win32u!NtGdiDdDDIWaitForVerticalBlankEvent+0x14:
00007ffb`1e245cc4 c3              ret

```

## Attachments

- [indexDeadBlockDeleter.html](attachments/indexDeadBlockDeleter.html) (text/html, 3.6 KB)
- [333420620.hlsl](attachments/333420620.hlsl) (application/octet-stream, 1.1 KB)
- [standalone.wgsl](attachments/standalone.wgsl) (application/octet-stream, 2.5 KB)
- [standalone.hlsl](attachments/standalone.hlsl) (application/octet-stream, 2.5 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-04-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5072445380689920.

### an...@chromium.org (2024-04-09)

Sending another WebGPU shader issue your way, @am...@google.com. I've also kicked off a clusterfuzz run.

### am...@google.com (2024-04-09)

I've attached `333420620.hlsl` which is the HLSL generated from Tint against the WGSL in this bug.

> On a linux dxc build, ASAN terminates with a UAF in DeadBlockDeleter in DxilRemoveDeadBlocks.cpp, when running Chrome the crash is a stack-use-after-return.

I built dxc using GN with `is_asan = true` and was unable to reproduce any ASAN error when run against the HLSL produced by Tint from the attached WGSL. Can you provide the exact commit of Dawn, along with the `gn args` (contents of `args.gn`) that were used to build `dxc`, and the exact args and hlsl used (if it's different from the one I attached)?

> REPRODUCTION CASE Attached is a .html file containing a WebGPU shader. Opening the html file (on windows with the D3D12 backend) crashes the GPU process.

With a local ASAN build of Chrome, I did get a GPU crash when opening the HTML file, but it was not an ASAN UAF with the same call stack. Instead, I hit an exception with this call stack:

```
 	KernelBase.dll!00007ffd35becf19()	Unknown
 	dxcompiler.dll!_CxxThrowException(void * pExceptionObject=0x0000001ebc9fbb80, const _s__ThrowInfo * pThrowInfo) Line 82	C++
 	dxcompiler.dll!__RTDynamicCast(void * inptr, long VfDelta=-1130382336, void * srcVoid=0x000001c767c00000, void * targetVoid=0xedcbd2bde4c2c19b, int isReference=0) Line 291	C++
>	dxcompiler.dll!clang::BackendConsumer::DxilDiagHandler(const llvm::DiagnosticInfoDxil &) Line 560	C++
 	dxcompiler.dll!clang::BackendConsumer::DiagnosticHandlerImpl(const llvm::DiagnosticInfo &) Line 618	C++
 	dxcompiler.dll!llvm::LLVMContext::diagnose(const llvm::DiagnosticInfo &) Line 230	C++
 	[Inline Frame] dxcompiler.dll!hlsl::dxilutil::EmitWarningOrErrorOnContext(llvm::LLVMContext &) Line 369	C++
 	dxcompiler.dll!hlsl::dxilutil::EmitWarningOnContext(llvm::LLVMContext &) Line 377	C++
 	dxcompiler.dll!`anonymous namespace'::DxilFinalizeModule::runOnModule(llvm::Module &) Line 857	C++
 	[Inline Frame] dxcompiler.dll!`anonymous namespace'::MPPassManager::runOnModule(llvm::Module &) Line 1669	C++
 	dxcompiler.dll!llvm::legacy::PassManagerImpl::run(llvm::Module &) Line 1771	C++
 	[Inline Frame] dxcompiler.dll!`anonymous namespace'::EmitAssemblyHelper::EmitAssembly(clang::BackendAction) Line 756	C++
 	dxcompiler.dll!clang::EmitBackendOutput(clang::DiagnosticsEngine &) Line 779	C++
 	dxcompiler.dll!clang::BackendConsumer::HandleTranslationUnit(clang::ASTContext &) Line 195	C++
 	dxcompiler.dll!clang::ParseAST(clang::Sema &) Line 164	C++
 	dxcompiler.dll!clang::CodeGenAction::ExecuteAction() Line 807	C++
 	dxcompiler.dll!clang::FrontendAction::Execute() Line 468	C++
 	dxcompiler.dll!DxcCompiler::Compile(const DxcBuffer *) Line 982	C++
 	[Inline Frame] chrome.dll!dawn::native::d3d::`anonymous namespace'::CompileShaderDXC(const dawn::native::d3d::D3DBytecodeCompilationRequest &) Line 155	C++
 	chrome.dll!dawn::native::d3d::CompileShader(dawn::native::d3d::D3DCompilationRequest) Line 355	C++
<snip>

```

And the code that it fails on is this `dynamic_cast` which makes sense because we do not build with RTTI in Chrome:

```
bool
BackendConsumer::DxilDiagHandler(const llvm::DiagnosticInfoDxil &D) {
...
  // If no location information is available, add function name
  if (Loc.isInvalid()) {
    auto *DiagClient = dynamic_cast<TextDiagnosticPrinter*>(Diags.getClient()); // <------------- HERE
...

```

This is a problem that needs fixing in DXC, so I'll look at fixing this; but this does not seem like the same bug that's reported here.

### am...@google.com (2024-04-09)

For the `dynamic_cast` crash/exception, I put up [this fix just now](https://github.com/microsoft/DirectXShaderCompiler/pull/6515). [wgslfuzz@gmail.com](mailto:wgslfuzz@gmail.com) if you can reproduce locally, try again with this patch. Thank you.

### wg...@gmail.com (2024-04-10)

Well, as you already observed there is a problem with the standalone reproducer, sorry about that. My setup passed the wgsl shader through tint into libdxcompiler.so and for some reason that behaves slightly different than invoking dxc-3.7 via command line.
That being said, I attached are a variant of the wgsl shader + generated hlsl shader that should work with the command line versions of tint and dxc-3.7. I checked out the latest version (0781ded87bd78c11f208bc206a35ea3830b31ae1) of dxc, applied the patch from PR 6515 and compiled dxc as described here: <https://issues.chromium.org/issues/333508731#comment7>

Invoking dxc as `./dxc-3.7 standalone.hlsl -T ps_6_2` produces the ASAN violation.

### am...@google.com (2024-04-10)

I was able to reproduce an ASAN failure by building DXC using your instructions from <https://issues.chromium.org/issues/333508731#comment7> and running against the latest `standalone.hlsl`. I now understand why I was not able to reproduce this with my own Linux build, and the reason is that I build with `-DLLVM_ENABLE_LIBCXX=1` - that is, use libc++ if available. Chrome also builds and links against libc++, so I'm wondering whether there are two distinct bugs here: this one that reproduces with dxc using libstdc++, and the one you originally reported that happened with the Windows ASAN build of Chrome.

> VERSION Chrome Version: Pre-compiled ASAN Chromium 125.0.6406.0 (Developer Build) (64-bit) Operating System: Win10 Build 19045

Can you please tell me how you retrieved the ASAN Windows build of Chrome you used? I would like to be able to properly reproduce this crash as reported. In the meantime, I'll look into this potentially unrelated heap-use-after-free.

### wg...@gmail.com (2024-04-10)

There is a repository of pre-build ASAN version: <https://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=win32-release_x64/>
The directory listing takes a while, the exact version I used for this report is available via the following link: <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-1283679.zip?generation=1712540864604245&alt=media>

ASAN logs can either be collected with log files described here <https://chromium.googlesource.com/chromium/src/+/master/docs/asan.md#run-chrome-under-asan> or using windbg. For the latter approach, start chrome under windbg (you have to run `.childdbg 1` after windbg creates the target process, otherwise the GPU process will not run under windbg control). Resuming execution triggers either an "Access Violation" or a "Breakpoint" event, this seems normal and expected. These two events can be disabled via `Debug -> Event Filters`, set them to Unhandled/Ignored. Now resume execution, the browser should start normally. When opening the .html file, the GPU process terminates and prints the log to debug out visible in windbg.

### am...@google.com (2024-04-10)

Thank you, [wgslfuzz@gmail.com](mailto:wgslfuzz@gmail.com), I was able to reproduce the original Chrome asan failure initially reported using the downloaded build of Chrome as you specified, and opening up indexDeadBlockDeleter.html file you provided. In the debugger, I can see the full call stack of the asan failure, which unfortunately got cut off in the ASAN report, and the interesting bit is that we can clearly see the `dynamic_cast` I was referring to above:

```
 	chrome.exe!__sanitizer::internal__exit(int exitcode=1) Line 843	C++
 	chrome.exe!__sanitizer::Die() Line 59	C++
 	chrome.exe!__asan::ScopedInErrorReport::~ScopedInErrorReport() Line 193	C++
 	chrome.exe!__asan::ReportGenericError(unsigned __int64 pc, unsigned __int64 bp, unsigned __int64 sp, unsigned __int64 addr, bool is_write, unsigned __int64 access_size=8, unsigned int fatal, bool) Line 498	C++
 	chrome.exe!__asan_report_load8(unsigned __int64 addr) Line 131	C++
 	dxcompiler.dll!`anonymous namespace'::EmitAssemblyHelper::~EmitAssemblyHelper() Line 160	C++
 	dxcompiler.dll!clang::EmitBackendOutput(clang::DiagnosticsEngine &) Line 797	C++
 	dxcompiler.dll!00007ffbdc620000()	Unknown
 	000000000000000c()	Unknown
 	00000099a91fa128()	Unknown
 	00000099a91fa1c0()	Unknown
 	dxcompiler.dll!_CallSettingFrame() Line 50	Unknown
 	dxcompiler.dll!__FrameHandler3::FrameUnwindToState(unsigned __int64 * pRN=0x00007ffbdf8298bc, _xDISPATCHER_CONTEXT * pDC=0x00007ffbdf1bdc60, const _s_FuncInfo * pFuncInfo=0x00007ffbdfba7220, int targetState=-1363511820) Line 1231	C++
 	dxcompiler.dll!__FrameHandler3::FrameUnwindToEmptyState(unsigned __int64 * pRN, _xDISPATCHER_CONTEXT * pDC=0x00000099a91fa7b0, const _s_FuncInfo * pFuncInfo=0x00007ffbdf8298bc) Line 257	C++
 	dxcompiler.dll!__InternalCxxFrameHandler<__FrameHandler3>(EHExceptionRecord * pExcept=0x00000099a91fa940, unsigned __int64 * pRN=0x00000000ffffffff, _CONTEXT * pContext=0x00000099a91fad30, _xDISPATCHER_CONTEXT * pDC=0x00000099a91fa7b0, const _s_FuncInfo * pFuncInfo=0x00007ffbdf8298bc, int CatchDepth=0, unsigned __int64 * pMarkerRN=0x0000000000000000, unsigned char recursive='\0') Line 372	C++
 	dxcompiler.dll!__CxxFrameHandler3(EHExceptionRecord * pExcept=0x00000099a91fa940, unsigned __int64 RN, _CONTEXT * pContext=0x00000099a91fad30, _xDISPATCHER_CONTEXT * pDC=0x00000099a91fa7b0) Line 283	C++
 	ntdll.dll!00007ffd381b242f()	Unknown
 	ntdll.dll!00007ffd38140939()	Unknown
 	dxcompiler.dll!__FrameHandler3::UnwindNestedFrames(unsigned __int64 * pFrame, EHExceptionRecord * pExcept, _CONTEXT * pContext, unsigned __int64 * pEstablisher, void * Handler=0x00007ffbdc69aaa0, const _s_FuncInfo * pFuncInfo=0x00007ffbdf7c495c, int TargetUnwindState=51, int __formal=135, const _s_HandlerType * __formal=0x00000099a91fab98, _xDISPATCHER_CONTEXT * pDC=0x00000099a91fb280, unsigned char recursive='\0') Line 766	C++
 	dxcompiler.dll!CatchIt<__FrameHandler3>(EHExceptionRecord * pExcept=0x00000099a91fb8f0, unsigned __int64 * pRN=0x00000099a91facc0, _CONTEXT * pContext=0x00000099a91fb400, _xDISPATCHER_CONTEXT * pDC=0x00000099a91fb280, const _s_FuncInfo * pFuncInfo=0x00007ffbdf7c495c, const _s_HandlerType * pCatch=0x00000099a91fab98, const _s_CatchableType * pConv=0x00007ffbdf9f82c8, const _s_TryBlockMapEntry * pEntry=0x00000099a91fab40, int CatchDepth=0, unsigned __int64 * pMarkerRN=0x0000000000000000, unsigned char IsRethrow='\0', unsigned char recursive='\0') Line 1374	C++
 	dxcompiler.dll!FindHandler<__FrameHandler3>(EHExceptionRecord * pExcept=0x00000099a91fb8f0, unsigned __int64 * pRN=0x00000099a91facc0, _CONTEXT * pContext=0x00000099a91fb400, _xDISPATCHER_CONTEXT * pDC=0x00000099a91fb280, const _s_FuncInfo * pFuncInfo=0x00007ffbdf7c495c, unsigned char recursive='\0', int CatchDepth=0, unsigned __int64 * pMarkerRN=0x0000000000000000) Line 650	C++
 	dxcompiler.dll!__InternalCxxFrameHandler<__FrameHandler3>(EHExceptionRecord * pExcept=0x00000099a91fb8f0, unsigned __int64 * pRN=0x00000099a91facc0, _CONTEXT * pContext=0x00000099a91fb400, _xDISPATCHER_CONTEXT * pDC=0x00000099a91fb280, const _s_FuncInfo * pFuncInfo=0x00007ffbdf7c495c, int CatchDepth=0, unsigned __int64 * pMarkerRN=0x0000000000000000, unsigned char recursive='\0') Line 403	C++
 	dxcompiler.dll!__CxxFrameHandler3(EHExceptionRecord * pExcept=0x00000099a91fb8f0, unsigned __int64 RN, _CONTEXT * pContext=0x00000099a91fb400, _xDISPATCHER_CONTEXT * pDC=0x00000099a91fb280) Line 283	C++
 	ntdll.dll!00007ffd381b23af()	Unknown
 	ntdll.dll!00007ffd381614b4()	Unknown
 	ntdll.dll!00007ffd381b0ebe()	Unknown
 	KernelBase.dll!00007ffd35becf19()	Unknown
 	dxcompiler.dll!_CxxThrowException(void * pExceptionObject=0x00000099a91fbca0, const _s__ThrowInfo * pThrowInfo) Line 82	C++
-----> 	dxcompiler.dll!__RTDynamicCast(void * inptr, long VfDelta=-1457537760, void * srcVoid=0x000001c14c580000, void * targetVoid=0x000011e34c7166b0, int isReference=0) Line 291	C++
	dxcompiler.dll!clang::BackendConsumer::DxilDiagHandler(const llvm::DiagnosticInfoDxil &) Line 560	C++
 	dxcompiler.dll!clang::BackendConsumer::DiagnosticHandlerImpl(const llvm::DiagnosticInfo &) Line 618	C++
 	dxcompiler.dll!llvm::LLVMContext::diagnose(const llvm::DiagnosticInfo &) Line 230	C++
 	[Inline Frame] dxcompiler.dll!hlsl::dxilutil::EmitWarningOrErrorOnContext(llvm::LLVMContext &) Line 369	C++
 	dxcompiler.dll!hlsl::dxilutil::EmitWarningOnContext(llvm::LLVMContext &) Line 377	C++
 	dxcompiler.dll!`anonymous namespace'::DxilFinalizeModule::runOnModule(llvm::Module &) Line 857	C++

```

So based on this, I'm quite sure now that we're looking at two different bugs. The Chrome ASAN failure should be fixed once [my upstream patch](https://github.com/microsoft/DirectXShaderCompiler/pull/6515) lands. This is the same failure I hit with my local asan build of Chrome (see [#comment4](https://issues.chromium.org/issues/333420620#comment4)), but my debugger had stopped on the exception throw, so I did not hit the ASAN failure that follows.

The other ASAN failure that's reproducible with your `standalone.hlsl` against a non-libc++ build of dxc, is a separate issue, and not necessarily a Chrome crash/asan failure. If you can reproduce a crash using this new shader in Chrome that is not due to the `dynamic_cast`, please open a new bug for it. This bug will be used to track this `dynamic_cast` issue.

### am...@google.com (2024-04-10)

I've renamed the bug to clarify that it's for the `dynamic_cast` exception, and not the second ASAN failure reported here.

### wg...@gmail.com (2024-04-10)

Thanks for pointing out the `LIBCXX` flag, I'll recompile and verify before reporting the other findings.

### am...@google.com (2024-04-11)

Patch has landed [upstream](https://github.com/microsoft/DirectXShaderCompiler/pull/6515). Waiting for it to roll into Dawn, then Dawn into Chrome to test on Canary.

### an...@chromium.org (2024-04-11)

@am...@google.com thanks for the quick patch! Do we know the earliest release affected? We only need to go back to the current extended stable (M122).

### am...@google.com (2024-04-11)

> @[amaiorano@google.com](mailto:amaiorano@google.com) thanks for the quick patch! Do we know the earliest release affected? We only need to go back to the current extended stable (M122).

This affects all versions, so from M122 onwards.

### pe...@google.com (2024-04-12)

Setting milestone because of s0/s1 severity.

### am...@google.com (2024-04-15)

I tested opening `indexDeadBlockDeleter.html` (file attached to the bug) on the latest ASAN build of Chromium (`chromium-125.0.6420.0-win64-asan`), and the GPU process does not crash.

I also tested in Canary `Version 125.0.6415.0 (Official Build) canary (64-bit)`, and it does not crash there either.

anunoy@ please let me know which Chromium branches we need to patch, and I'll take care of it.

### am...@google.com (2024-04-17)

[anunoy@chromium.org](mailto:anunoy@chromium.org) can you please let me know which Chromium branches we need to patch?

### an...@chromium.org (2024-04-18)

tagging in @am...@chromium.org - do we merge this patch all the way back to M122 (per <https://issues.chromium.org/issues/333420620#comment14>)?

### am...@chromium.org (2024-04-18)

Hi amaiorano@ the security merge process (<https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/merge_request.md#Security-merge-triage>) allows the automation to automatically update the bug with the correct merge request labels based on severity, security impact, and milestone.

I've closed this bug as fixed to allow the bot to do that as well as put this issue into the security merge review queue.

That all being said, there are no further releases of M122. M124 is current Stable milestone and will be the forthcoming next Extended Stable milestone once M125 is promoted to Stable next month. So this fix would only need to be backmerged as far as M124, but only after the Dawn roll to Chromium has been completed and has been on Canary for at least 48 hours.

### am...@google.com (2024-04-18)

> Hi amaiorano@ the security merge process (<https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/merge_request.md#Security-merge-triage>) allows the automation to automatically update the bug with the correct merge request labels based on severity, security impact, and milestone.

Ah, thank you for the clarification, Amy. I will be sure to mark future bugs as fixed and let the bot do it's thing.

> That all being said, there are no further releases of M122. M124 is current Stable milestone and will be the forthcoming next Extended Stable milestone once M125 is promoted to Stable next month. So this fix would only need to be backmerged as far as M124, but only after the Dawn roll to Chromium has been completed and has been on Canary for at least 48 hours.

I test this on Monday 3 days ago, so I'll go ahead and cherry-pick this fix to M124.

### am...@chromium.org (2024-04-18)

Can you please link the dawn->Chromium roll here so we can review it also? Once that is complete I can officially mark this as approved for merge to M124 assuming there have been no stability issues since this landed on Canary.

### am...@google.com (2024-04-18)

DirectXShaderCompiler -> Dawn roll that includes my fix: <https://dawn.googlesource.com/dawn.git/+/8be0f9e24b250259fb527015c924f6916956b1e3>

Dawn -> Chromium roll that includes the above roll: <https://chromium.googlesource.com/chromium/src/+/d2b8cf3d170bb5006398bd49a232621cb7d700c8>

### pe...@google.com (2024-04-18)

This is sufficiently serious that it should be merged to stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M124. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to beta. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M125. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [124, 125].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### am...@google.com (2024-04-18)

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)

Effectively: <https://dawn-review.googlesource.com/c/dawn/+/183303>. However, I will be cherry-picking my specific fix (<https://github.com/microsoft/DirectXShaderCompiler/pull/6515>) to a milestone-specific branch in Dawn for Chrome.

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes.

3. Does this fix pose any potential non-verifiable stability risks?

No.

4. Does this fix pose any known compatibility risks?

No.

5. Does it require manual verification by the test team? If so, please describe required testing.

Open `indexDeadBlockDeleter.html` (file attached to the bug) in latest Canary, and validate that the GPU process does not crash by looking at the developer console.

### ap...@google.com (2024-04-18)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6367

commit bc18aec94c828f7dc3ba0eb8ad964dfb6453b903
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Thu Apr 18 13:07:04 2024

    Replace dynamic_cast with virtual call (#6515)
    
    Make TextDiagnosticPrinter::setPrefix a virtual function in base class
    DiagnosticConsumer. This allows us to avoid using dynamic_cast in
    BackendConsumer::DxilDiagHandler, required for codebases that do not
    enable RTTI. This is also the only place in the codebase that uses RTTI
    (AFAICT).
    
    Bug: chromium:333420620
    Change-Id: Ida73077f24fdb4b705b5d868b04ac6cfecb30327
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5464347
    Reviewed-by: dan sinclair <dsinclair@chromium.org>
    Reviewed-by: David Neto <dneto@google.com>

M       tools/clang/include/clang/Basic/Diagnostic.h
M       tools/clang/include/clang/Frontend/TextDiagnosticPrinter.h
M       tools/clang/lib/CodeGen/CodeGenAction.cpp

https://chromium-review.googlesource.com/5464347


### am...@google.com (2024-04-18)

- For M124, I've landed the [cherry-pick of my fix](https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5464347) and updated [DEPS to point at it] on Dawn's `chromium/6367` branch. Now waiting for this to be pulled into Chromium's `refs/branch-heads/6367`.
- For M125, this fix is already included in the version of DXC that it was branched at, so nothing further needed here.

### am...@google.com (2024-04-18)

Okay, for M124, my Dawn change has been pulled into Chrome: <https://chromium.googlesource.com/chromium/src.git/+/f39d51abf67acc349b1bca7fad8282760f442ee6>

### am...@chromium.org (2024-04-22)

This fix was landed on 125 and already merged in 124 (thanks, amaiorano@), removing review labels.

### wf...@chromium.org (2024-04-25)

I'm curious - how come the `dynamic_cast` wasn't caught by the tool chain when we tried to compile it and ship it with chrome? Can we add a check for this somewhere? are we using `dynamic_cast` elsewhere in chromium third party deps without realizing it?

### am...@google.com (2024-04-25)

This is in a separate compiled DLL (dxcompiler.dll) which has to be
compiled with rtti and exceptions. Dawn uses LoadLibrary and GetProcAddress
to call into it.

Antonio Maiorano



On Thu, Apr 25, 2024 at 6:21 PM wfh <buganizer-system@google.com> wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/333420620
>
> *Changed*
>
> *wfh@chromium.org <wfh@chromium.org> added comment #29
> <https://issues.chromium.org/issues/333420620#comment29>:*
>
> I'm curious - how come the dynamic_cast wasn't caught by the tool chain
> when we tried to compile it and ship it with chrome? Can we add a check for
> this somewhere? are we using dynamic_cast elsewhere in chromium third
> party deps without realizing it?
>
> _______________________________
>
> *Reference Info: 333420620 GPU process crash via WebGPU shader -
> dynamic_cast exception in DXC*
> component:  Public Trackers > Chromium Public Trackers > Chromium >
> Internals > GPU > Dawn <https://issues.chromium.org/components/1456576>
> status:  Fixed
> reporter:  wgslfuzz@gmail.com
> assignee:  amaiorano@google.com
> cc:  amyressler@chromium.org, anunoy@chromium.org, dneto@google.com, and
> 3 more
> collaborators:  security-notify@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P1
> severity:  S1
> found in:  122
> hotlist:  CVE_description-missing
> <https://issues.chromium.org/hotlists/5433501>, external_security_report
> <https://issues.chromium.org/hotlists/5433527>, reward-topanel
> <https://issues.chromium.org/hotlists/5432096>, Security_Impact-Extended
> <https://issues.chromium.org/hotlists/5432548>, Unconfirmed
> <https://issues.chromium.org/hotlists/5437934>, Untriaged
> <https://issues.chromium.org/hotlists/5614589>
> retention:  Component default
> Component Ancestor Tags:  Internals, Internals>GPU, Internals>GPU>Dawn,
> Internals>GPU>Tint
> Component Tags:  Internals>GPU>Dawn, Internals>GPU>Tint
> CVE:  2024-4060
> Merge:  Merged-124, Merged-6367
> Milestone:  124
> OS:  Linux, Windows
> Security_Release:  1-M124
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you are subscribed to updates on
> Google IssueTracker issue 333420620
> <https://issues.chromium.org/issues/333420620> where you have the roles:
> assignee
> Unsubscribe from this issue.
> <https://issues.chromium.org/issues/333420620?unsubscribe=true>
>


### am...@google.com (2024-04-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### wf...@chromium.org (2024-04-25)

rE: #30 if so, why does it matter if this if dynamic cast is used here since if RTTI is enabled for dxcompiler.dll then it should just work - are these classes passed across the module boundary?

### am...@chromium.org (2024-04-25)

Congratulations wgslfuzz! The Chrome VRP Panel has decided to award you $10,000 for this report of GPU process memory corruption. Thank you for your efforts and reporting this issue to us -- nice work!

### am...@google.com (2024-04-26)

wfh@ sorry, I mispoke, which is what I get for writing from my phone. We
build dxcompiler.dll with RTTI disabled, so as to match Chrome as much as
possible, since one of our goals is to eventually link against it as a
static lib (one obstacle is that it presently makes use of exceptions, so
that's currently enabled).

Anyway, with RTTI disabled, we needed to remove this dynamic_cast, which
was not too contentious as it was the only one in the codebase.

- Antonio



On Thu, Apr 25, 2024 at 7:37 PM amyressler <buganizer-system@google.com>
wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/333420620
>
> *Changed*
>
> *amyressler@chromium.org <amyressler@chromium.org> added comment #33
> <https://issues.chromium.org/issues/333420620#comment33>:*
>
> Congratulations wgslfuzz! The Chrome VRP Panel has decided to award you
> $10,000 for this report of GPU process memory corruption. Thank you for
> your efforts and reporting this issue to us -- nice work!
>
> _______________________________
>
> *Reference Info: 333420620 GPU process crash via WebGPU shader -
> dynamic_cast exception in DXC*
> component:  Public Trackers > Chromium Public Trackers > Chromium >
> Internals > GPU > Dawn <https://issues.chromium.org/components/1456576>
> status:  Fixed
> reporter:  wgslfuzz@gmail.com
> assignee:  amaiorano@google.com
> cc:  amyressler@chromium.org, anunoy@chromium.org, dneto@google.com, and
> 3 more
> collaborators:  security-notify@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P1
> severity:  S1
> found in:  122
> hotlist:  CVE_description-missing
> <https://issues.chromium.org/hotlists/5433501>, external_security_report
> <https://issues.chromium.org/hotlists/5433527>, reward-unpaid
> <https://issues.chromium.org/hotlists/5432783>, Security_Impact-Extended
> <https://issues.chromium.org/hotlists/5432548>, Unconfirmed
> <https://issues.chromium.org/hotlists/5437934>, Untriaged
> <https://issues.chromium.org/hotlists/5614589>
> retention:  Component default
> Component Ancestor Tags:  Internals, Internals>GPU, Internals>GPU>Dawn,
> Internals>GPU>Tint
> Component Tags:  Internals>GPU>Dawn, Internals>GPU>Tint
> CVE:  2024-4060
> Merge:  Merged-124, Merged-6367
> Milestone:  124
> OS:  Linux, Windows
> Security_Release:  1-M124
> vrp-reward:  10000
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you are subscribed to updates on
> Google IssueTracker issue 333420620
> <https://issues.chromium.org/issues/333420620> where you have the roles:
> assignee
> Unsubscribe from this issue.
> <https://issues.chromium.org/issues/333420620?unsubscribe=true>
>


### pe...@google.com (2024-07-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/333420620)*

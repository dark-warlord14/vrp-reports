# Security: use-after-poison in blink::MLGraphXnnpack::ComputeAsyncImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [41489926](https://issues.chromium.org/issues/41489926) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebML |
| **Platforms** | Mac |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ni...@intel.com |
| **Created** | 2024-01-09 |
| **Bounty** | $10,000.00 |

## Description

---

### Report description


Security: use-after-poison in blink::MLGraphXnnpack::ComputeAsyncImpl


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


---

### The problem


#### Please describe the technical details of the vulnerability

VULNERABILITY DETAILS
RCA and Bisect coming soon!!!

VERSION
Chrome Version: [120.0.0.0] + [stable, beta, or dev]
Operating System: MacOS M1

REPRODUCTION CASE
1. Compile an asan chromium on macos with m1 architecture. The commit I used to test the vulnerability is 6b2b6f5aa258a1616fab24634c4e9477cfef5daf.
2. Start asan chromium: ./out/asan-chromium/Chromium.app/Contents/MacOS/Chromium --no-sandbox --enable-features=WebMachineLearningNeuralNetwork http://127.0.0.1:8000/index.html --user-data-dir=/tmp/noexists
3. The use-after-poison vulnerability will trigger immediately



FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
```
=================================================================
==4450==ERROR: AddressSanitizer: use-after-poison on address 0x60200005881f at pc 0x00017a4b43c0 bp 0x000170b02580 sp 0x000170b02578
READ of size 16 at 0x60200005881f thread T4
==4450==WARNING: invalid path to external symbolizer!
==4450==WARNING: Failed to use and restart external symbolizer!
    #0 0x17a4b43bc in xnn_f32_vclamp_ukernel__neon_u8+0x404 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libblink_modules.dylib:arm64+0x39903bc)
    #1 0x17a47e988 in pthreadpool_parallelize_1d_tile_1d+0x158 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libblink_modules.dylib:arm64+0x395a988)
    #2 0x17a4436b8 in xnn_run_operator_with_index+0x7b4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libblink_modules.dylib:arm64+0x391f6b8)
    #3 0x17a46d410 in xnn_invoke_runtime+0xf0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libblink_modules.dylib:arm64+0x3949410)
    #4 0x178f125ac in blink::(anonymous namespace)::XnnRuntimeWrapper::Invoke(std::__Cr::unique_ptr<WTF::Vector<xnn_external_value, 0u, WTF::PartitionAllocator>, std::__Cr::default_delete<WTF::Vector<xnn_external_value, 0u, WTF::PartitionAllocator>>>, WTF::String&)+0x3dc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libblink_modules.dylib:arm64+0x23ee5ac)
    #5 0x178f10f18 in blink::MLGraphXnnpack::ComputeOnBackgroundThread(blink::ScopedMLTrace, scoped_refptr<blink::(anonymous namespace)::XnnRuntimeWrapper>, std::__Cr::unique_ptr<WTF::Vector<xnn_external_value, 0u, WTF::PartitionAllocator>, std::__Cr::default_delete<WTF::Vector<xnn_external_value, 0u, WTF::PartitionAllocator>>>, std::__Cr::unique_ptr<WTF::Vector<std::__Cr::pair<WTF::String, blink::ArrayBufferViewInfo>, 0u, WTF::PartitionAllocator>, std::__Cr::default_delete<WTF::Vector<std::__Cr::pair<WTF::String, blink::ArrayBufferViewInfo>, 0u, WTF::PartitionAllocator>>>, std::__Cr::unique_ptr<WTF::Vector<std::__Cr::pair<WTF::String, blink::ArrayBufferViewInfo>, 0u, WTF::PartitionAllocator>, std::__Cr::default_delete<WTF::Vector<std::__Cr::pair<WTF::String, blink::ArrayBufferViewInfo>, 0u, WTF::PartitionAllocator>>>, blink::internal::BasicCrossThreadHandle<blink::MLGraphXnnpack, blink::internal::StrongCrossThreadHandleWeaknessPolicy>, blink::internal::BasicCrossThreadHandle<blink::ScriptPromiseResolver, blink::internal::StrongCrossThreadHandleWeaknessPolicy>, scoped_refptr<base::SequencedTaskRunner>)+0x258 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libblink_modules.dylib:arm64+0x23ecf18)
    #6 0x178f3c7f4 in base::internal::Invoker<base::internal::BindState<void (*)(blink::ScopedMLTrace, scoped_refptr<blink::(anonymous namespace)::XnnRuntimeWrapper>, std::__Cr::unique_ptr<WTF::Vector<xnn_external_value, 0u, WTF::PartitionAllocator>, std::__Cr::default_delete<WTF::Vector<xnn_external_value, 0u, WTF::PartitionAllocator>>>, std::__Cr::unique_ptr<WTF::Vector<std::__Cr::pair<WTF::String, blink::ArrayBufferViewInfo>, 0u, WTF::PartitionAllocator>, std::__Cr::default_delete<WTF::Vector<std::__Cr::pair<WTF::String, blink::ArrayBufferViewInfo>, 0u, WTF::PartitionAllocator>>>, std::__Cr::unique_ptr<WTF::Vector<std::__Cr::pair<WTF::String, blink::ArrayBufferViewInfo>, 0u, WTF::PartitionAllocator>, std::__Cr::default_delete<WTF::Vector<std::__Cr::pair<WTF::String, blink::ArrayBufferViewInfo>, 0u, WTF::PartitionAllocator>>>, blink::internal::BasicCrossThreadHandle<blink::MLGraphXnnpack, blink::internal::StrongCrossThreadHandleWeaknessPolicy>, blink::internal::BasicCrossThreadHandle<blink::ScriptPromiseResolver, blink::internal::StrongCrossThreadHandleWeaknessPolicy>, scoped_refptr<base::SequencedTaskRunner>), blink::ScopedMLTrace, scoped_refptr<blink::(anonymous namespace)::XnnRuntimeWrapper>, std::__Cr::unique_ptr<WTF::Vector<xnn_external_value, 0u, WTF::PartitionAllocator>, std::__Cr::default_delete<WTF::Vector<xnn_external_value, 0u, WTF::PartitionAllocator>>>, std::__Cr::unique_ptr<WTF::Vector<std::__Cr::pair<WTF::String, blink::ArrayBufferViewInfo>, 0u, WTF::PartitionAllocator>, std::__Cr::default_delete<WTF::Vector<std::__Cr::pair<WTF::String, blink::ArrayBufferViewInfo>, 0u, WTF::PartitionAllocator>>>, std::__Cr::unique_ptr<WTF::Vector<std::__Cr::pair<WTF::String, blink::ArrayBufferViewInfo>, 0u, WTF::PartitionAllocator>, std::__Cr::default_delete<WTF::Vector<std::__Cr::pair<WTF::String, blink::ArrayBufferViewInfo>, 0u, WTF::PartitionAllocator>>>, blink::internal::BasicCrossThreadHandle<blink::MLGraphXnnpack, blink::internal::StrongCrossThreadHandleWeaknessPolicy>, blink::internal::BasicCrossThreadHandle<blink::ScriptPromiseResolver, blink::internal::StrongCrossThreadHandleWeaknessPolicy>, scoped_refptr<base::SequencedTaskRunner>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x2cc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libblink_modules.dylib:arm64+0x24187f4)
    #7 0x1033293ac in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x3c4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x1c93ac)
    #8 0x1033d6af0 in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0x1ac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x276af0)
    #9 0x1033d5858 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&)+0x550 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x275858)
    #10 0x1033d4984 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource)+0x68c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x274984)
    #11 0x1033f500c in base::internal::WorkerThread::RunWorker()+0x804 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x29500c)
    #12 0x1033f4460 in base::internal::WorkerThread::RunPooledWorker()+0xb4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x294460)
    #13 0x1033f3d90 in base::internal::WorkerThread::ThreadMain()+0x1b8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x293d90)
    #14 0x103486554 in base::(anonymous namespace)::ThreadFunc(void*)+0x138 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x326554)
    #15 0x101c907b8 in __sanitizer_weak_hook_memcmp+0x345bc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4c7b8)
    #16 0x182926030 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64+0x7030)
    #17 0x9c6a000182920e38  (<unknown module>)

0x60200005881f is located 3 bytes after 12-byte region [0x602000058810,0x60200005881c)
allocated by thread T0 here:
    #0 0x101ca2640 in __sanitizer_finish_switch_fiber+0x73c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libclang_rt.asan_osx_dynamic.dylib:arm64+0x5e640)
    #1 0x178f0c454 in blink::MLGraphXnnpack::CreateXnnSubgraph(blink::HeapVector<std::__Cr::pair<WTF::String, cppgc::internal::BasicMember<blink::MLOperand, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>>, 0u> const&, std::__Cr::unique_ptr<xnn_subgraph, xnn_status (*)(xnn_subgraph*)>&, WTF::Vector<std::__Cr::unique_ptr<unsigned char [], std::__Cr::default_delete<unsigned char []>>, 0u, WTF::PartitionAllocator>&, WTF::String&)+0x1278 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libblink_modules.dylib:arm64+0x23e8454)
    #2 0x178f08ff8 in blink::MLGraphXnnpack::OnDidGetSharedXnnpackContext(blink::ScopedMLTrace, scoped_refptr<blink::(anonymous namespace)::SharedXnnpackContext>, blink::HeapVector<std::__Cr::pair<WTF::String, cppgc::internal::BasicMember<blink::MLOperand, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>>, 0u>*, blink::ScriptPromiseResolver*, WTF::String)+0x2a8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libblink_modules.dylib:arm64+0x23e4ff8)
    #3 0x178f379a4 in base::internal::Invoker<base::internal::BindState<void (blink::MLGraphXnnpack::*)(blink::ScopedMLTrace, scoped_refptr<blink::(anonymous namespace)::SharedXnnpackContext>, blink::HeapVector<std::__Cr::pair<WTF::String, cppgc::internal::BasicMember<blink::MLOperand, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>>, 0u>*, blink::ScriptPromiseResolver*, WTF::String), blink::internal::BasicUnwrappingCrossThreadHandle<blink::MLGraphXnnpack, blink::internal::StrongCrossThreadHandleWeaknessPolicy>, blink::ScopedMLTrace, scoped_refptr<blink::(anonymous namespace)::SharedXnnpackContext>, blink::internal::BasicUnwrappingCrossThreadHandle<blink::HeapVector<std::__Cr::pair<WTF::String, cppgc::internal::BasicMember<blink::MLOperand, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>>, 0u>, blink::internal::StrongCrossThreadHandleWeaknessPolicy>, blink::internal::BasicUnwrappingCrossThreadHandle<blink::ScriptPromiseResolver, blink::internal::StrongCrossThreadHandleWeaknessPolicy>, WTF::String>, void ()>::RunOnce(base::internal::BindStateBase*)+0x1f4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libblink_modules.dylib:arm64+0x24139a4)
    #4 0x1033293ac in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x3c4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x1c93ac)
    #5 0x103389b08 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x798 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x229b08)
    #6 0x103388ec8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x15c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x228ec8)
    #7 0x1031f0a0c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1d8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x90a0c)
    #8 0x10338b374 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3e8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x22b374)
    #9 0x1032ab818 in base::RunLoop::Run(base::Location const&)+0x494 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x14b818)
    #10 0x110cb3344 in content::RendererMain(content::MainFunctionParams)+0x8ac (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libcontent.dylib:arm64+0x34ab344)
    #11 0x110e6cae4 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x418 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libcontent.dylib:arm64+0x3664ae4)
    #12 0x110e6eb50 in content::ContentMainRunnerImpl::Run()+0x5bc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libcontent.dylib:arm64+0x3666b50)
    #13 0x110e6a220 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x620 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libcontent.dylib:arm64+0x3662220)
    #14 0x110e6ac04 in content::ContentMain(content::ContentMainParams)+0x174 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libcontent.dylib:arm64+0x3662c04)
    #15 0x1182c65b0 in ChromeMain+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libchrome_dll.dylib:arm64+0xa5b0)
    #16 0x100cb4d34 in main+0x2a4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/122.0.6235.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000d34)
    #17 0x1825a50dc  (<unknown module>)
    #18 0xf264fffffffffffc  (<unknown module>)

Thread T4 created by T0 here:
    #0 0x101c8b540 in __sanitizer_weak_hook_memcmp+0x2f344 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libclang_rt.asan_osx_dynamic.dylib:arm64+0x47540)
    #1 0x10348598c in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x278 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x32598c)
    #2 0x1033f3150 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*)+0x4bc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x293150)
    #3 0x1033e63d0 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThreadWaitableEvent*)::operator()(base::internal::WorkerThreadWaitableEvent*) const+0x1bc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x2863d0)
    #4 0x1033e5fb4 in void base::internal::ThreadGroupImpl::ScopedCommandsExecutor::WorkerContainer::ForEachWorker<base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThreadWaitableEvent*)>(base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThreadWaitableEvent*))+0xf8 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x285fb4)
    #5 0x1033e66dc in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor()+0xf4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x2866dc)
    #6 0x1033de86c in base::internal::ThreadGroupImpl::Start(unsigned long, unsigned long, base::TimeDelta, scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*, base::internal::ThreadGroup::WorkerEnvironment, bool, std::__Cr::optional<base::TimeDelta>)+0x2e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x27e86c)
    #7 0x1033ebcec in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver*)+0x82c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libbase.dylib:arm64+0x28bcec)
    #8 0x10d8c51a8 in content::ChildProcess::ChildProcess(base::ThreadType, std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>)+0x2e0 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libcontent.dylib:arm64+0xbd1a8)
    #9 0x110c8b358 in content::RenderProcess::RenderProcess(std::__Cr::unique_ptr<base::ThreadPoolInstance::InitParams, std::__Cr::default_delete<base::ThreadPoolInstance::InitParams>>)+0x20 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libcontent.dylib:arm64+0x3483358)
    #10 0x110c8b4c4 in content::RenderProcessImpl::RenderProcessImpl()+0x10c (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libcontent.dylib:arm64+0x34834c4)
    #11 0x110cb2f18 in content::RendererMain(content::MainFunctionParams)+0x480 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libcontent.dylib:arm64+0x34aaf18)
    #12 0x110e6cae4 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x418 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libcontent.dylib:arm64+0x3664ae4)
    #13 0x110e6eb50 in content::ContentMainRunnerImpl::Run()+0x5bc (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libcontent.dylib:arm64+0x3666b50)
    #14 0x110e6a220 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x620 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libcontent.dylib:arm64+0x3662220)
    #15 0x110e6ac04 in content::ContentMain(content::ContentMainParams)+0x174 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libcontent.dylib:arm64+0x3662c04)
    #16 0x1182c65b0 in ChromeMain+0x348 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libchrome_dll.dylib:arm64+0xa5b0)
    #17 0x100cb4d34 in main+0x2a4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/122.0.6235.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000d34)
    #18 0x1825a50dc  (<unknown module>)
    #19 0xf264fffffffffffc  (<unknown module>)

SUMMARY: AddressSanitizer: use-after-poison (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libblink_modules.dylib:arm64+0x39903bc) in xnn_f32_vclamp_ukernel__neon_u8+0x404
Shadow bytes around the buggy address:
  0x602000058580: f7 fa fd fd f7 fa fd fd f7 fa fd fd f7 fa fd fd
  0x602000058600: f7 fa fd fd f7 fa fd fa f7 fa fd fd f7 fa fd fa
  0x602000058680: f7 fa 00 00 f7 fa fd fd f7 fa fd fd f7 fa fd fa
  0x602000058700: f7 fa 00 fa f7 fa fd fd f7 fa fd fd f7 fa fd fa
  0x602000058780: f7 fa fd fd f7 fa fd fa f7 fa fd fd f7 fa fd fd
=>0x602000058800: f7 fa 00[04]f7 fa fd fa f7 fa 00 fa f7 fa fd fd
  0x602000058880: f7 fa fd fd f7 fa fd fd f7 fa fd fa f7 fa fd fa
  0x602000058900: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fd
  0x602000058980: f7 fa fd fd f7 fa fd fd f7 fa fd fd f7 fa fd fd
  0x602000058a00: f7 fa fd fd f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x602000058a80: f7 fa fd fa f7 fa fd fa f7 fa fd fd f7 fa fd fd
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

==4450==ADDITIONAL INFO

==4450==Note: Please include this section with the ASan report.
Task trace:
    #0 0x178f0e830 in blink::MLGraphXnnpack::ComputeAsyncImpl(blink::ScopedMLTrace, blink::HeapVector<std::__Cr::pair<WTF::String, blink::NotShared<blink::DOMArrayBufferView>>, 0u> const&, blink::HeapVector<std::__Cr::pair<WTF::String, blink::NotShared<blink::DOMArrayBufferView>>, 0u> const&, blink::ScriptPromiseResolver*, blink::ExceptionState&)+0x2f4 (/Users/zh1x1an1221/xcode-chromium/src/out/asan-chromium-0108/libblink_modules.dylib:arm64+0x23ea830)


==4450==END OF ADDITIONAL INFO
==4450==ABORTING
```


#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

use-after-poison in the renderer process



---

### The cause


#### What version of Chrome have you found the security issue in?

122.0.6235.0


#### Is the security issue related to a crash?

Yes


#### Choose the type of vulnerability

Memory Corruption (in a sandboxed processs) 


#### How would you like to be publicly acknowledged for your report?

@zh1x1an1221 of Ant Group Light-Year Security Lab




## Attachments

- [asan-use-after-poison](attachments/asan-use-after-poison) (text/plain, 18.7 KB)
- [index.html](attachments/index.html) (text/plain, 522 B)
- [poc.mov](attachments/poc.mov) (video/quicktime, 4.3 MB)
- [poc.mov](attachments/poc.mov) (video/quicktime, 7.3 MB)
- [heap-buffer-overflow](attachments/heap-buffer-overflow) (text/plain, 26.9 KB)

## Timeline

### ch...@appspot.gserviceaccount.com (2024-01-09)

[Empty comment from Monorail migration]

### hc...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### zh...@gmail.com (2024-01-10)

Update the index.html and video required to trigger the vulnerability

It should be noted that so far I recommend reproducing this vulnerability on macos with m1 architecture.

### zh...@gmail.com (2024-01-10)

## RCA here !!!

In the index.html code, I constructed this line of code:

```
const output = builder.relu(builder.constant({ dataType: 'float32', dimensions: [3] }, new Float32Array([-1, 0, 1])));
```

Here, a `Float32Array([-1,0,1])` is passed in. This `-1` will eventually be used as a `const float* input` type variable and executed according to the following call chain: [1][2][3][ 4]


[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack.cc;l=2082-2096?q=ml_graph_xnnpack.cc:2076

[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack.cc;l=330?q=ml_graph_xnnpack.cc:330&sq=

[3] https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/operator-run.c;l=2771-2774?q=operator-run.c:2774

If it is an arm system, the code will eventually be executed here, which is why I emphasize the need to use the mac m1 system to trigger the vulnerability:

[4] https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/amalgam/gen/neon.c;l=9235?q=neon.c:9229

```
if XNN_UNLIKELY(batch != 0) {
    float32x4_t vacc = vld1q_f32(input); // no check here
```

`vld1q_f32` is a macro, take a look at its code implementation: [5]

[5] https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:gen/arm64-generic/chroot/usr/lib64/clang/18/include/arm_neon.h;l=8812-8817?q=arm_neon.h:8818


```c
#ifdef __LITTLE_ENDIAN__
#define vld1q_f32(__p0) __extension__ ({ \
  float32x4_t __ret; \
  __ret = (float32x4_t) __builtin_neon_vld1q_v(__p0, 41); \
  __ret; \
})
#else
```

This macro vld1q_f32 uses the NEON instruction set to load data, which is designed for vector processing. The float32x4_t type represents a 128-bit vector that can store 4 single-precision floating point numbers. When using the vld1q_f32 macro, it will expect that the memory area pointed to by the input pointer has space for at least 4 floating point numbers (4 32 bits = 128 bits), because NEON's load instruction loads 128 bits of data at a time.

If the input pointer only points to a single floating point number, then the load operation will exceed the memory area behind the single floating point number, resulting in memory out of bounds.

In order to ensure safe use of the vld1q_f32 macro, I think it may be necessary to add a check to ensure that the memory area pointed to by the incoming pointer can store at least 4 consecutive float values.

The general meaning is that if we can ensure that it is like this every time it is executed, then there should be no memory overflow:

```c
float data[4] = {1.0, 2.0, 3.0, 4.0};
const float* input = data; // The memory area pointed to by input can store at least 4 consecutive float values.
float32x4_t vacc = vld1q_f32(input);
```

In order to verify my analysis, I provide a small test code, because essentially the vulnerability principle is the same, and it is more concise and easy to understand:

```c
#include <stdio.h>
#include <stdint.h>
#include <arm_neon.h>

int main() {
    float single_value = 1.0f;
    const float* input = &single_value;

    float32x4_t vacc = vld1q_f32(input);
    return 0;
}
```

```
gcc -fsanitize=address -march=native -o test 1.c;./test

=================================================================
==70015==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x00016f51336f at pc 0x0001008efdd8 bp 0x00016f513330 sp 0x00016f513328
READ of size 16 at 0x00016f51336f thread T0
    #0 0x1008efdd4 in main+0x234 (test:arm64+0x100003dd4)
    #1 0x1825a50dc  (<unknown module>)

Address 0x00016f51336f is located in stack of thread T0 at offset 47 in frame
    #0 0x1008efbac in main+0xc (test:arm64+0x100003bac)

  This frame has 1 object(s):
    [32, 36) 'single_value' <== Memory access at offset 47 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow (test:arm64+0x100003dd4) in main+0x234
Shadow bytes around the buggy address:
  0x00016f513080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x00016f513100: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x00016f513180: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x00016f513200: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x00016f513280: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x00016f513300: 00 00 00 00 00 00 00 00 f1 f1 f1 f1 04[f3]f3 f3
  0x00016f513380: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x00016f513400: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x00016f513480: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x00016f513500: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x00016f513580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
==70015==ABORTING
[1]    70015 abort      ./test
```

Finally, the remaining thing that makes me more curious is why in my vulnerability report, asan shows uap instead of heap-buffer-overflow? Maybe this is related to blink's memory management? For example, gc marks the memory as poison?

### zh...@gmail.com (2024-01-10)

## Bisect

Based on my previous analysis, I think the reasonable Bisect commit should be this, which is the commit that adds the `xnn_f32_vclamp_ukernel__neon_u8` function:

https://source.chromium.org/chromium/_/chromium/external/github.com/google/XNNPACK.git/+/bf8c1b8ddfa1a955d56f9eded85219546e0c2f4e:src/amalgam/neon.c;dlc=2303b09d9178922909d21b69984202af11972a8e

maratek@google.com should be a more reasonable owner

When creating this code, some basic assertion checks were performed, but there was no check whether the input pointer really pointed to enough memory space, which was the source of the problem. However, I am not a qualified developer, so now I am not sure whether it is more appropriate to check input in `xnn_f32_vclamp_ukernel__neon_u8`, or whether it is more appropriate to check input in the call above.

If you have any questions about my analysis or have other suggestions, please let me know, thank you.

### hc...@google.com (2024-01-10)

[Empty comment from Monorail migration]

### hc...@google.com (2024-01-10)

[Empty comment from Monorail migration]

### hc...@google.com (2024-01-10)

[Empty comment from Monorail migration]

### zh...@gmail.com (2024-01-12)

It seems that compiling a complete chromium reproduction vulnerability on mac m1 is a bit complicated and time-consuming, so if you want to reproduce the vulnerability, you can also download asan-mac-release-1246313 on an m1 architecture mac computer, and then execute `sudo xattr -rd com.apple.quarantine Chromium.app`, this can more easily reproduce the vulnerability without compiling the entire chromium.


### hc...@google.com (2024-01-12)

[Empty comment from Monorail migration]

### hc...@google.com (2024-01-12)

Chatted w/ alankelly@, he thinks the root cause is:

I know what's happening. It's an issue with webNN
For performance reasons, XNNPack requires that input buffers be padded with 16 extra bytes
The WebNN team is aware of this
XNNPack will read up to 16 bytes past the end of an array
const output = builder.relu(builder.constant({ dataType: 'float32', dimensions: [3] }, new Float32Array([-1, 0, 1])));
The sample given here is an input array of 12 bytes (3x float)
So it looks like WebNN need to protect against users passing insufficient memory as input
Other users of XNNPack such as TFLite allocate the input buffer and require the user to use this as the input

amoylan or qjw@, could you take a look and possibly reroute if you're not the right people?

[Monorail components: Blink>WebML]

### aj...@google.com (2024-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-12)

[Empty comment from Monorail migration]

### fb...@google.com (2024-01-12)

I think the issue is the remainder handling of vclamp
  if XNN_UNLIKELY(batch != 0) {
    float32x4_t vacc = vld1q_f32(input);   // <-- read 4 floats
    vacc = vmaxq_f32(vacc, vy_min);
    vacc = vminq_f32(vacc, vy_max);

    float32x2_t vacc_lo = vget_low_f32(vacc);
    if (batch & (2 * sizeof(float))) {
      vst1_f32(output, vacc_lo); output += 2;
      vacc_lo = vget_high_f32(vacc);
    }
    if (batch & (1 * sizeof(float))) {
      vst1_lane_f32(output, vacc_lo, 0);
    }
  }

The function is marked as having out of bounds reads, but with floats it is unsafe to use garbage values.
We have a number of solutions to remainder handling of floats available
1. mask the vector
2. switch statement and load exactly the remainder with custom code, such as ld3 for remainder of 3 floats
3. loop 1 at a time
4. divide and conquer - test bits and handle powers of 2
On ARM we usually use divide conquer and that includes the load and store being exact power of 2.  Here the store is done right but the load should also be exact.

Also this kernel isnt M1 optimized.  Apple M1 and Cortex X1 have 3 optimizations that should be applied
1. ldp is preferred to load 2 vectors at a time.  ld4 is slow, however.
2. 4 vector units means unroll everything to 4 so 4 max instructions can dispatch in 1 cycle
3. high latency destination (Vd Latency) is high.  Unroll and use multiple destination registers.  On top of unrolling by 4 for 4 clamp instructions per cycle, it may help to unroll by 8 or 16 so the same destination register is not used in the next cycle.

Is this used on a large model?  If so
1. You should consider FP16 and I should ensure the fix is in that kernel as well.
2. I could add a prefetch to help with memory throughput
fp16 is more than 2x faster, since vectors process 8 elements at a time instead of 4, and the memory reads hit cache more often.




### fb...@google.com (2024-01-13)

There are potentially 2 issues with the code
1. the remainder code reads out of bounds
2. there is a bug in clang with vld1_dup which typically affects params such as
const float32x4_t vy_min = vld1q_dup_f32(&params->scalar.min);
const float32x4_t vy_max = vld1q_dup_f32(&params->scalar.max);


1. The fix for xnn_f32_vclamp_ukernel__neon_u8 is:

<     const union xnn_f32_minmax_params params[restrict XNN_MIN_ELEMENTS(1)]) XNN_OOB_READS
---
>     const union xnn_f32_minmax_params params[restrict XNN_MIN_ELEMENTS(1)])
52,56d51
<     float32x4_t vacc = vld1q_f32(input);
<     vacc = vmaxq_f32(vacc, vy_min);
<     vacc = vminq_f32(vacc, vy_max);
< 
<     float32x2_t vacc_lo = vget_low_f32(vacc);
58,59c53,56
<       vst1_f32(output, vacc_lo); output += 2;
<       vacc_lo = vget_high_f32(vacc);
---
>       float32x2_t vacc = vld1_f32(input); input += 2;
>       vacc = vmax_f32(vacc, vget_low_f32(vy_min));
>       vacc = vmin_f32(vacc, vget_low_f32(vy_max));
>       vst1_f32(output, vacc); output += 2;
62c59,62
<       vst1_lane_f32(output, vacc_lo, 0);
---
>       float32x2_t vacc = vld1_dup_f32(input);
>       vacc = vmax_f32(vacc, vget_low_f32(vy_min));
>       vacc = vmin_f32(vacc, vget_low_f32(vy_max));
>       vst1_lane_f32(output, vacc, 0);

If you're running into the bug with vld1_dup, this fix makes it worse, but I've only seen it on newer versions are armv7 clang.
For the clamp values, the work around is use vld2_dup, which is better anyway, so I'll make a followup CL for that.

The same code patterns affect all cpus, so you'll likely see the same asan warning on x86 macOS, and fp16.
The remainder code is not a serious bug... the invalid values use used by min/max but not stored.
If you hit the vld1_dup bug, it is more serious - the results are corrupt.
You can tell by disassembling the function and look for vld1_dup

clang 17 produces inefficient code, but it looks ok.  The 2 vld1_dup generates:
ldp	s0, s1, [x3]
dup	v2.4s, v0.s[0]
dup	v3.4s, v1.s[0]
and later it dups them again:
dup	v0.2s, v0.s[0]
dup	v1.2s, v1.s[0]

When it would be better to
ld2r	{ v0.4s, v1.4s }, [x3]

The cl to fix this is checked into our internal repo.  Not sure how you take changes into chrome




### qj...@chromium.org (2024-01-15)

Ningxin, can you take a look at this?

> "XNNPack will read up to 16 bytes past the end of an array"

We should guard this in XNNPACK Graph impl.

---

Bumping priority to P-1 given this causes out of bounds memory access in the renderer, which according to https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#toc-medium-severity is at least medium severity.



### qj...@chromium.org (2024-01-15)

/cc reillyg who has been looking into WebNN on MacOS

### ni...@intel.com (2024-01-15)

> For performance reasons, XNNPack requires that input buffers be padded with 16 extra bytes

Thanks Alan! I am uploading a CL that allocates extra bytes for input buffers in WebNN XNNPACK implementation. 

https://chromium-review.googlesource.com/c/chromium/src/+/5196857. Please take a look.

I cannot reproduce this issue on x86 Windows and I don't have a M1 Mac at hand, so if someone can help me verify this fix, that would be extremely helpful. Thanks in advance!

### fb...@google.com (2024-01-15)

Its still not best practice for float/fp16 code process out of bounds data.
I've checked in fixes for neon fp32/fp16.  riscv and avx512 were ok.
todo - wasmsimd, sse, avx.

### ni...@intel.com (2024-01-16)

Do we have Mac asan bot can help verify the fix? WebNN has relu unit test [1] which sets one float value or two float values to XNNPACK graph. I suppose it should be able to reproduce this issue.

[1]: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/ml/webnn/ml_graph_test.cc;l=581

### zh...@gmail.com (2024-01-17)

I can't make a 100% guarantee, but for now, the patch has blocked my poc for repo the bug, and I haven't found any other problems for now

### re...@chromium.org (2024-01-17)

I'm checking whether I can reproduce this failure using the existing test in ml_graph_test.cc and whether it is fixed by fbarchard@'s upstream change to XNNPACK.

### re...@chromium.org (2024-01-18)

I'm having some trouble rolling XNNPACK to the latest to test. It sounds like both the XNNPACK fix and appropriate padding on the Chrome side are necessary to truly resolve this issue. Adding sophiechang@ to get this on her radar for a future TensorFlow/XNNPACK roll.

### so...@chromium.org (2024-01-18)

robert is going to roll this week. so cc-ing him

### gi...@appspot.gserviceaccount.com (2024-01-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/863707c26f35d9744bba4646adecfd238a4e220a

commit 863707c26f35d9744bba4646adecfd238a4e220a
Author: Robert Ogden <robertogden@chromium.org>
Date: Sat Jan 20 17:37:12 2024

Roll XNNPACK to HEAD

The TFLite open-source build is broken at the moment, but roll XNNPACK
forward this week at least.

Bug: 1516943, b:201542766
Change-Id: I650c4a64dd8d86a2d0797a8d43fe17d9525572e5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5220093
Auto-Submit: Robert Ogden <robertogden@chromium.org>
Reviewed-by: Sophie Chang <sophiechang@chromium.org>
Commit-Queue: Sophie Chang <sophiechang@chromium.org>
Commit-Queue: Robert Ogden <robertogden@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1249840}

[modify] https://crrev.com/863707c26f35d9744bba4646adecfd238a4e220a/third_party/xnnpack/src
[modify] https://crrev.com/863707c26f35d9744bba4646adecfd238a4e220a/DEPS
[modify] https://crrev.com/863707c26f35d9744bba4646adecfd238a4e220a/third_party/xnnpack/README.chromium
[modify] https://crrev.com/863707c26f35d9744bba4646adecfd238a4e220a/third_party/xnnpack/BUILD.gn


### zh...@gmail.com (2024-01-21)

After testing, I can also trigger another function `xnn_f32_vaddc_minmax_ukernel__neon_u8` [1] heap-buffer-overflow vulnerability:

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/amalgam/gen/neon.c;l=8556?q=neon.c:8556&sq=

I'm not sure yet whether these two vulnerabilities have exactly the same root cause, but at least so far, the overflow of two different functions can be triggered in different ways, one is the uap in the vulnerability report, and the other is the heap-buffer-overflow here.I don’t know if VRP will consider it as two vulnerabilities in this case. To avoid trouble, I will submit them under this vulnerability report.

### aj...@chromium.org (2024-01-21)

Thanks for the extra information - ningxin could you take a look and leave a comment if the report in https://crbug.com/chromium/1516943#c26 is the same root cause or a different one?

### gi...@appspot.gserviceaccount.com (2024-01-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8ab8ec6714e86957219cff897a9bb66ebdcea359

commit 8ab8ec6714e86957219cff897a9bb66ebdcea359
Author: luci-bisection@appspot.gserviceaccount.com <luci-bisection@appspot.gserviceaccount.com>
Date: Mon Jan 22 10:32:57 2024

Revert "Roll XNNPACK to HEAD"

This reverts commit 863707c26f35d9744bba4646adecfd238a4e220a.

Reason for revert:
LUCI Bisection has identified this change as the cause of a test failure. See the analysis: https://ci.chromium.org/ui/p/chromium/bisection/test-analysis/b/5164591178842112

Sample build with failed test: https://ci.chromium.org/b/8758357091669518465
Affected test(s):
[ninja://third_party/blink/renderer/controller:blink_unittests/MLGraphTest.Pool2dTest/All.Xnnpack_Async](https://ci.chromium.org/ui/test/chromium/ninja:%2F%2Fthird_party%2Fblink%2Frenderer%2Fcontroller:blink_unittests%2FMLGraphTest.Pool2dTest%2FAll.Xnnpack_Async?q=VHash%3A8ff0919b88aee026)
[ninja://third_party/blink/renderer/controller:blink_unittests/MLGraphTest.Pool2dTest/All.Xnnpack_Sync](https://ci.chromium.org/ui/test/chromium/ninja:%2F%2Fthird_party%2Fblink%2Frenderer%2Fcontroller:blink_unittests%2FMLGraphTest.Pool2dTest%2FAll.Xnnpack_Sync?q=VHash%3A8ff0919b88aee026)
[ninja://third_party/blink/renderer/controller:blink_unittests_v2/MLGraphTest.Pool2dTest/All.Xnnpack_Async](https://ci.chromium.org/ui/test/chromium/ninja:%2F%2Fthird_party%2Fblink%2Frenderer%2Fcontroller:blink_unittests_v2%2FMLGraphTest.Pool2dTest%2FAll.Xnnpack_Async?q=VHash%3A3f07fa8873a209f3)

If this is a false positive, please report it at http://b.corp.google.com/createIssue?component=1199205&description=Analysis%3A+https%3A%2F%2Fci.chromium.org%2Fui%2Fp%2Fchromium%2Fbisection%2Ftest-analysis%2Fb%2F5164591178842112&format=PLAIN&priority=P3&title=Wrongly+blamed+https%3A%2F%2Fchromium-review.googlesource.com%2Fc%2Fchromium%2Fsrc%2F%2B%2F5220093&type=BUG

Original change's description:
> Roll XNNPACK to HEAD
>
> The TFLite open-source build is broken at the moment, but roll XNNPACK
> forward this week at least.
>
> Bug: 1516943, b:201542766
> Change-Id: I650c4a64dd8d86a2d0797a8d43fe17d9525572e5
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5220093
> Auto-Submit: Robert Ogden <robertogden@chromium.org>
> Reviewed-by: Sophie Chang <sophiechang@chromium.org>
> Commit-Queue: Sophie Chang <sophiechang@chromium.org>
> Commit-Queue: Robert Ogden <robertogden@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1249840}
>

Bug: 1516943, b:201542766
Change-Id: I248e4f3751d17615c9c8183ea487ec8ee5eddf70
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5220801
Commit-Queue: Adem Derinel <derinel@google.com>
Reviewed-by: Adem Derinel <derinel@google.com>
Owners-Override: Adem Derinel <derinel@google.com>
Cr-Commit-Position: refs/heads/main@{#1250076}

[modify] https://crrev.com/8ab8ec6714e86957219cff897a9bb66ebdcea359/third_party/xnnpack/src
[modify] https://crrev.com/8ab8ec6714e86957219cff897a9bb66ebdcea359/DEPS
[modify] https://crrev.com/8ab8ec6714e86957219cff897a9bb66ebdcea359/third_party/xnnpack/README.chromium
[modify] https://crrev.com/8ab8ec6714e86957219cff897a9bb66ebdcea359/third_party/xnnpack/BUILD.gn


### ro...@chromium.org (2024-01-22)

[Empty comment from Monorail migration]

### ni...@intel.com (2024-01-23)

> Thanks for the extra information - ningxin could you take a look and leave a comment if the report in https://crbug.com/chromium/1516943#c26 is the same root cause or a different one?

It looks like the same root cause. It's also `vld1q_f32()` that reads 4 floats a time.

### gi...@appspot.gserviceaccount.com (2024-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c7ef273ccdb8faa2f886ea6616301eebd56fd2b3

commit c7ef273ccdb8faa2f886ea6616301eebd56fd2b3
Author: Ningxin Hu <ningxin.hu@intel.com>
Date: Wed Jan 24 02:51:47 2024

WebNN: Allocate extra bytes for XNNPACK input buffers

XNNPACK may read `XNN_EXTRA_BYTES` number of bytes beyond array bounds.
It may cause an out-of-bounds access issue if the caller fails to
allocate at least this many extra bytes after the tensor data passed to
XNNPACK [1].

This CL fixes this issue by allocating `XNN_EXTRA_BYTES` extra bytes for
input buffers, copying the input tensor data into these newly allocated
buffers and using them for XNNPACK Runtime setup.

[1]:https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/include/xnnpack.h;l=25

Bug: 1516943,1273291
Change-Id: I3ed4b4fc0504a334eb5a6c47fa7affb0ed043aec
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5196857
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: ningxin hu <ningxin.hu@intel.com>
Reviewed-by: Jiewei Qian <qjw@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1251200}

[modify] https://crrev.com/c7ef273ccdb8faa2f886ea6616301eebd56fd2b3/third_party/blink/renderer/modules/ml/DEPS
[modify] https://crrev.com/c7ef273ccdb8faa2f886ea6616301eebd56fd2b3/third_party/blink/renderer/platform/wtf/cross_thread_copier_base.h
[modify] https://crrev.com/c7ef273ccdb8faa2f886ea6616301eebd56fd2b3/third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack.cc
[modify] https://crrev.com/c7ef273ccdb8faa2f886ea6616301eebd56fd2b3/third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack_test.cc
[modify] https://crrev.com/c7ef273ccdb8faa2f886ea6616301eebd56fd2b3/third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack.h


### ro...@chromium.org (2024-01-24)

should we try to roll xnnpack to HEAD again now? Not sure if there are any upstream changes that also need to be made

### aj...@chromium.org (2024-01-24)

If the CL in https://crbug.com/chromium/1516943#c31 prevents this security issue then we should mark this issue as Fixed.

### ni...@intel.com (2024-01-25)

> If the CL in https://crbug.com/chromium/1516943#c31 prevents this security issue then we should mark this issue as Fixed.

Sure. I would appreciate if someone can help verify this fix on Mac.

### [Deleted User] (2024-01-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3ba6ea2891b2ffc90401177885ba3714bddd0f0e

commit 3ba6ea2891b2ffc90401177885ba3714bddd0f0e
Author: Robert Ogden <robertogden@chromium.org>
Date: Thu Jan 25 18:37:30 2024

Roll XNNPACK to HEAD

The TFLite open-source build is still broken, but roll XNNPACK
forward this week at least.

Bug: 1516943, b:201542766
Change-Id: Ieb0607e09de68a91485ca8cf51e66ed81c2d9efa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5236195
Commit-Queue: Sophie Chang <sophiechang@chromium.org>
Reviewed-by: Sophie Chang <sophiechang@chromium.org>
Auto-Submit: Robert Ogden <robertogden@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1252219}

[modify] https://crrev.com/3ba6ea2891b2ffc90401177885ba3714bddd0f0e/third_party/xnnpack/src
[modify] https://crrev.com/3ba6ea2891b2ffc90401177885ba3714bddd0f0e/DEPS
[modify] https://crrev.com/3ba6ea2891b2ffc90401177885ba3714bddd0f0e/third_party/xnnpack/README.chromium
[modify] https://crrev.com/3ba6ea2891b2ffc90401177885ba3714bddd0f0e/third_party/xnnpack/BUILD.gn


### [Deleted User] (2024-01-25)

[Empty comment from Monorail migration]

### re...@chromium.org (2024-01-25)

I can confirm that this issue is no longer reproducible on 123.0.6264.0.

### zh...@gmail.com (2024-01-27)

After several days of trying, I couldn't find any other way to reproduce use-after-poison and heap-buffer-overflow. So I think at least judging from the current code, there is no problem.

### am...@google.com (2024-02-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-02)

Congratulations @zh1x1an1221! The Chrome VRP Panel has decided to award you $10,000 for this high quality report of memory corruptions in the renderer / sandboxed process + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### zh...@gmail.com (2024-02-02)

Thanks amy, commemorating my last old issue tracker submitted bug, Cheers🍻

### am...@chromium.org (2024-02-02)

Cheers! 🍻 See you on the other side in the new tracker. 🫡

### am...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1516943?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1516942]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-05-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41489926)*

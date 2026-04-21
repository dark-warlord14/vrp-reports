# Security: Use-After-Free in WebContentsFrameTracker::OnPossibleTargetChange

| Field | Value |
|-------|-------|
| **Issue ID** | [40071686](https://issues.chromium.org/issues/40071686) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media>SurfaceCapture |
| **Platforms** | Mac |
| **Reporter** | pw...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2023-09-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-After-Free in WebContentsFrameTracker::OnPossibleTargetChange when close browser

==18939==ERROR: AddressSanitizer: heap-use-after-free on address 0x6100003f5740 at pc 0x000101d212e0 bp 0x00016fdfbd50 sp 0x00016fdfbd48  

READ of size 1 at 0x6100003f5740 thread T0  

==18939==WARNING: invalid path to external symbolizer!  

==18939==WARNING: Failed to use and restart external symbolizer!  

#0 0x101d212dc in base::internal::(anonymous namespace)::CrashImmediatelyOnUseAfterFree(unsigned long)+0x114 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x7d2dc)  

#1 0x101d20e10 in base::internal::(anonymous namespace)::SafelyUnwrapForDereference(unsigned long)+0x6c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x7ce10)  

#2 0x10f2e82dc in content::WebContentsFrameTracker::OnPossibleTargetChange()+0x32c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x2ac82dc)  

#3 0x10efc819c in void content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::\*)()>(void (content::WebContentsObserver::\*)())+0x4b4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x27a819c)  

#4 0x10efc595c in content::WebContentsImpl::~WebContentsImpl()+0xb4c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x27a595c)  

#5 0x10efc8768 in content::WebContentsImpl::~WebContentsImpl()+0x8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x27a8768)  

#6 0x11eeca7a4 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications\*)+0x744 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7f327a4)  

#7 0x11eed36d8 in TabStripModel::CloseTabs(base::span<content::WebContents\* const, 18446744073709551615ul>, unsigned int)+0xba8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7f3b6d8)  

#8 0x11eed2794 in TabStripModel::CloseAllTabs()+0x3a0 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7f3a794)  

#9 0x11ef3dc38 in UnloadController::ProcessPendingTabs(bool)+0x620 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7fa5c38)  

#10 0x11ef3c258 in UnloadController::ClearUnloadState(content::WebContents\*, bool)+0x16c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7fa4258)  

#11 0x11ef3bf98 in UnloadController::CanCloseContents(content::WebContents\*)+0x5c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7fa3f98)  

#12 0x11ecef8e8 in non-virtual thunk to Browser::CloseContents(content::WebContents\*)+0x18 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7d578e8)  

#13 0x10f048f84 in content::WebContentsImpl::Close()+0x1a4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x2828f84)  

#14 0x10e9c9aec in void base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::\*)(content::RenderFrameHostImpl::ClosePageSource), base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);), content::RenderFrameHostImpl::ClosePageSource>, void ()>::RunImpl<void (content::RenderFrameHostImpl::\*)(content::RenderFrameHostImpl::ClosePageSource), std::\_\_Cr::tuple<base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);), content::RenderFrameHostImpl::ClosePageSource>, 0ul, 1ul>(void (content::RenderFrameHostImpl::\*&&)(content::RenderFrameHostImpl::ClosePageSource), std::\_\_Cr::tuple<base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);), content::RenderFrameHostImpl::ClosePageSource>&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul, 1ul>)+0x1a0 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x21a9aec)  

#15 0x132ba957c in blink::mojom::LocalMainFrame\_ClosePage\_ForwardToCallback::Accept(mojo::Message\*)+0x12c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libblink\_common.dylib:arm64+0x58557c)  

#16 0x1019c6aa8 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*)+0xae4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libmojo\_public\_cpp\_bindings.dylib:arm64+0x22aa8)  

#17 0x1019db884 in mojo::MessageDispatcher::Accept(mojo::Message\*)+0x370 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libmojo\_public\_cpp\_bindings.dylib:arm64+0x37884)  

#18 0x1019cb200 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*)+0x158 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libmojo\_public\_cpp\_bindings.dylib:arm64+0x27200)  

#19 0x10358fe94 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message)+0x374 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libipc.dylib:arm64+0x3fe94)  

#20 0x103587a20 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*)+0x16c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libipc.dylib:arm64+0x37a20)  

#21 0x101e69ff8 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x398 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x1c5ff8)  

#22 0x101ec9c50 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*)+0x8a4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x225c50)  

#23 0x101ec8fc8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x154 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x224fc8)  

#24 0x102032514 in base::MessagePumpCFRunLoopBase::RunWork()+0x1f8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x38e514)  

#25 0x10201eef0 in base::apple::CallWithEHFrame(void () block\_pointer)+0xc (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x37aef0)  

#26 0x102030328 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*)+0x13c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x38c328)  

#27 0x19c76e638 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7f638)  

#28 0x733280019c76e5cc (<unknown module>)  

#29 0x5e6780019c76e33c (<unknown module>)  

#30 0x685c80019c76cf44 (<unknown module>)  

#31 0x841000019c76c4b4 (<unknown module>)  

#32 0xbf368001a5fbedec (<unknown module>)  

#33 0xd71d8001a5fbea7c (<unknown module>)  

#34 0xba040001a5fbe980 (<unknown module>)  

#35 0x622a00019f993978 (<unknown module>)  

#36 0xe03700019f992b14 (<unknown module>)  

#37 0xda7400011979e11c (<unknown module>)  

#38 0x10201eef0 in base::apple::CallWithEHFrame(void () block\_pointer)+0xc (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x37aef0)  

#39 0x11979dc9c in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]+0x2b8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x2805c9c)  

#40 0x19f986f78 in -[NSApplication run]+0x1cc (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64+0x2cf78)  

#41 0xb101800102034914 (<unknown module>)  

#42 0x10202ee20 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*)+0x2a4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x38ae20)  

#43 0x101ecba50 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x36c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x227a50)  

#44 0x101de8ad4 in base::RunLoop::Run(base::Location const&)+0x4cc (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x144ad4)  

#45 0x10d67d8d4 in content::BrowserMainLoop::RunMainMessageLoop()+0x264 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0xe5d8d4)  

#46 0x10d6841d0 in content::BrowserMainRunnerImpl::Run()+0x30 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0xe641d0)  

#47 0x10d67640c in content::BrowserMain(content::MainFunctionParams)+0x1c8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0xe5640c)  

#48 0x10feb7678 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*)+0x210 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x3697678)  

#49 0x10feba3e4 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool)+0x3a4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x369a3e4)  

#50 0x10feb9d34 in content::ContentMainRunnerImpl::Run()+0x624 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x3699d34)  

#51 0x10feb4f54 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*)+0x6a4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x3694f54)  

#52 0x10feb5ba0 in content::ContentMain(content::ContentMainParams)+0x1cc (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x3695ba0)  

#53 0x116fa255c in ChromeMain+0x34c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0xa55c)  

#54 0x100000bb4 in main+0x22c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/Chromium.app/Contents/MacOS/Chromium:arm64+0x100000bb4)  

#55 0x19c337f24 (<unknown module>)  

#56 0x58507ffffffffffc (<unknown module>)

0x6100003f5740 is located 0 bytes inside of 184-byte region [0x6100003f5740,0x6100003f57f8)  

freed by thread T0 here:  

#0 0x100826a70 in \_\_sanitizer\_finish\_switch\_fiber+0xb4c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/Chromium.app/Contents/MacOS/libclang\_rt.asan\_osx\_dynamic.dylib:arm64+0x5ea70)  

#1 0x10f2df938 in void content::BrowserThread::DeleteOnThread<(content::BrowserThread::ID)0>::Destruct[content::MouseCursorOverlayController](javascript:void(0);)(content::MouseCursorOverlayController const\*)+0xd4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x2abf938)  

#2 0x10f2d8e20 in content::FrameSinkVideoCaptureDevice::~FrameSinkVideoCaptureDevice()+0x154 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x2ab8e20)  

#3 0x10f2ed034 in content::WebContentsVideoCaptureDevice::~WebContentsVideoCaptureDevice()+0x64 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x2acd034)  

#4 0x10e69db54 in (anonymous namespace)::StopAndReleaseDeviceOnDeviceThread(media::VideoCaptureDevice\*, base::OnceCallback<void ()>)+0x134 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x1e7db54)  

#5 0x10e6a0b84 in base::internal::Invoker<base::internal::BindState<void (\*)(media::VideoCaptureDevice\*, base::OnceCallback<void ()>), base::internal::UnretainedWrapper<media::VideoCaptureDevice, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, base::internal::DoNothingCallbackTag::WithBoundArguments<scoped\_refptr[base::SingleThreadTaskRunner](javascript:void(0);)>>, void ()>::RunOnce(base::internal::BindStateBase\*)+0x1e0 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x1e80b84)  

#6 0x101e69ff8 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x398 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x1c5ff8)  

#7 0x101ec9c50 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*)+0x8a4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x225c50)  

#8 0x101ec8fc8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x154 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x224fc8)  

#9 0x102032514 in base::MessagePumpCFRunLoopBase::RunWork()+0x1f8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x38e514)  

#10 0x10201eef0 in base::apple::CallWithEHFrame(void () block\_pointer)+0xc (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x37aef0)  

#11 0x102030328 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*)+0x13c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x38c328)  

#12 0x19c76e638 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7f638)  

#13 0x733280019c76e5cc (<unknown module>)  

#14 0x5e6780019c76e33c (<unknown module>)  

#15 0x685c80019c76cf44 (<unknown module>)  

#16 0x841000019c76c4b4 (<unknown module>)  

#17 0xbf368001a5fbedec (<unknown module>)  

#18 0xd71d8001a5fbea7c (<unknown module>)  

#19 0xba040001a5fbe980 (<unknown module>)  

#20 0x622a00019f993978 (<unknown module>)  

#21 0xe03700019f992b14 (<unknown module>)  

#22 0xda7400011979e11c (<unknown module>)  

#23 0x10201eef0 in base::apple::CallWithEHFrame(void () block\_pointer)+0xc (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x37aef0)  

#24 0x11979dc9c in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]+0x2b8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x2805c9c)  

#25 0x19f986f78 in -[NSApplication run]+0x1cc (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64+0x2cf78)  

#26 0xb101800102034914 (<unknown module>)  

#27 0x10202ee20 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*)+0x2a4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x38ae20)  

#28 0x101ecba50 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x36c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x227a50)  

#29 0x101de8ad4 in base::RunLoop::Run(base::Location const&)+0x4cc (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x144ad4)

previously allocated by thread T0 here:  

#0 0x100826650 in \_\_sanitizer\_finish\_switch\_fiber+0x72c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/Chromium.app/Contents/MacOS/libclang\_rt.asan\_osx\_dynamic.dylib:arm64+0x5e650)  

#1 0x10f2d8a64 in content::FrameSinkVideoCaptureDevice::FrameSinkVideoCaptureDevice()+0xf0 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x2ab8a64)  

#2 0x10f2ebc08 in content::WebContentsVideoCaptureDevice::WebContentsVideoCaptureDevice(content::GlobalRenderFrameHostId const&)+0x134 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x2acbc08)  

#3 0x10f2ed21c in content::WebContentsVideoCaptureDevice::Create(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&)+0x138 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x2acd21c)  

#4 0x10e6a88c8 in content::InProcessVideoCaptureDeviceLauncher::DoStartTabCaptureOnDeviceThread(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, media::VideoCaptureParams const&, std::\_\_Cr::unique\_ptr<media::VideoFrameReceiver, std::\_\_Cr::default\_delete[media::VideoFrameReceiver](javascript:void(0);)>, base::OnceCallback<void (std::\_\_Cr::unique\_ptr<media::VideoCaptureDevice, std::\_\_Cr::default\_delete[media::VideoCaptureDevice](javascript:void(0);)>)>)+0x10c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x1e888c8)  

#5 0x10e6ac83c in base::internal::Invoker<base::internal::BindState<void (content::InProcessVideoCaptureDeviceLauncher::\*)(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, media::VideoCaptureParams const&, std::\_\_Cr::unique\_ptr<media::VideoFrameReceiver, std::\_\_Cr::default\_delete[media::VideoFrameReceiver](javascript:void(0);)>, base::OnceCallback<void (std::\_\_Cr::unique\_ptr<media::VideoCaptureDevice, std::\_\_Cr::default\_delete[media::VideoCaptureDevice](javascript:void(0);)>)>), base::internal::UnretainedWrapper<content::InProcessVideoCaptureDeviceLauncher, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, media::VideoCaptureParams, std::\_\_Cr::unique\_ptr<media::VideoFrameReceiverOnTaskRunner, std::\_\_Cr::default\_delete[media::VideoFrameReceiverOnTaskRunner](javascript:void(0);)>, base::OnceCallback<void (std::\_\_Cr::unique\_ptr<media::VideoCaptureDevice, std::\_\_Cr::default\_delete[media::VideoCaptureDevice](javascript:void(0);)>)>>, void ()>::RunOnce(base::internal::BindStateBase\*)+0x208 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x1e8c83c)  

#6 0x101e69ff8 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x398 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x1c5ff8)  

#7 0x101ec9c50 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*)+0x8a4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x225c50)  

#8 0x101ec8fc8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x154 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x224fc8)  

#9 0x102032514 in base::MessagePumpCFRunLoopBase::RunWork()+0x1f8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x38e514)  

#10 0x10201eef0 in base::apple::CallWithEHFrame(void () block\_pointer)+0xc (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x37aef0)  

#11 0x102030134 in base::MessagePumpCFRunLoopBase::RunDelayedWorkTimer(\_\_CFRunLoopTimer\*, void\*)+0x13c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x38c134)  

#12 0x19c7883c4 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_TIMER\_CALLBACK\_FUNCTION**+0x1c (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x993c4)  

#13 0x1e5680019c78806c (<unknown module>)  

#14 0x942580019c787bc4 (<unknown module>)  

#15 0xe72a80019c76d344 (<unknown module>)  

#16 0x841000019c76c4b4 (<unknown module>)  

#17 0xbf368001a5fbedec (<unknown module>)  

#18 0x221b8001a5fbec28 (<unknown module>)  

#19 0xba040001a5fbe980 (<unknown module>)  

#20 0x622a00019f993978 (<unknown module>)  

#21 0xe03700019f992b14 (<unknown module>)  

#22 0xda7400011979e11c (<unknown module>)  

#23 0x10201eef0 in base::apple::CallWithEHFrame(void () block\_pointer)+0xc (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x37aef0)  

#24 0x11979dc9c in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]+0x2b8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x2805c9c)  

#25 0x19f986f78 in -[NSApplication run]+0x1cc (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64+0x2cf78)  

#26 0xb101800102034914 (<unknown module>)  

#27 0x10202ee20 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*)+0x2a4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x38ae20)  

#28 0x101ecba50 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x36c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x227a50)  

#29 0x101de8ad4 in base::RunLoop::Run(base::Location const&)+0x4cc (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x144ad4)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x7d2dc) in base::internal::(anonymous namespace)::CrashImmediatelyOnUseAfterFree(unsigned long)+0x114  

Shadow bytes around the buggy address:  

0x6100003f5480: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x6100003f5500: fa fa fa fa fa fa f7 fa 00 00 00 00 00 00 00 00  

0x6100003f5580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x6100003f5600: fa fa fa fa fa fa f7 fa fa fa fa fa fa fa fa fa  

0x6100003f5680: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x6100003f5700: fa fa fa fa fa fa f7 fa[fd]fd fd fd fd fd fd fd  

0x6100003f5780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x6100003f5800: fa fa fa fa fa fa f7 fa fa fa fa fa fa fa fa fa  

0x6100003f5880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x6100003f5900: fa fa fa fa fa fa f7 fa fa fa fa fa fa fa fa fa  

0x6100003f5980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb

**VERSION**  

Chrome Version: Browser::TryToCloseWindow  

Operating System: MacOS 13.4.1 (c) (22F770820d)

**REPRODUCTION CASE**

1. Launch Chrome
2. navigator.mediaDevices.getDisplayMedia() many time
3. Close browser

Reproducing it exactly is difficult, but it seems like there was a crash when attempting to screen share with multiple tabs that were cross-referencing each other.

**CREDIT INFORMATION**  

Reporter credit: [pwn2car]

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 21.3 KB)

## Timeline

### [Deleted User] (2023-09-07)

[Empty comment from Monorail migration]

### ke...@chromium.org (2023-09-07)

Thanks for the report. We'll see if we can do anything with the ASAN report.

I'm setting severity to Medium based on it being an unusual scenario and also the UAF is mitigated by raw_ptr.

jophba@: Are you able to have a look at this, or pass it on to someone else who might?

This is during WebContents destruction, it is calling WebContentsFrameTracker::OnPossibleTargetChange(), and hitting a UAF.

[Monorail components: Internals>Media>SurfaceCapture]

### jo...@chromium.org (2023-09-11)

I'll take a look. Thanks for the report!

### jo...@chromium.org (2023-09-11)

[Comment Deleted]

### ad...@google.com (2023-09-25)

jophba@ thanks for agreeing to take a look here. Do you have any theories yet? In particular, it would be good to know if you think this might be a recent regression, or if this code has been unchanged for a while.

### jo...@google.com (2023-09-26)

So fundamentally the problem in this stack is that the MouseCursorOverlayController has been deleted on the UI thread already before this observer method gets called. I think this is only possible because we call into the mouse cursor overlay controller synchronously because the gfx::NativeView pointer may be invalid on Mac OSX if we post back to the UI thread.

So, ironically, the desire to avoid a use-after-free is why we have a use-after-free. I've been pondering a fix and am hoping to get it resolved this week.

### jo...@google.com (2023-09-26)

And it doesn't look like a recent regression + the UaF is caught by RawPtr so I don't think this is a huge problem. Regardless I want to close this out ASAP and clear out my bug backlog.

### jo...@google.com (2023-09-26)

This doesn't look like a new problem, and was likely introduced when we fixed the use-after-free on Mac OSX.

### ad...@google.com (2023-09-27)

Thanks muchly, that enables me to label the bug to indicate it's not a regression, which will keep our automation happy.

### [Deleted User] (2023-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-27)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/250c8f3d44964a307ccfb059cb710dd972399aa5

commit 250c8f3d44964a307ccfb059cb710dd972399aa5
Author: Jordan Bayles <jophba@chromium.org>
Date: Fri Oct 06 23:50:59 2023

Fix UaF in WebContentsFrameTracker

This patch fixes a use-after-free by moving to a base::WeakPtr
instead of a raw_ptr. Looking at the callstack in the referenced bug, what is clearly happening is that the frame tracker is deleted AFTER the capture device. I believe that this is due to the MouseCursorOverlayController being deleted through the DeleteOnUIThread destructor, which, if you are already on the UI thread, is synchronous:

https://source.chromium.org/chromium/chromium/src/+/main:content/public/browser/browser_thread.h;l=141?q=BrowserThread::DeleteOnThread&ss=chromium%2Fchromium%2Fsrc

In comparison, the WebContentsFrameTracker is implemented using base::SequenceBound, which ends up calling an internal destruct method that ALWAYS posts back a task:

https://source.chromium.org/chromium/chromium/src/+/main:base/threading/sequence_bound_internal.h;drc=f5bdc89c7395ed24f1b8d196a3bdd6232d5bf771;l=122

So, this bug is ultimately caused by the simple fact that base::SequenceBound does NOT have an optimization to not post a deletion task if we are already running on that sequence. There may be a good followup task here to change either DeleteOnThread or base::SequenceBound to have the same behavior, however I think this change a good first step.

Bug: 1480152
Change-Id: Iee2d41e66b10403d6c78547bcbe84d2454236d5b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4908770
Reviewed-by: Mark Foltz <mfoltz@chromium.org>
Commit-Queue: Jordan Bayles <jophba@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1206698}

[modify] https://crrev.com/250c8f3d44964a307ccfb059cb710dd972399aa5/content/browser/media/capture/web_contents_frame_tracker.h
[modify] https://crrev.com/250c8f3d44964a307ccfb059cb710dd972399aa5/content/browser/media/capture/web_contents_frame_tracker.cc


### jo...@google.com (2023-10-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-07)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-11)

Congratulations pwn2car! The Chrome VRP Panel has decided to award you $1,000 for this report of a heavily mitigated security bug. The reward amount was decided due to this UAF being BRP/MiraclePtr protected and shutdown. Thank you for your efforts and reporting this issue to us. In the future, we would appreciate it if you could please include the asan stack trace in its entirety and refrain from removing the portion about BRP protection. Thanks again!  

### am...@google.com (2023-10-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-12-06)

[Empty comment from Monorail migration]

### pg...@google.com (2023-12-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-13)

This issue was migrated from crbug.com/chromium/1480152?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071686)*

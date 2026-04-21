# Security: UAF in extensions::OffscreenCreateDocumentFunction::OnExtensionHostDestroyed (browser process)

| Field | Value |
|-------|-------|
| **Issue ID** | [40065191](https://issues.chromium.org/issues/40065191) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2023-06-02 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in extensions::OffscreenCreateDocumentFunction::OnExtensionHostDestroyed in browser process.

**VERSION**  

Chromium 116.0.5807.0 (Developer Build) (arm64)  

Revision 52bc891f506397897ef06192beda312c480e9937-refs/heads/main@{#1152210}  

OS macOS Version 13.3.1 (a) (Build 22E772610a)

**REPRODUCTION CASE**

1. put manifest.json/background.js into the extension\_path
2. run the command:  
   
   ./out/Chromium.app/Contents/MacOS/Chromium --user-data-dir=/tmp --no-first-run --load-extension="extension\_path"

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: [browser]

==81623==ERROR: AddressSanitizer: heap-use-after-free on address 0x6140002d01e0 at pc 0x00011f789e44 bp 0x00016b0bfed0 sp 0x00016b0bfec8  

READ of size 8 at 0x6140002d01e0 thread T0  

==81623==WARNING: invalid path to external symbolizer!  

==81623==WARNING: Failed to use and restart external symbolizer!  

#0 0x11f789e40 in extensions::OffscreenCreateDocumentFunction::OnExtensionHostDestroyed(extensions::ExtensionHost\*)+0x320 (/tmp/libchrome\_dll.dylib:arm64+0x18b9e40) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#1 0x11f35555c in extensions::ExtensionHost::~ExtensionHost()+0x800 (/tmp/libchrome\_dll.dylib:arm64+0x148555c) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#2 0x11f477b1c in extensions::OffscreenDocumentHost::~OffscreenDocumentHost()+0x8 (/tmp/libchrome\_dll.dylib:arm64+0x15a7b1c) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#3 0x11f78c638 in extensions::OffscreenDocumentManager::OffscreenDocumentData::~OffscreenDocumentData()+0x14c (/tmp/libchrome\_dll.dylib:arm64+0x18bc638) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#4 0x11f79030c in std::\_\_Cr::\_\_tree<std::\_\_Cr::\_\_value\_type<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, extensions::OffscreenDocumentManager::OffscreenDocumentData>, std::\_\_Cr::\_\_map\_value\_compare<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, std::\_\_Cr::\_\_value\_type<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, extensions::OffscreenDocumentManager::OffscreenDocumentData>, std::\_\_Cr::less<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>>, true>, std::\_\_Cr::allocator<std::\_\_Cr::\_\_value\_type<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, extensions::OffscreenDocumentManager::OffscreenDocumentData>>>::erase(std::\_\_Cr::\_\_tree\_const\_iterator<std::\_\_Cr::\_\_value\_type<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, extensions::OffscreenDocumentManager::OffscreenDocumentData>, std::\_\_Cr::\_\_tree\_node<std::\_\_Cr::\_\_value\_type<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, extensions::OffscreenDocumentManager::OffscreenDocumentData>, void\*>\*, long>)+0xf8 (/tmp/libchrome\_dll.dylib:arm64+0x18c030c) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#5 0x11f78e470 in extensions::OffscreenDocumentManager::CloseOffscreenDocumentForExtensionId(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&)+0x1e4 (/tmp/libchrome\_dll.dylib:arm64+0x18be470) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#6 0x11f78a9c8 in extensions::OffscreenCloseDocumentFunction::Run()+0x138 (/tmp/libchrome\_dll.dylib:arm64+0x18ba9c8) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#7 0x11f33ff8c in ExtensionFunction::RunWithValidation()+0x1ec (/tmp/libchrome\_dll.dylib:arm64+0x146ff8c) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#8 0x11f34b550 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(extensions::mojom::RequestParams const&, content::RenderFrameHost\*, content::RenderProcessHost&, base::OnceCallback<void (ExtensionFunction::ResponseType, base::Value::List, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, mojo::StructPtr[extensions::mojom::ExtraResponseData](javascript:void(0);))>)+0xc5c (/tmp/libchrome\_dll.dylib:arm64+0x147b550) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#9 0x11f34cc14 in extensions::ExtensionFunctionDispatcher::DispatchForServiceWorker(mojo::StructPtr[extensions::mojom::RequestParams](javascript:void(0);), int)+0x8b8 (/tmp/libchrome\_dll.dylib:arm64+0x147cc14) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#10 0x11f4dcab8 in extensions::ServiceWorkerHost::RequestWorker(mojo::StructPtr[extensions::mojom::RequestParams](javascript:void(0);))+0x1b0 (/tmp/libchrome\_dll.dylib:arm64+0x160cab8) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#11 0x11e30de20 in extensions::mojom::ServiceWorkerHostStubDispatch::Accept(extensions::mojom::ServiceWorkerHost\*, mojo::Message\*)+0x10b0 (/tmp/libchrome\_dll.dylib:arm64+0x43de20) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#12 0x107d58254 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*)+0xb5c (/tmp/libmojo\_public\_cpp\_bindings.dylib:arm64+0x30254) (BuildId: 4c4c44c055553144a1199b67a8a68e3432000000200000000100000000000b00)  

#13 0x107d704a0 in mojo::MessageDispatcher::Accept(mojo::Message\*)+0x2d8 (/tmp/libmojo\_public\_cpp\_bindings.dylib:arm64+0x484a0) (BuildId: 4c4c44c055553144a1199b67a8a68e3432000000200000000100000000000b00)  

#14 0x107d5e354 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*)+0x1c4 (/tmp/libmojo\_public\_cpp\_bindings.dylib:arm64+0x36354) (BuildId: 4c4c44c055553144a1199b67a8a68e3432000000200000000100000000000b00)  

#15 0x10a2f398c in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message)+0x538 (/tmp/libipc.dylib:arm64+0x4b98c) (BuildId: 4c4c448255553144a17901ff895510a832000000200000000100000000000b00)  

#16 0x10a2e9bec in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*)+0x170 (/tmp/libipc.dylib:arm64+0x41bec) (BuildId: 4c4c448255553144a17901ff895510a832000000200000000100000000000b00)  

#17 0x106d8e340 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x3c0 (/tmp/libbase.dylib:arm64+0x1fa340) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#18 0x106e1acf0 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*)+0xb20 (/tmp/libbase.dylib:arm64+0x286cf0) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#19 0x106e1969c in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x1c0 (/tmp/libbase.dylib:arm64+0x28569c) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#20 0x10700cb90 in base::MessagePumpCFRunLoopBase::RunWork()+0x16c (/tmp/libbase.dylib:arm64+0x478b90) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#21 0x106ff4d1c in base::mac::CallWithEHFrame(void () block\_pointer)+0xc (/tmp/libbase.dylib:arm64+0x460d1c) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#22 0x10700a54c in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*)+0x13c (/tmp/libbase.dylib:arm64+0x47654c) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#23 0x1a497670c in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7f70c) (BuildId: b4fdaece97273969b01427f7f24c8e0132000000200000000100000000030d00)  

#24 0x687f0001a49766a0 (<unknown module>)  

#25 0x24288001a4976410 (<unknown module>)  

#26 0x64d8001a4975018 (<unknown module>)  

#27 0xdf650001a4974588 (<unknown module>)  

#28 0x2c0c8001ae1a9df0 (<unknown module>)  

#29 0x48380001ae1a9c2c (<unknown module>)  

#30 0x73578001ae1a9984 (<unknown module>)  

#31 0xa27f8001a7b93f54 (<unknown module>)  

#32 0xe1598001a7b930f0 (<unknown module>)  

#33 0xe3048001212694d0 (<unknown module>)  

#34 0x106ff4d1c in base::mac::CallWithEHFrame(void () block\_pointer)+0xc (/tmp/libbase.dylib:arm64+0x460d1c) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#35 0x121268fb0 in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]+0x2b4 (/tmp/libchrome\_dll.dylib:arm64+0x3398fb0) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#36 0x1a7b87554 in -[NSApplication run]+0x1cc (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64+0x2c554) (BuildId: cc3e52154cd7364c87506eb7002720ce32000000200000000100000000030d00)  

#37 0x232c00010700f63c (<unknown module>)  

#38 0x10700925c in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*)+0x23c (/tmp/libbase.dylib:arm64+0x47525c) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#39 0x106e1d500 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x504 (/tmp/libbase.dylib:arm64+0x289500) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#40 0x106cf05d0 in base::RunLoop::Run(base::Location const&)+0x488 (/tmp/libbase.dylib:arm64+0x15c5d0) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#41 0x11485f6cc in content::BrowserMainLoop::RunMainMessageLoop()+0x1dc (/tmp/libcontent.dylib:arm64+0x13d76cc) (BuildId: 4c4c447e55553144a1c22ccc79ce73ae32000000200000000100000000000b00)  

#42 0x114866340 in content::BrowserMainRunnerImpl::Run()+0x138 (/tmp/libcontent.dylib:arm64+0x13de340) (BuildId: 4c4c447e55553144a1c22ccc79ce73ae32000000200000000100000000000b00)  

#43 0x1148581b4 in content::BrowserMain(content::MainFunctionParams)+0x1c8 (/tmp/libcontent.dylib:arm64+0x13d01b4) (BuildId: 4c4c447e55553144a1c22ccc79ce73ae32000000200000000100000000000b00)  

#44 0x11749eb78 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*)+0x228 (/tmp/libcontent.dylib:arm64+0x4016b78) (BuildId: 4c4c447e55553144a1c22ccc79ce73ae32000000200000000100000000000b00)  

#45 0x1174a1e04 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool)+0x5bc (/tmp/libcontent.dylib:arm64+0x4019e04) (BuildId: 4c4c447e55553144a1c22ccc79ce73ae32000000200000000100000000000b00)  

#46 0x1174a13b8 in content::ContentMainRunnerImpl::Run()+0x6b0 (/tmp/libcontent.dylib:arm64+0x40193b8) (BuildId: 4c4c447e55553144a1c22ccc79ce73ae32000000200000000100000000000b00)  

#47 0x11749cb70 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*)+0x934 (/tmp/libcontent.dylib:arm64+0x4014b70) (BuildId: 4c4c447e55553144a1c22ccc79ce73ae32000000200000000100000000000b00)  

#48 0x11749d1c4 in content::ContentMain(content::ContentMainParams)+0x144 (/tmp/libcontent.dylib:arm64+0x40151c4) (BuildId: 4c4c447e55553144a1c22ccc79ce73ae32000000200000000100000000000b00)  

#49 0x11deda714 in ChromeMain+0x420 (/tmp/libchrome\_dll.dylib:arm64+0xa714) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#50 0x104d3cbb4 in main+0x22c (/tmp/Chromium.app/Contents/MacOS/Chromium:arm64+0x100000bb4) (BuildId: 4c4c44d155553144a12379ba3d682b0832000000200000000100000000000b00)  

#51 0x1a453ff24 (<unknown module>)  

#52 0x274ffffffffffffc (<unknown module>)

0x6140002d01e0 is located 416 bytes inside of 424-byte region [0x6140002d0040,0x6140002d01e8)  

freed by thread T0 here:  

Chromium Helper (Renderer)(81641,0x1ffd05b40) malloc: nano zone abandoned due to inability to reserve vm space.  

#0 0x1054d6a2c in \_\_sanitizer\_finish\_switch\_fiber+0xb68 (/tmp/Chromium.app/Contents/MacOS/libclang\_rt.asan\_osx\_dynamic.dylib:arm64+0x5ea2c) (BuildId: 4c4c443e55553144a1400716444dd55532000000200000000100000000000b00)  

#1 0x11f789ff0 in extensions::OffscreenCreateDocumentFunction::SendResponseToExtension(ExtensionFunction::ResponseValue)+0x19c (/tmp/libchrome\_dll.dylib:arm64+0x18b9ff0) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#2 0x11f789ca4 in extensions::OffscreenCreateDocumentFunction::OnExtensionHostDestroyed(extensions::ExtensionHost\*)+0x184 (/tmp/libchrome\_dll.dylib:arm64+0x18b9ca4) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#3 0x11f35555c in extensions::ExtensionHost::~ExtensionHost()+0x800 (/tmp/libchrome\_dll.dylib:arm64+0x148555c) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#4 0x11f477b1c in extensions::OffscreenDocumentHost::~OffscreenDocumentHost()+0x8 (/tmp/libchrome\_dll.dylib:arm64+0x15a7b1c) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#5 0x11f78c638 in extensions::OffscreenDocumentManager::OffscreenDocumentData::~OffscreenDocumentData()+0x14c (/tmp/libchrome\_dll.dylib:arm64+0x18bc638) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#6 0x11f79030c in std::\_\_Cr::\_\_tree<std::\_\_Cr::\_\_value\_type<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, extensions::OffscreenDocumentManager::OffscreenDocumentData>, std::\_\_Cr::\_\_map\_value\_compare<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, std::\_\_Cr::\_\_value\_type<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, extensions::OffscreenDocumentManager::OffscreenDocumentData>, std::\_\_Cr::less<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>>, true>, std::\_\_Cr::allocator<std::\_\_Cr::\_\_value\_type<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, extensions::OffscreenDocumentManager::OffscreenDocumentData>>>::erase(std::\_\_Cr::\_\_tree\_const\_iterator<std::\_\_Cr::\_\_value\_type<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, extensions::OffscreenDocumentManager::OffscreenDocumentData>, std::\_\_Cr::\_\_tree\_node<std::\_\_Cr::\_\_value\_type<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, extensions::OffscreenDocumentManager::OffscreenDocumentData>, void\*>\*, long>)+0xf8 (/tmp/libchrome\_dll.dylib:arm64+0x18c030c) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#7 0x11f78e470 in extensions::OffscreenDocumentManager::CloseOffscreenDocumentForExtensionId(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&)+0x1e4 (/tmp/libchrome\_dll.dylib:arm64+0x18be470) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#8 0x11f78a9c8 in extensions::OffscreenCloseDocumentFunction::Run()+0x138 (/tmp/libchrome\_dll.dylib:arm64+0x18ba9c8) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#9 0x11f33ff8c in ExtensionFunction::RunWithValidation()+0x1ec (/tmp/libchrome\_dll.dylib:arm64+0x146ff8c) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#10 0x11f34b550 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(extensions::mojom::RequestParams const&, content::RenderFrameHost\*, content::RenderProcessHost&, base::OnceCallback<void (ExtensionFunction::ResponseType, base::Value::List, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, mojo::StructPtr[extensions::mojom::ExtraResponseData](javascript:void(0);))>)+0xc5c (/tmp/libchrome\_dll.dylib:arm64+0x147b550) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#11 0x11f34cc14 in extensions::ExtensionFunctionDispatcher::DispatchForServiceWorker(mojo::StructPtr[extensions::mojom::RequestParams](javascript:void(0);), int)+0x8b8 (/tmp/libchrome\_dll.dylib:arm64+0x147cc14) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#12 0x11f4dcab8 in extensions::ServiceWorkerHost::RequestWorker(mojo::StructPtr[extensions::mojom::RequestParams](javascript:void(0);))+0x1b0 (/tmp/libchrome\_dll.dylib:arm64+0x160cab8) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#13 0x11e30de20 in extensions::mojom::ServiceWorkerHostStubDispatch::Accept(extensions::mojom::ServiceWorkerHost\*, mojo::Message\*)+0x10b0 (/tmp/libchrome\_dll.dylib:arm64+0x43de20) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#14 0x107d58254 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*)+0xb5c (/tmp/libmojo\_public\_cpp\_bindings.dylib:arm64+0x30254) (BuildId: 4c4c44c055553144a1199b67a8a68e3432000000200000000100000000000b00)  

#15 0x107d704a0 in mojo::MessageDispatcher::Accept(mojo::Message\*)+0x2d8 (/tmp/libmojo\_public\_cpp\_bindings.dylib:arm64+0x484a0) (BuildId: 4c4c44c055553144a1199b67a8a68e3432000000200000000100000000000b00)  

#16 0x107d5e354 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*)+0x1c4 (/tmp/libmojo\_public\_cpp\_bindings.dylib:arm64+0x36354) (BuildId: 4c4c44c055553144a1199b67a8a68e3432000000200000000100000000000b00)  

#17 0x10a2f398c in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message)+0x538 (/tmp/libipc.dylib:arm64+0x4b98c) (BuildId: 4c4c448255553144a17901ff895510a832000000200000000100000000000b00)  

#18 0x10a2e9bec in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*)+0x170 (/tmp/libipc.dylib:arm64+0x41bec) (BuildId: 4c4c448255553144a17901ff895510a832000000200000000100000000000b00)  

#19 0x106d8e340 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x3c0 (/tmp/libbase.dylib:arm64+0x1fa340) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#20 0x106e1acf0 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*)+0xb20 (/tmp/libbase.dylib:arm64+0x286cf0) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#21 0x106e1969c in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x1c0 (/tmp/libbase.dylib:arm64+0x28569c) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#22 0x10700cb90 in base::MessagePumpCFRunLoopBase::RunWork()+0x16c (/tmp/libbase.dylib:arm64+0x478b90) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#23 0x106ff4d1c in base::mac::CallWithEHFrame(void () block\_pointer)+0xc (/tmp/libbase.dylib:arm64+0x460d1c) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#24 0x10700a54c in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*)+0x13c (/tmp/libbase.dylib:arm64+0x47654c) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#25 0x1a497670c in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7f70c) (BuildId: b4fdaece97273969b01427f7f24c8e0132000000200000000100000000030d00)  

#26 0x687f0001a49766a0 (<unknown module>)  

#27 0x24288001a4976410 (<unknown module>)  

#28 0x64d8001a4975018 (<unknown module>)  

#29 0xdf650001a4974588 (<unknown module>)

previously allocated by thread T0 here:  

#0 0x1054d660c in \_\_sanitizer\_finish\_switch\_fiber+0x748 (/tmp/Chromium.app/Contents/MacOS/libclang\_rt.asan\_osx\_dynamic.dylib:arm64+0x5e60c) (BuildId: 4c4c443e55553144a1400716444dd55532000000200000000100000000000b00)  

#1 0x12484c8d4 in scoped\_refptr<ExtensionFunction> NewExtensionFunction[extensions::OffscreenCreateDocumentFunction](javascript:void(0);)()+0xe4 (/tmp/libchrome\_dll.dylib:arm64+0x697c8d4) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#2 0x11f353a54 in ExtensionFunctionRegistry::NewFunction(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&)+0x178 (/tmp/libchrome\_dll.dylib:arm64+0x1483a54) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#3 0x11f34df58 in extensions::ExtensionFunctionDispatcher::CreateExtensionFunction(extensions::mojom::RequestParams const&, extensions::Extension const\*, int, bool, GURL const\*, extensions::Feature::Context, extensions::ExtensionAPI\*, base::OnceCallback<void (ExtensionFunction::ResponseType, base::Value::List, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, mojo::StructPtr[extensions::mojom::ExtraResponseData](javascript:void(0);))>, content::RenderFrameHost\*)+0x264 (/tmp/libchrome\_dll.dylib:arm64+0x147df58) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#4 0x11f34aea0 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(extensions::mojom::RequestParams const&, content::RenderFrameHost\*, content::RenderProcessHost&, base::OnceCallback<void (ExtensionFunction::ResponseType, base::Value::List, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, mojo::StructPtr[extensions::mojom::ExtraResponseData](javascript:void(0);))>)+0x5ac (/tmp/libchrome\_dll.dylib:arm64+0x147aea0) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#5 0x11f34cc14 in extensions::ExtensionFunctionDispatcher::DispatchForServiceWorker(mojo::StructPtr[extensions::mojom::RequestParams](javascript:void(0);), int)+0x8b8 (/tmp/libchrome\_dll.dylib:arm64+0x147cc14) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#6 0x11f4dcab8 in extensions::ServiceWorkerHost::RequestWorker(mojo::StructPtr[extensions::mojom::RequestParams](javascript:void(0);))+0x1b0 (/tmp/libchrome\_dll.dylib:arm64+0x160cab8) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#7 0x11e30de20 in extensions::mojom::ServiceWorkerHostStubDispatch::Accept(extensions::mojom::ServiceWorkerHost\*, mojo::Message\*)+0x10b0 (/tmp/libchrome\_dll.dylib:arm64+0x43de20) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00)  

#8 0x107d58254 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*)+0xb5c (/tmp/libmojo\_public\_cpp\_bindings.dylib:arm64+0x30254) (BuildId: 4c4c44c055553144a1199b67a8a68e3432000000200000000100000000000b00)  

#9 0x107d704a0 in mojo::MessageDispatcher::Accept(mojo::Message\*)+0x2d8 (/tmp/libmojo\_public\_cpp\_bindings.dylib:arm64+0x484a0) (BuildId: 4c4c44c055553144a1199b67a8a68e3432000000200000000100000000000b00)  

#10 0x107d5e354 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*)+0x1c4 (/tmp/libmojo\_public\_cpp\_bindings.dylib:arm64+0x36354) (BuildId: 4c4c44c055553144a1199b67a8a68e3432000000200000000100000000000b00)  

#11 0x10a2f398c in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message)+0x538 (/tmp/libipc.dylib:arm64+0x4b98c) (BuildId: 4c4c448255553144a17901ff895510a832000000200000000100000000000b00)  

#12 0x10a2e9bec in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*)+0x170 (/tmp/libipc.dylib:arm64+0x41bec) (BuildId: 4c4c448255553144a17901ff895510a832000000200000000100000000000b00)  

#13 0x106d8e340 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x3c0 (/tmp/libbase.dylib:arm64+0x1fa340) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#14 0x106e1acf0 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*)+0xb20 (/tmp/libbase.dylib:arm64+0x286cf0) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#15 0x106e1969c in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x1c0 (/tmp/libbase.dylib:arm64+0x28569c) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#16 0x10700cb90 in base::MessagePumpCFRunLoopBase::RunWork()+0x16c (/tmp/libbase.dylib:arm64+0x478b90) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#17 0x106ff4d1c in base::mac::CallWithEHFrame(void () block\_pointer)+0xc (/tmp/libbase.dylib:arm64+0x460d1c) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#18 0x10700a54c in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*)+0x13c (/tmp/libbase.dylib:arm64+0x47654c) (BuildId: 4c4c44df55553144a182eaadbe21d29b32000000200000000100000000000b00)  

#19 0x1a497670c in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7f70c) (BuildId: b4fdaece97273969b01427f7f24c8e0132000000200000000100000000030d00)  

#20 0x687f0001a49766a0 (<unknown module>)  

#21 0x24288001a4976410 (<unknown module>)  

#22 0x64d8001a4975018 (<unknown module>)  

#23 0xdf650001a4974588 (<unknown module>)  

#24 0x2c0c8001ae1a9df0 (<unknown module>)  

#25 0x48380001ae1a9c2c (<unknown module>)  

#26 0x73578001ae1a9984 (<unknown module>)  

#27 0xa27f8001a7b93f54 (<unknown module>)  

#28 0xe1598001a7b930f0 (<unknown module>)  

#29 0xe3048001212694d0 (<unknown module>)

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/libchrome\_dll.dylib:arm64+0x18b9e40) (BuildId: 4c4c449c55553144a17822fc39cc2ae332000000200000000100000000000b00) in extensions::OffscreenCreateDocumentFunction::OnExtensionHostDestroyed(extensions::ExtensionHost\*)+0x320  

Shadow bytes around the buggy address:  

0x6140002cff00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x6140002cff80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x6140002d0000: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x6140002d0080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x6140002d0100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x6140002d0180: fd fd fd fd fd fd fd fd fd fd fd fd[fd]fa fa fa  

0x6140002d0200: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x6140002d0280: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x6140002d0300: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x6140002d0380: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x6140002d0400: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

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

==81623==ADDITIONAL INFO

==81623==Note: Please include this section with the ASan report.  

Task trace:  

#0 0x10a2e7760 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::Accept(mojo::Message\*)+0xcd4 (/tmp/libipc.dylib:arm64+0x3f760) (BuildId: 4c4c448255553144a17901ff895510a832000000200000000100000000000b00)  

#1 0x1065cb190 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x320 (/tmp/libmojo\_public\_system\_cpp.dylib:arm64+0x1f190) (BuildId: 4c4c442955553144a108fbe29d1b073d32000000200000000100000000000b00)

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 232 B)
- [background.js](attachments/background.js) (text/plain, 146 B)

## Timeline

### [Deleted User] (2023-06-02)

[Empty comment from Monorail migration]

### ca...@chromium.org (2023-06-02)

Im able to reproduce this in current stable on Linux.

Devlin: Passing this to you since I see you in the git history for the relevant file, but feel free to reassign as appropriate. Thanks

[Monorail components: Platform>Extensions]

### [Deleted User] (2023-06-02)

[Empty comment from Monorail migration]

### rd...@chromium.org (2023-06-02)

Thanks for the report!  This definitely is a bug (silly mistake on my part).  I'll have a CL up to fix it on Monday.

One thing worth noting: the UAF occurs in a DCHECK, so this shouldn't affect large populations of stable users.  (But very obviously, still something we have to fix!)

### [Deleted User] (2023-06-03)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-03)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2023-06-05)

WIP CL: https://chromium-review.googlesource.com/c/chromium/src/+/4590681

I'm also lowering this to medium because:
1) It requires the user to install an extension to exploit it, and
2) It only affects users with DCHECK enabled

Security team, feel free to increase if you think it's appropriate.

### gi...@appspot.gserviceaccount.com (2023-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bb04074866a59716ce7e78ec045f5a11eeab08df

commit bb04074866a59716ce7e78ec045f5a11eeab08df
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Tue Jun 06 20:24:19 2023

[Extensions] Remove bad DCHECK in offscreen API

Bug: 1450784
Change-Id: I84f280200b31cb95a13fe3e14838707decb344a4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4590681
Reviewed-by: Tim <tjudkins@chromium.org>
Commit-Queue: Devlin Cronin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1154035}

[modify] https://crrev.com/bb04074866a59716ce7e78ec045f5a11eeab08df/chrome/browser/extensions/api/offscreen/offscreen_apitest.cc
[modify] https://crrev.com/bb04074866a59716ce7e78ec045f5a11eeab08df/extensions/browser/api/offscreen/offscreen_api.cc


### rd...@chromium.org (2023-06-06)

This should be fixed with c#8.

### [Deleted User] (2023-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-07)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-16)

Congratulations, asnine! The VRP Panel has decided to award you $1,000 for this report of a highly mitigated security bug as this issue requires the installation of an extension and only impacts builds with DCHECK enabled, which is relegated to Canary users. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2023-09-21)

[Empty comment from Monorail migration]

### rz...@google.com (2023-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-22)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-09-22)

1. https://crrev.com/c/4886254
2. Low, only had a simple conflict with the added test
3. 116
4. Yes

### gm...@google.com (2023-09-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b0df6f9322338976a78bdd572c426e8d3eae7e27

commit b0df6f9322338976a78bdd572c426e8d3eae7e27
Author: Zakhar Voit <voit@google.com>
Date: Fri Sep 29 09:06:26 2023

[M114-LTS] [Extensions] Remove bad DCHECK in offscreen API

M114 merge issues:
  Conflicting tests around the added test (A few tests aren't
  present in 114)

(cherry picked from commit bb04074866a59716ce7e78ec045f5a11eeab08df)

Bug: 1450784
Change-Id: I84f280200b31cb95a13fe3e14838707decb344a4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4590681
Commit-Queue: Devlin Cronin <rdevlin.cronin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1154035}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4886254
Owners-Override: Victor Gabriel Savu <vsavu@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Reviewed-by: Victor Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1612}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/b0df6f9322338976a78bdd572c426e8d3eae7e27/chrome/browser/extensions/api/offscreen/offscreen_apitest.cc
[modify] https://crrev.com/b0df6f9322338976a78bdd572c426e8d3eae7e27/extensions/browser/api/offscreen/offscreen_api.cc


### vo...@google.com (2023-09-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1450784?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065191)*

# Security: heap-use-after-free in  TemplateURLRef::ParseHostAndSearchTermKey

| Field | Value |
|-------|-------|
| **Issue ID** | [40058177](https://issues.chromium.org/issues/40058177) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2021-12-09 |
| **Bounty** | $7,000.00 |

## Description

I don’t know if you can reproduce this vulnerability, and I don’t always reproduce it successfully, but when I try to record a video, it often fails, so I can only say the following steps

1. ./chrome/Chromium.app/Contents/MacOS/Chromium <https://baidu.com>  
   
   2.When the browser starts, immediately shift+commoand+N to start the incognito window 2  
   
   3.Quickly close window 2 and window 1

=================================================================  

==1640==ERROR: AddressSanitizer: heap-use-after-free on address 0x602000074570 at pc 0x000125b6d619 bp 0x7ffeebf35510 sp 0x7ffeebf35508  

READ of size 8 at 0x602000074570 thread T0  

==1640==WARNING: Can't read from symbolizer at fd 26  

==1640==WARNING: Can't read from symbolizer at fd 27  

==1640==WARNING: Can't read from symbolizer at fd 28  

==1640==WARNING: Can't read from symbolizer at fd 30  

==1640==WARNING: Failed to use and restart external symbolizer!  

#0 0x125b6d618 in TemplateURLRef::ParseHostAndSearchTermKey(SearchTermsData const&) const+0x1fc8 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x13d66618)  

#1 0x125b5938f in TemplateURLRef::ParseIfNecessary(SearchTermsData const&) const+0x3af (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x13d5238f)  

#2 0x125b6319d in TemplateURLRef::IsValid(SearchTermsData const&) const+0xd (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x13d5c19d)  

#3 0x125b98466 in (anonymous namespace)::SafeTemplateURLParser::OnXmlParseComplete(data\_decoder::DataDecoder::ResultOrError[base::Value](javascript:void(0);))+0x6716 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x13d91466)  

#4 0x125b99ca9 in base::internal::Invoker<base::internal::BindState<void ((anonymous namespace)::SafeTemplateURLParser::\*)(data\_decoder::DataDecoder::ResultOrError[base::Value](javascript:void(0);)), std::\_\_1::unique\_ptr<(anonymous namespace)::SafeTemplateURLParser, std::\_\_1::default\_delete<(anonymous namespace)::SafeTemplateURLParser> > >, void (data\_decoder::DataDecoder::ResultOrError[base::Value](javascript:void(0);))>::RunOnce(base::internal::BindStateBase\*, data\_decoder::DataDecoder::ResultOrError[base::Value](javascript:void(0);)&&)+0x249 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x13d92ca9)  

#5 0x115d4b062 in base::internal::Invoker<base::internal::BindState<data\_decoder::DataDecoder::ParseXmlIsolated(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, base::OnceCallback<void (data\_decoder::DataDecoder::ResultOrError[base::Value](javascript:void(0);))>)::$\_1, std::\_\_1::unique\_ptr<data\_decoder::DataDecoder, std::\_\_1::default\_delete<data\_decoder::DataDecoder> >, base::OnceCallback<void (data\_decoder::DataDecoder::ResultOrError[base::Value](javascript:void(0);))> >, void (data\_decoder::DataDecoder::ResultOrError[base::Value](javascript:void(0);))>::RunOnce(base::internal::BindStateBase\*, data\_decoder::DataDecoder::ResultOrError[base::Value](javascript:void(0);)&&)+0x3c2 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x3f44062)  

#6 0x115d4554f in data\_decoder::(anonymous namespace)::ValueParseRequest<data\_decoder::mojom::XmlParser, base::Value>::OnServiceValueOrError(absl::optional[base::Value](javascript:void(0);), absl::optional<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > > const&)+0x61f (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x3f3e54f)  

#7 0x115d4aa73 in base::internal::Invoker<base::internal::BindState<void (data\_decoder::(anonymous namespace)::ValueParseRequest<data\_decoder::mojom::XmlParser, base::Value>::\*)(absl::optional[base::Value](javascript:void(0);), absl::optional<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > > const&), scoped\_refptr<data\_decoder::(anonymous namespace)::ValueParseRequest<data\_decoder::mojom::XmlParser, base::Value> > >, void (absl::optional[base::Value](javascript:void(0);), absl::optional<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > > const&)>::RunOnce(base::internal::BindStateBase\*, absl::optional[base::Value](javascript:void(0);)&&, absl::optional<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > > const&)+0x1b3 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x3f43a73)  

#8 0x115d6c6fc in data\_decoder::mojom::XmlParser\_Parse\_ForwardToCallback::Accept(mojo::Message\*)+0x3bc (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x3f656fc)  

#9 0x11f954932 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*)+0xa22 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xdb4d932)  

#10 0x11f962885 in mojo::MessageDispatcher::Accept(mojo::Message\*)+0x365 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xdb5b885)  

#11 0x11f9586e4 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*)+0x154 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xdb516e4)  

#12 0x11f96ef79 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*)+0x7f9 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xdb67f79)  

#13 0x11f96d38d in mojo::internal::MultiplexRouter::Accept(mojo::Message\*)+0x6ed (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xdb6638d)  

#14 0x11f962885 in mojo::MessageDispatcher::Accept(mojo::Message\*)+0x365 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xdb5b885)  

#15 0x11f948bda in mojo::Connector::DispatchMessage(mojo::Message)+0x36a (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xdb41bda)  

#16 0x11f94b078 in mojo::Connector::ReadAllAvailableMessages()+0x268 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xdb44078)  

#17 0x11f9ba7ae in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x36e (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xdbb37ae)  

#18 0x11f9bb7e2 in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase\*)+0x1f2 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xdbb47e2)  

#19 0x11f35bb0f in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34f (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd554b0f)  

#20 0x11f3991cc in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*)+0x4dc (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd5921cc)  

#21 0x11f3989c6 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x126 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd5919c6)  

#22 0x11f399e91 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x11 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd592e91)  

#23 0x11f479ed8 in base::MessagePumpCFRunLoopBase::RunWork()+0x188 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd672ed8)  

#24 0x11f466d59 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd65fd59)  

#25 0x11f4787f5 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*)+0x175 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd6717f5)  

#26 0x7fff34ea0d51 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x10 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86\_64h+0x83d51)  

#27 0x7fff34ea0cf0 in \_\_CFRunLoopDoSource0+0x66 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86\_64h+0x83cf0)  

#28 0x7fff34ea0b0a in \_\_CFRunLoopDoSources0+0xd0 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86\_64h+0x83b0a)  

#29 0x7fff34e9f839 in \_\_CFRunLoopRun+0x39e (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86\_64h+0x82839)  

#30 0x7fff34e9ee3d in CFRunLoopRunSpecific+0x1cd (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86\_64h+0x81e3d)  

#31 0x7fff33acbabc in RunCurrentEventLoopInMode+0x123 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:x86\_64+0x2fabc)  

#32 0x7fff33acb7d4 in ReceiveNextEventCommon+0x247 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:x86\_64+0x2f7d4)  

#33 0x7fff33acb578 in \_BlockUntilNextEventMatchingListInModeWithFilter+0x3f (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:x86\_64+0x2f578)  

#34 0x7fff32111038 in \_DPSNextEvent+0x372 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86\_64+0x41038)  

#35 0x7fff3210f87f in -[NSApplication(NSEvent) \_nextEventMatchingEventMask:untilDate:inMode:dequeue:]+0x547 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86\_64+0x3f87f)  

#36 0x11e1df642 in \_\_71-[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]\_block\_invoke+0x192 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc3d8642)  

#37 0x11f466d59 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd65fd59)  

#38 0x11e1df1da in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]+0x32a (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc3d81da)  

#39 0x7fff3210158d in -[NSApplication run]+0x291 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86\_64+0x3158d)  

#40 0x11f47b89a in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate\*)+0x3da (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd67489a)  

#41 0x11f4775d8 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*)+0x208 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd6705d8)  

#42 0x11f39a57a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x2aa (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd59357a)  

#43 0x11f2d067c in base::RunLoop::Run(base::Location const&)+0x4ac (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd4c967c)  

#44 0x116565448 in content::BrowserMainLoop::RunMainMessageLoop()+0x268 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x475e448)  

#45 0x116569991 in content::BrowserMainRunnerImpl::Run()+0x31 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x4762991)  

#46 0x11655f165 in content::BrowserMain(content::MainFunctionParams)+0x2a5 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x4758165)  

#47 0x11e033d2a in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*)+0x26a (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc22cd2a)  

#48 0x11e0369be in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool)+0xb3e (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc22f9be)  

#49 0x11e035c36 in content::ContentMainRunnerImpl::Run()+0x306 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc22ec36)  

#50 0x11e030ef2 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*)+0x4f2 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc229ef2)  

#51 0x11e032df1 in content::ContentMain(content::ContentMainParams)+0xf1 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc22bdf1)  

#52 0x111e0bae4 in ChromeMain+0x254 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x4ae4)  

#53 0x103cc3baf in main+0x1ff (/Users/yaozhihua/Desktop/./asan-mac-release-945735/Chromium.app/Contents/MacOS/Chromium:x86\_64+0x100000baf)  

#54 0x7fff6ef10cc8 in start+0x0 (/usr/lib/system/libdyld.dylib:x86\_64+0x1acc8)

0x602000074570 is located 0 bytes inside of 8-byte region [0x602000074570,0x602000074578)  

freed by thread T0 here:  

#0 0x103e0c609 in \_\_asan\_memmove+0x1d19 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/MacOS/libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x47609)  

#1 0x125bafbdf in TemplateURLService::~TemplateURLService()+0x97f (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x13da8bdf)  

#2 0x125bb00b4 in non-virtual thunk to TemplateURLService::~TemplateURLService()+0x14 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x13da90b4)  

#3 0x1230744f2 in KeyedServiceFactory::Disassociate(void\*)+0x232 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x1126d4f2)  

#4 0x123074712 in KeyedServiceFactory::ContextDestroyed(void\*)+0x22 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x1126d712)  

#5 0x123072365 in DependencyManager::PerformInterlockedTwoPhaseShutdown(DependencyManager\*, void\*, DependencyManager\*, void\*)+0x775 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x1126b365)  

#6 0x11e7aff2f in ProfileImpl::~ProfileImpl()+0x6ff (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc9a8f2f)  

#7 0x11e7b071d in ProfileImpl::~ProfileImpl()+0xd (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc9a971d)  

#8 0x11e76d57f in ProfileDestroyer::DestroyOriginalProfileNow(Profile\*)+0x1ef (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc96657f)  

#9 0x11e76c9c6 in ProfileDestroyer::DestroyProfileWhenAppropriate(Profile\*)+0x1d6 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc9659c6)  

#10 0x11e7d0f14 in ProfileManager::ProfileInfo::~ProfileInfo()+0x64 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc9c9f14)  

#11 0x11e7d87a7 in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<base::FilePath, std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo, std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >, std::\_\_1::\_\_map\_value\_compare<base::FilePath, std::\_\_1::\_\_value\_type<base::FilePath, std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo, std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >, std::\_\_1::less[base::FilePath](javascript:void(0);), true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<base::FilePath, std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo, std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > > > >::erase(std::\_\_1::\_\_tree\_const\_iterator<std::\_\_1::\_\_value\_type<base::FilePath, std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo, std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >, std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<base::FilePath, std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo, std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >, void\*>\*, long>)+0x167 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc9d17a7)  

#12 0x11e7cd7ff in ProfileManager::RemoveProfile(base::FilePath const&)+0x24f (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc9c67ff)  

#13 0x11e7cd45b in ProfileManager::DeleteProfileIfNoKeepAlive(ProfileManager::ProfileInfo const\*)+0x49b (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc9c645b)  

#14 0x11e7ccd83 in ProfileManager::RemoveKeepAlive(Profile const\*, ProfileKeepAliveOrigin)+0x8b3 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc9c5d83)  

#15 0x11f35bb0f in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34f (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd554b0f)  

#16 0x11f3991cc in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*)+0x4dc (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd5921cc)  

#17 0x11f3989c6 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x126 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd5919c6)  

#18 0x11f399e91 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x11 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd592e91)  

#19 0x11f479ed8 in base::MessagePumpCFRunLoopBase::RunWork()+0x188 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd672ed8)  

#20 0x11f466d59 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd65fd59)  

#21 0x11f4787f5 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*)+0x175 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xd6717f5)  

#22 0x7fff34ea0d51 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x10 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86\_64h+0x83d51)  

#23 0x7fff34ea0cf0 in \_\_CFRunLoopDoSource0+0x66 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86\_64h+0x83cf0)  

#24 0x7fff34ea0b0a in \_\_CFRunLoopDoSources0+0xd0 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86\_64h+0x83b0a)  

#25 0x7fff34e9f839 in \_\_CFRunLoopRun+0x39e (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86\_64h+0x82839)  

#26 0x7fff34e9ee3d in CFRunLoopRunSpecific+0x1cd (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86\_64h+0x81e3d)  

#27 0x7fff33acbabc in RunCurrentEventLoopInMode+0x123 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:x86\_64+0x2fabc)  

#28 0x7fff33acb7d4 in ReceiveNextEventCommon+0x247 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:x86\_64+0x2f7d4)  

#29 0x7fff33acb578 in \_BlockUntilNextEventMatchingListInModeWithFilter+0x3f (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:x86\_64+0x2f578)

previously allocated by thread T0 here:  

#0 0x103e0c4c0 in \_\_asan\_memmove+0x1bd0 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/MacOS/libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x474c0)  

#1 0x111e09427 in operator new(unsigned long)+0x27 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x2427)  

#2 0x11e83b9d1 in TemplateURLServiceFactory::BuildInstanceFor(content::BrowserContext\*)+0x131 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xca349d1)  

#3 0x123073af6 in KeyedServiceFactory::GetServiceForContext(void\*, bool)+0x2c6 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x1126caf6)  

#4 0x11e83b7bd in TemplateURLServiceFactory::GetForProfile(Profile\*)+0x1d (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xca347bd)  

#5 0x1277855e5 in extensions::OmniboxAPI::OmniboxAPI(content::BrowserContext\*)+0x135 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x1597e5e5)  

#6 0x12778abd1 in extensions::BrowserContextKeyedAPIFactory[extensions::OmniboxAPI](javascript:void(0);)::BuildServiceInstanceFor(content::BrowserContext\*) const+0x21 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x15983bd1)  

#7 0x123073af6 in KeyedServiceFactory::GetServiceForContext(void\*, bool)+0x2c6 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x1126caf6)  

#8 0x1230712bd in DependencyManager::CreateContextServices(void\*, bool)+0x2cd (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x1126a2bd)  

#9 0x126ef9580 in BrowserContextDependencyManager::CreateBrowserContextServices(content::BrowserContext\*)+0x130 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x150f2580)  

#10 0x11e7b27eb in ProfileImpl::OnLocaleReady(Profile::CreateMode)+0xeb (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc9ab7eb)  

#11 0x11e7aafcb in ProfileImpl::OnPrefsLoaded(Profile::CreateMode, bool)+0x11b (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc9a3fcb)  

#12 0x11e7a9ae9 in ProfileImpl::ProfileImpl(base::FilePath const&, Profile::Delegate\*, Profile::CreateMode, base::Time, scoped\_refptr[base::SequencedTaskRunner](javascript:void(0);))+0x649 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc9a2ae9)  

#13 0x11e7a5cd5 in Profile::CreateProfile(base::FilePath const&, Profile::Delegate\*, Profile::CreateMode)+0x235 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc99ecd5)  

#14 0x11e7bd20a in ProfileManager::CreateAndInitializeProfile(base::FilePath const&)+0x3ba (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc9b620a)  

#15 0x11e7b9f94 in ProfileManager::GetProfile(base::FilePath const&)+0x174 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc9b2f94)  

#16 0x12942f2e3 in GetStartupProfile(base::FilePath const&, base::CommandLine const&)+0x1e3 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x176282e3)  

#17 0x11e21965e in (anonymous namespace)::CreatePrimaryProfile(content::MainFunctionParams const&, base::FilePath const&, base::CommandLine const&)+0x2ae (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc41265e)  

#18 0x11e2166a9 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl()+0x7e9 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc40f6a9)  

#19 0x11e215ccd in ChromeBrowserMainParts::PreMainMessageLoopRun()+0x5d (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc40eccd)  

#20 0x116563275 in content::BrowserMainLoop::PreMainMessageLoopRun()+0xa5 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x475c275)  

#21 0x1176b5a4f in content::StartupTaskRunner::RunAllTasksNow()+0x13f (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x58aea4f)  

#22 0x116562800 in content::BrowserMainLoop::CreateStartupTasks()+0x640 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x475b800)  

#23 0x11656901e in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams)+0x18e (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x476201e)  

#24 0x11655f117 in content::BrowserMain(content::MainFunctionParams)+0x257 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x4758117)  

#25 0x11e033d2a in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*)+0x26a (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc22cd2a)  

#26 0x11e0369be in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool)+0xb3e (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc22f9be)  

#27 0x11e035c36 in content::ContentMainRunnerImpl::Run()+0x306 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc22ec36)  

#28 0x11e030ef2 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*)+0x4f2 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc229ef2)  

#29 0x11e032df1 in content::ContentMain(content::ContentMainParams)+0xf1 (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0xc22bdf1)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/yaozhihua/Desktop/asan-mac-release-945735/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/98.0.4733.0/Chromium Framework:x86\_64+0x13d66618) in TemplateURLRef::ParseHostAndSearchTermKey(SearchTermsData const&) const+0x1fc8  

Shadow bytes around the buggy address:  

0x1c040000e850: fa fa fd fd fa fa fd fa fa fa fd fd fa fa fd fd  

0x1c040000e860: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x1c040000e870: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x1c040000e880: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x1c040000e890: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

=>0x1c040000e8a0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa[fd]fa  

0x1c040000e8b0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

0x1c040000e8c0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd  

0x1c040000e8d0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

0x1c040000e8e0: fa fa fd fd fa fa fd fd fa fa fd fa fa fa fd fa  

0x1c040000e8f0: fa fa fd fd fa fa fd fd fa fa fd fa fa fa fd fd  

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

==1640==ABORTING

**VERSION**  

Chrome Version: 98.0.4733.0 x64  

Operating System: macOS Catalina 10.15.7  

credit information:

Zhihua Yao of KunLun Lab

## Attachments

- [demo.mp4](attachments/demo.mp4) (video/mp4, 6.2 MB)

## Timeline

### ha...@gmail.com (2021-12-09)

I will analyze the cause of the vulnerability later, and I will try to record a video that reproduces the success.

### [Deleted User] (2021-12-09)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-12-09)

+omnibox owners. A browser process UaF is normally Critical vulnerability, but this is very hard to trigger, so I'm downgrading it to Medium.

[Monorail components: UI>Browser>Omnibox]

### [Deleted User] (2021-12-09)

[Empty comment from Monorail migration]

### ha...@gmail.com (2021-12-10)

Hello dominickn,I think this can be raised to high because I found that I can trigger the vulnerability with very little interaction.
reproduce step:
1../chrome/Chromium.app/Contents/MacOS/Chromium https://baidu.com
2.wait 2 sec and then close the window immediately 
3. UAF trigger

### ha...@gmail.com (2021-12-10)

[0] https://source.chromium.org/chromium/chromium/src/+/main:components/search_engines/template_url_service.h;l=709
  std::unique_ptr<SearchTermsData> search_terms_data_ =
      std::make_unique<SearchTermsData>();  //SearchTermsData is owned by TemplateURLService ,while TemplateURLService destroyed,SearchTermsData will be free
[1] https://source.chromium.org/chromium/chromium/src/+/main:components/search_engines/template_url.cc;l=901

void TemplateURLRef::ParseHostAndSearchTermKey(
    const SearchTermsData& search_terms_data) const {
  std::string url_string(GetURL());
  base::ReplaceSubstringsAfterOffset(
      &url_string, 0, "{google:baseURL}",
      search_terms_data.GoogleBaseURLValue());  // UAF here
  base::ReplaceSubstringsAfterOffset(
      &url_string, 0, "{google:baseSuggestURL}",
      search_terms_data.GoogleBaseSuggestURLValue());
  base::ReplaceSubstringsAfterOffset(&url_string, 0, "{yandex:searchPath}",
                                     YandexSearchPathFromDeviceFormFactor());
.......



windows asan log
=================================================================
==748==ERROR: AddressSanitizer: heap-use-after-free on address 0x1204ff4d6f70 at pc 0x7ffcc2378303 bp 0x0082d4bf8d80 sp 0x0082d4bf8dc8
READ of size 8 at 0x1204ff4d6f70 thread T0
    #0 0x7ffcc2378302 in TemplateURLRef::ParseHostAndSearchTermKey E:\src\chromium\src\components\search_engines\template_url.cc:901
    #1 0x7ffcc2363e03 in TemplateURLRef::ParseIfNecessary E:\src\chromium\src\components\search_engines\template_url.cc:868
    #2 0x7ffcc236c048 in TemplateURLRef::IsValid E:\src\chromium\src\components\search_engines\template_url.cc:427
    #3 0x7ffcc533b32e in `anonymous namespace'::SafeTemplateURLParser::OnXmlParseComplete E:\src\chromium\src\components\search_engines\template_url_parser.cc:223
    #4 0x7ffcc533cc23 in base::internal::Invoker<base::internal::BindState<void ((anonymous namespace)::SafeTemplateURLParser::*)(data_decoder::DataDecoder::ResultOrError<base::Value>),std::__1::unique_ptr<(anonymous namespace)::SafeTemplateURLParser,std::__1::default_delete<(anonymous namespace)::SafeTemplateURLParser> > >,void (data_decoder::DataDecoder::ResultOrError<base::Value>)>::RunOnce E:\src\chromium\src\base\bind_internal.h:741
    #5 0x7ffcbd0126e5 in base::internal::Invoker<base::internal::BindState<`lambda at ../../services/data_decoder/public/cpp/data_decoder.cc:238:16',std::__1::unique_ptr<data_decoder::DataDecoder,std::__1::default_delete<data_decoder::DataDecoder> >,base::OnceCallback<void (data_decoder::DataDecoder::ResultOrError<base::Value>)> >,void (data_decoder::DataDecoder::ResultOrError<base::Value>)>::RunOnce E:\src\chromium\src\base\bind_internal.h:741
    #6 0x7ffcbd00ce79 in data_decoder::`anonymous namespace'::ValueParseRequest<data_decoder::mojom::XmlParser,base::Value>::OnServiceValueOrError E:\src\chromium\src\services\data_decoder\public\cpp\data_decoder.cc:90
    #7 0x7ffcbd0123fb in base::internal::Invoker<base::internal::BindState<void (data_decoder::(anonymous namespace)::ValueParseRequest<data_decoder::mojom::XmlParser,base::Value>::*)(absl::optional<base::Value>, const absl::optional<std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > > &),scoped_refptr<data_decoder::(anonymous namespace)::ValueParseRequest<data_decoder::mojom::XmlParser,base::Value> > >,void (absl::optional<base::Value>, const absl::optional<std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > > &)>::RunOnce E:\src\chromium\src\base\bind_internal.h:741
    #8 0x7ffcbd037f5b in base::OnceCallback<void (absl::optional<base::Value>, const absl::optional<std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > > &)>::Run E:\src\chromium\src\base\callback.h:142
    #9 0x7ffcbd03dedd in data_decoder::mojom::XmlParser_Parse_ForwardToCallback::Accept E:\src\chromium\src\out\Default\gen\services\data_decoder\public\mojom\xml_parser.mojom.cc:205
    #10 0x7ffcf4d69884 in mojo::InterfaceEndpointClient::HandleValidatedMessage E:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:895
    #11 0x7ffcf4d79a88 in mojo::MessageDispatcher::Accept E:\src\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #12 0x7ffcf4d6d3c4 in mojo::InterfaceEndpointClient::HandleIncomingMessage E:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:657
    #13 0x7ffcf4d86ccc in mojo::internal::MultiplexRouter::ProcessIncomingMessage E:\src\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1104
    #14 0x7ffcf4d85a65 in mojo::internal::MultiplexRouter::Accept E:\src\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:724
    #15 0x7ffcf4d79a88 in mojo::MessageDispatcher::Accept E:\src\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #16 0x7ffcf4d59a91 in mojo::Connector::DispatchMessageW E:\src\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:556
    #17 0x7ffcf4d5b584 in mojo::Connector::ReadAllAvailableMessages E:\src\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:614
    #18 0x7ffcf9f545db in mojo::SimpleWatcher::OnHandleReady E:\src\chromium\src\mojo\public\cpp\system\simple_watcher.cc:278
    #19 0x7ffccfcb7494 in base::TaskAnnotator::RunTaskImpl E:\src\chromium\src\base\task\common\task_annotator.cc:135
    #20 0x7ffccfd06ad9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356
    #21 0x7ffccfd061a8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #22 0x7ffccfe02376 in base::MessagePumpForUI::DoRunLoop E:\src\chromium\src\base\message_loop\message_pump_win.cc:220
    #23 0x7ffccfdffe2f in base::MessagePumpWin::Run E:\src\chromium\src\base\message_loop\message_pump_win.cc:78
    #24 0x7ffccfd08253 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468
    #25 0x7ffccfc01e23 in base::RunLoop::Run E:\src\chromium\src\base\run_loop.cc:140
    #26 0x7ffcb705acf1 in content::BrowserMainLoop::RunMainMessageLoop E:\src\chromium\src\content\browser\browser_main_loop.cc:1038
    #27 0x7ffcb7060af3 in content::BrowserMainRunnerImpl::Run E:\src\chromium\src\content\browser\browser_main_runner_impl.cc:153
    #28 0x7ffcb705417f in content::BrowserMain E:\src\chromium\src\content\browser\browser_main.cc:30
    #29 0x7ffcb91a155e in content::RunBrowserProcessMain E:\src\chromium\src\content\app\content_main_runner_impl.cc:646
    #30 0x7ffcb91a4713 in content::ContentMainRunnerImpl::RunBrowser E:\src\chromium\src\content\app\content_main_runner_impl.cc:1160
    #31 0x7ffcb91a3841 in content::ContentMainRunnerImpl::Run E:\src\chromium\src\content\app\content_main_runner_impl.cc:1026
    #32 0x7ffcb919f5ef in content::RunContentProcess E:\src\chromium\src\content\app\content_main.cc:398
    #33 0x7ffcb91a0657 in content::ContentMain E:\src\chromium\src\content\app\content_main.cc:426
    #34 0x7ffcbc6f14a5 in ChromeMain E:\src\chromium\src\chrome\app\chrome_main.cc:177
    #35 0x7ff65e535554 in MainDllLoader::Launch E:\src\chromium\src\chrome\app\main_dll_loader_win.cc:169
    #36 0x7ff65e532a02 in main E:\src\chromium\src\chrome\app\chrome_exe_main_win.cc:382
    #37 0x7ff65e70ef1b in __scrt_common_main_seh D:\agent\_work\13\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #38 0x7ffd30497033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #39 0x7ffd32402650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x1204ff4d6f70 is located 0 bytes inside of 8-byte region [0x1204ff4d6f70,0x1204ff4d6f78)
freed by thread T0 here:
    #0 0x7ffcd095070b in operator delete+0x8b (E:\src\chromium\src\out\Default\clang_rt.asan_dynamic-x86_64.dll+0x18004070b)
    #1 0x7ffcc23611a3 in UIThreadSearchTermsData::~UIThreadSearchTermsData E:\src\chromium\src\chrome\browser\search_engines\ui_thread_search_terms_data.h:14
    #2 0x7ffcc233c92f in TemplateURLService::~TemplateURLService E:\src\chromium\src\components\search_engines\template_url_service.cc:310
    #3 0x7ffcc2356e46 in TemplateURLService::`vector deleting destructor'+0x16 (E:\src\chromium\src\out\Default\chrome.dll+0x185c66e46)
    #4 0x7ffcfa11ea70 in std::__1::__tree<std::__1::__value_type<void *,std::__1::unique_ptr<KeyedService,std::__1::default_delete<KeyedService> > >,std::__1::__map_value_compare<void *,std::__1::__value_type<void *,std::__1::unique_ptr<KeyedService,std::__1::default_delete<KeyedService> > >,std::__1::less<void *>,1>,std::__1::allocator<std::__1::__value_type<void *,std::__1::unique_ptr<KeyedService,std::__1::default_delete<KeyedService> > > > >::erase E:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__tree:2422
    #5 0x7ffcfa11d828 in KeyedServiceFactory::Disassociate E:\src\chromium\src\components\keyed_service\core\keyed_service_factory.cc:97
    #6 0x7ffcfa11dab8 in KeyedServiceFactory::ContextDestroyed E:\src\chromium\src\components\keyed_service\core\keyed_service_factory.cc:107
    #7 0x7ffcfa11b5df in DependencyManager::PerformInterlockedTwoPhaseShutdown E:\src\chromium\src\components\keyed_service\core\dependency_manager.cc:127
    #8 0x7ffcc113a901 in ProfileImpl::~ProfileImpl E:\src\chromium\src\chrome\browser\profiles\profile_impl.cc:909
    #9 0x7ffcc113e58b in ProfileImpl::~ProfileImpl E:\src\chromium\src\chrome\browser\profiles\profile_impl.cc:856
    #10 0x7ffcc1150cfb in ProfileDestroyer::DestroyOriginalProfileNow E:\src\chromium\src\chrome\browser\profiles\profile_destroyer.cc:133
    #11 0x7ffcc1150500 in ProfileDestroyer::DestroyProfileWhenAppropriate E:\src\chromium\src\chrome\browser\profiles\profile_destroyer.cc:61
    #12 0x7ffcbfef410d in ProfileManager::ProfileInfo::~ProfileInfo E:\src\chromium\src\chrome\browser\profiles\profile_manager.cc:1648
    #13 0x7ffcbfefc4dd in std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> >::reset E:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:315
    #14 0x7ffcbfefcc88 in std::__1::__tree<std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > >,std::__1::__map_value_compare<base::FilePath,std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > >,std::__1::less<base::FilePath>,1>,std::__1::allocator<std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > > > >::erase E:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__tree:2422
    #15 0x7ffcbfefcbdd in std::__1::__tree<std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > >,std::__1::__map_value_compare<base::FilePath,std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > >,std::__1::less<base::FilePath>,1>,std::__1::allocator<std::__1::__value_type<base::FilePath,std::__1::unique_ptr<ProfileManager::ProfileInfo,std::__1::default_delete<ProfileManager::ProfileInfo> > > > >::__erase_unique<base::FilePath> E:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__tree:2445
    #16 0x7ffcbfef1aa7 in ProfileManager::RemoveProfile E:\src\chromium\src\chrome\browser\profiles\profile_manager.cc:1753
    #17 0x7ffcbfef1848 in ProfileManager::DeleteProfileIfNoKeepAlive E:\src\chromium\src\chrome\browser\profiles\profile_manager.cc:1483
    #18 0x7ffcbfef1392 in ProfileManager::RemoveKeepAlive E:\src\chromium\src\chrome\browser\profiles\profile_manager.cc:1440
    #19 0x7ffccfcb7494 in base::TaskAnnotator::RunTaskImpl E:\src\chromium\src\base\task\common\task_annotator.cc:135
    #20 0x7ffccfd06ad9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356
    #21 0x7ffccfd061a8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #22 0x7ffccfe02376 in base::MessagePumpForUI::DoRunLoop E:\src\chromium\src\base\message_loop\message_pump_win.cc:220
    #23 0x7ffccfdffe2f in base::MessagePumpWin::Run E:\src\chromium\src\base\message_loop\message_pump_win.cc:78
    #24 0x7ffccfd08253 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468
    #25 0x7ffccfc01e23 in base::RunLoop::Run E:\src\chromium\src\base\run_loop.cc:140
    #26 0x7ffcb705acf1 in content::BrowserMainLoop::RunMainMessageLoop E:\src\chromium\src\content\browser\browser_main_loop.cc:1038
    #27 0x7ffcb7060af3 in content::BrowserMainRunnerImpl::Run E:\src\chromium\src\content\browser\browser_main_runner_impl.cc:153

previously allocated by thread T0 here:
    #0 0x7ffcd095041b in operator new+0x8b (E:\src\chromium\src\out\Default\clang_rt.asan_dynamic-x86_64.dll+0x18004041b)
    #1 0x7ffcc1176698 in TemplateURLServiceFactory::BuildInstanceFor E:\src\chromium\src\chrome\browser\search_engines\template_url_service_factory.cc:52
    #2 0x7ffcc1176a24 in TemplateURLServiceFactory::BuildServiceInstanceFor E:\src\chromium\src\chrome\browser\search_engines\template_url_service_factory.cc:74
    #3 0x7ffcdba7329d in BrowserContextKeyedServiceFactory::BuildServiceInstanceFor E:\src\chromium\src\components\keyed_service\content\browser_context_keyed_service_factory.cc:95
    #4 0x7ffcfa11cfd2 in KeyedServiceFactory::GetServiceForContext E:\src\chromium\src\components\keyed_service\core\keyed_service_factory.cc:80
    #5 0x7ffcc11764cf in TemplateURLServiceFactory::GetForProfile E:\src\chromium\src\chrome\browser\search_engines\template_url_service_factory.cc:33
    #6 0x7ffcc38eb605 in extensions::OmniboxAPI::OmniboxAPI E:\src\chromium\src\chrome\browser\extensions\api\omnibox\omnibox_api.cc:187
    #7 0x7ffcdba7329d in BrowserContextKeyedServiceFactory::BuildServiceInstanceFor E:\src\chromium\src\components\keyed_service\content\browser_context_keyed_service_factory.cc:95
    #8 0x7ffcfa11cfd2 in KeyedServiceFactory::GetServiceForContext E:\src\chromium\src\components\keyed_service\core\keyed_service_factory.cc:80
    #9 0x7ffcfa11a851 in DependencyManager::CreateContextServices E:\src\chromium\src\components\keyed_service\core\dependency_manager.cc:87
    #10 0x7ffcdba713d4 in BrowserContextDependencyManager::DoCreateBrowserContextServices E:\src\chromium\src\components\keyed_service\content\browser_context_dependency_manager.cc:46
    #11 0x7ffcc113cdd4 in ProfileImpl::OnLocaleReady E:\src\chromium\src\chrome\browser\profiles\profile_impl.cc:1100
    #12 0x7ffcc113705d in ProfileImpl::OnPrefsLoaded E:\src\chromium\src\chrome\browser\profiles\profile_impl.cc:1141
    #13 0x7ffcc1134904 in ProfileImpl::ProfileImpl E:\src\chromium\src\chrome\browser\profiles\profile_impl.cc:535
    #14 0x7ffcc1133adf in Profile::CreateProfile E:\src\chromium\src\chrome\browser\profiles\profile_impl.cc:365
    #15 0x7ffcbfeef3ff in ProfileManager::CreateProfileHelper E:\src\chromium\src\chrome\browser\profiles\profile_manager.cc:1356
    #16 0x7ffcbfee2d02 in ProfileManager::CreateAndInitializeProfile E:\src\chromium\src\chrome\browser\profiles\profile_manager.cc:1791
    #17 0x7ffcbfee0285 in ProfileManager::GetProfile E:\src\chromium\src\chrome\browser\profiles\profile_manager.cc:741
    #18 0x7ffcc21b6e84 in GetStartupProfile E:\src\chromium\src\chrome\browser\ui\startup\startup_browser_creator.cc:1365
    #19 0x7ffcc0eba96c in `anonymous namespace'::CreatePrimaryProfile E:\src\chromium\src\chrome\browser\chrome_browser_main.cc:421
    #20 0x7ffcc0eb7c32 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl E:\src\chromium\src\chrome\browser\chrome_browser_main.cc:1427
    #21 0x7ffcc0eb68a7 in ChromeBrowserMainParts::PreMainMessageLoopRun E:\src\chromium\src\chrome\browser\chrome_browser_main.cc:1082
    #22 0x7ffcb7058950 in content::BrowserMainLoop::PreMainMessageLoopRun E:\src\chromium\src\content\browser\browser_main_loop.cc:977
    #23 0x7ffcb80be423 in content::StartupTaskRunner::RunAllTasksNow E:\src\chromium\src\content\browser\startup_task_runner.cc:43
    #24 0x7ffcb7057d40 in content::BrowserMainLoop::CreateStartupTasks E:\src\chromium\src\content\browser\browser_main_loop.cc:885
    #25 0x7ffcb7060008 in content::BrowserMainRunnerImpl::Initialize E:\src\chromium\src\content\browser\browser_main_runner_impl.cc:132
    #26 0x7ffcb705412a in content::BrowserMain E:\src\chromium\src\content\browser\browser_main.cc:26
    #27 0x7ffcb91a155e in content::RunBrowserProcessMain E:\src\chromium\src\content\app\content_main_runner_impl.cc:646

SUMMARY: AddressSanitizer: heap-use-after-free E:\src\chromium\src\components\search_engines\template_url.cc:901 in TemplateURLRef::ParseHostAndSearchTermKey
Shadow bytes around the buggy address:
  0x04419f31ad90: fa fa fd fd fa fa fd fa fa fa fd fd fa fa fd fd
  0x04419f31ada0: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
  0x04419f31adb0: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
  0x04419f31adc0: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
  0x04419f31add0: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
=>0x04419f31ade0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa[fd]fa
  0x04419f31adf0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x04419f31ae00: fa fa fd fd fa fa fd fa fa fa fd fd fa fa fd fa
  0x04419f31ae10: fa fa fd fd fa fa fd fa fa fa fd fd fa fa fd fa
  0x04419f31ae20: fa fa fd fd fa fa fd fa fa fa fd fd fa fa fd fa
  0x04419f31ae30: fa fa fd fd fa fa fd fa fa fa fd fd fa fa fd fa
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
==748==ABORTING


### do...@chromium.org (2021-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-10)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2021-12-14)

Sheriff ping: can owners please take a look and triage this High severity issue, thanks.

### [Deleted User] (2021-12-23)

tommycli: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2022-01-07)

Any update?

### [Deleted User] (2022-01-07)

tommycli: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2022-01-18)

blundell: Regarding services with factories and DependsOn declarations...

Does that mean we can rely on the parent services being valid for the whole lifetime of the child services?

Thanks,

Tommy

### to...@chromium.org (2022-01-19)

Okay I think I know what's going on. TemplateURLParser::Parse takes a raw pointer to SearchTermsData, and that's simply not safe.

TemplateURLService can be destroyed by the time the XML is finished parsing and we get a callback.

Likely the right thing to do is to either:
 1. Cancel the XML Parsing callback somehow, or
 2. Take a snapshot of the SearchTermsData (HistoryURLProvider already does this with a SearchTermsDataSnapshot class) and save that to use.

#1 is better from a pure software performance standpoint but architecturally more complicated...
#2 is better from a simplicity and architecture standpoint... and HistoryURLProvider already does this.

I plan to do #2, but will keep investigating.

### jd...@chromium.org (2022-01-20)

I agree that #2 is the best approach.

### gi...@appspot.gserviceaccount.com (2022-01-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/24459ac6c72b2fd7c90f9e58bdbd6808c1a19be0

commit 24459ac6c72b2fd7c90f9e58bdbd6808c1a19be0
Author: Tommy Li <tommycli@chromium.org>
Date: Thu Jan 20 18:33:14 2022

[omnibox] Fix UAF bug in TemplateURLParser

This CL takes a snapshot of SearchTermsData (just like
HistoryURLProvider does) within TemplateURLParser, so we eliminate a
source of UAF bugs, where the TemplateURL parsing outlives the original
SearchTermsData.

This bug happens during Chrome shutdown.

Bug: 1278322
Change-Id: I439d9d3193bcaa7ef57ec0a046d057c32ef6fb76
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3403242
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Commit-Queue: Tommy Li <tommycli@chromium.org>
Cr-Commit-Position: refs/heads/main@{#961536}

[modify] https://crrev.com/24459ac6c72b2fd7c90f9e58bdbd6808c1a19be0/components/search_engines/search_terms_data.h
[modify] https://crrev.com/24459ac6c72b2fd7c90f9e58bdbd6808c1a19be0/components/omnibox/browser/history_url_provider.cc
[modify] https://crrev.com/24459ac6c72b2fd7c90f9e58bdbd6808c1a19be0/components/search_engines/template_url_parser.cc
[modify] https://crrev.com/24459ac6c72b2fd7c90f9e58bdbd6808c1a19be0/components/search_engines/search_terms_data.cc


### to...@chromium.org (2022-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-22)

Requesting merge to extended stable M96 because latest trunk commit (961536) appears to be after extended stable branch point (929512).

Requesting merge to stable M97 because latest trunk commit (961536) appears to be after stable branch point (938553).

Requesting merge to beta M98 because latest trunk commit (961536) appears to be after beta branch point (950365).

Not requesting merge to dev (M99) because latest trunk commit (961536) appears to be prior to dev branch point (961656). If this is incorrect, please replace the Merge-NA-99 label with Merge-Request-99. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-22)

Merge review required: M98 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-22)

Merge review required: M97 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-22)

Merge review required: M96 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2022-01-24)

I wasn't going to recommend a merge. The fix was non-trivial and I'd feel most comfortable allowing it to trickle through the normal Canary/Dev, Beta, and then Stable cycle. It's only 10 weeks.

### am...@chromium.org (2022-01-25)

Yes, given the complexity and size of this fix, I concur with not merging this just yet, but this should ship in M99 stable at the latest. (as the fix commit is on M99/dev already, which will be promoted to beta next week) 

M98 stable cut is tomorrow, and so this is too early this should have more Canary bake time on canary given the non-trivial nature of this fix. There are no further planned releases m96 and m97 extended or stable, so I've NAed them. 


### to...@chromium.org (2022-01-25)

SGTM amyressler.

### am...@google.com (2022-01-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-28)

Congratulations - the VRP Panel has decided to award you $7,000 for this report. Thanks for your efforts and nice work! 

### ha...@gmail.com (2022-01-28)

hello amyressler,This only requires one interaction, why give so little.it doesn't make sense 

### am...@chromium.org (2022-01-28)

While this issue is a UAF in the browser process, it relies solely on user interaction and browser shutdown to trigger, so the exploitability potential is lower and the attacker control is lessened for UAFs that require a browser shutdown, which is why the lower amount in comparison to browser process memory corruption that are remotely exploitable through we content and don't require browser shutdown. 

### am...@google.com (2022-01-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-10)

While this bug does result in a UAF in the browser process, it does require Chrome shutdown to trigger and given the fix is quite complex and non-trivial, there is a high risk potential, so holding this back from merge to M98 at this time with off-bug concurrence from tommycli@ 

### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1278322?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058177)*

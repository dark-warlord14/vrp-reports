# Security: UaF in payments::SecurePaymentConfirmationAppFactory

| Field | Value |
|-------|-------|
| **Issue ID** | [40054539](https://issues.chromium.org/issues/40054539) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Payments |
| **Platforms** | Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | np...@chromium.org |
| **Created** | 2021-01-21 |
| **Bounty** | $20,000.00 |

## Description

**VERSION**  

Chrome Version: 90.0.4394.0 (Official Build) canary (x86\_64)  

Operating System: MacOS

**REPRODUCTION CASE**

Similar to <https://crbug.com/chromium/1110207>

1. Go to <http://localhost:8000/payment_request_new.html>
2. Try to close the tab manually

==13678==ERROR: AddressSanitizer: heap-use-after-free on address 0x621001894900 at pc 0x0001266db618 bp 0x7fff58d5dce0 sp 0x7fff58d5dcd8  

READ of size 8 at 0x621001894900 thread T0  

==13678==WARNING: Can't read from symbolizer at fd 119  

==13678==WARNING: Can't read from symbolizer at fd 123  

==13678==WARNING: Can't read from symbolizer at fd 124  

==13678==WARNING: Can't read from symbolizer at fd 125  

==13678==WARNING: Failed to use and restart external symbolizer!  

#0 0x1266db617 in content::InternalAuthenticatorImpl::~InternalAuthenticatorImpl()+0x137 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x16104617)  

#1 0x127fd3eed in void base::internal::FunctorTraits<void (payments::SecurePaymentConfirmationAppFactory::\*)(base::WeakPtr[payments::PaymentAppFactory::Delegate](javascript:void(0);), mojo::StructPtr[payments::mojom::SecurePaymentConfirmationRequest](javascript:void(0);), std::\_\_1::unique\_ptr<autofill::InternalAuthenticator, std::\_\_1::default\_delete[autofill::InternalAuthenticator](javascript:void(0);) >, bool), void>::Invoke<void (payments::SecurePaymentConfirmationAppFactory::\*)(base::WeakPtr[payments::PaymentAppFactory::Delegate](javascript:void(0);), mojo::StructPtr[payments::mojom::SecurePaymentConfirmationRequest](javascript:void(0);), std::\_\_1::unique\_ptr<autofill::InternalAuthenticator, std::\_\_1::default\_delete[autofill::InternalAuthenticator](javascript:void(0);) >, bool), base::WeakPtr[payments::SecurePaymentConfirmationAppFactory](javascript:void(0);), base::WeakPtr[payments::PaymentAppFactory::Delegate](javascript:void(0);), mojo::StructPtr[payments::mojom::SecurePaymentConfirmationRequest](javascript:void(0);), std::\_\_1::unique\_ptr<autofill::InternalAuthenticator, std::\_\_1::default\_delete[autofill::InternalAuthenticator](javascript:void(0);) >, bool>(void (payments::SecurePaymentConfirmationAppFactory::\*)(base::WeakPtr[payments::PaymentAppFactory::Delegate](javascript:void(0);), mojo::StructPtr[payments::mojom::SecurePaymentConfirmationRequest](javascript:void(0);), std::\_\_1::unique\_ptr<autofill::InternalAuthenticator, std::\_\_1::default\_delete[autofill::InternalAuthenticator](javascript:void(0);) >, bool), base::WeakPtr[payments::SecurePaymentConfirmationAppFactory](javascript:void(0);)&&, base::WeakPtr[payments::PaymentAppFactory::Delegate](javascript:void(0);)&&, mojo::StructPtr[payments::mojom::SecurePaymentConfirmationRequest](javascript:void(0);)&&, std::\_\_1::unique\_ptr<autofill::InternalAuthenticator, std::\_\_1::default\_delete[autofill::InternalAuthenticator](javascript:void(0);) >&&, bool&&)+0x2ed (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x179fceed)  

#2 0x127fd3b83 in base::internal::Invoker<base::internal::BindState<void (payments::SecurePaymentConfirmationAppFactory::\*)(base::WeakPtr[payments::PaymentAppFactory::Delegate](javascript:void(0);), mojo::StructPtr[payments::mojom::SecurePaymentConfirmationRequest](javascript:void(0);), std::\_\_1::unique\_ptr<autofill::InternalAuthenticator, std::\_\_1::default\_delete[autofill::InternalAuthenticator](javascript:void(0);) >, bool), base::WeakPtr[payments::SecurePaymentConfirmationAppFactory](javascript:void(0);), base::WeakPtr[payments::PaymentAppFactory::Delegate](javascript:void(0);), mojo::StructPtr[payments::mojom::SecurePaymentConfirmationRequest](javascript:void(0);), std::\_\_1::unique\_ptr<autofill::InternalAuthenticator, std::\_\_1::default\_delete[autofill::InternalAuthenticator](javascript:void(0);) > >, void (bool)>::RunOnce(base::internal::BindStateBase\*, bool)+0x153 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x179fcb83)  

#3 0x112456f17 in base::internal::Invoker<base::internal::BindState<base::OnceCallback<void (bool)>, bool>, void ()>::RunOnce(base::internal::BindStateBase\*)+0x117 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x1e7ff17)  

#4 0x11b2efc05 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*)+0x375 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xad18c05)  

#5 0x11b32e88f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*)+0x57f (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xad5788f)  

#6 0x11b32dfe7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x1f7 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xad56fe7)  

#7 0x11b41fdc8 in invocation function for block in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*)+0xe8 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xae48dc8)  

#8 0x11b40d369 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xae36369)  

#9 0x11b41e515 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*)+0x175 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xae47515)  

#10 0x7fffc2a96e50 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x10 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86\_64+0xa4e50)  

#11 0x7fffc2a780cb in \_\_CFRunLoopDoSources0+0x22b (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86\_64+0x860cb)  

#12 0x7fffc2a775b5 in \_\_CFRunLoopRun+0x3a5 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86\_64+0x855b5)  

#13 0x7fffc2a76fb3 in CFRunLoopRunSpecific+0x1a3 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86\_64+0x84fb3)  

#14 0x7fffc1fd5ebb in RunCurrentEventLoopInMode+0xef (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:x86\_64+0x30ebb)  

#15 0x7fffc1fd5cf0 in ReceiveNextEventCommon+0x1af (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:x86\_64+0x30cf0)  

#16 0x7fffc1fd5b25 in \_BlockUntilNextEventMatchingListInModeWithFilter+0x46 (/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/Versions/A/HIToolbox:x86\_64+0x30b25)  

#17 0x7fffc056aa03 in \_DPSNextEvent+0x45f (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86\_64+0x46a03)  

#18 0x7fffc0ce67ed in -[NSApplication(NSEvent) \_nextEventMatchingEventMask:untilDate:inMode:dequeue:]+0xaeb (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86\_64+0x7c27ed)  

#19 0x11c618972 in \_\_71-[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]\_block\_invoke+0x192 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xc041972)  

#20 0x11b40d369 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xae36369)  

#21 0x11c61850a in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]+0x32a (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xc04150a)  

#22 0x7fffc055f38a in -[NSApplication run]+0x39d (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86\_64+0x3b38a)  

#23 0x11b42178a in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate\*)+0x3da (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xae4a78a)  

#24 0x11b41d368 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*)+0x208 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xae46368)  

#25 0x11b330a1b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x2ab (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xad59a1b)  

#26 0x11b27349b in base::RunLoop::Run()+0x44b (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xac9c49b)  

#27 0x11b93d9e1 in ChromeBrowserMainParts::MainMessageLoopRun(int\*)+0x181 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xb3669e1)  

#28 0x114878269 in content::BrowserMainLoop::RunMainMessageLoopParts()+0x119 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x42a1269)  

#29 0x11487d831 in content::BrowserMainRunnerImpl::Run()+0x31 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x42a6831)  

#30 0x11486fa5c in content::BrowserMain(content::MainFunctionParams const&)+0x2ec (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x4298a5c)  

#31 0x11b050f86 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool)+0xbd6 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xaa79f86)  

#32 0x11b0501f3 in content::ContentMainRunnerImpl::Run(bool)+0x413 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xaa791f3)  

#33 0x11b04cf8b in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*)+0x15ab (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xaa75f8b)  

#34 0x11b04d64c in content::ContentMain(content::ContentMainParams const&)+0xdc (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xaa7664c)  

#35 0x1105ddcf5 in ChromeMain+0x225 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x6cf5)  

#36 0x106e9feff in main+0x1ff (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/MacOS/./chromium:x86\_64+0x100001eff)  

#37 0x7fffd86bf234 in start+0x0 (/usr/lib/system/libdyld.dylib:x86\_64+0x5234)

0x621001894900 is located 0 bytes inside of 4304-byte region [0x621001894900,0x6210018959d0)  

freed by thread T0 here:  

#0 0x107084e79 in \_\_asan\_memmove+0x1d49 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/MacOS/./libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x45e79)  

#1 0x11557f8bf in content::RenderFrameHostManager::~RenderFrameHostManager()+0x42f (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x4fa88bf)  

#2 0x1152a6dde in content::FrameTreeNode::~FrameTreeNode()+0x14ce (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x4ccfdde)  

#3 0x11529de41 in content::FrameTree::~FrameTree()+0x41 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x4cc6e41)  

#4 0x115aaed31 in content::WebContentsImpl::~WebContentsImpl()+0x3eb1 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x54d7d31)  

#5 0x115ab0f6d in content::WebContentsImpl::~WebContentsImpl()+0xd (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x54d9f6d)  

#6 0x126fd48b4 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications\*)+0xd14 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x169fd8b4)  

#7 0x126fdb39f in TabStripModel::InternalCloseTabs(base::span<content::WebContents\* const, 18446744073709551615ul>, unsigned int)+0x66f (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x16a0439f)  

#8 0x126fdbbb0 in TabStripModel::CloseWebContentsAt(int, unsigned int)+0x120 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x16a04bb0)  

#9 0x127b346c1 in TabStrip::CloseTabInternal(int, CloseTabSource)+0x551 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x1755d6c1)  

#10 0x127b33fd5 in TabStrip::CloseTab(Tab\*, CloseTabSource)+0x2d5 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x1755cfd5)  

#11 0x127abe2c8 in Tab::CloseButtonPressed(ui::Event const&)+0x298 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x174e72c8)  

#12 0x1267d0dd8 in views::ButtonController::OnMouseReleased(ui::MouseEvent const&)+0x2b8 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x161f9dd8)  

#13 0x11ea6d2fa in ui::EventHandler::OnEvent(ui::Event\*)+0x40a (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xe4962fa)  

#14 0x11ea79c27 in ui::ScopedTargetHandler::OnEvent(ui::Event\*)+0x157 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xe4a2c27)  

#15 0x11ea6b699 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*)+0x4c9 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xe494699)  

#16 0x11ea6ae74 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*)+0x174 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xe493e74)  

#17 0x11ea6aba0 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*)+0x1c0 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xe493ba0)  

#18 0x126abe2aa in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&)+0x2ca (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x164e72aa)  

#19 0x126ad992b in views::Widget::OnMouseEvent(ui::MouseEvent\*)+0x85b (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x1650292b)  

#20 0x1229c3b7c in -[BridgedContentView mouseEvent:]+0x24c (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x123ecb7c)  

#21 0x1229c0e17 in -[BridgedContentView processCapturedMouseEvent:]+0x3b7 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x123e9e17)  

#22 0x1229cf46b in invocation function for block in remote\_cocoa::CocoaMouseCapture::ActiveEventTap::Init()+0x6b (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x123f846b)  

#23 0x7fffc06eb7f9 in \_NSSendEventToObservers+0x173 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86\_64+0x1c77f9)  

#24 0x7fffc0ce423e in -[NSApplication(NSEvent) sendEvent:]+0x36 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86\_64+0x7c023e)  

#25 0x11c61b5a4 in \_\_34-[BrowserCrApplication sendEvent:]\_block\_invoke+0x294 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xc0445a4)  

#26 0x11b40d369 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xae36369)  

#27 0x11c61a5f6 in -[BrowserCrApplication sendEvent:]+0xb36 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xc0435f6)  

#28 0x7fffc055f3d6 in -[NSApplication run]+0x3e9 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86\_64+0x3b3d6)  

#29 0x11b42178a in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate\*)+0x3da (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xae4a78a)

previously allocated by thread T0 here:  

#0 0x107084d30 in \_\_asan\_memmove+0x1c00 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/MacOS/./libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x45d30)  

#1 0x11b170d67 in operator new(unsigned long)+0x27 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xab99d67)  

#2 0x1154c142e in content::RenderFrameHostFactory::Create(content::SiteInstance\*, scoped\_refptr[content::RenderViewHostImpl](javascript:void(0);), content::RenderFrameHostDelegate\*, content::FrameTree\*, content::FrameTreeNode\*, int, base::UnguessableToken const&, bool, content::RenderFrameHostImpl::LifecycleState)+0x20e (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x4eea42e)  

#3 0x115580983 in content::RenderFrameHostManager::CreateRenderFrameHost(content::RenderFrameHostManager::CreateFrameCase, content::SiteInstance\*, int, base::UnguessableToken const&, bool)+0x3b3 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x4fa9983)  

#4 0x115597cf6 in content::RenderFrameHostManager::CreateSpeculativeRenderFrame(content::SiteInstance\*, bool)+0x186 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x4fc0cf6)  

#5 0x11558dd71 in content::RenderFrameHostManager::CreateSpeculativeRenderFrameHost(content::SiteInstance\*, content::SiteInstance\*, bool)+0x1c1 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x4fb6d71)  

#6 0x11558b7ba in content::RenderFrameHostManager::GetFrameHostForNavigation(content::NavigationRequest\*, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >\*)+0x96a (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x4fb47ba)  

#7 0x11558ad50 in content::RenderFrameHostManager::DidCreateNavigationRequest(content::NavigationRequest\*)+0x1b0 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x4fb3d50)  

#8 0x1152acc50 in content::FrameTreeNode::CreatedNavigationRequest(std::\_\_1::unique\_ptr<content::NavigationRequest, std::\_\_1::default\_delete[content::NavigationRequest](javascript:void(0);) >)+0x200 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x4cd5c50)  

#9 0x1154afba6 in content::Navigator::Navigate(std::\_\_1::unique\_ptr<content::NavigationRequest, std::\_\_1::default\_delete[content::NavigationRequest](javascript:void(0);) >, content::ReloadType)+0x626 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x4ed8ba6)  

#10 0x11540de86 in content::NavigationControllerImpl::NavigateWithoutEntry(content::NavigationController::LoadURLParams const&)+0xaf6 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x4e36e86)  

#11 0x11540cf0e in content::NavigationControllerImpl::LoadURLWithParams(content::NavigationController::LoadURLParams const&)+0x23e (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x4e35f0e)  

#12 0x126e2259e in (anonymous namespace)::LoadURLInContents(content::WebContents\*, GURL const&, NavigateParams\*)+0xa9e (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x1684b59e)  

#13 0x126e1fc5a in Navigate(NavigateParams\*)+0x29ba (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x16848c5a)  

#14 0x126dfda3d in chrome::OpenCurrentURL(Browser\*)+0x37d (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x16826a3d)  

#15 0x126df816f in chrome::BrowserCommandController::ExecuteCommandWithDisposition(int, WindowOpenDisposition, base::TimeTicks)+0xfdf (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x1682116f)  

#16 0x126f238c0 in ChromeOmniboxEditController::OnAutocompleteAccept(GURL const&, std::\_\_1::pair<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > >\*, WindowOpenDisposition, ui::PageTransition, AutocompleteMatchType::Type, base::TimeTicks, bool)+0x80 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x1694c8c0)  

#17 0x125d738cd in OmniboxEditModel::OpenMatch(AutocompleteMatch, WindowOpenDisposition, GURL const&, std::\_\_1::basic\_string<char16\_t, std::\_\_1::char\_traits<char16\_t>, std::\_\_1::allocator<char16\_t> > const&, unsigned long, base::TimeTicks)+0x2fad (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x1579c8cd)  

#18 0x125dc794e in OmniboxView::OpenMatch(AutocompleteMatch const&, WindowOpenDisposition, GURL const&, std::\_\_1::basic\_string<char16\_t, std::\_\_1::char\_traits<char16\_t>, std::\_\_1::allocator<char16\_t> > const&, unsigned long, base::TimeTicks)+0x14e (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x157f094e)  

#19 0x125d6d3a5 in OmniboxEditModel::AcceptInput(WindowOpenDisposition, base::TimeTicks)+0xef5 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x157963a5)  

#20 0x127878f33 in OmniboxViewViews::HandleKeyEvent(views::Textfield\*, ui::KeyEvent const&)+0xdd3 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x172a1f33)  

#21 0x126971459 in views::Textfield::OnKeyPressed(ui::KeyEvent const&)+0x1a9 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x1639a459)  

#22 0x126a894bf in non-virtual thunk to views::View::OnKeyEvent(ui::KeyEvent\*)+0x7f (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x164b24bf)  

#23 0x11ea6d2fa in ui::EventHandler::OnEvent(ui::Event\*)+0x40a (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xe4962fa)  

#24 0x11ea6b699 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*)+0x4c9 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xe494699)  

#25 0x11ea6ae74 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*)+0x174 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xe493e74)  

#26 0x11ea6aba0 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*)+0x1c0 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xe493ba0)  

#27 0x11ea6e8ad in ui::EventProcessor::OnEventFromSource(ui::Event\*)+0x37d (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xe4978ad)  

#28 0x11ea6f8f9 in ui::EventSource::DeliverEventToSink(ui::Event\*)+0x159 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xe4988f9)  

#29 0x11ea6f563 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*)+0x5d3 (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0xe498563)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/iamtech/Desktop/asan-mac-release-843619/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/89.0.4389.0/Chromium Framework:x86\_64+0x16104617) in content::InternalAuthenticatorImpl::~InternalAuthenticatorImpl()+0x137  

Shadow bytes around the buggy address:  

0x1c42003128d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c42003128e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c42003128f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c4200312900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c4200312910: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x1c4200312920:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c4200312930: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c4200312940: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c4200312950: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c4200312960: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c4200312970: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

Shadow gap: cc

## Attachments

- [payment_request_new.html](attachments/payment_request_new.html) (text/plain, 307 B)
- [payment_request2_new.html](attachments/payment_request2_new.html) (text/plain, 764 B)
- deleted (application/octet-stream, 0 B)
- [screen .mov](attachments/screen .mov) (video/quicktime, 5.2 MB)

## Timeline

### [Deleted User] (2021-01-21)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-01-21)

[Comment Deleted]

### ch...@gmail.com (2021-01-21)

[Comment Deleted]

### ch...@gmail.com (2021-01-21)

Please ensure that ensure that #enable-experimental-web-platform-features is enabled.

This affects only macOS-only, I couldn't repro on other platforms.



### va...@chromium.org (2021-01-22)

crash reports at: http://shortn/_egJHRiQGlJ

### va...@chromium.org (2021-01-22)

[Empty comment from Monorail migration]

[Monorail components: Blink>Payments]

### va...@chromium.org (2021-01-22)

Please note that I haven't reproduce it yet. The security labels are based on the crash reports and the amount of user interaction (minimal and reasonable).

### ro...@chromium.org (2021-01-22)

vakh@ - is this UaF significant enough for us to cut the origin trial short? We may have collected enough data, IMHO, but the origin trial is set to expire in M-90, which hit stable in April. (This code path can be enabled either through flags or in an origin trial.)

### ro...@chromium.org (2021-01-22)

The easiest fix is to replace the RenderFrameHost* pointer with a GlobalFrameRoutingId here:

https://source.chromium.org/chromium/chromium/src/+/master:components/autofill/content/browser/webauthn/internal_authenticator_impl.h;l=65;drc=6dcf7e9dc54105f8e38df5ab760b6c3d3c356004

This is what the rest of the payments code does.

### [Deleted User] (2021-01-22)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-22)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2021-01-22)

> vakh@ - is this UaF significant enough for us to cut the origin trial short?

I'd recommend that, at least for the affected versions of Chrome (90.* only?)

### np...@chromium.org (2021-01-22)

I have a fix up for review now that works in my local build: https://chromium-review.googlesource.com/c/chromium/src/+/2644743

I'll look into the affected chrome versions now.

### np...@chromium.org (2021-01-22)

Looks like all versions (since at least 88) are affected, so we can cut the Origin Trial short. Without the origin trial, this bug is locked behind a flag that's disabled by default.

### np...@chromium.org (2021-01-22)

vakh@: Is it possible for the fix be merged to M-88 stable so we can continue the origin trial?

### ad...@google.com (2021-01-22)

Adjusting Security_Impact per https://crbug.com/chromium/1169317#c14.

Yes, we can merge this to the next M88 stable security refresh, which will be in about 10 days. Please get the fix landed on ToT, and then mark this crbug as Fixed, and Sheriffbot will apply appropriate merge request labels.

Please stop the origin trial meanwhile.

### ro...@chromium.org (2021-01-22)

[Empty comment from Monorail migration]

### ro...@chromium.org (2021-01-22)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3f4e1b8a33997807dea04089beb96e62967a53b1

commit 3f4e1b8a33997807dea04089beb96e62967a53b1
Author: Nick Burris <nburris@chromium.org>
Date: Sat Jan 23 01:00:37 2021

Ensure SecurePaymentConfirmationAppFactory owns InternalAuthenticator

This patch ensures that the InternalAuthenticator created by
SecurePaymentConfirmationAppFactory is always owned by a
WebContentsObserver, to ensure that the authenticator is outlived by
its RenderFrameHost.

Bug: 1169317
Change-Id: Ie22c3796d642589f912b880bcdadeb3badde8180
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2644743
Commit-Queue: Nick Burris <nburris@chromium.org>
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Auto-Submit: Nick Burris <nburris@chromium.org>
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#846426}

[modify] https://crrev.com/3f4e1b8a33997807dea04089beb96e62967a53b1/components/payments/content/secure_payment_confirmation_app_factory.cc
[modify] https://crrev.com/3f4e1b8a33997807dea04089beb96e62967a53b1/components/payments/content/secure_payment_confirmation_app_factory.h


### ch...@gmail.com (2021-01-23)

Thanks for the quick fix! 

Verified on Chromium 90.0.4397.0 refs/heads/master@{#846445}. Fixed.

### np...@chromium.org (2021-01-25)

Thanks for verifying! Marking fixed to get merge approval.

### [Deleted User] (2021-01-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-25)

Requesting merge to stable M88 because latest trunk commit (846426) appears to be after stable branch point (1784).

Requesting merge to beta M88 because latest trunk commit (846426) appears to be after beta branch point (1784).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-25)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### np...@chromium.org (2021-01-25)

1. Yes
2. https://chromium-review.googlesource.com/c/chromium/src/+/2644743
3. Yes
4. Yes, M89 as well.
5. Critical security bug fix
6. No
7. N/A
Note this fix is for a feature that is behind an origin trial feature flag which will be disabled until the fix is released.

### np...@chromium.org (2021-01-26)

Reopening for merge review to M88 and M89

### ad...@google.com (2021-01-26)

Thanks. For security bugs we do merges after they're marked fixed. Due to a known Sheriffbot bug this didn't get a M89 merge request, bah. Approving merge to M89, branch 4389. I'll approve M88 merge requests at a later date.

### ad...@google.com (2021-01-27)

Approving merge to M88, branch 4324.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/db7fc09956e866e7a473d6f65199b2ef80b853e2

commit db7fc09956e866e7a473d6f65199b2ef80b853e2
Author: Nick Burris <nburris@chromium.org>
Date: Wed Jan 27 17:49:24 2021

Ensure SecurePaymentConfirmationAppFactory owns InternalAuthenticator

[Merge to M89]
This patch ensures that the InternalAuthenticator created by
SecurePaymentConfirmationAppFactory is always owned by a
WebContentsObserver, to ensure that the authenticator is outlived by
its RenderFrameHost.

(cherry picked from commit 3f4e1b8a33997807dea04089beb96e62967a53b1)

Bug: 1169317
Change-Id: Ie22c3796d642589f912b880bcdadeb3badde8180
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2644743
Commit-Queue: Nick Burris <nburris@chromium.org>
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Auto-Submit: Nick Burris <nburris@chromium.org>
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#846426}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2650757
Cr-Commit-Position: refs/branch-heads/4389@{#318}
Cr-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}

[modify] https://crrev.com/db7fc09956e866e7a473d6f65199b2ef80b853e2/components/payments/content/secure_payment_confirmation_app_factory.cc
[modify] https://crrev.com/db7fc09956e866e7a473d6f65199b2ef80b853e2/components/payments/content/secure_payment_confirmation_app_factory.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/54115f8cf2db30cb781dab136a2df1c0a76412f0

commit 54115f8cf2db30cb781dab136a2df1c0a76412f0
Author: Nick Burris <nburris@chromium.org>
Date: Wed Jan 27 19:28:15 2021

Ensure SecurePaymentConfirmationAppFactory owns InternalAuthenticator

[Merge to M88]
This patch ensures that the InternalAuthenticator created by
SecurePaymentConfirmationAppFactory is always owned by a
WebContentsObserver, to ensure that the authenticator is outlived by
its RenderFrameHost.

(cherry picked from commit 3f4e1b8a33997807dea04089beb96e62967a53b1)

Bug: 1169317
Change-Id: Ie22c3796d642589f912b880bcdadeb3badde8180
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2644743
Commit-Queue: Nick Burris <nburris@chromium.org>
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Auto-Submit: Nick Burris <nburris@chromium.org>
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#846426}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2653568
Cr-Commit-Position: refs/branch-heads/4324@{#2026}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/54115f8cf2db30cb781dab136a2df1c0a76412f0/components/payments/content/secure_payment_confirmation_app_factory.cc
[modify] https://crrev.com/54115f8cf2db30cb781dab136a2df1c0a76412f0/components/payments/content/secure_payment_confirmation_app_factory.h


### am...@google.com (2021-01-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-27)

Congratulations, Khalil! The VRP Panel has decided to award you $20,000 for this report. Nice work! 

### am...@google.com (2021-01-28)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-31)

[Empty comment from Monorail migration]

### as...@google.com (2021-02-02)

Adding LTS labels and marking NotApplicable as per https://crbug.com/chromium/1169317#c4 (macOS-only).

### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1169317?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054539)*

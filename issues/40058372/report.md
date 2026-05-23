# Heap-use-after-free in ChromePermissionsClient::OverrideCanonicalOrigin

| Field | Value |
|-------|-------|
| **Issue ID** | [40058372](https://issues.chromium.org/issues/40058372) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>MediaStream |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | sa...@gmail.com |
| **Assignee** | he...@google.com |
| **Created** | 2021-12-30 |
| **Bounty** | $15,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36

Steps to reproduce the problem:
1. Install and open the extension. 

What is the expected behavior?

What went wrong?
=================================================================
==9200==ERROR: AddressSanitizer: heap-use-after-free on address 0x11d578b1385c at pc 0x7ffb211ef698 bp 0x000ecb5fdd80 sp 0x000ecb5fddc8
READ of size 4 at 0x11d578b1385c thread T0
==9200==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffb211ef697 in GURL::SchemeIs C:\b\s\w\ir\cache\builder\src\url\gurl.cc:352
    #1 0x7ffb2a7d28f7 in ChromePermissionsClient::OverrideCanonicalOrigin C:\b\s\w\ir\cache\builder\src\chrome\browser\permissions\chrome_permissions_client.cc:349
    #2 0x7ffb1bb1edf6 in permissions::PermissionManager::GetCanonicalOrigin C:\b\s\w\ir\cache\builder\src\components\permissions\permission_manager.cc:327
    #3 0x7ffb1bb1f608 in permissions::PermissionManager::RequestPermissions C:\b\s\w\ir\cache\builder\src\components\permissions\permission_manager.cc:386
    #4 0x7ffb1c93c531 in webrtc::MediaStreamDevicesController::RequestPermissions C:\b\s\w\ir\cache\builder\src\components\webrtc\media_stream_devices_controller.cc:141
    #5 0x7ffb269ba5fc in PermissionBubbleMediaAccessHandler::ProcessQueuedAccessRequest C:\b\s\w\ir\cache\builder\src\chrome\browser\media\webrtc\permission_bubble_media_access_handler.cc:249
    #6 0x7ffb269ba20d in PermissionBubbleMediaAccessHandler::HandleRequest C:\b\s\w\ir\cache\builder\src\chrome\browser\media\webrtc\permission_bubble_media_access_handler.cc:219
    #7 0x7ffb236eec21 in MediaCaptureDevicesDispatcher::ProcessMediaAccessRequest C:\b\s\w\ir\cache\builder\src\chrome\browser\media\webrtc\media_capture_devices_dispatcher.cc:162
    #8 0x7ffb2da6f4e4 in extensions::ChromeExtensionHostDelegate::ProcessMediaAccessRequest C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\chrome_extension_host_delegate.cc:67
    #9 0x7ffb1be50106 in extensions::ExtensionHost::RequestMediaAccessPermission C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_host.cc:424
    #10 0x7ffb1aed443b in content::WebContentsImpl::RequestMediaAccessPermission C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:4216
    #11 0x7ffb1a970641 in content::MediaStreamUIProxy::Core::RequestAccess C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\media\media_stream_ui_proxy.cc:138
    #12 0x7ffb1a976236 in base::internal::Invoker<base::internal::BindState<void (content::MediaStreamUIProxy::Core::*)(std::__1::unique_ptr<content::MediaStreamRequest,std::__1::default_delete<content::MediaStreamRequest> >),base::WeakPtr<content::MediaStreamUIProxy::Core>,std::__1::unique_ptr<content::MediaStreamRequest,std::__1::default_delete<content::MediaStreamRequest> > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:741
    #13 0x7ffb20e34814 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #14 0x7ffb23960f85 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356
    #15 0x7ffb23960658 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #16 0x7ffb20edd366 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #17 0x7ffb20edb5f8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #18 0x7ffb23962651 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468
    #19 0x7ffb20db3383 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
    #20 0x7ffb19fcec31 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1048
    #21 0x7ffb19fd4051 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:153
    #22 0x7ffb19fc82b9 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #23 0x7ffb1ca599d3 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:646
    #24 0x7ffb1ca5ca13 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1160
    #25 0x7ffb1ca5bb46 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1026
    #26 0x7ffb1ca57e1d in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398
    #27 0x7ffb1ca58ea8 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:426
    #28 0x7ffb1631148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:177
    #29 0x7ff7c7305b85 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #30 0x7ff7c7302b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #31 0x7ff7c770753f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #32 0x7ffbd16054df in BaseThreadInitThunk+0xf (C:\WINDOWS\System32\KERNEL32.DLL+0x1800154df)
    #33 0x7ffbd22c485a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18000485a)

0x11d578b1385c is located 92 bytes inside of 256-byte region [0x11d578b13800,0x11d578b13900)
freed by thread T0 here:
    #0 0x7ff7c73b23fb in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffb269bd36f in std::__1::__tree<std::__1::__value_type<long long,PermissionBubbleMediaAccessHandler::PendingAccessRequest>,std::__1::__map_value_compare<long long,std::__1::__value_type<long long,PermissionBubbleMediaAccessHandler::PendingAccessRequest>,std::__1::less<long long>,1>,std::__1::allocator<std::__1::__value_type<long long,PermissionBubbleMediaAccessHandler::PendingAccessRequest> > >::erase C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__tree:2424
    #2 0x7ffb269bc663 in PermissionBubbleMediaAccessHandler::OnAccessRequestResponse C:\b\s\w\ir\cache\builder\src\chrome\browser\media\webrtc\permission_bubble_media_access_handler.cc:416
    #3 0x7ffb269bb738 in PermissionBubbleMediaAccessHandler::OnMediaStreamRequestResponse C:\b\s\w\ir\cache\builder\src\chrome\browser\media\webrtc\permission_bubble_media_access_handler.cc:322
    #4 0x7ffb269bd262 in base::internal::Invoker<base::internal::BindState<void (PermissionBubbleMediaAccessHandler::*)(content::WebContents *, long long, content::MediaStreamRequest, const std::__1::vector<blink::MediaStreamDevice,std::__1::allocator<blink::MediaStreamDevice> > &, blink::mojom::MediaStreamRequestResult, bool, ContentSetting, ContentSetting),base::internal::UnretainedWrapper<PermissionBubbleMediaAccessHandler>,base::internal::UnretainedWrapper<content::WebContents>,long long,content::MediaStreamRequest>,void (const std::__1::vector<blink::MediaStreamDevice,std::__1::allocator<blink::MediaStreamDevice> > &, blink::mojom::MediaStreamRequestResult, bool, ContentSetting, ContentSetting)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:741
    #5 0x7ffb1c93d62f in webrtc::MediaStreamDevicesController::~MediaStreamDevicesController C:\b\s\w\ir\cache\builder\src\components\webrtc\media_stream_devices_controller.cc:152
    #6 0x7ffb1c93eb0f in std::__1::unique_ptr<webrtc::MediaStreamDevicesController,std::__1::default_delete<webrtc::MediaStreamDevicesController> >::reset C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:315
    #7 0x7ffb1c93ed69 in base::internal::BindState<void (*)(content::WebContents *, std::__1::unique_ptr<webrtc::MediaStreamDevicesController,std::__1::default_delete<webrtc::MediaStreamDevicesController> >, bool, bool, const std::__1::vector<ContentSetting,std::__1::allocator<ContentSetting> > &),base::internal::UnretainedWrapper<content::WebContents>,std::__1::unique_ptr<webrtc::MediaStreamDevicesController,std::__1::default_delete<webrtc::MediaStreamDevicesController> >,bool,bool>::Destroy C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:974
    #8 0x7ffb1bb2760d in std::__1::default_delete<permissions::PermissionManager::PendingRequest>::operator() C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:54
    #9 0x7ffb1bb275b7 in std::__1::__hash_node_destructor<std::__1::allocator<std::__1::__hash_node<std::__1::__hash_value_type<base::IdType<permissions::PermissionRequestID,long long,0,1>,std::__1::unique_ptr<permissions::PermissionManager::PendingRequest,std::__1::default_delete<permissions::PermissionManager::PendingRequest> > >,void *> > >::operator() C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__hash_table:849
    #10 0x7ffb1bb274db in std::__1::__hash_table<std::__1::__hash_value_type<base::IdType<permissions::PermissionRequestID,long long,0,1>,std::__1::unique_ptr<permissions::PermissionManager::PendingRequest,std::__1::default_delete<permissions::PermissionManager::PendingRequest> > >,std::__1::__unordered_map_hasher<base::IdType<permissions::PermissionRequestID,long long,0,1>,std::__1::__hash_value_type<base::IdType<permissions::PermissionRequestID,long long,0,1>,std::__1::unique_ptr<permissions::PermissionManager::PendingRequest,std::__1::default_delete<permissions::PermissionManager::PendingRequest> > >,std::__1::hash<base::IdType<permissions::PermissionRequestID,long long,0,1> >,std::__1::equal_to<base::IdType<permissions::PermissionRequestID,long long,0,1> >,1>,std::__1::__unordered_map_equal<base::IdType<permissions::PermissionRequestID,long long,0,1>,std::__1::__hash_value_type<base::IdType<permissions::PermissionRequestID,long long,0,1>,std::__1::unique_ptr<permissions::PermissionManager::PendingRequest,std::__1::default_delete<permissions::PermissionManager::PendingRequest> > >,std::__1::equal_to<base::IdType<permissions::PermissionRequestID,long long,0,1> >,std::__1::hash<base::IdType<permissions::PermissionRequestID,long long,0,1> >,1>,std::__1::allocator<std::__1::__hash_value_type<base::IdType<permissions::PermissionRequestID,long long,0,1>,std::__1::unique_ptr<permissions::PermissionManager::PendingRequest,std::__1::default_delete<permissions::PermissionManager::PendingRequest> > > > >::erase C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__hash_table:2498
    #11 0x7ffb1bb228d3 in base::IDMap<std::__1::unique_ptr<permissions::PermissionManager::PendingRequest,std::__1::default_delete<permissions::PermissionManager::PendingRequest> >,base::IdType<permissions::PermissionRequestID,long long,0,1> >::Remove C:\b\s\w\ir\cache\builder\src\base\containers\id_map.h:87
    #12 0x7ffb1bb2b2a9 in std::__1::unique_ptr<permissions::PermissionManager::PermissionResponseCallback,std::__1::default_delete<permissions::PermissionManager::PermissionResponseCallback> >::reset C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:315
    #13 0x7ffb1bb2b39d in base::internal::BindState<void (permissions::PermissionManager::PermissionResponseCallback::*)(ContentSetting),std::__1::unique_ptr<permissions::PermissionManager::PermissionResponseCallback,std::__1::default_delete<permissions::PermissionManager::PermissionResponseCallback> > >::Destroy C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:974
    #14 0x7ffb1bb17546 in permissions::PermissionContextBase::DecidePermission C:\b\s\w\ir\cache\builder\src\components\permissions\permission_context_base.cc:430
    #15 0x7ffb2b376ec7 in MediaStreamDevicePermissionContext::DecidePermission C:\b\s\w\ir\cache\builder\src\chrome\browser\media\webrtc\media_stream_device_permission_context.cc:49
    #16 0x7ffb1bb15368 in permissions::PermissionContextBase::RequestPermission C:\b\s\w\ir\cache\builder\src\components\permissions\permission_context_base.cc:221
    #17 0x7ffb1bb1f954 in permissions::PermissionManager::RequestPermissions C:\b\s\w\ir\cache\builder\src\components\permissions\permission_manager.cc:401
    #18 0x7ffb1c93c531 in webrtc::MediaStreamDevicesController::RequestPermissions C:\b\s\w\ir\cache\builder\src\components\webrtc\media_stream_devices_controller.cc:141
    #19 0x7ffb269ba5fc in PermissionBubbleMediaAccessHandler::ProcessQueuedAccessRequest C:\b\s\w\ir\cache\builder\src\chrome\browser\media\webrtc\permission_bubble_media_access_handler.cc:249
    #20 0x7ffb269ba20d in PermissionBubbleMediaAccessHandler::HandleRequest C:\b\s\w\ir\cache\builder\src\chrome\browser\media\webrtc\permission_bubble_media_access_handler.cc:219
    #21 0x7ffb236eec21 in MediaCaptureDevicesDispatcher::ProcessMediaAccessRequest C:\b\s\w\ir\cache\builder\src\chrome\browser\media\webrtc\media_capture_devices_dispatcher.cc:162
    #22 0x7ffb2da6f4e4 in extensions::ChromeExtensionHostDelegate::ProcessMediaAccessRequest C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\chrome_extension_host_delegate.cc:67
    #23 0x7ffb1be50106 in extensions::ExtensionHost::RequestMediaAccessPermission C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_host.cc:424
    #24 0x7ffb1aed443b in content::WebContentsImpl::RequestMediaAccessPermission C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:4216
    #25 0x7ffb1a970641 in content::MediaStreamUIProxy::Core::RequestAccess C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\media\media_stream_ui_proxy.cc:138
    #26 0x7ffb1a976236 in base::internal::Invoker<base::internal::BindState<void (content::MediaStreamUIProxy::Core::*)(std::__1::unique_ptr<content::MediaStreamRequest,std::__1::default_delete<content::MediaStreamRequest> >),base::WeakPtr<content::MediaStreamUIProxy::Core>,std::__1::unique_ptr<content::MediaStreamRequest,std::__1::default_delete<content::MediaStreamRequest> > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:741
    #27 0x7ffb20e34814 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135

previously allocated by thread T0 here:
    #0 0x7ff7c73b24fb in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffb335f6dbe in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ffb269bce38 in std::__1::__tree<std::__1::__value_type<long long,PermissionBubbleMediaAccessHandler::PendingAccessRequest>,std::__1::__map_value_compare<long long,std::__1::__value_type<long long,PermissionBubbleMediaAccessHandler::PendingAccessRequest>,std::__1::less<long long>,1>,std::__1::allocator<std::__1::__value_type<long long,PermissionBubbleMediaAccessHandler::PendingAccessRequest> > >::__emplace_unique_key_args<long long,long long,PermissionBubbleMediaAccessHandler::PendingAccessRequest> C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__tree:2096
    #3 0x7ffb269ba17e in PermissionBubbleMediaAccessHandler::HandleRequest C:\b\s\w\ir\cache\builder\src\chrome\browser\media\webrtc\permission_bubble_media_access_handler.cc:214
    #4 0x7ffb236eec21 in MediaCaptureDevicesDispatcher::ProcessMediaAccessRequest C:\b\s\w\ir\cache\builder\src\chrome\browser\media\webrtc\media_capture_devices_dispatcher.cc:162
    #5 0x7ffb2da6f4e4 in extensions::ChromeExtensionHostDelegate::ProcessMediaAccessRequest C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\chrome_extension_host_delegate.cc:67
    #6 0x7ffb1be50106 in extensions::ExtensionHost::RequestMediaAccessPermission C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_host.cc:424
    #7 0x7ffb1aed443b in content::WebContentsImpl::RequestMediaAccessPermission C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:4216
    #8 0x7ffb1a970641 in content::MediaStreamUIProxy::Core::RequestAccess C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\media\media_stream_ui_proxy.cc:138
    #9 0x7ffb1a976236 in base::internal::Invoker<base::internal::BindState<void (content::MediaStreamUIProxy::Core::*)(std::__1::unique_ptr<content::MediaStreamRequest,std::__1::default_delete<content::MediaStreamRequest> >),base::WeakPtr<content::MediaStreamUIProxy::Core>,std::__1::unique_ptr<content::MediaStreamRequest,std::__1::default_delete<content::MediaStreamRequest> > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:741
    #10 0x7ffb20e34814 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #11 0x7ffb23960f85 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356
    #12 0x7ffb23960658 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #13 0x7ffb20edd366 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #14 0x7ffb20edb5f8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #15 0x7ffb23962651 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468
    #16 0x7ffb20db3383 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
    #17 0x7ffb19fcec31 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1048
    #18 0x7ffb19fd4051 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:153
    #19 0x7ffb19fc82b9 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #20 0x7ffb1ca599d3 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:646
    #21 0x7ffb1ca5ca13 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1160
    #22 0x7ffb1ca5bb46 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1026
    #23 0x7ffb1ca57e1d in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398
    #24 0x7ffb1ca58ea8 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:426
    #25 0x7ffb1631148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:177
    #26 0x7ff7c7305b85 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #27 0x7ff7c7302b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\url\gurl.cc:352 in GURL::SchemeIs
Shadow bytes around the buggy address:
  0x03ee278626b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x03ee278626c0: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x03ee278626d0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x03ee278626e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x03ee278626f0: fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x03ee27862700: fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd
  0x03ee27862710: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x03ee27862720: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x03ee27862730: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x03ee27862740: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x03ee27862750: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
==9200==ABORTING

Did this work before? N/A 

Chrome version: 96.0.4664.110  Channel: stable
OS Version: 10.0

Thanks,

Samet Bekmezci @sametbekmezci

## Attachments

- asan.log (text/plain, 20.2 KB)
- PoC.zip (application/octet-stream, 578 B)
- base.html (text/plain, 69 B)
- manifest.json (text/plain, 124 B)
- script.js (text/plain, 63 B)
- poc.mp4 (video/mp4, 4.7 MB)

## Timeline

### [Deleted User] (2021-12-30)

[Empty comment from Monorail migration]

### sa...@gmail.com (2021-12-30)

Sorry forgot to share the extension:

### dr...@chromium.org (2022-01-04)

Can you give a little more details about the reproduction requirements? Installing and opening the extension, I just get an error "Uncaught (in promise) NotFoundError: Requested device not found"

### sa...@gmail.com (2022-01-04)

Hi drubery@, I am sharing a video with steps to reproduce it. If the problem is not fixed, I am sharing the codes for you to create the plugin yourself.

### [Deleted User] (2022-01-04)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2022-01-04)

It seems that this strictly requires having a camera/microphone on your test device. Even addressing that, I still can't reproduce this. https://bugs.chromium.org/p/chromium/issues/detail?id=160337 suggests that it's not possible to call getUserMedia from an extension page (with the exact error I'm seeing, "Failed due to shutdown"). I'm not sure why you're seeing a crash.

Forwarding this to guidou@, just in case I missed something about the setup for media streams. guidou@ - let me know if you manage to reproduce this.

[Monorail components: Blink>MediaStream]

### to...@chromium.org (2022-01-05)

I can take this, as Guido has moved teams.

I've got a repro (and on a machine without a hardware cam/mic, using the handy flag "--use-fake-device-for-media-stream"). Seems the difference to crbug/160337 etc is that this is actually using an extension popup rather than a background page to run gUM, which does usually work.

### dr...@chromium.org (2022-01-06)

That flag would definitely have been helpful! Thanks for reproducing!

I've marked this FoundIn-96, since the original report says this is possible in M96. Let me know if you find some evidence this can't be reproduced that far back.

### [Deleted User] (2022-01-06)

[Empty comment from Monorail migration]

### to...@chromium.org (2022-01-07)

Spent a while digging into the cause. We do indeed hit the same error as other calls by extension pages, which causes the content::MediaStreamRequest to be destroyed, but as both Audio and Video are being requested here, the per-permission loop in PermissionManager::RequestPermissions [1] runs a second time, so calling GetCanonicalOrigin() on the destroyed requesting_origin causes this UAF.

I'm still trying to get my head around how this should work for multiple permissions being requested in the happy path before finding a good fix for this.


[1]: https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/permission_manager.cc;drc=26479386abe0c05c9661f6d8c1412dde636d8ecb;l=383

### [Deleted User] (2022-01-07)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-07)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2022-01-10)

[Empty comment from Monorail migration]

### to...@chromium.org (2022-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-13)

herre: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### he...@google.com (2022-01-26)

Likely won't have time soon to think through and find a full fix for making gUM calls in extension pages work in a sane way, so will just do a quick fix to take a copy of the URL which might get destroyed after the first loop. That at least closes this security bug. Filed crbug.com/1291201 to follow up on redesigning the whole thing.

### he...@google.com (2022-01-26)

+orphis for context when reviewing.

### gi...@appspot.gserviceaccount.com (2022-01-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cb6778fb965e2b010922f157c68480de863c252e

commit cb6778fb965e2b010922f157c68480de863c252e
Author: Tony Herre <toprice@chromium.org>
Date: Fri Jan 28 12:37:20 2022

Switch to new RequestPermissionsFromCurrentDocument API method for Media Stream Devices

Switch away from the deprecated RequestPermissions() API, as a part of removing a bug where the previously provided request.security_origin param might get destroyed during the method execution.

Bug: 1283402
Change-Id: I512ce910146ec60d4d35fa1a86a71a3b0983a5d1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3417436
Reviewed-by: Florent Castelli <orphis@chromium.org>
Commit-Queue: Tony Herre <toprice@chromium.org>
Cr-Commit-Position: refs/heads/main@{#964535}

[modify] https://crrev.com/cb6778fb965e2b010922f157c68480de863c252e/components/webrtc/media_stream_devices_controller.cc


### he...@google.com (2022-01-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-11)

Congratulations, Samet! The VRP Panel has decided to award you $15,000 for this report. Thank you for reporting this issue and excellent work! 

### am...@google.com (2022-02-14)

[Empty comment from Monorail migration]

### he...@google.com (2022-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-16)

Merge review required: M99 is already shipping to beta.

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

### he...@google.com (2022-02-16)

1) Meets requirements as this is a security bug
2) crrev.com/c/3417436
3) Yes, tested on canary
4) NA
5) NA
6) No

### am...@chromium.org (2022-02-17)

Merge approved to M99, please merge to branch 4758 at your earliest convenience

### pb...@google.com (2022-02-17)

[Bulk update] Your change has been approved for M99 branch please refer to go/chrome-branches for branch info and merge the CL's to M99 branch manually asap so that they would be part of next week's M99 Beta release.

### he...@google.com (2022-02-18)

Branch 4758 is M98 - guess it was miscopied in #28?

Started a CP to 99,  refs/branch-heads/4844, in crrev.com/c/3473365

### gi...@appspot.gserviceaccount.com (2022-02-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/246c10dede97d21787c0ce57fa3032f6470954b3

commit 246c10dede97d21787c0ce57fa3032f6470954b3
Author: Tony Herre <toprice@chromium.org>
Date: Fri Feb 18 13:52:01 2022

[CherryPick to 99] Switch to new RequestPermissionsFromCurrentDocument API method for Media Stream Devices

Switch away from the deprecated RequestPermissions() API, as a part of removing a bug where the previously provided request.security_origin param might get destroyed during the method execution.

(cherry picked from commit cb6778fb965e2b010922f157c68480de863c252e)

Bug: 1283402
Change-Id: I512ce910146ec60d4d35fa1a86a71a3b0983a5d1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3417436
Reviewed-by: Florent Castelli <orphis@chromium.org>
Commit-Queue: Tony Herre <toprice@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#964535}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3473365
Cr-Commit-Position: refs/branch-heads/4844@{#655}
Cr-Branched-From: 007241ce2e6c8e5a7b306cc36c730cd07cd38825-refs/heads/main@{#961656}

[modify] https://crrev.com/246c10dede97d21787c0ce57fa3032f6470954b3/components/webrtc/media_stream_devices_controller.cc


### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1283402?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058372)*

# Security: container-overflow in RecordEngagementMetric

| Field | Value |
|-------|-------|
| **Issue ID** | [40057026](https://issues.chromium.org/issues/40057026) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2021-08-26 |
| **Bounty** | $20,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36

Steps to reproduce the problem:
1. download asan-linux-release-915402.zip and uznip chrome
2. `python copy_mojo_js_bindings.py path/to/ASAN/gen/` and copy poc.html to the same folder
3. start a server at poc.html's folder : python -m SimpleHTTPServer 8605
4. ASAN/chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/noexist http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html http://127.0.0.1:8605/poc.html

What is the expected behavior?

What went wrong?

=================================================================
==2350113==ERROR: AddressSanitizer: container-overflow on address 0x602000b47690 at pc 0x55eeb084958a bp 0x7fff2e33da30 sp 0x7fff2e33da28
READ of size 8 at 0x602000b47690 thread T0 (chrome)
    #0 0x55eeb0849589 in RecordEngagementMetric components/permissions/permission_uma_util.cc:175:33
    #1 0x55eeb0849589 in permissions::PermissionUmaUtil::PermissionPromptResolved(std::__1::vector<permissions::PermissionRequest*, std::__1::allocator<permissions::PermissionRequest*> > const&, content::WebContents*, permissions::PermissionAction, base::TimeDelta, permissions::PermissionPromptDisposition, absl::optional<permissions::PermissionPromptDispositionReason>, absl::optional<permissions::PermissionPrediction_Likelihood_DiscretizedLikelihood>) components/permissions/permission_uma_util.cc:501:3
    #2 0x55eeb08394bc in permissions::PermissionRequestManager::FinalizeCurrentRequests(permissions::PermissionAction) components/permissions/permission_request_manager.cc:712:3
    #3 0x55eeb083c8f3 in permissions::PermissionRequestManager::ShowBubble() components/permissions/permission_request_manager.cc:645:5
    #4 0x55eeb0844524 in Invoke<void (permissions::PermissionRequestManager::*)(), base::WeakPtr<permissions::PermissionRequestManager>> base/bind_internal.h:509:12
    #5 0x55eeb0844524 in MakeItSo<void (permissions::PermissionRequestManager::*)(), base::WeakPtr<permissions::PermissionRequestManager>> base/bind_internal.h:668:5
    #6 0x55eeb0844524 in RunImpl<void (permissions::PermissionRequestManager::*)(), std::__1::tuple<base::WeakPtr<permissions::PermissionRequestManager> >, 0UL> base/bind_internal.h:721:12
    #7 0x55eeb0844524 in base::internal::Invoker<base::internal::BindState<void (permissions::PermissionRequestManager::*)(), base::WeakPtr<permissions::PermissionRequestManager> >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #8 0x55eeb7df34a0 in Run base/callback.h:98:12
    #9 0x55eeb7df34a0 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #10 0x55eeb7e2bac9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #11 0x55eeb7e2b258 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #12 0x55eeb7e2c471 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #13 0x55eeb7ced8ca in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48
    #14 0x55eeb7e2cb3b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:467:12
    #15 0x55eeb7d6f1b1 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #16 0x55eeb7d7104c in base::RunLoop::RunUntilIdle() base/run_loop.cc:143:3
    #17 0x55eeaed72431 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:971:18
    #18 0x55eeaed77065 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:152:15
    #19 0x55eeaed6c41f in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:49:28
    #20 0x55eeb6beafbd in RunBrowserProcessMain content/app/content_main_runner_impl.cc:608:10
    #21 0x55eeb6beafbd in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1104:10
    #22 0x55eeb6bea0c5 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:971:12
    #23 0x55eeb6be3677 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:390:36
    #24 0x55eeb6be5292 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:418:10
    #25 0x55eeaa02c335 in ChromeMain chrome/app/chrome_main.cc:172:12
    #26 0x7fab7e3e00b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

0x602000b47690 is located 0 bytes inside of 8-byte region [0x602000b47690,0x602000b47698)
allocated by thread T0 (chrome) here:
    #0 0x55eeaa029acd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x55eeb0844714 in __libcpp_operator_new<unsigned long> buildtools/third_party/libc++/trunk/include/new:235:10
    #2 0x55eeb0844714 in __libcpp_allocate buildtools/third_party/libc++/trunk/include/new:261:10
    #3 0x55eeb0844714 in allocate buildtools/third_party/libc++/trunk/include/__memory/allocator.h:82:38
    #4 0x55eeb0844714 in allocate buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:261:20
    #5 0x55eeb0844714 in __split_buffer buildtools/third_party/libc++/trunk/include/__split_buffer:314:29
    #6 0x55eeb0844714 in void std::__1::vector<permissions::PermissionRequest*, std::__1::allocator<permissions::PermissionRequest*> >::__push_back_slow_path<permissions::PermissionRequest* const&>(permissions::PermissionRequest* const&) buildtools/third_party/libc++/trunk/include/vector:1625:49
    #7 0x55eeb083f446 in push_back buildtools/third_party/libc++/trunk/include/vector:1642:9
    #8 0x55eeb083f446 in permissions::PermissionRequestManager::DequeueRequestIfNeeded() components/permissions/permission_request_manager.cc:563:17
    #9 0x55eeb0844524 in Invoke<void (permissions::PermissionRequestManager::*)(), base::WeakPtr<permissions::PermissionRequestManager>> base/bind_internal.h:509:12
    #10 0x55eeb0844524 in MakeItSo<void (permissions::PermissionRequestManager::*)(), base::WeakPtr<permissions::PermissionRequestManager>> base/bind_internal.h:668:5
    #11 0x55eeb0844524 in RunImpl<void (permissions::PermissionRequestManager::*)(), std::__1::tuple<base::WeakPtr<permissions::PermissionRequestManager> >, 0UL> base/bind_internal.h:721:12
    #12 0x55eeb0844524 in base::internal::Invoker<base::internal::BindState<void (permissions::PermissionRequestManager::*)(), base::WeakPtr<permissions::PermissionRequestManager> >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #13 0x55eeb7df34a0 in Run base/callback.h:98:12
    #14 0x55eeb7df34a0 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #15 0x55eeb7e2bac9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #16 0x55eeb7e2b258 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #17 0x55eeb7e2c471 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #18 0x55eeb7ced8ca in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48
    #19 0x55eeb7e2cb3b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:467:12
    #20 0x55eeb7d6f1b1 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #21 0x55eeb7d7104c in base::RunLoop::RunUntilIdle() base/run_loop.cc:143:3
    #22 0x55eeaed72431 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:971:18
    #23 0x55eeaed77065 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:152:15
    #24 0x55eeaed6c41f in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:49:28
    #25 0x55eeb6beafbd in RunBrowserProcessMain content/app/content_main_runner_impl.cc:608:10
    #26 0x55eeb6beafbd in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1104:10
    #27 0x55eeb6bea0c5 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:971:12
    #28 0x55eeb6be3677 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:390:36
    #29 0x55eeb6be5292 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:418:10
    #30 0x55eeaa02c335 in ChromeMain chrome/app/chrome_main.cc:172:12
    #31 0x7fab7e3e00b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

HINT: if you don't care about these errors you may set ASAN_OPTIONS=detect_container_overflow=0.
If you suspect a false positive see also: https://github.com/google/sanitizers/wiki/AddressSanitizerContainerOverflow.
SUMMARY: AddressSanitizer: container-overflow components/permissions/permission_uma_util.cc:175:33 in RecordEngagementMetric
Shadow bytes around the buggy address:
  0x0c0480160e80: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c0480160e90: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c0480160ea0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c0480160eb0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c0480160ec0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
=>0x0c0480160ed0: fa fa[fc]fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c0480160ee0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c0480160ef0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c0480160f00: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
  0x0c0480160f10: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c0480160f20: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
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
==2350113==ABORTING

Did this work before? N/A 

Chrome version: 92.0.4515.107  Channel: n/a
OS Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [poc.html](attachments/poc.html) (text/plain, 1.9 KB)
- [video.webm](attachments/video.webm) (video/webm, 1.4 MB)
- [poc2.html](attachments/poc2.html) (text/plain, 906 B)
- [poc1.html](attachments/poc1.html) (text/plain, 194 B)
- [video2.webm](attachments/video2.webm) (video/webm, 1016.3 KB)

## Timeline

### me...@gmail.com (2021-08-26)

Sorry, here is the right poc and video.

### [Deleted User] (2021-08-26)

[Empty comment from Monorail migration]

### me...@gmail.com (2021-08-26)

BTW, if you set ASAN_OPTIONS=detect_container_overflow=0 flag, ASAN will report UAF instead.

=================================================================
==4610==ERROR: AddressSanitizer: heap-use-after-free on address 0x60e000341360 at pc 0x55de362d3341 bp 0x7ffc9f8074b0 sp 0x7ffc9f8074a8
READ of size 4 at 0x60e000341360 thread T0 (chrome)
    #0 0x55de362d3340 in request_type components/permissions/permission_request.h:63:45
    #1 0x55de362d3340 in RecordEngagementMetric components/permissions/permission_uma_util.cc:175:46
    #2 0x55de362d3340 in permissions::PermissionUmaUtil::PermissionPromptResolved(std::__1::vector<permissions::PermissionRequest*, std::__1::allocator<permissions::PermissionRequest*> > const&, content::WebContents*, permissions::PermissionAction, base::TimeDelta, permissions::PermissionPromptDisposition, absl::optional<permissions::PermissionPromptDispositionReason>, absl::optional<permissions::PermissionPrediction_Likelihood_DiscretizedLikelihood>) components/permissions/permission_uma_util.cc:501:3
    #3 0x55de362c34bc in permissions::PermissionRequestManager::FinalizeCurrentRequests(permissions::PermissionAction) components/permissions/permission_request_manager.cc:712:3
    #4 0x55de362c68f3 in permissions::PermissionRequestManager::ShowBubble() components/permissions/permission_request_manager.cc:645:5
    #5 0x55de362ce524 in Invoke<void (permissions::PermissionRequestManager::*)(), base::WeakPtr<permissions::PermissionRequestManager>> base/bind_internal.h:509:12
    #6 0x55de362ce524 in MakeItSo<void (permissions::PermissionRequestManager::*)(), base::WeakPtr<permissions::PermissionRequestManager>> base/bind_internal.h:668:5
    #7 0x55de362ce524 in RunImpl<void (permissions::PermissionRequestManager::*)(), std::__1::tuple<base::WeakPtr<permissions::PermissionRequestManager> >, 0UL> base/bind_internal.h:721:12
    #8 0x55de362ce524 in base::internal::Invoker<base::internal::BindState<void (permissions::PermissionRequestManager::*)(), base::WeakPtr<permissions::PermissionRequestManager> >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #9 0x55de3d87d4a0 in Run base/callback.h:98:12
    #10 0x55de3d87d4a0 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #11 0x55de3d8b5ac9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #12 0x55de3d8b5258 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #13 0x55de3d8b6471 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #14 0x55de3d7786c9 in HandleDispatch base/message_loop/message_pump_glib.cc:375:46
    #15 0x55de3d7786c9 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:125:43
    #16 0x7fc380938fbc in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x51fbc)

0x60e000341360 is located 128 bytes inside of 152-byte region [0x60e0003412e0,0x60e000341378)
freed by thread T0 (chrome) here:
    #0 0x55de2fab432d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x55de3629a0cd in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #2 0x55de3629a0cd in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #3 0x55de3629a0cd in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #4 0x55de3629a0cd in ~pair buildtools/third_party/libc++/trunk/include/utility:394:29
    #5 0x55de3629a0cd in destroy<std::__1::pair<const std::__1::string, std::__1::unique_ptr<permissions::PermissionRequest, std::__1::default_delete<permissions::PermissionRequest> > >, void, void> buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:318:15
    #6 0x55de3629a0cd in operator() buildtools/third_party/libc++/trunk/include/__hash_table:849:13
    #7 0x55de3629a0cd in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #8 0x55de3629a0cd in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #9 0x55de3629a0cd in erase buildtools/third_party/libc++/trunk/include/__hash_table:2498:5
    #10 0x55de3629a0cd in __erase_unique<std::__1::string> buildtools/third_party/libc++/trunk/include/__hash_table:2536:5
    #11 0x55de3629a0cd in erase buildtools/third_party/libc++/trunk/include/unordered_map:1271:59
    #12 0x55de3629a0cd in permissions::PermissionContextBase::CleanUpRequest(permissions::PermissionRequestID const&) components/permissions/permission_context_base.cc:499:38
    #13 0x55de3629c246 in Invoke<void (permissions::PermissionContextBase::*)(const permissions::PermissionRequestID &), base::WeakPtr<permissions::PermissionContextBase>, permissions::PermissionRequestID> base/bind_internal.h:509:12
    #14 0x55de3629c246 in MakeItSo<void (permissions::PermissionContextBase::*)(const permissions::PermissionRequestID &), base::WeakPtr<permissions::PermissionContextBase>, permissions::PermissionRequestID> base/bind_internal.h:668:5
    #15 0x55de3629c246 in RunImpl<void (permissions::PermissionContextBase::*)(const permissions::PermissionRequestID &), std::__1::tuple<base::WeakPtr<permissions::PermissionContextBase>, permissions::PermissionRequestID>, 0UL, 1UL> base/bind_internal.h:721:12
    #16 0x55de3629c246 in base::internal::Invoker<base::internal::BindState<void (permissions::PermissionContextBase::*)(permissions::PermissionRequestID const&), base::WeakPtr<permissions::PermissionContextBase>, permissions::PermissionRequestID>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #17 0x55de362c0d05 in Run base/callback.h:98:12
    #18 0x55de362c0d05 in permissions::PermissionRequest::RequestFinished() components/permissions/permission_request.cc:237:31
    #19 0x55de362c3b3a in RequestFinishedIncludingDuplicates components/permissions/permission_request_manager.cc:841:12
    #20 0x55de362c3b3a in permissions::PermissionRequestManager::FinalizeCurrentRequests(permissions::PermissionAction) components/permissions/permission_request_manager.cc:760:5
    #21 0x55de362c82ca in Closing components/permissions/permission_request_manager.cc:519:3
    #22 0x55de362c82ca in non-virtual thunk to permissions::PermissionRequestManager::Closing() components/permissions/permission_request_manager.cc
    #23 0x55de46db4401 in Run base/callback.h:98:12
    #24 0x55de46db4401 in RunCloseCallback ui/views/window/dialog_delegate.cc:178:23
    #25 0x55de46db4401 in views::DialogDelegate::WindowWillClose() ui/views/window/dialog_delegate.cc:228:5
    #26 0x55de46da79d3 in Run base/callback.h:98:12
    #27 0x55de46da79d3 in views::WidgetDelegate::WindowWillClose() ui/views/widget/widget_delegate.cc:215:25
    #28 0x55de46d86bb8 in views::Widget::CloseWithReason(views::Widget::ClosedReason) ui/views/widget/widget.cc:701:23
    #29 0x55de484e9a78 in PermissionPromptImpl::~PermissionPromptImpl() chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc:100:38
    #30 0x55de484e9bdd in PermissionPromptImpl::~PermissionPromptImpl() chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc:95:47
    #31 0x55de362c6740 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #32 0x55de362c6740 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #33 0x55de362c6740 in operator= buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:234:5
    #34 0x55de362c6740 in permissions::PermissionRequestManager::ShowBubble() components/permissions/permission_request_manager.cc:641:9
    #35 0x55de362ce524 in Invoke<void (permissions::PermissionRequestManager::*)(), base::WeakPtr<permissions::PermissionRequestManager>> base/bind_internal.h:509:12
    #36 0x55de362ce524 in MakeItSo<void (permissions::PermissionRequestManager::*)(), base::WeakPtr<permissions::PermissionRequestManager>> base/bind_internal.h:668:5
    #37 0x55de362ce524 in RunImpl<void (permissions::PermissionRequestManager::*)(), std::__1::tuple<base::WeakPtr<permissions::PermissionRequestManager> >, 0UL> base/bind_internal.h:721:12
    #38 0x55de362ce524 in base::internal::Invoker<base::internal::BindState<void (permissions::PermissionRequestManager::*)(), base::WeakPtr<permissions::PermissionRequestManager> >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #39 0x55de3d87d4a0 in Run base/callback.h:98:12
    #40 0x55de3d87d4a0 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #41 0x55de3d8b5ac9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #42 0x55de3d8b5258 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #43 0x55de3d8b6471 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #44 0x55de3d7786c9 in HandleDispatch base/message_loop/message_pump_glib.cc:375:46
    #45 0x55de3d7786c9 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:125:43
    #46 0x7fc380938fbc in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x51fbc)

previously allocated by thread T0 (chrome) here:
    #0 0x55de2fab3acd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x55de36298bce in make_unique<permissions::PermissionRequest, const GURL &, permissions::RequestType, bool &, base::OnceCallback<void (ContentSetting, bool)>, base::OnceCallback<void ()> > buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725:28
    #2 0x55de36298bce in permissions::PermissionContextBase::CreatePermissionRequest(GURL const&, ContentSettingsType, bool, content::WebContents*, base::OnceCallback<void (ContentSetting, bool)>, base::OnceCallback<void ()>) const components/permissions/permission_context_base.cc:231:10
    #3 0x55de36299975 in permissions::PermissionContextBase::DecidePermission(content::WebContents*, permissions::PermissionRequestID const&, GURL const&, GURL const&, bool, base::OnceCallback<void (ContentSetting)>) components/permissions/permission_context_base.cc:391:52
    #4 0x55de36297b75 in permissions::PermissionContextBase::RequestPermission(content::WebContents*, permissions::PermissionRequestID const&, GURL const&, bool, base::OnceCallback<void (ContentSetting)>) components/permissions/permission_context_base.cc:213:3
    #5 0x55de362a552d in permissions::PermissionManager::RequestPermissions(std::__1::vector<ContentSettingsType, std::__1::allocator<ContentSettingsType> > const&, content::RenderFrameHost*, GURL const&, bool, base::OnceCallback<void (std::__1::vector<ContentSetting, std::__1::allocator<ContentSetting> > const&)>) components/permissions/permission_manager.cc:401:14
    #6 0x55de362a73db in permissions::PermissionManager::RequestPermissions(std::__1::vector<content::PermissionType, std::__1::allocator<content::PermissionType> > const&, content::RenderFrameHost*, GURL const&, bool, base::OnceCallback<void (std::__1::vector<blink::mojom::PermissionStatus, std::__1::allocator<blink::mojom::PermissionStatus> > const&)>) components/permissions/permission_manager.cc:489:3
    #7 0x55de35140d7b in content::PermissionControllerImpl::RequestPermissions(std::__1::vector<content::PermissionType, std::__1::allocator<content::PermissionType> > const&, content::RenderFrameHost*, GURL const&, bool, base::OnceCallback<void (std::__1::vector<blink::mojom::PermissionStatus, std::__1::allocator<blink::mojom::PermissionStatus> > const&)>) content/browser/permissions/permission_controller_impl.cc:328:13
    #8 0x55de3514f536 in content::PermissionServiceImpl::RequestPermissions(std::__1::vector<mojo::StructPtr<blink::mojom::PermissionDescriptor>, std::__1::allocator<mojo::StructPtr<blink::mojom::PermissionDescriptor> > >, bool, base::OnceCallback<void (std::__1::vector<blink::mojom::PermissionStatus, std::__1::allocator<blink::mojom::PermissionStatus> > const&)>) content/browser/permissions/permission_service_impl.cc:128:9
    #9 0x55de3514e31e in content::PermissionServiceImpl::RequestPermission(mojo::StructPtr<blink::mojom::PermissionDescriptor>, bool, base::OnceCallback<void (blink::mojom::PermissionStatus)>) content/browser/permissions/permission_service_impl.cc:76:3
    #10 0x55de33303947 in blink::mojom::PermissionServiceStubDispatch::AcceptWithResponder(blink::mojom::PermissionService*, mojo::Message*, std::__1::unique_ptr<mojo::MessageReceiverWithStatus, std::__1::default_delete<mojo::MessageReceiverWithStatus> >) gen/third_party/blink/public/mojom/permissions/permission.mojom.cc:1411:13
    #11 0x55de3e3b77d7 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:860:56
    #12 0x55de3e3c918a in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #13 0x55de3e3bb737 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:655:20
    #14 0x55de3e3d5003 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1099:42
    #15 0x55de3e3d3559 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:719:7
    #16 0x55de3e3c9271 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #17 0x55de3e3b09e7 in mojo::Connector::DispatchMessage(mojo::Message) mojo/public/cpp/bindings/lib/connector.cc:546:49
    #18 0x55de3e3b2730 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:604:14
    #19 0x55de3e3b39b4 in Invoke<void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>> base/bind_internal.h:509:12
    #20 0x55de3e3b39b4 in MakeItSo<void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>> base/bind_internal.h:668:5
    #21 0x55de3e3b39b4 in RunImpl<void (mojo::Connector::*)(), std::__1::tuple<base::WeakPtr<mojo::Connector> >, 0UL> base/bind_internal.h:721:12
    #22 0x55de3e3b39b4 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector> >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #23 0x55de3d87d4a0 in Run base/callback.h:98:12
    #24 0x55de3d87d4a0 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #25 0x55de3d8b5ac9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #26 0x55de3d8b5258 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #27 0x55de3d8b6471 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #28 0x55de3d7778ca in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48
    #29 0x55de3d8b6b3b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:467:12
    #30 0x55de3d7f91b1 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #31 0x55de347fc525 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:988:18
    #32 0x55de34801065 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:152:15
    #33 0x55de347f641f in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:49:28
    #34 0x55de3c674fbd in RunBrowserProcessMain content/app/content_main_runner_impl.cc:608:10
    #35 0x55de3c674fbd in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1104:10

SUMMARY: AddressSanitizer: heap-use-after-free components/permissions/permission_request.h:63:45 in request_type
Shadow bytes around the buggy address:
  0x0c1c80060210: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x0c1c80060220: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1c80060230: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c1c80060240: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1c80060250: fd fd fd fd fa fa fa fa fa fa fa fa fd fd fd fd
=>0x0c1c80060260: fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd fa
  0x0c1c80060270: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c1c80060280: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x0c1c80060290: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1c800602a0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c1c800602b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==4610==ABORTING


### cl...@chromium.org (2021-08-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5944986582188032.

### me...@gmail.com (2021-08-27)

In components/permissions/permission_request_manager.cc [1], unique_ptr `view_` is re-assigned and old view will be freed, `requests_` will be cleaned up. FinalizeCurrentRequests will use requests[0] => overflow/UAF.

 view_ = view_factory_.Run(web_contents(), this); // re-assign to view_ will destroy old view_, which will erase requests_
  if (!view_) {
    current_request_prompt_disposition_ =
        PermissionPromptDisposition::NONE_VISIBLE;
    FinalizeCurrentRequests(PermissionAction::IGNORED);  // use requests_ again, uaf/overflow
    return;
  }

https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/permission_request_manager.cc;l=641;bpv=0;bpt=1

### dr...@chromium.org (2021-08-27)

This does reproduce as claimed. There are a number of DCHECKs/NOTREACHED that catch this, but none of those would affect an official build.

dominickn@, engedy@ - can you take a look?

[Monorail components: UI>Browser>Permissions>Prompts]

### [Deleted User] (2021-08-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-28)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-28)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2021-08-30)

+elklm, do you might taking a look? Seems that the call to FinalizeCurrentRequests() was added in https://chromium-review.googlesource.com/c/chromium/src/+/2690644

### el...@chromium.org (2021-09-01)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-09-01)

Was able to reproduce the crash. Working on fixing it.

The bug is labeled as M92, I believe it is not correct, because a CL that adds FinalizeCurrentRequests() at line 645 was landed to 93.0.4569.0.


### do...@chromium.org (2021-09-02)

I agree - I think M92 was because the bug filer used M92 to file the bug. Adjusting the target. :)

### [Deleted User] (2021-09-02)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-09-02)

merc.ouc@, is there a repro here that doesn't rely on MojoJS and can work solely using web-facing APIs?

### me...@gmail.com (2021-09-02)

Try poc1 on windows (it seems that navigator.permissions.request is not supported on Linux). Open many many poc.html at a time.

Sorry I don't test poc1.html because I don't have a asan release on windows. But I think it will work, because poc2 with MojoJS can also trigger this UAF (see video2). poc1 and poc2 both request a permission chip,  poc2 use MojoJS and poc1 use Web API.

### gi...@appspot.gserviceaccount.com (2021-09-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/58d05cfd21cd936120711f0337949eb6bc47e1c2

commit 58d05cfd21cd936120711f0337949eb6bc47e1c2
Author: Illia Klimov <elklm@google.com>
Date: Thu Sep 02 11:57:02 2021

Ensure ShowBubble is a no-op if already showing.

PermissionRequestManager::ShowBubble should be a no-op if the permission
bubble is already showing.

Bug: 1243646
Change-Id: Id7a523bfdaf4c43cf6f6cf1177691a3fa2e10a4d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3136913
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Commit-Queue: Illia Klimov <elklm@chromium.org>
Cr-Commit-Position: refs/heads/main@{#917624}

[modify] https://crrev.com/58d05cfd21cd936120711f0337949eb6bc47e1c2/components/permissions/permission_request_manager.cc


### el...@chromium.org (2021-09-02)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-09-02)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-09-02)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-09-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-02)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-02)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-09-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-03)

This bug requires manual review: M94's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2021-09-03)

1. Yes
2.  https://chromium-review.googlesource.com/c/chromium/src/+/3136913
3. Yes
4. Yes, it should be merged back into M93 and M92.
5. Security issue
6. No
7. Not a feature.

8. N/A

### sr...@google.com (2021-09-03)

Merge approved for M94 branch:4606 please merege asap

### gi...@appspot.gserviceaccount.com (2021-09-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/23ccfc423283b80da0f0beaa77f11d43ad4f7648

commit 23ccfc423283b80da0f0beaa77f11d43ad4f7648
Author: Illia Klimov <elklm@google.com>
Date: Sat Sep 04 11:49:22 2021

Ensure ShowBubble is a no-op if already showing.

PermissionRequestManager::ShowBubble should be a no-op if the permission
bubble is already showing.

(cherry picked from commit 58d05cfd21cd936120711f0337949eb6bc47e1c2)

Bug: 1243646
Change-Id: Id7a523bfdaf4c43cf6f6cf1177691a3fa2e10a4d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3136913
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Commit-Queue: Illia Klimov <elklm@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#917624}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3141602
Auto-Submit: Illia Klimov <elklm@chromium.org>
Commit-Queue: Balazs Engedy <engedy@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#730}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/23ccfc423283b80da0f0beaa77f11d43ad4f7648/components/permissions/permission_request_manager.cc


### am...@chromium.org (2021-09-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-07)

merge approved to M93, please merge to branch 4577 by 2pm PDT Friday, 10 September, so this fix can be included in next week's M93 security refresh. 
Also approved to M92, please go ahead and merge to branch 4515 at your earliest convenience so this is part of the Extended Stable release as we move to the 4W stable channel release cycle. Thank you. 

### am...@chromium.org (2021-09-07)

Apologies, please merge to M93 (branch 4577) by 2pm THURSDAY, 9 September for this fix to be included in stable cut for next week's security refresh of M93. Thanks!!

### gi...@appspot.gserviceaccount.com (2021-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3617086618ea350a7b181ae349264b6b5f9007ef

commit 3617086618ea350a7b181ae349264b6b5f9007ef
Author: Illia Klimov <elklm@google.com>
Date: Wed Sep 08 08:25:28 2021

Ensure ShowBubble is a no-op if already showing.

PermissionRequestManager::ShowBubble should be a no-op if the permission
bubble is already showing.

(cherry picked from commit 58d05cfd21cd936120711f0337949eb6bc47e1c2)

Bug: 1243646
Change-Id: Id7a523bfdaf4c43cf6f6cf1177691a3fa2e10a4d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3136913
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Commit-Queue: Illia Klimov <elklm@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#917624}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3145115
Cr-Commit-Position: refs/branch-heads/4515@{#2116}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/3617086618ea350a7b181ae349264b6b5f9007ef/components/permissions/permission_request_manager.cc


### gi...@appspot.gserviceaccount.com (2021-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/af1bad5fb8d2c020c77a27f81244b690103bad67

commit af1bad5fb8d2c020c77a27f81244b690103bad67
Author: Illia Klimov <elklm@google.com>
Date: Wed Sep 08 08:25:24 2021

Ensure ShowBubble is a no-op if already showing.

PermissionRequestManager::ShowBubble should be a no-op if the permission
bubble is already showing.

(cherry picked from commit 58d05cfd21cd936120711f0337949eb6bc47e1c2)

Bug: 1243646
Change-Id: Id7a523bfdaf4c43cf6f6cf1177691a3fa2e10a4d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3136913
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Commit-Queue: Illia Klimov <elklm@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#917624}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3145223
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4577@{#1200}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/af1bad5fb8d2c020c77a27f81244b690103bad67/components/permissions/permission_request_manager.cc


### gi...@appspot.gserviceaccount.com (2021-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3617086618ea350a7b181ae349264b6b5f9007ef

commit 3617086618ea350a7b181ae349264b6b5f9007ef
Author: Illia Klimov <elklm@google.com>
Date: Wed Sep 08 08:25:28 2021

Ensure ShowBubble is a no-op if already showing.

PermissionRequestManager::ShowBubble should be a no-op if the permission
bubble is already showing.

(cherry picked from commit 58d05cfd21cd936120711f0337949eb6bc47e1c2)

Bug: 1243646
Change-Id: Id7a523bfdaf4c43cf6f6cf1177691a3fa2e10a4d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3136913
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Commit-Queue: Illia Klimov <elklm@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#917624}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3145115
Cr-Commit-Position: refs/branch-heads/4515@{#2116}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/3617086618ea350a7b181ae349264b6b5f9007ef/components/permissions/permission_request_manager.cc


### el...@chromium.org (2021-09-08)

[Empty comment from Monorail migration]

### me...@gmail.com (2021-09-08)

[Comment Deleted]

### am...@chromium.org (2021-09-13)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-13)

[Empty comment from Monorail migration]

### vo...@google.com (2021-09-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-23)

Congratulations! The VRP Panel has decided to award you $20,000 for this report. Thank you for your detailed report and analysis. Very nice work! 

### me...@gmail.com (2021-09-24)

Thank you!

### am...@google.com (2021-09-24)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-09-28)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1243646?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1222016, crbug.com/chromium/1234252, crbug.com/chromium/1245158]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057026)*

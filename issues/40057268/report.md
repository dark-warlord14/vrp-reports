# Security: Use After Free in DevToolsFileHelper::GetFileSystems

| Field | Value |
|-------|-------|
| **Issue ID** | [40057268](https://issues.chromium.org/issues/40057268) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2021-09-15 |
| **Bounty** | $10,000.00 |

## Description

This UAF problem was discovered accidentally. The specific reason is not very clear. I only know that UAF has occurred, and there is no way to reproduce it successfully later. It may be that the competition conditions are a bit harsh.

void DevToolsFileHelper::FileSystemPathsSettingChanged() {
  PathToType remaining;
  remaining.swap(file_system_paths_);
  DCHECK(file_watcher_.get());

  for (auto file_system : GetAddedFileSystemPaths(profile_)) {
    if (remaining.find(file_system.first) == remaining.end()) {
      base::FilePath path = base::FilePath::FromUTF8Unsafe(file_system.first);
      std::string file_system_id = RegisterFileSystem(web_contents_, path);
      FileSystem filesystem = CreateFileSystemStruct(
          web_contents_, file_system.second, file_system_id, file_system.first);
      delegate_->FileSystemAdded(std::string(), &filesystem);
      file_watcher_->AddWatch(std::move(path));
    } else {
      remaining.erase(file_system.first);
    }
    file_system_paths_[file_system.first] = file_system.second;
  }

  for (auto file_system : remaining) {
    delegate_->FileSystemRemoved(file_system.first);
    base::FilePath path = base::FilePath::FromUTF8Unsafe(file_system.first);
    file_watcher_->RemoveWatch(std::move(path));  free here [1]
  }
}


std::vector<DevToolsFileHelper::FileSystem>
DevToolsFileHelper::GetFileSystems() {
  file_system_paths_ = GetAddedFileSystemPaths(profile_);
  std::vector<FileSystem> file_systems;
  if (!file_watcher_) {
    file_watcher_.reset(new DevToolsFileWatcher(
        base::BindRepeating(&DevToolsFileHelper::FilePathsChanged,
                            weak_factory_.GetWeakPtr()),
        base::SequencedTaskRunnerHandle::Get()));
    pref_change_registrar_.Add(
        prefs::kDevToolsFileSystemPaths,
        base::BindRepeating(&DevToolsFileHelper::FileSystemPathsSettingChanged,
                            base::Unretained(this)));
  }
  for (auto file_system_path : file_system_paths_) {
    base::FilePath path =
        base::FilePath::FromUTF8Unsafe(file_system_path.first);
    std::string file_system_id = RegisterFileSystem(web_contents_, path);
    FileSystem filesystem =
        CreateFileSystemStruct(web_contents_, file_system_path.second,
                               file_system_id, file_system_path.first);
    file_systems.push_back(filesystem);
    file_watcher_->AddWatch(std::move(path));  UAF here [2]
  }
  return file_systems;
}





[1]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/devtools/devtools_file_helper.cc;l=471;bpv=0;bpt=1

[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/devtools/devtools_file_helper.cc;l=405;bpv=0;bpt=1 

 

=================================================================
==7956==ERROR: AddressSanitizer: heap-use-after-free on address 0x11c2e6a6fe68 at pc 0x7ff913cb5023 bp 0x00711d5fb620 sp 0x00711d5fb668
READ of size 8 at 0x11c2e6a6fe68 thread T0
    #0 0x7ff913cb5022 in DevToolsFileHelper::GetFileSystems E:\src\chromium\src\chrome\browser\devtools\devtools_file_helper.cc:405
    #1 0x7ff912365ee2 in DevToolsUIBindings::RequestFileSystems E:\src\chromium\src\chrome\browser\devtools\devtools_ui_bindings.cc:997
    #2 0x7ff913cc9a4e in `anonymous namespace'::ParseAndHandle<> E:\src\chromium\src\chrome\browser\devtools\devtools_embedder_message_dispatcher.cc:110
    #3 0x7ff913cc9b9b in base::internal::Invoker<base::internal::BindState<bool (*)(const base::RepeatingCallback<void ()> &, base::OnceCallback<void (const base::Value *)>, const std::__1::vector<base::Value,std::__1::allocator<base::Value> > &),base::RepeatingCallback<void ()> >,bool (base::OnceCallback<void (const base::Value *)>, const std::__1::vector<base::Value,std::__1::allocator<base::Value> > &)>::Run E:\src\chromium\src\base\bind_internal.h:703
    #4 0x7ff913cc92ca in DispatcherImpl::Dispatch E:\src\chromium\src\chrome\browser\devtools\devtools_embedder_message_dispatcher.cc:144
    #5 0x7ff91235f646 in DevToolsUIBindings::HandleMessageFromDevToolsFrontend E:\src\chromium\src\chrome\browser\devtools\devtools_ui_bindings.cc:753
    #6 0x7ff912378e75 in base::internal::Invoker<base::internal::BindState<void (DevToolsUIBindings::*)(base::Value),base::internal::UnretainedWrapper<DevToolsUIBindings> >,void (base::Value)>::Run E:\src\chromium\src\base\bind_internal.h:703
    #7 0x7ff908af7f73 in content::DevToolsFrontendHostImpl::DispatchEmbedderMessage E:\src\chromium\src\content\browser\devtools\devtools_frontend_host_impl.cc:94
    #8 0x7ff900b6622c in blink::mojom::DevToolsFrontendHostStubDispatch::Accept E:\src\chromium\src\out\Default\gen\third_party\blink\public\mojom\devtools\devtools_frontend.mojom.cc:363
    #9 0x7ff946a67508 in mojo::InterfaceEndpointClient::HandleValidatedMessage E:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:898
    #10 0x7ff946a77519 in mojo::MessageDispatcher::Accept E:\src\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #11 0x7ff946a6aed6 in mojo::InterfaceEndpointClient::HandleIncomingMessage E:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:655
    #12 0x7ff943fee48c in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread E:\src\chromium\src\ipc\ipc_mojo_bootstrap.cc:981
    #13 0x7ff943fe7d82 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce E:\src\chromium\src\base\bind_internal.h:690
    #14 0x7ff944a213da in base::TaskAnnotator::RunTask E:\src\chromium\src\base\task\common\task_annotator.cc:178
    #15 0x7ff944a690d2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360
    #16 0x7ff944a68763 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260
    #17 0x7ff944b64ebf in base::MessagePumpForUI::DoRunLoop E:\src\chromium\src\base\message_loop\message_pump_win.cc:220
    #18 0x7ff944b62971 in base::MessagePumpWin::Run E:\src\chromium\src\base\message_loop\message_pump_win.cc:78
    #19 0x7ff944a6a628 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:467
    #20 0x7ff94496fdb0 in base::RunLoop::Run E:\src\chromium\src\base\run_loop.cc:134
    #21 0x7ff9076a4240 in content::BrowserMainLoop::RunMainMessageLoop E:\src\chromium\src\content\browser\browser_main_loop.cc:988
    #22 0x7ff9076aa0f1 in content::BrowserMainRunnerImpl::Run E:\src\chromium\src\content\browser\browser_main_runner_impl.cc:152
    #23 0x7ff90769d795 in content::BrowserMain E:\src\chromium\src\content\browser\browser_main.cc:49
    #24 0x7ff909765aae in content::RunBrowserProcessMain E:\src\chromium\src\content\app\content_main_runner_impl.cc:608
    #25 0x7ff909768437 in content::ContentMainRunnerImpl::RunBrowser E:\src\chromium\src\content\app\content_main_runner_impl.cc:1104
    #26 0x7ff9097675d9 in content::ContentMainRunnerImpl::Run E:\src\chromium\src\content\app\content_main_runner_impl.cc:971
    #27 0x7ff909763c95 in content::RunContentProcess E:\src\chromium\src\content\app\content_main.cc:390
    #28 0x7ff909764c8b in content::ContentMain E:\src\chromium\src\content\app\content_main.cc:418
    #29 0x7ff90c8a14a0 in ChromeMain E:\src\chromium\src\chrome\app\chrome_main.cc:172
    #30 0x7ff6b9a35550 in MainDllLoader::Launch E:\src\chromium\src\chrome\app\main_dll_loader_win.cc:169
    #31 0x7ff6b9a3299b in main E:\src\chromium\src\chrome\app\chrome_exe_main_win.cc:382
    #32 0x7ff6b9c06e0b in __scrt_common_main_seh D:\agent\_work\13\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #33 0x7ff980bc7033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #34 0x7ff982a82650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x11c2e6a6fe68 is located 8 bytes inside of 80-byte region [0x11c2e6a6fe60,0x11c2e6a6feb0)
freed by thread T11 here:
    #0 0x7ff926abe23b in operator delete+0x8b (E:\src\chromium\src\out\Default\clang_rt.asan_dynamic-x86_64.dll+0x18003e23b)
    #1 0x7ff90dba98e9 in std::__1::__tree<std::__1::__value_type<std::__1::string,std::__1::string>,std::__1::__map_value_compare<std::__1::string,std::__1::__value_type<std::__1::string,std::__1::string>,std::__1::less<std::__1::string>,1>,std::__1::allocator<std::__1::__value_type<std::__1::string,std::__1::string> > >::erase E:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__tree:2424
    #2 0x7ff90dd5ae48 in std::__1::__tree<std::__1::__value_type<std::__1::string,std::__1::string>,std::__1::__map_value_compare<std::__1::string,std::__1::__value_type<std::__1::string,std::__1::string>,std::__1::less<std::__1::string>,1>,std::__1::allocator<std::__1::__value_type<std::__1::string,std::__1::string> > >::__erase_unique<std::__1::string> E:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__tree:2445
    #3 0x7ff913cb5cc7 in DevToolsFileHelper::FileSystemPathsSettingChanged E:\src\chromium\src\chrome\browser\devtools\devtools_file_helper.cc:471
    #4 0x7ff944a213da in base::TaskAnnotator::RunTask E:\src\chromium\src\base\task\common\task_annotator.cc:178
    #5 0x7ff944a690d2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360
    #6 0x7ff944a68763 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260
    #7 0x7ff944b69065 in base::MessagePumpForIO::DoRunLoop E:\src\chromium\src\base\message_loop\message_pump_win.cc:720
    #8 0x7ff944b62971 in base::MessagePumpWin::Run E:\src\chromium\src\base\message_loop\message_pump_win.cc:78
    #9 0x7ff944a6a628 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:467
    #10 0x7ff94496fdb0 in base::RunLoop::Run E:\src\chromium\src\base\run_loop.cc:134
    #11 0x7ff944add249 in base::Thread::Run E:\src\chromium\src\base\threading\thread.cc:341
    #12 0x7ff9076ad4b8 in content::BrowserProcessIOThread::IOThreadRun E:\src\chromium\src\content\browser\browser_process_io_thread.cc:128
    #13 0x7ff944add647 in base::Thread::ThreadMain E:\src\chromium\src\base\threading\thread.cc:412
    #14 0x7ff944b99b98 in base::`anonymous namespace'::ThreadFunc E:\src\chromium\src\base\threading\platform_thread_win.cc:121
    #15 0x7ff926abcf43 in _asan_print_accumulated_stats+0x15f3 (E:\src\chromium\src\out\Default\clang_rt.asan_dynamic-x86_64.dll+0x18003cf43)
    #16 0x7ff980bc7033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #17 0x7ff982a82650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

previously allocated by thread T0 here:
    #0 0x7ff926abdf4b in operator new+0x8b (E:\src\chromium\src\out\Default\clang_rt.asan_dynamic-x86_64.dll+0x18003df4b)
    #1 0x7ff90d0b64a0 in std::__1::__tree<std::__1::__value_type<std::__1::string,std::__1::string>,std::__1::__map_value_compare<std::__1::string,std::__1::__value_type<std::__1::string,std::__1::string>,std::__1::less<std::__1::string>,1>,std::__1::allocator<std::__1::__value_type<std::__1::string,std::__1::string> > >::__construct_node<const std::__1::piecewise_construct_t &,std::__1::tuple<const std::__1::string &>,std::__1::tuple<> > E:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__tree:2133
    #2 0x7ff90d0b5e7d in std::__1::__tree<std::__1::__value_type<std::__1::string,std::__1::string>,std::__1::__map_value_compare<std::__1::string,std::__1::__value_type<std::__1::string,std::__1::string>,std::__1::less<std::__1::string>,1>,std::__1::allocator<std::__1::__value_type<std::__1::string,std::__1::string> > >::__emplace_unique_key_args<std::__1::string,const std::__1::piecewise_construct_t &,std::__1::tuple<const std::__1::string &>,std::__1::tuple<> > E:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__tree:2096
    #3 0x7ff913cb56b4 in `anonymous namespace'::GetAddedFileSystemPaths E:\src\chromium\src\chrome\browser\devtools\devtools_file_helper.cc:203
    #4 0x7ff913cb43d9 in DevToolsFileHelper::GetFileSystems E:\src\chromium\src\chrome\browser\devtools\devtools_file_helper.cc:387
    #5 0x7ff912365ee2 in DevToolsUIBindings::RequestFileSystems E:\src\chromium\src\chrome\browser\devtools\devtools_ui_bindings.cc:997
    #6 0x7ff913cc9a4e in `anonymous namespace'::ParseAndHandle<> E:\src\chromium\src\chrome\browser\devtools\devtools_embedder_message_dispatcher.cc:110
    #7 0x7ff913cc9b9b in base::internal::Invoker<base::internal::BindState<bool (*)(const base::RepeatingCallback<void ()> &, base::OnceCallback<void (const base::Value *)>, const std::__1::vector<base::Value,std::__1::allocator<base::Value> > &),base::RepeatingCallback<void ()> >,bool (base::OnceCallback<void (const base::Value *)>, const std::__1::vector<base::Value,std::__1::allocator<base::Value> > &)>::Run E:\src\chromium\src\base\bind_internal.h:703
    #8 0x7ff913cc92ca in DispatcherImpl::Dispatch E:\src\chromium\src\chrome\browser\devtools\devtools_embedder_message_dispatcher.cc:144
    #9 0x7ff91235f646 in DevToolsUIBindings::HandleMessageFromDevToolsFrontend E:\src\chromium\src\chrome\browser\devtools\devtools_ui_bindings.cc:753
    #10 0x7ff912378e75 in base::internal::Invoker<base::internal::BindState<void (DevToolsUIBindings::*)(base::Value),base::internal::UnretainedWrapper<DevToolsUIBindings> >,void (base::Value)>::Run E:\src\chromium\src\base\bind_internal.h:703
    #11 0x7ff908af7f73 in content::DevToolsFrontendHostImpl::DispatchEmbedderMessage E:\src\chromium\src\content\browser\devtools\devtools_frontend_host_impl.cc:94
    #12 0x7ff900b6622c in blink::mojom::DevToolsFrontendHostStubDispatch::Accept E:\src\chromium\src\out\Default\gen\third_party\blink\public\mojom\devtools\devtools_frontend.mojom.cc:363
    #13 0x7ff946a67508 in mojo::InterfaceEndpointClient::HandleValidatedMessage E:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:898
    #14 0x7ff946a77519 in mojo::MessageDispatcher::Accept E:\src\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #15 0x7ff946a6aed6 in mojo::InterfaceEndpointClient::HandleIncomingMessage E:\src\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:655
    #16 0x7ff943fee48c in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread E:\src\chromium\src\ipc\ipc_mojo_bootstrap.cc:981
    #17 0x7ff943fe7d82 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce E:\src\chromium\src\base\bind_internal.h:690
    #18 0x7ff944a213da in base::TaskAnnotator::RunTask E:\src\chromium\src\base\task\common\task_annotator.cc:178
    #19 0x7ff944a690d2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:360
    #20 0x7ff944a68763 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:260
    #21 0x7ff944b64ebf in base::MessagePumpForUI::DoRunLoop E:\src\chromium\src\base\message_loop\message_pump_win.cc:220
    #22 0x7ff944b62971 in base::MessagePumpWin::Run E:\src\chromium\src\base\message_loop\message_pump_win.cc:78
    #23 0x7ff944a6a628 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run E:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:467
    #24 0x7ff94496fdb0 in base::RunLoop::Run E:\src\chromium\src\base\run_loop.cc:134
    #25 0x7ff9076a4240 in content::BrowserMainLoop::RunMainMessageLoop E:\src\chromium\src\content\browser\browser_main_loop.cc:988
    #26 0x7ff9076aa0f1 in content::BrowserMainRunnerImpl::Run E:\src\chromium\src\content\browser\browser_main_runner_impl.cc:152
    #27 0x7ff90769d795 in content::BrowserMain E:\src\chromium\src\content\browser\browser_main.cc:49

Thread T11 created by T0 here:
    #0 0x7ff926abd952 in _asan_wrap_CreateThread+0x62 (E:\src\chromium\src\out\Default\clang_rt.asan_dynamic-x86_64.dll+0x18003d952)
    #1 0x7ff944b98fdf in base::`anonymous namespace'::CreateThreadInternal E:\src\chromium\src\base\threading\platform_thread_win.cc:185
    #2 0x7ff944adb988 in base::Thread::StartWithOptions E:\src\chromium\src\base\threading\thread.cc:216
    #3 0x7ff9084c0264 in content::BrowserTaskExecutor::CreateIOThread E:\src\chromium\src\content\browser\scheduler\browser_task_executor.cc:358
    #4 0x7ff909767e62 in content::ContentMainRunnerImpl::RunBrowser E:\src\chromium\src\content\app\content_main_runner_impl.cc:1074
    #5 0x7ff9097675d9 in content::ContentMainRunnerImpl::Run E:\src\chromium\src\content\app\content_main_runner_impl.cc:971
    #6 0x7ff909763c95 in content::RunContentProcess E:\src\chromium\src\content\app\content_main.cc:390
    #7 0x7ff909764c8b in content::ContentMain E:\src\chromium\src\content\app\content_main.cc:418
    #8 0x7ff90c8a14a0 in ChromeMain E:\src\chromium\src\chrome\app\chrome_main.cc:172
    #9 0x7ff6b9a35550 in MainDllLoader::Launch E:\src\chromium\src\chrome\app\main_dll_loader_win.cc:169
    #10 0x7ff6b9a3299b in main E:\src\chromium\src\chrome\app\chrome_exe_main_win.cc:382
    #11 0x7ff6b9c06e0b in __scrt_common_main_seh D:\agent\_work\13\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #12 0x7ff980bc7033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #13 0x7ff982a82650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

SUMMARY: AddressSanitizer: heap-use-after-free E:\src\chromium\src\chrome\browser\devtools\devtools_file_helper.cc:405 in DevToolsFileHelper::GetFileSystems
Shadow bytes around the buggy address:
  0x03ed4364df70: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd
  0x03ed4364df80: fd fd fa fa fa fa fd fd fd fd fd fd fd fd fd fd
  0x03ed4364df90: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fa fa
  0x03ed4364dfa0: fa fa fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x03ed4364dfb0: fd fd fd fd fd fd fd fd fd fd fa fa fa fa 00 00
=>0x03ed4364dfc0: 00 00 00 00 00 00 00 00 fa fa fa fa fd[fd]fd fd
  0x03ed4364dfd0: fd fd fd fd fd fd fa fa fa fa 00 00 00 00 00 00
  0x03ed4364dfe0: 00 00 00 fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x03ed4364dff0: fd fd fa fa fa fa 00 00 00 00 00 00 00 00 00 00
  0x03ed4364e000: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fa fa
  0x03ed4364e010: fa fa fd fd fd fd fd fd fd fd fd fd fa fa fa fa
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
==7956==ABORTING


## Timeline

### [Deleted User] (2021-09-15)

[Empty comment from Monorail migration]

### ca...@chromium.org (2021-09-15)

Setting severity high (since this presumably requires interaction with DevTools to trigger), and FoundIn-93 as this code has not changed recently.

dgozman: Can you help further triage this bug (and find an appropriate owner)? I wasn't able to reproduce (since there is no reproduction case in the report), but this seems plausible if GetFileSystems() gets called after FileSystemPathsSettingChanged().

[Monorail components: Platform>DevTools]

### [Deleted User] (2021-09-15)

[Empty comment from Monorail migration]

### dg...@chromium.org (2021-09-16)

[Empty comment from Monorail migration]

### bm...@chromium.org (2021-09-16)

Jaro & Danil, please take a look.

I'm reducing severity to medium, since it can only be triggered via the DevTools renderer (the only process that has access to the DevToolsUIBindings) and is likely limited to DevTools front-end itself then.

[Monorail components: -Platform>DevTools Platform>DevTools>Platform]

### bm...@chromium.org (2021-09-16)

[Empty comment from Monorail migration]

### ja...@chromium.org (2021-09-16)

 hackyzh002, could you tell us on which chromium version this was?

### ha...@gmail.com (2021-09-16)

It happen in chromium dev 96.0.4643.0 x64

### bm...@chromium.org (2021-09-16)

Bumping priority, since while the DevToolsUIBindings are only available to DevTools renderers, the UAF is in the browser process.

### ja...@chromium.org (2021-09-16)

The issue seems to be a data race between DevToolsFileHelper::FileSystemPathsSettingChanged and DevToolsFileHelper::GetFileSystems. They are invoked from different threads and there seems to by no synchronization.

Perhaps we need to handle DevToolsFileHelper::FileSystemPathsSettingChanged back on the main thread? I will try to cook a CL that handles the change notification on the main thread rather than the IO thread.

### [Deleted User] (2021-09-16)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-16)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-30)

jarin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2021-10-04)

Hello jarin,any response?

### ja...@chromium.org (2021-10-05)

CL in progress: https://chromium-review.googlesource.com/c/chromium/src/+/3172618, still going through code reviews.

### gi...@appspot.gserviceaccount.com (2021-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6bda8ff54af25de4feeae563ea8a040886bdb769

commit 6bda8ff54af25de4feeae563ea8a040886bdb769
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Wed Oct 06 06:17:22 2021

Run DevTools file system change handler on UI thread

There is no synchronization in the DevTools FileSystem
change handler, but it can be invoked on the IO thread.

This CL passes the change message to the UI thread
for the actual processing.

Bug: chromium:1249810
Change-Id: I49556da0c57a9ccd936179d12c04511ddea29e03
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3172618
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Reviewed-by: Simon Zünd <szuend@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/main@{#928550}

[modify] https://crrev.com/6bda8ff54af25de4feeae563ea8a040886bdb769/chrome/browser/devtools/devtools_file_helper.h
[modify] https://crrev.com/6bda8ff54af25de4feeae563ea8a040886bdb769/chrome/browser/devtools/devtools_file_helper.cc


### ja...@chromium.org (2021-10-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-07)

Requesting merge to stable M94 because latest trunk commit (928550) appears to be after stable branch point (911515).

Requesting merge to beta M95 because latest trunk commit (928550) appears to be after beta branch point (920003).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-07)

Merge review required: M95 is already shipping to beta.

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
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-07)

Merge review required: M94 is already shipping to stable.

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

### am...@chromium.org (2021-10-11)

merge approved to M95; please merge to branch 4638 as soon as possible so this fix can be included in tomorrow's 95 stable cut. 

merge also approved to M94; please merge to branch 4606 by EOD Friday so this fix can be included in the Extended Stable release for M94

### gi...@appspot.gserviceaccount.com (2021-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/01d6e2d93012480225e150c1ae73bc270a7d7a92

commit 01d6e2d93012480225e150c1ae73bc270a7d7a92
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Tue Oct 12 13:59:34 2021

Run DevTools file system change handler on UI thread

There is no synchronization in the DevTools FileSystem
change handler, but it can be invoked on the IO thread.

This CL passes the change message to the UI thread
for the actual processing.

(cherry picked from commit 6bda8ff54af25de4feeae563ea8a040886bdb769)

Bug: chromium:1249810
Change-Id: I49556da0c57a9ccd936179d12c04511ddea29e03
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3172618
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Reviewed-by: Simon Zünd <szuend@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#928550}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3218166
Auto-Submit: Jaroslav Sevcik <jarin@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Cr-Commit-Position: refs/branch-heads/4638@{#790}
Cr-Branched-From: 159257cab5585bc8421abf347984bb32fdfe9eb9-refs/heads/main@{#920003}

[modify] https://crrev.com/01d6e2d93012480225e150c1ae73bc270a7d7a92/chrome/browser/devtools/devtools_file_helper.h
[modify] https://crrev.com/01d6e2d93012480225e150c1ae73bc270a7d7a92/chrome/browser/devtools/devtools_file_helper.cc


### ja...@chromium.org (2021-10-13)

[Comment Deleted]

### ja...@chromium.org (2021-10-13)

Please ignore c26, that was meant for another bug. I am going ahead with the m94 merge.

### gi...@appspot.gserviceaccount.com (2021-10-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a0af9229eb1625e28ede99a374c830b0e9dec09a

commit a0af9229eb1625e28ede99a374c830b0e9dec09a
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Wed Oct 13 08:34:20 2021

Run DevTools file system change handler on UI thread

There is no synchronization in the DevTools FileSystem
change handler, but it can be invoked on the IO thread.

This CL passes the change message to the UI thread
for the actual processing.

(cherry picked from commit 6bda8ff54af25de4feeae563ea8a040886bdb769)

Bug: chromium:1249810
Change-Id: I49556da0c57a9ccd936179d12c04511ddea29e03
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3172618
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Reviewed-by: Simon Zünd <szuend@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#928550}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3218004
Reviewed-by: Yang Guo <yangguo@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#1353}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/a0af9229eb1625e28ede99a374c830b0e9dec09a/chrome/browser/devtools/devtools_file_helper.h
[modify] https://crrev.com/a0af9229eb1625e28ede99a374c830b0e9dec09a/chrome/browser/devtools/devtools_file_helper.cc


### am...@google.com (2021-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-13)

Congratulations-- the VRP Panel has decided to award you $10,000 for this report. Thank you for this report! 

### am...@google.com (2021-10-14)

[Empty comment from Monorail migration]

### ha...@gmail.com (2021-10-15)

Thanks,credit information:Zhihua Yao of KunLun Lab

### am...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-19)

[Empty comment from Monorail migration]

### rz...@google.com (2021-10-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-10-21)

extended stable labeling test 

### gi...@google.com (2021-10-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4c926456a81365cdd8e0a4fa67c02e812bd1b909

commit 4c926456a81365cdd8e0a4fa67c02e812bd1b909
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Tue Oct 26 13:46:25 2021

[M90-LTS] Run DevTools file system change handler on UI thread

There is no synchronization in the DevTools FileSystem
change handler, but it can be invoked on the IO thread.

This CL passes the change message to the UI thread
for the actual processing.

(cherry picked from commit 6bda8ff54af25de4feeae563ea8a040886bdb769)

Bug: chromium:1249810
Change-Id: I49556da0c57a9ccd936179d12c04511ddea29e03
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3172618
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#928550}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3234542
Reviewed-by: Michael Ershov <miersh@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1646}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/4c926456a81365cdd8e0a4fa67c02e812bd1b909/chrome/browser/devtools/devtools_file_helper.h
[modify] https://crrev.com/4c926456a81365cdd8e0a4fa67c02e812bd1b909/chrome/browser/devtools/devtools_file_helper.cc


### rz...@google.com (2021-10-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1249810?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057268)*

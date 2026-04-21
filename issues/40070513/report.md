# Security: heap-use-after-free in mojo::StringDataSource::Read

| Field | Value |
|-------|-------|
| **Issue ID** | [40070513](https://issues.chromium.org/issues/40070513) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2023-08-24 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

[TBD]

**VERSION**  

Chrome Version: 118.0.5966.0  

Operating System: Windows 11

**REPRODUCTION CASE**  

[TBD]

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

=================================================================  

==22932==ERROR: AddressSanitizer: heap-use-after-free on address 0x11e01c6f5928 at pc 0x7ffadf577959 bp 0x005edb7febe0 sp 0x005edb7fec28  

READ of size 1 at 0x11e01c6f5928 thread T4  

==22932==WARNING: Failed to use and restart external symbolizer!  

==22932==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==22932==\*\*\* Most likely this means that the app is already \*\*\*  

==22932==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==22932==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==22932==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ffadf577958 in mojo::StringDataSource::Read C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\string\_data\_source.cc:41  

#1 0x7ffadf585040 in mojo::DataPipeProducer::SequenceState::TransferSomeBytes C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\data\_pipe\_producer.cc:139  

#2 0x7ffadf585674 in base::internal::Invoker<base::internal::BindState<void (mojo::DataPipeProducer::SequenceState::\*)(unsigned int, const mojo::HandleSignalsState &),scoped\_refptr[mojo::DataPipeProducer::SequenceState](javascript:void(0);) >,void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:957  

#3 0x7ffadf57a7ca in base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#4 0x7ffadf579de3 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:278  

#5 0x7ffadf57b185 in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);),int,unsigned int,mojo::HandleSignalsState>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:944  

#6 0x7ffaded9c3c6 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:201  

#7 0x7ffae6a897df in base::internal::TaskTracker::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\task\_tracker.cc:643  

#8 0x7ffae6a8a9e9 in base::internal::TaskTracker::RunSkipOnShutdown C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\task\_tracker.cc:628  

#9 0x7ffae6a88b8a in base::internal::TaskTracker::RunTask C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\task\_tracker.cc:485  

#10 0x7ffae6a87c2f in base::internal::TaskTracker::RunAndPopNextTask C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\task\_tracker.cc:400  

#11 0x7ffaec03baab in base::internal::WorkerThread::RunWorker C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\worker\_thread.cc:483  

#12 0x7ffaec03ac7f in base::internal::WorkerThread::RunPooledWorker C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\worker\_thread.cc:359  

#13 0x7ffadecb4231 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:133  

#14 0x7ff70dfff9b5 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:291  

#15 0x7ffba6f6257c in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x18001257c)  

#16 0x7ffba7e4aa67 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005aa67)

0x11e01c6f5928 is located 86312 bytes inside of 114416-byte region [0x11e01c6e0800,0x11e01c6fc6f0)  

freed by thread T0 here:  

#0 0x7ff70e008ebd in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffade68646b in extensions::`anonymous namespace'::ExtensionLocalizationURLLoader::~ExtensionLocalizationURLLoader C:\b\s\w\ir\cache\builder\src\extensions\renderer\extension\_localization\_throttle.cc:42  

#2 0x7ffad49d7eb6 in mojo::internal::SelfOwnedReceiver[network::mojom::URLLoader](javascript:void(0);)::OnDisconnect C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\self\_owned\_receiver.h:109  

#3 0x7ffad49d89f8 in base::internal::Invoker<base::internal::BindState<void (mojo::internal::SelfOwnedReceiver[network::mojom::URLLoader](javascript:void(0);)::\*)(unsigned int, const std::\_\_Cr::basic\_string<char,std::\_\_Cr::char\_traits<char>,std::\_\_Cr::allocator<char> > &),base::internal::UnretainedWrapper<mojo::internal::SelfOwnedReceiver[network::mojom::URLLoader](javascript:void(0);),base::unretained\_traits::MayNotDangle,0> >,void (unsigned int, const std::\_\_Cr::basic\_string<char,std::\_\_Cr::char\_traits<char>,std::\_\_Cr::allocator<char> > &)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:944  

#4 0x7ffadf539dcf in mojo::InterfaceEndpointClient::NotifyError C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:745  

#5 0x7ffadf528057 in mojo::internal::MultiplexRouter::ProcessNotifyErrorTask C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:1010  

#6 0x7ffadf5206f9 in mojo::internal::MultiplexRouter::ProcessTasks C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:923  

#7 0x7ffadf51cac6 in mojo::internal::MultiplexRouter::OnPipeConnectionError C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:833  

#8 0x7ffadf52c6f0 in base::internal::Invoker<base::internal::BindState<void (mojo::internal::MultiplexRouter::\*)(bool),base::internal::UnretainedWrapper[mojo::internal::MultiplexRouter,base::unretained\_traits::MayNotDangle,0](javascript:void(0);),bool>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:944  

#9 0x7ffadf549056 in mojo::Connector::HandleError C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:688  

#10 0x7ffadf54b353 in mojo::Connector::OnWatcherHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:417  

#11 0x7ffadf54d899 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(const char \*, unsigned int),base::internal::UnretainedWrapper[mojo::Connector,base::unretained\_traits::MayNotDangle,0](javascript:void(0);),base::internal::UnretainedWrapper<const char,base::unretained\_traits::MayNotDangle,0> >,void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:957  

#12 0x7ffad49d690d in base::RepeatingCallback<void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#13 0x7ffad49d6733 in base::internal::Invoker<base::internal::BindState<void (\*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:957  

#14 0x7ffadf57a7ca in base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#15 0x7ffadf579de3 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:278  

#16 0x7ffadf57b185 in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);),int,unsigned int,mojo::HandleSignalsState>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:944  

#17 0x7ffaded9c3c6 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:201  

#18 0x7ffae25cd882 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:480  

#19 0x7ffae25cc60f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:345  

#20 0x7ffae26083d3 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:40  

#21 0x7ffae25cffaf in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:645  

#22 0x7ffadee05a17 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#23 0x7ffae1d2ba8f in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:339  

#24 0x7ffadd47c213 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:745  

#25 0x7ffadd47f023 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1118  

#26 0x7ffadd479c90 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:326  

#27 0x7ffadd47a91d in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:343

previously allocated by thread T0 here:  

#0 0x7ff70e008fbd in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffaf5223c5e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffade8f6d0c in std::\_\_Cr::basic\_string<char,std::\_\_Cr::char\_traits<char>,std::\_\_Cr::allocator<char> >::\_\_grow\_by\_and\_replace C:\b\s\w\ir\cache\builder\src\third\_party\libc++\src\include\string:2261  

#3 0x7ffade8f7c7f in std::\_\_Cr::basic\_string<char,std::\_\_Cr::char\_traits<char>,std::\_\_Cr::allocator<char> >::append C:\b\s\w\ir\cache\builder\src\third\_party\libc++\src\include\string:2576  

#4 0x7ffadf58719f in mojo::DataPipeDrainer::ReadData C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\data\_pipe\_drainer.cc:37  

#5 0x7ffadf58751d in base::internal::Invoker<base::internal::BindState<void (mojo::DataPipeDrainer::\*)(unsigned int),base::WeakPtr[mojo::DataPipeDrainer](javascript:void(0);) >,void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:957  

#6 0x7ffad49d690d in base::RepeatingCallback<void (unsigned int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#7 0x7ffad49d6733 in base::internal::Invoker<base::internal::BindState<void (\*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:957  

#8 0x7ffadf57a7ca in base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:333  

#9 0x7ffadf579de3 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:278  

#10 0x7ffadf57b185 in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);),int,unsigned int,mojo::HandleSignalsState>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:944  

#11 0x7ffaded9c3c6 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:201  

#12 0x7ffae25cd882 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:480  

#13 0x7ffae25cc60f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:345  

#14 0x7ffae26083d3 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:40  

#15 0x7ffae25cffaf in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:645  

#16 0x7ffadee05a17 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#17 0x7ffae1d2ba8f in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:339  

#18 0x7ffadd47c213 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:745  

#19 0x7ffadd47f023 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1118  

#20 0x7ffadd479c90 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:326  

#21 0x7ffadd47a91d in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:343  

#22 0x7ffad0d11722 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:187  

#23 0x7ff70df46184 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#24 0x7ff70df42b7e in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:390  

#25 0x7ff70e36f2cb in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#26 0x7ffba6f6257c in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x18001257c)  

#27 0x7ffba7e4aa67 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005aa67)

Thread T4 created by T0 here:  

#0 0x7ff70dffe4f2 in CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7ffadecb2f8f in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:198 #2 0x7ffaec0394f9 in base::internal::WorkerThread::Start C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:196 #3 0x7ffae6aa82b5 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl::<lambda_2>::operator() C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:178 #4 0x7ffae6aa7dc7 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::WorkerContainer::ForEachWorker<`lambda at ....\base\task\thread\_pool\thread\_group\_impl.cc:177:37'> C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\thread\_group\_impl.cc:145  

#5 0x7ffae6aa7554 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\thread\_group\_impl.cc:177  

#6 0x7ffae6a9e525 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\thread\_group\_impl.cc:101  

#7 0x7ffae6a9e12b in base::internal::ThreadGroupImpl::Start C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\thread\_group\_impl.cc:407  

#8 0x7ffae259ecd8 in base::internal::ThreadPoolImpl::Start C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\thread\_pool\_impl.cc:212  

#9 0x7ffae1a058d9 in content::ChildProcess::ChildProcess C:\b\s\w\ir\cache\builder\src\content\child\child\_process.cc:120  

#10 0x7ffaeabc066d in content::RenderProcess::RenderProcess C:\b\s\w\ir\cache\builder\src\content\renderer\render\_process.cc:18  

#11 0x7ffae58fed34 in content::RenderProcessImpl::RenderProcessImpl C:\b\s\w\ir\cache\builder\src\content\renderer\render\_process\_impl.cc:102  

#12 0x7ffae58ff37b in content::RenderProcessImpl::Create C:\b\s\w\ir\cache\builder\src\content\renderer\render\_process\_impl.cc:271  

#13 0x7ffae1d2b47c in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:281  

#14 0x7ffadd47c213 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:745  

#15 0x7ffadd47f023 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1118  

#16 0x7ffadd479c90 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:326  

#17 0x7ffadd47a91d in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:343  

#18 0x7ffad0d11722 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:187  

#19 0x7ff70df46184 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#20 0x7ff70df42b7e in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:390  

#21 0x7ff70e36f2cb in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#22 0x7ffba6f6257c in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x18001257c)  

#23 0x7ffba7e4aa67 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005aa67)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\string\_data\_source.cc:41 in mojo::StringDataSource::Read

Shadow bytes around the buggy address:  

0x11e01c6f5680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11e01c6f5700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11e01c6f5780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11e01c6f5800: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11e01c6f5880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x11e01c6f5900: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd  

0x11e01c6f5980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11e01c6f5a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11e01c6f5a80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11e01c6f5b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x11e01c6f5b80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==22932==ADDITIONAL INFO

==22932==Note: Please include this section with the ASan report.  

Task trace:  

#0 0x7ffadf57ac59 in mojo::SimpleWatcher::Context::Notify C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:102  

#1 0x7ffadf57ac59 in mojo::SimpleWatcher::Context::Notify C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:102  

#2 0x7ffadf58270e in mojo::DataPipeProducer::SequenceState::Start C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\data\_pipe\_producer.cc:63  

#3 0x7ffadf579718 in mojo::SimpleWatcher::ArmOrNotify C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:238

==22932==END OF ADDITIONAL INFO  

==22932==ABORTING

## Attachments

- [poc.css](attachments/poc.css) (text/plain, 2.9 MB)
- [manifest.json](attachments/manifest.json) (text/plain, 347 B)
- [background.js](attachments/background.js) (text/plain, 50 B)
- [poc.html](attachments/poc.html) (text/plain, 54 B)

## Timeline

### [Deleted User] (2023-08-24)

[Empty comment from Monorail migration]

### mp...@chromium.org (2023-08-28)

Do you have a PoC? When did this crash occur?

### mp...@chromium.org (2023-08-28)

horo@ we don't have a PoC but could this be because  uses STRING_STAYS_VALID_UNTIL_COMPLETION? https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/extension_localization_throttle.cc;drc=f2732aef3e95dca51f5d70c1242f0c7614a0b9aa;l=139

[Monorail components: Platform>Extensions]

### mp...@chromium.org (2023-08-28)

horo@ please see previous comment

### [Deleted User] (2023-08-29)

[Empty comment from Monorail migration]

### ho...@chromium.org (2023-08-29)

[Empty comment from Monorail migration]

### st...@gmail.com (2023-08-29)

Hi, thanks for triaging this. I have a PoC, but I am working on making it less flaky. However, I am currently AFK, so I will be able to share it in a week or two.
But this is essentially what I know about how to repro the bug:
1. Open an extension popup which loads a huge stylesheet (or any resource?)
2. Close the extension popup (x?) seconds later

Config: No enabled features/flags needed. No extension permissions. No user interaction.

Again, sorry for not having a PoC ready yet.

### [Deleted User] (2023-08-29)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-09-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b6e060e17ed9e46b3043a3c369fc10cbbe2245d8

commit b6e060e17ed9e46b3043a3c369fc10cbbe2245d8
Author: Tsuyoshi Horo <horo@chromium.org>
Date: Fri Sep 01 01:45:55 2023

Fix DataPipeDrainer usage in ExtensionLocalizationURLLoader

There is a bug that when ExtensionLocalizationURLLoader is destructed
by canceling the CSS requests from extensions, DataPipeProducer may
cause UAF.
This is because DataPipeProducer is not correctly used in
ExtensionLocalizationURLLoader. DataPipeProducer and the data must be
kept alive until notified of completion.

This CL fix this by changing ExtensionLocalizationURLLoader to keep
DataPipeProducer and the data even if ExtensionLocalizationURLLoader
itself is destructed.

Bug: 1475798
Change-Id: I013396f2c49f4712914b917c3330b99a1be791b8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4821086
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: David Bertoni <dbertoni@chromium.org>
Commit-Queue: Tsuyoshi Horo <horo@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1191115}

[modify] https://crrev.com/b6e060e17ed9e46b3043a3c369fc10cbbe2245d8/extensions/renderer/extension_localization_throttle.cc
[modify] https://crrev.com/b6e060e17ed9e46b3043a3c369fc10cbbe2245d8/extensions/renderer/extension_localization_throttle_unittest.cc


### ho...@chromium.org (2023-09-02)

[Empty comment from Monorail migration]

### ho...@chromium.org (2023-09-02)

I think the severity is low because this problem happens only when CSS requests from extensions are canceled and the background thread is slow.

### [Deleted User] (2023-09-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-02)

[Empty comment from Monorail migration]

### mp...@chromium.org (2023-09-06)

Re https://crbug.com/chromium/1475798#c11. How are CSS requests from extensions cancelled? What triggers the cancellation? Can attackers trigger the cancellation?

As for the background thread being slow we should never assume that attackers will have difficulty massaging timing (and other things like heap layout) to fit their attack.

I think for now we should mark this as High Severity. It's a way to take over an extension process, depending on how CSS requests are cancelled. See the severity guidelines: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#toc-high-severity

### mp...@chromium.org (2023-09-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-06)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-06)

Requesting merge to stable M116 because latest trunk commit (1191115) appears to be after stable branch point (1160321).

Requesting merge to beta M117 because latest trunk commit (1191115) appears to be after beta branch point (1181205).

Merge review required: M116 is already shipping to stable.

Merge review required: M117 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116, 117].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2023-09-07)


1. Which CLs should be backmerged? (Please include Gerrit links.)
https://chromium-review.googlesource.com/c/chromium/src/+/4821086

2. Has this fix been tested on Canary?
No I couldn't reproduce this manually in Chrome. I can reproduce this issue only in unit test.

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
Yes.

4. Does this fix pose any known compatibility risks?
No.

5. Does it require manual verification by the test team? If so, please describe required testing
No. 

### [Deleted User] (2023-09-07)

Requesting merge to extended stable M116 because latest trunk commit (1191115) appears to be after extended stable branch point (1160321).

Requesting merge to stable M117 because latest trunk commit (1191115) appears to be after stable branch point (1181205).

Not requesting merge to dev (M118) because latest trunk commit (1191115) appears to be prior to dev branch point (1192594). If this is incorrect, please replace the Merge-NA-118 label with Merge-Request-118. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge approved: your change passed merge requirements and is auto-approved for M118. Please go ahead and merge the CL to branch 5993 (refs/branch-heads/5993) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), govind (iOS), ceb (ChromeOS), danielyip (Desktop)

Merge review required: M116 is already shipping to stable.

Merge review required: M117 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116, 117].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2023-09-08)

1. Which CLs should be backmerged? (Please include Gerrit links.)
https://chromium-review.googlesource.com/c/chromium/src/+/4821086

2. Has this fix been tested on Canary?
No I couldn't reproduce this manually in Chrome. I can reproduce this issue only in unit test.

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
Yes.

4. Does this fix pose any known compatibility risks?
No.

5. Does it require manual verification by the test team? If so, please describe required testing
No.


### [Deleted User] (2023-09-11)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2023-09-11)

https://chromium-review.googlesource.com/c/chromium/src/+/4821086 is in M118. So, we don't need to merge to M118.
We need to merge to M117 and M116. But there is no Merge-Approved-117 nor Merge-Approved-116 yet.

### am...@chromium.org (2023-09-11)

Thanks for this information. Due to the timing of when this fix landed -- after the RC cut for M117 Stable, we are purposed holding off merge approvals for this issue for now. M117 Stable is being released tomorrow and M116 Stable / Extended Stable was recut late last week and was released early today to accommodate a Pri-0 security fix. We'll review / assess for merge tomorrow so this fix can ship in the next M117 Stable and M116 Extended Stable respins next week. 

### st...@gmail.com (2023-09-12)

I have retested this and I was not able to reproduce this after the fix. The PoC needs more tweaking as it's somewhat flaky, but does trigger the bug in the vulnerable versions of Chrome (and not in versions after the fix), so I think this should be enough to confirm the fix.



### am...@chromium.org (2023-09-13)

merges for https://crrev.com/c/4821086 approved, please merge this fix to M117 Stable / branch 5938 and M116 Extended Stable / branch 5845 by EOD Thursday, 14 September so this fix can be included in next weeks M117 Stable security refresh -- thank you

### gi...@appspot.gserviceaccount.com (2023-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0623eab92821eea83fe35a8f03bc56d488a9f15c

commit 0623eab92821eea83fe35a8f03bc56d488a9f15c
Author: Tsuyoshi Horo <horo@chromium.org>
Date: Wed Sep 13 18:15:08 2023

[M117] Fix DataPipeDrainer usage in ExtensionLocalizationURLLoader

There is a bug that when ExtensionLocalizationURLLoader is destructed
by canceling the CSS requests from extensions, DataPipeProducer may
cause UAF.
This is because DataPipeProducer is not correctly used in
ExtensionLocalizationURLLoader. DataPipeProducer and the data must be
kept alive until notified of completion.

This CL fix this by changing ExtensionLocalizationURLLoader to keep
DataPipeProducer and the data even if ExtensionLocalizationURLLoader
itself is destructed.

(cherry picked from commit b6e060e17ed9e46b3043a3c369fc10cbbe2245d8)

Bug: 1475798
Change-Id: I013396f2c49f4712914b917c3330b99a1be791b8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4821086
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: David Bertoni <dbertoni@chromium.org>
Commit-Queue: Tsuyoshi Horo <horo@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1191115}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4860250
Commit-Queue: David Bertoni <dbertoni@chromium.org>
Auto-Submit: Tsuyoshi Horo <horo@chromium.org>
Cr-Commit-Position: refs/branch-heads/5938@{#1279}
Cr-Branched-From: 2b50cb4bcc2318034581a816714d9535dc38966d-refs/heads/main@{#1181205}

[modify] https://crrev.com/0623eab92821eea83fe35a8f03bc56d488a9f15c/extensions/renderer/extension_localization_throttle.cc
[modify] https://crrev.com/0623eab92821eea83fe35a8f03bc56d488a9f15c/extensions/renderer/extension_localization_throttle_unittest.cc


### [Deleted User] (2023-09-13)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/454452c4ec1edd39dbb2341305ec8e27ee956b2c

commit 454452c4ec1edd39dbb2341305ec8e27ee956b2c
Author: Tsuyoshi Horo <horo@chromium.org>
Date: Wed Sep 13 19:54:33 2023

[M116] Fix DataPipeDrainer usage in ExtensionLocalizationURLLoader

There is a bug that when ExtensionLocalizationURLLoader is destructed
by canceling the CSS requests from extensions, DataPipeProducer may
cause UAF.
This is because DataPipeProducer is not correctly used in
ExtensionLocalizationURLLoader. DataPipeProducer and the data must be
kept alive until notified of completion.

This CL fix this by changing ExtensionLocalizationURLLoader to keep
DataPipeProducer and the data even if ExtensionLocalizationURLLoader
itself is destructed.

(cherry picked from commit b6e060e17ed9e46b3043a3c369fc10cbbe2245d8)

Bug: 1475798
Change-Id: I013396f2c49f4712914b917c3330b99a1be791b8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4821086
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: David Bertoni <dbertoni@chromium.org>
Commit-Queue: Tsuyoshi Horo <horo@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1191115}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4862200
Auto-Submit: Tsuyoshi Horo <horo@chromium.org>
Cr-Commit-Position: refs/branch-heads/5845@{#1810}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/454452c4ec1edd39dbb2341305ec8e27ee956b2c/extensions/renderer/extension_localization_throttle.cc
[modify] https://crrev.com/454452c4ec1edd39dbb2341305ec8e27ee956b2c/extensions/renderer/extension_localization_throttle_unittest.cc


### am...@google.com (2023-09-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-14)

Congratulations Thomas! The VRP Panel has decided to award you $2,000 for this renderer process UAF mitigated by race condition and requiring an extension. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-09-17)

[Empty comment from Monorail migration]

### rz...@google.com (2023-09-18)

[Empty comment from Monorail migration]

### rz...@google.com (2023-09-18)

Changed code doesn't exist in 108.

### rz...@google.com (2023-09-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-19)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-09-19)

1. Just https://crrev.com/c/4872577
2. Low, no conflicts
3. 116, 117
4. Yes

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-26)

[Empty comment from Monorail migration]

### gm...@google.com (2023-09-27)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/309b604c4e883f549693dd05d58a3e806a537d46

commit 309b604c4e883f549693dd05d58a3e806a537d46
Author: Tsuyoshi Horo <horo@chromium.org>
Date: Fri Sep 29 08:13:50 2023

[M114-LTS] Fix DataPipeDrainer usage in ExtensionLocalizationURLLoader

There is a bug that when ExtensionLocalizationURLLoader is destructed
by canceling the CSS requests from extensions, DataPipeProducer may
cause UAF.
This is because DataPipeProducer is not correctly used in
ExtensionLocalizationURLLoader. DataPipeProducer and the data must be
kept alive until notified of completion.

This CL fix this by changing ExtensionLocalizationURLLoader to keep
DataPipeProducer and the data even if ExtensionLocalizationURLLoader
itself is destructed.

(cherry picked from commit b6e060e17ed9e46b3043a3c369fc10cbbe2245d8)

Bug: 1475798
Change-Id: I013396f2c49f4712914b917c3330b99a1be791b8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4821086
Commit-Queue: Tsuyoshi Horo <horo@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1191115}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4872577
Commit-Queue: Zakhar Voit <voit@google.com>
Owners-Override: Victor Gabriel Savu <vsavu@google.com>
Reviewed-by: Victor Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1611}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/309b604c4e883f549693dd05d58a3e806a537d46/extensions/renderer/extension_localization_throttle.cc
[modify] https://crrev.com/309b604c4e883f549693dd05d58a3e806a537d46/extensions/renderer/extension_localization_throttle_unittest.cc


### vo...@google.com (2023-09-29)

[Empty comment from Monorail migration]

### gm...@google.com (2023-10-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1475798?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40070513)*

# UAF in net::HttpStreamPool::Group::ProcessPendingRequest

| Field | Value |
|-------|-------|
| **Issue ID** | [399995424](https://issues.chromium.org/issues/399995424) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Network |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | ba...@chromium.org |
| **Created** | 2025-03-02 |
| **Bounty** | $10,000.00 |

## Description

VULNERABILITY DETAILS
I found a heap-use-after-free bug in Chromium's network stack, specifically in the HttpStreamPool component. The crash happens when code tries to access an AttemptManager object after it's been freed. This looks like a  issue in how HTTP connections are managed. The bug happens during I fuzz the chromium with the `iframe`  tags in the Extension Popup windows. 

The crash occurs when std::__Cr::unique_ptr<net::HttpStreamPool::AttemptManager> is dereferenced after its memory has been freed. The issue happens during HTTP stream lifecycle management, specifically when a stream socket is being released.
Group::ReleaseStreamSocket() is called to return a socket to the pool
During this process, Group::ProcessPendingRequest() tries to access an AttemptManager object
However, the Group object containing this pointer has already been freed

VERSION
Chromium:	135.0.7034.0 (Developer Build) (64-bit) 
OS:	Windows 11 Version 24H2 (Build 26120.3291)

REPRODUCTION CASE

It's very difficult for me to reproduce this vulnerability. The crash occurred when I was loading iframe tags within extension popup windows, and the http webserver I set up probably isn't robust enough, which led to this crash.
And there is no special switches when I fuzz.


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
```log
=================================================================
==12236==ERROR: AddressSanitizer: heap-use-after-free on address 0x116bfbbf4790 at pc 0x7ff8deba1677 bp 0x0010591fbf80 sp 0x0010591fbfc8
READ of size 8 at 0x116bfbbf4790 thread T6
#0 0x7ff8deba1676 in std::__Cr::unique_ptr<net::HttpStreamPool::AttemptManager,std::__Cr::default_delete<net::HttpStreamPool::AttemptManager> >::operator bool C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:274
#1 0x7ff8deba1676 in net::HttpStreamPool::Group::ProcessPendingRequest C:\b\s\w\ir\cache\builder\src\net\http\http_stream_pool_group.cc:270
#2 0x7ff8deba1676 in net::HttpStreamPool::Group::ReleaseStreamSocket(class std::__Cr::unique_ptr<class net::StreamSocket, struct std::__Cr::default_delete<class net::StreamSocket>>, __int64) C:\b\s\w\ir\cache\builder\src\net\http\http_stream_pool_group.cc:207:5
#3 0x7ff8e24b3cc2 in net::HttpStreamPoolHandle::Reset(void) C:\b\s\w\ir\cache\builder\src\net\http\http_stream_pool_handle.cc:35:13
#4 0x7ff8e2720580 in net::HttpNetworkTransaction::DoReadBodyComplete(int) C:\b\s\w\ir\cache\builder\src\net\http\http_network_transaction.cc:1562:14
#5 0x7ff8e271268e in net::HttpNetworkTransaction::DoLoop(int) C:\b\s\w\ir\cache\builder\src\net\http\http_network_transaction.cc:906:14
#6 0x7ff8e27158b7 in net::HttpNetworkTransaction::Read(class net::IOBuffer *, int, class base::OnceCallback<(int)>) C:\b\s\w\ir\cache\builder\src\net\http\http_network_transaction.cc:478:12
#7 0x7ff8df277623 in network::ThrottlingNetworkTransaction::Read(class net::IOBuffer *, int, class base::OnceCallback<(int)>) C:\b\s\w\ir\cache\builder\src\services\network\throttling\throttling_network_transaction.cc:209:34
#8 0x7ff8e2743b5e in net::URLRequestHttpJob::ReadRawData(class net::IOBuffer *, int) C:\b\s\w\ir\cache\builder\src\net\url_request\url_request_http_job.cc:1781:21
#9 0x7ff8d0b65a5d in net::URLRequestJob::ReadRawDataHelper(class net::IOBuffer *, int, class base::OnceCallback<(int)>) C:\b\s\w\ir\cache\builder\src\net\url_request\url_request_job.cc:685:16
#10 0x7ff8d0b66d83 in net::URLRequestJob::URLRequestJobSourceStream::Read(class net::IOBuffer *, int, class base::OnceCallback<(int)>) C:\b\s\w\ir\cache\builder\src\net\url_request\url_request_job.cc:77:18
#11 0x7ff8d0c1dd34 in net::FilterSourceStream::DoReadData C:\b\s\w\ir\cache\builder\src\net\filter\filter_source_stream.cc:135
#12 0x7ff8d0c1dd34 in net::FilterSourceStream::DoLoop(int) C:\b\s\w\ir\cache\builder\src\net\filter\filter_source_stream.cc:111:14
#13 0x7ff8d0c1f1ea in net::FilterSourceStream::OnIOComplete(int) C:\b\s\w\ir\cache\builder\src\net\filter\filter_source_stream.cc:204:12
#14 0x7ff8d0c1f71f in base::internal::DecayedFunctorTraits<void (net::FilterSourceStream::*)(int),net::FilterSourceStream *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:728
#15 0x7ff8d0c1f71f in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (net::FilterSourceStream::*&&)(int),net::FilterSourceStream *>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:920
#16 0x7ff8d0c1f71f in base::internal::Invoker<base::internal::FunctorTraits<void (net::FilterSourceStream::*&&)(int),net::FilterSourceStream *>,base::internal::BindState<1,1,0,void (net::FilterSourceStream::*)(int),base::internal::UnretainedWrapper<net::FilterSourceStream,base::unretained_traits::MayNotDangle,0> >,void (int)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1057
#17 0x7ff8d0c1f71f in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl net::FilterSourceStream::*&&)(int), class net::FilterSourceStream *>, struct base::internal::BindState<1, 1, 0, void (__cdecl net::FilterSourceStream::*)(int), class base::internal::UnretainedWrapper<class net::FilterSourceStream, struct base::unretained_traits::MayNotDangle, 0>>, (int)>::RunOnce(class base::internal::BindStateBase *, int) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970:12
#18 0x7ff8d0b64d2e in base::OnceCallback<void (int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
#19 0x7ff8d0b64d2e in net::URLRequestJob::ReadRawDataComplete(int) C:\b\s\w\ir\cache\builder\src\net\url_request\url_request_job.cc:540:33
#20 0x7ff8e273ee95 in net::URLRequestHttpJob::OnReadCompleted(int) C:\b\s\w\ir\cache\builder\src\net\url_request\url_request_http_job.cc:1356:3
#21 0x7ff8e27468ff in base::internal::DecayedFunctorTraits<void (net::URLRequestHttpJob::*)(int),net::URLRequestHttpJob *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:728
#22 0x7ff8e27468ff in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (net::URLRequestHttpJob::*&&)(int),net::URLRequestHttpJob *>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:920
#23 0x7ff8e27468ff in base::internal::Invoker<base::internal::FunctorTraits<void (net::URLRequestHttpJob::*&&)(int),net::URLRequestHttpJob *>,base::internal::BindState<1,1,0,void (net::URLRequestHttpJob::*)(int),base::internal::UnretainedWrapper<net::URLRequestHttpJob,base::unretained_traits::MayNotDangle,0> >,void (int)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1057
#24 0x7ff8e27468ff in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl net::URLRequestHttpJob::*&&)(int), class net::URLRequestHttpJob *>, struct base::internal::BindState<1, 1, 0, void (__cdecl net::URLRequestHttpJob::*)(int), class base::internal::UnretainedWrapper<class net::URLRequestHttpJob, struct base::unretained_traits::MayNotDangle, 0>>, (int)>::RunOnce(class base::internal::BindStateBase *, int) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970:12
#25 0x7ff8e270fbf3 in base::OnceCallback<void (int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
#26 0x7ff8e270fbf3 in net::HttpNetworkTransaction::DoCallback C:\b\s\w\ir\cache\builder\src\net\http\http_network_transaction.cc:811
#27 0x7ff8e270fbf3 in net::HttpNetworkTransaction::OnIOComplete(int) C:\b\s\w\ir\cache\builder\src\net\http\http_network_transaction.cc:817:5
#28 0x7ff8e2726237 in base::internal::DecayedFunctorTraits<void (net::HttpNetworkTransaction::*)(int),net::HttpNetworkTransaction *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:728
#29 0x7ff8e2726237 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (net::HttpNetworkTransaction::*const &)(int),net::HttpNetworkTransaction *>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:920
#30 0x7ff8e2726237 in base::internal::Invoker<base::internal::FunctorTraits<void (net::HttpNetworkTransaction::*const &)(int),net::HttpNetworkTransaction *>,base::internal::BindState<1,1,0,void (net::HttpNetworkTransaction::*)(int),base::internal::UnretainedWrapper<net::HttpNetworkTransaction,base::unretained_traits::MayNotDangle,0> >,void (int)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1057
#31 0x7ff8e2726237 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl net::HttpNetworkTransaction::*&&)(int), class net::HttpNetworkTransaction *>, struct base::internal::BindState<1, 1, 0, void (__cdecl net::HttpNetworkTransaction::*)(int), class base::internal::UnretainedWrapper<class net::HttpNetworkTransaction, struct base::unretained_traits::MayNotDangle, 0>>, (int)>::RunOnce(class base::internal::BindStateBase *, int) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970:12
#32 0x7ff8e43748ed in base::OnceCallback<void (int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
#33 0x7ff8e43748ed in net::HttpStreamParser::OnIOComplete(int) C:\b\s\w\ir\cache\builder\src\net\http\http_stream_parser.cc:380:26
#34 0x7ff8e4380d94 in base::internal::DecayedFunctorTraits<void (net::HttpStreamParser::*)(int),const base::WeakPtr<net::HttpStreamParser> &>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:728
#35 0x7ff8e4380d94 in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (net::HttpStreamParser::*const &)(int),const base::WeakPtr<net::HttpStreamParser> &>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:944
#36 0x7ff8e4380d94 in base::internal::Invoker<base::internal::FunctorTraits<void (net::HttpStreamParser::*const &)(int),const base::WeakPtr<net::HttpStreamParser> &>,base::internal::BindState<1,1,0,void (net::HttpStreamParser::*)(int),base::WeakPtr<net::HttpStreamParser> >,void (int)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1057
#37 0x7ff8e4380d94 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl net::HttpStreamParser::*&&)(int), class base::WeakPtr<class net::HttpStreamParser> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl net::HttpStreamParser::*)(int), class base::WeakPtr<class net::HttpStreamParser>>, (int)>::RunOnce(class base::internal::BindStateBase *, int) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970:12
#38 0x7ff8d56cad06 in base::OnceCallback<void (int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
#39 0x7ff8d56cad06 in net::TCPClientSocket::DidCompleteReadWrite C:\b\s\w\ir\cache\builder\src\net\socket\tcp_client_socket.cc:535
#40 0x7ff8d56cad06 in net::TCPClientSocket::DidCompleteRead(int) C:\b\s\w\ir\cache\builder\src\net\socket\tcp_client_socket.cc:522:3
#41 0x7ff8d56ce227 in base::internal::DecayedFunctorTraits<void (net::TCPClientSocket::*)(int),net::TCPClientSocket *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:728
#42 0x7ff8d56ce227 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (net::TCPClientSocket::*&&)(int),net::TCPClientSocket *>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:920
#43 0x7ff8d56ce227 in base::internal::Invoker<base::internal::FunctorTraits<void (net::TCPClientSocket::*&&)(int),net::TCPClientSocket *>,base::internal::BindState<1,1,0,void (net::TCPClientSocket::*)(int),base::internal::UnretainedWrapper<net::TCPClientSocket,base::unretained_traits::MayNotDangle,0> >,void (int)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1057
#44 0x7ff8d56ce227 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl net::TCPClientSocket::*&&)(int), class net::TCPClientSocket *>, struct base::internal::BindState<1, 1, 0, void (__cdecl net::TCPClientSocket::*)(int), class base::internal::UnretainedWrapper<class net::TCPClientSocket, struct base::unretained_traits::MayNotDangle, 0>>, (int)>::RunOnce(class base::internal::BindStateBase *, int) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970:12
#45 0x7ff8d56c436e in base::OnceCallback<void (int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
#46 0x7ff8d56c436e in net::TCPSocketDefaultWin::RetryRead(int) C:\b\s\w\ir\cache\builder\src\net\socket\tcp_socket_win.cc:1060:29
#47 0x7ff8d56c81af in base::internal::DecayedFunctorTraits<void (net::TCPSocketDefaultWin::*)(int),net::TCPSocketDefaultWin *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:728
#48 0x7ff8d56c81af in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (net::TCPSocketDefaultWin::*&&)(int),net::TCPSocketDefaultWin *>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:920
#49 0x7ff8d56c81af in base::internal::Invoker<base::internal::FunctorTraits<void (net::TCPSocketDefaultWin::*&&)(int),net::TCPSocketDefaultWin *>,base::internal::BindState<1,1,0,void (net::TCPSocketDefaultWin::*)(int),base::internal::UnretainedWrapper<net::TCPSocketDefaultWin,base::unretained_traits::MayNotDangle,0> >,void (int)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1057
#50 0x7ff8d56c81af in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl net::TCPSocketDefaultWin::*&&)(int), class net::TCPSocketDefaultWin *>, struct base::internal::BindState<1, 1, 0, void (__cdecl net::TCPSocketDefaultWin::*)(int), class base::internal::UnretainedWrapper<class net::TCPSocketDefaultWin, struct base::unretained_traits::MayNotDangle, 0>>, (int)>::RunOnce(class base::internal::BindStateBase *, int) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970:12
#51 0x7ff8d56be20c in base::OnceCallback<void (int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
#52 0x7ff8d56be20c in net::TCPSocketDefaultWin::DidSignalRead(void) C:\b\s\w\ir\cache\builder\src\net\socket\tcp_socket_win.cc:1161:38
#53 0x7ff8d027f737 in base::internal::DecayedFunctorTraits<void (base::win::ObjectWatcher::*)(base::win::ObjectWatcher::Delegate *),const base::WeakPtr<base::win::ObjectWatcher> &,base::win::ObjectWatcher::Delegate *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:728
#54 0x7ff8d027f737 in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (base::win::ObjectWatcher::*const &)(base::win::ObjectWatcher::Delegate *),const base::WeakPtr<base::win::ObjectWatcher> &,base::win::ObjectWatcher::Delegate *>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:944
#55 0x7ff8d027f737 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl base::win::ObjectWatcher::*const &)(class base::win::ObjectWatcher::Delegate *), class base::WeakPtr<class base::win::ObjectWatcher> const &, class base::win::ObjectWatcher::Delegate *>, struct base::internal::BindState<1, 1, 0, void (__cdecl base::win::ObjectWatcher::*)(class base::win::ObjectWatcher::Delegate *), class base::WeakPtr<class base::win::ObjectWatcher>, class base::internal::UnretainedWrapper<class base::win::ObjectWatcher::Delegate, struct base::unretained_traits::MayDangleUntriaged, 0>>, (void)>::RunImpl<void (__cdecl base::win::ObjectWatcher::*const &)(class base::win::ObjectWatcher::Delegate *), class std::__Cr::tuple<class base::WeakPtr<class base::win::ObjectWatcher>, class base::internal::UnretainedWrapper<class base::win::ObjectWatcher::Delegate, struct base::unretained_traits::MayDangleUntriaged, 0>> const &, 0, 1>(void (__cdecl base::win::ObjectWatcher::*const &)(class base::win::ObjectWatcher::Delegate *), class std::__Cr::tuple<class base::WeakPtr<class base::win::ObjectWatcher>, class base::internal::UnretainedWrapper<class base::win::ObjectWatcher::Delegate, struct base::unretained_traits::MayDangleUntriaged, 0>> const &, struct std::__Cr::integer_sequence<unsigned __int64, 0, 1>) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1057:14
#56 0x7ff8d0363e9c in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
#57 0x7ff8d0363e9c in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:209:34
#58 0x7ff8d5026004 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:106
#59 0x7ff8d5026004 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:456:23
#60 0x7ff8d5024e7f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330:40
#61 0x7ff8d02ad5ae in base::MessagePumpForIO::DoRunLoop(void) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:838:67
#62 0x7ff8d02a6a18 in base::MessagePumpWin::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:88:3
#63 0x7ff8d5027cf2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:629:12
#64 0x7ff8d03c267e in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
#65 0x7ff8d032552d in base::Thread::Run(class base::RunLoop *) C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:344:13
#66 0x7ff8d394c2c7 in content::`anonymous namespace'::ChildIOThread::Run C:\b\s\w\ir\cache\builder\src\content\child\child_process.cc:60:19
#67 0x7ff8d0325a42 in base::Thread::ThreadMain(void) C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:416:3
#68 0x7ff8d028c00e in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:114:13
#69 0x7ff9272c9e8d  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x180059e8d)
#70 0x7ff999dbe8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
#71 0x7ff99afd50ab  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800b50ab)

0x116bfbbf4790 is located 784 bytes inside of 856-byte region [0x116bfbbf4480,0x116bfbbf47d8)
freed by thread T6 here:
#0 0x7ff9272cae5d  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x18005ae5d)
#1 0x7ff8d9f6ca02 in std::__Cr::default_delete<net::HttpStreamPool::Group>::operator() C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:76
#2 0x7ff8d9f6ca02 in std::__Cr::unique_ptr<net::HttpStreamPool::Group,std::__Cr::default_delete<net::HttpStreamPool::Group> >::reset C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:287
#3 0x7ff8d9f6ca02 in std::__Cr::unique_ptr<net::HttpStreamPool::Group,std::__Cr::default_delete<net::HttpStreamPool::Group> >::~unique_ptr C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:256
#4 0x7ff8d9f6ca02 in std::__Cr::pair<const net::HttpStreamKey,std::__Cr::unique_ptr<net::HttpStreamPool::Group,std::__Cr::default_delete<net::HttpStreamPool::Group> > >::~pair C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__utility\pair.h:63
#5 0x7ff8d9f6ca02 in std::__Cr::__destroy_at C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\construct_at.h:63
#6 0x7ff8d9f6ca02 in std::__Cr::allocator_traits<std::__Cr::allocator<std::__Cr::__tree_node<std::__Cr::__value_type<net::HttpStreamKey,std::__Cr::unique_ptr<net::HttpStreamPool::Group,std::__Cr::default_delete<net::HttpStreamPool::Group> > >,void *> > >::destroy C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\allocator_traits.h:329
#7 0x7ff8d9f6ca02 in std::__Cr::__tree<std::__Cr::__value_type<net::HttpStreamKey,std::__Cr::unique_ptr<net::HttpStreamPool::Group,std::__Cr::default_delete<net::HttpStreamPool::Group> > >,std::__Cr::__map_value_compare<net::HttpStreamKey,std::__Cr::__value_type<net::HttpStreamKey,std::__Cr::unique_ptr<net::HttpStreamPool::Group,std::__Cr::default_delete<net::HttpStreamPool::Group> > >,std::__Cr::less<net::HttpStreamKey>,1>,std::__Cr::allocator<std::__Cr::__value_type<net::HttpStreamKey,std::__Cr::unique_ptr<net::HttpStreamPool::Group,std::__Cr::default_delete<net::HttpStreamPool::Group> > > > >::erase C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__tree:2050
#8 0x7ff8d9f6ca02 in std::__Cr::map<net::HttpStreamKey,std::__Cr::unique_ptr<net::HttpStreamPool::Group,std::__Cr::default_delete<net::HttpStreamPool::Group> >,std::__Cr::less<net::HttpStreamKey>,std::__Cr::allocator<std::__Cr::pair<const net::HttpStreamKey,std::__Cr::unique_ptr<net::HttpStreamPool::Group,std::__Cr::default_delete<net::HttpStreamPool::Group> > > > >::erase C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\map:1319
#9 0x7ff8d9f6ca02 in net::HttpStreamPool::OnGroupComplete(class net::HttpStreamPool::Group *) C:\b\s\w\ir\cache\builder\src\net\http\http_stream_pool.cc:296:11
#10 0x7ff8deba1cba in net::HttpStreamPool::Group::MaybeComplete C:\b\s\w\ir\cache\builder\src\net\http\http_stream_pool_group.cc:513
#11 0x7ff8deba1cba in net::HttpStreamPool::Group::AddIdleStreamSocket(class std::__Cr::unique_ptr<class net::StreamSocket, struct std::__Cr::default_delete<class net::StreamSocket>>) C:\b\s\w\ir\cache\builder\src\net\http\http_stream_pool_group.cc:225:3
#12 0x7ff8deba105e in net::HttpStreamPool::Group::ReleaseStreamSocket(class std::__Cr::unique_ptr<class net::StreamSocket, struct std::__Cr::default_delete<class net::StreamSocket>>, __int64) C:\b\s\w\ir\cache\builder\src\net\http\http_stream_pool_group.cc:206:5
#13 0x7ff8e24b3cc2 in net::HttpStreamPoolHandle::Reset(void) C:\b\s\w\ir\cache\builder\src\net\http\http_stream_pool_handle.cc:35:13
#14 0x7ff8e2720580 in net::HttpNetworkTransaction::DoReadBodyComplete(int) C:\b\s\w\ir\cache\builder\src\net\http\http_network_transaction.cc:1562:14
#15 0x7ff8e271268e in net::HttpNetworkTransaction::DoLoop(int) C:\b\s\w\ir\cache\builder\src\net\http\http_network_transaction.cc:906:14
#16 0x7ff8e27158b7 in net::HttpNetworkTransaction::Read(class net::IOBuffer *, int, class base::OnceCallback<(int)>) C:\b\s\w\ir\cache\builder\src\net\http\http_network_transaction.cc:478:12
#17 0x7ff8df277623 in network::ThrottlingNetworkTransaction::Read(class net::IOBuffer *, int, class base::OnceCallback<(int)>) C:\b\s\w\ir\cache\builder\src\services\network\throttling\throttling_network_transaction.cc:209:34
#18 0x7ff8e2743b5e in net::URLRequestHttpJob::ReadRawData(class net::IOBuffer *, int) C:\b\s\w\ir\cache\builder\src\net\url_request\url_request_http_job.cc:1781:21
#19 0x7ff8d0b65a5d in net::URLRequestJob::ReadRawDataHelper(class net::IOBuffer *, int, class base::OnceCallback<(int)>) C:\b\s\w\ir\cache\builder\src\net\url_request\url_request_job.cc:685:16
#20 0x7ff8d0b66d83 in net::URLRequestJob::URLRequestJobSourceStream::Read(class net::IOBuffer *, int, class base::OnceCallback<(int)>) C:\b\s\w\ir\cache\builder\src\net\url_request\url_request_job.cc:77:18
#21 0x7ff8d0c1dd34 in net::FilterSourceStream::DoReadData C:\b\s\w\ir\cache\builder\src\net\filter\filter_source_stream.cc:135
#22 0x7ff8d0c1dd34 in net::FilterSourceStream::DoLoop(int) C:\b\s\w\ir\cache\builder\src\net\filter\filter_source_stream.cc:111:14
#23 0x7ff8d0c1f1ea in net::FilterSourceStream::OnIOComplete(int) C:\b\s\w\ir\cache\builder\src\net\filter\filter_source_stream.cc:204:12
#24 0x7ff8d0c1f71f in base::internal::DecayedFunctorTraits<void (net::FilterSourceStream::*)(int),net::FilterSourceStream *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:728
#25 0x7ff8d0c1f71f in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (net::FilterSourceStream::*&&)(int),net::FilterSourceStream *>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:920
#26 0x7ff8d0c1f71f in base::internal::Invoker<base::internal::FunctorTraits<void (net::FilterSourceStream::*&&)(int),net::FilterSourceStream *>,base::internal::BindState<1,1,0,void (net::FilterSourceStream::*)(int),base::internal::UnretainedWrapper<net::FilterSourceStream,base::unretained_traits::MayNotDangle,0> >,void (int)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1057
#27 0x7ff8d0c1f71f in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl net::FilterSourceStream::*&&)(int), class net::FilterSourceStream *>, struct base::internal::BindState<1, 1, 0, void (__cdecl net::FilterSourceStream::*)(int), class base::internal::UnretainedWrapper<class net::FilterSourceStream, struct base::unretained_traits::MayNotDangle, 0>>, (int)>::RunOnce(class base::internal::BindStateBase *, int) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970:12
#28 0x7ff8d0b64d2e in base::OnceCallback<void (int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
#29 0x7ff8d0b64d2e in net::URLRequestJob::ReadRawDataComplete(int) C:\b\s\w\ir\cache\builder\src\net\url_request\url_request_job.cc:540:33
#30 0x7ff8e273ee95 in net::URLRequestHttpJob::OnReadCompleted(int) C:\b\s\w\ir\cache\builder\src\net\url_request\url_request_http_job.cc:1356:3
#31 0x7ff8e27468ff in base::internal::DecayedFunctorTraits<void (net::URLRequestHttpJob::*)(int),net::URLRequestHttpJob *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:728
#32 0x7ff8e27468ff in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (net::URLRequestHttpJob::*&&)(int),net::URLRequestHttpJob *>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:920
#33 0x7ff8e27468ff in base::internal::Invoker<base::internal::FunctorTraits<void (net::URLRequestHttpJob::*&&)(int),net::URLRequestHttpJob *>,base::internal::BindState<1,1,0,void (net::URLRequestHttpJob::*)(int),base::internal::UnretainedWrapper<net::URLRequestHttpJob,base::unretained_traits::MayNotDangle,0> >,void (int)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1057
#34 0x7ff8e27468ff in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl net::URLRequestHttpJob::*&&)(int), class net::URLRequestHttpJob *>, struct base::internal::BindState<1, 1, 0, void (__cdecl net::URLRequestHttpJob::*)(int), class base::internal::UnretainedWrapper<class net::URLRequestHttpJob, struct base::unretained_traits::MayNotDangle, 0>>, (int)>::RunOnce(class base::internal::BindStateBase *, int) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970:12
#35 0x7ff8e270fbf3 in base::OnceCallback<void (int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
#36 0x7ff8e270fbf3 in net::HttpNetworkTransaction::DoCallback C:\b\s\w\ir\cache\builder\src\net\http\http_network_transaction.cc:811
#37 0x7ff8e270fbf3 in net::HttpNetworkTransaction::OnIOComplete(int) C:\b\s\w\ir\cache\builder\src\net\http\http_network_transaction.cc:817:5
#38 0x7ff8e2726237 in base::internal::DecayedFunctorTraits<void (net::HttpNetworkTransaction::*)(int),net::HttpNetworkTransaction *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:728
#39 0x7ff8e2726237 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (net::HttpNetworkTransaction::*const &)(int),net::HttpNetworkTransaction *>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:920
#40 0x7ff8e2726237 in base::internal::Invoker<base::internal::FunctorTraits<void (net::HttpNetworkTransaction::*const &)(int),net::HttpNetworkTransaction *>,base::internal::BindState<1,1,0,void (net::HttpNetworkTransaction::*)(int),base::internal::UnretainedWrapper<net::HttpNetworkTransaction,base::unretained_traits::MayNotDangle,0> >,void (int)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1057
#41 0x7ff8e2726237 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl net::HttpNetworkTransaction::*&&)(int), class net::HttpNetworkTransaction *>, struct base::internal::BindState<1, 1, 0, void (__cdecl net::HttpNetworkTransaction::*)(int), class base::internal::UnretainedWrapper<class net::HttpNetworkTransaction, struct base::unretained_traits::MayNotDangle, 0>>, (int)>::RunOnce(class base::internal::BindStateBase *, int) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970:12
#42 0x7ff8e43748ed in base::OnceCallback<void (int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
#43 0x7ff8e43748ed in net::HttpStreamParser::OnIOComplete(int) C:\b\s\w\ir\cache\builder\src\net\http\http_stream_parser.cc:380:26
#44 0x7ff8e4380d94 in base::internal::DecayedFunctorTraits<void (net::HttpStreamParser::*)(int),const base::WeakPtr<net::HttpStreamParser> &>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:728
#45 0x7ff8e4380d94 in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (net::HttpStreamParser::*const &)(int),const base::WeakPtr<net::HttpStreamParser> &>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:944
#46 0x7ff8e4380d94 in base::internal::Invoker<base::internal::FunctorTraits<void (net::HttpStreamParser::*const &)(int),const base::WeakPtr<net::HttpStreamParser> &>,base::internal::BindState<1,1,0,void (net::HttpStreamParser::*)(int),base::WeakPtr<net::HttpStreamParser> >,void (int)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1057
#47 0x7ff8e4380d94 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl net::HttpStreamParser::*&&)(int), class base::WeakPtr<class net::HttpStreamParser> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl net::HttpStreamParser::*)(int), class base::WeakPtr<class net::HttpStreamParser>>, (int)>::RunOnce(class base::internal::BindStateBase *, int) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970:12
#48 0x7ff8d56cad06 in base::OnceCallback<void (int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
#49 0x7ff8d56cad06 in net::TCPClientSocket::DidCompleteReadWrite C:\b\s\w\ir\cache\builder\src\net\socket\tcp_client_socket.cc:535
#50 0x7ff8d56cad06 in net::TCPClientSocket::DidCompleteRead(int) C:\b\s\w\ir\cache\builder\src\net\socket\tcp_client_socket.cc:522:3
#51 0x7ff8d56ce227 in base::internal::DecayedFunctorTraits<void (net::TCPClientSocket::*)(int),net::TCPClientSocket *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:728
#52 0x7ff8d56ce227 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (net::TCPClientSocket::*&&)(int),net::TCPClientSocket *>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:920
#53 0x7ff8d56ce227 in base::internal::Invoker<base::internal::FunctorTraits<void (net::TCPClientSocket::*&&)(int),net::TCPClientSocket *>,base::internal::BindState<1,1,0,void (net::TCPClientSocket::*)(int),base::internal::UnretainedWrapper<net::TCPClientSocket,base::unretained_traits::MayNotDangle,0> >,void (int)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1057
#54 0x7ff8d56ce227 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl net::TCPClientSocket::*&&)(int), class net::TCPClientSocket *>, struct base::internal::BindState<1, 1, 0, void (__cdecl net::TCPClientSocket::*)(int), class base::internal::UnretainedWrapper<class net::TCPClientSocket, struct base::unretained_traits::MayNotDangle, 0>>, (int)>::RunOnce(class base::internal::BindStateBase *, int) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970:12
#55 0x7ff8d56c436e in base::OnceCallback<void (int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
#56 0x7ff8d56c436e in net::TCPSocketDefaultWin::RetryRead(int) C:\b\s\w\ir\cache\builder\src\net\socket\tcp_socket_win.cc:1060:29
#57 0x7ff8d56c81af in base::internal::DecayedFunctorTraits<void (net::TCPSocketDefaultWin::*)(int),net::TCPSocketDefaultWin *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:728
#58 0x7ff8d56c81af in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (net::TCPSocketDefaultWin::*&&)(int),net::TCPSocketDefaultWin *>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:920
#59 0x7ff8d56c81af in base::internal::Invoker<base::internal::FunctorTraits<void (net::TCPSocketDefaultWin::*&&)(int),net::TCPSocketDefaultWin *>,base::internal::BindState<1,1,0,void (net::TCPSocketDefaultWin::*)(int),base::internal::UnretainedWrapper<net::TCPSocketDefaultWin,base::unretained_traits::MayNotDangle,0> >,void (int)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1057
#60 0x7ff8d56c81af in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl net::TCPSocketDefaultWin::*&&)(int), class net::TCPSocketDefaultWin *>, struct base::internal::BindState<1, 1, 0, void (__cdecl net::TCPSocketDefaultWin::*)(int), class base::internal::UnretainedWrapper<class net::TCPSocketDefaultWin, struct base::unretained_traits::MayNotDangle, 0>>, (int)>::RunOnce(class base::internal::BindStateBase *, int) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970:12
#61 0x7ff8d56be20c in base::OnceCallback<void (int)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
#62 0x7ff8d56be20c in net::TCPSocketDefaultWin::DidSignalRead(void) C:\b\s\w\ir\cache\builder\src\net\socket\tcp_socket_win.cc:1161:38
#63 0x7ff8d027f737 in base::internal::DecayedFunctorTraits<void (base::win::ObjectWatcher::*)(base::win::ObjectWatcher::Delegate *),const base::WeakPtr<base::win::ObjectWatcher> &,base::win::ObjectWatcher::Delegate *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:728
#64 0x7ff8d027f737 in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (base::win::ObjectWatcher::*const &)(base::win::ObjectWatcher::Delegate *),const base::WeakPtr<base::win::ObjectWatcher> &,base::win::ObjectWatcher::Delegate *>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:944
#65 0x7ff8d027f737 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl base::win::ObjectWatcher::*const &)(class base::win::ObjectWatcher::Delegate *), class base::WeakPtr<class base::win::ObjectWatcher> const &, class base::win::ObjectWatcher::Delegate *>, struct base::internal::BindState<1, 1, 0, void (__cdecl base::win::ObjectWatcher::*)(class base::win::ObjectWatcher::Delegate *), class base::WeakPtr<class base::win::ObjectWatcher>, class base::internal::UnretainedWrapper<class base::win::ObjectWatcher::Delegate, struct base::unretained_traits::MayDangleUntriaged, 0>>, (void)>::RunImpl<void (__cdecl base::win::ObjectWatcher::*const &)(class base::win::ObjectWatcher::Delegate *), class std::__Cr::tuple<class base::WeakPtr<class base::win::ObjectWatcher>, class base::internal::UnretainedWrapper<class base::win::ObjectWatcher::Delegate, struct base::unretained_traits::MayDangleUntriaged, 0>> const &, 0, 1>(void (__cdecl base::win::ObjectWatcher::*const &)(class base::win::ObjectWatcher::Delegate *), class std::__Cr::tuple<class base::WeakPtr<class base::win::ObjectWatcher>, class base::internal::UnretainedWrapper<class base::win::ObjectWatcher::Delegate, struct base::unretained_traits::MayDangleUntriaged, 0>> const &, struct std::__Cr::integer_sequence<unsigned __int64, 0, 1>) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1057:14

previously allocated by thread T6 here:
#0 0x7ff9272ca63d  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x18005a63d)
#1 0x7ff8d9f6e98d in std::__Cr::make_unique C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:754
#2 0x7ff8d9f6e98d in net::HttpStreamPool::GetOrCreateGroup(class net::HttpStreamKey const &, class std::__Cr::optional<class net::QuicSessionAliasKey>) C:\b\s\w\ir\cache\builder\src\net\http\http_stream_pool.cc:458:9
#3 0x7ff8debac50b in net::HttpStreamPool::JobController::RequestStream(class net::HttpStreamRequest::Delegate *, class net::NetLogWithSource const &) C:\b\s\w\ir\cache\builder\src\net\http\http_stream_pool_job_controller.cc:223:26
#4 0x7ff8d9f69483 in net::HttpStreamPool::RequestStream(class net::HttpStreamRequest::Delegate *, struct net::HttpStreamPoolRequestInfo, enum net::RequestPriority, class std::__Cr::vector<struct net::SSLConfig::CertAndStatus, class std::__Cr::allocator<struct net::SSLConfig::CertAndStatus>> const &, bool, bool, class net::NetLogWithSource const &) C:\b\s\w\ir\cache\builder\src\net\http\http_stream_pool.cc:199:30
#5 0x7ff8e27195e3 in net::HttpNetworkTransaction::OnSwitchesToHttpStreamPool(struct net::HttpStreamPoolRequestInfo) C:\b\s\w\ir\cache\builder\src\net\http\http_network_transaction.cc:779:51
#6 0x7ff8deb738e9 in net::HttpStreamFactory::JobController::CallOnSwitchesToHttpStreamPool(struct net::HttpStreamPoolRequestInfo) C:\b\s\w\ir\cache\builder\src\net\http\http_stream_factory_job_controller.cc:1540:14
#7 0x7ff8deb7485a in base::internal::DecayedFunctorTraits<void (net::HttpStreamFactory::JobController::*)(net::HttpStreamPoolRequestInfo),base::WeakPtr<net::HttpStreamFactory::JobController> &&,net::HttpStreamPoolRequestInfo &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:728
#8 0x7ff8deb7485a in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (net::HttpStreamFactory::JobController::*&&)(net::HttpStreamPoolRequestInfo),base::WeakPtr<net::HttpStreamFactory::JobController> &&,net::HttpStreamPoolRequestInfo &&>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:944
#9 0x7ff8deb7485a in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl net::HttpStreamFactory::JobController::*&&)(struct net::HttpStreamPoolRequestInfo), class base::WeakPtr<class net::HttpStreamFactory::JobController> &&, struct net::HttpStreamPoolRequestInfo &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl net::HttpStreamFactory::JobController::*)(struct net::HttpStreamPoolRequestInfo), class base::WeakPtr<class net::HttpStreamFactory::JobController>, struct net::HttpStreamPoolRequestInfo>, (void)>::RunImpl<void (__cdecl net::HttpStreamFactory::JobController::*)(struct net::HttpStreamPoolRequestInfo), class std::__Cr::tuple<class base::WeakPtr<class net::HttpStreamFactory::JobController>, struct net::HttpStreamPoolRequestInfo>, 0, 1>(void (__cdecl net::HttpStreamFactory::JobController::*&&)(struct net::HttpStreamPoolRequestInfo), class std::__Cr::tuple<class base::WeakPtr<class net::HttpStreamFactory::JobController>, struct net::HttpStreamPoolRequestInfo> &&, struct std::__Cr::integer_sequence<unsigned __int64, 0, 1>) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1057:14
#10 0x7ff8d0363e9c in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
#11 0x7ff8d0363e9c in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:209:34
#12 0x7ff8d5026004 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:106
#13 0x7ff8d5026004 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:456:23
#14 0x7ff8d5024e7f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330:40
#15 0x7ff8d02ad5ae in base::MessagePumpForIO::DoRunLoop(void) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:838:67
#16 0x7ff8d02a6a18 in base::MessagePumpWin::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:88:3
#17 0x7ff8d5027cf2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:629:12
#18 0x7ff8d03c267e in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
#19 0x7ff8d032552d in base::Thread::Run(class base::RunLoop *) C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:344:13
#20 0x7ff8d394c2c7 in content::`anonymous namespace'::ChildIOThread::Run C:\b\s\w\ir\cache\builder\src\content\child\child_process.cc:60:19
#21 0x7ff8d0325a42 in base::Thread::ThreadMain(void) C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:416:3
#22 0x7ff8d028c00e in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:114:13
#23 0x7ff9272c9e8d  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x180059e8d)
#24 0x7ff999dbe8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
#25 0x7ff99afd50ab  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800b50ab)

Thread T6 created by T0 here:
#0 0x7ff9272c9da2  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x180059da2)
#1 0x7ff8d028b0d9 in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:182:7
#2 0x7ff8d03246e8 in base::Thread::StartWithOptions(struct base::Thread::Options) C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:211:26
#3 0x7ff8d394b3d4 in content::ChildProcess::ChildProcess(enum base::ThreadType, class std::__Cr::unique_ptr<struct base::ThreadPoolInstance::InitParams, struct std::__Cr::default_delete<struct base::ThreadPoolInstance::InitParams>>) C:\b\s\w\ir\cache\builder\src\content\child\child_process.cc:125:3
#4 0x7ff8cccf137e in content::UtilityMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\utility\utility_main.cc:381:16
#5 0x7ff8ce10c411 in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:779:14
#6 0x7ff8ce10e650 in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1153:10
#7 0x7ff8ce102955 in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:359:36
#8 0x7ff8ce1034fd in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:372:10
#9 0x7ff8bf0e16b4 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:222:12
#10 0x7ff6b2a645ed in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201:12
#11 0x7ff6b2a61fe4 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:352:20
#12 0x7ff6b30cb9fb in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
#13 0x7ff6b30cb9fb in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
#14 0x7ff999dbe8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
#15 0x7ff99afd50ab  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800b50ab)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:274 in std::__Cr::unique_ptr<net::HttpStreamPool::AttemptManager,std::__Cr::default_delete<net::HttpStreamPool::AttemptManager> >::operator bool
Shadow bytes around the buggy address:
0x116bfbbf4500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x116bfbbf4580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x116bfbbf4600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x116bfbbf4680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x116bfbbf4700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x116bfbbf4780: fd fd[fd]fd fd fd fd fd fd fd fd fa fa fa fa fa
0x116bfbbf4800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
0x116bfbbf4880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0x116bfbbf4900: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0x116bfbbf4980: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
0x116bfbbf4a00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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

==12236==ADDITIONAL INFO

==12236==Note: Please include this section with the ASan report.
Task trace:
#0 0x7ff8d56c4944 in net::TCPSocketDefaultWin::CoreImpl::WatchForRead C:\b\s\w\ir\cache\builder\src\net\socket\tcp_socket_win.cc:267


Command line: `"C:\chromium_version\latest_asan\chrome.exe" --type=utility --utility-sub-type=network.mojom.NetworkService --lang=zh-CN --service-sandbox-type=network --no-sandbox --enable-experimental-cookie-features --ignore-certificate-errors --enable-experimental-web-platform-features --ignore-certificate-errors --user-data-dir=C:/tmp/eiraxyqjtz --enable-experimental-extension-apis --extensions-on-chrome-urls --no-pre-read-main-dll --start-stack-profiler --metrics-shmem-handle=2104,i,17775151019830412106,15851300548300632526,524288 --field-trial-handle=1856,i,11329661967444346544,4001149037106662852,262144 --enable-features=BlockInsecurePrivateNetworkRequests,BlockInsecurePrivateNetworkRequestsFromPrivate,BlockInsecurePrivateNetworkRequestsFromUnknown,CookieSameSiteConsidersRedirectChain,CreateImageBitmapOrientationNone,CriticalClientHint,DisallowNonAsciiCookies,DocumentPictureInPictureAPI,DocumentPolicyIncludeJSCallStacksInCrashReports,DocumentPolicyNegotiation,EnableCanvas2DLayers,EnablePortBoundCookies,EnableSchemeBoundCookies,ExperimentalContentSecurityPolicyFeatures,FencedFrames,FencedFramesDefaultMode,FencedFramesDeveloperMode,OriginIsolationHeader,PartitionedPopins,Permissions,PrivateNetworkAccessRespectPreflightResults,SameSiteDefaultChecksMethodRigorously,SchemefulSameSite,StorageAccessHeaders,ThirdPartyStoragePartitioning --variations-seed-version --mojo-platform-channel-handle=2092 /prefetch:11`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==12236==END OF ADDITIONAL INFO
==12236==ABORTING
[27472:28756:0301/050144.727:ERROR:network_service_instance_impl.cc(612)] Network service crashed, restarting service.
```

## Attachments

- [manifest.json](attachments/manifest.json) (application/json, 252 B)
- [background.js](attachments/background.js) (text/javascript, 138 B)
- [popup.html](attachments/popup.html) (text/html, 268 B)

## Timeline

### es...@chromium.org (2025-03-03)

Thanks for the report. Are you able to provide any additional information about how to reproduce, such as a proof-of-concept even if it doesn't reproduce the crash reliably?

### pg...@google.com (2025-03-06)

@reporter, please provide a POC (even if not reliably crashing) when available.

ricea@ can you take a look? hoping the stacktrace is insightful enough to make this actionable!

Setting S1 - UAF in browser, but requiring an extension potentially?  

Setting FoundIn to be 134 to be conservative - please update to M135 or later if need be!

### ba...@chromium.org (2025-03-06)

I have no idea why UAF happens in HttpStreamPool::Group::ProcessPendingRequest(). Group owns `attempt_manager_` and the method checks `attempt_manager_` at the beginning.

### 0x...@gmail.com (2025-03-06)

I catch the crash when run the extension however I didn't fetch the urls in the iframe.src .  The extension popup page has a special lifecycle maybe cause this UAF.

### pe...@google.com (2025-03-06)

Thank you for providing more feedback. Adding the requester to the CC list.

### ba...@chromium.org (2025-03-06)

Can you also provide server implementation?

### 0x...@gmail.com (2025-03-06)

I use python aiohttp as the static https webserver with self-signed certicicate.

��ȡ Outlook for iOS<https://aka.ms/o0ukef>
________________________________
������: buganizer-system@google.com <buganizer-system@google.com>
����ʱ��: Thursday, March 6, 2025 10:48:10 AM
�ռ���: b-system+664851229@google.com <b-system+664851229@google.com>
����: 0xasnine@gmail.com <0xasnine@gmail.com>
����: Re: Issue 399995424: UAF in net::HttpStreamPool::Group::ProcessPendingRequest

Replying to this email means your email address will be shared with the team that works on this product.
https://issues.chromium.org/issues/399995424

Changed

ba...@chromium.org added comment #7<https://issues.chromium.org/issues/399995424#comment7>:

Can you also provide server implementation?

_______________________________

Reference Info: 399995424 UAF in net::HttpStreamPool::Group::ProcessPendingRequest
component:  Public Trackers > 1362134 > Chromium > Internals > Network<https://issues.chromium.org/components/1456527>
status:  Assigned
reporter:  0xasnine@gmail.com
assignee:  ba...@chromium.org
cc:  0xasnine@gmail.com, ba...@chromium.org, es...@chromium.org, and 4 more
collaborators:  se...@chromium.org
type:  Vulnerability
access level:  Limited visibility
priority:  P4
severity:  S1
found in:  134
hotlist:  external_security_report<https://issues.chromium.org/hotlists/5433527>, Needs-Feedback<https://issues.chromium.org/hotlists/5433459>, Security_Impact-Extended<https://issues.chromium.org/hotlists/5432548>, Unconfirmed<https://issues.chromium.org/hotlists/5437934>
retention:  Component default
Component Ancestor Tags:  Internals, Internals>Network
Component Tags:  Internals>Network
OS:  Android, Fuchsia, Linux, Mac, Windows, Lacros, ChromeOS


Generated by Google IssueTracker notification system.

You're receiving this email because you are subscribed to updates on Google IssueTracker issue 399995424<https://issues.chromium.org/issues/399995424> where you have the roles: cc, reporter
Unsubscribe from this issue.<https://issues.chromium.org/issues/399995424?unsubscribe=true>


### pe...@google.com (2025-03-06)

Thank you for providing more feedback. Adding the requester to the CC list.

### ba...@chromium.org (2025-03-06)

I was able to write a unittest to reproduce the UAF. Here is a crash log (Googler only): <https://paste.googleplex.com/4560260441047040>.

HttpStreamPool::Group destroyed itself in AddIdleStreamSocket(), but the group accessed itself immediately after AddIdleStreamSocket() deleted itself in ProcessPendingRequest(). To fix the UAF, we can just remove MaybeComplete() call from AddIdleStreamSocket(). CL is up: <https://chromium-review.googlesource.com/c/chromium/src/+/6332871>

### ap...@google.com (2025-03-06)

Project: chromium/src  

Branch: main  

Author: Kenichi Ishibashi <[bashi@chromium.org](mailto:bashi@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6332871>

HttpStreamPool: Remove redundant Group::MaybeComplete() call

---


Expand for full commit details
```
HttpStreamPool: Remove redundant Group::MaybeComplete() call 
 
This CL removes redundant MaybeComplete() call from 
Group::AddIdleStreamSocket(). It was introduced in crrev.com/c/5699606 
but we landed crrev.com/c/6170548 later and the method call became 
redundant. The MaybeComplete() call in AddIdleStreamSocket() could 
cause accessing deleted Group in ProcessPendingRequest() if the call 
actually destroys the Group. 
 
Bug: 399995424 
Change-Id: Id0cfd90570a67c4858c5a872f6e342522b959226 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6332871 
Reviewed-by: Nidhi Jaju <nidhijaju@chromium.org> 
Commit-Queue: Kenichi Ishibashi <bashi@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1428775}

```

---

Files:

- M `net/http/http_stream_pool_group.cc`
- M `net/http/http_stream_pool_group_unittest.cc`
- M `net/http/http_stream_pool_test_util.cc`
- M `net/http/http_stream_pool_test_util.h`

---

Hash: 9941bdc1347bc97cf2b16477661cf258a130c02a  

Date:  Thu Mar 06 00:36:55 2025


---

### ch...@google.com (2025-03-06)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-03-06)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### me...@google.com (2025-03-14)

[secondary security shepherd] bashi: Thanks for the fix! Can we mark the bug as fixed or is there followup work that needs to be done?

### ba...@chromium.org (2025-03-15)

I think we can mark this as fixed.

### ch...@google.com (2025-03-15)

Security Merge Request Consideration: Requesting merge to stable (M134) because latest trunk commit (1428775) appears to be after stable branch point (1415337).
Security Merge Request Consideration: Requesting merge to beta (M135) because latest trunk commit (1428775) appears to be after beta branch point (1427262).
Security Merge Request - Manual Review: Merge review required: M134 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M135 is already shipping to beta.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [134, 135].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ba...@chromium.org (2025-03-16)

The issue only happen when the HappyEyeballsV3 feature is enabled. The flag is disabled by default and we don't run experiments on Stable. Should we merge the fix?

### pg...@google.com (2025-03-16)

Thanks for the info! In that case, no - this does not need backmerging.

Updating Security\_Impact to None per [comment #17](https://issues.chromium.org/issues/399995424#comment17) and removing merge labels

### sp...@google.com (2025-03-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
report of memory corruption in a highly-privileged process (network stack) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-21)

Congratulations asnine! Thank you for your efforts and reporting this issue to us -- very nice work!

### ch...@google.com (2025-06-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of memory corruption in a highly-privileged process (network stack)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/399995424)*

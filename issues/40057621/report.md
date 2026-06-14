# Heap-use-after-free in SpeechRecognitionManagerImpl::DispatchEvent

| Field | Value |
|-------|-------|
| **Issue ID** | [40057621](https://issues.chromium.org/issues/40057621) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | ch...@gmail.com |
| **Assignee** | pr...@chromium.org |
| **Created** | 2012-05-03 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Chrome browser crashes with a use after free bug, when speech input is used.

**VERSION**  

Chrome Version: [20.0.1125.0 (135008)] + [ dev]  

Operating System: [Ubuntu, 11.04, 64 bit]

**REPRODUCTION CASE**

1. Download and copy test2.html to a folder.
2. Open test2.html on chrome web browser.
3. Click on microphone icon on speech input element.
4. Click somewhere else on web page.
5. Browser will crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]  

Asan output indicates two errors. I could not figure out which error causes browser crash.  

Crash State: [Asan output]

==5652== ERROR: AddressSanitizer heap-use-after-free on address 0x7f53c68944e0 at pc 0x7f53fc65c942 bp 0x7f53e16c4d50 sp 0x7f53e16c4d48  

WRITE of size 4 at 0x7f53c68944e0 thread T11  

#0 0x7f53fc65c942 in \_ZN6speech28SpeechRecognitionManagerImpl13DispatchEventEiNS0\_12FSMEventArgsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/speech/speech\_recognition\_manager\_impl.cc:339  

#1 0x7f53fc66431c in \_ZN4base8internal7InvokerILi3ENS0\_9BindStateINS0\_15RunnableAdapterIMN6speech28SpeechRecognitionManagerImplEFviNS5\_12FSMEventArgsEEEEFvPS5\_iS6\_EFvNS0\_17UnretainedWrapperIS5\_EEiS6\_EEESB\_E3RunEPNS0\_13BindStateBaseE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./base/bind\_internal.h:1384  

#2 0x7f53f76f7465 in \_ZNK4base8CallbackIFvvEE3RunEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./base/callback.h:272  

#3 0x7f53f76f7bae in \_ZN11MessageLoop21DeferOrRunPendingTaskERKN4base11PendingTaskE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:470  

#4 0x7f53f76f9120 in \_ZN11MessageLoop6DoWorkEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:647  

#5 0x7f53f768b6d3 in \_ZN4base19MessagePumpLibevent3RunEPNS\_11MessagePump8DelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_pump\_libevent.cc:241  

#6 0x7f53f76f6082 in \_ZN11MessageLoop11RunInternalEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:418  

#7 0x7f53f76f426e in ~AutoRunState /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:732  

#8 0x7f53f7772f94 in \_ZN4base6Thread10ThreadMainEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/thread.cc:163  

#9 0x7f53f7767cdc in \_ZN4base12\_GLOBAL\_\_N\_110ThreadFuncEPv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/platform\_thread\_posix.cc:65  

#10 0x7f53fe2343ac in \_ZN6\_\_asan10AsanThread11ThreadStartEv ??:0  

0x7f53c68944e0 is located 96 bytes inside of 104-byte region [0x7f53c6894480,0x7f53c68944e8)  

freed by thread T11 here:  

#0 0x7f53fe237b22 in \_ZdlPv ??:0  

#1 0x7f53fc664091 in \_ZN9\_\_gnu\_cxx13new\_allocatorISt13\_Rb\_tree\_nodeISt4pairIKiN6speech28SpeechRecognitionManagerImpl7SessionEEEE10deallocateEPS8\_m /usr/lib/x86\_64-linux-gnu/gcc/x86\_64-linux-gnu/4.5/../../../../../include/c++/4.5/ext/new\_allocator.h:95  

#2 0x7f53fc663df9 in \_ZNSt8\_Rb\_treeIiSt4pairIKiN6speech28SpeechRecognitionManagerImpl7SessionEESt10\_Select1stIS5\_ESt4lessIiESaIS5\_EE5clearEv /usr/lib/x86\_64-linux-gnu/gcc/x86\_64-linux-gnu/4.5/../../../../../include/c++/4.5/bits/stl\_tree.h:744  

#3 0x7f53fc663bd9 in \_ZNKSt8\_Rb\_treeIiSt4pairIKiN6speech28SpeechRecognitionManagerImpl7SessionEESt10\_Select1stIS5\_ESt4lessIiESaIS5\_EE4sizeEv /usr/lib/x86\_64-linux-gnu/gcc/x86\_64-linux-gnu/4.5/../../../../../include/c++/4.5/bits/stl\_tree.h:671  

#4 0x7f53fc662280 in \_ZN6speech28SpeechRecognitionManagerImpl13SessionDeleteERNS0\_7SessionERKNS0\_12FSMEventArgsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/speech/speech\_recognition\_manager\_impl.cc:542  

#5 0x7f53fc66084f in \_ZN6speech28SpeechRecognitionManagerImpl12SessionAbortERNS0\_7SessionERKNS0\_12FSMEventArgsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/speech/speech\_recognition\_manager\_impl.cc:465  

#6 0x7f53fc65c771 in \_ZN6speech28SpeechRecognitionManagerImpl13DispatchEventEiNS0\_12FSMEventArgsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/speech/speech\_recognition\_manager\_impl.cc:339  

#7 0x7f53fc66431c in \_ZN4base8internal7InvokerILi3ENS0\_9BindStateINS0\_15RunnableAdapterIMN6speech28SpeechRecognitionManagerImplEFviNS5\_12FSMEventArgsEEEEFvPS5\_iS6\_EFvNS0\_17UnretainedWrapperIS5\_EEiS6\_EEESB\_E3RunEPNS0\_13BindStateBaseE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./base/bind\_internal.h:1384  

#8 0x7f53f76f7465 in \_ZNK4base8CallbackIFvvEE3RunEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./base/callback.h:272  

#9 0x7f53f76f7bae in \_ZN11MessageLoop21DeferOrRunPendingTaskERKN4base11PendingTaskE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:470  

#10 0x7f53f76f9120 in \_ZN11MessageLoop6DoWorkEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:647  

#11 0x7f53f768b6d3 in \_ZN4base19MessagePumpLibevent3RunEPNS\_11MessagePump8DelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_pump\_libevent.cc:241  

#12 0x7f53f76f6082 in \_ZN11MessageLoop11RunInternalEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:418  

#13 0x7f53f76f426e in ~AutoRunState /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:732  

#14 0x7f53f7772f94 in \_ZN4base6Thread10ThreadMainEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/thread.cc:163  

#15 0x7f53f7767cdc in \_ZN4base12\_GLOBAL\_\_N\_110ThreadFuncEPv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/platform\_thread\_posix.cc:65  

#16 0x7f53fe2343ac in \_ZN6\_\_asan10AsanThread11ThreadStartEv ??:0  

previously allocated by thread T11 here:  

#0 0x7f53fe2379a2 in \_Znwm ??:0  

#1 0x7f53fc6648c0 in \_ZN9\_\_gnu\_cxx13new\_allocatorISt13\_Rb\_tree\_nodeISt4pairIKiN6speech28SpeechRecognitionManagerImpl7SessionEEEE8allocateEmPKv /usr/lib/x86\_64-linux-gnu/gcc/x86\_64-linux-gnu/4.5/../../../../../include/c++/4.5/ext/new\_allocator.h:89  

#2 0x7f53fc664da1 in *ZNSt8\_Rb\_treeIiSt4pairIKiN6speech28SpeechRecognitionManagerImpl7SessionEESt10\_Select1stIS5\_ESt4lessIiESaIS5\_EE16\_M\_insert\_uniqueERKS5* /usr/lib/x86\_64-linux-gnu/gcc/x86\_64-linux-gnu/4.5/../../../../../include/c++/4.5/bits/stl\_tree.h:1196  

#3 0x7f53fc6647b8 in *ZNSt8\_Rb\_treeIiSt4pairIKiN6speech28SpeechRecognitionManagerImpl7SessionEESt10\_Select1stIS5\_ESt4lessIiESaIS5\_EE17\_M\_insert\_unique\_ESt23\_Rb\_tree\_const\_iteratorIS5\_ERKS5* /usr/lib/x86\_64-linux-gnu/gcc/x86\_64-linux-gnu/4.5/../../../../../include/c++/4.5/bits/stl\_tree.h:1268  

#4 0x7f53fc65b49f in Session /usr/lib/x86\_64-linux-gnu/gcc/x86\_64-linux-gnu/4.5/../../../../../include/c++/4.5/bits/stl\_map.h:541  

#5 0x7f53fc65a700 in \_ZN6speech28SpeechRecognitionManagerImpl13CreateSessionERKN7content30SpeechRecognitionSessionConfigEPNS1\_30SpeechRecognitionEventListenerE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/speech/speech\_recognition\_manager\_impl.cc:69  

#6 0x7f53fc6587ad in \_ZN6speech28InputTagSpeechDispatcherHost18OnStartRecognitionERK45InputTagSpeechHostMsg\_StartRecognition\_Params /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/speech/input\_tag\_speech\_dispatcher\_host.cc:109  

#7 0x7f53fc65818e in \_Z16DispatchToMethodIN6speech28InputTagSpeechDispatcherHostEMS1\_FvRK45InputTagSpeechHostMsg\_StartRecognition\_ParamsES2\_EvPT\_T0\_RK6Tuple1IT1\_E /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./base/tuple.h:547  

#8 0x7f53fc46460f in \_ZN7content20BrowserMessageFilter15DispatchMessageERKN3IPC7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/public/browser/browser\_message\_filter.cc:106  

#9 0x7f53fc464459 in \_ZN7content20BrowserMessageFilter17OnMessageReceivedERKN3IPC7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/public/browser/browser\_message\_filter.cc:102  

#10 0x7f53f780ecd0 in \_ZN3IPC12ChannelProxy7Context10TryFiltersERKNS\_7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/ipc\_channel\_proxy.cc:70  

#11 0x7f53f7814bf3 in \_ZN3IPC8internal13ChannelReader17DispatchInputDataEPKci /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/ipc\_channel\_reader.cc:76  

#12 0x7f53f7814832 in \_ZN3IPC8internal13ChannelReader23ProcessIncomingMessagesEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/ipc\_channel\_reader.cc:29  

#13 0x7f53f78096d8 in \_ZN3IPC7Channel11ChannelImpl28OnFileCanReadWithoutBlockingEi /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/ipc\_channel\_posix.cc:795  

#14 0x7f53f768b048 in *ZN4base19MessagePumpLibevent21FileDescriptorWatcher28OnFileCanReadWithoutBlockingEiPS0* /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_pump\_libevent.cc:109  

#15 0x7f53f77c9f75 in event\_process\_active /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third\_party/libevent/event.c:386  

#16 0x7f53f768b9de in \_ZN4base19MessagePumpLibevent3RunEPNS\_11MessagePump8DelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_pump\_libevent.cc:279  

#17 0x7f53f76f6082 in \_ZN11MessageLoop11RunInternalEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:418  

#18 0x7f53f76f426e in ~AutoRunState /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:732  

#19 0x7f53f7772f94 in \_ZN4base6Thread10ThreadMainEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/thread.cc:163  

#20 0x7f53f7767cdc in \_ZN4base12\_GLOBAL\_\_N\_110ThreadFuncEPv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/platform\_thread\_posix.cc:65  

#21 0x7f53fe2343ac in \_ZN6\_\_asan10AsanThread11ThreadStartEv ??:0  

Thread T11 created by T0 here:  

#0 0x7f53fe22cb35 in pthread\_create ??:0  

#1 0x7f53f776789c in \_ZN4base12\_GLOBAL\_\_N\_112CreateThreadEmbPNS\_14PlatformThread8DelegateEPmNS\_14ThreadPriorityE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/platform\_thread\_posix.cc:127  

#2 0x7f53f776777d in \_ZN4base14PlatformThread6CreateEmPNS0\_8DelegateEPm /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/platform\_thread\_posix.cc:249  

#3 0x7f53f7772854 in \_ZN4base6Thread16StartWithOptionsERKNS0\_7OptionsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/thread.cc:73  

#4 0x7f53fc47594b in \_ZN7content15BrowserMainLoop13CreateThreadsEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/browser\_main\_loop.cc:411  

#5 0x7f53fc477fe7 in \_ZN12\_GLOBAL\_\_N\_121BrowserMainRunnerImpl10InitializeERKN7content18MainFunctionParamsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/browser\_main\_runner.cc:85  

#6 0x7f53fc472a5b in \_Z11BrowserMainRKN7content18MainFunctionParamsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/browser\_main.cc:17  

#7 0x7f53f75addc7 in \_ZN12\_GLOBAL\_\_N\_123RunNamedProcessTypeMainERKSsRKN7content18MainFunctionParamsEPNS2\_19ContentMainDelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main\_runner.cc:290  

#8 0x7f53f75ac145 in \_ZN7content11ContentMainEiPPKcPNS\_19ContentMainDelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main.cc:35  

#9 0x7f53f60b3637 in ChromeMain /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_main.cc:32  

#10 0x7f53f60b359b in main /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#11 0x7f53ef418eff in \_\_libc\_start\_main /build/buildd/eglibc-2.13/csu/libc-start.c:258  

==5652== ABORTING  

Stats: 126M malloced (168M for red zones) by 523581 calls  

Stats: 4M realloced by 16127 calls  

Stats: 92M freed by 439338 calls  

Stats: 0M really freed by 0 calls  

Stats: 324M (82974 full pages) mmaped in 78 calls  

mmaps by size class: 8:425958; 9:73719; 10:40950; 11:6141; 12:3072; 13:4608; 14:512; 15:128; 16:256; 17:32; 18:16; 19:8; 20:4; 21:2; 22:5; 24:1;  

mallocs by size class: 8:414501; 9:61935; 10:34565; 11:5031; 12:2399; 13:4298; 14:470; 15:86; 16:238; 17:28; 18:13; 19:6; 20:3; 21:2; 22:5; 24:1;  

frees by size class: 8:341191; 9:57607; 10:33591; 11:3692; 12:1874; 13:684; 14:404; 15:52; 16:207; 17:14; 18:9; 19:6; 20:2; 21:2; 22:2; 24:1;  

rfrees by size class:  

Stats: malloc large: 58 small slow: 2040  

Shadow byte and word:  

0x1fea78d1289c: fd  

0x1fea78d12898: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1fea78d12878: fb fb fb fb fb fb fb fb  

0x1fea78d12880: fa fa fa fa fa fa fa fa  

0x1fea78d12888: fa fa fa fa fa fa fa fa  

0x1fea78d12890: fd fd fd fd fd fd fd fd  

=>0x1fea78d12898: fd fd fd fd fd fd fd fd  

0x1fea78d128a0: fa fa fa fa fa fa fa fa  

0x1fea78d128a8: fa fa fa fa fa fa fa fa  

0x1fea78d128b0: 00 00 00 00 00 00 00 00  

0x1fea78d128b8: fb fb fb fb fb fb fb fb  

ASAN:SIGSEGV  

==5689== ERROR: AddressSanitizer crashed on unknown address 0xffffffffa148a9e8 (pc 0x7fccad156978 sp 0x7fff0e9d7950 bp 0x7fcca19418b2 T0)  

AddressSanitizer can not provide additional info. ABORTING  

#0 0x7fccad156978 in XQueryExtension /build/buildd/libx11-1.4.2/build/src/../../src/QuExt.c:39  

Stats: 46M malloced (39M for red zones) by 59836 calls  

Stats: 0M realloced by 256 calls  

Stats: 44M freed by 58247 calls  

Stats: 0M really freed by 0 calls  

Stats: 112M (28693 full pages) mmaped in 28 calls  

mmaps by size class: 8:65532; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:1792; 15:128; 16:64; 17:32; 18:16; 19:64;  

mallocs by size class: 8:52857; 9:2701; 10:956; 11:450; 12:597; 13:459; 14:1645; 15:55; 16:24; 17:18; 18:16; 19:58;  

frees by size class: 8:51789; 9:2356; 10:928; 11:418; 12:564; 13:397; 14:1637; 15:49; 16:22; 17:16; 18:15; 19:56;  

rfrees by size class:  

Stats: malloc large: 92 small slow: 417

## Attachments

- [test2.html](attachments/test2.html) (text/html; charset=us-ascii, 91 B)

## Timeline

### ch...@gmail.com (2012-05-03)

I first noticed this bug last friday (27th, April, 2012). I did not report this bug at that time because this is a very obvious error and I thought it happens because of a partial fix. I decided to report it today because this error still exists and I wonder whether it happens only on my PC configuration.

### in...@chromium.org (2012-05-03)

==8395== ERROR: AddressSanitizer heap-use-after-free on address 0x7f5d73799fe0 at pc 0x7f5d9da16712 bp 0x7f5d84272fb0 sp 0x7f5d84272fa8
WRITE of size 4 at 0x7f5d73799fe0 thread T11
    #0 0x7f5d9da16712 in speech::SpeechRecognitionManagerImpl::DispatchEvent(int, speech::SpeechRecognitionManagerImpl::FSMEventArgs) chrome-asan/src/content/browser/speech/speech_recognition_manager_impl.cc:341
    #1 0x7f5d9da1d9df in base::internal::RunnableAdapter<void (speech::SpeechRecognitionManagerImpl::*)(int, speech::SpeechRecognitionManagerImpl::FSMEventArgs)>::Run(speech::SpeechRecognitionManagerImpl*, int const&, speech::SpeechRecognitionManagerImpl::FSMEventArgs const&) chrome-asan/src/./base/bind_internal.h:246
    #2 0x7f5d9da1d7c9 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (speech::SpeechRecognitionManagerImpl::*)(int, speech::SpeechRecognitionManagerImpl::FSMEventArgs)>, void (speech::SpeechRecognitionManagerImpl*, int const&, speech::SpeechRecognitionManagerImpl::FSMEventArgs const&)>::MakeItSo(base::internal::RunnableAdapter<void (speech::SpeechRecognitionManagerImpl::*)(int, speech::SpeechRecognitionManagerImpl::FSMEventArgs)>, speech::SpeechRecognitionManagerImpl*, int const&, speech::SpeechRecognitionManagerImpl::FSMEventArgs const&) chrome-asan/src/./base/bind_internal.h:927
    #3 0x7f5d9da1d648 in base::internal::Invoker<3, base::internal::BindState<base::internal::RunnableAdapter<void (speech::SpeechRecognitionManagerImpl::*)(int, speech::SpeechRecognitionManagerImpl::FSMEventArgs)>, void (speech::SpeechRecognitionManagerImpl*, int, speech::SpeechRecognitionManagerImpl::FSMEventArgs), void (base::internal::UnretainedWrapper<speech::SpeechRecognitionManagerImpl>, int, speech::SpeechRecognitionManagerImpl::FSMEventArgs)>, void (speech::SpeechRecognitionManagerImpl*, int, speech::SpeechRecognitionManagerImpl::FSMEventArgs)>::Run(base::internal::BindStateBase*) chrome-asan/src/./base/bind_internal.h:1384
    #4 0x7f5d9a3024b3 in MessageLoop::RunTask(base::PendingTask const&) chrome-asan/src/base/message_loop.cc:459
    #5 0x7f5d9a302be9 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) chrome-asan/src/base/message_loop.cc:470
    #6 0x7f5d9a302f02 in MessageLoop::DoWork() chrome-asan/src/base/message_loop.cc:647
    #7 0x7f5d9a29f462 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) chrome-asan/src/base/message_pump_libevent.cc:241
    #8 0x7f5d9a301cac in MessageLoop::RunInternal() chrome-asan/src/base/message_loop.cc:418
    #9 0x7f5d9a3009b8 in MessageLoop::Run() chrome-asan/src/base/message_loop.cc:301
    #10 0x7f5d9a376de1 in base::Thread::ThreadMain() chrome-asan/src/base/threading/thread.cc:166
    #11 0x7f5d9a36bd4c in base::(anonymous namespace)::ThreadFunc(void*) chrome-asan/src/base/threading/platform_thread_posix.cc:65
    #12 0x7f5d9f129fdc in __asan::AsanThread::ThreadStart() ??:0
0x7f5d73799fe0 is located 96 bytes inside of 104-byte region [0x7f5d73799f80,0x7f5d73799fe8)
freed by thread T11 here:
    #0 0x7f5d9f12d752 in operator delete(void*) ??:0
    #1 0x7f5d9da1ccd9 in std::_Rb_tree<int, std::pair<int const, speech::SpeechRecognitionManagerImpl::Session>, std::_Select1st<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> >, std::less<int>, std::allocator<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> > >::_M_erase(std::_Rb_tree_node<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> >*) /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl_tree.h:971
    #2 0x7f5d9da1ca9d in std::_Rb_tree<int, std::pair<int const, speech::SpeechRecognitionManagerImpl::Session>, std::_Select1st<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> >, std::less<int>, std::allocator<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> > >::clear() /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl_tree.h:727
    #3 0x7f5d9da1c976 in std::_Rb_tree<int, std::pair<int const, speech::SpeechRecognitionManagerImpl::Session>, std::_Select1st<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> >, std::less<int>, std::allocator<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> > >::erase(std::_Rb_tree_iterator<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> >, std::_Rb_tree_iterator<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> >) /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl_tree.h:1385
    #4 0x7f5d9da1c502 in std::_Rb_tree<int, std::pair<int const, speech::SpeechRecognitionManagerImpl::Session>, std::_Select1st<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> >, std::less<int>, std::allocator<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> > >::erase(int const&) /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl_tree.h:1375
    #5 0x7f5d9da1ab36 in speech::SpeechRecognitionManagerImpl::SessionDelete(speech::SpeechRecognitionManagerImpl::Session&, speech::SpeechRecognitionManagerImpl::FSMEventArgs const&) chrome-asan/src/content/browser/speech/speech_recognition_manager_impl.cc:542
    #6 0x7f5d9da195e0 in speech::SpeechRecognitionManagerImpl::ExecuteTransitionAndGetNextState(speech::SpeechRecognitionManagerImpl::Session&, speech::SpeechRecognitionManagerImpl::FSMEventArgs const&) chrome-asan/src/content/browser/speech/speech_recognition_manager_impl.cc:410
    #7 0x7f5d9da165d6 in speech::SpeechRecognitionManagerImpl::DispatchEvent(int, speech::SpeechRecognitionManagerImpl::FSMEventArgs) chrome-asan/src/content/browser/speech/speech_recognition_manager_impl.cc:339
    #8 0x7f5d9da1d9df in base::internal::RunnableAdapter<void (speech::SpeechRecognitionManagerImpl::*)(int, speech::SpeechRecognitionManagerImpl::FSMEventArgs)>::Run(speech::SpeechRecognitionManagerImpl*, int const&, speech::SpeechRecognitionManagerImpl::FSMEventArgs const&) chrome-asan/src/./base/bind_internal.h:246
    #9 0x7f5d9da1d7c9 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (speech::SpeechRecognitionManagerImpl::*)(int, speech::SpeechRecognitionManagerImpl::FSMEventArgs)>, void (speech::SpeechRecognitionManagerImpl*, int const&, speech::SpeechRecognitionManagerImpl::FSMEventArgs const&)>::MakeItSo(base::internal::RunnableAdapter<void (speech::SpeechRecognitionManagerImpl::*)(int, speech::SpeechRecognitionManagerImpl::FSMEventArgs)>, speech::SpeechRecognitionManagerImpl*, int const&, speech::SpeechRecognitionManagerImpl::FSMEventArgs const&) chrome-asan/src/./base/bind_internal.h:927
    #10 0x7f5d9da1d648 in base::internal::Invoker<3, base::internal::BindState<base::internal::RunnableAdapter<void (speech::SpeechRecognitionManagerImpl::*)(int, speech::SpeechRecognitionManagerImpl::FSMEventArgs)>, void (speech::SpeechRecognitionManagerImpl*, int, speech::SpeechRecognitionManagerImpl::FSMEventArgs), void (base::internal::UnretainedWrapper<speech::SpeechRecognitionManagerImpl>, int, speech::SpeechRecognitionManagerImpl::FSMEventArgs)>, void (speech::SpeechRecognitionManagerImpl*, int, speech::SpeechRecognitionManagerImpl::FSMEventArgs)>::Run(base::internal::BindStateBase*) chrome-asan/src/./base/bind_internal.h:1384
    #11 0x7f5d9a3024b3 in MessageLoop::RunTask(base::PendingTask const&) chrome-asan/src/base/message_loop.cc:459
    #12 0x7f5d9a302be9 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) chrome-asan/src/base/message_loop.cc:470
    #13 0x7f5d9a302f02 in MessageLoop::DoWork() chrome-asan/src/base/message_loop.cc:647
    #14 0x7f5d9a29f462 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) chrome-asan/src/base/message_pump_libevent.cc:241
    #15 0x7f5d9a301cac in MessageLoop::RunInternal() chrome-asan/src/base/message_loop.cc:418
    #16 0x7f5d9a3009b8 in MessageLoop::Run() chrome-asan/src/base/message_loop.cc:301
    #17 0x7f5d9a376de1 in base::Thread::ThreadMain() chrome-asan/src/base/threading/thread.cc:166
    #18 0x7f5d9a36bd4c in base::(anonymous namespace)::ThreadFunc(void*) chrome-asan/src/base/threading/platform_thread_posix.cc:65
    #19 0x7f5d9f129fdc in __asan::AsanThread::ThreadStart() ??:0
previously allocated by thread T11 here:
    #0 0x7f5d9f12d5d2 in operator new(unsigned long) ??:0
    #1 0x7f5d9da1f40f in std::_Rb_tree<int, std::pair<int const, speech::SpeechRecognitionManagerImpl::Session>, std::_Select1st<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> >, std::less<int>, std::allocator<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> > >::_M_create_node(std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> const&) /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl_tree.h:369
    #2 0x7f5d9da1edc2 in std::_Rb_tree<int, std::pair<int const, speech::SpeechRecognitionManagerImpl::Session>, std::_Select1st<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> >, std::less<int>, std::allocator<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> > >::_M_insert_(std::_Rb_tree_node_base const*, std::_Rb_tree_node_base const*, std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> const&) /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl_tree.h:881
    #3 0x7f5d9da1f049 in std::_Rb_tree<int, std::pair<int const, speech::SpeechRecognitionManagerImpl::Session>, std::_Select1st<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> >, std::less<int>, std::allocator<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> > >::_M_insert_unique(std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> const&) /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl_tree.h:1177
    #4 0x7f5d9da1ea4a in std::_Rb_tree<int, std::pair<int const, speech::SpeechRecognitionManagerImpl::Session>, std::_Select1st<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> >, std::less<int>, std::allocator<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> > >::_M_insert_unique_(std::_Rb_tree_const_iterator<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> >, std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> const&) /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl_tree.h:1217
    #5 0x7f5d9da1e2e4 in std::map<int, speech::SpeechRecognitionManagerImpl::Session, std::less<int>, std::allocator<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> > >::insert(std::_Rb_tree_iterator<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> >, std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> const&) /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl_map.h:540
    #6 0x7f5d9da15587 in std::map<int, speech::SpeechRecognitionManagerImpl::Session, std::less<int>, std::allocator<std::pair<int const, speech::SpeechRecognitionManagerImpl::Session> > >::operator[](int const&) /usr/lib/gcc/x86_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl_map.h:450
    #7 0x7f5d9da14d5b in speech::SpeechRecognitionManagerImpl::CreateSession(content::SpeechRecognitionSessionConfig const&, content::SpeechRecognitionEventListener*) chrome-asan/src/content/browser/speech/speech_recognition_manager_impl.cc:69
    #8 0x7f5d9da12b21 in speech::InputTagSpeechDispatcherHost::OnStartRecognition(InputTagSpeechHostMsg_StartRecognition_Params const&) chrome-asan/src/content/browser/speech/input_tag_speech_dispatcher_host.cc:109
    #9 0x7f5d9da1268a in bool InputTagSpeechHostMsg_StartRecognition::Dispatch<speech::InputTagSpeechDispatcherHost, speech::InputTagSpeechDispatcherHost, void (speech::InputTagSpeechDispatcherHost::*)(InputTagSpeechHostMsg_StartRecognition_Params const&)>(IPC::Message const*, speech::InputTagSpeechDispatcherHost*, speech::InputTagSpeechDispatcherHost*, void (speech::InputTagSpeechDispatcherHost::*)(InputTagSpeechHostMsg_StartRecognition_Params const&)) chrome-asan/src/./content/common/speech_recognition_messages.h:48
    #10 0x7f5d9da12592 in speech::InputTagSpeechDispatcherHost::OnMessageReceived(IPC::Message const&, bool*) chrome-asan/src/content/browser/speech/input_tag_speech_dispatcher_host.cc:78
    #11 0x7f5d9d7fad8a in content::BrowserMessageFilter::DispatchMessage(IPC::Message const&) chrome-asan/src/content/public/browser/browser_message_filter.cc:106
    #12 0x7f5d9d7fa970 in content::BrowserMessageFilter::OnMessageReceived(IPC::Message const&) chrome-asan/src/content/public/browser/browser_message_filter.cc:91
    #13 0x7f5d9a3f0dc2 in IPC::ChannelProxy::Context::TryFilters(IPC::Message const&) chrome-asan/src/ipc/ipc_channel_proxy.cc:70
    #14 0x7f5d9a3f0eb2 in IPC::ChannelProxy::Context::OnMessageReceived(IPC::Message const&) chrome-asan/src/ipc/ipc_channel_proxy.cc:84
    #15 0x7f5d9a3f8777 in IPC::internal::ChannelReader::DispatchInputData(char const*, int) chrome-asan/src/ipc/ipc_channel_reader.cc:76
    #16 0x7f5d9a3f8450 in IPC::internal::ChannelReader::ProcessIncomingMessages() chrome-asan/src/ipc/ipc_channel_reader.cc:29
    #17 0x7f5d9a3eabae in IPC::Channel::ChannelImpl::OnFileCanReadWithoutBlocking(int) chrome-asan/src/ipc/ipc_channel_posix.cc:795
    #18 0x7f5d9a29db0a in base::MessagePumpLibevent::FileDescriptorWatcher::OnFileCanReadWithoutBlocking(int, base::MessagePumpLibevent*) chrome-asan/src/base/message_pump_libevent.cc:109
    #19 0x7f5d9a29ef24 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void*) chrome-asan/src/base/message_pump_libevent.cc:367
    #20 0x7f5d9a3c2519 in event_process_active chrome-asan/src/third_party/libevent/event.c:385
    #21 0x7f5d9a3c1758 in event_base_loop chrome-asan/src/third_party/libevent/event.c:526
    #22 0x7f5d9a29f79b in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) chrome-asan/src/base/message_pump_libevent.cc:279
Thread T11 created by T0 here:
    #0 0x7f5d9f122765 in pthread_create ??:0
    #1 0x7f5d9a36b8e6 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, unsigned long*, base::ThreadPriority) chrome-asan/src/base/threading/platform_thread_posix.cc:127
    #2 0x7f5d9a36b7cd in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate*, unsigned long*) chrome-asan/src/base/threading/platform_thread_posix.cc:249
    #3 0x7f5d9a376715 in base::Thread::StartWithOptions(base::Thread::Options const&) chrome-asan/src/base/threading/thread.cc:73
    #4 0x7f5d9d80ca79 in content::BrowserMainLoop::CreateThreads() chrome-asan/src/content/browser/browser_main_loop.cc:361
    #5 0x7f5d9d80f2d7 in (anonymous namespace)::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams const&) chrome-asan/src/content/browser/browser_main_runner.cc:86
    #6 0x7f5d9d80ab42 in BrowserMain(content::MainFunctionParams const&) chrome-asan/src/content/browser/browser_main.cc:17
    #7 0x7f5d9a1f3d5e in (anonymous namespace)::RunNamedProcessTypeMain(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) chrome-asan/src/content/app/content_main_runner.cc:290
    #8 0x7f5d9a1f3760 in (anonymous namespace)::ContentMainRunnerImpl::Run() chrome-asan/src/content/app/content_main_runner.cc:548
    #9 0x7f5d9a1f29ef in content::ContentMain(int, char const**, content::ContentMainDelegate*) chrome-asan/src/content/app/content_main.cc:35
    #10 0x7f5d98faa117 in ChromeMain chrome-asan/src/chrome/app/chrome_main.cc:32
    #11 0x7f5d98faa07b in main chrome-asan/src/chrome/app/chrome_exe_main_gtk.cc:18
    #12 0x7f5d92076c4d in ?? ??:0
==8395== ABORTING
Stats: 64M malloced (101M for red zones) by 312551 calls
Stats: 3M realloced by 17105 calls
Stats: 50M freed by 246893 calls
Stats: 0M really freed by 0 calls
Stats: 200M (51221 full pages) mmaped in 50 calls
  mmaps   by size class: 8:278511; 9:24573; 10:16380; 11:10235; 12:3072; 13:1024; 14:768; 15:128; 16:384; 17:64; 18:32; 19:8; 20:4;
  mallocs by size class: 8:268179; 9:17806; 10:14069; 11:8405; 12:2063; 13:992; 14:508; 15:97; 16:374; 17:35; 18:20; 19:1; 20:2;
  frees   by size class: 8:211592; 9:15184; 10:13130; 11:3782; 12:1534; 13:781; 14:438; 15:60; 16:350; 17:24; 18:16; 19:1; 20:1;
  rfrees  by size class:
Stats: malloc large: 58 small slow: 1304
Shadow byte and word:
  0x1febae6f33fc: fd
  0x1febae6f33f8: fd fd fd fd fd fd fd fd
More shadow bytes:
  0x1febae6f33d8: fb fb fb fb fb fb fb fb
  0x1febae6f33e0: fa fa fa fa fa fa fa fa
  0x1febae6f33e8: fa fa fa fa fa fa fa fa
  0x1febae6f33f0: fd fd fd fd fd fd fd fd
=>0x1febae6f33f8: fd fd fd fd fd fd fd fd
  0x1febae6f3400: fa fa fa fa fa fa fa fa
  0x1febae6f3408: fa fa fa fa fa fa fa fa
  0x1febae6f3410: 00 00 00 00 00 00 00 00
  0x1febae6f3418: fb fb fb fb fb fb fb fb


### [Deleted User] (2012-05-03)

primiano, this seems like a recent regression. Can you take a look?

### in...@chromium.org (2012-05-03)

[Empty comment from Monorail migration]

### pr...@chromium.org (2012-05-04)

Can I ask some further information to reproduce the bug? I am not able to reproduce it:

- Does it crash only with ASan or also without?
- Does it crash with both debug and release builds?

Thanks,
Primiano

### pr...@chromium.org (2012-05-04)

Ok, I was able to reproduce it (only when compiling with ASan), and will fix it soon.
Thanks for the report.

### bu...@chromium.org (2012-05-04)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=135356

------------------------------------------------------------------------
r135356 | primiano@chromium.org | Fri May 04 09:21:57 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/speech/speech_recognition_manager_impl.cc?r1=135356&r2=135355&pathrev=135356
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/speech/speech_recognizer_impl.cc?r1=135356&r2=135355&pathrev=135356

Fixed three memory bugs in SpeechRecognitionManagerImpl and SpeechRecognizerImpl.

- Use after free of SpeechRecognitionManagerImpl::Session, occurring regularly on session deletion.
- Use after free SpeechRecognitionManagerImpl, occurring (very seldom) when singleton dtor is called while a posted task is running. (Now SpeechRecognitionManagerImpl uses LeakySingletonTraits)
- Corruption of audio controller in SpeechRecognizer, happening if destroying ungracefully the recognizer without closing the audio_controller first.

BUG=126048,116954
TEST=Run content_unittests with ASan.

Review URL: https://chromiumcodereview.appspot.com/10317015
------------------------------------------------------------------------

### in...@chromium.org (2012-05-04)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-23)

Thanks for catching this regression Chamal! $1000

### ch...@gmail.com (2012-05-23)

Thank you very much for the reward :)

### ch...@gmail.com (2012-06-20)

When can I receive the reward for this issue? :)

### sc...@gmail.com (2012-07-09)

Invoice finalized, payment in system.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/126048?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057621)*

# Security: UAF in cast_channel::CastSocketServiceImpl::OpenSocket

| Field | Value |
|-------|-------|
| **Issue ID** | [40072664](https://issues.chromium.org/issues/40072664) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Cast |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | vu...@darknavy.com |
| **Assignee** | mf...@chromium.org |
| **Created** | 2023-09-18 |
| **Bounty** | $1,000.00 |

## Description

UAF in cast\_channel::CastSocketServiceImpl::OpenSocket

**VULNERABILITY DETAILS**  

The root cause is similar to [crbug.com/925864](https://crbug.com/925864)

`last_channel_id_` is an int, and it can wrap [0]. sockets\_.insert can fail when an id already exists, then `socket` is freed, causing UAF in the later usages in CastSocketServiceImpl::OpenSocket [1][2].

```
CastSocket\* CastSocketServiceImpl::AddSocket(  
    std::unique_ptr<CastSocket> socket) {  
  DCHECK(task_runner_->BelongsToCurrentThread());  
  DCHECK(socket);  
  int id = ++last_channel_id_; // [0]  
  socket->set_id(id);  
  
  auto\* socket_ptr = socket.get();  
  sockets_.insert(std::make_pair(id, std::move(socket)));  
  return socket_ptr;  
}  

```

UAF place:

```
void CastSocketServiceImpl::OpenSocket(  
    NetworkContextGetter network_context_getter,  
    const CastSocketOpenParams& open_params,  
    CastSocket::OnOpenCallback open_cb) {  
  // ... snip ...  
    } else {  
      socket = new CastSocketImpl(network_context_getter, open_params, logger_);  
      AddSocket(base::WrapUnique(socket));  
    }  
  }  
  
  for (auto& observer : observers_)  
    socket->AddObserver(&observer); // [1]  
  
  socket->Connect(std::move(open_cb)); // [2]  
}  

```

[0] <https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/common/providers/cast/channel/cast_socket_service.cc;drc=e74a812e4980bc9b74f308f96b516cf839046ec8;l=46>  

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/common/providers/cast/channel/cast_socket_service.cc;drc=e74a812e4980bc9b74f308f96b516cf839046ec8;l=113>

**VERSION**  

Chrome Version: stable  

Operating System: Linux, Mac, Windows

SUGGESTED FIX:  

Similar to [crbug.com/925864](https://crbug.com/925864)

**REPRODUCTION CASE**  

Currently I don't find a way to trigger this without a Chromecast device. I'm still working on it. But I believe this could be triggered by open/close the cast functionality repeatedly without a compromised renderer. Note that we don't need to keep all connections opened to trigger. Only the socket with a conflicted id needs to be held.  

For demonstrating the integer overflow only, we can change the type of |last\_channel\_id\_| to int8\_t. And OpenSocket 0x101 times. See poc.diff for detail.

Reproduce steps:  

Apply poc.diff and build components\_unittests. Run it with:  

$ ./components\_unittests --gtest\_filter="CastSocketServiceTest.TestChannelIdOverflow"

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: browser Crash log:

==24269==ERROR: AddressSanitizer: heap-use-after-free on address 0x51400006ba40 at pc 0x55b8ecacf483 bp 0x7ffd4482af50 sp 0x7ffd4482af48  

READ of size 8 at 0x51400006ba40 thread T0  

#0 0x55b8ecacf482 in cast\_channel::CastSocketServiceImpl::OpenSocket(base::RepeatingCallback<network::mojom::NetworkContext\* ()>, cast\_channel::CastSocketOpenParams const&, base::OnceCallback<void (cast\_channel::CastSocket\*)>) components/media\_router/common/providers/cast/channel/cast\_socket\_service.cc:115:11  

#1 0x55b8d21cb997 in cast\_channel::CastSocketServiceTest\_TestChannelIdOverflow\_Test::TestBody() components/media\_router/common/providers/cast/channel/cast\_socket\_service\_unittest.cc:109:27  

#2 0x55b8d3f2686f in void testing::internal::HandleSehExceptionsInMethodIfSupported<testing::Test, void>(testing::Test\*, void (testing::Test::\*)(), char const\*) third\_party/googletest/src/googletest/src/gtest.cc:2595:10  

#3 0x55b8d3ecf1e0 in void testing::internal::HandleExceptionsInMethodIfSupported<testing::Test, void>(testing::Test\*, void (testing::Test::\*)(), char const\*) third\_party/googletest/src/googletest/src/gtest.cc:2650:12  

#4 0x55b8d3ea0d6d in testing::Test::Run() third\_party/googletest/src/googletest/src/gtest.cc:2670:5  

#5 0x55b8d3ea207a in testing::TestInfo::Run() third\_party/googletest/src/googletest/src/gtest.cc:2849:11  

#6 0x55b8d3ea31f0 in testing::TestSuite::Run() third\_party/googletest/src/googletest/src/gtest.cc:3008:30  

#7 0x55b8d3ebc0a2 in testing::internal::UnitTestImpl::RunAllTests() third\_party/googletest/src/googletest/src/gtest.cc:5866:44  

#8 0x55b8d3f27e1f in bool testing::internal::HandleSehExceptionsInMethodIfSupported<testing::internal::UnitTestImpl, bool>(testing::internal::UnitTestImpl\*, bool (testing::internal::UnitTestImpl::\*)(), char const\*) third\_party/googletest/src/googletest/src/gtest.cc:2595:10  

#9 0x55b8d3ed430d in bool testing::internal::HandleExceptionsInMethodIfSupported<testing::internal::UnitTestImpl, bool>(testing::internal::UnitTestImpl\*, bool (testing::internal::UnitTestImpl::\*)(), char const\*) third\_party/googletest/src/googletest/src/gtest.cc:2650:12  

#10 0x55b8d3ebb521 in testing::UnitTest::Run() third\_party/googletest/src/googletest/src/gtest.cc:5440:10  

#11 0x55b8e157f180 in RUN\_ALL\_TESTS() third\_party/googletest/src/googletest/include/gtest/gtest.h:2284:73  

#12 0x55b8e157bfc0 in base::TestSuite::RunAllTests() base/test/test\_suite.cc:613:10  

#13 0x55b8e157975d in base::TestSuite::Run() base/test/test\_suite.cc:406:16  

#14 0x55b8e631c909 in content::UnitTestTestSuite::Run() content/public/test/unittest\_test\_suite.cc:189:23  

#15 0x55b8da91ae0b in int base::internal::FunctorTraits<int (content::UnitTestTestSuite::\*)(), void>::Invoke<int (content::UnitTestTestSuite::\*)(), std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>(int (content::UnitTestTestSuite::\*)(), std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>&&) base/functional/bind\_internal.h:713:12  

#16 0x55b8da91ab88 in int base::internal::InvokeHelper<false, int, 0ul>::MakeItSo<int (content::UnitTestTestSuite::\*)(), std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>>(int (content::UnitTestTestSuite::\*&&)(), std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>&&) base/functional/bind\_internal.h:868:12  

#17 0x55b8da91a8a8 in int base::internal::Invoker<base::internal::BindState<int (content::UnitTestTestSuite::\*)(), std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>, int ()>::RunImpl<int (content::UnitTestTestSuite::\*)(), std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>, 0ul>(int (content::UnitTestTestSuite::\*&&)(), std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul>) base/functional/bind\_internal.h:968:12  

#18 0x55b8da91a738 in base::internal::Invoker<base::internal::BindState<int (content::UnitTestTestSuite::\*)(), std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>, int ()>::RunOnce(base::internal::BindStateBase\*) base/functional/bind\_internal.h:919:12  

#19 0x55b8cf4221d8 in base::OnceCallback<int ()>::Run() && base/functional/callback.h:152:12  

#20 0x55b8e1597427 in base::(anonymous namespace)::RunTestSuite(base::OnceCallback<int ()>, unsigned long, int, unsigned long, bool, base::RepeatingCallback<void ()>, base::OnceCallback<void ()>) base/test/launcher/unit\_test\_launcher.cc:179:38  

#21 0x55b8e1594448 in base::(anonymous namespace)::LaunchUnitTestsInternal(base::OnceCallback<int ()>, unsigned long, int, unsigned long, bool, base::RepeatingCallback<void ()>, base::OnceCallback<void ()>) base/test/launcher/unit\_test\_launcher.cc:240:10  

#22 0x55b8e1594031 in base::LaunchUnitTests(int, char\*\*, base::OnceCallback<int ()>, unsigned long) base/test/launcher/unit\_test\_launcher.cc:288:10  

#23 0x55b8cd61da3f in main components/test/run\_all\_unittests.cc:8:10  

#24 0x7fc950e29d8f in \_\_libc\_start\_call\_main csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16

0x51400006ba40 is located 0 bytes inside of 416-byte region [0x51400006ba40,0x51400006bbe0)  

freed by thread T0 here:  

#0 0x55b8c2ca540d in operator delete(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:152:3  

#1 0x55b8ecb2aaf1 in cast\_channel::MockCastSocket::~MockCastSocket() components/media\_router/common/providers/cast/channel/cast\_test\_util.cc:46:35  

#2 0x55b8d21d7942 in std::\_\_Cr::default\_delete<cast\_channel::CastSocket>::operator()(cast\_channel::CastSocket\*) const third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:68:5  

#3 0x55b8d21d78bf in std::\_\_Cr::unique\_ptr<cast\_channel::CastSocket, std::\_\_Cr::default\_delete<cast\_channel::CastSocket>>::reset(cast\_channel::CastSocket\*) third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:297:7  

#4 0x55b8d21cd3c8 in std::\_\_Cr::unique\_ptr<cast\_channel::CastSocket, std::\_\_Cr::default\_delete<cast\_channel::CastSocket>>::~unique\_ptr() third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:263:75  

#5 0x55b8ecad1248 in std::\_\_Cr::pair<int, std::\_\_Cr::unique\_ptr<cast\_channel::CastSocket, std::\_\_Cr::default\_delete<cast\_channel::CastSocket>>>::~pair() third\_party/libc++/src/include/\_\_utility/pair.h:81:29  

#6 0x55b8ecacd563 in cast\_channel::CastSocketServiceImpl::AddSocket(std::\_\_Cr::unique\_ptr<cast\_channel::CastSocket, std::\_\_Cr::default\_delete<cast\_channel::CastSocket>>) components/media\_router/common/providers/cast/channel/cast\_socket\_service.cc:50:3  

#7 0x55b8ecacf1cc in cast\_channel::CastSocketServiceImpl::OpenSocket(base::RepeatingCallback<network::mojom::NetworkContext\* ()>, cast\_channel::CastSocketOpenParams const&, base::OnceCallback<void (cast\_channel::CastSocket\*)>) components/media\_router/common/providers/cast/channel/cast\_socket\_service.cc:105:16  

#8 0x55b8d21cb997 in cast\_channel::CastSocketServiceTest\_TestChannelIdOverflow\_Test::TestBody() components/media\_router/common/providers/cast/channel/cast\_socket\_service\_unittest.cc:109:27  

#9 0x55b8d3f2686f in void testing::internal::HandleSehExceptionsInMethodIfSupported<testing::Test, void>(testing::Test\*, void (testing::Test::\*)(), char const\*) third\_party/googletest/src/googletest/src/gtest.cc:2595:10  

#10 0x55b8d3ecf1e0 in void testing::internal::HandleExceptionsInMethodIfSupported<testing::Test, void>(testing::Test\*, void (testing::Test::\*)(), char const\*) third\_party/googletest/src/googletest/src/gtest.cc:2650:12  

#11 0x55b8d3ea0d6d in testing::Test::Run() third\_party/googletest/src/googletest/src/gtest.cc:2670:5  

#12 0x55b8d3ea207a in testing::TestInfo::Run() third\_party/googletest/src/googletest/src/gtest.cc:2849:11  

#13 0x55b8d3ea31f0 in testing::TestSuite::Run() third\_party/googletest/src/googletest/src/gtest.cc:3008:30  

#14 0x55b8d3ebc0a2 in testing::internal::UnitTestImpl::RunAllTests() third\_party/googletest/src/googletest/src/gtest.cc:5866:44  

#15 0x55b8d3f27e1f in bool testing::internal::HandleSehExceptionsInMethodIfSupported<testing::internal::UnitTestImpl, bool>(testing::internal::UnitTestImpl\*, bool (testing::internal::UnitTestImpl::\*)(), char const\*) third\_party/googletest/src/googletest/src/gtest.cc:2595:10  

#16 0x55b8d3ed430d in bool testing::internal::HandleExceptionsInMethodIfSupported<testing::internal::UnitTestImpl, bool>(testing::internal::UnitTestImpl\*, bool (testing::internal::UnitTestImpl::\*)(), char const\*) third\_party/googletest/src/googletest/src/gtest.cc:2650:12  

#17 0x55b8d3ebb521 in testing::UnitTest::Run() third\_party/googletest/src/googletest/src/gtest.cc:5440:10  

#18 0x55b8e157f180 in RUN\_ALL\_TESTS() third\_party/googletest/src/googletest/include/gtest/gtest.h:2284:73  

#19 0x55b8e157bfc0 in base::TestSuite::RunAllTests() base/test/test\_suite.cc:613:10  

#20 0x55b8e157975d in base::TestSuite::Run() base/test/test\_suite.cc:406:16  

#21 0x55b8e631c909 in content::UnitTestTestSuite::Run() content/public/test/unittest\_test\_suite.cc:189:23  

#22 0x55b8da91ae0b in int base::internal::FunctorTraits<int (content::UnitTestTestSuite::\*)(), void>::Invoke<int (content::UnitTestTestSuite::\*)(), std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>(int (content::UnitTestTestSuite::\*)(), std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>&&) base/functional/bind\_internal.h:713:12  

#23 0x55b8da91ab88 in int base::internal::InvokeHelper<false, int, 0ul>::MakeItSo<int (content::UnitTestTestSuite::\*)(), std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>>(int (content::UnitTestTestSuite::\*&&)(), std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>&&) base/functional/bind\_internal.h:868:12  

#24 0x55b8da91a8a8 in int base::internal::Invoker<base::internal::BindState<int (content::UnitTestTestSuite::\*)(), std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>, int ()>::RunImpl<int (content::UnitTestTestSuite::\*)(), std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>, 0ul>(int (content::UnitTestTestSuite::\*&&)(), std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul>) base/functional/bind\_internal.h:968:12  

#25 0x55b8da91a738 in base::internal::Invoker<base::internal::BindState<int (content::UnitTestTestSuite::\*)(), std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>, int ()>::RunOnce(base::internal::BindStateBase\*) base/functional/bind\_internal.h:919:12  

#26 0x55b8cf4221d8 in base::OnceCallback<int ()>::Run() && base/functional/callback.h:152:12  

#27 0x55b8e1597427 in base::(anonymous namespace)::RunTestSuite(base::OnceCallback<int ()>, unsigned long, int, unsigned long, bool, base::RepeatingCallback<void ()>, base::OnceCallback<void ()>) base/test/launcher/unit\_test\_launcher.cc:179:38  

#28 0x55b8e1594448 in base::(anonymous namespace)::LaunchUnitTestsInternal(base::OnceCallback<int ()>, unsigned long, int, unsigned long, bool, base::RepeatingCallback<void ()>, base::OnceCallback<void ()>) base/test/launcher/unit\_test\_launcher.cc:240:10  

#29 0x55b8e1594031 in base::LaunchUnitTests(int, char\*\*, base::OnceCallback<int ()>, unsigned long) base/test/launcher/unit\_test\_launcher.cc:288:10

previously allocated by thread T0 here:  

#0 0x55b8c2ca4bad in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x55b8d21cb5db in cast\_channel::CastSocketServiceTest\_TestChannelIdOverflow\_Test::TestBody() components/media\_router/common/providers/cast/channel/cast\_socket\_service\_unittest.cc:101:25  

#2 0x55b8d3f2686f in void testing::internal::HandleSehExceptionsInMethodIfSupported<testing::Test, void>(testing::Test\*, void (testing::Test::\*)(), char const\*) third\_party/googletest/src/googletest/src/gtest.cc:2595:10  

#3 0x55b8d3ecf1e0 in void testing::internal::HandleExceptionsInMethodIfSupported<testing::Test, void>(testing::Test\*, void (testing::Test::\*)(), char const\*) third\_party/googletest/src/googletest/src/gtest.cc:2650:12  

#4 0x55b8d3ea0d6d in testing::Test::Run() third\_party/googletest/src/googletest/src/gtest.cc:2670:5  

#5 0x55b8d3ea207a in testing::TestInfo::Run() third\_party/googletest/src/googletest/src/gtest.cc:2849:11  

#6 0x55b8d3ea31f0 in testing::TestSuite::Run() third\_party/googletest/src/googletest/src/gtest.cc:3008:30  

#7 0x55b8d3ebc0a2 in testing::internal::UnitTestImpl::RunAllTests() third\_party/googletest/src/googletest/src/gtest.cc:5866:44  

#8 0x55b8d3f27e1f in bool testing::internal::HandleSehExceptionsInMethodIfSupported<testing::internal::UnitTestImpl, bool>(testing::internal::UnitTestImpl\*, bool (testing::internal::UnitTestImpl::\*)(), char const\*) third\_party/googletest/src/googletest/src/gtest.cc:2595:10  

#9 0x55b8d3ed430d in bool testing::internal::HandleExceptionsInMethodIfSupported<testing::internal::UnitTestImpl, bool>(testing::internal::UnitTestImpl\*, bool (testing::internal::UnitTestImpl::\*)(), char const\*) third\_party/googletest/src/googletest/src/gtest.cc:2650:12  

#10 0x55b8d3ebb521 in testing::UnitTest::Run() third\_party/googletest/src/googletest/src/gtest.cc:5440:10  

#11 0x55b8e157f180 in RUN\_ALL\_TESTS() third\_party/googletest/src/googletest/include/gtest/gtest.h:2284:73  

#12 0x55b8e157bfc0 in base::TestSuite::RunAllTests() base/test/test\_suite.cc:613:10  

#13 0x55b8e157975d in base::TestSuite::Run() base/test/test\_suite.cc:406:16  

#14 0x55b8e631c909 in content::UnitTestTestSuite::Run() content/public/test/unittest\_test\_suite.cc:189:23  

#15 0x55b8da91ae0b in int base::internal::FunctorTraits<int (content::UnitTestTestSuite::\*)(), void>::Invoke<int (content::UnitTestTestSuite::\*)(), std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>(int (content::UnitTestTestSuite::\*)(), std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>&&) base/functional/bind\_internal.h:713:12  

#16 0x55b8da91ab88 in int base::internal::InvokeHelper<false, int, 0ul>::MakeItSo<int (content::UnitTestTestSuite::\*)(), std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>>(int (content::UnitTestTestSuite::\*&&)(), std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>&&) base/functional/bind\_internal.h:868:12  

#17 0x55b8da91a8a8 in int base::internal::Invoker<base::internal::BindState<int (content::UnitTestTestSuite::\*)(), std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>, int ()>::RunImpl<int (content::UnitTestTestSuite::\*)(), std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>, 0ul>(int (content::UnitTestTestSuite::\*&&)(), std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul>) base/functional/bind\_internal.h:968:12  

#18 0x55b8da91a738 in base::internal::Invoker<base::internal::BindState<int (content::UnitTestTestSuite::\*)(), std::\_\_Cr::unique\_ptr<content::UnitTestTestSuite, std::\_\_Cr::default\_delete[content::UnitTestTestSuite](javascript:void(0);)>>, int ()>::RunOnce(base::internal::BindStateBase\*) base/functional/bind\_internal.h:919:12  

#19 0x55b8cf4221d8 in base::OnceCallback<int ()>::Run() && base/functional/callback.h:152:12  

#20 0x55b8e1597427 in base::(anonymous namespace)::RunTestSuite(base::OnceCallback<int ()>, unsigned long, int, unsigned long, bool, base::RepeatingCallback<void ()>, base::OnceCallback<void ()>) base/test/launcher/unit\_test\_launcher.cc:179:38  

#21 0x55b8e1594448 in base::(anonymous namespace)::LaunchUnitTestsInternal(base::OnceCallback<int ()>, unsigned long, int, unsigned long, bool, base::RepeatingCallback<void ()>, base::OnceCallback<void ()>) base/test/launcher/unit\_test\_launcher.cc:240:10  

#22 0x55b8e1594031 in base::LaunchUnitTests(int, char\*\*, base::OnceCallback<int ()>, unsigned long) base/test/launcher/unit\_test\_launcher.cc:288:10  

#23 0x55b8cd61da3f in main components/test/run\_all\_unittests.cc:8:10  

#24 0x7fc950e29d8f in \_\_libc\_start\_call\_main csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16

SUMMARY: AddressSanitizer: heap-use-after-free components/media\_router/common/providers/cast/channel/cast\_socket\_service.cc:115:11 in cast\_channel::CastSocketServiceImpl::OpenSocket(base::RepeatingCallback<network::mojom::NetworkContext\* ()>, cast\_channel::CastSocketOpenParams const&, base::OnceCallback<void (cast\_channel::CastSocket\*)>)  

Shadow bytes around the buggy address:  

0x51400006b780: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa  

0x51400006b800: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x51400006b880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x51400006b900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x51400006b980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa  

=>0x51400006ba00: fa fa fa fa fa fa fa fa[fd]fd fd fd fd fd fd fd  

0x51400006ba80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x51400006bb00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x51400006bb80: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x51400006bc00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x51400006bc80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==24269==ADDITIONAL INFO

==24269==Note: Please include this section with the ASan report.  

Task trace:

==24269==END OF ADDITIONAL INFO  

==24269==ABORTING  

[1/1] CastSocketServiceTest.TestChannelIdOverflow (CRASHED)  

1 test crashed:  

CastSocketServiceTest.TestChannelIdOverflow (../../components/media\_router/common/providers/cast/channel/cast\_socket\_service\_unittest.cc:99)  

Tests took 5 seconds.

**CREDIT INFORMATION**  

Reporter credit: DarkNavy

## Attachments

- [poc.diff](attachments/poc.diff) (text/plain, 2.6 KB)

## Timeline

### [Deleted User] (2023-09-18)

[Empty comment from Monorail migration]

### nh...@google.com (2023-09-18)

I'm able to reproduce by patching in the provided diff.

I'm tentatively setting the severity assuming that this runs in the browser process. If CastSocketServiceImpl runs in a renderer instead, let me know so that the severity can be adjusted.

I'm also assuming that this applies to all OSes - please adjust if that's not the case.

[Monorail components: Internals>Cast]

### [Deleted User] (2023-09-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-19)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-19)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mf...@chromium.org (2023-09-19)

I don't get why this is high severity.  It involves a local patch to Chrome to reduce the socket counter from 32 bits to 8.  Of course it's going to be easy to overflow if you do that.


### mf...@chromium.org (2023-09-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4a89188f9b98ba9611807d0de7becc1e0c43a19d

commit 4a89188f9b98ba9611807d0de7becc1e0c43a19d
Author: mark a. foltz <mfoltz@chromium.org>
Date: Wed Sep 20 19:05:41 2023

[Cast Channel] Check for overflow in channel_id.

In extreme circumstances it may be possible for the channel_id used for
each Cast Channel connection to overflow; for example a browser running
for 3 years connecting and disconnecting to a Cast device every 50 ms.

CHECK-fail rather than trying to recover from this situation.

Fixed: 1484000
Change-Id: Ia423f3629b48a435fdf2e2e08d51817088383247
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4874182
Reviewed-by: Muyao Xu <muyaoxu@google.com>
Commit-Queue: Mark Foltz <mfoltz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1199141}

[modify] https://crrev.com/4a89188f9b98ba9611807d0de7becc1e0c43a19d/components/media_router/common/providers/cast/channel/cast_socket_service.cc


### [Deleted User] (2023-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-21)

Requesting merge to extended stable M116 because latest trunk commit (1199141) appears to be after extended stable branch point (1160321).

Requesting merge to stable M117 because latest trunk commit (1199141) appears to be after stable branch point (1181205).

Requesting merge to beta M118 because latest trunk commit (1199141) appears to be after beta branch point (1192594).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-21)

Merge review required: M118 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-21)

Merge review required: M117 is already shipping to stable.

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
Owners: harrysouders (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-21)

Merge review required: M116 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-09-22)

M118 merges approved for https://crrev.com/c/4874182

Please merge to M118 Beta / branch 5993 at your earliest convenience before EOD Tuesday, 26 September. 

M117 and M116 are in the process of being cut for scheduled security refresh, so I'll revisit this early next week for review for those branches.

### go...@chromium.org (2023-09-25)

Please merge your change to M118 branch ASAP so we can take it in for this week's beta release. Thank you. 

Branch Details: https://chromiumdash.appspot.com/branches

### go...@chromium.org (2023-09-25)

Please merge your change to M118 branch ASAP so we can take it in for this week's beta release. Thank you. 

Branch Details: https://chromiumdash.appspot.com/branches

### da...@google.com (2023-09-26)

I have manually cherry picked this to ensure it is included in tonights Beta RC cut.

### gi...@appspot.gserviceaccount.com (2023-09-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/625f55a3aa1b2621b28b0070f71805d8b7fcc741

commit 625f55a3aa1b2621b28b0070f71805d8b7fcc741
Author: mark a. foltz <mfoltz@chromium.org>
Date: Tue Sep 26 14:20:35 2023

[Cast Channel] Check for overflow in channel_id.

In extreme circumstances it may be possible for the channel_id used for
each Cast Channel connection to overflow; for example a browser running
for 3 years connecting and disconnecting to a Cast device every 50 ms.

CHECK-fail rather than trying to recover from this situation.

(cherry picked from commit 4a89188f9b98ba9611807d0de7becc1e0c43a19d)

Fixed: 1484000
Change-Id: Ia423f3629b48a435fdf2e2e08d51817088383247
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4874182
Reviewed-by: Muyao Xu <muyaoxu@google.com>
Commit-Queue: Mark Foltz <mfoltz@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1199141}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4885096
Auto-Submit: Daniel Yip <danielyip@google.com>
Reviewed-by: Daniel Yip <danielyip@google.com>
Owners-Override: Daniel Yip <danielyip@google.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5993@{#825}
Cr-Branched-From: 511350718e646be62331ae9d7213d10ec320d514-refs/heads/main@{#1192594}

[modify] https://crrev.com/625f55a3aa1b2621b28b0070f71805d8b7fcc741/components/media_router/common/providers/cast/channel/cast_socket_service.cc


### [Deleted User] (2023-09-26)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wf...@chromium.org (2023-09-27)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-28)

Removing merge labels since we do not backmerge to stable/extended for low severity bugs!

### am...@google.com (2023-09-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-29)

Congratulations, DarkNavy! The Chrome VRP Panel has decided to award you $1,000 for this significantly mitigated security bug. The reward amount was decided upon based on the preconditions of a malicious Cast device, and the significant preconditions and time to create the conditions to overflow. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-09-30)

[Empty comment from Monorail migration]

### gm...@google.com (2023-10-03)

This a low, rejecting for LTS-114.

### pg...@google.com (2023-10-09)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1484000?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40072664)*

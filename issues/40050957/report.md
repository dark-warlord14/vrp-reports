# Security:Wrong assumption lead to Use After Free in deserializer.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40050957](https://issues.chromium.org/issues/40050957) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | ul...@chromium.org |
| **Created** | 2019-12-12 |
| **Bounty** | $500.00 |

## Description

1. the bug
the function PostProcessNewObject assume there is no gc, but it's wrong.
HeapObject Deserializer::PostProcessNewObject(HeapObject obj,           ------------------> obj is a raw pointer
                                              SnapshotSpace space) {
  DisallowHeapAllocation no_gc; ---------------------> wrong assumption
  ......
   } else if (obj.IsJSArrayBuffer()) {
    JSArrayBuffer buffer = JSArrayBuffer::cast(obj);
    // Only fixup for the off-heap case.
    if (buffer.backing_store() != nullptr) {
      // Serializer writes backing store ref in |backing_store| field.
      size_t store_index = reinterpret_cast<size_t>(buffer.backing_store());
      auto backing_store = backing_stores_[store_index];
      SharedFlag shared = backing_store && backing_store->is_shared()
                              ? SharedFlag::kShared
                              : SharedFlag::kNotShared;
      buffer.Setup(shared, backing_store);  -------------------------> this call may cause a gc;
    }
  } 
  ......
  return obj;  --------------------> the raw pointer is used after gc, may be invalid.
}

Based on this wrong assumption, many raw poiters are use after calling PostProcessNewObject without handify, which will cause Use After Free too(gc move the object),

2. how to trigger
I add a test case to cctest to trigger this bug,the patch of the poc is as follows:

/v8/v8$ git diff
diff --git a/test/cctest/test-serialize.cc b/test/cctest/test-serialize.cc
index e2ab996796..c7bc0e8f71 100644
--- a/test/cctest/test-serialize.cc
+++ b/test/cctest/test-serialize.cc
@@ -980,6 +980,15 @@ UNINITIALIZED_TEST(CustomSnapshotDataBlobSharedArrayBuffer) {
   TypedArrayTestHelper(code, expectations);
 }
 
+UNINITIALIZED_TEST(CustomSnapshotBigArrayBuffer) {
+  const char* code =
+      "var x = new Int8Array(0x3fffffff);";
+  Int32Expectations expectations = {
+  };
+
+  TypedArrayTestHelper(code, expectations);
+}
+
 UNINITIALIZED_TEST(CustomSnapshotDataBlobArrayBufferWithOffset) {
   const char* code =
       "var x = new Int32Array([12, 24, 48, 96]);"

after applying the patch and compile cctest, run the command "./cctest  test-serialize/CustomSnapshotBigArrayBuffer"

if you build a debug version cctest, the crash is as follows:
Starting program: /hdd2/v8/v8/out/x64.debug/cctest test-serialize/CustomSnapshotBigArrayBuffer
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
[New Thread 0x7ffff0d85700 (LWP 18327)]
[New Thread 0x7ffff0584700 (LWP 18328)]
[New Thread 0x7fffefd83700 (LWP 18329)]
[New Thread 0x7fffef582700 (LWP 18330)]
[New Thread 0x7fffeed81700 (LWP 18331)]
[New Thread 0x7fffee580700 (LWP 18332)]
[New Thread 0x7fffedd7f700 (LWP 18333)]


#
# Fatal error in ../../src/heap/heap.cc, line 1527
# Debug check failed: AllowHeapAllocation::IsAllowed().
#
#
#
#FailureMessage Object: 0x7fffffffa390
==== C stack trace ===============================

    /hdd2/v8/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x21) [0x7ffff7feb731]
    /hdd2/v8/v8/out/x64.debug/libv8_libplatform.so(+0x40567) [0x7ffff7f83567]
    /hdd2/v8/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x22a) [0x7ffff7fd730a]
    /hdd2/v8/v8/out/x64.debug/libv8_libbase.so(+0x35d7c) [0x7ffff7fd6d7c]
    /hdd2/v8/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x27) [0x7ffff7fd73d7]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)+0x23f) [0x7ffff56f1d3f]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::Heap::CollectAllGarbage(int, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)+0x3c) [0x7ffff56f0f7c]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::Heap::ReportExternalMemoryPressure()+0x81) [0x7ffff56f2c81]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::Isolate::ReportExternalAllocationLimitReached()+0x3c) [0x7ffff5300bec]
    /hdd2/v8/v8/out/x64.debug/cctest(v8::Isolate::AdjustAmountOfExternalAllocatedMemory(long)+0xea) [0x5555568cb9aa]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::ArrayBufferTracker::RegisterNew(v8::internal::Heap*, v8::internal::JSArrayBuffer, std::__Cr::shared_ptr<v8::internal::BackingStore>)+0x2ad) [0x7ffff570e6ad]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::Heap::RegisterBackingStore(v8::internal::JSArrayBuffer, std::__Cr::shared_ptr<v8::internal::BackingStore>)+0x45) [0x7ffff56f9695]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::JSArrayBuffer::Attach(std::__Cr::shared_ptr<v8::internal::BackingStore>)+0x1d1) [0x7ffff5a57231]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::JSArrayBuffer::Setup(v8::internal::SharedFlag, std::__Cr::shared_ptr<v8::internal::BackingStore>)+0xf2) [0x7ffff5a57042]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::Deserializer::PostProcessNewObject(v8::internal::HeapObject, v8::internal::SnapshotSpace)+0xa31) [0x7ffff5e2d811]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::Deserializer::ReadObject(v8::internal::SnapshotSpace)+0xef) [0x7ffff5e2e5df]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::FullMaybeObjectSlot v8::internal::Deserializer::ReadDataCase<v8::internal::FullMaybeObjectSlot, (v8::internal::SerializerDeserializer::Bytecode)0, (v8::internal::SnapshotSpace)6>(v8::internal::Isolate*, v8::internal::FullMaybeObjectSlot, unsigned long, unsigned char, bool)+0x82) [0x7ffff5e34872]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(bool v8::internal::Deserializer::ReadData<v8::internal::FullMaybeObjectSlot>(v8::internal::FullMaybeObjectSlot, v8::internal::FullMaybeObjectSlot, v8::internal::SnapshotSpace, unsigned long)+0x1b7) [0x7ffff5e2f717]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::Deserializer::ReadObject(v8::internal::SnapshotSpace)+0xca) [0x7ffff5e2e5ba]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::FullMaybeObjectSlot v8::internal::Deserializer::ReadDataCase<v8::internal::FullMaybeObjectSlot, (v8::internal::SerializerDeserializer::Bytecode)0, (v8::internal::SnapshotSpace)6>(v8::internal::Isolate*, v8::internal::FullMaybeObjectSlot, unsigned long, unsigned char, bool)+0x82) [0x7ffff5e34872]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(bool v8::internal::Deserializer::ReadData<v8::internal::FullMaybeObjectSlot>(v8::internal::FullMaybeObjectSlot, v8::internal::FullMaybeObjectSlot, v8::internal::SnapshotSpace, unsigned long)+0x1b7) [0x7ffff5e2f717]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::Deserializer::ReadObject(v8::internal::SnapshotSpace)+0xca) [0x7ffff5e2e5ba]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::FullMaybeObjectSlot v8::internal::Deserializer::ReadDataCase<v8::internal::FullMaybeObjectSlot, (v8::internal::SerializerDeserializer::Bytecode)0, (v8::internal::SnapshotSpace)6>(v8::internal::Isolate*, v8::internal::FullMaybeObjectSlot, unsigned long, unsigned char, bool)+0x82) [0x7ffff5e34872]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(bool v8::internal::Deserializer::ReadData<v8::internal::FullMaybeObjectSlot>(v8::internal::FullMaybeObjectSlot, v8::internal::FullMaybeObjectSlot, v8::internal::SnapshotSpace, unsigned long)+0x1b7) [0x7ffff5e2f717]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::Deserializer::ReadObject(v8::internal::SnapshotSpace)+0xca) [0x7ffff5e2e5ba]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::FullMaybeObjectSlot v8::internal::Deserializer::ReadDataCase<v8::internal::FullMaybeObjectSlot, (v8::internal::SerializerDeserializer::Bytecode)0, (v8::internal::SnapshotSpace)6>(v8::internal::Isolate*, v8::internal::FullMaybeObjectSlot, unsigned long, unsigned char, bool)+0x82) [0x7ffff5e34872]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(bool v8::internal::Deserializer::ReadData<v8::internal::FullMaybeObjectSlot>(v8::internal::FullMaybeObjectSlot, v8::internal::FullMaybeObjectSlot, v8::internal::SnapshotSpace, unsigned long)+0x1b7) [0x7ffff5e2f717]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::Deserializer::ReadObject(v8::internal::SnapshotSpace)+0xca) [0x7ffff5e2e5ba]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::FullMaybeObjectSlot v8::internal::Deserializer::ReadDataCase<v8::internal::FullMaybeObjectSlot, (v8::internal::SerializerDeserializer::Bytecode)0, (v8::internal::SnapshotSpace)6>(v8::internal::Isolate*, v8::internal::FullMaybeObjectSlot, unsigned long, unsigned char, bool)+0x82) [0x7ffff5e34872]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(bool v8::internal::Deserializer::ReadData<v8::internal::FullMaybeObjectSlot>(v8::internal::FullMaybeObjectSlot, v8::internal::FullMaybeObjectSlot, v8::internal::SnapshotSpace, unsigned long)+0x1b7) [0x7ffff5e2f717]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::Deserializer::ReadObject(v8::internal::SnapshotSpace)+0xca) [0x7ffff5e2e5ba]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::FullMaybeObjectSlot v8::internal::Deserializer::ReadDataCase<v8::internal::FullMaybeObjectSlot, (v8::internal::SerializerDeserializer::Bytecode)0, (v8::internal::SnapshotSpace)6>(v8::internal::Isolate*, v8::internal::FullMaybeObjectSlot, unsigned long, unsigned char, bool)+0x82) [0x7ffff5e34872]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(bool v8::internal::Deserializer::ReadData<v8::internal::FullMaybeObjectSlot>(v8::internal::FullMaybeObjectSlot, v8::internal::FullMaybeObjectSlot, v8::internal::SnapshotSpace, unsigned long)+0x1b7) [0x7ffff5e2f717]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::Deserializer::VisitRootPointers(v8::internal::Root, char const*, v8::internal::FullObjectSlot, v8::internal::FullObjectSlot)+0x6c) [0x7ffff5e2c71c]
    /hdd2/v8/v8/out/x64.debug/cctest(v8::internal::RootVisitor::VisitRootPointer(v8::internal::Root, char const*, v8::internal::FullObjectSlot)+0x76) [0x5555568c6af6]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::PartialDeserializer::Deserialize(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSGlobalProxy>, v8::DeserializeInternalFieldsCallback)+0x106) [0x7ffff5e3db66]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::PartialDeserializer::DeserializeContext(v8::internal::Isolate*, v8::internal::SnapshotData const*, bool, v8::internal::Handle<v8::internal::JSGlobalProxy>, v8::DeserializeInternalFieldsCallback)+0xc4) [0x7ffff5e3d974]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::Snapshot::NewContextFromSnapshot(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSGlobalProxy>, unsigned long, v8::DeserializeInternalFieldsCallback)+0x155) [0x7ffff5e542c5]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::Genesis::Genesis(v8::internal::Isolate*, v8::internal::MaybeHandle<v8::internal::JSGlobalProxy>, v8::Local<v8::ObjectTemplate>, unsigned long, v8::DeserializeInternalFieldsCallback, v8::MicrotaskQueue*)+0x30e) [0x7ffff586fa1e]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::internal::Bootstrapper::CreateEnvironment(v8::internal::MaybeHandle<v8::internal::JSGlobalProxy>, v8::Local<v8::ObjectTemplate>, v8::ExtensionConfiguration*, unsigned long, v8::DeserializeInternalFieldsCallback, v8::MicrotaskQueue*)+0xc3) [0x7ffff5848fc3]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::InvokeBootstrapper<v8::internal::Context>::Invoke(v8::internal::Isolate*, v8::internal::MaybeHandle<v8::internal::JSGlobalProxy>, v8::Local<v8::ObjectTemplate>, v8::ExtensionConfiguration*, unsigned long, v8::DeserializeInternalFieldsCallback, v8::MicrotaskQueue*)+0x8f) [0x7ffff53518cf]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(+0x26944d4) [0x7ffff52ef4d4]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::NewContext(v8::Isolate*, v8::ExtensionConfiguration*, v8::MaybeLocal<v8::ObjectTemplate>, v8::MaybeLocal<v8::Value>, unsigned long, v8::DeserializeInternalFieldsCallback, v8::MicrotaskQueue*)+0x20b) [0x7ffff52eecfb]
    /hdd2/v8/v8/out/x64.debug/libv8_for_testing.so(v8::Context::New(v8::Isolate*, v8::ExtensionConfiguration*, v8::MaybeLocal<v8::ObjectTemplate>, v8::MaybeLocal<v8::Value>, v8::DeserializeInternalFieldsCallback, v8::MicrotaskQueue*)+0x7f) [0x7ffff52ef77f]
    /hdd2/v8/v8/out/x64.debug/cctest(v8::internal::TypedArrayTestHelper(char const*, std::__Cr::vector<std::__Cr::tuple<char const*, int>, std::__Cr::allocator<std::__Cr::tuple<char const*, int> > > const&, char const*, std::__Cr::vector<std::__Cr::tuple<char const*, int>, std::__Cr::allocator<std::__Cr::tuple<char const*, int> > > const&)+0x2b5) [0x555556d5a765]
    /hdd2/v8/v8/out/x64.debug/cctest(+0x1806a05) [0x555556d5aa05]
    /hdd2/v8/v8/out/x64.debug/cctest(CcTest::Run()+0x1b8) [0x5555566b99f8]
    /hdd2/v8/v8/out/x64.debug/cctest(main+0x3ec) [0x5555566baaec]
    /lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0xe7) [0x7ffff2144b97]
    /hdd2/v8/v8/out/x64.debug/cctest(_start+0x2a) [0x5555566b962a]

Thread 1 "cctest" received signal SIGILL, Illegal instruction.
v8::base::OS::Abort () at ../../src/base/platform/platform-posix.cc:407
407	    V8_IMMEDIATE_CRASH();
(gdb) bt
#0  v8::base::OS::Abort () at ../../src/base/platform/platform-posix.cc:407
#1  0x00007ffff7fd7324 in V8_Fatal (file=0x7ffff4470024 "../../src/heap/heap.cc", line=1527, format=0x7ffff7fbb245 "Debug check failed: %s.") at ../../src/base/logging.cc:182
#2  0x00007ffff7fd6d7c in v8::base::(anonymous namespace)::DefaultDcheckHandler (file=0x7ffff4470024 "../../src/heap/heap.cc", line=1527, 
    message=0x7ffff443108b "AllowHeapAllocation::IsAllowed()") at ../../src/base/logging.cc:57
#3  0x00007ffff7fd73d7 in V8_Dcheck (file=0x7ffff4470024 "../../src/heap/heap.cc", line=1527, message=0x7ffff443108b "AllowHeapAllocation::IsAllowed()")
    at ../../src/base/logging.cc:195
#4  0x00007ffff56f1d3f in v8::internal::Heap::CollectGarbage (this=0x5555578eade8, space=v8::internal::OLD_SPACE, 
    gc_reason=v8::internal::GarbageCollectionReason::kExternalMemoryPressure, 
    gc_callback_flags=(v8::kGCCallbackFlagSynchronousPhantomCallbackProcessing | v8::kGCCallbackFlagCollectAllAvailableGarbage | v8::kGCCallbackFlagCollectAllExternalMemory))
    at ../../src/heap/heap.cc:1527
#5  0x00007ffff56f0f7c in v8::internal::Heap::CollectAllGarbage (this=0x5555578eade8, flags=1, gc_reason=v8::internal::GarbageCollectionReason::kExternalMemoryPressure, 
    gc_callback_flags=(v8::kGCCallbackFlagSynchronousPhantomCallbackProcessing | v8::kGCCallbackFlagCollectAllAvailableGarbage | v8::kGCCallbackFlagCollectAllExternalMemory))
    at ../../src/heap/heap.cc:1284
#6  0x00007ffff56f2c81 in v8::internal::Heap::ReportExternalMemoryPressure (this=0x5555578eade8) at ../../src/heap/heap.cc:1431
#7  0x00007ffff5300bec in v8::Isolate::ReportExternalAllocationLimitReached (this=0x5555578e1a80) at ../../src/api/api.cc:7905
#8  0x00005555568cb9aa in v8::Isolate::AdjustAmountOfExternalAllocatedMemory (this=0x5555578e1a80, change_in_bytes=1073741823) at ../../include/v8.h:11457
#9  0x00007ffff570e6ad in v8::internal::ArrayBufferTracker::RegisterNew (heap=0x5555578eade8, buffer=..., backing_store=...) at ../../src/heap/array-buffer-tracker-inl.h:60
#10 0x00007ffff56f9695 in v8::internal::Heap::RegisterBackingStore (this=0x5555578eade8, buffer=..., backing_store=...) at ../../src/heap/heap.cc:2780
#11 0x00007ffff5a57231 in v8::internal::JSArrayBuffer::Attach (this=0x7fffffffab88, backing_store=...) at ../../src/objects/js-array-buffer.cc:61
#12 0x00007ffff5a57042 in v8::internal::JSArrayBuffer::Setup (this=0x7fffffffab88, shared=v8::internal::SharedFlag::kNotShared, backing_store=...)
    at ../../src/objects/js-array-buffer.cc:50
#13 0x00007ffff5e2d811 in v8::internal::Deserializer::PostProcessNewObject (this=0x7fffffffc990, obj=..., space=v8::internal::SnapshotSpace::kOld)
    at ../../src/snapshot/deserializer.cc:317
#14 0x00007ffff5e2e5df in v8::internal::Deserializer::ReadObject (this=0x7fffffffc990, space=v8::internal::SnapshotSpace::kOld) at ../../src/snapshot/deserializer.cc:403
#15 0x00007ffff5e34872 in v8::internal::Deserializer::ReadDataCase<v8::internal::FullMaybeObjectSlot, (v8::internal::SerializerDeserializer::Bytecode)0, (v8::internal::SnapshotSpace)6> (this=0x7fffffffc990, isolate=0x5555578e1a80, current=..., current_object_address=13712913891208, data=2 '\002', write_barrier_needed=true)
    at ../../src/snapshot/deserializer.cc:818
#16 0x00007ffff5e2f717 in v8::internal::Deserializer::ReadData<v8::internal::FullMaybeObjectSlot> (this=0x7fffffffc990, current=..., limit=..., 
    source_space=v8::internal::SnapshotSpace::kOld, current_object_address=13712913891208) at ../../src/snapshot/deserializer.cc:584
#17 0x00007ffff5e2e5ba in v8::internal::Deserializer::ReadObject (this=0x7fffffffc990, space=v8::internal::SnapshotSpace::kOld) at ../../src/snapshot/deserializer.cc:401
#18 0x00007ffff5e34872 in v8::internal::Deserializer::ReadDataCase<v8::internal::FullMaybeObjectSlot, (v8::internal::SerializerDeserializer::Bytecode)0, (v8::internal::SnapshotSpace)6> (this=0x7fffffffc990, isolate=0x5555578e1a80, current=..., current_object_address=13712913891168, data=2 '\002', write_barrier_needed=true)
    at ../../src/snapshot/deserializer.cc:818
#19 0x00007ffff5e2f717 in v8::internal::Deserializer::ReadData<v8::internal::FullMaybeObjectSlot> (this=0x7fffffffc990, current=..., limit=..., 
    source_space=v8::internal::SnapshotSpace::kOld, current_object_address=13712913891168) at ../../src/snapshot/deserializer.cc:584
#20 0x00007ffff5e2e5ba in v8::internal::Deserializer::ReadObject (this=0x7fffffffc990, space=v8::internal::SnapshotSpace::kOld) at ../../src/snapshot/deserializer.cc:401
#21 0x00007ffff5e34872 in v8::internal::Deserializer::ReadDataCase<v8::internal::FullMaybeObjectSlot, (v8::internal::SerializerDeserializer::Bytecode)0, (v8::internal::SnapshotSpace)6> (this=0x7fffffffc990, isolate=0x5555578e1a80, current=..., current_object_address=13712913865888, data=2 '\002', write_barrier_needed=true)
    at ../../src/snapshot/deserializer.cc:818
#22 0x00007ffff5e2f717 in v8::internal::Deserializer::ReadData<v8::internal::FullMaybeObjectSlot> (this=0x7fffffffc990, current=..., limit=..., 
    source_space=v8::internal::SnapshotSpace::kOld, current_object_address=13712913865888) at ../../src/snapshot/deserializer.cc:584
#23 0x00007ffff5e2e5ba in v8::internal::Deserializer::ReadObject (this=0x7fffffffc990, space=v8::internal::SnapshotSpace::kOld) at ../../src/snapshot/deserializer.cc:401
#24 0x00007ffff5e34872 in v8::internal::Deserializer::ReadDataCase<v8::internal::FullMaybeObjectSlot, (v8::internal::SerializerDeserializer::Bytecode)0, (v8::internal::SnapshotSpace)6> (this=0x7fffffffc990, isolate=0x5555578e1a80, current=..., current_object_address=13712913860896, data=2 '\002', write_barrier_needed=true)
    at ../../src/snapshot/deserializer.cc:818
#25 0x00007ffff5e2f717 in v8::internal::Deserializer::ReadData<v8::internal::FullMaybeObjectSlot> (this=0x7fffffffc990, current=..., limit=..., 
    source_space=v8::internal::SnapshotSpace::kOld, current_object_address=13712913860896) at ../../src/snapshot/deserializer.cc:584
#26 0x00007ffff5e2e5ba in v8::internal::Deserializer::ReadObject (this=0x7fffffffc990, space=v8::internal::SnapshotSpace::kOld) at ../../src/snapshot/deserializer.cc:401
#27 0x00007ffff5e34872 in v8::internal::Deserializer::ReadDataCase<v8::internal::FullMaybeObjectSlot, (v8::internal::SerializerDeserializer::Bytecode)0, (v8::internal::SnapshotSpace)6> (this=0x7fffffffc990, isolate=0x5555578e1a80, current=..., current_object_address=13712913858848, data=2 '\002', write_barrier_needed=true)
    at ../../src/snapshot/deserializer.cc:818
#28 0x00007ffff5e2f717 in v8::internal::Deserializer::ReadData<v8::internal::FullMaybeObjectSlot> (this=0x7fffffffc990, current=..., limit=..., 
    source_space=v8::internal::SnapshotSpace::kOld, current_object_address=13712913858848) at ../../src/snapshot/deserializer.cc:584
#29 0x00007ffff5e2e5ba in v8::internal::Deserializer::ReadObject (this=0x7fffffffc990, space=v8::internal::SnapshotSpace::kOld) at ../../src/snapshot/deserializer.cc:401
#30 0x00007ffff5e34872 in v8::internal::Deserializer::ReadDataCase<v8::internal::FullMaybeObjectSlot, (v8::internal::SerializerDeserializer::Bytecode)0, (v8::internal::SnapshotSpace)6> (this=0x7fffffffc990, isolate=0x5555578e1a80, current=..., current_object_address=0, data=2 '\002', write_barrier_needed=false) at ../../src/snapshot/deserializer.cc:818
---Type <return> to continue, or q <return> to quit---
#31 0x00007ffff5e2f717 in v8::internal::Deserializer::ReadData<v8::internal::FullMaybeObjectSlot> (this=0x7fffffffc990, current=..., limit=..., 
    source_space=v8::internal::SnapshotSpace::kNew, current_object_address=0) at ../../src/snapshot/deserializer.cc:584
#32 0x00007ffff5e2c71c in v8::internal::Deserializer::VisitRootPointers (this=0x7fffffffc990, root=v8::internal::Root::kPartialSnapshotCache, description=0x0, start=..., end=...)
    at ../../src/snapshot/deserializer.cc:95
#33 0x00005555568c6af6 in v8::internal::RootVisitor::VisitRootPointer (this=0x7fffffffc990, root=v8::internal::Root::kPartialSnapshotCache, description=0x0, p=...)
    at ../../src/objects/visitors.h:73
#34 0x00007ffff5e3db66 in v8::internal::PartialDeserializer::Deserialize (this=0x7fffffffc990, isolate=0x5555578e1a80, global_proxy=..., embedder_fields_deserializer=...)
    at ../../src/snapshot/partial-deserializer.cc:46
#35 0x00007ffff5e3d974 in v8::internal::PartialDeserializer::DeserializeContext (isolate=0x5555578e1a80, data=0x7fffffffcc90, can_rehash=true, global_proxy=..., 
    embedder_fields_deserializer=...) at ../../src/snapshot/partial-deserializer.cc:23
#36 0x00007ffff5e542c5 in v8::internal::Snapshot::NewContextFromSnapshot (isolate=0x5555578e1a80, global_proxy=..., context_index=0, embedder_fields_deserializer=...)
    at ../../src/snapshot/snapshot-common.cc:78
#37 0x00007ffff586fa1e in v8::internal::Genesis::Genesis (this=0x7fffffffd108, isolate=0x5555578e1a80, maybe_global_proxy=..., global_proxy_template=..., context_snapshot_index=0, 
    embedder_fields_deserializer=..., microtask_queue=0x0) at ../../src/init/bootstrapper.cc:5493
#38 0x00007ffff5848fc3 in v8::internal::Bootstrapper::CreateEnvironment (this=0x555557923680, maybe_global_proxy=..., global_proxy_template=..., extensions=0x7fffffffd5d0, 
    context_snapshot_index=0, embedder_fields_deserializer=..., microtask_queue=0x0) at ../../src/init/bootstrapper.cc:323
#39 0x00007ffff53518cf in v8::InvokeBootstrapper<v8::internal::Context>::Invoke (this=0x7fffffffd358, isolate=0x5555578e1a80, maybe_global_proxy=..., global_proxy_template=..., 
    extensions=0x7fffffffd5d0, context_snapshot_index=0, embedder_fields_deserializer=..., microtask_queue=0x0) at ../../src/api/api.cc:5738
#40 0x00007ffff52ef4d4 in v8::CreateEnvironment<v8::internal::Context> (isolate=0x5555578e1a80, extensions=0x7fffffffd5d0, maybe_global_template=..., maybe_global_proxy=..., 
    context_snapshot_index=0, embedder_fields_deserializer=..., microtask_queue=0x0) at ../../src/api/api.cc:5840
#41 0x00007ffff52eecfb in v8::NewContext (external_isolate=0x5555578e1a80, extensions=0x7fffffffd5d0, global_template=..., global_object=..., context_snapshot_index=0, 
    embedder_fields_deserializer=..., microtask_queue=0x0) at ../../src/api/api.cc:5881
#42 0x00007ffff52ef77f in v8::Context::New (external_isolate=0x5555578e1a80, extensions=0x0, global_template=..., global_object=..., internal_fields_deserializer=..., 
    microtask_queue=0x0) at ../../src/api/api.cc:5897
#43 0x0000555556d5a765 in v8::internal::TypedArrayTestHelper (code=0x555556348514 "var x = new Int8Array(0x3fffffff);", expectations=..., code_to_run_after_restore=0x0, 
    after_restore_expectations=...) at ../../test/cctest/test-serialize.cc:923
#44 0x0000555556d5aa05 in v8::internal::TestCustomSnapshotBigArrayBuffer () at ../../test/cctest/test-serialize.cc:989
#45 0x00005555566b99f8 in CcTest::Run (this=0x555557851d58 <v8::internal::register_test_CustomSnapshotBigArrayBuffer>) at ../../test/cctest/cctest.cc:108
#46 0x00005555566baaec in main (argc=2, argv=0x7fffffffdc18) at ../../test/cctest/cctest.cc:357


if you build a release version cctest, the crash stack is as follow:
Starting program: /hdd2/v8/v8/out/x64.release/cctest test-serialize/CustomSnapshotBigArrayBuffer
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
[New Thread 0x7ffff6614700 (LWP 12317)]
[New Thread 0x7ffff5e13700 (LWP 12318)]
[New Thread 0x7ffff5612700 (LWP 12319)]
[New Thread 0x7ffff4e11700 (LWP 12320)]
[New Thread 0x7ffff4610700 (LWP 12321)]
[New Thread 0x7ffff3e0f700 (LWP 12322)]
[New Thread 0x7ffff360e700 (LWP 12323)]

Thread 1 "cctest" received signal SIGSEGV, Segmentation fault.
0x00005555575971b0 in v8::internal::JSObject::OptimizeAsPrototype(v8::internal::Handle<v8::internal::JSObject>, bool) ()
(gdb) bt
#0  0x00005555575971b0 in v8::internal::JSObject::OptimizeAsPrototype(v8::internal::Handle<v8::internal::JSObject>, bool) ()
#1  0x00005555575b4340 in v8::internal::Map::SetPrototype(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Map>, v8::internal::Handle<v8::internal::HeapObject>, bool) ()
#2  0x0000555557598e95 in v8::internal::JSFunction::SetInitialMap(v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Map>, v8::internal::Handle<v8::internal::HeapObject>) ()
#3  0x00005555573d1425 in v8::internal::Factory::NewFunction(v8::internal::NewFunctionArgs const&) ()
#4  0x00005555574984db in v8::internal::Genesis::CreateNewGlobals(v8::Local<v8::ObjectTemplate>, v8::internal::Handle<v8::internal::JSGlobalProxy>) ()
#5  0x00005555574abd17 in v8::internal::Genesis::Genesis(v8::internal::Isolate*, v8::internal::MaybeHandle<v8::internal::JSGlobalProxy>, v8::Local<v8::ObjectTemplate>, unsigned long, v8::DeserializeInternalFieldsCallback, v8::MicrotaskQueue*) ()
#6  0x0000555557494970 in v8::internal::Bootstrapper::CreateEnvironment(v8::internal::MaybeHandle<v8::internal::JSGlobalProxy>, v8::Local<v8::ObjectTemplate>, v8::ExtensionConfiguration*, unsigned long, v8::DeserializeInternalFieldsCallback, v8::MicrotaskQueue*) ()
#7  0x00005555572784cc in v8::NewContext(v8::Isolate*, v8::ExtensionConfiguration*, v8::MaybeLocal<v8::ObjectTemplate>, v8::MaybeLocal<v8::Value>, unsigned long, v8::DeserializeInternalFieldsCallback, v8::MicrotaskQueue*) ()
#8  0x0000555557278937 in v8::Context::New(v8::Isolate*, v8::ExtensionConfiguration*, v8::MaybeLocal<v8::ObjectTemplate>, v8::MaybeLocal<v8::Value>, v8::DeserializeInternalFieldsCallback, v8::MicrotaskQueue*) ()
#9  0x0000555557011964 in v8::internal::TypedArrayTestHelper(char const*, std::__1::vector<std::__1::tuple<char const*, int>, std::__1::allocator<std::__1::tuple<char const*, int> > > const&, char const*, std::__1::vector<std::__1::tuple<char const*, int>, std::__1::allocator<std::__1::tuple<char const*, int> > > const&) ()
#10 0x0000555557011c39 in v8::internal::TestCustomSnapshotBigArrayBuffer() ()
#11 0x0000555556c1d21c in CcTest::Run() ()
#12 0x0000555556c1e0ca in main ()

I reproduced this bug on v8 version 7.9.317.31, the master branch should be vulnerable too.

## Timeline

### hi...@gmail.com (2019-12-12)

correct a mistake, the wrong assumption is in the function Deserializer::ReadObject not in Deserializer::PostProcessNewObject
https://cs.chromium.org/chromium/src/v8/src/snapshot/deserializer.cc?rcl=5a2f2203c80defe0adc943a2c15ff51da7b24196&l=379
HeapObject Deserializer::ReadObject(SnapshotSpace space) {
  DisallowHeapAllocation no_gc;  -------------------------------->wrong assumption

  const int size = source_.GetInt() << kObjectAlignmentBits;

  Address address = allocator()->Allocate(space, size);
  HeapObject obj = HeapObject::FromAddress(address);

  isolate_->heap()->OnAllocationEvent(obj, size);
  MaybeObjectSlot current(address);
  MaybeObjectSlot limit(address + size);

  if (ReadData(current, limit, space, address)) {
    // Only post process if object content has not been deferred.
    obj = PostProcessNewObject(obj, space);   ------------------------------------> PostProcessNewObject may call gc
  }

#ifdef DEBUG
  if (obj.IsCode()) {
    DCHECK(space == SnapshotSpace::kCode ||
           space == SnapshotSpace::kReadOnlyHeap);
  } else {
    DCHECK_NE(space, SnapshotSpace::kCode);
  }
#endif  // DEBUG
  return obj;
}

### oc...@google.com (2019-12-13)

mslekova, could you please help take a look, since you recently touched code here?

Assuming high severity, but please adjust if necessary.

[Monorail components: Blink>JavaScript]

### ya...@chromium.org (2019-12-13)

Good news is that Chrome is not affected. The deserializer is deterministic for the snapshot that is shipped with Chrome, which does not include any JSArrayBuffer.

### ya...@chromium.org (2019-12-13)

[Empty comment from Monorail migration]

### ya...@chromium.org (2019-12-13)

Fix here: https://chromium-review.googlesource.com/c/v8/v8/+/1965580/

### hi...@gmail.com (2019-12-13)

reply to #https://crbug.com/chromium/1033395#c3
It seems code cache use the deserializer too, 
we should note this call path ScriptCompiler::CompileUnboundInternal---->Compiler::GetSharedFunctionInfoForScript---->CodeSerializer::Deserialize--->ObjectDeserializer::DeserializeSharedFunctionInfo---->ObjectDeserializer::Deserialize---->Deserializer::DeserializeDeferredObjects---->Deserializer::PostProcessNewObject

### ul...@chromium.org (2019-12-13)

Adjusting security labels according to https://crbug.com/chromium/1033395#c3

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/83786cb49d1e74470b0d910da19ccd13bb6b2047

commit 83786cb49d1e74470b0d910da19ccd13bb6b2047
Author: Yang Guo <yangguo@chromium.org>
Date: Fri Dec 13 10:57:44 2019

Delay setting up deserialized JSArrayBuffer

Setting up JSArrayBuffer may trigger GC. Delay this until we
are done with deserialization.

R=ulan@chromium.org

Bug: chromium:1033395
Change-Id: I6c79bc47421bc2662dc1906534fc8e820c351ced
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1965580
Reviewed-by: Ulan Degenbaev <ulan@chromium.org>
Commit-Queue: Yang Guo <yangguo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#65441}

[modify] https://crrev.com/83786cb49d1e74470b0d910da19ccd13bb6b2047/include/v8.h
[modify] https://crrev.com/83786cb49d1e74470b0d910da19ccd13bb6b2047/src/api/api.cc
[modify] https://crrev.com/83786cb49d1e74470b0d910da19ccd13bb6b2047/src/snapshot/deserializer.cc
[modify] https://crrev.com/83786cb49d1e74470b0d910da19ccd13bb6b2047/src/snapshot/deserializer.h
[modify] https://crrev.com/83786cb49d1e74470b0d910da19ccd13bb6b2047/src/snapshot/object-deserializer.cc
[modify] https://crrev.com/83786cb49d1e74470b0d910da19ccd13bb6b2047/src/snapshot/partial-deserializer.cc
[modify] https://crrev.com/83786cb49d1e74470b0d910da19ccd13bb6b2047/src/snapshot/partial-deserializer.h
[modify] https://crrev.com/83786cb49d1e74470b0d910da19ccd13bb6b2047/src/snapshot/read-only-deserializer.cc
[modify] https://crrev.com/83786cb49d1e74470b0d910da19ccd13bb6b2047/src/snapshot/startup-deserializer.cc


### ya...@chromium.org (2019-12-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-13)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/d1aaf9dadcc54439a3e42404e78006f27ff6f89f

commit d1aaf9dadcc54439a3e42404e78006f27ff6f89f
Author: Michael Achenbach <machenbach@chromium.org>
Date: Fri Dec 13 18:44:52 2019

Revert "Delay setting up deserialized JSArrayBuffer"

This reverts commit 83786cb49d1e74470b0d910da19ccd13bb6b2047.

Reason for revert:
https://ci.chromium.org/p/v8/builders/ci/V8%20Blink%20Linux%20Debug/2037

Original change's description:
> Delay setting up deserialized JSArrayBuffer
> 
> Setting up JSArrayBuffer may trigger GC. Delay this until we
> are done with deserialization.
> 
> R=​ulan@chromium.org
> 
> Bug: chromium:1033395
> Change-Id: I6c79bc47421bc2662dc1906534fc8e820c351ced
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1965580
> Reviewed-by: Ulan Degenbaev <ulan@chromium.org>
> Commit-Queue: Yang Guo <yangguo@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#65441}

TBR=ulan@chromium.org,yangguo@chromium.org,petermarshall@chromium.org

Change-Id: I77b8ae836e9003eaaccef440dfaf3ae840c112cb
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:1033395
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1967327
Reviewed-by: Michael Achenbach <machenbach@chromium.org>
Commit-Queue: Michael Achenbach <machenbach@chromium.org>
Cr-Commit-Position: refs/heads/master@{#65450}

[modify] https://crrev.com/d1aaf9dadcc54439a3e42404e78006f27ff6f89f/include/v8.h
[modify] https://crrev.com/d1aaf9dadcc54439a3e42404e78006f27ff6f89f/src/api/api.cc
[modify] https://crrev.com/d1aaf9dadcc54439a3e42404e78006f27ff6f89f/src/snapshot/deserializer.cc
[modify] https://crrev.com/d1aaf9dadcc54439a3e42404e78006f27ff6f89f/src/snapshot/deserializer.h
[modify] https://crrev.com/d1aaf9dadcc54439a3e42404e78006f27ff6f89f/src/snapshot/object-deserializer.cc
[modify] https://crrev.com/d1aaf9dadcc54439a3e42404e78006f27ff6f89f/src/snapshot/partial-deserializer.cc
[modify] https://crrev.com/d1aaf9dadcc54439a3e42404e78006f27ff6f89f/src/snapshot/partial-deserializer.h
[modify] https://crrev.com/d1aaf9dadcc54439a3e42404e78006f27ff6f89f/src/snapshot/read-only-deserializer.cc
[modify] https://crrev.com/d1aaf9dadcc54439a3e42404e78006f27ff6f89f/src/snapshot/startup-deserializer.cc


### ya...@chromium.org (2019-12-13)

Looks like the assertion I added uncovered many more issues. Ulan, please own this!

### sh...@chromium.org (2019-12-14)

[Empty comment from Monorail migration]

### ma...@chromium.org (2019-12-16)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/ff7acbd6971d8d918e874a4f2c774a3175f7e178

commit ff7acbd6971d8d918e874a4f2c774a3175f7e178
Author: Ulan Degenbaev <ulan@chromium.org>
Date: Tue Dec 17 17:09:46 2019

Reland "Delay setting up deserialized JSArrayBuffer"

This is a reland of 83786cb49d1e74470b0d910da19ccd13bb6b2047

Original change's description:
> Delay setting up deserialized JSArrayBuffer
>
> Setting up JSArrayBuffer may trigger GC. Delay this until we
> are done with deserialization.
>
> R=ulan@chromium.org
>
> Bug: chromium:1033395
> Change-Id: I6c79bc47421bc2662dc1906534fc8e820c351ced
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1965580
> Reviewed-by: Ulan Degenbaev <ulan@chromium.org>
> Commit-Queue: Yang Guo <yangguo@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#65441}

Tbr: yangguo@chromium.org
Bug: chromium:1033395, chromium:1034059
Change-Id: I89d05768f52a480400d9c6f5aaaa233c5d5ba126
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1969896
Commit-Queue: Ulan Degenbaev <ulan@chromium.org>
Reviewed-by: Ulan Degenbaev <ulan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#65484}

[modify] https://crrev.com/ff7acbd6971d8d918e874a4f2c774a3175f7e178/src/api/api.cc
[modify] https://crrev.com/ff7acbd6971d8d918e874a4f2c774a3175f7e178/src/snapshot/deserializer.cc
[modify] https://crrev.com/ff7acbd6971d8d918e874a4f2c774a3175f7e178/src/snapshot/deserializer.h
[modify] https://crrev.com/ff7acbd6971d8d918e874a4f2c774a3175f7e178/src/snapshot/object-deserializer.cc
[modify] https://crrev.com/ff7acbd6971d8d918e874a4f2c774a3175f7e178/src/snapshot/partial-deserializer.cc
[modify] https://crrev.com/ff7acbd6971d8d918e874a4f2c774a3175f7e178/src/snapshot/partial-deserializer.h
[modify] https://crrev.com/ff7acbd6971d8d918e874a4f2c774a3175f7e178/src/snapshot/read-only-deserializer.cc
[modify] https://crrev.com/ff7acbd6971d8d918e874a4f2c774a3175f7e178/src/snapshot/startup-deserializer.cc


### ul...@chromium.org (2019-12-17)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-18)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/131ba0a0d40f19e4e2666741e3f358109fbacfab

commit 131ba0a0d40f19e4e2666741e3f358109fbacfab
Author: Nico Hartmann <nicohartmann@chromium.org>
Date: Thu Dec 19 10:30:00 2019

Revert "Reland "Delay setting up deserialized JSArrayBuffer""

This reverts commit ff7acbd6971d8d918e874a4f2c774a3175f7e178.

Reason for revert: https://ci.chromium.org/p/chromium/builders/try/win_optional_gpu_tests_rel/34257

Original change's description:
> Reland "Delay setting up deserialized JSArrayBuffer"
> 
> This is a reland of 83786cb49d1e74470b0d910da19ccd13bb6b2047
> 
> Original change's description:
> > Delay setting up deserialized JSArrayBuffer
> >
> > Setting up JSArrayBuffer may trigger GC. Delay this until we
> > are done with deserialization.
> >
> > R=ulan@chromium.org
> >
> > Bug: chromium:1033395
> > Change-Id: I6c79bc47421bc2662dc1906534fc8e820c351ced
> > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1965580
> > Reviewed-by: Ulan Degenbaev <ulan@chromium.org>
> > Commit-Queue: Yang Guo <yangguo@chromium.org>
> > Cr-Commit-Position: refs/heads/master@{#65441}
> 
> Tbr: yangguo@chromium.org
> Bug: chromium:1033395, chromium:1034059
> Change-Id: I89d05768f52a480400d9c6f5aaaa233c5d5ba126
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1969896
> Commit-Queue: Ulan Degenbaev <ulan@chromium.org>
> Reviewed-by: Ulan Degenbaev <ulan@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#65484}

TBR=ulan@chromium.org,yangguo@chromium.org,petermarshall@chromium.org

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: chromium:1033395, chromium:1034059
Change-Id: I3ad17293bfeba8a817346f57f885c7ba95739d36
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1975751
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/heads/master@{#65516}

[modify] https://crrev.com/131ba0a0d40f19e4e2666741e3f358109fbacfab/src/api/api.cc
[modify] https://crrev.com/131ba0a0d40f19e4e2666741e3f358109fbacfab/src/snapshot/deserializer.cc
[modify] https://crrev.com/131ba0a0d40f19e4e2666741e3f358109fbacfab/src/snapshot/deserializer.h
[modify] https://crrev.com/131ba0a0d40f19e4e2666741e3f358109fbacfab/src/snapshot/object-deserializer.cc
[modify] https://crrev.com/131ba0a0d40f19e4e2666741e3f358109fbacfab/src/snapshot/partial-deserializer.cc
[modify] https://crrev.com/131ba0a0d40f19e4e2666741e3f358109fbacfab/src/snapshot/partial-deserializer.h
[modify] https://crrev.com/131ba0a0d40f19e4e2666741e3f358109fbacfab/src/snapshot/read-only-deserializer.cc
[modify] https://crrev.com/131ba0a0d40f19e4e2666741e3f358109fbacfab/src/snapshot/startup-deserializer.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/7edaa330a17fc9ae61061295e1e757cb3521a8f4

commit 7edaa330a17fc9ae61061295e1e757cb3521a8f4
Author: Ulan Degenbaev <ulan@chromium.org>
Date: Thu Dec 19 13:01:46 2019

Reland "Reland "Delay setting up deserialized JSArrayBuffer""

This is a reland of ff7acbd6971d8d918e874a4f2c774a3175f7e178

Original change's description:
> Reland "Delay setting up deserialized JSArrayBuffer"
>
> This is a reland of 83786cb49d1e74470b0d910da19ccd13bb6b2047
>
> Original change's description:
> > Delay setting up deserialized JSArrayBuffer
> >
> > Setting up JSArrayBuffer may trigger GC. Delay this until we
> > are done with deserialization.
> >
> > R=ulan@chromium.org
> >
> > Bug: chromium:1033395
> > Change-Id: I6c79bc47421bc2662dc1906534fc8e820c351ced
> > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1965580
> > Reviewed-by: Ulan Degenbaev <ulan@chromium.org>
> > Commit-Queue: Yang Guo <yangguo@chromium.org>
> > Cr-Commit-Position: refs/heads/master@{#65441}
>
> Tbr: yangguo@chromium.org
> Bug: chromium:1033395, chromium:1034059
> Change-Id: I89d05768f52a480400d9c6f5aaaa233c5d5ba126
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1969896
> Commit-Queue: Ulan Degenbaev <ulan@chromium.org>
> Reviewed-by: Ulan Degenbaev <ulan@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#65484}

Tbr: yangguo@chromium.org
Bug: chromium:1033395, chromium:1034059
Change-Id: I1cc47fa742bd7c5ce602b1eb9a0a78cb479a86f1
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1975756
Reviewed-by: Ulan Degenbaev <ulan@chromium.org>
Commit-Queue: Ulan Degenbaev <ulan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#65522}

[modify] https://crrev.com/7edaa330a17fc9ae61061295e1e757cb3521a8f4/src/snapshot/deserializer.cc
[modify] https://crrev.com/7edaa330a17fc9ae61061295e1e757cb3521a8f4/src/snapshot/deserializer.h
[modify] https://crrev.com/7edaa330a17fc9ae61061295e1e757cb3521a8f4/src/snapshot/object-deserializer.cc
[modify] https://crrev.com/7edaa330a17fc9ae61061295e1e757cb3521a8f4/src/snapshot/partial-deserializer.cc
[modify] https://crrev.com/7edaa330a17fc9ae61061295e1e757cb3521a8f4/src/snapshot/partial-deserializer.h
[modify] https://crrev.com/7edaa330a17fc9ae61061295e1e757cb3521a8f4/src/snapshot/read-only-deserializer.cc
[modify] https://crrev.com/7edaa330a17fc9ae61061295e1e757cb3521a8f4/src/snapshot/startup-deserializer.cc


### na...@google.com (2019-12-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-19)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2019-12-19)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-01-07)

ulan@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### mm...@chromium.org (2020-01-09)

[Empty comment from Monorail migration]

### hi...@gmail.com (2020-03-02)

Could you assign a CVE to this issue?

### [Deleted User] (2020-03-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-03-26)

This issue was migrated from crbug.com/chromium/1033395?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1034059]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050957)*

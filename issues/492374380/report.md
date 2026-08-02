# [Linux] Cross-Thread Use-After-Free in FontLoader::openStream via Non-Owning MappedFontFile Cache

| Field | Value |
|-------|-------|
| **Issue ID** | [492374380](https://issues.chromium.org/issues/492374380) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Fonts |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2026-03-13 |
| **Bounty** | $11,000.00 |

## Description

# [Linux] Cross-Thread Use-After-Free in FontLoader::openStream via Non-Owning MappedFontFile Cache

## Summary

A use-after-free vulnerability exists in the Linux font service's `FontLoader::openStream` method. The `mapped_font_files_` map stores non-owning raw pointers to `MappedFontFile` objects, and the cleanup of stale entries relies on a destructor-driven observer callback that acquires the same lock protecting the map. When one thread finds a dying `MappedFontFile` in the map and calls `CreateMemoryStream` on it, a concurrent thread can complete the object's destruction and deallocation before the first thread's `SkData` release callback fires, resulting in a heap-use-after-free. The vulnerability is reachable from JavaScript through the `FontFace` local font loading API in Web Workers and affects Linux only.

## Bisect

Introducing Commit: `ae33b4cefb07476b0c28be444221436954797e31`

- Date: 2025-01-07
- Author: Ben Wagner
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/6138889>

The non-owning pointer pattern in `mapped_font_files_` dates back to `4196dfefc131b` (2015), but the vulnerability became practically exploitable when this commit restored the 42-entry `typeface_cache_` LRU. Cache eviction during `makeTypeface` now provides a reliable path to `MappedFontFile` destruction while other threads race to access the same entries through `openStream`.

## Root Cause

`FontLoader` maintains two caches that interact unsafely across threads. The `typeface_cache_` is a 42-entry LRU cache of `sk_sp<SkTypeface>`, and `mapped_font_files_` is an `std::unordered_map` storing non-owning `raw_ptr<MappedFontFile>` pointers keyed by font ID:

```
// font_loader.h
std::unordered_map<uint32_t,
                   raw_ptr<internal::MappedFontFile, CtnExperimental>>
    mapped_font_files_ GUARDED_BY(mapped_font_files_lock_);

```

`MappedFontFile` inherits from `RefCountedThreadSafe` and uses an observer pattern to remove itself from the map during destruction:

```
// mapped_font_file.cc
MappedFontFile::~MappedFontFile() {
  if (observer_)
    observer_->OnMappedFontFileDestroyed(this);
}

```

The observer callback acquires `mapped_font_files_lock_` and erases the entry:

```
// font_loader.cc
void FontLoader::OnMappedFontFileDestroyed(internal::MappedFontFile* f) {
  base::AutoLock lock(mapped_font_files_lock_);
  mapped_font_files_.erase(f->font_id());
}

```

The race manifests when `openStream` finds an entry in the map for a `MappedFontFile` whose refcount is concurrently reaching zero on another thread. The critical sequence is:

Thread A (racer Worker) calls `openStream`, acquires `mapped_font_files_lock_`, finds the entry, and calls `CreateMemoryStream`:

```
// font_loader.cc
SkStreamAsset* FontLoader::openStream(const FontIdentity& identity) {
  {
    base::AutoLock lock(mapped_font_files_lock_);
    auto mapped_font_files_it = mapped_font_files_.find(identity.fID);
    if (mapped_font_files_it != mapped_font_files_.end())
      return mapped_font_files_it->second->CreateMemoryStream();
  }
  // ...
}

```

`CreateMemoryStream` captures `this` as the `SkData` release callback context and increments the refcount:

```
// mapped_font_file.cc
SkMemoryStream* MappedFontFile::CreateMemoryStream() {
  sk_sp<SkData> data =
      SkData::MakeWithProc(mapped_font_file_.data(), mapped_font_file_.length(),
                           &MappedFontFile::ReleaseProc, this);
  AddRef();
  return new SkMemoryStream(std::move(data));
}

```

Thread B (loader Worker shutting down) simultaneously destroys the last `SkTypeface` that held a reference to the same `MappedFontFile`. The `SkData` release callback calls `MappedFontFile::Release()`, which decrements the refcount to zero and enters the destructor. The destructor calls `OnMappedFontFileDestroyed`, which blocks on `mapped_font_files_lock_` (held by Thread A). Thread A completes `CreateMemoryStream`, releasing the lock. Thread B then proceeds to erase the map entry and deallocate the `MappedFontFile`.

The `SkMemoryStream` returned to Thread A now contains an `SkData` whose release context points to freed memory. When Thread A's `SkTypeface` is eventually destroyed (during Worker shutdown or cache eviction), `ReleaseProc` executes an atomic decrement on the freed `MappedFontFile`'s refcount field:

```
// mapped_font_file.cc
void MappedFontFile::ReleaseProc(const void* ptr, void* context) {
  static_cast<MappedFontFile*>(context)->Release();
}

```

This constitutes a heap-use-after-free write. Additionally, the `SkData` data pointer references the `MappedFontFile`'s `MemoryMappedFile` backing, which is also destroyed, so any font data reads between `CreateMemoryStream` and the eventual crash access unmapped memory.

The `raw_ptr<MappedFontFile, CtnExperimental>` wrapper in the map does not prevent this UAF. MiraclePtr detects accesses to quarantined (freed) memory, but during the race the object is still mid-destruction (the destructor is blocked on the lock), so the memory has not yet been freed when Thread A dereferences the pointer. MiraclePtr only triggers after deallocation.

`RefCountedThreadSafe` with `StartRefCountFromZeroTag` does not enforce that `AddRef` is called on a live object (refcount > 0). In Release builds, `AddRef` from zero succeeds silently, allowing `CreateMemoryStream` to increment a dead object's refcount.

## Reproduce

### Platform Requirements

This vulnerability is Linux-only. The entire `FontLoader` / `MappedFontFile` / `FontServiceThread` stack under `components/services/font/` is compiled exclusively for Linux (guarded by `BUILDFLAG(IS_LINUX)`). On macOS, Windows, and Android, Chromium uses platform-native font APIs (CoreText, DirectWrite, Android Skia fontmgr respectively) that never instantiate `FontLoader` or touch `mapped_font_files_`. ChromeOS uses a different font service path. There is no way to reach the vulnerable code on any non-Linux platform.

### Font Requirements

The PoC relies on `FontFace` with `local()` sources, which resolve to system-installed fonts by PostScript name through `FontUniqueNameLookupLinux`. The race requires loading more than 42 distinct fonts (the `typeface_cache_` LRU capacity) so that cache eviction triggers `MappedFontFile` destruction on one thread while another thread races to access the same entry through `openStream`.

The PoC's font list (65 fonts for loading, 45 for flushing) was verified on Ubuntu 22.04 with the following font packages installed:

```
sudo apt install -y fonts-dejavu fonts-freefont-ttf fonts-liberation fonts-lato \
  fonts-urw-base35 fonts-indic fonts-kacst fonts-tlwg-garuda fonts-khmeros \
  fonts-tlwg-kinnari fonts-tlwg-laksaman fonts-sil-abyssinica

```

The `fonts-indic` meta-package pulls in `fonts-aakar`, `fonts-anjalioldlipi`, `fonts-chilanka`, `fonts-dyuthi`, `fonts-gayathri`, `fonts-gubbi`, and other Indic script fonts used by the PoC. On a minimal Linux installation where fewer than 43 of the listed PostScript names resolve to installed fonts, the PoC will not trigger because the typeface cache will not evict entries. Install additional font packages or adjust the font list in the PoC to match available local fonts if needed.

### Steps

Tested at commit `e256102970bf347f2cc827935dbcb09ee18a3b60`. No source modifications are required.

Build:

```
autoninja -C out/asan-release chrome

```

Run:

```
ASAN_OPTIONS=detect_odr_violation=0 out/asan-release/chrome \
  --no-sandbox --disable-gpu \
  --user-data-dir=/tmp/poc-$(date +%s) \
  issue_fontloader_openstream_uaf/poc.html

```

The renderer process crashes with a heap-use-after-free within the first few rounds (typically rounds 0-5 out of 30). Reproduction rate is 100% across repeated runs on the tested configuration.

```
=================================================================
==3754133==ERROR: AddressSanitizer: heap-use-after-free on address 0x7bcb975c4ea0 at pc 0x7f4c078f2586 bp 0x7b4998d5aa10 sp 0x7b4998d5aa08
WRITE of size 4 at 0x7bcb975c4ea0 thread T13 (DedicatedWorker)
    #0 0x7f4c078f2585 in font_service::internal::MappedFontFile::ReleaseProc(void const*, void*) gen/third_party/libc++/src/include/__atomic/support/c11.h:207:10
    #1 0x7f4c11f09f9b in SkTypeface_Fontations::~SkTypeface_Fontations() third_party/skia/include/core/SkRefCnt.h:181:13
    #2 0x7f4c11f09ffd in SkTypeface_Fontations::~SkTypeface_Fontations() third_party/skia/src/ports/SkTypeface_fontations_priv.h:188:7
    #3 0x7f4bb5bf0f0a in cppgc::internal::HeapVisitor<cppgc::internal::(anonymous namespace)::MutatorThreadSweeper>::Traverse(cppgc::internal::BasePage&) v8/src/heap/cppgc/sweeper.cc:277:13
    #4 0x7f4bb5befd11 in cppgc::internal::(anonymous namespace)::MutatorThreadSweeper::Sweep(cppgc::internal::(anonymous namespace)::SweepingState&) v8/src/heap/cppgc/sweeper.cc:653:36
    #5 0x7f4bb5bef6f3 in cppgc::internal::Sweeper::SweeperImpl::Finish() v8/src/heap/cppgc/sweeper.cc:1311:13
    #6 0x7f4bb5be352f in cppgc::internal::Sweeper::SweeperImpl::FinishIfRunning() v8/src/heap/cppgc/sweeper.cc:1236:7
    #7 0x7f4bb5ba475e in cppgc::internal::HeapBase::Terminate() v8/src/heap/cppgc/heap-base.cc:275:15
    #8 0x7f4bb3b13d42 in v8::internal::CppHeap::~CppHeap() v8/src/heap/cppgc-js/cpp-heap.cc:551:13
    #9 0x7f4bb3b13f37 in non-virtual thunk to v8::internal::CppHeap::~CppHeap() v8/src/heap/cppgc-js/cpp-heap.cc:539:21
    #10 0x7f4bb3c6eab5 in v8::internal::Heap::TearDown() v8/src/heap/heap.cc:6512:15
    #11 0x7f4bb397c8c5 in v8::internal::Isolate::Deinit() v8/src/execution/isolate.cc:4863:9
    #12 0x7f4bb397b8cf in v8::internal::Isolate::Deinitialize(v8::internal::Isolate*) v8/src/execution/isolate.cc:4427:12
    #13 0x7f4bb397b74d in v8::internal::Isolate::Delete(v8::internal::Isolate*) v8/src/execution/isolate.cc:4408:3
    #14 0x7f4bd2dcd912 in gin::IsolateHolder::~IsolateHolder() gin/isolate_holder.cc:152:13
    #15 0x7f4bba70f042 in blink::V8PerIsolateData::~V8PerIsolateData() third_party/blink/renderer/platform/bindings/v8_per_isolate_data.cc:133:37
    #16 0x7f4bba7101cf in blink::V8PerIsolateData::Destroy(v8::Isolate*) third_party/blink/renderer/platform/bindings/v8_per_isolate_data.cc:199:3
    #17 0x7f4bc5e62eed in blink::WorkerBackingThread::ShutdownOnBackingThread() third_party/blink/renderer/core/workers/worker_backing_thread.cc:168:3
    #18 0x7f4bc5e8f163 in blink::WorkerThread::PerformShutdownOnWorkerThread() third_party/blink/renderer/core/workers/worker_thread.cc:854:30
    #19 0x7f4bc5e9452c in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #20 0x7f4c15d614f2 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #21 0x7f4c15de29de in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #22 0x7f4c15de19b6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #23 0x7f4c15c03591 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #24 0x7f4c15de4058 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #25 0x7f4c15ccbb52 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #26 0x7f4bbb47000c in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run() third_party/blink/renderer/platform/scheduler/worker/non_main_thread_impl.cc:178:14
    #27 0x7f4c15ede6fc in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #28 0x557c12ce4936 in asan_thread_start(void*) asan_interceptors.cpp

0x7bcb975c4ea0 is located 0 bytes inside of 88-byte region [0x7bcb975c4ea0,0x7bcb975c4ef8)
freed by thread T19 (DedicatedWorker) here:
    #0 0x557c12d213f2 in operator delete(void*, unsigned long)
    #1 0x7f4c078f2510 in font_service::internal::MappedFontFile::ReleaseProc(void const*, void*) base/memory/ref_counted.h:438:5
    #2 0x7f4c11f09f9b in SkTypeface_Fontations::~SkTypeface_Fontations() third_party/skia/include/core/SkRefCnt.h:181:13
    #3 0x7f4c11f09ffd in SkTypeface_Fontations::~SkTypeface_Fontations() third_party/skia/src/ports/SkTypeface_fontations_priv.h:188:7
    #4 0x7f4bb5bf0f0a in cppgc::internal::HeapVisitor<cppgc::internal::(anonymous namespace)::MutatorThreadSweeper>::Traverse(cppgc::internal::BasePage&) v8/src/heap/cppgc/sweeper.cc:277:13
    #5 0x7f4bb5befd11 in cppgc::internal::(anonymous namespace)::MutatorThreadSweeper::Sweep(cppgc::internal::(anonymous namespace)::SweepingState&) v8/src/heap/cppgc/sweeper.cc:653:36
    #6 0x7f4bb5bef6f3 in cppgc::internal::Sweeper::SweeperImpl::Finish() v8/src/heap/cppgc/sweeper.cc:1311:13
    #7 0x7f4bb5be352f in cppgc::internal::Sweeper::SweeperImpl::FinishIfRunning() v8/src/heap/cppgc/sweeper.cc:1236:7
    #8 0x7f4bb5ba475e in cppgc::internal::HeapBase::Terminate() v8/src/heap/cppgc/heap-base.cc:275:15
    #9 0x7f4bb3b13d42 in v8::internal::CppHeap::~CppHeap() v8/src/heap/cppgc-js/cpp-heap.cc:551:13
    #10 0x7f4bb3b13f37 in non-virtual thunk to v8::internal::CppHeap::~CppHeap() v8/src/heap/cppgc-js/cpp-heap.cc:539:21
    #11 0x7f4bb3c6eab5 in v8::internal::Heap::TearDown() v8/src/heap/heap.cc:6512:15
    #12 0x7f4bb397c8c5 in v8::internal::Isolate::Deinit() v8/src/execution/isolate.cc:4863:9
    #13 0x7f4bb397b8cf in v8::internal::Isolate::Deinitialize(v8::internal::Isolate*) v8/src/execution/isolate.cc:4427:12
    #14 0x7f4bb397b74d in v8::internal::Isolate::Delete(v8::internal::Isolate*) v8/src/execution/isolate.cc:4408:3
    #15 0x7f4bd2dcd912 in gin::IsolateHolder::~IsolateHolder() gin/isolate_holder.cc:152:13
    #16 0x7f4bba70f042 in blink::V8PerIsolateData::~V8PerIsolateData() third_party/blink/renderer/platform/bindings/v8_per_isolate_data.cc:133:37
    #17 0x7f4bba7101cf in blink::V8PerIsolateData::Destroy(v8::Isolate*) third_party/blink/renderer/platform/bindings/v8_per_isolate_data.cc:199:3
    #18 0x7f4bc5e62eed in blink::WorkerBackingThread::ShutdownOnBackingThread() third_party/blink/renderer/core/workers/worker_backing_thread.cc:168:3
    #19 0x7f4bc5e8f163 in blink::WorkerThread::PerformShutdownOnWorkerThread() third_party/blink/renderer/core/workers/worker_thread.cc:854:30
    #20 0x7f4bc5e9452c in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #21 0x7f4c15d614f2 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12

previously allocated by thread T19 (DedicatedWorker) here:
    #0 0x557c12d207ed in operator new(unsigned long)
    #1 0x7f4c078e5cf6 in font_service::internal::FontServiceThread::OpenStream(SkFontConfigInterface::FontIdentity const&) components/services/font/public/cpp/font_service_thread.cc:178:7
    #2 0x7f4c078daab8 in font_service::FontLoader::openStream(SkFontConfigInterface::FontIdentity const&) components/services/font/public/cpp/font_loader.cc:78:16
    #3 0x7f4c078db6ac in font_service::FontLoader::makeTypeface(SkFontConfigInterface::FontIdentity const&, sk_sp<SkFontMgr>) components/services/font/public/cpp/font_loader.cc:112:44
    #4 0x7f4bba8fb055 in blink::SkTypeface_Factory::FromFontConfigInterfaceIdAndTtcIndex(int, int) third_party/blink/renderer/platform/fonts/skia/sktypeface_factory.cc:30:15
    #5 0x7f4bbb0d67b8 in blink::FontUniqueNameLookupLinux::MatchUniqueName(blink::String const&) third_party/blink/renderer/platform/fonts/linux/font_unique_name_lookup_linux.cc:34:10
    #6 0x7f4bba8f8448 in blink::FontCache::CreateFontPlatformData(...) third_party/blink/renderer/platform/fonts/skia/font_cache_skia.cc:323:16
    #7 0x7f4bba7efc92 in blink::FontPlatformDataCache::GetOrCreateFontPlatformData(...) third_party/blink/renderer/platform/fonts/font_platform_data_cache.cc:68:52
    #8 0x7f4bba79bfc9 in blink::FontCache::GetFontPlatformData(...) third_party/blink/renderer/platform/fonts/font_cache.cc:144:36
    #9 0x7f4bba79cd2d in blink::FontCache::IsPlatformFontUniqueNameMatchAvailable(...) third_party/blink/renderer/platform/fonts/font_cache.cc:191:10
    #10 0x7f4bc28730fb in blink::LocalFontFaceSource::IsValid() const third_party/blink/renderer/core/css/local_font_face_source.cc:46:42
    #11 0x7f4bc24c38bb in blink::CSSFontFace::Load(blink::FontDescription const&) third_party/blink/renderer/core/css/css_font_face.cc:257:17
    #12 0x7f4bc24c0fec in blink::CSSFontFace::Load() third_party/blink/renderer/core/css/css_font_face.cc:246:3
    #13 0x7f4bc27b1cbf in blink::FontFace::load(blink::ScriptState*) third_party/blink/renderer/core/css/font_face.cc:622:21

SUMMARY: AddressSanitizer: heap-use-after-free gen/third_party/libc++/src/include/__atomic/support/c11.h:207:10 in font_service::internal::MappedFontFile::ReleaseProc(void const*, void*)
Shadow bytes around the buggy address:
  0x7bcb975c4c00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x7bcb975c4c80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x7bcb975c4d00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x7bcb975c4d80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x7bcb975c4e00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
=>0x7bcb975c4e80: fa fa f7 fa[fd]fd fd fd fd fd fd fd fd fd fd fa
  0x7bcb975c4f00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x7bcb975c4f80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x7bcb975c5000: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x7bcb975c5080: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa
  0x7bcb975c5100: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fa

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 39.0 KB)
- [poc.html](attachments/poc.html) (text/html, 7.4 KB)
- [0001-Fix-ownership-of-mapped_font_files_-values.patch](attachments/0001-Fix-ownership-of-mapped_font_files_-values.patch) (text/x-diff, 8.5 KB)

## Timeline

### je...@gmail.com (2026-03-13)

Due to font requirements, I recommend verifying on a standard Ubuntu distribution rather than using ClusterFuzz. If you need any assistance with the verification, please feel free to contact me.

### cl...@appspot.gserviceaccount.com (2026-03-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5394117207031808.

### 24...@project.gserviceaccount.com (2026-03-14)

Testcase 5394117207031808 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5394117207031808.

### je...@gmail.com (2026-03-14)

As I mentioned, this requires font requirements, which should be met by default on any normal Linux desktop distribution, but clusterfuzzer may not be able to do so.

Is there anyone willing to manually reproduce and check? Thanks!

### dc...@chromium.org (2026-03-16)

Due to the number of incoming bug, it's not always easy to manually reproduce everything to confirm. In my particular case, I don't have packages for all the fonts requested above. But the report looks plausible to me, so I'll triage it accordingly :)

### bu...@chromium.org (2026-03-16)

The root issue here is that [`return mapped_font_files_it->second->CreateMemoryStream();`](https://source.chromium.org/chromium/chromium/src/+/main:components/services/font/public/cpp/font_loader.cc;l=63;drc=b15fc6bfe4ba99a5e278995f9946faea6525156c) is not a valid call (and never has been, even before the typeface cache re-introduction) since there is no ownership of what is pointed at by the `raw_ptr<internal::MappedFontFile> second` here (`second` is fine though may be dangling so the `->` after it is not). The `mapped_font_files_lock_` protects the `mapped_font_files_` container and its entries, but it does not protect what is pointed at but unowned by its entries. What is pointed at (and not owned) by these entries are actually owned by the SkData owned by SkTypeface which are owned elsewhere and on arbitrary threads. It appears the idea was to have the entries in the map always be valid by removing the entries before they became invalid, unfortunately they are currently being removed after becoming invalid.

It appears that `mapped_font_files_` wants to be a "weak map" and there wants to be a "try ref" here. Unfortunately it doesn't looks like Chromium provides a good way to do this. Skia has SkRefCnt/SkWeakRefCnt and c++ has std::shared\_ptr/std::weak\_ptr but those probably cannot be used here (note that `base::WeakPtr` is a confusingly named different thing).

It may be easier to band-aid this for now by moving the call to the `observer_` into `MappedFontFile::ReleaseProc` and changing the condition to having an `observer_` and `HasOneRef`. If this is done under a mutex which also includes the `Release` then this will always allow the `observer_` to remove the appropriate entry while it is still valid right before invalidating the entry. In other words, change `OnMappedFontFileDestroyed` (indicating it is already destroyed) to `OnMappedFontFileToBeDestroyed` (indicating that is about to be destroyed).

### ch...@google.com (2026-03-17)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-17)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### bu...@chromium.org (2026-03-17)

Attaching a patch which uses `std::shared_ptr`/`std::weak_ptr` to make this work as intended.

I have not been able to get this issue to reproduce locally. The `poc.html` gets to 30/30 without any ASAN reports, with "Loader loaded 52 fonts" since on my machine some of these are Type1 fonts so don't get loaded. I've also tried adjusting `kMaxTypefacesCached`. Since this is a race that depends on a lot of factors it isn't all that surprising that it is difficult to reproduce.

### je...@gmail.com (2026-03-17)

I'll try to see if I can better construct a PoC to trigger this vulnerability more effectively. Also, if there are any patches you need me to verify, please let me know anytime.

### dr...@chromium.org (2026-03-18)

Downgrading this to S2 due to specific requirements for reproduction.

### bu...@chromium.org (2026-03-23)

It would be helpful to verify `0001-Fix-ownership-of-mapped_font_files_-values.patch` from [comment #10](https://issues.chromium.org/issues/492374380#comment10).

### je...@gmail.com (2026-03-23)

I found a place where I added a line of sleep, which might help you consistently reproduce this issue.

```
diff --git a/components/services/font/public/cpp/font_loader.cc b/components/services/font/public/cpp/font_loader.cc
index adad666abf1c5..57dabee625126 100644
--- a/components/services/font/public/cpp/font_loader.cc
+++ b/components/services/font/public/cpp/font_loader.cc
@@ -8,6 +8,7 @@
 
 #include "base/functional/bind.h"
 #include "base/memory/ref_counted.h"
+#include "base/threading/platform_thread.h"
 #include "base/trace_event/trace_event.h"
 #include "components/services/font/public/cpp/font_service_thread.h"
 #include "pdf/buildflags.h"
@@ -156,6 +157,7 @@ std::vector<std::string> FontLoader::ListFamilies() {
 void FontLoader::OnMappedFontFileDestroyed(internal::MappedFontFile* f) {
   TRACE_EVENT1("fonts", "FontLoader::OnMappedFontFileDestroyed", "identity",
                f->font_id());
+  base::PlatformThread::Sleep(base::Milliseconds(10));
   base::AutoLock lock(mapped_font_files_lock_);
   mapped_font_files_.erase(f->font_id());
 }

```

Additionally, I just tested it, and after applying the patch mentioned in [comment #10](https://issues.chromium.org/issues/492374380#comment10), this vulnerability has been properly fixed.

### bu...@chromium.org (2026-03-23)

With the sleep patch applied I am reproducing. Though in my case this is almost always an SIGSEGV when Fontations code is reading font data which no longer exists. Applying the patch from [comment #10](https://issues.chromium.org/issues/492374380#comment10) is observed to fix this version of the issue as well.

### je...@gmail.com (2026-04-17)

I believe we can apply the patch and fix this vulnerability directly.

### dx...@google.com (2026-04-22)

Project: chromium/src  

Branch:  main  

Author:  Daniel Cheng [dcheng@chromium.org](mailto:dcheng@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7706875>

Implement helper for a thread-safe shared cache of weakly-owned values

---


Expand for full commit details
```
     
    The core logic is taken from blink::AtomicStringTable; the key insight 
    is the final decrement to zero needs to be coordinated with the table to 
    avoid a race where one thread acquires a new reference just as another 
    thread is trying to drop the final reference. In the future, this may be 
    rewritten to take advantage of primitives from the standard library, 
    i.e. `std::shared_ptr` and `std::weak_ptr`. 
     
    Migrate the font service to use this new helper; in theory, it might be 
    possible to layer `blink::AtomicStringTable` on top of this helper as 
    well, but `base::AtomicStringTable` has a lot of additional complexity 
    to ensure atomicity of strings, so that is left as an exercise for a 
    future reader. 
     
    gemini-cli was used to expand test TODOs into actual tests as well as 
    suggest and implement additional test coverage. 
     
    Bug: 492374380 
    Change-Id: If903b247109e11be2fb6440297a59e78d20d4ac7 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7706875 
    Commit-Queue: Daniel Cheng <dcheng@chromium.org> 
    Reviewed-by: Sean Maher <spvm@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1619150}

```

---

Files:

- M `base/BUILD.gn`
- A `base/containers/weak_value_table.h`
- A `base/containers/weak_value_table_unittest.cc`
- M `components/services/font/public/cpp/font_loader.cc`
- M `components/services/font/public/cpp/font_loader.h`
- M `components/services/font/public/cpp/font_service_thread.cc`
- M `components/services/font/public/cpp/mapped_font_file.cc`
- M `components/services/font/public/cpp/mapped_font_file.h`

---

Hash: [dd21b7b159ee1575fe6e21a82d9ff2a60f6feca0](https://chromiumdash.appspot.com/commit/dd21b7b159ee1575fe6e21a82d9ff2a60f6feca0)  

Date: Wed Apr 22 22:43:36 2026


---

### aj...@google.com (2026-06-24)

-> S1 as this renderer UAF can be reproduced on a vanilla linux install

### sp...@google.com (2026-06-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
High Quality. Renderer RCE / memory corruption in a sandboxed process with bisect.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-07-31)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492374380)*

# Security: [webkit] heap-use-after-free in WebCore::DOMWrapperWorld::~DOMWrapperWorld()+0x25b

| Field | Value |
|-------|-------|
| **Issue ID** | [40061108](https://issues.chromium.org/issues/40061108) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Mobile>iOSWeb |
| **Platforms** | iOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2022-09-23 |
| **Bounty** | $7,000.00 |

## Description

#Summary
heap-use-after-free in WebCore::DOMWrapperWorld::~DOMWrapperWorld()+0x25b

#Reproduce
/WebKit/Tools/Scripts/run-minibrowser poc.html

#CrashType
WebContent process crashed

#Affect
chrome on ios

#RCA
Coming soon

#ASAN
➜  ~ /WebKit/Tools/Scripts/run-minibrowser
Starting MiniBrowser with DYLD_FRAMEWORK_PATH set to point to built WebKit in /Users/ldd/work/WebKit/WebKitBuild/Release.
MiniBrowser(813,0x7ff84f293100) malloc: nano zone abandoned due to inability to preallocate reserved vm space.
2022-09-23 11:11:30.873 com.apple.WebKit.WebContent.Development[815:8030] ApplePersistence=NO
=================================================================
==815==ERROR: AddressSanitizer: heap-use-after-free on address 0x62f00007a288 at pc 0x00021ae4a51c bp 0x70000be3c450 sp 0x70000be3c448
READ of size 8 at 0x62f00007a288 thread T14

    #0 0x21ae4a51b in WebCore::DOMWrapperWorld::~DOMWrapperWorld()+0x25b (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x313351b)
    #1 0x21ae4a868 in WebCore::DOMWrapperWorld::~DOMWrapperWorld()+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x3133868)
    #2 0x21aeb1f92 in std::__1::default_delete<WebCore::DOMWrapperWorld>::operator()(WebCore::DOMWrapperWorld*) const+0x12 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x319af92)
    #3 0x21aeb1f29 in WTF::RefCounted<WebCore::DOMWrapperWorld, std::__1::default_delete<WebCore::DOMWrapperWorld> >::deref() const+0x19 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x319af29)
    #4 0x21aeb1f03 in WTF::Ref<WebCore::DOMWrapperWorld, WTF::RawPtrTraits<WebCore::DOMWrapperWorld> >::~Ref()+0x33 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x319af03)
    #5 0x21ae5d8a8 in WTF::Ref<WebCore::DOMWrapperWorld, WTF::RawPtrTraits<WebCore::DOMWrapperWorld> >::~Ref()+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x31468a8)
    #6 0x21ae8ae64 in WebCore::JSEventListener::~JSEventListener()+0x34 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x3173e64)
    #7 0x21ae8d0b8 in WebCore::JSEventListener::~JSEventListener()+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x31760b8)
    #8 0x21ae8d0cd in WebCore::JSEventListener::~JSEventListener()+0xd (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x31760cd)
    #9 0x217f2a479 in std::__1::default_delete<WebCore::EventListener>::operator()(WebCore::EventListener*) const+0x39 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x213479)
    #10 0x217f2a3ed in WTF::RefCounted<WebCore::EventListener, std::__1::default_delete<WebCore::EventListener> >::deref() const+0x1d (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x2133ed)
    #11 0x217f2a3c7 in WTF::Ref<WebCore::EventListener, WTF::RawPtrTraits<WebCore::EventListener> >::~Ref()+0x37 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x2133c7)
    #12 0x217f2a378 in WTF::Ref<WebCore::EventListener, WTF::RawPtrTraits<WebCore::EventListener> >::~Ref()+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x213378)
    #13 0x217f2a351 in WebCore::RegisteredEventListener::~RegisteredEventListener()+0x11 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x213351)
    #14 0x217f2a328 in WebCore::RegisteredEventListener::~RegisteredEventListener()+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x213328)
    #15 0x217f2a302 in std::__1::default_delete<WebCore::RegisteredEventListener>::operator()(WebCore::RegisteredEventListener*) const+0x12 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x213302)
    #16 0x217f2a2d9 in WTF::RefCounted<WebCore::RegisteredEventListener, std::__1::default_delete<WebCore::RegisteredEventListener> >::deref() const+0x19 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x2132d9)
    #17 0x217f2a2a4 in WTF::VectorDestructor<true, WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> > >::destruct(WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> >*, WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> >*)+0x34 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x2132a4)
    #18 0x217f2a178 in WTF::VectorTypeOperations<WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> > >::destruct(WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> >*, WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> >*)+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x213178)
    #19 0x217f2a13a in WTF::Vector<WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> >, 1ul, WTF::CrashOnOverflow, 2ul, WTF::FastMalloc>::~Vector()+0x4a (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x21313a)
    #20 0x217f2a0e8 in WTF::Vector<WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> >, 1ul, WTF::CrashOnOverflow, 2ul, WTF::FastMalloc>::~Vector()+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x2130e8)
    #21 0x217f2a0c1 in std::__1::pair<WTF::AtomString, WTF::Vector<WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> >, 1ul, WTF::CrashOnOverflow, 2ul, WTF::FastMalloc> >::~pair()+0x11 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x2130c1)
    #22 0x217f2a0a8 in std::__1::pair<WTF::AtomString, WTF::Vector<WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> >, 1ul, WTF::CrashOnOverflow, 2ul, WTF::FastMalloc> >::~pair()+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x2130a8)
    #23 0x217f2a087 in WTF::VectorDestructor<true, std::__1::pair<WTF::AtomString, WTF::Vector<WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> >, 1ul, WTF::CrashOnOverflow, 2ul, WTF::FastMalloc> > >::destruct(std::__1::pair<WTF::AtomString, WTF::Vector<WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> >, 1ul, WTF::CrashOnOverflow, 2ul, WTF::FastMalloc> >*, std::__1::pair<WTF::AtomString, WTF::Vector<WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> >, 1ul, WTF::CrashOnOverflow, 2ul, WTF::FastMalloc> >*)+0x27 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x213087)
    #24 0x217f29f48 in WTF::VectorTypeOperations<std::__1::pair<WTF::AtomString, WTF::Vector<WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> >, 1ul, WTF::CrashOnOverflow, 2ul, WTF::FastMalloc> > >::destruct(std::__1::pair<WTF::AtomString, WTF::Vector<WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> >, 1ul, WTF::CrashOnOverflow, 2ul, WTF::FastMalloc> >*, std::__1::pair<WTF::AtomString, WTF::Vector<WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> >, 1ul, WTF::CrashOnOverflow, 2ul, WTF::FastMalloc> >*)+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x212f48)
    #25 0x21b8e7871 in WTF::Vector<std::__1::pair<WTF::AtomString, WTF::Vector<WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> >, 1ul, WTF::CrashOnOverflow, 2ul, WTF::FastMalloc> >, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>::shrink(unsigned long)+0x31 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x3bd0871)
    #26 0x21b8e7796 in WTF::Vector<std::__1::pair<WTF::AtomString, WTF::Vector<WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> >, 1ul, WTF::CrashOnOverflow, 2ul, WTF::FastMalloc> >, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>::shrinkCapacity(unsigned long)+0x36 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x3bd0796)
    #27 0x21b8d6dba in WTF::Vector<std::__1::pair<WTF::AtomString, WTF::Vector<WTF::RefPtr<WebCore::RegisteredEventListener, WTF::RawPtrTraits<WebCore::RegisteredEventListener>, WTF::DefaultRefDerefTraits<WebCore::RegisteredEventListener> >, 1ul, WTF::CrashOnOverflow, 2ul, WTF::FastMalloc> >, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>::clear()+0xa (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x3bbfdba)
    #28 0x21b8e6188 in WebCore::EventListenerMap::clearEntriesForTearDown()+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x3bcf188)
    #29 0x21b8e03c8 in WebCore::EventTargetData::clear()+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x3bc93c8)
    #30 0x21b8e0357 in WebCore::EventTarget::~EventTarget()+0x47 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x3bc9357)
    #31 0x21b416b95 in WebCore::FontFaceSet::~FontFaceSet()+0x35 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x36ffb95)
    #32 0x21b416c08 in WebCore::FontFaceSet::~FontFaceSet()+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x36ffc08)
    #33 0x218996e42 in std::__1::default_delete<WebCore::FontFaceSet>::operator()(WebCore::FontFaceSet*) const+0x12 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0xc7fe42)
    #34 0x218996ddd in WTF::RefCounted<WebCore::FontFaceSet, std::__1::default_delete<WebCore::FontFaceSet> >::deref() const+0x1d (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0xc7fddd)
    #35 0x21b2c7e81 in WebCore::CSSFontSelector::~CSSFontSelector()+0x81 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x35b0e81)
    #36 0x21b2c7fd8 in WebCore::CSSFontSelector::~CSSFontSelector()+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x35b0fd8)
    #37 0x21b2c800d in WebCore::CSSFontSelector::~CSSFontSelector()+0xd (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x35b100d)
    #38 0x21a77c779 in std::__1::default_delete<WebCore::FontSelector>::operator()(WebCore::FontSelector*) const+0x39 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x2a65779)
    #39 0x21a77c72d in WTF::RefCounted<WebCore::FontSelector, std::__1::default_delete<WebCore::FontSelector> >::deref() const+0x1d (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x2a6572d)
    #40 0x21b2dbc7c in WebCore::CSSFontSelector::deref()+0xc (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x35c4c7c)
    #41 0x21df5cfe3 in WebCore::WorkerGlobalScope::~WorkerGlobalScope()+0x253 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x6245fe3)
    #42 0x21df4d4d9 in WebCore::DedicatedWorkerGlobalScope::~DedicatedWorkerGlobalScope()+0x29 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x62364d9)
    #43 0x21df4d4f8 in WebCore::DedicatedWorkerGlobalScope::~DedicatedWorkerGlobalScope()+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x62364f8)
    #44 0x21df4d54d in WebCore::DedicatedWorkerGlobalScope::~DedicatedWorkerGlobalScope()+0xd (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x623654d)
    #45 0x21838d2e9 in std::__1::default_delete<WebCore::WorkerOrWorkletGlobalScope>::operator()(WebCore::WorkerOrWorkletGlobalScope*) const+0x39 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x6762e9)
    #46 0x21838d260 in WTF::RefCounted<WebCore::WorkerOrWorkletGlobalScope, std::__1::default_delete<WebCore::WorkerOrWorkletGlobalScope> >::deref() const+0x20 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x676260)
    #47 0x21df72de0 in WTF::RefPtr<WebCore::WorkerOrWorkletGlobalScope, WTF::RawPtrTraits<WebCore::WorkerOrWorkletGlobalScope>, WTF::DefaultRefDerefTraits<WebCore::WorkerOrWorkletGlobalScope> >::operator=(std::nullptr_t)+0x20 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x625bde0)
    #48 0x21df728d2 in WebCore::WorkerOrWorkletThread::workerOrWorkletThread()+0x722 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x625b8d2)
    #49 0x21dfbb624 in WebCore::WorkerThread::createThread()::$_5::operator()() const+0x24 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x62a4624)
    #50 0x21dfbb5ec in WTF::Detail::CallableWrapper<WebCore::WorkerThread::createThread()::$_5, void>::call()+0xc (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x62a45ec)
    #51 0x207346d1e in WTF::Function<void ()>::operator()() const+0x3e (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x3fd1e)
    #52 0x20745ff98 in WTF::Thread::entryPoint(WTF::Thread::NewThreadContext*)+0x188 (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x158f98)
    #53 0x20746a548 in WTF::wtfThreadEntryPoint(void*)+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x163548)
    #54 0x7ff80bc5e258 in _pthread_start+0x7c (/usr/lib/system/libsystem_pthread.dylib:x86_64+0x6258)
    #55 0x7ff80bc59c7a in thread_start+0xe (/usr/lib/system/libsystem_pthread.dylib:x86_64+0x1c7a)

0x62f00007a288 is located 40584 bytes inside of 52152-byte region [0x62f000070400,0x62f00007cfb8)
freed by thread T14 here:
    #0 0x1d83fdb66 in __sanitizer_mz_free+0x86 (/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/clang/14.0.0/lib/darwin/libclang_rt.asan_osx_dynamic.dylib:x86_64h+0x4bb66)
    #1 0x20758b1b4 in bmalloc::DebugHeap::free(void*)+0x24 (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x2841b4)
    #2 0x20758bae3 in pas_debug_heap_free+0x33 (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x284ae3)
    #3 0x207584ecc in bmalloc_heap_config_specialized_try_deallocate_not_small_exclusive_segregated+0x5dc (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x27decc)
    #4 0x20a94e0c8 in WTF::ThreadSafeRefCountedBase::operator delete(void*)+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x36470c8)
    #5 0x2084a4c26 in WTF::ThreadSafeRefCounted<JSC::VM, (WTF::DestructionThread)0>::deref() const::'lambda'()::operator()() const+0x36 (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x119dc26)
    #6 0x208485aa9 in WTF::ThreadSafeRefCounted<JSC::VM, (WTF::DestructionThread)0>::deref() const+0xd9 (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x117eaa9)
    #7 0x209c38d7a in WTF::RefPtr<JSC::VM, WTF::RawPtrTraits<JSC::VM>, WTF::DefaultRefDerefTraits<JSC::VM> >::operator=(std::nullptr_t)+0x1a (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x2931d7a)
    #8 0x20aa8e88d in JSC::JSLockHolder::~JSLockHolder()+0xfd (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x378788d)
    #9 0x20aa8e968 in JSC::JSLockHolder::~JSLockHolder()+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x3787968)
    #10 0x21df6cfc6 in WebCore::WorkerOrWorkletScriptController::~WorkerOrWorkletScriptController()+0x146 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x6255fc6)
    #11 0x21df6d078 in WebCore::WorkerOrWorkletScriptController::~WorkerOrWorkletScriptController()+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x6256078)
    #12 0x21df8dd02 in std::__1::default_delete<WebCore::WorkerOrWorkletScriptController>::operator()(WebCore::WorkerOrWorkletScriptController*) const+0x12 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x6276d02)
    #13 0x21df8dcbc in std::__1::unique_ptr<WebCore::WorkerOrWorkletScriptController, std::__1::default_delete<WebCore::WorkerOrWorkletScriptController> >::reset(WebCore::WorkerOrWorkletScriptController*)+0x3c (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x6276cbc)
    #14 0x21df6c388 in std::__1::unique_ptr<WebCore::WorkerOrWorkletScriptController, std::__1::default_delete<WebCore::WorkerOrWorkletScriptController> >::operator=(std::nullptr_t)+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x6255388)
    #15 0x21df6c36f in WebCore::WorkerOrWorkletGlobalScope::clearScript()+0xf (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x625536f)
    #16 0x21df9b7c0 in WebCore::WorkerOrWorkletThread::stop(WTF::Function<void ()>&&)::$_33::operator()(WebCore::ScriptExecutionContext&) const::'lambda'(WebCore::ScriptExecutionContext&)::operator()(WebCore::ScriptExecutionContext&) const+0x10 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x62847c0)
    #17 0x21df9b79b in WTF::Detail::CallableWrapper<WebCore::WorkerOrWorkletThread::stop(WTF::Function<void ()>&&)::$_33::operator()(WebCore::ScriptExecutionContext&) const::'lambda'(WebCore::ScriptExecutionContext&), void, WebCore::ScriptExecutionContext&>::call(WebCore::ScriptExecutionContext&)+0xb (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x628479b)
    #18 0x21ab311a5 in WTF::Function<void (WebCore::ScriptExecutionContext&)>::operator()(WebCore::ScriptExecutionContext&) const+0x45 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x2e1a1a5)
    #19 0x21ab156a8 in WebCore::ScriptExecutionContext::Task::performTask(WebCore::ScriptExecutionContext&)+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x2dfe6a8)
    #20 0x21df9ebc0 in WebCore::WorkerDedicatedRunLoop::Task::performTask(WebCore::WorkerOrWorkletGlobalScope*)+0x50 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x6287bc0)
    #21 0x21df9ddef in WebCore::WorkerDedicatedRunLoop::runCleanupTasks(WebCore::WorkerOrWorkletGlobalScope*)+0xdf (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x6286def)
    #22 0x21df9d54c in WebCore::WorkerDedicatedRunLoop::run(WebCore::WorkerOrWorkletGlobalScope*)+0x13c (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x628654c)
    #23 0x21df7219b in WebCore::WorkerOrWorkletThread::runEventLoop()+0x4b (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x625b19b)
    #24 0x21df4e248 in WebCore::DedicatedWorkerThread::runEventLoop()+0x78 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x6237248)
    #25 0x21df7275e in WebCore::WorkerOrWorkletThread::workerOrWorkletThread()+0x5ae (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x625b75e)
    #26 0x21dfbb624 in WebCore::WorkerThread::createThread()::$_5::operator()() const+0x24 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x62a4624)
    #27 0x21dfbb5ec in WTF::Detail::CallableWrapper<WebCore::WorkerThread::createThread()::$_5, void>::call()+0xc (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x62a45ec)
    #28 0x207346d1e in WTF::Function<void ()>::operator()() const+0x3e (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x3fd1e)
    #29 0x20745ff98 in WTF::Thread::entryPoint(WTF::Thread::NewThreadContext*)+0x188 (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x158f98)

previously allocated by thread T14 here:
    #0 0x1d83fd760 in __sanitizer_mz_malloc+0xa0 (/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/clang/14.0.0/lib/darwin/libclang_rt.asan_osx_dynamic.dylib:x86_64h+0x4b760)
    #1 0x7ff80bace118 in _malloc_zone_malloc_instrumented_or_legacy+0x57 (/usr/lib/system/libsystem_malloc.dylib:x86_64+0x1f118)
    #2 0x20758b0c8 in bmalloc::DebugHeap::malloc(unsigned long, bmalloc::FailureAction)+0x28 (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x2840c8)
    #3 0x20758b9f8 in pas_debug_heap_malloc+0x38 (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x2849f8)
    #4 0x207553a91 in pas_debug_heap_allocate+0x21 (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x24ca91)
    #5 0x2075201d6 in bmalloc_allocate_impl_casual_case+0x2b6 (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x2191d6)
    #6 0x20751ff18 in bmalloc_allocate_casual+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x218f18)
    #7 0x207325558 in WTF::ThreadSafeRefCountedBase::operator new(unsigned long)+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x1e558)
    #8 0x20ae5c5dd in JSC::VM::create(JSC::HeapType, WTF::RunLoop*)+0x1d (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x3b555dd)
    #9 0x21df5c056 in WebCore::WorkerGlobalScope::WorkerGlobalScope(WebCore::WorkerThreadType, WebCore::WorkerParameters const&, WTF::Ref<WebCore::SecurityOrigin, WTF::RawPtrTraits<WebCore::SecurityOrigin> >&&, WebCore::WorkerThread&, WTF::Ref<WebCore::SecurityOrigin, WTF::RawPtrTraits<WebCore::SecurityOrigin> >&&, WebCore::IDBClient::IDBConnectionProxy*, WebCore::SocketProvider*)+0x176 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x6245056)
    #10 0x21df4d406 in WebCore::DedicatedWorkerGlobalScope::DedicatedWorkerGlobalScope(WebCore::WorkerParameters const&, WTF::Ref<WebCore::SecurityOrigin, WTF::RawPtrTraits<WebCore::SecurityOrigin> >&&, WebCore::DedicatedWorkerThread&, WTF::Ref<WebCore::SecurityOrigin, WTF::RawPtrTraits<WebCore::SecurityOrigin> >&&, WebCore::IDBClient::IDBConnectionProxy*, WebCore::SocketProvider*)+0x36 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x6236406)
    #11 0x21df4d384 in WebCore::DedicatedWorkerGlobalScope::DedicatedWorkerGlobalScope(WebCore::WorkerParameters const&, WTF::Ref<WebCore::SecurityOrigin, WTF::RawPtrTraits<WebCore::SecurityOrigin> >&&, WebCore::DedicatedWorkerThread&, WTF::Ref<WebCore::SecurityOrigin, WTF::RawPtrTraits<WebCore::SecurityOrigin> >&&, WebCore::IDBClient::IDBConnectionProxy*, WebCore::SocketProvider*)+0x14 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x6236384)
    #12 0x21df4d2d2 in WebCore::DedicatedWorkerGlobalScope::create(WebCore::WorkerParameters const&, WTF::Ref<WebCore::SecurityOrigin, WTF::RawPtrTraits<WebCore::SecurityOrigin> >&&, WebCore::DedicatedWorkerThread&, WTF::Ref<WebCore::SecurityOrigin, WTF::RawPtrTraits<WebCore::SecurityOrigin> >&&, WebCore::IDBClient::IDBConnectionProxy*, WebCore::SocketProvider*)+0x52 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x62362d2)
    #13 0x21df4dfd6 in WebCore::DedicatedWorkerThread::createWorkerGlobalScope(WebCore::WorkerParameters const&, WTF::Ref<WebCore::SecurityOrigin, WTF::RawPtrTraits<WebCore::SecurityOrigin> >&&, WTF::Ref<WebCore::SecurityOrigin, WTF::RawPtrTraits<WebCore::SecurityOrigin> >&&)+0x116 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x6236fd6)
    #14 0x21dfa4960 in WebCore::WorkerThread::createGlobalScope()+0x100 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x628d960)
    #15 0x21df724ce in WebCore::WorkerOrWorkletThread::workerOrWorkletThread()+0x31e (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x625b4ce)
    #16 0x21dfbb624 in WebCore::WorkerThread::createThread()::$_5::operator()() const+0x24 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x62a4624)
    #17 0x21dfbb5ec in WTF::Detail::CallableWrapper<WebCore::WorkerThread::createThread()::$_5, void>::call()+0xc (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x62a45ec)
    #18 0x207346d1e in WTF::Function<void ()>::operator()() const+0x3e (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x3fd1e)
    #19 0x20745ff98 in WTF::Thread::entryPoint(WTF::Thread::NewThreadContext*)+0x188 (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x158f98)
    #20 0x20746a548 in WTF::wtfThreadEntryPoint(void*)+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x163548)
    #21 0x7ff80bc5e258 in _pthread_start+0x7c (/usr/lib/system/libsystem_pthread.dylib:x86_64+0x6258)
    #22 0x7ff80bc59c7a in thread_start+0xe (/usr/lib/system/libsystem_pthread.dylib:x86_64+0x1c7a)

Thread T14 created by T0 here:
    #0 0x1d83f699c in wrap_pthread_create+0x5c (/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/clang/14.0.0/lib/darwin/libclang_rt.asan_osx_dynamic.dylib:x86_64h+0x4499c)
    #1 0x20746a40b in WTF::Thread::establishHandle(WTF::Thread::NewThreadContext*, std::__1::optional<unsigned long>, WTF::Thread::QOS)+0x18b (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x16340b)
    #2 0x20746024b in WTF::Thread::create(char const*, WTF::Function<void ()>&&, WTF::ThreadType, WTF::Thread::QOS)+0x1cb (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x15924b)
    #3 0x21dfa4776 in WebCore::WorkerThread::createThread()+0x236 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x628d776)
    #4 0x21df72f4f in WebCore::WorkerOrWorkletThread::start(WTF::Function<void (WTF::String const&)>&&)+0x11f (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x625bf4f)
    #5 0x21df692ff in WebCore::DedicatedWorkerThread::start()+0xbf (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x62522ff)
    #6 0x21df68ad5 in WebCore::WorkerMessagingProxy::startWorkerGlobalScope(WTF::URL const&, PAL::SessionID, WTF::String const&, WebCore::WorkerInitializationData&&, WebCore::ScriptBuffer const&, WebCore::ContentSecurityPolicyResponseHeaders const&, bool, WebCore::CrossOriginEmbedderPolicy const&, WTF::MonotonicTime, WebCore::ReferrerPolicy, WebCore::WorkerType, WebCore::FetchOptions::Credentials, JSC::RuntimeFlags)+0x585 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x6251ad5)
    #7 0x21df517e9 in WebCore::Worker::notifyFinished()+0x619 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x623a7e9)
    #8 0x21dfa3399 in WebCore::WorkerScriptLoader::notifyFinished()+0xa9 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x628c399)
    #9 0x21dfa2fcd in WebCore::WorkerScriptLoader::didFinishLoading(WTF::ObjectIdentifier<WebCore::ResourceLoader>, WebCore::NetworkLoadMetrics const&)+0x17d (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x628bfcd)
    #10 0x21c58ae08 in WebCore::DocumentThreadableLoader::didFinishLoading(WTF::ObjectIdentifier<WebCore::ResourceLoader>, WebCore::NetworkLoadMetrics const&)+0x4e8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x4873e08)
    #11 0x21c58a727 in WebCore::DocumentThreadableLoader::notifyFinished(WebCore::CachedResource&, WebCore::NetworkLoadMetrics const&)+0x67 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x4873727)
    #12 0x21c731b6f in WebCore::CachedResource::checkNotify(WebCore::NetworkLoadMetrics const&)+0x17f (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x4a1ab6f)
    #13 0x21c71f83e in WebCore::CachedResource::finishLoading(WebCore::FragmentedSharedBuffer const*, WebCore::NetworkLoadMetrics const&)+0x4e (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x4a0883e)
    #14 0x21c72e557 in WebCore::CachedRawResource::finishLoading(WebCore::FragmentedSharedBuffer const*, WebCore::NetworkLoadMetrics const&)+0x267 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x4a17557)
    #15 0x21c6a95bf in WebCore::SubresourceLoader::didFinishLoading(WebCore::NetworkLoadMetrics const&)+0x62f (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x49925bf)
    #16 0x1ed25eaa2 in WebKit::WebResourceLoader::didFinishResourceLoad(WebCore::NetworkLoadMetrics&&)+0x2b2 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebKit.framework/Versions/A/WebKit:x86_64+0x27feaa2)
    #17 0x1edc818f7 in void IPC::callMemberFunctionImpl<WebKit::WebResourceLoader, void (WebKit::WebResourceLoader::*)(WebCore::NetworkLoadMetrics&&), std::__1::tuple<WebCore::NetworkLoadMetrics>, 0ul>(WebKit::WebResourceLoader*, void (WebKit::WebResourceLoader::*)(WebCore::NetworkLoadMetrics&&), std::__1::tuple<WebCore::NetworkLoadMetrics>&&, std::__1::integer_sequence<unsigned long, 0ul>)+0x47 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebKit.framework/Versions/A/WebKit:x86_64+0x32218f7)
    #18 0x1edc81837 in void IPC::callMemberFunction<WebKit::WebResourceLoader, void (WebKit::WebResourceLoader::*)(WebCore::NetworkLoadMetrics&&), std::__1::tuple<WebCore::NetworkLoadMetrics>, std::__1::integer_sequence<unsigned long, 0ul> >(std::__1::tuple<WebCore::NetworkLoadMetrics>&&, WebKit::WebResourceLoader*, void (WebKit::WebResourceLoader::*)(WebCore::NetworkLoadMetrics&&))+0x17 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebKit.framework/Versions/A/WebKit:x86_64+0x3221837)
    #19 0x1edc771f2 in void IPC::handleMessage<Messages::WebResourceLoader::DidFinishResourceLoad, WebKit::WebResourceLoader, void (WebKit::WebResourceLoader::*)(WebCore::NetworkLoadMetrics&&)>(IPC::Connection&, IPC::Decoder&, WebKit::WebResourceLoader*, void (WebKit::WebResourceLoader::*)(WebCore::NetworkLoadMetrics&&))+0x152 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebKit.framework/Versions/A/WebKit:x86_64+0x32171f2)
    #20 0x1edc76539 in WebKit::WebResourceLoader::didReceiveWebResourceLoaderMessage(IPC::Connection&, IPC::Decoder&)+0x1f9 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebKit.framework/Versions/A/WebKit:x86_64+0x3216539)
    #21 0x1ed24877e in WebKit::NetworkProcessConnection::didReceiveMessage(IPC::Connection&, IPC::Decoder&)+0x10e (/Users/ldd/work/WebKit/WebKitBuild/Release/WebKit.framework/Versions/A/WebKit:x86_64+0x27e877e)
    #22 0x1edded0bc in IPC::Connection::dispatchMessage(IPC::Decoder&)+0x25c (/Users/ldd/work/WebKit/WebKitBuild/Release/WebKit.framework/Versions/A/WebKit:x86_64+0x338d0bc)
    #23 0x1edded987 in IPC::Connection::dispatchMessage(std::__1::unique_ptr<IPC::Decoder, std::__1::default_delete<IPC::Decoder> >)+0x2e7 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebKit.framework/Versions/A/WebKit:x86_64+0x338d987)
    #24 0x1eddee4c4 in IPC::Connection::dispatchOneIncomingMessage()+0x184 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebKit.framework/Versions/A/WebKit:x86_64+0x338e4c4)
    #25 0x1ede07b75 in IPC::Connection::enqueueIncomingMessage(std::__1::unique_ptr<IPC::Decoder, std::__1::default_delete<IPC::Decoder> >)::$_16::operator()()+0x35 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebKit.framework/Versions/A/WebKit:x86_64+0x33a7b75)
    #26 0x1ede07adc in WTF::Detail::CallableWrapper<IPC::Connection::enqueueIncomingMessage(std::__1::unique_ptr<IPC::Decoder, std::__1::default_delete<IPC::Decoder> >)::$_16, void>::call()+0xc (/Users/ldd/work/WebKit/WebKitBuild/Release/WebKit.framework/Versions/A/WebKit:x86_64+0x33a7adc)
    #27 0x207346d1e in WTF::Function<void ()>::operator()() const+0x3e (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x3fd1e)
    #28 0x20740a4f7 in WTF::RunLoop::performWork()+0x317 (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x1034f7)
    #29 0x20740d5da in WTF::RunLoop::performWork(void*)+0xba (/Users/ldd/work/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:x86_64+0x1065da)
    #30 0x7ff80bd39763 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x10 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x7f763)
    #31 0x7ff80bd39712 in __CFRunLoopDoSource0+0x9c (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x7f712)
    #32 0x7ff80bd394ec in __CFRunLoopDoSources0+0xd3 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x7f4ec)
    #33 0x7ff80bd3816a in __CFRunLoopRun+0x3a0 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x7e16a)
    #34 0x7ff80bd3774f in CFRunLoopRunSpecific+0x22f (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x7d74f)
    #35 0x7ff80cb8c8b9 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:]+0xd7 (/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation:x86_64+0x5e8b9)
    #36 0x7ff80cc0f26b in -[NSRunLoop(NSRunLoop) run]+0x4b (/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation:x86_64+0xe126b)
    #37 0x7ff80b9d66bd in _xpc_objc_main+0x304 (/usr/lib/system/libxpc.dylib:x86_64+0x166bd)
    #38 0x7ff80b9d60d5 in xpc_main+0x62 (/usr/lib/system/libxpc.dylib:x86_64+0x160d5)
    #39 0x1eb92b6de in WebKit::XPCServiceMain(int, char const**)+0x27e (/Users/ldd/work/WebKit/WebKitBuild/Release/WebKit.framework/Versions/A/WebKit:x86_64+0xecb6de)
    #40 0x1eddb4eb8 in WKXPCServiceMain+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/WebKit.framework/Versions/A/WebKit:x86_64+0x3354eb8)
    #41 0x10bcfeea8 in main+0x8 (/Users/ldd/work/WebKit/WebKitBuild/Release/com.apple.WebKit.WebContent.xpc/Contents/MacOS/com.apple.WebKit.WebContent.Development:x86_64+0x100003ea8)
    #42 0x7ff80b92d30f  (<unknown module>)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/ldd/work/WebKit/WebKitBuild/Release/WebCore.framework/Versions/A/WebCore:x86_64+0x313351b) in WebCore::DOMWrapperWorld::~DOMWrapperWorld()+0x25b
Shadow bytes around the buggy address:
  0x1c5e0000f400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c5e0000f410: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c5e0000f420: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c5e0000f430: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c5e0000f440: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x1c5e0000f450: fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c5e0000f460: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c5e0000f470: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c5e0000f480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c5e0000f490: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c5e0000f4a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==815==ABORTING
2022-09-23 11:11:48.735 MiniBrowser[813:7927] WebContent process crashed; reloading
2022-09-23 11:11:49.347 com.apple.WebKit.WebContent.Development[825:8307] ApplePersistence=NO


## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 38.2 KB)
- [poc.html](attachments/poc.html) (text/plain, 833 B)

## Timeline

### [Deleted User] (2022-09-23)

[Empty comment from Monorail migration]

### hc...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-09-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4807592092303360.

### ro...@chromium.org (2022-09-24)

@ajuma can you take a look and file with WebKit if needed? I tried running locally on Safari/Chromium in the simulator and wasn't able to repro the crash. No crash on Clusterfuzz either.

### [Deleted User] (2022-09-24)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-09-26)

Local test env:

WebKit with Asan

commit e8982cd006743388b0a9204010bf3dc3bbb57cfa (HEAD -> main, origin/main, origin/HEAD) 
Author: Vitaly Dyachkov <vitaly@igalia.com>; 
Date: Tue Sep 13 03:32:30 2022 -0700

### aj...@chromium.org (2022-09-28)

Which revision of WebKit are you testing on (trunk?) and what version of iOS?

### m....@gmail.com (2022-09-28)

trunk and macos 13 beta


### mp...@chromium.org (2022-10-03)

[Empty comment from Monorail migration]

[Monorail components: Mobile>iOSWeb]

### [Deleted User] (2022-10-03)

[Empty comment from Monorail migration]

### aj...@chromium.org (2022-10-04)

Ah, the reason this doesn't repro in ClusterFuzz is that it requires clicking on the button (and then waiting 3.6 seconds). Doing that, I can repro locally on macOS 12.6.

### m....@gmail.com (2022-10-04)

My fault, forgot to mention this~

### aj...@chromium.org (2022-10-04)

I've filed https://bugs.webkit.org/show_bug.cgi?id=246022. Please let me know if you'd like to be cc'd on the bug.

### [Deleted User] (2022-10-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-04)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2022-10-04)

Removing RBS since this requires a fix to land in WebKit and then get shipped with an iOS update.

### [Deleted User] (2022-10-04)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-05)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2022-10-05)

Removing RBS again. This is not a bug that we are fixing inside Chromium.

### aj...@chromium.org (2022-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-06)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2022-10-26)

re https://crbug.com/chromium/1367125#c13 Please cc me on that issue

### aj...@chromium.org (2022-10-26)

Tried to cc you but got an error message about your account not being found. Please make sure you have an account at bugs.webkit.org (and let me know if the user id is different than the address you are using here).

### m....@gmail.com (2022-10-26)

I just registered, please try again

### aj...@chromium.org (2022-10-26)

Thanks, done.

### [Deleted User] (2022-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-12-20)

Apple has fixed the issue

Status:	RESOLVED FIXED

### aj...@chromium.org (2022-12-20)

Thanks for the update!

The link to the patch (https://commits.webkit.org/252432.807@safari-7614-branch) in the WebKit bug redirects to an Apple-internal repo that we can't see, so it looks like this has landed but not shipped anywhere yet. I'm going to wait until this makes it into a public beta before marking this fixed, to be on the safe side (i.e., to avoid starting the clock on making this public, when we don't know Apple's timeline for shipping the fix).

Setting a NextAction date to check if this fixed in a public build.

### aj...@chromium.org (2023-01-09)

Still no public releases with this fix. 

### aj...@chromium.org (2023-01-13)

The WebKit bug was updated to note that the patch was reverted, and is being re-landed (again in an Apple-internal repo).

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### aj...@chromium.org (2023-02-13)

WebKit bug is still open.

### aj...@chromium.org (2023-03-21)

The fix is still not released.

### aj...@chromium.org (2023-03-29)

Fixed in iOS 16.4. The patch has also landed in upstream WebKit now: https://commits.webkit.org/262247@main

### aj...@chromium.org (2023-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-30)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M110. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to other stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M111. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M112. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M113. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111, 112, 113].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2023-03-30)

Woah! This fix landed in WebKit and shipped with iOS 16.4. There is nothing for us to merge since we didn't make any change.

### go...@chromium.org (2023-03-31)

Thank you ajuma@.

+Amy (Security TPM) for visibility of https://crbug.com/chromium/1367125#c43. No merged needed here. 

### am...@chromium.org (2023-03-31)

Thanks for the update in comments #39 and #43 ajuma@! 
No merge needed, but into the vrp panel queue this does go. Thanks! 

### am...@google.com (2023-04-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-05)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us!

### am...@google.com (2023-04-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1367125?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061108)*

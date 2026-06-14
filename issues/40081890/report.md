# Heap-use-after-free in blink::SMILTimeContainer::updateAnimations

| Field | Value |
|-------|-------|
| **Issue ID** | [40081890](https://issues.chromium.org/issues/40081890) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>SVG |
| **Reporter** | at...@gmail.com |
| **Assignee** | fs...@opera.com |
| **Created** | 2015-04-19 |
| **Bounty** | $2,000.00 |

## Description



Tested on:

OS: Ubuntu 14.04

Chrome: asan-symbolized-linux-release-325771

Note: There is some timing condition in the repro-file. It prevents me from minimizing the file automatically, so I'll take a closer look manually when I have some spare time.

You need to hit refresh couple of times to reproduce the crash, so it might not reproduce on clusterfuzz. Also sometimes the crash occurs as a null-pointer and sometimes as an UAF.


ASAN-trace:(UAF)


==31305==ERROR: AddressSanitizer: heap-use-after-free on address 0x617000004860 at pc 0x7f20bdb75284 bp 0x7ffddd692af0 sp 0x7ffddd692ae8
READ of size 8 at 0x617000004860 thread T0 (chrome)
    #0 0x7f20bdb75283 in operator==<blink::SVGElement *, blink::QualifiedName> /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../buildtools/third_party/libc++/trunk/include/utility:405
    #1 0x7f20bdb74f9a in WTF::HashTableHelper<WTF::KeyValuePair<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > >, WTF::KeyValuePairKeyExtractor, WTF::HashTraits<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> > >::isEmptyOrDeletedBucket(WTF::KeyValuePair<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > > const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/HashTable.h:328
    #2 0x7f20bdb7a3c1 in WTF::HashTableConstIterator<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::KeyValuePair<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > >, WTF::KeyValuePairKeyExtractor, WTF::PairHash<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName>, WTF::HashMapValueTraits<WTF::HashTraits<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> >, WTF::HashTraits<WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > > >, WTF::HashTraits<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> >, WTF::DefaultAllocator>::skipEmptyBuckets() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/HashTable.h:120
    #3 0x7f20bdb7a5ce in WTF::HashTableConstIterator<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::KeyValuePair<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > >, WTF::KeyValuePairKeyExtractor, WTF::PairHash<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName>, WTF::HashMapValueTraits<WTF::HashTraits<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> >, WTF::HashTraits<WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > > >, WTF::HashTraits<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> >, WTF::DefaultAllocator>::operator++() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/HashTable.h:173
    #4 0x7f20bdb7a57a in WTF::HashTableIterator<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::KeyValuePair<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > >, WTF::KeyValuePairKeyExtractor, WTF::PairHash<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName>, WTF::HashMapValueTraits<WTF::HashTraits<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> >, WTF::HashTraits<WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > > >, WTF::HashTraits<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> >, WTF::DefaultAllocator>::operator++() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/HashTable.h:230
    #5 0x7f20bdb7132a in WTF::HashTableIteratorAdapter<WTF::HashTable<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::KeyValuePair<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > >, WTF::KeyValuePairKeyExtractor, WTF::PairHash<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName>, WTF::HashMapValueTraits<WTF::HashTraits<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> >, WTF::HashTraits<WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > > >, WTF::HashTraits<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> >, WTF::DefaultAllocator>, WTF::KeyValuePair<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > > >::operator++() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/HashIterators.h:73
    #6 0x7f20bdb6ee9f in updateAnimations /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/svg/animation/SMILTimeContainer.cpp:464 (discriminator 3)
    #7 0x7f20bdb7144a in blink::SMILTimeContainer::updateAnimationsAndScheduleFrameIfNeeded(blink::SMILTime, bool) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/svg/animation/SMILTimeContainer.cpp:432
    #8 0x7f20bdb6c2f4 in blink::SMILTimeContainer::wakeupTimerFired(blink::Timer<blink::SMILTimeContainer>*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/svg/animation/SMILTimeContainer.cpp:313
    #9 0x7f20c5c6b094 in blink::ThreadTimers::sharedTimerFiredInternal() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/ThreadTimers.cpp:137
    #10 0x7f20c5c6a80e in blink::ThreadTimers::sharedTimerFired() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/ThreadTimers.cpp:107
    #11 0x7f20c0a9c736 in content::BlinkPlatformImpl::DoTimeout() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/child/blink_platform_impl.h:178
    #12 0x7f20c0a9efb1 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (content::BlinkPlatformImpl::*)()>, base::internal::TypeList<content::BlinkPlatformImpl*> >::MakeItSo(base::internal::RunnableAdapter<void (content::BlinkPlatformImpl::*)()>, content::BlinkPlatformImpl*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/bind_internal.h:293
.
.
.
0x617000004860 is located 480 bytes inside of 768-byte region [0x617000004680,0x617000004980)
freed by thread T0 (chrome) here:
    #0 0x7f20b621e46b in __interceptor_free ??:?
    #1 0x7f20bdb74b63 in WTF::HashTable<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::KeyValuePair<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > >, WTF::KeyValuePairKeyExtractor, WTF::PairHash<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName>, WTF::HashMapValueTraits<WTF::HashTraits<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> >, WTF::HashTraits<WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > > >, WTF::HashTraits<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> >, WTF::DefaultAllocator>::rehash(unsigned int, WTF::KeyValuePair<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > >*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/HashTable.h:1148
    #2 0x7f20bdb74070 in WTF::HashTableAddResult<WTF::HashTable<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::KeyValuePair<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > >, WTF::KeyValuePairKeyExtractor, WTF::PairHash<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName>, WTF::HashMapValueTraits<WTF::HashTraits<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> >, WTF::HashTraits<WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > > >, WTF::HashTraits<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> >, WTF::DefaultAllocator>, WTF::KeyValuePair<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > > > WTF::HashTable<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::KeyValuePair<std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > >, WTF::KeyValuePairKeyExtractor, WTF::PairHash<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName>, WTF::HashMapValueTraits<WTF::HashTraits<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> >, WTF::HashTraits<WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > > >, WTF::HashTraits<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> >, WTF::DefaultAllocator>::add<WTF::HashMapTranslator<WTF::HashMapValueTraits<WTF::HashTraits<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> >, WTF::HashTraits<WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > > >, WTF::PairHash<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> >, std::__1::pair<blink::SVGElement*, blink::QualifiedName>, WTF::PassOwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > >(std::__1::pair<blink::SVGElement*, blink::QualifiedName> const&, WTF::PassOwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/HashTable.h:847
    #3 0x7f20bdb73cc1 in WTF::HashMap<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName>, WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> >, WTF::PairHash<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName>, WTF::HashTraits<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> >, WTF::HashTraits<WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > >, WTF::DefaultAllocator>::inlineAdd(std::__1::pair<blink::SVGElement*, blink::QualifiedName> const&, WTF::PassOwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> >&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/HashMap.h:359
    #4 0x7f20bdb6ca91 in WTF::HashMap<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName>, WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> >, WTF::PairHash<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName>, WTF::HashTraits<std::__1::pair<WTF::RawPtr<blink::SVGElement>, blink::QualifiedName> >, WTF::HashTraits<WTF::OwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> > >, WTF::DefaultAllocator>::add(std::__1::pair<blink::SVGElement*, blink::QualifiedName> const&, WTF::PassOwnPtr<WTF::LinkedHashSet<WTF::RawPtr<blink::SVGSMILElement>, WTF::PtrHash<WTF::RawPtr<blink::SVGSMILElement> >, WTF::HashTraits<WTF::RawPtr<blink::SVGSMILElement> >, WTF::DefaultAllocator> >) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/HashMap.h:386
    #5 0x7f20bdb6c7a8 in schedule /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/svg/animation/SMILTimeContainer.cpp:93
    #6 0x7f20bdb8c50e in schedule /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/svg/animation/SVGSMILElement.cpp:1326
    #7 0x7f20bda76ee1 in blink::SVGAnimationElement::setTargetElement(blink::SVGElement*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/svg/SVGAnimationElement.cpp:692
.
.
.


ASAN-trace:(null-pointer)

==30816==ERROR: AddressSanitizer: SEGV on unknown address 0x000000000000 (pc 0x7f321eca7727 bp 0x7fff4767ef30 sp 0x7fff4767ee60 T0)
    #0 0x7f321eca7726 in calculateAnimatedValue /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/svg/SVGAnimatedTypeAnimator.cpp:254
    #1 0x7f321ec9e5f7 in calculateAnimatedValue /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/svg/SVGAnimateElement.cpp:99
    #2 0x7f321ecb221f in blink::SVGAnimationElement::updateAnimation(float, unsigned int, blink::SVGSMILElement*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/svg/SVGAnimationElement.cpp:638
    #3 0x7f321edcffd5 in blink::SVGSMILElement::progress(blink::SMILTime, blink::SVGSMILElement*, bool) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/svg/animation/SVGSMILElement.cpp:1184
    #4 0x7f321edab09c in updateAnimations /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/svg/animation/SMILTimeContainer.cpp:490
    #5 0x7f321edad44a in blink::SMILTimeContainer::updateAnimationsAndScheduleFrameIfNeeded(blink::SMILTime, bool) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/svg/animation/SMILTimeContainer.cpp:432
    #6 0x7f321eda82f4 in blink::SMILTimeContainer::wakeupTimerFired(blink::Timer<blink::SMILTimeContainer>*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/svg/animation/SMILTimeContainer.cpp:313
    #7 0x7f3226ea7094 in blink::ThreadTimers::sharedTimerFiredInternal() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/ThreadTimers.cpp:137
.
.
.

## Attachments

- [chrome-heap-use-after-free-operatorblinkSVGElement.svg](attachments/chrome-heap-use-after-free-operatorblinkSVGElement.svg) (image/svg+xml, 135.6 KB)
- [chrome-heap-use-after-free-operatorblinkSVGElement-min.svg](attachments/chrome-heap-use-after-free-operatorblinkSVGElement-min.svg) (image/svg+xml, 56.4 KB)
- [chrome-heap-use-after-free-operatorblinkSVGElement-min.html](attachments/chrome-heap-use-after-free-operatorblinkSVGElement-min.html) (text/html, 542 B)

## Timeline

### in...@chromium.org (2015-04-19)

Kouhei@, you seem to have dived into this code recently, can you please take a look.

### at...@gmail.com (2015-04-20)


I did some work with the test case. At least on my laptop the crash reproduces reliably within 10s, when the file is loaded into Chrome. You could try the new repro-file on ClusterFuzz.

I reduced most of the JavaScript and some of the XML, but there is still some weird timing conditions.

JavaScript has one setInterval and two setTimeout left and SVG/XML has lots of animation timings.

JavaScript part doesn't touch any of the animation values, so I think that the timing condition is between the animations set in the SVG/XML and the DOM and style manipulations in JavaScript code.


### ko...@chromium.org (2015-04-20)

[Empty comment from Monorail migration]

### ko...@chromium.org (2015-04-20)

repro memo: Load the svg in debug content_shell and it will crash on ASSERT:
89          ASSERT(!m_preventScheduledAnimationsChanges);

#0  0x000000000b338d31 in blink::SMILTimeContainer::schedule (this=0x6120000accc0, animation=0x616000365180, target=0x616000365180, attributeName=...)
    at ../../third_party/WebKit/Source/core/svg/animation/SMILTimeContainer.cpp:89



### ko...@chromium.org (2015-04-20)

SMILTimeContainer::progress in the CSS animation may cause the target element render tree to be created in-place, and that may instantiate the use shadow tree which may contain <animate> elements which then need to be scheduled in the SMILTimeContainer.

We have to prevent this somewhere, but it is not obvious to me right away where is the right place to do.

### fe...@chromium.org (2015-04-21)

[Empty comment from Monorail migration]

### fe...@chromium.org (2015-04-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-21)

[Empty comment from Monorail migration]

### ko...@chromium.org (2015-04-23)

Workaround CL: https://codereview.chromium.org/1098913004/


### fs...@opera.com (2015-04-23)

To me it feels like we could block these (animation elements) when cloning the shadow-tree (isDisallowedElement in SVGUseElement.cpp)

### fs...@opera.com (2015-04-23)

nvm, looks like that's done already...

### fs...@opera.com (2015-04-23)

Looks like the TC has some <use> that directly reference animation elements (ID4 and ID28), and that clone+append doesn't appear directly guarded by isDisallowedElement (checked "after the fact").

### ko...@chromium.org (2015-04-23)

That would be easier if its acceptable.

The animation elements in the shadow tree may reference a different element, so blocking it would change behavior in some cases.

### ko...@chromium.org (2015-04-23)

Sorry please ignore #13.

Thanks for investigating. #12 seems to explain this bug. I'm onboarding to a flight now and will be offline for ~24hrs, so feel free to take this from me.

### fs...@opera.com (2015-04-23)

Will do.

### in...@chromium.org (2015-04-24)

[Empty comment from Monorail migration]

### fs...@opera.com (2015-04-24)

Reduced down to the attached, which seems to reproduce pretty reliably.

### fs...@opera.com (2015-04-24)

Reduced based on the assert in SMILTimeContainer::schedule I should've said.

### bu...@chromium.org (2015-04-25)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=194421

------------------------------------------------------------------
r194421 | fs@opera.com | 2015-04-25T01:10:46.501939Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGUseElement.cpp?r1=194421&r2=194420&pathrev=194421
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/custom/use-referencing-animation-crash-expected.txt?r1=194421&r2=194420&pathrev=194421
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/custom/use-referencing-animation-crash.html?r1=194421&r2=194420&pathrev=194421

Avoid transiently creating disallowed elements when building <use> trees

When building a shadow tree for a <use>, a direct reference to a
"disallowed" element would cause the element to first be inserted before
buildShadowTree() noticed it's disallowed and returns false, so it's
removed again.
This transient mutation could take place while computing an animation
update, if a CSS property was being animated and the layout tree/style
was dirty.
Avoid the insert-remove sequence by checking if the initial target is
disallowed up-front. This matches how it's done in the general subtree
building case inside buildShadowTree().

BUG=478549

Review URL: https://codereview.chromium.org/1105873002
-----------------------------------------------------------------

### in...@chromium.org (2015-04-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-25)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### fs...@opera.com (2015-05-06)

[Empty comment from Monorail migration]

### la...@google.com (2015-05-06)

[Automated comment] Less than 2 weeks to go before stable on M43, manual review required.

### la...@google.com (2015-05-06)

[Automated comment] Request affecting a post-stable build (M42), manual review required.

### la...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2015-05-06)

I don't plan to take this for M42 given where we are in the release cycle.  Ping me if you have any objections.

### bu...@chromium.org (2015-05-07)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=195031

------------------------------------------------------------------
r195031 | fs@opera.com | 2015-05-07T08:03:41.925923Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2357/LayoutTests/svg/custom/use-referencing-animation-crash.html?r1=195031&r2=195030&pathrev=195031
   M http://src.chromium.org/viewvc/blink/branches/chromium/2357/Source/core/svg/SVGUseElement.cpp?r1=195031&r2=195030&pathrev=195031
   A http://src.chromium.org/viewvc/blink/branches/chromium/2357/LayoutTests/svg/custom/use-referencing-animation-crash-expected.txt?r1=195031&r2=195030&pathrev=195031

Merge 194421 "Avoid transiently creating disallowed elements whe..."

> Avoid transiently creating disallowed elements when building <use> trees
> 
> When building a shadow tree for a <use>, a direct reference to a
> "disallowed" element would cause the element to first be inserted before
> buildShadowTree() noticed it's disallowed and returns false, so it's
> removed again.
> This transient mutation could take place while computing an animation
> update, if a CSS property was being animated and the layout tree/style
> was dirty.
> Avoid the insert-remove sequence by checking if the initial target is
> disallowed up-front. This matches how it's done in the general subtree
> building case inside buildShadowTree().
> 
> BUG=478549
> 
> Review URL: https://codereview.chromium.org/1105873002

TBR=fs@opera.com

Review URL: https://codereview.chromium.org/1134453003
-----------------------------------------------------------------

### ti...@google.com (2015-05-11)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-28)

$2000 for this one.

Notes from reward panel: "$2,000 here as UaF is less reliable".

### ti...@google.com (2015-06-25)

Processing rewards - should be paid in approximately 2 weeks.

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### cl...@chromium.org (2015-08-01)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/478549?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081890)*

# Heap-use-after-free in void blink::ImageDecodingStore::insertCacheInternal<blink::ImageDecodingSto

| Field | Value |
|-------|-------|
| **Issue ID** | [40080933](https://issues.chromium.org/issues/40080933) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **Reporter** | ao...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2014-11-30 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0

Steps to reproduce the problem:
1. chrome-asan ch-uaf-DoublyLinkedListNode.gif

What is the expected behavior?
Tab lives.

What went wrong?
Tab dies.

Did this work before? N/A 

Chrome version: 41.0.2234.0 (Developer Build)   Channel: n/a
OS Version: 
Flash Version: 

==6618==ERROR: AddressSanitizer: heap-use-after-free on address 0x6060001091e0 at pc 0x7f10a0a02de9 bp 0x7f1063ffd4c0 sp 0x7f1063ffd4b8
WRITE of size 8 at 0x6060001091e0 thread T6 (CompositorRaste)
    #0 0x7f10a0a02de8 in WTF::DoublyLinkedListNode<blink::ImageDecodingStore::CacheEntry>::setNext(blink::ImageDecodingStore::CacheEntry*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/DoublyLinkedList.h:56
    #1 0x7f10a09f7397 in WTF::DoublyLinkedList<blink::ImageDecodingStore::CacheEntry>::append(blink::ImageDecodingStore::CacheEntry*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/DoublyLinkedList.h:156
    #2 0x7f10a09f7c9f in void blink::ImageDecodingStore::insertCacheInternal<blink::ImageDecodingStore::DecoderCacheEntry, WTF::HashMap<std::__1::pair<blink::ImageFrameGenerator const*, SkTSize<int> >, WTF::OwnPtr<blink::ImageDecodingStore::DecoderCacheEntry>, WTF::PairHash<blink::ImageFrameGenerator const*, SkTSize<int> >, WTF::HashTraits<std::__1::pair<blink::ImageFrameGenerator const*, SkTSize<int> > >, WTF::HashTraits<WTF::OwnPtr<blink::ImageDecodingStore::DecoderCacheEntry> >, WTF::DefaultAllocator>, WTF::HashMap<blink::ImageFrameGenerator const*, WTF::HashSet<std::__1::pair<blink::ImageFrameGenerator const*, SkTSize<int> >, WTF::PairHash<blink::ImageFrameGenerator const*, SkTSize<int> >, WTF::HashTraits<std::__1::pair<blink::ImageFrameGenerator const*, SkTSize<int> > >, WTF::DefaultAllocator>, WTF::PtrHash<blink::ImageFrameGenerator const*>, WTF::HashTraits<blink::ImageFrameGenerator const*>, WTF::HashTraits<WTF::HashSet<std::__1::pair<blink::ImageFrameGenerator const*, SkTSize<int> >, WTF::PairHash<blink::ImageFrameGenerator const*, SkTSize<int> >, WTF::HashTraits<std::__1::pair<blink::ImageFrameGenerator const*, SkTSize<int> > >, WTF::DefaultAllocator> >, WTF::DefaultAllocator> >(WTF::PassOwnPtr<blink::ImageDecodingStore::DecoderCacheEntry>, WTF::HashMap<std::__1::pair<blink::ImageFrameGenerator const*, SkTSize<int> >, WTF::OwnPtr<blink::ImageDecodingStore::DecoderCacheEntry>, WTF::PairHash<blink::ImageFrameGenerator const*, SkTSize<int> >, WTF::HashTraits<std::__1::pair<blink::ImageFrameGenerator const*, SkTSize<int> > >, WTF::HashTraits<WTF::OwnPtr<blink::ImageDecodingStore::DecoderCacheEntry> >, WTF::DefaultAllocator>*, WTF::HashMap<blink::ImageFrameGenerator const*, WTF::HashSet<std::__1::pair<blink::ImageFrameGenerator const*, SkTSize<int> >, WTF::PairHash<blink::ImageFrameGenerator const*, SkTSize<int> >, WTF::HashTraits<std::__1::pair<blink::ImageFrameGenerator const*, SkTSize<int> > >, WTF::DefaultAllocator>, WTF::PtrHash<blink::ImageFrameGenerator const*>, WTF::HashTraits<blink::ImageFrameGenerator const*>, WTF::HashTraits<WTF::HashSet<std::__1::pair<blink::ImageFrameGenerator const*, SkTSize<int> >, WTF::PairHash<blink::ImageFrameGenerator const*, SkTSize<int> >, WTF::HashTraits<std::__1::pair<blink::ImageFrameGenerator const*, SkTSize<int> > >, WTF::DefaultAllocator> >, WTF::DefaultAllocator>*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/ImageDecodingStore.cpp:224
    #3 0x7f10a09f75bb in blink::ImageDecodingStore::insertDecoder(blink::ImageFrameGenerator const*, WTF::PassOwnPtr<blink::ImageDecoder>) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/ImageDecodingStore.cpp:103
    #4 0x7f10a09de7fe in blink::ImageFrameGenerator::tryToResumeDecode(SkTSize<int> const&, unsigned long) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/ImageFrameGenerator.cpp:253
    #5 0x7f10a09dde45 in blink::ImageFrameGenerator::decodeAndScale(SkImageInfo const&, unsigned long, void*, unsigned long) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/ImageFrameGenerator.cpp:134
    #6 0x7f10a09f54c4 in onGetPixels /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/DecodingImageGenerator.cpp:82
[...]

## Attachments

- [ch-uaf-DoublyLinkedListNode.gif](attachments/ch-uaf-DoublyLinkedListNode.gif) (image/gif, 471.3 KB)

## Timeline

### in...@chromium.org (2014-11-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-30)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4510988152864768

### in...@chromium.org (2014-11-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-30)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4510988152864768

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x60c00022cde0
Crash State:
  void blink::ImageDecodingStore::insertCacheInternal<blink::ImageDecodingSto
  blink::ImageDecodingStore::insertDecoder
  blink::ImageFrameGenerator::tryToResumeDecode
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=266423:266861

Minimized Testcase (471.26 Kb): https://cluster-fuzz.appspot.com/download/AMIfv977lT3pYUs-JFpqh26yFRxAWicp4tiPoK2KgO-LVLa-2C4BD80b73_cG_WTohfTqVor8HVnh5VS5eGF5fXIoO6knJCRN93WyvPjw35Zfjq7RI6FRVOxd3FiI_uhGHU0JH2YQJ1Goarywkdn-IjXMpxdCR_Ev5bN9MHdzHni2IV3v1kFGo4



### cl...@chromium.org (2014-11-30)

[Empty comment from Monorail migration]

### no...@chromium.org (2014-12-01)

Thanks for the report.  +reveman +hclam, could one of take it please?  Assign to Dave for the moment, reassign as you see fit.

### cl...@chromium.org (2014-12-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4510988152864768

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x60c00020ede0
Crash State:
  void blink::ImageDecodingStore::insertCacheInternal<blink::ImageDecodingSto
  blink::ImageDecodingStore::insertDecoder
  blink::ImageFrameGenerator::tryToResumeDecode
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=266423:266861

Minimized Testcase (471.26 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94XvKANp3bVnA183ijlI0loh_ccfO3dRGyQdvG-zINZ6mfkG3877YZNVLIijBBUgtuxpgJ6SsWJlzWIxxCIxNFHTy1nMLPEtHl44lZWZbFZZXS8jy2slwskHusu-idTJvpnhB0Jumqqyt_yNNaMcAWYwev1ziRlIjPt-dOoFR7jru-TMjQ



### cl...@chromium.org (2014-12-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-08)

reveman@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-16)

reveman@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-12-18)

Author: sohan.jyoti@samsung.com
Component: chromium
Changelist: https://chromium.googlesource.com/chromium/src//+/cfa7fd92d44fd9254bfbbeeb9a4940425520d887
Time: Tue Apr 29 11:50:03 2014
File layer_tree_host_impl.cc is changed in this cl (and is part of stack frame #8, "cc::LayerTreeHostImpl::CreateResourceAndRasterWorkerPool"; frame #9, "cc::LayerTreeHostImpl::CreateAndSetTileManager"; frame #10, "cc::LayerTreeHostImpl::InitializeRenderer")
Minimum distance from crash line to modified line: 729. (file: layer_tree_host_impl.cc, crashed on: 1957, modified: 1228).

### cl...@chromium.org (2014-12-18)

reveman@: Uh oh! This issue is still open and hasn't been updated in the last 17 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-19)

reveman@: Uh oh! This issue is still open and hasn't been updated in the last 17 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### re...@chromium.org (2014-12-22)

I've been able to reproduce this and it seems like
ImageDecodingStore::insertCacheInternal is inserting an entry in cacheMap with the same key as an already existing entry and that is causing the existing value to unexpectedly be destroyed. Not sure yet why this is happening. Alpha, could you take a look?

### cl...@chromium.org (2015-01-06)

hclam@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-01-07)

No more M39 patches, moving to M40.

### [Deleted User] (2015-01-07)

Staring to look into it now.

### [Deleted User] (2015-01-08)

[Empty comment from Monorail migration]

### [Deleted User] (2015-01-08)

The file is a broken GIF which triggers a bug in decoding. I have a that fixes the bug in decoding. It might fix the issue found in ImageDecodingStore.

### bu...@chromium.org (2015-01-14)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=188423

------------------------------------------------------------------
r188423 | hclam@chromium.org | 2015-01-14T23:28:11.533345Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/image-decoders/gif/GIFImageReader.cpp?r1=188423&r2=188422&pathrev=188423
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/image-decoders/gif/GIFImageDecoderTest.cpp?r1=188423&r2=188422&pathrev=188423
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/image-decoders/testing/first-frame-has-greater-size-than-screen-size.gif?r1=188423&r2=188422&pathrev=188423
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/image-decoders/gif/GIFImageReader.h?r1=188423&r2=188422&pathrev=188423

Fix handling of broken GIFs with weird frame sizes

Code didn't handle well if a GIF frame has dimension greater than the
"screen" dimension. This will break deferred image decoding.

This change reports the size as final only when the first frame is
encountered.

Added a test to verify this behavior. Frame size reported by the decoder
should be constant.

BUG=437651
R=pkasting@chromium.org, senorblanco@chromium.org

Review URL: https://codereview.chromium.org/813943003
-----------------------------------------------------------------

### in...@chromium.org (2015-01-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-15)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-01-16)

ClusterFuzz has detected this issue as fixed in range 311576:311657.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4510988152864768

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x60c00022cea0
Crash State:
  void blink::ImageDecodingStore::insertCacheInternal<blink::ImageDecodingSto
  blink::ImageDecodingStore::insertDecoder
  blink::ImageFrameGenerator::tryToResumeDecode
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=266423:266861
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=311576:311657

Minimized Testcase (471.26 Kb): https://cluster-fuzz.appspot.com/download/AMIfv972EE7Ocb5aINqfGI1wHU5L-Q4Jlq6PTKhXsNvMxgnHJT80vc34YPiwSCm7Iuw_BCJnQnJqZjXxR2lY_ZSbWq06LKkhaDda0asjjWDHdYS7QGClV_m3qf9lVygg1kwhzPiSPfe2JX5MzanlbM3Ne7amo2oIu2xFkw5JIxF9s_r68NSpJfg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### pe...@google.com (2015-01-25)

[Automated comment] Request affecting a post-stable build (M40), manual review required.

### pe...@google.com (2015-01-25)

Approved for M41 (branch: 2272)

### bu...@chromium.org (2015-01-29)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189154

------------------------------------------------------------------
r189154 | pennymac@google.com | 2015-01-29T02:29:40.066741Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/platform/image-decoders/gif/GIFImageReader.cpp?r1=189154&r2=189153&pathrev=189154
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/platform/image-decoders/gif/GIFImageDecoderTest.cpp?r1=189154&r2=189153&pathrev=189154
   A http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/platform/image-decoders/testing/first-frame-has-greater-size-than-screen-size.gif?r1=189154&r2=189153&pathrev=189154
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/platform/image-decoders/gif/GIFImageReader.h?r1=189154&r2=189153&pathrev=189154

Merge 188423 into M41 branch 2272: "Fix handling of broken GIFs with weird frame sizes"

> Fix handling of broken GIFs with weird frame sizes
> 
> Code didn't handle well if a GIF frame has dimension greater than the
> "screen" dimension. This will break deferred image decoding.
> 
> This change reports the size as final only when the first frame is
> encountered.
> 
> Added a test to verify this behavior. Frame size reported by the decoder
> should be constant.
> 
> BUG=437651
> R=pkasting@chromium.org, senorblanco@chromium.org
> 
> Review URL: https://codereview.chromium.org/813943003

TBR=hclam@chromium.org

Review URL: https://codereview.chromium.org/868803008
-----------------------------------------------------------------

### dx...@chromium.org (2015-02-03)

too risky for m40.  

### pe...@chromium.org (2015-02-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-03)

Congratulations - $3000 for this report (reward panel notes: higher amount as not in partition).

### ao...@gmail.com (2015-03-03)

Awesome :)

### ti...@google.com (2015-03-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-15)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### ti...@google.com (2015-04-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-23)

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

This issue was migrated from crbug.com/chromium/437651?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080933)*

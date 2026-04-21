# Security: heap-use-after-free in blink::FormData::append form_data.cc:151

| Field | Value |
|-------|-------|
| **Issue ID** | [40075982](https://issues.chromium.org/issues/40075982) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection, Blink>Network>FetchAPI |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2023-10-31 |
| **Bounty** | $10,000.00 |

## Description

heap-use-after-free in blink::FormData::append form_data.cc:151

#Teston
1217490 Winx64

#Reproduce
install node&puppeteer-core
python -m http.server 1337
node 1031.js chrome.exe http://localhost:1337/poc.html

##Note
Because the test case reproduction is unstable, I have written an automation test script using puppeteer-core.

#Minicase
Coming soon

#RCA
Coming soon

#ASAN
=================================================================
==19136==ERROR: AddressSanitizer: heap-use-after-free on address 0x1198ecad6da0 at pc 0x7ff9728bfc68 bp 0x00144e1fce30 sp 0x00144e1fce78
READ of size 8 at 0x1198ecad6da0 thread T0
==19136==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff9728bfc67 in blink::MakeGarbageCollected<blink::FormData::Entry,WTF::String,WTF::String> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\heap\garbage_collected.h:37
    #1 0x7ff9728bf5b4 in blink::FormData::append C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\forms\form_data.cc:151
    #2 0x7ff9747bf0de in blink::`anonymous namespace'::BodyFormDataConsumer::DidFetchDataLoadedString C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\fetch\body.cc:139
    #3 0x7ff978516132 in blink::`anonymous namespace'::FetchDataLoaderAsString::OnStateChange C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\fetch\fetch_data_loader.cc:508
    #4 0x7ff971ece3d9 in blink::BodyStreamBuffer::StartLoading C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\fetch\body_stream_buffer.cc:275
    #5 0x7ff9747b71aa in blink::Body::formData C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\fetch\body.cc:288
    #6 0x7ff9747a5dec in blink::`anonymous namespace'::v8_response::FormDataOperationCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\core\v8\v8_response.cc:398
    #7 0x7ff97ce85f12 in Builtins_CallApiCallbackGeneric+0xd2 (D:\chrome_asan\asan-win32-release_x64-1215390\chrome.dll+0x1a5215f12)
    #8 0x7ff9dce8aa8c  (<unknown module>)

0x1198ecad6da0 is located 16 bytes inside of 48-byte region [0x1198ecad6d90,0x1198ecad6dc0)
freed by thread T0 here:
    #0 0x7ff66d6e19ad in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ff96c539cf9 in WTF::ConditionalDestructor<WTF::Vector<std::__Cr::pair<WTF::String,WTF::String>,0,WTF::PartitionAllocator>,1>::~ConditionalDestructor C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\conditional_destructor.h:21
    #2 0x7ff9784ecef0 in blink::URLSearchParams::~URLSearchParams C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\url\url_search_params.cc:116
    #3 0x7ff95e7a4147 in cppgc::internal::HeapVisitor<cppgc::internal::(anonymous namespace)::MutatorThreadSweeper>::Traverse C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\heap-visitor.h:47
    #4 0x7ff95e798f34 in cppgc::internal::Sweeper::SweeperImpl::SweepForAllocationIfRunning C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc:881
    #5 0x7ff95e782e32 in cppgc::internal::ObjectAllocator::TryRefillLinearAllocationBuffer C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\object-allocator.cc:217
    #6 0x7ff95e7819ff in cppgc::internal::ObjectAllocator::OutOfLineAllocateImpl C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\object-allocator.cc:173
    #7 0x7ff95e78121f in cppgc::internal::ObjectAllocator::OutOfLineAllocateGCSafePoint C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\object-allocator.cc:121
    #8 0x7ff95e74f33f in cppgc::internal::MakeGarbageCollectedTraitInternal::Allocate C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\allocation.cc:38
    #9 0x7ff9728bfab7 in blink::MakeGarbageCollected<blink::FormData::Entry,WTF::String,WTF::String> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\heap\garbage_collected.h:37
    #10 0x7ff9728bf5b4 in blink::FormData::append C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\forms\form_data.cc:151
    #11 0x7ff9747bf0de in blink::`anonymous namespace'::BodyFormDataConsumer::DidFetchDataLoadedString C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\fetch\body.cc:139
    #12 0x7ff978516132 in blink::`anonymous namespace'::FetchDataLoaderAsString::OnStateChange C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\fetch\fetch_data_loader.cc:508
    #13 0x7ff971ece3d9 in blink::BodyStreamBuffer::StartLoading C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\fetch\body_stream_buffer.cc:275
    #14 0x7ff9747b71aa in blink::Body::formData C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\fetch\body.cc:288
    #15 0x7ff9747a5dec in blink::`anonymous namespace'::v8_response::FormDataOperationCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\core\v8\v8_response.cc:398
    #16 0x7ff97ce85f12 in Builtins_CallApiCallbackGeneric+0xd2 (D:\chrome_asan\asan-win32-release_x64-1215390\chrome.dll+0x1a5215f12)
    #17 0x7ff9dce8aa8c  (<unknown module>)

previously allocated by thread T0 here:
    #0 0x7ff66d6e1aad in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ff957c9d339 in partition_alloc::PartitionRoot::Alloc<0> C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_root.h:461
    #2 0x7ff96462f331 in WTF::Vector<std::__Cr::pair<WTF::String,WTF::String>,0,WTF::PartitionAllocator>::ReallocateBuffer C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\vector.h:2289
    #3 0x7ff96462f1c0 in WTF::Vector<std::__Cr::pair<WTF::String,WTF::String>,0,WTF::PartitionAllocator>::ExpandCapacity C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\vector.h:1775
    #4 0x7ff96462efab in WTF::Vector<std::__Cr::pair<WTF::String,WTF::String>,0,WTF::PartitionAllocator>::AppendSlowCase<std::__Cr::pair<WTF::String,WTF::String> > C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\vector.h:1984
    #5 0x7ff9784e734c in blink::URLSearchParams::AppendWithoutUpdate C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\url\url_search_params.cc:186
    #6 0x7ff9784e7fec in blink::URLSearchParams::SetInputWithoutUpdate C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\url\url_search_params.cc:168
    #7 0x7ff9784e75ef in blink::URLSearchParams::URLSearchParams C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\url\url_search_params.cc:102
    #8 0x7ff9747bf06a in blink::`anonymous namespace'::BodyFormDataConsumer::DidFetchDataLoadedString C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\fetch\body.cc:138
    #9 0x7ff978516132 in blink::`anonymous namespace'::FetchDataLoaderAsString::OnStateChange C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\fetch\fetch_data_loader.cc:508
    #10 0x7ff971ece3d9 in blink::BodyStreamBuffer::StartLoading C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\fetch\body_stream_buffer.cc:275
    #11 0x7ff9747b71aa in blink::Body::formData C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\fetch\body.cc:288
    #12 0x7ff9747a5dec in blink::`anonymous namespace'::v8_response::FormDataOperationCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\core\v8\v8_response.cc:398
    #13 0x7ff97ce85f12 in Builtins_CallApiCallbackGeneric+0xd2 (D:\chrome_asan\asan-win32-release_x64-1215390\chrome.dll+0x1a5215f12)
    #14 0x7ff9dce8aa8c  (<unknown module>)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\heap\garbage_collected.h:37 in blink::MakeGarbageCollected<blink::FormData::Entry,WTF::String,WTF::String>
Shadow bytes around the buggy address:
  0x1198ecad6b00: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd
  0x1198ecad6b80: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fa
  0x1198ecad6c00: fa fa 00 00 00 00 00 00 fa fa fd fd fd fd fd fa
  0x1198ecad6c80: fa fa 00 00 00 00 00 05 fa fa 00 00 00 00 00 fa
  0x1198ecad6d00: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fa
=>0x1198ecad6d80: fa fa fd fd[fd]fd fd fd fa fa fd fd fd fd fd fd
  0x1198ecad6e00: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd
  0x1198ecad6e80: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fa
  0x1198ecad6f00: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd
  0x1198ecad6f80: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd
  0x1198ecad7000: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd
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

==19136==ADDITIONAL INFO

==19136==Note: Please include this section with the ASan report.
Task trace:


==19136==END OF ADDITIONAL INFO
==19136==ABORTING


## Attachments

- [poc.js](attachments/poc.js) (text/plain, 21.4 KB)
- [poc.html](attachments/poc.html) (text/plain, 162 B)
- [h1.js](attachments/h1.js) (text/plain, 1017 B)
- [testharness.js](attachments/testharness.js) (text/plain, 181.1 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 8.8 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2023-10-31)

[Empty comment from Monorail migration]

### m....@gmail.com (2023-10-31)

#RCA
"The URLSearchParams::Create function call returns an on-heap object [2]. 
However, this on-heap object is not held in the DidFetchDataLoadedString function [1],
causing a Use-After-Free (UAF) when the GC is triggered [3], resulting in the memory referenced by name and value being freed."

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/fetch/body.cc;drc=719c18366c0226fa751f38693b00f822d1b7ea9b;l=138
void DidFetchDataLoadedString(const String& string) override {
	auto* formData = MakeGarbageCollected<FormData>();
	for (const auto& pair : URLSearchParams::Create(string)->Params())	<<----[1]
		formData->append(pair.first, pair.second);
	DidFetchDataLoadedFormData(formData);
}

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/url/url_search_params.h;drc=719c18366c0226fa751f38693b00f822d1b7ea9b;l=46
static URLSearchParams* Create(const String& query_string,
                                 DOMURL* url_object = nullptr) {
    return MakeGarbageCollected<URLSearchParams>(query_string, url_object);	<<----[2]
}

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/html/forms/form_data.cc;drc=719c18366c0226fa751f38693b00f822d1b7ea9b;l=151
void FormData::append(const String& name, const String& value) {
  entries_.push_back(MakeGarbageCollected<Entry>(name, value)); <<----[3]
}

### m....@gmail.com (2023-10-31)

My fix patch
https://chromium-review.googlesource.com/c/chromium/src/+/4995224

### cl...@chromium.org (2023-10-31)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4652622703689728.

### xi...@chromium.org (2023-10-31)

Thanks for the report. Looping in Blink>Network>FetchAPI owners to take a look.

[Monorail components: Blink>Network>FetchAPI]

### [Deleted User] (2023-10-31)

[Empty comment from Monorail migration]

### m....@gmail.com (2023-11-01)

The problematic code was introduced a long time ago, making it difficult to pinpoint the exact commit. However, during my testing, I found that it can be triggered as early as version asan-win32-release_x64-1174590.

### dc...@chromium.org (2023-11-01)

Oilpan team might be interested in this.

This is kind of interesting because the original code looks like this:

```
    for (const auto& pair : URLSearchParams::Create(string)->Params())
```
and a proposed fix looks like this:
```
    auto* search_params = URLSearchParams::Create(string);
    for (const auto& pair : search_params->Params())
```

Params() is a reference to a field inside URLSearchParams, allocated on the Oilpan heap. The reference should be in a register or on the stack, but it seems like URLSearchParams is being collected and finalized, which would seem to indicate that the GC is not finding it?

Is this expected?

[Monorail components: Blink>GarbageCollection]

### ri...@chromium.org (2023-11-01)

As `search_params` is never read from after looking up the `begin` and `end` iterators, the compiler is not required to retain it on the stack, so the conservative GC may not find it.

I believe the fix here to be safe: https://chromium-review.googlesource.com/c/chromium/src/+/4996929

### [Deleted User] (2023-11-01)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2023-11-01)

(I am a bot: this is an auto-cc on a security bug)

### ml...@chromium.org (2023-11-02)

From skimming the issue:

WTF::Vector (w/ PartitionAllocator) iterators are non managed (just like regular C++ iterators) and will not keep their underlying data structure alive (i.e. they don't provide temporal memory safety). Users need to manage liveness of the container themselves. With URLParams being GCed this becomes tricky. The CL with the fix will work.

That said, we haven't made a guideline here but HeapVector will be strictly better when used from GCed objects. We do support them for non-traceable types (e.g. pair<String, String>). Some properties:
1. Fix this case (see below);
2. Don't add dtors to the surrounding GCed object;
3. Support compaction;
4. Support inline growing (opportunistically);
5. Support eager freeing if necessary (using .clear());

Ad 1.: Iterators for HeapVector provide temporal memory safety and keep their backing store alive even if the surrounding HeapVector and/or GCed objects are gone. As such, they would support this case in that URLParams would be reclaimed but the iterator is perfectly fine to use here. 

So far the motivation for HeapVector of non-traceable types was just performancee. This is the first case where it would have also prevented a correctness issue.

### gi...@appspot.gserviceaccount.com (2023-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8b1bd7726a1394e2fe287f6a882822d8ee9d4e96

commit 8b1bd7726a1394e2fe287f6a882822d8ee9d4e96
Author: Nidhi Jaju <nidhijaju@chromium.org>
Date: Thu Nov 02 08:16:57 2023

Make URLSearchParams persistent to avoid UaF

The URLSearchParams::Create() function returns an on-heap object, but it
can be garbage collected, so making it a persistent variable in
DidFetchDataLoadedString() mitigates the issue.

Bug: 1497997
Change-Id: I229efec33451792a10a185cb2f9aa37dd0579823
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4996929
Reviewed-by: Adam Rice <ricea@chromium.org>
Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1218682}

[modify] https://crrev.com/8b1bd7726a1394e2fe287f6a882822d8ee9d4e96/third_party/blink/renderer/core/fetch/body.cc


### ni...@chromium.org (2023-11-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-07)

Requesting merge to extended stable M118 because latest trunk commit (1218682) appears to be after extended stable branch point (1192594).

Requesting merge to stable M119 because latest trunk commit (1218682) appears to be after stable branch point (1204232).

Requesting merge to beta M120 because latest trunk commit (1218682) appears to be after beta branch point (1217362).

Merge review required: M118 is already shipping to stable.

Merge review required: M119 is already shipping to stable.

Merge review required: M120 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [118, 119, 120].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-07)

merges approved for https://crrev.com/c/4996929
please merge this fix to 120 Beta / branch 6099 at soonest so this fix can be included in the next 120 Beta update tomorrow
please merge this fix to 119 Stable / branch 6045 and 118 Extended / branch 5993 at your earliest convenience (before EOD Thursday, 9 November) so this fix can be included in the next Stable and Extended Stable security updates 

### gi...@appspot.gserviceaccount.com (2023-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9384cddc77054d9935d5a1217ca9510180be0714

commit 9384cddc77054d9935d5a1217ca9510180be0714
Author: Nidhi Jaju <nidhijaju@chromium.org>
Date: Wed Nov 08 04:19:31 2023

[Merge to M118] Make URLSearchParams persistent to avoid UaF

The URLSearchParams::Create() function returns an on-heap object, but it
can be garbage collected, so making it a persistent variable in
DidFetchDataLoadedString() mitigates the issue.

(cherry picked from commit 8b1bd7726a1394e2fe287f6a882822d8ee9d4e96)

Bug: 1497997
Change-Id: I4ae0f93fccc561cd8a088d3fa0bf2968bf298acf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4996929
Reviewed-by: Adam Rice <ricea@chromium.org>
Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1218682}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5007484
Commit-Queue: Adam Rice <ricea@chromium.org>
Auto-Submit: Nidhi Jaju <nidhijaju@chromium.org>
Cr-Commit-Position: refs/branch-heads/5993@{#1546}
Cr-Branched-From: 511350718e646be62331ae9d7213d10ec320d514-refs/heads/main@{#1192594}

[modify] https://crrev.com/9384cddc77054d9935d5a1217ca9510180be0714/third_party/blink/renderer/core/fetch/body.cc


### [Deleted User] (2023-11-08)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1e397bbaaeddaee77b2381a4cd9e030c6948301c

commit 1e397bbaaeddaee77b2381a4cd9e030c6948301c
Author: Nidhi Jaju <nidhijaju@chromium.org>
Date: Wed Nov 08 06:37:19 2023

[Merge to M119] Make URLSearchParams persistent to avoid UaF

The URLSearchParams::Create() function returns an on-heap object, but it
can be garbage collected, so making it a persistent variable in
DidFetchDataLoadedString() mitigates the issue.

(cherry picked from commit 8b1bd7726a1394e2fe287f6a882822d8ee9d4e96)

Bug: 1497997
Change-Id: I3c27ba18b9c46d22d841e06f4a91bcc360aad287
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4996929
Reviewed-by: Adam Rice <ricea@chromium.org>
Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1218682}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5009227
Commit-Queue: Adam Rice <ricea@chromium.org>
Auto-Submit: Nidhi Jaju <nidhijaju@chromium.org>
Cr-Commit-Position: refs/branch-heads/6045@{#1260}
Cr-Branched-From: 905e8bdd32d891451d94d1ec71682e989da2b0a1-refs/heads/main@{#1204232}

[modify] https://crrev.com/1e397bbaaeddaee77b2381a4cd9e030c6948301c/third_party/blink/renderer/core/fetch/body.cc


### gi...@appspot.gserviceaccount.com (2023-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6e10e71e613f792ad031e3ab47bba66c05bc2964

commit 6e10e71e613f792ad031e3ab47bba66c05bc2964
Author: Nidhi Jaju <nidhijaju@chromium.org>
Date: Wed Nov 08 06:37:01 2023

[Merge to M120] Make URLSearchParams persistent to avoid UaF

The URLSearchParams::Create() function returns an on-heap object, but it
can be garbage collected, so making it a persistent variable in
DidFetchDataLoadedString() mitigates the issue.

(cherry picked from commit 8b1bd7726a1394e2fe287f6a882822d8ee9d4e96)

Bug: 1497997
Change-Id: I3d393b991ba885bf5bcadd765f5e5aea312d0670
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4996929
Reviewed-by: Adam Rice <ricea@chromium.org>
Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1218682}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5009226
Auto-Submit: Nidhi Jaju <nidhijaju@chromium.org>
Commit-Queue: Adam Rice <ricea@chromium.org>
Cr-Commit-Position: refs/branch-heads/6099@{#359}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[modify] https://crrev.com/6e10e71e613f792ad031e3ab47bba66c05bc2964/third_party/blink/renderer/core/fetch/body.cc


### [Deleted User] (2023-11-08)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1497997&entry.364066060=External&entry.958145677=Android&entry.958145677=Chrome&entry.958145677=Linux&entry.958145677=Mac&entry.958145677=Windows&entry.958145677=Lacros&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>GarbageCollection,Blink>Network>FetchAPI&entry.975983575=nidhijaju@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-11-08)

[Empty comment from Monorail migration]

### rz...@google.com (2023-11-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-08)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-11-08)

1. Just https://crrev.com/c/5013923
2. Low, no conflicts
3. 118, 119
4. Yes

### gm...@google.com (2023-11-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-11-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-09)

Congratulations! The Chrome VRP Panel has decided to award you $10,000 for this high quality report of renderer memory corruption. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-11-11)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-13)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-15)

[Empty comment from Monorail migration]

### na...@google.com (2023-11-21)

[Empty comment from Monorail migration]

### na...@google.com (2023-11-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3b59c7729c2863194a8ea97a81c8f4df037ae36c

commit 3b59c7729c2863194a8ea97a81c8f4df037ae36c
Author: Nidhi Jaju <nidhijaju@chromium.org>
Date: Fri Nov 24 15:24:52 2023

[M114-LTS] Make URLSearchParams persistent to avoid UaF

The URLSearchParams::Create() function returns an on-heap object, but it
can be garbage collected, so making it a persistent variable in
DidFetchDataLoadedString() mitigates the issue.

(cherry picked from commit 8b1bd7726a1394e2fe287f6a882822d8ee9d4e96)

Bug: 1497997
Change-Id: I229efec33451792a10a185cb2f9aa37dd0579823
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4996929
Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1218682}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5013923
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1643}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/3b59c7729c2863194a8ea97a81c8f4df037ae36c/third_party/blink/renderer/core/fetch/body.cc


### vo...@google.com (2023-11-28)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1497997?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>GarbageCollection, Blink>Network>FetchAPI]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40075982)*

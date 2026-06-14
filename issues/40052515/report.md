# Security: global-buffer-overflow in bytesPerVertex

| Field | Value |
|-------|-------|
| **Issue ID** | [40052515](https://issues.chromium.org/issues/40052515) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | br...@google.com |
| **Created** | 2020-06-08 |
| **Bounty** | $1,000.00 |

## Description

This issue was found by fuzzing against a 64-bit asan linux build of fuzz.

**VERSION**  

chrome 83.0.4103.97 (stable)

**REPRODUCTION CASE**

download <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-stable-83.0.4103.97.zip>

./filter\_fuzz\_stub global-buffer-overflow-bytesPerVertex.fil

==2001456==ERROR: AddressSanitizer: global-buffer-overflow on address 0x555b9e940a78 at pc 0x555b9f07119a bp 0x7fff1a8b83b0 sp 0x7fff1a8b83a8  

READ of size 8 at 0x555b9e940a78 thread T0  

#0 0x555b9f071199 in bytesPerVertex third\_party/skia/src/core/SkVertices.cpp:42:5  

#1 0x555b9f071199 in custom\_data\_size third\_party/skia/src/core/SkVertices.cpp:55:26  

#2 0x555b9f071199 in SkVertices::Sizes::Sizes(SkVertices::Desc const&) third\_party/skia/src/core/SkVertices.cpp:81:27  

#3 0x555b9f073bcc in SkVertices::Decode(void const\*, unsigned long) third\_party/skia/src/core/SkVertices.cpp:433:11  

#4 0x555b9f147ac4 in create\_vertices\_from\_buffer(SkReadBuffer&) third\_party/skia/src/core/SkPictureData.cpp:379:19  

#5 0x555b9f147602 in bool new\_array\_from\_buffer<SkVertices const, SkVertices>(SkReadBuffer&, unsigned int, SkTArray<sk\_sp<SkVertices const>, false>&, sk\_sp<SkVertices> (\*)(SkReadBuffer&)) third\_party/skia/src/core/SkPictureData.cpp:398:20  

#6 0x555b9f146b11 in SkPictureData::parseBufferTag(SkReadBuffer&, unsigned int, unsigned int) third\_party/skia/src/core/SkPictureData.cpp:443:13  

#7 0x555b9f148a7e in parseBuffer third\_party/skia/src/core/SkPictureData.cpp:525:15  

#8 0x555b9f148a7e in SkPictureData::CreateFromBuffer(SkReadBuffer&, SkPictInfo const&) third\_party/skia/src/core/SkPictureData.cpp:494:16  

#9 0x555b9f141407 in SkPicturePriv::MakeFromBuffer(SkReadBuffer&) third\_party/skia/src/core/SkPicture.cpp:213:40  

#10 0x555b9f21f10a in (anonymous namespace)::SkPictureImageFilterImpl::CreateProc(SkReadBuffer&) third\_party/skia/src/effects/imagefilters/SkPictureImageFilter.cpp:86:19  

#11 0x555b9ef462cd in SkReadBuffer::readFlattenable(SkFlattenable::Type) third\_party/skia/src/core/SkReadBuffer.cpp:428:15  

#12 0x555b9edf25d7 in SkFlattenable::Deserialize(SkFlattenable::Type, void const\*, unsigned long, SkDeserialProcs const\*) third\_party/skia/src/core/SkFlattenable.cpp:144:40  

#13 0x555b9ecfe9f8 in Deserialize third\_party/skia/include/core/SkImageFilter.h:149:17  

#14 0x555b9ecfe9f8 in RunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:32:38  

#15 0x555b9ecfe9f8 in ReadAndRunTestCase skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:66:3  

#16 0x555b9ecfe9f8 in main skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:86:10  

#17 0x7f38771a11a2 in \_\_libc\_start\_main (/lib64/libc.so.6+0x271a2)

0x555b9e940a78 is located 40 bytes to the left of global variable '<string literal>' defined in '../../third\_party/skia/src/core/SkXfermode.cpp:70:43' (0x555b9e940aa0) of size 8  

'<string literal>' is ascii string 'DstOver'  

0x555b9e940a78 is located 16 bytes to the right of global variable '<string literal>' defined in '../../third\_party/skia/src/core/SkXfermode.cpp:70:32' (0x555b9e940a60) of size 8  

'<string literal>' is ascii string 'SrcOver'  

SUMMARY: AddressSanitizer: global-buffer-overflow third\_party/skia/src/core/SkVertices.cpp:42:5 in bytesPerVertex  

Shadow bytes around the buggy address:  

0x0aabf3d200f0: f9 f9 f9 f9 00 00 00 00 00 00 00 00 00 00 04 f9  

0x0aabf3d20100: f9 f9 f9 f9 00 00 00 00 00 f9 f9 f9 f9 f9 f9 f9  

0x0aabf3d20110: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0aabf3d20120: 01 f9 f9 f9 f9 f9 f9 f9 00 00 00 00 00 00 00 00  

0x0aabf3d20130: 00 00 00 00 06 f9 f9 f9 f9 f9 f9 f9 04 f9 f9 f9  

=>0x0aabf3d20140: f9 f9 f9 f9 04 f9 f9 f9 f9 f9 f9 f9 00 f9 f9[f9]  

0x0aabf3d20150: f9 f9 f9 f9 00 f9 f9 f9 f9 f9 f9 f9 06 f9 f9 f9  

0x0aabf3d20160: f9 f9 f9 f9 06 f9 f9 f9 f9 f9 f9 f9 07 f9 f9 f9  

0x0aabf3d20170: f9 f9 f9 f9 07 f9 f9 f9 f9 f9 f9 f9 00 f9 f9 f9  

0x0aabf3d20180: f9 f9 f9 f9 00 f9 f9 f9 f9 f9 f9 f9 04 f9 f9 f9  

0x0aabf3d20190: f9 f9 f9 f9 05 f9 f9 f9 f9 f9 f9 f9 00 01 f9 f9  

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

Shadow gap: cc  

==2001456==ABORTING

testcase is in the attachment. Thanks

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### cl...@chromium.org (2020-06-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5690634914037760.

### cl...@chromium.org (2020-06-08)

Testcase 5690634914037760 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5690634914037760.

### cl...@chromium.org (2020-06-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5712211521110016.

### mb...@chromium.org (2020-06-08)

Tentatively assigning this one to myself as well while ClusterFuzz tries to track down the CL that fixed it. This one also seems to affect stable but not head, so if there is any work to do here it would just be a merge.

### mb...@chromium.org (2020-06-08)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia]

### cl...@chromium.org (2020-06-09)

Detailed Report: https://clusterfuzz.com/testcase?key=5712211521110016

Fuzzer: 
Job Type: linux_asan_filter_fuzz_stub
Platform Id: linux

Crash Type: Global-buffer-overflow READ 8
Crash Address: 0x55df43e129f8
Crash State:
  SkVertices::Sizes::Sizes
  SkVertices::Decode
  create_vertices_from_buffer
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=755716:755721

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5712211521110016

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5712211521110016 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2020-06-09)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-09)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-06-09)

ClusterFuzz testcase 5712211521110016 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_filter_fuzz_stub&range=756886:756888

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2020-06-10)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-12)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M84. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-12)

This bug requires manual review: M84's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2020-06-12)

+Adetaylor@(Security TPM) for Merge decision. Thank you.

### ad...@chromium.org (2020-06-12)

This is a duplicate of something in this fix range... I will track it down...
https://skia.googlesource.com/skia/+log/6d3bc2951dd61e25752a7370b56880222517654e..afbf2aa737c8f0b48dfa28c88c51f56a46d32843?pretty=fuller&n=10000

Please hold, your merge request is important to us...

### ad...@chromium.org (2020-06-12)

OK. I am not sure exactly which commit fixed it but it was something in

https://bugs.chromium.org/p/skia/issues/detail?id=9984

That's the general ticket for progress in this area, rather than a specific report of this bug, so I don't consider this to be a duplicate.

Per the regression range in https://crbug.com/chromium/1092274#c6 this regressed in M83, and per the fix range in https://crbug.com/chromium/1092274#c9 it was fixed in M84. There's therefore no need to merge the fix here to M84, and we've just missed the final M83 respin so I'm not going to consider merging this back to M83.

### zh...@gmail.com (2020-06-15)

Hi team，

Thanks for fixing this issue, as it affects stable edition, could I request a CVE for this issue?

### ad...@chromium.org (2020-06-15)

Hi, yes, we will allocate a CVE when we release M84. https://chromiumdash.appspot.com/schedule says ~Jul 14th.

### na...@google.com (2020-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-06-24)

Congrats! The Panel decided to award $1,000 for this report

### na...@google.com (2020-06-24)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-07-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1092274?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052515)*

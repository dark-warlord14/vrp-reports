# SEGV in media::InMemoryUrlProtocol::Read

| Field | Value |
|-------|-------|
| **Issue ID** | [40079360](https://issues.chromium.org/issues/40079360) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebAudio |
| **Reporter** | as...@hofaware.de |
| **Assignee** | ac...@chromium.org |
| **Created** | 2014-04-16 |
| **Bounty** | $1,000.00 |

## Description

Looks like a heap overflow.

**VERSION**  

Chrome Version: Version 36.0.1940.0 aura (263620) ASAN Build  

Operating System: Ubuntu 12.04 64 Bit

REPRO:

<html><script>

var r0=new AudioContext();  

var r33=new ArrayBuffer(2147483649);  

r0.decodeAudioData(r33,function(){});

</script></body></html>

ASAN:

==26680==ERROR: AddressSanitizer: SEGV on unknown address 0x625000380000 (pc 0x7f655531e587 sp 0x7f651cdf01a8 bp 0x7f651cdf0a10 T9)  

#0 0x7f655531e586 in **sanitizer::internal\_memcpy(void\*, void const\*, unsigned long) /usr/local/google/home/thakis/src/chrome/src/third\_party/llvm/projects/compiler-rt/lib/sanitizer\_common/sanitizer\_libc.cc:54  

#1 0x7f65552f9ae9 in memcpy *asan\_rtl*  

#2 0x7f65608a7c7b in media::InMemoryUrlProtocol::Read(int, unsigned char\*) /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../media/filters/in\_memory\_url\_protocol.cc:24  

#3 0x7f6558aad9fa in media::AVIOReadOperation(void\*, unsigned char\*, int) /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/../../media/filters/ffmpeg\_glue.cc:24  

#4 0x7f6558aae167 in media::FFmpegGlue::OpenContext() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../media/filters/ffmpeg\_glue.cc:166  

#5 0x7f65608322fb in media::AudioFileReader::Open() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../media/filters/audio\_file\_reader.cc:35  

#6 0x7f655f26f70c in content::DecodeAudioFileData(blink::WebAudioBus\*, char const\*, unsigned long) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../content/renderer/media/audio\_decoder.cc:39  

#7 0x7f6558c0d1e1 in WebCore::decodeAudioFileData(char const\*, unsigned long) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/platform/audio/AudioBus.cpp:641  

#8 0x7f6558c0d6d1 in WebCore::createBusFromInMemoryAudioFile(void const\*, unsigned long, bool, float) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/platform/audio/AudioBus.cpp:666  

#9 0x7f655b9b8065 in WebCore::AudioBuffer::createFromAudioFileData(void const\*, unsigned long, bool, float) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/modules/webaudio/AudioBuffer.cpp:69  

#10 0x7f655bab5b25 in WebCore::AsyncAudioDecoder::decode(WTF::ArrayBuffer\*, float, WebCore::AudioBufferCallback\*, WebCore::AudioBufferCallback\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/modules/webaudio/AsyncAudioDecoder.cpp:67

## Timeline

### cl...@chromium.org (2014-04-16)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=4655488530644992

### in...@chromium.org (2014-04-16)

Looks like acolwell@ wrote this code. Aaron, can you please take a look.

### in...@chromium.org (2014-04-16)

weird, ASAN reproduce this on Beta (35.0.1916.27), but not on trunk.

### da...@chromium.org (2014-04-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-04-16)

This is too flaky on clusterfuzz :(

### fe...@chromium.org (2014-04-17)

Provisionally labeling this as Medium severity. Aaron, can you look into this and verify that this isn't leading later to an out of bounds write?

### rt...@chromium.org (2014-04-17)

Is it possible to create an ArrayBuffer of that size?  When I try this in JS console in ToT chromium Linux build(yesterday), I get "RangeError: Invalid array buffer length"

### as...@hofaware.de (2014-04-17)

It's possible with the 64 bit version.

### cl...@chromium.org (2014-04-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-24)

acolwell@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ac...@chromium.org (2014-04-28)

[Empty comment from Monorail migration]

### ac...@chromium.org (2014-04-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-04-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ecc4d3b3f6f131387b8c0e01598a702a09e259d9

commit ecc4d3b3f6f131387b8c0e01598a702a09e259d9
Author: acolwell@chromium.org <acolwell@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Wed Apr 30 18:56:22 2014 +0000

Fix InMemoryUrlProtocol available_bytes computation.

Fixed available_bytes computation to properly handle large buffers and
add defensive logic to Read() to protect against negative sizes.

BUG=364065
TESTS=InMemoryUrlProtocolTest.*

Review URL: https://codereview.chromium.org/253923002

git-svn-id: svn://svn.chromium.org/chrome/trunk/src@267280 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-04-30)

------------------------------------------------------------------
r267280 | acolwell@chromium.org | 2014-04-30T18:56:22.686393Z

Changed paths:
   A http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/in_memory_url_protocol_unittest.cc?r1=267280&r2=267279&pathrev=267280
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/in_memory_url_protocol.cc?r1=267280&r2=267279&pathrev=267280
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/media.gyp?r1=267280&r2=267279&pathrev=267280

Fix InMemoryUrlProtocol available_bytes computation.

Fixed available_bytes computation to properly handle large buffers and
add defensive logic to Read() to protect against negative sizes.

BUG=364065
TESTS=InMemoryUrlProtocolTest.*

Review URL: https://codereview.chromium.org/253923002
-----------------------------------------------------------------

### in...@chromium.org (2014-04-30)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-04-30)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-05-01)

This won't make M34, but should make M35 after baking.

### ti...@chromium.org (2014-05-05)

Merge requested for M35 (branch 1916).

### ka...@google.com (2014-05-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-05-06)

------------------------------------------------------------------
r268594 | acolwell@chromium.org | 2014-05-06T19:59:26.841388Z

Changed paths:
   A http://src.chromium.org/viewvc/chrome/branches/1916/src/media/filters/in_memory_url_protocol_unittest.cc?r1=268594&r2=268593&pathrev=268594
   M http://src.chromium.org/viewvc/chrome/branches/1916/src/media/filters/in_memory_url_protocol.cc?r1=268594&r2=268593&pathrev=268594
   M http://src.chromium.org/viewvc/chrome/branches/1916/src/media/media.gyp?r1=268594&r2=268593&pathrev=268594

Merge 267280 "Fix InMemoryUrlProtocol available_bytes computation."

> Fix InMemoryUrlProtocol available_bytes computation.
> 
> Fixed available_bytes computation to properly handle large buffers and
> add defensive logic to Read() to protect against negative sizes.
> 
> BUG=364065
> TESTS=InMemoryUrlProtocolTest.*
> 
> Review URL: https://codereview.chromium.org/253923002

TBR=acolwell@chromium.org

Review URL: https://codereview.chromium.org/269953007
-----------------------------------------------------------------

### bu...@chromium.org (2014-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/73cb8e4fdbb96c28e5d280d5dcd6f8812b77253a

commit 73cb8e4fdbb96c28e5d280d5dcd6f8812b77253a
Author: acolwell@chromium.org <acolwell@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Tue May 06 19:59:26 2014 +0000

Merge 267280 "Fix InMemoryUrlProtocol available_bytes computation."

> Fix InMemoryUrlProtocol available_bytes computation.
> 
> Fixed available_bytes computation to properly handle large buffers and
> add defensive logic to Read() to protect against negative sizes.
> 
> BUG=364065
> TESTS=InMemoryUrlProtocolTest.*
> 
> Review URL: https://codereview.chromium.org/253923002

TBR=acolwell@chromium.org

Review URL: https://codereview.chromium.org/269953007

git-svn-id: svn://svn.chromium.org/chrome/branches/1916/src@268594 0039d316-1c4b-4281-b951-d872f2087c98



### ti...@chromium.org (2014-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-05-07)

ClusterFuzz has detected this issue as fixed in range 265382:266423.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4655488530644992

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: 
Crash Address: 
Crash State:
  - crash stack -
  
Regressed: https://cluster-fuzz.appspot.com//revisions?job=linux_asan_chrome_mp&range=254148:254228
Fixed: https://cluster-fuzz.appspot.com//revisions?job=linux_asan_chrome_mp&range=265382:266423

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95bfNYAak0BcC17sIdVMUiTU0I959KzLyLiZJVDypnnnBFNux1ocpILt7aJ146_39XyqwBE9Le7erFLSPliXSudJsUAlRfSp2yXAr9jIPHY_lKm1haddcNYcPeBE7rJmMcyWbQ_lf2uTeHBeqwmxVxap5zuhQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-05-13)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-05-16)

ashi@ - What name/handle would you like to be credited under in our release notes?

### as...@hofaware.de (2014-05-17)

As Holger Fuhrmannek

### ti...@chromium.org (2014-05-19)

Congrats - $1000 for this report! The release notes should be going out tomorrow and someone from our finance area will be in contact in the next week or two regarding payment.

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-09)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-09-06)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/364065?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079360)*

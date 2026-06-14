# Security: Use-of-uninitialized-value on Heap

| Field | Value |
|-------|-------|
| **Issue ID** | [40089027](https://issues.chromium.org/issues/40089027) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ku...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2017-09-15 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS

Analysis done on LINUX System, Only the reporting was done on Windows System.

PoC has been tested on latest Chrome Linux "MSAN" build (#502326) as of Sept 15 4:15PM PST. 

Build links have been shared in the Step 1 of the "Reproduction Case" section.

VERSION
Chrome Version: Latest Linux "MSAN" release build.

Operating System: Ubuntu

REPRODUCTION CASE

1. Download latest chrome "MSAN" build from https://www.googleapis.com/download/storage/v1/b/chromium-browser-msan/o/linux-release%2Fmsan-chained-origins-linux-release-502326.zip?generation=1505510729205749&alt=media

2. Unzip the downloaded "msan" builds.

3. Change directory to filter_fuzz_stub location.

4. Run the filter_fuzz_stub binary against the New_Msan_PoC2.fil testcase file.

5. Check the crash details in the terminal window.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Binary crashes and displays Warning of Use-Of-Uninitialized-Value.

See output below: -

root@kush:~/Desktop# /root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub /root/Desktop/fil_msan/New_Msan_PoC2.fil
[0915/153811.601814:INFO:filter_fuzz_stub.cc(60)] Test case: /root/Desktop/fil_msan/New_Msan_PoC2.fil
[0915/153811.605503:INFO:filter_fuzz_stub.cc(37)] Valid stream detected.
==30516==WARNING: MemorySanitizer: use-of-uninitialized-value
    #0 0x8ec803  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x8ec803)
    #1 0x8c9cef  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x8c9cef)
    #2 0xe46c85  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0xe46c85)
    #3 0x7cccef  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x7cccef)
    #4 0x7cdd98  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x7cdd98)
    #5 0x62eb2f  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x62eb2f)
    #6 0xd0e86a  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0xd0e86a)
    #7 0xd10ec9  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0xd10ec9)
    #8 0x61f2e7  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x61f2e7)
    #9 0x5addee  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x5addee)
    #10 0x5995ea  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x5995ea)
    #11 0xf7bee6  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0xf7bee6)
    #12 0x658e01  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x658e01)
    #13 0xd136a1  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0xd136a1)
    #14 0x5af3ce  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x5af3ce)
    #15 0x59bc8a  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x59bc8a)
    #16 0x493a8e  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x493a8e)
    #17 0x7f7e5de7b2b0  (/lib/x86_64-linux-gnu/libc.so.6+0x202b0)
    #18 0x424c79  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x424c79)

  Uninitialized value was created by a heap allocation
    #0 0x4923f9  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x4923f9)
    #1 0x618895  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x618895)
    #2 0x6192c2  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x6192c2)
    #3 0x563254  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x563254)
    #4 0xe5134a  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0xe5134a)
    #5 0xf7adea  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0xf7adea)
    #6 0x83bf60  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x83bf60)
    #7 0x64d90b  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x64d90b)
    #8 0x49341e  (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x49341e)
    #9 0x7f7e5de7b2b0  (/lib/x86_64-linux-gnu/libc.so.6+0x202b0)

SUMMARY: MemorySanitizer: use-of-uninitialized-value (/root/Desktop/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x8ec803) 
Exiting
root@kali:~/Desktop#


## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### ku...@gmail.com (2017-09-15)

Hello Google Product Security Team,

Good Evening.

I just noticed that there was a more recent release (#502343) right after my report.

I would like to confirm that the issue is consistently reproducible in the most latest release i.e. build #502343 available at https://www.googleapis.com/download/storage/v1/b/chromium-browser-msan/o/linux-release%2Fmsan-chained-origins-linux-release-502343.zip?generation=1505516956191346&alt=media

Thanks,
~ Kushal.

### me...@google.com (2017-09-16)

Thanks for the report. Adding reed@ to confirm.

[Monorail components: Internals>Skia]

### pa...@chromium.org (2017-09-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-09-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5573869816774656.

### pa...@chromium.org (2017-09-19)

[Empty comment from Monorail migration]

### ku...@gmail.com (2017-09-20)

Hello @reed, @palmer, @meacer, Google Product Security Team [skia],

Good Evening.

I would like to confirm that the crash is consistently reproducible on the latest Chrome MSAN "Beta" build available at https://www.googleapis.com/download/storage/v1/b/chromium-browser-msan/o/linux-release%2Fmsan-linux-beta-62.0.3202.18.zip?generation=1505796962687871&alt=media

Thanks,
~ Kushal.

### pa...@chromium.org (2017-09-21)

I downloaded https://www.googleapis.com/download/storage/v1/b/chromium-browser-msan/o/linux-release%2Fmsan-chained-origins-linux-release-502326.zip?generation=1505510729205749&alt=media and got this:

=====
~/Downloads/test/msan-chained-origins-linux-release-502326 $ ./filter_fuzz_stub ~/Downloads/New_Msan_PoC2.fil 
[0920/173925.105009:INFO:filter_fuzz_stub.cc(60)] Test case: /usr/local/google/home/palmer/Downloads/New_Msan_PoC2.fil
[0920/173925.123986:INFO:filter_fuzz_stub.cc(37)] Valid stream detected.
==106740==WARNING: MemorySanitizer: use-of-uninitialized-value
    #0 0x8ec803 in round third_party/skia/src/jumper/SkJumper_vectors.h:438:41
    #1 0x8ec803 in store_bgra_k third_party/skia/src/jumper/SkJumper_stages.cpp:982
    #2 0x8ec803 in sk_store_bgra third_party/skia/src/jumper/SkJumper_stages.cpp:979
    #3 0x8c9cef in sk_start_pipeline third_party/skia/src/jumper/SkJumper_stages.cpp:87:13
    #4 0xe46c85 in operator() buildtools/third_party/libc++/trunk/include/functional:1924:12
    #5 0xe46c85 in SkRasterPipelineBlitter::blitRect(int, int, int, int) third_party/skia/src/core/SkRasterPipelineBlitter.cpp:333
    #6 0x7cccef in blitrect third_party/skia/src/core/SkScan.cpp:25:14
    #7 0x7cccef in SkScan::FillIRect(SkIRect const&, SkRegion const*, SkBlitter*) third_party/skia/src/core/SkScan.cpp:40
    #8 0x7cdd98 in FillRect third_party/skia/src/core/SkScan.cpp:71:5
    #9 0x7cdd98 in SkScan::FillRect(SkRect const&, SkRasterClip const&, SkBlitter*) third_party/skia/src/core/SkScan.cpp:113
    #10 0x62eb2f in SkDraw::drawRect(SkRect const&, SkPaint const&, SkMatrix const*, SkRect const*) const third_party/skia/src/core/SkDraw.cpp:805:21
    #11 0xd0e86a in drawRect third_party/skia/src/core/SkDraw.h:42:15
    #12 0xd0e86a in SkBitmapDevice::drawRect(SkRect const&, SkPaint const&) third_party/skia/src/core/SkBitmapDevice.cpp:195
    #13 0xd10ec9 in SkBitmapDevice::drawBitmapRect(SkBitmap const&, SkRect const*, SkRect const&, SkPaint const&, SkCanvas::SrcRectConstraint) third_party/skia/src/core/SkBitmapDevice.cpp:349:11
    #14 0x61f2e7 in SkBaseDevice::drawImageRect(SkImage const*, SkRect const*, SkRect const&, SkPaint const&, SkCanvas::SrcRectConstraint) third_party/skia/src/core/SkDevice.cpp:195:15
    #15 0x5addee in SkCanvas::onDrawImageRect(SkImage const*, SkRect const*, SkRect const&, SkPaint const*, SkCanvas::SrcRectConstraint) third_party/skia/src/core/SkCanvas.cpp:2252:23
    #16 0x5995ea in SkCanvas::drawImageRect(SkImage const*, SkRect const&, SkRect const&, SkPaint const*, SkCanvas::SrcRectConstraint) third_party/skia/src/core/SkCanvas.cpp:1774:11
    #17 0xf7bee6 in SkImageSource::onFilterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/effects/SkImageSource.cpp:127:13
    #18 0x658e01 in SkImageFilter::filterImage(SkSpecialImage*, SkImageFilter::Context const&, SkIPoint*) const third_party/skia/src/core/SkImageFilter.cpp:212:40
    #19 0xd136a1 in SkBitmapDevice::drawSpecial(SkSpecialImage*, int, int, SkPaint const&, SkImage*, SkMatrix const&) third_party/skia/src/core/SkBitmapDevice.cpp:421:33
    #20 0x5af3ce in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const*) third_party/skia/src/core/SkCanvas.cpp:2298:27
    #21 0x59bc8a in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const*) third_party/skia/src/core/SkCanvas.cpp:1831:11
    #22 0x493a8e in RunTestCase skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:47:13
    #23 0x493a8e in ReadAndRunTestCase skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:66
    #24 0x493a8e in main skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:85
    #25 0x7f269acebf44 in __libc_start_main /build/eglibc-SvCtMH/eglibc-2.19/csu/libc-start.c:287
    #26 0x424c79 in _start (/usr/local/google/home/palmer/Downloads/test/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x424c79)

  Uninitialized value was created by a heap allocation
    #0 0x4923f9 in operator new(unsigned long) (/usr/local/google/home/palmer/Downloads/test/msan-chained-origins-linux-release-502326/filter_fuzz_stub+0x4923f9)
    #1 0x618895 in SkData::PrivateNewWithCopy(void const*, unsigned long) third_party/skia/src/core/SkData.cpp:69:21
    #2 0x6192c2 in SkData::MakeUninitialized(unsigned long) third_party/skia/src/core/SkData.cpp:104:12
    #3 0x563254 in SkBitmap::ReadRawPixels(SkReadBuffer*, SkBitmap*) third_party/skia/src/core/SkBitmap.cpp:687:24
    #4 0xe5134a in SkReadBuffer::readImage() third_party/skia/src/core/SkReadBuffer.cpp:294:13
    #5 0xf7adea in SkImageSource::CreateProc(SkReadBuffer&) third_party/skia/src/effects/SkImageSource.cpp:66:33
    #6 0x83bf60 in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) third_party/skia/src/core/SkValidatingReadBuffer.cpp:301:11
    #7 0x64d90b in SkValidatingDeserializeFlattenable third_party/skia/src/core/SkFlattenableSerialization.cpp:26:19
    #8 0x64d90b in SkValidatingDeserializeImageFilter(void const*, unsigned long) third_party/skia/src/core/SkFlattenableSerialization.cpp:30
    #9 0x49341e in RunTestCase skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:32:38
    #10 0x49341e in ReadAndRunTestCase skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:66
    #11 0x49341e in main skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:85
    #12 0x7f269acebf44 in __libc_start_main /build/eglibc-SvCtMH/eglibc-2.19/csu/libc-start.c:287

SUMMARY: MemorySanitizer: use-of-uninitialized-value third_party/skia/src/jumper/SkJumper_vectors.h:438:41 in round
Exiting
=====

So at least we have symbols now. +mtklein, who seems to have touched the top few stack frames' code recently.

Given the code at SkJumper_vectors.h:438, I'd guess? that it's machine-specific code expecting to get register-sized values and instead getting a value smaller than that, and doing a less-than-word-size OOB read? I'm not sure. Skia crew obviously are better people to diagnose, so I'll stop. :)

### [Deleted User] (2017-09-21)

Hmm.  Usually these problems are way up the stack and a bit back in time, when a buffer should have been initialized but wasn't.  When there are bugs way low down like this, they usually affect everything catastrophically.

But in this case, we recently switched Chrome MSAN builds from testing scalar code (not very realistic) to testing SSE2 (somewhat more realistic).  This did introduce the possibility of false positives in MSAN.  If MSAN considers round() (i.e. _mm_cvtps_epi32 / cvtps2dq) to be an interesting "use" of uninitialized memory, it very well could explain this.  Sometimes when using SSE near the edge of a buffer we'll ignore one or more upper lanes, never loading them from or storing them to memory, but continue to do math on them blindly.  Ordinarily those lanes are initialized to zero, but it's possible a path slipped through here that left them uninitialized.

We've also seen MSAN just not understand some instructions, but that's always been in later instruction sets.  I would think it's got SSE2 down solid.

I'm going to have to see if I can reproduce this locally to figure out if that's what's going on.  If it is, there's no correctness or security issue here, but it would represent a _performance_ issue.  If we leave register lanes uninitialized, that can create a false data dependency between consecutive iterations of our loops, which means the CPU can't run "ahead" and execute independent loops independently.  This kills the IPC.  :(

### pa...@chromium.org (2017-09-21)

#8: Thanks. Yeah, I've seen an "uninitialized use" of memory just like this once before, in audio processing code. Fun — I would not have realized it could be a performance concern! Thanks for the analysis.

I don't know whether MSan would 'know' about SSE2 or other particular instruction sets' behaviors. For that, +kcc, who might be able to shed some light.

But it sounds like this is unlikely to be a security concern. Unless kcc has exciting information :) I'll remove the security labels after a while.

### [Deleted User] (2017-09-21)

It's still more likely that this is just an uninitialized buffer, which I guess could still be a security concern?

### kc...@chromium.org (2017-09-21)

> MSan would 'know' about SSE2 
MSan should know about anything that is a compiler-intrinsic. 
But it knows nothing about inline assembly or pre-compiled binaries. 
Which one is used here? Is a minimized case possible? 
(I may not have time to reproduce in chrome, sorry)

### [Deleted User] (2017-09-21)

This is a mix of Clang vector extensions and intrinsics from immintrin.h compiled for -msse2 (but not above).  Does MSAN consider _mm_cvtps_epi32() something to report about?

We've seen situations where MSAN did not understand some instructions, I think maybe,
  - F16<->F32 conversions
  - mask loads and stores
  - (masked) gathers



### kc...@chromium.org (2017-09-21)

+eugenis for the specific question on _mm_cvtps_epi32

I can see this code in lib/Transforms/Instrumentation/MemorySanitizer.cpp:
    case llvm::Intrinsic::x86_sse_cvtps2pi:
    case llvm::Intrinsic::x86_sse_cvttps2pi:
      handleVectorConvertIntrinsic(I, 2);
      break;


### eu...@chromium.org (2017-09-21)

MemorySanitizer treats _mm_cvtps_epi32 as an "interesting use" of the entire input register, because floating point to integer conversion may trigger a invalid-operation exception (when input if nan, inf, or out of bounds for the destination type).

Scalar conversion is not treated the same way for some reason. Maybe it should.


### [Deleted User] (2017-09-21)

Ah, gotcha, that certainly helps explain what's going on here.

But yeah, it is a little surprising that cvtss... is uninteresting and cvtps... is interesting.

### pa...@chromium.org (2017-09-21)

#10: Since it's "blindly doing math" on in-bounds but uninitialized bytes/things, *and not doing anything else with them*, this seems to be to only be a correctness problem (re: #14) and not a security problem.

If we treated that uninitialized stuff as a pointer, array index, enum value later used in a switch/case, et c., then yes. But I gather this is all about putting pixels on the screen, and not influencing control flow. If I have that right, we can take the security labels off of this bug.

### kc...@chromium.org (2017-09-21)

>> putting pixels on the screen

Can't resist:
https://googleprojectzero.blogspot.com/2014/08/what-does-pointer-look-like-anyway.html

### pa...@chromium.org (2017-09-21)

The classics never die. :)

### ku...@gmail.com (2017-09-21)

@palmer, #9 & #16: I fail to understand why you seem to be in such a hurry to label this Vulnerability report as a non-security bug??

@kcc, nice share indeed!!!:)

Here are some [previously accepted and thereafter fixed] reference bugs, before the "apparent" hurry to close this one as not a security-bug.

crbug.com/727678
crbug.com/726199
crbug.com/725127
crbug.com/714374
crbug.com/710082
crbug.com/717935

Thanks,
~ Kushal.

### pa...@chromium.org (2017-09-21)

#19: Not all uses of uninitialized data are security vulnerabilities. (And not all the bugs you list were accepted or rewarded as such.)

I'm in a hurry to correctly triage all the bugs in my queue, not to potentially-incorrectly mark bugs as non-security.

If you look at the fixes for the bugs you list that have fixes, you can see that they were clear cases of uninitialized data, in ways that could at least in principle have an effect on control flow or some other security-relevant property. It's not clear that that's the case here.

(If you're thinking of pointers leaking as pixels, and that that might be useful in an ASLR bypass: I don't yet see an indication that it's *pointers*, or other sensitive data, in the uninitialized data. If you think the data are sensitive in some way, and if you can get them to leak, that'd be a great bug report.)

### ku...@gmail.com (2017-09-21)

#20: I agree, not all uninitialized data "appear to be" security vulnerabilities at first glance. And Yes, not all the bugs I listed were rewarded, BUT they were all "accepted" as Security-Bugs!! None of them had been labelled as "Type-Bug"!!

I don't mind the hurry, as long as one does not have to come back later and say "Oh, I missed that". We all want a safer world, primary reason why the bugs are being responsibly reported.

As per your c#7 and subsequent comments, you seemed unsure, which led me to believe you would give it some time and not be in such a hurry. 

Nevertheless, if you believe it to be not-a-security bug, then by all means go ahead and make it public. After all, you hold the reins!!

Thanks,
~ Kushal.

### [Deleted User] (2017-09-22)

No matter how this bug is labeled I'm going to investigate it until we don't have to speculate about what's going on, and will let you know what I find.

### [Deleted User] (2017-09-25)

Just wanted to let you know that I can reproduce this locally at head, with what looks like an identical stack trace to the one in https://crbug.com/chromium/765858#c7.  Here we go...

### [Deleted User] (2017-09-25)

As expected, MSAN doesn't peep if we drop back to scalar code.

When using SSE2, MSAN is complaining when we're doing a 16384 x 2 run.  That's very interesting, as 16384 is an even multiple of 4.  That rules out anything to do with carrying around uninitialized data in the high lanes of the vector near the edge... we happen to fill the vectors perfectly every time in this case.

This has me leaning toward the simple answer, that the original buffer has not been initialized.  Still digging.

### [Deleted User] (2017-09-25)

So, yes, the original image that we deserialize and draw is uninitialized.

The problem is rooted in SkBitmap::ReadRawPixels().  The information describing the serialized image is in an impossible state, and we're failing to detect that (basically, a <= where we should have >=).  We're reading a bunch of pixels that don't exist, running off the end of the serialized image filter into whatever memory is mapped next.

For what it's worth, we would have caught this earlier if scalar float -> int conversions were considered interesting uses.  We got lucky here that I switched that raster pipeline code over to SSE2 and that MSAN started picking this up.

### [Deleted User] (2017-09-25)

Sorry, got that mixed up a little.  In this particular case, we're reading only bytes within the serialized image filter, likely the exact number of bytes we ought to be reading for this image.

Where we're going wrong is allocating a buffer to hold them that's too big.  It's those extra bytes from the over-allocation that are never initialized.

So I don't think we're reading any memory out of bounds.  But we are drawing uninitialized pixels.

### [Deleted User] (2017-09-25)

I have a proposed fix here: https://skia-review.googlesource.com/c/skia/+/50800

With that patched in, we just get 

  [0925/135135.271292:INFO:filter_fuzz_stub.cc(61)] Test case: /home/mtklein/Downloads/clusterfuzz-testcase-5573869816774656.fil
  [0925/135135.275893:INFO:filter_fuzz_stub.cc(53)] Invalid stream detected.
  #EOF

as desired.

### [Deleted User] (2017-09-25)

Hey palmer@, I noticed that when clusterfuzz tried to reproduce this in https://crbug.com/chromium/765858#c4, it did so as an ASAN job, while this is an MSAN issue.  Is there a way we can switch it over to MSAN?

### cl...@chromium.org (2017-09-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5604842839212032.

### [Deleted User] (2017-09-25)

Looks like I got it?

### pa...@chromium.org (2017-09-25)

Yep, looks good.

### bu...@chromium.org (2017-09-25)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/d6c04d9a05c1b4066c09083a673d7d3cf61a3aa6

commit d6c04d9a05c1b4066c09083a673d7d3cf61a3aa6
Author: Mike Klein <mtklein@chromium.org>
Date: Mon Sep 25 19:26:39 2017

Simplify / fix SkBitmap::ReadRawPixels()

We no longer need to look at the field snugRB except to check for the
simple no-pixels case.  This is good, because our snugRB <= ramRB check
is actually too weak, and is the source of this linked Chromium issue.

BUG=chromium:765858

Instead of doing complicated checks against that stored snugRB and the
computed ramRB, we now just ignore snugRB.  We know the images written
by write_row_bytes() will be snug, so we can just look at width, height,
and color type to figure out exactly how many bytes we should be
reading.

Then it becomes the call to readByteArray()'s responsibility to make
sure that we have an array there of exactly that many bytes to read.
We've just got to make sure we check for its failure.

Change-Id: Ia05c36d8a77b0de16ee03a80f6cb2dab6fcedbae
Reviewed-on: https://skia-review.googlesource.com/50800
Reviewed-by: Mike Reed <reed@google.com>
Commit-Queue: Mike Klein <mtklein@chromium.org>

[modify] https://crrev.com/d6c04d9a05c1b4066c09083a673d7d3cf61a3aa6/src/core/SkBitmap.cpp


### cl...@chromium.org (2017-09-25)

Detailed report: https://clusterfuzz.com/testcase?key=5604842839212032

Job Type: linux_msan_filter_fuzz_stub
Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  sk_store_bgra
  sk_start_pipeline
  SkScan::FillIRect
  
Sanitizer: memory (MSAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_msan_filter_fuzz_stub&range=497828:497874

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5604842839212032

See https://github.com/google/clusterfuzz-tools for more information.

The recommended severity is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.


### bu...@chromium.org (2017-09-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/328102d194aaaa8b8ad2bf0b93aaa8e5126d863a

commit 328102d194aaaa8b8ad2bf0b93aaa8e5126d863a
Author: skia-deps-roller@chromium.org <skia-deps-roller@chromium.org>
Date: Mon Sep 25 22:20:16 2017

Roll src/third_party/skia/ 94fddf838..f40ae1a4b (5 commits)

https://skia.googlesource.com/skia.git/+log/94fddf83816a..f40ae1a4b536

$ git log 94fddf838..f40ae1a4b --date=short --no-merges --format='%ad %ae %s'
2017-09-25 reed Revert "migrate to sk_sp for SkFontMgr API"
2017-09-25 benjaminwagner Specify CPU for CT Swarming tasks.
2017-09-25 reed migrate to sk_sp for SkFontMgr API
2017-09-25 mtklein Simplify / fix SkBitmap::ReadRawPixels()
2017-09-22 enne Make SkPath::readFromMemory failure silent

Created with:
  roll-dep src/third_party/skia
BUG=765858


Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls


CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_trusty_blink_rel;master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel;master.tryserver.chromium.android:android_optional_gpu_tests_rel
TBR=jvanverth@chromium.org

Change-Id: Id721b8de8164bd59065b7a4a5203a5689e1022a3
Reviewed-on: https://chromium-review.googlesource.com/682954
Reviewed-by: Skia Deps Roller <skia-deps-roller@chromium.org>
Commit-Queue: Skia Deps Roller <skia-deps-roller@chromium.org>
Cr-Commit-Position: refs/heads/master@{#504186}
[modify] https://crrev.com/328102d194aaaa8b8ad2bf0b93aaa8e5126d863a/DEPS


### eu...@chromium.org (2017-09-25)

Hmm, scalar fp-to-int does not check for uninitialized input, but it is supposed to mark the result of the conversion as uninitialized. Any idea why we do not catch this problem when the pixels are eventually rendered to screen?

### [Deleted User] (2017-09-26)

That conversion from float to int is very nearly the end as far as rendering to the screen goes.  The only operations done to those values after that are a couple left shifts and bitwise ors, and then it's all GL compositor and GPU hardware the rest of the way.

(In this case, the image must be marked as opaque... we're not mixing the source image in any way with the existing pixels of the destination buffer.  But even our most complex blend mode is implemented in a branch-free way, so it can vectorize.)

### cl...@chromium.org (2017-09-26)

ClusterFuzz has detected this issue as fixed in range 504165:504212.

Detailed report: https://clusterfuzz.com/testcase?key=5604842839212032

Job Type: linux_msan_filter_fuzz_stub
Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  sk_store_bgra
  sk_start_pipeline
  SkScan::FillIRect
  
Sanitizer: memory (MSAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_msan_filter_fuzz_stub&range=497828:497874
Fixed: https://clusterfuzz.com/revisions?job=linux_msan_filter_fuzz_stub&range=504165:504212

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5604842839212032

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-09-26)

ClusterFuzz testcase 5604842839212032 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-09-26)

[Empty comment from Monorail migration]

### eu...@chromium.org (2017-09-26)

If you can point to a place where a buffer needs to be fully initialized, like when it is being passed to GPU, we could annotate it with __msan_check_mem_is_initialized() and hopefully catch more bugs like this.

### ku...@gmail.com (2017-09-27)

Any CVE-ID and/or bounty for this one?

Thanks,
~ Kushal.

### pa...@chromium.org (2017-09-27)

[Empty comment from Monorail migration]

### ku...@gmail.com (2017-10-03)

Hello @ahwalley, @mtklein, 

I would like to ask for assignment of Labels, namely reward-topanel and Security_Severity-Medium for this one.

Thanks,
~ Kushal.

### aw...@google.com (2017-10-16)

Hi Kushal - flagging for the panel, who will also take a look at the severity rating.

### aw...@chromium.org (2017-10-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-10-20)

Nice one - the VRP awarded $1,000 for this one :-)

### aw...@chromium.org (2017-10-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-27)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), gkihumba@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-10-27)

+awhalley@ (Security TPM) for M63 merge review

### aw...@chromium.org (2017-10-30)

[Empty comment from Monorail migration]

### ku...@gmail.com (2017-10-31)

Hello Andrew, 

Thank you for the generous bounty, and especially more so for taking the initiative to take it up to the Panel..:)

Any update on the CVE-ID for the same?

Thanks,
~Kushal.

### aw...@chromium.org (2017-11-01)

Hi Kushal - a CVE will be assigned with Chrome M63 goes stable

### ku...@gmail.com (2017-11-09)

Hello Andrew,

It's been a while since this one was awarded but I haven't received the bounty as yet. 

I am not sure if anything is amiss from my end.

Could you help in this issue. I just want to make sure all the invoices are in place before year end and tax filing starts so..

Thanks,
~Kushal.

### aw...@chromium.org (2017-11-09)

Hi Kushal - I'll look into this and follow up over email.

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/765858?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089027)*

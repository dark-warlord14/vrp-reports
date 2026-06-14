# Security: ffmpeg oob write4 (222)

| Field | Value |
|-------|-------|
| **Issue ID** | [40076594](https://issues.chromium.org/issues/40076594) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Codecs |
| **Reporter** | pa...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2012-11-17 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

==12054== ERROR: AddressSanitizer stack-buffer-overflow on address 0xbf8f2730 at pc 0x8c02b4d bp 0xbf8f25b8 sp 0xbf8f25b0  

WRITE of size 4 at 0xbf8f2730 thread T0  

#0 0x8c02b4c in apply\_tns /home/p/ffmpeg-1.0/libavcodec/aacdec.c:2051  

#1 0x8c02188 in apply\_ltp /home/p/ffmpeg-1.0/libavcodec/aacdec.c:2108  

#2 0x8c015ed in spectral\_to\_sample /home/p/ffmpeg-1.0/libavcodec/aacdec.c:2322  

#3 0x8bfd735 in aac\_decode\_frame\_int /home/p/ffmpeg-1.0/libavcodec/aacdec.c:2527  

#4 0x8bfc209 in aac\_decode\_frame /home/p/ffmpeg-1.0/libavcodec/aacdec.c:2636  

#5 0x8a2e8e0 in avcodec\_decode\_audio4 /home/p/ffmpeg-1.0/libavcodec/utils.c:1683  

#6 0x80a451c in decode\_audio /home/p/ffmpeg-1.0/ffmpeg.c:1445  

#7 0x80a168a in output\_packet /home/p/ffmpeg-1.0/ffmpeg.c:1772  

#8 0x80ae426 in process\_input /home/p/ffmpeg-1.0/ffmpeg.c:2840  

#9 0x809e7bd in transcode\_step /home/p/ffmpeg-1.0/ffmpeg.c:2936  

#10 0x8095bc3 in transcode /home/p/ffmpeg-1.0/ffmpeg.c:2988  

#11 0x8095906 in main /home/p/ffmpeg-1.0/ffmpeg.c:3168  

#12 0xb756c4d2 in \_\_libc\_start\_main /build/buildd/eglibc-2.15/csu/libc-start.c:226  

Address 0xbf8f2730 is located at offset 240 in frame <apply\_tns> of T0's stack:  

This frame has 2 object(s):  

[32, 112) 'lpc'  

[160, 240) 'tmp'  

HINT: this may be a false positive if your program uses some custom stack unwind mechanism  

(longjmp and C++ exceptions \*are\* supported)  

Shadow byte and word:  

0x37f1e4e6: f4  

0x37f1e4e4: 00 00 f4 f4  

More shadow bytes:  

0x37f1e4d4: 00 00 f4 f4  

0x37f1e4d8: f2 f2 f2 f2  

0x37f1e4dc: 00 00 00 00  

0x37f1e4e0: 00 00 00 00  

=>0x37f1e4e4: 00 00 f4 f4  

0x37f1e4e8: f3 f3 f3 f3  

0x37f1e4ec: 00 00 00 00  

0x37f1e4f0: 00 00 00 00  

0x37f1e4f4: 00 00 00 00  

Stats: 3M malloced (1M for red zones) by 1637 calls  

Stats: 0M realloced by 98 calls  

Stats: 2M freed by 1406 calls  

Stats: 0M really freed by 0 calls  

Stats: 40M (10246 full pages) mmaped in 10 calls  

mmaps by size class: 8:16383; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 19:8;  

mallocs by size class: 8:1086; 9:313; 10:27; 11:56; 12:4; 13:8; 14:132; 15:5; 16:2; 19:4;  

frees by size class: 8:951; 9:241; 10:23; 11:50; 12:3; 13:4; 14:128; 15:3; 16:1; 19:2;  

rfrees by size class:  

Stats: malloc large: 4 small slow: 29  

==12054== ABORTING

**VERSION**  

ffmpeg-1.0

**REPRODUCTION CASE**  

Included.

Compile ffmpeg with ASAN and run:  

./ffmpeg -i 222.min -f null - 2>&1 | asan\_symbolize.py

## Attachments

- [222.min](attachments/222.min) (audio/x-hx-aac-adts; charset=binary, 31.9 KB)
- [test.m4a](attachments/test.m4a) (video/mp4; charset=binary, 34.0 KB)
- [0001-aac-prevent-stack-overwrite-in-TNS-ma-filter.patch](attachments/0001-aac-prevent-stack-overwrite-in-TNS-ma-filter.patch) (text/plain; charset=us-ascii, 886 B)

## Timeline

### in...@chromium.org (2012-11-17)

Can you reproduce this in chrome ?

### pa...@gmail.com (2012-11-18)

I wasn't able to mux this stream into something digestible by chrome like mp4.

### sc...@gmail.com (2012-11-18)

Maybe super Dale has a few minutes to see if this can be turned into something that affects Chrome?

### da...@chromium.org (2012-11-18)

+rbultje will know better than I.

I'll take a look on Monday if it can be muxed.

### [Deleted User] (2012-11-18)

I can confirm this crashes chrome (ffmpeg -i 222.min -f mp4 -acodec copy file.m4a). Alex Converse (youtube team, he knows more about AAC than me) may be able to tell you what the correct fix is, but it seems that there's a one-off in the TNS MA filter code (see patch coming in next msg):

    float tmp[TNS_MAX_ORDER];
[..]
                    for (i = order; i > 0; i--)
                        tmp[i] = tmp[i - 1];

order goes up until TNS_MAX_ORDER, so writing into tmp[order] is invalid. It seems to me it should simply start the loop from order - 1.

### [Deleted User] (2012-11-18)

Proposed patch.

### [Deleted User] (2012-11-18)

Quick update, some "fate" tests fail in ffmpeg with that patch applied, so it may be incorrect and we may have to increase the size of the "tmp" array mentioned earlier by one. Again, Alex Converse will know better than me...

### pa...@gmail.com (2012-11-18)

"order" is set here:

file: ffmpeg-1.0\libavcodec\aacdec.c
func: decode_tns
(1)              if ((tns->order[w][filt] = get_bits(gb, 5 - 2 * is8)) > tns_max_order) {
                    av_log(ac->avctx, AV_LOG_ERROR, "TNS filter order %d is greater than maximum %d.\n",
                           tns->order[w][filt], tns_max_order);
                    tns->order[w][filt] = 0;
                    return -1;
                }

1 - tns_max_order is equal to 20 or 12. Perhaps patching ">" to ">=" would be better?


### pa...@gmail.com (2012-11-18)

Btw, are there any 'google chrome' [0] ASAN builds which are able to consume h264/aac?

0 - http://code.google.com/p/chromium/wiki/ChromiumBrowserVsGoogleChrome

### [Deleted User] (2012-11-18)

Do you guys mind if I CC Alex (aconverse@)? He'll probably know which of the proposed solutions is likely best.

### sc...@gmail.com (2012-11-18)

@rbultje: go right ahead!

@pawlkt: I don't think we provide any officially but if you were building your own Chromium under ASAN, you can make it more Chrome-like with something like

export GYP_DEFINES='branding=Chrome buildtype=Official'


### da...@chromium.org (2012-11-18)

To build chrome with all codecs you can set ffmpeg_branding=Chrome (or ChromeOS on Linux to get all the CrOS codecs too) and proprietary_codecs=1. No need for the branding=Chrome buildtype=Official.

### [Deleted User] (2012-11-18)

+aconverse.

Alex, it seems the TNS ma filter code has a stack overwrite that can crash chrome (see earlier comments or sample .m4a file, aacdec.c line 2016 in current Libav git master, or line 2051 in ffmpeg git master). Can you comment on which of the proposed fixes (increase stack array size by 1, clamp order by one less, fix the bounds of the ma filter loop to start at order-1, something else?) is the right thing to do from an algorithmic point of view without risking to break AAC decoding of valid files?

### in...@chromium.org (2012-11-19)

[Empty comment from Monorail migration]

### ac...@google.com (2012-11-19)

order = 20 should never occur during TNS forward mode (ma). Order 20 can only occur in AOT MAIN and forward operation can only happen when LTP is used (the LTP tool does not operate in AOT MAIN). So the decoder is already in an illegal state when we enter this function, which isn't great. 

For this particular crash, you definitely want to make tmp one larger. I'm looking deeper into how we go into a the illegal state now. 

### ac...@google.com (2012-11-19)

The order=20 in LTP issue is a result from switching from MAIN profile to LTP profile while not coding the the channel with the large TNS value in the first frame after the switch of to MAIN. 

### da...@chromium.org (2012-11-19)

@Alex are you working on a correct fix for this or should we just increase tmp?

### ac...@google.com (2012-11-19)

Increase tmp for now. I may try to reject cases like this earlier in the decoding process, but that will take some further thought and even then it still may not have 100% coverage. 

### bu...@chromium.org (2012-11-19)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=31003

------------------------------------------------------------------------
r31003 | dalecurtis@google.com | 2012-11-19T22:45:31.790129Z

------------------------------------------------------------------------

### da...@chromium.org (2012-11-20)

M25 fix is in the CQ now. I'll need to branch the M24 and M23 version of FFmpeg in order to update them since they're not tracking M25 at present.

### bu...@chromium.org (2012-11-20)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=168731

------------------------------------------------------------------------
r168731 | dalecurtis@chromium.org | 2012-11-20T04:36:55.170313Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=168731&r2=168730&pathrev=168731
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/pipeline_integration_test_base.cc?r1=168731&r2=168730&pathrev=168731
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/ffmpeg/ffmpeg_regression_tests.cc?r1=168731&r2=168730&pathrev=168731

Roll FFMpeg DEPS to pick up security fixes.

- Adds a test case for the issue.
- Fixes ordering issues with EXPECT_EQ()
- Notes a recent memory leak regression.
- Fixes stale errors and hashes for unit test.

Includes:
82ae69c Prevent stack buffer overflow during AAC decoding.

BUG=161639
TEST=unit test under asan/valgrind.


Review URL: https://chromiumcodereview.appspot.com/11414076
------------------------------------------------------------------------

### sc...@gmail.com (2012-11-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-11-21)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=168939

------------------------------------------------------------------------
r168939 | dalecurtis@google.com | 2012-11-21T01:06:39.555363Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/ffmpeg/1312/libavcodec/aacdec.c?r1=168939&r2=168938&pathrev=168939

Prevent stack buffer overflow during AAC decoding. BUG=161639
------------------------------------------------------------------------

### bu...@chromium.org (2012-11-21)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=31048

------------------------------------------------------------------------
r31048 | dalecurtis@google.com | 2012-11-21T01:11:25.041937Z

------------------------------------------------------------------------

### da...@chromium.org (2012-11-21)

Merged for M24 which thankfully requires no binary rolls now! (Yay!) But still need to merge to M23 tomorrow with binary roll :(

### sc...@gmail.com (2012-11-30)

Marking Merge-Approved, we'll merge this to the final M23 patch.

### bu...@chromium.org (2012-12-01)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=170612

------------------------------------------------------------------------
r170612 | dalecurtis@google.com | 2012-12-01T00:26:35.052646Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/ffmpeg/1271/libavcodec/aacdec.c?r1=170612&r2=170611&pathrev=170612

Prevent stack buffer overflow during AAC decoding. BUG=161639
------------------------------------------------------------------------

### sc...@gmail.com (2012-12-01)

Thanks, Dale. Are the Windows binaries taken care of too?

@pawlkt: do you want to make a case about exploitability? It seems to me that writing an arbitrary 4-byte value exactly 4 bytes out-of-bounds on the stack would exactly clobber the canary value and nothing else.

Is there a Chromium platform that hasn't opted in to stack canaries?

### bu...@chromium.org (2012-12-01)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=31319

------------------------------------------------------------------------
r31319 | dalecurtis@google.com | 2012-12-01T01:37:29.659192Z

------------------------------------------------------------------------

### da...@chromium.org (2012-12-01)

Just rolled the M23 deps, so everything should be taken care of. I verified this does not crash anymore with an M23 build and the new DLLs.

### bu...@chromium.org (2012-12-01)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=31320

------------------------------------------------------------------------
r31320 | dalecurtis@google.com | 2012-12-01T01:44:25.382088Z

------------------------------------------------------------------------

### pa...@gmail.com (2012-12-01)

@scarybeasts:

Here's where chrome for windows (23.0.1271.91 m) is crashing when parsing test.m4a:

(1ea0.14f4): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=00000000 ebx=00000000 ecx=00000001 edx=00000003 esi=03d2f980 edi=03d31980
eip=6ac737e1 esp=0427f3d0 ebp=00000000 iopl=0         nv up ei pl zr na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246
avcodec_54!avpriv_aac_parse_header+0x22e1:
6ac737e1 0fb603          movzx   eax,byte ptr [ebx]         ds:002b:00000000=??

This isn't a canary fail.

avcodec-54.dll doesn't seem to be compiled with /GS -- I don't see any canary checks anywhere.

### sc...@gmail.com (2012-12-01)

@pawlkt: thanks! That is very helpful and I trust your analysis. Looks bad to me. ebp is NULL so probably 0 was written as the 4-byte out of bounds write.

### sc...@gmail.com (2012-12-04)

@pawlkt: thanks for reporting this bug.

We're happy to reward it at $2000.
$1000 for the base bug and a $1000 bonus for finding an issue in an area of code that has been reasonably well fuzzed.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2012-12-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-12-14)

Payment in system.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### hv...@gmail.com (2017-01-19)

[Comment Deleted]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/161639?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076594)*

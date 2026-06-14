# Heap-buffer-overflow in UpsampleBgraLinePairSSE2

| Field | Value |
|-------|-------|
| **Issue ID** | [40061167](https://issues.chromium.org/issues/40061167) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Media>Video |
| **Reporter** | as...@ut.ee |
| **Assignee** | jz...@chromium.org |
| **Created** | 2012-07-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Webp decoder integer overflow in buffer.c:CheckDecBuffer leads  

to heap-buffer-overflow.

Overflow occurs in:  

ok &= (buf->stride \* height <= buf->size);

(All types are int)

It triggers when:  

VP8X chunk declares a resolution of 0x10000 x 1  

VP8 chunk declares a resolution of 1 x 0x3fff

Then:  

buf->stride = 0x10000 \* 4 = 0x40000  

height = 0x3fff  

buf->stride \* height = 0xfffc0000 (overflows to negative)

Buffer check should fail, but succeeds and the buffer is overflown.

**VERSION**  

Chrome Version: 21.0.1163.0 (Developer Build 140236)  

Operating System: 64 bit linux

**REPRODUCTION CASE**  

Reproducer bad.webp is attached. But for me an img tag was necessary  

for chrome to start decoding:

<http://www.ut.ee/~asd/webp/bad.html>

## Attachments

- [bad.webp](attachments/bad.webp) (application/octet-stream; charset=binary, 526 B)
- [crash_details.txt](attachments/crash_details.txt) (text/plain; charset=us-ascii, 19.8 KB)

## Timeline

### in...@chromium.org (2012-07-11)

ClusterFuzz report coming soon.

### in...@chromium.org (2012-07-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=75907691

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow WRITE 1
Crash Address: 0x7f829e966080
Crash State:
  - crash stack -
  UpsampleBgraLinePairSSE2
  EmitFancyRGB
  CustomPut
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=116918:116938

Minimized Testcase (0.38 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94tYlqxU2OvE2lhE4wnKPJbTBPV6NCqtqHfBSdUyHfE9yC8ke3XPWqPREYYvxdVDy0Rkp-ZheXp01P-4MHIllhwS-PWJokkTcqjo2g4tmylesdy_vx8pEF5P3BC8K4Q25rTA2B3n8EE_hit4kMySNtIskS0Ie3ZHoifvhL09ZEfpVovItk

### in...@chromium.org (2012-07-12)

Looks to regress in http://src.chromium.org/viewvc/chrome?view=rev&revision=116933

### in...@chromium.org (2012-07-12)

Hi,

On Wed, Jul 11, 2012 at 5:34 PM, Andrew Scherkus <scherkus@google.com> wrote:
Hey Pascal and James,

Looks like we've got an overflow in libwebp:
http://code.google.com/p/chromium/issues/detail?id=136894

skal@ I don't think you have a chromium account so I can't cc you to that bug, but here are the details:


hmm.. indeed, i don't have a chromium account it seems. Strange, i'd'd swear i had one...

  
<snip>
VULNERABILITY DETAILS
Webp decoder integer overflow in buffer.c:CheckDecBuffer leads
to heap-buffer-overflow.

Overflow occurs in:
    ok &= (buf->stride * height <= buf->size);

thanks for the detail report!
 
Indeed, it's fixed since, as we all use constructs like:
     const size_t size = buf->stride * height;
   ...
    ok &= (size <= buf->size);

now

(see: the latest http://git.chromium.org/gitweb/?p=webm/libwebp.git;a=blob;f=src/dec/buffer.c;h=ad953737b0363264a9f262eb658d211683fc9466;hb=HEAD )


But now that you mention it, i'm not sure size_t is enough for 32-bit platforms. We use uint64_t
at other places and i think we should uniformize this use. I'll have a look...

Going forward, it's seems the chrome version of libwebp needs a fix, sure.
Shall i do it?

### in...@chromium.org (2012-07-12)

skal@ does not have a chromium account but he has a patch ready.

### in...@chromium.org (2012-07-12)

https://chromiumcodereview.appspot.com/10690171/

### bu...@chromium.org (2012-07-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=146440

------------------------------------------------------------------------
r146440 | scherkus@chromium.org | Thu Jul 12 14:23:09 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/README.chromium?r1=146440&r2=146439&pathrev=146440
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/webp/types.h?r1=146440&r2=146439&pathrev=146440
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/dec/buffer.c?r1=146440&r2=146439&pathrev=146440
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/webp/decode.h?r1=146440&r2=146439&pathrev=146440

libwebp: fix some int <-> size_t mix for buffer sizes

This is to prevent overflow to negative.
(althought we're testing total_size = (size_t)total_size)

Patch by skal@google.com.

BUG=136894
TEST=none

Review URL: https://chromiumcodereview.appspot.com/10690171
------------------------------------------------------------------------

### in...@chromium.org (2012-07-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2012-07-13)

ClusterFuzz has detected this issue as fixed in range 146439:146443.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=75907691

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow WRITE 1
Crash Address: 0x7f829e966080
Crash State:
  - crash stack -
  UpsampleBgraLinePairSSE2
  EmitFancyRGB
  CustomPut
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=116918:116938
Fixed: https://cluster-fuzz.appspot.com/revisions?range=146439:146443

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94tYlqxU2OvE2lhE4wnKPJbTBPV6NCqtqHfBSdUyHfE9yC8ke3XPWqPREYYvxdVDy0Rkp-ZheXp01P-4MHIllhwS-PWJokkTcqjo2g4tmylesdy_vx8pEF5P3BC8K4Q25rTA2B3n8EE_hit4kMySNtIskS0Ie3ZHoifvhL09ZEfpVovItk

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2012-07-24)

merged in r148210

### bu...@chromium.org (2012-07-24)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=148210

------------------------------------------------------------------------
r148210 | inferno@chromium.org | 2012-07-24T21:45:33.461164Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/third_party/libwebp/README.chromium?r1=148210&r2=148209&pathrev=148210
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/third_party/libwebp/dec/buffer.c?r1=148210&r2=148209&pathrev=148210
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/third_party/libwebp/webp/decode.h?r1=148210&r2=148209&pathrev=148210
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/third_party/libwebp/webp/types.h?r1=148210&r2=148209&pathrev=148210

Merge 146440 - libwebp: fix some int <-> size_t mix for buffer sizes

This is to prevent overflow to negative.
(althought we're testing total_size = (size_t)total_size)

Patch by skal@google.com.

BUG=136894
TEST=none

Review URL: https://chromiumcodereview.appspot.com/10690171

TBR=scherkus@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10819006
------------------------------------------------------------------------

### sc...@gmail.com (2012-07-30)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-31)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-31)

Please keep this good finds coming, Juri. $1000

### sc...@gmail.com (2012-07-31)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-31)

[Empty comment from Monorail migration]

### as...@ut.ee (2012-07-31)

Thank you!

I hope to start searching again soon. Btw, I'm coming to an
interview on August 8 :)


### sc...@gmail.com (2012-09-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-01-18)

Restrict-View-EditIssue is preferred since it allows anyone who can edit an issue (committers and contributors) to view the bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/136894?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Media>Video]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061167)*

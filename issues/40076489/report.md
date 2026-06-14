# Security: Integer overflow in libwebp "ParseOptionalChunks" allows memory disclosure

| Field | Value |
|-------|-------|
| **Issue ID** | [40076489](https://issues.chromium.org/issues/40076489) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Reporter** | ph...@gmail.com |
| **Assignee** | jz...@chromium.org |
| **Created** | 2012-10-22 |
| **Bounty** | $3,500.00 |

## Description

**VULNERABILITY DETAILS**  

An integer overflow in libwebp 'ParseOptionalChunks' (third\_party/libwebp/dec/webp.c)  

allows an attacker to disclose the contents of the heap and infer the layout of memory.

The calculation of 'disk\_chunk\_size' in 'ParseOptionalChunks' causes an overflow if  

the attacker controlled 'chunk\_size' is greater than 0xfffffff6. The main loop of  

'ParseOptionalChunks' looks like:

while (1) {  

uint32\_t chunk\_size;  

uint32\_t disk\_chunk\_size; // chunk\_size with padding  

...  

chunk\_size = get\_le32(buf + TAG\_SIZE);  

// For odd-sized chunk-payload, there's one byte padding at the end.  

disk\_chunk\_size = (CHUNK\_HEADER\_SIZE + chunk\_size + 1) & ~1;  

total\_size += disk\_chunk\_size;  

...  

// We have a full and valid chunk; skip it.  

buf += disk\_chunk\_size;  

buf\_size -= disk\_chunk\_size;  

}

A patch to fix the issue is attached (ParseOptionalChunks\_integer\_overflow.patch).

**VERSION**  

Confirmed bug on:  

Chromium SVN r163168 (dev) on OS X (10.6.8)  

Chrome Version 22.0.1229.94 (stable) on OS X (10.6.8)  

Chrome Version 22.0.1229.94 (stable) on Debian (6.0.5, uname -r is '2.6.32-5-amd64')

Tested attched patch on:  

Chromium SVN r163168 (dev) on OS X (10.6.8)

**REPRODUCTION CASE**  

I've attached two reproducers:

loop.html: A minimal testcase which causes an infinite loop by setting 'chunk\_size' to  

0xfffffff7 which overflows 'disk\_chunk\_size' to zero. The pointer 'buf' never advances,  

so the function never terminates.

---

leak.html: A more involved testcase which uses the integer overflow to disclose the  

contents of memory. To do this we place a chunk with 'chunk\_size' of 0xffffffff and a tag  

of "ALPH". The integer overflow causes 'disk\_chunk\_size' to become 0x00000008 (which is a  

valid chunk size). As our malicious chunk has tag "ALPH", ParseOptionalChunks sets  

'\*alpha\_size' (the size of the alpha channel in bytes) to 0xffffffff.

We set the flags in the alpha chunk to be ALPHA\_NO\_COMPRESSION and WEBP\_FILTER\_NONE so that  

our alpha chunk contains uncompressed data that does not have any filters applied to it.

The alpha data has a size of 0xffffffff, so extends over the image data and into the  

remainder of the heap. We end up with a malicous image that looks like so:

```
                           /---- image data ----\  
                           v                    V  

```

| RIFF header | ALPH chunk | VP8 chunk |  

^  

---------- alpha data ----------------------- - - - - - - +0xffffffff

The alpha channel of the image now consists of the image data itself (slightly confusing)  

and then any remaining data on the heap. The alpha channel is constructed in DecodeAlpha  

(third\_party/libwebp/dec/alpha.c). One byte of heap data is disclosed for each pixel in  

the image so the attacker has fine-grained control over how much memory is disclosed.

An 'onload' event handler in 'leak.html' uses the canvas API to read the alpha channel of  

the image and display the contents of the heap following the image. This can be confirmed  

by inspecting the the data after 'dataBytes' in WEBPImageDecoder::decode(bool onlySize)  

(third\_party/WebKit/Source/WebCore/platform/image-decoders/webp/WEBPImageDecoder.cpp) in a  

debugger.

The heap can likely be groomed to contain pointers to other objects, providing an ASLR  

defeat. This could be used in conjunction with another vulnerability (say, a use-after-free)  

to gain stable code execution in the Renderer process. This is presumably a 'Medium' severity  

vulnerability.

## Attachments

- [loop.html](attachments/loop.html) (text/plain; charset=us-ascii, 132 B)
- [leak.html](attachments/leak.html) (text/html; charset=us-ascii, 1.8 KB)
- [ParseOptionalChunks_integer_overflow.patch](attachments/ParseOptionalChunks_integer_overflow.patch) (text/x-diff; charset=us-ascii, 775 B)

## Timeline

### ke...@chromium.org (2012-10-22)

Thanks for the excellent report and repros. Medium severity indeed.

jzern: this looks like an easy patch to libwebp, would you mind taking this or punting it to someone else who can?

### sc...@gmail.com (2012-10-22)

Pascal, you still working on webp? Nasty security bug here.

@philip.turnbull: this is indeed an excellent report. I look forward to proposing it for reward once we've fixed it!

### jz...@chromium.org (2012-10-22)

I can reproduce this. The patch looks ok; I'm having a look around to make sure there aren't other similar instances.

### jz...@chromium.org (2012-10-23)

The fix is ready to land.

Can this report be reused for Opera? Their beta uses 0.2.0 too:
Version 12.10 beta RC 
Build 1620

### sc...@gmail.com (2012-10-23)

@jzern: yes, feel free to let Opera know.

Let us know if you used Philip's fix or not, because it factors into our reward discussion.

### sk...@google.com (2012-10-23)

Hi,

we won't use it 'as is', but his analysis is invaluable, along with his
forged bitstreams for regression-testing!

### jz...@chromium.org (2012-10-23)

+1. reports like this should be encouraged.

### sc...@gmail.com (2012-10-23)

Do not worry, it will be encouraged :)
I'm guessing this might end be a safe change so can we get it merged to M23 too?

### jz...@chromium.org (2012-10-23)

Yes this would be good for M23. It's in the commit queue now.

### bu...@chromium.org (2012-10-23)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=163677

------------------------------------------------------------------------
r163677 | jzern@chromium.org | 2012-10-23T21:17:24.641069Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/dec/webp.c?r1=163677&r2=163676&pathrev=163677
   M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/README.chromium?r1=163677&r2=163676&pathrev=163677

libwebp: validate chunk size in ParseOptionalChunks

the max wasn't checked leading to a rollover case, possibly exploitable.
additionally check the RIFF size early, to avoid similar issues.

BUG=157079


Review URL: https://chromiumcodereview.appspot.com/11229048
------------------------------------------------------------------------

### in...@chromium.org (2012-10-23)

[Empty comment from Monorail migration]

### jz...@chromium.org (2012-10-23)

> @jzern: yes, feel free to let Opera know.

Filed DSK-376099.

### sc...@gmail.com (2012-10-29)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-29)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=164663

------------------------------------------------------------------------
r164663 | cevans@chromium.org | 2012-10-29T17:07:26.214617Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/third_party/libwebp/README.chromium?r1=164663&r2=164662&pathrev=164663
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/third_party/libwebp/dec/webp.c?r1=164663&r2=164662&pathrev=164663

Merge 163677 - libwebp: validate chunk size in ParseOptionalChunks

the max wasn't checked leading to a rollover case, possibly exploitable.
additionally check the RIFF size early, to avoid similar issues.

BUG=157079


Review URL: https://chromiumcodereview.appspot.com/11229048

TBR=jzern@chromium.org
Review URL: https://codereview.chromium.org/11315022
------------------------------------------------------------------------

### sc...@gmail.com (2012-10-29)

@philip.turnbull: now come the fun parts :)

1) Credit! How might we credit you in our upcoming release notes? "Philip Turnbull"?

2) Reward! Always awesome to see new security bug reporters, welcome! :D
And you've picked a good time to send this in. We just upped the reward structure for bugs with demos, particularly ones like this.
Total reward == $500 base bug + $3000 exploitability bonus
Total: $3500 -- great bug.

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

### ph...@gmail.com (2012-10-30)

Can I get credited as "Phil Turnbull"? Thanks guys! :D

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-02-19)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### se...@gmail.com (2013-04-12)

The reward not paid yet ?

### pa...@chromium.org (2013-06-24)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/157079?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076489)*

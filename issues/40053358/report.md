# Security: Heap-buffer-overflow in png_decompress_chunk

| Field | Value |
|-------|-------|
| **Issue ID** | [40053358](https://issues.chromium.org/issues/40053358) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | as...@ut.ee |
| **Assignee** | [Deleted User] |
| **Created** | 2012-02-06 |
| **Bounty** | $1,337.00 |

## Description

**VULNERABILITY DETAILS**  

Some code from png\_decompress\_chunk:

```
  png_size_t expanded_size = png_inflate(png_ptr,  
            (png_bytep)(png_ptr->chunkdata + prefix_size),  
            chunklength - prefix_size,  
            0/\*output\*/, 0/\*output size\*/);  

  /\* some code removed \*/  

  png_charp text = png_malloc_warn(png_ptr,  
                    prefix_size + expanded_size + 1);  

  /\* some code removed \*/  

  png_memcpy(text, png_ptr->chunkdata, prefix_size);  

```

Here expanded\_size returned by png\_inflate can be arbitrarily large. This is  

because png\_inflate decompresses data in small chunks and throws them away if  

output argument is 0.

Therefore prefix\_size + expanded\_size can overflow png\_size\_t (32 bits on my machine) which leads to faulty malloc and heap-buffer-overflow. Bytes at chunkdata and prefix\_size are attacker-controlled.

**VERSION**  

Tested on:  

Chrome 18.0.969.0 (Developer Build 113953 Linux) custom  

Aurora 9.0  

epiphany 2.30.2  

Operating System: Linux 2.6.32, Ubuntu 10.04

**REPRODUCTION CASE**  

Attached is gzipped bad.png with an iCCP chunk that contains 0x10000 'a'-s as prefix and 0xfffff000 'A'-s compressed to 4 MiB.

ADDITIONAL CRASH INFORMATION  

Type of crash: tab  

Crash State:  

Program received signal SIGSEGV, Segmentation fault.  

0xd18676d9 in ?? ()  

(gdb) bt  

#0 0xd18676d9 in ?? ()  

#1 0xb18e6ff4 in ?? () from /lib/libpng12.so.0  

#2 0xb18cbe1a in ?? () from /lib/libpng12.so.0  

#3 0xb18ce117 in ?? () from /lib/libpng12.so.0  

#4 0xb18e2217 in ?? () from /lib/libpng12.so.0  

#5 0xb18e27d4 in ?? () from /lib/libpng12.so.0  

#6 0xb18e287c in png\_process\_data () from /lib/libpng12.so.0  

#7 0xb49b1204 in WebCore::PNGImageReader::decode (this=0xb85e0f00, data=...,  

sizeOnly=true)  

at third\_party/WebKit/Source/WebCore/platform/image-decoders/png/PNGImageDecoder.cpp:143  

#8 0xb49b0f02 in WebCore::PNGImageDecoder::decode (this=0xb85dff60,  

onlySize=true)  

at third\_party/WebKit/Source/WebCore/platform/image-decoders/png/PNGImageDecoder.cpp:437  

#9 0xb49b033c in WebCore::PNGImageDecoder::isSizeAvailable (this=0xb85dff60)  

at third\_party/WebKit/Source/WebCore/platform/image-decoders/png/PNGImageDecoder.cpp:188  

#10 0xb493a841 in WebCore::ImageSource::isSizeAvailable (this=0xb840bc24)  

at third\_party/WebKit/Source/WebCore/platform/graphics/ImageSource.cpp:100  

#11 0xb4905421 in WebCore::BitmapImage::isSizeAvailable (this=0xb840bc00)  

at third\_party/WebKit/Source/WebCore/platform/graphics/BitmapImage.cpp:254  

#12 0xb490534b in WebCore::BitmapImage::dataChanged (this=0xb840bc00,  

---Type <return> to continue, or q <return> to quit---q  

(gdb) x/1i $eip  

=> 0xd18676d9: Cannot access memory at address 0xd18676d9  

(gdb) info reg  

eax 0xb8581200 -1202187776  

ecx 0xfffff000 -4096  

edx 0xb8ab8002 -1196720126  

ebx 0xd18676d9 -779716903  

esp 0xbfffd9b8 0xbfffd9b8  

ebp 0xbfffda58 0xbfffda58  

esi 0xb85e3900 -1201784576  

edi 0x2000 8192  

eip 0xd18676d9 0xd18676d9  

eflags 0x210282 [ SF IF RF ID ]  

cs 0x73 115  

ss 0x7b 123  

ds 0x7b 123  

es 0x7b 123  

fs 0x0 0  

gs 0x33 51

## Attachments

- [bad.png.gz](attachments/bad.png.gz) (application/x-gzip; charset=binary, 6.7 KB)

## Timeline

### sc...@gmail.com (2012-02-06)

Seems like a very interesting bug! I'll take it for now.

### sc...@gmail.com (2012-02-07)

@asd@ut.ee: this doesn't affect your chance for reward, but any idea if this is fixed in upstream libpng or not?

### as...@ut.ee (2012-02-08)

@scarybeasts: I think it isn't. I tested that libpng-1.5.8 is not fixed. libpng-1.6.0beta10 doesn't seem to be either by looking at the code.

### sc...@gmail.com (2012-02-08)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-08)

@asd@ut.ee: congratulations! The rewards panel is really impressed with this find. It's hard to find a libpng bug these days and some good people have already fuzzed and audited it.

So, a $1337 reward for a clever find! :)

I have a fix which I'll commit and describe shortly.

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

### as...@ut.ee (2012-02-08)

Thank you :)

### bu...@chromium.org (2012-02-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=121019

------------------------------------------------------------------------
r121019 | cevans@chromium.org | Wed Feb 08 11:23:05 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libpng/README.chromium?r1=121019&r2=121018&pathrev=121019
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libpng/pngrutil.c?r1=121019&r2=121018&pathrev=121019

Fix integer issues in a way that caters for both 32-bit and 64-bit.

BUG=112822

Review URL: http://codereview.chromium.org/9363013
------------------------------------------------------------------------

### bu...@chromium.org (2012-02-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=121044

------------------------------------------------------------------------
r121044 | cevans@chromium.org | Wed Feb 08 13:43:49 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libpng/libpng.gyp?r1=121044&r2=121043&pathrev=121044

Don't use system libpng by default. It causes security maintenance problems
for ChromeOS. It's worth noting that we also don't use the system library
for many other important components such as libxml.

BUG=112822

Review URL: http://codereview.chromium.org/9365007
------------------------------------------------------------------------

### bu...@chromium.org (2012-02-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=121090

------------------------------------------------------------------------
r121090 | csilv@chromium.org | Wed Feb 08 15:39:44 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libpng/libpng.gyp?r1=121090&r2=121089&pathrev=121090

Revert 121044 - Don't use system libpng by default. It causes security maintenance problems
for ChromeOS. It's worth noting that we also don't use the system library
for many other important components such as libxml.

Reverting due to compile errors on Linux:
http://chromegw.corp.google.com/i/chromium/builders/Linux%20Builder%20%28dbg%29%28shared%29/builds/17665/steps/compile/logs/stdio

BUG=112822

Review URL: http://codereview.chromium.org/9365007

TBR=cevans@chromium.org
Review URL: https://chromiumcodereview.appspot.com/9374001
------------------------------------------------------------------------

### bu...@chromium.org (2012-02-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=121199

------------------------------------------------------------------------
r121199 | cevans@chromium.org | Wed Feb 08 21:36:28 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libpng/libpng.gyp?r1=121199&r2=121198&pathrev=121199

Don't use system libpng by default. It causes security maintenance problems
for ChromeOS. It's worth noting that we also don't use the system library
for many other important components such as libxml.

BUG=112822
R=wad,abarth
Review URL: https://chromiumcodereview.appspot.com/9365007
------------------------------------------------------------------------

### sc...@gmail.com (2012-02-09)

cc:ing the gentlemen who have helped me get changes landed to compile libpng directly into Linux and ChromeOS

### sc...@gmail.com (2012-02-09)

Ok, all the pieces are now landed AFAIK. Extra pieces that were needed beyond the two CLs referenced in this bug:

r121206: build libpng as a static library for the "Linux shared" build mode. Fixes compile fail.

r21892 (internal): no longer expect libpng dynamic lib dependency for .debs

r21896 (internal): roll DEPS for above change




### sc...@gmail.com (2012-02-09)

Ok, just a note on the actual libpng fix: the bug is fairly interesting because it is slightly different on 32-bit vs. 64-bit.

32-bit: straight integer overflow in addition.
64-bit: the types in the addition are actually 64-bit so no overflow there. HOWEVER, the internal malloc()-like function called is actually takes a 32-bit type for "size" so there is truncation! Doh!

I believe there's also an additional integer overflow in the loop that spins to calculate the overall length of the decompressed data. Seems harmless though, as this will simply result in a smaller buffer allocation for the actual decompress, which in turn will truncate the decompressed data rather than causing a corruption. So I left that alone.

### sc...@gmail.com (2012-02-09)

Also
r21895 (internal): remove libpng deps from RPM build

### bu...@chromium.org (2012-02-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=121493

------------------------------------------------------------------------
r121493 | cevans@chromium.org | Fri Feb 10 11:46:14 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1025/src/third_party/libpng/pngrutil.c?r1=121493&r2=121492&pathrev=121493
 M http://src.chromium.org/viewvc/chrome/branches/1025/src/third_party/libpng/README.chromium?r1=121493&r2=121492&pathrev=121493

Merge 121019 - Fix integer issues in a way that caters for both 32-bit and 64-bit.

BUG=112822

Review URL: http://codereview.chromium.org/9363013

TBR=cevans@chromium.org
Review URL: https://chromiumcodereview.appspot.com/9381014
------------------------------------------------------------------------

### bu...@chromium.org (2012-02-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=121492

------------------------------------------------------------------------
r121492 | cevans@chromium.org | Fri Feb 10 11:45:46 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/963/src/third_party/libpng/README.chromium?r1=121492&r2=121491&pathrev=121492
 M http://src.chromium.org/viewvc/chrome/branches/963/src/third_party/libpng/pngrutil.c?r1=121492&r2=121491&pathrev=121492

Merge 121019 - Fix integer issues in a way that caters for both 32-bit and 64-bit.

BUG=112822

Review URL: http://codereview.chromium.org/9363013

TBR=cevans@chromium.org
Review URL: https://chromiumcodereview.appspot.com/9384012
------------------------------------------------------------------------

### bu...@chromium.org (2012-02-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=121494

------------------------------------------------------------------------
r121494 | cevans@chromium.org | Fri Feb 10 11:55:27 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/963/src/third_party/libpng/libpng.gyp?r1=121494&r2=121493&pathrev=121494

Merge 121199 - Don't use system libpng by default. It causes security maintenance problems
for ChromeOS. It's worth noting that we also don't use the system library
for many other important components such as libxml.

BUG=112822
R=wad,abarth
Review URL: https://chromiumcodereview.appspot.com/9365007

TBR=cevans@chromium.org
Review URL: https://chromiumcodereview.appspot.com/9382011
------------------------------------------------------------------------

### bu...@chromium.org (2012-02-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=121495

------------------------------------------------------------------------
r121495 | cevans@chromium.org | Fri Feb 10 11:55:51 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1025/src/third_party/libpng/libpng.gyp?r1=121495&r2=121494&pathrev=121495

Merge 121199 - Don't use system libpng by default. It causes security maintenance problems
for ChromeOS. It's worth noting that we also don't use the system library
for many other important components such as libxml.

BUG=112822
R=wad,abarth
Review URL: https://chromiumcodereview.appspot.com/9365007

TBR=cevans@chromium.org
Review URL: https://chromiumcodereview.appspot.com/9385012
------------------------------------------------------------------------

### sc...@gmail.com (2012-02-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-02-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=121548

------------------------------------------------------------------------
r121548 | cevans@chromium.org | Fri Feb 10 13:48:30 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/963/src/third_party/libpng/libpng.gyp?r1=121548&r2=121547&pathrev=121548

Revert 121494 - Merge 121199 - Don't use system libpng by default. It causes security maintenance problems
for ChromeOS. It's worth noting that we also don't use the system library
for many other important components such as libxml.

BUG=112822
R=wad,abarth
Review URL: https://chromiumcodereview.appspot.com/9365007

TBR=cevans@chromium.org
Review URL: https://chromiumcodereview.appspot.com/9382011

TBR=cevans@chromium.org
Review URL: https://chromiumcodereview.appspot.com/9383016
------------------------------------------------------------------------

### bu...@chromium.org (2012-02-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=121550

------------------------------------------------------------------------
r121550 | cevans@chromium.org | Fri Feb 10 13:50:22 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1025/src/third_party/libpng/libpng.gyp?r1=121550&r2=121549&pathrev=121550

Revert 121495 - Merge 121199 - Don't use system libpng by default. It causes security maintenance problems
for ChromeOS. It's worth noting that we also don't use the system library
for many other important components such as libxml.

BUG=112822
R=wad,abarth
Review URL: https://chromiumcodereview.appspot.com/9365007

TBR=cevans@chromium.org
Review URL: https://chromiumcodereview.appspot.com/9385012

TBR=cevans@chromium.org
Review URL: https://chromiumcodereview.appspot.com/9378023
------------------------------------------------------------------------

### sc...@gmail.com (2012-02-11)

[Empty comment from Monorail migration]

### si...@gmail.com (2012-02-15)

Was this ever reported to libpng upstream?

### si...@gmail.com (2012-02-15)

This should affect moz. as well, can i be permitted to share the repro. with them?

### sc...@gmail.com (2012-02-15)

I sent it upstream yesterday (I couldn't find a libpng mailing list but I did find the current maintainer's e-mail which hopefully will suffice?)

Please do share with moz and any other significantly impacted party.

### sc...@gmail.com (2012-02-15)

Ok, reward for both your recent bugs is in the e-payment system. For some reason bank wires takes ages even in this electronic age so give it a week or two :)

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### js...@chromium.org (2012-07-13)

CC'ing Debian libxml maintainer.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/112822?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053358)*

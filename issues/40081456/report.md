# Segmentation fault in WebCore::RenderLayer::paintList when a malformed PNG image is viewed

| Field | Value |
|-------|-------|
| **Issue ID** | [40081456](https://issues.chromium.org/issues/40081456) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **CVE IDs** | CVE-2010-1205 |
| **Reporter** | ao...@gmail.com |
| **Assignee** | ch...@gmail.com |
| **Created** | 2010-06-07 |
| **Bounty** | $1,000.00 |

## Description

A segmentation fault occurs in WebCore::RenderLayer::paintList when a
malformed PNG image is opened on x86 Ubuntu 10.04 and Chromium (6.0.427.0
(Developer Build 49012) Ubuntu) or Google Chrome (5.0.375.55 (Official
Build 47796)), in which the file occasionally seems to cause memory corruption.

To reproduce, 
  $ chromium-browser http://www.ee.oulu.fi/~aki/spark.png

The file also causes a segmentation fault in Firefox, but the backtraces
look pretty different. The Bugzilla issue is #570451.

Backtrace begins:

Program received signal SIGSEGV, Segmentation fault.
0x0902d9d8 in WebCore::RenderLayer::paintList (this=0xa53b2e0, list=0xa5fe4e0, 
    rootLayer=0xa53b2e0, p=0xbfffde18, paintDirtyRect=..., paintBehavior=0, 
    paintingRoot=0x0, overlapTestRequests=0xbfffdb2c, paintFlags=0)
    at third_party/WebKit/WebCore/rendering/RenderLayer.cpp:2488
2488    third_party/WebKit/WebCore/rendering/RenderLayer.cpp: No such file
or directory.
        in third_party/WebKit/WebCore/rendering/RenderLayer.cpp
(gdb) bt
#0  0x0902d9d8 in WebCore::RenderLayer::paintList (this=0xa53b2e0, 
    list=0xa5fe4e0, rootLayer=0xa53b2e0, p=0xbfffde18, paintDirtyRect=..., 
    paintBehavior=0, paintingRoot=0x0, overlapTestRequests=0xbfffdb2c, 
    paintFlags=0) at third_party/WebKit/WebCore/rendering/RenderLayer.cpp:2488
#1  0x0902e014 in WebCore::RenderLayer::paintLayer (this=0xa53b2e0, 
    rootLayer=0xa53b2e0, p=0xbfffde18, paintDirtyRect=..., paintBehavior=0, 
    paintingRoot=0x0, overlapTestRequests=0xbfffdb2c, paintFlags=0)
    at third_party/WebKit/WebCore/rendering/RenderLayer.cpp:2458
#2  0x0902e905 in WebCore::RenderLayer::paint (this=0xa53b2e0, p=0xbfffde18, 
    damageRect=..., paintBehavior=0, paintingRoot=0x0)
    at third_party/WebKit/WebCore/rendering/RenderLayer.cpp:2243
#3  0x08f4ef2a in WebCore::FrameView::paintContents (this=0xa55c400, 
    p=0xbfffde18, rect=...)
    at third_party/WebKit/WebCore/page/FrameView.cpp:1878
#4  0x08fb8eda in WebCore::ScrollView::paint (this=0xa55c400, 
    context=0xbfffde18, rect=...)
    at third_party/WebKit/WebCore/platform/ScrollView.cpp:790
#5  0x08d303ab in WebKit::WebFrameImpl::paintWithContext (this=0xa527000, 
    gc=..., rect=...)
    at third_party/WebKit/WebKit/chromium/src/WebFrameImpl.cpp:1773
[...]


## Timeline

### in...@chromium.org (2010-06-07)

It results in a sad tab for both v5 stable and v6 trunk (6.0.426.0 (49004)) for
windows. it does not reproduce on safari nightly and running in the debugger should a
debug assert hitting in skia code.

Stephen, can you please take a look at this.

### ao...@gmail.com (2010-06-09)

I'll add a few similar files crashing Chromium and/or Firefox to http://www.ee.oulu.fi/~aki/png-cases/ to help check a fix.

### ao...@gmail.com (2010-06-10)

Looks like a possible memory corruption also in newer Chromium (testing with 6.0.430.0 (Developer Build 49219) Ubuntu)). Two backtraces from pages which have an image causing the same issue in them:

Program received signal SIGSEGV, Segmentation fault.
SLL_PopRange (this=0xa4d4000, src=0xa4d4034, cl=2, N=12)
    at third_party/tcmalloc/chromium/src/linked_list.h:73
73      third_party/tcmalloc/chromium/src/linked_list.h: No such file or directory.
        in third_party/tcmalloc/chromium/src/linked_list.h
(gdb) bt
#0  SLL_PopRange (this=0xa4d4000, src=0xa4d4034, cl=2, N=12)
    at third_party/tcmalloc/chromium/src/linked_list.h:73
#1  tcmalloc::ThreadCache::FreeList::PopRange (this=0xa4d4000, src=0xa4d4034, 
    cl=2, N=12) at third_party/tcmalloc/chromium/src/thread_cache.h:209
#2  tcmalloc::ThreadCache::ReleaseToCentralCache (this=0xa4d4000, 
    src=0xa4d4034, cl=2, N=12)
    at third_party/tcmalloc/chromium/src/thread_cache.cc:218
#3  0x08635a4c in tcmalloc::ThreadCache::Scavenge (this=0xa4d4000)
    at third_party/tcmalloc/chromium/src/thread_cache.cc:237
#4  0x08fa81b7 in ~GIFFrameReader (this=0xa5928c0)
    at third_party/WebKit/WebCore/platform/image-decoders/gif/GIFImageReader.h:150
#5  ~GIFImageReader (this=0xa5928c0)
    at third_party/WebKit/WebCore/platform/image-decoders/gif/GIFImageReader.h:197
#6  deleteOwnedPtr<GIFImageReader> (this=0xa5928c0)
    at third_party/WebKit/JavaScriptCore/wtf/OwnPtrCommon.h:57
#7  WTF::OwnPtr<GIFImageReader>::clear (this=0xa5928c0)
    at third_party/WebKit/JavaScriptCore/wtf/OwnPtr.h:60
#8  WebCore::GIFImageDecoder::gifComplete (this=0xa5928c0)
    at third_party/WebKit/WebCore/platform/image-decoders/gif/GIFImageDecoder.cpp:288
[...]

#0  SLL_Pop (size=11) at third_party/tcmalloc/chromium/src/linked_list.h:56
#1  tcmalloc::ThreadCache::FreeList::Pop (size=11)
    at third_party/tcmalloc/chromium/src/thread_cache.h:200
#2  tcmalloc::ThreadCache::Allocate (size=11)
    at third_party/tcmalloc/chromium/src/thread_cache.h:349
#3  do_malloc (size=11) at third_party/tcmalloc/chromium/src/tcmalloc.cc:981
#4  cpp_alloc (size=11) at third_party/tcmalloc/chromium/src/tcmalloc.cc:1250
#5  do_malloc_or_cpp_alloc (size=11)
    at third_party/tcmalloc/chromium/src/tcmalloc.cc:919
#6  tc_malloc (size=11) at third_party/tcmalloc/chromium/src/tcmalloc.cc:1373
#7  0x093c4ed1 in WTF::fastMalloc (n=11)
    at third_party/WebKit/JavaScriptCore/wtf/FastMalloc.cpp:249
#8  0x093c8751 in WTF::VectorBufferBase<char>::allocateBuffer (
    this=0xbfffd1f8, str=0xbfffcdb8 "User-Agent0 H\325\377\277|\322\377\277", 
    length=10) at third_party/WebKit/JavaScriptCore/wtf/Vector.h:286
#9  VectorBuffer (this=0xbfffd1f8, 
    str=0xbfffcdb8 "User-Agent0 H\325\377\277|\322\377\277", length=10)
    at third_party/WebKit/JavaScriptCore/wtf/Vector.h:361
[...]

### sc...@gmail.com (2010-06-14)

Nice. Sad tab on my 32-bit Linux 5.0.375.70.
Marking SecSeverity-High as there's clearly some memory corruption going on from the trace in https://crbug.com/chromium/45983#c3.

### ao...@gmail.com (2010-06-16)

From bugzilla #580451: this seems to be caused by libpng calling row_callback with a row_num outside of the image, which often causes an out of range write unless the caller checks whether the row is in range. Libpng will probably be modified to check the row before calling the callback, but in the meantime row_callback should have something like the example.c's:

/* Check if row_num is in bounds. */
if ((row_num >= 0) && (row_num < height))
{ proceed

in the beginning to avoid this.

### in...@chromium.org (2010-06-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-06-16)

[Empty comment from Monorail migration]

### ch...@gmail.com (2010-06-16)

Underlying issue is the same. Basically libPNG hands an extra row to PNGImageDecoder::rowAvailable which causes 

buffer.setRGBA(x, destY, pixel[0], pixel[1], pixel[2], alpha);

to write past the end of the buffer. This is sort of a libpng bug but we can implent a check to just drop out of bounds rows.

### ch...@gmail.com (2010-06-17)

I'll file a CL once I get a machine up and working but the check is really easy.

Something like:

if (scaledY(rowIndex) < 0 || scaledY(rowIndex) >= scaledSize().height())
  return;

### ch...@gmail.com (2010-06-17)

[Empty comment from Monorail migration]

### ch...@gmail.com (2010-06-18)

CL awaiting webkit review

https://bugs.webkit.org/show_bug.cgi?id=40798


### ao...@gmail.com (2010-06-18)

Can you wait a while before making the patch public? It does fix the the symptom, but also exposes an error which could leave other programs using progressive PNG reading vulnerable. Firefox has not yet applied the patch to trunk for this reason. Glenn Randers-Pehrson (current libpng maintainer) has been looking at this in bugzilla. It would probably make sense to sync the patch with a libpng update.

### ch...@gmail.com (2010-06-18)

Yeah it really is more of a libPNG issue.. Let us know when you would like to disclose it.

### ao...@gmail.com (2010-06-18)

Great. I'll post here when there is a libpng fix coming and/or Mozilla plans to apply the workaround.

### ch...@gmail.com (2010-06-18)

aohelin,

Is libPNG tracking this issue? If so can you provide a link.

### ao...@gmail.com (2010-06-18)

I only know of the bugzilla entry. I did not see anything public about this in libpng bugtracker or mailing list.

### sc...@gmail.com (2010-06-19)

Heya Aki, we'd like to ship this sooner rather than later if possible, in order to protect our users. We're typically faster than other browsers to patch problems, so we don't like being held back :D In these sorts of cases, we can do a commit with a non-security-sounding message and keep the underlying bug hidden until such time as others have caught up. We've not had any hassles with this approach before (i.e. we've never been shouted at by Apple or Mozilla).

### ao...@gmail.com (2010-06-20)

I posted to bugzilla and told you would like to use the workaround patch asap with some non-suspicious message, and asked if they would be interested in doing the same. A patch for libpng (checking the row before making the callback) is currently being reviewed by the libpng group. Mozilla likely has a code freeze coming in a few days, so they are also interested in getting this fixed sooner rather than later.

Obviously I have no authority to say if and when a patch can be used. I'm just trying to mediate this responsibly. The time and work of doing a responsible disclosure does not seem to scale linearly in the number of parties involved. :)

### ao...@gmail.com (2010-06-20)

A more complete libpng patch also addressing the underlying cause is now under review.

### [Deleted User] (2010-06-21)

[Empty comment from Monorail migration]

### ao...@gmail.com (2010-06-21)

A probably final libpng fix is being tested. Fixed versions 1.2.44 and 1.4.3 will be released shortly. I'll post here once the the library update time is known. The row number check may still be useful in case the system libpng is not upgraded yet. Mozilla will add the check in sync with the libpng update. Glenn Randers-Pehrson sent a report to CERT earlier today. This will be CVE-2010-1205.

Thanks for holding the patch. Embarrassing to report an issue and then ask to not even apply a known workaround...

### js...@chromium.org (2010-06-22)

Bulk move back to M5 for anything SecSeverity-High or worse.

### sc...@gmail.com (2010-06-22)

Great bug Aki! Due to the difficulty of finding a PNG-triggered crash in this modern era, we're provisionally qualifying this for a $1000 reward.
Please, give us as much notice as you can re: the public disclosure date for this. We might take the libpng fix or use a WebKit-based workaround depending on which seems lower risk.

### ao...@gmail.com (2010-06-23)

Cool \o/ (provisionally). I'll let you know as soon as there are more developments.

Since you seem to keep a restrict-view on these for a while, it is probably safe to add alternative reproduction instructions:

 $ mkdir -p $HOME/pngtest/{samples,fuzzed}
 $ cd $HOME/pngtest
 $ curl http://www.schaik.com/pngsuite/PngSuite.tar.gz | tar -C samples -zxvf -
 $ curl http://ouspg.googlecode.com/files/radamsa-0.1.c.gz | gzip -d | gcc -O2 -o
radamsa -x c -
 $ ./radamsa -e surfy -n 1000 -o fuzzed/%f-%i.png samples/*.png

and then '$ for file in fuzzed/*.png; do echo "<img src=$file>"; done >
all.html; chromium-browser all.html' when the set is full, and remove the files to get more if nothing happened. This is in effect what I have been occasionally leaving my laptop to do overnight, modulo some automation, testing several file formats in parallel, using fresh samples and dropping "-e surfy" to make more varied test cases.

### ao...@gmail.com (2010-06-23)

The Mozilla folks agreed they and Chromium should apply the row number workaround right now with an innocuous comment, that keeps attention away from libpng. Their patch was just marked approved.

### ao...@gmail.com (2010-06-23)

Glenn informed that libpng-1.4.3 is also ready for release.

### js...@chromium.org (2010-06-25)

Landed upstream as: http://trac.webkit.org/changeset/61816


### ao...@gmail.com (2010-06-26)

Mozilla's workaround patch landed to 1.9.1. Libpng group is testing 1.4.3rc03.

### ao...@gmail.com (2010-06-26)

libpng 1.4.3 is out.

### js...@chromium.org (2010-06-26)

Thanks for the head up Aki.


### js...@chromium.org (2010-06-26)

Aki, I forgot to ask, do you have any idea when the disclosure announcement on libpng will be made?


### js...@chromium.org (2010-06-26)

Nevermind. Apparently they publicly disclosed this yesterday: http://www.libpng.org/pub/png/libpng.html

@laforge - here's a head's up.

### sc...@gmail.com (2010-06-26)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-06-26)

Dropping the hidden flags because this is now public

### in...@chromium.org (2010-06-28)

Mark did merge this to 375 branch. verified.

### sc...@gmail.com (2010-07-12)

Payment on its way.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/45983?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081456)*

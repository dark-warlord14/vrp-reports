# Security: missing xslt import causes crash w/preloading

| Field | Value |
|-------|-------|
| **Issue ID** | [40050877](https://issues.chromium.org/issues/40050877) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ga...@chromium.org |
| **Created** | 2011-11-04 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free when altering innerHTML of tag that has an iframe that is trying to load an xslt import that doesn't exist.

**VERSION**  

Chrome Version: dev

Google Chrome 17.0.928.0 (Official Build 108431) dev  

OS Linux  

WebKit 535.8 (@99105)  

JavaScript V8 3.6.6.3

Operating System: 64bit oneiric

**REPRODUCTION CASE**

<html>
<head>
<script>
window.onload = function() {
document.getElementById('d').innerHTML=''
}
</script>
</head>
<body>
<span id="d">
<iframe src="resources/xslt-bad-import-uri.xml"></iframe>
</span>
</body>
</html>

and xslt-bad-import-uri.xml and xslt-bad-import-uri.xsl are from layouttests.

http:// schema required.

xml:

<?xml version='1.0' encoding="UTF-8" ?>
<?xml-stylesheet type="text/xsl" href="xslt-bad-import-uri.xsl"?>
<catalog>
</catalog>

xsl:

<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0" xmlns:xsl="[http://www.w3.org/1999/XSL/Transform">](http://www.w3.org/1999/XSL/Transform%22%3E)  

<xsl:import href="nosuchfileatall"/>  

<xsl:template match="/">  

[xsl:apply-imports/](javascript:void(0);)  

</xsl:template>  

</xsl:stylesheet>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:

==26806== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffe3dd74c8 at pc 0x7ffff317860c bp 0x7fffffff9d50 sp 0x7fffffff9d48  

READ of size 8 at 0x7fffe3dd74c8 thread T0  

#0 0x7ffff317860c in WebCore::CachedResourceLoader::checkForPendingPreloads() ???:0  

#1 0x7ffff3178081 in WebCore::CachedResourceLoader::loadDone() ???:0

0x7fffe3dd74c8 is located 72 bytes inside of 168-byte region [0x7fffe3dd7480,0x7fffe3dd7528)  

freed by thread T0 here:  

#0 0x7ffff5d527a6 in free /usr/local/google/asan/address-sanitizer/asan/asan\_malloc\_linux.cc:29  

#1 0x7ffff2515f32 in WebCore::Document::~Document() ???:0  

#2 0x7ffff2515c21 in WebCore::Document::~Document() ???:0  

#3 0x7ffff321417f in WebCore::Frame::setDocument(WTF::PassRefPtr[WebCore::Document](javascript:void(0);)) ???:0

## Attachments

- [xslt-bad-import-uri.xsl](attachments/xslt-bad-import-uri.xsl) (application/xml; charset=us-ascii, 242 B)
- [xslt-bad-import-uri.xml](attachments/xslt-bad-import-uri.xml) (application/xml; charset=us-ascii, 129 B)
- [72168.html](attachments/72168.html) (text/html; charset=us-ascii, 267 B)
- deleted (application/octet-stream, 0 B)
- [asan72168.txt](attachments/asan72168.txt) (text/x-java; charset=us-ascii, 7.9 KB)

## Timeline

### mi...@gmail.com (2011-11-04)

better asan log

### sc...@gmail.com (2011-11-05)

I'm excited to confirm this on Monday :)
Any idea if it affects Chrome 16 Beta or earlier?

### mi...@gmail.com (2011-11-06)

afaict it's only in dev channel.



### sc...@gmail.com (2011-11-07)

Yeah, this does seem to be specific to M17. Nice regression catch. And all sorts of wonderful symptoms :)

Release:
pure virtual method called

Debug:
ASSERTION FAILED: m_thread == currentThread()
third_party/WebKit/Source/WebCore/platform/Timer.h(108) : bool WebCore::TimerBase::isActive() const

Valgrind:
==4662== Invalid read of size 8
==4662==    at 0x1CAA6A4: WebCore::CachedResourceLoader::checkForPendingPreloads() (in /home/chris/chrome/src/out/Release/chrome)
==4662==    by 0x1CAADC8: WebCore::CachedResourceLoader::performPostLoadActions() (in /home/chris/chrome/src/out/Release/chrome)
==4662==    by 0x1CAAE10: WebCore::CachedResourceLoader::loadDone() (in /home/chris/chrome/src/out/Release/chrome)
==4662==    by 0x1CABB1C: WebCore::CachedResourceRequest::end() (in /home/chris/chrome/src/out/Release/chrome)


==4662==  Address 0x13c9d930 is 80 bytes inside a block of size 168 free'd
==4662==    at 0x4E645BA: free (vg_replace_malloc.c:1079)
==4662==    by 0x18C9CA9: WebCore::Document::~Document() (in /home/chris/chrome/src/out/Release/chrome)
==4662==    by 0x1CDF022: WebCore::Frame::setDocument(WTF::PassRefPtr<WebCore::Document>) (in /home/chris/chrome/src/out/Release/chrome)
==4662==    by 0x1C5F75C: WebCore::FrameLoader::clear(bool, bool, bool) (in /home/chris/chrome/src/out/Release/chrome)
==4662==    by 0x1C672D9: WebCore::FrameLoader::cancelAndClear() (in /home/chris/chrome/src/out/Release/chrome)
==4662==    by 0x1CE0013: WebCore::Frame::~Frame() (in /home/chris/chrome/src/out/Release/chrome)
==4662==    by 0x1BA164C: WTF::RefCounted<WebCore::Frame>::deref() (in /home/chris/chrome/src/out/Release/chrome)
==4662==    by 0x1CAAE08: WebCore::CachedResourceLoader::loadDone() (in /home/chris/chrome/src/out/Release/chrome)
==4662==    by 0x1CABB1C: WebCore::CachedResourceRequest::end() (in /home/chris/chrome/src/out/Release/chrome)

### sc...@gmail.com (2011-11-07)

[Empty comment from Monorail migration]

### cb...@chromium.org (2011-11-07)

Different type of preload from "prerender". 

This looks like WebKit's preload scanner - tonyg may be a good person to add.


### sc...@gmail.com (2011-11-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-11-07)

@tonyg: any thoughts? Know of a good owner?

### [Deleted User] (2011-11-08)

I'm OOO until Thurs and then gardening until Wed Nov 16, so I can't get to this until then. Since it is a P0, security bug, I'm bouncing it back to you to ensure it doesn't go ownerless in the meantime. If it is still available next Wednesday, I'll pick it up.

FWIW, I'm not aware of any preload scanner changes in M17 but not M16.

Gavin, any idea if this is related to http://crbug.com/75604 ? I know that recently changed some things about the way we respond to resource load errors.

### sc...@gmail.com (2011-11-08)

Sorry, it's more like a P1. Adjusted.

### ga...@chromium.org (2011-11-08)

Tony, it's definitely a possibility.  The change affected the handling of status code >= 400, which this likely is getting.  I'll take this, if you don't object Abhishek?

### in...@chromium.org (2011-11-08)

Thanks a lot Gavin!!! 

### ga...@chromium.org (2011-11-08)

This is definitely caused by my fix to 75604.

### ga...@chromium.org (2011-11-08)

#0  ~CachedResourceLoader (this=0x7fffdab8ab40, __in_chrg=<value optimized out>) at ../../third_party/WebKit/Source/WebCore/loader/cache/CachedResourceLoader.cpp:115
#1  0x00007fffef6837d3 in WTF::deleteOwnedPtr<WebCore::CachedResourceLoader> (ptr=0x7fffdab8ab40) at ../../third_party/WebKit/Source/JavaScriptCore/wtf/OwnPtrCommon.h:53
#2  0x00007fffef67f688 in WTF::OwnPtr<WebCore::CachedResourceLoader>::clear (this=0x7fffdaf00b48) at ../../third_party/WebKit/Source/JavaScriptCore/wtf/OwnPtr.h:99
#3  0x00007fffef66939a in ~Document (this=0x7fffdaf00800, __in_chrg=<value optimized out>) at ../../third_party/WebKit/Source/WebCore/dom/Document.cpp:502
#4  0x00007fffef67c387 in WebCore::Document::guardDeref (this=0x7fffdaf00800) at ../../third_party/WebKit/Source/WebCore/dom/Document.h:251
#5  0x00007fffef669cf7 in WebCore::Document::removedLastRef (this=0x7fffdaf00800) at ../../third_party/WebKit/Source/WebCore/dom/Document.cpp:581
#6  0x00007fffeebe0b59 in WebCore::TreeShared<WebCore::ContainerNode>::deref (this=0x7fffdaf00810) at ../../third_party/WebKit/Source/WebCore/platform/TreeShared.h:79
#7  0x00007fffeec3875c in WTF::derefIfNotNull<WebCore::Document> (ptr=0x7fffdaf00800) at ../../third_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:59
#8  0x00007fffef4794ca in WTF::RefPtr<WebCore::Document>::operator= (this=0x7fffd76e52a8, o=...) at ../../third_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:143
#9  0x00007fffef474e65 in WebCore::Frame::setDocument (this=0x7fffd76e4c00, newDoc=...) at ../../third_party/WebKit/Source/WebCore/page/Frame.cpp:302
#10 0x00007fffef3b6093 in WebCore::FrameLoader::clear (this=0x7fffd76e4cb8, clearWindowProperties=false, clearScriptObjects=true, clearFrameView=true)
    at ../../third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:545
#11 0x00007fffef3b5e5f in WebCore::FrameLoader::cancelAndClear (this=0x7fffd76e4cb8) at ../../third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:509
#12 0x00007fffef474818 in ~Frame (this=0x7fffd76e4c00, __in_chrg=<value optimized out>) at ../../third_party/WebKit/Source/WebCore/page/Frame.cpp:218
#13 0x00007fffeebf746b in WTF::RefCounted<WebCore::Frame>::deref (this=0x7fffd76e4c00) at ../../third_party/WebKit/Source/JavaScriptCore/wtf/RefCounted.h:183
#14 0x00007fffeebf72bb in WTF::derefIfNotNull<WebCore::Frame> (ptr=0x7fffd76e4c00) at ../../third_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:59
#15 0x00007fffeebf71d7 in ~RefPtr (this=0x7fffd93004e0, __in_chrg=<value optimized out>) at ../../third_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58
#16 0x00007fffef3b6bf6 in WebCore::FrameLoader::checkCompleted (this=0x7fffd76e4cb8) at ../../third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:739
#17 0x00007fffef3b699c in WebCore::FrameLoader::loadDone (this=0x7fffd76e4cb8) at ../../third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:680
#18 0x00007fffef40cd1e in WebCore::CachedResourceLoader::loadDone (this=0x7fffdab8ab40) at ../../third_party/WebKit/Source/WebCore/loader/cache/CachedResourceLoader.cpp:634
#19 0x00007fffef413f14 in WebCore::CachedResourceRequest::end (this=0x7fffd68cbea0) at ../../third_party/WebKit/Source/WebCore/loader/cache/CachedResourceRequest.cpp:331
#20 0x00007fffef413cc2 in WebCore::CachedResourceRequest::didReceiveData (this=0x7fffd68cbea0, loader=0x7fffd68d2d00, 

Note that the CachedResourceLoader in frame #18 is deleting itself, which later causes the crash.  This is triggered by the new load stop in didReceiveData, which I added to fix 75604.  I'll scratch my head until I can find a solution...

### ja...@chromium.org (2011-11-08)

I missed something obvious when reviewing the fix for http://crbug.com/75604. It should have a "RefPtr<Document> protector(m_cachedResourceLoader->document());" before ending the load.

We should probably eventually remove that style of protector and have CachedResourceLoader::loadDone() do the protecting, but that's a problem for another day.

### ga...@chromium.org (2011-11-08)

Yup, japhet, that works, and it's a pattern replicated elsewhere in CachedResourceRequest.  So I'll upload a patch with a minimised test tomorrow AM.

### sc...@gmail.com (2011-11-10)

@gavinp: what's the WebKit bug id where the latest action is occurring?

### ga...@chromium.org (2011-11-10)

scarybeasts, there's no webkit bug yet: the reproduction case provided doesn't work in DumpRenderTree, so making a layout test is proving problematic.  I'm looking at that now.

I think this bug is back up to P0, btw, since it is blocking the merge of 75604 into 16 beta. 

### ke...@chromium.org (2011-11-10)

Use-after-free bugs are not reliable in producing crashes. I was recently struggling with a layout test and was told that if ASAN will pick up the problem it's good enough -- i.e. the layout test doesn't necessarily have to crash plain-Jane DumpRenderTree without your patch.

Crashiness will likely vary between platforms anyway.

### ga...@chromium.org (2011-11-10)

That's true, but the use after free isn't happening in DumpRenderTree, even, so far as I can tell!  I'm thinking it has to do with the resource load order being different; so the reproducing chrome test isn't ideal either. 

### ga...@chromium.org (2011-11-10)

DRT's tree dumping code seems to be holding the doc reference, which prevents the use after free.  With some reworking of the test I should be able to reproduce it and land something.

### ga...@chromium.org (2011-11-11)

The wk bug is https://bugs.webkit.org/show_bug.cgi?id=72068

japhet or scarybeasts: I'm waiting for a review of the testing component of this related addition of a webkit_browsertest on the chrome side http://codereview.chromium.org/8531002/



### sc...@gmail.com (2011-11-12)

Thanks for the quick fix, Gavin.

Committed r99982: <http://trac.webkit.org/changeset/99982>

### ga...@chromium.org (2011-11-15)

Merged into webkit branch 912, http://trac.webkit.org/changeset/100218

### bu...@chromium.org (2011-11-16)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=110321

------------------------------------------------------------------------
r110321 | gavinp@chromium.org | Wed Nov 16 09:54:49 PST 2011

Changed paths:
 A http://src.chromium.org/viewvc/chrome/trunk/src/chrome/test/data/webkit/resources/xslt-bad-import-uri.xml?r1=110321&r2=110320&pathrev=110321
 A http://src.chromium.org/viewvc/chrome/trunk/src/chrome/test/data/webkit/resources?r1=110321&r2=110320&pathrev=110321
 A http://src.chromium.org/viewvc/chrome/trunk/src/chrome/test/data/webkit/xslt-bad-import.html?r1=110321&r2=110320&pathrev=110321
 A http://src.chromium.org/viewvc/chrome/trunk/src/chrome/test/data/webkit/resources/xslt-bad-import-uri.xsl?r1=110321&r2=110320&pathrev=110321
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/webkit_browsertest.cc?r1=110321&r2=110320&pathrev=110321

new webkit_browsertest for crbug.com/103058

Unfortunately, I haven't been able to reproduce https://crbug.com/chromium/103058 very well
in WebKit's LayoutTest engine, because DumpRenderTree's libraries interfere with
resource lifetime; a browser_test doesn't have this issue, so it's able to
act as a good regression test for this issue.

BUG=103058


Review URL: http://codereview.chromium.org/8531002
------------------------------------------------------------------------

### sc...@gmail.com (2011-11-17)

Nice regression catch, miaubiz. And a $1000 Chromium Security Reward which I can pay out right away since only dev channel was affected :D

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

### sc...@gmail.com (2011-11-23)

Payment in system.

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

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-22)

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

This issue was migrated from crbug.com/chromium/103058?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050877)*

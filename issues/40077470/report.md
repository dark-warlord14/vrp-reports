# ASSERTION FAILED: m_table, Heap-use-after-free in WTF::HashTable<WebCore::SVGElement const*, WTF::KeyValuePair<WebCore::SVGElement const*, WebCore::SV

| Field | Value |
|-------|-------|
| **Issue ID** | [40077470](https://issues.chromium.org/issues/40077470) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | sl...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2013-04-25 |
| **Bounty** | $1,000.00 |

## Description

Tested on linux 195394.

----- repro1.xml -----
<html xmlns="http://www.w3.org/1999/xhtml">
    <script>
        setTimeout("window.location.reload()", 1);
    </script>

    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <set attributeName="font-weight"></set>
        <font>
            <font-face font-family="any" id="foo"></font-face>
        </font>
        <use xlink:href="#foo">
            <set attributeName="text-anchor"></set>
        </use>
    </svg>
</html>
----------------------

==17896==ERROR: AddressSanitizer: heap-use-after-free on address 0x615000356bf0 at pc 0x7f42af6e9ef2 bp 0x7f4285988940 sp 0x7f4285988938
WRITE of size 8 at 0x615000356bf0 thread T21 (Chrome_InProcRe)
    #0 0x7f42af6e9ef1 in constructDeletedValue /build/third_party/WebKit/Source/wtf/HashTraits.h:113
    #1 0x7f42af6e9d80 in remove /build/third_party/WebKit/Source/wtf/HashTable.h:1033
    #2 0x7f42af6e9cf4 in removeWithoutEntryConsistencyCheck /build/third_party/WebKit/Source/wtf/HashTable.h:1058
    #3 0x7f42af6e39d9 in remove /build/third_party/WebKit/Source/wtf/HashMap.h:388
    #4 0x7f42af6e34e6 in ~SVGElement /build/third_party/WebKit/Source/core/svg/SVGElement.cpp:81
    #5 0x7f42af795349 in ~SVGUseElement /build/third_party/WebKit/Source/core/svg/SVGUseElement.cpp:116
    #6 0x7f42af79509d in ~SVGUseElement /build/third_party/WebKit/Source/core/svg/SVGUseElement.cpp:112
    #7 0x7f42ad6bd146 in removeDetachedChildrenInContainer<WebCore::Node, WebCore::ContainerNode> /build/third_party/WebKit/Source/core/dom/ContainerNodeAlgorithms.h:104
    #8 0x7f42ad6df6df in dispose /build/third_party/WebKit/Source/core/dom/Document.cpp:641
    #9 0x7f42ad7b0b42 in removedLastRefToScope /build/third_party/WebKit/Source/core/dom/Node.cpp:2556
    #10 0x7f42adc12d80 in PostGarbageCollectionProcessing /build/v8/src/global-handles.cc:277
    #11 0x7f42adc127f4 in PostGarbageCollectionProcessing /build/v8/src/global-handles.cc:659
    #12 0x7f42adc3feb1 in PerformGarbageCollection /build/v8/src/heap.cc:994
    #13 0x7f42adc3f5a2 in CollectGarbage /build/v8/src/heap.cc:653
    #14 0x7f42adb967b9 in CollectGarbage /build/v8/src/heap-inl.h:493
    #15 0x7f42adc3f16e in CollectAllGarbage /build/v8/src/heap.cc:564
[...]


## Attachments

- [asan1.log](attachments/asan1.log) (text/plain; charset=us-ascii, 14.4 KB)
- [repro1.xml](attachments/repro1.xml) (text/html; charset=us-ascii, 429 B)
- [history-2022-10-12.kml](attachments/history-2022-10-12.kml) (application/octet-stream, 1.4 KB)

## Timeline

### in...@chromium.org (2013-04-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-04-26)

Very nice catch Slaweck.

### in...@chromium.org (2013-04-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=180606485

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x615000147120
Crash State:
  - crash stack -
  WTF::HashTable<WebCore::SVGElement const*, WTF::KeyValuePair<WebCore::SVGElement const*, WebCore::SV
  WebCore::SVGElement::~SVGElement
  - free stack -
  WebCore::SVGElement::~SVGElement
  WebCore::SVGFontFaceElement::~SVGFontFaceElement
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=178763:178818

Minimized Testcase (0.35 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96nKV5cJ73lObH06Pvfv9nEIaMiCvQqBfpazwjqb0QmONvPknYuf6MOrIAv8PRS-sPvEKr0YE-uuOQ51Q6kSc0saUJ088Orw7egOIo5iaLKhFbmYVOcMkSJLI3U0w8Cq2jp3GC31cDRUiYQ8W65GL6LQJZrnU_hxTa5U0b9fS4T5dVMeAA
<html xmlns="http://www.w3.org/1999/xhtml">
    <script>
        setTimeout("window.location.reload()", 1);
    </script>

    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"	    ><font>
		    <font-face font-family="any" id="foo"></font-face>
		<use xlink:href="#foo">
			<set attributeName="text-anchor"></set>
		</use>

### sc...@chromium.org (2013-04-26)

[Empty comment from Monorail migration]

### sc...@chromium.org (2013-04-26)

Gotta love the easy ones. Patch by end of day - the only issue is coming up with a test.

### sc...@chromium.org (2013-04-26)

Security team, any idea how to make a test out of this.

Nothing obvious works for me at this point. The fix is easy though, so I am somewhat tempted to just submit without test.

### sc...@gmail.com (2013-04-27)

I don't understand why the test is hard?

### in...@chromium.org (2013-04-27)

Stephen, in these reload ones, you need to see how many reloads are required. In an ASAN build, this should be reliable and probably need just like one reload. In that case, you just use location.hash and then do notifydone. see https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/LayoutTests/fast/css-generated-content/bug91547.html&q=reload%20%22%231%22%20file:layouttests&sq=package:chromium&type=cs&l=8 as an example.

### sc...@chromium.org (2013-04-28)

Of course, I had forgotten about about the location.hash method fo counting across reloads. In this case we need 12, for reasons I do not really understand (something about lazy deletion of nodes).

### sc...@chromium.org (2013-04-29)

https://codereview.chromium.org/14533008

### sc...@chromium.org (2013-04-29)

[Empty comment from Monorail migration]

### sc...@chromium.org (2013-04-29)

Security team: Will you look after the merge? It's simple and this issue has existed forever, I think.

### in...@chromium.org (2013-04-29)

We will do the merges. Thanks for the fix.
https://src.chromium.org/viewvc/blink?view=rev&revision=149347

### sc...@chromium.org (2013-04-29)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-30)

------------------------------------------------------------------------
r149347 | schenney@chromium.org | 2013-04-29T17:40:21.620153Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/custom/svg-element-destructor-iteration-crash.html?r1=149347&r2=149346&pathrev=149347
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGElement.cpp?r1=149347&r2=149346&pathrev=149347
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/custom/svg-element-destructor-iteration-crash-expected.txt?r1=149347&r2=149346&pathrev=149347

SVGElement destructor may use invalid iterator

When an SVGElement object has rare data, its destructor gets a
hash map iterator for the rare data, uses it to clear resources,
then uses the iterator to delete the rare data. However, the resource
cleanup can delete other SVG elements, thus modifying the hash map
from which the iterator came and hence invalidating the iterator
itself.

The fix is to re-get the iterator before deleting the rare data.

BUG=235638
R=inferno@chromium.org, pdr@chromium.org

Review URL: https://codereview.chromium.org/14533008
------------------------------------------------------------------------

### cl...@chromium.org (2013-05-01)

ClusterFuzz has detected this issue as fixed in range 197259:197308.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=180606485

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x615000147120
Crash State:
  - crash stack -
  WTF::HashTable<WebCore::SVGElement const*, WTF::KeyValuePair<WebCore::SVGElement const*, WebCore::SV
  WebCore::SVGElement::~SVGElement
  - free stack -
  WebCore::SVGElement::~SVGElement
  WebCore::SVGFontFaceElement::~SVGFontFaceElement
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=178763:178818
Fixed: https://cluster-fuzz.appspot.com/revisions?range=197259:197308

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96nKV5cJ73lObH06Pvfv9nEIaMiCvQqBfpazwjqb0QmONvPknYuf6MOrIAv8PRS-sPvEKr0YE-uuOQ51Q6kSc0saUJ088Orw7egOIo5iaLKhFbmYVOcMkSJLI3U0w8Cq2jp3GC31cDRUiYQ8W65GL6LQJZrnU_hxTa5U0b9fS4T5dVMeAA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2013-05-06)

M27 is https://src.chromium.org/viewvc/blink?view=rev&revision=149750

### bu...@chromium.org (2013-05-06)

------------------------------------------------------------------------
r149750 | cevans@chromium.org | 2013-05-06T17:37:12.464447Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/svg/SVGElement.cpp?r1=149750&r2=149749&pathrev=149750

Merge Blink r149347 to M27

BUG=235638
TBR=schenney@chromium.org

Review URL: https://codereview.chromium.org/14649017
------------------------------------------------------------------------

### bu...@chromium.org (2013-05-13)

------------------------------------------------------------------------
r150247 | schenney@chromium.org | 2013-05-13T19:17:41.719281Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGElement.cpp?r1=150247&r2=150246&pathrev=150247

Improving the way we remove the element from the iterator.

This just reflects an suggested improvement from Darin Adler
over on WebKit Bugzilla. Makes sense to me. No need to merge.

BUG=235638

Review URL: https://chromiumcodereview.appspot.com/15134002
------------------------------------------------------------------------

### sc...@gmail.com (2013-05-17)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-08-21)

We did decide a $1000 reward. Sorry for the delay in tagging.

### pa...@chromium.org (2013-10-18)

I just kicked off payment via e-payment system, which can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

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

### te...@gmail.com (2022-10-12)

Help me stop it this is my12 the account 

### is...@google.com (2022-10-12)

This issue was migrated from crbug.com/chromium/235638?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077470)*

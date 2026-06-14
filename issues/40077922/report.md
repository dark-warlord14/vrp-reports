# Heap-use-after-free in xsltApplySequenceConstructor

| Field | Value |
|-------|-------|
| **Issue ID** | [40077922](https://issues.chromium.org/issues/40077922) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>SVG, Blink>XML |
| **Reporter** | at...@gmail.com |
| **Assignee** | pd...@chromium.org |
| **Created** | 2013-08-13 |
| **Bounty** | $1,000.00 |

## Description


Tested on:

OS: Ubuntu 12.04
Chromium: 30.0.1599.0 (Developer Build 217118) 

Repro-file:

<?xml-stylesheet type="application/xml" href=""?>
<svg xmlns="http://www.w3.org/2000/svg"
		xmlns:xslt="http://www.w3.org/1999/XSL/Transform"
		xslt:version="1.0">
		<xslt:attribute nnnnnnnnnnname="fill">lime</xslt:attribute>


ASAN-report:

==4158==ERROR: AddressSanitizer: heap-use-after-free on address 0x612000032450 at pc 0x7ff68861e869 bp 0x7fff97b6fe90 sp 0x7fff97b6fe88
READ of size 8 at 0x612000032450 thread T0 (chrome)
    #0 0x7ff68861e868 in xsltApplySequenceConstructor /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libxslt/libxslt/transform.c:2588:0
    #1 0x7ff68861c139 in xsltApplyXSLTTemplate /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libxslt/libxslt/transform.c:3044:0
    #2 0x7ff68861a278 in xsltProcessOneNode /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libxslt/libxslt/transform.c:2045:0
    #3 0x7ff68862bac8 in xsltApplyStylesheetInternal /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libxslt/libxslt/transform.c:6049:0
    #4 0x7ff687b8e298 in WebCore::XSLTProcessor::transformToString(WebCore::Node*, WTF::String&, WTF::String&, WTF::String&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/xml/XSLTProcessorLibxslt.cpp:327:0
    #5 0x7ff68696dc44 in WebCore::Document::applyXSLTransform(WebCore::ProcessingInstruction*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:3966:0
.
.
.
0x612000032450 is located 16 bytes inside of 312-byte region [0x612000032440,0x612000032578)
freed by thread T0 (chrome) here:
    #0 0x7ff68041c955 in free _asan_rtl_:0
    #1 0x7ff68860f8c4 in xsltFreeStylePreComps /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libxslt/libxslt/preproc.c:1947:0
    #2 0x7ff68863592b in xsltFreeStylesheet /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libxslt/libxslt/xslt.c:960:0
    #3 0x7ff68863b1d6 in xsltParseStylesheetImportedDoc /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libxslt/libxslt/xslt.c:6638:0
    #4 0x7ff68863b7cb in xsltParseStylesheetDoc /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libxslt/libxslt/xslt.c:6666:0
    #5 0x7ff687b8ba53 in WebCore::XSLStyleSheet::compileStyleSheet() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/xml/XSLStyleSheetLibxslt.cpp:232:0
    #6 0x7ff687b8ed08 in WebCore::xsltStylesheetPointer(WTF::RefPtr<WebCore::XSLStyleSheet>&, WebCore::Node*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/xml/XSLTProcessorLibxslt.cpp:241:0
.
.
.


## Timeline

### at...@gmail.com (2013-08-13)

Sorry, copy-paste failure with the repro-file.

Real repro-file:

<?xml-stylesheet type="application/xml" href=""?>
<svg xmlns="http://www.w3.org/2000/svg"
		xmlns:xslt="http://www.w3.org/1999/XSL/Transform"
		xslt:version="1.0">
		<xslt:attribute nnnnnnnnnnname="fill">lime</xslt:attribute>
</svg>

### cl...@chromium.org (2013-08-13)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5890470404161536

### cl...@chromium.org (2013-08-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5890470404161536

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61300002dc10
Crash State:
  - crash stack -
  xsltApplySequenceConstructor
  xsltApplyXSLTTemplate
  - free stack -
  xsltFreeStylePreComps
  xsltFreeStylesheet
  

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97D5KXmf-Oi4FPqAJccJz_7gHCiBFwysxeRU0sTo1xOK-m3Qw5mVvk1RIbxMGad5TrZCZvxON-W5AIS4_PGfGzF8pO46fDs0s57ZOdU2JuFIpL32qIqX4TRVSymE_Xt3M5lxSHaZqksR5g6mNKrJWp6HuxwGw

Fully reproducible crash found using linux_tsan_chrome_mp job type (history_size=6).


### wf...@chromium.org (2013-08-13)

[Empty comment from Monorail migration]

### wf...@chromium.org (2013-08-13)

[Empty comment from Monorail migration]

### pd...@chromium.org (2013-08-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-08-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5890470404161536

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61300002dc10
Crash State:
  - crash stack -
  xsltApplySequenceConstructor
  xsltApplyXSLTTemplate
  - free stack -
  xsltFreeStylePreComps
  xsltFreeStylesheet
  

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97D5KXmf-Oi4FPqAJccJz_7gHCiBFwysxeRU0sTo1xOK-m3Qw5mVvk1RIbxMGad5TrZCZvxON-W5AIS4_PGfGzF8pO46fDs0s57ZOdU2JuFIpL32qIqX4TRVSymE_Xt3M5lxSHaZqksR5g6mNKrJWp6HuxwGw

Fully reproducible crash found using linux_tsan_chrome_mp job type (history_size=6).


### pd...@chromium.org (2013-08-14)

Handing off to fmalita (my plate is getting full)

### fm...@chromium.org (2013-08-16)

This smells like an libxslt bug:

* xsltParseStylesheetImportedDoc calls xsltFreeStylesheet(retStyle) when parsing fails (https://code.google.com/p/chromium/codesearch#chromium/src/third_party/libxslt/libxslt/xslt.c&q=Document.cpp&sq=package:chromium&type=cs&l=6638) and that appears to free not just the allocated result but also some data belonging to the xmlDoc
* later on, we call xsltParseStylesheetImportedDoc again from a different context but on the same xmlDoc, and we end up poking at deallocated mem

The common entry point above libxslt is XSLStyleSheet::compileStyleSheet(), so I think we can add a kludge there to prevent calling xsltParseStylesheetImportedDoc again after a failed compilation. Unless we think we should fix the morass called libxslt - which I'm not ready to sign up for :)

### in...@chromium.org (2013-08-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-08-16)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=156248

------------------------------------------------------------------------
r156248 | fmalita@chromium.org | 2013-08-16T22:40:22.606035Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/custom/invalid-xslt-crash.svg?r1=156248&r2=156247&pathrev=156248
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/TestExpectations?r1=156248&r2=156247&pathrev=156248
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/xml/XSLStyleSheetLibxslt.cpp?r1=156248&r2=156247&pathrev=156248
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/xml/XSLStyleSheet.h?r1=156248&r2=156247&pathrev=156248

Avoid reparsing an XSLT stylesheet after the first failure.

Certain libxslt versions appear to leave the doc in an invalid state when parsing fails. We should cache this result and avoid re-parsing.

(The test cannot be converted to text-only due to its invalid stylesheet).

R=inferno@chromium.org,abarth@chromium.org,pdr@chromium.org
BUG=271939

Review URL: https://chromiumcodereview.appspot.com/23103007
------------------------------------------------------------------------

### in...@chromium.org (2013-08-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-12)

Please merge your change to the m30 branch (1599) by early next week [using drover]. We have m30 beta coming next week and we want all the security changes in by that time. 

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### pd...@chromium.org (2013-09-16)

Assigning to myself for the merge

### pd...@chromium.org (2013-09-16)

Merged as https://src.chromium.org/viewvc/blink?view=rev&revision=157838

### pd...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-09-16)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157838

------------------------------------------------------------------------
r157838 | pdr@chromium.org | 2013-09-16T18:06:39.096247Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1599/LayoutTests/svg/custom/invalid-xslt-crash.svg?r1=157838&r2=157837&pathrev=157838
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/LayoutTests/TestExpectations?r1=157838&r2=157837&pathrev=157838
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/xml/XSLStyleSheetLibxslt.cpp?r1=157838&r2=157837&pathrev=157838
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/xml/XSLStyleSheet.h?r1=157838&r2=157837&pathrev=157838

Merge 156248 "Avoid reparsing an XSLT stylesheet after the first..."

> Avoid reparsing an XSLT stylesheet after the first failure.
> 
> Certain libxslt versions appear to leave the doc in an invalid state when parsing fails. We should cache this result and avoid re-parsing.
> 
> (The test cannot be converted to text-only due to its invalid stylesheet).
> 
> R=inferno@chromium.org,abarth@chromium.org,pdr@chromium.org
> BUG=271939
> 
> Review URL: https://chromiumcodereview.appspot.com/23103007

TBR=fmalita@chromium.org

Review URL: https://codereview.chromium.org/23868029
------------------------------------------------------------------------

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-18)

ClusterFuzz thinks that this bug might be eligible for a reward! Forwarding to reward panel for consideration.

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mb...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-28)

Looks hard to control the free / use

### pa...@chromium.org (2013-10-18)

Payment sent out on this one too.

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### gl...@chromium.org (2015-06-29)

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/271939?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SVG, Blink>XML]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077922)*

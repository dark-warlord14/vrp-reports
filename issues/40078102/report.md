# ASSERTION FAILED: m_pendingActivityCount > 0, Heap-use-after-free in WebCore::XMLHttpRequest::open

| Field | Value |
|-------|-------|
| **Issue ID** | [40078102](https://issues.chromium.org/issues/40078102) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Network>XHR |
| **Reporter** | at...@gmail.com |
| **Assignee** | ty...@chromium.org |
| **Created** | 2013-09-16 |
| **Bounty** | $1,000.00 |

## Description


Tested on:

OS: Ubuntu 12.04

Chromium: ASAN 31.0.1632.0 (Developer Build 223309) 


Repro-file:

<script>
function addElement() {
    document.documentElement.appendChild(document.createTextNode('X'));
    xhr.open("GET", "", true);
}
document.addEventListener("DOMContentLoaded", addElement, false);
window.onload = addElement;
var xhr = new XMLHttpRequest;
function sendXHR()
{
    xhr.send();
}
window.addEventListener("DOMSubtreeModified", sendXHR);
addElement();
</script>

ASAN-report:

==4753==ERROR: AddressSanitizer: heap-use-after-free on address 0x6190000047b0 at pc 0x7f0a64a8f828 bp 0x7fff90eadf30 sp 0x7fff90eadf28
READ of size 4 at 0x6190000047b0 thread T0 (chrome)
    #0 0x7f0a64a8f827 in WebCore::XMLHttpRequest::open(WTF::String const&, WebCore::KURL const&, bool, WebCore::ExceptionState&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/xml/XMLHttpRequest.cpp:486:0
    #1 0x7f0a63f734c8 in WebCore::V8XMLHttpRequest::openMethodCustom(v8::FunctionCallbackInfo<v8::Value> const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/bindings/v8/custom/V8XMLHttpRequestCustom.cpp:195:0
    #2 0x7f0a63a22f2b in WebCore::XMLHttpRequestV8Internal::openMethodCallback(v8::FunctionCallbackInfo<v8::Value> const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/gen/blink/bindings/V8XMLHttpRequest.cpp:313:0
    #3 0x7f0a6131243f in v8::internal::FunctionCallbackArguments::Call(void (*)(v8::FunctionCallbackInfo<v8::Value> const&)) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/arguments.cc:56:0
    #4 0x7f0a60dcf078 in v8::internal::MaybeObject* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/builtins.cc:1272:0
.
.
.
freed by thread T0 (chrome) here:
    #0 0x7f0a5d0341b4 in __interceptor_free _asan_rtl_
    #1 0x7f0a64a8ea84 in open /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/xml/XMLHttpRequest.cpp:485
    #2 0x7f0a63f734c8 in openMethodCustom /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/bindings/v8/custom/V8XMLHttpRequestCustom.cpp:195
    #3 0x7f0a63a22f2b in openMethodCallback /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/gen/blink/bindings/V8XMLHttpRequest.cpp:313
    #4 0x7f0a6131243f in Call /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../v8/src/arguments.cc:56
.
.
.


## Timeline

### cl...@chromium.org (2013-09-16)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5118000403316736

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-16)

It should be definitely 

157609 12.09.2013 00:33:41, by tyoshino@chromium.org
Add Streams API support to XMLHttpRequest

Hidden behind the --enable-experimental-webkit-features flag.

Original Streams API spec is:
https://dvcs.w3.org/hg/streams-api/raw-file/tip/Overview.htm

How to read data from Stream in JavaScript is still under
discussion at this thread
http://lists.w3.org/Archives/Public/public-webapps/2013AprJun/0706.html
but integration with XHR is not controversial.

So, to allow APIs depending on Stream but not on JavaScript
Stream read/write API to start development (e.g. Media Source
Extensions API
https://dvcs.w3.org/hg/html-media/raw-file/tip/media-source/media-source.html),
I'd like to land XHR integration part.

BUG=169957

Review URL: https://chromiumcodereview.appspot.com/18883002
M /trunk/LayoutTests/fast/xmlhttprequest/xmlhttprequest-set-responsetype-expected.txt 
M /trunk/LayoutTests/fast/xmlhttprequest/xmlhttprequest-set-responsetype.html 
A /trunk/LayoutTests/http/tests/xmlhttprequest/response-stream-abort-expected.txt 
A /trunk/LayoutTests/http/tests/xmlhttprequest/response-stream-abort.html 
A /trunk/LayoutTests/http/tests/xmlhttprequest/response-stream-expected.txt 
A /trunk/LayoutTests/http/tests/xmlhttprequest/response-stream.html 
M /trunk/Source/bindings/v8/custom/V8XMLHttpRequestCustom.cpp 
M /trunk/Source/core/fileapi/Stream.cpp 
M /trunk/Source/core/fileapi/Stream.h 
M /trunk/Source/core/xml/XMLHttpRequest.cpp 
And 2 more

I will revert it once confirmed by ClusterFuzz regression range.

### cl...@chromium.org (2013-09-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5118000403316736

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x6190000065b0
Crash State:
  - crash stack -
  WebCore::XMLHttpRequest::open
  WebCore::V8XMLHttpRequest::openMethodCustom
  - free stack -
  WebCore::XMLHttpRequest::open
  WebCore::V8XMLHttpRequest::openMethodCustom
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=107314:107422

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95sF5rfcxghR-hFAIhWBJq0DDs1fdttSjSSc0MKQXPHGWSbDwFpGym30Fe4geS4Q6JHHHRwbwHuCvZ4kR735S66kuIQxhO-9ClZWcSblc2LupgZLVOFWEh16GRhc-vP4_E2H74qB344KGc90vn0qwbbcoUsHg



### in...@chromium.org (2013-09-16)

Looks like internalAbort can blow |this|. Weird, is this really a regression, or just became easier to reproduce now.

void XMLHttpRequest::open(const String& method, const KURL& url, bool async, ExceptionState& es)
{
    internalAbort();
    State previousState = m_state;

### cl...@chromium.org (2013-09-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5118000403316736

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x6190000065b0
Crash State:
  - crash stack -
  WebCore::XMLHttpRequest::open
  WebCore::V8XMLHttpRequest::openMethodCustom
  - free stack -
  WebCore::XMLHttpRequest::open
  WebCore::V8XMLHttpRequest::openMethodCustom
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=107314:107422

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95sF5rfcxghR-hFAIhWBJq0DDs1fdttSjSSc0MKQXPHGWSbDwFpGym30Fe4geS4Q6JHHHRwbwHuCvZ4kR735S66kuIQxhO-9ClZWcSblc2LupgZLVOFWEh16GRhc-vP4_E2H74qB344KGc90vn0qwbbcoUsHg



### in...@chromium.org (2013-09-16)

This file is full of protects :(

void XMLHttpRequest::didTimeout()
{
    // internalAbort() calls dropProtection(), which may release the last reference.
    RefPtr<XMLHttpRequest> protect(this);

### in...@chromium.org (2013-09-16)

Shouldn't we always drop protection async ?

    if (async == DropProtectionAsync)
        dropProtectionSoon();
    else
        dropProtection();

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### ko...@chromium.org (2013-09-16)

We should drop sync where possible. If send() was called just after internalAbort(), it may drop pendingActivity for active m_loader.

### ty...@chromium.org (2013-09-17)

[Empty comment from Monorail migration]

### ty...@chromium.org (2013-09-17)

open() for onload invokes open() set for DOMContentLoaded via resource->removeClient(this) call in DocumentThreadableLoader.cpp.

1. open() invokes internalAbort()
2. m_loader->cancel() invokes open() again via RawResource
3. the open() call drops reference count
4. now, we're back to internalAbort() for the original open(). dropProtection() is called, and... aw snap.

### ty...@chromium.org (2013-09-17)

Correction.

First, DOMContentLoaded is called, and then onload is called.

### ty...@chromium.org (2013-09-17)

This is minimal case.

var xhr = new XMLHttpRequest;
document.addEventListener("DOMContentLoaded", function() { xhr.open("GET", true); xhr.send(); xhr.open("GET", true); });
window.onload = function() { xhr.open("GET", true); };

Quick fix is adding "if (m_loader) return;" between m_loader->cancel() and m_loader = 0.

### ty...@chromium.org (2013-09-17)

s/m_loader/!m_loader/

### ty...@chromium.org (2013-09-19)

[Empty comment from Monorail migration]

### ty...@chromium.org (2013-09-19)

We could take several ways to fix this e.g. fixing onload timing, but I'd like to just block reentrant of open(), send() and abort() while m_loader->cancel() is running by making them NOP and raising InvalidStateError to tell developers to refrain from using such code.

I'm writing a CL to do this. Tell me if you have any opinion.

### ty...@chromium.org (2013-09-19)

Uploaded: https://codereview.chromium.org/23465030/

FTR, this is old CL written by japhet to solve similar problem.
http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/xmlhttprequest/reentrant-cancel.html?pathrev=120845


### cl...@chromium.org (2013-09-19)

[Comment Deleted]

### cl...@chromium.org (2013-09-19)

[Comment Deleted]

### cl...@chromium.org (2013-09-19)

[Comment Deleted]

### ty...@chromium.org (2013-09-19)

Looks like the path leading to synchronous onload invocation is as follows (not confirmed)

Resource::allClientsRemoved
Resource::cancelTimerFired
ResourceLoader::cancelIfNotFinishing
ResourceLoader::cancel
Resource::error
Resource::checkNotify
DocumentLoader::notifyFinished
DocumentLoader::mainReceivedError
FrameLoader::receivedMainResourceError
FrameLoader::checkCompleted
Document::implicitClose


### ty...@chromium.org (2013-09-20)

Uploaded new CL: https://codereview.chromium.org/24304004/

in response to discussion with japhet@ on the previous CL.

### in...@chromium.org (2013-09-21)

https://src.chromium.org/viewvc/blink?view=rev&revision=158146

### bu...@chromium.org (2013-09-21)

Is there a merge required here?

### cl...@chromium.org (2013-09-21)

Adding Merge-Approved to track merges across stable and beta branches. Please do not merge without checking with the release manager first. If the fix is not applicable for merge, change this label to Merge-NA.

### cl...@chromium.org (2013-09-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-09-23)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=158046

------------------------------------------------------------------------
r158046 | tyoshino@chromium.org | 2013-09-19T19:46:41.497981Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/xmlhttprequest/cross-site-denied-response-sync-2.html?r1=158046&r2=158045&pathrev=158046
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/xml/XMLHttpRequest.h?r1=158046&r2=158045&pathrev=158046
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/xmlhttprequest/xmlhttprequest-sync-no-progress-events-expected.txt?r1=158046&r2=158045&pathrev=158046
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/xmlhttprequest/onloadend-event-after-sync-requests-expected.txt?r1=158046&r2=158045&pathrev=158046
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/xmlhttprequest/connection-error-sync.html?r1=158046&r2=158045&pathrev=158046
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/xmlhttprequest/xmlhttprequest-unsafe-redirect-expected.txt?r1=158046&r2=158045&pathrev=158046
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/xmlhttprequest/onloadend-event-after-sync-requests.html?r1=158046&r2=158045&pathrev=158046
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/xml/XMLHttpRequest.cpp?r1=158046&r2=158045&pathrev=158046

Don't dispatch events when XHR is set to sync mode

Any of readystatechange, progress, abort, error, timeout and loadend
event are not specified to be dispatched in sync mode in the latest
spec. Just an exception corresponding to the failure is thrown.

Clean up for readability done in this CL
- factor out dispatchEventAndLoadEnd calling code
- make didTimeout() private
- give error handling methods more descriptive names
- set m_exceptionCode in failure type specific methods
-- Note that for didFailRedirectCheck, m_exceptionCode was not set
   in networkError(), but was set at the end of createRequest()

This CL is prep for fixing crbug.com/292422

BUG=292422

Review URL: https://chromiumcodereview.appspot.com/24225002
------------------------------------------------------------------------

### bu...@chromium.org (2013-09-23)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=158146

------------------------------------------------------------------------
r158146 | tyoshino@chromium.org | 2013-09-21T01:35:32.585008Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/xml/XMLHttpRequest.cpp?r1=158146&r2=158145&pathrev=158146
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/xml/XMLHttpRequest.h?r1=158146&r2=158145&pathrev=158146
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/xmlhttprequest/reentrant-cancel-expected.txt?r1=158146&r2=158145&pathrev=158146

[XHR] Abort method execution when m_loader->cancel() in internalAbort() caused reentry

Calling cancel() on DocumentThreadableLoader may results in calling
window.onload synchronously. If open(), send(), etc. are called on the same
XMLHttpRequest object, it'll be hard to resolve conflict of states without
losing spec conformance. This CL avoids that by just aborting execution of
code for the outer method that calls internalAbort() if it returns false.

BUG=292422

Review URL: https://chromiumcodereview.appspot.com/24304004
------------------------------------------------------------------------

### ka...@google.com (2013-09-23)

we'll let this bake a bit aarya said.

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### ty...@chromium.org (2013-09-26)

OK. I'll wait for another approval from kareng@.

### ty...@chromium.org (2013-09-26)

FYI, filed another bug for long-term fix. crbug.com/298662

### aa...@google.com (2013-10-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-10-02)

Migrating old milestone labels.

### ka...@google.com (2013-10-04)

pls merge to M30 - branch 1599 and then switch mstone to 31 and re-request merge. ty.

### ty...@chromium.org (2013-10-07)

Merge done. Blink 158146 into Blink branch for Chromium 1599
https://codereview.chromium.org/26209004/

Changing to M31 and set Merge-Requested tag again.

### la...@google.com (2013-10-07)

We branched Blink at r158192 (which should include 158146).

### in...@chromium.org (2013-10-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-10-07)

add merge label based on c#37

### ty...@chromium.org (2013-10-08)

Ah, yes. M31 doesn't need merge.

### ke...@google.com (2013-10-08)

This merge is causing the branch to not compile on all platforms.  I've reverted.  Please watch your merges in the future.

http://master.chrome.corp.google.com:8010/builders/precise64/builds/556/steps/compile/logs/stdio
http://go/stablebuilders

### ty...@chromium.org (2013-10-08)

Sorry about the breakage. Fix is in. Builder is running now.

### ty...@chromium.org (2013-10-08)

Compilation successful on all platforms. No new failure considered to be related to this change found.

### bu...@chromium.org (2013-10-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=159004

------------------------------------------------------------------------
r159004 | tyoshino@chromium.org | 2013-10-07T05:36:03.312738Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/xml/XMLHttpRequest.cpp?r1=159004&r2=159003&pathrev=159004
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/xml/XMLHttpRequest.h?r1=159004&r2=159003&pathrev=159004
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/LayoutTests/http/tests/xmlhttprequest/reentrant-cancel-expected.txt?r1=159004&r2=159003&pathrev=159004

Merge 158146 "[XHR] Abort method execution when m_loader->cancel..."

> [XHR] Abort method execution when m_loader->cancel() in internalAbort() caused reentry
> 
> Calling cancel() on DocumentThreadableLoader may results in calling
> window.onload synchronously. If open(), send(), etc. are called on the same
> XMLHttpRequest object, it'll be hard to resolve conflict of states without
> losing spec conformance. This CL avoids that by just aborting execution of
> code for the outer method that calls internalAbort() if it returns false.
> 
> BUG=292422
> 
> Review URL: https://chromiumcodereview.appspot.com/24304004

TBR=tyoshino@chromium.org

Review URL: https://codereview.chromium.org/26209004
------------------------------------------------------------------------

### bu...@chromium.org (2013-10-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=159087

------------------------------------------------------------------------
r159087 | kerz@chromium.org | 2013-10-08T04:36:45.439191Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/xml/XMLHttpRequest.cpp?r1=159087&r2=159086&pathrev=159087
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/xml/XMLHttpRequest.h?r1=159087&r2=159086&pathrev=159087
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/LayoutTests/http/tests/xmlhttprequest/reentrant-cancel-expected.txt?r1=159087&r2=159086&pathrev=159087

Revert 159004 "Merge 158146 "[XHR] Abort method execution when m..."
This broke the 1599 branch.

> Merge 158146 "[XHR] Abort method execution when m_loader->cancel..."
> 
> > [XHR] Abort method execution when m_loader->cancel() in internalAbort() caused reentry
> > 
> > Calling cancel() on DocumentThreadableLoader may results in calling
> > window.onload synchronously. If open(), send(), etc. are called on the same
> > XMLHttpRequest object, it'll be hard to resolve conflict of states without
> > losing spec conformance. This CL avoids that by just aborting execution of
> > code for the outer method that calls internalAbort() if it returns false.
> > 
> > BUG=292422
> > 
> > Review URL: https://chromiumcodereview.appspot.com/24304004
> 
> TBR=tyoshino@chromium.org
> 
> Review URL: https://codereview.chromium.org/26209004

TBR=tyoshino@chromium.org

Review URL: https://codereview.chromium.org/26341006
------------------------------------------------------------------------

### bu...@chromium.org (2013-10-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=159105

------------------------------------------------------------------------
r159105 | tyoshino@chromium.org | 2013-10-08T07:25:39.397027Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/LayoutTests/http/tests/xmlhttprequest/reentrant-cancel-expected.txt?r1=159105&r2=159104&pathrev=159105
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/xml/XMLHttpRequest.cpp?r1=159105&r2=159104&pathrev=159105
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/xml/XMLHttpRequest.h?r1=159105&r2=159104&pathrev=159105

Revert 159087 "Revert 159004 "Merge 158146 "[XHR] Abort method e..."

Fixed compilation error.

> Revert 159004 "Merge 158146 "[XHR] Abort method execution when m..."
> This broke the 1599 branch.
> 
> > Merge 158146 "[XHR] Abort method execution when m_loader->cancel..."
> > 
> > > [XHR] Abort method execution when m_loader->cancel() in internalAbort() caused reentry
> > > 
> > > Calling cancel() on DocumentThreadableLoader may results in calling
> > > window.onload synchronously. If open(), send(), etc. are called on the same
> > > XMLHttpRequest object, it'll be hard to resolve conflict of states without
> > > losing spec conformance. This CL avoids that by just aborting execution of
> > > code for the outer method that calls internalAbort() if it returns false.
> > > 
> > > BUG=292422
> > > 
> > > Review URL: https://chromiumcodereview.appspot.com/24304004
> > 
> > TBR=tyoshino@chromium.org
> > 
> > Review URL: https://codereview.chromium.org/26209004
> 
> TBR=tyoshino@chromium.org
> 
> Review URL: https://codereview.chromium.org/26341006

TBR=kerz@chromium.org

BUG=292422

Review URL: https://codereview.chromium.org/26114005
------------------------------------------------------------------------

### mb...@google.com (2013-10-09)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-10-12)

$1000 since there does not seem to be control between the free and use.

### pa...@chromium.org (2013-10-18)

Payment sent out on this one too.

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### tk...@chromium.org (2015-11-27)

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

This issue was migrated from crbug.com/chromium/292422?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078102)*

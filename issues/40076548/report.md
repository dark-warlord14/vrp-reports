# Heap-use-after-free in WebCore::SVGDocumentExtensions::removeAllElementReferencesForTarget

| Field | Value |
|-------|-------|
| **Issue ID** | [40076548](https://issues.chromium.org/issues/40076548) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>SVG |
| **Reporter** | at...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2012-11-04 |
| **Bounty** | $1,000.00 |

## Description


Repro-file as attachment.

Tested on: 

ASAN Chrome 25.0.1316.0 (Developer Build 165738) 

ASAN-report:

==2771== ERROR: AddressSanitizer heap-use-after-free on address 0x7f80d58b2240 at pc 0x7f81084752fb bp 0x7fff2272d670 sp 0x7fff2272d668
READ of size 8 at 0x7f80d58b2240 thread T0
    #0 0x7f81084752fa in WebCore::SVGDocumentExtensions::removeAllElementReferencesForTarget(WebCore::SVGElement*) ???:0
    #1 0x7f810847df69 in WebCore::SVGElement::~SVGElement() ???:0
    #2 0x7f81086a2714 in WebCore::SVGPathElement::~SVGPathElement() ???:0
    #3 0x7f8108747f15 in WebCore::ContainerNode::removeAllChildren() ???:0
    #4 0x7f810877b330 in WebCore::Document::removedLastRef() ???:0
    #5 0x7f810ab8d7c0 in v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing(v8::internal::Isolate*, v8::internal::GlobalHandles*) ???:0
.
.
.
freed by thread T0 here:
    #0 0x7f810da976f0 in operator delete(void*) ??:0
    #1 0x7f8108747f15 in WebCore::ContainerNode::removeAllChildren() ???:0
    #2 0x7f810877b330 in WebCore::Document::removedLastRef() ???:0
    #3 0x7f810ab8d7c0 in v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing(v8::internal::Isolate*, v8::internal::GlobalHandles*) ???:0
    #4 0x7f810ab8d17e in v8::internal::GlobalHandles::PostGarbageCollectionProcessing(v8::internal::GarbageCollector) ???:0
    #5 0x7f810abacfb7 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GCTracer*) ???:0
    #6 0x7f810abab714 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollector, char const*, char const*) ???:0
.
.
.


## Attachments

- [chrome-heap-use-after-free-WebCoreSVGDocumentExtensionsremoveAllElementReferencesForTarget-6cb8.html](attachments/chrome-heap-use-after-free-WebCoreSVGDocumentExtensionsremoveAllElementReferencesForTarget-6cb8.html) (text/html; charset=us-ascii, 640 B)

## Timeline

### in...@chromium.org (2012-11-05)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-11-05)

I'll take it.

### sc...@chromium.org (2012-11-06)

This crashes reliably in debug builds, but I cannot reduce it to a DRT test. I've tried forcing GC but to no avail. Next is to try Asan builds and see if that reproduces reliably with forced gc.

### in...@chromium.org (2012-11-06)

did you add waitUntilDone() and notifyDone() ?

### sc...@chromium.org (2012-11-06)

Yes. Made sure I waited. Made sure I collected garbage.

The issue is that the crash seems to require the V8 handle for document to be released, and I don't see how to remove the last reference to document in a script in the document itself. Any ideas? Maybe put it in an object tag in another document?

### sc...@chromium.org (2012-11-06)

Turn out this is another Zimmermann screw up.

See this patch: https://bugs.webkit.org/show_bug.cgi?id=73860

Note that it is missing handling of mpath elements that also have xlink:href. It's also missing <use> and <tpath>, but those were added already.

I'll get a patch prepared on the plane tomorrow. Good news is that I might have a better way to test it now.

### pd...@chromium.org (2012-11-06)

I think Zimmerman can be exonerated on this count. This is likely a regression caused by a recent patch that added resource handling to <mpath>: http://trac.webkit.org/changeset/133074

I've never really trusted the author of that patch. We can assign it to him if you want.

### sc...@chromium.org (2012-11-07)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-11-08)

Patch up: https://bugs.webkit.org/show_bug.cgi?id=101505

Test is not great, but I tried to reduce it in every way I could think of and could not get it any faster.

### js...@chromium.org (2012-11-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-11-11)

I fixed Twister fuzzer. It is catching this now.

### in...@chromium.org (2012-11-11)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=137859794

Fuzzer: Inferno_twister_custom_bundle

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7fec06f79c40
Crash State:
  - crash stack -
  WebCore::SVGDocumentExtensions::removeAllElementReferencesForTarget
  WebCore::SVGElement::~SVGElement
  - free stack -
  WebCore::ContainerNode::removeAllChildren
  WebCore::Document::removedLastRef
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=165313:165320

Minimized Testcase (1.49 Kb): https://cluster-fuzz.appspot.com/download/AMIfv971lvStrynlEt7LC0RNXNA0FQdZojbdt4WQ6eeiN-qjIkYGmu3MpAz9awXkMnAfSqH-wK5KGwW8iqm8aO1Ehbv6qAcsIE4nR0Rv0mRjt8qpOamjqOhcny08oVBl2Vm0ZDnFxuAJhVmWDbJHstKCwS1JJBPE-q_d-0nPj7aYXsJN-5WShFc

Additional requirements: Requires Interaction Gestures

### in...@chromium.org (2012-11-16)

http://trac.webkit.org/changeset/134851

### cl...@chromium.org (2012-11-17)

ClusterFuzz has detected this issue as fixed in range 168170:168178.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=137859794

Fuzzer: Inferno_twister_custom_bundle

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7fec06f79c40
Crash State:
  - crash stack -
  WebCore::SVGDocumentExtensions::removeAllElementReferencesForTarget
  WebCore::SVGElement::~SVGElement
  - free stack -
  WebCore::ContainerNode::removeAllChildren
  WebCore::Document::removedLastRef
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=165313:165320
Fixed: https://cluster-fuzz.appspot.com/revisions?range=168170:168178

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv971lvStrynlEt7LC0RNXNA0FQdZojbdt4WQ6eeiN-qjIkYGmu3MpAz9awXkMnAfSqH-wK5KGwW8iqm8aO1Ehbv6qAcsIE4nR0Rv0mRjt8qpOamjqOhcny08oVBl2Vm0ZDnFxuAJhVmWDbJHstKCwS1JJBPE-q_d-0nPj7aYXsJN-5WShFc

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-11-20)

"Merge-Approved" seems incorrect for what is labeled as a trunk regression, and fixed before the branch point.


### in...@chromium.org (2012-11-20)

yes, that was wrong.

### sc...@gmail.com (2012-11-24)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-11-24)

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

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-06-25)

Old bug is old! $1000

### pa...@chromium.org (2013-08-20)

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

This issue was migrated from crbug.com/chromium/159338?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SVG]
[Monorail mergedwith: crbug.com/chromium/162454]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076548)*

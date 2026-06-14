# ASSERTION FAILED: !needsLayout(), UNKNOWN in WebCore::RenderSVGResourceClipper::applyClippingToContext

| Field | Value |
|-------|-------|
| **Issue ID** | [40078024](https://issues.chromium.org/issues/40078024) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | fm...@chromium.org |
| **Created** | 2013-08-31 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4738863507439616

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0000977537dd
Crash State:
  - crash stack -
  WebCore::RenderSVGResourceMasker::applyResource
  WebCore::SVGRenderingContext::prepareToRenderSVGContent
  WebCore::RenderSVGRoot::paintReplaced
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=220409:220463

Minimized Testcase (5.58 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94ub7cittjSedwniCjb0odK-Jf8GaiJm39ARo_bpwP8STlufZFGgQcLBPCrlKrPKocN5N3oYAHSbm_ffgFRbzuSxJIkE-6XcGBHcEQrlYTiiDlxT1E7aeAWOU6i8EUFp3yH5yvgtnDLkCOcnvVpiMPCBSDogw

## Attachments

- [layout_assert.html](attachments/layout_assert.html) (text/html; charset=us-ascii, 418 B)

## Timeline

### in...@chromium.org (2013-08-31)

Hey Philip, I think this assert was marked as a security assert. Do you remember that if this always led to use-after-free. This was found by an external reporter fuzzer, so we would need to consider for rewards.

### pd...@chromium.org (2013-09-01)

@inferno, this was always a debug-only assert because it requires re-walking the render tree after layout which would be too slow in non-debug builds. I should have made this a security assert though (albeit behind #ifdef NDEBUG). I'll post a patch shortly to fix that.

Assigning this bug to fmalita.

### in...@chromium.org (2013-09-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-03)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5595356221931520

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0000977537dd
Crash State:
  - crash stack -
  WebCore::RenderSVGResourceClipper::applyClippingToContext
  WebCore::RenderSVGResourceClipper::applyResource
  WebCore::SVGRenderingContext::prepareToRenderSVGContent
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=220409:220463

Minimized Testcase (1.23 Kb): https://cluster-fuzz.appspot.com/download/AMIfv957TqCSGRm6-QivYgOWnXX2BsFQCqnTkq7hfp2K1NW3IILlpN_dF37rY8LMALvAXrRo2Chp78oZl25VtgqSovgq9csllOfGonO5DNNAV4XmH7sNnaUHuN0iV01STrdTvzeUfZDLttR-eMee9YY8D3yuB_8ORw



### bu...@chromium.org (2013-09-03)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157153

------------------------------------------------------------------------
r157153 | pdr@chromium.org | 2013-09-03T21:48:00.499957Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/page/FrameView.cpp?r1=157153&r2=157152&pathrev=157153

Change post-layout !needsLayout assert to ASSERT_WITH_SECURITY_IMPL

Hitting this assertion has security implications and should be marked
as such. Unfortunately, for performance reasons we cannot do this
for release builds.

BUG=282925

Review URL: https://chromiumcodereview.appspot.com/23819017
------------------------------------------------------------------------

### in...@chromium.org (2013-09-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-06)

ClusterFuzz has detected this issue as fixed in range 220708:220715.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5595356221931520

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0000977537dd
Crash State:
  - crash stack -
  WebCore::RenderSVGResourceClipper::applyClippingToContext
  WebCore::RenderSVGResourceClipper::applyResource
  WebCore::SVGRenderingContext::prepareToRenderSVGContent
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=220409:220463
Fixed: https://cluster-fuzz.appspot.com/revisions?range=220708:220715

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv957TqCSGRm6-QivYgOWnXX2BsFQCqnTkq7hfp2K1NW3IILlpN_dF37rY8LMALvAXrRo2Chp78oZl25VtgqSovgq9csllOfGonO5DNNAV4XmH7sNnaUHuN0iV01STrdTvzeUfZDLttR-eMee9YY8D3yuB_8ORw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-09-06)

fmalita@, any idea what fixed this from the fixed range above ?

### cl...@chromium.org (2013-09-09)

ClusterFuzz has detected this issue as fixed in range 220661:220700.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4738863507439616

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0000977537dd
Crash State:
  - crash stack -
  WebCore::RenderSVGResourceMasker::applyResource
  WebCore::SVGRenderingContext::prepareToRenderSVGContent
  WebCore::RenderSVGRoot::paintReplaced
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=220409:220463
Fixed: https://cluster-fuzz.appspot.com/revisions?range=220661:220700

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94ub7cittjSedwniCjb0odK-Jf8GaiJm39ARo_bpwP8STlufZFGgQcLBPCrlKrPKocN5N3oYAHSbm_ffgFRbzuSxJIkE-6XcGBHcEQrlYTiiDlxT1E7aeAWOU6i8EUFp3yH5yvgtnDLkCOcnvVpiMPCBSDogw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### fm...@chromium.org (2013-09-09)

inferno@: I don't see anything related, no idea. The minimized test case still asserts (but earlier, after r157153).

### cl...@chromium.org (2013-09-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4871021530185728

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0000977537dd
Crash State:
  - crash stack -
  WebCore::RenderSVGResourceMasker::applyResource
  WebCore::SVGRenderingContext::prepareToRenderSVGContent
  WebCore::RenderSVGShape::paint
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=220409:220463

Minimized Testcase (2.52 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96GktCM7eNr0lXIrWXXUhN16ohsf8qRakcDWcEjtZeJPRteBnnjhjdrbLg9GtUmG83ne3iTzjM-4wvb_rUcJZiPKeAiceDlK7sjey4iM1n-JJnOLazfOq7bdXEdgVcXyyq-nwUM1rBVDfr7iFqzlbeZ1ai6gg

Additional requirements: Requires Interaction Gestures



### in...@chromium.org (2013-09-09)

Yes, the bug still exists. testcase https://crbug.com/chromium/282925#c11 came up.

### cl...@chromium.org (2013-09-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5023153566777344

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0000977537dd
Crash State:
  - crash stack -
  WebCore::RenderSVGResourceClipper::applyClippingToContext
  WebCore::RenderSVGResourceClipper::applyResource
  WebCore::SVGRenderingContext::prepareToRenderSVGContent
  

Minimized Testcase (2.55 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96iknKhYe5bEI4N8Xfi_fi0nEmXCSgY7ZRENpZyEHRmSXfud2tkTB54aNuddOVySriNEPs1xXEqNCLzx3soWkHhDq6cAou-BSMScgu3lP-Yr8pAdB8nFRydTXpnTK2MxvrpWftU7Bv2f4q2TVt9nGq_XPkEYA



### fm...@chromium.org (2013-09-09)

I suspect the root cause is unrelated to the svg mask/clip refactoring - we're just hitting these newly introduced ASSERTs now.

Still investigating. Attaching a minimized filter-only test that triggers pdr's FrameView::layout() assert.


### fm...@chromium.org (2013-09-09)

This goes back to our unsound handling of resource dependencies in SVG:

<svg id="svg1" filter="url(#f)"/>
<svg if="svg2">
  <filter id="f"/>
</svg>

* the resource #f lives under svg2, but is being applied to svg1
* during svg2/filter layout, we trigger removeAllClientsFromCache(), which (re)tags #f's svg1 client for layout
* if this happens after svg1 was laid out, well, tough luck :(

Note that there's a kludge in RenderSVGRoot::layout() that attempts to deal with removeAllClientsFromCache() side effects: we're calling SVGRenderSupport::layoutChildren() a second time (per comment - "// Invalidate resource clients, which may mark some nodes for layout."). The problem in this case is that svg1 is not a child of svg2 and there's no common RenderSVGRoot ancestor because these are independent fragments in an HTML doc.


### cl...@chromium.org (2013-09-10)

ClusterFuzz has detected this issue as fixed in range 221913:221928.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5023153566777344

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0000977537dd
Crash State:
  - crash stack -
  WebCore::RenderSVGResourceClipper::applyClippingToContext
  WebCore::RenderSVGResourceClipper::applyResource
  WebCore::SVGRenderingContext::prepareToRenderSVGContent
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=221913:221928

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96iknKhYe5bEI4N8Xfi_fi0nEmXCSgY7ZRENpZyEHRmSXfud2tkTB54aNuddOVySriNEPs1xXEqNCLzx3soWkHhDq6cAou-BSMScgu3lP-Yr8pAdB8nFRydTXpnTK2MxvrpWftU7Bv2f4q2TVt9nGq_XPkEYA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### fm...@chromium.org (2013-09-11)

Here's an even more nightmarish scenario:

<svg id="svg1" filter="url(#f2)"><filter id="f1"/></svg>
<svg id="svg2" filter="url(#f1)"><filter id="f2"/></svg>

Deadly embrace FTW: laying out any SVG element re-tags the other one for layout :(

Converting to a DAG will not solve this since the current representation would introduce a cycle. We really need to rethink the whole resources mechanism and what/when needs to be re-laid-out - FF has no problem dealing with this...

### sc...@chromium.org (2013-09-12)

I thought that the cycle detector caught these cases and fails to create the second filter. If not, it should.

### fm...@chromium.org (2013-09-12)

I think the cycle detector is only concerned with reference cycles. That's not the case here: what we have is a layout dependency cycle. (There's also some cycle detection logic at applyResource time, but that's too late.)

A couple of questions:

1) is there really a fundamental cycle in the example above, or is it just an implementation-imposed cycle? Like I said, FF seems to deal with this case just fine and draws both filters. The main problem I believe is we're tying the layout of the resource container to the layout of its enclosing element - it seems it should be linked to the target instead (but since it can be applied to multiple targets, maybe the solution is instancing?).

2) even if we decide that it's a a cycle and shouldn't support it, we still have the related problem in c#15, which is obviously cycle for any interpretation of "cycle".

### fm...@chromium.org (2013-09-12)

"which is obviously cycle"

err, meant cycle-free.

### sc...@chromium.org (2013-09-12)

I think a DAG would fix this. We need the <filter> elements to be laid out before either of the <svg> elements, which is possible to do. I think that's actually the heart of all these problems: by putting resources into the render tree, rather than evaluating them first, we (meaning those who went before) have create the cycles. Surely there's a better way.

### fm...@chromium.org (2013-09-12)

Agreed: a DAG + breaking the enclosing_elem -> resource dependency would solve this. (my initial DAG comment was missing the second part).

### fm...@chromium.org (2013-09-18)

CCing folks from duplicate issues.

### in...@chromium.org (2013-09-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-18)

Fixing impact labels.

### in...@chromium.org (2013-09-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mi...@gmail.com (2013-09-26)

can I have the repro case please?

### cl...@chromium.org (2013-09-27)

fmalita@: you haven't provided any bug update or come up with a fix for this issue in the last 7 days. Please note that this is a medium+ severity security vulnerability that needs your immediate response. If you have a patch in progress and don't want future nags, please add a codereview link and a WIP label. If the issue is already fixed or you can't reproduce it, please close the bug.

### fm...@chromium.org (2013-09-27)

[Empty comment from Monorail migration]

### fm...@chromium.org (2013-09-27)

WIP CL: https://codereview.chromium.org/23785014/

### fm...@chromium.org (2013-09-27)

miaubiz: 

(inferno mentioned you know how to access the repro by now)

Note that this is likely no longer triggering - the condition is now caught by a higher level ASSERT added recently:

ASSERTION FAILED: !needsLayout()
../../third_party/WebKit/Source/core/rendering/RenderObject.h(240) : void WebCore::RenderObject::assertRendererLaidOut() const

### bu...@chromium.org (2013-09-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=158480

------------------------------------------------------------------------
r158480 | fmalita@chromium.org | 2013-09-28T04:17:17.586364Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/custom/cross-referenced-resources-expected.html?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/custom/unicode-in-tspan-multi-svg-crash.html?r1=158480&r2=158479&pathrev=158480
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/custom/cross-referenced-resources.html?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/svg/SVGResources.cpp?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/svg/SVGRenderSupport.cpp?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGElement.cpp?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/svg/SVGResources.h?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/svg/SVGRenderSupport.h?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/custom/unicode-in-tspan-multi-svg-crash-expected.txt?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGElement.h?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/svg/RenderSVGRoot.cpp?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/text/text-layout-crash-expected.txt?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/svg/RenderSVGRoot.h?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/svg/RenderSVGResourceMarker.cpp?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/svg/RenderSVGResourceContainer.cpp?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderView.cpp?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGSVGElement.cpp?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/svg/RenderSVGResourceContainer.h?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/custom/circular-marker-reference-4-expected.txt?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/TestExpectations?r1=158480&r2=158479&pathrev=158480
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/platform/win/svg/W3C-SVG-1.1/masking-path-04-b-expected.txt?r1=158480&r2=158479&pathrev=158480

[SVG] Resources should be laid out in dependecy order.

We're currently laying out resources in tree order, while they are
(conceptually) forming a DAG - and this disconnect results in
complicated logic and an extra layout pass attempting to re-validate
nodes that might have been invalidated by the resource layout. This is
broken in (at least) two ways:

  * two passes are not guaranteed to be enough, we could need an
    arbitrary number of passes to stabilize the tree.
  * the re-layout logic hangs off RenderSVGRoot, and falls apart when
    multiple root nodes are present (html doc with multiple svg fragments).

Recently introduced asserts are testing for render tree nodes which are
still marked for layout at paint time, and are catching several invariant
violations due to the above.

To address this problem, we should lay out resources in transitive
dependency order (where node A depends on resource B if it references
it directly: <rect id="a" filter="url(#b)"/>). Turns out this is not as
complicated as it sounds, and we can avoid building an explicit resources
DAG because we already have the sparse version: each node tracks the list
of resources it is referencing.

So before laying out a node, we should ensure that its resources are laid
out first. Applying this recursively, we are effectively traversing the
dependency DAG in the correct order.

(This relies on the assumption that a resource' layout does not depend on
its in-tree parent layout - which should be the case as resources only
make sense in the context of their clients).

The CL also removes the RenderSVGRoot re-layout logic added in
http://trac.webkit.org/changeset/111601 as it is no longer needed: a
resource is now guaranteed to be laid out before any of its clients.

BUG=282925,294237,294238
R=pdr@chromium.org,schenney@chromium.org,dschulze@chromium.org,ojan@chromium.org,eseidel@chromium.org

Review URL: https://chromiumcodereview.appspot.com/23785014
------------------------------------------------------------------------

### in...@chromium.org (2013-09-28)

So amazing to see this getting fixed. Thanks a lot Florin.

### sc...@gmail.com (2013-09-28)

+1 for a refactor that improves stability, security, code quality :D

### cl...@chromium.org (2013-09-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-28)

Adding Merge-Approved to track merges across stable and beta branches. Please do not merge without checking with the release manager first. If the fix is not applicable for merge, change this label to Merge-NA.

### cl...@chromium.org (2013-09-30)

ClusterFuzz has detected this issue as fixed in range 225895:225905.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4871021530185728

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0000977537dd
Crash State:
  - crash stack -
  WebCore::RenderSVGResourceMasker::applyResource
  WebCore::SVGRenderingContext::prepareToRenderSVGContent
  WebCore::RenderSVGShape::paint
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=220409:220463
Fixed: https://cluster-fuzz.appspot.com/revisions?range=225895:225905

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96GktCM7eNr0lXIrWXXUhN16ohsf8qRakcDWcEjtZeJPRteBnnjhjdrbLg9GtUmG83ne3iTzjM-4wvb_rUcJZiPKeAiceDlK7sjey4iM1n-JJnOLazfOq7bdXEdgVcXyyq-nwUM1rBVDfr7iFqzlbeZ1ai6gg

Additional requirements: Requires Interaction Gestures

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### aa...@google.com (2013-10-01)

[Comment Deleted]

### cl...@chromium.org (2013-10-02)

Migrating old milestone labels.

### in...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone labels first. Make sure to re-request merge for every milestone in the Merge-To-M-* label. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2013-10-18)

[Empty comment from Monorail migration]

### la...@google.com (2013-10-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-10-21)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=160096

------------------------------------------------------------------------
r160096 | chrome-bot@google.com | 2013-10-21T16:45:05.599998Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/rendering/svg/RenderSVGResourceContainer.h?r1=160096&r2=160095&pathrev=160096
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/TestExpectations?r1=160096&r2=160095&pathrev=160096
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/platform/win/svg/W3C-SVG-1.1/masking-path-04-b-expected.txt?r1=160096&r2=160095&pathrev=160096
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/svg/custom/circular-marker-reference-4-expected.txt?r1=160096&r2=160095&pathrev=160096
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/svg/custom/unicode-in-tspan-multi-svg-crash.html?r1=160096&r2=160095&pathrev=160096
   A http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/svg/custom/cross-referenced-resources-expected.html?r1=160096&r2=160095&pathrev=160096
   A http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/svg/custom/cross-referenced-resources.html?r1=160096&r2=160095&pathrev=160096
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/rendering/svg/SVGResources.cpp?r1=160096&r2=160095&pathrev=160096
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/rendering/svg/SVGRenderSupport.cpp?r1=160096&r2=160095&pathrev=160096
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/svg/SVGElement.cpp?r1=160096&r2=160095&pathrev=160096
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/rendering/svg/SVGResources.h?r1=160096&r2=160095&pathrev=160096
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/svg/SVGElement.h?r1=160096&r2=160095&pathrev=160096
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/svg/custom/unicode-in-tspan-multi-svg-crash-expected.txt?r1=160096&r2=160095&pathrev=160096
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/rendering/svg/SVGRenderSupport.h?r1=160096&r2=160095&pathrev=160096
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/rendering/svg/RenderSVGRoot.cpp?r1=160096&r2=160095&pathrev=160096
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/svg/text/text-layout-crash-expected.txt?r1=160096&r2=160095&pathrev=160096
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/rendering/svg/RenderSVGRoot.h?r1=160096&r2=160095&pathrev=160096
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/rendering/svg/RenderSVGResourceMarker.cpp?r1=160096&r2=160095&pathrev=160096
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/rendering/svg/RenderSVGResourceContainer.cpp?r1=160096&r2=160095&pathrev=160096
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/rendering/RenderView.cpp?r1=160096&r2=160095&pathrev=160096
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/svg/SVGSVGElement.cpp?r1=160096&r2=160095&pathrev=160096

Merge 158480 "[SVG] Resources should be laid out in dependecy or..."

> [SVG] Resources should be laid out in dependecy order.
> 
> We're currently laying out resources in tree order, while they are
> (conceptually) forming a DAG - and this disconnect results in
> complicated logic and an extra layout pass attempting to re-validate
> nodes that might have been invalidated by the resource layout. This is
> broken in (at least) two ways:
> 
>   * two passes are not guaranteed to be enough, we could need an
>     arbitrary number of passes to stabilize the tree.
>   * the re-layout logic hangs off RenderSVGRoot, and falls apart when
>     multiple root nodes are present (html doc with multiple svg fragments).
> 
> Recently introduced asserts are testing for render tree nodes which are
> still marked for layout at paint time, and are catching several invariant
> violations due to the above.
> 
> To address this problem, we should lay out resources in transitive
> dependency order (where node A depends on resource B if it references
> it directly: <rect id="a" filter="url(#b)"/>). Turns out this is not as
> complicated as it sounds, and we can avoid building an explicit resources
> DAG because we already have the sparse version: each node tracks the list
> of resources it is referencing.
> 
> So before laying out a node, we should ensure that its resources are laid
> out first. Applying this recursively, we are effectively traversing the
> dependency DAG in the correct order.
> 
> (This relies on the assumption that a resource' layout does not depend on
> its in-tree parent layout - which should be the case as resources only
> make sense in the context of their clients).
> 
> The CL also removes the RenderSVGRoot re-layout logic added in
> http://trac.webkit.org/changeset/111601 as it is no longer needed: a
> resource is now guaranteed to be laid out before any of its clients.
> 
> BUG=282925,294237,294238
> R=pdr@chromium.org,schenney@chromium.org,dschulze@chromium.org,ojan@chromium.org,eseidel@chromium.org
> 
> Review URL: https://chromiumcodereview.appspot.com/23785014

TBR=inferno@chromium.org

Review URL: https://codereview.chromium.org/33043002
------------------------------------------------------------------------

### in...@chromium.org (2013-10-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-10-22)

Thanks for the report! This one qualifies for a $500 reward. The assert being hit here tends to lead to OOB reads.

### mb...@chromium.org (2013-11-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-12)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-14)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/282925?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/294237, crbug.com/chromium/294238]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078024)*

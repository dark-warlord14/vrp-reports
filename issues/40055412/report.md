# Heap-use-after-free in WebCore::SVGStyledElement::buildPendingResourcesIfNeeded

| Field | Value |
|-------|-------|
| **Issue ID** | [40055412](https://issues.chromium.org/issues/40055412) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>SVG |
| **Reporter** | ke...@chromium.org |
| **Assignee** | pd...@chromium.org |
| **Created** | 2012-03-22 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=29331092

Uploader: kenrb@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f8f887e6c80
Crash State:
  - crash stack -
  WebCore::SVGStyledElement::buildPendingResourcesIfNeeded
  WebCore::SVGStyledElement::svgAttributeChanged
  - free stack -
  WebCore::SVGElementInstance::detach
  WebCore::SVGUseElement::clearResourceReferences
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=124014:124069

Minimized Testcase (0.52 Kb): https://cluster-fuzz.appspot.com/download/AMIfv941jzCcmAgPrpDXybwHtuDiIJgplpFrPGshwY6hw93qe7maM-T89nOfiqpFszJMKrnuQQVt1fAVtjV9-xzkCHN__rJ-zvm557Relgaye1HheD--zCitqouvzVz3LLpW4po-znv0wvOO31L9u6Cb-SaTaY5GUw

## Timeline

### ke...@chromium.org (2012-03-22)

This is the remaining test case from Ax330d that was on https://crbug.com/chromium/118593.

pdr, are you able to have a look at this one also? It has a more recent regression range, though, so we could try to track down whose change caused the bug to occur.

### pd...@chromium.org (2012-03-22)

Thanks for putting this patch up kenrb. I am working on another blocker but I think I have a good patch there and I'll start on this one ASAP.

### in...@chromium.org (2012-03-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-22)

Thanks a lot Philip. Does adding WebKit-SVG label not add you guys to cc ?

### sc...@chromium.org (2012-03-22)

WebKit-SVG label only adds me. I then add pdr and/or fmalita if it seems relevant, or maybe someone else does.

### pd...@chromium.org (2012-03-24)

WebKit bug and patch: https://bugs.webkit.org/show_bug.cgi?id=82115

### sc...@chromium.org (2012-03-25)

WebKit Committed r112030: <http://trac.webkit.org/changeset/112030>

### sc...@gmail.com (2012-03-25)

[Empty comment from Monorail migration]

### ke...@chromium.org (2012-03-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2012-03-27)

ClusterFuzz has detected this issue as fixed in range 128733:128739.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=29331092

Uploader: kenrb@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f8f887e6c80
Crash State:
  - crash stack -
  WebCore::SVGStyledElement::buildPendingResourcesIfNeeded
  WebCore::SVGStyledElement::svgAttributeChanged
  - free stack -
  WebCore::SVGElementInstance::detach
  WebCore::SVGUseElement::clearResourceReferences
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=124014:124069
Fixed: https://cluster-fuzz.appspot.com/revisions?range=128733:128739

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv941jzCcmAgPrpDXybwHtuDiIJgplpFrPGshwY6hw93qe7maM-T89nOfiqpFszJMKrnuQQVt1fAVtjV9-xzkCHN__rJ-zvm557Relgaye1HheD--zCitqouvzVz3LLpW4po-znv0wvOO31L9u6Cb-SaTaY5GUw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-05-04)

Arthur, a separate root cause / patch for this repro so a separate reward!
$1000

### sc...@gmail.com (2012-05-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

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

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/119501?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055412)*

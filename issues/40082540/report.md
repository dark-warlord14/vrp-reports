# Use after free with nested use elements

| Field | Value |
|-------|-------|
| **Issue ID** | [40082540](https://issues.chromium.org/issues/40082540) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ku...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2010-08-05 |
| **Bounty** | $500.00 |

## Description

1.svg
==============================
<?xml version="1.0" standalone="no"?>
<svg width="100%" height="100%"  version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">  
<a id="crash">
			<pattern xlink:href="#crash">
			</pattern>
</a>										
<use xlink:href="#crash">
</use>
<a>
</svg>
==============================
test chromium 6.0.485.0 (54871) only
chrome and safari does not crash

## Attachments

- [crbug51252.svg](attachments/crbug51252.svg) (text/plain; charset=us-ascii, 193 B)
- [output.txt](attachments/output.txt) (text/x-c++; charset=utf-8, 4.3 KB)

## Timeline

### js...@chromium.org (2010-08-05)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-08-05)

This behaves like a duplicate of https://crbug.com/chromium/50712, but the code path after <use> destruction is entirely different. Even though they're probably the same underlying bug in destruction ordering, I'm keeping them separate until that's confirmed.


### ku...@gmail.com (2010-08-10)

<?xml version="1.0" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <g id="crash">
     <tspan fill="url(#fill)" />   <!-- tspan rect -->
  </g>																													
<a id="fill"/>  
<use xlink:href="#crash"/> 																								
<as>
</svg>

### js...@chromium.org (2010-08-12)

Oops. I forgot to list this when I reported upstream:
https://bugs.webkit.org/show_bug.cgi?id=43587


### js...@chromium.org (2010-08-16)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-08-16)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-08-19)

It turns out that the repro in https://crbug.com/chromium/51252#c1 of https://crbug.com/chromium/49596 can infrequently trigger this bug. So, we'll need to verify the fix against that repro. Triggering requires a location.reload() in the onload handler and letting it spin for up to 10 minutes.


### ku...@gmail.com (2010-08-20)

Yes fixed can you cc me?

### ku...@gmail.com (2010-08-20)

But #3 still crash chrome 7.0.500.0 (56781)
(bd4.8e4): Access violation - code c0000005 (!!! second chance !!!)
eax=0098e620 ebx=00a33200 ecx=0098e7e0 edx=0098e460 esi=00a3316c edi=00a18a00
eip=0098e620 esp=0041f02c ebp=00a573a0 iopl=0         nv up ei ng nz na pe cy
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010287
0098e620 40              inc     eax
0:000> .exr -1
ExceptionAddress: 0098e620
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000008
   Parameter[1]: 0098e620
Attempt to execute non-executable address 0098e620

### in...@chromium.org (2010-08-20)

kuzzcc, you should be getting email updates since you are the reporter of this bug. i just added you now explicitly to the cc list. just a fyi, the bug is still in 'Available' status which means it is still being worked upon. So, it is not fixed.

### in...@chromium.org (2010-08-26)

[Empty comment from Monorail migration]

### ke...@chromium.org (2010-09-03)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-09-04)

I worked the fix out yesterday. I should have a patch up for review shortly (just have to test some corner cases and work out some additional layout tests).


### js...@chromium.org (2010-09-06)

Landed upstream: http://trac.webkit.org/changeset/66847
There will be some layout test expectation updates following.

### sc...@gmail.com (2010-09-08)

@kuzzcc: congratulations! This report provisionally qualifies for a $500 Chromium Security Reward.
To increase chances of higher rewards, try not to confuse multiple issues in one bug and include crash details (faulting instruction and address; registers at time of fault; etc).

### in...@chromium.org (2010-09-08)

http://trac.webkit.org/search?q=RenderSVGResourceContainer.cpp was added on July 28th. We can punt this to M7, otherwise Justin, if you want to take a chance, please feel to manually identify the change and do the merge.

### in...@chromium.org (2010-09-09)

This has to be merged to 517 (v7), so i merged it. We branched off webkit at 66804. Not merged to v6 yet. So, retaining the status.

### bu...@gmail.com (2010-09-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=59011

------------------------------------------------------------------------
r59011 | cevans@chromium.org | Thu Sep 09 15:44:40 PDT 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/WebKit/472/WebCore/svg/SVGElement.cpp?r1=59011&r2=59010&pathrev=59011
 M http://src.chromium.org/viewvc/chrome/branches/WebKit/472/WebCore/rendering/RenderSVGResourceContainer.h?r1=59011&r2=59010&pathrev=59011
 M http://src.chromium.org/viewvc/chrome/branches/WebKit/472/WebCore/svg/SVGDocumentExtensions.cpp?r1=59011&r2=59010&pathrev=59011
 M http://src.chromium.org/viewvc/chrome/branches/WebKit/472/WebCore/svg/SVGDocumentExtensions.h?r1=59011&r2=59010&pathrev=59011

Manual merge of Justin's SVG fix.
See bug.

TEST=manual
BUG=51252
TBR=jschuh@chromium.org
Review URL: http://codereview.chromium.org/3329017
------------------------------------------------------------------------

### sc...@gmail.com (2010-09-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-09-22)

Payment is in the electronic system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

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

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/51252?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/51257, crbug.com/chromium/52224]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082540)*

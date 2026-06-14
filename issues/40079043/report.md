# Security: Integer Overflows in CharacterData::deleteData & CharacterData::replaceData

| Field | Value |
|-------|-------|
| **Issue ID** | [40079043](https://issues.chromium.org/issues/40079043) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM |
| **Reporter** | [Deleted User] |
| **Assignee** | [Deleted User] |
| **Created** | 2014-03-06 |
| **Bounty** | $1,500.00 |

## Description

**VULNERABILITY DETAILS**  

Both CharacterData::deleteData and CharacterData::replaceData do not properly check for integer overflows. This is shown in the following code from deleteData, where offset and count are both user-specified values.

unsigned realCount;  

if (offset + count > length())  

realCount = length() - offset;  

else  

realCount = count;  

...  

document().didRemoveText(this, offset, realCount);

didRemoveText eventually calls Range::didRemoveText, which updates the start and end offsets of the range with the invalid values. Very similar code is also present in replaceData.

The patches should be trivial, so I've assigned it to myself to work on.

**VERSION**  

Confirmed on stable (33.0.1750.146) on Windows and Linux, also confirmed on a LKGR (35.0.1867.0) build on Linux.

**REPRODUCTION CASE**  

A minimised testcase is attached. With assertions enabled, it triggers an assertion. Without assertions enabled, it doesn't crash, and the endOffset property of the range object can be observed to be above the length of the underlying text.

## Attachments

- [range_oob.html](attachments/range_oob.html) (text/html, 430 B)

## Timeline

### in...@chromium.org (2014-03-06)

Thanks Jon. Please make sure to change that assertion into ASSERT_WITH_SECURITY_IMPLICATION as part of your patch. Which assertion are we talking about here ?

### [Deleted User] (2014-03-06)

Ok, will do. The assertion in question is in editing/FrameSelection.cpp:386.

I'm just in the process of submitting another patch, once that one is done I'll submit this one too.

### in...@chromium.org (2014-03-06)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-03-06)

[Empty comment from Monorail migration]

### [Deleted User] (2014-03-06)

https://codereview.chromium.org/188693007/

Yet to update with layout tests, will wait to assign until I've finished that.

### pa...@chromium.org (2014-03-06)

[Empty comment from Monorail migration]

### [Deleted User] (2014-03-06)

Layout tests uploaded, patch out for review.

### [Deleted User] (2014-03-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-15)

jbutler@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-03-24)

jbutler@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### [Deleted User] (2014-03-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-31)

[Empty comment from Monorail migration]

### ia...@chromium.org (2014-04-08)

jbutler: any updates on this?

### in...@chromium.org (2014-04-09)

Sigbjornf@, can you please drive this to completion. Jbutler@ is an external contributor (ignore the @chromium account) and unfamiliar with the codebase and spec requirements. This is a high severity security vulnerability that has been open for 1.5 months, please help to close this soon.

### [Deleted User] (2014-04-09)

certainly, i can round off jbutler's CL & work.

### [Deleted User] (2014-04-09)

Created a separate CL, https://codereview.chromium.org/229793004/

### bu...@chromium.org (2014-04-09)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=171165

------------------------------------------------------------------
r171165 | sigbjornf@opera.com | 2014-04-09T19:00:32.975283Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/editing/FrameSelection.cpp?r1=171165&r2=171164&pathrev=171165
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/CharacterData.cpp?r1=171165&r2=171164&pathrev=171165
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/Range/deleteData-replaceData-count-overflow.html?r1=171165&r2=171164&pathrev=171165
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/Range/deleteData-replaceData-count-overflow-expected.txt?r1=171165&r2=171164&pathrev=171165

Add CharacterData.deleteData()/replaceData() overflow handling.

If the offset and count exceed the underlying length, the spec tells us

  http://dom.spec.whatwg.org/#concept-cd-replace (step 3)

to use a count that is equal to length minus the offset. Perform that
check in an overflow-sensitive manner.

(Change based on https://codereview.chromium.org/188693007/ )

R=
BUG=349898

Review URL: https://codereview.chromium.org/229793004
-----------------------------------------------------------------

### in...@chromium.org (2014-04-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-09)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### bu...@chromium.org (2014-04-10)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=171240

------------------------------------------------------------------
r171240 | yurys@chromium.org | 2014-04-10T07:41:11.808687Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/CharacterData.cpp?r1=171240&r2=171239&pathrev=171240

Fix compilation on Chromium OS after r171165

r171165 broke compilation on Chromium OS bot and we had to revert Blink roll.
...
../../../../../../../home/chrome-bot/chrome_root/src/third_party/WebKit/Source/core/dom/CharacterData.cpp:146:36:
error: 'realCount' may be used uninitialized in this function
...
I simply added initialization for realCount variables to make the compiler happy.

[1] http://build.chromium.org/p/chromium.chromiumos/builders/ChromiumOS%20%28x86%29/builds/20955

BUG=349898
TBR=sigbjornf@opera.com

Review URL: https://codereview.chromium.org/232243004
-----------------------------------------------------------------

### ti...@chromium.org (2014-04-17)

Merge Requested for M35. This hasn't baked enough for M34 Patch 1, so let's see if we can take it in M34 Patch 2 (providing there is one). 

Also removing jbutler@chromium.org from cc as account is disabled.

### ka...@google.com (2014-04-21)

approved for m35

### ti...@chromium.org (2014-04-22)

Yury - please merge into M35 (branch 1916)

### in...@chromium.org (2014-04-25)

merged to m35 in r172583, r172584, requesting for m34.

### bu...@chromium.org (2014-04-25)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=172584

------------------------------------------------------------------
r172584 | inferno@chromium.org | 2014-04-25T04:09:22.905450Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1916/Source/core/dom/CharacterData.cpp?r1=172584&r2=172583&pathrev=172584

Merge 171240 "Fix compilation on Chromium OS after r171165"

> Fix compilation on Chromium OS after r171165
> 
> r171165 broke compilation on Chromium OS bot and we had to revert Blink roll.
> ...
> ../../../../../../../home/chrome-bot/chrome_root/src/third_party/WebKit/Source/core/dom/CharacterData.cpp:146:36:
> error: 'realCount' may be used uninitialized in this function
> ...
> I simply added initialization for realCount variables to make the compiler happy.
> 
> [1] http://build.chromium.org/p/chromium.chromiumos/builders/ChromiumOS%20%28x86%29/builds/20955
> 
> BUG=349898
> TBR=sigbjornf@opera.com
> 
> Review URL: https://codereview.chromium.org/232243004

TBR=yurys@chromium.org

Review URL: https://codereview.chromium.org/259783002
-----------------------------------------------------------------

### bu...@chromium.org (2014-04-25)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=172583

------------------------------------------------------------------
r172583 | inferno@chromium.org | 2014-04-25T04:08:15.336489Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1916/LayoutTests/fast/dom/Range/deleteData-replaceData-count-overflow.html?r1=172583&r2=172582&pathrev=172583
   A http://src.chromium.org/viewvc/blink/branches/chromium/1916/LayoutTests/fast/dom/Range/deleteData-replaceData-count-overflow-expected.txt?r1=172583&r2=172582&pathrev=172583
   M http://src.chromium.org/viewvc/blink/branches/chromium/1916/Source/core/editing/FrameSelection.cpp?r1=172583&r2=172582&pathrev=172583
   M http://src.chromium.org/viewvc/blink/branches/chromium/1916/Source/core/dom/CharacterData.cpp?r1=172583&r2=172582&pathrev=172583

Merge 171165 "Add CharacterData.deleteData()/replaceData() overf..."

> Add CharacterData.deleteData()/replaceData() overflow handling.
> 
> If the offset and count exceed the underlying length, the spec tells us
> 
>   http://dom.spec.whatwg.org/#concept-cd-replace (step 3)
> 
> to use a count that is equal to length minus the offset. Perform that
> check in an overflow-sensitive manner.
> 
> (Change based on https://codereview.chromium.org/188693007/ )
> 
> R=
> BUG=349898
> 
> Review URL: https://codereview.chromium.org/229793004

TBR=sigbjornf@opera.com

Review URL: https://codereview.chromium.org/255803002
-----------------------------------------------------------------

### in...@chromium.org (2014-04-25)

Merge Requested for m34 patch 2.

### ti...@chromium.org (2014-04-28)

ping dxie@ - merge requested for M34 (in case patch 2 happens).

### dx...@chromium.org (2014-04-30)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-30)

inferno@ - please merge into M34 (branch 1847)

### in...@chromium.org (2014-04-30)

merged in r173028, 173029.

### bu...@chromium.org (2014-04-30)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=173028

------------------------------------------------------------------
r173028 | inferno@chromium.org | 2014-04-30T21:16:33.887009Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1847/Source/core/dom/CharacterData.cpp?r1=173028&r2=173027&pathrev=173028
   A http://src.chromium.org/viewvc/blink/branches/chromium/1847/LayoutTests/fast/dom/Range/deleteData-replaceData-count-overflow.html?r1=173028&r2=173027&pathrev=173028
   A http://src.chromium.org/viewvc/blink/branches/chromium/1847/LayoutTests/fast/dom/Range/deleteData-replaceData-count-overflow-expected.txt?r1=173028&r2=173027&pathrev=173028
   M http://src.chromium.org/viewvc/blink/branches/chromium/1847/Source/core/editing/FrameSelection.cpp?r1=173028&r2=173027&pathrev=173028

Merge 171165 "Add CharacterData.deleteData()/replaceData() overf..."

> Add CharacterData.deleteData()/replaceData() overflow handling.
> 
> If the offset and count exceed the underlying length, the spec tells us
> 
>   http://dom.spec.whatwg.org/#concept-cd-replace (step 3)
> 
> to use a count that is equal to length minus the offset. Perform that
> check in an overflow-sensitive manner.
> 
> (Change based on https://codereview.chromium.org/188693007/ )
> 
> R=
> BUG=349898
> 
> Review URL: https://codereview.chromium.org/229793004

TBR=sigbjornf@opera.com

Review URL: https://codereview.chromium.org/268523002
-----------------------------------------------------------------

### bu...@chromium.org (2014-04-30)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=173029

------------------------------------------------------------------
r173029 | inferno@chromium.org | 2014-04-30T21:17:10.046840Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1847/Source/core/dom/CharacterData.cpp?r1=173029&r2=173028&pathrev=173029

Merge 171240 "Fix compilation on Chromium OS after r171165"

> Fix compilation on Chromium OS after r171165
> 
> r171165 broke compilation on Chromium OS bot and we had to revert Blink roll.
> ...
> ../../../../../../../home/chrome-bot/chrome_root/src/third_party/WebKit/Source/core/dom/CharacterData.cpp:146:36:
> error: 'realCount' may be used uninitialized in this function
> ...
> I simply added initialization for realCount variables to make the compiler happy.
> 
> [1] http://build.chromium.org/p/chromium.chromiumos/builders/ChromiumOS%20%28x86%29/builds/20955
> 
> BUG=349898
> TBR=sigbjornf@opera.com
> 
> Review URL: https://codereview.chromium.org/232243004

TBR=yurys@chromium.org

Review URL: https://codereview.chromium.org/267573002
-----------------------------------------------------------------

### ti...@chromium.org (2014-05-01)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-05-13)

Congrats - $1500 for this one (the bump in amount was for the patch).

### cl...@chromium.org (2014-07-20)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-08-21)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-26)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!


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

This issue was migrated from crbug.com/chromium/349898?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079043)*

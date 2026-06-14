# Heap-use-after-free in v8::internal::GlobalHandles::Create

| Field | Value |
|-------|-------|
| **Issue ID** | [40079962](https://issues.chromium.org/issues/40079962) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2014-07-02 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testfile (crash.html) triggers a series of different crashes on the latest ASAN build of chrome (maybe a JIT issue?). The ogg file is required to trigger the event.

Multiple tabs make the test case more reliable and crashing it multiple times leads to different crash signature.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-280802  

Operating System: Linux 64-bit

**REPRODUCTION CASE**  

Attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: Different crashes as asan output in sym\*.txt

## Attachments

- [crash.html](attachments/crash.html) (text/html, 497 B)
- [sym3.txt](attachments/sym3.txt) (text/plain, 12.6 KB)
- [sym2.txt](attachments/sym2.txt) (text/plain, 9.9 KB)
- [sym.txt](attachments/sym.txt) (text/plain, 16.0 KB)
- [mov_bbb.ogg](attachments/mov_bbb.ogg) (application/octet-stream, 600.1 KB)

## Timeline

### cl...@chromium.org (2014-07-02)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5100809668788224

### cl...@chromium.org (2014-07-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-03)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5100809668788224

Uploader: felt@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x614000051f10
Crash State:
  - crash stack -
  v8::internal::GlobalHandles::Create
  void WebCore::DOMDataStore::setWrapper<WebCore::V8HTMLDocument, WebCore::HT
  - free stack -
  WebCore::GraphicsContext::~GraphicsContext
  WebCore::OpaqueRectTrackingContentLayerDelegate::paintContents
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=263040:263157

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95cK-Lns1L8RdSiiFRnEeqF9-tOyV8Reui2czthgOTqED6n5xwnlWAAUes1Y6JVQnYfhkDgEGd_lPD9YBFJEupw0iO24hT3BWlF0MX2-UmEG9XyakFw2PD_2IkY_Hgn8DHnNWuEulwBQm3fWE6PhcfwsHoTYZ1Va1cCoFCqWvPxCEz29N0



### in...@chromium.org (2014-07-03)

Any idea what caused this from the regression range ?

### ya...@chromium.org (2014-07-03)

Can reproduce with an x64 asan build.

### cl...@chromium.org (2014-07-05)

[Empty comment from Monorail migration]

### fe...@chromium.org (2014-07-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-06)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-07-11)

Bulk edit of medium severity issues impacting head to M-38.

### cl...@chromium.org (2014-07-11)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

dcarney@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### la...@google.com (2014-07-14)

[Empty comment from Monorail migration]

### dc...@chromium.org (2014-07-16)

[Empty comment from Monorail migration]

### dc...@chromium.org (2014-07-23)

on vacation - assigning to jochen

### jo...@chromium.org (2014-07-23)

uh uh uh, that looks like a pretty bad use after free. We add persistent values to some hash map instead of replacing the old ones with new ones.

bumping labels

fix is simple: https://codereview.chromium.org/412843003

### in...@chromium.org (2014-07-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-07-23)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=178780

------------------------------------------------------------------
r178780 | jochen@chromium.org | 2014-07-23T19:58:47.776625Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/core/v8/V8PersistentValueMap.h?r1=178780&r2=178779&pathrev=178780

When overwriting a persistent handle, actually overwrite it

BUG=390928
R=haraken@chromium.org

Review URL: https://codereview.chromium.org/412843003
-----------------------------------------------------------------

### in...@chromium.org (2014-07-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-07-23)

Is there a merge required here?

### cl...@chromium.org (2014-07-23)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### jo...@chromium.org (2014-07-24)

requesting merge so we don't miss M36-p1

### bu...@chromium.org (2014-07-24)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=178823

------------------------------------------------------------------
r178823 | jochen@chromium.org | 2014-07-24T08:07:31.891202Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/core/v8/SerializedScriptValue.cpp?r1=178823&r2=178822&pathrev=178823
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/core/v8/DOMWrapperMap.h?r1=178823&r2=178822&pathrev=178823

Replace further questionable HashMap::add usages in bindings

BUG=390928
R=dcarney@chromium.org

Review URL: https://codereview.chromium.org/411273002
-----------------------------------------------------------------

### am...@chromium.org (2014-07-28)

Which CLs are required here, r178780, r178823 or both?  If both, why do we have a second CL required the day after the first?

### ha...@chromium.org (2014-07-28)

I think r178780 is enough to fix the issue. r178823 is a just-in-case fix.


### jo...@chromium.org (2014-07-28)

No, we need both. DomWrapperMap had the same uaf

### jo...@chromium.org (2014-07-28)

The reason for the second cl is that I searched for other sites exposing the same bug

### [Deleted User] (2014-07-29)

Does this look good on canary?

### jo...@chromium.org (2014-07-29)

Very good.

### am...@chromium.org (2014-07-30)

merge approved for m37 branch 2062

### bu...@chromium.org (2014-07-30)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=179237

------------------------------------------------------------------
r179237 | jochen@chromium.org | 2014-07-30T15:28:35.330107Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2062/Source/bindings/v8/V8PersistentValueMap.h?r1=179237&r2=179236&pathrev=179237

Merge 178780 "When overwriting a persistent handle, actually ove..."

> When overwriting a persistent handle, actually overwrite it
> 
> BUG=390928
> R=haraken@chromium.org
> 
> Review URL: https://codereview.chromium.org/412843003

TBR=jochen@chromium.org

Review URL: https://codereview.chromium.org/426243003
-----------------------------------------------------------------

### bu...@chromium.org (2014-07-30)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=179238

------------------------------------------------------------------
r179238 | jochen@chromium.org | 2014-07-30T15:31:52.394738Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2062/Source/bindings/v8/DOMWrapperMap.h?r1=179238&r2=179237&pathrev=179238
   M http://src.chromium.org/viewvc/blink/branches/chromium/2062/Source/bindings/v8/SerializedScriptValue.cpp?r1=179238&r2=179237&pathrev=179238

Merge 178823 "Replace further questionable HashMap::add usages i..."

> Replace further questionable HashMap::add usages in bindings
> 
> BUG=390928
> R=dcarney@chromium.org
> 
> Review URL: https://codereview.chromium.org/411273002

TBR=jochen@chromium.org

Review URL: https://codereview.chromium.org/429233002
-----------------------------------------------------------------

### in...@chromium.org (2014-08-02)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-08-19)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-08-28)

Thanks for the report! This qualifies for a $4000 reward. We decided to add a bonus to this one because it helped us identify a pattern for similar bugs.

### ti...@chromium.org (2014-09-18)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-18)

[Empty comment from Monorail migration]

### ti...@google.com (2014-10-07)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2014-10-29)

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

This issue was migrated from crbug.com/chromium/390928?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079962)*

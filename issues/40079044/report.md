# ASSERTION FAILED: !object || (object->isListBox()), UNKNOWN in WebCore::HTMLSelectElement::listBoxDefaultEventHandler

| Field | Value |
|-------|-------|
| **Issue ID** | [40079044](https://issues.chromium.org/issues/40079044) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Reporter** | [Deleted User] |
| **Assignee** | tk...@chromium.org |
| **Created** | 2014-03-06 |
| **Bounty** | $1,500.00 |

## Description

**VULNERABILITY DETAILS**  

Select elements with a size property of more than one, or with the multiple property set are rendered as a RenderListBox by the rendering layer. HTMLSelectElement::listBoxDefaultEventHandler handles dispatched events for these objects.

When a mousedown event is fired on such an object, the object is focussed, and the process of re-rendering the object is started. When focussing the object, it is possible to return control to JavaScript via an event handler, and modify the size or multiple properties of the element to force it to be rendered as a different type.

HTMLSelectElement::listBoxDefaultEventHandler checks that the renderer was not removed, but it does not check that the object has the same renderer type as before. The renderer for the element is then passed to call to toRenderListBox, which triggers a bad cast.

A similar issue exists in HTMLSelectElement::platformHandleKeydownEvent, and affects all platforms except Windows, which has it's own version of the function which isn't vulnerable.

The patches should be trivial, so I've assigned it to myself to work on.

**VERSION**  

Confirmed on stable (33.0.1750.146) on Windows and Linux, also confirmed on a LKGR (35.0.1867.0) build on Linux.

**REPRODUCTION CASE**  

A minimised testcase is attached. With assertions enabled, it triggers an ASSERT\_WITH\_SECURITY\_IMPLICATION on the bad cast. Without, no crash can be observed.

## Attachments

- [renderer_bad_cast.html](attachments/renderer_bad_cast.html) (text/html, 583 B)

## Timeline

### cl...@chromium.org (2014-03-06)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=6048531966066688

### in...@chromium.org (2014-03-06)

[Empty comment from Monorail migration]

### [Deleted User] (2014-03-06)

https://codereview.chromium.org/188803002

### [Deleted User] (2014-03-06)

@Yuta,

You were the suggested owner for this, but I'm not sure it sent the mail. Are you happy to take this or should I find someone else?

### cl...@chromium.org (2014-03-06)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6048531966066688

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x00009f7537dd
Crash State:
  - crash stack -
  WebCore::HTMLSelectElement::listBoxDefaultEventHandler
  WebCore::HTMLSelectElement::defaultEventHandler
  WebCore::EventDispatcher::dispatchEventPostProcess
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=178763:178818

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95dOhJBcWOO9Wgg65use9-TaLcp_wjjirM_hNCAfcNyId27mi21_IcBgnBV2RUcB13YO2VI9MyJZPAgnbX9WQWaVfzwdhV3eETo_EhHiEWckOLltnSgSz1z52Uf7HPcGX3FpZ7qxK-VU_Xn8GPLmmgmykEXWg



### in...@chromium.org (2014-03-06)

Jon, i added tkent@ as reviewer for your patch. Please also include the crasher as a layout test. 

### cl...@chromium.org (2014-03-06)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-03-06)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-03-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-15)

jbutler@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### [Deleted User] (2014-03-16)

Sorry, I was on vacation for the last week.

Code review process is under way, I'm just making some required changes now.



### cl...@chromium.org (2014-03-30)

ClusterFuzz has detected this issue as fixed in range 254874:254895.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6048531966066688

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x00009f7537dd
Crash State:
  - crash stack -
  WebCore::HTMLSelectElement::listBoxDefaultEventHandler
  WebCore::HTMLSelectElement::defaultEventHandler
  WebCore::EventDispatcher::dispatchEventPostProcess
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=178763:178818
Fixed: https://cluster-fuzz.appspot.com/revisions?range=254874:254895

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95dOhJBcWOO9Wgg65use9-TaLcp_wjjirM_hNCAfcNyId27mi21_IcBgnBV2RUcB13YO2VI9MyJZPAgnbX9WQWaVfzwdhV3eETo_EhHiEWckOLltnSgSz1z52Uf7HPcGX3FpZ7qxK-VU_Xn8GPLmmgmykEXWg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-03-31)

[Empty comment from Monorail migration]

### ia...@chromium.org (2014-04-08)

jbutler: it looks like your CL never got committed - was this bug fixed by another CL or is clusterfuzz confused when it says this bug is fixed? (It doesn't look to me like that code has changed.)

If it hasn't actually been fixed by another CL you should try rebasing your patch and ticking the commit box again. The trybots can be flaky and sometimes it takes a few tries.

### in...@chromium.org (2014-04-09)

tkent@, can you please drive this to completion. Jbutler@ is an external contributor (ignore the @chromium account) and does know this part of the codebase. This bug has been open for a month and a half and we can't wait anymore on this high severity vulnerability. 

### tk...@chromium.org (2014-04-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-04-10)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=171216

------------------------------------------------------------------
r171216 | tkent@chromium.org | 2014-04-10T01:45:36.902156Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/platform/mac/fast/forms/select/select-change-type-on-keydown-focus.html?r1=171216&r2=171215&pathrev=171216
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/forms/select/select-change-type-on-mousedown-focus-expected.txt?r1=171216&r2=171215&pathrev=171216
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/platform/mac/fast/forms/select/select-change-type-on-keydown-focus-expected.txt?r1=171216&r2=171215&pathrev=171216
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/forms/select/select-change-type-on-mousedown-focus.html?r1=171216&r2=171215&pathrev=171216
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLSelectElement.cpp?r1=171216&r2=171215&pathrev=171216

Add renderer type checks to HTMLSelectElement event handlers.

focus() can change the renderer type.


This CL is based on a patch by jbutler@chromium.org. This CL fixed one bug in
the original CL, and added a test.
The test is only for OSX because other platforms don't use
HTMLSelectElement::platformHandleKeydownEvent.

BUG=349903
TEST=automated

Review URL: https://codereview.chromium.org/230143004
-----------------------------------------------------------------

### in...@chromium.org (2014-04-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-10)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-04-11)

ClusterFuzz has detected this issue as fixed in range 260908:260919.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6048531966066688

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x00009f7537dd
Crash State:
  - crash stack -
  WebCore::HTMLSelectElement::listBoxDefaultEventHandler
  WebCore::HTMLSelectElement::defaultEventHandler
  WebCore::EventDispatcher::dispatchEventPostProcess
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=178763:178818
Fixed: https://cluster-fuzz.appspot.com/revisions?range=260908:260919

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95dOhJBcWOO9Wgg65use9-TaLcp_wjjirM_hNCAfcNyId27mi21_IcBgnBV2RUcB13YO2VI9MyJZPAgnbX9WQWaVfzwdhV3eETo_EhHiEWckOLltnSgSz1z52Uf7HPcGX3FpZ7qxK-VU_Xn8GPLmmgmykEXWg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### tk...@chromium.org (2014-04-13)

[Empty comment from Monorail migration]

### dx...@chromium.org (2014-04-14)

Let's get this merged in M35 and then I will take it in M34.

### ka...@google.com (2014-04-15)

aproved for m35.

### bu...@chromium.org (2014-04-16)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=171726

------------------------------------------------------------------
r171726 | tkent@chromium.org | 2014-04-16T01:36:36.136419Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1916/LayoutTests/fast/forms/select/select-change-type-on-mousedown-focus.html?r1=171726&r2=171725&pathrev=171726
   M http://src.chromium.org/viewvc/blink/branches/chromium/1916/Source/core/html/HTMLSelectElement.cpp?r1=171726&r2=171725&pathrev=171726
   A http://src.chromium.org/viewvc/blink/branches/chromium/1916/LayoutTests/platform/mac/fast/forms/select/select-change-type-on-keydown-focus.html?r1=171726&r2=171725&pathrev=171726
   A http://src.chromium.org/viewvc/blink/branches/chromium/1916/LayoutTests/fast/forms/select/select-change-type-on-mousedown-focus-expected.txt?r1=171726&r2=171725&pathrev=171726
   A http://src.chromium.org/viewvc/blink/branches/chromium/1916/LayoutTests/platform/mac/fast/forms/select/select-change-type-on-keydown-focus-expected.txt?r1=171726&r2=171725&pathrev=171726

Merge 171216 "Add renderer type checks to HTMLSelectElement even..."

> Add renderer type checks to HTMLSelectElement event handlers.
> 
> focus() can change the renderer type.
> 
> 
> This CL is based on a patch by jbutler@chromium.org. This CL fixed one bug in
> the original CL, and added a test.
> The test is only for OSX because other platforms don't use
> HTMLSelectElement::platformHandleKeydownEvent.
> 
> BUG=349903
> TEST=automated
> 
> Review URL: https://codereview.chromium.org/230143004

TBR=tkent@chromium.org

Review URL: https://codereview.chromium.org/236133016
-----------------------------------------------------------------

### tk...@chromium.org (2014-04-16)

[Empty comment from Monorail migration]

### dx...@google.com (2014-04-16)

approved for m34.

### bu...@chromium.org (2014-04-17)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=171828

------------------------------------------------------------------
r171828 | tkent@chromium.org | 2014-04-17T02:33:00.906922Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1847/LayoutTests/platform/mac/fast/forms/select/select-change-type-on-keydown-focus.html?r1=171828&r2=171827&pathrev=171828
   A http://src.chromium.org/viewvc/blink/branches/chromium/1847/LayoutTests/fast/forms/select/select-change-type-on-mousedown-focus-expected.txt?r1=171828&r2=171827&pathrev=171828
   A http://src.chromium.org/viewvc/blink/branches/chromium/1847/LayoutTests/platform/mac/fast/forms/select/select-change-type-on-keydown-focus-expected.txt?r1=171828&r2=171827&pathrev=171828
   A http://src.chromium.org/viewvc/blink/branches/chromium/1847/LayoutTests/fast/forms/select/select-change-type-on-mousedown-focus.html?r1=171828&r2=171827&pathrev=171828
   M http://src.chromium.org/viewvc/blink/branches/chromium/1847/Source/core/html/HTMLSelectElement.cpp?r1=171828&r2=171827&pathrev=171828

Merge 171216 "Add renderer type checks to HTMLSelectElement even..."

> Add renderer type checks to HTMLSelectElement event handlers.
> 
> focus() can change the renderer type.
> 
> 
> This CL is based on a patch by jbutler@chromium.org. This CL fixed one bug in
> the original CL, and added a test.
> The test is only for OSX because other platforms don't use
> HTMLSelectElement::platformHandleKeydownEvent.
> 
> BUG=349903
> TEST=automated
> 
> Review URL: https://codereview.chromium.org/230143004

TBR=tkent@chromium.org

Review URL: https://codereview.chromium.org/240163004
-----------------------------------------------------------------

### ti...@chromium.org (2014-04-22)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-26)

Congrats - $1500 for this one.

### cl...@chromium.org (2014-07-20)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-08-21)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-26)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### la...@google.com (2015-01-09)

Migrate from Cr-Blink-Rendering to Cr-Blink-Layout

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

This issue was migrated from crbug.com/chromium/349903?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079044)*

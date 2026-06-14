# Heap-use-after-free in WebCore::Node::containsIncludingHostElements

| Field | Value |
|-------|-------|
| **Issue ID** | [40078067](https://issues.chromium.org/issues/40078067) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | jo...@gmail.com |
| **Assignee** | ad...@chromium.org |
| **Created** | 2013-09-07 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

References to a template's content are not freed when the template is destroyed. Interacting with the template's document fragment (such as appending a child) causes a crash on the latest available asan prebuild.

Currently crashes on a read, but I suspect I can change that given a little time... I wanted to get this posted though as the trigger is very simple and I wanted to get in before the masses :)

**VERSION**  

Chrome Version: 29.0.1547.57  

Operating System: Debian Wheezy

**REPRODUCTION CASE**  

A minimized testcase is attached. For ease of reproduction, enable the use of window.gc() in the JS flags. A full symbolized ASAN output is also attached.

## Attachments

- [asan_sym.txt](attachments/asan_sym.txt) (text/plain; charset=us-ascii, 10.9 KB)
- [repro.html](attachments/repro.html) (text/html; charset=us-ascii, 249 B)

## Timeline

### jo...@gmail.com (2013-09-07)

Ok, I've had a shot at doing some analysis of the issue, here is what I have:

When retrieving the content of an HTML template element (HTMLTemplateElement::content), a new document fragment object is created through a call to TemplateContentDocumentFragment::create. This call passes a pointer to the current template object, which is used to initialize the m_host property of the TemplateContentDocumentFragment class being constructed. This pointer is a raw Element* (TemplateContentDocumentFragment.h:52), and is not managed by one of the usual smart pointer classes.

This pointer is not invalidated when the template element is freed, and is left "dangling", pointing at the freed memory that used to contain the template element. Subsequent accesses to this pointer after garbage collection trigger a use-after-free condition.

My thoughts on exploitation are that it would depend on the size of the HTMLTemplateElement in memory, and my ability to fill the freed memory with something useful (thanks to PartitionAlloc, this may no longer be trivial). I remain hopeful, but need to setup an environment for debugging first to confirm what is possible.

### in...@chromium.org (2013-09-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-07)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=4902838647914496

### cl...@chromium.org (2013-09-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4902838647914496

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60f00001d554
Crash State:
  - crash stack -
  WebCore::Node::containsIncludingHostElements
  WebCore::checkAcceptChild
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=175112:175121

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96zzKk4DpSI2gPEEqMNV2LWQpMgzdIR32A0hOsRfXD2HAZxeIWFD00z_AbGCsd0EQRA0Xf-7ztZAbhhyWpuWRRC3f9Lhn0EwuTWuf6whC2p6IDQoQOwj8PrVs9t6v7bNM_DpvJ1uvf0GRHHOx64JRmCAO0lXw



### in...@chromium.org (2013-09-08)

Looks like regression from http://src.chromium.org/viewvc/blink?view=rev&revision=138730

### in...@chromium.org (2013-09-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-09)

ClusterFuzz has detected this issue as fixed in range 221902:221913.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4902838647914496

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60f00001d554
Crash State:
  - crash stack -
  WebCore::Node::containsIncludingHostElements
  WebCore::checkAcceptChild
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=175112:175121
Fixed: https://cluster-fuzz.appspot.com/revisions?range=221902:221913

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96zzKk4DpSI2gPEEqMNV2LWQpMgzdIR32A0hOsRfXD2HAZxeIWFD00z_AbGCsd0EQRA0Xf-7ztZAbhhyWpuWRRC3f9Lhn0EwuTWuf6whC2p6IDQoQOwj8PrVs9t6v7bNM_DpvJ1uvf0GRHHOx64JRmCAO0lXw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### ad...@chromium.org (2013-09-10)

The code is pretty clearly busted, working on a (very straightforward) fix now.

### ad...@chromium.org (2013-09-10)

Fix up for review at https://codereview.chromium.org/23708025

### cl...@chromium.org (2013-09-10)

[Comment Deleted]

### cl...@chromium.org (2013-09-10)

[Comment Deleted]

### bu...@chromium.org (2013-09-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157543

------------------------------------------------------------------------
r157543 | adamk@chromium.org | 2013-09-10T20:36:03.518281Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLTemplateElement/content-outlives-template-crash-expected.txt?r1=157543&r2=157542&pathrev=157543
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLTemplateElement.h?r1=157543&r2=157542&pathrev=157543
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLTemplateElement/content-outlives-template-crash.html?r1=157543&r2=157542&pathrev=157543
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/TemplateContentDocumentFragment.h?r1=157543&r2=157542&pathrev=157543
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLTemplateElement.cpp?r1=157543&r2=157542&pathrev=157543

Clear TemplateContentDocumentFragment::m_host when HTMLTemplateElement is destroyed

Note that the included test only crashes reliably in an asan build.

R=inferno@chromium.org
BUG=286975

Review URL: https://chromiumcodereview.appspot.com/23708025
------------------------------------------------------------------------

### in...@chromium.org (2013-09-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-12)

Please merge your change to the m30 branch (1599) by early next week [using drover]. We have m30 beta coming next week and we want all the security changes in by that time. 

### bu...@chromium.org (2013-09-16)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157861

------------------------------------------------------------------------
r157861 | karen@chromium.org | 2013-09-16T22:48:28.460339Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/html/HTMLTemplateElement.cpp?r1=157861&r2=157860&pathrev=157861
   A http://src.chromium.org/viewvc/blink/branches/chromium/1599/LayoutTests/fast/dom/HTMLTemplateElement/content-outlives-template-crash-expected.txt?r1=157861&r2=157860&pathrev=157861
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/html/HTMLTemplateElement.h?r1=157861&r2=157860&pathrev=157861
   A http://src.chromium.org/viewvc/blink/branches/chromium/1599/LayoutTests/fast/dom/HTMLTemplateElement/content-outlives-template-crash.html?r1=157861&r2=157860&pathrev=157861
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/dom/TemplateContentDocumentFragment.h?r1=157861&r2=157860&pathrev=157861

Merge 157543 "Clear TemplateContentDocumentFragment::m_host when..."

> Clear TemplateContentDocumentFragment::m_host when HTMLTemplateElement is destroyed
> 
> Note that the included test only crashes reliably in an asan build.
> 
> R=inferno@chromium.org
> BUG=286975
> 
> Review URL: https://chromiumcodereview.appspot.com/23708025

TBR=adamk@chromium.org

Review URL: https://codereview.chromium.org/24023006
------------------------------------------------------------------------

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-18)

ClusterFuzz thinks that this bug might be eligible for a reward! Forwarding to reward panel for consideration.

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### aa...@google.com (2013-09-27)

[Empty comment from Monorail migration]

### aa...@google.com (2013-09-27)

jonbutler88@, what name would you like us to use when we give you credit for this bug in the release notes on the Chrome blog?

### jo...@gmail.com (2013-09-27)

Hi,

Please credit the bug to "Jon Butler".

Thanks,
Jon

### sc...@gmail.com (2013-09-27)

*** Correcting CVE ***
It now matches the release notes.
CVE errors are a real pain to correct once we've published our release notes, so let's be careful :)

### mb...@chromium.org (2013-09-27)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-28)

This goes off inside the Node partition, but looks like JS control between the free and the use.
$2000 !

### pa...@chromium.org (2013-10-18)

Thanks Jon! I just kicked off payment for this, so you should see it in a few weeks.

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/286975?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078067)*

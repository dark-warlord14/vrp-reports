# Heap-use-after-free in blink::Document::didRemoveAllPendingStylesheet

| Field | Value |
|-------|-------|
| **Issue ID** | [40080209](https://issues.chromium.org/issues/40080209) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ta...@google.com |
| **Created** | 2014-08-13 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Testcase attached in crash.zip as it requires multiple files. Crashes the latest ASAN build. Pretty reliable for me, however might need a few reloads.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-289059  

Operating System: Linux

**REPRODUCTION CASE**  

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: ASAN output in debug.txt

## Attachments

- [debug.txt](attachments/debug.txt) (text/plain, 15.2 KB)
- [crash.zip](attachments/crash.zip) (application/zip, 12.8 KB)

## Timeline

### cl...@chromium.org (2014-08-13)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=4998298608861184

### cl...@chromium.org (2014-08-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-14)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4998298608861184

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x61e00003b614
Crash State:
  - crash stack -
  blink::Document::didRemoveAllPendingStylesheet
  blink::StyleEngine::removePendingSheet
  - free stack -
  blink::Document::~Document
  blink::XMLDocument::~XMLDocument
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=274265:274467

Minimized Testcase (10.63 Kb): https://cluster-fuzz.appspot.com/download/AMIfv9425Y_GAjiTO6NwvFlUuwsCL3g2l6Zvyw7yIU1UfPH9gX5H4JsZMnVEbwJORdPr5Nn7aVPTNlMVj9gLTsT3uxui8m6wFKCJO_g7t37dA8EpaT5KevNkvBhTJ6aCJm5ge6y-gugzPBYgQLVcwuw8_hsaVHOtvw



### js...@chromium.org (2014-08-14)

Ends up inside a stale document, so I'm going to assume that's high-severity.

japhet@ - I'm assigning to you since it looks loadery and I'm hoping you can help find the right owner (or take ownership), since the regression range is so large. Feel free to punt it back if you disagree or can't help.

### cl...@chromium.org (2014-08-14)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-14)

i think yet another regression from http://src.chromium.org/viewvc/blink?view=rev&revision=175255

### cl...@chromium.org (2014-08-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-18)

[Empty comment from Monorail migration]

### ta...@chromium.org (2014-08-18)

Looking.


### ta...@google.com (2014-08-18)

I think, this is not related to http://src.chromium.org/viewvc/blink?view=rev&revision=175255.

Looking at debug.txt (I would like to see debug build's stack trace), free and read (heap-use-after-free) has the same stacktrace.
I'm not sure why document is destroyed in XSLTProcessor::createDocumentFromSource,but probably we need to check whether a given document is valid or not, or to guard a given document.

I'm now trying to reproduce this crash.



### cl...@chromium.org (2014-08-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4998298608861184

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x61e00003b614
Crash State:
  blink::Document::didRemoveAllPendingStylesheet
  blink::StyleEngine::removePendingSheet
  - free stack -
  blink::Document::~Document
  blink::XMLDocument::~XMLDocument
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=274265:274467

Minimized Testcase (10.63 Kb): https://cluster-fuzz.appspot.com/download/AMIfv9425Y_GAjiTO6NwvFlUuwsCL3g2l6Zvyw7yIU1UfPH9gX5H4JsZMnVEbwJORdPr5Nn7aVPTNlMVj9gLTsT3uxui8m6wFKCJO_g7t37dA8EpaT5KevNkvBhTJ6aCJm5ge6y-gugzPBYgQLVcwuw8_hsaVHOtvw



### bu...@chromium.org (2014-08-19)

[Comment Deleted]

### bu...@chromium.org (2014-08-19)

[Comment Deleted]

### ta...@google.com (2014-08-19)

I'm still investigating this issue.

I think, result->setContent(documentSource) in XSLTProcessor::createDocumentFromSource probably causes this issue.
In the setContent, Frame::setDOMWindow is invoked and a LocalDOMWindow, which owns a newly created document and a source document, is detached.

I will see setContent and documentSource.



### bu...@chromium.org (2014-08-20)

[Comment Deleted]

### bu...@chromium.org (2014-08-20)

[Comment Deleted]

### ta...@google.com (2014-08-20)

I'm wrong. Now I'm thinking of the following:

(1) XSLStyleSheetResource::checkNotify invokes ProcessingInstruction::setXSLStyleSheet,
(2) setXSLStyleSheet causes XSLTransfrom (invokes Document::applyXSLTransform),
(3) applyXSLTransform might destroy document, processing instruction, XSLImports and so on,

So XSLStyleSheetResourceClient is not available. Crashes.

I think, probably we need to defer applying XSLTransform (until XSLStyleSheet::checkNotify is finished).


### cl...@chromium.org (2014-08-21)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4998298608861184

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x61e000001a14
Crash State:
  blink::Document::didRemoveAllPendingStylesheet
  blink::StyleEngine::removePendingSheet
  blink::ProcessingInstruction::sheetLoaded
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=274265:274467

Minimized Testcase (10.63 Kb): https://cluster-fuzz.appspot.com/download/AMIfv9425Y_GAjiTO6NwvFlUuwsCL3g2l6Zvyw7yIU1UfPH9gX5H4JsZMnVEbwJORdPr5Nn7aVPTNlMVj9gLTsT3uxui8m6wFKCJO_g7t37dA8EpaT5KevNkvBhTJ6aCJm5ge6y-gugzPBYgQLVcwuw8_hsaVHOtvw



### ta...@google.com (2014-08-25)

I think, this is not a regression. The old webkit/blink always applies XSL transform when checkNotify is invoked.


### am...@chromium.org (2014-08-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4998298608861184

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x61e000001a14
Crash State:
  blink::Document::didRemoveAllPendingStylesheet
  blink::StyleEngine::removePendingSheet
  blink::ProcessingInstruction::sheetLoaded
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=274265:274467

Minimized Testcase (10.63 Kb): https://cluster-fuzz.appspot.com/download/AMIfv9425Y_GAjiTO6NwvFlUuwsCL3g2l6Zvyw7yIU1UfPH9gX5H4JsZMnVEbwJORdPr5Nn7aVPTNlMVj9gLTsT3uxui8m6wFKCJO_g7t37dA8EpaT5KevNkvBhTJ6aCJm5ge6y-gugzPBYgQLVcwuw8_hsaVHOtvw



### cl...@chromium.org (2014-09-01)

tasak@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-09-08)

tasak@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-09-16)

tasak@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-09-16)

Tasak@, are you looking into this ? If not, can you please help with an owner.

### ta...@google.com (2014-09-17)

I have already found what causes this issue.

We should not apply XLSTTransform while XSLStyleSheetResource->notify().
I think, this is an old bug.

So we need to defer applyXSLTransform... (1) adding transform available bit to document? or (2) adding timer to document.

I have already found XSLT in PrivateScript could solve this issue. However, because of PrivateScript policy discussion, I cannot land the patch.


### in...@chromium.org (2014-09-17)

What is "PrivateScript policy discussion". Do you have a CL already. This is a high severity vulnerability that should be fixed asap, has already been open for more than a month.

### ta...@google.com (2014-09-18)

The CL is https://codereview.chromium.org/365873002/.

I have already closed the CL because I couldn't get lgtm.
The policy means, how to add OnlyExposedToPrivateScript method to IDL files.

I will try to add XSLTForbiddenScope.



### ta...@google.com (2014-09-18)

I found better approach. We should protect document in ProcessingInstruction::setXSLStyleSheet.

http://codereview.chromium.org/579133004

### bu...@chromium.org (2014-09-19)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=182309

------------------------------------------------------------------
r182309 | tasak@google.com | 2014-09-19T09:08:07.500048Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ProcessingInstruction.cpp?r1=182309&r2=182308&pathrev=182309

Should protect document in ProcessingInstruction::setXSLStyleSheet.

BUG=403276

Review URL: https://codereview.chromium.org/579133004
-----------------------------------------------------------------

### in...@chromium.org (2014-09-19)

[Empty comment from Monorail migration]

### am...@google.com (2014-09-19)

Is there a merge required here?

### cl...@chromium.org (2014-09-19)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-09-23)

Matthew - Merge Requested for M38 (Branch 2125)

### [Deleted User] (2014-09-24)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-24)

tasak@ - please merge to M38 / branch 2125

### ta...@google.com (2014-09-25)

Sure.

I have just commited -- Committed revision 182660.



### bu...@chromium.org (2014-09-25)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=182660

------------------------------------------------------------------
r182660 | tasak@google.com | 2014-09-25T09:25:52.658566Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2125/Source/core/dom/ProcessingInstruction.cpp?r1=182660&r2=182659&pathrev=182660

Merge 182309 "Should protect document in ProcessingInstruction::..."

> Should protect document in ProcessingInstruction::setXSLStyleSheet.
> 
> BUG=403276
> 
> Review URL: https://codereview.chromium.org/579133004

TBR=tasak@google.com

Review URL: https://codereview.chromium.org/598363002
-----------------------------------------------------------------

### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-07)

Congratulations - $2000 for this under our new reward structure. Notes from the panel: "bug in partition alloc and does not appear to have control between use and free"

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-22)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2014-12-26)

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

This issue was migrated from crbug.com/chromium/403276?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080209)*

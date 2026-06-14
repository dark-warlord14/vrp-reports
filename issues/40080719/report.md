# ASSERTION FAILED: m_pendingStylesheets > 0, Heap-use-after-free in blink::StyleEngine::clearResolver

| Field | Value |
|-------|-------|
| **Issue ID** | [40080719](https://issues.chromium.org/issues/40080719) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ta...@google.com |
| **Created** | 2014-10-26 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest asan build of chrome.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-301067  

Operating System: Linux 64bit

**REPRODUCTION CASE**  

The testcase consists of three files which should be loaded from a webserver. The file are also attached in crash.zip.

crash.html:

<script>
function start() {
o0=document.createElement('iframe');
o0.src='iframe.xml';
document.getElementById('store\_div').appendChild(o0);
window.setTimeout('startrly()', 100);
}
function startrly() {
o6=document.body;
o17=document.createElement('frame');
o19=document.createElement('marquee');
window.o6.appendChild(o19);
o6.scrollIntoView(false);
o69=document.createElementNS('http://www.w3.org/1999/xhtml','iframe');
o69.src='iframe2.html';
window.o6.appendChild(o69);
o114=document.createElement('input');
o17.appendChild(o114);
document.documentElement.appendChild(o0.contentDocument.firstChild);
window.o114.appendChild(o19);
window.setTimeout('location.reload();',20);
}
</script>
<body onload="start()">
<div id="store\_div"></div>
</script>

iframe.xml:

<?xml-stylesheet type="text/xsl" href="mathml.xsl"?>

iframe2.html:

<script>
function start(){
document.body.appendChild(window.top.o17);
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: asan output attached in debug.txt

## Attachments

- [crash.zip](attachments/crash.zip) (application/zip, 968 B)
- [debug.txt](attachments/debug.txt) (text/plain, 18.3 KB)

## Timeline

### in...@chromium.org (2014-10-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-26)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5003813416075264

### cl...@chromium.org (2014-10-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-10-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5003813416075264

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60b00034d450
Crash State:
  blink::StyleEngine::clearResolver
  blink::Document::detach
  blink::Document::prepareForDestruction
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=298200:298214

Minimized Testcase (0.79 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96pFXNC5x2mF6DZpfNUKtTcDhAfNn0DcnUycwwwXvDrNnUz9mmz8sE4pFC6lLgqC3q3x9FqJtO_zhBS3stbWF-fWDMGJsky8LRiKPLQZe6mTqp1hCXdIxXDBaN9CyX2U5oX2pqTPU0WcOJ5Q6XGuCdIBGU_Bw

Additional requirements: Requires HTTP



### cl...@chromium.org (2014-10-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-27)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-10-27)

looks like regression from https://chromium.googlesource.com/chromium/blink.git/+/9fcedc6f2493fd2e06fee81a6a869ff362eaf83a based on regression range.

### dc...@chromium.org (2014-10-27)

I don't think it's a regression from that particular patch, since it literally just shuffles some member functions around. There are a number of other patches that might be responsible though (though it looks like CF's regression range might be a bit off):

https://codereview.chromium.org/655063003
https://codereview.chromium.org/678673002
https://codereview.chromium.org/657263002


### dc...@chromium.org (2014-10-27)

Actually, looking more closely, this is almost certainly the marquee change (https://chromium.googlesource.com/chromium/blink/+/721800d78fc536c60ef7329c56b4440e69a63e3f).

haraken@, is it possible that migrating the marquee impl to JS exposed a bug here?

### cl...@chromium.org (2014-11-04)

haraken@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-08)

[Empty comment from Monorail migration]

### ha...@chromium.org (2014-11-10)

I don't think this is related to marquee-in-JS.

As far as I see the crash report, the issue is that StyleEngine::m_scopedStyleResolvers can hold stale raw pointers to ScopedStyleResolvers.

kochi-san: Would you mind taking a look at this?


### ko...@chromium.org (2014-11-10)

looking.

### ko...@chromium.org (2014-11-10)

Ccing hayato

### ko...@chromium.org (2014-11-10)

(removing dcheng, sigbjornf as they are unlikely involved in this case)

Looks like there are 2 paths for this to crash.

One looks like a error handling path when XSL failed to load.
The backtrace looks as follows:

blink::StyleEngine::removePendingSheet
blink::ProcessingInstruction::sheetLoaded
blink::XSLStyleSheet::checkLoaded
blink::ProcessingInstruction::parseStyleSheet
blink::ProcessingInstruction::setXSLStyleSheet
blink::XSLStyleSheetResource::checkNotify
blink::Resource::error
blink::ResourceLoader::didReceiveResponse

Here it gets erorr at Resource::error but after that it proceeds
to parseStyleSheet, and eventually results in SEGV.
Takashi, could you check this path is expected?

The other case is a double-free in blink::StyleEngine::clearResolver(),
which tries to free already-freed SocpedStyleResolver.
I'm investigating the case.

### ta...@chromium.org (2014-11-10)

As far as I investigated, we need to unregister ScopedStyleResolver with StyleEngine before destroying TreeScope.
I guess, TreeScope's dispose might be the best place to unregister?



### ko...@chromium.org (2014-11-12)

I think now I understand the problem.

When a node is moved from one document to another, some states are not migrated
properly.

- a set of ScopedStyleResolvers in StyleEngine
  => caused double-free.
- pendingStyleSheets in StyleEngine
  => caused assertion check in StyleEngine::removePendingSheet

I'm working on a fix, but it's tough to write a reproducing layout test.



### ko...@chromium.org (2014-11-13)

Tentative fix:
https://codereview.chromium.org/718293002/

This seems to fix the crash for both Release/Debug builds.

### [Deleted User] (2014-11-14)

[Empty comment from Monorail migration]

### ko...@chromium.org (2014-11-14)

No, this is not OS specific.
This happens in OS-neutral code.

### ko...@chromium.org (2014-11-14)

Adding haraken back to cc...

With the debug print:
https://codereview.chromium.org/722233005

The marquee element in the minimized testcase seems inserted into <input>
and <body>.  Expectation is that once inserted into <body>, then removed
and added again into iframe.contentDocument.

=====================
HTMLMarqueeElement::insertedInto this:0x60b000011c30 insertedto:0x60b000013b20 (BODY)
HTMLMarqueeElement::removedFrom this:0x60b000011c30 from:0x60b000013b20 (BODY) 
HTMLMarqueeElement::insertedInto this:0x60b000011c30 insertedto:0x61100011f340 (INPUT)
reload
HTMLMarqueeElement::insertedInto this:0x60b000011c30 insertedto:0x60b0000203e0 (BODY)
=====================

The last one looks racy with location.reload().

Sometimes it happens before reload.

=====================
HTMLMarqueeElement::insertedInto this:0x60b000039f00 insertedto:0x60b000022f30 (BODY)
HTMLMarqueeElement::removedFrom this:0x60b000039f00 from:0x60b000022f30 (BODY) 
HTMLMarqueeElement::insertedInto this:0x60b000039f00 insertedto:0x61100011f980 (INPUT)
reload
HTMLMarqueeElement::insertedInto this:0x60b000048ef0 insertedto:0x60b00002d7a0 (BODY)
HTMLMarqueeElement::removedFrom this:0x60b000048ef0 from:0x60b00002d7a0 (BODY) 
HTMLMarqueeElement::insertedInto this:0x60b000048ef0 insertedto:0x61100017aec0 (INPUT)
HTMLMarqueeElement::insertedInto this:0x60b000048ef0 insertedto:0x60b000046030 (BODY)
reload
=====================


### ko...@chromium.org (2014-11-14)

Changing owner to tasak

### bu...@chromium.org (2014-11-18)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=185504

------------------------------------------------------------------
r185504 | kochi@chromium.org | 2014-11-18T07:33:40.271026Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/StyleSheet/detached-style-pi-2.xhtml?r1=185504&r2=185503&pathrev=185504
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ProcessingInstruction.cpp?r1=185504&r2=185503&pathrev=185504

Handle case when XSL stylesheet node is removed during load

When a XSL stylesheet node is removed from document while its content
is being loaded, the current code doesn't handle the case to clear the resource,
while when the node is added again the new resource is created again.

This causes reference count (StyleEngine::m_pendingStyleSheets) leakage.

BUG=427249
TEST=minimized clusterfuzz test

Review URL: https://codereview.chromium.org/722093002
-----------------------------------------------------------------

### in...@chromium.org (2014-11-18)

[Empty comment from Monorail migration]

### am...@google.com (2014-11-18)

Is there a merge required here?

### ko...@chromium.org (2014-11-18)

No, not fixed yet - another fix
https://codereview.chromium.org/721103002/
has to land.

### ko...@chromium.org (2014-11-19)

re c#24, Takashi explained to me that it may happen when an element which has
orphaned (not-in-document) parent nodes is inserted to a node altogether,
insertedInto() can be called more than once for an element, but only one of
these calls is with inDocument = true (otherwise false).

But then how 'reload' and 'insertedInto' race can happen?

### bu...@chromium.org (2014-11-19)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=185598

------------------------------------------------------------------
r185598 | kochi@chromium.org | 2014-11-19T14:47:23.377221Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/StyleSheet/stylesheet-move-between-documents-crash.html?r1=185598&r2=185597&pathrev=185598
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/StyleSheet/resources/stylesheet-move-iframe1.xml?r1=185598&r2=185597&pathrev=185598
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/StyleSheet/resources/stylesheet-move-iframe2.html?r1=185598&r2=185597&pathrev=185598
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/StyleSheet/stylesheet-move-between-documents-crash-expected.txt?r1=185598&r2=185597&pathrev=185598
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/css/resolver/StyleResolver.cpp?r1=185598&r2=185597&pathrev=185598
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/shadow/ShadowRoot.cpp?r1=185598&r2=185597&pathrev=185598

Fix lifespan of ScopedStyleResolver

When a Shadow Tree is moved between different documents
(e.g. document <-> iframe), ScopedStyleResolver can remain
registered from its original document, which can result in
duplicate registration and possibly cause double-free etc.

This CL fixes it by clearing a shadow tree's
ScopedStyleResolver when the ShadowRoot is removed.

BUG=427249
TEST=pass the new layout test

Review URL: https://codereview.chromium.org/721103002
-----------------------------------------------------------------

### ko...@chromium.org (2014-11-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-19)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ko...@chromium.org (2014-11-20)

Let's wait for https://crbug.com/chromium/434970 to settle before merging.

### ko...@chromium.org (2014-11-20)

r185598 was reverted as r185673 just in case the fix for https://crbug.com/chromium/434970 can't make in a day or two.
https://codereview.chromium.org/745613003

### ko...@chromium.org (2014-11-20)

Reopening

### bu...@chromium.org (2014-11-20)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=185673

------------------------------------------------------------------
r185673 | kochi@chromium.org | 2014-11-20T15:50:08.708030Z

Changed paths:
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/StyleSheet/stylesheet-move-between-documents-crash.html?r1=185673&r2=185672&pathrev=185673
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/StyleSheet/resources/stylesheet-move-iframe1.xml?r1=185673&r2=185672&pathrev=185673
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/StyleSheet/resources/stylesheet-move-iframe2.html?r1=185673&r2=185672&pathrev=185673
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/StyleSheet/stylesheet-move-between-documents-crash-expected.txt?r1=185673&r2=185672&pathrev=185673
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/css/resolver/StyleResolver.cpp?r1=185673&r2=185672&pathrev=185673
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/shadow/ShadowRoot.cpp?r1=185673&r2=185672&pathrev=185673

Revert 185598 "Fix lifespan of ScopedStyleResolver"

Reason: regressed on trunk, which is filed as crbug.com/434970.
This needs rework and shall be committed with this layout test
and more appropriate fix.

> Fix lifespan of ScopedStyleResolver
> 
> When a Shadow Tree is moved between different documents
> (e.g. document <-> iframe), ScopedStyleResolver can remain
> registered from its original document, which can result in
> duplicate registration and possibly cause double-free etc.
> 
> This CL fixes it by clearing a shadow tree's
> ScopedStyleResolver when the ShadowRoot is removed.
> 
> BUG=427249
> TEST=pass the new layout test
> 
> Review URL: https://codereview.chromium.org/721103002

TBR=kochi@chromium.org

Review URL: https://codereview.chromium.org/745613003
-----------------------------------------------------------------

### ta...@google.com (2014-11-21)

I think, I found how to fix this issue.
I'm now trying to create a patch for this.


### ko...@chromium.org (2014-11-21)

Thanks Takashi!

### ta...@google.com (2014-11-21)

I've just uploaded a patch for this:
https://codereview.chromium.org/751593002/


### bu...@chromium.org (2014-11-26)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=186026

------------------------------------------------------------------
r186026 | tasak@google.com | 2014-11-26T10:37:16.764055Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/StyleSheet/resources/stylesheet-move-iframe1.xml?r1=186026&r2=186025&pathrev=186026
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/StyleEngine.cpp?r1=186026&r2=186025&pathrev=186026
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/shadow/make-marquee-bold-by-exec-command-crash-expected.html?r1=186026&r2=186025&pathrev=186026
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/shadow/make-marquee-bold-by-exec-command-crash.html?r1=186026&r2=186025&pathrev=186026
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/StyleSheet/resources/stylesheet-move-iframe2.html?r1=186026&r2=186025&pathrev=186026
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/StyleSheet/stylesheet-move-between-documents-crash-expected.txt?r1=186026&r2=186025&pathrev=186026
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/StyleEngine.h?r1=186026&r2=186025&pathrev=186026
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/css/resolver/StyleResolver.cpp?r1=186026&r2=186025&pathrev=186026
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ProcessingInstruction.cpp?r1=186026&r2=186025&pathrev=186026
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/StyleSheet/stylesheet-move-between-documents-crash.html?r1=186026&r2=186025&pathrev=186026
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/animation/css/CSSAnimations.cpp?r1=186026&r2=186025&pathrev=186026

Removed add/removeScopedStyleResolver from StyleEngine

Since ScopedStyleResolvers are owned by TreeScopes (i.e. replacing ScopedStyleTree with TreeScope tree), StyleEngine should know only about TreeScopes which have stylesheets.

BUG=427249
TEST=fast/dom/StyleSheet/stylesheet-move-between-documents-crash.html,fast/dom/shadow/make-marquee-bold-by-exec-command-crash.html

Review URL: https://codereview.chromium.org/751593002
-----------------------------------------------------------------

### ko...@chromium.org (2014-11-28)

[Empty comment from Monorail migration]

### [Deleted User] (2014-12-03)

[Empty comment from Monorail migration]

### ta...@google.com (2014-12-03)

We also need to merge https://code.google.com/p/chromium/issues/detail?id=437174, because the patch fixed 
the bug of http://src.chromium.org/viewvc/blink?view=rev&rev=186026.


### ta...@google.com (2014-12-03)

tasak@ and kochi@ discussed whether we need to merge the patches.

Our conclusion is "we don't need", because this issue is use-after-free, but actually double-free.
The issue doesn't leak confidential information. The issue also depends on XSLT, which is rarely used.
So the impact is very low for the complexity of this fix.

We would like to remove ReleaseBlock-Stable.


### in...@chromium.org (2014-12-10)

Security team will do a triage again later. UAF can definitely be exploitable and from an attacker perspective, rarely used feature is not a blocker. in fact, attacker prefer to find bugs in rarely used feature and fuzz them.

### in...@chromium.org (2014-12-15)

We can't punt this, needs to be merged to M40 since this is high severity.

### ma...@google.com (2014-12-15)

[Automated comment] Reverts referenced in bugdroid comments, needs manual review.

### [Deleted User] (2014-12-15)

I think what @tasak was trying to say is that this is actually a a double-free issue and not a UAF (feel free to correct me if I am wrong).

@inferno, does that change the severity?

### [Deleted User] (2014-12-15)

Accidentally changed the label, reverting back....

### in...@chromium.org (2014-12-16)

That does not change severity, unless we can surely say there is no control like JS between the two free points. We should err on side of caution and uptake this since M40 is already far away.

### in...@chromium.org (2014-12-16)

[Empty comment from Monorail migration]

### ma...@google.com (2014-12-16)

[Automated comment] Reverts referenced in bugdroid comments, needs manual review.

### [Deleted User] (2014-12-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-12-17)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=187348

------------------------------------------------------------------
r187348 | kochi@chromium.org | 2014-12-17T07:24:46.226695Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/dom/shadow/move-marquee-crossing-treescope-crash.html?r1=187348&r2=187347&pathrev=187348
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/dom/shadow/marquee-and-link-element-crash-expected.html?r1=187348&r2=187347&pathrev=187348
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/dom/shadow/marquee-and-link-element-crash.html?r1=187348&r2=187347&pathrev=187348
   M http://src.chromium.org/viewvc/blink/branches/chromium/2214/Source/core/dom/StyleEngine.h?r1=187348&r2=187347&pathrev=187348
   M http://src.chromium.org/viewvc/blink/branches/chromium/2214/Source/core/css/resolver/StyleResolver.cpp?r1=187348&r2=187347&pathrev=187348
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/dom/StyleSheet/stylesheet-move-between-documents-crash.html?r1=187348&r2=187347&pathrev=187348
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/dom/shadow/move-marquee-crossing-treescope-crash-expected.txt?r1=187348&r2=187347&pathrev=187348
   M http://src.chromium.org/viewvc/blink/branches/chromium/2214/Source/core/animation/css/CSSAnimations.cpp?r1=187348&r2=187347&pathrev=187348
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/dom/StyleSheet/resources/stylesheet-move-iframe1.xml?r1=187348&r2=187347&pathrev=187348
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/dom/shadow/make-marquee-bold-by-exec-command-crash-expected.html?r1=187348&r2=187347&pathrev=187348
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/dom/shadow/make-marquee-bold-by-exec-command-crash.html?r1=187348&r2=187347&pathrev=187348
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/dom/StyleSheet/resources/stylesheet-move-iframe2.html?r1=187348&r2=187347&pathrev=187348
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/dom/StyleSheet/stylesheet-move-between-documents-crash-expected.txt?r1=187348&r2=187347&pathrev=187348
   M http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/dom/StyleSheet/detached-style-pi-2.xhtml?r1=187348&r2=187347&pathrev=187348
   M http://src.chromium.org/viewvc/blink/branches/chromium/2214/Source/core/dom/ProcessingInstruction.cpp?r1=187348&r2=187347&pathrev=187348
   M http://src.chromium.org/viewvc/blink/branches/chromium/2214/Source/core/dom/StyleEngine.cpp?r1=187348&r2=187347&pathrev=187348

Aggregated patch for fixing https://crbug.com/chromium/427249

The problem required the following changes to fix completely.

For https://crbug.com/chromium/427249
 - r185504
 - r186026
For https://crbug.com/chromium/437174
 - r186152
For https://crbug.com/chromium/439319
 - r187237

This required some manual merging and tested locally.

BUG=427249

-----------------------------------------------------------------

### in...@chromium.org (2014-12-17)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

Mo' money - panel notes: "$2000 as no control between use and free". 

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-10)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-04-07)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/427249?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/434970]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080719)*

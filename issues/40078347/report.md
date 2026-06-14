# Heap-use-after-free in WebCore::HTMLTreeBuilder::adjustedCurrentStackItem

| Field | Value |
|-------|-------|
| **Issue ID** | [40078347](https://issues.chromium.org/issues/40078347) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | cl...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2013-11-06 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the latest chrome asan build.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-232951  

Operating System: Linux 64-bit

**REPRODUCTION CASE**  

Attached in crash.zip as it requires multiple files. Requires the following command-line options: --no-sandbox --allow-file-access-from-files --enable-logging=stderr --js-flags=--expose\_gc

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: ASAN output attached in stack.txt

## Attachments

- [stack.txt](attachments/stack.txt) (text/plain; charset=us-ascii, 10.5 KB)
- [crash.zip](attachments/crash.zip) (application/zip; charset=binary, 1.0 KB)

## Timeline

### cl...@chromium.org (2013-11-06)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5750675711459328

### cl...@chromium.org (2013-11-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5750675711459328

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x6110000a0314
Crash State:
  - crash stack -
  WebCore::HTMLTreeBuilder::adjustedCurrentStackItem
  WebCore::HTMLTreeBuilder::constructTree
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=232951:233008

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96_eRrjxCXwLVYDHPzETiTZnhEGA6jlcuXulCHgol0z8BA3gqaJyAbDhNEoc3dHfai7PkSuiCDznv32WfSlq0quHG-F-aaV8LdWfpCwlQuhrz4H97cn6mPvcR1y3oC3MxrV7ZXCBNsrV6nJ-4mHKrNQvvW4Mw



### cl...@chromium.org (2013-11-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5750675711459328

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x6110000a0314
Crash State:
  - crash stack -
  WebCore::HTMLTreeBuilder::adjustedCurrentStackItem
  WebCore::HTMLTreeBuilder::constructTree
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=232951:233008

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96_eRrjxCXwLVYDHPzETiTZnhEGA6jlcuXulCHgol0z8BA3gqaJyAbDhNEoc3dHfai7PkSuiCDznv32WfSlq0quHG-F-aaV8LdWfpCwlQuhrz4H97cn6mPvcR1y3oC3MxrV7ZXCBNsrV6nJ-4mHKrNQvvW4Mw



### cl...@chromium.org (2013-11-07)

Adding milestone and impact labels.

### ae...@chromium.org (2013-11-07)

Thanks for the report.

Minimized repro:

<script>
function free() {
  document.adoptNode(input);
  gc();
}

svg = document.createElementNS('http://www.w3.org/2000/svg','mover');
input = document.createElement('input');
svg.appendChild(input);
svg = null;
input.insertAdjacentHTML('afterend', '<section onload="free()"></section>');
</script>


### ae...@chromium.org (2013-11-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-08)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

Adding ReleaseBlock-Stable label.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-11-08)

Fixing bug priority based on security_severity-* and releaseblock-* labels.

### cl...@chromium.org (2013-11-08)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5808562206932992

### cl...@chromium.org (2013-11-08)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5808562206932992

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x611000033c14
Crash State:
  - crash stack -
  WebCore::HTMLTreeBuilder::adjustedCurrentStackItem
  WebCore::HTMLTreeBuilder::constructTree
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=232100:232107

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95jzuao7O6ESgFP84kbq4_atU-qQWCaKugYCQWlz7r5gYwUBTRtkPBJq8ozBKO6n_iofpm0j9wlT4l1EykAmMP6CxlWJ56nygl61AKCRTdfYDrGUh-gyWUAtEPnWNjSLN2Vd9yDolEK_62M-nifbBLcgwarFg



### in...@chromium.org (2013-11-08)

From reduced testcase, regression range looks right. Definitely looks like regrssion from http://src.chromium.org/viewvc/blink?view=rev&revision=160981

davve@, please look at minimized repro in https://code.google.com/p/chromium/issues/detail?id=315842#c5. If you are unable to look into this soon, please verify and revert your changeset.



### [Deleted User] (2013-11-09)

I'm looking into it now.

### [Deleted User] (2013-11-09)

I can't reproduce this locally, perhaps because of timing issues or because I need to instrument my build somehow to get gc() and timing right, but from stack.txt and minimized test it looks like the following happens:

1. An SVG element is created.
2. An <input> element is created and appended as child to the SVG element.
3. The SVG element reference is removed (set to null).
4. (GC may happen here)
5. insertAdjacentHTML, afterend-variant is called on <input>, which means the operation will really operate of the *parent* of <input>: the SVG element.
6. During the call to insertAdjacentHTML, the code I added in r160981 looks at the "context element", which is the SVG element, which is allegedly somehow deleted in the GC of step 4 and we get an use-after-free.

I still don't know how the explicitly called gc and adoptNode, also in the minimized test, fits into this. Since I haven't been able to reproduce locally, so I can't verify if the above is correct. It seems really strange to me that the parentNode of <input> is garbage collected, so I guess I'm missing something.

Since I'm not sure how to proceed with this at this stage, unless I am able to get some help with this, I will upload a CL for revert soon.

### [Deleted User] (2013-11-09)

I meant http://src.chromium.org/viewvc/blink?view=rev&revision=160981 in step 6 of the previous comment.

### [Deleted User] (2013-11-09)

Revert is https://codereview.chromium.org/67773002

### [Deleted User] (2013-11-09)

After contemplating this some more, I realized the SVG load handling is a bit special, and that there the SVG load may be fired during parsing. That means adoptNode would be called *during* the insertAdjacentHTML call, clearing references to its parent and contextElement would be left without a reference. The call to gc() would remove it.

The fix to the scenario above seems simple, protect the contextElement during insertAdjacentHTML: https://codereview.chromium.org/67813002

Side note: What a deliciously crafted minimized test case. I'm amazed there are tools  able to find this and minimize it down to the bare essentials. 

### [Deleted User] (2013-11-09)

The update scenario is: (Superseeds https://code.google.com/p/chromium/issues/detail?id=315842#c13)

1. An SVG element is created.
2. An <input> element is created and appended as child to the SVG element.
3. The SVG element reference is removed (set to null).
4. insertAdjacentHTML, afterend-variant is called on <input>, which means the operation will really operate of the *parent* of <input>: the SVG element.
5. During the call to insertAdjacentHTML, the load event fires on the SVG and propagates downward the tree and hits the load event handler at <input>. In the event handler, the <input> is made parent-less through a call to adoptNode. When the event handler also triggers a GC, the SVG element is deleted, it has no references anymore.
6. Also during the call to insertAdjacentHTML, the code I added in http://src.chromium.org/viewvc/blink?view=rev&revision=160981 looks at the "context element", the deleted SVG element, and we get an use-after-free.

### in...@chromium.org (2013-11-09)

were you testing this in a memory debugging ASAN build - http://www.chromium.org/developers/testing/addresssanitizer ?

Pass this flag to chrome --js-flags="--expose-gc" to enable gc

### [Deleted User] (2013-11-09)

Thanks! I actually did find out about --js-flags="--expose-gc" when reading the bug a bit closer.

### cl...@chromium.org (2013-11-10)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5500954501709824

Fuzzer: Inferno_twister
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x60f0000064a4
Crash State:
  - crash stack -
  WebCore::HTMLTreeBuilder::adjustedCurrentStackItem
  WebCore::HTMLTreeBuilder::constructTree
  - free stack -
  WebCore::LiveNodeListBase::~LiveNodeListBase
  WebCore::ChildNodeList::~ChildNodeList
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=232100:232107

Minimized Testcase (5.93 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95exIsC9N-f9_KS6ek_R_ANxOC7mnDq95-0iwJCtZ_8apFC5yKUGB_RjdPS1f_VSI6f6OgMeH57fbx9RHhTL2rj6ekom-BBLTfQlLCvULyX7lBB8h-raSZlBr5d-JvC7gjOOqsqcvy_MI2QvfiQyRA_3J6DnA



### bu...@chromium.org (2013-11-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=161697

------------------------------------------------------------------------
r161697 | davve@opera.com | 2013-11-10T21:07:29.950287Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLElement.cpp?r1=161697&r2=161696&pathrev=161697
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/insertAdjacentHTML-afterend-crash-expected.txt?r1=161697&r2=161696&pathrev=161697
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/insertAdjacentHTML-afterend-crash.html?r1=161697&r2=161696&pathrev=161697

Protect contextElement during insertAdjacentHTML call

JS event handlers may cause element to lose its last ref during
parsing.

BUG=315842

Review URL: https://codereview.chromium.org/67813002
------------------------------------------------------------------------

### in...@chromium.org (2013-11-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-11-10)

Is there a merge required here?

### cl...@chromium.org (2013-11-10)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-11-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-11)

m32 branch info
Branch number is: 1700
Branched Chromium at revision: 232870
Branched Blink at revision:  161254

Since regression revision is http://src.chromium.org/viewvc/blink?view=rev&revision=160981, m32 is impacted. Merged to m32 in r161729


### bu...@chromium.org (2013-11-11)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=161729

------------------------------------------------------------------------
r161729 | inferno@chromium.org | 2013-11-11T16:11:25.069310Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1700/LayoutTests/fast/dom/insertAdjacentHTML-afterend-crash.html?r1=161729&r2=161728&pathrev=161729
   M http://src.chromium.org/viewvc/blink/branches/chromium/1700/Source/core/html/HTMLElement.cpp?r1=161729&r2=161728&pathrev=161729
   A http://src.chromium.org/viewvc/blink/branches/chromium/1700/LayoutTests/fast/dom/insertAdjacentHTML-afterend-crash-expected.txt?r1=161729&r2=161728&pathrev=161729

Merge 161697 "Protect contextElement during insertAdjacentHTML call"

> Protect contextElement during insertAdjacentHTML call
> 
> JS event handlers may cause element to lose its last ref during
> parsing.
> 
> BUG=315842
> 
> Review URL: https://codereview.chromium.org/67813002

TBR=davve@opera.com

Review URL: https://codereview.chromium.org/64123004
------------------------------------------------------------------------

### cl...@chromium.org (2013-11-12)

ClusterFuzz has detected this issue as fixed in range 234212:234345.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5500954501709824

Fuzzer: Inferno_twister
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x60f0000064a4
Crash State:
  - crash stack -
  WebCore::HTMLTreeBuilder::adjustedCurrentStackItem
  WebCore::HTMLTreeBuilder::constructTree
  - free stack -
  WebCore::LiveNodeListBase::~LiveNodeListBase
  WebCore::ChildNodeList::~ChildNodeList
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=232100:232107
Fixed: https://cluster-fuzz.appspot.com/revisions?range=234212:234345

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95exIsC9N-f9_KS6ek_R_ANxOC7mnDq95-0iwJCtZ_8apFC5yKUGB_RjdPS1f_VSI6f6OgMeH57fbx9RHhTL2rj6ekom-BBLTfQlLCvULyX7lBB8h-raSZlBr5d-JvC7gjOOqsqcvy_MI2QvfiQyRA_3J6DnA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2013-11-12)

ClusterFuzz has detected this issue as fixed in range 234212:234345.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5808562206932992

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x611000033c14
Crash State:
  - crash stack -
  WebCore::HTMLTreeBuilder::adjustedCurrentStackItem
  WebCore::HTMLTreeBuilder::constructTree
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=232100:232107
Fixed: https://cluster-fuzz.appspot.com/revisions?range=234212:234345

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95jzuao7O6ESgFP84kbq4_atU-qQWCaKugYCQWlz7r5gYwUBTRtkPBJq8ozBKO6n_iofpm0j9wlT4l1EykAmMP6CxlWJ56nygl61AKCRTdfYDrGUh-gyWUAtEPnWNjSLN2Vd9yDolEK_62M-nifbBLcgwarFg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2013-11-13)

ClusterFuzz has detected this issue as fixed in range 234212:234345.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5750675711459328

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x6110000a0314
Crash State:
  - crash stack -
  WebCore::HTMLTreeBuilder::adjustedCurrentStackItem
  WebCore::HTMLTreeBuilder::constructTree
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=232951:233008
Fixed: https://cluster-fuzz.appspot.com/revisions?range=234212:234345

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96_eRrjxCXwLVYDHPzETiTZnhEGA6jlcuXulCHgol0z8BA3gqaJyAbDhNEoc3dHfai7PkSuiCDznv32WfSlq0quHG-F-aaV8LdWfpCwlQuhrz4H97cn6mPvcR1y3oC3MxrV7ZXCBNsrV6nJ-4mHKrNQvvW4Mw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### mb...@chromium.org (2013-12-10)

Thanks for the report! This one qualifies for a $2000 reward. There seems to be control between the free and use, but the freed object is in one of our heap partitions.

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

Hey Nils, it's payout time! I kicked off our process on this, so expect to see the money on this one (and the other pending issues) in a few weeks. Thanks and happy holidays.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-28)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/315842?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078347)*

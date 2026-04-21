# Security: Universal XSS via ContainerNode::parserInsertBefore

| Field | Value |
|-------|-------|
| **Issue ID** | [40082665](https://issues.chromium.org/issues/40082665) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM |
| **Reporter** | ma...@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2015-08-11 |
| **Bounty** | $8,837.00 |

## Description

**VULNERABILITY DETAILS**  

From /WebKit/Source/core/dom/ContainerNode.cpp:

---

void ContainerNode::parserInsertBefore(PassRefPtrWillBeRawPtr<Node> newChild, Node& nextChild)  

{  

(...)  

while (RefPtrWillBeRawPtr<ContainerNode> parent = newChild->parentNode())  

parent->parserRemoveChild(\*newChild);

```
if (document() != newChild->document())  
    document().adoptNode(newChild.get(), ASSERT_NO_EXCEPTION);  

{  
    EventDispatchForbiddenScope assertNoEventDispatch;  
    ScriptForbiddenScope forbidScript;  

    treeScope().adoptIfNeeded(\*newChild);  
    insertBeforeCommon(nextChild, \*newChild);  
    newChild->updateAncestorConnectedSubframeCountForInsertion();  
    ChildListMutationScope(\*this).childAdded(\*newChild);  
}  

notifyNodeInserted(\*newChild, ChildrenChangeSourceParser);  

```
## }

|parserRemoveChild| can run script, and it can remove |nextChild| from DOM or move the node around. When this happens, the tree will be in an inconsistent state after the |insertBeforeCommon| call, allowing an attacker to bypass the frame restrictions.

**VERSION**  

Chrome 44.0.2403.130 (Stable)  

Chrome 45.0.2454.26 (Beta)  

Chrome 46.0.2471.2 (Dev)  

Chromium 46.0.2480.0 (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/zip, 1.8 KB)
- [patch-519558.txt](attachments/patch-519558.txt) (text/plain, 1.0 KB)

## Timeline

### ma...@gmail.com (2015-08-11)

Here's a potential patch for the issue.

### rs...@chromium.org (2015-08-11)

Thank you for the report. I can confirm that the alert dialog does display the wrong origin.

esprehn: source control says you have touched this function in the past. Can you take a look?

### rs...@chromium.org (2015-08-11)

Also, if you can write an automated test for this (and ideally upload it to our code review system per http://dev.chromium.org/developers/contributing-code), the reward amount will be higher than just for the PoC.

### ma...@gmail.com (2015-08-11)

Okay, I'll give it a try in a few hours.

### ma...@gmail.com (2015-08-12)

Please see https://codereview.chromium.org/1283263002

### es...@chromium.org (2015-08-12)

The location.href when the javascript url runs is:

Safari: about:blank
Firefox/Chrome: data:text/html,crossOrigin

All these things appear to be same origin though, can you explain where the XSS is?

### ma...@gmail.com (2015-08-12)

The XSS is exactly there, data: URIs are cross-origin with the opener in Google Chrome. You can verify it by opening a data: URI in a frame and trying to access properties of the window. You can also replace the "data:" URI with a remote address in the exploit code and it will work the same. Yes, Firefox has a different behavior in this respect, ie. it's same-origin.

I used a data: URI because it has a unique origin and can be opened locally, which is useful for testing in network isolated VMs. OTOH, trying to load a website with no network available results in opening a data: URI (data:text/html,chromewebdata), so maybe it doesn't make much difference :-) I'll remember to use a remote address in the future to avoid confusion.

### bu...@chromium.org (2015-08-18)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=200690

------------------------------------------------------------------
r200690 | marius.mlynski@gmail.com | 2015-08-18T04:30:56.325244Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/parser/scriptexec-during-parserInsertBefore-expected.txt?r1=200690&r2=200689&pathrev=200690
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/parser/scriptexec-during-parserInsertBefore.html?r1=200690&r2=200689&pathrev=200690
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ContainerNode.cpp?r1=200690&r2=200689&pathrev=200690

parserInsertBefore: Bail out if the parent no longer contains the child.

nextChild may be removed from the DOM tree during the
|parserRemoveChild(*newChild)| call which triggers unload events of newChild's 
descendant iframes. In order to maintain the integrity of the DOM tree, the
insertion of newChild must be aborted in this case.

This patch adds a return statement that rectifies the behavior in this
edge case.

BUG=519558

Review URL: https://codereview.chromium.org/1283263002
-----------------------------------------------------------------

### rs...@chromium.org (2015-08-18)

Thanks for the report, patch, and test!

### cl...@chromium.org (2015-08-18)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### ti...@google.com (2015-08-30)

#9: +1! Thanks Marius!

This is already in M46 based on the branch point, so no merge required to M46. 

If there's an additional release of M45, we can try to sneak this patch into it. Leaving the Merge-Triage label on this bug for that reason.

### bu...@chromium.org (2015-09-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c71a21e6dda9025c2bf823c5aab791c2ae8cdfc2

commit c71a21e6dda9025c2bf823c5aab791c2ae8cdfc2
Author: marius.mlynski@gmail.com <marius.mlynski@gmail.com>
Date: Tue Aug 18 04:30:56 2015

parserInsertBefore: Bail out if the parent no longer contains the child.

nextChild may be removed from the DOM tree during the
|parserRemoveChild(*newChild)| call which triggers unload events of newChild's 
descendant iframes. In order to maintain the integrity of the DOM tree, the
insertion of newChild must be aborted in this case.

This patch adds a return statement that rectifies the behavior in this
edge case.

BUG=519558

Review URL: https://codereview.chromium.org/1283263002

git-svn-id: svn://svn.chromium.org/blink/trunk@200690 bbb929c8-8fbe-4397-9dbb-9b2b20218538

[add] http://crrev.com/c71a21e6dda9025c2bf823c5aab791c2ae8cdfc2/third_party/WebKit/LayoutTests/fast/parser/scriptexec-during-parserInsertBefore-expected.txt
[add] http://crrev.com/c71a21e6dda9025c2bf823c5aab791c2ae8cdfc2/third_party/WebKit/LayoutTests/fast/parser/scriptexec-during-parserInsertBefore.html
[modify] http://crrev.com/c71a21e6dda9025c2bf823c5aab791c2ae8cdfc2/third_party/WebKit/Source/core/dom/ContainerNode.cpp


### ti...@google.com (2015-10-12)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-13)

Nice work again - $8837 for this report. ($7500 for the high quality report with functioning exploit + $1337 bonus for the high quality patch)

Panel notes: Very nice XSS + exploit + patch!

I'll credit you in the release notes tomorrow and add this payment to your tab :) Congratulations! I'll add in a CVE shortly.

### ma...@gmail.com (2015-10-13)

Great, thanks! :)

### ti...@google.com (2015-10-13)

Thank you - keep them coming :)

### cl...@chromium.org (2015-11-24)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-03-12)

As discussed, I'll use this one to try the new process (because it's the oldest).

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

This issue was migrated from crbug.com/chromium/519558?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082665)*

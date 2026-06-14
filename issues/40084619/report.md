# Security: Universal XSS with Flash calling into JavaScript inside Node::removedFrom

| Field | Value |
|-------|-------|
| **Issue ID** | [40084619](https://issues.chromium.org/issues/40084619) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>HTML |
| **Reporter** | se...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2016-06-19 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

|Node::removedFrom()| is called while the DOM tree is in an inconsistent state and therefore is not supposed  

to run user JavaScript code. However, HTMLPlugInElement overrides |removedFrom()| to call |Widget::dispose()|,  

and <https://crbug.com/chromium/546545> demonstrates how the Flash plugin can be used to call JavaScript code inside |dispose()|.

src/third\_party/WebKit/Source/core/html/HTMLPlugInElement.cpp:85:  

void HTMLPlugInElement::setPersistedPluginWidget(Widget\* widget)  

{  

if (m\_persistedPluginWidget == widget)  

return;  

if (m\_persistedPluginWidget) {  

if (m\_persistedPluginWidget->isPluginView()) {  

m\_persistedPluginWidget->hide();  

m\_persistedPluginWidget->dispose();  

} else {  

ASSERT(m\_persistedPluginWidget->isFrameView() || m\_persistedPluginWidget->isRemoteFrameView());  

}  

}  

m\_persistedPluginWidget = widget;  

}

[...]

void HTMLPlugInElement::removedFrom(ContainerNode\* insertionPoint)  

{  

if (m\_persistedPluginWidget) {  

HTMLFrameOwnerElement::UpdateSuspendScope suspendWidgetHierarchyUpdates;  

setPersistedPluginWidget(nullptr);  

}  

HTMLFrameOwnerElement::removedFrom(insertionPoint);  

}

Note that |HTMLFrameOwnerElement::UpdateSuspendScope| doesn't defer the disposal of |m\_persistedPluginWidget|.

Also, in this case, unlike <https://crbug.com/chromium/546545>, it is not possible to use |ExternalInterface.call()| because  

|ScriptForbiddenScope| would block the script execution:

src/third\_party/WebKit/Source/core/dom/ContainerNode.cpp:728:  

void ContainerNode::notifyNodeRemoved(Node& root)  

{  

ScriptForbiddenScope forbidScript;  

EventDispatchForbiddenScope assertNoEventDispatch;

```
for (Node& node : NodeTraversal::inclusiveDescendantsOf(root)) {  
    if (!node.isContainerNode() && !node.isInTreeScope())  
        continue;  
    node.removedFrom(this);  
    for (ShadowRoot\* shadowRoot = node.youngestShadowRoot(); shadowRoot; shadowRoot = shadowRoot->olderShadowRoot())  
        notifyNodeRemoved(\*shadowRoot);  
}  

```

}

Instead, the repro case defines an [object-element-name]\_DoFSCommand getter on the global object in JavaScript  

and calls |fscommand()| in Flash.

The code that turns a corrupted DOM tree into a UXSS bug is copied from <https://crbug.com/chromium/456518>.

**VERSION**  

Google Chrome 51.0.2704.103 (Official Build) m (64-bit)  

Google Chrome 53.0.2772.0 (Official Build) canary (64-bit)

--

I would like to remain anonymous for this report.

## Attachments

- [repro.zip](attachments/repro.zip) (application/octet-stream, 2.0 KB)

## Timeline

### es...@chromium.org (2016-06-20)

[Empty comment from Monorail migration]

[Monorail components: Blink>HTML]

### es...@chromium.org (2016-06-20)

dcheng, do you think you could suggest an owner for this? Thanks.

### cl...@chromium.org (2016-06-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-21)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-06-21)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-06-21)

Incidentally, this is yet another reason letting plugins synchronously script during teardown is turning out very very poorly.

I wonder if we can force the dispose earlier, like when ChildFrameDisconnector is tearing down frames attached to nodes that are being removed from the DOM…

### dc...@chromium.org (2016-06-21)

+piman, +bbudge for a separate thread I'm going to start to see if we can get rid of this insanity altogether. We'll have to figure out another patch in the interim though.

### sh...@chromium.org (2016-07-06)

dcheng: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7bf106f2192e922c18f18cac4ae18d79ea90c1b0

commit 7bf106f2192e922c18f18cac4ae18d79ea90c1b0
Author: dcheng <dcheng@chromium.org>
Date: Wed Jul 13 05:15:53 2016

Use ChildFrameDisconnector when detaching child frames of a LocalFrame.

Currently, UpdateSuspendScope is used to defer widget updates when the
DOM hierarchy is mutated. This is used to prevent script from running
in the middle of DOM mutations, since plugins can run script when
destroyed.

This is part 1 of 2 CLs to remove the need for UpdateSuspendScope. Part
1 changes LocalFrame detach to always use ChildFrameDisconnector to
detach child frames. Part 2 will rework ChildFrameDisconnector to also
detach plugin elements. This should eliminate the need to defer widget
updates, since script will never have to run during the actual mutation
of internal state.

BUG=524113,528867,561683,621362

Review-Url: https://codereview.chromium.org/2134113002
Cr-Commit-Position: refs/heads/master@{#405040}

[modify] https://crrev.com/7bf106f2192e922c18f18cac4ae18d79ea90c1b0/third_party/WebKit/Source/core/frame/Frame.cpp
[modify] https://crrev.com/7bf106f2192e922c18f18cac4ae18d79ea90c1b0/third_party/WebKit/Source/core/frame/Frame.h
[modify] https://crrev.com/7bf106f2192e922c18f18cac4ae18d79ea90c1b0/third_party/WebKit/Source/core/frame/LocalFrame.cpp
[modify] https://crrev.com/7bf106f2192e922c18f18cac4ae18d79ea90c1b0/third_party/WebKit/Source/core/frame/LocalFrame.h
[modify] https://crrev.com/7bf106f2192e922c18f18cac4ae18d79ea90c1b0/third_party/WebKit/Source/core/frame/RemoteFrame.cpp
[modify] https://crrev.com/7bf106f2192e922c18f18cac4ae18d79ea90c1b0/third_party/WebKit/Source/core/frame/RemoteFrame.h


### bu...@chromium.org (2016-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7bf106f2192e922c18f18cac4ae18d79ea90c1b0

commit 7bf106f2192e922c18f18cac4ae18d79ea90c1b0
Author: dcheng <dcheng@chromium.org>
Date: Wed Jul 13 05:15:53 2016

Use ChildFrameDisconnector when detaching child frames of a LocalFrame.

Currently, UpdateSuspendScope is used to defer widget updates when the
DOM hierarchy is mutated. This is used to prevent script from running
in the middle of DOM mutations, since plugins can run script when
destroyed.

This is part 1 of 2 CLs to remove the need for UpdateSuspendScope. Part
1 changes LocalFrame detach to always use ChildFrameDisconnector to
detach child frames. Part 2 will rework ChildFrameDisconnector to also
detach plugin elements. This should eliminate the need to defer widget
updates, since script will never have to run during the actual mutation
of internal state.

BUG=524113,528867,561683,621362

Review-Url: https://codereview.chromium.org/2134113002
Cr-Commit-Position: refs/heads/master@{#405040}

[modify] https://crrev.com/7bf106f2192e922c18f18cac4ae18d79ea90c1b0/third_party/WebKit/Source/core/frame/Frame.cpp
[modify] https://crrev.com/7bf106f2192e922c18f18cac4ae18d79ea90c1b0/third_party/WebKit/Source/core/frame/Frame.h
[modify] https://crrev.com/7bf106f2192e922c18f18cac4ae18d79ea90c1b0/third_party/WebKit/Source/core/frame/LocalFrame.cpp
[modify] https://crrev.com/7bf106f2192e922c18f18cac4ae18d79ea90c1b0/third_party/WebKit/Source/core/frame/LocalFrame.h
[modify] https://crrev.com/7bf106f2192e922c18f18cac4ae18d79ea90c1b0/third_party/WebKit/Source/core/frame/RemoteFrame.cpp
[modify] https://crrev.com/7bf106f2192e922c18f18cac4ae18d79ea90c1b0/third_party/WebKit/Source/core/frame/RemoteFrame.h


### sh...@chromium.org (2016-07-14)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-07-15)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-07-20)

This isn't fixed yet, I'm still working out the details of widget cleanup, which is proving to be surprisingly complicated.

For now, I'll likely check in a horrible hack. Blah.

### oc...@chromium.org (2016-07-20)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-07-21)

I'm having trouble reproing this on dev channel chrome: are there any special steps I need to take before running this repro?

### se...@gmail.com (2016-07-21)

The issue still reproduces for me on chrome dev win64, the only requirement is that the repro should be hosted on a web server.

### dc...@chromium.org (2016-07-21)

Thanks, I was missing that step: sorry, I should have tried that first!

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-21)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2016-07-21)

Note: https://chromium.googlesource.com/chromium/src/+/cade7295256e7adabf84272fe5e269834eb44dde is the actual fix for this. I plan on revisiting this in a few weeks still, to rework widget detach.

### se...@gmail.com (2016-07-22)

#19: Sorry, I should have noted that in the report. Hopefully, it won't happen again since I add a protocol check to more recent repro cases.

### dc...@chromium.org (2016-07-27)

Removing the bogus merge label and requesting a merge to M52.

### di...@chromium.org (2016-07-27)

[Automated comment] Request affecting a post-stable build (M52), manual review required.

### go...@chromium.org (2016-07-27)

+awhalley@, seems like this also require a merge to M53 branch 2785, correct?



### aw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-27)

Yep!

### di...@chromium.org (2016-07-27)

Your change meets the bar and is auto-approved for M53 (branch: 2785)

### go...@chromium.org (2016-07-27)

Please try to merge you change to M53 branch 2785 ASAP latest by 5:00 PM PDT today (sooner the better to avoid compile failure and merge conflicts) so we can take it for tomorrow's M53 beta promotion. Thank you.

### dc...@chromium.org (2016-07-27)

I'm in Tokyo time atm and about to go to sleep. I don't feel comfortable merging without being around for potential failures; is anyone else willing to do the merge for me? Thanks!

### aw...@chromium.org (2016-07-27)

Ok, I'll take a shot at it.

### bu...@chromium.org (2016-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4d1400b0018d9e7e301a49d9ee1a6c38197e35ce

commit 4d1400b0018d9e7e301a49d9ee1a6c38197e35ce
Author: awhalley <awhalley@chromium.org>
Date: Wed Jul 27 17:50:22 2016

[merge to M53] Make sure Widget::dispose() respects UpdateSuspendScope.

BUG=621362

Review-Url: https://codereview.chromium.org/2171683002
Cr-Commit-Position: refs/heads/master@{#406802}
(cherry picked from commit cade7295256e7adabf84272fe5e269834eb44dde)

TBR=dcheng
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true

Review-Url: https://codereview.chromium.org/2190693002
Cr-Commit-Position: refs/branch-heads/2785@{#371}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/4d1400b0018d9e7e301a49d9ee1a6c38197e35ce/third_party/WebKit/Source/core/html/HTMLFrameOwnerElement.cpp
[modify] https://crrev.com/4d1400b0018d9e7e301a49d9ee1a6c38197e35ce/third_party/WebKit/Source/core/html/HTMLFrameOwnerElement.h
[modify] https://crrev.com/4d1400b0018d9e7e301a49d9ee1a6c38197e35ce/third_party/WebKit/Source/core/html/HTMLPlugInElement.cpp


### aw...@chromium.org (2016-07-29)

[Comment Deleted]

### aw...@chromium.org (2016-07-29)

[Comment Deleted]

### aw...@chromium.org (2016-08-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-02)

Another great bug, many thanks.  $7,500 from the panel.

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2019-02-16)

[Empty comment from Monorail migration]

### is...@google.com (2019-02-16)

This issue was migrated from crbug.com/chromium/621362?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084619)*

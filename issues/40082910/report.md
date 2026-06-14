# Security: Universal XSS via the unload_event module

| Field | Value |
|-------|-------|
| **Issue ID** | [40082910](https://issues.chromium.org/issues/40082910) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM, Platform>Extensions |
| **Reporter** | ma...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2015-09-22 |
| **Bounty** | $7,500.00 |

## Description

## **VULNERABILITY DETAILS** From /WebKit/Source/core/loader/DocumentLoader.cpp:

PassRefPtrWillBeRawPtr<DocumentWriter> DocumentLoader::createWriterFor(const Document\* ownerDocument, const DocumentInit& init, ...)  

{  

LocalFrame\* frame = init.frame();

```
ASSERT(!frame->document() || !frame->document()->isActive());  
ASSERT(frame->tree().childCount() == 0);  

if (!init.shouldReuseDefaultView())  
    frame->setDOMWindow(LocalDOMWindow::create(\*frame));  

RefPtrWillBeRawPtr<Document> document = frame->localDOMWindow()->installNewDocument(mimeType, init);  

```
## (...) }

|frame->setDOMWindow| clears the window proxy, which disposes the V8 context, which notifies observers of WillReleaseScriptContext. Among the observers, there's |extension\_dispatcher\_|, which loads the "unload\_event" module and triggers its |dispatch| method. This in turn can run user's code through getters/setters. Having arbitrary script at this execution point may lead to all sorts of broken/unexpected behavior, the example below bypasses SOP by attaching a document that's never forced to detach itself from the frame.

**VERSION**  

Chrome 45.0.2454.99 (Stable)  

Chrome 46.0.2490.33 (Beta)  

Chrome 47.0.2508.0 (Dev)  

Chromium 47.0.2517.0 (Release build compiled today)

## Attachments

- deleted (application/octet-stream, 0 B)
- [exploit.html](attachments/exploit.html) (text/html, 561 B)

## Timeline

### ma...@gmail.com (2015-09-22)

The original PoC had a leftover line, here's the cleaned version.

### md...@chromium.org (2015-09-23)

Ouch, nice find.

dcheng/kenrb: Git blame shows you two have poked around nearby recently. Can you help identify someone to fix this?

### md...@chromium.org (2015-09-23)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-09-23)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-09-23)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-09-23)

I think we can work around this by:
1. explicitly clearing the window proxy in FrameLoader::prepareForCommit(), so it will run with the same timing as normal unload events.
2. asserting that the window proxy has been cleared in LocalFrame::setDOMWindow().

### dc...@chromium.org (2015-09-24)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-09-25)

I have a Blink-side fix in https://codereview.chromium.org/1362203002.

However, looking at this more carefully, I'm wondering if we should be executing script in the main world at all. In general, it seems dangerous to have to run extension-related JS in the main world. It looks like it's used for two things: custom runtime bindings (https://code.google.com/p/chromium/codesearch#chromium/src/extensions/renderer/resources/runtime_custom_bindings.js) and the stash client (no idea what this is: https://code.google.com/p/chromium/codesearch#chromium/src/extensions/renderer/resources/stash_client.js). Are either of these exposed to the main world?

### [Deleted User] (2015-09-25)

There are a couple of extension APIs we expose to the main world.

### jo...@chromium.org (2015-09-29)

hum, exposing APIs to the main world is one thing, but we really shouldn't run script in it

### [Deleted User] (2015-09-30)

In extensions, exposing APIs == executing scripts. The ship has long sailed to change this.

### dc...@chromium.org (2015-09-30)

As mentioned earlier, I see two uses of the unload_event module in extensions.

One is in runtime_custom_bindings.js. I don't understand the purpose of these checks:
- wasDispatched should never be true while Documents are able to execute script
- by the time this is set to true, Documents aren't able to execute script (the exception is, of course, this current bug). So it should be impossible to hit these checks.

The other use is in stash_client.js. It looks like this is related to something for stashing mojo connections (https://chromium.googlesource.com/chromium/src/+/a0a73e578b6785c23cc945021fc9a955b19f8231)... and that doesn't seem like something that should be exposed to the main world either.

Given this, can we also change the extensions code to not execute the unload_event module in the main world?

### dc...@chromium.org (2015-09-30)

I'm still doing a few more tests on my fix, but I've also filed https://crbug.com/chromium/537658 to explore the feasibility of removing unload_event.js completely.

### [Deleted User] (2015-09-30)

FYI I was doing work a while ago to remove the unload event, the last was r325156 (a while ago, never got back to it).

### dc...@chromium.org (2015-10-01)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-10-03)

I've removed unload_event in the Chrome side. The UXSS should no longer be possible, but I plan on updating my Blink patch and landing that too as an additional mitigation.

### dc...@chromium.org (2015-10-15)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-10-20)

+bokan for reference

### ke...@chromium.org (2015-10-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-23)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### dc...@chromium.org (2015-11-23)

The fix has already been landed in the blocking bugs.

### cl...@chromium.org (2015-11-23)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-11-23)

We'll use this bug for release tracking and reward. Note that the actual fixes are linked off https://crbug.com/chromium/537658 and are in M46 + M47, though we'll use the release notes for M47 for public acknowledgement.

### ti...@google.com (2015-12-01)

Another $7500 here for another great report. Keep them coming, but I hope that they are getting harder to find :)

### bu...@chromium.org (2016-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/718b48fe05a4405c2edf2748e3819c5a2b8ccd3e

commit 718b48fe05a4405c2edf2748e3819c5a2b8ccd3e
Author: dcheng <dcheng@chromium.org>
Date: Mon Feb 01 06:08:21 2016

Disallow scripting earlier in LocalFrame::detach().

The Chrome extension implementation no longer needs to run script in
WebFrameClient::willReleaseScriptContext(), so forbid scripting earlier
in detach to make it harder to break invariants.

BUG=534923,555773

Review URL: https://codereview.chromium.org/1657583002

Cr-Commit-Position: refs/heads/master@{#372611}

[modify] http://crrev.com/718b48fe05a4405c2edf2748e3819c5a2b8ccd3e/third_party/WebKit/Source/core/frame/LocalFrame.cpp


### as...@chromium.org (2016-02-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-02)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

- Your friendly Sheriffbot

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### ki...@gmail.com (2017-07-12)

Yes

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/534923?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>DOM, Platform>Extensions]
[Monorail blocked-on: crbug.com/chromium/537658]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082910)*

# Security: Universal XSS using an <input type="color"> element

| Field | Value |
|-------|-------|
| **Issue ID** | [40085773](https://issues.chromium.org/issues/40085773) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Forms |
| **Platforms** | Android, Linux, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2016-10-22 |
| **Bounty** | $7,500.00 |

## Description

## **VULNERABILITY DETAILS** When an input element is removed, the popup is closed during the layout tree detach:

## void HTMLInputElement::detachLayoutTree(const AttachContext& context) { HTMLTextFormControlElement::detachLayoutTree(context); m\_needsToUpdateViewValue = true; m\_inputTypeView->closePopupView(); }

## If the chooser is still being displayed, its associated popup is torn down and the client (ColorChooserPopupUIController for inputs of type "color") is notified:

## void WebPagePopupImpl::closePopup() { // This function can be called in EventDispatchForbiddenScope for the main // document, and the following operations dispatch some events. It's safe // because web authors can't listen the events. EventDispatchForbiddenScope::AllowUserAgentEvents allowEvents; (...) m\_popupClient->didClosePopup(); m\_webView->cleanupPagePopup(); }

## The notification is propagated back to the input type, which may dispatch a change event to the input element if its value has changed recently:

## void ColorInputType::didEndChooser() { EventQueueScope scope; if (LayoutTheme::theme().isModalColorChooser()) element().dispatchFormControlChangeEvent(); m\_chooser.clear(); }

An attacker can exploit this synchronous event to corrupt the DOM tree.

**VERSION**  

Chrome 54.0.2840.59 (Stable)  

Chrome 55.0.2883.21 (Beta)  

Chrome 56.0.2896.3 (Dev)  

Chromium 56.0.2899.0 (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 1.4 KB)

## Timeline

### mb...@chromium.org (2016-10-23)

tkent: would you mind taking a look at this one?

[Monorail components: Blink>Forms]

### sh...@chromium.org (2016-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-23)

[Empty comment from Monorail migration]

### tk...@chromium.org (2016-10-24)

> An attacker can exploit this synchronous event to corrupt the DOM tree.

No. We can do DOM operations here, but it's expected and unable to *corrupt* DOM tree.

expoit.zip you attached didn't have any security issues.


### ma...@gmail.com (2016-10-24)

>No. We can do DOM operations here, but it's expected and unable to *corrupt* DOM tree.

That'd be great, but DOM operations in the middle of node removal can definitely leave DOM in a corrupted state, you can attach frames or move the node which is being removed (or its siblings). In case it's unclear, here's the stack for the offending event dispatch:

#0  blink::EventDispatcher::dispatchEvent
#1  blink::ScopedEventQueue::dispatchEvent
#2  blink::ScopedEventQueue::dispatchAllEvents
#3  blink::ScopedEventQueue::decrementScopingLevel
#4  blink::EventQueueScope::~EventQueueScope
#5  blink::ColorInputType::didEndChooser
#6  blink::ColorChooserUIController::didEndChooser
#7  blink::ColorChooserPopupUIController::didClosePopup
#8  blink::WebPagePopupImpl::closePopup
#9  blink::WebViewImpl::closePagePopup
#10 blink::ChromeClientImpl::closePagePopup
#11 blink::ColorChooserPopupUIController::closePopup
#12 blink::ColorChooserPopupUIController::endChooser
#13 blink::ColorInputType::endColorChooser
#14 blink::ColorInputType::closePopupView
#15 blink::HTMLInputElement::detachLayoutTree
#16 blink::ContainerNode::removeBetween
#17 blink::ContainerNode::removeChild
#18 blink::Node::remove
#19 blink::ChildNode::remove
#20 blink::ElementV8Internal::removeMethod
#21 blink::ElementV8Internal::removeMethodCallback
#22 v8::internal::FunctionCallbackArguments::Call

>expoit.zip you attached didn't have any security issues.

Could you please provide more details? When I open exploit.html and click anywhere in the content area, a dialog appears with the message: "An embedded page at example.org says: https://example.org". The exploit was tested on Windows and Linux, and I didn't see any issues with reliability. Thanks for checking and sorry for an inconvenience.

### tk...@chromium.org (2016-10-24)

> a dialog appears with the message: "An embedded page at example.org says: https://example.org".

You mean cross-domain access to window.location for the iframe should be blocked but it bypassed the cross-domain check, right?
Yeah, it's a security issue definitely.


### tk...@chromium.org (2016-10-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fbe37c7239e4a6e75f12c0d35e60987a6aa75ee0

commit fbe37c7239e4a6e75f12c0d35e60987a6aa75ee0
Author: tkent <tkent@chromium.org>
Date: Tue Oct 25 06:20:07 2016

INPUT element: Do not dispatch events in detachLayoutTree().

When a color chooser is closed, we dispatches a 'change' event asynchronously.
Some tests need to be updated due to this behavior change.

BUG=658535

Review-Url: https://codereview.chromium.org/2447653002
Cr-Commit-Position: refs/heads/master@{#427286}

[add] https://crrev.com/fbe37c7239e4a6e75f12c0d35e60987a6aa75ee0/third_party/WebKit/LayoutTests/fast/forms/color/color-no-event-during-detach.html
[modify] https://crrev.com/fbe37c7239e4a6e75f12c0d35e60987a6aa75ee0/third_party/WebKit/LayoutTests/fast/forms/color/input-color-choose-default-value-after-set-value.html
[modify] https://crrev.com/fbe37c7239e4a6e75f12c0d35e60987a6aa75ee0/third_party/WebKit/LayoutTests/fast/forms/color/input-color-onchange-event-expected.txt
[modify] https://crrev.com/fbe37c7239e4a6e75f12c0d35e60987a6aa75ee0/third_party/WebKit/LayoutTests/fast/forms/color/input-color-onchange-event.html
[modify] https://crrev.com/fbe37c7239e4a6e75f12c0d35e60987a6aa75ee0/third_party/WebKit/LayoutTests/platform/mac/fast/forms/color/input-color-onchange-event-expected.txt
[modify] https://crrev.com/fbe37c7239e4a6e75f12c0d35e60987a6aa75ee0/third_party/WebKit/Source/core/html/HTMLTextFormControlElement.cpp
[modify] https://crrev.com/fbe37c7239e4a6e75f12c0d35e60987a6aa75ee0/third_party/WebKit/Source/core/html/HTMLTextFormControlElement.h
[modify] https://crrev.com/fbe37c7239e4a6e75f12c0d35e60987a6aa75ee0/third_party/WebKit/Source/core/html/forms/ColorInputType.cpp
[modify] https://crrev.com/fbe37c7239e4a6e75f12c0d35e60987a6aa75ee0/third_party/WebKit/Source/web/WebPagePopupImpl.cpp


### tk...@chromium.org (2016-10-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-26)

[Empty comment from Monorail migration]

### tk...@chromium.org (2016-10-27)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-10-27)

[Automated comment] Request affecting a post-stable build (M54), manual review required.

### di...@chromium.org (2016-10-27)

Your change meets the bar and is auto-approved for M55 (branch: 2883)

### di...@chromium.org (2016-10-27)

[Automated comment] Request affecting a post-stable build (M54), manual review required.

### bu...@chromium.org (2016-10-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/84a1c644124f7803e63efbde9aed259016cd2c19

commit 84a1c644124f7803e63efbde9aed259016cd2c19
Author: Kent Tamura <tkent@chromium.org>
Date: Fri Oct 28 00:46:23 2016

Merge "INPUT element: Do not dispatch events in detachLayoutTree()." to M55 branch.

When a color chooser is closed, we dispatches a 'change' event asynchronously.
Some tests need to be updated due to this behavior change.

BUG=658535

Review-Url: https://codereview.chromium.org/2447653002
Cr-Commit-Position: refs/heads/master@{#427286}
(cherry picked from commit fbe37c7239e4a6e75f12c0d35e60987a6aa75ee0)

Review URL: https://codereview.chromium.org/2458743004 .

Cr-Commit-Position: refs/branch-heads/2883@{#353}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[add] https://crrev.com/84a1c644124f7803e63efbde9aed259016cd2c19/third_party/WebKit/LayoutTests/fast/forms/color/color-no-event-during-detach.html
[modify] https://crrev.com/84a1c644124f7803e63efbde9aed259016cd2c19/third_party/WebKit/LayoutTests/fast/forms/color/input-color-choose-default-value-after-set-value.html
[modify] https://crrev.com/84a1c644124f7803e63efbde9aed259016cd2c19/third_party/WebKit/LayoutTests/fast/forms/color/input-color-onchange-event-expected.txt
[modify] https://crrev.com/84a1c644124f7803e63efbde9aed259016cd2c19/third_party/WebKit/LayoutTests/fast/forms/color/input-color-onchange-event.html
[modify] https://crrev.com/84a1c644124f7803e63efbde9aed259016cd2c19/third_party/WebKit/LayoutTests/platform/mac/fast/forms/color/input-color-onchange-event-expected.txt
[modify] https://crrev.com/84a1c644124f7803e63efbde9aed259016cd2c19/third_party/WebKit/Source/core/html/HTMLTextFormControlElement.cpp
[modify] https://crrev.com/84a1c644124f7803e63efbde9aed259016cd2c19/third_party/WebKit/Source/core/html/HTMLTextFormControlElement.h
[modify] https://crrev.com/84a1c644124f7803e63efbde9aed259016cd2c19/third_party/WebKit/Source/core/html/forms/ColorInputType.cpp
[modify] https://crrev.com/84a1c644124f7803e63efbde9aed259016cd2c19/third_party/WebKit/Source/web/WebPagePopupImpl.cpp


### aw...@chromium.org (2016-10-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2016-10-28)

Spoke with awhalley@ about this offline, we won't be CPing this for 54 - the fix is larger than we'd like at this stage in the game and the change hasn't baked in beta at all.

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-07)

Congratulations, $7,500 from the panel for this report!

### aw...@chromium.org (2016-11-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/658535?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085773)*

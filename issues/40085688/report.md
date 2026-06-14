# Security: Universal XSS via fullscreen element updates

| Field | Value |
|-------|-------|
| **Issue ID** | [40085688](https://issues.chromium.org/issues/40085688) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>SVG |
| **Reporter** | ma...@gmail.com |
| **Assignee** | fo...@chromium.org |
| **Created** | 2016-10-14 |
| **Bounty** | $7,500.00 |

## Description

## **VULNERABILITY DETAILS** From /third\_party/WebKit/Source/core/dom/Fullscreen.cpp:

## void Fullscreen::didEnterFullscreenForElement(Element\* element) { (...) // FIXME: This should not call updateStyleAndLayoutTree. document()->updateStyleAndLayoutTree(); (...) }

Indeed. |didEnterFullscreenForElement| may be called in the middle of DOM node removal if the node being removed is the active fullscreen element and there are other fullscreen elements on the Fullscreen::m\_fullscreenElementStack (see Fullscreen::exitFullscreen()). In specific circumstances, when the document's focused node is in a <use> shadow tree with a scheduled update, this synchronous layout update may result in events being dispatched at a wrong time, which allows an attacker to corrupt the DOM tree.

**VERSION**  

Chrome 54.0.2840.59 (Stable)  

Chrome 54.0.2840.59 (Beta)  

Chrome 55.0.2883.11 (Dev)  

Chromium 56.0.2890.0 (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 4.5 KB)

## Timeline

### mm...@chromium.org (2016-10-14)

Thanks for your report! That's cool.

[Monorail components: Blink>DOM]

### sh...@chromium.org (2016-10-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-14)

[Empty comment from Monorail migration]

### jo...@chromium.org (2016-10-14)

[Empty comment from Monorail migration]

### es...@chromium.org (2016-10-14)

If you reduce the test case a bunch you correctly hit the ScriptForbiddenScope which should mitigate these attacks (the crash is still a bug, but it's not a security bug). 

What seems so serious here is that somehow the page is getting JS to execute and *not* hit the ScriptForbiddenScope? :(

I don't understand how the full screen API is related, what's happening inside the full screen code that creates the UXSS?

[Monorail components: -Blink>DOM Blink>SVG]

### es...@chromium.org (2016-10-14)

[Empty comment from Monorail migration]

### aa...@google.com (2016-10-14)

[Empty comment from Monorail migration]

### ma...@gmail.com (2016-10-14)

The fullscreen code triggers a layout update, and that can fire events in the middle of child node removal -- if you run the exploit in a debug build, it should hit an EventDispatchForbiddenScope assertion with a stack like this:

[1:1:1012/225739:FATAL:EventDispatcher.cpp(56)] Check failed: !EventDispatchForbiddenScope::isEventDispatchForbidden(). 
#0 0x7f2901a8ee4e base::debug::StackTrace::StackTrace()
#1 0x7f2901afcc8f logging::LogMessage::~LogMessage()
#2 0x7f28e943ac36 blink::EventDispatcher::dispatchEvent()
#3 0x7f28e91f4a24 blink::Node::dispatchEventInternal()
#4 0x7f28e945489c blink::EventTarget::dispatchEvent()
#5 0x7f28e91758ef blink::Element::dispatchBlurEvent()
#6 0x7f28e9e0f16b blink::SVGAElement::dispatchBlurEvent()
#7 0x7f28e9105224 blink::Document::setFocusedElement()
#8 0x7f28e9104aea blink::Document::clearFocusedElement()
#9 0x7f28e9104aa5 blink::Document::removeFocusedElementOfSubtree()
#10 0x7f28e90bce65 blink::ContainerNode::removeChildren()
#11 0x7f28e9ebb0f2 blink::SVGUseElement::clearShadowTree()
#12 0x7f28e9ebc1ca blink::SVGUseElement::buildPendingResource()
#13 0x7f28e90fa214 blink::Document::updateUseShadowTreesIfNeeded()
#14 0x7f28e90f686c blink::Document::updateStyleAndLayoutTree()
#15 0x7f28e91a68d8 blink::Fullscreen::didEnterFullscreenForElement()
#16 0x7f28f2d69a72 blink::FullscreenController::didEnterFullscreen()
#17 0x7f28f2d69f0f blink::FullscreenController::enterFullscreenForElement()
#18 0x7f28f2e7feef blink::WebViewImpl::enterFullscreenForElement()
#19 0x7f28f2d2b681 blink::ChromeClientImpl::enterFullscreenForElement()
#20 0x7f28e91a61a8 blink::Fullscreen::exitFullscreen()
#21 0x7f28e91a710e blink::Fullscreen::elementRemoved()
#22 0x7f28e916ea54 blink::Element::removedFrom()
#23 0x7f28e90bcd60 blink::ContainerNode::notifyNodeRemoved()
#24 0x7f28e90bcf14 blink::ContainerNode::removeChildren()
#25 0x7f28e91f055f blink::Node::setTextContent()
#26 0x7f28ea150609 blink::NodeV8Internal::textContentAttributeSetter()
#27 0x7f28ea150510 blink::NodeV8Internal::textContentAttributeSetterCallback()
#28 0x7f28f733615d v8::internal::FunctionCallbackArguments::Call()

Events are undesirable in ScriptForbiddenScopes -- the dispatch can call into V8 in the process, for example to instantiate a JS event wrapper (this is probably the crash you're seeing) or to fetch a function from an event listener object (this is where you see JS execute).

### es...@chromium.org (2016-10-14)

Here's a fix for the ScriptForbiddenScope bypass: https://codereview.chromium.org/2423623002

document.addEventListener("blur", {get handleEvent() { 
  /* this getter will run */
  return function() { /* this won't run */ };
}});

We won't run the event listener because of the early return in V8ScriptRunner::callFunction, but we will still call the getter.

I do wonder if v8 should be running the beforeCallEnteredCallback in this case? We run it when doing micro tasks but not around getters/setters which can run arbitrary code too.

### fo...@chromium.org (2016-10-17)

I would say that the core problem is that both Fullscreen::requestFullscreen() and exitFullscreen() take a synchronous shortcut for nested fullscreen cases, in this case the Fullscreen::didEnterFullscreenForElement().

Per spec, calls to requestFullscreen() and exitFullscreen() should synchronously merely determine whether to resize the window or not. If we shouldn't which is the case here, we should wait until the next animation frame to actually do the work of changing the fullscreen element stack, firing events and fiddling with the layout. I'm treating https://crbug.com/chromium/402421 as tracking that, because to fix those timing issues is precisely what it would take to make webkitCurrentFullScreenElement an alias.

esprehn@, do you think that https://codereview.chromium.org/2423623002 is a sufficient mitigation for this that could be backported? The work that I still have on a branch for https://crbug.com/chromium/402421 might also fix this, but it comes with compat risk and not a great idea to backport I think.

### bu...@chromium.org (2016-10-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/610b88604db99184334982ab982d758296718879

commit 610b88604db99184334982ab982d758296718879
Author: esprehn <esprehn@chromium.org>
Date: Mon Oct 17 20:10:35 2016

Don't run handleEvent getter in V8EventListener::getListenerFunction if script is forbidden.

It results in arbitrary code execution under ScriptForbiddenScopes. :(

BUG=655904

Review-Url: https://codereview.chromium.org/2423623002
Cr-Commit-Position: refs/heads/master@{#425763}

[modify] https://crrev.com/610b88604db99184334982ab982d758296718879/third_party/WebKit/Source/bindings/core/v8/V8EventListener.cpp


### es...@chromium.org (2016-10-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-22)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-24)

[Empty comment from Monorail migration]

### di...@google.com (2016-10-24)

[Automated comment] There appears to be on-going work (i.e. bugroid changes), needs manual review.

### aw...@chromium.org (2016-10-24)

Good for M55.

### go...@chromium.org (2016-10-24)

Approving merge to M55 branch 2883 per https://crbug.com/chromium/655904#c17. Please merge ASAP. Thank you.

### bu...@chromium.org (2016-10-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e4aa8931b775f144de76b4ae3f335348f8e1e0ff

commit e4aa8931b775f144de76b4ae3f335348f8e1e0ff
Author: Philip Jägenstedt <foolip@chromium.org>
Date: Mon Oct 24 20:47:43 2016

Don't run handleEvent getter in V8EventListener::getListenerFunction if script is forbidden.

It results in arbitrary code execution under ScriptForbiddenScopes. :(

BUG=655904

Review-Url: https://codereview.chromium.org/2423623002
Cr-Commit-Position: refs/heads/master@{#425763}
(cherry picked from commit 610b88604db99184334982ab982d758296718879)

Review URL: https://codereview.chromium.org/2449623002 .

Cr-Commit-Position: refs/branch-heads/2883@{#259}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/e4aa8931b775f144de76b4ae3f335348f8e1e0ff/third_party/WebKit/Source/bindings/core/v8/V8EventListener.cpp


### aw...@chromium.org (2016-10-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-27)

Very nice, $7,500 for this report :-)

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e4aa8931b775f144de76b4ae3f335348f8e1e0ff

commit e4aa8931b775f144de76b4ae3f335348f8e1e0ff
Author: Philip Jägenstedt <foolip@chromium.org>
Date: Mon Oct 24 20:47:43 2016

Don't run handleEvent getter in V8EventListener::getListenerFunction if script is forbidden.

It results in arbitrary code execution under ScriptForbiddenScopes. :(

BUG=655904

Review-Url: https://codereview.chromium.org/2423623002
Cr-Commit-Position: refs/heads/master@{#425763}
(cherry picked from commit 610b88604db99184334982ab982d758296718879)

Review URL: https://codereview.chromium.org/2449623002 .

Cr-Commit-Position: refs/branch-heads/2883@{#259}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/e4aa8931b775f144de76b4ae3f335348f8e1e0ff/third_party/WebKit/Source/bindings/core/v8/V8EventListener.cpp


### aw...@chromium.org (2016-10-28)

[Empty comment from Monorail migration]

### es...@chromium.org (2016-11-02)

tkent@ adamk@ dcheng@ I think there's still a bug here, how was running script in the middle of the full screen code causing a UXSS like this? The ScriptForbiddenScope plugs the hole, but I'm not sure I understand how full screen was related here.

### dc...@chromium.org (2016-11-03)

The problem is the fullscreen code is getting invoked in the middle of DOM mutation. Running JS in the middle of DOM tree mutation is a primitive that's been leveraged to achieve UXSS several times in the past by corrupting the DOM tree...

I'll try to find some other UXSS bugs that abused the same primitive; I think one of them might have an explanation of how DOM tree corruption = UXSS.

### di...@google.com (2016-11-04)

[Automated comment] removing mislabelled merge-merged-2840

### di...@google.com (2016-11-04)

[Automated comment] removing mislabelled merge-merged-2840

### tk...@chromium.org (2016-11-07)

I recently fixed a similar security issue, https://crbug.com/chromium/658535.
I think we can make more improvement.

* ScriptForbiddenScope actually forbids script in release build, but EventDispatchForbiddenScope doesn't affect release build.  EventDispatchForbiddenScope should imply ScriptForbiddenScope.

* Updating <use> Shadow DOM in updateStyleAndLayoutTree sounds very bad.

* Both of this issue and https://crbug.com/chromium/658535 load content of a disconnected iframe, and bypass cross-origin check.  We should investigate why the bypass is possible, and should make the code defensive.


### es...@chromium.org (2016-11-09)

> tkent@ said:
> * Updating <use> Shadow DOM in updateStyleAndLayoutTree sounds very bad.

That was my design, it's a step right before we update style. Unfortunately the web requires it because it assumes that use trees are always synchronously updated, so we either need to update all use trees inside every DOM mutation (slow), or we need to do them async whenever we update style so getBoundingClientRect() and getComputedStyle() return the right answer. 

### aw...@chromium.org (2016-11-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/655904?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/656160]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085688)*

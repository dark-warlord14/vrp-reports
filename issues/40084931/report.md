# Security: Universal XSS by intercepting a UA shadow tree

| Field | Value |
|-------|-------|
| **Issue ID** | [40084931](https://issues.chromium.org/issues/40084931) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM, Blink>SVG |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ha...@chromium.org |
| **Created** | 2016-07-24 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

When an event is dispatched to an element in a SVG <use> shadow tree, Event::currentTarget returns the original corresponding node, but Event::target doesn't make any attempt to redirect access. Therefore, the tree can be trivially leaked like this:

<svg>
<g id="a">
<image href="" onerror="if (event.currentTarget !== event.target) {alert(event.target.parentNode.parentNode)}">
</g>
<use href="#a">
</svg>

Gaining access to the internal shadow tree allows an attacker to manipulate it in a way that allows triggering focus events in theoretically impossible circumstances, which may lead to DOM tree corruption.

**VERSION**  

Chrome 52.0.2743.82 (Stable)  

Chrome 52.0.2743.82 (Beta)  

Chrome 53.0.2785.21 (Dev)  

Chromium 54.0.2806.0 (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 1.4 KB)
- [exploit.html](attachments/exploit.html) (text/plain, 1021 B)
- [s.svg](attachments/s.svg) (image/svg+xml, 234 B)
- [svg-use-event.html](attachments/svg-use-event.html) (text/plain, 506 B)
- [exploit2.html](attachments/exploit2.html) (text/plain, 984 B)
- [s.svg](attachments/s_52940435.svg) (image/svg+xml, 227 B)

## Timeline

### ke...@chromium.org (2016-07-25)

When I try to reproduce in a VM, I just see a dialog that says "An embedded page at abc.xyz says:" and then a frame that contains errors.

Can you provide more details about what I should see when reproducing the problem and then re-open the bug? Thank you.

### ma...@gmail.com (2016-07-25)

You should see a dialog that says "An embedded page at abc.xyz says:". "abc.xyz" is a domain that should be protected by the same-origin policy. If you can execute arbitrary javascript code in the context of abc.xyz, it means the same-origin policy has been violated. If you replace "https://abc.xyz" with any other website that can be framed, you will see a dialog that says "An embedded page at [the domain of the website] says:".

Unfortunately, external contributors can't edit or re-open bugs.

### ke...@chromium.org (2016-07-25)

Thanks for the information. jww, mkwest, or estark, can one of you please take a look or let me know who can? Thank you.

[Monorail components: Blink]

### mk...@chromium.org (2016-07-26)

I'm OOO today. CCing Jochen and Max, as they _love_ UXSS bugs.

### mk...@chromium.org (2016-07-26)

Actually, Jochen's out too. Hrm. dcheng@? haraken@?

### dc...@chromium.org (2016-07-26)

[Empty comment from Monorail migration]

[Monorail components: -Blink Blink>DOM]

### ko...@chromium.org (2016-07-26)

+hayato@

### sh...@chromium.org (2016-07-26)

[Empty comment from Monorail migration]

### ri...@chromium.org (2016-07-26)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-07-27)

This looks a real exploit. 

I am impressed that we can be exploited by leaking SVG's UA shadow tree.

Let me investigate further. It looks that we have to retarget event's target correctly in case of svg's <use>, which is not retargeted correctly by a general event retarget mechanism, I guess.

Since I am not familiar with how SVG uses a UA shadow tree, the advise from the implementor of svg's <use> might be helpful.

### ha...@chromium.org (2016-07-27)

It looks that svg's <use>'s implementation is cloning a user-provided node (subtree) into their UA shadow tree.
I do not think cloning a user's node into UA shadow tree is a good idea. That might be a bad idea.

Given the current implementation of <use>, a quick fix would be https://codereview.chromium.org/2186823002.

This CL fixed only the *entrance* of the exploit. There might be another loophole.

I do not understand why leaking a node in svg's UA shadow tree can be an exploit, fully yet.


### ha...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

[Monorail components: Blink>SVG]

### jw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### pd...@chromium.org (2016-08-01)

I still don't understand the part shadow dom plays in this exploit so I'm a little reluctant to commit https://codereview.chromium.org/2186823002 just yet (but I do think we should land it).

This exploit hits an assertion failure in debug builds: "ASSERTION FAILED: !EventDispatchForbiddenScope::isEventDispatchForbidden()" in https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/events/EventDispatcher.cpp?l=49. As a mitigation, can we turn each of the 12 isEventDispatchForbidden ASSERTs into CHECKs which will crash in release?

I made some progress towards the root cause. https://src.chromium.org/viewvc/blink?view=rev&revision=190980 changed how frames are detached from the parser. 's.svg' adds an onunload hook and then introduces an xml parser error which causes the parser to put up a pink "This page contains the following errors:" page. A parser-created pink xml error page would explain how r190980 changed behavior to start letting the onunload handler run. Syncing before chrome@r318424 no longer reproduces this bug. I've attached a small modification to the testcase which is needed to work before https://crrev.com/2f0b655515af2df03d41d4f894e0dd59d5cb6411.

### ha...@chromium.org (2016-08-02)

Thanks for the investigation.

I am totally okay not to land this https://codereview.chromium.org/2186823002 as is, if we can fix the root cause.

We can think of another plan B, instead of this CL. At least, we should make SVGUseElement use an author open (or closed) shadow root, instead of UA shadow root, because UA shadow root is completely an implementation detail, and the spec should not use it.

If SVGUseElement uses an author open shadow root, I would not be reluctant to expose a node in a shadow tree. That's fine.






### ha...@chromium.org (2016-08-02)

> As a mitigation, can we turn each of the 12 isEventDispatchForbidden ASSERTs into CHECKs which will crash in release?

I think we can. Let me do it.


### ha...@chromium.org (2016-08-02)

> I think we can. Let me do it.

Hmm. Per https://cs.chromium.org/chromium/src/third_party/WebKit/Source/platform/EventDispatchForbiddenScope.h, it looks this is intended to be used only in DEBUB build. Maybe this might cause a performance regression slightly.

### ma...@gmail.com (2016-08-02)

> We can think of another plan B, instead of this CL. At least, we should make SVGUseElement use an author open (or closed) shadow root, instead of UA shadow root, because UA shadow root is completely an implementation detail, and the spec should not use it.
> If SVGUseElement uses an author open shadow root, I would not be reluctant to expose a node in a shadow tree. That's fine.

If you want to avoid the unexpected event dispatch and DEBUG crashes, you need to make sure that user scripts can't access nodes in a SVGUseElement shadow tree. I'm not an expert in this shadow business, but I think UA shadow trees might be better suited for this kind of isolation.

### ha...@chromium.org (2016-08-02)

> "ASSERTION FAILED: !EventDispatchForbiddenScope::isEventDispatchForbidden()" in https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/events/EventDispatcher.cpp?l=49.

I have investigated the cause of this ASSERTION hit.

I am afraid that this is caused by SVGUseElement's wrong management of a shadow tree. 

SVGUseElement::removedFrom(ContainerNode* insertionPoint), which is overriding Node::removedFrom(ContainerNode* insertionPoint), is doing their own management of shadow root and shadow root's children's lifetime.
The shadow root's children are removed at this timing. :( That would violate our assumption for node removal process.

As a result, we are wrongly dispatching focus/blur events, where an event dispatch is prohibited in our code base.

Thus, I think this exploit is making use of:

1. We allow an access to a node in <use>'s UA shadow tree via an event listener
2. Due to the wrong management of a <use>'s shadow tree, we wrongly dispatch an event, where the release build can not catch.
3. pdr@' explanation follows, I think.




### ha...@chromium.org (2016-08-02)

> If you want to avoid the unexpected event dispatch and DEBUG crashes, you need to make sure that user scripts can't access nodes in a SVGUseElement shadow tree. I'm not an expert in this shadow business, but I think UA shadow trees might be better suited for this kind of isolation.

Thanks. Yeah, given that the current implementation of SVGUseElement, I would be leaning toward the behavior: We never allow any access to a shadow tree of <use>, at least until we can rewrite SVGUseElement's implementation. That would be the safest approach, I think.

So this CL, https://codereview.chromium.org/2186823002, might be okay to land as the first step.




### ha...@chromium.org (2016-08-02)

Let me attach the test case which can hit ASSERT: ASSERTION FAILED: !EventDispatchForbiddenScope::isEventDispatchForbidden()", using SVGUseElement.

### ha...@chromium.org (2016-08-02)

[Empty comment from Monorail migration]

### pd...@chromium.org (2016-08-02)

Excellent analysis Hayato, that explanation makes sense to me. I support landing https://codereview.chromium.org/2186823002 now. Is there a way to test the bug introduced by https://src.chromium.org/viewvc/blink?view=rev&revision=190980 with that patch landed though?

### ha...@chromium.org (2016-08-03)

> Excellent analysis Hayato, that explanation makes sense to me. I support landing https://codereview.chromium.org/2186823002 now.

Thanks. Let me land the CL after I fix the failing tests.

> Is there a way to test the bug introduced by https://src.chromium.org/viewvc/blink?view=rev&revision=190980 with that patch landed though?

Good question. I can not think of any way for ToT after I land the CL :(

Though, I can prepare yet another small patch which is intentionally creating a *loophole* after I land the CL.

We can continue to investigate with a patched ToT. I will post a patch.




### ma...@gmail.com (2016-08-03)

> Is there a way to test the bug introduced by https://src.chromium.org/viewvc/blink?view=rev&revision=190980

I think you're barking up a wrong tree here. Before https://src.chromium.org/viewvc/blink?view=rev&revision=190980, you could attach iframes between the calls to parserRemoveChild and their associated frames wouldn't be detached, introducing another vulnerability. After that commit, there's a last-minute disconnector to catch any remaining descendant frames. Actually, the introduced disconnector gets in the way of the exploit, because it'd disconnect the corrupted frame if it was attached earlier. Without the disconnector introduced in that commit, there'd be no need to wait for a descendant iframe's unload handler -- an attacker could simply attach it at an earlier time.

> Though, I can prepare yet another small patch which is intentionally creating a *loophole* after I land the CL.

The easiest way to create the corrupted condition is to remove the |ChildFrameDisconnector(*this).disconnect(ChildFrameDisconnector::DescendantsOnly);| call from |ContainerNode::willRemoveChildren|. This way, each iframe you remove via |ContainerNode::removeChildren| (for example using |node.textContent=''|) is corrupted even without a bug like the one described in this report.

### bu...@chromium.org (2016-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c4f2b0897923d1fa54fd2b644f6771290e812f4b

commit c4f2b0897923d1fa54fd2b644f6771290e812f4b
Author: hayato <hayato@chromium.org>
Date: Wed Aug 03 04:37:46 2016

Do not call an event listener on a cloned node in svg <use>'s UA shadow tree

SVG <use> element tries to clone a user-provided subtree into its UA shadow tree.
This approach allows a user to access a cloned node in UA's shadow tree if a node
has an event listener.

e.g.
<svg>
  <g id="a">
    <image href="" onerror="window.nodes.push(event.target);">
  </g>
  <use href="#a">
</svg>

As a result, we will leak a node in <use>'s UA shadow tree.

Given the current implementation of <use>, we have to shrink an event path so
it does not include a node in <use>'s UA shadow tree.

A <use> element itself still receives an event if an event is a composed event.

This CL also reverts the most parts of https://codereview.chromium.org/312423002
because it is no longer valid in the latest SVG spec, and stop copying event
listeners from a referenced node into a cloned node because it is no longer
necessary.

BUG=630870

Review-Url: https://codereview.chromium.org/2186823002
Cr-Commit-Position: refs/heads/master@{#409455}

[modify] https://crrev.com/c4f2b0897923d1fa54fd2b644f6771290e812f4b/third_party/WebKit/LayoutTests/TestExpectations
[modify] https://crrev.com/c4f2b0897923d1fa54fd2b644f6771290e812f4b/third_party/WebKit/LayoutTests/svg/custom/resources/use-instanceRoot-event-bubbling.js
[add] https://crrev.com/c4f2b0897923d1fa54fd2b644f6771290e812f4b/third_party/WebKit/LayoutTests/svg/custom/use-event-attribute.html
[delete] https://crrev.com/476d90d93453f586a13e7bf83e596663a708a7b9/third_party/WebKit/LayoutTests/svg/custom/use-event-handler-on-referenced-element-addEventListener-expected.txt
[delete] https://crrev.com/476d90d93453f586a13e7bf83e596663a708a7b9/third_party/WebKit/LayoutTests/svg/custom/use-event-handler-on-referenced-element-addEventListener.svg
[delete] https://crrev.com/476d90d93453f586a13e7bf83e596663a708a7b9/third_party/WebKit/LayoutTests/svg/custom/use-event-handler-on-referenced-element-expected.txt
[delete] https://crrev.com/476d90d93453f586a13e7bf83e596663a708a7b9/third_party/WebKit/LayoutTests/svg/custom/use-event-handler-on-referenced-element-hierarchy-expected.txt
[delete] https://crrev.com/476d90d93453f586a13e7bf83e596663a708a7b9/third_party/WebKit/LayoutTests/svg/custom/use-event-handler-on-referenced-element-hierarchy.svg
[delete] https://crrev.com/476d90d93453f586a13e7bf83e596663a708a7b9/third_party/WebKit/LayoutTests/svg/custom/use-event-handler-on-referenced-element.svg
[modify] https://crrev.com/c4f2b0897923d1fa54fd2b644f6771290e812f4b/third_party/WebKit/LayoutTests/svg/custom/use-instanceRoot-event-bubbling-expected.txt
[modify] https://crrev.com/c4f2b0897923d1fa54fd2b644f6771290e812f4b/third_party/WebKit/LayoutTests/svg/custom/use-instanceRoot-event-listener-liveness.xhtml
[modify] https://crrev.com/c4f2b0897923d1fa54fd2b644f6771290e812f4b/third_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.h
[modify] https://crrev.com/c4f2b0897923d1fa54fd2b644f6771290e812f4b/third_party/WebKit/Source/core/events/Event.cpp
[modify] https://crrev.com/c4f2b0897923d1fa54fd2b644f6771290e812f4b/third_party/WebKit/Source/core/events/Event.h
[modify] https://crrev.com/c4f2b0897923d1fa54fd2b644f6771290e812f4b/third_party/WebKit/Source/core/events/EventListener.h
[modify] https://crrev.com/c4f2b0897923d1fa54fd2b644f6771290e812f4b/third_party/WebKit/Source/core/events/EventListenerMap.cpp
[modify] https://crrev.com/c4f2b0897923d1fa54fd2b644f6771290e812f4b/third_party/WebKit/Source/core/events/EventListenerMap.h
[modify] https://crrev.com/c4f2b0897923d1fa54fd2b644f6771290e812f4b/third_party/WebKit/Source/core/events/EventPath.cpp
[modify] https://crrev.com/c4f2b0897923d1fa54fd2b644f6771290e812f4b/third_party/WebKit/Source/core/svg/SVGUseElement.cpp
[modify] https://crrev.com/c4f2b0897923d1fa54fd2b644f6771290e812f4b/third_party/WebKit/Source/core/svg/SVGUseElement.h


### ha...@chromium.org (2016-08-03)

The CL, https://codereview.chromium.org/2186823002, was landed.

> We can continue to investigate with a patched ToT. I will post a patch.

I have made a small patch for ToT: https://codereview.chromium.org/2202173004.

You can use this patch for ToT to test the bug. I have also updated the exploit to make use of it. The attached exploit should work for ToT with the patch.


### ha...@chromium.org (2016-08-09)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-08-15)

I have filed a bug for SVGUseElement here: https://bugs.chromium.org/p/chromium/issues/detail?id=637641.

prd@, do you have a plan to continue to investigate what you explained https://bugs.chromium.org/p/chromium/issues/detail?id=637641 ?




### ha...@chromium.org (2016-08-15)

I meant https://bugs.chromium.org/p/chromium/issues/detail?id=630870#c15

### pd...@chromium.org (2016-08-15)

I think marius.mlynski's response (https://crbug.com/630870#c26) was correct that I was barking up the wrong tree. Lets mark this as fixed.

### ha...@chromium.org (2016-08-16)

I see. Let's mark this as fixed. Thank you for investigating this issue.


marius.mlynski,
Thank you for reporting. We really appreciate that.

### sh...@chromium.org (2016-08-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-25)

[Empty comment from Monorail migration]

### pd...@chromium.org (2016-08-25)

Glad to see this one got the maximum XSS reward. Thank you for your helpful comments on this bug Marius!

### bu...@chromium.org (2016-08-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fa6aa8c5e4a44fef3eba64f9ba2551f06ef3103f

commit fa6aa8c5e4a44fef3eba64f9ba2551f06ef3103f
Author: schenney <schenney@chromium.org>
Date: Thu Aug 25 20:58:54 2016

Change svg/animations/use-animate-width-and-height.html to Timeout instead of Skip

The goal is to discover if this times out forever, or is just slow.

TBR=pdr@chromium.org
BUG=630870

Review-Url: https://codereview.chromium.org/2277043002
Cr-Commit-Position: refs/heads/master@{#414532}

[modify] https://crrev.com/fa6aa8c5e4a44fef3eba64f9ba2551f06ef3103f/third_party/WebKit/LayoutTests/TestExpectations


### sc...@chromium.org (2016-08-26)

The test should be moved to Slow. I'll open a new bug.

### sh...@chromium.org (2016-11-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/66a0e78c24b56758cd9733959f583e6e75fa2b66

commit 66a0e78c24b56758cd9733959f583e6e75fa2b66
Author: hayato <hayato@chromium.org>
Date: Wed Nov 30 10:14:02 2016

Stop a SVG <use> element from modifying its UA shadow tree when it is removed

Each element should not modify its UA shadow tree when being removed.
That is like a *double-free* because a super class's |removedFrom()| handles that.

BUG=630870,637641

Review-Url: https://codereview.chromium.org/2537143004
Cr-Commit-Position: refs/heads/master@{#435205}

[modify] https://crrev.com/66a0e78c24b56758cd9733959f583e6e75fa2b66/third_party/WebKit/Source/core/svg/SVGUseElement.cpp


### aw...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### pd...@chromium.org (2017-01-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/630870?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>DOM, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084931)*

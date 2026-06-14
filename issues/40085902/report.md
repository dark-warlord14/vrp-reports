# Security: Universal XSS through removing link elements

| Field | Value |
|-------|-------|
| **Issue ID** | [40085902](https://issues.chromium.org/issues/40085902) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM |
| **Reporter** | ma...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2016-11-08 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

When a link element is notified about its removal from the tree and the linked stylesheet happens to be the last pending one in the document, the fragment anchor may be updated, which triggers layout updates when it should be forbidden. In special circumstances, the updates may end up resolving a FontFace load promise, which allows an attacker to bypass the ScriptForbiddenScope and corrupt the DOM tree. The exploit circumvents all the nifty protections planned in <https://codereview.chromium.org/2478573002/> as a bonus.

**VERSION**  

Chrome 54.0.2840.87 (Stable)  

Chrome 55.0.2883.35 (Beta)  

Chrome 56.0.2906.0 (Dev)  

Chromium 56.0.2914.0 (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 15.0 KB)

## Timeline

### dc...@chromium.org (2016-11-08)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-11-08)

[Empty comment from Monorail migration]

### ri...@chromium.org (2016-11-08)

Thanks for yet another great report! Adding tkent@ from the linked CL as well.

[Monorail components: Blink>DOM]

### sh...@chromium.org (2016-11-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-09)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-11-10)

Here's the stack:

#0 0x7efee25a948e base::debug::StackTrace::StackTrace()
#1 0x7efed556349c blink::FontFace::setLoadStatus()
#2 0x7efed551e53a blink::CSSFontFace::getFontData()
#3 0x7efed5541466 blink::CSSSegmentedFontFace::getFontData()
#4 0x7efed5522839 blink::CSSFontSelector::getFontData()
#5 0x7efedcf75640 blink::FontFallbackList::getFontData()
#6 0x7efedcf7553b blink::FontFallbackList::fontDataAt()
#7 0x7efedcf7533e blink::FontFallbackList::determinePrimarySimpleFontData()
#8 0x7efed5bed96e blink::ComputedStyle::computedLineHeight()
#9 0x7efed59f7121 blink::LayoutBlock::lineHeight()
#10 0x7efed59f763b blink::LayoutBlock::minLineHeightForReplacedObject()
#11 0x7efed5aed42c blink::LineWidth::updateAvailableWidth()
#12 0x7efed5ae5352 blink::LineBreaker::nextLineBreak()
#13 0x7efed5a0d9fb blink::LayoutBlockFlow::layoutRunsAndFloatsInRange()
#14 0x7efed5a0bfbe blink::LayoutBlockFlow::layoutRunsAndFloats()
#15 0x7efed5a104c1 blink::LayoutBlockFlow::layoutInlineChildren()
#16 0x7efed59fb4fe blink::LayoutBlockFlow::layoutBlockFlow()
#17 0x7efed59faf20 blink::LayoutBlockFlow::layoutBlock()
#18 0x7efed59f26b3 blink::LayoutBlock::layout()
#19 0x7efed59fc3c4 blink::LayoutBlockFlow::positionAndLayoutOnceIfNeeded()
#20 0x7efed59fc7a5 blink::LayoutBlockFlow::layoutBlockChild()
#21 0x7efed5a0063e blink::LayoutBlockFlow::layoutBlockChildren()
#22 0x7efed59fb4f5 blink::LayoutBlockFlow::layoutBlockFlow()
#23 0x7efed59faf20 blink::LayoutBlockFlow::layoutBlock()
#24 0x7efed59f26b3 blink::LayoutBlock::layout()
#25 0x7efed59fc3c4 blink::LayoutBlockFlow::positionAndLayoutOnceIfNeeded()
#26 0x7efed59fc7a5 blink::LayoutBlockFlow::layoutBlockChild()
#27 0x7efed5a0063e blink::LayoutBlockFlow::layoutBlockChildren()
#28 0x7efed59fb4f5 blink::LayoutBlockFlow::layoutBlockFlow()
#29 0x7efed59faf20 blink::LayoutBlockFlow::layoutBlock()
#30 0x7efed59f26b3 blink::LayoutBlock::layout()
#31 0x7efed5ab0c1c blink::LayoutView::layout()
#32 0x7efed57c9bbf blink::FrameView::performLayout()
#33 0x7efed57c7e9f blink::FrameView::layout()
#34 0x7efed57cc60d blink::FrameView::processUrlFragmentHelper()
#35 0x7efed57cc39c blink::FrameView::processUrlFragment()
#36 0x7efed562ec0e blink::Document::didLoadAllScriptBlockingResources()
#37 0x7efed585f8c9 blink::HTMLLinkElement::removedFrom()
#38 0x7efed560cb4f blink::ContainerNode::notifyNodeRemoved()
#39 0x7efed560c026 blink::ContainerNode::removeChild()
#40 0x7efed5d4170a blink::ElementV8Internal::removeMethodCallback()
#41 0x7efede2bd71f v8::internal::FunctionCallbackArguments::Call()
#42 0x7efede34579d v8::internal::(anonymous namespace)::HandleApiCallHelper<>()
#43 0x7efede344ca5 v8::internal::Builtin_Impl_HandleApiCall()

skobes@, mind looking at this one?

### sk...@chromium.org (2016-11-11)

I'm not the best person to tackle this.

It seems like blink::ScriptPromiseProperty ought to check ScriptForbiddenScope::isScriptForbidden before calling into v8::Promise::Resolver.

@dominicc, could you take a look?

### es...@chromium.org (2016-11-11)

Why does resolving the promise run script synchronously? That should queue a microtask and since there's no microtask scope as we're not inside script it should end up at end of task timing not inside layout.



### sk...@chromium.org (2016-11-11)

Perhaps because we are inside script (the one calling Element.remove)?

### es...@chromium.org (2016-11-12)

This is because we synchronously access the "then" property of whatever value is resolved in a promise, ex.

var thenable = {get then() { console.log(2); }}
console.log(1); Promise.resolve(thenable); console.log(3)

prints 1 2 3

There's two bugs here:

1. v8 needs to run the BeforeCallEnteredCallback whenever we call into v8, ex. calling Resolve() on a promise should crash in ScriptForbiddenScope. Here we call into the getter for "then" which should have run the entry hook and crashed in the ScriptForbiddenScope.

  isolate()->AddBeforeCallEnteredCallback(&beforeCallEnteredCallback);

https://cs.chromium.org/chromium/src/third_party/WebKit/Source/bindings/core/v8/V8PerIsolateData.cpp?q=ScriptForbiddenScope::isScript&sq=package:chromium&l=48&dr=C

2. We need to treat promise resolution like invoking user code, which means we need to go audit every algorithm that resolves promises synchronously to make sure it's actually posting a task. That sucks, and may require some spec changes, but it's a side effect of this thenable business. Everything using ScriptPromiseProperty needs to be audited too.

### do...@chromium.org (2016-11-12)

Per "spec" (not a great spec) at https://www.w3.org/2001/tag/doc/promises-guide#shorthand-manipulating you're supposed to queue a task when resolving/rejecting if inside an "in parallel" algorithm.

### es...@chromium.org (2016-11-18)

I have a hypothetical stop the bleeding patch: 
https://codereview.chromium.org/2516553002

We still need to fix the entry hooks for v8 and audit all of the callers, but at least this fixes the security bugs. Lets see what the bots say.

### bu...@chromium.org (2016-11-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/863f2af2768cddc229e8822c622fa7dd539de290

commit 863f2af2768cddc229e8822c622fa7dd539de290
Author: esprehn <esprehn@chromium.org>
Date: Fri Nov 18 08:21:04 2016

Never resolve promises inside ScriptForbiddenScopes.

BUG=663476

Review-Url: https://codereview.chromium.org/2516553002
Cr-Commit-Position: refs/heads/master@{#433149}

[modify] https://crrev.com/863f2af2768cddc229e8822c622fa7dd539de290/third_party/WebKit/Source/bindings/core/v8/ScriptPromiseResolver.h


### aw...@chromium.org (2016-11-21)

[Empty comment from Monorail migration]

### es...@chromium.org (2016-11-21)

[Empty comment from Monorail migration]

### jo...@chromium.org (2016-11-21)

still working on the v8 side of this, but it's a huge mess :-/

### di...@chromium.org (2016-11-21)

Your change meets the bar and is auto-approved for M56 (branch: 2924)

### bu...@chromium.org (2016-11-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a926d67b5e868f72ede22e72483ea873280bdaf1

commit a926d67b5e868f72ede22e72483ea873280bdaf1
Author: Elliott Sprehn <esprehn@chromium.org>
Date: Mon Nov 21 20:32:49 2016

Never resolve promises inside ScriptForbiddenScopes.

BUG=663476

Review-Url: https://codereview.chromium.org/2516553002
Cr-Commit-Position: refs/heads/master@{#433149}
(cherry picked from commit 863f2af2768cddc229e8822c622fa7dd539de290)

Review URL: https://codereview.chromium.org/2519153002 .

Cr-Commit-Position: refs/branch-heads/2924@{#38}
Cr-Branched-From: 3a87aecc31cd1ffe751dd72c04e5a96a1fc8108a-refs/heads/master@{#433059}

[modify] https://crrev.com/a926d67b5e868f72ede22e72483ea873280bdaf1/third_party/WebKit/Source/bindings/core/v8/ScriptPromiseResolver.h


### sh...@chromium.org (2016-11-22)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-11-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### mm...@google.com (2016-11-30)

CC'ing tkent@ as per c#3.

### aw...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-02)

Nice one, $7,500 for this report!

### aw...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-19)

[Empty comment from Monorail migration]

### jb...@chromium.org (2016-12-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/76b781d16735162ce3304f95c2749742185e12f1

commit 76b781d16735162ce3304f95c2749742185e12f1
Author: adithyas <adithyas@chromium.org>
Date: Fri Jan 13 17:36:41 2017

Make CSSFontFace::setLoadStatus post a task

Setting the load status to LOADED results in the promise associated with the FontFace "loaded" property being resolved synchronously. The promise is resolved with a loaded FontFace object. This could result in script being executed in a forbidden scope.

Posting a task when the status is ERROR/LOADED prevents the promise from being resolved inside a forbidden scope and matches the spec ("When the load operation completes, successfully or not, queue a task to run the following steps synchronously", see https://drafts.csswg.org/css-font-loading/#font-face-load).

BUG=663476

Review-Url: https://codereview.chromium.org/2610593002
Cr-Commit-Position: refs/heads/master@{#443596}

[modify] https://crrev.com/76b781d16735162ce3304f95c2749742185e12f1/third_party/WebKit/LayoutTests/fast/css/fontface-properties.html
[modify] https://crrev.com/76b781d16735162ce3304f95c2749742185e12f1/third_party/WebKit/Source/core/css/FontFace.cpp
[modify] https://crrev.com/76b781d16735162ce3304f95c2749742185e12f1/third_party/WebKit/Source/core/css/FontFace.h


### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### aa...@google.com (2017-02-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/663476?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085902)*

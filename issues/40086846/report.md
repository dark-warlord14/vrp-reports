# Corrupted memory use in blink::visualRectForDisplayItem

| Field | Value |
|-------|-------|
| **Issue ID** | [40086846](https://issues.chromium.org/issues/40086846) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Paint |
| **Platforms** | Windows |
| **Reporter** | wa...@gmail.com |
| **Assignee** | wk...@chromium.org |
| **Created** | 2017-02-19 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36

Steps to reproduce the problem:
1. Open http://localhost/poc.html 

What is the expected behavior?
No crash should occur

What went wrong?
Under certain conditions, setting the z-index of an animated node during its animation (with -webkit-animation) then removing this node from DOM before the end of the animation will cause this crash (see crash_stack_trace.txt).

Did this work before? N/A 

Chrome version: 56.0.2924.87  Channel: stable
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)
Flash Version: Shockwave Flash 24.0 r0


## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 3.4 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.1 KB)
- [iframe.html](attachments/iframe.html) (text/plain, 235 B)

## Timeline

### ra...@chromium.org (2017-02-20)

Thanks for the report!

I can repro this. There is a crash stack at go/crash/691675d740000000

chrishtr: could you please help triage? Thanks!

[Monorail components: Blink>Paint]

### ra...@chromium.org (2017-02-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-21)

[Empty comment from Monorail migration]

### sc...@chromium.org (2017-02-21)

Reassigning.

### sh...@chromium.org (2017-03-05)

wkorman: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sc...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### wk...@chromium.org (2017-03-09)

I can repro at ToT, and with a debug build we get more info thanks to Xianzhu's previous work on debug notification of short-lived display item clients.

Test case with reformatting attached. Run with:

% ./out/Debug/content_shell --disable-composited-antialiasing --enable-threaded-compositing poc.html

[1:1:0308/213631.338921:2276793983482:FATAL:DisplayItemClient.cpp(37)] Check failed: !item.value.contains(this). Short-lived DisplayItemClient: "LayoutBlockFlow (relative positioned) DIV". See crbug.com/609218.
#0 0x7f820b50dbbb base::debug::StackTrace::StackTrace()
#1 0x7f820b50c24c base::debug::StackTrace::StackTrace()
#2 0x7f820b57a73f logging::LogMessage::~LogMessage()
#3 0x7f8204dbfffa blink::DisplayItemClient::~DisplayItemClient()
#4 0x7f8202558cfe blink::PaintLayer::~PaintLayer()
#5 0x7f8202559069 blink::PaintLayer::~PaintLayer()
#6 0x7f820128321f std::default_delete<>::operator()()
#7 0x7f82021c951c std::unique_ptr<>::reset()
#8 0x7f82021c8257 _ZNSt10unique_ptrIN5blink10PaintLayerESt14default_deleteIS1_EEaSEDn
#9 0x7f82021c1913 blink::LayoutBoxModelObject::destroyLayer()
#10 0x7f82021c1851 blink::LayoutBoxModelObject::willBeDestroyed()
#11 0x7f820219b1f8 blink::LayoutBox::willBeDestroyed()
#12 0x7f820214f628 blink::LayoutBlock::willBeDestroyed()
#13 0x7f8202173091 blink::LayoutBlockFlow::willBeDestroyed()
#14 0x7f8202244d5d blink::LayoutObject::destroy()
#15 0x7f8202244d3a blink::LayoutObject::destroyAndCleanupAnonymousWrappers()
#16 0x7f82018fd6ca blink::Node::detachLayoutTree()
#17 0x7f82017aca30 blink::ContainerNode::detachLayoutTree()
#18 0x7f820186f073 blink::Element::detachLayoutTree()
#19 0x7f82017ac0c5 blink::ContainerNode::removeBetween()
#20 0x7f82017ab636 blink::ContainerNode::removeChild()
#21 0x7f82018fae1a blink::Node::removeChild()
#22 0x7f82029c071f blink::NodeV8Internal::removeChildMethod()
#23 0x7f82029c03f2 blink::V8Node::removeChildMethodCallback()
#24 0x7f82059a55cb v8::internal::FunctionCallbackArguments::Call()
#25 0x7f8205a8a19f v8::internal::(anonymous namespace)::HandleApiCallHelper<>()
#26 0x7f8205a88a87 v8::internal::Builtin_Impl_HandleApiCall()
#27 0x3b8766884204 <unknown>


### sc...@chromium.org (2017-03-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-23)

wkorman: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wk...@chromium.org (2017-03-23)

I have not forgotten about this, and hope to look at it soon.

### wk...@chromium.org (2017-03-24)

This looks fixed at ToT by a change from wangxianzhu@, detail below. Should we explore merging a fix to M58? It looks like (1) below is the fixing change.

DETAIL --

I can no longer repro at ToT. Bisecting locally with bisect-builds.py for fixing change leads to:

https://chromium.googlesource.com/chromium/src/+log/85eb0199323407db76feaa192e0d0a0fd9b24f6f..0c449aad3898922b599d8a32c2380cc8c962040e

Two potentially fixing changes:

1. https://chromium.googlesource.com/chromium/src/+/0c449aad3898922b599d8a32c2380cc8c962040e
Eagerly invalidate when a layer becomes stacking context

2. https://chromium.googlesource.com/chromium/src/+/68ce3db5142fd83af38eb4ae9b5bc701d0555f7b
Fix another caret paint invalidation issue


### wk...@chromium.org (2017-03-24)

Marking fixed figuring per c#10 that will prompt follow-up from security team.

### sh...@chromium.org (2017-03-25)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-30)

Your change meets the bar and is auto-approved for M58. Please go ahead and merge the CL to branch 3029 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wk...@chromium.org (2017-03-30)

The fix was already merged to M58 about two weeks ago in:

https://codereview.chromium.org/2747143004

### aw...@google.com (2017-03-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-31)

Nice one! The panel decided to award $1,000 for this bug, but noted that if you are able to demonstrate exploitability they'll revisit to see if a higher amount might be justified.

### aw...@chromium.org (2017-03-31)

[Empty comment from Monorail migration]

### wa...@gmail.com (2017-04-01)

Thanks!

### aw...@google.com (2017-04-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/693974?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086846)*

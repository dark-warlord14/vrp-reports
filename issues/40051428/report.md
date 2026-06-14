# Heap-use-after-free in WebCore::InlineFlowBox::computeOverAnnotationAdjustment

| Field | Value |
|-------|-------|
| **Issue ID** | [40051428](https://issues.chromium.org/issues/40051428) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | sl...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2011-11-19 |
| **Bounty** | $1,000.00 |

## Description

Crashes on dev (17.0.942.0 [110446]) and canary (17.0.943.0 [110669]). I can't reproduce it on stable.

Repro:
----- crash1.html -----
<!DOCTYPE html>
<script>
    function main(){
        console.log(window.document.documentElement.previousSibling.nextSibling.clientLeft)
        window.document.designMode = 'on'
        console.log(window.document.documentElement.previousSibling.nextSibling.clientLeft)
    }
    window.onload = main;
</script>

<summary>
    <bdi>
        <object>
            <ruby>foo</ruby>
            <bdi dir="ltr">
                <embed>foo</embed>
            </bdi>
        </object>
    </bdi>
</summary>
-----------------------

(10d4.11b8): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=00dfa93c ebx=00df8280 ecx=00dfa8c0 edx=63b67110 esi=00dfaf8c edi=00df8400
eip=017c1f00 esp=0012e934 ebp=0012e95c iopl=0         nv up ei pl nz na po nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010202
017c1f00 d86ab6          fsubr   dword ptr [edx-4Ah]  ds:0023:63b670c6=76456472

ExceptionAddress: 017c1f00
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000008
   Parameter[1]: 017c1f00
Attempt to execute non-executable address 017c1f00

ChildEBP RetAddr  
WARNING: Frame IP not in any known module. Following frames may be wrong.
0012e930 6312b838 0x17c1f00
0012e95c 631275de chrome_624a0000!WebCore::InlineFlowBox::computeOverAnnotationAdjustment+0x6c
0012e980 63133d91 chrome_624a0000!WebCore::RootInlineBox::selectionTop+0x32
0012e990 63133f18 chrome_624a0000!WebCore::RenderReplaced::localSelectionRect+0x7f
0012e9e4 630d4cf7 chrome_624a0000!WebCore::RenderReplaced::clippedOverflowRectForRepaint+0x54
0012ea1c 630f8386 chrome_624a0000!WebCore::RenderObject::repaint+0x49
0012ea3c 630d2eb7 chrome_624a0000!WebCore::RenderObjectChildList::removeChildNode+0x4b
0012ea5c 630d6668 chrome_624a0000!WebCore::RenderObject::removeChild+0x2a
0012ea70 630dbf16 chrome_624a0000!WebCore::RenderObject::willBeDestroyed+0xb1
0012ea80 630e204f chrome_624a0000!WebCore::RenderBoxModelObject::willBeDestroyed+0x18
0012eaa0 6310d0d2 chrome_624a0000!WebCore::RenderBox::willBeDestroyed+0x86
0012eaa8 6334064f chrome_624a0000!WebCore::RenderWidget::destroy+0xb
0012eab8 6334b142 chrome_624a0000!WebCore::Node::detach+0x1b
0012eac0 63347890 chrome_624a0000!WebCore::Element::detach+0x2e
0012eacc 6334b142 chrome_624a0000!WebCore::ContainerNode::detach+0x13
0012ead4 63347890 chrome_624a0000!WebCore::Element::detach+0x2e
0012eae0 6334b142 chrome_624a0000!WebCore::ContainerNode::detach+0x13
0012eae8 63347890 chrome_624a0000!WebCore::Element::detach+0x2e
0012eaf4 6334b142 chrome_624a0000!WebCore::ContainerNode::detach+0x13
0012eafc 634a7b62 chrome_624a0000!WebCore::Element::detach+0x2e
0012eb08 6334786b chrome_624a0000!WebCore::ShadowContentElement::attach+0x42
0012eb18 6335eb1e chrome_624a0000!WebCore::ContainerNode::attach+0x14
0012eb20 6334b6ee chrome_624a0000!WebCore::ShadowRoot::attach+0x8
0012eb54 6334b66a chrome_624a0000!WebCore::Element::recalcStyle+0x41f
0012eb8c 6334b66a chrome_624a0000!WebCore::Element::recalcStyle+0x39b
0012ebc4 6333807c chrome_624a0000!WebCore::Element::recalcStyle+0x39b
0012ebf4 6333819a chrome_624a0000!WebCore::Document::recalcStyle+0x15c
0012ec00 63338227 chrome_624a0000!WebCore::Document::updateStyleIfNeeded+0x42
0012ec08 633382bf chrome_624a0000!WebCore::Document::updateLayout+0x20
0012ec14 63013514 chrome_624a0000!WebCore::Document::updateLayoutIgnorePendingStylesheets+0x6c
0012ec24 635269ef chrome_624a0000!WebCore::ElementInternal::clientLeftAttrGetter+0x1f
0012ec70 63532704 chrome_624a0000!v8::internal::JSObject::GetPropertyWithCallback+0x15f
0012ec90 63630445 chrome_624a0000!v8::internal::Object::GetProperty+0x1c4
0012ecd4 63631445 chrome_624a0000!v8::internal::LoadIC::Load+0x475
0012edb0 6354a65f chrome_624a0000!v8::internal::LoadIC_Miss+0x75
0012ede4 6354b057 chrome_624a0000!v8::internal::Invoke+0xff
0012ee18 6350e184 chrome_624a0000!v8::internal::Execution::Call+0x107
0012ee58 631f97be chrome_624a0000!v8::Function::Call+0xf4
0012ee98 631f9685 chrome_624a0000!WebCore::V8Proxy::instrumentedCallFunction+0xca
0012eec4 63251d19 chrome_624a0000!WebCore::V8Proxy::callFunction+0x45
0012ef00 63163e4d chrome_624a0000!WebCore::V8EventListener::callListenerFunction+0x6d
0012ef48 63163d0c chrome_624a0000!WebCore::V8AbstractEventListener::invokeEventHandler+0xcf
0012ef88 63350ec1 chrome_624a0000!WebCore::V8AbstractEventListener::handleEvent+0x69
0012efb8 63350dfe chrome_624a0000!WebCore::EventTarget::fireEventListeners+0xb6
0012efd4 6313f46a chrome_624a0000!WebCore::EventTarget::fireEventListeners+0x2c
0012f000 6313f501 chrome_624a0000!WebCore::DOMWindow::dispatchEvent+0xb6
0012f010 6313f2f9 chrome_624a0000!WebCore::DOMWindow::dispatchTimedEvent+0x31
0012f044 6333904c chrome_624a0000!WebCore::DOMWindow::dispatchLoadEvent+0x8e
0012f070 631de6bc chrome_624a0000!WebCore::Document::implicitClose+0xff
[...]


## Attachments

- [crash1.html](attachments/crash1.html) (text/html; charset=us-ascii, 503 B)
- [stack1.txt](attachments/stack1.txt) (text/x-c++; charset=us-ascii, 12.3 KB)
- [crash2.html](attachments/crash2.html) (text/plain; charset=us-ascii, 143 B)
- [crash3.html](attachments/crash3.html) (text/plain; charset=us-ascii, 224 B)
- [stack3.txt](attachments/stack3.txt) (text/x-c; charset=us-ascii, 8.6 KB)
- [stack4.txt](attachments/stack4.txt) (text/x-c++; charset=us-ascii, 6.7 KB)
- [crash4.html](attachments/crash4.html) (text/plain; charset=us-ascii, 345 B)

## Timeline

### sl...@gmail.com (2011-11-21)

A little simpler repro:

----- crash2.html -----
<bdi>
    <ruby>foo</ruby>
    <em  dir="ltr">
        <embed></embed>
        <audio onerror="open()" src="foo"></audio>
    </em>
</bdi>
-----------------------


### [Deleted User] (2011-11-21)

can you still reproduce this. We haven't been able to get it to crash on Trunk or Canary.

### sl...@gmail.com (2011-11-21)

Just tested on canary - 17.0.946.0 (110890). Still crashes - both repros.

### sl...@gmail.com (2011-11-21)

Please try this repro. Litle diferent stack but it looks related.

----- crash3.html -----
<pre>
    <textarea style="height: 500px;">x</textarea>
    <bdi>
    <object>x</object>
    few
    new
    lines
    </bdi>
    <bdi>

        <object>x</object>
    
    </bdi>    

    <select autofocus></select>
</pre>
-----------------------

(12d8.cc8): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=00f5f948 ebx=00f5d7f8 ecx=00f5fae0 edx=0013e404 esi=0013e4a8 edi=0013e430
eip=bf800000 esp=0013e3ec ebp=0013e440 iopl=0         nv up ei pl zr na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010246
bf800000 ??              ???

ExceptionAddress: bf800000
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000008
   Parameter[1]: bf800000
Attempt to execute non-executable address bf800000

ChildEBP RetAddr  
WARNING: Frame IP not in any known module. Following frames may be wrong.
0013e3e8 63126895 0xbf800000
0013e440 6312ac15 chrome_624a0000!WebCore::InlineBox::paint+0xb1
0013e4ac 63126f69 chrome_624a0000!WebCore::InlineFlowBox::paint+0x1d7
0013e4c8 6310af56 chrome_624a0000!WebCore::RootInlineBox::paint+0x17
0013e554 63100068 chrome_624a0000!WebCore::RenderLineBoxList::paint+0x216
0013e584 63100477 chrome_624a0000!WebCore::RenderBlock::paintContents+0x53
0013e5c0 630ff9f0 chrome_624a0000!WebCore::RenderBlock::paintObject+0xda
0013e600 631001c0 chrome_624a0000!WebCore::RenderBlock::paint+0xbd
0013e664 63100073 chrome_624a0000!WebCore::RenderBlock::paintChildren+0x147
0013e694 63100477 chrome_624a0000!WebCore::RenderBlock::paintContents+0x5e
0013e6d0 630ff9f0 chrome_624a0000!WebCore::RenderBlock::paintObject+0xda
0013e710 631001c0 chrome_624a0000!WebCore::RenderBlock::paint+0xbd
0013e774 63100073 chrome_624a0000!WebCore::RenderBlock::paintChildren+0x147
0013e7a4 63100477 chrome_624a0000!WebCore::RenderBlock::paintContents+0x5e
0013e7e0 630ff9f0 chrome_624a0000!WebCore::RenderBlock::paintObject+0xda
0013e820 630c4e60 chrome_624a0000!WebCore::RenderBlock::paint+0xbd
0013e9d8 630c508b chrome_624a0000!WebCore::RenderLayer::paintLayer+0x566
0013ea0c 630c4f5b chrome_624a0000!WebCore::RenderLayer::paintList+0x39
0013ebe0 630c46e7 chrome_624a0000!WebCore::RenderLayer::paintLayer+0x661
0013ec30 6314404d chrome_624a0000!WebCore::RenderLayer::paint+0x3f
0013ec70 6328c003 chrome_624a0000!WebCore::FrameView::paintContents+0x151
0013ecd0 62c61965 chrome_624a0000!WebCore::ScrollView::paint+0x1b4
0013ed20 62c61a04 chrome_624a0000!WebKit::WebFrameImpl::paintWithContext+0x6c
0013edd8 62c65d65 chrome_624a0000!WebKit::WebFrameImpl::paint+0x3e
0013ee18 62a6f9b1 chrome_624a0000!WebKit::WebViewImpl::paint+0xa3
0013eec8 62a7065a chrome_624a0000!RenderWidget::PaintRect+0x1e2
0013f0ec 62a70043 chrome_624a0000!RenderWidget::DoDeferredUpdate+0x5f9
0013f100 62a7001d chrome_624a0000!RenderWidget::DoDeferredUpdateAndSendInputAck+0x10
0013f124 625cd4f2 chrome_624a0000!RenderWidget::InvalidationCallback+0x92
0013f150 625cd59a chrome_624a0000!MessageLoop::RunTask+0xa3
[...]


### in...@chromium.org (2011-11-21)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=670002

Uploader: inferno@chromium.org [2011-11-21 23:08:10]

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x7f31f1f6d8b0
Crash State:
  - crash stack -
  WebCore::InlineFlowBox::computeOverAnnotationAdjustment
  WebCore::RootInlineBox::selectionTop
  - free stack -
  WebCore::RenderObjectChildList::destroyLeftoverChildren
  WebCore::RenderInline::willBeDestroyed
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=108984:109026

Minimized Testcase (0.21 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv9459911MBUbJtTJtHCYEiUeH-6r-MMRAIwxXYEhEqXhaCb-Y6kdPvpuk1OlLIAraKR4elztR6vFmlOExHjaJEAWW48SKqGTcIY8rH2hV1iz1kIE51llH5hQQgf6891Q23taKgF5L2xVmEax3yi3_Fnsachkqg
<script>
    function main(){
        window.document.designMode = 'on'
    }
    window.onload = main;
</script>

<summary>
    <bdi>
        <ruby>foo</ruby>
            <bdi dir="ltr">
                <embed>

### in...@chromium.org (2011-11-21)

Assigning to Ken since it looks to be the only webkit change relating to bidi in that regression range. https://trac.webkit.org/changeset/99462

### in...@chromium.org (2011-11-21)

[Empty comment from Monorail migration]

### ke...@chromium.org (2011-11-22)

I don't think it's my change, as I can repro after building with that fix reverted. I can still take this, but it will probably be a few days before I can get to it.

### in...@chromium.org (2011-11-22)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=72978

### sc...@gmail.com (2011-11-23)

Trunk regression => blocks release of M17 stable.

### ke...@chromium.org (2011-11-25)

Okay I get it now. This is another bug in the UBA which screws up line boxes. Inferno committed an earlier attempt at fixing https://bugs.webkit.org/show_bug.cgi?id=66015, which stopped the use-after-free condition in some scenarios but not all: http://trac.webkit.org/changeset/94001

Inferno's patch also prevented the above test case from manifesting as a use-after-free. However my fix for 66015 reverted his patch (I replaced the non-NULL-check-plus-delete with an ASSERT). That is why my patch shows as a regression: previously the lineboxes were still getting screwed up but the bad ones were getting deleted anyway.

Since we've seen that corrupted linebox trees can turn into UAF bugs in multiple ways, this bug probably affects beta and stable. We just don't have a test case to prove it right now.

UBA bugs suck and I'm not sure how long it will take me to fix this, but if I get it in time then I would advocate for the fix to be merged to M16.

### in...@chromium.org (2011-11-27)

Awesome Ken! i like your approach fixing the functional problem. What do you think of changing that assert back into a non-null-check-plus-delete so that we dont run into some variant of this problem, thereby causing a use after free. You can probably add this in your upstream patch. Also, do you think it is SecImpacts-Stable, Beta ? Because previously, it was just a functional bug and didnt cause a use after free.

### ke...@chromium.org (2011-11-27)

To answer both questions, I'm going based on the previous UBA bug we had where the delete resolved some of the test cases, but it was possible to construct other tests that generated corrupt lineboxes, didn't hit that code, and still resulted in use-after-free. This is likely to be similar, because the delete was fixing a downstream symptom of the bug.

I thought about changing the delete back. I am generally favorable of putting run-time checks for potential security issues where things should never be true, in addition to ASSERTs. But there are two reasons why I didn't do that here:
1. Last time I asked you about a similar situation, you told me that isn't done in WebKit for performance reasons :)
2. It is only really masking bugs in other areas of code, not resolving them. It potentially could turn a security bug into a non-security bug, but based on the above it's hard to be confident that it really happens.

### in...@chromium.org (2011-11-28)

http://trac.webkit.org/changeset/101272

### js...@chromium.org (2011-12-01)

[Empty comment from Monorail migration]

### sl...@gmail.com (2011-12-02)

crash3.html still crashes on windows beta 16.0.912.59 (112386).

### ke...@chromium.org (2011-12-02)

Thanks slaweck, I see this. I'm investigating whether this warrants creating a new bug or if it's a special case of the same bug that my fix somehow doesn't catch.

### sl...@gmail.com (2011-12-03)

Ken, please check this repro. Crashes on beta as well and it can be "special case of the same bug" :)

----- crash4.html -----
<script>
    setTimeout("crash()", 1000);

    function crash(){
        bdi = document.getElementById('bdi');
        document.adoptNode(bdi);
    }
</script>

<object></object>
<bdi id="bdi">
    <bdo>aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa</bdo>
    <ruby>bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb</ruby>
    <embed></embed>
    <dfn dir="ltr"></dfn>
</bdi>
-----------------------

(d08.10b4): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=0108e8b8 ebx=0108c674 ecx=0108e83c edx=59ca10d8 esi=0108ece4 edi=0108ecbc
eip=01068230 esp=003ff18c ebp=003ff1b4 iopl=0         nv up ei pl nz na po nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010202
01068230 e804cb5940      call    41604d39

ExceptionAddress: 01068230
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000008
   Parameter[1]: 01068230
Attempt to execute non-executable address 01068230

ChildEBP RetAddr  
WARNING: Frame IP not in any known module. Following frames may be wrong.
003ff188 5927fb4f 0x1068230
003ff1b4 5927b9e1 chrome_58640000!WebCore::InlineFlowBox::computeOverAnnotationAdjustment+0x6c
003ff1d8 5928c103 chrome_58640000!WebCore::RootInlineBox::selectionTop+0x32
003ff1e8 5928c28d chrome_58640000!WebCore::RenderReplaced::localSelectionRect+0x7f
003ff23c 59227214 chrome_58640000!WebCore::RenderReplaced::clippedOverflowRectForRepaint+0x57
003ff274 59249564 chrome_58640000!WebCore::RenderObject::repaint+0x49
003ff294 59225449 chrome_58640000!WebCore::RenderObjectChildList::removeChildNode+0x4b
003ff2b4 59228bab chrome_58640000!WebCore::RenderObject::removeChild+0x2a
003ff2c8 59230161 chrome_58640000!WebCore::RenderObject::willBeDestroyed+0xb1
003ff2d8 59235f97 chrome_58640000!WebCore::RenderBoxModelObject::willBeDestroyed+0x18
003ff2fc 5927941a chrome_58640000!WebCore::RenderBox::willBeDestroyed+0x8a
003ff304 5947ef23 chrome_58640000!WebCore::RenderWidget::destroy+0xb
003ff314 594899d1 chrome_58640000!WebCore::Node::detach+0x1b
003ff31c 59485f8d chrome_58640000!WebCore::Element::detach+0x2e
003ff328 594899d1 chrome_58640000!WebCore::ContainerNode::detach+0x13
003ff330 59485845 chrome_58640000!WebCore::Element::detach+0x2e
003ff338 594857d5 chrome_58640000!WebCore::ContainerNode::removeBetween+0x19
003ff368 59475174 chrome_58640000!WebCore::ContainerNode::removeChild+0xf2
003ff38c 5916f683 chrome_58640000!WebCore::Document::adoptNode+0x11c
003ff3c8 596e543f chrome_58640000!WebCore::DocumentInternal::adoptNodeCallback+0xac
003ff42c 596e5813 chrome_58640000!v8::internal::HandleApiCallHelper<0>+0x19f
003ff4e4 5968a625 chrome_58640000!v8::internal::Builtin_HandleApiCall+0x13
003ff51c 5968b05c chrome_58640000!v8::internal::Invoke+0x115
003ff554 59652731 chrome_58640000!v8::internal::Execution::Call+0x11c
003ff5b4 5936e5dd chrome_58640000!v8::Script::Run+0x181
003ff5fc 5936e4ac chrome_58640000!WebCore::V8Proxy::runScript+0xe5
003ff654 5931b029 chrome_58640000!WebCore::V8Proxy::evaluate+0x1b2
003ff69c 5931af7c chrome_58640000!WebCore::ScheduledAction::execute+0x91
003ff6b4 5936987d chrome_58640000!WebCore::ScheduledAction::execute+0x1e
003ff6e0 593f8686 chrome_58640000!WebCore::DOMTimer::fired+0xfe
003ff70c 5876d81a chrome_58640000!WebCore::ThreadTimers::sharedTimerFiredInternal+0x8e
003ff714 587667db chrome_58640000!base::subtle::TaskClosureAdapter::Run+0xb
003ff740 58766857 chrome_58640000!MessageLoop::RunTask+0x8a
[...]


### ke...@chromium.org (2011-12-06)

slaweck, crash4.html looks likely to be the same bug as crash3.html. crash3.html was spun off into its own bug - https://crbug.com/chromium/106200. I'm moving crash4 over there now but it can be spun off again if it turns out to be different.

Specifically: cluster-fuzz claims crash4.html is a duplicate of another test case (from our own fuzzing) which we think is the same as 106200.

### sc...@gmail.com (2011-12-10)

@slaweck: thanks for catching this! Looks like we were able to address at least some of the problem in time for Chrome 16. Hence a $1000 Chromium Security Reward for the parts covered by this bug.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2011-12-20)

Payment in system.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-06-13)

ClusterFuzz has detected this issue as fixed in range 111700:112063.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=670002

Uploader: inferno@chromium.org [2011-11-21 23:08:10]

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x7f31f1f6d8b0
Crash State:
  - crash stack -
  WebCore::InlineFlowBox::computeOverAnnotationAdjustment
  WebCore::RootInlineBox::selectionTop
  - free stack -
  WebCore::RenderObjectChildList::destroyLeftoverChildren
  WebCore::RenderInline::willBeDestroyed
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=108984:109026
Fixed: https://cluster-fuzz.appspot.com/revisions?range=111700:112063

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv9459911MBUbJtTJtHCYEiUeH-6r-MMRAIwxXYEhEqXhaCb-Y6kdPvpuk1OlLIAraKR4elztR6vFmlOExHjaJEAWW48SKqGTcIY8rH2hV1iz1kIE51llH5hQQgf6891Q23taKgF5L2xVmEax3yi3_Fnsachkqg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/104859?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051428)*

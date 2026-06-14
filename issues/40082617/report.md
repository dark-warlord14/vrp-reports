# Memory corruption in Counter Nodes.

| Field | Value |
|-------|-------|
| **Issue ID** | [40082617](https://issues.chromium.org/issues/40082617) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ku...@gmail.com |
| **Assignee** | ch...@gmail.com |
| **Created** | 2010-08-10 |
| **Bounty** | $500.00 |

## Description

see 1.htm

## Attachments

- deleted (application/octet-stream, 0 B)
- [bug51653.html](attachments/bug51653.html) (text/html; charset=us-ascii, 508 B)

## Timeline

### in...@chromium.org (2010-08-10)

It is a straight null deref. the reason i remember this is i worked with Justin on the counter related bugs and definitely remember this testname. it hits those same asserts and crashes with a null renderer. We do have a functional bug open on this in webkit - https://bugs.webkit.org/show_bug.cgi?id=41472.

### in...@chromium.org (2010-08-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-08-10)

I need to look more closely on this one. As per kuzzcc, this is exploitable.

Kuzzcc comments.
--------
(538.9f0): Access violation - code c0000005 (!!! second chance !!!)
eax=00000000 ebx=00730075 ecx=00730075 edx=00000000 esi=0033f270 edi=00000000
eip=6af9f068 esp=0033f228 ebp=0033f250 iopl=0         nv up ei pl zr na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246
chrome_6adb0000!WebCore::CounterNode::removeChild+0x6:
6af9f068 83611800        and     dword ptr [ecx+18h],0 ds:002b:0073008d=00000000
0:000> .exr -1
ExceptionAddress: 6af9f068 (chrome_6adb0000!WebCore::CounterNode::removeChild+0x00000006)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000001
   Parameter[1]: 0073008d
Attempt to write to address 0073008d


### in...@chromium.org (2010-08-10)

Code crashes in. m_lastchild object value is all bad showing clear signs of memory corruption. Needs to be analyzed more.

---------
CounterNode* CounterNode::lastDescendant() const
{
    CounterNode* last = m_lastChild;
    if (!last)
        return 0;

    while (CounterNode* lastChild = last->m_lastChild)
        last = lastChild;

WebCore::CounterNode::lastDescendant()  Line 73 + 0x3 bytes
WebCore::destroyCounterNodeWithoutMapRemoval(const WebCore::AtomicString & identifier={...}, WebCore::CounterNode * node=0x09168de0)  Line 343 + 0x8 bytes
WebCore::RenderCounter::destroyCounterNodes(WebCore::RenderObject * renderer=0x090f000c)  Line 375 + 0x15 bytes
WebCore::RenderObject::destroy()  Line 2149 + 0x9 bytes
WebCore::RenderBoxModelObject::destroy()  Line 221
WebCore::RenderBox::destroy()  Line 98
WebCore::RenderBlock::destroy()  Line 200
WebCore::Node::detach()  Line 1274 + 0x1d bytes
WebCore::ContainerNode::detach()  Line 648
WebCore::Element::detach()  Line 839
WebCore::ContainerNode::detach()  Line 645 + 0x12 bytes
WebCore::Element::detach()  Line 839
WebCore::ContainerNode::detach()  Line 645 + 0x12 bytes
WebCore::Element::detach()  Line 839
WebCore::ContainerNode::detach()  Line 645 + 0x12 bytes
WebCore::Document::detach()  Line 1691
WebCore::Frame::setView(WTF::PassRefPtr<WebCore::FrameView> view=NULL)  Line 239 + 0x23 bytes
WebKit::WebFrameImpl::createFrameView()  Line 1853
WebKit::FrameLoaderClientImpl::makeDocumentView()  Line 213

### in...@chromium.org (2010-08-10)

Filed WebKit Bug - https://bugs.webkit.org/show_bug.cgi?id=43812

### in...@chromium.org (2010-08-12)

Reduced testcase. Did take a couple of hours since crash was not predictable, but with this one, it does hit the right place in 1 or 2 tries max (after clicking through the asserts).

### sc...@gmail.com (2010-08-13)

@kuzzcc: congratulations! We'd like to provisionally offer you a $500 reward for your help in reporting this bug.

Please continue to keep the details confidential until we release the fix in a patch. Also, once we've released the fix, please be considerate that other WebKit-based products might be releasing fix on different timelines.

In the future, the following things might help towards a "high quality report" and the higher $1000 reward:
- Remove unrelated HTML constructs from the repro.
- Make the repro fire the crash as reliably as possible.
- Always include stack traces, assembly instruction and register dumps.
- Explain why it is a security bug (e.g. "Attempt to write to address 0073008d")
- Avoid duplicate bugs where possible.

### sc...@gmail.com (2010-08-13)

Oh, PLEASE PLEASE PLEASE use a detailed description for the bug "Summary". e.g. "Crash / memory corruption in counter node handling" or "Crash / memory corruption in <rt> handling".
The stack traces may help here, e.g. even this would be a good summary: "Crash with corrupt ecx register in chrome_6adb0000!WebCore::CounterNode::removeChild"

### sc...@gmail.com (2010-08-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-08-25)

Fixed in WK r66052. Also merged to 472.

### bu...@gmail.com (2010-08-25)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=57412 

------------------------------------------------------------------------
r57412 | inferno@chromium.org | 2010-08-25 16:16:05 -0700 (Wed, 25 Aug 2010) | 24 lines
Changed paths:
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/fast/css/counters/counter-traverse-object-crash-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/fast/css/counters/counter-traverse-object-crash.html
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/472/WebCore/rendering/RenderCounter.cpp?r1=57412&r2=57411

Merge 66052 - 2010-08-25  Cris Neckar  <cdn@chromium.org>

        Reviewed by Darin Adler.

        Added abort condition for RenderCounters when traversing a detached render tree.
        https://bugs.webkit.org/show_bug.cgi?id=43812

        Test: fast/css/counters/counter-traverse-object-crash.html

        * rendering/RenderCounter.cpp:
        (WebCore::findPlaceForCounter):
2010-08-25  Cris Neckar  <cdn@chromium.org>

        Reviewed by Darin Adler.

        Assertion failure in RenderCounter when traversing a detached render trees.
        https://bugs.webkit.org/show_bug.cgi?id=43812

        * fast/css/counters/counter-traverse-object-crash-expected.txt: Added.
        * fast/css/counters/counter-traverse-object-crash.html: Added.

BUG=51653

Review URL: http://codereview.chromium.org/3189023
------------------------------------------------------------------------


### sc...@gmail.com (2010-09-02)

Fix is live to users: http://googlechromereleases.blogspot.com/2010/09/stable-and-beta-channel-updates.html
And payment is in the electronic system :)

### ku...@gmail.com (2010-09-03)

thanks :)

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/51653?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/51661]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082617)*

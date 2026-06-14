# ASSERTION FAILED: node->parentNode(), Heap-use-after-free in WebCore::RenderBox::exclusionShapeOutsideInfo

| Field | Value |
|-------|-------|
| **Issue ID** | [40077603](https://issues.chromium.org/issues/40077603) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2013-05-25 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in isBox WebKit/Source/core/rendering/RenderObject.h:1069

**VERSION**  

Chrome Version: dev  

Operating System: ubuntu 64bit

**REPRODUCTION CASE**

<html>
<head>
<style>
#el1 {
margin: 1px;
}
#el1:nth-last-child(2n) {
display: table-header-group;
}
#el2:first-child {
display: inline-table;
}
#el2:nth-last-child(2n) {
-webkit-appearance:discrete-capacity-level-indicator;
}
#el2 {
display: table-header-group;
}
#el4 {
visibility: collapse;
}
#el5:nth-last-child(2n) {
-webkit-appearance:discrete-capacity-level-indicator;
}
#el5 {
display: table-header-group;
}
#el6 {
-webkit-border-after: solid;
float: left;
}
#el6:last-of-type {
content: "B";
}
#el7::before {
content: "A";
}
</style>
<script>
onload = function() {
el0=document.createElement('div')
document.body.appendChild(el0)
el0.appendChild(document.createElement('li'))
el1=document.createElement('canvas')
el1.setAttribute('id','el1')
document.body.appendChild(el1)
el2=document.createElement('canvas')
el2.setAttribute('id','el2')
document.body.appendChild(el2)
el3=document.createElement('meter')
document.body.appendChild(el3)
el4=document.createElement('div')
el4.setAttribute('id','el4')
document.body.appendChild(el4)
el5=document.createElement('canvas')
el5.setAttribute('id','el5')
document.body.appendChild(el5)
el5.appendChild(document.createTextNode('A'))
el6=document.createElement('span')
el6.setAttribute('id','el6')
document.body.appendChild(el6)
document.body.appendChild(document.createElement('span'))
el7=document.createElement('div')
el7.setAttribute('id','el7')
document.body.appendChild(el7)
document.designMode='on'
window.getSelection().setBaseAndExtent(el3, 1, el3, 1)
document.execCommand('InsertLineBreak')
document.execCommand('selectall')
document.execCommand('strikethrough')
document.execCommand('FormatBlock', false, '<'+'pre>')
document.execCommand('Undo')
document.body.offsetTop
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==27122==ERROR: AddressSanitizer: heap-use-after-free on address 0x60f00001b820 at pc 0x7f91df1b2381 bp 0x7fffd9d3ea70 sp 0x7fffd9d3ea68  

READ of size 4 at 0x60f00001b820 thread T0 (asan-release)  

#0 0x7f91df1b2380 in isBox /b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderObject.h:1069:0  

#1 0x7f91df1b2380 in isBox /b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderObject.h:533:0  

#2 0x7f91df1b2380 in isFloatingWithShapeOutside /b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderObject.h:835:0

0x60f00001b820 is located 48 bytes inside of 176-byte region [0x60f00001b7f0,0x60f00001b8a0)  

freed by thread T0 (asan-release) here:  

#0 0x7f91d9d1b8e2 in free ??:0  

#1 0x7f91e0b88a81 in WebCore::Node::detach() /b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.cpp:1127:0  

#2 0x7f91e0b2de7f in WebCore::Element::detach() /b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1318:0  

#3 0x7f91e0b2f2ac in reattach /b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.h:864:0  

#4 0x7f91e0b2f2ac in WebCore::Element::recalcStyle(WebCore::Node::StyleChange)

## Attachments

- [48176.txt](attachments/48176.txt) (text/plain; charset=us-ascii, 20.0 KB)
- [48176.html](attachments/48176.html) (text/html; charset=us-ascii, 2.3 KB)

## Timeline

### in...@chromium.org (2013-05-26)

Please use llvm-symbolizer in future, so that we can see namespaces quickly. it really helps in triage.

This bug was hit by BJ's fuzzer on June 9, https://cluster-fuzz.appspot.com/testcase?key=182314783,but it was one-time crasher, so never filed. So, this bug is still eligible for reward i think, adding tags.

### in...@chromium.org (2013-05-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=187424218

Uploader: aarya@google.com

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x6110000e5a70
Crash State:
  - crash stack -
  WebCore::RenderBox::exclusionShapeOutsideInfo
  WebCore::RenderBlock::logicalLeftOffsetForLine
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=200103:200144

Minimized Testcase (2.15 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96aRC2Hu4PSDDH0jTiZHR18lpehdXUzHp9UcCpLGBR58NsC9PYzWAjuvDwBX2gU5__y-P4hBneFZvXoMD3evw4p3DLP1G9ylU140IAvTbYy3Gako5LCrN7ecT8_BcQM0eNdtIC_CcFZOWLqwoh2x6YOzUVSfg

### in...@chromium.org (2013-05-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=186297097

Fuzzer: Bj_broddelwerk

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60f00001beb0
Crash State:
  - crash stack -
  WebCore::RenderBox::exclusionShapeOutsideInfo
  WebCore::RenderBlock::logicalRightOffsetForLine
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=186293:186370

Minimized Testcase (3.67 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95nCrCfhEMlmVcqd-ffTNWsjWKGAXtHcUlAP5ShgtVnxVwEwX73seLe6Jz0wYFMScePhlJFyRjG9fSCaMddTdb6pTtvf0k0z9pp1-51BKXW0Xn7KAi4-T-7SRJCWVipH74h9m2YJ2j2vDNp2HIK1tfxGwLejg

### in...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-28)

Ken, can you please take a look or help with an owner.

### ke...@chromium.org (2013-05-28)

I'll take a look.

### jl...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-29)

just for fun, while debugging, this is yet another floats crap. if you add this code to end in removeFloatingOrPositionedChildFromBlockLists, you will see this assert hitting. 

        for (RenderObject* curr = parent(); curr && !curr->isRenderView(); curr = curr->previousInPreOrder()) {
            if (curr->isRenderBlock()) {
                ASSERT(!toRenderBlock(curr)->containsFloat(this));
            }
        }

There is bailout code in

void RenderBlock::markAllDescendantsWithFloatsForLayout(RenderBox* floatToRemove, bool inLayout)
{
    if (!everHadLayout())
        return;

So, it never gets removed. Now, we have new code moveAllChildrenIncludingFloatsTo that will move this removed float to another renderblock.

### in...@chromium.org (2013-05-29)

void RenderBlock::removeChild(RenderObject* oldChild)
{
..........
        } else {
            // Take all the children out of the |next| block and put them in
            // the |prev| block.
            nextBlock->moveAllChildrenIncludingFloatsTo(prevBlock, nextBlock->hasLayer() || prevBlock->hasLayer());
            
            // Delete the now-empty block's lines and nuke it.
            nextBlock->deleteLineBoxTree();
            nextBlock->destroy();
            next = 0;
        }
    }

There is a little confusion on what the right fix would be - 1) whether prevBlock should be marked for layout. in RenderBlock::removeChild or 2) we should not move floats in situations where everHadLayout() is false.

Kenrb@, Betravis@ - any thoughts ? 

### ke...@chromium.org (2013-05-29)

I have just started looking at this, and I'm not clear on what is happening yet.

How did the floating object list get populated if the RenderBlock has never had layout?

### in...@chromium.org (2013-05-29)

That looks to be again because of moveAllChildrenIncludingFloatsTo call, it can move it to a renderblock without marking that block for layout. 

When the use-after-free happens, that block is still marked as needing layout. so it happened to call that destroyed float before that block got a chance to layout.

### in...@chromium.org (2013-05-29)

Solution 1 does not work since prevblock does not get chance to layout before the crash happens. Solution 2 works.

I will let your independent thoughts chime in on.

### be...@gmail.com (2013-05-29)

The only different thing moveAllChildrenIncludingFloats does from moveAllChildren is that it copies the parent's floating object list to the destination block. As far as I understand it, I have the same question as kenrb@ : how did nextBlock get a floating objects list if it never had layout? Maybe the associated question is: are you saying that you don't move the floating objects list if nextBlock never had layout or if prevBlock never had layout?

### in...@chromium.org (2013-05-29)

Here is the sequence of events that happen

1. moveAllChildrenIncludingFloats moves children from nextBlock to prevBlock. nextBlock (lets say A1) had layout, has the floats, prevBlock never had layout. Now prevBlock (lets say A2) contains floats and its everHadLayout is false.
2. removeFloatingOrPositionedChildFromBlockLists is called on a float that is getting removed. Since A2 never got layout, the float is not removed from its list.
3. Float is destroyed.
4. Later moveAllChildrenIncludingFloats is again called on A2 [everHadLayout is false], moving to its prevBlock (lets say A3) [everHadLayout is true, but needsLayout is true].
5. We try to access the float from A3 and crash.

I think the bug is point 1), since removeFloatingOrPositionedChildFromBlockLists fails and assumes that everHadLayout false meaning it does not have floats. I think we should not move floats if prevBlock never had layout. WDYT ? 

### be...@gmail.com (2013-05-30)

That reasoning makes sense to me, especially since this bug showed up after we added the new code. Also, I'm happy to do the WebKIt port of any fix for this and run it by Hyatt.

### ke...@chromium.org (2013-05-30)

Interesting thing: I was having trouble seeing this behavior, until I realized that I was working from an old sync that didn't yet have the the breaking change (so moveAllChildrenIncludingFloats() doesn't exist yet)... but I was still seeing a use-after-free from the test case in https://crbug.com/chromium/244036#c5. There are probably two separate bugs on this thread.

It seemed really weird to me that we are populating the floating object list outside of layout, but I get it now after reading the bug associated with the fix that introduced this problem. It appears to have been the least bad choice available.

Obviously that patch breaks the assumption that a RenderBlock will not have a floating object list if it has not had layout, so the everHadLayout() optimization has to be removed. Hopefully this is the only place where we assume that. (And hopefully that optimization isn't particularly important!) :)

I can post a simple patch but the test case will need a bit of work to get a reasonable layout test out of it. I'll also verify shortly that there are in fact two separate bugs here.

### be...@gmail.com (2013-05-30)

The test case in #5 still reproduces on an old build, but the original test case doesn't?

I'm wary of removing the everHadLayout() optimization (I know at least that a fix like that is very unlikely to land in WebKit). I'd strongly argue for fix #2 that inferno@ set forth, as I'm pretty sure that in the cases for the bug that introduced moveAllChildrenIncludingFloats(), prevBlock had layout before.

### ke...@chromium.org (2013-05-30)

Doesn't that re-introduce the original bug in https://crbug.com/chromium/230907, where we can cause a condition where a float is not in its parent's floating object list but in floating object lists of siblings?

### ke...@chromium.org (2013-05-30)

inferno suggested offline that we change the bail-out condition to:
if (!everHadLayout() && !containsFloats())
    return;

I'll try this out.

### be...@gmail.com (2013-05-30)

I'm not sure if it does, since when fixing https://crbug.com/chromium/230907, I did not check to see if prevBlock everHadLayout. However, from what I saw when I was debugging, I believe all of the cases did have a prevBlock that had layout before, it just didn't have the floats in it because they didn't overhang into that block. So I believe that it should be OK, but it definitely would be worth testing.

### be...@gmail.com (2013-05-30)

Changing the condition to check for floats as well as layout sounds like it would be good from a performance standpoint. I'm definitely interested in hearing how that goes.

### in...@chromium.org (2013-05-31)

Other than the fix [which Ken is working on], we should add asserts to help in debugging in the future. https://codereview.chromium.org/16255006/

### ke...@chromium.org (2013-05-31)

I've moved the CF report on c#5 to a new bug, https://crbug.com/chromium/245727.

### be...@gmail.com (2013-05-31)

Can you cc me on https://crbug.com/chromium/245727? I'd like to port the fix for that to WebKit when it happens. Thanks.

### in...@chromium.org (2013-05-31)

done!

### ke...@chromium.org (2013-06-01)

Patch for review https://codereview.chromium.org/15736029/

### ke...@chromium.org (2013-06-03)

Committed https://src.chromium.org/viewvc/blink?revision=151610&view=revision


### cl...@chromium.org (2013-06-04)

ClusterFuzz has detected this issue as fixed in range 203701:203787.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=187424218

Uploader: aarya@google.com

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x6110000e5a70
Crash State:
  - crash stack -
  WebCore::RenderBox::exclusionShapeOutsideInfo
  WebCore::RenderBlock::logicalLeftOffsetForLine
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=200103:200144
Fixed: https://cluster-fuzz.appspot.com/revisions?range=203701:203787

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96aRC2Hu4PSDDH0jTiZHR18lpehdXUzHp9UcCpLGBR58NsC9PYzWAjuvDwBX2gU5__y-P4hBneFZvXoMD3evw4p3DLP1G9ylU140IAvTbYy3Gako5LCrN7ecT8_BcQM0eNdtIC_CcFZOWLqwoh2x6YOzUVSfg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2013-06-07)

ClusterFuzz seems sure this is a M29 regression.
If anyone disagrees, let me know :-)

### sc...@gmail.com (2013-08-11)

$1000, etc.!

### sc...@gmail.com (2013-08-11)

(A note on reward -- we're rewarding @miaubiz even though this was also caught by an internal fuzzer, because the internal fuzzer emitted an awful repro)

### pa...@chromium.org (2013-08-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

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

This issue was migrated from crbug.com/chromium/244036?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077603)*

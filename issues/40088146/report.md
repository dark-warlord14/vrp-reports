# Floats not cleared to logical height wraps.

| Field | Value |
|-------|-------|
| **Issue ID** | [40088146](https://issues.chromium.org/issues/40088146) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-02-19 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

stale pointer RIP goes to random address

**VERSION**  

Google Chrome 9.0.597.98 (Official Build 74359)  

Chromium 11.0.673.0 (Developer Build 75059) Ubuntu 10.10  

on Linux 2.6.35-27-generic #47-Ubuntu SMP Fri Feb 11 22:52:49 UTC 2011 x86\_64

Google Chrome 9.0.597.102 (official build 74604)  

OSX Snow Leopard 10.6.6

**REPRODUCTION CASE**

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

#0 0x00007ffffa1c59c0 in ?? ()  

#1 0x00007ffff67e8699 in WebCore::RenderBlock::insertFloatingObject at third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:3073  

#2 0x00007ffff68029ae in WebCore::RenderBlock::layoutInlineChildren at third\_party/WebKit/Source/WebCore/rendering/RenderBlockLineLayout.cpp:870

0x00007ffff67e8693 <+195>: callq \*0x140(%rax)

## Attachments

- [insertfloating.html](attachments/insertfloating.html) (text/html; charset=us-ascii, 819 B)
- [valgrind_73526.txt](attachments/valgrind_73526.txt) (text/x-pascal; charset=us-ascii, 12.6 KB)
- [b3.html](attachments/b3.html) (text/html; charset=us-ascii, 4.0 KB)
- [2.html](attachments/2.html) (text/html; charset=us-ascii, 741 B)
- [b2.html](attachments/b2.html) (text/html; charset=us-ascii, 4.0 KB)
- [b1.html](attachments/b1.html) (text/html; charset=us-ascii, 4.0 KB)
- [3.html](attachments/3.html) (application/octet-stream; charset=binary, 728 B)
- [1.html](attachments/1.html) (text/html; charset=us-ascii, 722 B)
- [4.html](attachments/4.html) (text/html; charset=us-ascii, 733 B)
- [null140.html](attachments/null140.html) (text/plain; charset=us-ascii, 335 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### mi...@gmail.com (2011-02-19)

valgrind log

==1379==  Address 0x3647b4ab is 91 bytes inside a block of size 96 free'd
==1379==    at 0x4C29146: free (vg_replace_malloc.c:913)
==1379==    by 0x1CE8A0F: WebCore::RenderObject::~RenderObject() (RefCounted.h:136)

==1379== Process terminating with default action of signal 4 (SIGILL)
==1379==  Illegal opcode at address 0x35A98344
==1379==    at 0x35A98344: ???
==1379==    by 0xF772777: ???
==1379==    by 0x1C70698: WebCore::RenderBlock::insertFloatingObject(WebCore::RenderBox*) (RenderBlock.cpp:3073)


### in...@chromium.org (2011-02-19)

Does not crash on both windows trunk (webkit 78997) and linux trunk (webkit 78540). Seeing the repro, this is pretty obvious dup of http://trac.webkit.org/changeset/77565

### mi...@gmail.com (2011-02-19)

I thought it looked familiar :D

But this is reproducible for me on trunk (webkit 79006), and the repros from the other bug do nothing.

This crash has something to do with the -webkit-columns CSS directive being present in the repro.

I'll attach some more repros.  The b?.html segfault at RIP and the numbered ones nullptr at 140.



### in...@chromium.org (2011-02-19)

Ok, i will recheck again with your new repros. Reopening bug.

### mi...@gmail.com (2011-02-20)

here's a smaller one for nullptr 0x140..  the instructions is callq %rax+0x140

can repro on ubuntu chromium daily version on maverick 64bit:
Chromium	11.0.678.0 (Developer Build 75511) Ubuntu 10.10
WebKit	534.21 (trunk@79111)

### in...@chromium.org (2011-02-21)

miaubiz, you are awesome!! this new repro works. and this is not a dup.

the logical height is wrapping up at 
setLogicalHeight(logicalHeight() + logicalHeightForChild(child)); in RenderBlock.cpp

and hence we are not able to clear the linebox in markLinesDirtyInBlockRange. note that logical height wrap leads to negative block logical height leading to linebox not cleared -> stale linebox -> use after free. my last two fixes in this area 

these signed int are really bad, they are all over the place in webkit. and atleast negative logical height has a meaning, i am still checking if we can fix this more generically using block logical height for which negative value is probably invalid.


### in...@chromium.org (2011-02-23)

taking a look.

### in...@chromium.org (2011-02-23)

Fixed in http://trac.webkit.org/changeset/79462

### mi...@gmail.com (2011-02-23)

@inferno <3 thank you.

I can get RIP to go to bad places with the attached repros with r79479.  I'm using webkit master git branch, because gclient branch with lkgr isn't up to date yet.

not sure if it's more of the same bug or should be filed as a different one

Chromium	11.0.682.0 (Developer Build f504cfe)
WebKit	534.22 (git@58b0446) == r79479

==12302==  Address 0xf7d44ab is 91 bytes inside a block of size 96 free'd
==12302==    at 0x4C29146: free (vg_replace_malloc.c:913)
==12302==    by 0x1E3ECFF: WebCore::RenderObject::~RenderObject() (in /home/clooney/chromium/src/out/Release/chrome)
==12302==    by 0x1DF9156: WebCore::RenderEmbeddedObject::~RenderEmbeddedObject() (in /home/clooney/chromium/src/out/Release/chrome)
==12302==    by 0x1E3971A: WebCore::RenderObject::arenaDelete(WebCore::RenderArena*, void*) (in /home/clooney/chromium/src/out/Release/chrome)
==12302== 
==12302== Jump to the invalid address stated on the next line
==12302==    at 0x0: ???
==12302==    by 0x1DC5968: WebCore::RenderBlock::insertFloatingObject(WebCore::RenderBox*) (in /home/clooney/chromium/src/out/Release/chrome)
==12302==    by 0x1DE008D: WebCore::RenderBlock::layoutInlineChildren(bool, int&, int&) (in /home/clooney/chromium/src/out/Release/chrome)



### in...@chromium.org (2011-02-23)

@miaubiz: can you please file a new bug with these repros.

### mi...@gmail.com (2011-02-24)

[Comment Deleted]

### in...@chromium.org (2011-02-24)

@Miaubiz: thank you very much for your continued patience and testing on trunk build. Please try to include all new repros concerning this case of overflow in the new bug. (dont worry if those repros are big, we want to make sure we have them all before I try another fix to cover rest of scenarios).

### mi...@gmail.com (2011-02-24)

@inferno: https://crbug.com/chromium/73962

### sc...@gmail.com (2011-03-17)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-18)

@miaubiz: thanks for all your high-quality help as usual :)
We'll reward you $1000 for this bug and consider the other bug for additional reward once we've fixed it and verified all the different repros.

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

### sc...@gmail.com (2011-03-19)

Probably no more M10 patches. Going to let this fix roll into M11. I love having regular release trains :D

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-04-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-04-22)

https://bugs.webkit.org/show_bug.cgi?id=54995

### sc...@gmail.com (2011-05-04)

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

This issue was migrated from crbug.com/chromium/73526?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088146)*

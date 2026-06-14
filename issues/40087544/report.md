# stale pointer in WebCore::RenderBlock::insertFloatingObject

| Field | Value |
|-------|-------|
| **Issue ID** | [40087544](https://issues.chromium.org/issues/40087544) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-02-03 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

stale pointer

**VERSION**  

11.0.658.0 (Developer Build 73582) Ubuntu 10.10 + 2.6.35-25-generic x86\_64  

9.0.597.84 Official Build 72991 on OSX Snow Leopard 10.6  

9.0.597.84 Official Build 72991 on Windows 7 32bit  

9.0.597.84 Official Build 72991 on Windows XP 32bit

**REPRODUCTION CASE**

<textarea rows="100000000"></textarea>
<textarea style="width: 100%" rows="100000000"></textarea>

<object data="a" align="right"></object>

this segfaults at 140.. but a more complex case which I'll attach will have jump to random memory.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: sad tab  

Crash State:  

#0 0x0000000000000000 in ?? ()  

#1 0x00007ffff680e859 in WebCore::RenderBlock::insertFloatingObject (this=0x7ffffa1cd560, o=0x7ffff9230120) at third\_party/WebKit/Source/WebCore/rendering/RenderBlock.cpp:3074  

#2 0x00007ffff682894e in WebCore::RenderBlock::layoutInlineChildren (this=0x7ffffa1cd560, relayoutChildren=<value optimized out>, repaintLogicalTop=<value optimized out>,  

repaintLogicalBottom=<value optimized out>) at third\_party/WebKit/Source/WebCore/rendering/RenderBlockLineLayout.cpp:869

## Attachments

- [71855_complicated.html](attachments/71855_complicated.html) (text/plain; charset=us-ascii, 1.5 KB)
- [71855_minimal.html](attachments/71855_minimal.html) (text/plain; charset=us-ascii, 139 B)
- [71855_valgrind.txt](attachments/71855_valgrind.txt) (text/plain; charset=us-ascii, 9.4 KB)
- [71855_gdb.txt](attachments/71855_gdb.txt) (application/x-elc; charset=us-ascii, 23.4 KB)

## Timeline

### mi...@gmail.com (2011-02-03)

the complicated one has just more of the same, to entice the browser to put some random crap in the stale pointer

### mi...@gmail.com (2011-02-03)

valgrind log..

==24821==  Address 0xf76f02b is 91 bytes inside a block of size 96 free'd
==24821==    at 0x4C28EA6: free (vg_replace_malloc.c:913)


### mi...@gmail.com (2011-02-03)

gdb log

### in...@chromium.org (2011-02-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-02-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-02-04)

Fixed in http://trac.webkit.org/changeset/77565

### in...@chromium.org (2011-02-09)

qt build fix in http://trac.webkit.org/changeset/77573. still lets merge it too.


### in...@chromium.org (2011-02-09)

merged to m10 in r78130, 78131

merged to m9 in r78133.

### sc...@gmail.com (2011-02-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-02-13)

@miaubiz: another nice bug and another provisional $1000 Chromium Security Reward :)

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

### in...@chromium.org (2011-02-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-02-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-02-26)

https://bugs.webkit.org/show_bug.cgi?id=53729

### sc...@gmail.com (2011-03-04)

Invoice finalized; payment is in e-payment system.

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

This issue was migrated from crbug.com/chromium/71855?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087544)*

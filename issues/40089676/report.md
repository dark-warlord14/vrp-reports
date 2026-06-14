# invalid access with bad html

| Field | Value |
|-------|-------|
| **Issue ID** | [40089676](https://issues.chromium.org/issues/40089676) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-04-08 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. Please use a different**  

**template for other types of bug reports.**

**Please see the following link for instructions on filing security bugs:**  

**<http://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

Chrome Version: all  

Operating System: all

**REPRODUCTION CASE**  

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

(gdb) x/i $rip  

=> 0x7ffff66217ea <WebCore::RenderBlock::createLineBoxes(WebCore::RenderObject\*, bool, WebCore::InlineBox\*)+106>:  

testb $0x2,0x34(%rax)  

(gdb) p/x $rax  

$1 = 0x800000008

## Attachments

- [12.html](attachments/12.html) (text/plain; charset=us-ascii, 386 B)
- [crashlog.txt](attachments/crashlog.txt) (text/plain; charset=us-ascii, 39.7 KB)
- [vg78841.txt](attachments/vg78841.txt) (text/plain; charset=us-ascii, 4.1 KB)
- [8.html](attachments/8.html) (text/plain; charset=us-ascii, 303 B)
- [segfault.html](attachments/segfault.html) (text/plain; charset=us-ascii, 262 B)
- [null.html](attachments/null.html) (text/plain; charset=us-ascii, 260 B)
- [gpf-write2.html](attachments/gpf-write2.html) (text/plain; charset=us-ascii, 329 B)
- [otherseg2.html](attachments/otherseg2.html) (text/plain; charset=us-ascii, 559 B)
- [gpf-write.html](attachments/gpf-write.html) (text/plain; charset=us-ascii, 263 B)
- [otherseg.html](attachments/otherseg.html) (text/plain; charset=us-ascii, 352 B)
- [78841-rip.html](attachments/78841-rip.html) (text/plain; charset=us-ascii, 569 B)
- [78841-use-after-free.html](attachments/78841-use-after-free.html) (text/plain; charset=us-ascii, 561 B)
- [78841-rip-vg.txt](attachments/78841-rip-vg.txt) (text/plain; charset=us-ascii, 5.2 KB)
- [78841-use-after-free-vg.txt](attachments/78841-use-after-free-vg.txt) (text/plain; charset=us-ascii, 8.0 KB)

## Timeline

### mi...@gmail.com (2011-04-08)

osx crash wrangler log

exception=EXC_BAD_ACCESS:signal=11:is_exploitable=yes:instruction_disassembly=movl      %esi,CONSTANT(%eax):instruction_address=0x0000000001d92280:access_type=write:access_address=0x000000008642997c:


### mi...@gmail.com (2011-04-08)

vg log



### mi...@gmail.com (2011-04-09)

related nullptr at 0x148 or 0x140

WebCore::RenderBlock::insertFloatingObject(WebCore::RenderBox*) (RenderBlock.cpp:3125)


### mi...@gmail.com (2011-04-09)

here's some more simplified repros.  there are 3 distinct places it can crash.

beginning from the attached null.html, which nullptr's at 0x148,
if I add a character at the end of the file, it will segfault as in the original repro, it is possible to control RAX to some degree, and it seems deterministic as to where it will try to write.

if I add an empty line and then a character it will GPF, with rax set to the value of some string. this is deterministic, and it's possible to control to some degree rdi which is the source for rax


### in...@chromium.org (2011-04-10)

Another awesomeness from miaubiz. Also affects m10 stable, so not a regression.

Oh! i hate the <img> tag now. Note that one testcase might be different from the other issue. Without looking further i cannot tell.

This hits our usual bad cast assert in RenderBlock::createLineBoxes, but problem is somewhere else.

### ch...@gmail.com (2011-04-20)

inferno is 94.3287% sure that this is the same as http://crbug.com/72832 so I am linking for clarity.

### mi...@gmail.com (2011-05-05)

here's another one that has RIP going to bad places, also says use-after-free in vg.



### mi...@gmail.com (2011-05-05)

vg logs

### in...@chromium.org (2011-05-09)

filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=60307

### in...@chromium.org (2011-05-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-05-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-05-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-05-26)

Mass update to M12.

### in...@chromium.org (2011-06-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-21)

[Empty comment from Monorail migration]

### mi...@gmail.com (2011-06-28)

do you know if it's one bug or many? do you need more stack traces?

### in...@chromium.org (2011-06-29)

http://trac.webkit.org/changeset/90068


### sc...@gmail.com (2011-06-30)

Merged to M13: http://trac.webkit.org/changeset/90171

### sc...@gmail.com (2011-07-20)

@miaubiz: congrats! As you might imagine, your fine efforts on this bug qualify you for a $1000 Chromium Security Reward.

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

### sc...@gmail.com (2011-07-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-09)

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

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/78841?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/82354, crbug.com/chromium/86852]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089676)*

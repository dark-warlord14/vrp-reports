# [LangFuzz] CHECK(fixed_size + height_in_bytes == input_frame_size) failed or crash with invalid read

| Field | Value |
|-------|-------|
| **Issue ID** | [40056431](https://issues.chromium.org/issues/40056431) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2012-04-09 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The JavaScript code below crashes Chromium 19.0.1084.15 dev and d8 shell (trunk revision 11244) on heap with an invalid read from address 0xdeadbeec.

In a debug build, it causes the following assertion:

# 

# Fatal error in src/x64/deoptimizer-x64.cc, line 246

# CHECK(fixed\_size + height\_in\_bytes == input\_frame\_size) failed

# 

**VERSION**  

Chrome Version: 19.0.1084.15 dev  

Operating System: Ubuntu 11.10

**REPRODUCTION CASE**  

while(1==1) eval("print", (Math - 0.5) << 2);

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

Program received signal SIGSEGV, Segmentation fault.  

0x00001f45e7e34282 in ?? ()  

(gdb) bt 8  

#0 0x00001f45e7e34282 in ?? ()  

#1 0x00001f45e7e3447a in ?? ()  

#2 0x0000000000000000 in ?? ()  

(gdb) x /i $pc  

=> 0x1f45e7e34282: mov -0x1(%rdi),%rcx  

(gdb) info reg rdi rcx  

rdi 0xbeeddead 3203260077  

rcx 0x1f45e7e34466 34385103635558  

(gdb)

## Timeline

### pa...@google.com (2012-04-09)

Provisionally assigning to vegorov because the ASSERT is his.

### ve...@chromium.org (2012-04-10)

Strictly speaking assert is not mine, but I'll take care of this.

### ve...@chromium.org (2012-04-10)

Fixed by r11256. Might potentially cause dereference of a zap value 0xbeeddead (or different combinations of it's hi/lo 16bit parts)

### in...@chromium.org (2012-04-10)

is this a recent regression, if not, we need to merge this to m18, m19. Also, please help to set the Milestone tag on this.

### ve...@chromium.org (2012-04-10)

m18 (V8 3.8) is not affected.
m19 (V8 3.9) is affected, I'll merge the fix.

### in...@chromium.org (2012-04-10)

Great! thanks.

### de...@googlemail.com (2012-04-10)

Note that I reproduced this on 64 bit where 0xbeeddead might be a perfectly valid, allocated address (compared to 32 bit where this is likely to be a safe crash).

### sc...@gmail.com (2012-04-10)

I'd say the other way around: extremely unlikely to be mapped on our 64-bit platform (Linux) but a spray can easily ensure it's allocated on 32-bit Linux.

### de...@googlemail.com (2012-04-10)

That's interesting :) I should think about that again, I surely got something wrong when I thought about this the first time.

### ve...@chromium.org (2012-04-11)

Merged to V8 3.9: r11258, 3.9.24.8

### sc...@gmail.com (2012-04-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-04)

Interesting bug. Might plausibly be useful as an infoleak, i.e. we cannot discount this possibility. Hence:
$500

### sc...@gmail.com (2012-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Updating status to Fixed on security bugs which were fixed when m19 went to stable.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

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

### sh...@chromium.org (2016-06-22)

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

This issue was migrated from crbug.com/chromium/122681?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056431)*

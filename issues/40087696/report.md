# use after free in WebCore::RenderCounter::destroyCounterNode

| Field | Value |
|-------|-------|
| **Issue ID** | [40087696](https://issues.chromium.org/issues/40087696) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2011-02-08 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

segfault with bad html

this is a variation on the file:  

chromium/src/third\_party/WebKit/LayoutTests/http/tests/css/resources/counter-crash-frame-src.html

that is related webkit <https://crbug.com/chromium/53344>  

<https://bugs.webkit.org/show_bug.cgi?id=53344>

apparently versions that don't have that commit aren't affected

**VERSION**  

Chrome Version:  

Chromium 11.0.663.0 (Developer Build 15ad4b6)  

WebKit 534.19 (git@e7457c4)  

(self-built chromium LKGR + webkit git)  

on Linux 2.6.35-26-generic #46-Ubuntu x86\_64

Chromium 11.0.663.0 (Developer Build 74077) Ubuntu 10.10  

WebKit 534.19 (unknown@0)  

on Linux 2.6.35-26-generic #46-Ubuntu x86\_64

not affected: everything else I tested

**REPRODUCTION CASE**  

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

=> 0x00007ffff69ad3e3 <+19>: mov 0x38(%rax),%rdx

rax 0x65004e00200073 28429307657322611

#0 WebCore::CounterNode::previousInPreOrder (this=0x7ffff90cfa40) at third\_party/WebKit/Source/WebCore/rendering/CounterNode.cpp:90  

#1 0x00007ffff6984109 in WebCore::destroyCounterNodeWithoutMapRemoval (identifier="a", node=0x7ffff90cfb00) at third\_party/WebKit/Source/WebCore/rendering/RenderCounter.cpp:514  

#2 0x00007ffff6984bc9 in WebCore::RenderCounter::destroyCounterNodes (renderer=0x7ffff9035818) at third\_party/WebKit/Source/WebCore/rendering/RenderCounter.cpp:543

## Attachments

- [counter.html](attachments/counter.html) (text/plain; charset=us-ascii, 298 B)
- [valgrind_72340.txt](attachments/valgrind_72340.txt) (text/plain; charset=us-ascii, 8.6 KB)
- [gdb_72340.txt](attachments/gdb_72340.txt) (text/plain; charset=us-ascii, 10.3 KB)

## Timeline

### mi...@gmail.com (2011-02-08)

Chromium	11.0.664.0 (Developer Build 74135)
WebKit	534.19 (trunk@77958)

on Windows 7 also crashes

### mi...@gmail.com (2011-02-08)

valgrind log

==6874==  Address 0xf7844d8 is 40 bytes inside a block of size 64 free'd
==6874==    by 0x1D8571C: WebCore::RenderCounter::destroyCounterNode(WebCore::RenderObject*, WTF::AtomicString const&) (RefCounted.h:136)

==6874==  Address 0xf7844e8 is 56 bytes inside a block of size 64 free'd
WebCore::RenderCounter::destroyCounterNode(WebCore::RenderObject*, WTF::AtomicString const&) (RefCounted.h:136)


### mi...@gmail.com (2011-02-08)

gdb log

### js...@chromium.org (2011-02-09)

It couldn't have been the change for webkit.org/b/53344 because that was just a test. My guess is that this is from http://trac.webkit.org/changeset/76859

@cdn - Care to take a crack at another counter node bug?

### ch...@gmail.com (2011-02-09)

[Empty comment from Monorail migration]

### ch...@gmail.com (2011-02-09)

This is yet another regression... Doesn't seem to affect stable. My guess is that Carol's last patch introduced this.

### ch...@gmail.com (2011-02-15)

Filed upstream as https://bugs.webkit.org/show_bug.cgi?id=54478

### in...@chromium.org (2011-02-16)

committed for carol - http://trac.webkit.org/changeset/78728.

This will be very tedious to merge since carol did update counter node code a lot :(

### sc...@gmail.com (2011-02-16)

Is M10 merge easier? At this stage we should be considering that maybe our last M9 patch is already done.

### in...@chromium.org (2011-02-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-02-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-02-18)

Thanks miaubiz. Hopefully this takes CSS counters towards being in good shape now. And there's a provisional $1000 Chromium Security Reward, thanks to the high quality of the report.

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

### ch...@gmail.com (2011-02-28)

to be safe I am merging Carol's changes to the counternode code prior to this change they were merged as follows

http://trac.webkit.org/changeset/79929
http://trac.webkit.org/changeset/79931
http://trac.webkit.org/changeset/79932

I then merged this fix as http://trac.webkit.org/changeset/79933

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-04-29)

Looks like we forgot to pay this reward out. I'll add it in to your reward for all the Chrome 11 fixes that we just announced.

### sc...@gmail.com (2011-05-04)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### js...@chromium.org (2011-10-05)

Batch update: Guessing based on search criteria that this security bug impacted a stable release.

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

This issue was migrated from crbug.com/chromium/72340?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087696)*

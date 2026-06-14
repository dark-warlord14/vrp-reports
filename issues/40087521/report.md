# use-after-free when document.close and document.write are called after requesting a non-existing script

| Field | Value |
|-------|-------|
| **Issue ID** | [40087521](https://issues.chromium.org/issues/40087521) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2011-02-03 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

RIP == 0  

valgrind says it's because  

Address 0x358ded70 is 0 bytes inside a block of size 128 free'd

**VERSION**  

Chromium 11.0.656.0 Ubuntu 10.10  

on Ubuntu Maverick 64bit 2.6.35-25-generic  

Google Chrome 10.0.648.11 dev  

on Ubuntu Maverick 64bit 2.6.35-25-generic

8.0.552.237 (Official build 70801)  

on Windows 7 32-bit

**REPRODUCTION CASE**

<script src="non-existent.js"></script>
<iframe onload="document.close(); document.write();"></iframe>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: sad tab  

Crash State: #0 0x0000000000000000 in ?? ()  

#1 0x00007ffff62e6910 in WebCore::HTMLConstructionSite::attach[WebCore::Element](javascript:void(0);) (this=0x7ffff8e8fe30, parent=0x7ffff9170a00, prpChild=<value optimized out>)  

at third\_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:98  

#2 0x00007ffff62e69d5 in WebCore::HTMLConstructionSite::attachToCurrent (this=0x1, child=<value optimized out>)  

at third\_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:237  

#3 0x00007ffff62e6dc7 in WebCore::HTMLConstructionSite::insertHTMLElement (this=0x7ffff8e8fe30, token=<value optimized out>)  

at third\_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:267

## Attachments

- [valgrind.txt](attachments/valgrind.txt) (text/plain; charset=us-ascii, 8.2 KB)
- [gdb.txt](attachments/gdb.txt) (text/plain; charset=us-ascii, 14.0 KB)
- [71763.html](attachments/71763.html) (text/plain; charset=us-ascii, 103 B)

## Timeline

### mi...@gmail.com (2011-02-03)

valgrind log

### mi...@gmail.com (2011-02-03)

gdb log

### mi...@gmail.com (2011-02-03)

repro as a file.  it's just those two lines

### js...@chromium.org (2011-02-03)

Yep, that's a very stale this pointer. Looks like somewhere up this hierarchy we need to hold a RefPtr to parent.

@abarth - Since this is in the parser you might be the best to turn around a quick fix. I'd probably just naively use a protector on parent in HTMLConstructionSite::attach.

@miaubiz - Nice bug. And it's also very handy when you use the bug ID on filenames in follow up attachments like that.

### js...@chromium.org (2011-02-03)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-02-03)

Actually, I think I'll just submit a patch with my naive solution. @abarth can chastise me upstream if it's the wrong fix.

Reported upstream at: https://bugs.webkit.org/show_bug.cgi?id=53689


### js...@chromium.org (2011-02-03)

I take it back. This needs the work of a parser expert. Protecting the pointer fixes the crash, but there are asserts hitting and generally confusing behavior.

### ab...@chromium.org (2011-02-07)

Looking again.

### ab...@chromium.org (2011-02-08)

This bug is complex.  :-/

### ab...@chromium.org (2011-02-08)

Path posted upstream.

### ab...@chromium.org (2011-02-09)

Fixenated: http://trac.webkit.org/changeset/78147

### in...@chromium.org (2011-02-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-02-10)

I do think this change is rather quite fresh and might be risky for M9P2, lets pick it up in M9P3.

### js...@chromium.org (2011-02-28)

We're not cutting another m9, so merging straight to m10.

### js...@chromium.org (2011-02-28)

Merged to m10: http://trac.webkit.org/changeset/79901

### sc...@gmail.com (2011-03-03)

@miaubiz: Nice report! This provisionally qualifies for a $1000 Chromium Security Reward.
This bug is an awesome report, and rewarded at the higher $1000 level due to various things:
- Truly minimal repro :D
- The inclusion of a valgrind report is really useful.

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

### sc...@gmail.com (2011-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-15)

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

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/71763?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087521)*

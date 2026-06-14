# Use after free in WebCore::findPlainText

| Field | Value |
|-------|-------|
| **Issue ID** | [40093123](https://issues.chromium.org/issues/40093123) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-07-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

**VERSION**  

Chrome Version: stable + trunk  

Operating System: linux 64bit

**REPRODUCTION CASE**

<script>
function x() {
document.body.offsetHeight;
document.body.innerHTML=" ";
window.find('a')
}
</script>
<body onload="x()">
a
</body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

==18653== ERROR: AddressSanitizer crashed on address 0x00007fffbeacef22 at pc 0x7ffff34debcc bp 0x7fffffff68f0 sp 0x7fffffff68b0  

READ of size 2 at 0x00007fffbeacef22 thread T0  

#0 0x7ffff34debcc in void WTF::Vector<unsigned short, 0ul>::append<unsigned short>(unsigned short const\*, unsigned long) ??:0  

#1 0x7ffff49120d3 in WebCore::findPlainText(WebCore::Range const\*, WTF::String const&, unsigned int) media/base/yuv\_row\_table.cc:0

0x00007fffbeacef22 is located 0 bytes to the right of 34-byte region [0x00007fffbeacef00,0x00007fffbeacef22)  

allocated by thread T0 here:  

#0 0x7ffff6e54d3a in malloc *asan\_rtl*  

#1 0x7ffff3c57569 in WTF::fastMalloc(unsigned long) media/base/yuv\_row\_table.cc:0

## Attachments

- [asan-symbols.txt](attachments/asan-symbols.txt) (text/plain; charset=us-ascii, 4.4 KB)
- [plain.html](attachments/plain.html) (text/html; charset=us-ascii, 146 B)
- [vg-90668.txt](attachments/vg-90668.txt) (text/plain; charset=us-ascii, 6.6 KB)

## Timeline

### mi...@gmail.com (2011-07-27)

valgrind log

### kc...@chromium.org (2011-07-27)

issue  74649 ? 

### in...@chromium.org (2011-07-27)

Yeah this is 74649, but we will keep this one open for reward purpose since this has repro.

### in...@chromium.org (2011-07-27)

Also see tracking https://bugs.webkit.org/show_bug.cgi?id=63611

### sc...@gmail.com (2011-07-27)

Wonderful, thanks for getting us a nice simple repro for a bug that was irritating us, miaubiz :)

### [Deleted User] (2011-07-28)

It turned out that this is not a duplicate of the https://crbug.com/chromium/63611 so I filed https://bugs.webkit.org/show_bug.cgi?id=65296.  I'm posting a patch shortly.

### [Deleted User] (2011-07-28)

Ok, I have a patch on the webkit bug.  This was a really easy bug to fix preciously because of the reduction.  Hooray!

### sc...@gmail.com (2011-07-28)

@rniwa: urock++! Looking at the patch, is it almost more of a use-after-free than a OOB read?

### [Deleted User] (2011-07-28)

Yeah, it appears to be use-after-free.  Maybe I should rename the bug title but it doesn't really matter anyways because it won't show up anywhere.


### sc...@gmail.com (2011-07-28)

Not too bothered about the bug title, but it affects the severity (raised) and the reward nomination :)

### [Deleted User] (2011-07-28)

I see.

### in...@chromium.org (2011-07-28)

http://trac.webkit.org/changeset/91908

### js...@chromium.org (2011-07-28)

Bulk move for WillMerge change.

### js...@chromium.org (2011-07-28)

Bulk move for WillMerge change.

### sc...@gmail.com (2011-08-06)

Merged to M13: http://trac.webkit.org/changeset/92534
Merged to M14: http://trac.webkit.org/changeset/92535

### sc...@gmail.com (2011-08-16)

@miaubiz: thanks! It's not clear how serious this is, but our culture is to assume the worst and reward at that level, hence $1000 and our thanks for repro'ing a bug that was really irritating us.

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

### sc...@gmail.com (2011-08-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-26)

Payment in system...

### js...@chromium.org (2011-10-05)

Batch update.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed.. 

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

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

This issue was migrated from crbug.com/chromium/90668?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093123)*

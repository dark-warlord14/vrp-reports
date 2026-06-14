# Regression: Use-after-free in CounterNode::insertAfter

| Field | Value |
|-------|-------|
| **Issue ID** | [40092406](https://issues.chromium.org/issues/40092406) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-07-01 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

counter related use after free

without memory debugging tools it just hangs forever, asan and vg say it's use after free.

**VERSION**  

Chrome Version: daily + canary + trunk  

Operating System: linux 64bit, win7

bisect-builds puts it here:  

<http://build.chromium.org/f/chromium/perf/dashboard/ui/changelog.html?url=/trunk/src&range=88127:88339>  

probably the webkit roll to 88326

**REPRODUCTION CASE**  

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer/hang  

Crash State:  

Invalid read of size 8  

at 0x1D289C8: WebCore::CounterNode::insertAfter(WebCore::CounterNode\*, WebCore::CounterNode\*, WTF::AtomicString const&) (CounterNode.cpp:202)  

Address 0xf4c45a0 is 16 bytes inside a block of size 72 free'd

## Attachments

- [13b.html](attachments/13b.html) (text/plain; charset=us-ascii, 174 B)
- [vg.txt](attachments/vg.txt) (text/x-pascal; charset=us-ascii, 7.3 KB)
- [asan.txt](attachments/asan.txt) (text/plain; charset=us-ascii, 7.3 KB)
- [88216-vg-56inside72.txt](attachments/88216-vg-56inside72.txt) (text/plain; charset=us-ascii, 14.0 KB)
- [counter56inside72.html](attachments/counter56inside72.html) (text/html; charset=us-ascii, 4.9 KB)
- [counters-min.html](attachments/counters-min.html) (text/html; charset=us-ascii, 240 B)

## Timeline

### in...@chromium.org (2011-07-07)

Checking out the webkit range from the regression, looks like it might be coming from http://trac.webkit.org/changeset/88308 (which makes changes to content property and the repro has it too :). I cannot see anything else counter node specific.

Cris, what do you think ??

### in...@chromium.org (2011-07-07)

[Empty comment from Monorail migration]

### mi...@gmail.com (2011-07-14)

here's another repro with offset 56 inside 72

### [Deleted User] (2011-07-28)

Was this never filed upstream?

I have a minimized repro for this and a way to make counters safe. I think I am going to file a new bug for the fix though and mark this one non-security as the tree will still be jacked up. My fix will just cause things like this to no longer allow stale references hanging around.

### [Deleted User] (2011-07-28)

the upstream bug is https://bugs.webkit.org/show_bug.cgi?id=64129

### sc...@gmail.com (2011-08-04)

A broad approach to close down lots of counter node trouble is tracked at https://bugs.webkit.org/show_bug.cgi?id=65346

### [Deleted User] (2011-08-08)

This no longer has security implications after http://trac.webkit.org/changeset/92630 but is still a functional bug. I suggest that we drop flags on this once all relevant branches are patched but leave it open as a functional bug in CSS counters.

Also we should merge http://trac.webkit.org/changeset/92630

### [Deleted User] (2011-08-08)

Bottle of champagne time to celebrate the death of counter node use-after-free.

### sc...@gmail.com (2011-08-09)

Merged to M14: http://trac.webkit.org/changeset/92663

### sc...@gmail.com (2011-08-12)

Merged to M13: http://trac.webkit.org/changeset/92889

### sc...@gmail.com (2011-08-16)

@miaubiz: nice bug as always. $1000

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

### sc...@gmail.com (2011-08-24)

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

This issue was migrated from crbug.com/chromium/88216?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092406)*

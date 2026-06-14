# use after free due to floats not removed

| Field | Value |
|-------|-------|
| **Issue ID** | [40092118](https://issues.chromium.org/issues/40092118) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-06-22 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

more floats

**VERSION**  

Chrome Version: webkit r89189 and all others  

Operating System: all?

**REPRODUCTION CASE**  

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:  

Jump to the invalid address stated on the next line  

at 0x414141417FFFFFFF: ???  

by 0x1C04452: WebCore::RenderBlock::addOverflowFromFloats()

## Attachments

- [vg.txt](attachments/vg.txt) (text/plain; charset=us-ascii, 11.2 KB)
- [floatsy.html](attachments/floatsy.html) (text/plain; charset=us-ascii, 442 B)
- [24.html](attachments/24.html) (text/plain; charset=us-ascii, 488 B)
- [27.html](attachments/27.html) (text/plain; charset=us-ascii, 595 B)
- [22.html](attachments/22.html) (text/plain; charset=us-ascii, 475 B)
- [22b.html](attachments/22b.html) (text/plain; charset=us-ascii, 442 B)
- [87148.zip](attachments/87148.zip) (application/zip; charset=binary, 21.8 KB)

## Timeline

### in...@chromium.org (2011-06-22)

Can you please check your build. I cannot reproduce it on windows canary (14.0.800.0 canary), windows debug build (14.0.798.0 (Developer Build 89747)). Please try updating to trunk, deleting the ./out/Release, Debug folders and recompiling. This should be fixed by http://trac.webkit.org/changeset/89165.

### mi...@gmail.com (2011-06-22)

will do.  it looked 99% the same as 86502, but the repros from that one didn't crash anymore on my build, so I figured it's different.  I'll check back once I rebuild. 

### mi...@gmail.com (2011-06-22)

in the meantime, here's a variation that crashes on WebKit r89415 on osx (Safari though)

Thread 0 Crashed:
0   ???                           	000000000000000000 0 + 0
1   com.apple.WebCore             	 WebCore::RenderBlock::computeOverflow(int, bool) + 91


### mi...@gmail.com (2011-06-22)

rm -rf out && rebuilt with webkit 89393 and it's still crashing. I'm uploading a few more variations in case it makes a difference 

### in...@chromium.org (2011-06-23)

Thank you very much Miaubiz for this bug. Can you please provide us with as many testcases as possible (like < 50) so that we can make sure to fix it properly this time. Thank you very much for your continued fuzzing and I can ask the reward panel for higher reward consideration for your fuzzing testcases.

### mi...@gmail.com (2011-06-23)

@inferno: here you go. 49 ;)

### in...@chromium.org (2011-06-23)

Thanks a lot Miaubiz. We will try our best to properly fix it this time.

### in...@chromium.org (2011-06-27)

Have a patch up for review - https://bugs.webkit.org/show_bug.cgi?id=63355

### in...@chromium.org (2011-06-27)

http://trac.webkit.org/changeset/89836

Miaubiz, it will be awesome if you can please run your fuzzers again on the new patch and file a bug if you see anything missing.

### sc...@gmail.com (2011-06-28)

Merged to M13: http://trac.webkit.org/changeset/89893

### sc...@gmail.com (2011-07-20)

$1000

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

This issue was migrated from crbug.com/chromium/87148?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092118)*

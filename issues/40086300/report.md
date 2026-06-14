# Security: libxslt generation of text nodes integer overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [40086300](https://issues.chromium.org/issues/40086300) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>XML |
| **CVE IDs** | CVE-2017-5029 |
| **Reporter** | ho...@gmail.com |
| **Assignee** | do...@chromium.org |
| **Created** | 2016-12-22 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

With a xslt file which generates big text nodes it is possible to trigger an integer overflow in xsltAddTextString in transform.c of the libxslt library. The function handles the memory management if new data are added to a text node. The vulnerability exists because there is no check for overflow while calculating a new size of a buffer to hold the data of a text node. The issue can be exploited to trigger an out of bounds write.

A simple fix would limit the max size of a text node to a sane value.  

A mitigation would it be to use a size\_checked\_realloc like in libxml in libxslt.

**VERSION**  

Chrome Version: 57.0.2953.0 + beta  

Operating System: Ubuntu 16.04.1 LTS

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace, registers, exception record]**  

**Client ID (if relevant): [see link above]**

## Attachments

- [chrome.poc.html](attachments/chrome.poc.html) (text/plain, 2.3 KB)

## Timeline

### ho...@gmail.com (2016-12-22)

Type of crash: tab
Crash State:

==1==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7fd7a76a2000 at pc 0x564695670354 bp 0x7ffd5c6a4020 sp 0x7ffd5c6a37d0
WRITE of size 5614304 at 0x7fd7a76a2000 thread T0 (chrome)

    #0 0x564695670353 in __asan_memcpy ??:?
    #1 0x7fd93b807573 in xsltAddTextString ./out/Debug/../../third_party/libxslt/libxslt/transform.c:837
    #2 0x7fd93b806cd9 in xsltCopyTextString ./out/Debug/../../third_party/libxslt/libxslt/transform.c:929
    #3 0x7fd93b81f988 in xsltValueOf ./out/Debug/../../third_party/libxslt/libxslt/transform.c:4540
    #4 0x7fd93b80e26d in xsltApplySequenceConstructor ./out/Debug/../../third_party/libxslt/libxslt/transform.c:2766
    #5 0x7fd93b80c4e0 in xsltApplyXSLTTemplate ./out/Debug/../../third_party/libxslt/libxslt/transform.c:3204
    #6 0x7fd93b82101a in xsltCallTemplate ./out/Debug/../../third_party/libxslt/libxslt/transform.c:4780
    #7 0x7fd93b80e26d in xsltApplySequenceConstructor ./out/Debug/../../third_party/libxslt/libxslt/transform.c:2766
    #8 0x7fd93b825857 in xsltIf ./out/Debug/../../third_party/libxslt/libxslt/transform.c:5390
    #9 0x7fd93b80e26d in xsltApplySequenceConstructor ./out/Debug/../../third_party/libxslt/libxslt/transform.c:2766
    #10 0x7fd93b80c4e0 in xsltApplyXSLTTemplate ./out/Debug/../../third_party/libxslt/libxslt/transform.c:3204
…

0x7fd7a76a2000 is located 6144 bytes to the left of 5616152-byte region [0x7fd7a76a3800,0x7fd7a7bfea18)


### ho...@gmail.com (2016-12-22)

sorry for splitted report

### cl...@chromium.org (2016-12-22)

[Comment Deleted]

### cl...@chromium.org (2016-12-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4937030674153472

### pe...@chromium.org (2016-12-22)

Hi Dominic,

Feel free to adjust labels, or reassign as appropriate.

Thanks!

[Monorail components: Blink>XML]

### sh...@chromium.org (2016-12-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-12-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5731321122127872

### mb...@chromium.org (2016-12-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-12-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5684287069487104

### sh...@chromium.org (2017-01-05)

dominicc: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2017-01-11)

[Empty comment from Monorail migration]

### do...@chromium.org (2017-01-11)

Patch up at https://codereview.chromium.org/2626983002

I have filed upstream https://bugzilla.gnome.org/show_bug.cgi?id=777124

### do...@chromium.org (2017-01-11)

[Empty comment from Monorail migration]

### mm...@chromium.org (2017-01-11)

[Empty comment from Monorail migration]

### do...@chromium.org (2017-01-12)

[Empty comment from Monorail migration]

### do...@chromium.org (2017-01-12)

hofusec, can I CC you on the upstream libxslt bug?

### ho...@gmail.com (2017-01-12)

yes

### do...@chromium.org (2017-01-13)

Nick Wellnhofer contributed a simpler, better patch upstream at https://bugzilla.gnome.org/attachment.cgi?id=343366 see https://codereview.chromium.org/2626983002 patch 2 for posterity.

### do...@chromium.org (2017-01-13)

Note: Per upstream request, we need to ping the upstream bug when we land something.

### bu...@chromium.org (2017-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/14b7c024aaec338adcbf87cbeee54cf6137d7f8a

commit 14b7c024aaec338adcbf87cbeee54cf6137d7f8a
Author: dominicc <dominicc@chromium.org>
Date: Wed Jan 25 09:50:13 2017

xsltAddTextString: Check for overflow when merging text nodes.

BUG=676623

Review-Url: https://codereview.chromium.org/2626983002
Cr-Commit-Position: refs/heads/master@{#445987}

[modify] https://crrev.com/14b7c024aaec338adcbf87cbeee54cf6137d7f8a/third_party/libxslt/README.chromium
[modify] https://crrev.com/14b7c024aaec338adcbf87cbeee54cf6137d7f8a/third_party/libxslt/libxslt/transform.c
[modify] https://crrev.com/14b7c024aaec338adcbf87cbeee54cf6137d7f8a/third_party/libxslt/libxslt/xsltInternals.h


### do...@chromium.org (2017-02-01)

This should be fixed.

### sh...@chromium.org (2017-02-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-03)

Your change meets the bar and is auto-approved for M57. Please go ahead and merge the CL to branch 2987 manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-02-03)

Please merge your change to M57 branch 2987 before 5:00 PM Pt, Monday (02/06/) so we can pick it up for next week Beta release. Thank you.

### sh...@chromium.org (2017-02-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-02-06)

Please merge your change to M57 branch 2987 before 5:00 PM PT, Tuesday (02/07/17) so we can pick it up for next Beta release. Thank you.

### aw...@chromium.org (2017-02-06)

[Empty comment from Monorail migration]

### do...@chromium.org (2017-02-07)

I'm not sure why a bot did not comment here, but I merged this yesterday:

https://storage.googleapis.com/chromium-find-releases-static/14b.html#14b7c024aaec338adcbf87cbeee54cf6137d7f8a

Merged to 57.0.2987.33 (as 3b4c1d91...).

If someone could please sanity check me on that :)

### go...@chromium.org (2017-02-07)

Per https://crbug.com/chromium/676623#c29, this is already merged to M57 branch 2987 and I can see the merge here: https://chromium.googlesource.com/chromium/src/+/3b4c1d91912bbc7fa1e75c7034318a241c03a7ae

### dd...@apple.com (2017-02-07)

Thanks for the CC folks.  Tracking this at Apple with <rdar://problem/30398908>.


### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-13)

Nice one!  The panel decided to award $3,000 for this report.  A member of our finance team will be in touch shortly to arrange payment.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************


### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-14)

[Empty comment from Monorail migration]

### dd...@apple.com (2017-03-01)

Has a CVE-ID been assigned to this issue?  Apple wants to mention the CVE-ID in an upcoming security bulletin.


### mm...@chromium.org (2017-03-01)

Andrew, did it get a CVE?

### aw...@chromium.org (2017-03-02)

Yep, it's CVE-2017-5029. Thanks for the ping.

### mm...@google.com (2017-03-02)

Cool, thanks for the fast response!

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### mm...@chromium.org (2017-03-09)

Wait, two CVEs for a single bug? I've pinged Andrew to ensure that this is correct.

### aw...@chromium.org (2017-03-09)

Good spot - overly zealous automation :-(

### dd...@apple.com (2017-03-24)

FYI, this already went public via Debian:
https://security-tracker.debian.org/tracker/CVE-2017-5029
https://www.mail-archive.com/debian-bugs-dist@lists.debian.org/msg1508434.html


### aw...@google.com (2017-03-24)

Removing view restrictions given #44

### da...@gmail.com (2017-04-28)

[Comment Deleted]

### da...@gmail.com (2017-04-28)

In the patch I see

+        if (len >= INT_MAX - ctxt->lasttuse) {
+            xsltTransformError(ctxt, NULL, target,
+                "xsltCopyText: text allocation failed\n");
+            return(NULL);
+        }
+        minSize = ctxt->lasttuse + len + 1;
+

So shouldn't the condition be

    if (len >= INT_MAX - ctxt->lasttuse - 1)
 ?

Or, moreover, maybe ctxt->lasttuse == INT_MAX, so a better condition could be
    if (ctxt->lasttuse == INT_MAX || len >= INT_MAX - ctxt->lasttuse - 1)
?

### do...@chromium.org (2017-05-01)

Yeah, that needs to account for the + 1. I have filed https://crbug.com/chromium/716967.

### do...@chromium.org (2017-05-08)

See the other issue but ddkilzer points out that the existing code is OK because of the >= check, and as you point out using a > check has the added complication of lasttuse being INT_MAX that >= does not have.

### dd...@apple.com (2017-05-08)

The only reason to change it now would be if it makes the code clearer (when someone looks at it in the future).

There is no residual security issue based on my analysis of the current code.


### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/676623?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086300)*

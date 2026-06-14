# Security: Unknown memory corruption in HTML rendering.

| Field | Value |
|-------|-------|
| **Issue ID** | [40087942](https://issues.chromium.org/issues/40087942) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Blink>Accessibility |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | be...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2017-05-31 |
| **Bounty** | $500.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://www.chromium.org/Home>**  

**/chromium-security/security-faq**

**Please see the following link for instructions on filing security bugs:**  

**<http://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**VULNERABILITY DETAILS**  

A simple HTML file causes an access violation when running Chrome with page heap on and accessibility enabled.

**VERSION**  

Chrome Version: 61.0.3116.0 canary  

Operating System: Windows 10

## **REPRODUCTION CASE** A html file with this content will crash chrome.

<canvas/>
<!
------------
If you remove the CR/LF, it still crashes, but with a NULL pointer, rather than a seemingly random address.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: See attached BugId report for stack and other details.

## Attachments

- [AVW@Arbitrary 36f.32e @ chrome.exe!chrome_child.dll!blink։։HTMLScriptElement։։InitiatorName.html](attachments/AVW@Arbitrary 36f.32e @ chrome.exe!chrome_child.dll!blink։։HTMLScriptElement։։InitiatorName.html) (text/plain, 1.5 MB)

## Timeline

### be...@gmail.com (2017-05-31)

[Comment Deleted]

### be...@gmail.com (2017-05-31)

My comment was somehow deleted, let's try again: full command-line used for testing:
"C:\Users\SkyLined\AppData\Local\Google\Chrome SxS\Application\chrome.exe" --enable-experimental-accessibility-features --enable-experimental-canvas-features --enable-experimental-input-view-features --enable-experimental-web-platform-features --enable-usermedia-screen-capturing --enable-viewport --enable-webgl-draft-extensions --enable-webvr --expose-internals-for-testing --disable-popup-blocking --disable-prompt-on-repost --force-renderer-accessibility --javascript-harmony --no-sandbox

### be...@gmail.com (2017-06-02)

has anyone had time to look at and reproduce this issue?

### el...@chromium.org (2017-06-02)

In a quick look, I couldn't reproduce, but I suspect that it's because I don't have PageHeap enabled. Based on the markup, I assume the issue is somewhere in the Canvas fallback content code here in Element::LayoutObjectIsFocusable(): https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/dom/Element.cpp?type=cs&q=IsFocusable+canvas+package:%5Echromium$&l=235

### mb...@chromium.org (2017-06-02)

Sorry for the delay, I was able to repro it. Looks like a bad cast, and of the arguments above it only seems to require --force-renderer-accessibility. Tentatively assigning medium severity.

dmazzoni: Could you take a look or reassign this?

[Monorail components: Blink>Accessibility]

### cl...@chromium.org (2017-06-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5380166569426944

### cl...@chromium.org (2017-06-02)

Detailed report: https://clusterfuzz.com/testcase?key=5380166569426944

Job Type: linux_asan_chrome_mp
Crash Type: Abrt
Crash Address: 0x03e900000001
Crash State:
  blink::AXObjectImpl::CanReceiveAccessibilityFocus
  blink::AXObjectImpl::NameFromContents
  blink::AXNodeObject::TextAlternative
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=474481:474544

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5380166569426944


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### mb...@chromium.org (2017-06-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-03)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-06-03)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-06-03)

Reverting https://codereview.chromium.org/2894983002 fixes this problem, but I wonder if the IsFocusable() call is just exposing a bug somewhere in IsInert().

### al...@chromium.org (2017-06-05)

Stealing this if that's ok. I have a fix.

### bu...@chromium.org (2017-06-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7eabf15d969800c61602296bc60fc013fc4e657f

commit 7eabf15d969800c61602296bc60fc013fc4e657f
Author: Aaron Leventhal <aleventhal@chromium.org>
Date: Mon Jun 05 20:29:13 2017

No AX objects for comments and other irrelevant node types

DCHECK was failing for comment node when we try node->ToElement().
Don't create AX objects for comments and other irrelevant node types

Bug: 728185
Change-Id: I377b0cdf0b96e8c0bc805a6f3f0e1f0ed8997749
Reviewed-on: https://chromium-review.googlesource.com/524242
Commit-Queue: Aaron Leventhal <aleventhal@chromium.org>
Reviewed-by: Dominic Mazzoni <dmazzoni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#477071}
[modify] https://crrev.com/7eabf15d969800c61602296bc60fc013fc4e657f/third_party/WebKit/Source/modules/accessibility/AXObjectCacheImpl.cpp
[modify] https://crrev.com/7eabf15d969800c61602296bc60fc013fc4e657f/third_party/WebKit/Source/modules/accessibility/AXObjectImpl.cpp


### al...@chromium.org (2017-06-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-06-06)

ClusterFuzz has detected this issue as fixed in range 477026:477088.

Detailed report: https://clusterfuzz.com/testcase?key=5380166569426944

Job Type: linux_asan_chrome_mp
Crash Type: Abrt
Crash Address: 0x03e900000001
Crash State:
  blink::AXObjectImpl::CanReceiveAccessibilityFocus
  blink::AXObjectImpl::NameFromContents
  blink::AXNodeObject::TextAlternative
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=474481:474544
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=477026:477088

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5380166569426944


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-08)

The VRP Panel decided to award $500 for this - many thanks!

### aw...@chromium.org (2017-06-08)

[Empty comment from Monorail migration]

### aw...@google.com (2017-07-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-06)

This bug requires manual review: M60 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), josafat@(ChromeOS), bustamante@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-07-07)

Approving merge to M60. 

### sh...@chromium.org (2017-07-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-07-10)

Please merge this to M60 ASAP. branch:3112

### al...@chromium.org (2017-07-10)

@abdulsyed, I'm not able to use drover. I may not have enough status/credentials.

> git drover --branch 3112 --cherry-pick 7eabf15d969800c61602296bc60fc013fc4e657f
Going to cherry-pick
"""
commit 7eabf15d969800c61602296bc60fc013fc4e657f
Author: Aaron Leventhal <aleventhal@chromium.org>
Date:   Mon Jun 5 14:13:59 2017 -0400

    No AX objects for comments and other irrelevant node types
    
    DCHECK was failing for comment node when we try node->ToElement().
    Don't create AX objects for comments and other irrelevant node types
    
    Bug: 728185
    Change-Id: I377b0cdf0b96e8c0bc805a6f3f0e1f0ed8997749
    Reviewed-on: https://chromium-review.googlesource.com/524242
    Commit-Queue: Aaron Leventhal <aleventhal@chromium.org>
    Reviewed-by: Dominic Mazzoni <dmazzoni@chromium.org>
    Cr-Commit-Position: refs/heads/master@{#477071}
"""
to 3112. Continue (y/n)? y
Running presubmit upload checks ...

Presubmit checks passed.
 third_party/WebKit/Source/modules/accessibility/AXObjectCacheImpl.cpp | 3 +++
 third_party/WebKit/Source/modules/accessibility/AXObjectImpl.cpp      | 6 +-----
 2 files changed, 4 insertions(+), 5 deletions(-)
remote: Processing changes: updated: 1, done            
remote: (W) 59e3ea7: commit subject >50 characters; use shorter first paragraph        
remote: (I) 59e3ea7: no files changed, message updated        
remote: 
remote: Updated Changes:        
remote:   https://chromium-review.googlesource.com/565444 No AX objects for comments and other irrelevant node types        
remote: 
To https://chromium.googlesource.com/chromium/src.git
 * [new branch]                59e3ea7dff495601eec4d0045f53a559f738f517 -> refs/for/refs/branch-heads/3112%ready,notify=ALL,m=Initial_upload
Adding self-LGTM (Code-Review +1) because of TBRs.
Your Gerrit credentials might be misconfigured. Try: 
  git cl creds-check
Error: Upload failed

> git cl creds-check
git is already configured to use your .gitcookies from /usr/local/google/home/aleventhal/.gitcookies
Your .netrc and .gitcookies have credentials for these hosts:
                            Host	                       User	 Which file
================================	===========================	===========
chromium-review.googlesource.com	git-aleventhal.chromium.org	.gitcookies
       chromium.googlesource.com	git-aleventhal.chromium.org	.gitcookies

No problems detected in your .gitcookies file.


### bu...@chromium.org (2017-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4cd85345dc057cefc318c3bdb60497d8f0f27911

commit 4cd85345dc057cefc318c3bdb60497d8f0f27911
Author: Andrew R. Whalley <awhalley@chromium.org>
Date: Mon Jul 10 21:43:20 2017

[M60 Merge] No AX objects for comments and other irrelevant node types

DCHECK was failing for comment node when we try node->ToElement().
Don't create AX objects for comments and other irrelevant node types

Bug: 728185
Change-Id: I377b0cdf0b96e8c0bc805a6f3f0e1f0ed8997749
Reviewed-on: https://chromium-review.googlesource.com/524242
Commit-Queue: Aaron Leventhal <aleventhal@chromium.org>
Reviewed-by: Dominic Mazzoni <dmazzoni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#477071}
(cherry picked from commit 7eabf15d969800c61602296bc60fc013fc4e657f)

Review-Url: https://codereview.chromium.org/2974823003 .
Cr-Commit-Position: refs/branch-heads/3112@{#567}
Cr-Branched-From: b6460e24cf59f429d69de255538d0fc7a425ccf9-refs/heads/master@{#474897}

[modify] https://crrev.com/4cd85345dc057cefc318c3bdb60497d8f0f27911/third_party/WebKit/Source/modules/accessibility/AXObjectCacheImpl.cpp
[modify] https://crrev.com/4cd85345dc057cefc318c3bdb60497d8f0f27911/third_party/WebKit/Source/modules/accessibility/AXObjectImpl.cpp


### aw...@google.com (2017-07-10)

Most odd, I just did the honours and it worked OK.

### aw...@google.com (2017-07-10)

[Empty comment from Monorail migration]

### be...@gmail.com (2017-07-12)

Thanks for the reward - do you have any idea when I can expect a transfer?

My apologies for the limited information in the original report - I literally had half an hour before I had to catch a flight in which to create a repro, do analysis, and file the bug. I'll try to submit something more useful next time.

In my hurry, I forgot to mention that I normally expect a fix to be publicly available within 60 days of reporting simple security issues such as this one, unless you can provide me with a good reason to extend it. The fix was created more than a month ago, so I have to ask: why has this not been released yet? Also, will you be able to release this to the public before the 30th of this month, within 60 days of the original report?

I'm reluctant to enforce the deadline, as I did not mention it in the original report and it appears that you are close to releasing this to the public. But it also appears that you have been sitting on the fix for over a month from June 6th without any reason, which is exactly the kind of thing I want to prevent by setting such deadlines. If you could share some details on the timeline, that would be much appreciated.

### aw...@google.com (2017-07-13)

Hi berendjanwever@! Thanks for the note. I'll drop you an email about the reward payment.

With respect to the fix time, it looks like this bug was a regression that was first introduced in M60. M59 is the current stable, released version and seems to be unaffected (unless you believe otherwise?). So there's been no stable version to patch, and the fix will go out with the first M60 stable release around the week of the 25th July. Thanks for helping to catch this before it made it out!

### sk...@gmail.com (2017-07-29)

Hi Andrew,

Sorry, I was not paying sufficient attention (we recently had another baby, so I am not getting a lot of sleep :). Did this go out in the recent releases I saw on the blog?

### el...@chromium.org (2017-07-29)

Yes. Commit 4cd85345 landed in 60.0.3112.65

Current stable is 60.0.3112.78

https://chromereleases.googleblog.com/2017/07/stable-channel-update-for-desktop.html?m=1

### el...@chromium.org (2017-07-29)

(oh, and congrats!!)

### be...@gmail.com (2017-08-15)

Thanks, Eric!

I noticed that I opened this bug from my personal @gmail.com account and not my @chromium.org account. Is it possible for you to cc skylined@chromium.org, so I can unstar this with berendjanwever@gmail.com? It would save me some manual inbox organizing... thanks again!

### el...@chromium.org (2017-08-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@google.com (2021-11-20)

In an effort to clean up some old bugs in monorail, will be archiving this bug as it appears to be fixed and with no further recent activity or action required. Feel free to reopen if still relevant

### is...@google.com (2021-11-20)

This issue was migrated from crbug.com/chromium/728185?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087942)*

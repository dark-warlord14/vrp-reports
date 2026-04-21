# Security: UAF in ReadAnythingAppController::OnAXTreeDistilled

| Field | Value |
|-------|-------|
| **Issue ID** | [40064112](https://issues.chromium.org/issues/40064112) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Accessibility |
| **Platforms** | Mac |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ab...@google.com |
| **Created** | 2023-04-19 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**

1. Download asan-mac-release-1132387 from here: <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/mac-release%2Fasan-mac-release-1132387.zip?generation=1681906922585379&alt=media>
2. Start Chromium on MacOS: `./Chromium.app/Contents/MacOS/Chromium`
3. Follow the steps in the video to reproduce,may require multiple refreshes

**Problem Description:**  

After testing, it may take several refreshes to reproduce UAF stably and successfully.

It is currently unclear when the vulnerability was introduced.Bisect coming soon :)

**Additional Comments:**

\*\*Chrome version: \*\* 114.0.5722.0 \*\*Channel: \*\* Not sure

**OS:** Mac OS

## Attachments

- [asan](attachments/asan) (text/plain, 13.6 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 35.9 KB)
- [poc.mov](attachments/poc.mov) (video/quicktime, 8.3 MB)
- [asan2.txt](attachments/asan2.txt) (text/plain, 35.9 KB)
- [index.html](attachments/index.html) (text/plain, 70 B)
- [poc2.mov](attachments/poc2.mov) (video/quicktime, 9.2 MB)

## Timeline

### zh...@gmail.com (2023-04-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-19)

[Empty comment from Monorail migration]

### zh...@gmail.com (2023-04-19)

[Empty comment from Monorail migration]

### zh...@gmail.com (2023-04-19)

At present, it can only be reproduced stably on the m1 mac through the above method, and it seems that the intel mac cannot be reproduced through it.

### za...@google.com (2023-04-19)

Adding SI-None label as ReadAnything is not yet enabled and is an unlaunched feature. 
Tagging aleventhal@ as this looks like an accessibility bug but it's highly mitigated by user interaction and the multiple refreshes. Feel free to let me know if this belongs to other team. Thanks. 

[Monorail components: UI>Accessibility]

### zh...@gmail.com (2023-04-20)

Thank you for your quick reply, I would like to briefly update some of my progress here, mainly in two aspects:

First: Regarding user interaction, you can execute location.reload in the html file through setTimeout to reduce user interaction, so that the victim only needs to click on ReadAnything in the SidePanel to trigger UAF stably. According to: https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules#scope-of-program
The rules explicitly mention the following:
```
Mildly mitigated: Security bug with minimal mitigations; e.g. a security bug reliably triggered by two or fewer standard user interactions OR winning a race condition; does not require profile destruction or shutdown to trigger
```

This should belong to Mildly mitigated rather than highly mitigated.

Second: In fact, intel's macos can also stably reproduce this UAF vulnerability, but the asan log I get will be a little different. At present, I am not sure whether these are two different vulnerabilities, because the steps to reproduce are very similar. Just one on the intel mac and the other on the m1 mac.

The repro steps video and the aforementioned html files are updated here. Bisect is also a work in progress, please let me know if you have any other questions about bug reproduction.

### al...@chromium.org (2023-04-20)

[Empty comment from Monorail migration]

### zh...@gmail.com (2023-04-24)

Bisect:
https://chromium-review.googlesource.com/c/chromium/src/+/4370494

This commit introduces this vulnerability. Therefore, on macos systems, Canary version 114.0.5685.0 and Dev version 114.0.5696.0 are affected.

The earliest affected mac asan that is easy to download and test should be this link released on March 30:

1124048

https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/mac-release%2Fasan-mac-release-1124048.zip?generation=1680171707261730&alt=media

If you want to reproduce stably in this old version or other versions of mac asan chromium, then the startup parameters we need may be a little different, at least the following two features are required. In version 114, these two flags are enabled by default, so as mentioned at the beginning of my report, the vulnerability can be reproduced stably without any flags.

```
./Chromium.app/Contents/MacOS/Chromium --enable-features=ReadAnything,ReadAnythingWithScreen2x http://127.0.0.1:8000/index.html
```

In order to prove the above point more rigorously, you can download the previous version 1124012:

https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/mac-release%2Fasan-mac-release-1124012.zip?generation=1680165073989370&alt=media

I have no way to reproduce this bug on this version of mac.

### ar...@google.com (2023-04-27)

Thanks for the bisection!

Adding owner (rhalavati@) and reviewers(danakj@) who might be able to take a look.

### rh...@chromium.org (2023-04-27)

I don't see how that commit can be related to a UAF in ReadAnythingAppController::OnAXTreeDistilled as it does not modify anything in ReadAnything and any interface for Main Content Extraction in Screen AI service.

Since abigailbklein@ is the owner of ReadAnything and distiller and knows more about it, assigning back to her, please let me know if I am wrong.

### zh...@gmail.com (2023-04-28)

Thank you for your reply, I agree with your point of view, this is also a problem that bothered me for a few days before, because I got another conclusion from the perspective of source code audit. Of the two asan files I provided, one is related to |ProcessScreen2xResult|:

The callback function |AXTreeDistiller::ProcessScreen2xResult| stores a |ui::AXTree| of UnsafeDanglingUntriaged raw_ref, and this |ui::AXTree| can be released before the callback is executed by continuously executing `location.reload();`

```
https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/renderer/accessibility/ax_tree_distiller.cc;l=126-135;drc=15d2e059bf8cb5cd56e9571697fb75f00954642f;bpv=0;bpt = 1
```

I think this might be the root cause of the bug.If my judgment is wrong or you have other opinions, you can also tell me immediately, I am also very curious about this problem.

As for the commit obtained by Bisect, it may be the first commit that enables the successful and stable reproduction of the vulnerability, but this does not mean that the source of the vulnerability must be introduced from here. Maybe this commit directly or indirectly introduces a path that triggers the vulnerability.

For us, if we must submit the commit that actually introduces the vulnerability, it may be a complicated and uncertain thing, because there can be multiple commits that introduce the vulnerability, some introduce dangling pointers,some introduce trigger paths , some feature flags required to trigger vulnerabilities are introduced, and the corresponding repair solutions also have many possibilities, and the logic is very complicated. Therefore, I only submitted the first commit that can stably reproduce the vulnerability on my macos device as Bisect commit.I hope you can understand me, sorry for the confusion.

### rh...@chromium.org (2023-04-28)

No worries, thank you for raising the issue. :)

### da...@chromium.org (2023-05-01)

Putting a reference given to a function into a Callback without any lifetime tracking is a very risky proposition. We should correct that.

### da...@chromium.org (2023-05-01)

[Comment Deleted]

### ab...@google.com (2023-05-01)

Thanks for catching. We'll pass a tree id in the callback rather than a pointer to the tree itself.

### pg...@google.com (2023-05-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-05-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/34db57eae7436599dbacd7838e9decf99a629552

commit 34db57eae7436599dbacd7838e9decf99a629552
Author: Abigail Klein <abigailbklein@google.com>
Date: Mon May 01 22:37:37 2023

[Read Anything] Pass AXTreeID to screen2x callback.

We should never pass a reference to a callback without any lifetime
tracking. Passing an AXTreeID removes this risk.

This also removes the call to distill by algorithm after a failed
screen2x attempt. We had discussed removing this before so this is an
opportune time.

Fixed: 1434669
Bug: 1266555
Change-Id: If03255c1ab0c4636e2b0580389850b1e5da21c53
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4494011
Commit-Queue: Abigail Klein <abigailbklein@google.com>
Reviewed-by: Kristi Saney <kristislee@google.com>
Cr-Commit-Position: refs/heads/main@{#1138051}

[modify] https://crrev.com/34db57eae7436599dbacd7838e9decf99a629552/chrome/renderer/accessibility/ax_tree_distiller.h
[modify] https://crrev.com/34db57eae7436599dbacd7838e9decf99a629552/chrome/renderer/accessibility/ax_tree_distiller.cc


### [Deleted User] (2023-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-02)

[Empty comment from Monorail migration]

### ab...@google.com (2023-05-03)

[Empty comment from Monorail migration]

### ab...@google.com (2023-05-10)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-12)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us! 

### zh...@gmail.com (2023-05-12)

Thank you so much!

### zh...@gmail.com (2023-05-12)

Thank you very much for your efficient work. 

I would like to take this opportunity to ask some questions about Bisect.This confusion is what I generated in the process of submitting this vulnerability report:

For us, should we submit the commit that introduces the *root cause* of the vulnerability or submit the first commit that can *successfully trigger* the vulnerability?


### am...@chromium.org (2023-05-12)

The bisect should be the commit that introduces the root cause of the vulnerability. This allows us to quickly understand how the vulnerability was introduced, who the fix should be assigned to, and what build / revision range we should use to reproduced the issue and quickly understand how far back this vulnerability was introduced. This is set forth in the VRP policies and rewards page regarding the bisect bonus " identifying the specific commit that introduced the bug". 



### zh...@gmail.com (2023-05-12)

OK, thanks！

### am...@google.com (2023-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-08)

This issue was migrated from crbug.com/chromium/1434669?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1430192, crbug.com/chromium/1441628, crbug.com/chromium/1441659]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064112)*

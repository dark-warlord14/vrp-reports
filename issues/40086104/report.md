# Security: Circumvent CSP Header restrictions via about:blank

| Field | Value |
|-------|-------|
| **Issue ID** | [40086104](https://issues.chromium.org/issues/40086104) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature |
| **Reporter** | gr...@gmail.com |
| **Assignee** | mk...@chromium.org |
| **Created** | 2016-11-28 |
| **Bounty** | $1,000.00 |

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

**Please provide a brief explanation of the security issue.**

By loading a new document using window.open("","\_blank") and document.write-ing into it, (being in about:blank) I can circumvent the CSP restrictions put on the document my js code was running on and reach out to other sites.  

One could argue that the code was loaded with unsafe-inline in the CSP header, but that should still block any cross-site communication (e.g. 1x1px tracking image etc).  

The about:blank page has the same origin as its loading document, but CSP restrictions have been removed.  

I have seen there have been many issues around about:blank, but I have not found any reports just like this.

My tests show that Firefox does not show this behavior, but rather makes the new document inherit CSP from its loading document.

Here is a POC: <https://grodum.org/csptest/hey.html>

**VERSION**  

Chrome Version: Version 54.0.2840.71 (64-bit) + [stable, beta, or dev]  

Operating System: macosx 10.11.6 (15G1108)

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug.**

Demo: <https://grodum.org/csptest/hey.html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace, registers, exception record]**  

**Client ID (if relevant): [see link above]**

## Timeline

### el...@chromium.org (2016-11-28)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature]

### gr...@gmail.com (2016-11-28)

Mozilla is expicit about it here: https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy

Content from about:blank and javascript: URLs inherits the origin from the document that loaded the URL, since the URL itself does not give any information about the origin.

### do...@chromium.org (2016-11-28)

+mkwst - do you have thoughts on this? Tentatively assigning medium severity.

### do...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### mk...@chromium.org (2016-11-29)

It surprises me that Chrome's not inheriting the policy; the spec is pretty explicit about it: https://w3c.github.io/webappsec-csp/#initialize-document-csp. Sounds like a bug in our implementation.

### mk...@chromium.org (2016-11-29)

https://codereview.chromium.org/2530343006 up for review.

### sh...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e598765e4822eac833a547abca92ce87a1287dc0

commit e598765e4822eac833a547abca92ce87a1287dc0
Author: mkwst <mkwst@chromium.org>
Date: Wed Nov 30 12:36:42 2016

CSP: "local schemes" should inherit policy when window.opened.

https://w3c.github.io/webappsec-csp/#initialize-document-csp mandates
that resources with "local schemes" ('data:', 'blob:', 'filesystem:',
'about:') inherit the policy of their opening context when opened via
things like 'window.open'. We're not doing that, but we ought to.

BUG=669086
R=jochen@chromium.org

Review-Url: https://codereview.chromium.org/2530343006
Cr-Commit-Position: refs/heads/master@{#435233}

[add] https://crrev.com/e598765e4822eac833a547abca92ce87a1287dc0/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/cascade/cross-origin-window-open.html
[add] https://crrev.com/e598765e4822eac833a547abca92ce87a1287dc0/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/cascade/cross-origin-with-own-policy-window-open.html
[add] https://crrev.com/e598765e4822eac833a547abca92ce87a1287dc0/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/cascade/same-origin-window-open.html
[add] https://crrev.com/e598765e4822eac833a547abca92ce87a1287dc0/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/cascade/same-origin-with-own-policy-window-open.html
[modify] https://crrev.com/e598765e4822eac833a547abca92ce87a1287dc0/third_party/WebKit/Source/core/dom/Document.cpp


### sh...@chromium.org (2016-12-13)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2016-12-19)

Any more changes expected here, or can we close as Fixed?

### sh...@chromium.org (2016-12-27)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-01-17)

Marking as fixed, please re-open if that's not correct.

### sh...@chromium.org (2017-01-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-27)

Nice find!  The panel decided to award $1,000 for this report.  A member of our finance team will be in touch shortly.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************


### aw...@chromium.org (2017-01-27)

[Empty comment from Monorail migration]

### gr...@gmail.com (2017-01-30)

Awesome, thanks!

Btw, I must say I am very impressed with your communication and transparency with me from the moment I reported to you testing and triaging, fixing and code-reviewing.
Having reported security issues to many other companies before (even other parts of G), you guys are certainly leaders the field and the way you handle security issues leaves me with confidence in Chrome.

Nicolai Grødum

### sh...@chromium.org (2017-02-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-03)

Your change meets the bar and is auto-approved for M57. Please go ahead and merge the CL to branch 2987 manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mk...@chromium.org (2017-02-03)

I think this patch landed in M57 to begin with? https://storage.googleapis.com/chromium-find-releases-static/e59.html#e598765e4822eac833a547abca92ce87a1287dc0

### go...@chromium.org (2017-02-03)

Please merge your change to M57 branch 2987 before 5:00 PM Pt, Monday (02/06/) so we can pick it up for next week Beta release. Thank you.

### go...@chromium.org (2017-02-09)

Please merge your change to M57 branch 2987 before 5:00 PM PT, Friday 02/10 (sooner the better please) so we can take it in for next week beta release. Thank you.

### mk...@chromium.org (2017-02-09)

I still don't think this needs to be merged. It's already in 57. Dropping the merge flags, CCing govind@ to confirm that I'm holding omahaproxy correctly. :)

### go...@chromium.org (2017-02-09)

M57 was branched at Chromium revision 444943 and cl listed at #23 https://chromium.googlesource.com/chromium/src/+/e598765e4822eac833a547abca92ce87a1287dc0 {#435233} so no merged is needed. Thank you mkwst@.

### mk...@chromium.org (2017-02-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-08)

[Comment Deleted]

### aw...@chromium.org (2017-03-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/669086?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/511824]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086104)*

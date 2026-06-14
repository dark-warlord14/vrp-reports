# Security: Full screen notification overlap on Windows and Linux (take two)

| Field | Value |
|-------|-------|
| **Issue ID** | [40052479](https://issues.chromium.org/issues/40052479) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Linux, Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2020-06-03 |
| **Bounty** | $500.00 |

## Description

avi@ fixed a bug in https://crbug.com/chromium/1037730, which the reporter says has recurred in https://bugs.chromium.org/p/chromium/issues/detail?id=1037730#c26.

cthomp@ - we're wondering if Enamel should own this full-screen bubble? It's not really Avi's area.

## Attachments

- [screen.mov](attachments/screen.mov) (video/quicktime, 2.6 MB)

## Timeline

### ad...@google.com (2020-06-03)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>FullScreen]

### ch...@gmail.com (2020-06-03)

I'm able to repro this on Windows and Linux, the popup show up over the fullscreen notification. This bug doesn't affect MacOS.

### av...@chromium.org (2020-06-03)

Last year I committed https://crrev.com/c/1682667 which added z-ordering to Views, and used it to fix this once and for all on the Mac, so I’m not surprised re the Mac.

I need to look into what’s going on for the other platforms.

### [Deleted User] (2020-06-03)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-03)

[Empty comment from Monorail migration]

### mb...@chromium.org (2020-06-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-05)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-05)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-08)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-09)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2020-06-09)

Please apply appropriate OSs label. Thank you.

### ad...@google.com (2020-06-09)

A reminder govind@ - we still need you to write something here explaining why the OS field is important to you - https://docs.google.com/document/d/1LGcuyYVTte2UbMtEsEObHOyToJYhOVV-c-M9fUePUag/edit...

### av...@chromium.org (2020-06-12)

I’m not sure how my original fix worked here. It eliminated the race, but the issue here is that the WebContents doing the popup isn’t the child of the fullscreen WebContents, but the parent.

### av...@chromium.org (2020-06-15)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/339729451dfe8f286089f93da0a9e6ce3b83fb12

commit 339729451dfe8f286089f93da0a9e6ce3b83fb12
Author: Avi Drissman <avi@chromium.org>
Date: Fri Jun 19 14:16:01 2020

Fix fullscreen dropping for security

If a WebContents performs a UI-sensitive action (such as showing a
dialog or popup), we want to drop fullscreen from all related
WebContentses, and to prevent those WebContentses from gaining
fullscreen until the UI-sensitive situation is over.

Currently the search for related WebContentses is achieved by walking
up the opener and outer chains, but that misses related WebContentses
that are down those chains. These are one-directional chains that
aren't easily walked in the other direction.

This is fixed with two changes.

First, we keep a list of WebContentses that are in fullscreen, which
can then be searched to determine if they are down the chain from the
affected WebContents.

Second, when a request comes in to go fullscreen, we not only check if
the WebContents is prohibited from entering fullscreen, but we now
also check if one of the WebContentses up the chain is prohibited.

Bug: 1090835
Change-Id: I031e2e0a9ff79b387543a22ec3d643ab468d4d29
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2249090
Commit-Queue: Charlie Harrison <csharrison@chromium.org>
Reviewed-by: Charlie Harrison <csharrison@chromium.org>
Auto-Submit: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#780290}

[modify] https://crrev.com/339729451dfe8f286089f93da0a9e6ce3b83fb12/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/339729451dfe8f286089f93da0a9e6ce3b83fb12/content/browser/web_contents/web_contents_impl_browsertest.cc


### av...@chromium.org (2020-06-19)

chromium.khalil@gmail.com :

PTAL and try to repro once 339729451dfe8f286089f93da0a9e6ce3b83fb12 hits canary. I think this should fix it.

### ch...@gmail.com (2020-06-19)

I can now confirm this is fixed after r780290. Verified on Chromium 85.0.4178.0 r780294 on Windows (on Linux as well), the page loses full-screen after it shows a popup. Thanks Avi for the quick fix.

### av...@chromium.org (2020-06-19)

Thank you!

### [Deleted User] (2020-06-20)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-22)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-06-24)

Congrats! The Panel decided to award $500 for this report

### na...@google.com (2020-06-24)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1090835?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052479)*

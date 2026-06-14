# Security: URL bar spoofing on iOS with a very long URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40050513](https://issues.chromium.org/issues/40050513) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ju...@chromium.org |
| **Created** | 2019-10-24 |
| **Bounty** | $2,000.00 |

## Description

Chrome Version: 78.0.3904.59 beta  

Operating System: iOS

This is similar to <https://crbug.com/chromium/989497>.

**REPRODUCTION CASE**

1. Go to <https://lbstyle.github.io/x.html>
2. Click on the button
3. On the new page (about:blank), try to reload it and wait.
4. Then click on "Go to google.com" button.

Actual: Observe that ..tform.accounts.google.com URL displayed.

## Attachments

- [x.html](attachments/x.html) (text/plain, 291 B)
- [attack.html](attachments/attack.html) (text/plain, 502 B)
- deleted (application/octet-stream, 0 B)
- [IMG_7578.MP4](attachments/IMG_7578.MP4) (video/mp4, 1.7 MB)

## Timeline

### ch...@gmail.com (2019-10-24)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-10-24)

Thanks for the report! Adding the same set of iOS folks.

Because of the more complicated interaction, I'm bumping this down to medium. Also, not clear from the video, but if the progress bar doesn't settle, and/or if the page contents aren't fully interactive, this'll be further mitigated.

[Monorail components: UI>Browser>Navigation UI>Security>UrlFormatting]

### ju...@chromium.org (2019-10-24)

jdeblasio@ I think we can do better here, but I think we should at least move this to M79  / lower to severity-low.  The progress bar does indeed never settle.  That said, rewriting a reload page from about:// to chrome:// is wrong (and I think a relatively simple fix).  

### ch...@gmail.com (2019-10-24)

The content area is interactive, so the user can enter enter data.

### ch...@gmail.com (2019-10-24)

[Empty comment from Monorail migration]

### ju...@chromium.org (2019-10-24)

https://chromium-review.googlesource.com/c/chromium/src/+/1879328

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e3f10ed9d67b888132f570d89b753891585c64c1

commit e3f10ed9d67b888132f570d89b753891585c64c1
Author: Justin Cohen <justincohen@google.com>
Date: Thu Oct 24 19:49:29 2019

[ios] Don't rewrite transition reloads to chrome URLs.

iOS13 will commit a URL change when using window.open followed by a
child.location change.  If the browser triggers a reload here we
shouldn't rewrite URLs to chrome, as window.open to chrome URLs are
not allowed.

Bug: 1017564
Change-Id: I09384f4e6825c9ae34523458516b20715d4b4961
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1879328
Reviewed-by: Eugene But <eugenebut@chromium.org>
Commit-Queue: Justin Cohen <justincohen@chromium.org>
Cr-Commit-Position: refs/heads/master@{#709173}

[modify] https://crrev.com/e3f10ed9d67b888132f570d89b753891585c64c1/ios/web/navigation/navigation_manager_impl.mm
[modify] https://crrev.com/e3f10ed9d67b888132f570d89b753891585c64c1/ios/web/navigation/navigation_manager_impl_unittest.mm


### jd...@chromium.org (2019-10-24)

Thanks for getting started on this.

In general, we try to remain consistent by sticking with our severity guidelines: https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md

In this case, I'm considering the progress bar as a mitigation to sev-medium, but even there it's not much of a mitigation. A typical mitigation to sev-low would need something like a non-interactive body and/or only available on some sites under some circumstances.

Hopefully it's not too burdensome of a fix. Is the one in c#7 all that's needed, or is there additional work?

### ju...@chromium.org (2019-10-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-25)

[Empty comment from Monorail migration]

### ju...@chromium.org (2019-10-25)

[Empty comment from Monorail migration]

### ka...@google.com (2019-10-25)

Approved for M79 pending canary verification. Thanks for the unit test!

### sr...@chromium.org (2019-10-25)

Verified on M80.0.3950.0 canary. about:blank is displayed even after reload.

### na...@google.com (2019-10-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ju...@chromium.org (2019-10-28)

kariahda@ this was cherry picked in https://chromium-review.googlesource.com/c/chromium/src/+/1879679 to refs/branch-heads/3945

Is there something broken in this nag?

### ka...@google.com (2019-10-29)

Sheriffbot specifically looks for merge-approved label which is still present here. And merge-merged is not here.

I'll just remove merge-approved since this is already merged.

### na...@google.com (2019-11-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-11-21)

Congrats the Panel decided to reward $2,000 for this report. 

In the interests of keeping these vulnerabilities undisclosed until a patch is generally available to our users, please do not host the exploit on a publicly available website, instead attach the source files to the bug and provide reproduction steps. We thank you for your videos as these really help our triage process!

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-01-31)

This issue was migrated from crbug.com/chromium/1017564?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Navigation, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050513)*

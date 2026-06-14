# Security: Bypassing Chrome's File URI Restrictions with View-Source in Extensions

| Field | Value |
|-------|-------|
| **Issue ID** | [40074299](https://issues.chromium.org/issues/40074299) |
| **Status** | Accepted |
| **Severity** | Unknown |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | jk...@google.com |
| **Created** | 2023-10-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

In the latest version of Chrome, navigation to the file URI is disabled when "Allow File Access" is turned off. This change addresses most file access vulnerabilities in extensions and aims to prevent future exploitations. However, I've discovered a method where this restriction can be bypassed by an extension using a combination of file URI and view-source.

**VERSION**  

Chrome Version: 120.0.6050.0 (Official Build) canary (64-bit) (cohort: Clang-64)

**REPRODUCTION CASE**

1. Install the attached extension. Make sure to disable "Allows access to file URLs".
2. Observe that navigation to the file URL has occurred (even though "Allow access to file URLs" is disabled).

**CREDIT INFORMATION**  

Reporter credit: Shaheen Fazim

## Attachments

- [demo.mp4](attachments/demo.mp4) (video/mp4, 3.0 MB)
- [background.js](attachments/background.js) (text/plain, 87 B)
- [manifest.json](attachments/manifest.json) (text/plain, 180 B)
- [error.png](attachments/error.png) (image/png, 24.1 KB)
- [changes-to-file-scheme.png](attachments/changes-to-file-scheme.png) (image/png, 80.7 KB)

## Timeline

### [Deleted User] (2023-10-06)

[Empty comment from Monorail migration]

### wf...@chromium.org (2023-10-06)

Hi thanks for your report, I agree that it appears this extension, with tabs permission, can create a tab to point to the file, but I'm not sure this means that the extensions is necessarily able to read this data, since it's contained in a different origin, and is not loaded directly within the extension. Are you able to demonstrate that the extension can read this e.g. you could print out an entry from the hosts file to console, or something like that?

I am looping in some extension folks to get their opinions as well, while we work together to try and triage the impact.

I await your reply.

[Monorail components: Platform>Extensions]

### fa...@gmail.com (2023-10-06)

[Comment Deleted]

### [Deleted User] (2023-10-06)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fa...@gmail.com (2023-10-06)

[Comment Deleted]

### fa...@gmail.com (2023-10-06)

Other similar older issues: crbug.com/1113565, crbug.com/1467169

I believe the new security measure, which aims to completely prevent the loading of file URIs, could effectively block such vulnerabilities. However, this method could circumvent this security mechanism.

### wf...@chromium.org (2023-10-06)

thanks for the additional context, I am adding caseq@chromium.org who was involved in those fixes to comment on whether or not this bypass has security implications or not.

### ca...@chromium.org (2023-10-11)

I don't immediately see whether this is exploitable. In the particular case of DevTools, we do check inner URLs with the intent of catching cases like this. Extensions also don't seem to regard this as a valid scheme for extensions (https://source.chromium.org/chromium/chromium/src/+/main:extensions/common/url_pattern.cc;drc=f5bdc89c7395ed24f1b8d196a3bdd6232d5bf771;l=31). But I may as well be missing some vectors. +dsv@ as he spent some time looking into similar problems and may recall some tricks that I don't.

### kr...@chromium.org (2023-10-11)

Solomon can you take a look as well as extensions are involved?

### fa...@gmail.com (2023-10-11)

I would like to provide further clarification based on my issue crbug.com/1468620 (duplicate) which is similar to crbug.com/1385343 (fixed). Upon retesting in the latest Chrome update, I found out that the vulnerability no longer works, displaying the error "cannot navigate to file URL without local file access" which is a new security mechanism implemented by Chrome to restrict opening file URIs [1]. Later, I attempted to bypass this, discovering that the new security mechanism could be circumvented by prefixing "view-source" to the file URL. Consequently, I was once again able to access the local files of the victim.

[1] - https://groups.google.com/a/chromium.org/g/chromium-extensions/c/ZtCvVISQU54/m/tOjjlzkfAgAJ


### fa...@gmail.com (2023-10-11)

[Comment Deleted]

### fa...@gmail.com (2023-10-11)

[Empty comment from Monorail migration]

### kr...@google.com (2023-10-11)

Solomon can you take a look? I'm marking it as medium for now, as an malicious extension would need to be installed but I am not clear about the security model for extensions so feel free to update.

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### so...@chromium.org (2023-10-12)

I'm planning on trying to reproduce this bug this week.

### [Deleted User] (2023-10-12)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2023-10-12)

Jun, do you mind taking a look?

I think this is a bit different than some of the other risks associated with opening file URLs (because a viewsource would never result in the file executing... right?), but it would still be good to fix.

I'd also lean towards this being a Security-Severity-Low and removing RBS, given the restriction on file URL navigation is very new, but I'll leave that up to you.

### jk...@google.com (2023-10-12)

I don't think this is a security issue, as view-source: wouldn't allow JS execution when rendering content (which is the requirement of exploit primitive we wanted to prevent).

I can work on fixing this if this is required because of consistency, but I don't think this requires blocking stable.

### be...@google.com (2023-10-13)

Adding Hotlist-RBS-Removed for tracking purposes.

### fa...@gmail.com (2023-10-13)

[Comment Deleted]

### jk...@google.com (2023-10-13)

Unfortunately, https://crbug.com/chromium/1418820 does not entirely remove the ability to navigate to file URLs (see https://bugs.chromium.org/p/chromium/issues/detail?id=1418820#c14).

### jk...@google.com (2023-10-13)

And it seems like this bug is already public.
https://bugs.chromium.org/p/chromium/issues/detail?id=1418820#c17

### fa...@gmail.com (2023-10-13)

Yes, you're right. Thank you for sharing.

### jk...@google.com (2023-10-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-10-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/99530c08b7b5c5e50f533fd7ad0dfcb205761134

commit 99530c08b7b5c5e50f533fd7ad0dfcb205761134
Author: Jun Kokatsu <jkokatsu@google.com>
Date: Tue Oct 17 20:58:32 2023

Don't allow view-source scheme with file URLs in tabs API

As a consistency for recent deprecation of navigations to file URLs in
tabs and windows APIs (crbug.com/1418820), ensure that view-source
schemes are not pointing to file URLs as well.

Bug: 1490617
Change-Id: Ieefce5a62bb638c87d78cf8342541b777aaa9556
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4942979
Auto-Submit: Jun Kokatsu <jkokatsu@google.com>
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Jun Kokatsu <jkokatsu@google.com>
Cr-Commit-Position: refs/heads/main@{#1211083}

[modify] https://crrev.com/99530c08b7b5c5e50f533fd7ad0dfcb205761134/chrome/browser/extensions/extension_tab_util.cc
[modify] https://crrev.com/99530c08b7b5c5e50f533fd7ad0dfcb205761134/chrome/browser/extensions/extension_tab_util_unittest.cc


### jk...@google.com (2023-10-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-10-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-10-26)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-26)

The Chrome VRP Panel has decided to extend a reward to ndevtk in appreciation for their contributions on https://crbug.com/chromium/1418820 that resulted in this discovery and fix. Since this issue was already conveyed in https://crbug.com/chromium/1418820 the day prior to this report and they collaborated on that issue, we felt that the fair thing here is to extend the reward to them. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-10-28)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-24)

This issue was migrated from crbug.com/chromium/1490617?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedinto: crbug.com/chromium/1418820]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40074299)*

# Security: chrome.debugger can attach to any target

| Field | Value |
|-------|-------|
| **Issue ID** | [40090278](https://issues.chromium.org/issues/40090278) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools, Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | dg...@chromium.org |
| **Created** | 2018-01-24 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The chrome.debugger API is only supposed to attach to targets for which the extension has scripting access. This is enforced in the chrome.debugger.attach method.

The chrome.debugger API seems to use the latest protocol version (even though the only supported versions are 1.0, 1.1 and 1.2 according to DevToolsAgentHost::IsSupportedProtocolVersion [1]).

With the latest protocol version, extensions can attach to any target with the Target.attachToTarget message, and effectively bypass the validation. As a result, extensions can automatically debug any page.

**VERSION**  

Chrome Version: 63.0.3239.132 (stable), 66.0.3330.0 (canary)

**REPRODUCTION CASE**  

Install the attached extension and observe an alert dialog at chrome://version.  

The impact is serve: program execution using <https://crbug.com/chromium/798222>, and even if that bug is fixed, local file access by flipping the "Allow access to file URLs" flag at chrome://extensions, or any other powerful feature via chrome://flags.

SUGGESTED FIX  

At the very least, the Target DevTools domain should be disabled.

But I think that the latest protocol version is too powerful and not designed for extension usage in mind, so until the protocol has undergone a security audit, I suggest to enforce that the messages in the chrome.debugger API must match the requested protocol version (1.2 or lower).

[1] <https://chromium.googlesource.com/chromium/src/+/5bb32276369f855317b3fd647670f6ccf905a27a/content/browser/devtools/devtools_agent_host_impl.cc#86>

## Attachments

- [debugger-target-bypass.zip](attachments/debugger-target-bypass.zip) (application/octet-stream, 1.3 KB)

## Timeline

### el...@chromium.org (2018-01-24)

Nice find, thanks!

[Monorail components: -Platform>Extensions Platform>Extensions>API]

### me...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2018-01-24)

I have audited the DevTools protocol today, and looked for privilege escalation in extensions (local file access and privileged code execution), and reported https://crbug.com/chromium/805445 and https://crbug.com/chromium/805557 .

Given the usefulness of the DevTools protocol, I retract my second suggestion (restricting the DevTools protocol to <=1.2) and recommend to modify the chrome.debugger API to enforce the existing target checks on all methods in the "Target.*" DevTools domain.

This could be an extensions/-only change (validating messages in chrome/browser/extensions/api/debugger/debugger_api.cc).
This may also involve changes the DevTools backend (e.g. adding logic to enforce that clients can only access certain web origins/schemes or processes).

### sh...@chromium.org (2018-01-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-07)

dgozman: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-02-22)

dgozman: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-03-30)

Friendly ping from the security sheriff. Can we get any update on this?

### dg...@chromium.org (2018-03-30)

Now that we have a mechanism of restricted clients in place, this should be easy to fix.

### bu...@chromium.org (2018-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/46f5cfb6414c04b65cba4ec59ca992f338934fc9

commit 46f5cfb6414c04b65cba4ec59ca992f338934fc9
Author: Dmitry Gozman <dgozman@chromium.org>
Date: Mon Apr 02 19:55:26 2018

[DevTools] Do not create target handler for restricted sessions

Bug: 805224
Change-Id: I08528e44e79d0a097cfe72ab4949dda538efd098
Reviewed-on: https://chromium-review.googlesource.com/988695
Reviewed-by: Pavel Feldman <pfeldman@chromium.org>
Commit-Queue: Dmitry Gozman <dgozman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#547496}
[modify] https://crrev.com/46f5cfb6414c04b65cba4ec59ca992f338934fc9/content/browser/devtools/render_frame_devtools_agent_host.cc


### dg...@chromium.org (2018-04-03)

This should be fixed now.

### sh...@chromium.org (2018-04-04)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-16)

And $2,000 for this report, thanks as ever!

### aw...@chromium.org (2018-04-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/805224?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools, Platform>Extensions>API]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090278)*

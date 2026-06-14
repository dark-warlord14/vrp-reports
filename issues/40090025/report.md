# Security: DevTools protocol can be abused to download and run external programs

| Field | Value |
|-------|-------|
| **Issue ID** | [40090025](https://issues.chromium.org/issues/40090025) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools, Platform>Extensions, UI>Browser>Downloads |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | dg...@chromium.org |
| **Created** | 2018-01-01 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

chrome://downloads can launch external programs after an explicit user gesture. After <https://crbug.com/chromium/668653>, there is even an explicit check that verifies that dangerous operations are initiated by a user gesture.

The DevTools protocol can run scripts with a user gesture, so this check is rendered useless.  

In the past week, I have found three different ways to run arbitrary code in WebUI pages via DevTools:  

<https://crbug.com/chromium/797497> + <https://crbug.com/chromium/797500>  

<https://crbug.com/chromium/798163>  

<https://crbug.com/chromium/798184>  

All of these vulnerabilities allow an extension to launch external programs without further user interaction through this bug.

Even if these bugs are fixed, then this vulnerability can still be exploited through the remote debugging protocol.  

In that situation, the data in the browser is naturally no longer secure. However, it should not be possible to also compromise the whole system via arbitrary executables.

**VERSION**  

Chrome Version: 63.0.3239.108 (stable) + 65.0.3309.0 (canary)

**REPRODUCTION CASE**  

Load the attached extension, and observe that paint is launched (on Windows). The extension uses <https://crbug.com/chromium/797497> + <https://crbug.com/chromium/797500> to run scripts in chrome://downloads.  

See the attached video for a demonstration.

I suggest to ignore the userGesture flag for the DevTools protocol in privileged/webui pages, for the following DevTools methods (this exhaustive list is based on the protocol definition at [1]):

- Runtime.callFunctionOn
- Runtime.evaluate

[1] <https://chromium.googlesource.com/v8/v8.git/+/3cbf26e8a21aa76703d2c3c51adb9c96119500da/src/inspector/js_protocol.pdl>

## Attachments

- [devtools-mspaint.zip](attachments/devtools-mspaint.zip) (application/octet-stream, 3.6 KB)
- [devtools-mspaint.ogv](attachments/devtools-mspaint.ogv) (video/ogg, 675.1 KB)

## Timeline

### el...@chromium.org (2018-01-02)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-01-03)

I couldn't quite get this to reproduce on Linux (I don't have a Windows machine), it caused my editor to open, I strongly suspect that it is reproducible on Windows.

I'm unsure if double-clicking a downloaded file will cause the file to be executed on the other platforms.

dgozman@ do you think this issue should be fixed on the dev-tools side?

### dg...@chromium.org (2018-01-03)

Not sure what we can do here apart from disallowing to debug chrome:// pages. Running under user gesture is essential to DevTools. We should fix underlying issues so one cannot script DevTools from extension at least.


### ro...@robwu.nl (2018-01-03)

I have suggested to ignore the userGesture flag when running in a privileged page.
If there is a use case for wanting to enable user gestures for DevTools on privileged pages, guard it by a default-off command-line flag, so that the average user is not at risk whenever a DevTools client is compromised.

What do you think of this?

### sh...@chromium.org (2018-01-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-17)

dgozman: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-01-23)

+asanka as this is another bug that could potentially be mitigated by a fix to https://crbug.com/chromium/595841.

[Monorail components: UI>Browser>Downloads]

### me...@chromium.org (2018-01-23)

+devlin for the extension angle. Is there anything we can do to tame chrome.debugger API?

[Monorail components: Platform>Extensions]

### me...@chromium.org (2018-01-23)

Upon further inspection, this looks similar to https://crbug.com/chromium/666824: Both use extensions + devtools + debugger + downloads to launch files on chrome://downloads, but there are some significant differences (https://crbug.com/chromium/666824 uses downloads.open whereas this one doesn't).

### ro...@robwu.nl (2018-01-23)

@#7 Can you cc me on https://crbug.com/chromium/595841 ?

@#8 The chrome.debugger API does not necessarily have a vulnerability here. It is only used in my exploit to automatically open the DevTools window (using the feature from https://crbug.com/chromium/410958) in order to exploit the vulnerability in attached DevTools instance.

If you think that this feature needs to be constrained, I suggest to add a check to only accept the Page.setAutoAttachToCreatedPages command if the user has enabled the "Enable developer mode" option at chrome://extensions . In this way, developers still have the ability to automatically open the DevTools.

But even if the feature were to be locked, users who manually open the DevTools are still fully susceptible to the consequences of the reported vulnerability.

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-31)

dgozman: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-02-14)

dgozman: Any updates for this is a high severity bug?

### ke...@chromium.org (2018-02-28)

This should only be Medium severity, but still needs to be fixed.

dgozman@: Are you able to do anything with this, or else pass it on to someone else who can?

### dg...@chromium.org (2018-02-28)

We have a plan to address this, together with other chrome.debugger issues.

### bu...@chromium.org (2018-03-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2aec794f26098c7a361c27d7c8f57119631cca8a

commit 2aec794f26098c7a361c27d7c8f57119631cca8a
Author: Dmitry Gozman <dgozman@chromium.org>
Date: Mon Mar 05 20:27:54 2018

[DevTools] Do not allow chrome.debugger to attach to web ui pages

If the page navigates to web ui, we force detach the debugger extension.

TBR=alexclarke@chromium.org

Bug: 798222
Change-Id: Idb46c2f59e839388397a8dfa6ce2e2a897698df3
Reviewed-on: https://chromium-review.googlesource.com/935961
Commit-Queue: Dmitry Gozman <dgozman@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Pavel Feldman <pfeldman@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Cr-Commit-Position: refs/heads/master@{#540916}
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/chrome/browser/extensions/api/debugger/debugger_api.h
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/chrome/browser/extensions/api/debugger/debugger_api_constants.cc
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/chrome/browser/extensions/api/debugger/debugger_api_constants.h
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/chrome/test/data/extensions/api_test/debugger/background.js
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/chrome/test/data/extensions/api_test/debugger_extension/background.js
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/content/browser/devtools/browser_devtools_agent_host.cc
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/content/browser/devtools/browser_devtools_agent_host.h
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/content/browser/devtools/devtools_agent_host_impl.cc
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/content/browser/devtools/devtools_agent_host_impl.h
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/content/browser/devtools/devtools_session.cc
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/content/browser/devtools/devtools_session.h
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/content/browser/devtools/render_frame_devtools_agent_host.cc
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/content/browser/devtools/render_frame_devtools_agent_host.h
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/content/browser/devtools/service_worker_devtools_agent_host.cc
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/content/browser/devtools/service_worker_devtools_agent_host.h
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/content/browser/devtools/shared_worker_devtools_agent_host.cc
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/content/browser/devtools/shared_worker_devtools_agent_host.h
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/content/public/browser/devtools_agent_host.h
[modify] https://crrev.com/2aec794f26098c7a361c27d7c8f57119631cca8a/headless/public/util/testing/mock_devtools_agent_host.h


### dg...@chromium.org (2018-03-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-06)

[Empty comment from Monorail migration]

### pf...@chromium.org (2018-03-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

This bug requires manual review: M66 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-03-19)

Seems like a fairly large change. awhalley@ any issues with taking this in M67 instead of 66?

### ab...@chromium.org (2018-03-23)

Checking with awhalley, we should consider this merge. dgozman@: how safe is this merge overall? I'm a bit worried about the size of the change. 

### aw...@chromium.org (2018-03-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-03-26)

Thanks Rob! The VRP panel decided to reward $2,000 for this report.

### ab...@chromium.org (2018-03-26)

Approving merge to M66. Branch:3359

### aw...@chromium.org (2018-03-26)

[Empty comment from Monorail migration]

### ab...@chromium.org (2018-04-11)

checking with dgozman@, let's target this for M67. 

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/798222?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools, Platform>Extensions, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090025)*

# Security: compromised renderer is able to send extension message to another tab

| Field | Value |
|-------|-------|
| **Issue ID** | [40060492](https://issues.chromium.org/issues/40060492) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Sandbox>SiteIsolation, Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ym...@ym.kim |
| **Assignee** | lu...@chromium.org |
| **Created** | 2022-08-04 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

A compromised renderer is able to send an extension message to another tab.

The browser process (extensions::MessageService) does not check ExtensionHostMsg\_OpenChannelToTab message came from an extension process or a process with access to chrome.tabs.sendMessage API.

Therefore, a compromised renderer can spoof an ExtensionHostMsg\_OpenChannelToTab.

Furthermore, the message to tab does not include MessageSender information such as url, origin, tab, so there is no way for content scripts to verify the message came from the extension.

Prior to <https://crrev.com/1008190>, the tabId starts from 0, so the attacker can brute-force the tab ID from zero. After the revision, the attacker can brute-force the tab ID from its tab ID. I'm not sure the compromised renderer can retrieve it, but many extensions allow retrieving its tab ID.

**VERSION**  

Chrome Version: 106.0.5219.0

**REPRODUCTION CASE**

1. Apply the attached patch.
2. Install the attached extension.
3. Open a new tab, e.g., <https://example.com>.
4. Open another tab, e.g., <https://example.org>.
5. Check the alert is shown in the first tab.

**CREDIT INFORMATION**  

Reporter credit: Young Min Kim (@ylemkimon), CompSec Lab at Seoul National University

## Attachments

- [renderer.patch](attachments/renderer.patch) (text/plain, 2.5 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 229 B)
- [background.js](attachments/background.js) (text/plain, 99 B)
- [content.js](attachments/content.js) (text/plain, 219 B)

## Timeline

### [Deleted User] (2022-08-04)

[Empty comment from Monorail migration]

### ym...@ym.kim (2022-08-04)

The message also seems to be dispatched to "runtime.onMessage" listeners in the extension page opened in a tab. Since the url and tab property of MessageSender is undefined, it can be used to bypass sender checks.


### ma...@google.com (2022-08-05)

Devlin, PTAL at this one too?



### [Deleted User] (2022-08-05)

[Empty comment from Monorail migration]

### rd...@chromium.org (2022-08-05)

Good find!

This sounds like a great next step for lukasza@'s recent work.  Lukasz is out right now, but I don't think this is actually a medium severity bug: this results in a spoofed message being sent to an extension content script, but content scripts are relatively (but not completely) unpermissioned.  Additionally, this doesn't give the sender direct access to the content script execution environment, so it requires crafting a specific message and an extension that returns sensitive data as a result.  Finally, content scripts are already (and fundamentally) prone to some kinds of attacks as they operate in the same world as untrusted web page code.  A meaningful difference between this and a "normal" renderer exploit is that it could leak cross-origin information, given the right content script.

I *do* agree this is a security bug, but think it's more of a Low vulnerability than Medium; I'm tentatively changing the label accordingly.  Security sheriff, feel free to change back if you disagree.

### ym...@ym.kim (2022-08-05)

As mentioned in https://crbug.com/chromium/1350111#c2, the message is also dispatched to (high-privileged) scripts in extension contexts. Still, the background page is not a tab, so it cannot send message to the background page, and a compromised renderer cannot navigate to non-web-accessible-resources, so I agree it'd be a mitigating factor.

### [Deleted User] (2022-08-06)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lu...@chromium.org (2022-08-25)

[Empty comment from Monorail migration]

[Monorail components: Internals>Sandbox>SiteIsolation Platform>Extensions]

### lu...@chromium.org (2022-08-25)

WIP CL: https://chromium-review.googlesource.com/c/chromium/src/+/3857925

### gi...@appspot.gserviceaccount.com (2022-08-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6ad87925fa9a9fa10b66adbbccf31cf53987a24f

commit 6ad87925fa9a9fa10b66adbbccf31cf53987a24f
Author: Lukasz Anforowicz <lukasza@chromium.org>
Date: Wed Aug 31 16:46:30 2022

Validate `extension_id` in ExtensionHostMsg_OpenChannelToTab.

Bug: 1350111
Change-Id: Ideedc370adaebd1db8b9bedf70f16a121a3ad83d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3857925
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Commit-Queue: Łukasz Anforowicz <lukasza@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1041588}

[modify] https://crrev.com/6ad87925fa9a9fa10b66adbbccf31cf53987a24f/chrome/browser/extensions/extension_security_exploit_browsertest.cc
[modify] https://crrev.com/6ad87925fa9a9fa10b66adbbccf31cf53987a24f/extensions/browser/api/messaging/messaging_api_message_filter.cc
[modify] https://crrev.com/6ad87925fa9a9fa10b66adbbccf31cf53987a24f/extensions/browser/bad_message.h
[modify] https://crrev.com/6ad87925fa9a9fa10b66adbbccf31cf53987a24f/tools/metrics/histograms/enums.xml


### lu...@chromium.org (2022-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-07)

Congratulations, Young Min Kim! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us - nice work! 

### am...@google.com (2022-10-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-27)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-12-07)

This issue was migrated from crbug.com/chromium/1350111?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060492)*

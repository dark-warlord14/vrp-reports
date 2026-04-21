# Security: Source maps support for file:// URLs gives devtools_page extensions local file access

| Field | Value |
|-------|-------|
| **Issue ID** | [40060465](https://issues.chromium.org/issues/40060465) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2022-4955 |
| **Reporter** | ma...@fingerprint.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2022-08-01 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Extensions using devtools\_page can read local files because source maps support file:// URLs without restrictions.

**VERSION**  

Chrome Version: 103.0.5060.134 (Official Build) (arm64)  

Operating System: macOS Monterey Version 12.3

**REPRODUCTION CASE**  

The following information is macOS-specific.

1. Install the attached extension. Make sure to disable "Allows access to file URLs".
2. Open Developer Tools on the new tab opened by the extension.
3. You'll see an alert box with the contents of the /etc/hosts file.

The extension opens a new page with a single script tag containing only a sourceMappingURL reference pointing at `data:application/json,{"version":3,"sources":["file:///etc/hosts"]}`.

When Developer Tools are opened, the file from the sources list will be loaded as a resource. As a result the devtools\_page can access its contents via chrome.devtools.inspectedWindow.getResources.

In theory, any page could assist a malicious extension in reading local files, by crafting a script or style tag with a specific sourceMappingURL.

**CREDIT INFORMATION**  

Reporter credit: Martin Bajanik (fingerprint.com)

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 200 B)
- [devtools.js](attachments/devtools.js) (text/plain, 217 B)
- [devtools.html](attachments/devtools.html) (text/plain, 35 B)
- [background.js](attachments/background.js) (text/plain, 186 B)

## Timeline

### [Deleted User] (2022-08-01)

[Empty comment from Monorail migration]

### bh...@google.com (2022-08-02)

I do not have a mac device, so unable to reproduce. Adding in extension folks to comment on whether this is considered a bug.

[Monorail components: Platform>Extensions]

### ma...@fingerprint.com (2022-08-03)

To reproduce on a Windows machine, it's enough to reference a different file in the sources list in background.js, for example sourceMappingURL=data:application/json,{"version":3,"sources":["file:///C:/Windows/System32/Drivers/etc/hosts"]}.

### ma...@google.com (2022-08-03)

https://crbug.com/chromium/1349146#c2 CCd the wrong Devlin, I think.

Extensions folks, could you help with assessing this, please?

### ma...@google.com (2022-08-04)

[Empty comment from Monorail migration]

### rd...@chromium.org (2022-08-04)

Oh, this is a fun one.  Thanks for the report!

There's a few mitigating factors to this:
- User has to install a malicious extension
- The malicious extension uses the devtools permission, which warns the user about accessing all data on all web sites
- The user has to open devtools

However, none of those should grant file access.  Tentatively assigning security severity medium based on the barriers to entry, but security sheriffs, feel free to change.

Assigning to dsv@ as a devtools owner; can you take a look?  Offhand, I can think of two potential solutions here:
1) Require the extension to have file permission to use a source mapping of a local file
2) Only expose a file-backed source mapping resource via getResources if the extension has file access

2) is more principled, but 1) is likely more straightforward (and seems like a reasonable compromise).  I'd be interested in any other suggestions, too.

### ma...@google.com (2022-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-05)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-16)

dsv: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-30)

dsv: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/28cfaf314c9a3bbc29bdf4d335f220913fcc0c3a

commit 28cfaf314c9a3bbc29bdf4d335f220913fcc0c3a
Author: Danil Somsikov <dsv@chromium.org>
Date: Tue Sep 27 15:36:55 2022

Skip file URLs in chrome.devtools.inspectedWindow.getResources if the
extensions doesn't have file access.

Chromium counterpart at crrev.com/c/3921760

Bug: 1349146
Change-Id: I44fa9d13f7a8ebf2c3cde89e8e92a23686c49566
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3921601
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Wolfgang Beyer <wolfi@chromium.org>
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>

[modify] https://crrev.com/28cfaf314c9a3bbc29bdf4d335f220913fcc0c3a/front_end/models/extensions/ExtensionAPI.ts
[modify] https://crrev.com/28cfaf314c9a3bbc29bdf4d335f220913fcc0c3a/front_end/models/extensions/ExtensionServer.ts


### ma...@fingerprint.com (2022-10-04)

Just for completeness, the local resource contents can also be read through at least one other method: `chrome.devtools.inspectedWindow.onResourceAdded`.

Maybe `onResourceContentCommitted` too (but I didn't confirm), or even completely different ways that might be available besides the inspectedWindow object (not sure if there are any other though).

### gi...@appspot.gserviceaccount.com (2022-10-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1b128e4d9ee100989e23ed66a83b9e9b6edbdd53

commit 1b128e4d9ee100989e23ed66a83b9e9b6edbdd53
Author: Danil Somsikov <dsv@chromium.org>
Date: Wed Oct 05 15:13:25 2022

Propagate extension file access and test that file URLs are skipped in chrome.devtools.inspectedWindow.getResources if the
extensions doesn't have it.

Devtools frontend counterpart at crrev.com/c/3921601

Bug: 1349146
Change-Id: I485ed6bc42e411beac2101296d603dac82970b5a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3921760
Reviewed-by: Wolfgang Beyer <wolfi@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1055289}

[modify] https://crrev.com/1b128e4d9ee100989e23ed66a83b9e9b6edbdd53/chrome/browser/devtools/devtools_browsertest.cc
[modify] https://crrev.com/1b128e4d9ee100989e23ed66a83b9e9b6edbdd53/chrome/browser/devtools/devtools_ui_bindings.cc


### gi...@appspot.gserviceaccount.com (2022-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/56210838235e34b8e08b719331e5115c75ca13f3

commit 56210838235e34b8e08b719331e5115c75ca13f3
Author: Danil Somsikov <dsv@chromium.org>
Date: Wed Oct 05 13:17:58 2022

Hanlding other cases where devtools extension wo/ file access may read file resources.

Bug: 1349146
Change-Id: I3cda5f8d165aaa7f675a2363726de25012b96f7f
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3936285
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Wolfgang Beyer <wolfi@chromium.org>
Commit-Queue: Wolfgang Beyer <wolfi@chromium.org>

[modify] https://crrev.com/56210838235e34b8e08b719331e5115c75ca13f3/front_end/models/extensions/ExtensionAPI.ts
[modify] https://crrev.com/56210838235e34b8e08b719331e5115c75ca13f3/front_end/models/extensions/ExtensionServer.ts


### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### ds...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-09)

Congratulations, Martin! The VRP Panel has decided to award you $5,000 for this report. A member of our finance team will be in touch with you to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### am...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-04-03)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-26)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

Oops, I added the wrong CVE label to this bug - thank you Amy for catching my mistake! Updating to the correct one: CVE-2022-4955

### pg...@google.com (2023-08-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1349146?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060465)*

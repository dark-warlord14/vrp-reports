# Security: UAF in PageHandler::Navigate

| Field | Value |
|-------|-------|
| **Issue ID** | [40055226](https://issues.chromium.org/issues/40055226) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools, Platform>Extensions>API, UI>Browser>Navigation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2021-03-16 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

One of the methods available via the Chrome DevTools protocol is Page.navigate. That method allows the caller to navigate the target page to a specified URL.

When an extension uses that method to navigate a crashed page to a restricted URL, the debugging session will be detached. However, that occurs in the middle of PageHandler::Navigate, resulting in the PageHandler object being deleted midway through the method.

**VERSION**  

Chrome Version: 89.0.4389.90 (stable), 91.0.4448.0 (canary)  

Operating System: Windows 10, version 20H2

**REPRODUCTION CASE**

1. Install the attached extension.
2. The extension will create a create a tab, attach the debugger to it, crash the associated page, then issue the following Page.navigate call:

chrome.debugger.sendCommand({tabId: tab.id}, "Page.navigate", {url: "chrome://settings/"});

This will result in a use-after-free in the browser process. You can verify that by running the browser under a debugger, though you'll need to manually kill the page created by the extension. This is because the method used to crash the page (the Page.crash DevTools protocol method) will simply result in the debugger breaking.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 1.4 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 197 B)

## Timeline

### de...@gmail.com (2021-03-16)

The debugging session is detached as a result of the following call within PageHandler::Navigate:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/protocol/page_handler.cc;l=506;drc=09a4396a448775456084fe36bb84662f5757d988

The reason that the session is detached is that the URL being navigated to is restricted (and therefore can't be debugged by an extension).

That results in the PageHandler object being deleted (along with the other domain handlers) once LoadURLWithParams has finished executing.

### [Deleted User] (2021-03-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2021-03-17)

[Empty comment from Monorail migration]

[Monorail components: Platform>DevTools Platform>Extensions>API UI>Browser>Navigation]

### cr...@chromium.org (2021-03-17)

I suspect carloscab's CL is unrelated to this, and that someone familiar with DevTools and PageHandler may need to take a look.  The problem probably goes back at least as far as pfeldman's r532140, but probably even before (since there was a LoadURL call there before that CL added LoadURLWithParams).

caseq@: Can you help find an appropriate owner in DevTools?  I suspect the code will need to handle the case the PageHandler is deleted during the LoadURLWithParams case, without proceeding to execute code in the deleted object.  Thanks!

(CC'ing danakj@ and dcheng@, as we've been looking at related issues.)

### ha...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-17)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-25)

caseq@ ping - please help move this to the right owner.

### ca...@chromium.org (2021-03-26)

[Empty comment from Monorail migration]

### ca...@chromium.org (2021-03-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ff5e70191ec701cce4f84aaa25cd676376253a8a

commit ff5e70191ec701cce4f84aaa25cd676376253a8a
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Tue Mar 30 08:04:11 2021

DevTools: expect PageHandler may be destroyed during Page.navigate

Bug: 1188889
Change-Id: I5c2fcca84834d66c46d77a70683212c2330177a5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2787756
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#867507}

[modify] https://crrev.com/ff5e70191ec701cce4f84aaa25cd676376253a8a/chrome/browser/extensions/api/debugger/debugger_apitest.cc
[add] https://crrev.com/ff5e70191ec701cce4f84aaa25cd676376253a8a/chrome/test/data/extensions/api_test/debugger_navigate_to_forbidden_url/background.js
[add] https://crrev.com/ff5e70191ec701cce4f84aaa25cd676376253a8a/chrome/test/data/extensions/api_test/debugger_navigate_to_forbidden_url/manifest.json
[modify] https://crrev.com/ff5e70191ec701cce4f84aaa25cd676376253a8a/content/browser/devtools/protocol/page_handler.cc
[modify] https://crrev.com/ff5e70191ec701cce4f84aaa25cd676376253a8a/content/browser/devtools/render_frame_devtools_agent_host.cc


### ca...@chromium.org (2021-03-30)

Adrian, does it look like something worth merging to m90 to you?

### [Deleted User] (2021-03-30)

This bug requires manual review: We are only 13 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2021-03-31)

> 1. Does your merge fit within the Merge Decision Guidelines?

Yes, as a P1 security issue (though not sure if it's really P1, deferring to adetaylor@ on this)

> 2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/2787756

> 3. Has the change landed and been verified on ToT?
Yes

> 4. Does this change need to be merged into other active release branches (M-1, M+1)?
No

> 5. Why are these changes required in this milestone after branch?
Because of discovery and fixing timeline.

> 6. Is this a new feature?
No

> 7. If it is a new feature, is it behind a flag using finch?

N/A


### [Deleted User] (2021-03-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-31)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-31)

This didn't gain a security severity, so attaching one here - I believe it's High as a browser process crash mitigated by the need to install an extension.

On that basis, approving merge to M90. Please merge to branch 4430.

### gi...@appspot.gserviceaccount.com (2021-04-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f79751ee25416fdc27faef6308efec5c3e543ee1

commit f79751ee25416fdc27faef6308efec5c3e543ee1
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Thu Apr 01 06:51:26 2021

[m90] DevTools: expect PageHandler may be destroyed during Page.navigate

(cherry picked from commit ff5e70191ec701cce4f84aaa25cd676376253a8a)

Bug: 1188889
Change-Id: I5c2fcca84834d66c46d77a70683212c2330177a5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2787756
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#867507}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2798538
Cr-Commit-Position: refs/branch-heads/4430@{#968}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/f79751ee25416fdc27faef6308efec5c3e543ee1/chrome/browser/extensions/api/debugger/debugger_apitest.cc
[add] https://crrev.com/f79751ee25416fdc27faef6308efec5c3e543ee1/chrome/test/data/extensions/api_test/debugger_navigate_to_forbidden_url/background.js
[add] https://crrev.com/f79751ee25416fdc27faef6308efec5c3e543ee1/chrome/test/data/extensions/api_test/debugger_navigate_to_forbidden_url/manifest.json
[modify] https://crrev.com/f79751ee25416fdc27faef6308efec5c3e543ee1/content/browser/devtools/protocol/page_handler.cc
[modify] https://crrev.com/f79751ee25416fdc27faef6308efec5c3e543ee1/content/browser/devtools/render_frame_devtools_agent_host.cc


### ad...@google.com (2021-04-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-07)

Congratulations, David! The VRP Panel has decided to award you $10,000 for this report. Nice work! 

### am...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### ja...@google.com (2021-04-12)

[Empty comment from Monorail migration]

### gi...@google.com (2021-04-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fe20b05a0e5e4477c313c247180d94d7904176fc

commit fe20b05a0e5e4477c313c247180d94d7904176fc
Author: Jana Grill <janagrill@google.com>
Date: Tue Apr 20 18:23:33 2021

M86-LTS: DevTools: expect PageHandler may be destroyed during Page.navigate

(cherry picked from commit ff5e70191ec701cce4f84aaa25cd676376253a8a)

Bug: 1188889
Change-Id: I5c2fcca84834d66c46d77a70683212c2330177a5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2787756
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#867507}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2821536
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1618}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/fe20b05a0e5e4477c313c247180d94d7904176fc/chrome/browser/extensions/api/debugger/debugger_apitest.cc
[add] https://crrev.com/fe20b05a0e5e4477c313c247180d94d7904176fc/chrome/test/data/extensions/api_test/debugger_navigate_to_forbidden_url/background.js
[add] https://crrev.com/fe20b05a0e5e4477c313c247180d94d7904176fc/chrome/test/data/extensions/api_test/debugger_navigate_to_forbidden_url/manifest.json
[modify] https://crrev.com/fe20b05a0e5e4477c313c247180d94d7904176fc/content/browser/devtools/protocol/page_handler.cc
[modify] https://crrev.com/fe20b05a0e5e4477c313c247180d94d7904176fc/content/browser/devtools/render_frame_devtools_agent_host.cc


### ja...@google.com (2021-04-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-07-28)

This issue was migrated from crbug.com/chromium/1188889?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools, Platform>Extensions>API, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055226)*

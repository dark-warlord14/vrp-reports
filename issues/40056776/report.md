# Security: Extensions with debugger permission can list URLs and send commands to incognito tabs and other profile tabs

| Field | Value |
|-------|-------|
| **Issue ID** | [40056776](https://issues.chromium.org/issues/40056776) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools, Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2021-08-04 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Extensions with debugger permission installed in a profile without explicit incognito access, and not installed in other profiles, can list URLs of and send commands to:  

\* incognito tabs  

\* other profiles' tabs

To list the URLs, the extension can use the chrome.debugger.getTargets() API: <https://developer.chrome.com/docs/extensions/reference/debugger/#method-getTargets>

To send commands to the incognito/cross-profile tabs, the extension can provide the {targetId: ...} parameter instead of the {tabId: ...} parameter when using the chrome.debugger.attach() and .sendCommand() APIs:  

<https://developer.chrome.com/docs/extensions/reference/debugger/#method-attach>  

<https://developer.chrome.com/docs/extensions/reference/debugger/#method-sendCommand>

This might be working as intended, but was unexpected behavior to me (especially across profiles). Using the tabId instead of targetId results in no incognito or cross-profile access.

**VERSION**  

Chrome Version: 92.0.4515.107 (Official Build) (64-bit) (cohort: Stable), 94.0.4596.0 Canary  

Operating System: Windows 10 OS Version 2009 (Build 19042.1110)

**REPRODUCTION CASE**  

Setup:

1. If there is a single profile in your browser, create a second profile.
2. In one profile, install attached extension (manifest.json + background.js), which is based on PoC from <https://crbug.com/chromium/1139156>.

Baseline scenario: Same profile (expected)

1. Navigate a tab in the \*first\* profile to <https://example.com/?aodebug>

Unexpected scenario 1: Incognito on same profile

1. Navigate an \*incognito\* tab in Profile 1 to <https://example.com/?aodebug>

Unexpected scenario 2: Different profile

1. Navigate a tab in the \*second\* profile to <https://example.com/?aodebug>

For the unexpected scenarios:  

Observed: Extension is able to see URLs or send commands to tab.  

Expected: Extension is not able to see URLs or send commands to tab.

To observe that incognito/cross-profile tab URLs can be listed by the extension, inspect the extension's background page and view the console output of getTargets(). Note that some listed targets are still properly restricted, such as chrome:// URLs, so those can only be listed but cannot be attached to.

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 364 B)
- [background.js](attachments/background.js) (text/plain, 1.5 KB)
- [extension-debugger.mp4](attachments/extension-debugger.mp4) (video/mp4, 2.8 MB)

## Timeline

### [Deleted User] (2021-08-04)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2021-08-04)

Relevant code below:

Code path for targetId: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/debugger/debugger_api.cc;l=482;drc=d0b89fe9c3d6ecc1ec4ffaf0baeb6b36c34ba7fd

Code path for tabId calls ExtensionTabUtil::GetTabById() here: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/debugger/debugger_api.cc;l=455;drc=d0b89fe9c3d6ecc1ec4ffaf0baeb6b36c34ba7fd

Definition of ExtensionTabUtil::GetTabById(): https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/extension_tab_util.cc;l=700;drc=d0b89fe9c3d6ecc1ec4ffaf0baeb6b36c34ba7fd

Presumably ExtensionTabUtil::GetTabById() works per-profile (and does restrict incognito access unless explicitly allowed), but the methods used in the targetId path don't have these per-profile or incognito checks. Again, might be WAI but seemed unexpected to me.

### al...@alesandroortiz.com (2021-08-04)

As additional data point, chrome://inspect/#pages only shows pages for the current profile (excluding incognito; that's also separate).

### ke...@chromium.org (2021-08-04)

Thanks for the report.

rdevlin.cronin@ can you please help triage this? It might be WAI.

[Monorail components: Platform>Extensions]

### ke...@chromium.org (2021-08-09)

karandeepb@ are you able to assess this bug?

### ka...@chromium.org (2021-08-10)

This doesn't seem to be WAI. An extension should never be able to cross the profile boundary. Additionally, extensions should respect the "Allow in incognito" flag. So we should hide cross-profile debug targets as well as incognito targets if the extension is disabled in incognito. Similarly we should also disallow the extension to attach-to or send-commands-to such inaccessible targets. 

Note that the bug is somewhat circumvented by the fact that this requires the extension to be installed and that we display an infobar whenever the debugger is attached to a tab. I'll defer to the security team to access the bug severity but it seems like Low-Severity to me based on https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md. (A limited extension permission bypass). 

caseq: Are you a good owner here?

[Monorail components: Platform>DevTools]

### ad...@google.com (2021-08-12)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-08-16)

This seems medium to me, given it's a limited security mitigation bypass with pre-requisites. Any progress on a solution to the issue?

### [Deleted User] (2021-08-17)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-18)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-01)

caseq: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-09-07)

Marking with FoundIn to keep the bots happy. That doesn't imply that I've done any extra testing or reproduced this, I haven't.

### [Deleted User] (2021-09-07)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2021-09-16)

I verified this works on ChromeOS when two profiles are simultaneously logged in. Everything is identical in terms of observed behavior in both Windows and ChromeOS.

I don't know if it's possible for two users to be logged in but not have access to each other's accounts, since the way I'm currently doing simultaneous logins intentionally allows access to both profiles without passwords (after initial authentication). Therefore it currently doesn't seem useful, but I'm not very familiar with ChromeOS yet.

Would appreciate if someone could confirm if there is or isn't a state where two accounts are simultaneously logged in but are not meant to have access to each other.

### al...@alesandroortiz.com (2021-09-22)

caseq@, karandeepb@: Friendly ping. Any updates on this issue? No notable crbug activity since mid-August and don't see an open CL.

Also see https://crbug.com/chromium/1236325#c14 re: ChromeOS impacts which may upgrade severity if noted conditions are indeed possible.

### al...@alesandroortiz.com (2021-11-12)

Friendly ping: Any updates on this issue?

### ya...@google.com (2021-11-12)

Thinking through this, I'm not sure this is a security vulnerability. Can you elaborate on a scenario where this becomes an issue?

If someone installs an extension that can monitor all pages of their profile, why would they assume that other profiles are not affected?

### al...@alesandroortiz.com (2021-11-12)

Some users (like myself) use profiles as soft security boundaries to minimize impacts of untrustworthy or compromised extensions.

For example, I use Profile 1 for casual web browsing, Profile 2 exclusively for security work, and Profile 3 for software engineering work which typically requires higher-privileged extensions. I also create temporary profiles as needed for security work which requires further isolation.

If a user installs an extension only in Profile 1, and it only appears in chrome://extensions under Profile 1, and incognito access is disabled in the extension details, a user would reasonably expect that the extension cannot affect other profiles or incognito sessions. I don't believe there's any user-visible messages indicating these extensions would have access to other profiles or incognito sessions.

In ChromeOS, extensions from Profile A can access Profile B if simultaneously logged in. This isn't useful for local privilege escalation (see https://crbug.com/chromium/1236325#c14), but still allows unexpected access for an extension from Profile A that Profile B never installed and probably isn't aware of.

### ya...@google.com (2021-11-12)

@adetaylor is this security expectation on profiles even reasonable?

### ad...@chromium.org (2021-11-15)

I think probably yes.

For example enterprise admins can force-install an extension into a profile, but are not supposed to have access to other profiles:
https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/faq.md#are-enterprise-admins-considered-privileged

Also see:
https://chromium.googlesource.com/chromium/src/+/main/extensions/docs/security_faq.md#an-extension-is-able-to-read-and-store-data-from-incognito-browsing_is-this-a-security-bug

"If an extension is able to access incognito contexts without this setting enabled, this may be a security bug; please report any such bugs here."

### ca...@chromium.org (2021-11-29)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-01-05)

Friendly ping: Any progress on this crbug? Last update was around the holidays, so hoping this gets some attention this month.

### al...@alesandroortiz.com (2022-02-23)

Friendly ping: Any progress on this bug? Don't see an open CL yet. Last update was in November.

### ya...@google.com (2022-02-25)

Andrey, this is marked as started. Were you able to make any progress?

### da...@google.com (2022-03-07)

[Empty comment from Monorail migration]

### pf...@chromium.org (2022-03-07)

[Empty comment from Monorail migration]

### pf...@chromium.org (2022-03-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-03-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e2614a3e51ba8ad7dd25a6884d8a10aa1012fa0c

commit e2614a3e51ba8ad7dd25a6884d8a10aa1012fa0c
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Thu Mar 24 06:19:48 2022

Only allow chrome.debugger extensions to attach to targets with same profile

Drive-by: rename `profile` param to ExtensionMayAttachToFoo functions to
extension_profile and group it along with other extension-specific params
to make it obvious this is not a debuggee profile.

Bug: 1236325
Change-Id: I4108a089db2d2bb6a4d73bc6cb85313dd17def84
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3514069
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/main@{#984702}

[modify] https://crrev.com/e2614a3e51ba8ad7dd25a6884d8a10aa1012fa0c/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] https://crrev.com/e2614a3e51ba8ad7dd25a6884d8a10aa1012fa0c/chrome/browser/extensions/api/debugger/debugger_apitest.cc


### ca...@chromium.org (2022-03-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-27)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-03-28)

Verified as fixed in 102.0.4969.0 Canary on Windows 10 by testing with original PoC and reviewing patch.

### am...@google.com (2022-03-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-31)

Congratulations, Alesandro! The VRP Panel has decided to award you $5,000 for this report. Thank you for all your efforts throughout this one and for this high-quality report and interesting finding! 

### al...@alesandroortiz.com (2022-03-31)

Thanks for the reward!

### am...@google.com (2022-04-01)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-04-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### gm...@google.com (2022-05-25)

[Empty comment from Monorail migration]

### rz...@google.com (2022-05-26)

[Empty comment from Monorail migration]

### rz...@google.com (2022-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2022-05-31)

We are still evaluating

### rz...@google.com (2022-06-01)

1. https://crrev.com/c/3669112
2. Medium, needed to do a few changes to the original CL and needed review from the author
3. Merged to main on Mar 24
4. Yes

### gm...@google.com (2022-06-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ab59e1c838a6cc99a9140378c806d3b6f81d67d5

commit ab59e1c838a6cc99a9140378c806d3b6f81d67d5
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Wed Jun 01 21:24:37 2022

[M96-LTS] Only allow chrome.debugger extensions to attach to targets with same profile

M96 merge issues:
  debugger_api.cc:
    ExtensionMayAttachToURLOrInnerURL and ExtensionMayAttachToRenderFrameHost
    are not present in M96

    ExtensionMayAttachToWebContents():
      ExtensionMayAttachToRenderFrameHost doesn't exist, only
      parameter naming changes applied

    DebuggerGetTargetsFunction::Run():
      conflicting loop (range-based in main, iterator in M96)

  debugger_apitest.cc:
    conflicting includes
    minor build fixes regarding parameter naming and order in some calls

Drive-by: rename `profile` param to ExtensionMayAttachToFoo functions to
extension_profile and group it along with other extension-specific params
to make it obvious this is not a debuggee profile.

(cherry picked from commit e2614a3e51ba8ad7dd25a6884d8a10aa1012fa0c)

Bug: 1236325
Change-Id: I4108a089db2d2bb6a4d73bc6cb85313dd17def84
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3514069
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#984702}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3669112
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1645}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/ab59e1c838a6cc99a9140378c806d3b6f81d67d5/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] https://crrev.com/ab59e1c838a6cc99a9140378c806d3b6f81d67d5/chrome/browser/extensions/api/debugger/debugger_apitest.cc


### rz...@google.com (2022-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2022-07-29)

This issue was migrated from crbug.com/chromium/1236325?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools, Platform>Extensions]
[Monorail mergedwith: crbug.com/chromium/1301950]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056776)*

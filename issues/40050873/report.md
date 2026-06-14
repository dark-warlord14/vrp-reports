# JavaScript injection via malicious WebExtension in CWS

| Field | Value |
|-------|-------|
| **Issue ID** | [40050873](https://issues.chromium.org/issues/40050873) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | Ju...@microsoft.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2019-12-03 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome is protecting privileged origins like <https://chrome.google.com/webstore/category/extensions> against  

modifications by malicious WebExtensions. These protections include the  

prohibition of intercepting requests via the WebRequest functionality or  

injecting custom JavaScript via Content or Background scripts.  

Additionally Chrome does not allow to attach a debugger to these origins.  

In case a tab is already debugged when a privileged origin is loaded,  

the debugger gets disconnected.  

It was discovered that this protection can be bypassed, which allows a  

WebExtension to execute JavaScript in these origins via the debugger  

functionality.  

At first a malicious WebExtension loads a new about:blank tab and  

attaches a debugger. The debugger registers interception so it is able  

to modify any HTTP responses received inside this tab. Now the  

WebExtension can load an API endpoint like  

<https://chrome.google.com/webstore/category/extensions> as the top  

origin in the debugged tab. The WebExtension is not only able to see the  

request but also able to return a custom HTTP response for this  

endpoint. By simply returning an HTML payload, it is possible to execute  

JavaScript in <https://chrome.google.com/webstore/category/extensions>. Afterwards the debugger gets finally  

disconnected from the tab, but the custom response was already rendered.  

It must be noted that this attack scenario works for other privileged  

origins like the NTP as well.

It is recommended that a debugger gets detached as soon as a request to  

a privileged origin is triggered. This ensures that the current security  

design handles top navigations as well and therefore protects these  

origins properly.

**VERSION**  

Chrome Version: 79.0.3945.56 beta  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Extract attached ZIP file
2. Load the folder as unpacked extension
3. Observe an alert in CWS

## Attachments

- [interception.zip](attachments/interception.zip) (application/octet-stream, 2.7 KB)

## Timeline

### Ju...@microsoft.com (2019-12-03)

Just FYI, this bug was found internally by someone else, but I'm reporting on behalf of him.

[Monorail components: Platform>Extensions]

### me...@chromium.org (2019-12-04)

rdevlin.cronin@ or karandeepb@ could one of you please take a look?
Thanks!

### rd...@chromium.org (2019-12-04)

Thanks for the report!

Over to caseq for devtools / debugger API.  Is there a way we could prevent the extension from intercepting requests to origins it doesn't have access to (at least, top-level requests like this?).  It seems like that would be a good generic check, in addition to protecting the webstore.

### sh...@chromium.org (2019-12-05)

Setting milestone and target because of Security_Impact=Beta and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-05)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-12-05)

+adetaylor@ (Security TPM).

This is security severity "Medium" and no fix available. Can we please target this for M80?

### ad...@chromium.org (2019-12-05)

This is marked as Security_Impact-Beta, which implies it is a serious regression between 78 and 79. I doubt that's the case. caseq@/rdevlin.cronin@ - can you confirm this affects M78 and earlier too?

### ca...@chromium.org (2019-12-05)

Thanks for the report, that's an impressive trick -- we'll work on fixing this soon! However, I don't think this is new for m79, the API being exploited has been around for a while. Removing RB-Stable based on this, but will still treat this as P1.

### Ju...@microsoft.com (2019-12-05)

I did see Stable build blocking this attack. I think this is a regression. Have you tested in Stable build?

### ca...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ca...@chromium.org (2019-12-06)

Jun, you're right, I couldn't reproduce this on m78 so far. My understanding is that this is prevented by the check for current _visible_ URL of the tab being debugged, which happens to be new (not yet committed URL of the privileged origin) in m78 and old (about:blank) in m79. Bringing RBS back for the time being, although I *think* m78 may be exploitable as well with some modifications, let me try...

### pb...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ca...@chromium.org (2019-12-06)

I bisected this down to this CL: https://chromium-review.googlesource.com/c/chromium/src/+/1737819. Over to tjudkins@ whether the side effect that we have is expected and whether fixes in other places are required.

For some background,  DebuggerFunction::InitAgentHost() started somehow started using the last committed URL (about:blank) instead of new, not-yet-comitted, restricted URL in a call to ExtensionCanAttachToURL() here: https://cs.chromium.org/chromium/src/chrome/browser/extensions/api/debugger/debugger_api.cc?rcl=11f4508e563f02e900ad9f963e7c4e90a4c1d637&l=431. I don't see what exactly in the CL lead to this behavior, but are we using the right web contents there?

We can fix this by having checks elsewhere in DevTools, but I'd like someone who's more familiar with extensions code to assess whether there may be a similar problem elsewhere.

### ad...@chromium.org (2019-12-06)

Discussed with Devlin. It's essentially too late to wait for a fix here for M79, so the only option is to revert https://crbug.com/chromium/981628. But that would be a horrendous revert - it's a huge change and has developer-visible consequences. I am removing RBS for that reason.

So, we will unfortunately need to ship with this regression in M79. However we should include this in the first stable update of M79 as it's a regression, even though it's only medium severity. Once this is fixed, please add Merge-Request-79.

Consequences of this bug potentially include spoofing extensions or triggering extension installation flow. There might be other protected origins with even more serious consequences. But this can only be triggered from a malicious extension, and there will still be a native confirmation dialog which cannot be bypassed, so it remains medium severity.

### ca...@chromium.org (2019-12-06)

I'm not suggesting we have to revert this as a fix, there may be other fixes available. Also, my understanding that the observed change may be due to this:

https://chromium-review.googlesource.com/c/chromium/src/+/1737819/31/chrome/browser/extensions/api/tabs/tabs_api.cc

In which case there's a chance there's a chance this exploit can be slightly modified to work on m78 as well (investigating this right now).

### ca...@chromium.org (2019-12-06)

[Comment Deleted]

### ca...@chromium.org (2019-12-06)

... a-and it's so indeed. So basically the good news is that this is not a regression. The bad news is that we have this problem in earlier versions as well.

What crrev.com/c/1737819 does essentially is that it switches the extension-initiated navigation to be treated as the renderer-initiated one. So if we update the exploit to use renderer-initiated navigation to navigate about:blank, we get it working for the older versions as well.

I'll grab this and implement a check upon initiating navigation request in the DevTools land.

### ad...@chromium.org (2019-12-06)

Thanks caseq@!

### ca...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0788b1d419f78050f1114fffefd1f68cd88d1dab

commit 0788b1d419f78050f1114fffefd1f68cd88d1dab
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Tue Dec 10 04:28:11 2019

DevTools: check session can inspect URL we're about to navigate to

Bug: 1030411
Change-Id: I0696686982f1a089dc554013847ab4a2dafce83b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1956529
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/master@{#723234}

[modify] https://crrev.com/0788b1d419f78050f1114fffefd1f68cd88d1dab/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] https://crrev.com/0788b1d419f78050f1114fffefd1f68cd88d1dab/content/browser/devtools/devtools_instrumentation.cc
[modify] https://crrev.com/0788b1d419f78050f1114fffefd1f68cd88d1dab/content/browser/devtools/render_frame_devtools_agent_host.cc
[modify] https://crrev.com/0788b1d419f78050f1114fffefd1f68cd88d1dab/content/browser/devtools/render_frame_devtools_agent_host.h
[modify] https://crrev.com/0788b1d419f78050f1114fffefd1f68cd88d1dab/content/public/browser/devtools_agent_host_client.cc
[modify] https://crrev.com/0788b1d419f78050f1114fffefd1f68cd88d1dab/content/public/browser/devtools_agent_host_client.h


### me...@google.com (2020-01-02)

Andrey, thanks for the fix. Just checking if there is any remaining work here.

### ca...@chromium.org (2020-01-02)

Ah, sorry, no, there's no more work to do. The fix is there, I just forgot to close the bug.

### sh...@chromium.org (2020-01-03)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-07)

Requesting merge to beta M80 because latest trunk commit (723234) appears to be after beta branch point (722274).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-07)

This bug requires manual review: M80's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), Kariahda@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-01-07)

caseq@ pls help answer the questions in https://crbug.com/chromium/1030411#c26 for merge-review.

### ca...@google.com (2020-01-07)

> 1. Does your merge fit within the Merge Decision Guidelines?
> - Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines

This is a security fix, so I defer to security team for judgement on how critical this is. It should be mostly harmless, but it technically does introduce additional checks that may cause an extension to get disconnected, so potentially some extensions *may* be broken, although the chances of breaking some useful behavior appear pretty slim to me.

> 2. Links to the CLs you are requesting to merge.

https://chromium-review.googlesource.com/c/chromium/src/+/1956529

> 3. Has the change landed and been verified on master/ToT?

Yes

> 4. Why are these changes required in this milestone after branch?

This is a fix for a security problem.

> 5. Is this a new feature?
> 6. If it is a new feature, is it behind a flag using finch?

This is not a feature.


### sr...@google.com (2020-01-07)

adetaylor@ can you chime in your thoughts if we should take this merge to M80? 

### ad...@chromium.org (2020-01-07)

I'd say yes. This is not serious enough to want to merge to stable, but a merge to beta would be good, to get the fix out a bit sooner.

### sr...@google.com (2020-01-09)

merge approved to M80 branch:3987

### na...@google.com (2020-01-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-09)

Congrats! The Panel decided to reward $5,000 for this report!

### na...@google.com (2020-01-09)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a8264ba685f1bdfde1a1e8b17ec30ef6194a0dec

commit a8264ba685f1bdfde1a1e8b17ec30ef6194a0dec
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Fri Jan 10 04:45:57 2020

DevTools: check session can inspect URL we're about to navigate to

TBR=rdevlin.cronin@chromium.org

(cherry picked from commit 0788b1d419f78050f1114fffefd1f68cd88d1dab)

Bug: 1030411
Change-Id: I0696686982f1a089dc554013847ab4a2dafce83b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1956529
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#723234}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1992764
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/branch-heads/3987@{#456}
Cr-Branched-From: c4e8da9871cc266be74481e212f3a5252972509d-refs/heads/master@{#722274}

[modify] https://crrev.com/a8264ba685f1bdfde1a1e8b17ec30ef6194a0dec/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] https://crrev.com/a8264ba685f1bdfde1a1e8b17ec30ef6194a0dec/content/browser/devtools/devtools_instrumentation.cc
[modify] https://crrev.com/a8264ba685f1bdfde1a1e8b17ec30ef6194a0dec/content/browser/devtools/render_frame_devtools_agent_host.cc
[modify] https://crrev.com/a8264ba685f1bdfde1a1e8b17ec30ef6194a0dec/content/browser/devtools/render_frame_devtools_agent_host.h
[modify] https://crrev.com/a8264ba685f1bdfde1a1e8b17ec30ef6194a0dec/content/public/browser/devtools_agent_host_client.cc
[modify] https://crrev.com/a8264ba685f1bdfde1a1e8b17ec30ef6194a0dec/content/public/browser/devtools_agent_host_client.h


### ad...@google.com (2020-02-02)

[Empty comment from Monorail migration]

### ad...@google.com (2020-02-03)

jun.kokatsu@microsoft.com - in https://crbug.com/chromium/1030411#c1 you mention this was found by someone else. By default, I'll credit you in the release notes, but if you'd like the original reporter to be credited, please let me know the correct attribution in the next hour or two. Thanks!

### Ju...@microsoft.com (2020-02-03)

Hi, please use "Microsoft Edge Team" as a credit.

### ad...@chromium.org (2020-02-03)

Will do, thanks!

### ad...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1030411?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050873)*

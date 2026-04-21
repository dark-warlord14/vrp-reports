# heap-use-after-free on content::DevToolsAgentHostImpl::ForceDetachAllSessions

| Field | Value |
|-------|-------|
| **Issue ID** | [40059457](https://issues.chromium.org/issues/40059457) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Portals, Platform>DevTools |
| **Platforms** | Windows |
| **Reporter** | xp...@gmail.com |
| **Assignee** | ad...@chromium.org |
| **Created** | 2022-04-25 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

Prerequisite flags: chrome://flags#enable-portals  

0. Setup a webserver (needed for portals to work).

1. Start Chrome with PoC.html. e.g. chrome <http://127.0.0.1:5500/PoC.html>
2. When you see the window for Chrome, focus window and spam key F12 for devtools.

**Problem Description:**  

heap-use-after-free on content::DevToolsAgentHostImpl::ForceDetachAllSessions

**Additional Comments:**

\*\*Chrome version: \*\* 103.0.5024.0 \*\*Channel: \*\* Canary

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 17.8 KB)
- [eRRLU15FqD.mp4](attachments/eRRLU15FqD.mp4) (video/mp4, 7.6 MB)
- [PoC.html](attachments/PoC.html) (text/plain, 364 B)

## Timeline

### xp...@gmail.com (2022-04-25)

Sorry, I forgot to attach the PoC. Attached now.

### dt...@chromium.org (2022-04-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-25)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-04-25)

I wasn't able to reproduce on my linux setup. Over to devtools folks for triage, given that the ASAN trace looks credible. Assigning per devtools/OWNERS

[Monorail components: Platform>DevTools]

### ds...@chromium.org (2022-04-26)

Adithya, we already agreed with prerendering folks that we will disable prerendering when devtools session is present. Can we do the same for portals activation. Who can decided that?

### ds...@chromium.org (2022-04-26)

Setting security to medium as this requires enabling experimental web platform feature. However it is memory corruptions in the browser process, so we should fix this promptly.

### ad...@chromium.org (2022-04-26)

I'm not sure if we can disable portals/portal activation when a devtools session is present, at least in a spec compliant way - unlike prerendering, portals cannot really be cancelled invisibly in the background, they are visible from the start.

ccing jbroman@ who can comment on this better

[Monorail components: Blink>Portals]

### ds...@chromium.org (2022-04-26)

Sorry, I didn't mean to cancel portals entirely, but disable an activation and either throw or do a hard transition. DevTools is not going to behave correctly after the portal activation anyway, until crbug.com/1317959 is addressed.

### ad...@chromium.org (2022-04-26)

Right, even for activation - the spec does make some guarantees on its success (there are documented possible failure reasons) - and we'd have to add one for devtools specifically, I'm not sure if there's precedent for that.

Also we already have some support for portal activation in DevTools, although it is buggy, and crbug.com/1317959 will be a huge improvement.

### ad...@chromium.org (2022-04-26)

The current support for portals is based on the fact that it's implemented with inner WebContents, it will not work once we move portals to MPArch though.

### jb...@chromium.org (2022-04-26)

Dev tools is somewhat outside of the scope of web standards. Practically, in the long term I think we should make it work. In the short term, the feature is disabled so we could either throw a non-compliant exception or crash, and either would mitigate the immediate security risk.

### ds...@chromium.org (2022-04-26)

Thanks! I personally would prefer an exception. Can you point me to a right place where this logic could live?

### ad...@chromium.org (2022-04-26)

In the renderer process: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/html/portal/html_portal_element.cc;l=110;drc=c5e1d7dd6c3ffb90c34b26b96178378dfd0c6db8

In the browser process:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/portal/portal.cc;l=327;drc=c5e1d7dd6c3ffb90c34b26b96178378dfd0c6db8

### ad...@chromium.org (2022-04-26)

Sorry this is a more accurate browser link: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/portal/portal.cc;l=486;drc=c5e1d7dd6c3ffb90c34b26b96178378dfd0c6db8

### ds...@chromium.org (2022-04-26)

Thanks! Do these correspond to different ways to activate a portal or is one implemented in terms of the other?

### ds...@chromium.org (2022-04-26)

[Empty comment from Monorail migration]

### ds...@chromium.org (2022-04-26)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-04-26)

Oh they're the same way - portal activation is always initiated in the renderer, so we do some checks there before sending an IPC to the browser, where we do more checks.

### ds...@chromium.org (2022-04-26)

So, would it make sense to only have a check in renderer?

### ad...@chromium.org (2022-04-26)

I think browser is probably the better place, renderer might be too early (you could have the window being opened after the IPC is sent from the renderer but before it's processed in the browser)

### [Deleted User] (2022-04-26)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2022-04-26)

Assigning to Adithya since he already has a fix in flight for this.

### gi...@appspot.gserviceaccount.com (2022-04-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/24a6fb1714d41e7901600907fe3eddf76c31c75a

commit 24a6fb1714d41e7901600907fe3eddf76c31c75a
Author: Adithya Srinivasan <adithyas@chromium.org>
Date: Tue Apr 26 22:25:55 2022

DevTools: Fix UaF with portal activation

There is a slight gap between when the DevToolsUIBindings object is destroyed and when the DevToolsWindow is cleaned up. We currently would
execute the reattach callback in the destructor, which would then go on
to access the bindings of the window that is being destroyed (hence the UAF).

This patch moves the reattach callback to be run after we remove the
window is removed from the global list of instances (so it won't be
retrieved by the callback).

Bug: 1319302
Change-Id: I6a7c130bc65093e8ed4081576ebe2582aa5e358a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3605743
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Adithya Srinivasan <adithyas@chromium.org>
Cr-Commit-Position: refs/heads/main@{#996401}

[modify] https://crrev.com/24a6fb1714d41e7901600907fe3eddf76c31c75a/chrome/browser/devtools/devtools_window.cc


### do...@chromium.org (2022-04-27)

Setting Impact=None as this requires portals to be enabled.

### ad...@chromium.org (2022-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-27)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-24)

Congratulations on another one! The VRP Panel has decided to award you $3,000 for this report based on this issue not being fully web accessible and the specific user interaction required. Thank you for your efforts and reporting this issue to us! 

### xp...@gmail.com (2022-05-24)

@amyressler@chromium.org 

Thank you! I have a question about: "this report based on this issue not being fully web accessible..."

In most, if not all portal security reports, there is not a mention of web accessibility affecting the bounty [1-4]. Even dating before the origin trial [1][5]. 

Was there a change to how portal security issues are rewarded? I respect the panel's decision, however knowing the process helps me understand how bugs are rewarded. Thanks again :)


[1] https://bugs.chromium.org/p/chromium/issues/detail?id=971702
[2] https://bugs.chromium.org/p/chromium/issues/detail?id=1041406
[3] https://bugs.chromium.org/p/chromium/issues/detail?id=1083128
[4] https://bugs.chromium.org/p/chromium/issues/detail?id=1158376
[5] https://developer.chrome.com/origintrials/#/view_trial/-7680889164480380927

### am...@chromium.org (2022-05-24)

Hello and thanks for your question! 
It appears all the issues you linked with the exception of https://crbug.com/chromium/1158376 were web accessible, so the issue with not being web accessible would not have been mentioned in any of those issues. The reason it was not mentioned for https://crbug.com/chromium/1158376 was due to that issue the date that issues were reported, which was back in December 2020.

The change in reward amounts around non-web accessible security issues is not specific issues in the Portals feature, but to all Chrome bugs. In February 2022, we updated the Chrome VRP rules and policies [1] to communicate lower reward amounts for security bugs that are harder to exploit and more difficult for the attacker to successfully use. This update was also communicated directly to the Chrome VRP researcher community via email. 
"The amounts listed are for good quality reports that don't require complex or unlikely user interaction. Reports of issues that rely heavily or solely on user interaction, instead of being triggered by remote content, will generally receive significantly reduced rewards. Less convincing or more constrained bug submissions will likely qualify for reduced reward amounts, as chosen at the discretion of the reward panel."

We will be updating our rules and policies further in the near future (as well as communicating those updates to the researcher community) to add further clarity and information around reward amounts and reward decision criteria. 

[1] https://g.co/chrome/vrp 

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### xp...@gmail.com (2022-05-24)

That all makes sense! Thank you a ton for the detailed response.

### [Deleted User] (2022-08-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ds...@chromium.org (2023-12-13)

[Empty comment from Monorail migration]

### is...@google.com (2023-12-13)

This issue was migrated from crbug.com/chromium/1319302?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Portals, Platform>DevTools]
[Monorail mergedwith: crbug.com/chromium/1319306]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059457)*

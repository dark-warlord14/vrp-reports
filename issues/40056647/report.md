# heap buffer over flow in printing::PrintPreviewUI::SetInitialParams(use devtools)

| Field | Value |
|-------|-------|
| **Issue ID** | [40056647](https://issues.chromium.org/issues/40056647) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>PrintPreview |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | wx...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2021-07-23 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36

Steps to reproduce the problem:
1.open a chromium (out\asan\chrome.exe --user-data-dir=e:\data\xxx --remote-debugging-port=9000)
open anathor chromium(out\asan\chrome.exe --user-data-dir=e:\data\xxxxx) and visit http://127.0.0.1:9000/ and steps like my video.
2.
3. my chromium version is 3f011eda583817f209cc2d064eba276a7926537b

I think these steps may can be reproduced by unsafe extension.

What is the expected behavior?

What went wrong?
browser crash

Did this work before? N/A 

Chrome version: 92.0.4515.107  Channel: stable
OS Version: 10.0

## Attachments

- [heap_over_flow.txt](attachments/heap_over_flow.txt) (text/plain, 16.7 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 17.8 MB)

## Timeline

### wx...@gmail.com (2021-07-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-23)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-24)

Thanks for the report. I suspect this, https://crbug.com/chromium/1232404, https://crbug.com/chromium/1232408, https://crbug.com/chromium/1232409, https://crbug.com/chromium/1232425, https://crbug.com/chromium/1232448 are all caused by the same underlying problem: navigating the chrome://print WebUI via devtools remote debugging. The print preview page appears to have all the wiring to listen to navigations for its initiator, so maybe devtools navigation is skipping that somehow?

+folks who've touched chrome/browser/ui/webui/print_preview/print_preview_ui.cc recently, do you mind taking a look? I will cc you on the other bugs I've mentioned as well, please feel free to dedupe if necessary. Also +devtools folks if they're helpful.

[Monorail components: UI>Browser>PrintPreview]

### [Deleted User] (2021-07-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-24)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-24)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wx...@gmail.com (2021-07-25)

I think these bug should be set as high, cause my steps in video may could be reproduced by the chrome extension api(chrome.debugger), the api could attach the print view tab, and can send other commands like (page navigate, and may could execute js). here is the devtools protocol(https://chromedevtools.github.io/devtools-protocol/), well, just my opinion, I haven't try it.

### do...@chromium.org (2021-07-25)

We usually regard memory corruption that requires an extension to be installed as Medium severity[1]

1. https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md

### aw...@chromium.org (2021-07-26)

Re: https://crbug.com/chromium/1232402#c3, I agree that these all look like the same underlying issue.  I think these navigations happening within the Print Preview dialog are not supposed to be allowed for that nested run loop.  I think the correction will be for such navigations to be blocked in this case.

### do...@chromium.org (2021-07-26)

#9 - thanks. I will merge the other bugs into here for now, and if one of them does turn out to be an independent issue we can split it back out.

### do...@chromium.org (2021-07-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-26)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-07-27)

I feel a little unfair to me, If I submit a bug, maybe you set a small fix for the specific components. If I submit serveral bugs at the same time,  developer could set a wider fix for bugs.Anyway I will try to keep find vul but not submit lots of bug at the same time.

### aa...@google.com (2021-07-27)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-27)

#17: we look at things from the point of view of the fix. If the same fix addresses multiple bugs, we consider those bugs to be equivalent. We try our best to reasonably split things out where it makes sense. In this case, while you've gotten several different crashes and stack traces here, they all look like the exact same underlying problem: the chrome://print dialog isn't correctly handling navigations. If we do find that one of these is caused by a different problem, we will split it back out independently.

### wx...@gmail.com (2021-07-27)

#19: get it, thanks a lot.

### aw...@chromium.org (2021-07-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2021-08-10)

+alexmos - This sounds similar to your description for https://crbug.com/chromium/1097137.  Perhaps the proper resolution to this is to not even allow the navigation to happen?

### wx...@gmail.com (2021-08-11)

Would you please merge https://bugs.chromium.org/p/chromium/issues/detail?id=1232405#c10 into here?

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-09-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-01-09)

Any update?

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-07-19)

thestig -- could you take a look and see if we can get this very old bug moving again? Thanks!

### th...@chromium.org (2022-07-20)

I haven't repro'd this one yet, but I just landed r1025870 to fix https://crbug.com/chromium/1345034 a few hours ago. These 2 bugs may have the same underlying cause.

### th...@chromium.org (2022-07-20)

I don't know if --remote-debugging-port has changed since when this bug report was opened, or if it's just broken in my environment. I can connect to the debug port, but it always return 0 bytes of data. If I load /json, then that works fine.

### wx...@gmail.com (2022-07-20)

you can open devtools from the print preview ui

### th...@chromium.org (2022-07-20)

Sure. I was just wondering why the initial repro steps no longer works. Found out that's intentional - https://crbug.com/chromium/1232509.

Anyway, it's roughly the same bug as https://crbug.com/chromium/134034. Now trying to repro this triggers a CHECK() failure in PrintPreviewUI::SetInitialParams(). (The other bug doesn't hit this CHECK()) I'm not sure if it's worthwhile to do additional work to handle the CHECK() failure.

### pb...@chromium.org (2022-07-20)

[Empty comment from Monorail migration]

### co...@chromium.org (2022-07-20)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-07-20)

tsepez@: Thoughts on how this bug status should be updated? Should I mark this as a duplicate of https://crbug.com/chromium/1345034, or vice versa, or just mark it as fixed?

### ts...@chromium.org (2022-07-20)

Please mark this as fixed, then dup 1345034 into this one.

### th...@chromium.org (2022-07-20)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-07-20)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2022-07-28)

Congratulations! The VRP Panel has decided to award you $2,000 for this report. The reward amount decided was based on this issue being significantly mitigated by not being remote accessible, user interaction required, and in progress mitigations from ongoing work (https://crbug.com/chromium/1232509). Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2022-07-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2022-12-13)

https://crbug.com/chromium/1345034 was the last to be duped into this bug.

considering the latest fix in https://crbug.com/chromium/1345034 to be the fix for this umbrella bug, as well: https://chromium.googlesource.com/chromium/src/+/754bc497cf08ea408df0476300c8d10759aa6a15

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1232402?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1232404, crbug.com/chromium/1232405, crbug.com/chromium/1232408, crbug.com/chromium/1232409, crbug.com/chromium/1232425, crbug.com/chromium/1232427, crbug.com/chromium/1232448, crbug.com/chromium/1233026, crbug.com/chromium/1345034]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056647)*

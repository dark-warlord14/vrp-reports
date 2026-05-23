# uaf in  browser_switcher::`anonymous namespace'::OpenBrowserSwitchPage

| Field | Value |
|-------|-------|
| **Issue ID** | [40058928](https://issues.chromium.org/issues/40058928) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Enterprise>BrowserSwitcher |
| **Platforms** | Windows |
| **Reporter** | wx...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2022-03-01 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36

Steps to reproduce the problem:
1.I patch the chromium to easy enter the code path
2. open chromium. it will  Open 'chrome://browser-switch/?url=...' in the current tab.
3.then close the current tab

What is the expected behavior?

What went wrong?
uaf occur

Did this work before? N/A 

Chrome version: 98.0.4758.102  Channel: stable
OS Version: 10.0

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 17.4 KB)
- [issue_poc.png](attachments/issue_poc.png) (image/png, 67.0 KB)
- 0001-fix-issue-1301840-uaf.patch (text/plain, 2.0 KB)
- poc1.png (image/png, 92.0 KB)
- test.html (text/plain, 172 B)
- [poc1.mp4](attachments/poc1.mp4) (video/mp4, 8.2 MB)

## Timeline

### [Deleted User] (2022-03-01)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-03-01)

[Comment Deleted]

### wx...@gmail.com (2022-03-01)

you can set owner to nicolaso@chromium.org. 
how to fix
 - set web_contents to weak_ptr

### wx...@gmail.com (2022-03-01)

my chromium commit is 1648616c1dafa4d3624552c2ce282be5129290db

### wx...@gmail.com (2022-03-01)

[Comment Deleted]

### wx...@gmail.com (2022-03-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-03-01)

I have not reproduced this, tentatively setting this as medium severity based on POC and that the patch being introduced seems to be a requirement to trigger; over to you nicolaso@ as requested 

[Monorail components: Enterprise>BrowserSwitcher]

### [Deleted User] (2022-03-01)

[Empty comment from Monorail migration]

### ni...@chromium.org (2022-03-02)

Hm, this doesn't repro locally on Windows. wxhusst@, what's the contents of your args.gn? Maybe something in there is making it easier to trigger.

IIUC, your patch only adds logging, and sets should_switch=true.

>the patch being introduced seems to be a requirement to trigger

It's not a requirement, but I suspect it's *very* hard (impossible?) to trigger in an official build. What the patch does is "force all navigations to trigger BrowserSwitcher".

BrowserSwitcher is a feature hidden behind an enterprise policy (which only has ~8M 30DAUs). It sets a list of URLs (typically a small number of websites) that will trigger this particular code path. It's also a *really* tight race condition, at least without the patch.

More importantly, this seems to depend on certain build-time arguments. Even on an asan build, I can't seem to repro this bug...

### ni...@chromium.org (2022-03-02)

In short, I don't know whether this actually repros in the wild/has a security impact.

It's an easy fix though. Using a WeakPtr is the correct thing to do, so let me work on that

### ni...@chromium.org (2022-03-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-03-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e7e87d05d58bc70611401f655dc845498357f8e4

commit e7e87d05d58bc70611401f655dc845498357f8e4
Author: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Date: Wed Mar 02 17:47:01 2022

[BrowserSwitcher] Use a WeakPtr in the NavigationThrottle

When calling OpenBrowserSwitchPage(), we passed the WebContents by
raw pointer rather than a WeakPtr. It was posted to a task, so that
can be unsafe.

Bug: 1301840
Change-Id: I42e1daaf0773d08251000770e65c5d8674867921
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3498165
Commit-Queue: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Auto-Submit: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Reviewed-by: Julian Pastarmov <pastarmovj@chromium.org>
Commit-Queue: Julian Pastarmov <pastarmovj@chromium.org>
Cr-Commit-Position: refs/heads/main@{#976720}

[modify] https://crrev.com/e7e87d05d58bc70611401f655dc845498357f8e4/chrome/browser/browser_switcher/browser_switcher_navigation_throttle.cc


### [Deleted User] (2022-03-02)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-02)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wx...@gmail.com (2022-03-02)

this is my contents of args.gn, I just patch chrome/browser/browser_switcher/browser_switcher_navigation_throttle.cc 
# Build arguments go here.
# See "gn args <out_dir> --list" for available build arguments.
is_debug =false
is_asan = true
dcheck_always_on = false
enable_mojom_fuzzer = true

### wx...@gmail.com (2022-03-02)

>BrowserSwitcher is a feature hidden behind an enterprise policy (which only has ~8M 30DAUs). It sets a list of URLs (typically a small number of websites) that will trigger this particular code path. It's also a *really* tight race condition, at least without the patch.

 could the list of URLs  set to "chrome://browser-switch/*" ? If it can, I think the bug can be triggered easily , because all navigations will enter into "chrome://browser-switch/" and always reload.

### ni...@chromium.org (2022-03-02)

> could the list of URLs  set to "chrome://browser-switch/*" ?

No. Only http://, https://, and ftp:// URLs are allowed

### wx...@gmail.com (2022-03-02)

oh, it seems a tight race condition in real chrome

### wx...@gmail.com (2022-03-02)

oh, I can trigger it stable,
- set a url to switch
- open test.html
- then close chrome

### wx...@gmail.com (2022-03-02)

I think this bug should set Security_Severity-High 

### wx...@gmail.com (2022-03-02)

hello, nicolaso, I think we can set the bug to fixed.

### ni...@chromium.org (2022-03-03)

Correct, it's Fixed by crrev.com/c/3498165

test.html in https://crbug.com/chromium/1301840#c19 is important, as it shows how an attacker could try to exploit this vulnerability.

There's a few mitigating factors:
- Requires the BrowserSwitcherEnabled policy to be set. (relatively low usage, ~8M DAUs)
- The attacker needs to know (or guess!) the contents of the BrowserSwitcherUrlList policy, in order to know what JavaScript to "inject".
- The user has to click the "X" button to trigger the UaF.
    - ... but they're pretty likely to do that, if Chrome is freezing because of 100+ tabs opening suddenly.
    - ... and if the attacker is running their JS in a malicious extension, they can close all windows via JavaScript.

Anyways, if all those conditions are fulfilled it's a pretty big deal. I'll let the security team make the final call RE: severity, but it seems rather high.

### ni...@chromium.org (2022-03-04)

Actually combing through Severity Guidelines for the firs time [1] I would be tempted to leave it as Medium severity.

> Bugs that would normally be rated at a higher severity level with unusual mitigating factors may be rated as medium severity.

Again, this requires the attacker to know the policy's value, and that they already have a malicious extension on the user's machine (or control an origin in that list, in which case it requires user interaction).

And it only affects users with the BrowserSwitcherEnabled policy, which has low usage; but IIUC this is not a big mitigating factor:

> Conversely, we do not consider it a mitigating factor if a vulnerability applies only to a particular group of users. For instance, a Critical vulnerability is still considered Critical even if it applies only to Linux or to those users running with accessibility features enabled.

Anyways, Medium seems more appropriate based on the examples on that page.

[1] https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md

### [Deleted User] (2022-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-11)

Congratulations, raven! The VRP Panel has decided to award you $2,000 for this report. 
This report was judged under the updated VRP rules and policies related to bugs requiring complex user interaction. [1] We appreciate your efforts and reporting this issue to us! 

[1] https://g.co/chrome/vrp 

### am...@google.com (2022-03-11)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-03-12)

hi amy, I don't think this bug need complex user interaction.You can see the step of https://crbug.com/chromium/1301840#c22. Hope you can recheck it. Can this bug get cve id?

### wx...@gmail.com (2022-03-12)

as [1] shows that the suggest patch can get additional rewards, can my patch in [2] get the   additional rewards?

[1] https://g.co/chrome/vrp
[2] https://bugs.chromium.org/p/chromium/issues/detail?id=1301840#c6

### am...@chromium.org (2022-03-14)

Hi raven, thanks for your questions in comments 29-30: 

>> I don't think this bug need complex user interaction.You can see the step of https://crbug.com/chromium/1301840#c22.

In https://crbug.com/chromium/1301840#c22-23, the developer lists the number of mitigations, which are significant and also concurs with the severity and impact (in https://crbug.com/chromium/1301840#c23)
The VRP Panel took all of this into consideration when making the reward decision. 

>>Can this bug get cve id?
As always, CVEs are allocated when the patch is shipped in a stable channel release. One will be allocated to this bug report once this patch is included in the a stable release candidate. 

>>as [1] shows that the suggest patch can get additional rewards, can my patch in [2] get the   additional rewards?
while it does not appear we used your patch in full, we will reassess the potential patch reward at the next panel 




### wx...@gmail.com (2022-03-14)

Ok, thank you 

### am...@chromium.org (2022-03-16)

hello raven, the VRP panel has reviewed this issue for reassessment and has decided that the original award amount was sufficient for this report. 

### wx...@gmail.com (2022-03-16)

Thanks a lot 👍

### am...@chromium.org (2022-04-25)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1301840?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058928)*

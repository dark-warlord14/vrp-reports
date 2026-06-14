# iframe sandbox allow_top_navigation_by_user_activation can be bypassed with certain extensions

| Field | Value |
|-------|-------|
| **Issue ID** | [40051014](https://issues.chromium.org/issues/40051014) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>IFrameSandbox, Platform>Extensions, UI>Browser>Navigation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@gmail.com |
| **Assignee** | mu...@chromium.org |
| **Created** | 2019-12-18 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version : 78.0.3904.108 (Build officiel) (64 bits) (cohort: Stable)

**URLs (if applicable) :** <http://w3c-test.org/html/semantics/embedded-content/the-iframe-element/iframe_sandbox_allow_top_navigation_by_user_activation-manual.html>

**What steps will reproduce the problem?**  

**(1)** Open the link  

**(2)**  

**(3)**

**What is the expected result?**

You should not be redirected and the page should show at the bottom:  

The sandboxed iframe should post a message saying the top navigation was blocked when no user gesture.

You should see the error in console :

iframe-that-performs-top-navigation.html:7 Unsafe JavaScript attempt to initiate navigation for frame with URL '<http://w3c-test.org/html/semantics/embedded-content/the-iframe-element/iframe_sandbox_allow_top_navigation_by_user_activation-manual.html>' from frame with URL '<http://w3c-test.org/html/semantics/embedded-content/the-iframe-element/support/iframe-that-performs-top-navigation.html>'. The frame attempting navigation of the top-level window is sandboxed with the 'allow-top-navigation-by-user-activation' flag, but has no user activation (aka gesture). See <https://www.chromestatus.com/feature/5629582019395584>.

**What happens instead?**

You are redirect to <http://w3c-test.org/html/semantics/embedded-content/the-iframe-element/support/navigation-changed-iframe.html>

The page contains :  

"PASSED: Navigation succeeded."

If you click on the link and you quickly stop loading the page before the redirection then you do F5, the page works correctly and the redirection is done only when clicking on the button in the iframe

## Attachments

- deleted (application/octet-stream, 0 B)
- [1035315 - ifram sandbox llow_top_navigation_by_user_activation does not work as expected - chromium - An open-source project to help move the web forward. - Monorail - Google Chrome 2019-12-19 18-44-11~1.mp4](attachments/1035315 - ifram sandbox llow_top_navigation_by_user_activation does not work as expected - chromium - An open-source project to help move the web forward. - Monorail - Google Chrome 2019-12-19 18-44-11~1.mp4) (video/mp4, 3.0 MB)

## Timeline

### va...@chromium.org (2019-12-18)

[Empty comment from Monorail migration]

### pe...@chromium.org (2019-12-19)

Tested the issue on reported chrome version#78.0.3904.108 using Mac 10.14.6 by the following steps:
Steps:
1. Navigated to the given link - 'http://w3c-test.org/html/semantics/embedded-content/the-iframe-element/iframe_sandbox_allow_top_navigation_by_user_activation-manual.html'
2. Observed error in console 'Unsafe JavaScript attempt to'
3. On clicking the 'Navigate the top page' button, it is redirecting to this link -'http://w3c-test.org/html/semantics/embedded-content/the-iframe-element/support/navigation-changed-iframe.html'

Attached screencast for reference.
@Reporter: Could you please review the attached screencast and confirm if this is the issue you are pointing to.
Thanks...

### al...@gmail.com (2019-12-19)

Your screencast does not show the bug.
Here is a video that shows that the problem seems random. You can see that sometimes I am redirected (when it shouldn't be) and sometimes not.



### sh...@chromium.org (2019-12-19)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tk...@chromium.org (2019-12-23)

[Empty comment from Monorail migration]

[Monorail components: -Blink Blink>SecurityFeature]

### mk...@chromium.org (2019-12-24)

Assigning to domenic@ for triage, as the others listed on the chromestatus entry aren't actually on the project anymore.

### mk...@chromium.org (2019-12-24)

Also +jahpet, FYI.

[Monorail components: -Blink>SecurityFeature Blink>SecurityFeature>IFrameSandbox UI>Browser>Navigation]

### do...@chromium.org (2020-01-06)

Yao, I know you've been working on sandboxed downloads. This feature is related and seems likely to be in the same area; is your team an appropriate owner for it, who could help wit hthe triaging?

### ya...@chromium.org (2020-01-06)

I'm able to reproduce on current stable build (M79) though it seems rare/random, but I couldn't reproduce it on the ToT build.

@mustaq: Do you know if anything got fixed recently around user activation that may have fixed the bug like this?


### mm...@chromium.org (2020-01-22)

Gentle ping: 
mustaq@ : Could you please provide update on bug


Thanks..!!

### mu...@chromium.org (2020-01-22)

alexandre.leborgne.83@gmail.com: I couldn't reproduce the bug on 79.0.3945.130.  Please give us more details about your setup:
- Which OS are you using?
- Can you reproduce after disabling all extensions (through chrome://extensions)?
- Does it repro for you in latest Chrome beta (M80)?

### al...@gmail.com (2020-01-22)

I tried to activate / deactivate my extensions and it turns out that this bug is due to this extension (https://chrome.google.com/webstore/detail/adblock-plus-free-ad-bloc/cfhdojbkjhnklbpkdaibdccddilifddb) which causes this security vulnerability.

I'm using Windows 10.0.18362
I can't try on the M80 version

### va...@chromium.org (2020-01-29)

Gentle ping: 
mustaq@ : As per the https://crbug.com/chromium/1035315#c12, could you please provide further inputs.

Thanks..!!

### mu...@chromium.org (2020-01-29)

Thanks alexandre.leborgne.83@gmail.com for spotting the root cause.

We were able to repro the bug on both Windows and Mac!  And also through a different ad-blocker extension:
  https://chrome.google.com/webstore/detail/adblock-%E2%80%94-best-ad-blocker/gighmmpiobklfepjocnamgkkbiglidom

Given the popularity of these extension, I am making this bug P2.

[Monorail components: Platform>Extensions]

### mu...@chromium.org (2020-01-29)

[Empty comment from Monorail migration]

### mu...@chromium.org (2020-01-29)

[Empty comment from Monorail migration]

### mu...@chromium.org (2020-01-29)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-01-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-29)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@google.com (2020-02-04)

All security bugs must have an owner. mustaq@, let me please assign this to you for the time being. Please re-assign if needed.

### mu...@chromium.org (2020-02-05)

Found a consistent repro, see below.  The core problem is that switching tabs by clicking on the tab-strip allows the bypass to happen within the first 5 seconds.

IMHO, browser UI clicks allowing the bypass seems bad.  The mentioned ad-blockers seem very popular, and there may be other extensions that repro this.


[Repro steps]

1. Install any of the ad-blocker extensions mentioned above.

2. Go to this test wrapper page:
  data:text/html,<a href="http://w3c-test.org/html/semantics/embedded-content/the-iframe-element/iframe_sandbox_allow_top_navigation_by_user_activation-manual.html">test link</a>

3. Right click on the link, then choose "open in a new tab".

4. Click on the tab-strip to switch away then come back to the test link tab.  Within 5 seconds right click on the link to open it in a new tab.

5. Repeat Step 4 but wait for more than 5 seconds.

[Outcome]
Tabs opened through Step 3 and Step 5 correctly prevents navigation, but the tab opened through Step 4 navigates away without user interaction.


### mu...@chromium.org (2020-02-05)

Good news is that none of the tab content is activated.  On receiving tabs.onActivated event, the background script gets activated here, which seems reasonable.

Still not sure why the content-initiated navigation is affected by the background activation state.


[1] https://cs.chromium.org/chromium/src/extensions/renderer/dispatcher.cc?rcl=d90d3c6341c9c65834e39fcd149b2dbbcdae9ddc&l=1058

### al...@gmail.com (2020-02-05)

[Comment Deleted]

### mu...@chromium.org (2020-02-05)

My last comment was partially wrong...all new tabs gets activated for those ad blockers even though tab-click doesn't activate them directly:
- Click on tab-strip sends tabs.onActivated event to the background script only and activates it.
- Upon navigation, the ad blockers send messages to navigated tab through this code [1], which activates the page.

[1] https://cs.chromium.org/chromium/src/extensions/renderer/native_renderer_messaging_service.cc?rcl=ba08c24e87fe57098cfe562967dfb328cda9547e&l=319


### [Deleted User] (2020-02-20)

mustaq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mu...@chromium.org (2020-02-20)

This is blocked on a reasonable and non-breaking fix for extension messaging user activation.  See blocker https://crbug.com/chromium/957633.

### mu...@chromium.org (2020-02-24)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6f9f33b66f3b94918efcdd41768a40b7c5e3df13

commit 6f9f33b66f3b94918efcdd41768a40b7c5e3df13
Author: Mustaq Ahmed <mustaq@google.com>
Date: Wed Feb 26 21:29:00 2020

Extension: remove USER_GESTURE_ENABLED state from tab-change events.

A past fix for activation propagation from an extension button to
extension script seems to have added additional user activation
propagation path from tab-strip to all installed extensions:
https://chromiumcodereview.appspot.com/10821120/

This crack caused every tab-switching to activate /all/ installed
extensions, which seems bad.  Because of this, we encountered a security
issue with unintended top frame navigation from an iframe.  (Luckily
only tab switching was affected, not tab clicking.)

A user interaction with the tab-strip is different from an interaction
with extension buttons.  Tab-strip interactions are similar to those
on any browser-provided UI element like top menu: they don't at all
indicate the user's intention to interact with any extension or website.
Therefore, like clicks on top-menu and unlike clicks on extension
buttons, tab-switching should suppress activating any background script
thus prevent access to use user-activation gated APIs like popup,
fullscreen, navigation, etc.

Bug: 957633, 1035315
Change-Id: I8d56e02a3a2966521b7bbc4f4efadf67e1acc371
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2072654
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Commit-Queue: Mustaq Ahmed <mustaq@chromium.org>
Cr-Commit-Position: refs/heads/master@{#744802}

[modify] https://crrev.com/6f9f33b66f3b94918efcdd41768a40b7c5e3df13/chrome/browser/extensions/api/tabs/tabs_event_router.cc
[modify] https://crrev.com/6f9f33b66f3b94918efcdd41768a40b7c5e3df13/chrome/browser/extensions/api/tabs/tabs_event_router.h


### mu...@google.com (2020-02-26)

Note: to verify the fix, please follow the consistent repro steps in https://crbug.com/chromium/1035315#c21.

### [Deleted User] (2020-02-27)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-02)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-02)

Requesting merge to beta M81 because latest trunk commit (744802) appears to be after beta branch point (737173).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-02)

This bug requires manual review: M81's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mu...@chromium.org (2020-03-02)

Here are most of the answers:
1. This is a very simple change.
2. CL to merge: https://chromium-review.googlesource.com/c/chromium/src/+/2072654
3. I just verified the fix in latest Win Canary (82.0.4075.0), with each of the ad blockers above.
4. *See below.*
5. Not a new feature.
6. N/A.


Q4 (M81 vs M82) is a tricky question.  If malicious subframes (possibly in ads) discover this, they could cause lots of user annoyances and could cause false clicks in ads.  The old behavior has been there for many years, and we don't know if it has been abused in the wild or if it has got attention already.  So I am slightly biased towards M81.

mmoroz@chromium.org, alexmos@chromium.org: what's your opinion from security perspective?

### pb...@google.com (2020-03-03)

+adetaylor@ (Security TPM) for M81 merge review

### ad...@chromium.org (2020-03-03)

I think I'm going to decline this merge to M81. Thanks for the answers though mustaq@. My rationale is that this is a Medium severity bug, and we only merge mediums back if it's trivially low-risk in every respect. Although the patch is trivial, this does (deliberately) change behavior which faces web developers and/or extension developers. Whilst it's probably very unlikely that any legitimate developers are relying on this functionality, we can't entirely rule it out. So I think we should organically release this in M82 so they have maximum possible time to react.

### mu...@chromium.org (2020-03-03)

Sounds good, given that the bug has been there for years already.

### na...@google.com (2020-03-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-03-05)

Congrats! The Panel decided to award $1,000 for this report! 

### na...@google.com (2020-03-05)

[Empty comment from Monorail migration]

### al...@gmail.com (2020-03-06)

Hello, Thank you for the attention you have given to my report. 
I wish to claim the reward. I am a resident of France. What information is necessary for you and by what means should I communicate it to you?

### ad...@chromium.org (2020-03-06)

Hi alexandre.leborgne.83, thanks again for the report! You don't need to do anything - someone from our finance team till get in touch with you.

How would you like to be credited in the Chrome release notes? (At present this isn't planned to be released until M82 so it will be a while before it appears.)

### al...@gmail.com (2020-03-06)

No idea .. what is normally done and where does it appear? In the commit message?
You can use :
Alexandre Le Borgne <alexandre.leborgne.83@gmail.com>

### bi...@google.com (2020-03-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-03-07)

Re https://crbug.com/chromium/1035315#c43, thanks, I'll just use your name. It appears on https://chromereleases.googleblog.com/.

### mu...@chromium.org (2020-03-09)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### mu...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### mu...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-06-04)

This issue was migrated from crbug.com/chromium/1035315?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature>IFrameSandbox, Platform>Extensions, UI>Browser>Navigation]
[Monorail blocking: crbug.com/chromium/957633]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051014)*

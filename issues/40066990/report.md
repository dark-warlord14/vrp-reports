# Security: Eyedropper API can confuse real cursor position which can cause users to be tricked into clicking unwanted positions (ie. accepting permission prompts)

| Field | Value |
|-------|-------|
| **Issue ID** | [40066990](https://issues.chromium.org/issues/40066990) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>Color |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | lu...@microsoft.com |
| **Created** | 2023-07-06 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

When an eyedropper is spawned on the main page and a window is opened, surprisingly, the main page overlay over the eyedropper. Doing this results in the cursor being invisible in the newly opened window.

Attackers can abuse this to cause clicks in unwanted position such as accepting a permission prompt.

**VERSION**  

Chrome Version: 117.0.5874.0 (Official Build) canary (64-bit) (cohort: Clang-64)  

Operating System: Windows 10 Version 22H2 (Build 19045.3086)

**REPRODUCTION CASE**

1. Go to <https://eastern-earthy-galley.glitch.me/accept-da-prompt.html>
2. Double or triple click to open a game. In the game, you are supposed to move the circle to the stationary circle and click.
3. Doing so in a specific way will result in the permission prompt being accepted. (The visuals can probably be improved)  
   
   **CREDIT INFORMATION**  
   
   **Externally reported security bugs may appear in Chrome release notes. If**  
   
   **this bug is included, how would you like to be credited?**  
   
   Reporter credit: Axel Chong

## Attachments

- [accept-da-prompt.html](attachments/accept-da-prompt.html) (text/plain, 370 B)
- [helper.html](attachments/helper.html) (text/plain, 897 B)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 179.8 KB)
- [helper.html](attachments/helper.html) (text/plain, 1.1 KB)

## Timeline

### [Deleted User] (2023-07-06)

[Empty comment from Monorail migration]

### ma...@google.com (2023-07-06)

I can't really repro this on Windows on macOS, which may be because the PoC is too specific to your screen resolution and window size? Could you upload a screen recording of what it's meant to look like perhaps?


### ma...@google.com (2023-07-06)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-07-07)

Sorry, I tried using Screencastify software but weirdly it causes the cursor to show in the video when it does not while recording. I instead used VLC media recorder to record the interaction.

I also took the opportunity to recode the game such that the prompt now opens when you are very close to the cursor. So now the game's objective is to try to align the circles as close as possible and then click.

### ha...@gmail.com (2023-07-07)

Updated helper.html

### ha...@gmail.com (2023-07-07)

Side note: I just realised that VLC media player hides the cursor by default. But the video shows what the game would look like when playing it without any screen recording software interfering with the mouse cursor.

### ha...@gmail.com (2023-07-07)

Hello martinkr@, any updates here?

### ha...@gmail.com (2023-07-07)

Hi martinkr@ I made a simplified PoC at https://scrawny-comet-mosquito.glitch.me/accept-da-prompt.html. In this PoC, the circle accurately reflects the where the actual cursor is. You can test by moving the circle to the permission prompt

Note that in this PoC it is not a game, it only demonstrates the fact that the cursor doesn't show when hovering over the permission prompt. 

### ma...@google.com (2023-07-07)

This PoC still doesn't work for me I'm afraid.

More generally, from playing around with the EyeDropper it doesn't look like "clicking" with the eyedropper doesn't actually result in a click to the UI element underneath the dropper. If I hover of a button with the dropper and click, the dropper disappears, but the button does not register a click. So even if the hypothetical victim in your PoC falls for the trick with the game, I still don't understand how the permission prompt allow button would actually get clicked. Can you elaborate?

pkasting@, you're in c/b/ui/views/eye_dropper/OWNERS. Any opinion on this one?


[Monorail components: Blink>Forms>Color]

### ha...@gmail.com (2023-07-07)

How it works is as follows:

(1) The dropper remains on the previous page.
(2) The newly window opened is in focus
(3) The mouse cursor is invisible on the newly open window amd can send input events -- this is the bug.
(4) As the mouse cursor is invisible, now I can trick the user on the actual location of the cursor.
(5) The input events can be sent by the invisible mouse cursor to a permission prompt on a newly opened window.
 

### ha...@gmail.com (2023-07-07)

Note I am testing w/ Canary

### ha...@gmail.com (2023-07-07)

Note that the mouse cursor actually can send inputs in the newly opened window*

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### pk...@chromium.org (2023-07-19)

I agree there's a problem here. Using the initial testcase I was able to hover the allow/block permission prompt buttons (visible by looking for the hover effect on the button) without seeing the actual mouse cursor above them.

I'm not really sure what the right fix is here. I don't know how the eyedropper stuff is specced. Offhand, I'd think the "right thing" is that the eyedropper cursor should always be Z-ordered above other windows, even windows that spawn after the eyedropper itself. This way, it's obvious where the cursor is.

### pk...@chromium.org (2023-07-19)

Hmm, looks like maybe iopopesc@microsoft no longer works (should probably be out of the OWNERS file then?) and honestly I'm probably not a very good OWNER there either as all I did was review the initial implementation work.

martinkr@, are you able to find someone from either the web platform or the top chrome sides to work on this? I'm somewhat bandwidth-constrained, but if all else fails, I could try to take a look here.

### pk...@chromium.org (2023-07-19)

[Empty comment from Monorail migration]

### pk...@chromium.org (2023-07-19)

[Empty comment from Monorail migration]

### sa...@microsoft.com (2023-07-24)

This has been fixed by https://chromium-review.googlesource.com/c/chromium/src/+/4698115.

### [Deleted User] (2023-07-24)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@microsoft.com (2023-07-24)

masonf@, pkasting@: This issue was fixed against the merged crbug. The dupe's security bug classification was removed. Should we do the same here?

### fl...@google.com (2023-07-24)

Hi, this week's security shepherd checking in.

Reading both bugs, it's hard for me to tell if they both are fixing the same thing.  It seems like the other bug was reporting an issue that was in fact easy to escape (which downgraded it to not-a-security-bug), but this "hovering over a permissions UI without realizing it" issue seems like it may in fact be a security bug, and thus perhaps should still be assgned a severity rating accordingly?  Perhaps the owner can give their judgment if that understanding is correct, and, if so, what the severity should be?

### ma...@chromium.org (2023-07-25)

Re https://crbug.com/chromium/1462723#c20, I can't see crbug.com/1464963 due to permissions. So hard for me to comment. https://crbug.com/chromium/1462723#c21 sounds relevant.

### sa...@microsoft.com (2023-07-25)

Thanks for the responses. flowerhack@, agree that this looks like a separate issue on second glance. lusanpad@ is already working on a fix. I'll unmerge the two issues as well.

### [Deleted User] (2023-07-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-25)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-07-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e09166a4272ae1d3fc2ef67b932e615cf97799ba

commit e09166a4272ae1d3fc2ef67b932e615cf97799ba
Author: Luis Juan Sanchez Padilla <lusanpad@microsoft.com>
Date: Wed Jul 26 20:16:44 2023

Do not show Eye Dropper if the owner frame is not active.

Currently, while the Eye Dropper is dismissed when a window focus change happens, it can still be opened if the parent frame is not focused on the time of invocation. This gives opening to a scenario in which a different Chrome window is focused but no cursor is shown on the screen as the Eye Dropper grid is being rendered behind the focused window. Attackers could use this opportunity to trick the user into clicking different parts of the screen, such as having the user grant unwanted permissions. This change fixes this issue by ensuring that the frame view is focused when the Eye Dropper is shown.

Bug: 1462723
Change-Id: I5f7ca420f2cedd07ce03b70966b64ad200bd32df
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4720045
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1175644}

[modify] https://crrev.com/e09166a4272ae1d3fc2ef67b932e615cf97799ba/chrome/browser/ui/views/eye_dropper/eye_dropper_view_aura.cc
[modify] https://crrev.com/e09166a4272ae1d3fc2ef67b932e615cf97799ba/chrome/browser/ui/views/eye_dropper/eye_dropper_view_aura_browsertest.cc
[modify] https://crrev.com/e09166a4272ae1d3fc2ef67b932e615cf97799ba/chrome/browser/ui/views/eye_dropper/eye_dropper_browsertest.cc


### lu...@microsoft.com (2023-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-27)

Requesting merge to beta M116 because latest trunk commit (1175644) appears to be after beta branch point (1160321).

Merge rejected: M116 is already shipping to beta and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-28)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-28)

Requesting merge to beta M116 because latest trunk commit (1175644) appears to be after beta branch point (1160321).

Merge review required: M116 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-29)

Requesting merge to beta M116 because latest trunk commit (1175644) appears to be after beta branch point (1160321).

Merge review required: M116 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-30)

Requesting merge to beta M116 because latest trunk commit (1175644) appears to be after beta branch point (1160321).

Merge review required: M116 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-31)

Since this issue was erroneously set to Pri-2 originally, sheriffbot rejected it's own merge request. As a medium severity issue, this fix should be backmerged to M116. 
116 merge approved, please merge this fix to branch 5845 at soonest so this fix can be included in the next M116 Beta update. Thank you! 

### am...@chromium.org (2023-07-31)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-08-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/09055d0498542343b65403a2cee889171f42e62e

commit 09055d0498542343b65403a2cee889171f42e62e
Author: Luis Juan Sanchez Padilla <lusanpad@microsoft.com>
Date: Tue Aug 01 01:00:09 2023

Do not show Eye Dropper if the owner frame is not active.

Currently, while the Eye Dropper is dismissed when a window focus change happens, it can still be opened if the parent frame is not focused on the time of invocation. This gives opening to a scenario in which a different Chrome window is focused but no cursor is shown on the screen as the Eye Dropper grid is being rendered behind the focused window. Attackers could use this opportunity to trick the user into clicking different parts of the screen, such as having the user grant unwanted permissions. This change fixes this issue by ensuring that the frame view is focused when the Eye Dropper is shown.

(cherry picked from commit e09166a4272ae1d3fc2ef67b932e615cf97799ba)

Bug: 1462723
Change-Id: I5f7ca420f2cedd07ce03b70966b64ad200bd32df
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4720045
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1175644}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4735601
Auto-Submit: Luis Sanchez Padilla <lusanpad@microsoft.com>
Cr-Commit-Position: refs/branch-heads/5845@{#990}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/09055d0498542343b65403a2cee889171f42e62e/chrome/browser/ui/views/eye_dropper/eye_dropper_view_aura.cc
[modify] https://crrev.com/09055d0498542343b65403a2cee889171f42e62e/chrome/browser/ui/views/eye_dropper/eye_dropper_browsertest.cc


### am...@google.com (2023-08-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-03)

Congratulations, Axel! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-08-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1462723?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1464963]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066990)*

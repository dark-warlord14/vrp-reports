# Security: Chrome for Android Prevent Back Button to Exit Fullscreen Mode using Text Selection

| Field | Value |
|-------|-------|
| **Issue ID** | [40057691](https://issues.chromium.org/issues/40057691) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>FullScreen, UI>Browser>Selection |
| **Platforms** | Android |
| **CVE IDs** | CVE-2021-29983 |
| **Reporter** | su...@gmail.com |
| **Assignee** | la...@chromium.org |
| **Created** | 2021-10-24 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

After call document.execCommand("selectAll") to select the text with the appearance of the Android text selection menu, then interestingly after call document.getSelection().removeAllRanges() while text selection menu still appears it will prevent back button including on full screen mode, therefore user won't able to exit fullscreen mode with the back button.

As user unable to exit the fullscreen after pressing the back button, it can be abused to convinced the user that after press the back button it already exit the fullscreen mode, so the user can be tricked that it already shows the legitimate address bar.

As described above, I do believe this is a security issue, previously I have reported similar issue (lock exit full screen mode) that affect Firefox for Android <https://www.mozilla.org/en-US/security/advisories/mfsa2021-33/#CVE-2021-29983>

**VERSION**  

Tested on:

- Chrome 94.0.4606.85
- Chrome Beta 96.0.4664.17
- Chrome Dev 97.0.4676.0
- Chrome Canary 97.0.4680.0  
  
  Operating System: Android 11; Mi 9T and Android 10; Android Emulator Pixel\_2\_API\_29

**REPRODUCTION CASE**

1. Visit attached spoof-lockfullscreen-textselection.html
2. Tap anywhere on the page
3. After Android text selection menu appears, repeatedly press back the back button
4. The browser won't exit the fullscreen

**CREDIT INFORMATION**  

Irvan Kurniawan (sourc7)

## Attachments

- [spoof-lockfullscreen-textselection.html](attachments/spoof-lockfullscreen-textselection.html) (text/plain, 621.7 KB)
- [Chrome for Android - Fullscreen Exit Lock with Text Selection Menu.mp4](attachments/Chrome for Android - Fullscreen Exit Lock with Text Selection Menu.mp4) (video/mp4, 424.2 KB)
- [spoof-lockfullscreen-hidetextselection.html](attachments/spoof-lockfullscreen-hidetextselection.html) (text/plain, 621.8 KB)
- [Chrome for Android - Prevent Back to Exit Fullscreen with Hidden Text Selection Menu.mp4](attachments/Chrome for Android - Prevent Back to Exit Fullscreen with Hidden Text Selection Menu.mp4) (video/mp4, 423.5 KB)

## Timeline

### [Deleted User] (2021-10-24)

[Empty comment from Monorail migration]

### es...@chromium.org (2021-10-25)

editing owners, could you PTAL?

[Monorail components: Blink>Editing>Selection UI>Browser>FullScreen]

### [Deleted User] (2021-10-25)

[Empty comment from Monorail migration]

### yo...@chromium.org (2021-10-26)

ctzsm@, could you take look?

Because Blink doesn't control full screen mode.
Thanks!

[Monorail components: -Blink>Editing>Selection]

### [Deleted User] (2021-10-26)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2021-10-26)

Looking at the spoof-lockfullscreen-textselection.html source code, I think either we didn't issue dismiss for document.getSelection().removeAllRanges(), or the dismissal signal reached to browser earlier than show selection menu signal for document.execCommand("selectAll", false).

I am also not very familiar with the fullscreen support in Chrome, so don't quite know why the selection menu will block back button to exit fullscreen mode, but can take a look.

However I don't think this is that critical, there are many new Android devices don't have the navigation bar, so user doesn't use navigation bar for going back, I am not sure if the gesture navigation is also blocked though. On the other hand, I think people will try to engage with the selection menu if they see it on the screen rather than trying with the bottom navigation bar. But I'll lean to the security team to review.

[Monorail components: UI>Browser>Selection]

### su...@gmail.com (2021-11-01)

> However I don't think this is that critical, there are many new Android devices don't have the navigation bar, so user doesn't use navigation bar for going back, I am not sure if the gesture navigation is also blocked though. On the other hand, I think people will try to engage with the selection menu if they see it on the screen rather than trying with the bottom navigation bar. But I'll lean to the security team to review.

It also works on gesture navigation, the back swipe is also blocked. I also found I able to hide the text selection menu using marginLeft: 99% so user won't see the  selection menu.

### ct...@chromium.org (2022-03-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-28)

This issue has been Available for over a year. If it's no longer important or seems unlikely to be fixed, please consider closing it out. If it is important, please re-triage the issue.

Sorry for the inconvenience if the bug really should have been left as Available.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-03-28)

This issue was migrated from crbug.com/chromium/1262845?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>FullScreen, UI>Browser>Selection]
[Monorail components added to Component Tags custom field.]

### am...@chromium.org (2025-01-08)

Assigning current Blink editing selection owners.
Since this issue currently has no owner. That all being said, this is at least a functional bug and in terms of security, is very borderline as consideration of a vulnerability very little attacker utility or potential for user harm. The spoof is somewhat believable, which is this is remaining type:vulnerability / S3 for the time being. But otherwise, there is a fullscreen notification and a user could easily escape from fullscreen mode rather than reliance on the back button.

### su...@gmail.com (2025-01-08)

Thanks @amyressler for the update and assignee for this bug.

However, I no longer able to reproduce the bug, when I press back it go back as normally.

I still able reproduce this on older version, I think it has been fixed by commit around 2024, I'm currently take a look to see which commit that addresses this bug. I'll post the update.

### su...@gmail.com (2025-01-09)

After looking through past commit, and re-compile the Chromium, I found this bug already been fixed by [issue 40065810](https://issues.chromium.org/issues/40065810), after commit [[M116] Exit fullscreen before dismissing selection popup via back press.](https://chromium.googlesource.com/chromium/src/+/c439e21e2a8321105df6fd7f981d620513231f02), when press back or trigger gesture back on the testcase, it will now exit the fullscreen.

However, the text selection menu still intact, the text selection menu will disappear after commit on around 2024, which fully fixes the gesture-back or button-back to become working properly. I'll also find the commit and post the update.

### su...@gmail.com (2025-01-09)

@amyressler I see the [issue 40065810](https://issues.chromium.org/issues/40065810) is similar to this bug, which is using text selection menu (the testcase.html on that issue is same to my [issue 40062567](https://issues.chromium.org/issues/40062567), which previously I was also aware that testcase can cause same as this issue)

I really hope that it can be rated the same as on [issue 40065810](https://issues.chromium.org/issues/40065810), which can attacker used to "can make people think they are escaping the fullscreen to fake the UI." [issue 40065810 -> comment 13](https://issues.chromium.org/issues/40065810#comment13), so when victim press back or gesture-back it can trick victim that he already exited the fullscreen and seeing the legitimate address bar. I also demonstrate I able to hide the selection menu as on [comment 8](https://issues.chromium.org/issues/40057691#comment8), which make more convincing, thanks!

### su...@gmail.com (2025-01-11)

> However, the text selection menu still intact, the text selection menu will disappear after commit on around 2024, which fully fixes the gesture-back or button-back to become working properly. I'll also find the commit and post the update.

Ok, after re-compile the Chromium, I found that the [Merge select and paste action modes [6/x].](https://issues.chromium.org/issues/320643289) is fixed the issue. So, when pressing back, it able to dismiss the text selection menu and navigate back (but have to press back twice or swipe twice to dismiss the selection menu, when try on attached testcase html above).

However, I guess that no longer security issue, as we [able to exit fullscreen after the first back-button or first swipe](https://chromium.googlesource.com/chromium/src/+/c439e21e2a8321105df6fd7f981d620513231f02) after that commit.

### su...@gmail.com (2025-01-11)

@amyressler after my analysis above, can this issue also be marked as Fixed? Thanks!

### am...@chromium.org (2025-01-24)

- lazzzis@ the patch author of <https://crrev.com/c/4730397> to confirm
- muyaoxu@ working through fullscreen issues to this was the canonical bug for this issue in Fullscreen in Android

### su...@gmail.com (2025-03-04)

lazzzis@ as this already fixed by [issue 40065810](https://issues.chromium.org/issues/40065810), after commit [[M116] Exit fullscreen before dismissing selection popup via back press.](https://chromium.googlesource.com/chromium/src/+/c439e21e2a8321105df6fd7f981d620513231f02).

Could you please take a look, and marked this as Fixed, thanks!

### ch...@google.com (2025-03-12)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-03-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
report of lower impact security UI issue 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-21)

Congratulations Irvan! Thank you for your efforts and reporting this issue to us.

### su...@gmail.com (2025-03-21)

Thank you very much for the reward! I really appreciate it 🙏

### ch...@google.com (2025-06-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057691)*

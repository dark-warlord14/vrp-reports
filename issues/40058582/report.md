# Security: Autofill prompt can be obscured by Picture-in-Picture overlay, allows stealthy autofill data theft

| Field | Value |
|-------|-------|
| **Issue ID** | [40058582](https://issues.chromium.org/issues/40058582) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | sc...@google.com |
| **Created** | 2022-01-25 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

A page can render an autofill prompt under a Picture-in-Picture (PiP) overlay. The prompt will remain open under the PiP overlay, and selecting an autofill item using the keyboard will send data to the background page. This bypasses the fix in commit 3fb0945de5e50b8e6d2f9b0dd8a65e3f7a767b14 and other checks to ensure the autofill prompt is only visible in safe conditions.

This vulnerability has same impacts as <https://crbug.com/chromium/1290213>. The fix may be the same, since this also occurs due to the use of ShowInactive() on a window shown above the autofill prompt. But filing separately since this overlay intentionally stays above other windows and may require different considerations and fixes.

<https://source.chromium.org/chromium/chromium/src/+/main:content/browser/picture_in_picture/picture_in_picture_window_controller_impl.cc;l=92;drc=2e2b046d9f992abdf56668cb451d8e42447d290e> calls window\_->ShowInactive() on the PiP overlay window (not the page's window).

The PiP overlay will only be able to obscure autofill prompts under the overlay, and at least on my Windows system, the PiP overlay consistently appears near the bottom-right of the screen. Therefore, a successful attack will only work if the window is maximized or covers the bottom-right of the screen. The PoC checks the window position and instructs the user to move or maximize the window if it's not covering the expected area.

ADDITIONAL CONTEXT  

Opening the autofill prompt and selecting an autofill item are possible only via keyboard input, since the down arrow selects the autofill item on the first step, and the PiP overlay prevents any mouse interaction with the obscured autofill prompt on the second step.

I've tested this with addresses (which includes name + email), credit cards, and single-field autofills.

**VERSION**  

Chrome Version: 97.0.4692.71 Stable, 100.0.4850.3 Canary  

Operating System: Windows 10 Version 20H2 (Build 19042.1415)

**REPRODUCTION CASE**  

PoC for address (multiple fields):  

Prerequisites: Have at least one address with email address in chrome://settings/addresses

1. Navigate to <https://alesandroortiz.com/security/chromium/autofill-obscured-pip.html>
2. Press down arrow in keyboard.
3. Press enter (or tab) in keyboard.  
   
   (After step 3, extension will close the PiP overlay on a delay to make PoC behavior clearer, but the delay is not needed. You can also manually close the PiP overlay.)
4. Check background page output.

PoC for credit card (multiple fields):  

Prerequisites: Have at least one credit card in chrome://settings/payments

1. Navigate to <https://alesandroortiz.com/security/chromium/autofill-obscured-pip.html?creditcard> (or use in-page links)
2. (Same as first PoC)
3. (Same as first PoC)
4. (Same as first PoC)

PoC for easier debugging (partially obscured):  

Prerequisites: Have at least one credit card in chrome://settings/payments

1. Navigate to <https://alesandroortiz.com/security/chromium/autofill-obscured-pip.html?debug> (or use in-page links)
2. (Same as first PoC)
3. (Same as first PoC)
4. (Same as first PoC)

For autofill data theft PoCs:  

Observed: Autofill prompt remains open below the PiP overlay. Upon selection with keyboard, data is provided to page.  

Expected: Autofill prompt is closed when below the PiP overlay (or other safer behavior).

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [autofill-obscured-pip.mp4](attachments/autofill-obscured-pip.mp4) (video/mp4, 579.5 KB)
- [autofill-obscured-pip.html](attachments/autofill-obscured-pip.html) (text/plain, 4.4 KB)
- [autofill-obscured-pip-overlay.mp4](attachments/autofill-obscured-pip-overlay.mp4) (video/mp4, 8.7 KB)

## Timeline

### [Deleted User] (2022-01-25)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-01-25)

Minor correction: "After step 3, extension will close the PiP overlay on a delay..." should read "...page will close..."

### al...@alesandroortiz.com (2022-01-25)

Clarification on potentially shared fixes: "The fix may be the same as https://crbug.com/chromium/1290098 or 1290213, since this also occurs due to the use of ShowInactive()..."

### ca...@chromium.org (2022-01-25)

I can reproduce, so triaging the same as the related bugs. schwering: Feel free to duplicate if this does end up having the same fix as the other bugs. Thanks

[Monorail components: UI>Browser>Autofill]

### [Deleted User] (2022-01-25)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-01-25)

This repros on 97 Stable (and probably before), so should be FoundIn-97 and Security_Impact-Stable.

### [Deleted User] (2022-01-26)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-26)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-26)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2022-01-27)

Is this bug applicable to Android, iOS and Chrome OS?  If yes, please apply appropriate OSs label. 

### ma...@google.com (2022-01-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-27)

This does not appear to be a regression and was discovered on and reported by the OP in Stable/M97; appears to go back farther so labeling as FoundIn-96 and this should not be considered a release blocker for M98 stable 

### [Deleted User] (2022-01-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-08)

schwering: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-24)

schwering: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2022-03-03)

After filing https://crbug.com/chromium/1302159, I realized the PiP behavior in this report probably has the same impacts as https://crbug.com/chromium/1302159 if the obscured area can fit behind the PiP overlay. I haven't verified this yet, but I don't see why it wouldn't work for most or all scenarios in the other issue.

### al...@alesandroortiz.com (2022-03-15)

Friendly ping: Any updates on this issue?

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-06-03)

Friendly ping: Any updates on this issue? Still repros on 104.0.5101.0 Canary. Note potential additional impacts noted in https://crbug.com/chromium/1290664#c20.

### sc...@google.com (2022-06-14)

Thanks, I'll try to finally look into this week.

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-09-28)

Friendly ping: This still repros on 108.0.5327.1 Canary on Windows 10. Probably has same impacts as https://crbug.com/chromium/1302159.

### tl...@chromium.org (2022-09-30)

kerenzhu@ do you know if your layering work will address this issue?

### ke...@chromium.org (2022-09-30)

Probably need to apply some mutual exclusion here. The z-order trick won't work, because the PiP window is an always-on-top window, which is ought be higher than other windows, including autofill popup and windows of other application.

### ba...@chromium.org (2022-09-30)

Would it be reasonable to use chrome/browser/picture_in_picture/picture_in_picture_window_manager.h as a choke point by making it observable? While any document is in PiP mode or when a document enters PiP mode we would suppress/close the autofill dropdown. WDYT?

### ke...@chromium.org (2022-09-30)

Sounds reasonable to me. A less intrusive approach might be to block autofill dropdown only if it will be occluded, like is done with the interop between the autofill dropdown and the permission bubble (https://crrev.com/c/3236729).

### al...@alesandroortiz.com (2022-09-30)

FWIW, this also occludes most other browser UI including those identified in https://crbug.com/chromium/1302159. The main limitation is the position of the PiP window being in the bottom right of the screen. However, a website can create a window with an additional user interaction in that area with the sensitive UI, or an extension can create the window without user interaction. I can develop PoCs if helpful for those other scenarios in the next week or two.

### al...@alesandroortiz.com (2022-11-29)

Friendly ping: Any updates on this issue? Still repros in 107.0.5304.107 Stable. Probably has same impacts as https://crbug.com/chromium/1302159.

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### ba...@chromium.org (2022-12-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-02-14)

See related https://crbug.com/chromium/1416380.

### al...@alesandroortiz.com (2023-02-23)

I saw https://crbug.com/chromium/1358647 which appears to be a (later) duplicate of this issue.

Fix for that issue was released in 109.0.5408.0 Canary, 109.0.5414.74 Stable: https://chromiumdash.appspot.com/commit/ff1874e9b31c51520032643e4ce3101a42743dee

Issue does not repro using PoC [1] from my report above on 112.0.5612.0 Canary and 110.0.5481.104 Stable, with behavior consistent with the fix above.

Within a week or so I will perform bisect to confirm and also look at patch more closely to see if there are any bypasses.

[1] https://alesandroortiz.com/security/chromium/autofill-obscured-pip.html


### al...@alesandroortiz.com (2023-02-27)

Bisect confirms commit ff1874e9b31c51520032643e4ce3101a42743dee fixes issue. Verified using snapshot builds from https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/

Repro (before patch): build 1068096 
No repro (after patch): build 1068146

Feel free to mark this as fixed.

Will VRP also reward this issue, since I was first to report by ~9 months? (IIRC in similar cases of undetected duplicates, first report has been rewarded despite duplicate already being rewarded.)

### am...@google.com (2023-03-16)

[Comment Deleted]

### am...@chromium.org (2023-03-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-16)

Hi Alesandro, thank you for reaching out to let us know. Apologies that this issue has appeared to have been overlooked.
This will be certainly be considered by VRP panel at a future session once the owner has a chance to verify or add any comments. VRP assessment outcome will be updated here once that occurs. 

schwering@ it appears this issue was resolved by https://chromium-review.googlesource.com/c/chromium/src/+/3959939 (landed on 1358647). 
Closing as fixed accordingly. PTAL to verify or update if there are any issues with this.

### [Deleted User] (2023-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-22)

Congratulations, Alesandro! The VRP Panel has decided to award you $5,000 for this report Thank you for your efforts and reporting this issue to us! Thank you again for your patience while this issue got resolved in terms of report duplications. 

### am...@google.com (2023-03-27)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-04-22)

Thanks for the reward and sorting out the duplicate reports!

### al...@alesandroortiz.com (2023-04-22)

[Comment Deleted]

### [Deleted User] (2023-06-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

This issue was migrated from crbug.com/chromium/1290664?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058582)*

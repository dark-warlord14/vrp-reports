# Security: PiP window can obscure sensitive UI: External protocol dialog

| Field | Value |
|-------|-------|
| **Issue ID** | [40067401](https://issues.chromium.org/issues/40067401) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2023-07-13 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

A PiP window can obscure sensitive UI and users can interact with the obscured UI.

This report is for the external protocol dialog. This report applies to both Video PiP and Document PiP.

For external protocol dialog, impact is page can launch app with attacker-controlled arguments without user awareness. With slightly different instructions, the user can also check "Always allow..." to bypass future dialogs for the protocol.

ADDITIONAL CONTEXT (same across related bugs)  

Document PiP is currently in origin trial and can also be enabled via flag. Will be on by default in M116 Stable (August). It also seems to be only enforced by renderer, so in theory a compromised renderer should also be able to toggle the flag.

Filing separate bugs for each impacted UI, since each bug probably requires distinct fixes specific to the UI element, similar to previous bugs where a PiP window obscures sensitive UI [1][2]. Feel free to merge reports if there's a common patch.

[1] <https://crbug.com/chromium/1290664>, autofill, commit ff1874e9b31c51520032643e4ce3101a42743dee  

[2] <https://crbug.com/chromium/1394410>, permission prompts, commit 073278eae6d6ce07cc40107567907e545ec56157

The size of PiP windows is limited to ~80% of the screen, enforced by the browser [3][4].  

[3] Max video PiP size set here: <https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/ui/views/overlay/video_overlay_window_views.cc;l=627;drc=f09c12c84b39d13189a7039a05253ca3766d4751>  

[4] Max document PiP size set here: <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/picture_in_picture/picture_in_picture_window_manager.cc;l=28;drc=af9589e7a772b7df79d7e4dd7197f66b7b6b465c>

BISECT  

Current PoCs work after commit 67df4c338d22f5d9f3e16d7a9e78187eba17fcbb (Sept 2022), when Video PiP size was increased to 80% of display. Prior to that commit, Video PiP size was limited to 50% of display.

A modified PoC that considers the 50% limit works down to commit 8a3927cdbddfd2a03a94990138235f0acfed4d91 (Dec 2020).

Prior to the Dec 2020 commit, a modified PoC seems to work down to commit 13df529ae56f4319392e222acb1359c8341e643a (Jan 2019).

Prior to the Jan 2019 commit, maybe yet another modified PoC might work.

**VERSION**  

Chrome Version: (All channels) 114.0.5735.199 Stable, 115.0.5790.90 Beta, 116.0.5845.14 Dev, 117.0.5881.0 Canary  

Operating System: Windows 10 Version 22H2 (Build 19045.3086)

**REPRODUCTION CASE**  

PoC, Video PiP:

1. Navigate to <https://alesandroortiz.com/security/chromium/pip-video-external-protocol.html>  
   
   1a. Move window as instructed, if page indicates this. (A PoC can also open a new window to avoid manual moving.)
2. Press any key (such as an arrow key) once, or click anywhere once.
3. Press any arrow key once
4. Press enter

PoC, Document PiP:  

Prerequisites: Enabled Document PiP flag chrome://flags/#document-picture-in-picture-api

1. Navigate to <https://alesandroortiz.com/security/chromium/pip-document-external-protocol.html>  
   
   1a. Move window as instructed, if page indicates this. (A PoC can also open a new window to avoid manual moving.)
2. Press any key (such as an arrow key) once, or click anywhere once.
3. Press any arrow key once
4. Press enter

For both PoCs:  

Observed: PiP window obscures external protocol dialog. User can interact with external protocol dialog. Page can launch app with attacker-controlled args without user awareness.  

Expected: User cannot interact with external protocol dialog while obscured. Page cannot launch app without user awareness.

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [pip-video-external-protocol.html](attachments/pip-video-external-protocol.html) (text/plain, 3.1 KB)
- [pip-document-external-protocol.html](attachments/pip-document-external-protocol.html) (text/plain, 2.4 KB)
- [pip-video-external-protocol.mp4](attachments/pip-video-external-protocol.mp4) (video/mp4, 578.6 KB)
- [pip-document-external-protocol.mp4](attachments/pip-document-external-protocol.mp4) (video/mp4, 607.1 KB)
- [pip-video-external-protocol-chromeos.html](attachments/pip-video-external-protocol-chromeos.html) (text/plain, 3.0 KB)
- [pip-video-external-protocol-chromeos.webm](attachments/pip-video-external-protocol-chromeos.webm) (video/webm, 301.0 KB)
- [pip-document-external-protocol-July2024.html](attachments/pip-document-external-protocol-July2024.html) (text/html, 2.6 KB)
- [pip-document-external-protocol-July2024.mp4](attachments/pip-document-external-protocol-July2024.mp4) (video/mp4, 3.3 MB)
- [pip-document-external-protocol-July2025.html](attachments/pip-document-external-protocol-July2025.html) (text/html, 1.5 KB)
- [pip-document-external-protocol-July2025.mp4](attachments/pip-document-external-protocol-July2025.mp4) (video/mp4, 1.0 MB)

## Timeline

### [Deleted User] (2023-07-13)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-07-14)

Note that this report is for the hidden UI interaction behavior. For the Video PiP resize report, which has additional standalone impacts, see https://crbug.com/chromium/1464825. For the Document PiP resize report, which has additional standalone impacts, see https://crbug.com/chromium/1464829.

### al...@alesandroortiz.com (2023-07-14)

[Comment Deleted]

### al...@alesandroortiz.com (2023-07-14)

Also see related https://crbug.com/chromium/1464757 and https://crbug.com/chromium/1464760 for other impacted UIs.

### rs...@chromium.org (2023-07-18)

This does not repro on Mac because the external protocol dialog is not navigable with the keyboard. But this does repro on Windows and Linux (I don’t have a Chromebook handy to test CrOS). Triaging the same as https://crbug.com/chromium/1464825.

[Monorail components: Blink>Media>PictureInPicture]

### [Deleted User] (2023-07-18)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-07-19)

On a physical ChromeOS device, external protocol dialogs only seem to work if there's an Android app installed. For example, installing Spotify and updating the PoC to call `spotify:` instead of `ms-calculator:` will show a different dialog which only requires a single enter keypress to run.

Attached is a ChromeOS-specific PoC (although existing PoC could easily be adapted to detect ChromeOS), along with video recording. Repro was on Chrome 114.0.5735.205 Stable, ChromeOS 15437.61.0 Stable.

Repro steps for ChromeOS:
Setup: Install Spotify as an example target app (no need to login or anything).
1. Navigate to https://alesandroortiz.com/security/chromium/pip-video-external-protocol-chromeos.html
2. Press any key once
3. Press enter

Observed: PiP window obscures external protocol dialog. User can interact with external protocol dialog. Page can launch app with attacker-controlled args without user awareness.
Expected: User cannot interact with external protocol dialog while obscured. Page cannot launch app without user awareness.

### is...@google.com (2023-07-19)

This issue was migrated from crbug.com/chromium/1464759?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### al...@alesandroortiz.com (2024-07-17)

This still repros for Video PiP, but needs an updated PoC for Document PiP after a commit [1] changed the focus behavior. Tested on 126.0.6478.127 Stable.

[1] <https://crrev.com/9e221cc13a05d316994d6ac1c004d5dd442773c3> `[document pip] Focus the window when opened manually`

### al...@alesandroortiz.com (2024-07-17)

Document PiP focus behavior landed in M120: <https://chromiumdash.appspot.com/commit/9e221cc13a05d316994d6ac1c004d5dd442773c3>.

However, an attacker can re-focus the opener tab and have the same behavior after commit <https://crrev.com/73a9a9977689ec4665759588480b153b08cedb50> which shipped in M123: <https://chromiumdash.appspot.com/commit/73a9a9977689ec4665759588480b153b08cedb50>

Updated PoC for Document PiP attached.

PoC, Document PiP:

1. Navigate to <https://alesandroortiz.com/security/chromium/pip-document-external-protocol-July2024.html>   
   
   1a. Move window as instructed, if page indicates this. (A PoC can also open a new window to avoid manual moving.)
2. Press any key (such as an arrow key) once, or click anywhere once.
3. Press any arrow key twice
4. Press enter

Observed: PiP window obscures external protocol dialog. User can interact with external protocol dialog. Page can launch app with attacker-controlled args without user awareness.

Expected: User cannot interact with external protocol dialog while obscured. Page cannot launch app without user awareness.

### al...@alesandroortiz.com (2025-07-05)

This was fixed by <https://crrev.com/49c81fdf7cdc912c9aa22744c9487976b67e02ad> (June 16, 2025). Verified through bisect and on 140.0.7278.0 Canary on Windows 10.

Feel free to mark as fixed. The other crbugs seem newer, so not sure if those should be duped into this crbug.

### ch...@google.com (2025-07-07)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### al...@alesandroortiz.com (2025-07-10)

Friendly ping: Can someone please review [#comment13](https://issues.chromium.org/issues/40067401#comment13) and then mark as fixed again? Thanks!

### am...@chromium.org (2025-07-21)

I have added this the CL and re-closed this issue as Fixed.
It is important to note, however, that the issues tagged in this CL were deemed not sufficiently impactful spoofing issues to be considered security vulnerabilities.

This POC is slightly different than those in the issues present, though there are still pretty significant user gestures required here and does require the user to somewhat put themselves in the position of a self-own though not quite to the extent of the later reported issues. Either way, I'll keep this as a vulnerability for now and we can discuss at a future VRP panel session.

### al...@alesandroortiz.com (2025-07-21)

Thanks for marking as fixed and for the heads up on the classification of the other issues.

I quickly improved the PoC to use a popup and move around some steps so window positioning isn't a prerequisite anymore, while keeping same number of keyboard interactions with a normal renderer:

- Hold any key, then press arrow key, then enter. (3 interactions)
- Press any key twice, then arrow key, then enter. (4 interactions)

### Reproduction Steps

1. Navigate to <https://alesandroortiz.com/security/chromium/pip-document-external-protocol-July2025.html>
2. Hold enter (or any key)
3. Press any arrow key, then enter.

---

For the VRP Panel to consider when making a decision:

- Launching external protocols has been used to achieve RCE when chained with an OS vulnerability or installed app vulnerability. The target's prerequisites are mitigating factors, but these attacks have been seen ITW before. [1](https://unit42.paloaltonetworks.com/cve-2022-30190-msdt-code-execution-vulnerability/) [2](https://parsiya.net/blog/2021-03-17-attack-surface-analysis-part-2-custom-protocol-handlers/)
- Compromised renderers can open popups and PiP windows without user interaction (see [issue 338398040](https://issues.chromium.org/issues/338398040)), which would reduce user interaction to the "press arrow, then enter" to launch app. For real attacks, there's likely better uses of a compromised renderer than this, but could still be beneficial to attackers if they don't have access to another sandbox escape.

3-4 user interactions with normal renderer is certainly a mitigating factor, but IMO there's still some security impacts because of the well-known potential of RCE/sandbox escape when chained with external OS/app vulnerabilities.

### sp...@google.com (2025-07-24)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact security UI issue with multiple UI interaction preconditions


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### al...@alesandroortiz.com (2025-07-24)

Thanks for reward!

### ch...@google.com (2025-10-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067401)*

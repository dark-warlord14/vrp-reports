# Security: FedCM prompt bubble renders outside of opening window, causing various issues

| Field | Value |
|-------|-------|
| **Issue ID** | [338233148](https://issues.chromium.org/issues/338233148) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Identity>FedCM |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | ta...@google.com |
| **Created** | 2024-05-01 |
| **Bounty** | $2,000.00 |

## Description

#### SUMMARY

The FedCM prompt has two dialog types [1]: bubble and modal. The bubble dialog can render outside of the page, causing impacts such as:

- Origin confusion by user
- Hidden login
- Obscuring sensitive UI

(It also feels broken when in the wrong place, so this is a functional issue too.)

Showing the FedCM prompt does not require user interaction.   

A compromised renderer can open popups without user interaction, so these attacks can be performed with minimal user interaction in some cases.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.h;l=52;drc=6f3f85b321146cfc0f9eb81a74c7c2257821461e>

#### VULNERABILITY DETAILS

AccountSelectionBubbleView::GetBubbleBounds() [2] overrides the bubbles bounds to ensure desired placement, by setting margins to the top and right of the bubble. Unfortunately, this does not take into account all window sizes and positions, often resulting in the bubble being rendered in an unsafe manner for the bubble itself or for other UIs.

The issues occur in non-maximized windows, and are most impactful in very small windows.
When the opening window's top edge is near the top of the screen, the FedCM bubble is shown at a significant distance below the opening window.   

The position is also unexpected when the opening window's right edge is near the right of the screen.   

The position is also not updated when the opening window is near the bottom of the screen, causing the bubble to render mostly offscreen.

[2] AccountSelectionBubbleView::GetBubbleBounds(): <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/webid/account_selection_bubble_view.cc;l=582;drc=6f3f85b321146cfc0f9eb81a74c7c2257821461e>

Impacts:

- Origin confusion by user:
  
  When the bubble is opened from a small popup, and the popup is near the top edge, the FedCM bubble can render over a page on another origin while appearing to be from the page due to the distance from the opening popup.
  
  While the bubble still shows the correct origin (albeit in relatively small text), the bubble appears to be associated with the shown page instead of the popup.
- Hidden login:
  
  When the opening window is near the bottom of the screen, the FedCM bubble remains rendered below the window, effectively hiding most if not all of it from the user while remaining fully interactive. An attacker can instruct the user to press keys, resulting in login without user awareness.
  
  Other bubbles, such as permission prompts, generally stay within the browser window, and avoid being fully obscured when moved offscreen by moving away from the screen edge. This safer behavior is overridden for FedCM bubbles.
- Obscured sensitive UI:
  
  The bubble can obscure sensitive UIs such as permission prompts, autofill prompts, and other sensitive UIs.   
  
  Other sensitive UIs generally have input protections in place to avoid interaction when obscured. However, these checks can be bypassed when fully obscured by the FedCM bubble. Partial obscuring also work well, as shown in the permission prompt PoC.

#### VERSION

Chrome Version: 126.0.6448.0 Canary, 124.0.6367.92 Stable. Verified repro down to 105.0.5127.0

Operating System: Windows 10 Version 22H2 (Build 19045.4170)

#### BISECT

Introduced by commit <https://chromium.googlesource.com/chromium/src/+/917ae35ff6c8ad5fd1c1e5c9732c425aad6d0c57>

Landed in 105.0.5127.0 in June 2022: <https://chromiumdash.appspot.com/commit/917ae35ff6c8ad5fd1c1e5c9732c425aad6d0c57>

Verified repro down to 105.0.5127.0.

FedCM is enabled by default starting with M108: <https://caniuse.com/mdn-api_identitycredential>

Between 105 and 108, behavior repros with FedCM flag enabled. Some older versions prior to M108 need modified PoCs for repro, since the API changed a couple of times before reaching Stable.

old-chrome.png and old-chrome-expanded.png show behavior prior to the commit.

#### REPRODUCTION CASE

**Note**: While not implemented in these PoCs, compromised renderers can open windows without user interaction, reducing the amount of repro steps.

**Important**: The hosted PoCs use IDPs hosted on Glitch.com which may require warm up. When not warmed up, the hosted PoCs will not work as expected. This is not a relevant detail in real scenarios: an attacker can either host their own IDPs or use a legit IDP.
To warm up the IDPs, please visit these URLs once shortly before running any set of PoCs:

- <https://webid-fcm-idp.glitch.me/test/fedcm.json>
- <https://ao-fedcm-idp.glitch.me/test/fedcm.json>
- <https://ao-fedcm-idp-2.glitch.me/test/fedcm.json>

##### Minimal PoC: Use to test positioning issues

1. Navigate to <https://alesandroortiz.com/security/chromium/fedcm-placement.html>
2. Unmaximize winow and move/resize in various ways, such as:
   - Move near the top screen edge
   - Move near the right screen edge
   - With a short window, move near the bottom edge
   - Other placements may also be interesting, so play around

##### Scenario 1: Bubble over another origin (origin confusion by user)

1. Navigate to <https://alesandroortiz.com/security/chromium/fedcm-overlay.html>
2. Click page once.
3. Interact with FedCM bubble to login.

Observed: FedCM bubble is shown over another origin, at a distance from the opening window.

Expected: FedCM bubble is shown within the opening window, or is visually connected to the opening window.

##### Scenario 2: Bubble shown off screen (hidden login)

1. Navigate to <https://alesandroortiz.com/security/chromium/fedcm-offscreen.html>
2. Click page once.
3. When instructed, press tab twice, then press enter. Then wait a few seconds.

Observed: FedCM bubble is shown mostly off screen. User is able to interact with bubble. Attacker is able to obtain login token without user awareness.

Expected: FedCM bubble is shown on screen at all times, similar to permission prompt bubbles. If somehow offscreen, bubble is hidden or made non-interactive.

##### Scenario 3: Bubble obscures sensitive UI

This PoC uses the permission prompt, but other sensitive UIs are also impacted.

1. Navigate to <https://alesandroortiz.com/security/chromium/fedcm-perm-obscured.html>
2. Press and hold any key. Release key when Allow button is show.
3. Press Allow button.

Observed: FedCM bubble is shown above permission prompt, at a distance from the opening window. User can interact with the permission prompt while partially obscured.

Expected: FedCM bubble is shown within the opening window, or is visually connected to the opening window.

#### CREDIT INFORMATION

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [fedcm-placement.html](attachments/fedcm-placement.html) (text/html, 427 B)
- [fedcm-overlay.html](attachments/fedcm-overlay.html) (text/html, 1.3 KB)
- [fedcm-offscreen.html](attachments/fedcm-offscreen.html) (text/html, 1.3 KB)
- [fedcm-perm-obscured.html](attachments/fedcm-perm-obscured.html) (text/html, 2.6 KB)
- [old-chrome.png](attachments/old-chrome.png) (image/png, 266.6 KB)
- [old-chrome-expanded.png](attachments/old-chrome-expanded.png) (image/png, 199.0 KB)
- [fedcm-placement.mp4](attachments/fedcm-placement.mp4) (video/mp4, 26.3 MB)
- [fedcm-placement-google-quora.mp4](attachments/fedcm-placement-google-quora.mp4) (video/mp4, 22.1 MB)
- [fedcm-overlay.mp4](attachments/fedcm-overlay.mp4) (video/mp4, 3.3 MB)
- [fedcm-offscreen.mp4](attachments/fedcm-offscreen.mp4) (video/mp4, 837.6 KB)
- [fedcm-perm-obscured.mp4](attachments/fedcm-perm-obscured.mp4) (video/mp4, 1.4 MB)
- [fedcm-multiple.png](attachments/fedcm-multiple.png) (image/png, 886.3 KB)
- [modal-hanging-outside-webcontents.png](attachments/modal-hanging-outside-webcontents.png) (image/png, 134.7 KB)
- [passkey-modal-hanging-outside-webcontents.png](attachments/passkey-modal-hanging-outside-webcontents.png) (image/png, 100.2 KB)
- [linux-clipping-2.png](attachments/linux-clipping-2.png) (image/png, 187.8 KB)
- [linux-clipping-1.png](attachments/linux-clipping-1.png) (image/png, 207.0 KB)
- [fedcm-offscreen-v2.html](attachments/fedcm-offscreen-v2.html) (text/html, 1.9 KB)
- [fedcm-offscreen-v2.mp4](attachments/fedcm-offscreen-v2.mp4) (video/mp4, 1.7 MB)
- [server-single-account.js](attachments/server-single-account.js) (text/javascript, 2.3 KB)

## Timeline

### al...@alesandroortiz.com (2024-05-01)

FWIW, I discovered this accidentally while visiting Stack Overflow with an unmaximized window near the right edge of my screen, so it's not too difficult for others to discover.

It's also possible to have multiple FedCM bubbles open on different windows (see attached screenshot), so ✨imagine the possibilities✨.

### al...@alesandroortiz.com (2024-05-01)

Issue tracker shows a couple of non-security reports by @chromium.org users describing the same behavior, but don't mention the security impacts:

<https://issues.chromium.org/issues/40261354> (filed March 2023)

<https://issues.chromium.org/issues/40276254> (filed July 2023)

### ch...@chromium.org (2024-05-03)

Thank you for the detailed report!

The POCs aren't *quite* as convincing when I tried on Linux, ChromeOS, and Mac since sometimes the positioning is off, but the idea is definitely there. Thank you for the screencasts as well.

yigu: Could you please take a look?

Setting medium severity on the basis that the positioning may be finicky for an attacker to get right.

### al...@alesandroortiz.com (2024-05-03)

Thanks for triage! I didn't spend too much time on perfecting the positioning, so with some more effort an attacker can make it more convincing across different environments.

### yi...@chromium.org (2024-05-03)

Thank you so much for the detailed report! We'll start to look into these issues. Marking it as P1 as well.

### pe...@google.com (2024-05-04)

Setting milestone because of s0/s1 severity.

### ta...@google.com (2024-05-15)

We have a fix that will land soon for the bubble dialog. The fix is to compute the bubble dialog bounds with respect to the web contents and the bubble dialog will hide itself when it is smaller than the web contents.

Would love to get some opinions on whether this security problem also applies to our modal dialog. Unlike the bubble dialog, the modal dialog can only be opened upon user click. In our current implementation, it is possible for the modal dialog to hang outside of the web contents (see attached screenshot).

### ta...@google.com (2024-05-15)

As far as I can tell, modal dialogs being able to hang outside of the web contents is the default behaviour for modal dialogs (see attached screenshot of passkeys modal dialog).

### al...@alesandroortiz.com (2024-05-15)

Are those screenshots on Mac and (ChromeOS or Linux)? On Windows, modals are always within the browser window.

There are discrepancies in how modals are handled in some platforms. I'll look up some of my prior reports for citations shortly, but that's a somewhat known issue for all modal dialogs more broadly.

### ta...@google.com (2024-05-15)

Ah interesting. modal-hanging-outside-webcontents.png is on ChromeOS and passkey-modal-hanging-outside-webcontents.png is on Mac.

### al...@alesandroortiz.com (2024-05-15)

This is a relevant issue, focused on the Payment Request/Handler dialog: <https://issues.chromium.org/issues/40058363>

This comment from early 2022 indicates the plan was to *not* clip dialogs on Windows to align with Mac and other platforms: <https://issues.chromium.org/issues/40058363#comment42>

Not sure whether that's still the plan now. There's problems both ways, as noted in the discussion there. If clipped, we need to make sure the buttons can't be interacted with (otherwise you run into things like [issue 40067462](https://issues.chromium.org/issues/40067462), [issue 40055478](https://issues.chromium.org/issues/40055478), and many others).

Also see a bunch of related issues in this August 2023 comment: <https://issues.chromium.org/issues/40067462#comment7>

> Otherwise various dialogs/bubbles being clipped by small windows are tracked in many dup'able issues, e.g.:
> 
> - <https://crbug.com/chromium/1283234> (lots of discussion there), <https://crbug.com/chromium/1196750> (cited above), <https://crbug.com/chromium/1368222>, > <https://crbug.com/chromium/1258008>, <https://crbug.com/chromium/1280332>, etc.

### al...@alesandroortiz.com (2024-05-15)

If you want, ask someone from Views team (or the relevant team) about their current plans for this, and other security issues they may be aware of for similarly-sensitive UIs.

In this week's backlog, I have a new security report for the FedCM modal being clipped and still being interactive in small windows on Windows, but that will likely be added to the pile of clipped-dialogs bugs.

I hadn't thought about your perspective of using modals to obscure other UIs, so I will need to experiment with that this week.

### al...@alesandroortiz.com (2024-05-15)

Also interesting: On Linux, bubbles and modals are also clipped but in a slightly different way than Windows.

Seems like this will be fixed soon on Linux per <https://issues.chromium.org/issues/40058249#comment111>

### ap...@google.com (2024-05-15)

Project: chromium/src
Branch: main

commit 359cece04b0da05c40ce5ed9c5333df574069a7d
Author: Zachary Tan <tanzachary@chromium.org>
Date:   Wed May 15 22:12:24 2024

    [FedCM] Fix bubble dialog positioning issues
    
    This patch:
    1. Changes the way we compute the bubble dialog position, such that we
    do not depend on the bubble dialog's height, which has caused drastic
    shifts in the UI positioning in unexpected cases.
    2. Considers the web contents' bounds when showing the bubble dialog.
    If the bubble dialog cannot fit in the web contents, the dialog is
    hidden or remains hidden. When the web contents is later resized to be
    able the fit the bubble dialog, it is then shown.
    
    Bug: 335829872, 335481979, 338233148
    Change-Id: Ia3a828ec41786873ff9c81982b25f88bf5a99fb2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5527555
    Commit-Queue: Zachary Tan <tanzachary@chromium.org>
    Reviewed-by: Yi Gu <yigu@chromium.org>
    Reviewed-by: Nicolás Peña <npm@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1301618}

M       chrome/browser/ui/views/webid/account_selection_bubble_view.cc
M       chrome/browser/ui/views/webid/account_selection_bubble_view.h
M       chrome/browser/ui/views/webid/account_selection_bubble_view_unittest.cc
M       chrome/browser/ui/views/webid/account_selection_modal_view.cc
M       chrome/browser/ui/views/webid/account_selection_modal_view.h
M       chrome/browser/ui/views/webid/account_selection_view_base.cc
M       chrome/browser/ui/views/webid/account_selection_view_base.h
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.h
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop_browsertest.cc
M       chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop_unittest.cc

https://chromium-review.googlesource.com/5527555


### ta...@google.com (2024-05-16)

Thanks for the detailed explanation and all the links Alesandro, these are very helpful. It's likely that your upcoming security report warrants a more generic fix that applies to all BubbleDialogDelegateView modals - looking forward to it so that we can verify whether that is the case. In the meantime, I'll ask around for current plans and will keep you posted. Marking this bug as fixed because we'd like to request a merge.

### al...@alesandroortiz.com (2024-05-16)

Thanks for fix Zachary and team, will verify once it lands on Canary.

re: [#comment16](https://issues.chromium.org/issues/338233148#comment16), SGTM. Feel free to comment their response in the upcoming bug, since it's more relevant there.

### al...@alesandroortiz.com (2024-05-16)

Filed [issue 341095528](https://issues.chromium.org/issues/341095528) for the FedCM modal dialog clipping.

### pe...@google.com (2024-05-17)

Requesting merge to extended stable (M124) because latest trunk commit (1301618) appears to be after extended stable branch point (1274542).
Requesting merge to stable (M125) because latest trunk commit (1301618) appears to be after stable branch point (1287751).
Requesting merge to beta (M126) because latest trunk commit (1301618) appears to be after beta branch point (1300313).
Merge review required: M124 is already shipping to stable.


Merge review required: M125 is already shipping to stable.


Merge approved: your change passed merge requirements and is auto-approved for M126. Please go ahead and merge the CL to branch 6478 (refs/branch-heads/6478) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: harrysouders (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [124, 125, 126].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### al...@alesandroortiz.com (2024-05-17)

Verified as fixed in 127.0.6485.0 Canary on Windows 10 Version 22H2 (Build 19045.4170), using all PoCs from report (and playing around with <https://alesandroortiz.com/security/chromium/fedcm-placement.html> to try to break it).

Also verified this prevents interacting with the bubble dialog when clipped in small windows.

Thanks for fixing!

### am...@chromium.org (2024-05-20)

Upon review, resetting back to medium severity (s1) based on security triage also impacts merge review and approval.
Given that and this is a rather sizable change, declining merge approval for 125 (current Stable channel) and 124 (Extended Stable).
This fix was already approved for 126 merge, so please feel free to merge to branch 6478 at this time.

### ta...@google.com (2024-05-20)

There's a crash report that came in as a result of this change: crbug.com/341240034. I have a fix on the way but it will be a speculative fix - I wasn't able to reproduce the crash reliably since the case where the crash happens should not be able to happen in the first place. Please advise on how I should proceed. Otherwise, I plan on landing the crash fix first then merging both this merge approved patch and the crash fix together.

### am...@chromium.org (2024-05-20)

I would concur with that plan (as long as it's not easier to revert and rework this fix and you are confident in the crash fix), but you'll want to coordinate with a release manager on the crash bug. I can only approve merge from a security standpoint.
Since this merge was auto-approved since it was right after branching it was not reviewed for stability. So if to resolve the crash it would be easier to revert and re-work the fix for this issue, I would suggest that instead. We can't merge the fix if we don't have confidence that the crash will be resolved.

### pe...@google.com (2024-05-21)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### am...@chromium.org (2024-05-22)

Thank you for the report, Alesandro. We had a pretty lengthy discussion about this issue during VRP Panel today and it was decided that this should not be considered a security bug. While you report does a good job of discussing the art of the possible in terms of potential issues to a user, actual harm or potential harm or security consequences to a user were not demonstrated in your report. The malicious origin displays clearly on the prompt and there is no crossing the line of death or obstruction of any important security UI that would result in a convincing spoof demonstrated in through your POC or report.

We did noticed that your [comment #5](https://issues.chromium.org/issues/338233148#comment5) `I didn't spend too much time on perfecting the positioning, so with some more effort an attacker can make it more convincing across different environments.` If you are able demonstrate this issue in more convincing manner that demonstrates the potential user harm you purport here, we would be very happy to reassess for consideration of a potential VRP reward.

### al...@alesandroortiz.com (2024-05-22)

Hi Amy, thanks for the details about the VRP Panel discussion. I understand that Scenarios 1 and 3 might not meet the bar given mitigating factors, but I still think Scenario 2 (`Bubble shown off screen (hidden login)`) does meet the bar for security consequences to a user.

My understanding is that FedCM dialogs are considered sensitive UI and they should be protected like any other sensitive browser UI. If a user accepts a FedCM prompt, the page can obtain sensitive data, such as email, name, photo, and a token. Depending on the IDP, the token may allow an RP to use the IDP's API to obtain even more sensitive info or perform actions on behalf of the user on the IDP's products.

This makes FedCM dialogs similar to autofill or permission prompts, which also provide a page with sensitive info or capabilities. Providing autofill data or granting permissions without user awareness is considered a security issue. This should also apply to FedCM dialogs for the same reasons it applies to those other sensitive UIs.

Much like autofill and permission prompts, the FedCM bubble is already protected against some unintentional interactions, such as clickjacking. Autofill and permission prompts also protect against clickjacking and other forms of unintentional interaction, but the FedCM bubble didn't protect against unintentional interaction via offscreen rendering prior to the patch.

Unintentional interaction via offscreen rendering is demonstrated in `Scenario 2: Bubble shown off screen (hidden login)` (video: `fedcm-offscreen.mp4`).

Other reports of sensitive UI being offscreen and interactive have been considered security reports (e.g. [issue 40058916](https://issues.chromium.org/issues/40058916) which impacted several UIs, including autofill and permission prompts).

---

> there is no crossing the line of death

Technically, Scenario 3 (`Bubble over another origin`) essentially renders anywhere, including above the line of death, but as you mentioned, the origin display mitigates impacts in this scenario.

---

There are greater impacts when chained with [issue 340893685](https://issues.chromium.org/issues/340893685) [1], but these impacts are probably more relevant in that other issue. I did want to mention it here in case it's relevant for this issue's classification and reward discussion.

[1] See <https://issues.chromium.org/issues/340893685#comment2> for chained repro steps

---

Re: [#comment5](https://issues.chromium.org/issues/338233148#comment5), that was in response to the shepherd's report of placement issues on non-Windows OSes (since I developed and tested the PoC on Windows):

> The POCs aren't quite as convincing when I tried on Linux, ChromeOS, and Mac since sometimes the positioning is off, but the idea is definitely there

The videos still show the placements where they would have security impacts, and the PoCs probably repro the same on most Windows devices. I'm not sure if fixing placement on other OSes will help to further demonstrate security impacts, since demonstrating the placement on Windows should be sufficient.

### am...@chromium.org (2024-05-23)

Hi Alesandro, thanks for the response. I didn't have the opportunity to review all of this and respond with the consideration it deserves sooner.

We'll take a second look specifically at scenario 2.
In reviewing your response, I did just reproduce this for myself (which I will admit I didn't attempt to do during panel for all the scenarios) and I can see the possible *potential* for security impact here, but I do want to note that for this scenario to come to fruition, there are a quite a few well-time gestures that must be done here. The click, then tab-tab-enter. When not timed well, this doesn't execute and doesn't result in the login. This is not to nit-pick here at all, but more to have a dialog around the potential for exploitability, which presents as fairly low.

But I do think this particular scenario of the off-window bubble warrants another review, which we'll do next week and get respond accordingly.

### al...@alesandroortiz.com (2024-05-23)

Thanks for the response and taking a second look.

> there are a quite a few well-time gestures that must be done here. The click, then tab-tab-enter. When not timed well, this doesn't execute and doesn't result in the login.

I can improve the PoC to remove these timing issues. The gestures don't need to win a race, but instead wait long enough for the FedCM prompt to render (which isn't a long time). The Glitch-hosted IDPs might be slowing this down significantly, causing the repro to fail if the tab-tab-enter is done too soon (i.e. before the FedCM prompt is displayed).

Will provide an updated PoC by Tuesday so you can have it for the next VRP Panel. I'll use a locally-hosted IDP to remove unrealistically slow IDP response times from the equation (Glitch's response times are often not realistic by any means), and try to identify + remove any other timing issues.

### am...@chromium.org (2024-05-24)

This fix was autoapproved when it was landed; the security impact of this issue does not warrant a backmerge for this fix, so I am removing the auto-approval.

### ta...@google.com (2024-05-24)

deleted

### al...@alesandroortiz.com (2024-05-28)

For VRP Panel: Attached is updated offscreen/hidden login PoC that uses local IDP for improved timing vs. Glitch-hosted IDP, which hopefully solves the reliability problems mentioned in [#comment27](https://issues.chromium.org/issues/338233148#comment27). A proper remotely-hosted IDP should work similarly to the local IDP. (Again, the Glitch-hosted IDP doesn't always have realistic response times.)

The v2 PoC also uses a keypress for initial input, to avoid user having to switch between input devices. It also adds a debug mode to see the timing of the FedCM prompt more clearly on your device (in case it's still taking longer than expected).

As mentioned in [#comment28](https://issues.chromium.org/issues/338233148#comment28), timing is only important between the first keypress and the first tab, and it's a minimum time threshold, not a maximum time threshold. This is because the FedCM prompt needs a few hundred milliseconds to fetch data from the IDP and then render the prompt. After the FedCM prompt renders, the remaining gestures can be made at any time with any amount of time between the gestures.

IMO, most users will be able to wait until the FedCM prompt renders, either because the website asks them to wait, or because they type at a slower speed than us (who are likely fast typers).

I verified this PoC on Windows 10 using snapshot build 1301615 [1] which is the closest build before patch [2].

#### REPRODUCTION CASE

(Almost identical to Scenario 2 from original report)

Setup:

1. Run a simulated IDP server: `node server-single-account.js` (attached in [#comment32](https://issues.chromium.org/issues/338233148#comment32))

In real scenarios, an attacker would use a legit IDP since they would want real credentials.

Repro steps:

1. Navigate to <https://alesandroortiz.com/security/chromium/fedcm-offscreen-v2.html>
2. Press any key once.
3. When instructed, press tab twice, then press enter. Then wait a few seconds.

Observed: FedCM bubble is shown mostly off screen. User is able to interact with bubble. Attacker is able to obtain login token without user awareness.

Expected: FedCM bubble is shown on screen at all times, similar to permission prompt bubbles. If somehow offscreen, bubble is hidden or made non-interactive.

[1] <https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/1301615/>

[2] <https://chromium.googlesource.com/chromium/src/+/359cece04b0da05c40ce5ed9c5333df574069a7d>

### al...@alesandroortiz.com (2024-05-28)

Attached `server-single-account.js`

### sp...@google.com (2024-05-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Based the low severity and impact of this scenario with the preconditions of multiple user gestures required. 

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are not already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### am...@chromium.org (2024-05-30)

Thank you for the new POC and additional information, Alesandro. Since the origin information was not made readily available to the user with the prompt off-window, we do agree there are security implications from this scenario. Due to the high gesture preconditions and low impact of this issue individually, we have instated this as a security bug, but a low severity one.
Thanks again for taking the time to discover and report this and the other FedCM bugs you reported to us -- nice work!

### al...@alesandroortiz.com (2024-05-30)

Thanks for the reconsideration and reward!

To clarify, is the reward $1k for report + $1k bisect bonus, or was there no bisect bonus?

### am...@chromium.org (2024-06-27)

Hi Alesandro -- apologies for the delay in responding here. In terms of reward amount breakdown, this was a $1,000 for the report and $1,000 bisect bonus. 

### al...@alesandroortiz.com (2024-06-27)

No worries, thanks for clarification!

### pe...@google.com (2024-08-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/338233148)*

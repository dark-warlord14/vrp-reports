# Security: Extension can obscure active window with an unfocused window, allows interaction with permission API prompt dialog without awareness

| Field | Value |
|-------|-------|
| **Issue ID** | [40061026](https://issues.chromium.org/issues/40061026) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2022-2616 |
| **Reporter** | vi...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2022-09-18 |
| **Bounty** | $2,000.00 |

## Description

**VERSION**

Chrome Version: 105.0.5195.127 (Official Build) (64-bit)  

Operating System: Windows 10 Pro Version 21H1 (Build 19043.2006)

**VULNERABILITY DETAILS**

This report covers some behavior previously reported in 1302159 (CVE-2022-2616), 1290213, and 1301203; expanding the impacts not included in the final CVE fix

It's the same history: An extension can create an inactive window (chrome.windows.create with focused: false) over an active window, which obscures the active window. The active window still can receive keyboard inputs and this can hide user keyboard interaction inputs with sensitive browser UI and web pages, for example, permissions request from the site.

Impact: Granting permission API requests without the user awareness and the extension does not require any permission.

Here in this report, I'm covering the usage of the Permissions API as an example but it could leave a door open for many more cases.

\* Permission API requests: Accepting permission requests with 3 user key presses;

The extension can inject javascript code into the page DOM, so we could use the extension to monitor the PermissionStatus.state or place observers on methods like a navigator.geolocation.getCurrentPosition (and tons of others that uses the permission API) by hooking it / overwriting or such on this function to as soon as any permission prompt gets called, the extension knows the timing when to create a new unfocused window over the permissions API prompt from the browser, at this moment the main window still can receive keyboard inputs, being able to grant permissions without the awareness.

**REPRODUCTION CASE**

1. Install the attached extension, the extension does not require any permission, not even externally\_connectable;
2. Visit <https://chrome-permissions.vercel.app/> ( could be any site that prompts the permission API request to the user, but for this example, I'm using this link using only the navigator. geolocation case );
3. Once the extension reveals the active window, observe the interaction (TAB TAB ENTER);
4. The user granted permission without the awareness

**CREDIT INFORMATION**

Reporter credit: Vitor Torres <https://github.com/vtorres/>

## Attachments

- [defaultBehavior.mp4](attachments/defaultBehavior.mp4) (video/mp4, 1.0 MB)
- [unexpectedBehaviorWhenPromptedPermissions.mp4](attachments/unexpectedBehaviorWhenPromptedPermissions.mp4) (video/mp4, 1.4 MB)
- [extension.rar](attachments/extension.rar) (application/octet-stream, 3.1 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 832 B)
- [bg.js](attachments/bg.js) (text/plain, 1.7 KB)
- [crbug-1365104.html](attachments/crbug-1365104.html) (text/plain, 1.2 KB)
- [crbug-1365104-instructions.html](attachments/crbug-1365104-instructions.html) (text/plain, 349 B)
- [crbug-1365104-stable.mp4](attachments/crbug-1365104-stable.mp4) (video/mp4, 791.0 KB)
- [crbug-1365104-canary.mp4](attachments/crbug-1365104-canary.mp4) (video/mp4, 860.3 KB)
- [background.js](attachments/background.js) (text/javascript, 689 B)
- [content.js](attachments/content.js) (text/javascript, 1.5 KB)
- [manifest.json](attachments/manifest.json) (application/json, 720 B)
- [popup.html](attachments/popup.html) (text/html, 219 B)
- [README.md](attachments/README.md) (text/markdown, 2.1 KB)
- [extension.zip](attachments/extension.zip) (application/zip, 3.5 KB)

## Timeline

### [Deleted User] (2022-09-18)

[Empty comment from Monorail migration]

### vi...@gmail.com (2022-09-19)

Observed: Active window is below the inactive window and not visible to the user. Obscured active window accepts keyboard input in sensitive browser UI and web pages.

Expected: Sensitive browser UI is always visible to the user, or the active window does not accept keyboard input when not properly visible to the user.

Ps.: On the previously provided extension, we could update the manifest.json and change the content_scripts configuration from "https://chrome-permissions.vercel.app/*" to "<all_urls>" to test it any site - in the provided example we are only covering the geolocation API (which requires permission API dialog prompt to ask the user) so the site would be using: navigator.geolocation.getCurrentPosition((position) => { // logic }, () => {}), but the same logic could be applied to all permission API request box if the inactive window is created right after it prompts the permission dialog to the user, it keeps over, obscuring the main window when it should not.

### ts...@chromium.org (2022-09-19)

Assigning/labeling per 1302159.

[Monorail components: Platform>Extensions>API]

### vi...@gmail.com (2022-09-19)

[Comment Deleted]

### [Deleted User] (2022-09-19)

[Empty comment from Monorail migration]

### vi...@gmail.com (2022-09-20)

Looks like a CVE-2022-2616 bypass. https://bugs.chromium.org/p/chromium/issues/detail?id=1302159

### [Deleted User] (2022-09-20)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-20)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-02)

kerenzhu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vi...@gmail.com (2022-10-06)

More info:

Seems like windows.getLastFocused() returns the newly created window when a bubble-type UI is shown, so I'm guessing IsActive() is returning false returns false when a bubble-type UI is open in a browser window

So my PoC would work in any bubble-type UI while demonstrated with the permissions API dialog but
it would work with the chrome.action.openPopup(), with device chooser dialogs (e.g. navigator.USB, .hid, .serial APIs), and also works with the tab search menu at the top (ctrl+shift+a), not useful for attacker like the permissions API dialog, but good to know

----

Therefore the patch for crbug 1302159 doesn't work, since reset_active is never set to true, so the Activate() call to re-activate the correct window is never made: 

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/tabs/tabs_api.cc;l=813;drc=f0298416263b1f0c4fedc3e342c5ea2ac7f7e43d

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/permissions/chooser_bubble_ui.cc;l=224;drc=8d399817282e3c12ed54eb23ec42a5e418298ec6

### ke...@chromium.org (2022-10-06)

Thank you for you report.

I am not able to reproduce with Chrome 108.0.5341.0 on Windows 10.0.19042 Build 19042. In my reproduce attempts, the newly open window will always be opened behind the old window. 

vitortorresvt@, your screencast seems to be captured in Chrome's tablet mode (Chrome is using the tablet mode UI). Was this intentional? Are you able to reproduce it in the normal mode? 

### vi...@gmail.com (2022-10-06)

It's reproducible on 108.0.5341.0 too and all versions that I tried, but NOT on canary because for some reason Canary tries to show the permission prompt twice or there's some other UI jank that breaks the Poc

Could you cc alesandro@alesandroortiz.com on this report for visibility and comment? 

His latest reports have much in common and could be a great cc to help 


### vi...@gmail.com (2022-10-06)

He will provide a better PoC in response of https://crbug.com/chromium/1365104#c11

### [Deleted User] (2022-10-20)

kerenzhu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2022-10-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-20)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-10-21)

Attached repro that works on Stable + Canary. In bg.js, set isCanary boolean based on which channel you're using, since Canary requires a delay due to a possible UI bug. Delay can be minimal in 106 Stable. I'm using 700ms in Canary, but even then it fails sometimes. In Stable it's 100% reliable with no delay, and in Canary it's 100% reliable with a larger delay.

In terms of impacts, it's essentially the same impacts as the other bugs I reported, although I would need to re-verify later if any of the impacts are different. Impacts should not limited to permission prompts.

Tested on 108.0.5344.0 + 109.0.5371.0 Canary.
Tested on 106.0.5249.91 + 106.0.5249.103 + 106.0.5249.119 Stable.
OS: Windows 10 Version 21H2 (Build 19044.2006)

Repro steps:
1. Download extension (manifest.json + bg.js)
2. Edit bg.js to set isCanary boolean depending on whether you're using Canary or Stable.
3. Install extension (or reload if already installed)
4. Follow instructions on first page (click page) to open inactive window over active window
5. Follow instructions on second page (press indicated keys) to accept camera permission in inactive window

Observed: Inactive window renders over active window. Inactive window keeps focus and receives keyboard input.
Expected: Inactive window renders below active window. Active window keeps focus and receives keyboard input.

### al...@alesandroortiz.com (2022-10-21)

Attachments went poof on upload, retrying.

### al...@alesandroortiz.com (2022-10-21)

Re: https://crbug.com/chromium/1365104#c11 tablet mode, my repro in https://crbug.com/chromium/1365104#c17/#c18 is using the normal UI I get on my machine (I didn't even realize there was a tablet mode that Vitor used).

### al...@alesandroortiz.com (2022-11-01)

Have a CL up at https://chromium-review.googlesource.com/c/chromium/src/+/3996184 but haven't tested it, so not assigning for review just yet. Should be able to test it either Tuesday or Wednesday.

### al...@alesandroortiz.com (2022-11-02)

Tested my patch on local build (checkout of commit 59b631329c10c3b1f365b78a01d3e81780cec48a from 1.5 days ago) on Windows 10 Version 21H2 (Build 19044.2006).

Issue is mitigated due to new window getting activation, therefore the new window receives keyboard interactions. Will add reviewers to CL after submitting this comment.

### al...@alesandroortiz.com (2022-11-29)

kerenzhu@: Left comment in CL to check in on your investigation into other potential approaches to resolve issue. We can also move discussion here; either way, let me know if you have an update.

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-12-13)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-12-14)

I am working a fix (https://crrev.com/c/4075475) that should maintain the extension API semantic (as opposed to https://crrev.com/c/3996184)
There is a separate issue crbug.com/1401116 that is blocking https://crrev.com/c/4075475. Will work on resolving that first. 

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-04-22)

kerenzhu@: I see https://crbug.com/chromium/1401116 and associated CLs are still open. Are there plans to work on the issue(s) blocking this issue?

### ke...@chromium.org (2023-04-24)

I don't have time to investigate https://crbug.com/chromium/1401116 at least for the next two weeks, but I will give it another shot after that. It is a more fundamental issue in that solving it requires changing the window activation semantic and I fear it might cause regression. 


### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-10-08)

Following up to see if there has been any progress on this and the associated bugs.

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1365104?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1401116]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-10-26)

kerenzhu: Uh oh! This issue still open and hasn't been updated in the last 550 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-10)

kerenzhu: Uh oh! This issue still open and hasn't been updated in the last 565 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ar...@chromium.org (2024-12-13)

**secondary security shepherd**

[kerenzhu@chromium.org](mailto:kerenzhu@chromium.org): Could you please provide an update?

I observe the focus is moved away from the document to the chrome UI. This result in "TAB ENTER ENTER" to click on some buttons of the omnibox. Locally this wasn't clicking on accepting the localisation button. It might have changed. Still, we probably don't want document to force focus to be moved away.

### ke...@chromium.org (2024-12-13)

> Still, we probably don't want document to force focus to be moved away.

Preventing focus changes initiated by the document could regress the user experience. A common case is when the location permission prompt intentionally takes focus to enable immediate keyboard interaction (e.g., dismissing the prompt with the Esc key). If we were to force the prompt to appear without focus, the user would need an extra step (clicking the prompt) to interact with it, which feels less intuitive.

The current [implementation](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/tabs/tabs_api.cc;l=883-902;drc=323cf9806c735d83c0820980dcfc0e2977cf2e84) in `extensions::WindowsCreateFunction::Run()` already attempts to prevent the newly created unfocused window from occluding the existing one. It does so by reactivating the previously active browser window if it was active:

```
  if (focused) {
    new_window->window()->Show();
  } else {
    // The new window isn't supposed to be focused. Here, instead of showing an
    // unfocused window on top (possible on some operating systems), we show
    // the window and then bring the old focused window back on top.
    // We still use ShowInactive() (instead of doing a Show() followed
    // immediately by Deactivate()) because the process of showing the window is
    // somewhat asynchronous. This causes the immediate Deactivate() call to not
    // work.
    BrowserList* const browser_list = BrowserList::GetInstance();
    Browser* active_browser = browser_list->GetLastActive();
    bool reset_active = false;
    // Check if there's a currently-active window that should re-take focus.
    // NOTE: This browser *may* be from another profile. We don't access any
    // data from it.
    if (active_browser && active_browser->window()->IsActive())
      reset_active = true;
    new_window->window()->ShowInactive();
    // NOTE: It's possible that showing the new browser synchronously caused
    // the old one to close. Ensure it's still valid before activating it.
    if (reset_active && base::Contains(*browser_list, active_browser))
      active_browser->window()->Activate();
  }

```

The issue is that the activation test is unreliable. Specifically, `active_browser->window()->IsActive()` may return false when the permission prompt is open, because technically the activation is on the prompt window, not on the browser window.

The [solution](https://crrev.com/c/4075475) I proposed in 2022 was to add a `IsTreeActive()` to BaseWindow. This functions returns true if a window or any of its descendants is active. The idea is to re-activate the old browser window if the **window tree** was active. Then I encountered difficulty in writing tests due to [issue 40062245](https://issues.chromium.org/issues/40062245), that there can be multiple active widgets at the same time. Technically this does not break the fix, but we wanted good coverage of framework-level API like `IsTreeActive()`, so this became a blocker.

alesandro@ suggested in code review that we may simply remove the `active_browser->window()->IsActive()` test. Back then, I was opposed to this idea because I think it may break user's input flow. For example, if a user is typing in another application (non-chrome), unconditionally activating the browser window would steal focus.

Nevertheless, I am going to give Alesandro's proposal a try. While it does make the window creation process slightly more intrusive, extensions already disrupt the user experience to some degree when creating new windows. We should perhaps hold the extensions responsible for choosing appropriate timings for window creation.

### al...@alesandroortiz.com (2024-12-13)

Shepherd and kerenzhu@: Thanks for taking a look again.

For future reference, the CL comment referenced in [#comment54](https://issues.chromium.org/issues/40061026#comment54) is <https://chromium-review.googlesource.com/c/chromium/src/+/3996184/comment/0f8664a9_0bb5d552/> (line 819 comment thread)

### ap...@google.com (2024-12-16)

Project: chromium/src  

Branch: main  

Author: Keren Zhu <[kerenzhu@chromium.org](mailto:kerenzhu@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6087847>

extensions: fix an unfocused new window obscuring the old window

---


Expand for full commit details
```
extensions: fix an unfocused new window obscuring the old window 
 
This CL unconditionally re-activate the last active browser window when 
opening a new unfocused browser window using chrome.windows.create with 
focused: false. 
 
Previously the code re-activates the old window only if the old window 
is active. This is unreliable because the old window could be inactive 
while one of its child window (e.g. permission bubble) is active. We want the old window to be at the front for this case. Otherwise, the new 
unfocused window will obscure the old window which still has the input 
focus. The malicious content in the new window can then misleads the 
user into interacting with the old window without their awareness. 
 
Bug: 40061026 
Change-Id: I29468b9429009bcbb07072b1b1c5ef4ec0953f46 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6087847 
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com> 
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
Commit-Queue: Keren Zhu <kerenzhu@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1397024}

```

---

Files:

- M `chrome/browser/extensions/api/tabs/tabs_api.cc`

---

Hash: 286e17e176c1e6938b7e1d4e42313c14db0aa8e5  

Date:  Mon Dec 16 14:54:45 2024


---

### al...@alesandroortiz.com (2024-12-17)

Thanks for landing patch kerenzhu@, I'll verify once there's a snapshot build with patch available. (I checked with original reporter Vitor, but he's busy this week.)

### ke...@chromium.org (2024-12-17)

Thank you alesandro@. I look forward to your verification.

### al...@alesandroortiz.com (2024-12-19)

Verified as fixed on 133.0.6905.0 Canary using PoC from [#comment18](https://issues.chromium.org/issues/40061026#comment18) and 19.

Also checked that this still reproduces on 131.0.6778.205 Stable, to rule out that any other changes would have otherwise broken repro.

Thanks again for fixing!

For reporter credit of this bug, please use: Vitor Torres and Alesandro Ortiz

### sp...@google.com (2025-01-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
$2,000 for report of lower impact web platform privilege escalation 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-09)

Congratulations Vitor and Alesandro! Thank you for your efforts and reporting this issue to us.

### al...@alesandroortiz.com (2025-01-14)

Thanks for the reward!

(For my future reference and public record, we split the reward 70/30, with most going to Vitor; p2p-vrp@ already processed the split request)

### ch...@google.com (2025-03-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $2,000 for report of lower impact web platform privilege escalation

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061026)*

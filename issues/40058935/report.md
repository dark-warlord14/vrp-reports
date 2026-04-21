# Security: Extension can obscure active window with an inactive window, user can interact with sensitive UI using keyboard without being aware

| Field | Value |
|-------|-------|
| **Issue ID** | [40058935](https://issues.chromium.org/issues/40058935) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Fuchsia, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2022-03-02 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

This report covers some behavior previously reported in <https://crbug.com/chromium/1290213> ("Autofill prompt can be obscured by inactive extension-created popup, allows stealthy autofill data theft"). While researching <https://crbug.com/chromium/1301203>. I realized most of the impacts of that issue also apply to <https://crbug.com/chromium/1290213>. This report covers the expanded impacts not included in the initial report. Feel free to mark this issue as duplicate of <https://crbug.com/chromium/1290213> or vice versa if the fixes are the same for both.

An extension can create an inactive window over an active window, which obscures the active window. The active window can still receive keyboard input. This can hide user interactions using keyboard input with sensitive browser UI and web pages. I've identified a myriad of affected areas, and there are potentially other areas which may have similar or greater severity impacts. The extension does not require any permissions (except for the "bookmarkxss" scenario).

For some scenarios, the active window must be slightly visible. This is not an issue for the attack, but something to be aware of if testing the PoC or developing new scenarios.

Verified impacts ("without user awareness" implied unless otherwise specified):

\* Autofill: (Previously reported in <https://crbug.com/chromium/1290213>, not included in this report's PoC.) Open autofill prompt, select item, and fill autofill entry into page with 2 keypresses. The browser fills in multiple fields at once with this interaction. Can obtain name, address, and credit card info.

\* Screen share dialog: Share screen with 3 keypresses. Only mitigation is the small widget/notification after sharing that says "example.com is sharing your screen".

\* Payment request: Complete payment request with a few keypresses (as few as 2 keypresses; depends on payment flow).

\* Web pages: Interact with any page. Can perform sensitive actions on logged-in or intranet pages.

\* chrome:// pages: Interact with any chrome:// page.  

\* chrome://settings/security contains settings related to Safe Browsing, and other chrome://settings page may have sensitive settings.  

\* chrome://flags/ can toggle features which may affect security with 3 keypresses.

\* External protocols: Allow website to open app with 2 keypresses. Also can enable "always allow {origin} to open links of this type..." to allow multi-step or future drive-by external protocol launches.

\* Downloads: Open downloads in download bar with 2 keypresses, or in chrome://downloads with a few keypresses (does not bypass any OS-level protection)

\* Pointer lock: Obtain pointer lock without notification. Might be useful when combined with other bugs.

\* Copy/paste: Can obtain page content with Ctrl+A, Ctrl+C, Ctrl+V from most web pages or chrome:// pages. This is an issue if the page has sensitive content.  

\* chrome://predictors/  

\* chrome://local-state/ (os\_crypt.encrypted\_key?)  

\* chrome://prefs-internals/ (gaia, sync entries?)  

\* And others which provide potentially sensitive info such as frequent sites, recent sites/URLs, installed extensions, etc.

\* XSS via bookmark + address bar: Run attacker-provided JavaScript on any web page with 4 or 6 keypresses. Requires "bookmarks" permission. See <https://crbug.com/chromium/1301874> for more details on this attack.

Mitigated impact:

\* Permssion prompts: Browser moves active window to front when it shows permission prompt.

\* Installing extension from Chrome Web Store requires a lot of keypresses (at least 7), and the confirmation dialog always appears on screen even if window is off screen.

(Note to self: Avoid disclosing this crbug before <https://crbug.com/chromium/1301874> since this report + PoCs include details of the other crbug.)

**VERSION**  

Chrome Version: 98.0.4758.102 (Official Build) (64-bit) (cohort: Stable), 101.0.4918.0 Canary  

Operating System: Windows 10 Version 20H2 (Build 19042.1526)

**REPRODUCTION CASE**  

Initial setup:

1. Install attached extension: manifest.json + bg.js  
   
   Note that the "bookmarks" permission is only required for the "bookmarkxss" scenario. You can remove the permission in the manifest to verify all other scenarios work without any particular permissions.

All PoC scenarios:

1. Set the scenario variable in bg.js.  
   
   Available scenarios: screenshare, download, payment, externalprotocol, flags, bookmarkxss  
   
   Available but will not work: permission, extension
2. Reload the extension.
3. Follow instructions shown in the extension-created inactive window.
4. Once the extension reveals the active window, observe the interaction results.

Observed: Active window is below inactive window and not visible to user. Obscured active window accepts keyboard input in sensitive browser UI and web pages.  

Expected: Sensitive browser UI is always visible to user, or active window does not accept keyboard input when not properly visible to user.

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 342 B)
- [bg.js](attachments/bg.js) (text/plain, 3.9 KB)
- [inactive-target.html](attachments/inactive-target.html) (text/plain, 2.3 KB)
- [inactive-instructions.html](attachments/inactive-instructions.html) (text/plain, 1.7 KB)
- [inactive-window.mp4](attachments/inactive-window.mp4) (video/mp4, 5.7 MB)

## Timeline

### [Deleted User] (2022-03-02)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-03-02)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-03-02)

Leaving this one as separate from https://crbug.com/chromium/1301203: IIRC, window.open() doesn't allow creation of an unfocused window, and wouldn't allow things to be occluded in a similar way probably.

Though... a page could probably use window.moveTo() to creatively obscure windows and maybe then we'd have the same problem?

[Monorail components: Platform>Extensions>API]

### [Deleted User] (2022-03-02)

[Empty comment from Monorail migration]

### ms...@chromium.org (2022-03-03)

RE: #3
> window.open() doesn't allow creation of an unfocused window, and wouldn't allow things to be occluded in a similar way probably.
We might begin allowing window.open() to create and show windows without activating them in a very specific scenario.
Even then, it still shouldn't be possible to produce this behavior (showing an inactive window over an active one).
I'm happy to discuss this in another venue soon.

> a page could probably use window.moveTo() to creatively obscure windows and maybe then we'd have the same problem?
I've explored this in a limited fashion, and haven't found an obvious way to obscure an active window with an inactive one using web platform APIs.
Generally, activation raises the z-order of the window over inactive windows; it's definitely a bit odd that extension apis allow arbitrary unfocused window creation.

### al...@alesandroortiz.com (2022-03-03)

Re: https://crbug.com/chromium/1302159#c5, I recently audited Chromium to find other areas that might create inactive windows. The only interesting areas I was able to identify were detailed in https://crbug.com/chromium/1290098's "OTHER AREAS OF INTEREST" section + https://crbug.com/chromium/1290664's report. Most of the discussion around fixing inactive windows has occurred in the comments of https://crbug.com/chromium/1290213.

Quoting from https://crbug.com/chromium/1290098:
"OTHER AREAS OF INTEREST
I audited other ShowInactive() call sites and indirect uses (such as setting NavigateParams::SHOW_WINDOW_INACTIVE) and identified several areas of interest which in theory result in the same behavior as chrome.windows.create({focused: false}). However, these areas either aren't useful to attackers or I was unable to repro. Other than these areas, I was unable to identify other useful ways for web pages or extensions to open an inactive window via window->ShowInactive().

1. https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_navigator.cc;l=635;drc=cc56431a98152461ad58cf220ea03f4098f7008c
// If we create a popup window from a non user-gesture, don't activate it.
if (params->window_action == NavigateParams::SHOW_WINDOW &&
    params->disposition == WindowOpenDisposition::NEW_POPUP &&
    params->user_gesture == false) {
  params->window_action = NavigateParams::SHOW_WINDOW_INACTIVE;
}
In theory if a popup is opened without user gesture, we reach this block. However, I tried opening a popup without user gesture (by allowing popups for the origin) and it still activates the popup. Not sure if this code block is unreachable or if something else is activating the window later regardless of the window_action value here.

2. https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/app_window/app_window.cc;l=704;drc=cc56431a98152461ad58cf220ea03f4098f7008c
chrome.app.window.create() also calls ShowInactive() so in theory it also would result in same behavior. However, CWS has not accepted new apps since March 2020 and will only accept updates to existing apps through June 2022. It seems that public apps also cannot run after June 2021 without enterprise policy on non-Chrome OS devices (uncertain about this).
https://developer.chrome.com/docs/extensions/reference/app_window/
https://blog.chromium.org/2020/08/changes-to-chrome-app-support-timeline.html

3. https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/devtools/protocol/target_handler.cc;l=28;drc=372e9f2142da5ca6febcff2a7084d75602c435f0
DevTools protocol uses NavigateParams::WindowAction::SHOW_WINDOW_INACTIVE, but this is not useful for an attacker because having DevTools protocol access allows for more interesting attacks."

In addition to the three areas above, also see https://crbug.com/chromium/1290664 which details another area of interest.

### al...@alesandroortiz.com (2022-03-03)

FWIW, I realize a lot of my recent crbugs are closely related and most of the inactive window reports might even have the same fix depending on the approach, so it's okay if they're marked as duplicates of each other.

### ms...@chromium.org (2022-03-03)

FWIW, I don't have access to https://crbug.com/chromium/1290098 nor https://crbug.com/chromium/1290213; maybe someone can CC me there.

1) Indeed, it's not entirely straightforward to trace under what conditions that might trigger (very few places set/plumb user_gesture to false)

2) Yeah, Chrome App deprecation might make that approach a little less readily accessible, but the corresponding chrome.windows.create extension API is still applicable, as you've shown.

3) Indeed, devtools protocol usage isn't likely a strong security consideration here.

### [Deleted User] (2022-03-03)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### en...@chromium.org (2022-03-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-16)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-30)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2022-03-31)

Sorry, this one slipped under my radar.

The simplest solution here would be to just deprecate `focused` in windows.create().  I wonder if there's an alternative - it looks like windows.update() also takes a `focused` parameter, but the docs for that one say it brings the next window in the z-order to the front.  The code for that uses a window Deactivate() call, rather than ShowInactive().  I wonder if we could do something in windows.create() like 1) call Show() (window active) and then 2) call Deactivate() (window inactive, next window in z-order brought forward).  Perhaps that would be a reasonable middle ground, rather than getting rid of focused entirely?

alesandro@, have you been able to repro any of this behavior using chrome.windows.update()?  Or does the implementation of that function seem safe?

[1] https://developer.chrome.com/docs/extensions/reference/windows/#method-update

### al...@alesandroortiz.com (2022-03-31)

When I last tried a month or two ago, wasn't able to repro with chrome.windows.update() because of the Deactivate() behavior you described. It brings another window to the front, so there's no way to obscure a window in a manner that benefits an attacker.

See https://crbug.com/chromium/1302159#c6 + https://crbug.com/chromium/1290664 for my audit results on other ways to obscure sensitive UI with an active window with similar impacts. I'll let the Chromium team decide, but this crbug can be focused on chrome.windows.create() and the other crbugs can focus on the other inactive window instances. Not sure if a single fix would work since there might be legitimate use cases for inactive windows that can't be misused by attackers.

### rd...@chromium.org (2022-04-01)

@msw, do you know of any legit cases for ShowInactive()?  Would it make sense to change the behavior of it across the board to opening a window in the background, rather than the foreground?

I'm hesitant to get rid of `focused` entirely in extensions, since I imagine there might be some cases where an extension wants to open something without "interrupting" a user.  But, we obviously need to change the behavior of an inactive window rendering in front of the active window.  If we can do that by changing ShowInactive(), that'd be best (and address any other cases of ShowInactive()), but we could also do an extensions-specific fix like Show() -> Deactivate().

### rd...@chromium.org (2022-04-15)

Following up here, I'm hoping to get a patch for this soon.  A few notes:
- The Show() -> Deactivate() technique doesn't work for... reasons.  (The window doesn't properly deactivate, and I assume this is because some of the Show() mechanism is asynchronous and not playing nicely.)
- New tentative plan: in the case of focus: false, we can re-activate() the previously-active window.  This would essentially display the new window under the active window.  Testing this out, there is a slight UI flash (because the new window very briefly renders on top, then goes behind), but I think this is acceptable.
- I'm unable to reproduce this bug on Chrome Dev on Linux - the inactive window is opened under the active window (as we'd like).  I'm tentatively removing Linux.  I was able to repro on Win + CrOS; haven't tested Mac yet.

### rd...@chromium.org (2022-04-15)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-04-19)

re c#15, ShowInactive() is useful for showing bubbles without interrupting user's keyboard focus, for example, on IPH bubble. For those most of its use case we need the widget to be display on the foreground. Changing that behavior is not feasible.

fwiw, FF does not support chrome.windows.create({focused: false}). https://bugzilla.mozilla.org/show_bug.cgi?id=1253129

### ms...@chromium.org (2022-04-19)

Sorry for the delayed reply; #18 is a good point; I bet the status bubble uses ShowInactive. They probably shouldn't be in the background. A new prototype also uses NavigateParams::SHOW_WINDOW_INACTIVE when fullscreen windows open cross-screen popups, and they should be foreground (see https://crbug.com/chromium/1315749):
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser.cc;drc=83833ba1837c237f48dc481089568b1fa05a80fa;l=1647

### rd...@chromium.org (2022-04-20)

WIP CL is here: https://chromium-review.googlesource.com/c/chromium/src/+/3565494

Unfortunately, it looks like we don't have a good way to test this yet - views::test::WidgetTest::IsWindowStackedAbove() doesn't work well with comparing different BrowserViews, so the test fails (but I *think* the fix is good - it appears to be on Windows).

kerenzhu@ offered to take this to investigate a good way to compare BrowserView z-orders; passing to them.  Keren, feel free to pass back to me if there's something in place.

If it looks like a solution here would take a lot more investigation, we could also optionally land the CL as-is (and just leave out the assertion) so that the fix in place, even though the test isn't yet (but that should ideally be a fallback).

### ke...@chromium.org (2022-04-20)

I lean towards landing your CL as-is since this is a P1 and there's currently no test support for comparing BrowserView z-orders. This test support will take time to implement since they are platform-specific. I will work on it in follow-ups. 

### gi...@appspot.gserviceaccount.com (2022-05-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dec7efecd33af8c058671bb89a980c5e47345a57

commit dec7efecd33af8c058671bb89a980c5e47345a57
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Fri May 13 21:47:23 2022

[Extensions] Ensure windows created with `focused: false` aren't on top

Ensure that windows created using the `chrome.windows.create` API with
`focused: false` specified don't overlap another, active window.

Bug: 1302159
Change-Id: Ibf140576f68f9cdf482c814ca1dbbf8f66310033
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3565494
Commit-Queue: Devlin Cronin <rdevlin.cronin@chromium.org>
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1003336}

[modify] https://crrev.com/dec7efecd33af8c058671bb89a980c5e47345a57/chrome/browser/extensions/api/tabs/tabs_interactive_test.cc
[modify] https://crrev.com/dec7efecd33af8c058671bb89a980c5e47345a57/chrome/browser/extensions/api/tabs/tabs_api.cc


### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-06-03)

Verified as fixed in 104.0.5101.0 Canary on Windows 10 Version 21H2 (Build 19044.1706).

Should this be merged to Stable and other branches?

### al...@alesandroortiz.com (2022-06-03)

The fix in https://crbug.com/chromium/1302159#c22 also fixed https://crbug.com/chromium/1290213 (which was same behavior but only described autofill impacts), so feel free to mark the other issue as duplicate of this issue.

### al...@alesandroortiz.com (2022-06-03)

The fix in https://crbug.com/chromium/1302159#c22 also fixed https://crbug.com/chromium/1290098, which is a different type of attack that was possible due to inactive windows being shown above active windows.

### rd...@chromium.org (2022-06-05)

Thanks, alesandro@!

Re merging: I don't have a strong opinion.  Given the barrier to entry here (installing a malicious extension that leverages this), I don't think it's critical that we merge, and I think there's a small-but-present chance that this may break extension behavior, and rolling out through the normal release process may alert us to any issues before it reaches stable.  That said, I think the risk is small enough that I wouldn't oppose a merge.  I defer here to +adetaylor or his delegate of choice. : )

Re duplicates: While this fixed the particular attack vector used in those bugs, I think there's an argument made for keeping those bugs open as, ideally, I don't think autofill should be able to render in any occluded window.  Even though this was the easiest technique, I don't think it's the *only* technique (though others may require more user interaction).  Strawman: Perhaps we should generalize one of those issues into a more holistic fix and lower the security severity since there isn't an active exploit?  Here, too, happy to defer to adetaylor@.

Finally, kerenzhu@, given the reason this bug is still open is the test (rather than the fix), I'd say you can feel free to close this bug out and file a separate issue for that (so that we don't have an open security bug for an issue that is effectively fixed - though ensuring we have a regression test would certainly be valuable!).

### ke...@chromium.org (2022-06-06)

Closing given that this bug is effectively fixed per https://crbug.com/chromium/1302159#c27. Tracking the task to add regression test at crbug.com/1333445.

### ke...@chromium.org (2022-06-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-06)

[Empty comment from Monorail migration]

### sc...@google.com (2022-06-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-13)

Congratulations, Alesandro! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and great work! 

### al...@alesandroortiz.com (2022-06-13)

Thanks for the reward!

### am...@google.com (2022-06-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-14)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1302159?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1290098, crbug.com/chromium/1290213]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058935)*

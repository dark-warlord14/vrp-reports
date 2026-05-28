# Improper restriction in password saving form, while navigation from one site to another site

| Field | Value |
|-------|-------|
| **Issue ID** | [399131922](https://issues.chromium.org/issues/399131922) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Privacy, UI>Browser>Passwords |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | va...@chromium.org |
| **Created** | 2025-02-26 |
| **Bounty** | $500.00 |

## Description

## SUMMARY

The Save Password bubble can save attacker-provided credentials to the wrong site under certain circumstances.

This occurs when a second Save Password bubble is opened while the first bubble is still open, and then the tab is navigated to the target cross-site page with a login form. When the user types at least one character into the password field of the target site, and then clicks "Save" in the open Save Password bubble, the attacker-provided credentials are saved to the target site and are immediately autofilled.

With optimized PoC, the user only needs to hold down any key (e.g. space) for ~1s and then click "Save" on the next page.

This is essentially a browser-assisted persistent login CSRF (creds from attacker site to target site).

## VULNERABILITY DETAILS

A malicious page can open the Save Password bubble with arbitrary credentials using either...

- the Credentials API (`navigator.credentials.store(new PasswordCredentials(...))`). This does not require any user interaction.
- a form submission, as detected by the browser. The browser detects same-page form submissions, therefore the easiest way to open bubble is to clear+remove the form and call `history.pushState()`. This or any other type of form submission PoC requires minimal user interaction, such as holding down a key for a second.

Using the techniques above, an attacker can open two bubbles in quick succession. The bubbles will have attacker-provided credentials.

After the 2nd bubble is opened, the attacker can redirect the user to the target site. When the user types at least one character into the password field of the target site, the browser's password-saving logic will associate the pending credentials with the current site instead of the previous site, but keep the attacker-provided credentials displayed in the bubble UI.

At this point, the user can click "Save" which will prioritize saving the credentials shown in the bubble UI, which are the attacker-provided credentials. Since the previous step associated the internal pending credentials with the target site, the attacker-provided creds will be saved to the target site. Immediately after saving, one or both of the username/password fields will be autofilled with the saved attacker-provided credentials.

In most cases, only empty fields will be automatically filled when clicking save, but I have observed many cases where both fields will be automatically filled when clicking save. I am not yet certain why the browser sometimes autofills on non-empty fields.

## ROOT CAUSE

Observations below based on logs and code analysis.

In `PasswordSaveManagerImpl`, `pending_credentials_` [1] is a `PasswordForm` struct that "contains credentials that are ready to be written (saved or updated) to a password store" and has these relevant properties: `signon_realm`, `url`, `username_value`, and `password_value`.

In `PasswordFormManager`, `parsed_submitted_form_` [2] is also a `PasswordForm` struct.

When Credentials API `.store()` is called or form submission is detected, the browser will eventually call `PasswordFormManager::CreatePendingCredentials()` -> `PasswordSaveManagerImpl::CreatePendingCredentials()` -> `PasswordSaveManagerImpl::BuildPendingCredentials()` [3].

In the provided PoCs, this results in `pending_credentials_` with site and credentials set to the attacker site + attacker-provided values. So far, so good. (`pending_credentials_`: `attacker.com, attacker@example.com:attackerpa55word`)

When the first password input field value change occurs in the target site, `pending_credentials_`'s site and credentials are set to the target site + user-provided values. Normally, the Save Password bubble would close at this point, because the `pending_credentials_`'s site has changed but bubble input fields do not contain credential values from that site. However, the bubble stays open with the attacker-controlled credentials in the bubble's input fields. So far, despite the UI mismatch, the internal `pending_credentials_` state is still okay. (`pending_credentials_`: `example.com, user@example.com:userpa55word`)

When "Save" is pressed in the Save Password bubble, things get interesting. `UpdatePasswordFormUsernameAndPassword()` [4] is called with credentials from the bubble, which are the attacker-provided credentials. That calls `PasswordFormManager::OnUpdatePasswordFromPrompt()` [5] (and `OnUpdateUsernameFromPrompt()` too) which will override creds values in `parsed_submitted_form_` without updating any site-related values. This means `parsed_submitted_form` will have `signon_realm` and `url` values of the target site, but credentials from the bubble which were attacker-provided. After this point until the credentials are persisted, there are no more relevant updates or checks made. (`parsed_submitted_form`: `example.com, attacker@example.com:attackerpa55word`)

To persist the credentials, `BuildPendingCredentials()` [3] is called, where `pending_credentials_state_` is `PendingCredentialsState::NEW_LOGIN` and `password_to_save` is set to the attacker-provided password. Then `PendingCredentialsForNewCredentials()` uses `parsed_submitted_form_` as the source for username and resets the password value, but later in `BuildPendingCredentials()` lines 671-673 the password is set again to `password_to_save` (attacker-controlled password). Therefore, the returned pending credentials will have target site realm/URL but attacker-controlled credentials. (`pending_credentials_`: `example.com, attacker@example.com:attackerpa55word`)

[1] `pending_credentials_` <https://source.chromium.org/chromium/chromium/src/+/main:components/password_manager/core/browser/password_save_manager_impl.h;l=173;drc=20799f4c32d950ce93d495f44eec648400f38a19>

[2] `parsed_submitted_form_` <https://source.chromium.org/chromium/chromium/src/+/main:components/password_manager/core/browser/password_form_manager.h;l=465;drc=20799f4c32d950ce93d495f44eec648400f38a19>

[3] `PasswordSaveManagerImpl::BuildPendingCredentials()` <https://source.chromium.org/chromium/chromium/src/+/main:components/password_manager/core/browser/password_save_manager_impl.cc;l=623;drc=20799f4c32d950ce93d495f44eec648400f38a19>

[4] `UpdatePasswordFormUsernameAndPassword()` <https://source.chromium.org/chromium/chromium/src/+/main:components/password_manager/core/browser/password_ui_utils.cc;l=88;drc=20799f4c32d950ce93d495f44eec648400f38a19>

[5] `PasswordFormManager::OnUpdatePasswordFromPrompt()` <https://source.chromium.org/chromium/chromium/src/+/main:components/password_manager/core/browser/password_form_manager.cc;l=527;drc=20799f4c32d950ce93d495f44eec648400f38a19>

## ADDITIONAL CONTEXT

If a user has Chrome Sync enabled, the saved attacker-provided credentials will also be synced to other devices.

PoCs work regardless of whether user has existing creds saved for target site.

The Save Password bubble normally would indicate if you are saving a password for a previous site, but this does not occur in the provided PoCs. In PoC variations (can provide upon request), the cross-site message is used in the bubble, but the attacker site is still shown even when the credentials will be saved to the target site. In all scenarios, the bubble never shows the correct site.

In no-repro cases (before vuln was introduced), the 1st bubble is closed when 2nd bubble is opened, and the 2nd bubble closes when password field is typed into on the target site. In repro cases, the 2nd bubble does not close when password field is typed into on target site.

Possibly related: When opening the second bubble, I'm also seeing `WARNING:bubble_dialog_delegate_view.cc(1198)] |anchor_view| has already anchored a focusable widget.` in logs. Not sure if that's relevant to any of the bubble-not-closing behavior.

There are a couple of related nullptr read and `NOTREACHED` bugs related to multiple bubbles being open, but those should be fixed if the bubble-closing logic is fixed. AFAICT, those memory issues don't have security impacts, but I can file a separate bug if y'all want to take a quick look since I can't determine why browser enters that state.

## VERSION

Verified repro on these versions:

Chrome Version: 134.0.6998.23 Beta, 135.0.7023.0 Dev, 135.0.7034.0 Canary

Does not repro on 133.0.6943.127 Stable.

Operating System: Windows 10 (likely affects other desktop platforms too)

Does not appear to repro on Android.

## BISECT

`Fix PasswordBubbleControllerBase::OnBubbleClosing crash` <https://crrev.com/901e1c73243b371d1e159070400bb56437798f52> (Feb 12, 2025)

That was merged into M134 so it's also in M134 Beta and will likely be in M134 Stable very soon: <https://crrev.com/0ccd98952903924cb9769bb01a6c8240f3c9dc19>

Before the commit above, the Save Password bubble closes when password field is typed into on the target website. If the bubble is reopened manually, the target site's input field values will be in the bubble, not the attacker-provided credentials.

## REPRODUCTION CASE

Note: While testing, if the save creds bubble stops opening automatically, please go to chrome://settings/clearBrowserData select the Advanced tab and delete "Passwords and other sign-in data". AFAICT after a few times (5+ times?) if the user ignores the save creds bubbles, the bubble will not be automatically opened.

### PoC: Using form submit

1. Navigate to <https://alesandroortiz.com/security/chromium/save-creds-cross-site-form.html>
2. Press and hold any key (e.g. space) until next page loads.
3. Click "Save" in Save Password bubble.
4. If password field is not autofilled: Interact with password field again and choose saved password from autofill menu. (Password will sometimes be autofilled, so this step may not be needed.)

To see where the credentials were saved, open chrome://password-manager

Observed: Save Password bubble remains open even after typing in password field in target site. Browser saves credentials provided by attacker site (first site) to the target site (second site).

Expected: Save Password bubble is closed after typing in password field in target site. Browser does not save credentials provided by attacker site (first site) to the target site (second site) even if the bubble remains open due to a bug.

### PoC: Using Credentials API

1. Navigate to <https://alesandroortiz.com/security/chromium/save-creds-cross-site-api.html>

Steps 2-4: (Same as previous PoC)

Observed/Expected: Same as previous PoC.

## Credit Information

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [save-creds-cross-site-form.html](attachments/save-creds-cross-site-form.html) (text/html, 2.6 KB)
- [save-creds-cross-site-api.html](attachments/save-creds-cross-site-api.html) (text/html, 1.9 KB)
- [login-form.html](attachments/login-form.html) (text/html, 481 B)
- [save-creds-cross-site-form.mp4](attachments/save-creds-cross-site-form.mp4) (video/mp4, 2.5 MB)
- [save-creds-cross-site-api.mp4](attachments/save-creds-cross-site-api.mp4) (video/mp4, 2.3 MB)

## Timeline

### al...@alesandroortiz.com (2025-02-26)

I might be biting more than I can chew, but I'll try to work on a patch to fix the underlying cross-site credentials issue. Ideally, even if the bubble remains open due to any current or future bugs, the creds should be saved to the correct site (or other safe behavior should occur).

I'll provide one or more potential strategies in comments in the coming days, since there are probably many ways to approach fix.

The reason why I want to harden the credential-saving logic, instead of only fixing the bubble remaining open, is because a similar issue was reported back in 2021: <https://crbug.com/40057696#comment20> . The views issue was fixed, but the credential-saving logic was not hardened. Essentially the same bug is occurring again now.

### al...@alesandroortiz.com (2025-02-26)

To examine behavior more closely, you can use the Form Submit PoC but instead of holding down a key, you press a key once, then wait, and repeat until you've typed into the target site's password field.

This was helpful when doing logging of internal state.

### hc...@google.com (2025-02-26)

I was not able to repro the form example, but the credentials API version did work. Repro was on Mac, both canary (135.0.7037.0) and beta (134.0.6998.23)

Provisionally, i'm going to mark this as Medium (S2) severity, though I could be convinced of a higher or lower severity.

@tschafhitzel, could you take a look at this (or delegate to someone who can take a look)?

### ch...@google.com (2025-02-27)

Setting milestone because of s2 severity.

### ch...@google.com (2025-02-27)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### va...@chromium.org (2025-02-27)

Interesting bug. I confirm that r1419263 is the culprit. The problem is that when another bubble opens the order of open/close events is reversed:
- bubble1 opens with PasswordBubbleViewBase::ShowBubble
- bubble2 opens with PasswordBubbleViewBase::ShowBubble
- bubble1 receives WindowClosingCallback and NULLs the `g_manage_passwords_bubble_` variable. That code should be more careful and should not overwrite `g_manage_passwords_bubble_` if it's value has changed.

### va...@chromium.org (2025-02-27)

Unfortunately we passed the first release candidate but it would be useful to merge it to the next respin.

### va...@chromium.org (2025-02-27)

The fix is here https://chromium-review.googlesource.com/c/chromium/src/+/6310316

Anna, we need a browser test and a merge back.

### ap...@google.com (2025-02-27)

Project: chromium/src  

Branch: main  

Author: Vasilii Sukhanov <[vasilii@google.com](mailto:vasilii@google.com)>  

Link:      <https://chromium-review.googlesource.com/6310316>

NULL `g_manage_passwords_bubble_` variable only when there is no next password bubble already open.

---


Expand for full commit details
```
NULL `g_manage_passwords_bubble_` variable only when there is no next 
password bubble already open. 
 
Bug: 399131922 
Change-Id: I353f79d68a60685dae8f9959d17d862eabdff4a7 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6310316 
Reviewed-by: Maria Kazinova <kazinova@google.com> 
Commit-Queue: Vasilii Sukhanov <vasilii@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1425828}

```

---

Files:

- M `chrome/browser/ui/views/passwords/password_bubble_view_base.cc`

---

Hash: dd20082c991be9e8e404ac85dcd13c5972781f30  

Date:  Thu Feb 27 10:12:32 2025


---

### al...@alesandroortiz.com (2025-02-27)

Thanks for landing quick fix for bubble issue.

I'll still look into hardening the save password logic to avoid similar issues from ocurring again.

### am...@chromium.org (2025-02-27)

Since the fix has been landed, I'm going to go ahead and close this as fixed so the security automation can tag this with the correct tags as a backmerge candidate.
The M134 Stable RC for release on Tuesday has already been cut so there's no rush atm for backmerge.
As a medium severity issue, we would not rush to get this in any faster.

It would also be helpful if the test can be landed in parallel to all this.

### ch...@google.com (2025-02-28)

Merge review required: M134 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### at...@google.com (2025-03-04)

1. This is a security issue fix. This is also a regression in M134.
2.  https://chromium-review.googlesource.com/6310316
3. Yes
4. This is not behind the feature flag.
5. N/A
6. Doesn't require manual verification.

### ap...@google.com (2025-03-05)

Project: chromium/src  

Branch: main  

Author: Anna Tsvirchkova <[atsvirchkova@google.com](mailto:atsvirchkova@google.com)>  

Link:      <https://chromium-review.googlesource.com/6322787>

Browser test for new bubble opened while the old one still pending

---


Expand for full commit details
```
Browser test for new bubble opened while the old one still pending 
 
Adds a browser test, which opens a new bubble while the old one is still 
not closed. Verifies that the value of the currently opened bubble is 
correct. 
 
Bug: 399131922 
Change-Id: Ic82a1097e52bcbcd252ce10b3cfbd984f5556258 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6322787 
Commit-Queue: Anna Tsvirchkova <atsvirchkova@google.com> 
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1428201}

```

---

Files:

- M `chrome/browser/ui/views/passwords/password_bubble_interactive_uitest.cc`

---

Hash: 8bf1b0979341d043e600580ff68327c9aa125956  

Date:  Wed Mar 05 01:45:38 2025


---

### am...@chromium.org (2025-03-06)

Hi Alesandro, thank you for this report. While we appreciate this report, in our assessment, there does not appear to be a real potential for user harm resulting from this issue.
The goal of this report appears focused on hardening in this area rather than addressing and reporting a security issue. We really appreciate reports like this, but could you please submit them as Feature Requests in the future? Given your familiarity with a previous report of this issue, I'm sure the outcome is not surprising given a similar assessment was conveyed in that report as well (<https://issues.chromium.org/issues/40057696#comment56>), despite my follow-up was lacking by not converting that issue to a functional bug at the time.
We're unfortunately unable to extend a Chrome VRP reward for this report, but did want to ensure we addressed the full outcome directly on the bug.

### sr...@google.com (2025-03-06)

i will let Amy review/approve this for respin next week

### am...@chromium.org (2025-03-06)

This is not a security issue, but a functional bug, This fix does not meet the justification for a backmerge from a security standpoint.

### ch...@google.com (2025-06-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/399131922)*

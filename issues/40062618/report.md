# Security: FedCM should have clickjacking protection

| Field | Value |
|-------|-------|
| **Issue ID** | [40062618](https://issues.chromium.org/issues/40062618) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Identity>FedCM |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | re...@gmail.com |
| **Assignee** | np...@chromium.org |
| **Created** | 2023-01-12 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The Federated Credential Management API allows a website to link to a Terms of Service page. This link is not checked against the usual blocklists and can be used to open internal (chrome://, chrome-devtools://, chrome-search://, chrome-extension:// etc) or otherwise blocked (file:///, javascript:, data:, blob: etc) URLs in a new tab. The Terms of Service link can also be easily clickjacked.

By itself this vulnerability isn't particularly harmful, but it can be used as a part of an exploit chain if combined with an url-based vulnerability (this could also be in a 3rd party extension through the chrome-extension:// scheme).

Affected component: Blink>Identity>FedCM  

Relevant code: <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc;l=228;drc=eb4b4965cd56b40dc1afdbb4c2aefe46eed0dcc7>  

A check such as `if (!url.is_valid() || !url.SchemeIsHTTPOrHTTPS()) return;` could be used here to mitigate the issue.

**VERSION**  

Chrome Version: Stable, Dev (110.0.5481.30)  

Operating System: Windows, macOS, Linux

**REPRODUCTION CASE**

1. Download the `accounts_endpoint.json`, `client_metadata_static.json`, `fedcm.json`, and `poc.html` files into a folder.
2. Download the `web-identity` file into a subfolder named `.well-known`.
3. Run a webserver on port 8000 in the main folder (`python3 -m http.server`).
4. Open `http://localhost:8000/` in Chrome (preferably maximized) and rapidly click the cookie.
5. The browser should open `chrome://restart/` in a new tab and restart the browser.

This reproduction case can also be seen in the `demo.mp4` file.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Jasper Rebane (popstonia)

## Attachments

- [demo.mp4](attachments/demo.mp4) (video/mp4, 1.0 MB)
- [accounts_endpoint.json](attachments/accounts_endpoint.json) (text/plain, 270 B)
- [client_metadata_static.json](attachments/client_metadata_static.json) (text/plain, 49 B)
- [fedcm.json](attachments/fedcm.json) (text/plain, 176 B)
- [poc.html](attachments/poc.html) (text/plain, 526 B)
- [web-identity](attachments/web-identity) (text/plain, 61 B)
- [With protection.mov](attachments/With protection.mov) (video/quicktime, 3.0 MB)
- [Without protection.mov](attachments/Without protection.mov) (video/quicktime, 1.8 MB)

## Timeline

### [Deleted User] (2023-01-12)

[Empty comment from Monorail migration]

### ke...@chromium.org (2023-01-12)

Thanks for the report.

This is a dupe of https://crbug.com/chromium/1404822.

Clickjacking of Chrome UI over the content area is a concern but is being looked at in a context more broad than FedCM.

### ke...@chromium.org (2023-01-12)

Re-opening, because cthomp@ mentioned that there are protections against clickjacking in other features, and that is distinct from the problem with allowing chrome:// URLs in the privacy policy.

For example, PaymentRequestUI on Android has a 225ms delay before appearing, after the page invokes it.

Clickjacking FedCM dialogs would be bad for user privacy, and a similar mitigation might be appropriate here.

[Monorail components: Blink>Identity>FedCM]

### [Deleted User] (2023-01-12)

[Empty comment from Monorail migration]

### np...@chromium.org (2023-01-12)

Is the concern that the dialog could show up too soon, hence the developer can clickjack it by:
1. Adding some content which entices the user to click on.
2. Adding a hover listener which immediately invokes FedCM
3. If the user clicks right at the right moment, the FedCM dialog is invoked since the content is placed in the location where the continue button would show.

If so,
1. How does this work on Android in terms of clickjacking?
2. Is a delay considered good enough mitigation? It can be done (on desktop and/or mobile)

### ke...@chromium.org (2023-01-12)

There is some documentation on this at https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/security-considerations-for-browser-ui.md#clickjacking-and-keyjacking.

### cb...@chromium.org (2023-01-12)

Clickjacking fedcm is harder than other dialogs since we do only show the dialog after some network requests (so there's network latency in between)

### yi...@chromium.org (2023-01-12)

Not sure having a delay is sufficient: an attacker can trick users to click on a specific location 10 times to win a prize so even if the UI is delayed, clickjacking still happens.

Alternatively we can make the FedCM non-clickable for N ms. Luckily we have data showing how long it takes a user to click the "Continue" button after the UI is displayed so we can come up with a reasonable "N".

### np...@chromium.org (2023-01-12)

Making the UI non-clickable on purpose for some amount of time would be great against clickjacking, but I think it is a very bad user experience (well, I guess it depends on how long). I much rather have delayed UI than non-interactable UI.

### cb...@chromium.org (2023-01-12)

Yi is right that delayed UI does not help here unfortunately.

On the positive side the delay should be something like 200ms-ish (as suggested in https://crbug.com/chromium/1406900#c3), so hopefully it won't annoy users in practice.

### re...@gmail.com (2023-01-12)

The permissions prompt component implements non-clickable UI delay and I think the same delay would make sense here. The way it works there is that it has a relatively short delay (500ms by default) that gets reset on every click, which means that repeated clicking from a clickjack attack gets blocked but the delay isn't that noticable in real-world use.

See: https://source.chromium.org/chromium/chromium/src/+/main:ui/views/input_event_activation_protector.cc

### np...@chromium.org (2023-01-12)

Based on looking at our internal data, we think making the UI unclickable for 300ms would not cause significant harm to users. cthomp@ or others from security, do you think this. is a good enough mitigation for the clickjacking?

### ct...@chromium.org (2023-01-18)

That seems like a reasonable mitigation for this feature if it is compatible with your required user experience. In practice, few clickjacking protections are "perfect" but introducing some protections can greatly reduce the feasibility of abuse.

### np...@chromium.org (2023-01-24)

The desktop protection is landing, but I'm still investigating if there is an equivalent sort of thing for mobile.

### gi...@appspot.gserviceaccount.com (2023-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c72670da208ec24ad630490a2f183ee943a7e6d9

commit c72670da208ec24ad630490a2f183ee943a7e6d9
Author: Nicolás Peña Moreno <npm@chromium.org>
Date: Tue Jan 24 21:55:31 2023

[FedCM] Add input event protection on desktop

This CL leverages InputEventActivationProtector to add protection
against events that happen too quickly after the FedCM bubble becomes
visible to the user.

Bug: 1406900
Change-Id: I77f65573280915fb98947a4f6d8e09bedb76fee8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4184294
Commit-Queue: Nicolás Peña <npm@chromium.org>
Reviewed-by: Yi Gu <yigu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1096393}

[modify] https://crrev.com/c72670da208ec24ad630490a2f183ee943a7e6d9/chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc
[modify] https://crrev.com/c72670da208ec24ad630490a2f183ee943a7e6d9/chrome/browser/ui/views/webid/account_selection_bubble_view.h
[modify] https://crrev.com/c72670da208ec24ad630490a2f183ee943a7e6d9/chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.h
[modify] https://crrev.com/c72670da208ec24ad630490a2f183ee943a7e6d9/chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop_unittest.cc


### np...@chromium.org (2023-01-25)

I have a draft CL to protect the UI on mobile but it does not seem like it adds a lot because the UI is animated in. See the two attached for behavior with and without protection (it's hard to activate the protection). One could argue that the timer needs to be larger, to account for the animation, but this could also be disruptive for users actually attempting to login. I'm tempted to consider the Android animation as sufficient click jacking protection and close this issue. cthomp@ what do you think?

### ct...@chromium.org (2023-02-08)

Thanks for investigating and capturing the videos for comparison. Since the animation already takes roughly as long as the protection, that seems reasonable to me. One potential benefit of having the delay protection would be in case the animation changes in the future -- then having the delay would be a backstop. I don't feel strongly about that though, as this overall feels lower risk than on Desktop due to the different input modality.

### gi...@appspot.gserviceaccount.com (2023-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4e2bb66d385c8b15bcb5fea2722d00b9c42b7aad

commit 4e2bb66d385c8b15bcb5fea2722d00b9c42b7aad
Author: Nicolás Peña Moreno <npm@chromium.org>
Date: Thu Feb 09 17:17:06 2023

[FedCM] Dismiss account clicks if shortly after account is shown.

Bug: 1406900
Change-Id: I3b13fc9614af33401a790b908a8968284289538a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4195023
Reviewed-by: Christian Biesinger <cbiesinger@chromium.org>
Commit-Queue: Nicolás Peña <npm@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1103321}

[modify] https://crrev.com/4e2bb66d385c8b15bcb5fea2722d00b9c42b7aad/chrome/browser/ui/android/webid/internal/java/src/org/chromium/chrome/browser/ui/android/webid/AccountSelectionControllerTest.java
[modify] https://crrev.com/4e2bb66d385c8b15bcb5fea2722d00b9c42b7aad/chrome/browser/ui/android/webid/internal/java/src/org/chromium/chrome/browser/ui/android/webid/AccountSelectionMediator.java


### yi...@chromium.org (2023-03-02)

[Empty comment from Monorail migration]

### np...@chromium.org (2023-03-31)

Forgot to close this.

### am...@chromium.org (2023-03-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-01)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-13)

Congratulations, Jasper! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-07-08)

This issue was migrated from crbug.com/chromium/1406900?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedinto: crbug.com/chromium/1404822]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-25)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062618)*

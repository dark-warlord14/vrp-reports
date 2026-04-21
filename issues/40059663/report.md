# Security: UAF in WebAuthnIconView

| Field | Value |
|-------|-------|
| **Issue ID** | [40059663](https://issues.chromium.org/issues/40059663) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAuthentication |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ns...@chromium.org |
| **Created** | 2022-05-13 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

`WebAuthnIconView::UpdateImpl` will add[1] self as an observer into `AuthenticatorRequestDialogModel`, and the observer will not be removed. As shown in the POC, there is a way to let `WebAuthnIconView` be destructed before `AuthenticatorRequestDialogModel`, the UAF will be triggered when the observer gets access.

[1].<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/webauthn/webauthn_icon_view.cc;l=70;drc=5fcac0124af542ac029855dd600141c1c631bc53;bpv=0;bpt=0>

Fix suggestion:

diff --git a/chrome/browser/ui/views/webauthn/webauthn\_icon\_view.cc b/chrome/browser/ui/views/webauthn/webauthn\_icon\_view.cc  

index 5f618bdb882..c2e9e0f5700 100644  

--- a/chrome/browser/ui/views/webauthn/webauthn\_icon\_view.cc  

+++ b/chrome/browser/ui/views/webauthn/webauthn\_icon\_view.cc  

@@ -35,6 +35,8 @@ WebAuthnIconView::~WebAuthnIconView() {  

if (webauthn\_bubble\_) {  

webauthn\_bubble\_->GetWidget()->RemoveObserver(this);  

}

- for (const auto& it : dialog\_models\_)
- it.second->RemoveObserver(this);  
  
  }

views::BubbleDialogDelegate\* WebAuthnIconView::GetBubble() const {

**VERSION**  

stable with WebAuthenticationConditionalUI

**REPRODUCTION CASE**  

$ out/asan/chrome --user-data-dir=/tmp/xxxx --enable-features=WebAuthenticationConditionalUI --load-extension="/path/to/extension”

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [asan](attachments/asan) (text/plain, 30.8 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 234 B)
- [background.js](attachments/background.js) (text/plain, 496 B)
- [blank.html](attachments/blank.html) (text/plain, 5 B)
- [poc.html](attachments/poc.html) (text/plain, 30 B)
- [poc.js](attachments/poc.js) (text/plain, 730 B)

## Timeline

### [Deleted User] (2022-05-13)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-05-15)

Thank you for your report and your fix suggestion. I agree from code inspection this does seem to look like an oversight. I'm assigning to nsatragno@ to take a look.

[Monorail components: Blink>WebAuthentication]

### wf...@chromium.org (2022-05-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-15)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2022-05-16)

WebAuthn Conditional UI hasn't shipped so this is SecImpact-None.

### wf...@chromium.org (2022-05-16)

If WebAuthn Conditional UI is available via flag, switch or fieldtrial then it has security impact, can you confirm this please?

### ns...@chromium.org (2022-05-16)

The feature is available via a command-line switch only at this time.

### ke...@chromium.org (2022-05-16)

wfh@: The requirement to set a switch means it does not affect any users running a default configuration of Chrome. We have always set these as Security_Impact-None.
https://chromium.googlesource.com/chromium/src/+/master/docs/security/sheriff.md#step-3_set-foundin


### gi...@appspot.gserviceaccount.com (2022-05-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/861e20fffd861c900ddcd6bd6a219b0ce18bea02

commit 861e20fffd861c900ddcd6bd6a219b0ce18bea02
Author: Nina Satragno <nsatragno@chromium.org>
Date: Mon May 16 16:10:51 2022

[webauthn] Make dialog model observers checked

Make AuthenticatorRequestDialogModel::Observer a CheckedObserver to
defened against potential UAF. This is not a performance-sensitive
class.

Bug: 1325341
Change-Id: Ia401284a4e4d60f1ce0927b791a3bf9d98c5a422
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3645773
Auto-Submit: Nina Satragno <nsatragno@chromium.org>
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Commit-Queue: Nina Satragno <nsatragno@chromium.org>
Commit-Queue: Ken Buchanan <kenrb@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1003779}

[modify] https://crrev.com/861e20fffd861c900ddcd6bd6a219b0ce18bea02/chrome/browser/webauthn/authenticator_request_dialog_model.h


### gi...@appspot.gserviceaccount.com (2022-05-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/58a021df658a303179913f8103d3fc1e5feb62b9

commit 58a021df658a303179913f8103d3fc1e5feb62b9
Author: Nina Satragno <nsatragno@chromium.org>
Date: Mon May 16 16:39:56 2022

[webauthn] Remove Conditional UI bubble

The current direction of Conditional UI does not involve showing an
omnibar bubble, that was mostly left from a previous prototype. The code
also has a UAF that will go away after this code is removed.

Bug: 1171985
Change-Id: Ifa809699b398afdd0e76f598bddaaf8af043826c
Fixed: 1325341
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3650855
Commit-Queue: Evan Stade <estade@chromium.org>
Reviewed-by: Evan Stade <estade@chromium.org>
Auto-Submit: Nina Satragno <nsatragno@chromium.org>
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1003792}

[modify] https://crrev.com/58a021df658a303179913f8103d3fc1e5feb62b9/chrome/browser/ui/views/page_action/page_action_icon_controller.cc
[delete] https://crrev.com/a466dc2ea8c51c471c8236597681af10e60f6149/chrome/browser/ui/views/webauthn/webauthn_icon_view.cc
[delete] https://crrev.com/a466dc2ea8c51c471c8236597681af10e60f6149/chrome/browser/ui/views/webauthn/webauthn_bubble_view.h
[modify] https://crrev.com/58a021df658a303179913f8103d3fc1e5feb62b9/chrome/browser/webauthn/chrome_authenticator_request_delegate.cc
[modify] https://crrev.com/58a021df658a303179913f8103d3fc1e5feb62b9/chrome/test/BUILD.gn
[modify] https://crrev.com/58a021df658a303179913f8103d3fc1e5feb62b9/chrome/browser/ui/BUILD.gn
[modify] https://crrev.com/58a021df658a303179913f8103d3fc1e5feb62b9/chrome/browser/ui/views/location_bar/location_bar_view.cc
[modify] https://crrev.com/58a021df658a303179913f8103d3fc1e5feb62b9/chrome/browser/ui/page_action/page_action_icon_type.h
[delete] https://crrev.com/a466dc2ea8c51c471c8236597681af10e60f6149/chrome/browser/ui/views/webauthn/webauthn_bubble_view.cc
[delete] https://crrev.com/a466dc2ea8c51c471c8236597681af10e60f6149/chrome/browser/ui/views/webauthn/webauthn_icon_interactive_uitest.cc
[delete] https://crrev.com/a466dc2ea8c51c471c8236597681af10e60f6149/chrome/browser/ui/views/webauthn/webauthn_icon_view.h


### [Deleted User] (2022-05-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-16)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-27)

Congratulations, Leecraso and Guang Gong! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts in reporting this issue to us and great work! 

### am...@google.com (2022-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-08-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/319a2dd4ec59efaec80d1752c24a22a43169bc7b

commit 319a2dd4ec59efaec80d1752c24a22a43169bc7b
Author: Sergei Glazunov <glazunov@google.com>
Date: Wed Aug 31 14:30:15 2022

[BRP] Use raw_ptr<T> in UncheckedObserverAdapter

In the past few months, we've seen multiple use-after-free issues caused
by using the `ObserverList::Unchecked` container, which currently isn't
protected by MiraclePtr. Although we haven't yet started modifying all
containers to use raw_ptr<T> by default, this high-risk case is worth of
addressing immediately.

Bug: 1325341
Change-Id: Ib22bfb17d6f9c9983174489aeeb58c7fdbe31223
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3864671
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Sergei Glazunov <glazunov@google.com>
Cr-Commit-Position: refs/heads/main@{#1041510}

[modify] https://crrev.com/319a2dd4ec59efaec80d1752c24a22a43169bc7b/base/observer_list_internal.h


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1325341?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059663)*

# Autofill suggestions appear off-screen, allowing covert access to user data

| Field | Value |
|-------|-------|
| **Issue ID** | [430555440](https://issues.chromium.org/issues/430555440) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ku...@google.com |
| **Created** | 2025-07-09 |
| **Bounty** | Confirmed (amount unknown) |

## Description

---

### Report description

Autofill suggestions appear off-screen, allowing covert access to user data

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

1. Open <https://alesandroortiz.com/security/chromium/fedcm-autofill.html>
2. Move the window to the right, partially off-screen, so that a portion of the autofill input field (and its dropdown area) is no longer visible.
3. Press the down arrow key, then press Enter.

#### Impact analysis – Please briefly explain who can exploit the vulnerability, and what they gain when doing so

Once the autofill popup is hidden off-screen, the attacker can trick the user into pressing the arrow key and Enter, revealing sensitive autofill data without any visible indication.

---

### The cause

#### What version of Chrome have you found the security issue in?

140.0.7284.0

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Clickjacking

## Attachments

- [09.07.2025_02.58.32_REC.mp4](attachments/09.07.2025_02.58.32_REC.mp4) (video/mp4, 662.2 KB)
- [fedcm-autofill.html](attachments/fedcm-autofill.html) (text/html, 4.3 KB)

## Timeline

### el...@chromium.org (2025-07-09)

Security shepherd: thanks for the report. Your repro doesn't work for me: the down arrow key doesn't cause the autofill prompt to appear. Maybe I'm missing a step?

Given that this requires a somewhat unlikely user interaction (positioning the page in a specific way) in order to allow an autofill of same-origin data, I'm going to call this a medium-severity bug.

### ch...@gmail.com (2025-07-09)

Prerequisite: Have at least one address in chrome://settings/addresses

### pe...@google.com (2025-07-09)

Thank you for providing more feedback. Adding the requester to the CC list.

### el...@chromium.org (2025-07-09)

Aha, got it - thank you. I can repro this on macOS 15.5 with 140.0.7281.0 and 137.0.7151.120. I would expect this to apply on all desktop platforms. Marking Pri / Sev, FoundIn, and OS, and sending to autofill :)

### ba...@google.com (2025-07-09)

Attaching the proof of concept.

### ba...@google.com (2025-07-09)

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/autofill/popup/popup_view_utils.cc> is where the fix would probably live.

### el...@chromium.org (2025-07-09)

-> battre@ for triage!

### ch...@gmail.com (2025-07-09)

I think the proper fix is updating the popup positioning code (such as in popup_view_utils.cc) to ensure the autofill dropdown is always fully visible within the browser window bounds. Additionally, keyboard navigation should be disabled or ignored when the popup is not visible to prevent covert exposure of sensitive autofill data.


### ba...@google.com (2025-07-10)

Rafal, can you please find an owner?

### ch...@google.com (2025-07-10)

Setting milestone because of s2 severity.

### ch...@gmail.com (2025-07-17)

Any update? Thanks.

### dx...@google.com (2025-08-04)

Project: chromium/src  

Branch:  main  

Author:  Dominic Battré [battre@chromium.org](mailto:battre@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6788649>

Clarify the logic for placing the popup on the screen

---


Expand for full commit details
```
     
    This CL adds clarifying comments to the `popup_view_utils` and `popup_base_view`. It also fixes a typo. 
     
    No functional changes are intended. 
     
    Bug: 430555440 
    Change-Id: Ic8d16472c34e23738d34a2cee1eab88e4c1ce016 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6788649 
    Commit-Queue: Dominic Battré <battre@chromium.org> 
    Reviewed-by: Bruno Braga <brunobraga@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1496211}

```

---

Files:

- M `chrome/browser/ui/views/autofill/popup/popup_base_view.cc`
- M `chrome/browser/ui/views/autofill/popup/popup_view_utils.cc`
- M `components/autofill/core/browser/ui/popup_open_enums.h`

---

Hash: [0ab42489bd437544d3679282dad771d3db2403dd](http://crrev.com/0ab42489bd437544d3679282dad771d3db2403dd)  

Date: Mon Aug 4 10:06:38 2025


---

### ch...@google.com (2025-08-05)

kuchyn: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ku...@google.com (2025-08-19)

CCing for visibility: @jk...@google.com @br...@google.com

### dx...@google.com (2025-09-05)

Project: chromium/src  

Branch:  main  

Author:  Mikita Kuchyn [kuchyn@google.com](mailto:kuchyn@google.com)  

Link:    <https://chromium-review.googlesource.com/6779373>

Fix a clickjacking out-of-screen Autofill popup issue

---


Expand for full commit details
```
     
    Autofill popups could appear on the page off-screen horizontally. 
    This CL restricts popup-generating elements to appear at least 100px 
    horizontally on-screen to generate the popup. 
     
    Bug: 430555440 
    Change-Id: Ic0d66a980d6bf80d033b0b7ea96ae2bb76067317 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6779373 
    Auto-Submit: Mikita Kuchyn <kuchyn@chromium.org> 
    Reviewed-by: Jan Keitel <jkeitel@google.com> 
    Reviewed-by: Dominic Battré <battre@chromium.org> 
    Commit-Queue: Jan Keitel <jkeitel@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1511370}

```

---

Files:

- M `chrome/browser/ui/views/autofill/popup/popup_base_view.cc`
- M `chrome/browser/ui/views/autofill/popup/popup_view_utils.cc`
- M `chrome/browser/ui/views/autofill/popup/popup_view_utils.h`
- M `chrome/browser/ui/views/autofill/popup/popup_view_views.cc`
- M `chrome/browser/ui/views/autofill/popup/popup_view_views_unittest.cc`

---

Hash: [b4f503e5ac9434d71742855e548f243098d35071](https://chromiumdash.appspot.com/commit/b4f503e5ac9434d71742855e548f243098d35071)  

Date: Fri Sep 5 08:10:46 2025


---

### dx...@google.com (2025-09-05)

Project: chromium/src  

Branch:  main  

Author:  [luci-bisection@appspot.gserviceaccount.com](mailto:luci-bisection@appspot.gserviceaccount.com) [luci-bisection@appspot.gserviceaccount.com](mailto:luci-bisection@appspot.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/6918682>

Revert "Fix a clickjacking out-of-screen Autofill popup issue"

---


Expand for full commit details
```
     
    This reverts commit b4f503e5ac9434d71742855e548f243098d35071. 
     
    Reason for revert: 
    LUCI Bisection has identified this change as the cause of a test failure. See the analysis: https://ci.chromium.org/ui/p/chromium/bisection/test-analysis/b/5154229313339392 
     
    Sample build with failed test: https://ci.chromium.org/b/8704575934091332833 
    Affected test(s): 
    [ninja://chrome/test:unit_tests/PopupViewViewsTest.PopupPositioning](https://ci.chromium.org/ui/test/chromium/ninja:%2F%2Fchrome%2Ftest:unit_tests%2FPopupViewViewsTest.PopupPositioning?q=VHash%3A799aae891109c818) 
     
    If this is a false positive, please report it at http://b.corp.google.com/createIssue?component=1199205&description=Analysis%3A+https%3A%2F%2Fci.chromium.org%2Fui%2Fp%2Fchromium%2Fbisection%2Ftest-analysis%2Fb%2F5154229313339392&format=PLAIN&priority=P3&title=Wrongly+blamed+https%3A%2F%2Fchromium-review.googlesource.com%2Fc%2Fchromium%2Fsrc%2F%2B%2F6779373&type=BUG 
     
    Original change's description: 
    > Fix a clickjacking out-of-screen Autofill popup issue 
    > 
    > Autofill popups could appear on the page off-screen horizontally. 
    > This CL restricts popup-generating elements to appear at least 100px 
    > horizontally on-screen to generate the popup. 
    > 
    > Bug: 430555440 
    > Change-Id: Ic0d66a980d6bf80d033b0b7ea96ae2bb76067317 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6779373 
    > Auto-Submit: Mikita Kuchyn <kuchyn@chromium.org> 
    > Reviewed-by: Jan Keitel <jkeitel@google.com> 
    > Reviewed-by: Dominic Battré <battre@chromium.org> 
    > Commit-Queue: Jan Keitel <jkeitel@google.com> 
    > Cr-Commit-Position: refs/heads/main@{#1511370} 
    > 
     
    Bug: 430555440 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: I6eb01e9b6e339a5ade6cadee277249c2fb54a430 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6918682 
    Commit-Queue: Jan Keitel <jkeitel@google.com> 
    Reviewed-by: Jan Keitel <jkeitel@google.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1511464}

```

---

Files:

- M `chrome/browser/ui/views/autofill/popup/popup_base_view.cc`
- M `chrome/browser/ui/views/autofill/popup/popup_view_utils.cc`
- M `chrome/browser/ui/views/autofill/popup/popup_view_utils.h`
- M `chrome/browser/ui/views/autofill/popup/popup_view_views.cc`
- M `chrome/browser/ui/views/autofill/popup/popup_view_views_unittest.cc`

---

Hash: [7d786ea4823183dcb2c3cb7b77a22b8db1236592](https://chromiumdash.appspot.com/commit/7d786ea4823183dcb2c3cb7b77a22b8db1236592)  

Date: Fri Sep 5 11:51:24 2025


---

### ch...@google.com (2025-09-06)

kuchyn: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2025-09-09)

Project: chromium/src  

Branch:  main  

Author:  Mikita Kuchyn [kuchyn@google.com](mailto:kuchyn@google.com)  

Link:    <https://chromium-review.googlesource.com/6923585>

Fix a clickjacking out-of-screen Autofill popup issue

---


Expand for full commit details
```
     
    Autofill popups could appear on the page off-screen horizontally. This 
    CL restricts popup-generating elements to appear at least 100px 
    horizontally on-screen to generate the popup. 
     
    Previous attempt to upload this ( crrev.com/c/6779373 ) got reverted ( 
    crrev.com/c/6918682 ) since ResizeTestScreen function failed Linux UBSan 
    builder test. 
     
    List of changes from crrev.com/c/6779373 : 
    * Changed screen class from display::test::TestScreen to 
    display::ScreenBase (popup_view_views_unittest.cc:338-339) to fix Linux 
    UBSan builder test. 
    * Had to migrate from display::Screen::GetScreen() to 
    display::Screen::Get() (crrev.com/c/6860363) 
    * Added a comment over kMinHorizontalOverlapForPopup to mention 
    clickjacking as a goal of having this constant (popup_view_utils.h:23). 
     
    Bug: 430555440 
    Change-Id: If17de61a9d50688bbd556ce84fbc03b5026b70b0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6923585 
    Auto-Submit: Mikita Kuchyn <kuchyn@chromium.org> 
    Reviewed-by: Dominic Battré <battre@chromium.org> 
    Reviewed-by: Jan Keitel <jkeitel@google.com> 
    Commit-Queue: Dominic Battré <battre@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1512982}

```

---

Files:

- M `chrome/browser/ui/views/autofill/popup/popup_base_view.cc`
- M `chrome/browser/ui/views/autofill/popup/popup_view_utils.cc`
- M `chrome/browser/ui/views/autofill/popup/popup_view_utils.h`
- M `chrome/browser/ui/views/autofill/popup/popup_view_views.cc`
- M `chrome/browser/ui/views/autofill/popup/popup_view_views_unittest.cc`

---

Hash: [458cb99966914ffe4c4f175dc8f8b1a9e50aa425](https://chromiumdash.appspot.com/commit/458cb99966914ffe4c4f175dc8f8b1a9e50aa425)  

Date: Tue Sep 9 11:13:50 2025


---

### ch...@gmail.com (2025-09-09)

Fixed on Chromium 142.0.7404.0 (Branch: 1513012).

### ch...@google.com (2025-09-10)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-09-19)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

The panel believed this level of interaction is beyond what a “reasonable and prudent” user would do (see FAQ). if you can demonstrate programmatic ability to shift window off screen to hide suggestions the panel will consider a re-evaluation of this reward.

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2025-12-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> The panel believed this level of interaction is beyond what a “reasonable and prudent” user would do (see FAQ). if you can demonstrate programmatic ability to shift window off screen to hide suggestions the panel will consider a re-evaluation of this reward.
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you kno

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/430555440)*

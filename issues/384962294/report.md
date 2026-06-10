# Steps to reproduce the problem

| Field | Value |
|-------|-------|
| **Issue ID** | [384962294](https://issues.chromium.org/issues/384962294) |
| **Status** | Unknown |
| **Severity** | Unknown |
| **Priority** | Unknown |
| **Component** | Unknown |
| **Reporter** | Unknown |
| **Created** | 2024-12-18 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

- 1. Access <https://newuploadmethodfromgoogledrive.glitch.me/Google.html> on Chrome
- 2. Click anywhere on the page
- 3. A Small window will show up, Click anywhere in Small Window
- 4. A hidden origin PWA Installation Dialog will show up, now Click [Install]

`Result:` Successfully Installed Malicious Application on User Desktop

I have also attached the files used in the PoC - if you prefer, you can reproduce it by downloading and hosting POC.html on a web server.

# Problem Description

When a user clicks on the attacker's page it is possible to Hide origin in PWA Installation Dialog Using Small Window Due to the small size window the origin information goes hidden on Installation dialog

Because the origin doesn't not show on Installation dialog the user is not capable to know exact origin information, which allows attacker to Convince user to Install the Application

# Additional Comments

`OS:` Windows 10

# Summary

In PWA Installation Dialog Hide Origin Using Window

# Custom Questions

#### Reporter credit:

Puf Umar

# Additional Data

Category: Security   

Chrome Channel: Beta   

Regression: N/A

## Attachments

- [repro.mp4](attachments/repro.mp4) (video/mp4, 476.3 KB)
- deleted (application/octet-stream, 0 B)
- [HalfDialog133.png](attachments/HalfDialog133.png) (image/png, 34.2 KB)

## Timeline

### pu...@gmail.com (2024-12-18)

## Steps to reproduce the problem - Updated Link

- 1. Access <https://googleinstallcomvvtestsecurehereuftestsecure.glitch.me/Google.html> on - 2. Chrome
- 3. Click anywhere on the page
- 4. A Small window will show up, Click anywhere in Small Window
- 5. A hidden origin PWA Installation Dialog will show up, now Click [Install]

`Result:` Successfully Installed Malicious Application on User Desktop

I have also attached the files used in the PoC - if you prefer, you can reproduce it by downloading and hosting Google.html on a web server.

### dc...@chromium.org (2024-12-18)

While I was attempting to set FoundIn, it appears glitch has deleted the demo page—probably for tripping safe browsing warnings.

### pu...@gmail.com (2024-12-18)

To Reproduce this Issue Please Refer to [#comment2](https://issues.chromium.org/issues/384962294#comment2) I have Updated the link

### pu...@gmail.com (2024-12-18)

> it appears glitch has deleted the demo page

it was not deleted by glitch, it was my mistake I added the wrong link in #1 Sorry for that

### dc...@chromium.org (2024-12-19)

I'm going to tag this with 133, as from my testing, that's the milestone the UX starts featuring the Install button starts appearing in the clipped dialog rather than the (partially elided) origin.

### pe...@google.com (2024-12-19)

Setting milestone because of s2 severity.

### pe...@google.com (2024-12-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### di...@chromium.org (2024-12-19)

Trying to understand the issue here, is the problem here that since the pop up window is small, the dialog is showed with an elided origin string, so the user doesn't know where it got triggered from, like `HalfDialog133.png`?

I think this is reproducible on v133 more often compared to the lower versions, but it is possible to repro in v132 too by making the main Chrome window that triggers the dialog too small.

One naive fix that I can think of is to make sure that the install dialog is always created for its full size, regardless of the size of window it is anchored to. Let me look at that.

### dm...@chromium.org (2024-12-19)

I agree that showing the dialog at full size (requiring the origin & icon being shown) is likely the best fix here. We should be requiring that anyways, as the origin, name, and title are the security sensitive members for apps & need to be shown the user on install.

### di...@google.com (2024-12-20)

Unfortunately, a holistic fix for this is kind of impossible at the moment, owing to limitations of tab modal dialogs and how they interface with the OS. So a fix is possible in some OSes (I think Mac is one of them), but on Windows and Linux we might still need the underlying views/ architecture to start supporting this use-case. It's currently being tracked internally.

As a stopgap fix, we discussed as a team, and we'll abort the installation flow in such a case where the user cannot safely understand what they're installing. I'll be sending out a CL for this soon.

### ap...@google.com (2024-12-20)

Project: chromium/src  

Branch: main  

Author: Dibyajyoti Pal <[dibyapal@google.com](mailto:dibyapal@google.com)>  

Link:      <https://chromium-review.googlesource.com/6112742>

[PWA] Abort installation if PWA dialog occludes security information

---


Expand for full commit details
```
[PWA] Abort installation if PWA dialog occludes security information 
 
If the PWA installation dialog is triggered from a browser window that 
is smaller than intended, the dialog is constrainted to the limits of 
the window, causing important security information like origin to be 
hidden from the user. 
 
This CL introduces a stop gap fix for this use-case by aborting the 
installation by cancelling the dialog if the size of the install 
dialog is smaller than the preferred size. 
 
Until crbug.com/346974105 is fixed, this works as a security patch. 
 
Fixed: 384962294 
Change-Id: I6874695c1c124afaadf1063050863594b721c7d3 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6112742 
Reviewed-by: May Siem <msiem@chromium.org> 
Reviewed-by: Daniel Murphy <dmurph@chromium.org> 
Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1399281}

```

---

Files:

- M `chrome/browser/ui/views/web_apps/web_app_detailed_install_dialog.cc`
- M `chrome/browser/ui/views/web_apps/web_app_diy_install_dialog.cc`
- M `chrome/browser/ui/views/web_apps/web_app_install_dialog_delegate.cc`
- M `chrome/browser/ui/views/web_apps/web_app_install_dialog_delegate.h`
- M `chrome/browser/ui/views/web_apps/web_app_simple_install_dialog.cc`

---

Hash: 721353166352a8b08356c63dd8e4f34a14e62dfb  

Date:  Fri Dec 20 11:06:45 2024


---

### ap...@google.com (2024-12-21)

Project: chromium/src  

Branch: main  

Author: Dibyajyoti Pal <[dibyapal@google.com](mailto:dibyapal@google.com)>  

Link:      <https://chromium-review.googlesource.com/6115671>

[PWA] Tests for simple install dialog occlusion

---


Expand for full commit details
```
[PWA] Tests for simple install dialog occlusion 
 
This CL adds tests for the simple install dialog to: 
1. Automatically close if the browser window becomes too small 
dynamically. 
2. Automatically close if triggered from an already small browser 
window. 
 
Tests for detailed and DIY installed dialog will be submitted in 
separate CLs. 
 
Bug: 384962294 
Change-Id: Idad348904318d60e9a88256957d56df2ecb9cd29 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6115671 
Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org> 
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1399433}

```

---

Files:

- M `chrome/browser/ui/views/web_apps/simple_install_dialog_bubble_view_browsertest.cc`

---

Hash: 444ce6f5729025337fbb8868e54daa3499d6f122  

Date:  Fri Dec 20 16:26:59 2024


---

### pe...@google.com (2024-12-22)

Merge review required: M132 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), alonbajayo (ChromeOS), srinivassista (Desktop)

### ap...@google.com (2024-12-23)

Project: chromium/src  

Branch: main  

Author: Lingqi Chi <[lingqi@chromium.org](mailto:lingqi@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6108527>

Revert "[PWA] Tests for simple install dialog occlusion"

---


Expand for full commit details
```
Revert "[PWA] Tests for simple install dialog occlusion" 
 
This reverts commit 444ce6f5729025337fbb8868e54daa3499d6f122. 
 
Reason for revert: Tests are flaky on Mac 11, 12, 13 
https://ci.chromium.org/ui/p/chromium/builders/ci/Mac11%20Tests/33617/overview 
 
Original change's description: 
> [PWA] Tests for simple install dialog occlusion 
> 
> This CL adds tests for the simple install dialog to: 
> 1. Automatically close if the browser window becomes too small 
> dynamically. 
> 2. Automatically close if triggered from an already small browser 
> window. 
> 
> Tests for detailed and DIY installed dialog will be submitted in 
> separate CLs. 
> 
> Bug: 384962294 
> Change-Id: Idad348904318d60e9a88256957d56df2ecb9cd29 
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6115671 
> Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org> 
> Reviewed-by: Marijn Kruisselbrink <mek@chromium.org> 
> Cr-Commit-Position: refs/heads/main@{#1399433} 
 
Bug: 384962294 
Change-Id: Ifc64bd50e6075ff6397ff9134afa73e1eecd8eb9 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6108527 
Commit-Queue: Lingqi Chi <lingqi@chromium.org> 
Owners-Override: Lingqi Chi <lingqi@chromium.org> 
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
Auto-Submit: Lingqi Chi <lingqi@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1399686}

```

---

Files:

- M `chrome/browser/ui/views/web_apps/simple_install_dialog_bubble_view_browsertest.cc`

---

Hash: c72e0d1b8dfc05c31b6e90be8011bbaeadbab4d3  

Date:  Sun Dec 22 17:40:01 2024


---

### di...@google.com (2024-12-23)

Answer for questions in [#c14](https://g-issues.chromium.org/issues/384962294#comment14)

1. This merge fixes a security issue in the PWA installation dialog which hides origin if the browser window is too small, which might end up fooling the user to install a PWA for a malicious origin.
2. <https://chromium-review.googlesource.com/6112742>
3. Yes
4. No.
5. This seems to be affecting only certain OS platforms, but CrOS doesn't seem to be one of them.
6. Yes, this affects the Stable Channel as well. Testing instructions are in <https://g-issues.chromium.org/issues/384962294#comment2>.

### ap...@google.com (2024-12-23)

Project: chromium/src  

Branch: main  

Author: Dibyajyoti Pal <[dibyapal@google.com](mailto:dibyapal@google.com)>  

Link:      <https://chromium-review.googlesource.com/6119459>

[PWA] Add min bounds for install dialog occlusion security fix

---


Expand for full commit details
```
[PWA] Add min bounds for install dialog occlusion security fix 
 
The previous install dialog occlusion security fix landed as part of 
crbug.com/384962294 prevents the dialog from showing up if the size of 
the dialog is lower than the preferred size. This led to an issue on Mac 
where small changes in the dimensions (like 1 px less), would lead to 
the dialog to be automatically closed. 
 
This CL fixes that by creating a minimum bound that the install dialog 
can still be lowered to based on the sizes of the dialog on various OS 
surfaces, to provide a safe boundary on both sides for testing. 
 
See notes on Mac: https://paste.googleplex.com/6157163219910656#l=10 
 
Bug: 384962294 
Change-Id: I9310d9fe207957ef9daaa6167df72487fe448817 
Fixed: 385652969 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6119459 
Commit-Queue: May Siem <msiem@chromium.org> 
Auto-Submit: Dibyajyoti Pal <dibyapal@chromium.org> 
Reviewed-by: May Siem <msiem@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1399840}

```

---

Files:

- M `chrome/browser/ui/views/web_apps/web_app_install_dialog_delegate.cc`

---

Hash: 5e8d9e95100bb4251ab0530017158248a4ed32ef  

Date:  Mon Dec 23 10:51:15 2024


---

### ap...@google.com (2024-12-23)

Project: chromium/src  

Branch: main  

Author: Dibyajyoti Pal <[dibyapal@google.com](mailto:dibyapal@google.com)>  

Link:      <https://chromium-review.googlesource.com/6120377>

Reland "[PWA] Tests for simple install dialog occlusion"

---


Expand for full commit details
```
Reland "[PWA] Tests for simple install dialog occlusion" 
 
This is a reland of commit 444ce6f5729025337fbb8868e54daa3499d6f122 
 
The test failures are fixed by: 
1. Making the resizing test only work on non-Mac platforms, since 
window resizing does not seem to be working at all on Mac. The 
original use-case on production is also hard to reproduce, as the 
browser windows are hard to make smaller. 
2. Making the test for the popup window being shown be working on 
all platforms using a WebContentsObserver that creates popups. 
 
Original change's description: 
> [PWA] Tests for simple install dialog occlusion 
> 
> This CL adds tests for the simple install dialog to: 
> 1. Automatically close if the browser window becomes too small 
> dynamically. 
> 2. Automatically close if triggered from an already small browser 
> window. 
> 
> Tests for detailed and DIY installed dialog will be submitted in 
> separate CLs. 
> 
> Bug: 384962294 
> Change-Id: Idad348904318d60e9a88256957d56df2ecb9cd29 
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6115671 
> Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org> 
> Reviewed-by: Marijn Kruisselbrink <mek@chromium.org> 
> Cr-Commit-Position: refs/heads/main@{#1399433} 
 
Bug: 384962294 
Change-Id: I7d03839f0b0bbc7b13b955aac3d807ea0e4cd23a 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6120377 
Owners-Override: May Siem <msiem@chromium.org> 
Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org> 
Reviewed-by: May Siem <msiem@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1399880}

```

---

Files:

- M `chrome/browser/ui/views/web_apps/simple_install_dialog_bubble_view_browsertest.cc`

---

Hash: c5341681465608572675731d8d05b8c16ab9165d  

Date:  Mon Dec 23 12:48:39 2024


---

### am...@chromium.org (2024-12-26)

tentatively approving <https://crrev.com/c/6112742> for merge to M132
There is no Canary data showing any issues here, however, since we are in a release freeze and holiday period canary data will be more limited, merging this to 132 Beta at this time will not provide any beta data since we are in release freeze.

132 Stable RC will be cut directly after release freeze; if there are any stability or functional concerns or apprehension with merging this fix, please do not merge and it will go out with 133.
If there are no concerns, please merge this fix to branch 6834 at your earliest convenience / by EOD 2 January 2025.

### di...@google.com (2024-12-27)

@amyressleer@chromium.org we would also need to merge <https://chromium-review.googlesource.com/6119459>, a follow-up CL to fix the dialog auto disappearing on Mac. It's a follow-up to the CL that I requested merge for, and is a tiny follow-up that does not regress the feature.

Can I have your approval on merging that one as well? Without that, the fix doesn't work properly on Mac, and we'll be left with broken install prompts on Mac.

### ap...@google.com (2024-12-27)

Project: chromium/src  

Branch: main  

Author: Dibyajyoti Pal <[dibyapal@google.com](mailto:dibyapal@google.com)>  

Link:      <https://chromium-review.googlesource.com/6120717>

[PWA] Fix popup resizing test for simple install dialog

---


Expand for full commit details
```
[PWA] Fix popup resizing test for simple install dialog 
 
This CL fixes the resizing test for simple install dialogs to now work 
on Mac as well using the same popup watching logic added in 
crrev.com/c/6120377. 
 
Bug: 384962294 
Change-Id: If176427fed94f8ff66ca6c7587ff52bc13b5db48 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6120717 
Reviewed-by: May Siem <msiem@chromium.org> 
Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1400503}

```

---

Files:

- M `chrome/browser/ui/views/web_apps/simple_install_dialog_bubble_view_browsertest.cc`

---

Hash: 53ab105e66f83c411384c2fa60fa8d952953623e  

Date:  Fri Dec 27 07:51:10 2024


---

### am...@chromium.org (2024-12-27)

yes, please also backmerge <https://crrev.com/c/6119459> for Mac at this time since <https://crrev.com/c/6120717> has now been backmerged

### di...@google.com (2024-12-27)

Oh the landed CL isn't a backmerge, but a test for the fixes included this CL. Thanks for the approval, I'll land them together in a single cherry-picked CL to M132: <https://chromium-review.googlesource.com/c/chromium/src/+/6123602>

### ap...@google.com (2024-12-27)

Project: chromium/src  

Branch: refs/branch-heads/6834  

Author: Dibyajyoti Pal <[dibyapal@google.com](mailto:dibyapal@google.com)>  

Link:      <https://chromium-review.googlesource.com/6123602>

[PWA/M132] Abort installation if PWA dialog occludes security info

---


Expand for full commit details
```
[PWA/M132] Abort installation if PWA dialog occludes security info 
 
This is a cherry-pick of crrev.com/c/6119459 and crrev.com/c/6112742, 
being landed into M132. Merge approval is in linked bug. 
 
If the PWA installation dialog is triggered from a browser window that 
is smaller than intended, the dialog is constrainted to the limits of 
the window, causing important security information like origin to be 
hidden from the user. 
 
This CL introduces a stop gap fix for this use-case by aborting the 
installation by cancelling the dialog if the size of the install 
dialog is smaller than the preferred size. 
 
Until crbug.com/346974105 is fixed, this works as a security patch. 
 
(cherry picked from commit 721353166352a8b08356c63dd8e4f34a14e62dfb) 
 
Fixed: 384962294 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6112742 
Reviewed-by: May Siem <msiem@chromium.org> 
Reviewed-by: Daniel Murphy <dmurph@chromium.org> 
Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1399281} 
Change-Id: I955deff638b646841471c6f67b46db0436406c15 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6123602 
Reviewed-by: Alvin Ji <alvinji@chromium.org> 
Reviewed-by: Zelin Liu <zelin@chromium.org> 
Auto-Submit: Dibyajyoti Pal <dibyapal@chromium.org> 
Commit-Queue: Alvin Ji <alvinji@chromium.org> 
Owners-Override: Dibyajyoti Pal <dibyapal@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6834@{#2839} 
Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `chrome/browser/ui/views/web_apps/web_app_detailed_install_dialog.cc`
- M `chrome/browser/ui/views/web_apps/web_app_diy_install_dialog.cc`
- M `chrome/browser/ui/views/web_apps/web_app_install_dialog_delegate.cc`
- M `chrome/browser/ui/views/web_apps/web_app_install_dialog_delegate.h`
- M `chrome/browser/ui/views/web_apps/web_app_simple_install_dialog.cc`

---

Hash: 56051895181268452d6e00a75955edb9100e7e36  

Date:  Fri Dec 27 13:02:01 2024


---

### pe...@google.com (2024-12-27)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### di...@google.com (2024-12-27)

Answers to Q#25:

1. Not sure. I do not have a ChromeOS M126 device to test. The dialog in question is available on CrOS from [M128 onwards it seems](https://chromiumdash.appspot.com/commit/9ebd36b234c4ff0d67f203dae0311ccd539f8378), so there is a chance this bad behavior could be there on CrOS. The behavior should be fixed for all platforms though as per the new CLs.
2. As seen from [this commit](https://chromiumdash.appspot.com/commit/9ebd36b234c4ff0d67f203dae0311ccd539f8378), the dialog this is being seen in is available from M128 onwards on CrOS, as part of the universal install launch.

### ap...@google.com (2024-12-27)

Project: chromium/src  

Branch: main  

Author: msiem <[msiem@chromium.org](mailto:msiem@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6120207>

[PWA]: Test for diy install dialog occlusion

---


Expand for full commit details
```
[PWA]: Test for diy install dialog occlusion 
 
This CL tests diy installation dialogs for 2 use cases: 
1: DIY installation dialog closes automatically if triggered in a 
new browser window that has been shortened. 
2: DIY installation dialog does not show up if triggered from a 
browser window that is very short. 
 
Refactored OpenPopupOfSize() into a utils class to lower the size 
of a popup browser that would be suitable for these two tests. 
 
Bug: 385392038, 384962294 
Change-Id: I4b1195dcca5ba5797f74836d86d1f492b7e99a8d 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6120207 
Reviewed-by: Dibyajyoti Pal <dibyapal@chromium.org> 
Commit-Queue: May Siem <msiem@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1400584}

```

---

Files:

- M `chrome/browser/ui/views/web_apps/simple_install_dialog_bubble_view_browsertest.cc`
- A `chrome/browser/ui/views/web_apps/web_app_dialog_test_utils.cc`
- A `chrome/browser/ui/views/web_apps/web_app_dialog_test_utils.h`
- M `chrome/browser/ui/views/web_apps/web_app_diy_install_dialog_browsertest.cc`
- M `chrome/test/BUILD.gn`

---

Hash: 2076438e7bf681437a49b2ef07fabd66c6296d89  

Date:  Fri Dec 27 13:53:08 2024


---

### ap...@google.com (2024-12-30)

Project: chromium/src  

Branch: main  

Author: msiem <[msiem@chromium.org](mailto:msiem@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6127335>

[PWA]: Test for detailed install dialog occlusion

---


Expand for full commit details
```
[PWA]: Test for detailed install dialog occlusion 
 
This CL tests detailed installation dialogs for 2 use cases: 
1: Detailed installation dialog closes automatically if triggered in a 
new browser window that has been shortened. 
2: Detailed installation dialog does not show up if triggered from a 
browser window that is very short. 
 
Bug: 385391973, 384962294 
Change-Id: If2e80c1819b03dcc85ed7e2f978039a6c7b139e6 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6127335 
Reviewed-by: Dibyajyoti Pal <dibyapal@chromium.org> 
Commit-Queue: May Siem <msiem@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1400947}

```

---

Files:

- M `chrome/browser/ui/views/web_apps/web_app_detailed_install_dialog_browsertest.cc`

---

Hash: cc2f30ece80eaf665ea1a53732e408a7df62d8a8  

Date:  Mon Dec 30 09:58:19 2024


---

### qk...@google.com (2025-01-02)

Labeling as LTS-NotApplicable-126 because of some reasons. First of all, M126 LTS didn't enable `WebAppUniversalInstall` feature. So, it looks like the behavior couldn't happen on M126 LTS. Besides, there seems a side effect possibility because merging back the fix[1] requires dependent patches like [2]. So I think it would be good not to merge back the fix to M126 LTS.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/6123602
[2] https://chromium-review.googlesource.com/c/chromium/src/+/5689758

### sp...@google.com (2025-01-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
report of lower impact security UI issue 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-17)

Congratulations! Thank you for your efforts and reporting this issue to us.

### pu...@gmail.com (2025-01-19)

Thanks for the reward Really appreciate it.

### ch...@google.com (2025-03-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact security UI issue

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/384962294)*

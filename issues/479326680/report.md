# Incorrect Origin Display in PWA Install Prompt When Using RTL Characters

| Field | Value |
|-------|-------|
| **Issue ID** | [479326680](https://issues.chromium.org/issues/479326680) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>WebAppInstalls |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | me...@google.com |
| **Created** | 2026-01-28 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

Chrome Mac - Incorrect Origin Display in PWA Install Prompt When Using RTL Characters

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

Summary

When a domain containing RTL (Right-to-Left) Unicode characters is used, the PWA install prompt displays an incorrect and misleading origin. Instead of showing the real origin "<https://summa.sbs>", the install UI renders it as "<https://xn--mgb.google.com>", causing a reversal and reordering of the hostname. This results in origin confusion during a high-trust installation flow.

Steps to Reproduce

1. Open the POC URL in the Chrome MacOS - <https://xn--mgb.google.com.xn--mgb.yen.summa.sbs/webapp.html>
2. Trigger the PWA install prompt.
3. Observe the origin displayed in the install UI,App Info and Uninstall prompt

Expected Result

The install prompt should display the canonical, correctly ordered punycode origin: <https://xn--mgb.google.com.xn--mgb.yen.summa.sbs>

Actual Result

The install prompt displays a visually reordered and misleading origin: <https://yen.summa.sbs.xn--mgb.google.com.xn--mgb>
This misrepresentation makes the origin appear related to a trusted domain.

#### Impact analysis

This issue enables origin spoofing during the PWA installation flow, where users rely heavily on the displayed origin to make trust decisions. An attacker can craft a malicious PWA using RTL characters to visually impersonate a trusted brand and trick users into installing it. Once installed, the PWA runs in a standalone, address-bar-less context, increasing the risk of credential phishing, persistent UI deception, and long-term user compromise. The impact is amplified because installation is a one-time trust action with lasting consequences.

---

### The cause

#### What version of Chrome have you found the security issue in?

144.0.7559.110 (Official Build) (arm64)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Security UI Spoofing

#### How would you like to be publicly acknowledged for your report?

Barath Stalin K( <https://in.linkedin.com/in/barathstalin>)

## Attachments

- [Chrome PWA.mov](attachments/Chrome PWA.mov) (video/quicktime, 23.3 MB)
- [manifest.json](attachments/manifest.json) (application/json, 377 B)
- [webapp.html](attachments/webapp.html) (text/html, 2.1 KB)

## Timeline

### me...@google.com (2026-01-28)

Thanks for the report. Marking as medium severity because the omnibox is still visible when the install dialog is displayed.

mek@: Could you please take a look?

### di...@google.com (2026-01-28)

This is not just a Mac issue, but is seen on all OSes. There are a few issues here, based on the linked video:

1. Issue happening on PWA specific dialogs (like the install and uninstall dialog).
2. The url being shown on the page info dialog, triggered by clicking on App Info on the three dot menu.

Option 1 is being fixed via [crrev.com/c/7528915](https://crrev.com/c/7528915).

Option 2 is a bit complicated, because clicking on it shows the page info dialog. The text on the menu item is [set here](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/web_applications/web_app_menu_model.cc;l=163-165;bpv=1;bpt=1?q=WebAppMenuModel), and the url shown on the Page info dialog seems to be coming from the [NavigationEntry's virtual url](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/page_info/page_info_dialog.cc;l=40;drc=ab82920fc7ca2ba11aeb69a6552d09c6f6ca6ea5). Currently, both strings being shown are in sync, and I'm a little hesitant updating the string in the three dot menu but not changing the `page_info_dialog` behavior, as that would mean that the UX state on Chrome vs in the three dot menu will be out of sync. Changing the `page_info_dialog`, while trivial, might have more repurcussions, considering how that dialog is used in a lot of places like permissions, so that requires more updating.

@me...@google.com I see you're listed as one of the OWNERs of the page\_info code. Since you also helped triage this bug, do you think applying some form of security consideration, like `FormatUrlForSecurityDisplay()` [1] to the url shown in the page info bubble is a reasonable ask? There are some problems with the API I shared, which is [shared in this comment](https://source.chromium.org/chromium/chromium/src/+/main:components/url_formatter/elide_url.h;l=67-69?q=FormatUrlForSecurityDisplay) and we ran into [some time back](https://g-issues.chromium.org/issues/41487317).

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/url_formatter/elide_url.h;l=62-85?q=elide_url.h>

### dx...@google.com (2026-01-29)

Project: chromium/src  

Branch:  main  

Author:  Dibyajyoti Pal [dibyapal@google.com](mailto:dibyapal@google.com)  

Link:    <https://chromium-review.googlesource.com/7528915>

[PWA] Properly show origin on PWA dialogs

---


Expand for full commit details
```
     
    This CL updates the core logic of showing the origin on PWA dialogs to 
    use FormatOriginForSecurityDisplay() to align with user expectations of 
    showing the correct origin during PWA install and uninstall flows. 
     
    The API was being used as part of crbug.com/41487317, and this code 
    ensures that the behavior in that bug has not regressed. 
     
    See working screenshot: 
    https://screenshot.googleplex.com/7YKWHSnashCmve9 
     
    Bug: 479326680 
    Change-Id: I56d90b0d865b9ab4de3588d3abaccc05e26e915b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7528915 
    Reviewed-by: Marijn Kruisselbrink <mek@chromium.org> 
    Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1576324}

```

---

Files:

- M `chrome/browser/ui/views/web_apps/web_app_detailed_install_dialog.cc`
- M `chrome/browser/ui/views/web_apps/web_app_views_utils.cc`

---

Hash: [c56adc23de79b812f9e13b1cf37b22c25f945f6a](https://chromiumdash.appspot.com/commit/c56adc23de79b812f9e13b1cf37b22c25f945f6a)  

Date: Thu Jan 29 02:22:00 2026


---

### ch...@google.com (2026-01-29)

Setting milestone because of s2 severity.

### ch...@google.com (2026-01-30)

Merge review required: M145 has already been cut for stable release.

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
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### di...@google.com (2026-01-30)

1. For Chrome Browser, this solves an important security issue where the PWA dialog would show the origin incorrectly while using RTL characters.
2. <https://chromiumdash.appspot.com/commit/c56adc23de79b812f9e13b1cf37b22c25f945f6a>
3. They haven't launched on Canary yet it seems.
4. It's not a new feature.
5. Doesn't need CrOS end prod approval.
6. Manual verification steps are in the description of the bug. Basically:
   - Go to <https://xn--mgb.google.com.xn--mgb.yen.summa.sbs/webapp.html>.
   - Click on the install button from the omnibox.
   - Verify that the origin `xn--mgb.google.com.xn--mgb.yen.summa.sbs` is shown instead of anything else.

### dr...@chromium.org (2026-02-02)

Given the severity of S2, I don't think this should be merged to Stable. Let me know if there's something unusually severe about this bug, which would make us reconsider the merge.

### di...@google.com (2026-02-02)

Thanks for the review drubery@. The PWA team's work here is then done. Assigning to @me...@google.com for next steps, as per [#comment3](https://issues.chromium.org/issues/479326680#comment3).

### se...@gmail.com (2026-02-04)

Attaching POC files, Kindly check. Please let me know if any additional information is needed from my side.

### me...@chromium.org (2026-02-04)

dipyapal: Sorry for the delay. FormatUrlForSecurityDisplay() would be the right choice here, but I'm surprised it doesn't handle RTL URLs. Is that still the case, regardless of its documentation?

### di...@google.com (2026-02-04)

Yep, it doesn't handle RTL urls. We had a regression in our dialog code earlier due to this: <https://g-issues.chromium.org/issues/41487317>

### ch...@google.com (2026-02-17)

meacer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### me...@google.com (2026-02-25)

I have a fix for the page info issue at <https://chromium-review.git.corp.google.com/c/chromium/src/+/7608472>

### dx...@google.com (2026-02-27)

Project: chromium/src  

Branch:  main  

Author:  Mustafa Emre Acer [meacer@chromium.org](mailto:meacer@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7608472>

Render RTL URLs properly in the PWA page info menu

---


Expand for full commit details
```
     
    The PWA page info menu renders the App's origin as a minor text next 
    to the "App Info" menu item. Presently, this doesn't handle RTL 
    hostnames correctly. This CL fixes that by forcing directionality to 
    LTR. 
     
    Bug: 479326680 
    Change-Id: I421e2886e21dbdb9a8e8b298e3cebaa8de49955f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7608472 
    Reviewed-by: Dibyajyoti Pal <dibyapal@chromium.org> 
    Reviewed-by: Dana Fried <dfried@chromium.org> 
    Commit-Queue: Mustafa Emre Acer <meacer@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1591194}

```

---

Files:

- M `chrome/browser/ui/web_applications/web_app_menu_model.cc`
- M `ui/base/models/menu_model.cc`
- M `ui/base/models/menu_model.h`
- M `ui/menus/simple_menu_model.cc`
- M `ui/menus/simple_menu_model.h`
- M `ui/views/controls/menu/menu_item_view.cc`
- M `ui/views/controls/menu/menu_item_view.h`
- M `ui/views/controls/menu/menu_model_adapter.cc`

---

Hash: [637553f660ab74b759bc6848935df2a133311fab](https://chromiumdash.appspot.com/commit/637553f660ab74b759bc6848935df2a133311fab)  

Date: Fri Feb 27 00:49:26 2026


---

### ch...@google.com (2026-02-27)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-06-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. Security UI Spoofing.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/479326680)*

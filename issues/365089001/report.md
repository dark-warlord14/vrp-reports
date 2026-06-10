# Select Option can be opened on top of Popups with Different Origins and can be used to Spoof important Security Prompts

| Field | Value |
|-------|-------|
| **Issue ID** | [365089001](https://issues.chromium.org/issues/365089001) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>Select |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2024-09-06 |
| **Bounty** | $2,000.00 |

## Description

#### SUMMARY

The Select option can be opened on popup with a different origin than the one that initiated it, which is simialr to the issue documented at <https://issues.chromium.org/issues/41494315> (POC-1).

This issue also demonstrates different exploitation methods similar to <https://issues.chromium.org/issues/342194497>, where the permission prompt UI can be concealed (POC-2 and POC-3).

#### VULNERABILITY DETAILS

A malicious website can open a Select option on top of another website with an arbitrary origin via a popup, including trusted domains like google.com.

This allows the malicious website to display any text within the Select option on top of the opened popup.

The issue can be further exploited by opening a different permission or security prompt in this popup and hiding it with the Select option.

Below I have demonstrated this in three proof-of-concept files:

1. `poc-1.html`: Demonstrates that the Select option can appear on top of an origin like google.com.
2. `poc-2.html` and `poc-3.html`: Shows how the Select option can be used to cover the permission/security UI opened using a popup from a different website.

#### VERSION

- Chrome Version:
  
  - 130.0.6701.0 (Official Build) Canary (64-bit)
  - 128.0.6613.120 (Official Build) (64-bit) Stable
- Operating System: Windows 11

#### REPRODUCTION CASE

**POC-1:**

1. Download the attached `poc-1.html` file.
2. Host the page on a local server or open `poc-1.html` directly from the folder.
3. Visit the webpage using the latest Chrome browser.
4. Double-click on the website.
5. Observe that the Select option appears over a different origin opened as a popup.

**POC-2:**

1. Download the attached `poc-2.html` and `permission.html` files.
2. Host the page on a local server or open `poc-2.html` directly from the folder.
3. Visit the webpage using the latest Chrome browser.
4. Double-click on the website.
5. The Select option will request you to press Tab three times, then Enter to continue. Doing so will allow the hidden permission tab to proceed.

**POC-3:**

1. Download the attached `poc-3.html` and `permission.html` files.
2. Host the page on a local server or open `poc-3.html` directly from the folder.
3. Visit the webpage using the latest Chrome browser.
4. Double-click on the website.
5. The permission prompt from the popup window is concealed by the Select option, thus spoofing the user interface.

**Observed:**

The Select option can open on top of a different website via a popup, rather than being on the initiated page, thus allowing malicious websites to spoof other sites or security prompts. This can be exploited to obtain permissions without the user’s awareness.

**Expected:**

The Select option should not open on top of popups. It should strictly be tied to the opened website, and when popup is focused chrome should not allow the Select option to be placed on top of it.

#### CREDIT INFORMATION

Reporter credit: Shaheen Fazim

## Attachments

- [poc-1.html](attachments/poc-1.html) (text/html, 1.3 KB)
- [poc-2.html](attachments/poc-2.html) (text/html, 1.9 KB)
- [poc-3.html](attachments/poc-3.html) (text/html, 1.6 KB)
- [permission.html](attachments/permission.html) (text/html, 1.7 KB)
- [repro-1.mp4](attachments/repro-1.mp4) (video/mp4, 695.7 KB)
- [repro-2.mp4](attachments/repro-2.mp4) (video/mp4, 1.7 MB)
- [repro-3.mp4](attachments/repro-3.mp4) (video/mp4, 1.7 MB)
- [test-firefox.mp4](attachments/test-firefox.mp4) (video/mp4, 818.4 KB)
- [Screenshot 2024-11-13 at 1.25.06 PM.png](attachments/Screenshot 2024-11-13 at 1.25.06 PM.png) (image/png, 684.8 KB)

## Timeline

### aj...@google.com (2024-09-08)

CC some folks and assign to person that reviewed much of the showpicker code.

This seems like a reasonable spoof where the showpicker allows drawing over other windows.

### aj...@google.com (2024-09-08)

Assuming this affects deskop-type OSes - please expand OS field if necessary.
Setting Medium severity as pocs demonstrate reasonable control of popped over content.

### aj...@google.com (2024-09-08)

possibly relates to [issue 41494653](https://issues.chromium.org/issues/41494653)

### pe...@google.com (2024-09-08)

Setting milestone because of s2 severity.

### pe...@google.com (2024-09-08)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ma...@chromium.org (2024-09-10)

First, very nice proofs of concept, thanks for that.

But if I understand this exploit, it is nothing more than the fact that <select> (without `appearance:base-select`) can display outside the bounds of the renderer it comes from. (Which is a dupe of [crbug.com/41494315](https://crbug.com/41494315).) This is precisely why it requires user activation before `showPicker()` does anything.

I'm not sure there's a workaround or "fix" for this bug. Are there suggestions for a mitigation?

### fa...@gmail.com (2024-09-11)

Is it possible to close the select option when a different window is focused? When testing this issue with Firefox, I believe they are just closing the dialogue. but I'm not sure about the implementation.

These changes are probably new in Firefox (<https://issues.chromium.org/issues/41494315#comment15>). I have also helped and reported a few security issues with the select option to Firefox, which might have fixed this issue in their browser.

### pe...@google.com (2024-09-25)

masonf: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-10-18)

masonf: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-11-04)

Project: chromium/src  

Branch: main  

Author: Mason Freed <[masonf@chromium.org](mailto:masonf@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5909884>

Don't show popups (e.g. <select>) if the tab isn't focused

---


Expand for full commit details
```
Don't show popups (e.g. <select>) if the tab isn't focused 
 
It was previously possible for pickers like <select>'s picker to be 
shown on top of the not-currently-focused tab, confusing the user. 
With this change, the select picker must be the currently-focused 
tab for the picker to be opened. This is akin to existing protections 
for the tab being visible. 
 
Fixed: 365089001 
Change-Id: Id2b15f5d310cce877341d7e9d5a5c5d6da882887 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5909884 
Reviewed-by: Alexander Timin <altimin@chromium.org> 
Commit-Queue: Mason Freed <masonf@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1377731}

```

---

Files:

- M `content/browser/web_contents/web_contents_impl.cc`
- M `content/browser/web_contents/web_contents_impl.h`
- M `content/browser/web_contents/web_contents_impl_browsertest.cc`
- M `content/common/content_switches_internal.cc`
- M `content/common/content_switches_internal.h`
- M `content/public/test/browser_test_base.cc`
- M `content/renderer/render_thread_impl.cc`
- M `content/web_test/browser/web_test_browser_main_runner.cc`
- M `third_party/blink/web_tests/inspector-protocol/emulation/select-popup-auto-dark-mode.js`

---

Hash: 9a7e491a5c91e9a42b78e2ac3fc444c534ba2456  

Date:  Mon Nov 04 17:33:17 2024


---

### ap...@google.com (2024-11-12)

Project: chromium/src  

Branch: main  

Author: Mason Freed <[masonf@chromium.org](mailto:masonf@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6012850>

Revert "Don't show popups (e.g. <select>) if the tab isn't focused"

---


Expand for full commit details
```
Revert "Don't show popups (e.g. <select>) if the tab isn't focused" 
 
This reverts commit 9a7e491a5c91e9a42b78e2ac3fc444c534ba2456. 
 
Reason for revert: Seems to have caused an extensions issue: https://issues.chromium.org/issues/377830108 
 
Original change's description: 
> Don't show popups (e.g. <select>) if the tab isn't focused 
> 
> It was previously possible for pickers like <select>'s picker to be 
> shown on top of the not-currently-focused tab, confusing the user. 
> With this change, the select picker must be the currently-focused 
> tab for the picker to be opened. This is akin to existing protections 
> for the tab being visible. 
> 
> Fixed: 365089001 
> Change-Id: Id2b15f5d310cce877341d7e9d5a5c5d6da882887 
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5909884 
> Reviewed-by: Alexander Timin <altimin@chromium.org> 
> Commit-Queue: Mason Freed <masonf@chromium.org> 
> Cr-Commit-Position: refs/heads/main@{#1377731} 
 
Change-Id: I94470d6e18b3393c0c9b814439bda5c61aad5565 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6012850 
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
Auto-Submit: Mason Freed <masonf@chromium.org> 
Reviewed-by: Joey Arhar <jarhar@chromium.org> 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Commit-Queue: Alex Moshchuk <alexmos@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1381534}

```

---

Files:

- M `content/browser/web_contents/web_contents_impl.cc`
- M `content/browser/web_contents/web_contents_impl.h`
- M `content/browser/web_contents/web_contents_impl_browsertest.cc`
- M `content/common/content_switches_internal.cc`
- M `content/common/content_switches_internal.h`
- M `content/public/test/browser_test_base.cc`
- M `content/renderer/render_thread_impl.cc`
- M `content/web_test/browser/web_test_browser_main_runner.cc`
- M `third_party/blink/web_tests/inspector-protocol/emulation/select-popup-auto-dark-mode.js`

---

Hash: e379c4f2c9a4d37e15322655cf399186cc9a42c3  

Date:  Tue Nov 12 01:22:10 2024


---

### ma...@chromium.org (2024-11-13)

This might not be fixable in the way I was hoping, due to web compat. Not sure what to do otherwise.

### ma...@chromium.org (2024-11-13)

For those with access who might work on this in the future, also see [b/377832158](https://issues.chromium.org/issues/377832158).

### ct...@chromium.org (2024-11-13)

Reading through [b/377832158](https://issues.chromium.org/issues/377832158) it sounds like the issue was due to the <select> element being in an iframe and the *iframe* WebContents not having focus. I *think* that's the same issue as in [Issue 377830108](https://issues.chromium.org/issues/377830108) (see attached screenshot for my attempt to sleuth at how this extension provided options view is rendered -- it appears to be an iframe). Could we instead implement the restriction on the overall top level tab? As a very rough straw proposal, could we do the check something like this:

```
WebContents* top_level_wc = wc->GetOutermostWebContents();
if (!top_level_wc->ContainsOrIsFocusedWebContents()) {
  // Nothing in tab is focused, prevent opening select.
}

```

My understanding is this differs from the solution in [crrev.com/5237056](https://crrev.com/5237056) ("Don't create popups for hidden tabs") because the backgrounded tab is still *visible* it just no longer has focus because the popup has stolen focus and is rendered on top. Maybe the real check we need is an "is occluded" to be a bit more precise than "is visible" or "is focused" -- that is, maybe we'd be okay with showing the <select> popup in an unfocused window as long as it is not being occluded by anything.

Or, could we fix the Z-ordering issue here entirely, which seems like the root cause? That is, if we could render the <select> popup but have it pinned *between* the originating window and the popup window, then that is the most "correct" solution potentially. Actually fixing z-ordering issues can be challenging and platform-dependent I think though.

Assigning back to masonf@ as we require that all security vulnerabilities have assigned owners -- happy to help find an alternative owner if you are no longer working in this area though.

### fa...@gmail.com (2025-01-21)

Hi masonf@, can we update on this issue.

### fa...@gmail.com (2025-04-09)

deleted

### ma...@chromium.org (2026-01-21)

jarhar@ since this is <select> related, can I assign this one to you, at least to re-triage?

### ja...@chromium.org (2026-02-05)

I would have thought that using window.open() would have consumed any user activation and therefore a subsequent call to select.showPicker() would fail due to the user activation check, but I guess that's not the case. I'm not sure if I should change how user activation works with window.open(), so I'll try the suggestion in comment 15

### ja...@chromium.org (2026-02-05)

I tried using GetOutermostWebContents()->ContainsOrIsFocusedWebContents() in WebContentsImpl::ShowCreatedWidget, but it was returning true, indicating that the web contents or something in the tree of webcontents is focused after opening another window with window.open(). Maybe there is some way to find the webcontents of the window opened via window.open()? If we can find an opened webcontents, then we could also intersect with it like this if looking at focus doesn't work out: <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;l=5740-5748;drc=02b865d712cf3aa473d8c9aedbaa481bc1d7e60b>

### dx...@google.com (2026-02-26)

Project: chromium/src  

Branch:  main  

Author:  Joey Arhar [jarhar@chromium.org](mailto:jarhar@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7595027>

Prevent select popup from opening when window isn't focused

---


Expand for full commit details
```
     
    This prevents the popup document for the select element from being 
    opened if the corresponding OS window is not focused. 
     
    This change resulted in a DevTools test failing, probably because the OS 
    window is not active during the test. In order to resolve this, I 
    migrated the test from web_tests to a C++ test. 
     
    Fixed: 365089001 
    Change-Id: I1ad871f442f9ec861952d1655c44dc21cb588b2e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7595027 
    Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    Reviewed-by: Joey Arhar <jarhar@chromium.org> 
    Commit-Queue: Joey Arhar <jarhar@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1590893}

```

---

Files:

- M `content/browser/web_contents/web_contents_impl.cc`
- M `content/browser/web_contents/web_contents_impl_browsertest.cc`
- M `third_party/blink/renderer/core/html/forms/internal_popup_menu.h`
- M `third_party/blink/renderer/core/html/forms/internal_popup_menu_test.cc`
- M `third_party/blink/renderer/platform/runtime_enabled_features.json5`
- D `third_party/blink/web_tests/inspector-protocol/emulation/select-popup-auto-dark-mode.js`
- D `third_party/blink/web_tests/platform/linux/inspector-protocol/emulation/select-popup-auto-dark-mode-expected.txt`
- D `third_party/blink/web_tests/platform/mac/inspector-protocol/emulation/select-popup-auto-dark-mode-expected.txt`
- D `third_party/blink/web_tests/platform/win/inspector-protocol/emulation/select-popup-auto-dark-mode-expected.txt`

---

Hash: [a84fff044ccd66f54127fc1ba1239524851711a5](https://chromiumdash.appspot.com/commit/a84fff044ccd66f54127fc1ba1239524851711a5)  

Date: Thu Feb 26 17:25:45 2026


---

### ch...@google.com (2026-02-26)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-02-26)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-06-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-08)

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
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/365089001)*

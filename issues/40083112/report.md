# Security: Inline extension installation dialog doesn't block and persists after redirect

| Field | Value |
|-------|-------|
| **Issue ID** | [40083112](https://issues.chromium.org/issues/40083112) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **CVE IDs** | CVE-2016-1640 |
| **Reporter** | he...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2015-11-01 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

This vulnerability makes it possible to display an inline extension installation dialog on a different origin that initiated the install. Thus tricking the user into installing an Extension as if it was from that origin. As the dialog doesn't show the origin, it gives even more credibility to the attack.

**VERSION**  

Chrome Version: [46.0.2490.80 m] + [stable].

**REPRODUCTION CASE**

1. Download index.html
2. Change de ID of the extension to your extension's ID.
3. Open index.html and click on the link.

\* Given I don't have an extension capable of inline installation I can't set up a page for this PoC. But you can download the PoC and test it yourself (if you have an extension).

Here is a video simulating the attack:  

<https://www.youtube.com/watch?v=f_9ObDqBoo8>

## Attachments

- [index.html](attachments/index.html) (text/html, 448 B)
- [bug.png](attachments/bug.png) (image/png, 124.3 KB)

## Timeline

### me...@chromium.org (2015-11-02)

Repro: go/crbug_550047

We have https://crbug.com/chromium/416977 open to display the origin, and we are planning to redesign the dialog. Would be good to fix this one in the meanwhile. Assigning medium severity since there is no origin on the dialog, and the end result is potentially dangerous.

Antony, can you please take a look or reassign? Thanks.

### as...@chromium.org (2015-11-02)

I can take ownership of implementing a fix. 

Mustafa - likely the easiest thing to do is to kill the dialog when we navigate away from the frame where chrome.webstore.install was called to initiate the install - does that sound like a reasonable mitigation?

If not we can investigate changing the dialog title or contents to mention the origin.  This is probably not technically challenging but would be slower to roll out since it probably requires getting some PM/designer review on wording, and can't be merged into release branches because of the need to get translations. 




### me...@chromium.org (2015-11-02)

> Mustafa - likely the easiest thing to do is to kill the dialog when we navigate away from the frame where chrome.webstore.install was called to initiate the install - does that sound like a reasonable mitigation?

Sure, that sounds good to me. ainslie@ is helping with the redesign so you don't have to worry about that for now :)

### as...@chromium.org (2015-11-05)

CC'ing Devlin since I just sent him a CL for fixing this. 


### as...@chromium.org (2015-11-20)

Fix on its way through commit queue: https://codereview.chromium.org/1403293008/


### as...@chromium.org (2015-11-21)

By the way, killing the dialog entirely turned out to be more complicated than I'd hoped, so I opted for a more expedient strategy of just leaving the dialog up but making hitting the "ok" button turn into a no-op. This isn't the greatest user experience, but users shouldn't hit it under normal circumstances so it seemed better to get a fix out soon.


### me...@chromium.org (2015-11-21)

Thanks for the update Antony!

### he...@gmail.com (2015-11-21)

Could someone check if the code below would be stopped by this fix?
As it is opening a new tab and not redirecting the page that started the install I think this will still work.

<a href="javascript:window.open('https://support.google.com/installer/answer/98805?hl=en')" onclick="chrome.webstore.install()" id="install-link">Click here to check the newest Google Update.</a>

* For some reason, the dialog appears in the middle of the screen when the install is initiated using the code above.

### as...@chromium.org (2015-11-21)

@8 - great catch, my patch doesn't stop this modified attack you've described

I'll start working on an improvement - I wonder if we need to make the dialog modal to the tab or something like that. 


### bu...@chromium.org (2015-11-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bbe84115d3dc969bfcf6ca87bebd1f5608db6ecf

commit bbe84115d3dc969bfcf6ca87bebd1f5608db6ecf
Author: asargent <asargent@chromium.org>
Date: Mon Nov 23 23:40:07 2015

Don't allow inline install if frame is deleted before user accepts

If the frame that called the chrome.webstore.install method to begin an
inline install gets deleted before the user accepts from the dialog, we
don't want the install to continue because a navigation could make it
look like the install request was coming from some unrelated site.

One downside of this approach is that the dialog stays around even after
the frame is deleted, and hitting either accept or cancel buttons both
just cancel the install. It would be better if the dialog is
automatically cancelled, but doing that would involve a lot more
refactoring. The approach in this CL was easier and is probably worth
getting out, and we can improve on it in the future.

BUG=550047

Review URL: https://codereview.chromium.org/1403293008

Cr-Commit-Position: refs/heads/master@{#361218}

[modify] http://crrev.com/bbe84115d3dc969bfcf6ca87bebd1f5608db6ecf/chrome/browser/extensions/tab_helper.cc
[modify] http://crrev.com/bbe84115d3dc969bfcf6ca87bebd1f5608db6ecf/chrome/browser/extensions/webstore_inline_installer.cc
[modify] http://crrev.com/bbe84115d3dc969bfcf6ca87bebd1f5608db6ecf/chrome/browser/extensions/webstore_inline_installer.h
[modify] http://crrev.com/bbe84115d3dc969bfcf6ca87bebd1f5608db6ecf/chrome/browser/extensions/webstore_inline_installer_browsertest.cc
[modify] http://crrev.com/bbe84115d3dc969bfcf6ca87bebd1f5608db6ecf/chrome/browser/extensions/webstore_inline_installer_factory.cc
[modify] http://crrev.com/bbe84115d3dc969bfcf6ca87bebd1f5608db6ecf/chrome/browser/extensions/webstore_inline_installer_factory.h
[modify] http://crrev.com/bbe84115d3dc969bfcf6ca87bebd1f5608db6ecf/chrome/browser/extensions/webstore_inline_installer_unittest.cc
[add] http://crrev.com/bbe84115d3dc969bfcf6ca87bebd1f5608db6ecf/chrome/test/data/extensions/api_test/webstore_inline_install/empty.html


### as...@chromium.org (2015-11-23)

FYI the patch that just landed is the one I mentioned in https://crbug.com/chromium/550047#c5. I'm still working on an additional fix for the different scenario mentioned in https://crbug.com/chromium/550047#c8. 


### as...@chromium.org (2015-12-04)

New patch is up for review which makes the dialog modal to the tab where the request is made, and should fix the 'window.open' attack:

https://codereview.chromium.org/1496033003/


### as...@chromium.org (2015-12-07)

+cc finnur since I'm adding him as a reviewer for one of the files in the CL in just a moment

### bu...@chromium.org (2015-12-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0a1c15fecb1240ab909e1431b6127410c3b380e0

commit 0a1c15fecb1240ab909e1431b6127410c3b380e0
Author: asargent <asargent@chromium.org>
Date: Wed Dec 09 02:25:21 2015

Make the webstore inline install dialog be tab-modal

Also clean up a few minor lint errors while I'm in here.

BUG=550047

Review URL: https://codereview.chromium.org/1496033003

Cr-Commit-Position: refs/heads/master@{#363925}

[modify] http://crrev.com/0a1c15fecb1240ab909e1431b6127410c3b380e0/chrome/browser/extensions/extension_install_prompt.cc
[modify] http://crrev.com/0a1c15fecb1240ab909e1431b6127410c3b380e0/chrome/browser/extensions/extension_install_prompt.h
[modify] http://crrev.com/0a1c15fecb1240ab909e1431b6127410c3b380e0/chrome/browser/ui/views/extensions/extension_install_dialog_view.cc


### cl...@chromium.org (2015-12-29)

asargent@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### as...@chromium.org (2016-01-05)

Requesting merge to M48 branch, since this has been live in canary for a few weeks with no problem reports

### ti...@google.com (2016-01-05)

Congrats your change is auto-approved for M48 (branch: 2564)

### bu...@chromium.org (2016-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2639e878336ccd138e0ab20a3daea375998c3a81

commit 2639e878336ccd138e0ab20a3daea375998c3a81
Author: Antony Sargent <asargent@chromium.org>
Date: Tue Jan 05 20:59:35 2016

Don't allow inline install if frame is deleted before user accepts

If the frame that called the chrome.webstore.install method to begin an
inline install gets deleted before the user accepts from the dialog, we
don't want the install to continue because a navigation could make it
look like the install request was coming from some unrelated site.

One downside of this approach is that the dialog stays around even after
the frame is deleted, and hitting either accept or cancel buttons both
just cancel the install. It would be better if the dialog is
automatically cancelled, but doing that would involve a lot more
refactoring. The approach in this CL was easier and is probably worth
getting out, and we can improve on it in the future.

BUG=550047

Review URL: https://codereview.chromium.org/1403293008

Cr-Commit-Position: refs/heads/master@{#361218}
(cherry picked from commit bbe84115d3dc969bfcf6ca87bebd1f5608db6ecf)

Review URL: https://codereview.chromium.org/1554233005 .

Cr-Commit-Position: refs/branch-heads/2564@{#478}
Cr-Branched-From: 1283eca15bd9f772387f75241576cde7bdec7f54-refs/heads/master@{#359700}

[modify] http://crrev.com/2639e878336ccd138e0ab20a3daea375998c3a81/chrome/browser/extensions/tab_helper.cc
[modify] http://crrev.com/2639e878336ccd138e0ab20a3daea375998c3a81/chrome/browser/extensions/webstore_inline_installer.cc
[modify] http://crrev.com/2639e878336ccd138e0ab20a3daea375998c3a81/chrome/browser/extensions/webstore_inline_installer.h
[modify] http://crrev.com/2639e878336ccd138e0ab20a3daea375998c3a81/chrome/browser/extensions/webstore_inline_installer_browsertest.cc
[modify] http://crrev.com/2639e878336ccd138e0ab20a3daea375998c3a81/chrome/browser/extensions/webstore_inline_installer_factory.cc
[modify] http://crrev.com/2639e878336ccd138e0ab20a3daea375998c3a81/chrome/browser/extensions/webstore_inline_installer_factory.h
[modify] http://crrev.com/2639e878336ccd138e0ab20a3daea375998c3a81/chrome/browser/extensions/webstore_inline_installer_unittest.cc
[add] http://crrev.com/2639e878336ccd138e0ab20a3daea375998c3a81/chrome/test/data/extensions/api_test/webstore_inline_install/empty.html


### cl...@chromium.org (2016-01-05)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### bu...@chromium.org (2016-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a200eafc29fbb1e80818b6cea59fb433dd09f917

commit a200eafc29fbb1e80818b6cea59fb433dd09f917
Author: Antony Sargent <asargent@chromium.org>
Date: Tue Jan 05 21:04:35 2016

Make the webstore inline install dialog be tab-modal

Also clean up a few minor lint errors while I'm in here.

BUG=550047

Review URL: https://codereview.chromium.org/1496033003

Cr-Commit-Position: refs/heads/master@{#363925}
(cherry picked from commit 0a1c15fecb1240ab909e1431b6127410c3b380e0)

Review URL: https://codereview.chromium.org/1563543003 .

Cr-Commit-Position: refs/branch-heads/2564@{#479}
Cr-Branched-From: 1283eca15bd9f772387f75241576cde7bdec7f54-refs/heads/master@{#359700}

[modify] http://crrev.com/a200eafc29fbb1e80818b6cea59fb433dd09f917/chrome/browser/extensions/extension_install_prompt.cc
[modify] http://crrev.com/a200eafc29fbb1e80818b6cea59fb433dd09f917/chrome/browser/extensions/extension_install_prompt.h
[modify] http://crrev.com/a200eafc29fbb1e80818b6cea59fb433dd09f917/chrome/browser/ui/views/extensions/extension_install_dialog_view.cc


### bu...@chromium.org (2016-01-06)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/2639e878336ccd138e0ab20a3daea375998c3a81

commit 2639e878336ccd138e0ab20a3daea375998c3a81
Author: Antony Sargent <asargent@chromium.org>
Date: Tue Jan 05 20:59:35 2016


### bu...@chromium.org (2016-01-06)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/a200eafc29fbb1e80818b6cea59fb433dd09f917

commit a200eafc29fbb1e80818b6cea59fb433dd09f917
Author: Antony Sargent <asargent@chromium.org>
Date: Tue Jan 05 21:04:35 2016


### cl...@chromium.org (2016-01-06)

[Empty comment from Monorail migration]

### he...@gmail.com (2016-02-06)

Hey.. Is this bug eligible to go to the reward panel?

### me...@chromium.org (2016-02-08)

Yes, we'll consider it.

### ti...@google.com (2016-03-01)

Tagging for release in M-49 release notes (as this missed the last M-48).

### ti...@google.com (2016-03-02)

Congratulations Luan - $1,000 for this report. I'll follow up with a CVE-ID shortly and we'll credit you as "Luan Herrera" for this report in the Chrome 49 release notes today.

I'll add this to next week's payment run as well - thanks for your report!

### ti...@google.com (2016-03-02)

CVE-2016-1640

### ti...@google.com (2016-03-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-12)

Removing the view restriction from this one a bit early.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### la...@chromium.org (2016-12-09)

Security>UX component is deprecated in favor of the Team-Security-UX label

[Monorail components: -Security>UX]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/550047?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083112)*

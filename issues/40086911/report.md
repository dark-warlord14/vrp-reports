# Security: Filesystem dialog box to cover the self-window and no origin for spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40086911](https://issues.chromium.org/issues/40086911) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WindowDialog, UI>Browser, UI>Browser>Omnibox>SecurityIndicators |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | xi...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2017-02-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome in the MAC version, when the window's width=1 and height=1, the dialog box can override self-window。And in the dialog's UI is no origin.The issue may allow a remote attacker to carry out phishing style attacks.

**VERSION**  

Chrome Version:56.0.2924.87 (64-bit)[Stable]  

Operating System: MAC

Online Demo: <https://jsfiddle.net/xisigr/Le62kv0o/> .Please click "click me" button.

## Attachments

- [dialog1.png](attachments/dialog1.png) (image/png, 291.3 KB)
- [Screenshot from 2017-02-27 10:24:56.png](attachments/Screenshot from 2017-02-27 10_24_56.png) (image/png, 12.0 KB)
- [60-3093.png](attachments/60-3093.png) (image/png, 36.2 KB)
- [Variant.png](attachments/Variant.png) (image/png, 99.8 KB)

## Timeline

### ke...@chromium.org (2017-02-27)

Thanks for the report but I cannot reproduce. All I see is an error that says:

Your file was not found

It may have been moved or deleted.
ERR_FILE_NOT_FOUND

Can you please try reproducing on another machine and confirm this?

### xi...@gmail.com (2017-02-27)

@kerrnel, please open https://jsfiddle.net/xisigr/Le62kv0o/ in MAC chrome.Allow "jsfiddle.net" pop-up window。MAC version:10.12.3 (Latest version)

### ke...@chromium.org (2017-02-27)

Yes I did all of that but the resulting dialog just says "file was not found." I suspect for this attack to work users would have to ignore the filesystem and it has to be possible to place arbitrary contents on their filesystem. 

In your screenshot, is that dialog using a file saved on your local filesystem?

### xi...@gmail.com (2017-02-27)

Yes, the file saved victim's local filesystem.
Do you open it in chrome incognito mode? The filesystem is disable in incognito mode.


### ke...@chromium.org (2017-02-27)

Thanks I've reproduced now. I do find this bug concerning. At minimum I think the dialog should have the origin from the filesystem URL shown. I do think an ordinary user could be deceived with this dialog. Triaging as medium severity.

[Monorail components: Blink>HTML>Dialog]

### es...@chromium.org (2017-02-27)

On Linux, the dialog is constrained within the popup window (see screenshot). I don't suppose we might be able to do something similar on Mac -- Avi, do you know?

### ke...@chromium.org (2017-02-27)

I wonder if this difference in behavior is because Mac is still transitioning to Views based dialogs.

### av...@chromium.org (2017-02-27)

estark, kerrnel:

On Chrome Stable, every platform but the Mac uses Views, which for app-modal dialogs centers them on their parent window. On the Mac, NSAlerts are used, which center on the screen.

With my changes to alert ("OldSpice") which is 50% on the beta channel and 100% on dev and canary, we switch from app-modal dialogs to auto-dismissing tab-modal ones, which are centered on the parent window.

I wasn't thinking of my changes as being pro-security but it seems like a nice benefit. The next step for my dialog work is 1% stable and I'm going to ask to go for that in the next few days.

### sh...@chromium.org (2017-02-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-14)

avi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-03-28)

avi: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### ra...@chromium.org (2017-05-02)

avi: has there been any update on this? In #8 it seems like you were trying to get at least a partial fix shipped? 

### av...@chromium.org (2017-05-03)

I turned on auto-dismissing dialogs yesterday. This should be better. Sorry I can't check; I'm super deep into a regression right now.

Can you look?

### el...@chromium.org (2017-05-08)

This still seems reasonably compelling in 60.0.3093; the title bar for the window is visible (just barely) over the prompt itself. 

### av...@chromium.org (2017-05-08)

This is a fundamental problem with reusing the tab-modal dialogs rather than getting new UI.

For the auto-dismissing dialogs, I requested new UI from the UX team, to show the dialog in-page rather than attaching it like you see. They declined, saying we already have too much UI.

Without UX support and without new UI for alert/confirm/prompt dialogs, I'm not sure what I can do here. Do you have thoughts?

### el...@chromium.org (2017-05-17)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-05-17)

The variant duped in https://crbug.com/chromium/696454#c17 points out that the positioning of the alert window, instead of fully occluding its host window, might also occlude a security-sensitive portion of its omnibox leading to a similar spoof.

### av...@chromium.org (2017-05-30)

Same response as https://crbug.com/chromium/696454#c16. Alerts desperately need new UI. If you can get the UX team to approve new UI, this can be fixed.

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### mm...@chromium.org (2017-11-15)

CC'ing more folks and adding some labels as per c#16 and c#19. Please take a look.

[Monorail components: Blink>WindowDialog UI>Browser]

### ro...@chromium.org (2017-11-15)

Adding some Harmony devs.

### ko...@chromium.org (2017-11-16)

[Empty comment from Monorail migration]

### fa...@chromium.org (2017-11-16)

It looks like this is using Window#prompt() not the HTML <dialog> element, so removing Blink>HTML>Dialog.

[Monorail components: -Blink>HTML>Dialog]

### me...@chromium.org (2017-11-16)

Part of the problem is that the alert says "This page says" for filesystem, blob, data etc URLs.

For filesystem and blob it can instead show the effective origin.
For data URLs, there was previous discussion to block modal dialogs in https://crbug.com/chromium/537452. That'll probably break too many things, so perhaps we can use the origin of the first non-data URL parent of the data URL iframe.

### av...@chromium.org (2017-11-16)

My response is still the response in https://crbug.com/chromium/696454#c19. JavaScript dialogs need new UI.

Mitigation in https://crbug.com/chromium/696454#c28 can help; I'll investigate that.

### av...@chromium.org (2017-11-16)

Where was the discussion about blocking dialogs from data origins? What data was the decision that it would "probably break too many things" based on?

I don't see any metrics as to the URL type.

### me...@chromium.org (2017-11-17)

The discussion is at https://crbug.com/chromium/537452, comments #7 and #10.

No data for "probably break too many things", just a guess. I remember looking into adding metrics for modal dialogs on data URLs, but for some reason didn't land them. (maybe found it difficult? Idk)


### av...@chromium.org (2017-11-17)

Let's get some metrics. https://crrev.com/c/776123

### av...@chromium.org (2017-11-17)

Meanwhile, as discussed in https://crbug.com/chromium/746572, we should be passing RenderFrameHost into the JavaScript dialog API rather than the URL, which would give us the freedom to get more information about the URL.

### bu...@chromium.org (2017-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5427a3a3f716d18e5e57a4633c65bfb24eb551da

commit 5427a3a3f716d18e5e57a4633c65bfb24eb551da
Author: Avi Drissman <avi@chromium.org>
Date: Fri Nov 17 20:31:41 2017

Measure the schemes of alerting pages.

BUG=696454

Change-Id: I7ea839d6c9135c639b1a8a68843721142d4bf81c
Reviewed-on: https://chromium-review.googlesource.com/776123
Reviewed-by: Eric Lawrence <elawrence@chromium.org>
Reviewed-by: Mustafa Emre Acer <meacer@chromium.org>
Reviewed-by: Ilya Sherman <isherman@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#517540}
[modify] https://crrev.com/5427a3a3f716d18e5e57a4633c65bfb24eb551da/chrome/browser/ui/BUILD.gn
[modify] https://crrev.com/5427a3a3f716d18e5e57a4633c65bfb24eb551da/chrome/browser/ui/javascript_dialogs/javascript_dialog_tab_helper.cc
[modify] https://crrev.com/5427a3a3f716d18e5e57a4633c65bfb24eb551da/components/navigation_metrics/navigation_metrics.cc
[modify] https://crrev.com/5427a3a3f716d18e5e57a4633c65bfb24eb551da/components/navigation_metrics/navigation_metrics.h
[modify] https://crrev.com/5427a3a3f716d18e5e57a4633c65bfb24eb551da/tools/metrics/histograms/histograms.xml


### av...@chromium.org (2017-11-18)

If I had my druthers I would allow dialogs only from http/https/file origins, although it'll be interesting to see how the JSDialogs.Scheme.* metrics show up.

### av...@chromium.org (2017-11-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-11-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7

commit ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7
Author: Avi Drissman <avi@chromium.org>
Date: Tue Nov 28 21:18:12 2017

Measure the schemes of pages showing beforeunload dialogs.

BUG=696454
TBR=jam@chromium.org

Change-Id: I68bae775dfa3a4a5c74b19659b81cfe976502365
Reviewed-on: https://chromium-review.googlesource.com/791517
Reviewed-by: Avi Drissman <avi@chromium.org>
Reviewed-by: Lucas Gadani <lfg@chromium.org>
Reviewed-by: Ilya Sherman <isherman@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#519841}
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/android_webview/browser/aw_javascript_dialog_manager.cc
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/android_webview/browser/aw_javascript_dialog_manager.h
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/chrome/browser/ui/javascript_dialogs/javascript_dialog_tab_helper.cc
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/chrome/browser/ui/javascript_dialogs/javascript_dialog_tab_helper.h
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/components/app_modal/javascript_dialog_manager.cc
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/components/app_modal/javascript_dialog_manager.h
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/content/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/content/browser/frame_host/render_frame_host_impl_browsertest.cc
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/content/browser/web_contents/web_contents_impl_browsertest.cc
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/content/browser/web_contents/web_contents_impl_unittest.cc
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/content/public/browser/javascript_dialog_manager.h
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/content/shell/browser/layout_test/layout_test_javascript_dialog_manager.cc
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/content/shell/browser/layout_test/layout_test_javascript_dialog_manager.h
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/content/shell/browser/shell_javascript_dialog_manager.cc
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/content/shell/browser/shell_javascript_dialog_manager.h
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/extensions/browser/guest_view/web_view/javascript_dialog_helper.cc
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/extensions/browser/guest_view/web_view/javascript_dialog_helper.h
[modify] https://crrev.com/ff9ed750bd9a0c9a428a7e8439f003bfac4ec4e7/tools/metrics/histograms/histograms.xml


### pa...@chromium.org (2017-11-28)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Omnibox>SecurityIndicators]

### bu...@chromium.org (2017-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/82c4500f8a46069fb67416357a77f8ae04d89cda

commit 82c4500f8a46069fb67416357a77f8ae04d89cda
Author: Avi Drissman <avi@chromium.org>
Date: Wed Nov 29 22:32:29 2017

Refactor titling of JavaScript alerts.

No functional change, just making it testable.

BUG=696454
TEST=The new test!
TBR=caitkp@chromium.org

Change-Id: Iea28648b76856a7753776e21eeed809ef85460ec
Reviewed-on: https://chromium-review.googlesource.com/794171
Commit-Queue: Avi Drissman <avi@chromium.org>
Reviewed-by: Cait Phillips <caitkp@chromium.org>
Reviewed-by: Mustafa Emre Acer <meacer@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#520277}
[modify] https://crrev.com/82c4500f8a46069fb67416357a77f8ae04d89cda/components/BUILD.gn
[modify] https://crrev.com/82c4500f8a46069fb67416357a77f8ae04d89cda/components/app_modal/BUILD.gn
[modify] https://crrev.com/82c4500f8a46069fb67416357a77f8ae04d89cda/components/app_modal/javascript_dialog_manager.cc
[modify] https://crrev.com/82c4500f8a46069fb67416357a77f8ae04d89cda/components/app_modal/javascript_dialog_manager.h
[add] https://crrev.com/82c4500f8a46069fb67416357a77f8ae04d89cda/components/app_modal/javascript_dialog_manager_unittest.cc


### bu...@chromium.org (2017-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/63f6729074c017bdb26d756d5cdfc6eb49423216

commit 63f6729074c017bdb26d756d5cdfc6eb49423216
Author: Avi Drissman <avi@chromium.org>
Date: Fri Dec 01 02:06:47 2017

Improve titling of JavaScript alerts.

If the URL of an alerting page can be unwrapped, do so. This
improves the ability of the user to tell what page is showing
the alert.

BUG=696454
TEST=the dialog in that bug is labeled.

Change-Id: I71358be49418ab6d4a88e04f317241e134e361ce
Reviewed-on: https://chromium-review.googlesource.com/797677
Commit-Queue: Avi Drissman <avi@chromium.org>
Reviewed-by: Mustafa Emre Acer <meacer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#520787}
[modify] https://crrev.com/63f6729074c017bdb26d756d5cdfc6eb49423216/components/app_modal/javascript_dialog_manager.cc
[modify] https://crrev.com/63f6729074c017bdb26d756d5cdfc6eb49423216/components/app_modal/javascript_dialog_manager_unittest.cc


### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-02-14)

The original PoC will partially be broken by https://crbug.com/chromium/811558 where we'll block navigations to filesystem URLs. There is still blob: though, so this doesn't fully fix the problem.

Avi: What work remains here? Have you had a chance to look at the data from https://crbug.com/chromium/696454#c37?

### av...@chromium.org (2018-02-14)

First, as per https://crbug.com/chromium/696454#c40 we unwrap filesystem and blob URLs so they are no longer abusable by this.

The problem remains that the page can mask the origin using data: or the like. The real issue is that we put a URL into the dialog to try to explain to the user what's going on, and that's too much to ask. I'm working on getting new UI which would alleviate the issue.

The data from https://crbug.com/chromium/696454#c37 is unfortunately irrelevant. As per discussions with web standards folks, dropping alerts from non-attributable URLs is just about entirely a non-starter.

### bu...@chromium.org (2018-02-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2fefc4bd0b63b9be05846fddaaf47047f103544c

commit 2fefc4bd0b63b9be05846fddaaf47047f103544c
Author: Avi Drissman <avi@chromium.org>
Date: Thu Feb 22 20:41:01 2018

Give the JS dialog manager the alerting frame.

Back when this interface was originally designed, frames did not
have a proper type. Now that they do, plumb it through. That
allows the manager to make more intelligent decisions about
presenting the dialogs.

BUG=696454, 802007

Change-Id: I8aef92770bd80cfb00a59761ac492394b78d1953
Reviewed-on: https://chromium-review.googlesource.com/928828
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#538552}
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/android_webview/browser/aw_javascript_dialog_manager.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/android_webview/browser/aw_javascript_dialog_manager.h
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/chrome/browser/ui/javascript_dialogs/javascript_dialog_browsertest.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/chrome/browser/ui/javascript_dialogs/javascript_dialog_tab_helper.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/chrome/browser/ui/javascript_dialogs/javascript_dialog_tab_helper.h
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/components/app_modal/javascript_dialog_manager.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/components/app_modal/javascript_dialog_manager.h
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/browser/frame_host/render_frame_host_delegate.h
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/browser/frame_host/render_frame_host_impl.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/browser/frame_host/render_frame_host_impl_browsertest.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/browser/web_contents/web_contents_impl_browsertest.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/browser/web_contents/web_contents_impl_unittest.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/public/browser/javascript_dialog_manager.h
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/shell/browser/layout_test/layout_test_javascript_dialog_manager.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/shell/browser/layout_test/layout_test_javascript_dialog_manager.h
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/shell/browser/shell_javascript_dialog_manager.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/shell/browser/shell_javascript_dialog_manager.h
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/extensions/browser/guest_view/web_view/javascript_dialog_helper.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/extensions/browser/guest_view/web_view/javascript_dialog_helper.h


### bu...@chromium.org (2018-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5eb6e6f5c005711ee0cb3b18c8b928fb5164f560

commit 5eb6e6f5c005711ee0cb3b18c8b928fb5164f560
Author: Avi Drissman <avi@chromium.org>
Date: Tue Feb 27 16:54:20 2018

Get metrics on the use of cross-origin JavaScript dialogs.

BUG=696454, 802007

Change-Id: I32982c6c34a24f67cfbb7c8fe07b943efaf90822
Reviewed-on: https://chromium-review.googlesource.com/924373
Commit-Queue: Avi Drissman <avi@chromium.org>
Reviewed-by: Emily Stark <estark@chromium.org>
Reviewed-by: Ilya Sherman <isherman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#539461}
[modify] https://crrev.com/5eb6e6f5c005711ee0cb3b18c8b928fb5164f560/chrome/browser/ui/javascript_dialogs/javascript_dialog_tab_helper.cc
[modify] https://crrev.com/5eb6e6f5c005711ee0cb3b18c8b928fb5164f560/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/5eb6e6f5c005711ee0cb3b18c8b928fb5164f560/tools/metrics/histograms/histograms.xml


### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### me...@google.com (2018-07-27)

Avi: Another sheriff check :) 

So I am actually seeing the proper origin on the dialog (nice!) and I suppose this is after the fix at https://crbug.com/chromium/696454#c45. Is there still work to do here?

### av...@chromium.org (2018-07-27)

The problem is that this is again easily defeatable with the right URL scheme.

Not sure what do without custom UI.

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-12-03)

Sorry for getting back to this so randomly. With data and filesystem blocked and blob unrolled properly, what would be the right URL scheme to be used for the spoof?

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### ct...@chromium.org (2019-09-03)

Re #55: I don't think there are any remaining spoofs for this, as stated filesystem/data are blocked and blob is unrolled. The remaining schemes are http/https/file (acceptable), about/chrome (privileged), chrome-search/chrome-devtools (internal), and chrome-extension (privileged).

I'm separately going to try to pick up the "we need new alert UI" fight in the near future, but I don't think we technically need it to resolve this bug.

### sh...@chromium.org (2019-09-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-07)

Not requesting merge to beta (M77) because latest trunk commit (539461) appears to be prior to beta branch point (681094). If this is incorrect, please replace the Merge-na label with Merge-Request-77. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-19)

Congrats! The Panel decided to reward $1,000 for this report :) 

### na...@google.com (2019-09-19)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/696454?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>WindowDialog, UI>Browser, UI>Browser>Omnibox>SecurityIndicators]
[Monorail mergedwith: crbug.com/chromium/723546]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086911)*

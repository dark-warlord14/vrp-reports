# Security: Share dialog on Windows can render over address bar, window controls

| Field | Value |
|-------|-------|
| **Issue ID** | [40056848](https://issues.chromium.org/issues/40056848) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>WebShare |
| **Platforms** | Windows |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | mh...@microsoft.com |
| **Created** | 2021-08-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The navigator.share() dialog on Windows can be shown over sensitive browser UI, such as the address bar and window controls, in short windows. A malicious page can effectively trick a user into thinking the shared items (text, URL, files) are coming from a different origin, based on address bar origin and page contents of the visible background window, combined with the lack of browser UI or window controls in the popup window.

This may also occur in other OSes, but I have not tested them.

Code analysis indicates this is a system dialog initiated by Chrome. Hopefully there's a way for Chrome to tell the OS to show the dialog below sensitive browser UI such as the address bar. Alternatively, Chrome could avoid opening the dialog when the window is shorter than a safe threshold.

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/webshare/win/share_operation.cc;l=424;drc=7ef1cfdc609b6c5515a604c5f75ec5d45da2872f>  

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/webshare/win/show_share_ui_for_window_operation.cc;l=140;drc=e308547f071951c559ac93814733aa04a31c4e1d>

ADDITIONAL CONTEXT  

Adding origin information in the share dialog may help make the initiator clear to the user, both for security and usability purposes. Currently, even when used as intended, the initiator can be a mystery to the user. On Windows, the UI design looks like part of the OS or a non-Chrome application, therefore web origin information might be particularly important to prevent OS/app spoofing of some sort. Unsure how feasible this is, given the dialog seems to be implemented by the OS. Also unsure how this varies across OSes.

(I accidentally discovered the share dialog after an errant click in an embedded YouTube video; didn't think it was initiated by a website or Chrome, especially since UI design is from Windows, not Chrome. Initially thought I accidentally used a Windows keyboard shortcut that tried to share who-knows-what.)

**VERSION**  

Chrome Version: 92.0.4515.131 (Official Build) (64-bit) (cohort: Stable), 94.0.4603.1 Canary  

Operating System: Windows 10 OS Version 2009 (Build 19042.1110)

**REPRODUCTION CASE**

1. Navigate to <https://alesandroortiz.com/security/chromium/share-shortwin.html>
2. Double-click anywhere in page.

Observed: Share dialog is shown over address bar, window controls.  

Expected: Share dialog is shown below address bar and other sensitive browser UI.

Note: Under certain circumstances, the second click on the popup is not necessary due to <https://crbug.com/chromium/1085982> (security restricted). This allows for more effective spoofing.

A more plausible attack could be showing this over drive[.]google[.]com or another origin where sharing files might be more expected by user.

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [share-shortwin.mp4](attachments/share-shortwin.mp4) (video/mp4, 919.6 KB)
- [share-shortwin.html](attachments/share-shortwin.html) (text/plain, 1.0 KB)
- [share-shortwin-popup.html](attachments/share-shortwin-popup.html) (text/plain, 326 B)
- [crbug-1238631-fixed.png](attachments/crbug-1238631-fixed.png) (image/png, 171.2 KB)

## Timeline

### [Deleted User] (2021-08-11)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-08-11)

Thanks for your report. This does look similar to your other recent reports e.g. https://crbug.com/chromium/1235222.

[Monorail components: UI>Browser>Sharing]

### al...@alesandroortiz.com (2021-08-11)

Thanks for initial triage.

I'm exploring different ways to cover browser UI with other browser UIs, so expect a few more reports around this theme but using different features (and requiring different fixes).

Got inspired to focus on this by recently disclosed reports (mainly https://crbug.com/chromium/1172533) and this blog post: https://microsoftedge.github.io/edgevr/posts/ui-security-thinking-outside-the-viewport/

### wf...@chromium.org (2021-08-11)

[assign to correct component] ericwilligers can you take a look at this bug? Is it possible for us to represent the origin in the dialog somehow?

[Monorail components: -UI>Browser>Sharing Blink>WebShare]

### er...@chromium.org (2021-08-11)

[Empty comment from Monorail migration]

### er...@chromium.org (2021-08-11)

[Empty comment from Monorail migration]

### mh...@microsoft.com (2021-08-12)

At least the current implementation of the Windows Share dialog attempts to render itself entirely within the render space of the corresponding hwnd. It sounds a little heavy of a solution, but could we create an hwnd solely for the Share operation to control the dialog's placement?

### [Deleted User] (2021-08-12)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### er...@chromium.org (2021-08-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2021-09-21)

ericwilligers@, mho...@, and team: Friendly ping. Any updates on this issue? No crbug activity since a month ago.

### er...@chromium.org (2021-09-21)

Reassigning to Desktop PWAs team. (I'm in the ChromeOS team.) 

### gi...@appspot.gserviceaccount.com (2021-11-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c829098b81e868baa40a8fe7d113fc17b37ee2d2

commit c829098b81e868baa40a8fe7d113fc17b37ee2d2
Author: Hoch Hochkeppel <mhochk@microsoft.com>
Date: Thu Nov 04 21:12:30 2021

Accessible HWND for Windows navigator.Share

Updating the Windows implementation of navigator.Share to try to use
the HWND designated for accessibility with the WebContents. This allows
the resulting system dialog to better position/associate itself with
the WebContents, rather than just the entire window.

Fixed: 1238631
Change-Id: Ic5972234ce39ddef30115cc8139959e2146fdc3a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3262558
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Commit-Queue: Hoch Hochkeppel <mhochk@microsoft.com>
Cr-Commit-Position: refs/heads/main@{#938502}

[modify] https://crrev.com/c829098b81e868baa40a8fe7d113fc17b37ee2d2/chrome/browser/webshare/win/share_operation.cc


### [Deleted User] (2021-11-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-05)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2021-11-12)

Thanks for fix!

Verified as fixed in 98.0.4700.0 Canary on Windows 10 Version 20H2 (Build 19042.1288). Share dialog is shown below address bar as expected (see attached screenshot).

### cm...@chromium.org (2021-11-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-03-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-11)

Congratulations, Alesandro, on another one! We appreciate your efforts in reporting this issue. Given that this spoof is very overt and is a little tricky to execute in terms of tricking the user, we are extended a reduced reward in comparison to your other reports. We greatly appreciate your efforts as well as reporting these issues to us! 

### al...@alesandroortiz.com (2022-03-11)

Thanks for the reward!

### am...@google.com (2022-03-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2022-07-29)

This issue was migrated from crbug.com/chromium/1238631?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056848)*

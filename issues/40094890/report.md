# Chrome CORS Causes Unauthorized File Download and Arbitrary File Execution on macOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40094890](https://issues.chromium.org/issues/40094890) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | Mac |
| **Reporter** | ev...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2019-05-07 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36

Steps to reproduce the problem:
1. Select all URL Text with the mouse
2. Right-click the service to OpenTheURL
3. You'll see the calculator  popup and there's an unauthorized download file(evil.txt: Any type of file can actually be) in the local disk `/Users/{cpname}/Downloads` directory 

PoC: https://server.n0tr00t.com/chrome/openurl_spoof_rce.html
Video: https://server.n0tr00t.com/chrome/20190506.mp4

What is the expected behavior?
If it is not web protocol (http/https), it should be refused to open. In fact, any agreement here is OK. In addition, if it is a file protocol or FTP protocol, `Finder window` should be displayed instead of Open `file://args'.`

What went wrong?
Use the 4 problems that exist to form the above PoC chain.

1. Using Chrome to invoke Apple's service function, We can complete the call from HTTP to file domain.("CORS")
2. Because users are unlikely to open strange (malicious) addresses directly by right-clicking, we use CSS for content spoofing. But in fact, malicious content has been copied in the process of duplicating websites. The OpenURL function then automatically identifies the pseudo-protocol inside and sorts the arrays and opens them in turn.
3. Opening the URL This behavior should be either displaying the Finder window or disabling cross-domain. should not open the app directly and open any schemes without warning prompt. For example, the opening of x-man-page:// through have a browser actually a security warning, but it can be bypassed by the service. Of course the underlying is the interface provided by macOS, but we should use it more safely or discard it.
4. We have come up with a way to download files directly to computers that are not authorized. By creating anonymous FTP protocols and passing them directly into files, they are automatically downloaded to the user's Downloads directory. (e.g: ftp://anonymous:evi1m0@x.x.x/test.dmg)

Did this work before? N/A 

Chrome version: 74.0.3729.131  Channel: stable
OS Version: OS X 10.14.2
Flash Version: 

Firefox right-click does not invoke service/openurl functions.

## Attachments

- [openurl_spoof_rce.html](attachments/openurl_spoof_rce.html) (text/plain, 484 B)

## Timeline

### va...@chromium.org (2019-05-07)

[Description Changed]

### va...@chromium.org (2019-05-09)

Thanks for the report.
When you say "Right-click the service to OpenTheURL", you mean "Services" > "Open URL". Correct?

If so, I can repro this on Chrome, but I can repro this with Safari too. It seems like a platform issue.

### ev...@gmail.com (2019-05-09)

#2 Hi

Yes, I understand you mean.

So I described in my report: "Of course the underlying is the interface provided by macOS, but we should use it more safely or discard it. more Firefox right-click does not invoke service/openurl functions."

### sh...@chromium.org (2019-05-09)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2019-05-10)

eugenebut@ -- is there anything we can do about this?

I'm not convinced this is a security bug in Chrome; I think this is a platform bug.
Still setting Security_Severity-Low out of an abundance of caution.

### va...@chromium.org (2019-05-10)

[Empty comment from Monorail migration]

[Monorail components: Mobile>iOSWeb>Security]

### ev...@gmail.com (2019-05-10)

Yes, I've also shown that this is not a vulnable for Chrome itself. It's Apple's underlying interface, but Chrome uses it, and Firefox doesn't, so it's not affected.

### sh...@chromium.org (2019-05-10)

[Empty comment from Monorail migration]

### eu...@chromium.org (2019-05-13)

I don't think that component and owner were correctly determined for this bug. This bug does not seem to affect iOS.

[Monorail components: -Mobile>iOSWeb>Security]

### el...@chromium.org (2019-05-13)

Mac triage: to rsesek@ - what should we do with this?

### rs...@chromium.org (2019-05-13)

We already filter the services menu items for the renderer context menu here: https://cs.chromium.org/chromium/src/chrome/browser/ui/cocoa/renderer_context_menu/render_view_context_menu_mac_cocoa.mm?l=71&rcl=ed8977423fd49d88931f922d88bd9cd9a7cd5dcc

Can we filter the "Open URL" one too?

### el...@chromium.org (2019-05-14)

Probably! We can try at least. Over to avi@ :)

### av...@chromium.org (2019-05-14)

Given that we have an "Go to <url>" menu item that (in my testing) isn't falling victim to this, this appears to be a good approach. Lemme see what I can do.

### rs...@chromium.org (2019-05-14)

FYI I also tested Safari and the issue is repro-able there.

### av...@chromium.org (2019-05-14)

In addition to what we do, this should be reported to Apple.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6fef022129a480e8259d52b0b30923128f81c613

commit 6fef022129a480e8259d52b0b30923128f81c613
Author: Avi Drissman <avi@chromium.org>
Date: Tue May 14 18:50:33 2019

Remove "Open URL" service item.

It is redundant to the one that Chromium provides.

BUG=960209

Change-Id: I5d9133311f19196b3cbe4d59376300defe5451c8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1611910
Auto-Submit: Avi Drissman <avi@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#659597}

[modify] https://crrev.com/6fef022129a480e8259d52b0b30923128f81c613/chrome/browser/ui/cocoa/renderer_context_menu/render_view_context_menu_mac_cocoa.mm
[modify] https://crrev.com/6fef022129a480e8259d52b0b30923128f81c613/chrome/browser/ui/cocoa/renderer_context_menu/render_view_context_menu_mac_cocoa_browsertest.mm


### av...@chromium.org (2019-05-14)

Please confirm on Canary that this removes that item in the Services menu for you.

### rs...@chromium.org (2019-05-15)

The "Open URL" option is gone for me in 76.0.3795.0 on macOS 10.14.4.

### av...@chromium.org (2019-05-15)

Done then.

Worth merging?

### rs...@chromium.org (2019-05-15)

I don't think so given where M75 is in the cycle and that this is Sev-Low.

### sh...@chromium.org (2019-05-16)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-20)

[Empty comment from Monorail migration]

### na...@google.com (2019-06-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-06-20)

Congrats the Panel decided to reward $500 for this report

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### ad...@google.com (2019-07-29)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-07-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### is...@google.com (2019-11-23)

This issue was migrated from crbug.com/chromium/960209?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094890)*

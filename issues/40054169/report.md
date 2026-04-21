# Security: Bypass iframe security policy in the portal element

| Field | Value |
|-------|-------|
| **Issue ID** | [40054169](https://issues.chromium.org/issues/40054169) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Portals, Internals>Plugins>PDF, Platform>Apps>BrowserTag, UI>Browser>Navigation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | mc...@chromium.org |
| **Created** | 2020-12-14 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Activate the pdf in the portal element will bypass 'X-Frame-Options','Mixed Content' and some other security police.

the Chromium deals the http/https website with an error handler.  

That maybe causes some other issue.

Some like <https://crbug.com/chromium/1158376>

**VERSION**  

Chrome Version: The latest chromium, asan-win32-release\_x64-836542  

Operating System: Windows 10

**REPRODUCTION CASE**  

chrome://flags/#enable-portals

1. open the <http://127.0.0.1/poc1/portal.html>
2. click anywhere in the PDF document

See the png

## Attachments

- [poc.png](attachments/poc.png) (image/png, 215.1 KB)
- [poc1.zip](attachments/poc1.zip) (application/octet-stream, 776 B)
- [portal.html](attachments/portal.html) (text/plain, 170 B)
- [url.pdf](attachments/url.pdf) (application/pdf, 694 B)
- [1158381 extension popup.png](attachments/1158381 extension popup.png) (image/png, 17.5 KB)

## Timeline

### [Deleted User] (2020-12-14)

[Empty comment from Monorail migration]

### wf...@chromium.org (2020-12-14)

[Empty comment from Monorail migration]

### wf...@chromium.org (2020-12-14)

Portals folks, can you take a look at this issue. Despite needing a feature being enabled, I believe this is behind origin trial so exposed on the web (Triage: Severity Medium).

tsepez - both this bug and also https://crbug.com/chromium/1158376 require embedding a pdf file in a portal, do you think such a thing should be possible?

[Monorail components: Blink>Portals]

### [Deleted User] (2020-12-15)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-28)

lfg: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jb...@chromium.org (2020-12-29)

Origin trial has ended. Reducing security impact.

### lf...@chromium.org (2021-01-05)

[Empty comment from Monorail migration]

### mc...@chromium.org (2021-01-06)

Clicking the link in the pdf is navigating the inner contents away from the pdf extension while the outer contents stays on the mimehandler page.

### mc...@chromium.org (2021-01-08)

It's worth noting that https://crbug.com/chromium/1159267 appears to be essentially the same issue where the pdf extension is navigating the guest contents, as creis@ observed in that issue ( https://crbug.com/1159267#c22 ).

CL: https://chromium-review.googlesource.com/c/chromium/src/+/2618602

### mc...@chromium.org (2021-01-08)

Also, any other cases which hit that code path would presumably result in this issue--beyond the cases we know about: payments UI and portals. Should we bump the security impact back to stable given this possibility?

[Monorail components: Platform>Apps>BrowserTag]

### mc...@chromium.org (2021-01-08)

No PDF extension on Android.

### cr...@chromium.org (2021-01-09)

Thanks for fixing the navigator.js issue!  I do suspect it's relevant for other non-tab WebContents cases that are able to load PDFs.  Thus, I'm not opposed to Security_Impact-Stable, though we may want to find an example if we're going to justify merges after the fix lands.  (I think there's lots of non-tab WebContents uses, so it probably shouldn't be hard.)

[Monorail components: Internals>Plugins>PDF UI>Browser>Navigation]

### cr...@chromium.org (2021-01-09)

Also, you might check if the proposed CL affects https://crbug.com/chromium/1032794, with PDF links in ChromeOS QuickView.  Sounds like it might resolve it, per https://bugs.chromium.org/p/chromium/issues/detail?id=1159267#c24.

### mc...@chromium.org (2021-01-13)

Re c#13, yeah I just tried to repro the ChromeOS QuickView issue and it is indeed the same issue. The CL will fix that case as well.

### mc...@chromium.org (2021-01-14)

Re c#12: I can confirm that this at least applies to <webview>s. Although, in that case, I suppose it's mitigated by the lack of an inherent address bar UI.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/00a5132f9a91ea816a6106c03868247590e929a7

commit 00a5132f9a91ea816a6106c03868247590e929a7
Author: Kevin McNee <mcnee@chromium.org>
Date: Fri Jan 15 15:22:39 2021

Don't allow MimeHandlerViews to navigate away from their handling extension

Currently, the PDF viewer extension tries to navigate itself using
|window.location.href| when navigating the tab via the chrome.tabs API
is not available. This fallback behaviour is incorrect as it would
navigate the guest contents instead of the tab.

We remove this fallback behaviour from the PDF viewer.

Bug: 1158381
Change-Id: I5295a60c0e3d05e7058be81b39c0716c9f6e8d65
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2618602
Reviewed-by: Charlie Reis <creis@chromium.org>
Reviewed-by: Rebekah Potter <rbpotter@chromium.org>
Reviewed-by: Lucas Gadani <lfg@chromium.org>
Commit-Queue: Kevin McNee <mcnee@chromium.org>
Cr-Commit-Position: refs/heads/master@{#844080}

[modify] https://crrev.com/00a5132f9a91ea816a6106c03868247590e929a7/chrome/browser/pdf/pdf_extension_test.cc
[modify] https://crrev.com/00a5132f9a91ea816a6106c03868247590e929a7/extensions/browser/guest_view/mime_handler_view/mime_handler_view_guest.h
[modify] https://crrev.com/00a5132f9a91ea816a6106c03868247590e929a7/chrome/browser/resources/pdf/pdf_viewer.js
[modify] https://crrev.com/00a5132f9a91ea816a6106c03868247590e929a7/chrome/browser/resources/pdf/browser_api.js
[modify] https://crrev.com/00a5132f9a91ea816a6106c03868247590e929a7/extensions/browser/guest_view/mime_handler_view/mime_handler_view_guest.cc
[modify] https://crrev.com/00a5132f9a91ea816a6106c03868247590e929a7/chrome/browser/resources/pdf/BUILD.gn
[modify] https://crrev.com/00a5132f9a91ea816a6106c03868247590e929a7/chrome/browser/resources/pdf/navigator.js


### mc...@chromium.org (2021-01-15)

[Empty comment from Monorail migration]

### mc...@chromium.org (2021-01-15)

In addition to c#15, I also found that this can be used to bypass XFO in an extension popup. In the attached image, the top half of the popup is an iframe attempting to load google.com, but is blocked by XFO, and the bottom half is google.com loaded via the pdf.

### ad...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-15)

[Empty comment from Monorail migration]

### 0x...@gmail.com (2021-01-16)

Maybe the submitted code also fixed the https://crbug.com/chromium/1158376: Security: Browser process heap-use-after-free in the portal element.
The  https://crbug.com/chromium/1158376 is also exploit the pdf navigate to cause the UAF in the browser process.
Will these two issues count as the same vulnerability?

### [Deleted User] (2021-01-16)

[Empty comment from Monorail migration]

### lf...@chromium.org (2021-01-18)

Re#21: Yes, this fix should also fix the other issue, but I'm still planning on uploading another CL to harden the code around pointer lock and portals.

### mc...@chromium.org (2021-01-19)

Note that the above CL caused https://crbug.com/chromium/1168046. I have a fix for that as well. However, if there is a desire to do a merge for this issue, we should probably only merge the PDF viewer part of the fix and not the assertion, in case there are further issues like 1168046.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b903eefba70af2672568457f76613bb8fdad8556

commit b903eefba70af2672568457f76613bb8fdad8556
Author: Kevin McNee <mcnee@chromium.org>
Date: Wed Jan 20 19:27:27 2021

Don't CHECK on MimeHandlerViews navigating to about:blank

We recently added a CHECK that MimeHandlerViews can't navigate away from
their handling extension. However, attempting to perform a lighthouse
audit of the PDF viewer causes it to navigate to about:blank.

While this is still a bug, we no longer CHECK in response to about:blank.

Bug: 1168046, 1158381
Change-Id: I84f137cffb1dbf6173bd6ad53d7bf24703acba3f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2637404
Reviewed-by: Lucas Gadani <lfg@chromium.org>
Commit-Queue: Kevin McNee <mcnee@chromium.org>
Cr-Commit-Position: refs/heads/master@{#845283}

[modify] https://crrev.com/b903eefba70af2672568457f76613bb8fdad8556/extensions/browser/guest_view/mime_handler_view/mime_handler_view_guest.cc


### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-02-18)

The VRP Panel has decided to award you $500 for this report! Thank you for this report and for your efforts!

### aw...@google.com (2021-02-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1158381?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Portals, Internals>Plugins>PDF, Platform>Apps>BrowserTag, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054169)*

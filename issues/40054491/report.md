# Security: Offline view bypasses Content-Security-Policy of the original page

| Field | Value |
|-------|-------|
| **Issue ID** | [40054491](https://issues.chromium.org/issues/40054491) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy, UI>Browser>ReaderMode |
| **Platforms** | iOS |
| **Reporter** | ni...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2021-01-17 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

"Read Later" feature in Reading List generates a distilled HTML file for offline reading.  

Then, the distilled page strips all Content-Security-Policy rules of the original page.  

So, if a page prohibits inline script by CSP, attacker can execute it on the distilled HTML that works on the same origin as the original page.

**VERSION**  

Chrome Version: 88.0.4324.69+beta  

Operating System: iPhone 8 Simulator with iOS 14.3

**REPRODUCTION CASE**

1. Visit: <https://csrf.jp/2021/chromium_ios/csp-bypass-by-offline.php>  
   
   This page is protected by `Content-Security-Policy: default-src 'self'`
2. Tap "Read Later" in the Chromium's bottom menu (then the distilled HTML is generated in the background)
3. Open "Reading List"
4. Long tap the page 1) in the list and choose "Open Offline Version"
5. The distilled page is displayed on a tab
6. Tap a hyper-link "SUPPOSE XSS IS HERE" in the page
7. An alert dialog with cookie values of csrf.jp is shown (i.e., original page's CSP was bypassed)

**CREDIT INFORMATION**  

Muneaki Nishimura (nishimunea)

## Attachments

- [csp-bypass-by-offline.php](attachments/csp-bypass-by-offline.php) (text/plain, 864 B)
- [csp-bypass-demo.mov](attachments/csp-bypass-demo.mov) (video/quicktime, 7.3 MB)

## Timeline

### [Deleted User] (2021-01-17)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-01-18)

Assigning to corising@ for investigation.

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy UI>Browser>ReadLater]

### co...@chromium.org (2021-01-19)

We aren't creating offline pages on Desktop so this looks iOS specific. Passing this on to owners for reading list on iOS.

[Monorail components: UI>Browser>ReaderMode]

### ol...@chromium.org (2021-01-19)

ahuffman:
is this fixed by your patch?

### ar...@chromium.org (2021-01-19)

FYI: The non-IOS version of this: https://crbug.com/chromium/1012956 (filled by creis@)

I don't know about the IOS version. For the non-IOS, the distilled page is running within its own opaque origin, so it won't make any action on behalf of the original document. Risk are mainly about finding a bug in the distiller to execute javascript. You can also potentially be able to exfiltrate data when loading <img> that you weren't able before the distillation.

### ah...@microsoft.com (2021-01-19)

The issue of the CSP policy being relaxed in the case of JavaScript is fixed in 1111239. However it is true that on iOS distilled pages do not get a different opaque origin so overall the CSP policy for the original domain is being changed on the distilled page.  Not sure if that warrants any further changes however.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e197614b701958a0633bc836be73302aeb90fd08

commit e197614b701958a0633bc836be73302aeb90fd08
Author: Olivier Robin <olivierrobin@google.com>
Date: Wed Jan 27 09:17:42 2021

Block online content from offline pages

This CL
- moves the offline content in a chrome://offline domain.
- adds content rules to block online resources from chrome://, file://
  and chrome-distiller:// URLs

Bug: 1167507
Change-Id: Ib96bfed9ea48badb5cc5f34f828c3cbba0981b78
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2642625
Commit-Queue: Olivier Robin <olivierrobin@chromium.org>
Reviewed-by: Gauthier Ambard <gambard@chromium.org>
Cr-Commit-Position: refs/heads/master@{#847548}

[modify] https://crrev.com/e197614b701958a0633bc836be73302aeb90fd08/ios/chrome/browser/reading_list/offline_url_utils.h
[modify] https://crrev.com/e197614b701958a0633bc836be73302aeb90fd08/ios/chrome/browser/reading_list/offline_page_tab_helper.h
[modify] https://crrev.com/e197614b701958a0633bc836be73302aeb90fd08/ios/chrome/browser/reading_list/offline_url_utils_unittest.cc
[modify] https://crrev.com/e197614b701958a0633bc836be73302aeb90fd08/ios/chrome/browser/ui/reading_list/reading_list_egtest.mm
[modify] https://crrev.com/e197614b701958a0633bc836be73302aeb90fd08/ios/web/web_state/ui/wk_content_rule_list_util.mm
[modify] https://crrev.com/e197614b701958a0633bc836be73302aeb90fd08/ios/chrome/browser/ui/reading_list/BUILD.gn
[modify] https://crrev.com/e197614b701958a0633bc836be73302aeb90fd08/ios/web/web_state/ui/wk_content_rule_list_provider.mm
[modify] https://crrev.com/e197614b701958a0633bc836be73302aeb90fd08/ios/web/web_state/ui/wk_content_rule_list_provider.h
[modify] https://crrev.com/e197614b701958a0633bc836be73302aeb90fd08/ios/chrome/browser/reading_list/offline_url_utils.cc
[modify] https://crrev.com/e197614b701958a0633bc836be73302aeb90fd08/ios/chrome/browser/reading_list/offline_page_tab_helper.mm
[modify] https://crrev.com/e197614b701958a0633bc836be73302aeb90fd08/ios/chrome/browser/web/chrome_web_client.mm
[modify] https://crrev.com/e197614b701958a0633bc836be73302aeb90fd08/ios/web/web_state/ui/wk_content_rule_list_util.h
[modify] https://crrev.com/e197614b701958a0633bc836be73302aeb90fd08/ios/web/web_state/ui/wk_content_rule_list_util_unittest.mm


### ol...@chromium.org (2021-01-27)

It should be fixed by cl in #7

### [Deleted User] (2021-01-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-27)

[Empty comment from Monorail migration]

### ol...@chromium.org (2021-02-02)

cc subhashinik@google.com to test fix

### su...@google.com (2021-02-03)

Verified on:

App Version: 90.0.4405.0 canary
Devices: iPhone 6S Plus, iPhone 7 Plus
iOS Versions: 13.7 , 14.4

Blocks online resources and original page's CSP is blocked.

Video:
https://drive.google.com/file/d/1lrMRvZGYdrG21WIgUUwPlsDjmAlzIPDh/view?usp=sharing

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-31)

Congratulations, nishimunea@! The VRP Panel has decided to award you $3000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thanks for your efforts!

### am...@google.com (2021-04-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-06-24)

This issue was migrated from crbug.com/chromium/1167507?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature>ContentSecurityPolicy, UI>Browser>ReadLater, UI>Browser>ReaderMode]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054491)*

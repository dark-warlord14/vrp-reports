# Chrome iOS Address Bar Spoof Using 2 RTL (Arabic Characters) Subdomains

| Field | Value |
|-------|-------|
| **Issue ID** | [374285495](https://issues.chromium.org/issues/374285495) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Reporter** | re...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2024-10-18 |
| **Bounty** | $2,000.00 |

## Description

## Security Bug

---

## VERSION

Chrome Version: 130.0.6723.37 (Official Build) stable (64-bit)
Operating System: iOS 18 on iPhone 16

## REPRODUCTION CASE

- Using Chrome iOS open `https://xn--llb.login.wwww.accounts.google.com.xn--llb.pwr.wtf/`

## Expected Result

Address bar showing `ە.login.wwww.accounts.google.com.ە.pwr.wtf/`

## Actual Result

Address Bar shows `pwr.wtf.ە.ogin.wwww.accounts.google.com...`

## Details

The issue arises when using 2 RTL characters in different level subdomains and in between add a domain that we want to spoof. First we add a RTL character then any domain we want to spoof and in the end we add another RTL character that will confuse the address bar and mixes up the RTL LTR showing of the URL.

## CREDIT INFORMATION

Reporter credit: Renwa Hiwa @RenwaX23

## Attachments

- [chrome_ios_spoof.mp4](attachments/chrome_ios_spoof.mp4) (video/mp4, 7.3 MB)
- [chrome_ios_spoof.jpg](attachments/chrome_ios_spoof.jpg) (image/jpeg, 55.4 KB)

## Timeline

### aj...@google.com (2024-10-18)

Thanks for the report!

Interestingly, the address shown after tapping on the omnibox is correct, but the address displayed in the omnibox is not.

Something must be going wrong in the logic that extracts the domain from the full URL to display in the omnibox.

### pe...@google.com (2024-10-19)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### re...@gmail.com (2024-11-14)

Hey there, any update here? both Edge and Yandex browsers are also affected by this. Reported to both and they asked to report and recheck here with chromium team.

### re...@gmail.com (2025-11-21)

It's been more than a year and this address bar spoof is still silent, maybe someone wants to check?

### dx...@google.com (2026-02-18)

Project: chromium/src  

Branch:  main  

Author:  Ameur Hosni [ameurhosni@google.com](mailto:ameurhosni@google.com)  

Link:    <https://chromium-review.googlesource.com/7581320>

[IOS] Fix RTL URL component reordering in the location bar

---


Expand for full commit details
```
     
    This change fixes a visual issue where URLs containing RTL characters 
    (e.g., IDN with RTL scripts) would cause the Location Bar label to 
    switch to RTL paragraph alignment. 
    This resulted in the visual reversal of URL components, displaying the 
    Top-Level Domain on the left instead of the right, which could be 
    misleading regarding the site's actual domain authority. 
     
    Before: https://screenshot.googleplex.com/5KFCzgU68rw3D4D 
    After: https://screenshot.googleplex.com/zJ8fo6KTKNGDgiZ 
     
    Fixed: 470395720,374285495 
    Change-Id: I33884fc685cb7f9a26c93d67167b4f5529cbb668 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7581320 
    Reviewed-by: Gauthier Ambard <gambard@chromium.org> 
    Commit-Queue: Ameur Hosni <ameurhosni@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1586307}

```

---

Files:

- M `ios/chrome/browser/location_bar/ui_bundled/location_bar_steady_view.h`
- M `ios/chrome/browser/location_bar/ui_bundled/location_bar_steady_view.mm`
- M `ios/chrome/browser/location_bar/ui_bundled/location_bar_view_controller.mm`

---

Hash: [f545d50577ba5a72a89e1495293d5d4bc52b64a4](https://chromiumdash.appspot.com/commit/f545d50577ba5a72a89e1495293d5d4bc52b64a4)  

Date: Wed Feb 18 10:26:31 2026


---

### ch...@google.com (2026-04-07)

WARNING: Removing security\_release value because the issue is not on security\_impact-stable or security\_impact-extended hotlists. Please add to the correct hotlist if the issue is on a release branch.

### ch...@google.com (2026-05-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. Security UI Spoofing


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/374285495)*

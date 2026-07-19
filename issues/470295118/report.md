# Blank Address Bar Spoofing on Chrome for iOS

| Field | Value |
|-------|-------|
| **Issue ID** | [470295118](https://issues.chromium.org/issues/470295118) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | iOS |
| **Chrome Version** | 143.0.7499.151 (Official Build) stable (64-bit) |
| **Reporter** | sa...@gmail.com |
| **Assignee** | ga...@google.com |
| **Created** | 2025-12-19 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Open Chrome for iOS and visit this link: <https://vxyoka.github.io/spoof/>
2. Click on Login Button
3. You will notice blank address bar with fake contents.

# Problem Description

## Summary:

A UI spoofing issue exists in Chrome for iOS where navigating to a crafted about:blank URL results in a blank address bar

## What is the expected behavior?

When navigating to about:blank, the address bar should explicitly display about:blank.

## What went wrong?

Chrome for iOS displays a completely blank address bar

# Summary

Blank Address Bar Spoofing on Chrome for iOS

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A \

## Attachments

- [POC_Blank_Address Bar_Chrome_iOS_2025-12-19 at 23.51.59.mp4](attachments/POC_Blank_Address Bar_Chrome_iOS_2025-12-19 at 23.51.59.mp4) (video/mp4, 1.6 MB)
- [poc.html](attachments/poc.html) (text/html, 3.9 KB)
- [Video 2026-02-16 at 10.49.53 PM.mp4](attachments/Video 2026-02-16 at 10.49.53 PM.mp4) (video/mp4, 1.8 MB)

## Timeline

### ca...@chromium.org (2025-12-19)

Tentatively passing to iOS folks for further triage based on video evidence since I don't have an iOS device to reproduce, but this does seem like a valid bug. Setting severity to low since this hides the URL but doesn't allow arbitrary spoofing.

### ch...@google.com (2025-12-20)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sa...@gmail.com (2025-12-22)

Hi Team,

Sorry, I forgot to include the PoC in the attachment.

Here is the PoC file:

### ju...@chromium.org (2026-01-09)

Filed FB21578178, related to this issue.

### dx...@google.com (2026-01-12)

Project: chromium/src  

Branch:  main  

Author:  Justin Cohen [justincohen@google.com](mailto:justincohen@google.com)  

Link:    <https://chromium-review.googlesource.com/7404866>

net: Refactor GURLWithNSURL to fix 'about:' scheme percent-encoding

---


Expand for full commit details
```
     
    This CL introduces a kill switch feature kUseNSURLDataForGURLConversion 
    to control the logic in GURLWithNSURL. When enabled, the conversion 
    logic prefers [NSURL dataRepresentation] over [NSURL absoluteString] if 
    they differ with the `about` scheme URLs. The dataRepresentation of the 
    NSURL is the raw bytes of the URL pre-canonicalization, so the approach 
    tries to favor GURL's interpretation over NSURL. 
     
    This change aims to address issues where absoluteString returns a 
    percent-encoded string (e.g., about:blank%23hash) while 
    dataRepresentation returns the raw bytes (e.g., about:blank#hash), which 
    is the desired input for GURL. 
     
    A new histogram Net.Apple.NSURL.DataMismatch is recorded when the two 
    representations differ, helping to monitor the impact of this change. 
    Net.Apple.NSURL.DataMismatch.Scheme is recorded to identify which 
    schemes are affected, if this happens beyond `about` 
     
    Bug: 40932726, 470295118, 474953367 
    Change-Id: I5f2467903b13f73a287c722da6d5d892870680cf 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7404866 
    Reviewed-by: Mike Dougherty <michaeldo@chromium.org> 
    Reviewed-by: Charlie Harrison <csharrison@chromium.org> 
    Reviewed-by: Avi Drissman <avi@chromium.org> 
    Reviewed-by: Gauthier Ambard <gambard@chromium.org> 
    Commit-Queue: Justin Cohen <justincohen@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1568100}

```

---

Files:

- M `ios/chrome/browser/web/model/window_open_by_dom_egtest.mm`
- M `net/BUILD.gn`
- M `net/base/apple/url_conversions.mm`
- A `net/base/apple/url_conversions_fuzzer.mm`
- M `net/base/apple/url_conversions_unittest.mm`
- M `net/base/features.cc`
- M `net/base/features.h`
- M `tools/metrics/histograms/enums.xml`
- M `tools/metrics/histograms/metadata/net/histograms.xml`

---

Hash: [7346d5fe53b8a7aa372627224fc57553191bdf95](https://chromiumdash.appspot.com/commit/7346d5fe53b8a7aa372627224fc57553191bdf95)  

Date: Mon Jan 12 23:15:32 2026


---

### dx...@google.com (2026-01-13)

Project: chromium/src  

Branch:  main  

Author:  Tsuyoshi Horo [horo@chromium.org](mailto:horo@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7453488>

Revert "net: Refactor GURLWithNSURL to fix 'about:' scheme percent-encoding"

---


Expand for full commit details
```
     
    This reverts commit 7346d5fe53b8a7aa372627224fc57553191bdf95. 
     
    Reason for revert: Caused file handler related WebAppIntegration tests failure on Mac bots. 
     
    Bug: 475359573 
     
    Original change's description: 
    > net: Refactor GURLWithNSURL to fix 'about:' scheme percent-encoding 
    > 
    > This CL introduces a kill switch feature kUseNSURLDataForGURLConversion 
    > to control the logic in GURLWithNSURL. When enabled, the conversion 
    > logic prefers [NSURL dataRepresentation] over [NSURL absoluteString] if 
    > they differ with the `about` scheme URLs. The dataRepresentation of the 
    > NSURL is the raw bytes of the URL pre-canonicalization, so the approach 
    > tries to favor GURL's interpretation over NSURL. 
    > 
    > This change aims to address issues where absoluteString returns a 
    > percent-encoded string (e.g., about:blank%23hash) while 
    > dataRepresentation returns the raw bytes (e.g., about:blank#hash), which 
    > is the desired input for GURL. 
    > 
    > A new histogram Net.Apple.NSURL.DataMismatch is recorded when the two 
    > representations differ, helping to monitor the impact of this change. 
    > Net.Apple.NSURL.DataMismatch.Scheme is recorded to identify which 
    > schemes are affected, if this happens beyond `about` 
    > 
    > Bug: 40932726, 470295118, 474953367 
    > Change-Id: I5f2467903b13f73a287c722da6d5d892870680cf 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7404866 
    > Reviewed-by: Mike Dougherty <michaeldo@chromium.org> 
    > Reviewed-by: Charlie Harrison <csharrison@chromium.org> 
    > Reviewed-by: Avi Drissman <avi@chromium.org> 
    > Reviewed-by: Gauthier Ambard <gambard@chromium.org> 
    > Commit-Queue: Justin Cohen <justincohen@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1568100} 
     
    Bug: 40932726, 470295118, 474953367 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: Ide0a813a318b4cd8c245716702bb7e9124093ee0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7453488 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Tsuyoshi Horo <horo@chromium.org> 
    Owners-Override: Tsuyoshi Horo <horo@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1568222}

```

---

Files:

- M `ios/chrome/browser/web/model/window_open_by_dom_egtest.mm`
- M `net/BUILD.gn`
- M `net/base/apple/url_conversions.mm`
- D `net/base/apple/url_conversions_fuzzer.mm`
- M `net/base/apple/url_conversions_unittest.mm`
- M `net/base/features.cc`
- M `net/base/features.h`
- M `tools/metrics/histograms/enums.xml`
- M `tools/metrics/histograms/metadata/net/histograms.xml`

---

Hash: [f44363bdeacae33b03cb3a66c1a696b8ba31a489](https://chromiumdash.appspot.com/commit/f44363bdeacae33b03cb3a66c1a696b8ba31a489)  

Date: Tue Jan 13 04:13:34 2026


---

### dx...@google.com (2026-01-14)

Project: chromium/src  

Branch:  main  

Author:  Justin Cohen [justincohen@google.com](mailto:justincohen@google.com)  

Link:    <https://chromium-review.googlesource.com/7464958>

Reland "net: Refactor GURLWithNSURL to fix 'about:' scheme percent-encoding"

---


Expand for full commit details
```
     
    This CL introduces a kill switch feature kUseNSURLDataForGURLConversion 
    to control the logic in GURLWithNSURL. When enabled, the conversion 
    logic prefers [NSURL dataRepresentation] over [NSURL absoluteString] if 
    they differ with the `about` scheme URLs. The dataRepresentation of the 
    NSURL is the raw bytes of the URL pre-canonicalization, so the approach 
    tries to favor GURL's interpretation over NSURL. 
     
    This change aims to address issues where absoluteString returns a 
    percent-encoded string (e.g., about:blank%23hash) while 
    dataRepresentation returns the raw bytes (e.g., about:blank#hash), which 
    is the desired input for GURL. 
     
    A new histogram Net.Apple.NSURL.DataMismatch is recorded when the two 
    representations differ, helping to monitor the impact of this change. 
    Net.Apple.NSURL.DataMismatch.Scheme is recorded to identify which 
    schemes are affected, if this happens beyond `about` 
     
    Reland changes in patchset 2 
      Add UseNSURLDataForGURLConversion to AppShimController to allow-list 
      it to be checked in early startup of PWAs. 
     
    Include-Ci-Only-Tests: chromium.mac:Mac13 Tests|browser_tests 
    Bug: 40932726, 470295118, 474953367 
    Change-Id: I95930c7d299c9f1f04ec65868fcba2e4c8bd0bd1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7464958 
    Reviewed-by: Gauthier Ambard <gambard@chromium.org> 
    Reviewed-by: Marijn Kruisselbrink <mek@chromium.org> 
    Auto-Submit: Justin Cohen <justincohen@chromium.org> 
    Reviewed-by: Charlie Harrison <csharrison@chromium.org> 
    Reviewed-by: Nick Harper <nharper@chromium.org> 
    Reviewed-by: Hayato Ito <hayato@chromium.org> 
    Commit-Queue: Justin Cohen <justincohen@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1569077}

```

---

Files:

- M `chrome/app_shim/app_shim_controller.mm`
- M `ios/chrome/browser/web/model/window_open_by_dom_egtest.mm`
- M `net/BUILD.gn`
- M `net/base/apple/url_conversions.mm`
- A `net/base/apple/url_conversions_fuzzer.mm`
- M `net/base/apple/url_conversions_unittest.mm`
- M `net/base/features.cc`
- M `net/base/features.h`
- M `tools/metrics/histograms/enums.xml`
- M `tools/metrics/histograms/metadata/net/histograms.xml`

---

Hash: [52b34c645e8dbf90a43e3c7985f9c9bbe4d11918](https://chromiumdash.appspot.com/commit/52b34c645e8dbf90a43e3c7985f9c9bbe4d11918)  

Date: Wed Jan 14 14:15:19 2026


---

### sa...@gmail.com (2026-02-16)

Hello Chromium Team,

It appears that this issue has been fixed in Chrome for iOS v145.0.7632.55 (Official Build) stable (64-bit).

Here is the video:

### dx...@google.com (2026-02-24)

[Details redacted due to bug visibility]

Change-Id: I30f4fe20f3e661f0b51a644733427bb7c93118ee  

<https://chrome-internal-review.git.corp.google.com/8885923>

### dx...@google.com (2026-02-24)

Project: chromium/src  

Branch:  main  

Author:  chromium-internal-autoroll [chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com](mailto:chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7602938>

Roll ios\_internal from 2c50521cec77 to 46494b6c2a6d

---


Expand for full commit details
```
     
    https://chrome-internal.googlesource.com/chrome/ios_internal.git/+log/2c50521cec77..46494b6c2a6d 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://skia-autoroll.corp.goog/r/ios-internal-chromium-autoroll 
    Please CC chrome-brapp-engprod@google.com,ewannpv@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:470295118 
    Change-Id: Ib7fb96252e8e79a6a9328bcc780b62c580e9d975 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7602938 
    Bot-Commit: chromium-internal-autoroll <chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com> 
    Commit-Queue: chromium-internal-autoroll <chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1589300}

```

---

Files:

- M `DEPS`
- M `ios_internal`

---

Hash: [e40ceac29dc8645f4462379374992e9f6acd8229](https://chromiumdash.appspot.com/commit/e40ceac29dc8645f4462379374992e9f6acd8229)  

Date: Tue Feb 24 11:33:52 2026


---

### dx...@google.com (2026-02-24)

[Details redacted due to bug visibility]

Change-Id: Ie1cfff9b6b36af270d2da53f8080a109af06e120  

<https://chrome-internal-review.git.corp.google.com/9047796>

### dx...@google.com (2026-02-24)

Project: chromium/src  

Branch:  main  

Author:  chromium-internal-autoroll [chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com](mailto:chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7604034>

Roll ios\_internal from c75357cdcc61 to 24ed3ca97f97

---


Expand for full commit details
```
     
    https://chrome-internal.googlesource.com/chrome/ios_internal.git/+log/c75357cdcc61..24ed3ca97f97 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://skia-autoroll.corp.goog/r/ios-internal-chromium-autoroll 
    Please CC chrome-brapp-engprod@google.com,ewannpv@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:470295118 
    Change-Id: Ib314e3bce9b7479100cb5d5a8b5fa1bf15a67ded 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7604034 
    Commit-Queue: chromium-internal-autoroll <chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com> 
    Bot-Commit: chromium-internal-autoroll <chromium-internal-autoroll@skia-corp.google.com.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1589414}

```

---

Files:

- M `DEPS`
- M `ios_internal`

---

Hash: [36a856615a585f49308dfea6b91bbaf3f54e9277](https://chromiumdash.appspot.com/commit/36a856615a585f49308dfea6b91bbaf3f54e9277)  

Date: Tue Feb 24 15:41:19 2026


---

### dx...@google.com (2026-05-08)

Project: chromium/src  

Branch:  main  

Author:  Justin Cohen [justincohen@google.com](mailto:justincohen@google.com)  

Link:    <https://chromium-review.googlesource.com/7811809>

ios: Remove Net.Apple.NSURL.DataMismatch histograms and simplify workaround

---


Expand for full commit details
```
     
    Remove expiring Net.Apple.NSURL.DataMismatch and 
    Net.Apple.NSURL.DataMismatch.Scheme histograms, as the telemetry 
    indicates that scoping the fix narrowly to the "about:" scheme is 
    correct. Simplify GURLWithNSURL by performing the scheme check first and 
    returning the dataRepresentation-based GURL directly for "about:" URLs, 
    avoiding unnecessary dataRepresentation calls and mismatch checks. 
     
    Bug: 504634110, 470295118, 474953367 
    Change-Id: I21a60e4ebf578975d90bb5bff78104ac01295817 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7811809 
    Auto-Submit: Justin Cohen <justincohen@google.com> 
    Commit-Queue: Matt Mueller <mattm@chromium.org> 
    Reviewed-by: Avi Drissman <avi@chromium.org> 
    Reviewed-by: Charles Harrison <csharrison@chromium.org> 
    Reviewed-by: Matt Mueller <mattm@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1627912}

```

---

Files:

- M `net/base/apple/url_conversions.mm`
- M `net/base/apple/url_conversions_unittest.mm`
- M `tools/metrics/histograms/enums.xml`
- M `tools/metrics/histograms/metadata/net/histograms.xml`

---

Hash: [0ea9810b5c969ca904a12217991155737905d80a](https://chromiumdash.appspot.com/commit/0ea9810b5c969ca904a12217991155737905d80a)  

Date: Fri May 8 21:12:56 2026


---

### sp...@google.com (2026-05-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Security UI Spoofing


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/470295118)*

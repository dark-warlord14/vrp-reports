# Potential PDFium Use-After-Free in CPDFSDK_FormFillEnvironment::OnFormat

| Field | Value |
|-------|-------|
| **Issue ID** | [341313077](https://issues.chromium.org/issues/341313077) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Chrome Version** | 125.0.6422.60 |
| **Reporter** | kd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2024-05-18 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

It's a manual audit result, so there is no poc for now. Not sure if it's exploitable. now I'm trying to work on a poc.

# Problem Description

in function CPDFSDK\_FormFillEnvironment::OnFormat, there is a call to `CPDFSDK_InteractiveForm::ResetFieldAppearance`,
which, according to crbug 40088733, could potentially involves in a js call, allows attacker to free the object `pWidget`
or `m_pInteractiveForm`, further results in a Use-After-Free

```
void CPDFSDK_FormFillEnvironment::OnFormat(ObservedPtr<CPDFSDK_Annot>& pAnnot) {

  // ...

  if (sValue.has_value()) {
    m_pInteractiveForm->ResetFieldAppearance(pWidget->GetFormField(), sValue); // <= potentially invoke a js call
    m_pInteractiveForm->UpdateField(pWidget->GetFormField()); // <= use without validation
  }
}


```

To be more precise, crbug 40088733 demonstrate that `pWidget->ResetFieldAppearance()`, a call to
`CPDFSDK_Widget::ResetFieldAppearance`, can invoke the js call.

```

void CPDFSDK_Widget::ResetFieldAppearance() {
  CPDF_FormField* pFormField = GetFormField();
  DCHECK(pFormField);
  m_pInteractiveForm->ResetFieldAppearance(pFormField, std::nullopt);
}


```

from which we could infer that `CPDFSDK_Widget::ResetFieldAppearance` is finally
obtain `CPDFSDK_Widget::GetFormField` as the first argument and calling `CPDFSDK_InteractiveForm::ResetFieldAppearance`.
which is the same as what is called in `CPDFSDK_FormFillEnvironment::OnFormat`. So `m_pInteractiveForm->ResetFieldAppearance(pWidget->GetFormField(), sValue)` may also invoke a js call and should be checked when returning.

# Summary

Potential PDFium Use-After-Free in CPDFSDK\_FormFillEnvironment::OnFormat

# Custom Questions

#### Type of crash:

tab

#### Reporter credit:

Han Zheng (HexHive)

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Timeline

### ph...@chromium.org (2024-05-20)

Security shepherd: Please add the poc when you have one. Without a reproduce there's not much we can do.

### ph...@chromium.org (2024-05-20)

Bringing to thestig@'s attention anyway

### pe...@google.com (2024-05-20)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ts...@google.com (2024-05-20)

Thanks, it wouldn't hurt to be more careful here, though without a PoC the chances for a reward are greatly diminished ...

### ts...@chromium.org (2024-05-20)

https://pdfium-review.googlesource.com/c/pdfium/+/119350

### ap...@google.com (2024-05-21)

Project: chromium/src
Branch: main

commit 6c04b4b6041ae6e86b407314d1f0fa6d76d53a65
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Tue May 21 16:41:35 2024

    Roll PDFium from 49db42fb84e0 to 8007d6ed5cd1 (20 revisions)
    
    https://pdfium.googlesource.com/pdfium.git/+log/49db42fb84e0..8007d6ed5cd1
    
    2024-05-21 thestig@chromium.org Relax pdfium_test assertion for not depending on gtest
    2024-05-21 thestig@chromium.org Remove unneeded core/fxcrt/fx_memory_wrappers.h includes
    2024-05-21 thestig@chromium.org Rename DataVectorAndBytesConsumed to DataAndBytesConsumed
    2024-05-21 thestig@chromium.org Convert FlateUncompress() to return DataVectorAndBytesConsumed instead
    2024-05-21 thestig@chromium.org Change CFX_FolderFontInfo to use FixedSizeDataVector
    2024-05-21 tsepez@chromium.org Fix unsafe buffer usage in core/fxge/dib/cfx_cmyk_to_srgb.cpp.
    2024-05-21 tsepez@chromium.org Introduce more helpful FX_*_STRUCT classes.
    2024-05-21 thestig@chromium.org Remove unnecessary encode/decode inside FPDFAttachment_SetFile()
    2024-05-21 thestig@chromium.org Remove unused includes from {byte,wide}string.h
    2024-05-20 tsepez@chromium.org Avoid invoking methods directly against observed `this`.
    2024-05-20 thestig@chromium.org Change PDFDataDecodeResult to use DataVector
    2024-05-20 tsepez@chromium.org Defensive programming around ObservedPtr<CPDFSDK_Annot>().
    2024-05-20 tsepez@chromium.org Once `this` observed, only access members through observed ptr.
    2024-05-20 thestig@chromium.org Avoid depending on gtest in scoped_locale.cc
    2024-05-20 thestig@chromium.org Change FlateOrLZWDecode() to return DataVectorAndBytesConsumed
    2024-05-20 thestig@chromium.org Return DataVector from PNG_Predictor()
    2024-05-20 thestig@chromium.org Change CLZWDecoder to use DataVector
    2024-05-20 thestig@chromium.org Move switches out of inner loop in FlatePredictorScanlineDecoder
    2024-05-20 thestig@chromium.org Get rid of extra byte allocated in FlateUncompress()
    2024-05-20 thestig@chromium.org Use more spans inside flatemodule.cpp
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/pdfium-autoroll
    Please CC dhoss@chromium.org,pdfium-deps-rolls@chromium.org,thestig@chromium.org on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Bug: chromium:341313077
    Tbr: pdfium-deps-rolls@chromium.org
    Change-Id: I50f9a0c572e8264c63d8c20a158eee2bdbdefede
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5555440
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1303836}

M       DEPS
M       third_party/pdfium

https://chromium-review.googlesource.com/5555440


### pe...@google.com (2024-05-21)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

### pe...@google.com (2024-05-22)

Setting milestone because of s2 severity.

### ts...@chromium.org (2024-05-24)

Severity and Foundin appear set, re-closing.

### pe...@google.com (2024-05-25)

Requesting merge to beta (M126) because latest trunk commit (1303836) appears to be after beta branch point (1300313).
Merge review required: a commit with DEPS changes was detected.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### ts...@chromium.org (2024-05-28)

1. https://pdfium-review.googlesource.com/c/pdfium/+/119350
2.Yes
3. Seems unlikely.
4. No.
5. No.



### am...@chromium.org (2024-05-28)

I'm not sure if the foundin-125 is accurate; however, since this is more speculative, I'm going to leave merge approval to just M126

<https://pdfium-review.googlesource.com/c/pdfium/+/119350> approved for merge to M126
please merge to branch 6478 as soon as possible (by EOD tomorrow / Wednesday 29 May) so this fix can be included in the next M126 Beta update (and next week's M126 Stable Cut)

### ts...@chromium.org (2024-05-28)

Cherry-pick at https://pdfium-review.googlesource.com/c/pdfium/+/119678

### ap...@google.com (2024-05-29)

Project: pdfium
Branch: chromium/6478

commit f41ce6b71a15ce6206740cad084871a28ff2dcec
Author: Tom Sepez <tsepez@chromium.org>
Date:   Wed May 29 03:37:59 2024

    [M126] Defensive programming around ObservedPtr<CPDFSDK_Annot>().
    
    Such an argument is a strong hint to the caller that the object may
    be destroyed somewhere in the called function, but be careful even
    within the called function to not extract a raw pointer from it.
    
    -- Change some x.Reset(y.Get()) usage to assignment to cut down on
       number of (often dubious) Get() calls.
    
    Bug: 341313077
    Change-Id: I572a2c5093f110ee04dbd2e82e3994a8266d5422
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/119350
    Reviewed-by: Lei Zhang <thestig@chromium.org>
    Commit-Queue: Tom Sepez <tsepez@chromium.org>
    Reviewed-by: Thomas Sepez <tsepez@google.com>
    (cherry picked from commit a0d85587ff7212e24d1df8a6451c49f5eaa171d6)
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/119678

M       fpdfsdk/cpdfsdk_formfillenvironment.cpp
M       fpdfsdk/cpdfsdk_pageview.cpp

https://pdfium-review.googlesource.com/119678


### sp...@google.com (2024-06-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of highly mitigated memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-27)

Congratulations Han! We have decided to extend you a $1,000 thank you reward / reward for highly mitigated security bug given the speculative nature of your report that did allow us to make a security relevant change. Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2024-08-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/341313077)*

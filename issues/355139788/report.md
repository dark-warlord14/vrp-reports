# UAF in FacilitatedPaymentsPaymentMethodsControllerBridge

| Field | Value |
|-------|-------|
| **Issue ID** | [355139788](https://issues.chromium.org/issues/355139788) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | UI>Browser>Autofill>Payments |
| **Platforms** | Android |
| **Reporter** | jt...@gmail.com |
| **Assignee** | lo...@google.com |
| **Created** | 2024-07-24 |
| **Bounty** | $36,000.00 |

## Description

VULNERABILITY DETAILS
When the web content has finished loading in the primary main frame, the browser would trigger PIX code detection if kEnablePixPayments is enabled. It calls to `ChromeFacilitatedPaymentsClient::ShowPixPaymentPrompt` after validating the PIX code received from renderer [1]. This will create a Java object `FacilitatedPaymentsPaymentMethodsControllerBridge` through the following trace:
ChromeFacilitatedPaymentsClient::ShowPixPaymentPrompt
  FacilitatedPaymentsController::Show
    FacilitatedPaymentsBottomSheetBridge::RequestShowContent
      FacilitatedPaymentsBottomSheetBridge::GetJavaBridge
        FacilitatedPaymentsController::GetJavaObject
          Java_FacilitatedPaymentsPaymentMethodsControllerBridge_create

FacilitatedPaymentsPaymentMethodsControllerBridge holds a raw pointer pointing to the c++ object FacilitatedPaymentsController [2]. Although there are null checks of the native ptr before invoking JNI functions [3], there is no code to clear the ptr after FacilitatedPaymentsController is deleted, which leads to UAF when accessing the already freed FacilitatedPaymentsController through JNI call (e.g. trigger onDismissed function).

```
void FacilitatedPaymentsManager::OnApiAvailabilityReceived(
    bool is_api_available) {
  ...
  bool promptShown = client_->ShowPixPaymentPrompt(  // ===> [1]
      client_->GetPaymentsDataManager()->GetMaskedBankAccounts(),
      base::BindOnce(&FacilitatedPaymentsManager::OnPixPaymentPromptResult,
                     weak_ptr_factory_.GetWeakPtr()));
  LogFopSelectorShown(promptShown);
  if (promptShown) {
    fop_selector_shown_time_ = base::TimeTicks::Now();
  }
}

class FacilitatedPaymentsPaymentMethodsControllerBridge
        implements FacilitatedPaymentsPaymentMethodsComponent.Delegate {
    private long mNativeFacilitatedPaymentsController;  // ===> [2]

    
    // FacilitatedPaymentsPaymentMethodsComponent.Delegate
    @Override
    public void onDismissed() {
        if (mNativeFacilitatedPaymentsController != 0) {
            FacilitatedPaymentsPaymentMethodsControllerBridgeJni.get()
                    .onDismissed(mNativeFacilitatedPaymentsController);  // ===> [3]
        }
    }

```
[1] https://source.chromium.org/chromium/chromium/src/+/main:components/facilitated_payments/core/browser/facilitated_payments_manager.cc;l=274;drc=2017cd8a8925f180257662f78eaf9eb93e8e394d
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/facilitated_payments/ui/android/internal/java/src/org/chromium/chrome/browser/facilitated_payments/FacilitatedPaymentsPaymentMethodsControllerBridge.java;l=24;drc=2017cd8a8925f180257662f78eaf9eb93e8e394d
[3] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/facilitated_payments/ui/android/internal/java/src/org/chromium/chrome/browser/facilitated_payments/FacilitatedPaymentsPaymentMethodsControllerBridge.java;l=39;drc=2017cd8a8925f180257662f78eaf9eb93e8e394d

VERSION
Chrome Version: beta + dev
Operating System: Android

REPRODUCTION CASE
1. Apply the attached patch.diff, this is to simulate normal PIX code detection process, for the convenience of reproduction in the local asan environment.

2. Host poc.html at localhost
python3 -m http.server 8000
adb reverse tcp:8000 tcp:8000

3. Launch asan build chromium on Android
out/Default/bin/chrome_public_apk run --args='--enable-features=EnablePixPayments'

and navigate to http://localhost:8000/poc.html

4. Click the 'Test' button

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: browser
Crash State: see asan.log for details

== ADDITIONAL INFO ==
compromised renderer requirement: no
miracle ptr protected: no

Bisection:
This was introduces in https://chromium.googlesource.com/chromium/src/+/b351994b66e3c58623e18586f9c6e4507f6ab7ef

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 22.7 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 3.1 KB)
- [poc.html](attachments/poc.html) (text/html, 625 B)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 4.3 MB)

## Timeline

### jt...@gmail.com (2024-07-24)

Upload a repro screen recording

### ma...@chromium.org (2024-07-24)

[security shepherd]

Thanks for the detailed report!

Marking as Security\_Impact-None as the required feature `EnablePixPayments` appears to be disabled by default at this time. If this is incorrect, the bug should be removed from that hotlist.

Setting Severity to S0 as this appears to be a UAF in the browser process that is not mitigated by MiraclePtr. If there are other mitigating factors, such as the requirement that the user have configured a payment source or website allowlisting, it may be appropriate to downgrade the severity.

I'm unclear which Chromium component this bug should live in as CLs in the related code are not linked with bugs in the Chromium bug tracker.

Assigning to longsheng@ based on the bisection analysis.

### sm...@chromium.org (2024-07-29)

Thanks Mark - this is a reasonable component. (I don't think facilitated payments has its own component at this time).

Sid, Longshen - can you take a look ASAP? This is technically low priority given the feature is disabled, but it will block any rollout of EnablePixPayments. (cc irenelchang@ as fyi)

> I'm unclear which Chromium component this bug should live in as CLs in the related code are not linked with bugs in the Chromium bug tracker.

Longshen, Sid, Rouslan - this is one of the reasons we ask that CLs are tagged against bugs in Chromium components, rather than internal tracking bugs. (They can be private bugs in Chromium components, if needed). This can result in duplication of issues, which is unfortunate, but the benefit of allowing more visibility including for security triaging is very important!!

### ar...@chromium.org (2024-08-08)

*[secondary security shepherd]*

I see you're preparing a finch config: `EnablePixPayFlow.gcl`.

Just a friendly reminder: Please wait for the associated vulnerability to be fully resolved before assigning users to this experiment. This ensures a secure experience for our users, and keep this bug as `Security_Impact-None`.

[longsheng@google.com](mailto:longsheng@google.com), could you please acknowledge this bug is assigned to you? What's the current status?

### vi...@google.com (2024-08-08)

Created a CL([crrev.com/c/5774379](https://crrev.com/c/5774379))

> Longshen, Sid, Rouslan - this is one of the reasons we ask that CLs are tagged against bugs in Chromium components, rather than internal tracking bugs. (They can be private bugs in Chromium components, if needed). This can result in duplication of issues, which is unfortunate, but the benefit of allowing more visibility including for security triaging is very important!!

[smcgruer@chromium.org](mailto:smcgruer@chromium.org), do you think Facilitated Payments should be its own component, or file bugs under `Autofill > Payments` component? I can request for a new `Chromium > UI > Browser > Facilitated Payments` component to be created if former option is preferable.

### ap...@google.com (2024-08-09)

Project: chromium/src
Branch: main

commit 6278b1e477b67a57593db904a58aaeb0474850b9
Author: Vishwas Uppoor <vishwasuppoor@google.com>
Date:   Fri Aug 09 16:47:09 2024

    [PIX] Fix potential UAF of native pointer
    
    Java FacilitatedPaymentsPaymentMethodsControllerBridge has a pointer to
    the native FacilitatedPaymentsController. If the native object is
    destroyed, this could cause an UAF.
    
    Clear the native pointer when the native object is destroyed.
    
    Fixed: 355139788
    Change-Id: I33d0c9635cc232133e0819962642fd901e470186
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5774379
    Reviewed-by: Stephen McGruer <smcgruer@chromium.org>
    Commit-Queue: Vishwas Uppoor <vishwasuppoor@google.com>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: Siddharth Shah <siashah@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1339691}

M       chrome/browser/facilitated_payments/ui/android/facilitated_payments_controller.cc
M       chrome/browser/facilitated_payments/ui/android/internal/java/src/org/chromium/chrome/browser/facilitated_payments/FacilitatedPaymentsPaymentMethodsControllerBridge.java

https://chromium-review.googlesource.com/5774379


### sp...@google.com (2024-08-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $36000.00 for this report.

Rationale for this decision:
$35,000 for high quality report of demonstrated memory corruption in a non-sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### sm...@chromium.org (2024-08-14)

> [smcgruer@chromium.org](mailto:smcgruer@chromium.org), do you think Facilitated Payments should be its own component, or file bugs under Autofill > Payments component? I can request for a new Chromium > UI > Browser > Facilitated Payments component to be created if former option is preferable.

Apologies, missed this question. Filing under Autofill > Payments is fine for now imo.

### am...@chromium.org (2024-08-14)

Unrelated to the comment directly above but in ref to #8, congratulations, Rong! Always good to see more reports from you lately. :)

Finding non-mitigated and non-brp protected issues in the browser process has become increasingly difficult. While this may appear to be mildly mitigated by some interaction and preconditions to payment configuration, we feel these are very in-line with this feature at this time and glad we were able to resolve this before it impacted users. Nice finding and we appreciate your efforts and reporting this issue to us!

### pe...@google.com (2024-11-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/355139788)*

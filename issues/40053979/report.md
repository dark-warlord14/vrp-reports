# Security: UAF in PaymentResponseHelper::GeneratePaymentResponse

| Field | Value |
|-------|-------|
| **Issue ID** | [40053979](https://issues.chromium.org/issues/40053979) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Payments |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2020-11-24 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**

When users click the 'Pay' button on the PaymentRequestDialogView, a instance of `PaymentResponseHelper` will be initialized [1] in which stores a raw pointer {selected\_app\_}. In the constructor of `PaymentResponseHelper`, it will send a request to normalize the shipping address with a 5 seconds timeout [2]. Once the address is normalized or the request timeout, `PaymentResponseHelper::OnAddressNormalized` will be called which subsequently calls to `PaymentResponseHelper::GeneratePaymentResponse`. In this function, there is a virtual function call on {selected\_app\_} [3].

However, we can free {selected\_app\_} before invoking the callback function if we:

1. Fill the cvc code and click 'Confirm'.
2. Click back button and select another credit card.
3. Call `PaymentRequest::Retry` through mojo, this will free the {selected\_app\_} in PaymentResponseHelper.

After that, the invocation of `PaymentResponseHelper::OnAddressNormalized` will trigger UAF.

[1] <https://source.chromium.org/chromium/chromium/src/+/master:components/payments/content/payment_request_state.cc;l=392;drc=c6af32c989272a7388fe8b4f8dbfd571e11596b7>

[2] <https://source.chromium.org/chromium/chromium/src/+/master:components/payments/content/payment_response_helper.cc;l=53;drc=c6af32c989272a7388fe8b4f8dbfd571e11596b7>

[3] <https://source.chromium.org/chromium/chromium/src/+/master:components/payments/content/payment_response_helper.cc;l=180;drc=c6af32c989272a7388fe8b4f8dbfd571e11596b7>

**VERSION**  

Chrome Version: 87.0.4280.66 (stable)

**REPRODUCTION CASE**

(Un)fortunately, following the repro steps mentioned above would not trigger asan error in recent version of chromium. Instead, it will crash due to a WeakPtr validation check [4], which is aimed at preventing potential UAF of dereferencing an already-destroyed object (see <https://crbug.com/1146679> for more details).

This is because when clicking the 'Confirm' button, it calls to CvcUnmaskViewController::CvcConfirmed -> FullCardRequest::OnUnmaskPromptAccepted -> FullCardRequest::Reset, which invalidates the WeakPtr [5]. And when clicking the back button, it calls to CvcUnmaskViewController::BackButtonPressed which uses the already invalidated WeakPtr [6].

So my understanding is, the WeakPtr crash bug prevents the UAF bug from happening in this way (there maybe another path to trigger the UAF bug), but the UAF bug indeed exists and deserves to be fixed. :)

To trigger an asan crash easier, it is recommended to change some code in the browser side. One for killing the WeakPtr crash bug, and the other for delaying the timeout to trigger PaymentResponseHelper::OnAddressNormalized so that we can free {selected\_app\_} leisurely. See patch.diff in attachments.

[4] <https://source.chromium.org/chromium/chromium/src/+/master:base/memory/weak_ptr.h;l=255;drc=c6af32c989272a7388fe8b4f8dbfd571e11596b7>

[5] <https://source.chromium.org/chromium/chromium/src/+/master:components/autofill/core/browser/payments/full_card_request.cc;l=268;drc=c6af32c989272a7388fe8b4f8dbfd571e11596b7>

[6] <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/payments/cvc_unmask_view_controller.cc;l=370;drc=c6af32c989272a7388fe8b4f8dbfd571e11596b7>

Steps to reproduce:

1. Apply the patch.diff
2. Copy js mojo bindings and setup a HTTPServer  
   
   python ./copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/asan/gen  
   
   python -m SimpleHTTPServer
3. Run asan build chrome with MojoJS enabled  
   
   ./chrome --enable-blink-features=MojoJS <http://localhost:8000/poc.html>
4. Add two credit cards.
5. Click trigger, click 'Pay', fill the cvc code and click 'Confirm'.
6. Click back button and select another credit card. The asan error will show in several seconds.

**CREDIT INFORMATION**  

Rong Jian and Guang Gong of 360 Alpha Lab.

## Attachments

- [patch.diff](attachments/patch.diff) (text/plain, 1.3 KB)
- [poc.html](attachments/poc.html) (text/plain, 3.8 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 512 B)
- [asan.log](attachments/asan.log) (text/plain, 22.9 KB)

## Timeline

### [Deleted User] (2020-11-24)

[Empty comment from Monorail migration]

### jt...@gmail.com (2020-11-24)

[Comment Deleted]

### ct...@chromium.org (2020-11-30)

Security sheriff here: The WeakPtr crash is working-as-intended, and correctly avoids the security implications of this bug (CHECK-ing in all builds before it can dereference -- using a WeakPtr is generally the fix applied to UaF bugs).

Because of that, I think this a functional crash bug, although a compromised renderer can likely have many ways to DoS the browser. Removing this from the security queue and passing this to the Payments component to triage further.

[Monorail components: Blink>Payments]

### ro...@google.com (2020-12-01)

Will take a look.

### jt...@gmail.com (2020-12-01)

Re #3:

Sorry that I may not have expressed clearly.

There are two separate bugs. The first one is a WeakPtr crash bug, which can be triggered if one click 'Back' right after clicking 'Confirm' button. And yes this is a functional crash bug.

And the second one is a UaF bug. The root cause of this bug is the usage of a raw pointer (select_app_ in PaymentResponseHelper) in a timeout callback (PaymentResponseHelper::OnAddressNormalized) but one can free the raw pointer before triggering the callback through a Retry mojo call.

### ct...@chromium.org (2020-12-01)

Thanks for the added details and sorry for misunderstanding your report. Adding back the view restrictions for now and I'll triage this further tomorrow. It sounds like the second issue may be reachable via a compromised renderer (although the only current way you know to trigger it got stopped by the WeakPtr check), so agreed that we should address that.

Thanks rouslan@ for jumping on this bug in the meantime :-)

### ct...@chromium.org (2020-12-01)

[Empty comment from Monorail migration]

### ct...@chromium.org (2020-12-01)

Adding security labels: Setting Severity-High as it seems plausible the UAF is still reachable via a compromised renderer.

### ro...@chromium.org (2020-12-02)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a7d72a53216a615dcbd2a3855a52fd6871aad949

commit a7d72a53216a615dcbd2a3855a52fd6871aad949
Author: Rouslan Solomakhin <rouslan@chromium.org>
Date: Wed Dec 02 23:05:33 2020

[Web Payment] Store PaymentApp and WebContents safely.

Before this patch, the pointers to PaymentApp or WebContents could
become null or invalidated under some circumstances and cause a crash or
UaF.

This patch changes member variable PaymentApp pointers to use its
WeakPtr instead and checks the validity of the WeakPtr before using it,
as well as storing a GlobalFrameRoutingId in CvcUnmaskViewController.

After this patch, a null or invalidated reference to PaymentApp or
WebContents does not cause a crash or a UaF.

Bug: 1152334
Change-Id: Iad8678462980d203fd440d991c8e9d7e5ecc7abe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2566618
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Reviewed-by: Liquan (Max) Gu <maxlg@chromium.org>
Cr-Commit-Position: refs/heads/master@{#833025}

[modify] https://crrev.com/a7d72a53216a615dcbd2a3855a52fd6871aad949/chrome/browser/ui/views/payments/cvc_unmask_view_controller.cc
[modify] https://crrev.com/a7d72a53216a615dcbd2a3855a52fd6871aad949/chrome/browser/ui/views/payments/cvc_unmask_view_controller.h
[modify] https://crrev.com/a7d72a53216a615dcbd2a3855a52fd6871aad949/chrome/browser/ui/views/payments/payment_method_view_controller.cc
[modify] https://crrev.com/a7d72a53216a615dcbd2a3855a52fd6871aad949/components/payments/content/payment_request_state.cc
[modify] https://crrev.com/a7d72a53216a615dcbd2a3855a52fd6871aad949/components/payments/content/payment_request_state.h
[modify] https://crrev.com/a7d72a53216a615dcbd2a3855a52fd6871aad949/components/payments/content/payment_response_helper.cc
[modify] https://crrev.com/a7d72a53216a615dcbd2a3855a52fd6871aad949/components/payments/content/payment_response_helper.h
[modify] https://crrev.com/a7d72a53216a615dcbd2a3855a52fd6871aad949/components/payments/content/payment_response_helper_unittest.cc


### ro...@chromium.org (2020-12-03)

jtrrodant@ - could you please verify the bug fix? Thank you.

### [Deleted User] (2020-12-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-03)

Requesting merge to stable M87 because latest trunk commit (833025) appears to be after stable branch point (812852).

Requesting merge to beta M87 because latest trunk commit (833025) appears to be after beta branch point (812852).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-03)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@chromium.org (2020-12-03)

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

Yes.

2. Links to the CLs you are requesting to merge.

https://crrev.com/c/2566618

3. Has the change landed and been verified on ToT?

Yes.

4. Does this change need to be merged into other active release branches (M-1, M+1)?

Yes: M-88.

5. Why are these changes required in this milestone after branch?

Fixing a UaF in the browser that's possible to trigger with a compromised renderer.

6. Is this a new feature?

No.

7. If it is a new feature, is it behind a flag using finch?

N/A.

### jt...@gmail.com (2020-12-04)

Re #11

Applied the patch and tested the poc again. The fix prevents {selected_app_} UaF from happening ; ) 

### ro...@chromium.org (2020-12-04)

Thank you for verifying!

### ro...@chromium.org (2020-12-04)

[Empty comment from Monorail migration]

### ro...@chromium.org (2020-12-04)

adetaylor@ - should this be merged to M-87 too, or only M-88?

### ad...@chromium.org (2020-12-04)

Sheriffbot messed up the merge requests here (for known reasons which are recorded in a bug somewhere) so approving merge to M88, branch 4324.

As to M87, it's probable that I will approve merge to M87 in a couple of days, but there are some issues with Android releasing right now so the branch is effectively closed.

### go...@chromium.org (2020-12-04)

Please merge your change to M88 branch 4324 ASAP. Thank you.

### ro...@chromium.org (2020-12-04)

It's in the queue: https://crrev.com/c/2575339

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bf59fe706c0eb2df6d0e8536ec729beb392f104d

commit bf59fe706c0eb2df6d0e8536ec729beb392f104d
Author: Rouslan Solomakhin <rouslan@chromium.org>
Date: Fri Dec 04 20:39:11 2020

[Merge M-88][Web Payment] Store PaymentApp and WebContents safely.

Before this patch, the pointers to PaymentApp or WebContents could
become null or invalidated under some circumstances and cause a crash or
UaF.

This patch changes member variable PaymentApp pointers to use its
WeakPtr instead and checks the validity of the WeakPtr before using it,
as well as storing a GlobalFrameRoutingId in CvcUnmaskViewController.

After this patch, a null or invalidated reference to PaymentApp or
WebContents does not cause a crash or a UaF.

(cherry picked from commit a7d72a53216a615dcbd2a3855a52fd6871aad949)

Bug: 1152334
Change-Id: Iad8678462980d203fd440d991c8e9d7e5ecc7abe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2566618
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Reviewed-by: Liquan (Max) Gu <maxlg@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#833025}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2575339
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#602}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/bf59fe706c0eb2df6d0e8536ec729beb392f104d/chrome/browser/ui/views/payments/cvc_unmask_view_controller.cc
[modify] https://crrev.com/bf59fe706c0eb2df6d0e8536ec729beb392f104d/chrome/browser/ui/views/payments/cvc_unmask_view_controller.h
[modify] https://crrev.com/bf59fe706c0eb2df6d0e8536ec729beb392f104d/chrome/browser/ui/views/payments/payment_method_view_controller.cc
[modify] https://crrev.com/bf59fe706c0eb2df6d0e8536ec729beb392f104d/components/payments/content/payment_request_state.cc
[modify] https://crrev.com/bf59fe706c0eb2df6d0e8536ec729beb392f104d/components/payments/content/payment_request_state.h
[modify] https://crrev.com/bf59fe706c0eb2df6d0e8536ec729beb392f104d/components/payments/content/payment_response_helper.cc
[modify] https://crrev.com/bf59fe706c0eb2df6d0e8536ec729beb392f104d/components/payments/content/payment_response_helper.h
[modify] https://crrev.com/bf59fe706c0eb2df6d0e8536ec729beb392f104d/components/payments/content/payment_response_helper_unittest.cc


### ad...@google.com (2020-12-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-10)

Congratulations, the VRP panel has awarded $15,000 for this bug.

### ad...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-11)

Approving merge to M87, branch 4280.

### ro...@chromium.org (2020-12-12)

Running bots @ https://crrev.com/c/2587460.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d7170da0816ba3066453a8fef1e02c10a8f8db7f

commit d7170da0816ba3066453a8fef1e02c10a8f8db7f
Author: Rouslan Solomakhin <rouslan@chromium.org>
Date: Sat Dec 12 13:54:58 2020

[Merge M-87][Web Payment] Store PaymentApp and WebContents safely.

Before this patch, the pointers to PaymentApp or WebContents could
become null or invalidated under some circumstances and cause a crash or
UaF.

This patch changes member variable PaymentApp pointers to use its
WeakPtr instead and checks the validity of the WeakPtr before using it,
as well as storing a GlobalFrameRoutingId in CvcUnmaskViewController.

After this patch, a null or invalidated reference to PaymentApp or
WebContents does not cause a crash or a UaF.

(cherry picked from commit a7d72a53216a615dcbd2a3855a52fd6871aad949)

Bug: 1152334
Change-Id: Iad8678462980d203fd440d991c8e9d7e5ecc7abe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2566618
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Reviewed-by: Liquan (Max) Gu <maxlg@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#833025}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2587460
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#1865}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/d7170da0816ba3066453a8fef1e02c10a8f8db7f/components/payments/content/payment_response_helper.h
[modify] https://crrev.com/d7170da0816ba3066453a8fef1e02c10a8f8db7f/chrome/browser/ui/views/payments/cvc_unmask_view_controller.h
[modify] https://crrev.com/d7170da0816ba3066453a8fef1e02c10a8f8db7f/components/payments/content/payment_response_helper.cc
[modify] https://crrev.com/d7170da0816ba3066453a8fef1e02c10a8f8db7f/chrome/browser/ui/views/payments/cvc_unmask_view_controller.cc
[modify] https://crrev.com/d7170da0816ba3066453a8fef1e02c10a8f8db7f/components/payments/content/payment_request_state.cc
[modify] https://crrev.com/d7170da0816ba3066453a8fef1e02c10a8f8db7f/components/payments/content/payment_response_helper_unittest.cc
[modify] https://crrev.com/d7170da0816ba3066453a8fef1e02c10a8f8db7f/chrome/browser/ui/views/payments/payment_method_view_controller.cc
[modify] https://crrev.com/d7170da0816ba3066453a8fef1e02c10a8f8db7f/components/payments/content/payment_request_state.h


### ad...@google.com (2021-01-05)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-06)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-01-08)

[Empty comment from Monorail migration]

### ke...@google.com (2021-01-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@chromium.org (2021-01-12)

achuith@ - Are you mergin to 86-TLS? I'm not sure where that branch is located.

### [Deleted User] (2021-01-15)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-01-27)

[Empty comment from Monorail migration]

### gi...@google.com (2021-02-23)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0d223e17434c08c0f2a35912e67ead4c89a0b841

commit 0d223e17434c08c0f2a35912e67ead4c89a0b841
Author: Rouslan Solomakhin <rouslan@chromium.org>
Date: Wed Mar 10 16:39:28 2021

[Merge M86-LTS][Web Payment] Store PaymentApp and WebContents safely.

Before this patch, the pointers to PaymentApp or WebContents could
become null or invalidated under some circumstances and cause a crash or
UaF.

This patch changes member variable PaymentApp pointers to use its
WeakPtr instead and checks the validity of the WeakPtr before using it,
as well as storing a GlobalFrameRoutingId in CvcUnmaskViewController.

After this patch, a null or invalidated reference to PaymentApp or
WebContents does not cause a crash or a UaF.

(cherry picked from commit a7d72a53216a615dcbd2a3855a52fd6871aad949)

(cherry picked from commit d7170da0816ba3066453a8fef1e02c10a8f8db7f)

Bug: 1152334
Change-Id: Iad8678462980d203fd440d991c8e9d7e5ecc7abe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2566618
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Reviewed-by: Liquan (Max) Gu <maxlg@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#833025}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2587460
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4280@{#1865}
Cr-Original-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2617108
Auto-Submit: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1571}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/0d223e17434c08c0f2a35912e67ead4c89a0b841/chrome/browser/ui/views/payments/cvc_unmask_view_controller.cc
[modify] https://crrev.com/0d223e17434c08c0f2a35912e67ead4c89a0b841/chrome/browser/ui/views/payments/cvc_unmask_view_controller.h
[modify] https://crrev.com/0d223e17434c08c0f2a35912e67ead4c89a0b841/chrome/browser/ui/views/payments/payment_method_view_controller.cc
[modify] https://crrev.com/0d223e17434c08c0f2a35912e67ead4c89a0b841/components/payments/content/payment_request_state.cc
[modify] https://crrev.com/0d223e17434c08c0f2a35912e67ead4c89a0b841/components/payments/content/payment_request_state.h
[modify] https://crrev.com/0d223e17434c08c0f2a35912e67ead4c89a0b841/components/payments/content/payment_response_helper.cc
[modify] https://crrev.com/0d223e17434c08c0f2a35912e67ead4c89a0b841/components/payments/content/payment_response_helper.h
[modify] https://crrev.com/0d223e17434c08c0f2a35912e67ead4c89a0b841/components/payments/content/payment_response_helper_unittest.cc


### as...@google.com (2021-03-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1152334?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053979)*

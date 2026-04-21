# Security: UAF in AppFinder::OnGetAppDescriptions

| Field | Value |
|-------|-------|
| **Issue ID** | [40063010](https://issues.chromium.org/issues/40063010) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Payments |
| **Platforms** | Android |
| **Reporter** | jt...@gmail.com |
| **Assignee** | sm...@chromium.org |
| **Created** | 2023-02-10 |
| **Bounty** | $30,000.00 |

## Description

**VULNERABILITY DETAILS**  

Summary:  

The function `AppFinder::OnGetAppDescriptions` may synchronously call `AppFinder::OnIsReadyToPay` in a for loop. This may result in this AppFinder object to be deleted, which causes UAF.

Details:  

When initializing a PaymentRequest on Android platform (or ChromeOS with TWA payment apps), it calls to `AndroidPaymentAppFactory::Create` and create an instance of AppFinder to find payment apps. The AppFinder is owned by WebContents and will delete itself in `AppFinder::OnDoneCreatingPaymentApps` [1].

In the process of finding apps, it will call the function `AppFinder::OnGetAppDescriptions`. Consider the following scenario:

1. There are more than one app description in the vector single\_activity\_apps, it will then iterate over each item of this vector and query whether it is ready to pay
2. The iteration loop could synchronously call `AppFinder::OnIsReadyToPay` at line [2], which may call `AppFinder::OnDoneCreatingPaymentApps` [3]
3. `AppFinder::OnDoneCreatingPaymentApps` delete this object and return. However, the for loop does not end and will access the already freed memory at [4], which causes UAF.

In order to meet the conditions above, we need to make sure that both delegate\_ and delegate\_->GetSpec() are valid when calling `OnGetAppDescriptions`, otherwise the function will return at the beginning. We also need to make sure that the RenderFrameHost which initializes the PaymentRequest is gone, thus `OnIsReadyToPay` can call `OnDoneCreatingPaymentApps` to delete AppFinder. Fortunately the Android implementation of the interface PaymentRequest is not a DocumentService, so its lifetime is not bound to the RenderFrameHost. We can keep the messagepipe alive while delete the RenderFrameHost.

```
void OnDoneCreatingPaymentApps() {  
  if (delegate_)  
    delegate_->OnDoneCreatingPaymentApps();  
  
  owner_->RemoveUserData(this);  // ===> [1] delete this  
}  
  
void OnGetAppDescriptions(  
    const absl::optional<std::string>& error_message,  
    std::vector<std::unique_ptr<AndroidAppDescription>> app_descriptions) {  
  DCHECK_CURRENTLY_ON(content::BrowserThread::UI);  
  // The browser could be shutting down.  
  if (!communication_ || !delegate_ || !delegate_->GetSpec())  
    return;  
  
  // ...skip  
    
  
  number_of_pending_is_ready_to_pay_queries_ = single_activity_apps.size();  
  if (number_of_pending_is_ready_to_pay_queries_ == 0U) {  
    OnDoneCreatingPaymentApps();  
    return;  
  }  
  
  for (size_t i = 0; i < single_activity_apps.size(); ++i) {  
    // ...skip  
    std::unique_ptr<std::map<std::string, std::set<std::string>>>  
    stringified_method_data = data_util::FilterStringifiedMethodData(  
        delegate_->GetSpec()->stringified_method_data(),   // ===> [4]  
        supported_payment_methods);  
  
    if (delegate_->IsOffTheRecord() ||  
        single_activity_app->service_names.empty()) {  
      OnIsReadyToPay(std::move(single_activity_app), payment_method_names,  // ===> [2]  
                      std::move(stringified_method_data),  
                      /\*error_message=\*/absl::nullopt,  
                      /\*is_ready_to_pay=\*/true);  
      continue;  
    }  
  
    // ...skip  
  }  
}  
  
void OnIsReadyToPay() {  
  // The browser could be shutting down.  
  if (!communication_ || !delegate_ || !delegate_->GetSpec() ||  
      !delegate_->GetInitiatorRenderFrameHost()) {  
    OnDoneCreatingPaymentApps();  // ===> [3]  
    return;  
  }  
  // ...skip  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/payments/content/android_payment_app_factory.cc;l=216;drc=0c4306fc554c80506eb0f9b833a5d2a5fdd452d5>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:components/payments/content/android_payment_app_factory.cc;l=157;drc=0c4306fc554c80506eb0f9b833a5d2a5fdd452d5>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:components/payments/content/android_payment_app_factory.cc;l=193;drc=0c4306fc554c80506eb0f9b833a5d2a5fdd452d5>  

[4] <https://source.chromium.org/chromium/chromium/src/+/main:components/payments/content/android_payment_app_factory.cc;l=147;drc=0c4306fc554c80506eb0f9b833a5d2a5fdd452d5>

**VERSION**  

Chrome Version: 110.0.5481.63/.64 (stable) + dev  

Operating System: Android, ChromeOS

**REPRODUCTION CASE**

1. Apply the attached path.diff, this is to add app descriptions and delay one of the posted task, for the convenience of reproduction in the local asan environment
2. Comiple & Copy js mojo bindings  
   
   ninja -C /path/to/chrome/.../out/asan third\_party/blink/public/mojom:android\_mojo\_bindings\_js  
   
   (at your working directory)  
   
   mkdir mojo && cd mojo && python3 copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/asan/gen
3. Host poc.html and mojo files at localhost  
   
   (at your working directory)  
   
   python3 -m http.server 8000  
   
   adb reverse tcp:8000 tcp:8000
4. Launch android asan chromium with mojo enabled (--enable-blink-features=MojoJS,MojoJSTest) and navigate to <http://localhost:8000/poc.html>

\*\*Fix Suggestion\*\*  

Sync the shutting down check in `OnGetAppDescriptions` with the check in `OnIsReadyToPay`, so that `OnGetAppDescriptions` can return early instead of having a chance to call `OnIsReadyToPay` synchronously.

diff --git a/components/payments/content/android\_payment\_app\_factory.cc b/components/payments/content/android\_payment\_app\_factory.cc  

index 42a1a48944b35..db4c8a070e43a 100644  

--- a/components/payments/content/android\_payment\_app\_factory.cc  

+++ b/components/payments/content/android\_payment\_app\_factory.cc  

@@ -97,7 +109,7 @@ class AppFinder : public base::SupportsUserData::Data {  

std::vector<std::unique\_ptr<AndroidAppDescription>> app\_descriptions) {  

DCHECK\_CURRENTLY\_ON(content::BrowserThread::UI);  

// The browser could be shutting down.

- if (!communication\_ || !delegate\_ || !delegate\_->GetSpec())

- if (!communication\_ || !delegate\_ || !delegate\_->GetSpec() || !delegate\_->GetInitiatorRenderFrameHost())  
  
  return;
  
  if (error\_message.has\_value()) {

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan.log

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 63.8 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 512 B)
- [patch.diff](attachments/patch.diff) (text/plain, 3.0 KB)
- [poc.html](attachments/poc.html) (text/plain, 3.2 KB)

## Timeline

### [Deleted User] (2023-02-10)

[Empty comment from Monorail migration]

### ma...@google.com (2023-02-11)

Thanks for the report!

+smcgruer@. Could you help me repro this and evaluate whether this a reachable or exploitable issue?

Tentatively marking this Severity-Critical, since it's browser process UAF without any mitigating factors such as required user interaction; setting FoundIn-110 per reporter's assessment.

### [Deleted User] (2023-02-11)

[Empty comment from Monorail migration]

### ma...@google.com (2023-02-11)

> Tentatively marking this Severity-Critical
Ah, but the compromised renderer necessary for MojoJS makes it Sev-High.

### [Deleted User] (2023-02-12)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-12)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-12)

[Empty comment from Monorail migration]

### sm...@chromium.org (2023-02-13)

Thanks for the report, will start digging into it.

[Monorail components: Blink>Payments]

### sm...@chromium.org (2023-02-13)

[Empty comment from Monorail migration]

### sm...@chromium.org (2023-02-13)

[Empty comment from Monorail migration]

### sm...@chromium.org (2023-02-13)

Thanks for the report (and great quality!).

The UAF is definitely valid *if* we can end up in a state where the RenderFrameHost is null but the AndroidAppCommunication and PaymentAppFactory::Delegate are not. This is technically possible due to the ownership structure, but I'm not sure if it's feasible without a renderer bypass. So in the absence of evidence that it is, I'm going to consider this as requiring renderer bypass.

I have an immediate fix in review currently, and then we will need to additionally dig into a few additional details that I've laid out in https://docs.google.com/document/d/1aDDk1FJNklG4KYqi9U65bTJ6Ktm174mA9v-G7e4BZL0/edit?resourcekey=0-RFALbuFl1pNgpcHd8tnf_g# (internal team-visible only, sorry :)).

### gi...@appspot.gserviceaccount.com (2023-02-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f06f8ce3044f265d15ebda7578a76625d45df8f0

commit f06f8ce3044f265d15ebda7578a76625d45df8f0
Author: Stephen McGruer <smcgruer@chromium.org>
Date: Mon Feb 13 23:33:52 2023

[WebPayments] Unify early exits in AndroidPaymentAppFactory

This CL corrects an issue where AppFinder::OnGetAppDescriptions had a
different early-exit check than AppFinder::IsReadyToPay. This could
cause OnGetAppDescriptions to reach AppFinder::OnDoneCreatingPaymentApps
and delete the current instance whilst it was still in use.

A test is added that exercises the failing path before the fix.

Bug: 1414738
Change-Id: I31dd8a62a83acf60412df1d055aeba311f2df430
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4245784
Reviewed-by: Nick Burris <nburris@chromium.org>
Commit-Queue: Stephen McGruer <smcgruer@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1104754}

[add] https://crrev.com/f06f8ce3044f265d15ebda7578a76625d45df8f0/components/payments/content/mock_android_app_communication.cc
[add] https://crrev.com/f06f8ce3044f265d15ebda7578a76625d45df8f0/components/payments/content/mock_android_app_communication.h
[modify] https://crrev.com/f06f8ce3044f265d15ebda7578a76625d45df8f0/components/payments/content/android_payment_app_factory.cc
[modify] https://crrev.com/f06f8ce3044f265d15ebda7578a76625d45df8f0/components/payments/content/android_payment_app_factory_unittest.cc
[modify] https://crrev.com/f06f8ce3044f265d15ebda7578a76625d45df8f0/components/payments/content/BUILD.gn


### sm...@chromium.org (2023-02-14)

Above CL landed in 112.0.5595.0, and any release after that should no longer have the immediate UAF. There is some immediate follow-on work in the document (auditing other transitive callsites of OnDoneCreatingPaymentApps), which I will hold this bug open until I complete (expected soon). After that, there is longer term work that we will file follow-on bugs for.

Reporter - I was never able to reproduce this using your original approach (hosting the mojoJS file/etc), only by examining the code and writing a specific unittest for the code. If you are able to reproduce and can retry with 112.0.5595.0 or higher, that would be great :)

### sm...@chromium.org (2023-02-14)

We have completed the audit of OnDoneCreatingPaymentApps callsites and believe that after https://crbug.com/chromium/1414738#c12 they are technically safe, albeit still risky in their design. Have opened a bug to track follow on work (https://crbug.com/chromium/1416187), so closing this as believed Fixed (pending verification from original reporter), and will be requesting merge back.

Amy - can you guidance on how far back we should merge a fix here, for a browser UAF that we believe requires renderer compromise first? I.e., just to Beta, or all the way to Stable respin? (The issue has existed for a long time, probably introduced in early 2020 based on some code archaeology)

### [Deleted User] (2023-02-14)

[Empty comment from Monorail migration]

### ma...@google.com (2023-02-14)

Not Amy, but

> can you guidance on how far back we should merge a fix here, for a browser UAF that we believe requires renderer compromise first? I.e., just to Beta, or all the way to Stable respin?

I think sheriffbot should take care of that automatically based on the Severity and FoundIn labels. I.e., you don't need to manually request any merges here.


### am...@chromium.org (2023-02-14)

Hi Stephen, absolutely -- and thank you for fixing this bug so quickly! 
Browser UAFs can potentially result in a sandbox escape, as such, without the precondition of a compromised renderer this would be a critical severity bug. Since this does require a renderer compromise to exploit, it's a high-severity bug and as such should be backmerged to all the way Stable (M110). 

Since you're waiting on verification and this need some backtime on Canary first, there's not rush here. As long as there are no issues, this fix would just need to be backmerged by EOD Thursday to ensure your patch makes it into the next Stable respin.
Thanks for closing this as fixed in the interim! This allow the bot to do it's job too, and it should be along shortly to add the merge review labels for M111/beta and M110/stable. This get into the queue for me to come back around after some bake time to review for merge. 

>>> (The issue has existed for a long time, probably introduced in early 2020 based on some code archaeology)
This does doesn't impact backmerge decisions. We'll want to backmerge the patch for next Stable respin, given the severity and security impact in order to reduce the potential for n-day exploitation (see go/cott-32 for more info :)) 


### [Deleted User] (2023-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-14)

Requesting merge to stable M110 because latest trunk commit (1104754) appears to be after stable branch point (1084008).

Requesting merge to beta M111 because latest trunk commit (1104754) appears to be after beta branch point (1097615).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-14)

Merge review required: M111 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-14)

Merge review required: M110 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jt...@gmail.com (2023-02-15)

Re #13:
Retried the PoC with the CL [1] applied, and I think it's been fixed  : )

[1] https://chromium-review.googlesource.com/c/chromium/src/+/4245784

### sm...@chromium.org (2023-02-16)

Thanks jtrrodant@ for confirming! :)

 I guess I'm meant to fill out the merge  survey, so:

1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

For M110: Severity-High security issue, merge requested by security team
For M111: security issue

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/4245784

3. Have the changes been released and tested on canary?

Yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

Not a new feature, bug fix in very old feature :)

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A, I think (not a Chrome OS change?)

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

I think no, because of jtrrodant@'s work to verify. But Amy may override me and say yes :).

### am...@chromium.org (2023-02-16)

everything looks good here since canary bake time
M111 merge approved, please merge to branch 5563 at your earliest convenience 
M110 merge approved, please merge to branch 5481 by EOD today / no later than 9am Pacific tomorrow so this fix can be included in next week's Stable/110 security refresh -- ty! 

### gi...@appspot.gserviceaccount.com (2023-02-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ff1a6b756893496db6d5de67ad6186d6626157b8

commit ff1a6b756893496db6d5de67ad6186d6626157b8
Author: Stephen McGruer <smcgruer@chromium.org>
Date: Thu Feb 16 22:49:26 2023

[WebPayments] Unify early exits in AndroidPaymentAppFactory

(M111 merge)

This CL corrects an issue where AppFinder::OnGetAppDescriptions had a
different early-exit check than AppFinder::IsReadyToPay. This could
cause OnGetAppDescriptions to reach AppFinder::OnDoneCreatingPaymentApps
and delete the current instance whilst it was still in use.

A test is added that exercises the failing path before the fix.

(cherry picked from commit f06f8ce3044f265d15ebda7578a76625d45df8f0)

Bug: 1414738
Change-Id: I31dd8a62a83acf60412df1d055aeba311f2df430
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4245784
Reviewed-by: Nick Burris <nburris@chromium.org>
Commit-Queue: Stephen McGruer <smcgruer@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1104754}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4262695
Auto-Submit: Stephen McGruer <smcgruer@chromium.org>
Commit-Queue: Nick Burris <nburris@chromium.org>
Cr-Commit-Position: refs/branch-heads/5563@{#551}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[add] https://crrev.com/ff1a6b756893496db6d5de67ad6186d6626157b8/components/payments/content/mock_android_app_communication.cc
[add] https://crrev.com/ff1a6b756893496db6d5de67ad6186d6626157b8/components/payments/content/mock_android_app_communication.h
[modify] https://crrev.com/ff1a6b756893496db6d5de67ad6186d6626157b8/components/payments/content/android_payment_app_factory.cc
[modify] https://crrev.com/ff1a6b756893496db6d5de67ad6186d6626157b8/components/payments/content/android_payment_app_factory_unittest.cc
[modify] https://crrev.com/ff1a6b756893496db6d5de67ad6186d6626157b8/components/payments/content/BUILD.gn


### am...@google.com (2023-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-17)

Congratulations, Rong! The VRP Panel has decided to award you $30,000 for this report + $1,000 patch bonus. Thank you for your efforts in discovering and reporting this issue to us -- excellent work! 

### gi...@appspot.gserviceaccount.com (2023-02-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a88bdd614efaf3c1022148116fb831cff2cf7ac6

commit a88bdd614efaf3c1022148116fb831cff2cf7ac6
Author: Stephen McGruer <smcgruer@chromium.org>
Date: Fri Feb 17 13:55:16 2023

[WebPayments] Unify early exits in AndroidPaymentAppFactory

(M110 merge)

This CL corrects an issue where AppFinder::OnGetAppDescriptions had a
different early-exit check than AppFinder::IsReadyToPay. This could
cause OnGetAppDescriptions to reach AppFinder::OnDoneCreatingPaymentApps
and delete the current instance whilst it was still in use.

A test is added that exercises the failing path before the fix.

(cherry picked from commit f06f8ce3044f265d15ebda7578a76625d45df8f0)

Bug: 1414738
Change-Id: I31dd8a62a83acf60412df1d055aeba311f2df430
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4245784
Reviewed-by: Nick Burris <nburris@chromium.org>
Commit-Queue: Stephen McGruer <smcgruer@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1104754}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4262809
Auto-Submit: Stephen McGruer <smcgruer@chromium.org>
Cr-Commit-Position: refs/branch-heads/5481@{#1165}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[add] https://crrev.com/a88bdd614efaf3c1022148116fb831cff2cf7ac6/components/payments/content/mock_android_app_communication.cc
[add] https://crrev.com/a88bdd614efaf3c1022148116fb831cff2cf7ac6/components/payments/content/mock_android_app_communication.h
[modify] https://crrev.com/a88bdd614efaf3c1022148116fb831cff2cf7ac6/components/payments/content/android_payment_app_factory.cc
[modify] https://crrev.com/a88bdd614efaf3c1022148116fb831cff2cf7ac6/components/payments/content/android_payment_app_factory_unittest.cc
[modify] https://crrev.com/a88bdd614efaf3c1022148116fb831cff2cf7ac6/components/payments/content/BUILD.gn


### am...@google.com (2023-02-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-20)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-21)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1414738?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063010)*

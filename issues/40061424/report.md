# uaf in FederatedAuthRequestimpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40061424](https://issues.chromium.org/issues/40061424) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Identity>FedCM |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ta...@chromium.org |
| **Created** | 2022-10-20 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

1、Download all attachment.  

2、mkdir .well-known;mkdir fedcm1  

3、mv web-identity .well-known/web-identity  

4、cp -R web-identity1 fedcm1/.well-known;cp fedcm.json fedcm1/  

5、python -m SimpleHTTPServer 8000; python -m SimpleHTTPServer 8001;(in fedcm1)  

6、enable FedCmMultipleIdentityProviders and FedCM Sign-in status  

7、out/asan/chrome <http://localhost:8000/poc.html>  

8、Once the dialog show. Close it and uaf happen

**Problem Description:**  

Inspired by <https://bugs.chromium.org/p/chromium/issues/detail?id=1349322>. Similar to the same bug I submited before(<https://bugs.chromium.org/p/chromium/issues/detail?id=1375021>). In FederatedAuthRequestimpl::OnAccountsResponseReceived[1]. HandleAccountsFetchFailure[2] will ShowFailureDialog[3].

That means if navigator.credentials.get pass multiple IDP in one request. When Two or more than two server response it with the legal fedcm.json and .well-known/web-identity but with illegal accounts. Then ShowFailureDialog will call multiple times and create multiple dialog.

Create multiple dialog cause the reassign of bubble\_widget\_[4]. Reassign will result in when the FedCmAccountSelectionView destruction. It will not notice the previous bubble\_widget\_ . Lead to uaf when the previous bubble\_widget accessing FedCmAccountSelectionView.

[1]  

<https://source.chromium.org/chromium/chromium/src/+/main:content/browser/webid/federated_auth_request_impl.cc;l=905;drc=6c98208a4b42812f0ae40fc88ad94654bce31ec6;bpv=1;bpt=1>

[2]  

<https://source.chromium.org/chromium/chromium/src/+/main:content/browser/webid/federated_auth_request_impl.cc;l=913;drc=6c98208a4b42812f0ae40fc88ad94654bce31ec6;bpv=1;bpt=1>

[3]  

<https://source.chromium.org/chromium/chromium/src/+/main:content/browser/webid/federated_auth_request_impl.cc;l=896;drc=6c98208a4b42812f0ae40fc88ad94654bce31ec6;bpv=0;bpt=1>

[4]  

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc;l=87;drc=21a4c84dd469bfdc9f27375133dc309b62101ef8;bpv=1;bpt=1>

**Additional Comments:**  

This is a browser uaf without compromised renderer. Only need a simple click which user will easily click to close the dialog.

\*\*Chrome version: \*\* 106.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [web-identity](attachments/web-identity) (text/plain, 85 B)
- [web-identity1](attachments/web-identity1) (text/plain, 85 B)
- [fedcm.json](attachments/fedcm.json) (text/plain, 262 B)
- [asan.txt](attachments/asan.txt) (text/plain, 73.1 KB)
- [poc.html](attachments/poc.html) (text/plain, 732 B)

## Timeline

### [Deleted User] (2022-10-20)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-10-20)

+tanzachary, can you please take a look?

[Monorail components: Blink>Identity>FedCM]

### ta...@chromium.org (2022-10-21)

Sure thing, thanks for reporting and assigning.

### ke...@chromium.org (2022-10-21)

dominickn@: Should this be Sev-Critical?

### ta...@chromium.org (2022-10-21)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-10-23)

#4: I based the triage on https://bugs.chromium.org/p/chromium/issues/detail?id=1375021, which was Sev-High. However, I think you're right it should be updated, thanks for checking.

Impact remains none as this is a disabled feature.

### gi...@appspot.gserviceaccount.com (2022-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5b8cca4ade32df643a5de795f963d51e3f1f26bf

commit 5b8cca4ade32df643a5de795f963d51e3f1f26bf
Author: Zachary Tan <tanzachary@chromium.org>
Date: Thu Nov 10 03:25:19 2022

[FedCM] Disallow multiple FedCM dialogs to be shown

Bug: 1376995, 1375021
Change-Id: I27876364afb4c939fca72c510d79fc834c8451ae
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4003805
Reviewed-by: Yi Gu <yigu@chromium.org>
Commit-Queue: Zachary Tan <tanzachary@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1069560}

[modify] https://crrev.com/5b8cca4ade32df643a5de795f963d51e3f1f26bf/content/browser/webid/federated_auth_request_impl.cc
[modify] https://crrev.com/5b8cca4ade32df643a5de795f963d51e3f1f26bf/chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc


### ta...@chromium.org (2022-11-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-10)

[Empty comment from Monorail migration]

### np...@chromium.org (2022-11-10)

Bug reporter, could you confirm if you see this fixed on your end? I think this was a speculative fix.  The fix is not yet in any Chrome version so we can wait until the next Canary containing the fix is released.

### ha...@gmail.com (2022-11-11)

I had test the fix in my personal build chromium and confirm it works well. Thanks for the fix!

### am...@google.com (2022-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-17)

Congratulations! The VRP Panel has decided to award you $7,000 for this report of a mildly mitigated security bug + $3,000 renderer bonus. A member of our finance team will be in touch with you soon to arrange payment. In the interim, please let us know what name/handle/other identifier you would like us to use in acknowledging you for this issue. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@chromium.org (2022-11-17)

While I am here and following VRP assessment, adjusting severity to high due to this issue requiring a bit of user gesture to trigger based on this report. 

### am...@google.com (2022-11-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-02-16)

This issue was migrated from crbug.com/chromium/1376995?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-25)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061424)*

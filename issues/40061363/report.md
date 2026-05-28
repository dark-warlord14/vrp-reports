# uaf in FederatedAuthRequestImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40061363](https://issues.chromium.org/issues/40061363) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Identity>FedCM |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ta...@chromium.org |
| **Created** | 2022-10-15 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**  

1.Download all attachment.  

2.mkdir .well-known  

3.mv web-identity .well-known/web-identity  

4.python -m SimpleHTTPServer 8000  

5.out/asan/chrome --enable-features=FedCmMultipleIdentityProviders [http://localhost:8000/poc.html](http://localhost:8081/poc_parent.html)  

6.click anywhere(not only close show in the poc.mp4) in the show dialog and uaf happen.

**Problem Description:**  

In FederatedAuthRequestImpl::MaybeShowAccountsDialog[1]. It will ShowAccountsDialog[2] if pending\_idps\_.empty() is true. This situation will reach when all request are finish.

pending\_idps\_[3] is from FederatedAuthrequestImpl::RequestToken. It use idp\_ptr->config\_url as the key to insert value. idp\_ptrs can be controlled by user through dom api navigator.credentials.get. Thus if a user pass multiple idp\_ptr with the same config\_url. pending\_idps\_. Insert will fail because of the duplicate key. Which will make when not all request are finish, pending\_idps\_.empty() is still true. Then the ShowAccountsDialog will call multiple times and create multiple dialog.

Create multiple dialog cause the reassign of bubble\_widget\_[4]. Reassign will result in when the FedCmAccountSelectionView destruction. It will not notice the previous bubble\_widget\_ . Lead to uaf when the previous bubble\_widget accessing FedCmAccountSelectionView.

[1]  

<https://source.chromium.org/chromium/chromium/src/+/main:content/browser/webid/federated_auth_request_impl.cc;l=794;bpv=1;bpt=1?q=FederatedAuthRequestImpl::MaybeShowAccountsDialog&ss=chromium%2Fchromium%2Fsrc>

[2]

<https://source.chromium.org/chromium/chromium/src/+/main:content/browser/webid/federated_auth_request_impl.cc;l=794;bpv=1;bpt=1?q=FederatedAuthRequestImpl::MaybeShowAccountsDialog&ss=chromium%2Fchromium%2Fsrc>

[3]

for (auto& idp\_ptr : idp\_ptrs) {  

pending\_idps\_.insert(idp\_ptr->config\_url); -------------------[3]

```
if (!fedcm_metrics_) {  
  // Generate a random int for the FedCM call, to be used by the UKM events.  
  std::random_device dev;  
  std::mt19937 rng(dev());  
  std::uniform_int_distribution<std::mt19937::result_type> uniform_dist(  
      1, 1 << 30);  
  // TODO(crbug.com/1307709): Handle FedCmMetrics for multiple IDPs.  
  fedcm_metrics_ = std::make_unique<FedCmMetrics>(  
      idp_ptr->config_url, render_frame_host().GetPageUkmSourceId(),  
      uniform_dist(rng),  
      /\*is_disabled=\*/idp_ptrs.size() > 1);  
}  
prefer_auto_sign_in_ = prefer_auto_sign_in && IsFedCmAutoSigninEnabled();  
start_time_ = base::TimeTicks::Now();  

if (!network::IsOriginPotentiallyTrustworthy(  
        url::Origin::Create(idp_ptr->config_url))) {  
  CompleteRequestWithError(FederatedAuthRequestResult::kError,  
                           TokenStatus::kIdpNotPotentiallyTrustworthy,  
                           /\*should_delay_callback=\*/false);  
  return;  
}  

```

[4]

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc;l=87;drc=21a4c84dd469bfdc9f27375133dc309b62101ef8;bpv=1;bpt=1>

**Additional Comments:**

\*\*Chrome version: \*\* 106.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 73.1 KB)
- deleted (application/octet-stream, 0 B)
- [accounts](attachments/accounts) (text/plain, 337 B)
- [web-identity](attachments/web-identity) (text/plain, 85 B)
- [fedcm.json](attachments/fedcm.json) (text/plain, 262 B)
- [poc.html](attachments/poc.html) (text/plain, 938 B)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 977.1 KB)

## Timeline

### ha...@gmail.com (2022-10-15)

Steps to reproduce the problem:
1.Download all attachment.
2.mkdir .well-known
3.mv web-identity .well-known/web-identity
4.python -m SimpleHTTPServer 8000
5.out/asan/chrome  --enable-features=FedCmMultipleIdentityProviders http://localhost:8000/poc.html
6.click anywhere(not only close show in the poc.mp4) in the show dialog and uaf happen.

### [Deleted User] (2022-10-15)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-10-15)

Here is the true poc.mp4

### jd...@chromium.org (2022-10-17)

This sort of tanzachary@: would you mind taking a look at this? It seems like you're the right person, but if not, feel free to re-assign as needed. Thank you! (cc: pkotwicz just for visibility)

It looks like FedCmMultipleIdentityProviders is not enabled for anyone right now, so setting Impact=None.

[Monorail components: Blink>Identity>FedCM]

### ta...@chromium.org (2022-10-17)

Will look into this, thanks for assigning!

### gi...@appspot.gserviceaccount.com (2022-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bb81bbd40948b602e95cd642322cd03c5ffd00db

commit bb81bbd40948b602e95cd642322cd03c5ffd00db
Author: Zachary Tan <tanzachary@chromium.org>
Date: Thu Oct 20 01:05:21 2022

[FedCM] Fix use-after-free when duplicate IDPs are specified

Bug: 1375021
Change-Id: I1860c4a0ae8fa45cd52da48601247866d89f43dd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3963218
Reviewed-by: Yi Gu <yigu@chromium.org>
Commit-Queue: Zachary Tan <tanzachary@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1061346}

[modify] https://crrev.com/bb81bbd40948b602e95cd642322cd03c5ffd00db/content/browser/webid/federated_auth_request_impl.cc
[modify] https://crrev.com/bb81bbd40948b602e95cd642322cd03c5ffd00db/content/browser/webid/federated_auth_request_impl_unittest.cc


### ta...@chromium.org (2022-10-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-20)

[Empty comment from Monorail migration]

### cb...@chromium.org (2022-10-20)

I'm going to reopen this because I think that a more defense-in-depth approach would be to ensure that when the FedCmAccountSelectionView gets destroyed, that we also destroy the bubble_view_ so that it no longer has a dangling pointer to the FedCmAccountSelectionView via observer_ and the various callbacks it has created. (just setting observer_ to nullptr is probably not enough because the observer has also been passed to various BindOnce functions). Alternatively we could make sure to store weak pointers instead of raw pointers.

### ta...@chromium.org (2022-10-21)

[Empty comment from Monorail migration]

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

### am...@google.com (2022-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-17)

Congratulations! The VRP Panel has decided to award you $7,000 for this report of a mildly mitigated security bug + $3,000 renderer bonus. A member of our finance team will be in touch with you soon to arrange payment. In the interim, please let us know what name/handle/other identifier you would like us to use in acknowledging you for this issue. Thank you for your efforts and reporting this issue to us -- nice work!

### ha...@gmail.com (2022-11-18)

Please use identifier: anonymous for both issue and thanks for the reward! 

### am...@google.com (2022-11-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-02-16)

This issue was migrated from crbug.com/chromium/1375021?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-25)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061363)*

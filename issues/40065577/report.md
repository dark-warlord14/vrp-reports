# Security: Stack-use-after-return in BrowserAttestationService::OnChallengeValidated

| Field | Value |
|-------|-------|
| **Issue ID** | [40065577](https://issues.chromium.org/issues/40065577) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Enterprise>Connectors |
| **Platforms** | Mac |
| **Reporter** | me...@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2023-06-09 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**

1. apply the patch to Chromium and compile Chromium with ASAN enabled
2. start the server: `python server81.py`
3. run `./Chromium --enable-features=UserDTCInlineFlowEnabled --user-data-dir=./tmp1 http://127.0.0.1:8081/poc.html`

**Problem Description:**

1. Analysis

Function `BrowserAttestationService::OnChallengeValidated` has a local variable `key_info`, which is passed into a callback `BrowserAttestationService::OnKeyInfoDecorated`[1] as a `std::ref`.  

When function `BrowserAttestationService::OnChallengeValidated` run over, the local variable `key_info`'s lifetime will end, BUT the callback could still use its reference, which will cause stack-use-after-return.

```
void BrowserAttestationService::OnChallengeValidated(  
    const SignedData& signed_data,  
    base::Value::Dict signals,  
    const std::set<DTCPolicyLevel>& levels,  
    AttestationCallback callback,  
    bool is_va_challenge) {  
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);  
  if (!is_va_challenge) {  
    // Challenge does not come from VA, so mark the device as untrusted (no  
    // challenge response).  
    std::move(callback).Run(  
        {std::string(), DTAttestationResult::kBadChallengeSource});  
    return;  
  }  
  
  // Fill `key_info` out for Chrome Browser.  
  KeyInfo key_info;  
  key_info.set_key_type(CBCM);  
  // VA should accept signals JSON string.  
  std::string signals_json;  
  if (!base::JSONWriter::Write(signals, &signals_json)) {  
    std::move(callback).Run(  
        {std::string(), DTAttestationResult::kFailedToSerializeSignals});  
    return;  
  }  
  key_info.set_device_trust_signals_json(signals_json);  
  
  // Populate profile and/or device level information.  
  auto barrier_closure = base::BarrierClosure(  
      /\*num_closures=\*/attesters_.size(),  
      base::BindOnce(&BrowserAttestationService::OnKeyInfoDecorated,  
                     weak_factory_.GetWeakPtr(), signed_data, levels,  
                     std::move(callback), std::ref(key_info)));  
  
  for (const auto& attester : attesters_) {  
    attester->DecorateKeyInfo(levels, std::ref(key_info), barrier_closure);  
  }  
}  

```

Note that the callback `OnKeyInfoDecorated` is passed into this function  

`attester->DecorateKeyInfo`[2]. It will call `key_manager_->ExportPublicKeyAsync` with the callback, so the callback will run Async after the function `BrowserAttestationService::OnChallengeValidated` run over.

```
void DeviceAttester::DecorateKeyInfo(const std::set<DTCPolicyLevel>& levels,  
                                     KeyInfo& key_info,  
                                     base::OnceClosure done_closure) {  
  if (levels.find(DTCPolicyLevel::kBrowser) == levels.end()) {  
    std::move(done_closure).Run();  
    return;  
  }  
  
  auto dm_token = dm_token_storage_->RetrieveDMToken();  
  if (dm_token.is_valid()) {  
    key_info.set_dm_token(dm_token.value());  
  }  
  
  // The device_id is necessary to validate the dm_token.  
  key_info.set_device_id(dm_token_storage_->RetrieveClientId());  
  
  if (browser_cloud_policy_store_ &&  
      browser_cloud_policy_store_->has_policy()) {  
    const auto\* policy = browser_cloud_policy_store_->policy();  
    key_info.set_customer_id(policy->obfuscated_customer_id());  
  }  
  
  key_manager_->ExportPublicKeyAsync(base::BindOnce(  
      &DeviceAttester::OnPublicKeyExported, weak_factory_.GetWeakPtr(),  
      std::ref(key_info), std::move(done_closure)));  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/connectors/device_trust/attestation/browser/browser_attestation_service.cc;l=166;drc=19a3233d8310ae298b393be1e40840613756b243;bpv=1;bpt=0>  

[2] <https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/enterprise/connectors/device_trust/attestation/browser/device_attester.cc;l=52;drc=daa9d69ff2a1f724226f12c2c8faef657889fb56;bpv=0;bpt=0>

2. Bisect

This problem is introduced by this commit: db1a831caf0e6cb036e468a622498297012301cd  

<https://chromium-review.googlesource.com/c/chromium/src/+/4518120>

According to CrhomiumDash, this UAF affects Chrome Beta after 115.0.5790.13 and Canary after 115.0.5767.0 on Win & Linux & Mac.

3. Suggested Patch  
   
   Please pass a value rather than a reference to the callback.

**Additional Comments:**  

There are some preference settings to satisfy some conditions to trigger this problem.  

You can see the change.txt for more info. This change will not influence the logic of code.

\*\*Chrome version: \*\* 115.0.5790.13 \*\*Channel: \*\* Beta

**OS:** Mac OS

## Attachments

- [server81.py](attachments/server81.py) (text/plain, 2.2 KB)
- [poc1.html](attachments/poc1.html) (text/plain, 106 B)
- [poc.html](attachments/poc.html) (text/plain, 106 B)
- [asan.txt](attachments/asan.txt) (text/plain, 24.2 KB)
- [video.mov](attachments/video.mov) (video/quicktime, 3.8 MB)
- [change.txt](attachments/change.txt) (text/plain, 2.1 KB)
- [patch.txt](attachments/patch.txt) (text/plain, 1.0 KB)
- [change.txt](attachments/change.txt) (text/plain, 2.1 KB)

## Timeline

### [Deleted User] (2023-06-09)

[Empty comment from Monorail migration]

### ar...@google.com (2023-06-09)

Thanks for reporting this! Very well written bug report!

Preliminary classification:
- Security_Impact-None: This is behind the UserDTCInlineFlowEnabled feature which is still disabled by default.
- Security_Severity-Critical: Stack-use-after-return in the browser process
- FoundIn-115: Assuming this was caused by: https://chromium-review.googlesource.com/c/chromium/src/+/4518120

P2 => because this is Security_Impact-None

Note: For now I only checked the code and the problem is clear to me. I haven't yet try to reproduce. I will do it soon. In the meantime, I can assign the owner.

@hmare is currently OOO. Maybe @seblalancette (reviewer) could take a look instead. Removing the std::ref as the reporter suggested should be a straightforward fix.

[Monorail components: Enterprise]

### ar...@google.com (2023-06-09)

[Empty comment from Monorail migration]

[Monorail components: -Enterprise Enterprise>Connectors]

### me...@gmail.com (2023-06-09)

Thank you for your quick reply! 
BTW, C#2 says it’s Security_Severity-Critical, but the label is still High, is there anything mistake:P

### ar...@chromium.org (2023-06-09)

[Empty comment from Monorail migration]

### ar...@chromium.org (2023-06-09)

Fixed!

### me...@gmail.com (2023-06-12)

Sorry, I forgot the change.txt mentioned in repro step1.

### me...@gmail.com (2023-06-12)

Here is a patch. I replace `std::ref` with `base::OwnedRef` and verify that it works fine. Hope this could help you.

### me...@gmail.com (2023-06-12)

Sorry, I forgot the change.txt mentioned in repro step1.

### se...@chromium.org (2023-06-12)

Thanks for the bug! I don't think the suggested patch will work as expected, as we do want the same key_info variable to be modified by subsequent DecorateKeyInfo calls. However, base::OwnedRef will created a copy of the object before we modified it:
https://source.chromium.org/chromium/chromium/src/+/main:base/functional/bind.h;l=371?q=base::OwnedRef&ss=chromium

I will change the implementation to make use of a heap-allocated object instead.

### se...@chromium.org (2023-06-12)

[Empty comment from Monorail migration]

### se...@chromium.org (2023-06-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/acb8e0aba668af35cae2d4e4668b04da6a4d0c6a

commit acb8e0aba668af35cae2d4e4668b04da6a4d0c6a
Author: Sebastien Lalancette <seblalancette@chromium.org>
Date: Mon Jun 12 13:48:25 2023

[DTC] Fix UAF Issue In BrowserAttestationService Using a Unique Ptr

The root issue is that the KeyInfo variable was passed as std::ref to
the barrier closure's callback, while in theory it needed to pass over
ownership. Using a unique_ptr to handle the ownership of that variable
makes things very clear and will take care of that UAF issue.

Fixed: 1453608
Change-Id: Icf45313ad0ad7e14135f6359669501e1cf677572
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4605156
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Leon Masopust <lmasopust@google.com>
Commit-Queue: Sébastien Lalancette <seblalancette@chromium.org>
Auto-Submit: Sébastien Lalancette <seblalancette@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1156165}

[modify] https://crrev.com/acb8e0aba668af35cae2d4e4668b04da6a4d0c6a/chrome/browser/enterprise/connectors/device_trust/attestation/browser/browser_attestation_service.cc
[modify] https://crrev.com/acb8e0aba668af35cae2d4e4668b04da6a4d0c6a/chrome/browser/enterprise/connectors/device_trust/attestation/browser/browser_attestation_service.h


### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### me...@gmail.com (2023-06-16)

[Comment Deleted]

### am...@chromium.org (2023-06-16)

Hello, Krace, thank you for this report. You reached out before I was able to follow-up with the reasoning behind this reward decision. In assessing this issue, we believe this issue is not a Critical severity bug given that this is mitigated by the precondition of a malicious enterprise admin or man/person-in-the-middle scenario to enforce the enterprise policy change required to exploit this issue. While this is a bug that affects the browser process, this is a fairly substantial mitigation. As such, the VRP Panel has decided to award this as moderately mitigated security bug and $4,000 reward + $1,000 bisect bonus. 
I've updated the severity to avoid confusion and this response should also provide the reasoning for that for anyone following up on this issue as well. 
Thank you again for this report and your efforts in reporting this issue to us! 

### me...@gmail.com (2023-06-16)

Thank you for your explanation. 
I think the precondition is only related to the configuration just like some features flags that not enabled by default. Like https://crbug.com/chromium/1417122, I only change some prefs configuration which could be a normal condition in some orgnizations, the enterprise admin may or may not open this function but it doesn't affect the exploit of this bug. As a feature flag, once this function is enabled, we could levarage this bug to exploit it. 
About the url patched in configuration, it could be any url site that configured by enterprise admin, we could hijack DNS to bypass the url site check, and DNS hijack is not related to the browser security. I beg you to reconsider this problem. 

### am...@chromium.org (2023-06-16)

While there is the precondition to the enable the feature flag, there is also the patch / change.txt to allow list the enterprise policy change and allowlist the URLs.
This would not be enabled by default and to do this would require a forced change by a malicious admin or PiTM scenario. 

>>>About the url patched in configuration, it could be any url site that configured by enterprise admin, we could hijack DNS to bypass the url site check
Meaning someone would need to set this configuration and DNS hijack is not part of Chrome threat model in this regard. 

We can take another look to reassess, but I did want to respond in this regard to level set expectations in term of our considerations in for VRP assessment. 

### me...@gmail.com (2023-06-16)

[Comment Deleted]

### am...@chromium.org (2023-06-16)

Yes, we also agree it's potentially exploitable, but it is substantially mitigated by the a specific configuration needing to be put in place, but this is generally performed by an enterprise admin or involving a significant exploit scenario like a PiTM on the local network. As such, we consider this moderately mitigated, which is the basis for the $4,000 reward amount for the report (+$1,000 exploit bonus). 

### me...@gmail.com (2023-06-17)

[Comment Deleted]

### am...@google.com (2023-06-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-11)

Hi Krace, kind reminder once again that we consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), even when included in comments, so I have undeleted them. Please refrain from deleting this artifacts in future reports. Thanks! 

### is...@google.com (2023-11-11)

This issue was migrated from crbug.com/chromium/1453608?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-07)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065577)*

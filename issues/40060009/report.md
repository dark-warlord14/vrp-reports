# Security: use after free in DiceWebSigninInterceptor::OnAccountLevelManagedAccountsSigninRestrictionReceived

| Field | Value |
|-------|-------|
| **Issue ID** | [40060009](https://issues.chromium.org/issues/40060009) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | wx...@gmail.com |
| **Assignee** | yd...@chromium.org |
| **Created** | 2022-06-20 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**  

any version

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- [chromium_report.md](attachments/chromium_report.md) (text/plain, 1.9 KB)
- [0001-trigger-issue-1337676.patch](attachments/0001-trigger-issue-1337676.patch) (text/plain, 2.1 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 25.9 KB)

## Timeline

### [Deleted User] (2022-06-20)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-06-20)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-06-20)

[Comment Deleted]

### wx...@gmail.com (2022-06-20)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-06-20)

Thanks for the report. Updating the title and pasting the content in chromium_report.md for better visibility. 

I'm not convinced that this UaF can be triggered in production. I think the UaF is caused by the Unretained added in DiceWebSigninInterceptor::DiceWebSigninInterceptor in 0001-trigger-issue-1337676.patch, but I'll let ydago@ to determine.

Content in chromium_report.md:

```c++
void UserCloudSigninRestrictionPolicyFetcher::
    GetManagedAccountsSigninRestriction(
        signin::IdentityManager* identity_manager,
        const CoreAccountId& account_id,
        base::OnceCallback<void(const std::string&)> callback) {
  if (!base::FeatureList::IsEnabled(
          features::kEnableUserCloudSigninRestrictionPolicyFetcher)) {
    base::ThreadTaskRunnerHandle::Get()->PostTask(
        FROM_HERE, base::BindOnce(std::move(callback), std::string())); // here post thread task
    return;
  }
  // base::Unretained is safe here because the callback is called in the
  // lifecycle of `this`.
  FetchAccessToken(
      identity_manager, account_id,
      base::BindOnce(&UserCloudSigninRestrictionPolicyFetcher::
                         GetManagedAccountsSigninRestrictionInternal,
                     base::Unretained(this), std::move(callback)));
}
```

UserCloudSigninRestrictionPolicyFetcher::GetManagedAccountsSigninRestriction()->
DiceWebSigninInterceptor::FetchAccountLevelSigninRestrictionForInterceptedAccount()->
DiceWebSigninInterceptor::OnExtendedAccountInfoUpdated()
```c++
 // Fetch the ManagedAccountsSigninRestriction policy value for the intercepted
  // account with a timeout.
  if (!EnterpriseSeparationMaybeRequired(
           info.email, new_account_interception_,
           intercepted_account_level_policy_value_)
           .has_value()) {
    FetchAccountLevelSigninRestrictionForInterceptedAccount(
        info, base::BindOnce(
                  &DiceWebSigninInterceptor::
                      OnAccountLevelManagedAccountsSigninRestrictionReceived, // the callback will enter into thread task and use base::unretained(this)
                  base::Unretained(this), /*timed_out=*/false, info));
    return;
  }
```
DiceWebSigninInterceptor is a keyed service may destroyed when the profile destoryed
so we may can win the race condition.


[Monorail components: Services>SignIn]

### [Deleted User] (2022-06-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-20)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yd...@chromium.org (2022-06-22)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-06-24)

I think this is indeed a real bug, although it's super unlikely to actually happen in production.

In my opinion, UserCloudSigninRestrictionPolicyFetcher should be responsible for not calling its callback after it has been destroyed. Destroying the UserCloudSigninRestrictionPolicyFetcher should cancel the callback.

### gi...@appspot.gserviceaccount.com (2022-06-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9ec699e69caf083340e14584217f9b04996f4413

commit 9ec699e69caf083340e14584217f9b04996f4413
Author: Yann Dago <ydago@chromium.org>
Date: Thu Jun 30 09:14:04 2022

Use CancelableCallback in UserCloudSigninRestrictionPolicyFetcher to avoid use-after-free

Bug: 1337676
Change-Id: I5d5913252941396a74ca061bfb1fae38336c7e30
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3715638
Reviewed-by: David Roger <droger@chromium.org>
Commit-Queue: David Roger <droger@chromium.org>
Auto-Submit: Yann Dago <ydago@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1019525}

[modify] https://crrev.com/9ec699e69caf083340e14584217f9b04996f4413/components/policy/core/browser/signin/user_cloud_signin_restriction_policy_fetcher_unittest.cc
[modify] https://crrev.com/9ec699e69caf083340e14584217f9b04996f4413/components/policy/core/browser/signin/user_cloud_signin_restriction_policy_fetcher.cc
[modify] https://crrev.com/9ec699e69caf083340e14584217f9b04996f4413/components/policy/core/browser/signin/user_cloud_signin_restriction_policy_fetcher.h


### wx...@gmail.com (2022-07-05)

I think this bug can be set to fixed. And I find two bugs. The first one is https://crbug.com/chromium/1341918, I think the right owner is ydago@chromium.org
the second one is https://crbug.com/chromium/1341907, I think the right owner is droger@chromium.org

### wx...@gmail.com (2022-07-05)

feel free to close them if I am wrong.

### yd...@chromium.org (2022-07-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-07)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-21)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. Had the report provide evidence/analysis this issue was reachable or a POC to demonstrate that, it may have been potentially eligible for a larger reward. Thank you for your efforts and reporting this issue to us! 

### wx...@gmail.com (2022-07-21)

Hello, I don't know what I should submit.  I have submited the analysis, trigger patch and asan report.  Did I miss anything?

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-10-12)

This issue was migrated from crbug.com/chromium/1337676?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060009)*

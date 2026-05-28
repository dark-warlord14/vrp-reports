# Security: Heap-use-after-free in LoginStateChecker::OnExecutionResponseCallback 

| Field | Value |
|-------|-------|
| **Issue ID** | [460599518](https://issues.chromium.org/issues/460599518) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Passwords |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 142.0.7444.59 |
| **Reporter** | me...@gmail.com |
| **Assignee** | vs...@google.com |
| **Created** | 2025-11-14 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

1. apply the change.txt to the newest Chromium and compile chrome with ASAN
2. start a server at poc.html's folder : python -m SimpleHTTPServer 8605
3. ./chrome --user-data-dir=/tmp/noexist --password-change-url="<http://127.0.0.1:8605/>" <http://127.0.0.1:8605/poc.html>
4. After the popup shown, click the "Change it for me", and UAF occurs

**Note that this UAF could be used to escape sandbox WITHOUT a compromised render. All the patch I provided is to simulate an easier way to trigger this UAF in Chromium**

# Problem Description

**Vulnerability Analysis**

`login_state_checker_`[1] is an unique\_ptr with a callback `OnLoginStateCheckResult`[2]. This callback will reset the `login_state_checker_`, which means the `login_state_checker_` will be DELETED after the callback is invoked.

[1]

```
  if (base::FeatureList::IsEnabled(
          password_manager::features::kCheckLoginStateBeforePasswordChange)) {
    login_state_checker_ = std::make_unique<LoginStateChecker>(
        originator_.get(), logs_uploader_.get(),
        ChromePasswordManagerClient::FromWebContents(originator_),
        base::BindRepeating(
            &PasswordChangeDelegateImpl::OnLoginStateCheckResult,
            weak_ptr_factory_.GetWeakPtr()));
  }

```

[2]

```
void PasswordChangeDelegateImpl::OnLoginStateCheckResult(bool is_logged_in) {
  if (is_logged_in) {
    // User is logged in, start password change process.
    ProceedToChangePassword();
    return;
  }

  blocking_challenge_detected_ = true;
  if (!login_state_checker_->ReachedAttemptsLimit()) { //@audit: Only when ReachedAttemptsLimit is true, then `login_state_checker_` could be reset
    // Update the UI to encourage user to complete sign in.
    UpdateState(State::kLoginFormDetected);
    return;
  }

  // Maximum number of retries reached, convert to terminal state.
  UpdateState(State::kChangePasswordFormNotFound);
  login_state_checker_.reset();
}

```

However, in the `LoginStateChecker` Class, there is a `LoginStateChecker::OnExecutionResponseCallback`[3] function which will access the class member after the `callback` is invoked in the function `LoginStateChecker::OnPageContentReceived`[4]. This will lead to UAF.

[3]

```
void LoginStateChecker::OnExecutionResponseCallback(
    optimization_guide::OptimizationGuideModelExecutionResult execution_result,
    std::unique_ptr<
        optimization_guide::proto::PasswordChangeSubmissionLoggingData>
        logging_data) {
[...]
  if (cached_page_content_.has_value() && !is_logged_in &&
      !ReachedAttemptsLimit()) {
    OnPageContentReceived(std::move(cached_page_content_)); //@audit: OnPageContentReceived will invoke the callback and delete |this|
    // Clear the page content to ensure that this check doesn't pass next time,
    // which would lead to a request with empty page content.
    cached_page_content_ = std::nullopt;  //@audit: use after free
  }

  result_check_callback_.Run(is_logged_in); //@audit: user after free
}

```

[4]

```
void LoginStateChecker::OnPageContentReceived(
    std::optional<optimization_guide::AIPageContentResult> content) {
  CHECK(content);
  if (is_request_in_flight_) {
    cached_page_content_ = std::move(content);
    return;
  }

  is_request_in_flight_ = true;
  optimization_guide::proto::PasswordChangeRequest request;
  request.set_step(kLoginCheckStep);
  *request.mutable_page_context()->mutable_annotated_page_content() =
      std::move(content->proto);

  LogMessage(client_,
             SavePasswordProgressLogger::STRING_LOGIN_STATE_CHECK_REQUEST_SENT);
  optimization_guide::ExecuteModelWithLogging(  //@audit: this function will directly call the OnExecutionResponseCallback, whihc will call the `callback`
      GetOptimizationService(),
      optimization_guide::ModelBasedCapabilityKey::kPasswordChangeSubmission,
      request, /*execution_timeout=*/std::nullopt,
      base::BindOnce(&LoginStateChecker::OnExecutionResponseCallback,
                     weak_ptr_factory_.GetWeakPtr()));
}

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/password_manager/password_change_delegate_impl.cc;l=386>
[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/password_manager/password_change_delegate_impl.cc;l=407>
[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/password_manager/password_change/login_state_checker.cc;l=217-223>
[4] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/password_manager/password_change/login_state_checker.cc;l=142>

**Bisect**
This UAF is introduced in this commit: <https://source.chromium.org/chromium/chromium/src/+/b5d8d41f2047b2afd062112ea8b39958792a655a>
According to the commit, this UAF affects Chrome Stable 142.0.7444.59.

# Additional Comments

**Info about change.txt**
All the patch in `change.txt` is only used to simulate a more easier environment to trigger the UAF.

- Since the vulnerable function is invoked when the password is detected as "LEAK", so I patch some code to simulate this situation in `components/password_manager/core/browser/leak_detection/leak_detection_request_utils.cc`
- `chrome/browser/password_manager/password_change/login_state_checker.h` change the `kMaxLoginChecks` to `2` to trigger this issue more quickly.
- `components/optimization_guide/core/model_execution/model_execution_features_controller.cc` is patched to enable the `optimization_guide::UserVisibleFeatureKey::kPasswordChangeSubmission` feature.
- `chrome/browser/password_manager/chrome_password_change_service.cc` is patched to support IP format website(Otherwise you need a doamin name).
- `chrome/browser/password_manager/password_change/login_state_checker.cc` patch the checks for `response` to trigger the call to `OnPageContentReceived` function. It also simulate the situation that the first Attempt is not logged in(which will trigger the call to `OnPageContentReceived`), and second Attempt will reach the `ReachedAttemptsLimit` and run the callback to delete this.

# Summary

Security: Heap-use-after-free in LoginStateChecker::OnExecutionResponseCallback

# Custom Questions

#### Type of crash:

browser

#### Crash state:

Please see the attached asan.txt for ASAN logs.

#### Reporter credit:

Krace

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A \

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 88.9 KB)
- [change.txt](attachments/change.txt) (text/plain, 11.5 KB)
- [poc.html](attachments/poc.html) (text/html, 1.1 KB)
- [poc.webm](attachments/poc.webm) (video/webm, 2.3 MB)

## Timeline

### an...@chromium.org (2025-11-14)

[security shepherd]: Thanks for the report! Assigning to vsemeniuk@ who is the owner of the file.

Hi vsemeniuk@ would you be able to take a look at this UAF possibility?

### ch...@google.com (2025-11-15)

Setting milestone because of s2 severity.

### ch...@google.com (2025-11-15)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### me...@gmail.com (2025-11-21)

Hello, any update?

### va...@chromium.org (2025-11-21)

The culprit is `optimization_guide::ExecuteModelWithLogging` that can call the callback both synchronously and asynchronously. This [isn't allowed](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/chrome_browser_design_principles.md?pli=1#general) by the style guide.

### dx...@google.com (2025-11-21)

Project: chromium/src  

Branch:  main  

Author:  Viktor Semeniuk [vsemeniuk@google.com](mailto:vsemeniuk@google.com)  

Link:    <https://chromium-review.googlesource.com/7185380>

Post a task to check cached page content to avoid use-after-free

---


Expand for full commit details
```
     
    Bug: 460599518 
    Change-Id: I8213db7daa5418b42d4c77cefc6a51e907e835db 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7185380 
    Commit-Queue: Viktor Semeniuk <vsemeniuk@google.com> 
    Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1548452}

```

---

Files:

- M `chrome/browser/password_manager/password_change/login_state_checker.cc`
- M `chrome/browser/password_manager/password_change/login_state_checker_unittest.cc`

---

Hash: [001d0da1d38d7da4c2f55fcd57785ef73e67bb37](https://chromiumdash.appspot.com/commit/001d0da1d38d7da4c2f55fcd57785ef73e67bb37)  

Date: Fri Nov 21 15:01:14 2025


---

### ya...@chromium.org (2025-11-21)

Can this bug be marked fixed? FYI marking a bug as fixed will kick off the merge request process for you.

### vs...@google.com (2025-11-21)

Created a separate [bug](https://g-issues.chromium.org/issues/462738689) to fix `optimization_guide::ExecuteModelWithLogging`.

### vs...@google.com (2025-11-24)

I created a [merge](https://chromium-review.googlesource.com/c/chromium/src/+/7185166) manually, there was a merge conflict in unit tests

### dx...@google.com (2025-11-24)

Project: chromium/src  

Branch:  refs/branch-heads/7499  

Author:  Viktor Semeniuk [vsemeniuk@google.com](mailto:vsemeniuk@google.com)  

Link:    <https://chromium-review.googlesource.com/7185166>

[M143] Post a task to check cached page content to avoid use-after-free

---


Expand for full commit details
```
     
    (cherry picked from commit 001d0da1d38d7da4c2f55fcd57785ef73e67bb37) 
     
    Bug: 460599518 
    Change-Id: I8213db7daa5418b42d4c77cefc6a51e907e835db 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7185380 
    Commit-Queue: Viktor Semeniuk <vsemeniuk@google.com> 
    Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1548452} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7185166 
    Cr-Commit-Position: refs/branch-heads/7499@{#2610} 
    Cr-Branched-From: b30439823e5177773584139e72e0593e36863899-refs/heads/main@{#1536371}

```

---

Files:

- M `chrome/browser/password_manager/password_change/login_state_checker.cc`
- M `chrome/browser/password_manager/password_change/login_state_checker_unittest.cc`

---

Hash: [606dbc2ca1f0aeec333c8e97bb03a12e6653042e](https://chromiumdash.appspot.com/commit/606dbc2ca1f0aeec333c8e97bb03a12e6653042e)  

Date: Mon Nov 24 12:42:10 2025


---

### pe...@google.com (2025-11-24)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### vs...@google.com (2025-11-24)

The issue originally present in a feature launched in M141.

### qk...@google.com (2025-11-25)

Labeling as not applicable for M138 because the issue is caused by a feature launched in M141. Even M138 doesn't have the files that the fix modifies.

### me...@gmail.com (2025-12-05)

Hello, any updates about the reward?

### sp...@google.com (2025-12-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Heavily mitigated memory corruption in a non-sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### me...@gmail.com (2025-12-09)

Thank you for your reply. I have several questions about the reward.

1. Is this eligible for a Bisect bonus? Since I have provided the commit that introduces this UAF in [comment #1](https://issues.chromium.org/issues/460599518#comment1).
2. According to the rules in <https://bughunters.google.com/about/rules/chrome-friends/5745167867576320/chrome-vulnerability-reward-program-rules#reward-amounts-for-mitigated-security-bugs> :

> Mildly mitigated: Security bug with minimal mitigations; e.g. a security bug reliably triggered by two or fewer standard user interactions OR winning a race condition; does not require profile destruction or shutdown to trigger

> Moderately mitigated: Security bug with multiple mitigations; e.g. a malicious extension combined with user interaction or other mitigation, or winning a race condition combined with another mitigation

> Highly mitigated: Security bug with multiple types of mitigations or triggered by a series of steps; e.g. a security bug triggered by a series of user interactions or involving a non-standard/unlikely workflow

This UAF only requires ONE standard user interaction, but it is classified as "Highly mitigated". Did I miss something?

### aj...@google.com (2025-12-09)

Thanks - we did not notice the bisect and will return this to the panel for a reassessment.

### me...@gmail.com (2025-12-11)

Hello, sorry for bothering. However, I would like to change my credit info from "Weipeng Jiang (@Krace) of VRI" to "Krace" if possible. Thank you very much!

### sp...@google.com (2025-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
add a bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### me...@gmail.com (2025-12-19)

This UAF only requires ONE standard user interaction, but it is classified as "Highly mitigated". Did I miss something?

### wf...@chromium.org (2025-12-19)

While your PoC itself only requires one user gesture, it also involves a patch to the browser process that significantly simplifies the requirements for reproducing the UAF. For example, the user needs to have a pre-existing leaked password associated with the site. That qualifies as a mitigation. You also patch out some model responses, which may lead to instability in unpatched reproduction.

If you're able to demonstrate this bug with a significantly smaller browser-process patch, we can re-evaluate the reward.

### me...@gmail.com (2025-12-21)

Thank you for your explanation!

### ch...@google.com (2026-02-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/460599518)*

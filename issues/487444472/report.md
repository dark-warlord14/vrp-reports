# Security: Heap-use-after-free in AILanguageModel::PromptState::OnResponse

| Field | Value |
|-------|-------|
| **Issue ID** | [487444472](https://issues.chromium.org/issues/487444472) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>AI>Prompt |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 138.0.0.0 |
| **Reporter** | me...@gmail.com |
| **Assignee** | rm...@chromium.org |
| **Created** | 2026-02-25 |
| **Bounty** | $11,000.00 |

## Description

# Steps to reproduce the problem

1. apply the `change.txt` to Chromium and compile Chromium with ASAN enabled
2. start a http server at the folder of poc.html
3. enable the flag in chrome: `chrome://flags/#prompt-api-for-gemini-nano`
4. run `./chrome --user-data-dir=/userData-with-AILanguageModel http://127.0.0.1:8605/poc.html`, UAF occurs
   PS:On its first run, the `AILanguageModel` API will download the required model files (approx. 10 minutes, varying by network speed). This is a one-time process; the model is then cached locally for immediate access.

# Problem Description

## Introduction

This is a security vulnerability in the browser process that **does not** rely on a compromised renderer, meaning it could be leveraged to escape the Chrome sandbox. The `change.txt` file is used solely to simulate a standard `AIModel` configuration and does not influence Chrome's original logic.

## Bisect

This problem is introduced by this commit: <https://chromium-review.googlesource.com/c/chromium/src/+/6506998>
According to CrhomiumDash, this UAF affects Chrome Stable 138.0.7204.49

# Additional Comments

## Analysis

**Vulnerability Summary**

The vulnerability is a **Use-After-Free (UAF)** caused by the synchronous execution of a callback that deletes the `this` object. Subsequent access to a member variable of the deleted object results in a memory corruption.

In the `OnResponse` function **[1]**, `safety_checker_->RunRawOutputCheck` can synchronously invoke the `OnPartialResponseCheckComplete` function. This execution path eventually deletes the `this` object. However, the code continues to access the member variable `unchecked_output_tokens_` after that, triggering a **UAF**.

```
  void OnResponse(on_device_model::mojom::ResponseChunkPtr chunk) override {
    if (full_response_.empty()) {
      base::UmaHistogramMediumTimes(
          "AI.Session.LanguageModel.FirstResponseTime",
          base::TimeTicks::Now() - start_);
    }
    output_tokens_++;
    full_response_ += chunk->text;

    unchecked_output_tokens_++;
    unchecked_response_ += chunk->text;

    if (!safety_checker_->safety_cfg().CanCheckPartialOutput(
            output_tokens_, unchecked_output_tokens_)) {
      return;
    }
    safety_checker_->RunRawOutputCheck(   //@audit: RunRawOutputCheck will synchronously invoke the `OnPartialResponseCheckComplete`, which will delete |this|
        full_response_, optimization_guide::ResponseCompleteness::kPartial,
        base::BindOnce(&PromptState::OnPartialResponseCheckComplete,
                       weak_factory_.GetWeakPtr(),
                       std::move(unchecked_response_)));
    unchecked_output_tokens_ = 0;  //@audit: |this| has been deleted, UAF occurs. 
    unchecked_response_ = "";
  }

```

**Execution Path to Free:**
The destruction path starts from `OnPartialResponseCheckComplete` **[2]**, which invokes `HandleSafetyError` **[3]**, and finally calls `OnError` **[4]**. As indicated in the code comments, `OnError` executes a callback that deletes `this`.

```
  void OnPartialResponseCheckComplete(
      const std::string& response,
      optimization_guide::SafetyChecker::Result safety_result) {
    if (HandleSafetyError(std::move(safety_result))) {
      return;
    }
    responder_->OnStreaming(response);
  }

  bool HandleSafetyError(
      optimization_guide::SafetyChecker::Result safety_result) {
    if (safety_result.failed_to_run) {
      OnError(blink::mojom::ModelStreamingResponseStatus::kErrorGenericFailure);
      return true;
    }
    if (safety_result.is_unsafe) {
      OnError(blink::mojom::ModelStreamingResponseStatus::kErrorFiltered);
      return true;
    }
    if (safety_result.is_unsupported_language) {
      OnError(blink::mojom::ModelStreamingResponseStatus::
                  kErrorUnsupportedLanguage);
      return true;
    }
    return false;
  }

  void OnError(blink::mojom::ModelStreamingResponseStatus error,
               blink::mojom::QuotaErrorInfoPtr quota_error_info = nullptr) {
    if (responder_) {
      on_device_ai::SendStreamingStatus(responder_, error,
                                        std::move(quota_error_info));
    }
    session_.reset();
    responder_.reset();
    context_receiver_.reset();
    response_receiver_.reset();
    if (callback_) {
      std::move(callback_).Run();
      // `this` may be deleted.
    }
  }

```

**Conditions for Synchronous Invocation:**
To trigger the synchronous invocation within `RunRawOutputCheck`**[5]**, the following two requirements must be met:

1. **`safety_cfg_.HasRawOutputCheck()` is true**: The `PromptApi` configuration must include a `RawOutputCheck`.
2. \*\*`safety_cfg_.GetRawOutputCheckInput(raw_output)` returns `nullptr**`: The `raw_output` must not be found within the `RawOutputCheck`.

I have provided a `change.txt` file to simulate this specific configuration; this simulation does not alter the original logic of the Chromium source code.

```
void SafetyChecker::RunRawOutputCheck(const std::string& raw_output,
                                      ResponseCompleteness completeness,
                                      ResultCallback callback) {
  if (!safety_cfg_.HasRawOutputCheck()) {
    std::move(callback).Run(SafetyChecker::Result{});
    return;
  }
  auto& session = GetSession();
  if (!session.is_bound()) {
    std::move(callback).Run(FailToRunResult());
    return;
  }
  auto check_input = safety_cfg_.GetRawOutputCheckInput(raw_output);  //@audit: If safety_cfg_ cannot find the check_input, it will directly run the callback.
  if (!check_input) {
    std::move(callback).Run(FailToRunResult());
    return;
  }
  auto text = check_input->ToString();
  bool blocked_by_regex_filter =
      safety_cfg_.IsRawOutputBlockedByRegexFilter(text);

  auto make_result_then_callback =
      base::BindOnce(&RawOutputCheckResult, weak_ptr_factory_.GetWeakPtr(),
                     text, completeness, blocked_by_regex_filter)
          .Then(std::move(callback));

  if (blocked_by_regex_filter) {
    session->DetectLanguage(text,
                            base::BindOnce(&AsSafetyInfo)
                                .Then(std::move(make_result_then_callback)));
  } else {
    session->ClassifyTextSafety(text, std::move(make_result_then_callback));
  }
}

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ai/ai_language_model.cc;l=287>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ai/ai_language_model.cc;l=337>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ai/ai_language_model.cc;l=377>

[4] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ai/ai_language_model.cc;l=194>

[5] <https://source.chromium.org/chromium/chromium/src/+/main:components/optimization_guide/core/model_execution/safety_checker.cc;l=191>

# Summary

Security: Heap-use-after-free in AILanguageModel::PromptState::OnResponse

# Custom Questions

#### Type of crash:

browser

#### Crash state:

Please see asan.txt

#### Reporter credit:

Please only credit: Krace

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A \

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 26.7 KB)
- [poc.html](attachments/poc.html) (text/html, 1.6 KB)
- [change.txt](attachments/change.txt) (text/plain, 1.3 KB)
- [poc.webm](attachments/poc.webm) (video/webm, 2.2 MB)

## Timeline

### li...@chromium.org (2026-02-25)

@cd...@chromium.org do you mind taking a look or rerouting as necessary? (This still appears to be behind a flag and hasn't been rolled out.)

### rm...@google.com (2026-02-25)

Clark is no longer at Google, I'll take this instead.

### me...@gmail.com (2026-03-04)

Hello, any update?

### rm...@chromium.org (2026-03-04)

Sorry for the delay! I'm hoping to get a fix for this in this week for the M147 branch.

### dx...@google.com (2026-03-07)

Project: chromium/src  

Branch:  main  

Author:  Robbie McElrath [rmcelrath@chromium.org](mailto:rmcelrath@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7644609>

Prompt API: Delay callback execution in AILanguageModel::PromptState

---


Expand for full commit details
```
     
    This fixes a UaF due to a callback that deletes `this` being executed 
    synchronously. To fix this, the code is updated to not access `this` 
    after calling the function that could synchronously delete `this`, 
    and the problematic callback is posted to the current sequence instead 
    of being run immediately, which should prevent this issue in the future. 
     
    See the bug for more details. 
     
    Bug: 487444472 
    Change-Id: I823661ba5a3666012e52707afca9936647f44bdc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7644609 
    Reviewed-by: Mike Wasserman <msw@chromium.org> 
    Commit-Queue: Mike Wasserman <msw@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1595872}

```

---

Files:

- M `chrome/browser/ai/ai_language_model.cc`

---

Hash: [f2f5a9234975772e403a51e52103d38a64aacbbd](https://chromiumdash.appspot.com/commit/f2f5a9234975772e403a51e52103d38a64aacbbd)  

Date: Sat Mar 7 04:22:02 2026


---

### rm...@google.com (2026-03-09)

The fix for this should be in the M147 release.

Thank you for the excellent bug report and reproduction instructions!

### me...@gmail.com (2026-03-10)

:P

### me...@gmail.com (2026-04-08)

Hello, any update about the reward after one month?

### rm...@chromium.org (2026-04-08)

I'm not sure what the timeline is supposed to be for VRP review, but this bug is in the reward-topanel hotlist [1] so it should be in their queue.

1. <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/vrp-faq.md#how-do-i-know-if-my-bug-report-is-possibly-eligible-for-a-vrp-reward>

### me...@gmail.com (2026-04-09)

Thank you for your reply!

### sp...@google.com (2026-05-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
Mildly mitigated with bisect


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### me...@gmail.com (2026-05-04)

The change.txt file is used solely to simulate a standard AIModel configuration and does not influence Chrome's original logic.

And this UAF doesn’t need any user interaction, but it is classified as "Middly mitigated".

Are there any possible to re-evaluate this issue? Thank you!

### aj...@google.com (2026-05-07)

The team assures us this particular configuration was never released to users, so this bug remains mitigated by being somewhat theoretical.

### me...@gmail.com (2026-05-08)

Thank you.

### ch...@google.com (2026-06-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487444472)*

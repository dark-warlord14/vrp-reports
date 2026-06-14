# Security: Potential Use-After-Free in CallbackLayerAnimationObserver::OnDetachedFromSequence

| Field | Value |
|-------|-------|
| **Issue ID** | [351843813](https://issues.chromium.org/issues/351843813) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Compositing |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 124.0.0.0 |
| **Reporter** | kd...@gmail.com |
| **Assignee** | fl...@chromium.org |
| **Created** | 2024-07-09 |
| **Bounty** | $500.00 |

## Description

# Steps to reproduce the problem

The bug was found by static analysis, so there is no poc yet. However, prior bug fix <https://chromium.googlesource.com/chromium/src.git/+/5145254581a162ae9ad9c1f4f77d54a23c30af86%5E%21/#F1> suggests that it might be a UAF. So, I'm asking for your manual intervention. Thanks for the time!

# Problem Description

As demonstrated in <https://chromium.googlesource.com/chromium/src.git/+/5145254581a162ae9ad9c1f4f77d54a23c30af86%5E%21/#F1>, the callback in `CheckAllSequencesStarted` may destroy the `CallbackLayerAnimationObserver`

```
void CallbackLayerAnimationObserver::SetActive() {
  active_ = true;
  base::WeakPtr<CallbackLayerAnimationObserver> weak_this =
      weak_factory_.GetWeakPtr();
  CheckAllSequencesStarted();
  if (!weak_this)
    return;
  CheckAllSequencesCompleted();
}

```

However, in commit <https://chromium.googlesource.com/chromium/src.git/+/561bb1b239b727d6d0f33a4cbd8163c2efa6199c%5E%21/#F0>, the `OnDetachedFromSequence` is introduced, while didn't follow the restriction below.

```
void CallbackLayerAnimationObserver::OnDetachedFromSequence(
    ui::LayerAnimationSequence* sequence) {
  CHECK_LT(detached_sequence_count_, attached_sequence_count_);
  ++detached_sequence_count_;
  CheckAllSequencesStarted(); // may free |this| in callback
  CheckAllSequencesCompleted(); // UAF
}

```
## suggested path

add a weak\_ptr check after `CheckAllSequencesStarted` in function `OnDetachedFromSequence`.

# Summary

Security: Potential Use-After-Free in CallbackLayerAnimationObserver::OnDetachedFromSequence

# Custom Questions

#### Type of crash:

browser

#### Reporter credit:

Han Zheng (HexHive)

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Timeline

### fl...@google.com (2024-07-11)

Hi & thank you for the clear and detailed report.

I'm setting a provisional severity of Medium based on an assumption that this UAF would be somewhat hard to trigger (and might be protected by MiraclePtr—it's hard to say without a PoC). Reporter—if you are able to produce a PoC, please do update here, it'll be helpful for us.

updowndota@, assigning this to you since it looks like you're familiar with this part of the codebase. (Also: let me know if my assumption that this is hard to trigger is incorrect!)

### pe...@google.com (2024-07-13)

Setting milestone because of s2 severity.

### pe...@google.com (2024-07-13)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### th...@chromium.org (2024-07-15)

[secondary shepherd] updowndota@ is not available, so reassigning to edcourtney@ from [OWNERS file](https://source.chromium.org/chromium/chromium/src/+/main:ui/compositor/OWNERS;l=1;drc=321591501e4f231b29801247c4d90ca5d9e38fa2) and cc-ing other OWNERS as well.

### pe...@google.com (2024-07-30)

flackr: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### fl...@chromium.org (2024-07-30)

I put up a test and fix at <https://chromium-review.googlesource.com/c/chromium/src/+/5749866>

### ap...@google.com (2024-07-30)

Project: chromium/src
Branch: main

commit b09e8ffdd4d5f8373fde7335e9f93627e4095169
Author: Robert Flack <flackr@chromium.org>
Date:   Tue Jul 30 21:01:34 2024

    Ensure that CheckAllSequencesCompleted is not called on deleted observer
    
    Bug: 351843813
    Change-Id: I3627daf34c27d619e05ff2c00c438bfe0aa93139
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5749866
    Reviewed-by: Kyle Charbonneau <kylechar@chromium.org>
    Commit-Queue: Robert Flack <flackr@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1335088}

M       ui/compositor/callback_layer_animation_observer.cc
M       ui/compositor/callback_layer_animation_observer.h
M       ui/compositor/callback_layer_animation_observer_unittest.cc

https://chromium-review.googlesource.com/5749866


### sp...@google.com (2024-08-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
$500 thank you reward; no reachable or exploitable security bug was demonstrated in your report, but we were able to make a potentially security-relevant change from it


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-22)

Thank you for the report Han Zheng. We appreciate the opportunity to make a potentially security relevant change based on the information you provided.

### pe...@google.com (2024-11-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/351843813)*

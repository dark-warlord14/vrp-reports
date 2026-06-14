# use-after-free happening in unittest LayerTreeHostImplTest.ScrollSnapOnY

| Field | Value |
|-------|-------|
| **Issue ID** | [40094426](https://issues.chromium.org/issues/40094426) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>Input, Blink>Scroll |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | Ma...@microsoft.com |
| **Assignee** | sa...@chromium.org |
| **Created** | 2019-03-28 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3739.0 Safari/537.36 Edg/75.0.111.0

Steps to reproduce the problem:
1. Run the command cc_unittests --gtest_filter="LayerTreeHostImplTest.ScrollSnapOnY" --gtest_repeat=100
2. Even though the test passes in a chromium build, the test actually executes a use-after-free due to a recent change.

What is the expected behavior?

What went wrong?
The PR https://chromium-review.googlesource.com/c/chromium/src/%2B/1497375 made changes to LayerTreeHostImpl::ScrollEnd, which causes a use-after-free.

In detail:

1. Function LayerTreeHostImpl::ScrollOffsetAnimationFinished calls LayerTreeHostImpl::ScrollEnd, passing in &deferred_scroll_end_state_.value() as the argument.
2. ScrollEnd then calls Optional::reset on deferred_scroll_end_state_, which destructs the ScrollState it contains. Note that the parameter scroll_state still points to the now-destructed ScrollState.
3. ScrollEnd then calls ScrollEndImpl, which in turn calls DistributeScrollDelta, passing the scroll_state as an argument.
4. DistributeScrollDelta then attempts to set_scroll_chain_and_layer_tree on the destructed scroll_state. In the MSVC++ version of the STL, this causes a crash, but in the libc++ version, it does not. However, it is still a use-after-free.

Did this work before? N/A 

Chrome version: 75.0.3749.0  Channel: n/a
OS Version: 10.0
Flash Version:

## Timeline

### dt...@chromium.org (2019-03-29)

Setting Bug-Security due to use-after free. Security team to provide, looks only to impact Dev/Canary so far.

[Monorail components: Blink>Input]

### sa...@chromium.org (2019-03-29)

[Empty comment from Monorail migration]

[Monorail components: Blink>Scroll]

### dr...@chromium.org (2019-03-29)

I'm failing to reproduce this in an ASAN build on Linux. Can you please provide the gn args you used to build cc_unittests?

sahel@ were you able to reproduce this bug?

### dt...@chromium.org (2019-03-29)

I presume matthew.amert@ is likely using is_clang = false in gn config to use MSVC? 

### Ma...@microsoft.com (2019-03-29)

We are still using clang, but temporarily just using MVSC's version of the STL.

It makes sense that ASAN did not detect it. base::Optional holds the object, so the memory is still seen as valid, but the object itself has been destructed.

To view it happen, set a breakpoint in LayerTreeHostImpl::ScrollEnd, on the deferred_scroll_end_state_.reset() line. Notice how scroll_state and the address of the deferred_scroll_end_state_ member are the same (or, more accurately, off by 8 bytes due to base::Optional's member). You can step through ScrollEndImpl and the rest of the functions to see it use the now-invalid ScrollState, which is a use-after-free.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d8f4e5b1592a63199d81fd1216ebf2e6d2ba11df

commit d8f4e5b1592a63199d81fd1216ebf2e6d2ba11df
Author: Sahel Sharify <sahel@chromium.org>
Date: Fri Mar 29 22:10:33 2019

Reset deferred_scroll_end_state_ in LTHI::ScrollEnd after ScrollEndImpl.

Bug: 947240
Change-Id: Ib998cb7835f4d11b6f7ac4dc56bd8450ec433622
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1546357
Commit-Queue: David Bokan <bokan@chromium.org>
Reviewed-by: David Bokan <bokan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#645970}
[modify] https://crrev.com/d8f4e5b1592a63199d81fd1216ebf2e6d2ba11df/cc/trees/layer_tree_host_impl.cc


### sh...@chromium.org (2019-03-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-30)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bo...@chromium.org (2019-03-30)

The CL that introduced the issue isn't on a release branch so there's no branch impact. The CL in #6 should have fixed the issue, I'll leave to sahel@ to confirm.

### sh...@chromium.org (2019-03-31)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2019-04-01)

Based on #9, marking Security_Impact-None and removing ReleaseBlock-Stable.

### sa...@chromium.org (2019-04-01)

The code in https://crbug.com/chromium/947240#c6 is first landed in 75.0.3751.0. 
matthew.amert@ could you please verify the fix on Canary or ToT.

### sh...@chromium.org (2019-04-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### Ma...@microsoft.com (2019-04-08)

I apologize for the late reponse. I have indeed verified the fix. Thank you for you quick handling of this!

### aa...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-11)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### sa...@chromium.org (2019-04-18)

Marking it as verified per https://crbug.com/chromium/947240#c15

### pa...@chromium.org (2019-04-18)

Congrats! The Panel decided to reward $3,000 for this report!

### pa...@chromium.org (2019-04-18)

How would you like to be credited in our release notes?

### Ma...@microsoft.com (2019-04-19)

I would like to donate the reward to charity. Where could I find a list of eligible charities?

And for the credit, since my (then-)manager Rick James helped me identify some of the details of the bug, could you please list the credit as "Matt Amert and Rick James, Microsoft Edge"?

Thanks!

### pa...@chromium.org (2019-04-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/947240?no_tracker_redirect=1

[Multiple monorail components: Blink>Input, Blink>Scroll]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094426)*

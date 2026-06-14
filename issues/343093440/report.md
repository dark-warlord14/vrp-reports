# UAF in ScheduleCpuFrequencyTask

| Field | Value |
|-------|-------|
| **Issue ID** | [343093440](https://issues.chromium.org/issues/343093440) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>PerformanceManager |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2024-05-28 |
| **Bounty** | $500.00 |

## Description

deleted

## Timeline

### el...@chromium.org (2024-05-28)

Security shepherd: thanks for the report. I haven't reproed this locally but the bug is clear by code inspection. I'll do a fix for this one.

### el...@chromium.org (2024-05-28)

I'm calling this Sev-2 given that it seems quite hard to actually exploit.

### ap...@google.com (2024-05-29)

Project: chromium/src
Branch: main

commit aaeb7ce52514e4bdc594d56213b5daf08e11e794
Author: Anthony Vallée-Dubois <anthonyvd@google.com>
Date:   Wed May 29 17:28:36 2024

    Make CpuEstimation function statics to avoid possible UAF
    
    Bug: 343093440
    Change-Id: Ie31ce444d26909bb4aae9f7664d3d649a3f364dd
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5578179
    Reviewed-by: Francois Pierre Doray <fdoray@chromium.org>
    Commit-Queue: Anthony Vallée-Dubois <anthonyvd@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1307531}

M       chrome/browser/performance_manager/metrics/metrics_provider_desktop.cc
M       chrome/browser/performance_manager/metrics/metrics_provider_desktop.h

https://chromium-review.googlesource.com/5578179


### pg...@google.com (2024-05-30)

Looks like this got added <https://chromium-review.googlesource.com/c/chromium/src/+/5544754>, which landed on M127 - setting foundin as so, but [anthonyvd@google.com](mailto:anthonyvd@google.com), please correct me if im wrong!

### pe...@google.com (2024-05-31)

Setting milestone because of s2 severity.

### pe...@google.com (2024-05-31)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-06-12)

ellyjones: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### el...@chromium.org (2024-06-13)

The change in #4 fixed this.

### pe...@google.com (2024-06-13)

Not requesting merge to beta (M127) because latest trunk commit (1307531) appears to be prior to beta branch point (1313161). If this is incorrect please remove NA-127 from the 'Merge' field and add 127 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### sp...@google.com (2024-06-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
speculative report of highly mitigated memory corruption bug with low potential for exploitability 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-28)

Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2024-09-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/343093440)*

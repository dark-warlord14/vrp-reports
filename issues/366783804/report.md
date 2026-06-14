# Crash in blink::V8Initializer::ExceptionPropagationCallback

| Field | Value |
|-------|-------|
| **Issue ID** | [366783804](https://issues.chromium.org/issues/366783804) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>Bindings, Blink>JavaScript>Runtime |
| **Platforms** | Linux |
| **Reporter** | m....@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2024-09-15 |
| **Bounty** | $9,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=4847048679424000

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_content_shell_drt
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7be94bd18000
Crash State:
  blink::V8Initializer::ExceptionPropagationCallback
  v8::internal::Isolate::ReportExceptionFunctionCallback
  v8::internal::Isolate::NotifyExceptionPropagationCallback
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_content_shell_drt&range=1355412:1355430

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4847048679424000

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### 24...@project.gserviceaccount.com (2024-09-16)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-09-16)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/e19949bb7573247028a506d89595599a20084789 (Use v8::ExceptionPropagationCallback to set exception context information

This new v8 callback provides us an opportunity to modify the
exception immediately before it is thrown. We can use this callback
to add context information to the exception message, rather than
rely on the current system of having a stack-allocated object
(ExceptionState) apply this information, with the eventual goal
of either removing this stack-allocated class or rendering its
constructor/destructor trivial.

Practical results of this change:
1. Special handling is need for any case that throws an exception
   asynchronously, or rejects a promise with an exception. In those
   cases, ApplyContextToException() must be called manually.
2. A bunch of cases where we previiously couldn't apply exception
   context information now get it for free, so there are a lot of
   test updates to add exception context.

Bug: 328104148
Change-Id: Icef838874583f48a23036d8604402ceaad11ff25
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5530624
Reviewed-by: Rick Byers <rbyers@chromium.org>
Owners-Override: Rick Byers <rbyers@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Nate Chapin <japhet@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1355428}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### pe...@google.com (2024-09-16)

Setting milestone because of s2 severity.

### pe...@google.com (2024-09-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-09-16)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### 24...@project.gserviceaccount.com (2024-09-17)

ClusterFuzz testcase 4847048679424000 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_content_shell_drt&range=1356138:1356140

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pe...@google.com (2024-09-18)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M130. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [130].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pg...@google.com (2024-09-18)

Suspected regression CL reverted: <https://chromium-review.googlesource.com/c/chromium/src/+/5867091>, looks like a clean revert but landed in M131

The two days' worth of canary data doesnt show anything concerning about this revert, but please do take another look to ensure that the revert does not have any other impact on stability.

Merge approved for M130 - please merge to v8 branch 13.0 at your earliest convenience to get this change into the next beta release.

### ja...@chromium.org (2024-09-18)

re: comment #9: note that this is a chromium CL, not a v8 CL, so the merge will happen on chromium's refs/branch-heads/6723. 

### pe...@google.com (2024-09-18)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), gmpritchard (ChromeOS), danielyip (Desktop)

### ja...@chromium.org (2024-09-18)

Cherry picked to refs/branch-heads/6723 in https://chromium-review.googlesource.com/c/chromium/src/+/5873669. Sorry I forgot to update the commit description with a reference to this issue.

### pe...@google.com (2024-09-23)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2024-09-30)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $9000.00 for this report.

Rationale for this decision:
$7,000 for baseline report of renderer memory corruption + $2,000 fuzzer bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-30)

Congratulations! Thank you for your past fuzzer contributions that resulted in this report!

### pe...@google.com (2024-12-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/366783804)*

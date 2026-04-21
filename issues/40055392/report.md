# Security: OOB in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [40055392](https://issues.chromium.org/issues/40055392) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux, Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2021-03-31 |
| **Bounty** | $15,000.00 |

## Description

The attached poc triggers an OOB access in 32bit x86 builds of v8. Run with --stress-compaction  

Note that the crash can still be hit with a more complicated poc without that flag.

The problem in src/builtins/ia32/builtins-ia32.cc in the function Generate\_PushBoundArguments  

The stack overflow check fails to set up a proper frame

```
        FrameScope frame(masm, StackFrame::MANUAL);  
        __ CallRuntime(Runtime::kThrowStackOverflow);  

```

The fix is to add the following line between the two.  

\_\_ EnterFrame(StackFrame::INTERNAL);

As such the return address will be interpreted as an object during stack walking by the GC.  

The crashing address can be controlled by having the return address point to jitted code. The code will then be interpreted as an address.

In the attached poc it will crash at addresses like these  

Received signal 11 SEGV\_MAPERR 000041406815

**CREDIT INFORMATION**  

Reporter credit: Chris Salls (@salls)

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 465 B)

## Timeline

### [Deleted User] (2021-03-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-04-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5680271408824320.

### dr...@chromium.org (2021-04-01)

ClusterFuzz failed to reproduce the bug, but I suspect that's due to the 32-bit requirement, as this looks plausible. ishell@ - can you help triage?

### is...@chromium.org (2021-04-01)

Thank you for the report and suggestion for the fix!

Not sure how exploitable this crash is but it does happen without any flags.

[Monorail components: Blink>JavaScript]

### gi...@appspot.gserviceaccount.com (2021-04-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/8809cb11e206bd7b0bea5f36f9a5c7cc401cb65a

commit 8809cb11e206bd7b0bea5f36f9a5c7cc401cb65a
Author: Igor Sheludko <ishell@chromium.org>
Date: Thu Apr 01 14:11:28 2021

[builtins][ia32] Create internal frame before throwing StackOverflow

... in CallBoundFunction builtin.

Bug: chromium:1194358
Change-Id: I8ddd4fff39cf399d4af332cff8eddc40e217cfdb
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2800111
Auto-Submit: Igor Sheludko <ishell@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/master@{#73775}

[modify] https://crrev.com/8809cb11e206bd7b0bea5f36f9a5c7cc401cb65a/src/builtins/ia32/builtins-ia32.cc


### is...@chromium.org (2021-04-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-01)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-07)

ishell@ please can you let us know the appropriate Security_Severity and Security_Impact then mark this as Fixed again. We need those labels so it can be merged to the appropriate branches.

### is...@chromium.org (2021-04-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-07)

Congratulations, Chris! The VRP Panel has decided to award you $15,000 for this report. Thank you for your efforts and reporting this issue to us! 

### ch...@gmail.com (2021-04-08)

Thanks for the award!

### [Deleted User] (2021-04-08)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-07-15)

This issue was migrated from crbug.com/chromium/1194358?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055392)*

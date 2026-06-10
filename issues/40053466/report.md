# DCHECK failure in !IsJSGlobalObject(isolate) in js-objects-inl.h

| Field | Value |
|-------|-------|
| **Issue ID** | [40053466](https://issues.chromium.org/issues/40053466) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | cb...@chromium.org |
| **Created** | 2020-09-29 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36

Steps to reproduce the problem:
1. download chromium of asan-linux-debug-811138
2. ./chrome ./poc.pdf
3.

What is the expected behavior?

What went wrong?
In debug version, this poc will triger a DCHECK failure, the isolate is a Global Object which not satisfy the dcheck.
In asan-release version on Windows, it will print ASAN log with the accession-violation on UNKNOWN ADDRESS 
And, on windows ,you need to add `--no-sandbox` to see the ASAN.

Did this work before? N/A 

Chrome version: 85.0.4183.121  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- [debug-log.txt](attachments/debug-log.txt) (text/plain, 3.1 KB)
- [poc.pdf](attachments/poc.pdf) (application/pdf, 977 B)
- [asan-log.txt](attachments/asan-log.txt) (text/plain, 9.8 KB)
- [pdfium_test-asan.txt](attachments/pdfium_test-asan.txt) (text/plain, 4.7 KB)

## Timeline

### me...@gmail.com (2020-09-29)

Oh, I find that pdfium_test can also output the ASAN log in release build, do not need the chrome.

### me...@gmail.com (2020-09-29)

[Empty comment from Monorail migration]

### do...@chromium.org (2020-09-30)

+tsepez, can you take a look? Tentatively assigning a medium severity for the time being.

[Monorail components: Internals>Plugins>PDF]

### [Deleted User] (2020-09-30)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-09-30)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2020-09-30)

I hit the CHECK() using ToT chrome (811785 for my build) but not with pdfium_test.

Assigning to v8 triage as this is deep within V8 and there weren't obvious pdf callbacks on the stack (though it may well be PDFium causing some corruption).



[Monorail components: Blink>JavaScript]

### ec...@chromium.org (2020-10-01)

I can confirm that this is crashing on canary, but not on M85. Bisection on Linux64 led to the following changes:
https://chromium.googlesource.com/chromium/src/+log/3fa31f47b6ead95e5b0501293ee76c9f988b68ed..5a3468d7f408eda7fb07f8979ea3b7b22c5ec817

Of these, the most relevant one seems to be the V8 autoroller, which comprises the following CLs:
https://chromium.googlesource.com/v8/v8/+log/3e2d6551..bb481754

The most likely candidate is https://chromium-review.googlesource.com/c/v8/v8/+/2362961which changed JSReceiver::SetOrCopyDataProperties that occurs on top of the callstack (including the line in question).

@cbruni: Could you please take a look?

### do...@chromium.org (2020-10-02)

Updating security labels to HEAD. However, as M87 is branching today, we might need to merge a fix to M87 branch once one lands and rolls into trunk.

### do...@chromium.org (2020-10-02)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-02)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@google.com (2020-10-02)

+adetaylor@ (Security TPM)

### cb...@chromium.org (2020-10-04)

We're confusing the GlobalObject with the a normal JSObject in dict-mode via Object.assign.
Given that the backing store for the GlobalObject (kEntrySize=1) is 3 times smaller than the normal NameDictionary (kEntrySize=3) we easily get an OOB read here.

JS-code in the PDF:
  
  Object.assign(this,app.activeDocs[0]); 


Most likely culprit:

if (!from->HasFastProperties() && target->HasFastProperties()) {
    // Convert to slow properties if we're guaranteed to overflow the number of
    // descriptors.
    int source_length =
        from->property_dictionary().NumberOfEnumerableProperties();
    if (source_length > kMaxNumberOfDescriptors) {
      JSObject::NormalizeProperties(isolate, Handle<JSObject>::cast(target),
                                    CLEAR_INOBJECT_PROPERTIES, source_length,
                                    "Copying data properties");
    }
  }


from->property_dictionary() does not check if from is the GlobalObject.
Will fix on monday.




### is...@chromium.org (2020-10-05)

[Empty comment from Monorail migration]

### do...@chromium.org (2020-10-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-05)

Even though the original report states M85 (twice) I've discussed with Dominick and we suspect that https://crbug.com/chromium/1133210#c7 is correct and this doesn't affect M85. merc.ouc@ please let us know if we're wrong.

In which case I'm assuming this affects only M87 and M88 and so Security_Impact-Beta is correct. ReleaseBlock-Stable is also correct but I have adjusted M/Target labels.

### me...@gmail.com (2020-10-05)

Thanks for you analysis and I think you are right adetaylor@

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/28c2e433d04d618a1b4dd0092e49a28bcf530f3b

commit 28c2e433d04d618a1b4dd0092e49a28bcf530f3b
Author: Camillo Bruni <cbruni@chromium.org>
Date: Tue Oct 06 12:27:15 2020

[runtime] Fix global_dictionary case in SetOrCopyDataProperties

Bug: chromium:1133210
Change-Id: Ic60e88ab3c50602a71387f7c3a1253d70a7c69fa
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2450061
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Camillo Bruni <cbruni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#70341}

[modify] https://crrev.com/28c2e433d04d618a1b4dd0092e49a28bcf530f3b/src/objects/js-objects.cc
[modify] https://crrev.com/28c2e433d04d618a1b4dd0092e49a28bcf530f3b/test/mjsunit/es6/object-assign.js
[modify] https://crrev.com/28c2e433d04d618a1b4dd0092e49a28bcf530f3b/test/mjsunit/es8/object-values.js


### cb...@chromium.org (2020-10-07)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-10-07)

Approving merge to M87 branch 4280, but please mark security bugs as fixed before requesting merge.

### cb...@chromium.org (2020-10-12)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/a454c531f321f048d502b6fc51fe77775baf4f02

commit a454c531f321f048d502b6fc51fe77775baf4f02
Author: Camillo Bruni <cbruni@chromium.org>
Date: Mon Oct 12 08:08:09 2020

Merged: [runtime] Fix global_dictionary case in SetOrCopyDataProperties

Revision: 28c2e433d04d618a1b4dd0092e49a28bcf530f3b

BUG=chromium:1133210
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=ishell@chromium.org

Change-Id: I5222ad800c6c144295553d659ccb1116fa4667dc
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2464928
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.7@{#8}
Cr-Branched-From: 0d81cd72688512abcbe1601015baee390c484a6a-refs/heads/8.7.220@{#1}
Cr-Branched-From: 942c2ef85caef00fcf02517d049f05e9a3d4b440-refs/heads/master@{#70196}

[modify] https://crrev.com/a454c531f321f048d502b6fc51fe77775baf4f02/src/objects/js-objects.cc
[modify] https://crrev.com/a454c531f321f048d502b6fc51fe77775baf4f02/test/mjsunit/es6/object-assign.js
[modify] https://crrev.com/a454c531f321f048d502b6fc51fe77775baf4f02/test/mjsunit/es8/object-values.js


### cb...@chromium.org (2020-10-12)

CL has ben backmerged to V8 8.7, waiting for the next chrome 87 release to pick it up.

### cb...@chromium.org (2020-10-12)

[Empty comment from Monorail migration]

[Monorail components: -Internals>Plugins>PDF]

### [Deleted User] (2020-10-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cb...@chromium.org (2020-10-12)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-10-13)

ClusterFuzz testcase 5679229125853184 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=70294:70467

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### ad...@google.com (2020-10-18)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-21)

Congratulations, the VRP panel has awarded $5000 for this report.

### ad...@google.com (2020-10-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1133210?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1134984]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053466)*

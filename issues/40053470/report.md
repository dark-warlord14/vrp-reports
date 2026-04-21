# Security: Debug check failed: IsFound() || !holder_->HasFastProperties(isolate_)

| Field | Value |
|-------|-------|
| **Issue ID** | [40053470](https://issues.chromium.org/issues/40053470) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2020-09-29 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36

Steps to reproduce the problem:
Note: I am unable to submit on the proper bug bounty link (https://bugs.chromium.org/p/chromium/issues/entry?template=Security%20Bug) currently, potentially due to the bug with issue permissions (http://crbug.com/monorail/8426, which I don't have access to). When I submit at that link, the page reloads the submission page, without actually submitting.

Compilation flags: gn gen out/debugbuild --args='is_debug=true dcheck_always_on=true v8_static_library=true v8_enable_slow_dchecks=true v8_enable_v8_checks=true v8_enable_verify_heap=true v8_enable_verify_csa=true v8_enable_verify_predictable=true target_cpu="x64"'

Requires the --predictable flag when running

function main() {
    function v2(v3,v4) {
        try {
            const v5 = 1;
            const v6 = v4 + 1010532227;
            const v7 = v2(v3,v6);
        } catch(v8) {
        }
        const v9 = 5.3;
        const v10 = v4 * 13.37;
        const v12 = 43.35 >> 13.37;
        v3[v4] = v12;
    }
    const v14 = Array.prototype;
    const v16 = v2(v14,0);
}
main();

What is the expected behavior?
No assertion Failure!

What went wrong?

#
# Fatal error in ../../src/objects/lookup.cc, line 173
# Debug check failed: IsFound() || !holder_->HasFastProperties(isolate_)
#
#
#
#FailureMessage Object: 0x7ffffff1e7a0
==== C stack trace ===============================

    /home/b/projects/clean_js_engines/v8/out/debugbuild/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7ffff5db7f93]
    /home/b/projects/clean_js_engines/v8/out/debugbuild/libv8_libplatform.so(+0x154ed) [0x7ffff5d834ed]
    /home/b/projects/clean_js_engines/v8/out/debugbuild/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x153) [0x7ffff5dac8b3]
    /home/b/projects/clean_js_engines/v8/out/debugbuild/libv8_libbase.so(+0x1c145) [0x7ffff5dac145]
    /home/b/projects/clean_js_engines/v8/out/debugbuild/libv8.so(void v8::internal::LookupIterator::ReloadPropertyInformation<false>()+0x1c8) [0x7ffff73ab9a8]
    /home/b/projects/clean_js_engines/v8/out/debugbuild/libv8.so(v8::internal::LookupIterator::ApplyTransitionToDataProperty(v8::internal::Handle<v8::internal::JSReceiver>)+0xa75) [0x7ffff73aed15]
    /home/b/projects/clean_js_engines/v8/out/debugbuild/libv8.so(+0x167b3b0) [0x7ffff74393b0]
    /home/b/projects/clean_js_engines/v8/out/debugbuild/libv8.so(v8::internal::Object::SetProperty(v8::internal::LookupIterator*, v8::internal::Handle<v8::internal::Object>, v8::internal::StoreOrigin, v8::Maybe<v8::internal::ShouldThrow>)+0x119) [0x7ffff7436f29]
    /home/b/projects/clean_js_engines/v8/out/debugbuild/libv8.so(v8::internal::Runtime::SetObjectProperty(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, v8::internal::StoreOrigin, v8::Maybe<v8::internal::ShouldThrow>)+0x3bf) [0x7ffff768bfff]
    /home/b/projects/clean_js_engines/v8/out/debugbuild/libv8.so(+0x18d534f) [0x7ffff769334f]
    /home/b/projects/clean_js_engines/v8/out/debugbuild/libv8.so(+0x8605ff) [0x7ffff661e5ff]
Received signal 4 ILL_ILLOPN 7ffff5db5de2

Did this work before? N/A 

Chrome version: 85.0.4183.121  Channel: stable
OS Version: 
Flash Version:

## Timeline

### do...@chromium.org (2020-09-30)

+cc V8 sheriff for triage. Can you determine the severity of this issue?

Reporter: what version of V8 are you using?

[Monorail components: Blink>JavaScript]

### ha...@chromium.org (2020-09-30)

[Empty comment from Monorail migration]

### is...@chromium.org (2020-09-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-09-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5714754687795200.

### cl...@chromium.org (2020-09-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5631994157662208.

### cl...@chromium.org (2020-09-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5757194517938176.

### cl...@chromium.org (2020-09-30)

Testcase 5631994157662208 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5631994157662208.

### cl...@chromium.org (2020-09-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-09-30)

Detailed Report: https://clusterfuzz.com/testcase?key=5757194517938176

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  IsFound() || !holder_->HasFastProperties(isolate_) in lookup.cc
  void v8::internal::LookupIterator::ReloadPropertyInformation<false>
  v8::internal::LookupIterator::ApplyTransitionToDataProperty
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=69662:69663

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5757194517938176

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5757194517938176 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### is...@chromium.org (2020-09-30)

[Empty comment from Monorail migration]

### al...@gmail.com (2020-09-30)

@dominickn@chromium.org: Here is the version information. Looks like I missed including in in the initial report.

VERSION
V8 Version: 8.7.0 (Candidate)
V8 Commit: 52bebb7b2e94e976870c34a006885470bc6c99e2
Operating System: Ubuntu 20.04



### is...@chromium.org (2020-09-30)

Thank you for the report!
I managed to reproduce it, investigating...

### is...@chromium.org (2020-10-05)

[Empty comment from Monorail migration]

### me...@google.com (2020-10-06)

ishell: Could you also help with the severity assessment? Is this a pure DCHECK or are there any security implications as well? Thanks.

### ad...@google.com (2020-10-08)

ishell@ to add to the chorus, please add Security_Severity and let us know what happens if a release build goes past the DCHECK, such that the VRP panel can do the right thing here.

### is...@chromium.org (2020-10-09)

In release mode we don't hit any checks and end up writing a value to some other field in the same object instead of "desired" field.
Other field is overwritten without checking/updating field type tracking information.
Might probably cause an OOB write but I didn't try to carefully check that because the reason above is already enough.

The issue is caused by an improperly handled hash collision in DescriptorArray.
I'm not sure how hard is to reproduce/use it in the wild given that hash values depend on the random seed, so I set it to P1 for now.

I'm working on a fix.

### [Deleted User] (2020-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-10)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@gmail.com (2020-10-10)

Interesting root cause! I'm definitely interested to see the fix.
For any CVE or patch notes, please credit Bill Parks.

This was found with a modified version of Saelo's Fuzzilli, although I don't think my modifications played much of a role.

### sa...@google.com (2020-10-12)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/518d67ad652fc24b7eb03e48bb342f952d4ccf74

commit 518d67ad652fc24b7eb03e48bb342f952d4ccf74
Author: Igor Sheludko <ishell@chromium.org>
Date: Fri Oct 16 14:11:04 2020

[runtime] Fix sorted order of DescriptorArray entries

... and add respective regression tests.

This CL also adds similar regression tests for TransitionArray but it
doesn't have the same issue as DescriptorArray.

Bug: chromium:1133527
Change-Id: I668a90f126d76af0a39816ce8697cb29bc65d01b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2465833
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/master@{#70570}

[modify] https://crrev.com/518d67ad652fc24b7eb03e48bb342f952d4ccf74/src/codegen/code-stub-assembler.cc
[modify] https://crrev.com/518d67ad652fc24b7eb03e48bb342f952d4ccf74/src/codegen/code-stub-assembler.h
[modify] https://crrev.com/518d67ad652fc24b7eb03e48bb342f952d4ccf74/src/diagnostics/objects-debug.cc
[modify] https://crrev.com/518d67ad652fc24b7eb03e48bb342f952d4ccf74/src/objects/descriptor-array-inl.h
[modify] https://crrev.com/518d67ad652fc24b7eb03e48bb342f952d4ccf74/src/objects/descriptor-array.h
[modify] https://crrev.com/518d67ad652fc24b7eb03e48bb342f952d4ccf74/src/objects/fixed-array-inl.h
[modify] https://crrev.com/518d67ad652fc24b7eb03e48bb342f952d4ccf74/src/objects/name-inl.h
[modify] https://crrev.com/518d67ad652fc24b7eb03e48bb342f952d4ccf74/src/objects/name.h
[modify] https://crrev.com/518d67ad652fc24b7eb03e48bb342f952d4ccf74/src/objects/objects.cc
[modify] https://crrev.com/518d67ad652fc24b7eb03e48bb342f952d4ccf74/src/objects/transitions-inl.h
[modify] https://crrev.com/518d67ad652fc24b7eb03e48bb342f952d4ccf74/src/objects/transitions.cc
[modify] https://crrev.com/518d67ad652fc24b7eb03e48bb342f952d4ccf74/src/objects/transitions.h
[modify] https://crrev.com/518d67ad652fc24b7eb03e48bb342f952d4ccf74/test/cctest/BUILD.gn
[add] https://crrev.com/518d67ad652fc24b7eb03e48bb342f952d4ccf74/test/cctest/test-descriptor-array.cc
[modify] https://crrev.com/518d67ad652fc24b7eb03e48bb342f952d4ccf74/test/cctest/test-transitions.h


### cl...@chromium.org (2020-10-16)

ClusterFuzz testcase 5631994157662208 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2020-10-16)

ClusterFuzz testcase 5757194517938176 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=70569:70570

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### is...@chromium.org (2020-10-16)

Setting next action to Monday, when we'll have Canary coverage.

### [Deleted User] (2020-10-16)

This bug requires manual review: Less than 28 days to go before AppStore submit on M87
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-16)

[Empty comment from Monorail migration]

### pb...@google.com (2020-10-16)

+Adetaylor(Security TPM) for Merge decision.


Note : The change in https://crbug.com/chromium/1133527#c21 didn't got any Canary coverage yet.

### bi...@google.com (2020-10-16)

Component says Blink, so does this change impact iOS? 

### is...@chromium.org (2020-10-16)

It affects V8, the JavaScript engine. Do we use V8 on iOS?

### ad...@chromium.org (2020-10-16)

We don't.

### ad...@google.com (2020-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-10-19)

Approving merge to M87, branch 4280, assuming the change is looking good in Canary. ishell@ please would you comment on the stability risks of merging this back to M86 per https://crbug.com/chromium/1133527#c25 (but more generally). There's an M86 release being cut today, but in this case I'm not bold enough to approve merge without your commentary. (To state the obvious, this is important because patch-gappers will have been trying to weaponize your CL since you posted the first draft, but nonetheless I think we're too late for today's cut.)

### is...@chromium.org (2020-10-20)

The fix is not a one-liner, but still quite simple although the changes are spread across multiple components in V8. The fix contains a regression unit test, the V8 waterfall is ok, Canary looks good, so I don't expect any stability issues with merging the fix back.

The CL does NOT apply cleanly to both M87 and M86, but the required changes are trivial.


### is...@chromium.org (2020-10-20)

Clarification: The CL DOES apply cleanly but the regression tests require updating since the internal APIs have changed a bit.

### is...@chromium.org (2020-10-20)

Merged to M87: https://chromium-review.googlesource.com/c/v8/v8/+/2487121

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3bc7d790839a66378472bbeded1bfe66a06f156f

commit 3bc7d790839a66378472bbeded1bfe66a06f156f
Author: ishell@chromium.org <ishell@chromium.org>
Date: Tue Oct 20 11:31:38 2020

Merged: [runtime] Fix sorted order of DescriptorArray entries

Revision: 518d67ad652fc24b7eb03e48bb342f952d4ccf74

BUG=chromium:1133527
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=verwaest@chromium.org

Change-Id: I95929cfa42f052930121505d252a6726aeb10356
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2487121
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.7@{#14}
Cr-Branched-From: 0d81cd72688512abcbe1601015baee390c484a6a-refs/heads/8.7.220@{#1}
Cr-Branched-From: 942c2ef85caef00fcf02517d049f05e9a3d4b440-refs/heads/master@{#70196}

[modify] https://crrev.com/3bc7d790839a66378472bbeded1bfe66a06f156f/src/codegen/code-stub-assembler.cc
[modify] https://crrev.com/3bc7d790839a66378472bbeded1bfe66a06f156f/src/codegen/code-stub-assembler.h
[modify] https://crrev.com/3bc7d790839a66378472bbeded1bfe66a06f156f/src/diagnostics/objects-debug.cc
[modify] https://crrev.com/3bc7d790839a66378472bbeded1bfe66a06f156f/src/objects/descriptor-array-inl.h
[modify] https://crrev.com/3bc7d790839a66378472bbeded1bfe66a06f156f/src/objects/descriptor-array.h
[modify] https://crrev.com/3bc7d790839a66378472bbeded1bfe66a06f156f/src/objects/fixed-array-inl.h
[modify] https://crrev.com/3bc7d790839a66378472bbeded1bfe66a06f156f/src/objects/name-inl.h
[modify] https://crrev.com/3bc7d790839a66378472bbeded1bfe66a06f156f/src/objects/name.h
[modify] https://crrev.com/3bc7d790839a66378472bbeded1bfe66a06f156f/src/objects/objects.cc
[modify] https://crrev.com/3bc7d790839a66378472bbeded1bfe66a06f156f/src/objects/transitions-inl.h
[modify] https://crrev.com/3bc7d790839a66378472bbeded1bfe66a06f156f/src/objects/transitions.cc
[modify] https://crrev.com/3bc7d790839a66378472bbeded1bfe66a06f156f/src/objects/transitions.h
[modify] https://crrev.com/3bc7d790839a66378472bbeded1bfe66a06f156f/test/cctest/BUILD.gn
[add] https://crrev.com/3bc7d790839a66378472bbeded1bfe66a06f156f/test/cctest/test-descriptor-array.cc
[modify] https://crrev.com/3bc7d790839a66378472bbeded1bfe66a06f156f/test/cctest/test-transitions.h


### ad...@google.com (2020-10-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-21)

albntomat0@gmail.com congratulations, the VRP panel has decided to award $5000 for this report. Someone from our finance team will get in touch. How would you like to be credited in the Chrome release notes?

### al...@gmail.com (2020-10-21)

Awesome, thank you! I would like to be credited as Bill Parks.

### ad...@chromium.org (2020-10-21)

Will do! Thanks for the report :)

### [Deleted User] (2020-10-22)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-10-22)

[Empty comment from Monorail migration]

### is...@chromium.org (2020-10-23)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-10-23)

ishell@ thanks for the description in https://crbug.com/chromium/1133527#c32 and https://crbug.com/chromium/1133527#c33. I'm going to also approve merge to M86, branch 4240. We're expecting to do one more M86 security refresh.

### ad...@chromium.org (2020-10-23)

(oh, and normally the addition of Merge-Merged labels would result in the removal of Merge-Approved labels... could you take care of that manually if the V8 processes don't do that?)

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/815b12dfb5ecd30bd524902d5692d2a6415fcdc1

commit 815b12dfb5ecd30bd524902d5692d2a6415fcdc1
Author: ishell@chromium.org <ishell@chromium.org>
Date: Tue Oct 27 14:47:06 2020

Merged: [runtime] Fix sorted order of DescriptorArray entries

Revision: 518d67ad652fc24b7eb03e48bb342f952d4ccf74

BUG=chromium:1133527
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=verwaest@chromium.org

Change-Id: I10831b27c5c10b9a967e47a5fd08f806ef5d306d
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2502328
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.6@{#34}
Cr-Branched-From: a64aed2333abf49e494d2a5ce24bbd14fff19f60-refs/heads/8.6.395@{#1}
Cr-Branched-From: a626bc036236c9bf92ac7b87dc40c9e538b087e3-refs/heads/master@{#69472}

[modify] https://crrev.com/815b12dfb5ecd30bd524902d5692d2a6415fcdc1/src/codegen/code-stub-assembler.cc
[modify] https://crrev.com/815b12dfb5ecd30bd524902d5692d2a6415fcdc1/src/codegen/code-stub-assembler.h
[modify] https://crrev.com/815b12dfb5ecd30bd524902d5692d2a6415fcdc1/src/diagnostics/objects-debug.cc
[modify] https://crrev.com/815b12dfb5ecd30bd524902d5692d2a6415fcdc1/src/objects/descriptor-array-inl.h
[modify] https://crrev.com/815b12dfb5ecd30bd524902d5692d2a6415fcdc1/src/objects/descriptor-array.h
[modify] https://crrev.com/815b12dfb5ecd30bd524902d5692d2a6415fcdc1/src/objects/fixed-array-inl.h
[modify] https://crrev.com/815b12dfb5ecd30bd524902d5692d2a6415fcdc1/src/objects/name-inl.h
[modify] https://crrev.com/815b12dfb5ecd30bd524902d5692d2a6415fcdc1/src/objects/name.h
[modify] https://crrev.com/815b12dfb5ecd30bd524902d5692d2a6415fcdc1/src/objects/objects.cc
[modify] https://crrev.com/815b12dfb5ecd30bd524902d5692d2a6415fcdc1/src/objects/transitions-inl.h
[modify] https://crrev.com/815b12dfb5ecd30bd524902d5692d2a6415fcdc1/src/objects/transitions.cc
[modify] https://crrev.com/815b12dfb5ecd30bd524902d5692d2a6415fcdc1/src/objects/transitions.h
[modify] https://crrev.com/815b12dfb5ecd30bd524902d5692d2a6415fcdc1/test/cctest/BUILD.gn
[add] https://crrev.com/815b12dfb5ecd30bd524902d5692d2a6415fcdc1/test/cctest/test-descriptor-array.cc
[modify] https://crrev.com/815b12dfb5ecd30bd524902d5692d2a6415fcdc1/test/cctest/test-transitions.h


### [Deleted User] (2020-10-27)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@chromium.org (2020-10-27)

Merges are done, removing the Merge-Approved labels.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/d4801c46fd21e8fdf6a19620b6c413c1d9e5dd5e

commit d4801c46fd21e8fdf6a19620b6c413c1d9e5dd5e
Author: Igor Sheludko <ishell@chromium.org>
Date: Tue Oct 27 21:12:04 2020

Revert "Merged: [runtime] Fix sorted order of DescriptorArray entries"

This reverts commit 815b12dfb5ecd30bd524902d5692d2a6415fcdc1.

Reason for revert: breaks M86 branch build in component mode (https://ci.chromium.org/p/chromium-m86/builders/ci/Linux%20Builder%20%28dbg%29)

Original change's description:
> Merged: [runtime] Fix sorted order of DescriptorArray entries
>
> Revision: 518d67ad652fc24b7eb03e48bb342f952d4ccf74
>
> BUG=chromium:1133527
> NOTRY=true
> NOPRESUBMIT=true
> NOTREECHECKS=true
> R=​verwaest@chromium.org
>
> Change-Id: I10831b27c5c10b9a967e47a5fd08f806ef5d306d
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2502328
> Reviewed-by: Toon Verwaest <verwaest@chromium.org>
> Cr-Commit-Position: refs/branch-heads/8.6@{#34}
> Cr-Branched-From: a64aed2333abf49e494d2a5ce24bbd14fff19f60-refs/heads/8.6.395@{#1}
> Cr-Branched-From: a626bc036236c9bf92ac7b87dc40c9e538b087e3-refs/heads/master@{#69472}

TBR=ishell@chromium.org,verwaest@chromium.org

Change-Id: Icfaae7cc5af778165929fcd50aead433421728c3
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:1133527
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2504509
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.6@{#36}
Cr-Branched-From: a64aed2333abf49e494d2a5ce24bbd14fff19f60-refs/heads/8.6.395@{#1}
Cr-Branched-From: a626bc036236c9bf92ac7b87dc40c9e538b087e3-refs/heads/master@{#69472}

[modify] https://crrev.com/d4801c46fd21e8fdf6a19620b6c413c1d9e5dd5e/src/codegen/code-stub-assembler.cc
[modify] https://crrev.com/d4801c46fd21e8fdf6a19620b6c413c1d9e5dd5e/src/codegen/code-stub-assembler.h
[modify] https://crrev.com/d4801c46fd21e8fdf6a19620b6c413c1d9e5dd5e/src/diagnostics/objects-debug.cc
[modify] https://crrev.com/d4801c46fd21e8fdf6a19620b6c413c1d9e5dd5e/src/objects/descriptor-array-inl.h
[modify] https://crrev.com/d4801c46fd21e8fdf6a19620b6c413c1d9e5dd5e/src/objects/descriptor-array.h
[modify] https://crrev.com/d4801c46fd21e8fdf6a19620b6c413c1d9e5dd5e/src/objects/fixed-array-inl.h
[modify] https://crrev.com/d4801c46fd21e8fdf6a19620b6c413c1d9e5dd5e/src/objects/name-inl.h
[modify] https://crrev.com/d4801c46fd21e8fdf6a19620b6c413c1d9e5dd5e/src/objects/name.h
[modify] https://crrev.com/d4801c46fd21e8fdf6a19620b6c413c1d9e5dd5e/src/objects/objects.cc
[modify] https://crrev.com/d4801c46fd21e8fdf6a19620b6c413c1d9e5dd5e/src/objects/transitions-inl.h
[modify] https://crrev.com/d4801c46fd21e8fdf6a19620b6c413c1d9e5dd5e/src/objects/transitions.cc
[modify] https://crrev.com/d4801c46fd21e8fdf6a19620b6c413c1d9e5dd5e/src/objects/transitions.h
[modify] https://crrev.com/d4801c46fd21e8fdf6a19620b6c413c1d9e5dd5e/test/cctest/BUILD.gn
[delete] https://crrev.com/d16a3908793f5953f41c669a381b225ff990fbfd/test/cctest/test-descriptor-array.cc
[modify] https://crrev.com/d4801c46fd21e8fdf6a19620b6c413c1d9e5dd5e/test/cctest/test-transitions.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/1a7d55a9a4274897e1e2e744b99800c3a491af7f

commit 1a7d55a9a4274897e1e2e744b99800c3a491af7f
Author: ishell@chromium.org <ishell@chromium.org>
Date: Wed Oct 28 12:16:45 2020

Merged: [runtime] Fix sorted order of DescriptorArray entries

Revision: 518d67ad652fc24b7eb03e48bb342f952d4ccf74

This is a reland of the previous merge which addresses the cctest link
failure in component build mode.

BUG=chromium:1133527
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=verwaest@chromium.org

Change-Id: Icbbc69fd5403fd0c2ab6d07d4340292b2b8c72b9
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2504264
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.6@{#40}
Cr-Branched-From: a64aed2333abf49e494d2a5ce24bbd14fff19f60-refs/heads/8.6.395@{#1}
Cr-Branched-From: a626bc036236c9bf92ac7b87dc40c9e538b087e3-refs/heads/master@{#69472}

[modify] https://crrev.com/1a7d55a9a4274897e1e2e744b99800c3a491af7f/src/codegen/code-stub-assembler.cc
[modify] https://crrev.com/1a7d55a9a4274897e1e2e744b99800c3a491af7f/src/codegen/code-stub-assembler.h
[modify] https://crrev.com/1a7d55a9a4274897e1e2e744b99800c3a491af7f/src/diagnostics/objects-debug.cc
[modify] https://crrev.com/1a7d55a9a4274897e1e2e744b99800c3a491af7f/src/objects/descriptor-array-inl.h
[modify] https://crrev.com/1a7d55a9a4274897e1e2e744b99800c3a491af7f/src/objects/descriptor-array.h
[modify] https://crrev.com/1a7d55a9a4274897e1e2e744b99800c3a491af7f/src/objects/fixed-array-inl.h
[modify] https://crrev.com/1a7d55a9a4274897e1e2e744b99800c3a491af7f/src/objects/name-inl.h
[modify] https://crrev.com/1a7d55a9a4274897e1e2e744b99800c3a491af7f/src/objects/name.h
[modify] https://crrev.com/1a7d55a9a4274897e1e2e744b99800c3a491af7f/src/objects/objects.cc
[modify] https://crrev.com/1a7d55a9a4274897e1e2e744b99800c3a491af7f/src/objects/transitions-inl.h
[modify] https://crrev.com/1a7d55a9a4274897e1e2e744b99800c3a491af7f/src/objects/transitions.cc
[modify] https://crrev.com/1a7d55a9a4274897e1e2e744b99800c3a491af7f/src/objects/transitions.h
[modify] https://crrev.com/1a7d55a9a4274897e1e2e744b99800c3a491af7f/test/cctest/BUILD.gn
[add] https://crrev.com/1a7d55a9a4274897e1e2e744b99800c3a491af7f/test/cctest/test-descriptor-array.cc
[modify] https://crrev.com/1a7d55a9a4274897e1e2e744b99800c3a491af7f/test/cctest/test-transitions.h


### ad...@google.com (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2

commit 47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2
Author: Igor Sheludko <ishell@chromium.org>
Date: Wed Nov 11 12:21:07 2020

[runtime] Deconfuse Name::Hash() from Name::hash_field()

This CL
* renames Name::hash_field field to raw_hash_field.
* all local variables that store raw_hash_field value are also renamed
  to raw_hash_field where possible.

Bug: chromium:1133527, v8:11074
Change-Id: I17313f386110b33a64f629cc2b9d4afd1e06c6c0
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2471999
Reviewed-by: Peter Marshall <petermarshall@chromium.org>
Reviewed-by: Ulan Degenbaev <ulan@chromium.org>
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/master@{#71114}

[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/ast/ast-value-factory.cc
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/ast/ast-value-factory.h
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/builtins/builtins-string-gen.cc
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/builtins/number.tq
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/codegen/code-stub-assembler.cc
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/compiler/access-builder.cc
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/compiler/access-builder.h
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/compiler/effect-control-linearizer.cc
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/diagnostics/objects-printer.cc
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/heap/factory-base.cc
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/heap/factory-base.h
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/heap/factory.cc
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/ic/accessor-assembler.cc
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/ic/stub-cache.cc
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/objects/lookup-cache-inl.h
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/objects/name-inl.h
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/objects/name.tq
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/objects/string-inl.h
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/objects/string-table-inl.h
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/objects/string-table.cc
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/objects/string-table.h
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/objects/string.cc
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/objects/string.tq
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/profiler/strings-storage.cc
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/snapshot/deserializer.cc
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/snapshot/deserializer.h
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/src/strings/string-hasher.h
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/test/cctest/test-debug-helper.cc
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/test/cctest/test-descriptor-array.cc
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/test/cctest/test-strings.cc
[modify] https://crrev.com/47ddc5b18042e50de1d91240e80d0d8fb9b9b0d2/test/fuzzer/regexp-builtins.cc


### [Deleted User] (2021-01-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1133527?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053470)*

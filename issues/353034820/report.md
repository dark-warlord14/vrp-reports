# TINT_ASSERT(to != nullptr) in src/tint/lang/wgsl/resolver/uniformity.cc:157

| Field | Value |
|-------|-------|
| **Issue ID** | [353034820](https://issues.chromium.org/issues/353034820) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn, Dawn>Tint |
| **Platforms** | Android |
| **Reporter** | de...@gmail.com |
| **Assignee** | jr...@google.com |
| **Created** | 2024-07-15 |
| **Bounty** | $10,000.00 |

## Description

## REPRODUCE

1. Download Dawn as follow: <https://dawn.googlesource.com/dawn/+/HEAD/docs/building.md>
2. gn gen out/tint
3. ninja -C out/tint tint
4. out/tint/tint poc.wgsl

## CRASH LOG

```
../../src/tint/lang/wgsl/resolver/uniformity.cc:157 internal compiler error: TINT_ASSERT(to != nullptr)
********************************************************************
*  The tint shader compiler has encountered an unexpected error.   *
*                                                                  *
*  Please help us fix this issue by submitting a bug report at     *
*  crbug.com/tint with the source program that triggered the bug.  *
********************************************************************
[1]    249973 illegal hardware instruction  out/tint/tint poc.wgsl

```
## CRASH INFO AND CREDIT

Type of crash: gpu

Reporter credit: gelatin dessert

## Attachments

- [poc.wgsl](attachments/poc.wgsl) (application/octet-stream, 1.5 KB)

## Timeline

### ja...@google.com (2024-07-16)

I was able to reproduce this. Can you take a look geofflang@?

CCing a few others as well

### ja...@chromium.org (2024-07-16)

Provisionally marking as S0 as this looks like it impacts GPU. This may change as we get more information about any mitigiations or how accessible this is without user interaction.

### am...@chromium.org (2024-07-16)

I'm going to lower severity here this given that I'm not sure how it demonstrates exploitable memory corruption in Chrome.
jrprice@ sorry to keep punting these to you, but you've chipped through them so effectively lately. But lmk if I should be assigning these elsewhere.

### pe...@google.com (2024-07-16)

Setting milestone because of s0/s1 severity.

### jr...@google.com (2024-07-19)

amyressler@ no problem, I'm the right point-of-contact for these.

The issue here is that we're missing some WGSL validation to prevent a `continue` statement from bypassing a variable declaration which is referenced in the continuing block of a loop. The input WGSL is invalid, but we don't catch it, which leads to problems further down the line. I've put a fix up here:
<https://dawn-review.googlesource.com/c/dawn/+/199455>

While reducing this test case, I found that one of the other side-effects of the missing validation (if the `TINT_ASSERT` is not triggered) is that we can generate invalid SPIR-V. Specifically, we can generate SPIR-V that has an SSA value declared in a block that does not dominate all of its uses. `spirv-val` catches this, but we don't run SPIR-V validation on Android devices. As discussed in [another issue](https://g-issues.chromium.org/issues/342840932#comment7), we have been conservatively considering these sorts of issues to be potentially security impacting, as we do not know what the native GPU driver will do with them. For this case, it's plausible to imagine that this could lead to generated code that reads and uses an uninitialized value.

### am...@chromium.org (2024-07-19)

Thanks for the info and background. Given that we don't know what the native GPU drive is going to do with the invalid SPIR-V, I concur we'd want to consider this as potentially security impacting. Since this does not impact Android, keeping this as high severity since the GPU process is sandboxed on the other impacted platforms, so this would not be considered critical.

### ap...@google.com (2024-07-19)

Project: dawn
Branch: main

commit da0ac02382cea2820e23f69be709c54e43900999
Author: James Price <jrprice@google.com>
Date:   Fri Jul 19 18:50:28 2024

    [tint] Fix continue bypassing decl check
    
    We were missing cases where a reference to a bypassed variable was
    inside another loop continuing block nested inside the outer loop's
    continuing block. Use a loop to check all parent continuing blocks,
    not just the first parent.
    
    Bug: 353034820
    Change-Id: Iffd4be81043f43f07aa39f87cd2d7f7fa4936c7f
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/199455
    Commit-Queue: David Neto <dneto@google.com>
    Commit-Queue: James Price <jrprice@google.com>
    Auto-Submit: James Price <jrprice@google.com>
    Reviewed-by: David Neto <dneto@google.com>

M       src/tint/lang/wgsl/resolver/resolver.cc
M       src/tint/lang/wgsl/resolver/validation_test.cc

https://dawn-review.googlesource.com/199455


### jr...@google.com (2024-07-19)

Sorry, to clarify: Android is the /only/ OS affected by this (because we do not run the validation to would catch it). No other OS is affected.

### am...@chromium.org (2024-07-19)

Oh sorry, you're right I completely mis-read that. Thank you for correcting me!

### ap...@google.com (2024-07-20)

Project: chromium/src
Branch: main

commit 5eb2f7d3ea5dca7a7a460e68273ce7875f95bd4f
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Sat Jul 20 01:16:27 2024

    Roll Dawn from b55e53f3f925 to b19b17b62694 (9 revisions)
    
    https://dawn.googlesource.com/dawn.git/+log/b55e53f3f925..b19b17b62694
    
    2024-07-19 bsheedy@google.com Set up Dawn shadow buckets
    2024-07-19 cwallez@chromium.org Make more WireTests use the C++ device/queue.
    2024-07-19 dneto@google.com [node] Use wgpu::Adapter::GetInfo instead of GetProperties
    2024-07-19 senorblanco@chromium.org Compat mode: modify an e2e test comment.
    2024-07-19 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 2bb0d0cf8207 to 1bc271cfc641 (13 revisions)
    2024-07-19 jrprice@google.com [tint] Fix continue bypassing decl check
    2024-07-19 dneto@google.com spir-v validation: use substring match on error message
    2024-07-19 dawn-automated-expectations@chops-service-accounts.iam.gserviceaccount.com Roll third_party/webgpu-cts/ 428adb446..5167b7163 (3 commits)
    2024-07-19 dawn-autoroll@skia-public.iam.gserviceaccount.com Roll DirectX Shader Compiler from 6f1c8e2443cd to 9c154fb190a3 (2 revisions)
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/dawn-chromium-autoroll
    Please CC cwallez@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64
    Bug: chromium:353034820,chromium:353294052,chromium:354101900
    Tbr: cwallez@google.com
    Include-Ci-Only-Tests: true
    Change-Id: I8af78c0badc71fe7c9bc9c78ece52a9e0d5652bb
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5727292
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1330622}

M       DEPS
M       third_party/dawn

https://chromium-review.googlesource.com/5727292


### pe...@google.com (2024-07-23)

Requesting merge to extended stable (M126) because latest trunk commit (1330622) appears to be after extended stable branch point (1300313).
Requesting merge to stable (M127) because latest trunk commit (1330622) appears to be after stable branch point (1313161).
Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### pe...@google.com (2024-07-24)

Requesting merge to extended stable (M126) because latest trunk commit (1330622) appears to be after extended stable branch point (1300313).
Requesting merge to stable (M127) because latest trunk commit (1330622) appears to be after stable branch point (1313161).
Not requesting merge to dev (M128) because latest trunk commit (1330622) appears to be prior to dev branch point (1331488). If this is incorrect please remove NA-128 from the 'Merge' field and add 128 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### am...@chromium.org (2024-07-25)

126 and 127 merges approved for <https://dawn-review.googlesource.com/c/dawn/+/199455>; please merge this fix to M126 branch 6478 and M127 branch 6533 at soonest / NLT 10am Friday, 26 July so this fix can be included in the next updates of Stable and Extended Stable

### ap...@google.com (2024-07-25)

Project: dawn
Branch: chromium/6533

commit 8d87a262de03ba1b4d0d5c1de9e48209fdc6946c
Author: James Price <jrprice@google.com>
Date:   Thu Jul 25 20:21:48 2024

    [tint] Fix continue bypassing decl check
    
    We were missing cases where a reference to a bypassed variable was
    inside another loop continuing block nested inside the outer loop's
    continuing block. Use a loop to check all parent continuing blocks,
    not just the first parent.
    
    Bug: 353034820
    Change-Id: Iffd4be81043f43f07aa39f87cd2d7f7fa4936c7f
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/199455
    Commit-Queue: David Neto <dneto@google.com>
    Commit-Queue: James Price <jrprice@google.com>
    Auto-Submit: James Price <jrprice@google.com>
    Reviewed-by: David Neto <dneto@google.com>
    (cherry picked from commit da0ac02382cea2820e23f69be709c54e43900999)
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/200056
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>

M       src/tint/lang/wgsl/resolver/resolver.cc
M       src/tint/lang/wgsl/resolver/validation_test.cc

https://dawn-review.googlesource.com/200056


### ap...@google.com (2024-07-25)

Project: dawn
Branch: chromium/6478

commit 6cd92b687aaa6eb578bd06110d4a4c5a73a6deb4
Author: James Price <jrprice@google.com>
Date:   Thu Jul 25 20:21:41 2024

    [tint] Fix continue bypassing decl check
    
    We were missing cases where a reference to a bypassed variable was
    inside another loop continuing block nested inside the outer loop's
    continuing block. Use a loop to check all parent continuing blocks,
    not just the first parent.
    
    Bug: 353034820
    Change-Id: Iffd4be81043f43f07aa39f87cd2d7f7fa4936c7f
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/199455
    Commit-Queue: David Neto <dneto@google.com>
    Commit-Queue: James Price <jrprice@google.com>
    Auto-Submit: James Price <jrprice@google.com>
    Reviewed-by: David Neto <dneto@google.com>
    (cherry picked from commit da0ac02382cea2820e23f69be709c54e43900999)
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/200055
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>

M       src/tint/lang/wgsl/resolver/resolver.cc
M       src/tint/lang/wgsl/resolver/validation_test.cc

https://dawn-review.googlesource.com/200055


### ap...@google.com (2024-07-25)

Project: dawn
Branch: chromium/6533

commit 8d87a262de03ba1b4d0d5c1de9e48209fdc6946c
Author: James Price <jrprice@google.com>
Date:   Thu Jul 25 20:21:48 2024

    [tint] Fix continue bypassing decl check
    
    We were missing cases where a reference to a bypassed variable was
    inside another loop continuing block nested inside the outer loop's
    continuing block. Use a loop to check all parent continuing blocks,
    not just the first parent.
    
    Bug: 353034820
    Change-Id: Iffd4be81043f43f07aa39f87cd2d7f7fa4936c7f
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/199455
    Commit-Queue: David Neto <dneto@google.com>
    Commit-Queue: James Price <jrprice@google.com>
    Auto-Submit: James Price <jrprice@google.com>
    Reviewed-by: David Neto <dneto@google.com>
    (cherry picked from commit da0ac02382cea2820e23f69be709c54e43900999)
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/200056
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>

M       src/tint/lang/wgsl/resolver/resolver.cc
M       src/tint/lang/wgsl/resolver/validation_test.cc

https://dawn-review.googlesource.com/200056


### jr...@google.com (2024-07-25)

Merges complete, LMK if anything else is needed here.

### sp...@google.com (2024-08-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
baseline report of potential memory corruption in a highly privileged process (GPU)


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-14)

While we don't generally consider internal compiler errors (ICE) on their own to be security issues, this report allowed the team to find and resolve a deeper issue with potential security implications. Thanks for your efforts in finding and reporting this issue to us -- nice work!

### pe...@google.com (2024-10-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> baseline report of potential memory corruption in a highly privileged process (GPU)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/353034820)*

# Google Chrome WebGL Buffer11::getBufferStorage Code Execution Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40052887](https://issues.chromium.org/issues/40052887) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2020-6542 |
| **Reporter** | vu...@sourcefire.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2020-07-20 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15

Steps to reproduce the problem:
1.
2.
3.

What is the expected behavior?

What went wrong?
### Summary

A code execution vulnerability exists in the webgl functionality of Google Chrome 84.0.4147.89 and Google Chrome 85.0.4169.0 (Developer Build) (64-bit). A specially crafted web page can cause a use after free. An attacker can create special website to trigger this vulnerability.

Did this work before? N/A 

Chrome version: Google Chrome Google Chrome 84.0.4147.89     Channel: n/a
OS Version: OS X 10.14.6
Flash Version: Shockwave Flash 32.0 r0

## Attachments

- [TALOS-2020-1127 - Google_Chrome_WebGL_Buffer11__getBufferStorage_Code_Execution_Vulnerability.txt](attachments/TALOS-2020-1127 - Google_Chrome_WebGL_Buffer11_getBufferStorage_Code_Execution_Vulnerability.txt) (text/plain, 34.6 KB)
- [chromium_poc.html](attachments/chromium_poc.html) (text/plain, 10.0 KB)

## Timeline

### cl...@chromium.org (2020-07-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5726193462083584.

### me...@chromium.org (2020-07-20)

This is windows-only right?

[Monorail components: Blink>WebGL]

### me...@chromium.org (2020-07-20)

[Comment Deleted]

### me...@chromium.org (2020-07-20)

I couldn't reproduce this on a win/asan/head build of Chrome. I got this error instead of a crash:
```
WebGL: INVALID_OPERATION: texImage2D: no texture bound to target
chromium_poc.html:446 WebGL: too many errors, no more errors will be reported to the console for this context.
update @ chromium_poc.html:446
update @ chromium_poc.html:454
...
update @ chromium_poc.html:454
Show 170 more frames
chromium_poc.html:445 Uncaught RangeError: Maximum call stack size exceeded
```
Let's see what CF finds.
I'm not very optimistic about CF finding this though since CF bots don't have GPUs so swiftshader will be used instead.
jmadill@ geofflang@ cwallez@ could one of you please take a look?

[Monorail components: -Blink>WebGL Internals>GPU>ANGLE]

### [Deleted User] (2020-07-21)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2020-07-21)

CC'ing some more people. Could someone from the GPU team please take a look at this?

### aj...@google.com (2020-07-21)

I am not able to reproduce this using ASAN build of HEAD. vulndiscovery@ did you test on a specific revision?

### cl...@chromium.org (2020-07-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5685736103280640.

### aj...@google.com (2020-07-22)

Ping? Could someone volunteer to take a deeper look?

### ge...@chromium.org (2020-07-22)

I can try reproducing but not until tomorrow. Someone else please take it if you can look earlier.

### jm...@chromium.org (2020-07-22)

Will look now. Sorry, didn't see this come by yesterday.

### vu...@sourcefire.com (2020-07-22)

From our researcher:

We tested: 
Google Chrome Google Chrome 84.0.4147.89
Google Chrome Google Chrome 85.0.4169.0 (Developer Build) (64-bit)

For ASAN you need the following flags: --no-sandbox --javascript-harmony --js-flags="--expose-gc"
For the release version of Chrome: you need to attach debugger to all children current and new to see the crash

### jm...@chromium.org (2020-07-22)

I can reproduce. Trying to reduce the test now. Thanks.

### [Deleted User] (2020-07-23)

[Empty comment from Monorail migration]

### aj...@google.com (2020-07-23)

Thanks for taking a look Adding Impact-Stable is it may be in M84.

### jm...@chromium.org (2020-07-23)

Fix in review: https://chromium-review.googlesource.com/c/angle/angle/+/2314216

Some infrastructure issues today hence a lot of test failures. The fix should be safe.

### [Deleted User] (2020-07-24)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/44bb4d7abee6a030afc6ad2e37ec63d6a4935203

commit 44bb4d7abee6a030afc6ad2e37ec63d6a4935203
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Jul 28 15:57:56 2020

D3D11: Fix bug with static vertex attributes.

In some specific cases after binding a zero size buffer we could end
up trying to use a buffer storage that was no longer valid. Fix this
by ensuring we don't flush dirty bits when we have an early exit due
to a zero size buffer.

Also adds a regression test.

Bug: chromium:1107433
Change-Id: I9db560e8dd3699abed2bb7fe6d91060148ba1817
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2314216
Commit-Queue: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/44bb4d7abee6a030afc6ad2e37ec63d6a4935203/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/44bb4d7abee6a030afc6ad2e37ec63d6a4935203/src/libANGLE/renderer/d3d/d3d11/VertexArray11.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2e015a6925a47701454884659c11d328b153a84c

commit 2e015a6925a47701454884659c11d328b153a84c
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jul 28 19:12:33 2020

Roll ANGLE from 52d2563373fa to 44bb4d7abee6 (8 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/52d2563373fa..44bb4d7abee6

2020-07-28 jmadill@chromium.org D3D11: Fix bug with static vertex attributes.
2020-07-28 nguyenmh@google.com Adds sampler serialization capability
2020-07-28 syoussefi@chromium.org Vulkan: Fix sub invalidate marking render targets undefined
2020-07-28 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Vulkan-ValidationLayers from 361fb5311b9b to 171e04fac342 (8 revisions)
2020-07-28 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SPIRV-Tools from 8b5ed4448dfe to 150be20d4334 (33 revisions)
2020-07-28 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 3b2cd31c7400 to 12c9d4ac61f2 (4 revisions)
2020-07-28 cclao@google.com Vulkan: Make staging buffer per context
2020-07-28 nguyenmh@google.com Serializes GL context states and reformats frame_capture_utils

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC tobine@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win-asan;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1107433
Tbr: tobine@google.com
Change-Id: Ia736d2e43c9b1e899c60ef43009a33d17fdc9a1e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2323762
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#792353}

[modify] https://crrev.com/2e015a6925a47701454884659c11d328b153a84c/DEPS


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-29)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/4866d0ad5f3c152ca41d38e1b243b4287753705c

commit 4866d0ad5f3c152ca41d38e1b243b4287753705c
Author: skia-autoroll <skia-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Jul 29 06:32:35 2020

Roll ANGLE from de309a42385f to c20449a879c6 (12 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/de309a42385f..c20449a879c6

2020-07-28 jmadill@chromium.org DEPS: Remove use_relative_hooks.
2020-07-28 cnorthrop@google.com Capture/Replay: Break up SetupContext
2020-07-28 jonahr@google.com Add mac_xcode_version gclient arg to DEPS
2020-07-28 jmadill@chromium.org Perf Tests: Use timestamp queries for GPU time.
2020-07-28 tobine@google.com Vulkan: Add new validation skips
2020-07-28 nguyenmh@google.com Remove context id serialization
2020-07-28 jmadill@chromium.org D3D11: Fix bug with static vertex attributes.
2020-07-28 nguyenmh@google.com Adds sampler serialization capability
2020-07-28 syoussefi@chromium.org Vulkan: Fix sub invalidate marking render targets undefined
2020-07-28 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Vulkan-ValidationLayers from 361fb5311b9b to 171e04fac342 (8 revisions)
2020-07-28 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SPIRV-Tools from 8b5ed4448dfe to 150be20d4334 (33 revisions)
2020-07-28 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 3b2cd31c7400 to 12c9d4ac61f2 (4 revisions)

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-skia-autoroll
Please CC borenet@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Cq-Include-Trybots: skia/skia.primary:Build-Debian10-Clang-x86_64-Release-ANGLE;skia/skia.primary:Test-Win10-Clang-AlphaR2-GPU-RadeonR9M470X-x86_64-Debug-All-ANGLE;skia/skia.primary:Test-Win10-Clang-Golo-GPU-QuadroP400-x86_64-Debug-All-ANGLE;skia/skia.primary:Test-Win10-Clang-NUC5i7RYH-GPU-IntelIris6100-x86_64-Debug-All-ANGLE;skia/skia.primary:Test-Win10-Clang-NUC6i5SYK-GPU-IntelIris540-x86_64-Debug-All-ANGLE;skia/skia.primary:Test-Win10-Clang-NUC8i5BEK-GPU-IntelIris655-x86_64-Debug-All-ANGLE;skia/skia.primary:Test-Win10-Clang-NUCD34010WYKH-GPU-IntelHD4400-x86_64-Debug-All-ANGLE
Bug: chromium:1107325,chromium:1107433
Tbr: borenet@google.com
Test: Test: NBA2K20 MEC
Change-Id: I094230ff6499be68990551fb02ce49d55c97e662
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/306311
Reviewed-by: skia-autoroll <skia-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: skia-autoroll <skia-autoroll@skia-public.iam.gserviceaccount.com>

[modify] https://crrev.com/4866d0ad5f3c152ca41d38e1b243b4287753705c/DEPS


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f1b856b30bc9ab6ff4fa91f355d481b5344c63e3

commit f1b856b30bc9ab6ff4fa91f355d481b5344c63e3
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Jul 29 09:51:11 2020

Roll Skia from 620bfa3fffba to 4866d0ad5f3c (1 revision)

https://skia.googlesource.com/skia.git/+log/620bfa3fffba..4866d0ad5f3c

2020-07-29 skia-autoroll@skia-public.iam.gserviceaccount.com Roll ANGLE from de309a42385f to c20449a879c6 (12 revisions)

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/skia-autoroll
Please CC borenet@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
Bug: chromium:1107325,chromium:1107433
Tbr: borenet@google.com
Test: Test: Test: NBA2K20 MEC
Change-Id: I8f1f51d7d79fdaf5bcf752b10bf84c4d603fa86f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2325690
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#792627}

[modify] https://crrev.com/f1b856b30bc9ab6ff4fa91f355d481b5344c63e3/DEPS


### sr...@google.com (2020-07-30)

This bug is marked as RBS for M85. M85 has been promoted to beta. Please help review this bug if this indeed should block the stable release for M85, if not please remove RBS label, If it is a RBS , please help get a fix ready for merge to M85 asap so we can bake the fix on beta channel asap.

Beta release happens every wednesday and beta RC gets cut on Tuesday afternoon 3pm PST. Please help get the fixes landed and verified on canary so that the changes can be merged in time for beta release.

### jm...@chromium.org (2020-07-30)

Marking fixed and merge quest. See the fix here:

https://chromium-review.googlesource.com/c/angle/angle/+/2314216/6/src/libANGLE/renderer/d3d/d3d11/VertexArray11.cpp

Should be safe. According to reporter this is a code execution vulnerability.

### [Deleted User] (2020-07-30)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2020-07-30)

re: https://crbug.com/chromium/1107433#c25, see https://crbug.com/chromium/1107433#c24

### [Deleted User] (2020-07-31)

[Empty comment from Monorail migration]

### sr...@google.com (2020-07-31)

Merge approved for M85 branch:4183 please merge asap

### ad...@google.com (2020-08-03)

[Empty comment from Monorail migration]

### sr...@google.com (2020-08-03)

Please complete your merges to M85 branch before 2pm PST tuesday Aug 4th 2020, so they can be included in this week's beta release.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/006ab354313b493ccb6eba909e0831bb0b13aea7

commit 006ab354313b493ccb6eba909e0831bb0b13aea7
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Aug 03 21:06:23 2020

D3D11: Fix bug with static vertex attributes.

In some specific cases after binding a zero size buffer we could end
up trying to use a buffer storage that was no longer valid. Fix this
by ensuring we don't flush dirty bits when we have an early exit due
to a zero size buffer.

Also adds a regression test.

Bug: chromium:1107433
Change-Id: I9db560e8dd3699abed2bb7fe6d91060148ba1817
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2335022
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/006ab354313b493ccb6eba909e0831bb0b13aea7/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/006ab354313b493ccb6eba909e0831bb0b13aea7/src/libANGLE/renderer/d3d/d3d11/VertexArray11.cpp


### ad...@google.com (2020-08-03)

If no problems have shown up in canary, please also merge to M84, branch 4147.

### mm...@chromium.org (2020-08-05)

jmadill@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ad...@google.com (2020-08-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-05)

Congratulations! The VRP panel decided to award $10,000 for this report. Someone from our finance team will be in touch to arrange payment.

### ad...@google.com (2020-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/29a4abf96a83a1958675dd5c2870a1677cc011b7

commit 29a4abf96a83a1958675dd5c2870a1677cc011b7
Author: Jamie Madill <jmadill@chromium.org>
Date: Fri Aug 07 16:54:53 2020

D3D11: Fix bug with static vertex attributes.

In some specific cases after binding a zero size buffer we could end
up trying to use a buffer storage that was no longer valid. Fix this
by ensuring we don't flush dirty bits when we have an early exit due
to a zero size buffer.

Bug: chromium:1107433
Change-Id: I9db560e8dd3699abed2bb7fe6d91060148ba1817
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2343405
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/29a4abf96a83a1958675dd5c2870a1677cc011b7/src/libANGLE/renderer/d3d/d3d11/VertexArray11.cpp


### go...@chromium.org (2020-08-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-07)

[Empty comment from Monorail migration]

### mm...@google.com (2020-08-11)

[Empty comment from Monorail migration]

### vu...@sourcefire.com (2020-08-17)

Is this planned for 12 Sept public disclosure along with other issues reported for M84 release?

### ad...@google.com (2020-08-17)

This bug will become publicly visible 14 weeks after the date it was Fixed (#c24) which would be 5th November by my math.

### vu...@sourcefire.com (2020-09-14)

This issue reached 90 days on 2020-10-20. Per our 90 day policy, it is subject to public disclosure at that time. 5th November would put it around 115 days or so.

### ad...@google.com (2020-09-14)

OK. On this occasion, I'm happy to open up this bug on 2020-10-20. Please feel free to get in touch when you've published your information, and I will remove view restrictions on this bug. This won't affect the VRP reward. (The same will apply to https://crbug.com/chromium/1105202).

We are confident that the vast majority of Chrome users will have received the fix well before then. However, please note in our FAQ that the 14 week timescale exists partly so that other products also have plenty of time to absorb the fix (https://chromium.googlesource.com/chromium/src/+/master/docs/security/faq.md#can-you-please-un_hide-old-security-bugs). Downstream Chromium embedders typically don't find out about the bug until we've fixed it within Chromium (that's when the bug transitions from Restrict-View-SecurityTeam to Restrict-View-SecurityNotify).

Therefore, please take heed of the warning in https://bugs.chromium.org/p/chromium/issues/detail?id=1107433#c34 - earlier disclosure may cancel VRP rewards. Not all fixes will land as quickly as this one, and therefore it's unlikely that your 90 days and our 14 weeks will happen to line up so closely in most cases. You may of course decide to disclose early anyway!

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### vu...@sourcefire.com (2020-10-13)

Can you provide the CVE for this issue?

### ad...@google.com (2020-10-13)

It's CVE-2020-6542.

### vu...@sourcefire.com (2020-10-20)

The advisory is published


### [Deleted User] (2020-11-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1107433?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052887)*

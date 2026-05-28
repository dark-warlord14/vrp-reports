# Security:Debug check failed: HasBuiltinId() implies builtin_id() != Builtin::kCompileLazy.

| Field | Value |
|-------|-------|
| **Issue ID** | [40064282](https://issues.chromium.org/issues/40064282) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | wh...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2023-04-29 |
| **Bounty** | $8,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**

# Fatal error in ../../src/objects/shared-function-info.cc, line 683

# Debug check failed: HasBuiltinId() implies builtin\_id() != Builtin::kCompileLazy.

# 

**VERSION**  

only tested current head

**REPRODUCTION CASE**  

use default x64.debug  

run ./d8 1.js

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- [1.js](attachments/1.js) (text/plain, 1.2 KB)

## Timeline

### [Deleted User] (2023-04-29)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-04-29)

sorry, please using fuzzbuild-d8 to reproduce, I can't reproduce using default x64.debug d8.
fuzzbuild-d8 : 
```
gn gen out/fuzzbuild --args='is_debug=false dcheck_always_on=true v8_static_library=true v8_enable_slow_dchecks=true v8_enable_v8_checks=true v8_enable_verify_heap=true v8_enable_verify_csa=true v8_fuzzilli=true sanitizer_coverage_flags="trace-pc-guard" target_cpu="x64"'
ninja -C ./out/fuzzbuild d8
```

#2  0x0000555555d062f7 in V8_Fatal () at ../../src/base/logging.cc:167
#3  0x0000555555d05c35 in v8::base::(anonymous namespace)::DefaultDcheckHandler(char const*, int, char const*) () at ../../src/base/logging.cc:57
#4  0x0000555557065d84 in StartPosition () at ../../src/objects/shared-function-info.cc:683
#5  0x0000555557170662 in ParseFunction () at ../../src/parsing/parsing.cc:80
#6  0x0000555556088639 in Compile () at ../../src/codegen/compiler.cc:2517
#7  0x000055555608a9c8 in Compile () at ../../src/codegen/compiler.cc:2579
#8  0x0000555557437140 in __RT_impl_Runtime_CompileLazy () at ../../src/runtime/runtime-compiler.cc:64
#9  0x0000555557436818 in Runtime_CompileLazy () at ../../src/runtime/runtime-compiler.cc:45
#10 0x0000555558d41e76 in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit ()
#11 0x0000555558c96ff1 in Builtins_CompileLazy ()
#12 0x0000555558c95be6 in Builtins_InterpreterEntryTrampoline ()
#13 0x0000035900175b99 in ?? ()


### pg...@google.com (2023-04-29)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### pg...@google.com (2023-05-02)

Can reproduce on M114 and M115

A debug check failure at the same place (https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/shared-function-info.cc;l=683) was fixed before (https://crbug.com/chromium/956848) - setting owner to be the same - bmeurer@ could you take a look?

### bm...@chromium.org (2023-05-03)

Over to V8 for triaging.

### va...@chromium.org (2023-05-09)

Current security sheriff, PTAL

### is...@chromium.org (2023-05-09)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-05-10)

Sorry, I forget it. 

bisect 
I tested at commit 6b4700b59ed4544247a6739b3d7c002f6c2bed35 which can reproduce.
and before one commit 4fb4f9a57f796fa98fe7826670e3de85895d5467 which failed to reproduce.

https://chromium-review.googlesource.com/c/v8/v8/+/4422047
6b4700b59ed4544247a6739b3d7c002f6c2bed35
[interpreter] Fix hole elision for try and labeled blocks

This CL fixes TDZ hole check elision for try-catch, try-finally, and
labeled blocks. Credit to Kevin Gibbons (https://github.com/bakkot) for
pointing these out.
...

active release branch: 114/beta and 115/dev

### wh...@gmail.com (2023-05-10)

Re https://crbug.com/chromium/1441254#c4

> A debug check failure at the same place (https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/shared-function-info.cc;l=683) was fixed before (https://crbug.com/chromium/956848) -

From crash stack and commit which introduced the bug, I thinks the bug related interpreter component, should be security bug.



### is...@chromium.org (2023-05-22)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Runtime]

### gi...@appspot.gserviceaccount.com (2023-05-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/0e07abe6ae3828b12d2555abae45ac78f165d061

commit 0e07abe6ae3828b12d2555abae45ac78f165d061
Author: Igor Sheludko <ishell@chromium.org>
Date: Wed May 24 09:26:30 2023

[runtime] Create unoptimized data even if compilation is aborted

... because of stack overflow.

Bug: chromium:1441254
Change-Id: I802ab8b9c8093968f55dc6da113791ee35bae301
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4560025
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/heads/main@{#87829}

[modify] https://crrev.com/0e07abe6ae3828b12d2555abae45ac78f165d061/src/codegen/compiler.cc
[modify] https://crrev.com/0e07abe6ae3828b12d2555abae45ac78f165d061/src/objects/shared-function-info.cc
[modify] https://crrev.com/0e07abe6ae3828b12d2555abae45ac78f165d061/src/objects/shared-function-info.h


### gi...@appspot.gserviceaccount.com (2023-05-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/c4bace41c896eeceed948b365855ec0048880439

commit c4bace41c896eeceed948b365855ec0048880439
Author: Igor Sheludko <ishell@chromium.org>
Date: Thu May 25 09:10:44 2023

[class] Support reparsing of static initializers

Drive-by:
 - introduce --stress-lazy-compilation=N flag for simulating
   stack overflows during bytecode generation,
 - remove usages of --harmony-public-fields and --harmony-static-fields
   from the tests as these features are already shipped.

Bug: chromium:1441254
Change-Id: Idb97bf21df936b9ce268c65602a9a01827692d1c
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4561926
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Auto-Submit: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/main@{#87855}

[modify] https://crrev.com/c4bace41c896eeceed948b365855ec0048880439/src/flags/flag-definitions.h
[modify] https://crrev.com/c4bace41c896eeceed948b365855ec0048880439/test/inspector/debugger/get-possible-breakpoints-class-fields-expected.txt
[modify] https://crrev.com/c4bace41c896eeceed948b365855ec0048880439/test/inspector/debugger/get-possible-breakpoints-class-fields.js
[modify] https://crrev.com/c4bace41c896eeceed948b365855ec0048880439/test/debugger/debug/debug-break-class-fields.js
[modify] https://crrev.com/c4bace41c896eeceed948b365855ec0048880439/src/execution/local-isolate.h
[modify] https://crrev.com/c4bace41c896eeceed948b365855ec0048880439/src/parsing/parser.h
[modify] https://crrev.com/c4bace41c896eeceed948b365855ec0048880439/src/parsing/parser-base.h
[modify] https://crrev.com/c4bace41c896eeceed948b365855ec0048880439/test/mjsunit/regress/regress-7642.js
[modify] https://crrev.com/c4bace41c896eeceed948b365855ec0048880439/test/mjsunit/code-coverage-class-fields.js
[modify] https://crrev.com/c4bace41c896eeceed948b365855ec0048880439/src/parsing/parser.cc
[modify] https://crrev.com/c4bace41c896eeceed948b365855ec0048880439/src/interpreter/bytecode-generator.cc
[modify] https://crrev.com/c4bace41c896eeceed948b365855ec0048880439/test/inspector/debugger/class-fields-scopes.js
[add] https://crrev.com/c4bace41c896eeceed948b365855ec0048880439/test/mjsunit/regress/regress-crbug-1441254.js


### is...@chromium.org (2023-05-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-05-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/344c6df95371908fe5b057b286b09ca682d31943

commit 344c6df95371908fe5b057b286b09ca682d31943
Author: Igor Sheludko <ishell@chromium.org>
Date: Thu May 25 11:07:45 2023

[class] Fix --stress-lazy-compilation vs. TSan issue

... and enable the --stress-lazy-compilation machinery.

Bug: chromium:1441254
Change-Id: I4e59862ccd2dd81b3928df628ac48296cad52177
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4566303
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Auto-Submit: Igor Sheludko <ishell@chromium.org>
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/main@{#87858}

[modify] https://crrev.com/344c6df95371908fe5b057b286b09ca682d31943/src/interpreter/bytecode-generator.cc


### gi...@appspot.gserviceaccount.com (2023-05-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/1b55293a7140eb9310638621987c6d90dc00a80f

commit 1b55293a7140eb9310638621987c6d90dc00a80f
Author: Igor Sheludko <ishell@chromium.org>
Date: Thu May 25 13:04:54 2023

[class] Export SharedFunctionInfo::CreateAndSetUncompiledData

... as a speculative fix for linking issues.

Bug: chromium:1441254
Change-Id: Icb071a1d54f7b6024d2dd6ac4f6a53194d86ab86
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4565376
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Auto-Submit: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/heads/main@{#87863}

[modify] https://crrev.com/1b55293a7140eb9310638621987c6d90dc00a80f/src/objects/shared-function-info.cc


### [Deleted User] (2023-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/af794976088fea039b8efcf68b7d03f01b81c814

commit af794976088fea039b8efcf68b7d03f01b81c814
Author: Igor Sheludko <ishell@chromium.org>
Date: Tue May 30 16:52:40 2023

[class] Declare "this" when deserializing scope chain

... of class member initializer functions.

Bug: chromium:1441254, chromium:1449054
Change-Id: I52f8a714e7f9e991817f9cd37d25eb9a7fa99bb2
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4573678
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/main@{#87988}

[add] https://crrev.com/af794976088fea039b8efcf68b7d03f01b81c814/test/mjsunit/regress/regress-crbug-1449054.js
[modify] https://crrev.com/af794976088fea039b8efcf68b7d03f01b81c814/src/parsing/parser.cc


### is...@chromium.org (2023-06-01)

I think only the CLs in https://crbug.com/chromium/1441254#c11+#c15 should to be back merged. 

The CLs in https://crbug.com/chromium/1441254#c12, https://crbug.com/chromium/1441254#c14, https://crbug.com/chromium/1441254#c18 address correctness issue related to a bug in reparsing of class static intializers exposed by this POC.

### am...@chromium.org (2023-06-01)

Updating to security bug (additionally can appear in the security merge review queue); 
Since there has been human intervention with merge labels, adding merge label for 115, as the CL in https://crbug.com/chromium/1441254#c15 (to be evaluated for backmerge) landed on 116
(as sheriffbot won't update with additional merge labels despite the reclassification of this as a security bug) 

### wh...@gmail.com (2023-06-01)

[Comment Deleted]

### [Deleted User] (2023-06-02)

Merge review required: M115 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-02)

Merge review required: M114 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@chromium.org (2023-06-02)

1. This issue might have security implications.
2. https://chromium-review.googlesource.com/c/v8/v8/+/4560025 and https://chromium-review.googlesource.com/c/v8/v8/+/4565376
3. Yes, see https://chromiumdash.appspot.com/commit/0e07abe6ae3828b12d2555abae45ac78f165d061
4. No.
5. n/a
6. No.

### am...@chromium.org (2023-06-06)

115 and 114 merges for the CLs specified in item #2 in https://crbug.com/chromium/1441254#c24 above approved 
please merge this fix to M115/ 11.5-lkgr by EOD tomorrow (Tuesday, 6 June) so this fix can be included in M115 beta 
please merge this fix to M114/11.4-lkgr by 10am Pacific on Friday, 9 June so this fix can be included in the next M114/stable security update 


### am...@chromium.org (2023-06-06)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-06-06)

[Comment Deleted]

### am...@google.com (2023-06-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-09)

Congratulations! The VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us!

Re https://crbug.com/chromium/1441254#c27, regarding CVE: 
1) CVEs are only issued at the time the security fix is released in a Stable update of Chrome
2) CVEs are issued for bugs that impact Stable and Extended Stable; we do not issue CVEs for that do not impact Stable versions of Chrome

### wh...@gmail.com (2023-06-09)

Thanks.

### wh...@gmail.com (2023-06-09)

[Comment Deleted]

### go...@chromium.org (2023-06-09)

Please help complete the M114 merges before 12pm PST today, Friday June 9, so we can include the change in the RC build for re-spin next week. 

RC cut today @12:30 PM PT. 

### gi...@appspot.gserviceaccount.com (2023-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/b88cfd76d3cf2463619b1a890d1d3df0375de6f6

commit b88cfd76d3cf2463619b1a890d1d3df0375de6f6
Author: Leszek Swirski <leszeks@google.com>
Date: Fri Jun 09 15:17:18 2023

Merged: Squashed multiple commits.

Merged: [runtime] Create unoptimized data even if compilation is aborted
Revision: 0e07abe6ae3828b12d2555abae45ac78f165d061

Merged: [class] Export SharedFunctionInfo::CreateAndSetUncompiledData
Revision: 1b55293a7140eb9310638621987c6d90dc00a80f

BUG=chromium:1441254
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=verwaest@chromium.org

Change-Id: I39c4ab864776a9138d07c3c1dccd3a2be4acfe7c
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4604769
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.4@{#43}
Cr-Branched-From: 8a8a1e7086dacc426965d3875914efa66663c431-refs/heads/11.4.183@{#1}
Cr-Branched-From: 5483d8e816e0bbce865cbbc3fa0ab357e6330bab-refs/heads/main@{#87241}

[modify] https://crrev.com/b88cfd76d3cf2463619b1a890d1d3df0375de6f6/src/codegen/compiler.cc
[modify] https://crrev.com/b88cfd76d3cf2463619b1a890d1d3df0375de6f6/src/objects/shared-function-info.cc
[modify] https://crrev.com/b88cfd76d3cf2463619b1a890d1d3df0375de6f6/src/objects/shared-function-info.h


### le...@chromium.org (2023-06-09)

Merged to 11.4 in https://chromium-review.googlesource.com/c/v8/v8/+/4604769 since this needs immediate attention, I'll let Igor handle the 11.5 merge

### am...@chromium.org (2023-06-09)

[re: https://crbug.com/chromium/1441254#c31] Hello, we appreciate your bisect, but we feel that $1,000 is a sufficient reward for the bisect provided as it does not meet the criteria for the $2,000 bisect bonus as stipulated by the criteria in the Chrome VRP policies: 

"Example verification for the $2,000 bisect bonus would include ASAN stack trace output from builds for each active release channel, POC or reproduction steps specific to the particular release versions, or video reproduction demonstrating successful reproduction across all active releases channels impacted by the vulnerability."

### [Deleted User] (2023-06-09)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/8459fe6ec0eb9ac169240e7b9323860eb285af0b

commit 8459fe6ec0eb9ac169240e7b9323860eb285af0b
Author: Igor Sheludko <ishell@chromium.org>
Date: Fri Jun 09 14:37:15 2023

Merged: Squashed multiple commits.

Merged: [runtime] Create unoptimized data even if compilation is aborted
(cherry picked from commit 0e07abe6ae3828b12d2555abae45ac78f165d061)

Merged: [class] Export SharedFunctionInfo::CreateAndSetUncompiledData
(cherry picked from commit 1b55293a7140eb9310638621987c6d90dc00a80f)

Bug: chromium:1441254
Change-Id: I3c78d3972295c147d79d3734a4869c9b36f19433
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4603931
Auto-Submit: Igor Sheludko <ishell@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.5@{#10}
Cr-Branched-From: 0c4044b7336787781646e48b2f98f0c7d1b400a5-refs/heads/11.5.150@{#1}
Cr-Branched-From: b71d3038a7d99c79e1c21239e8ae07da5fc8c90b-refs/heads/main@{#87781}

[modify] https://crrev.com/8459fe6ec0eb9ac169240e7b9323860eb285af0b/src/codegen/compiler.cc
[modify] https://crrev.com/8459fe6ec0eb9ac169240e7b9323860eb285af0b/src/objects/shared-function-info.cc
[modify] https://crrev.com/8459fe6ec0eb9ac169240e7b9323860eb285af0b/src/objects/shared-function-info.h


### jk...@chromium.org (2023-06-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3fc83916220a3535a1523ecacf221597c9925d16

commit 3fc83916220a3535a1523ecacf221597c9925d16
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Jun 09 19:46:52 2023

Roll v8 11.5 from 6cdd546a3979 to 87971e779478 (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/6cdd546a3979..87971e779478

2023-06-09 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.5.150.6
2023-06-09 ishell@chromium.org Merged: Squashed multiple commits.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-11-5-chromium-m115
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.5: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m115: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1441254
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I90fac20ec37a88c2deda7cefb2882ada651401e6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4605735
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5790@{#545}
Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

[modify] https://crrev.com/3fc83916220a3535a1523ecacf221597c9925d16/DEPS


### am...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/303266edf1553130640bae4da515a44a2d5c4762

commit 303266edf1553130640bae4da515a44a2d5c4762
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Jun 09 23:40:17 2023

Roll v8 11.4 from 22206605545f to 3754be12c7ff (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/22206605545f..3754be12c7ff

2023-06-09 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.4.183.22
2023-06-09 leszeks@google.com Merged: Squashed multiple commits.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-11-4-chromium-m114
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.4: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m114: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1441254
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I95a110b3e996e2bf1f6f63b0e33fa4204b005f7b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4605617
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1231}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/303266edf1553130640bae4da515a44a2d5c4762/DEPS


### [Deleted User] (2023-08-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-31)

This issue was migrated from crbug.com/chromium/1441254?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Runtime]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064282)*

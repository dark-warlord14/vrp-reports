# UAF in AsyncCompileJob::Abort

| Field | Value |
|-------|-------|
| **Issue ID** | [40062372](https://issues.chromium.org/issues/40062372) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2022-12-24 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**  

tested chrome version:  

Chromium 111.0.5497.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1086812.zip)  

Chromium 110.0.5478.4  

os version:  

22.04  

repro steps:  

(1) python3 -m http.server 8000 --dir=|Directory path for containing the crash.html file.|  

(2) ./chrome --incognito <http://localhost:8000/crash.html>

**Problem Description:**  

I submitted this issue (<https://bugs.chromium.org/p/chromium/issues/detail?id=1400122>) two weeks ago. Because cf couldn't reproduce the issue, the issue was automatically closed. So I'm resubmitting it here (can be merged to one).  

I noticed there is a related CL (change list) recently:  

\*since many methods actually delete the  

{AsyncCompileJob}\*, so calling such methods twice would lead to a  

use-after-free.  

<https://chromium-review.googlesource.com/c/v8/v8/+/4110762>

After deleting |AsyncCompileJob| through calling WasmEngine::DeleteCompileJobsOnContext[0], a UAF (use-after-free) still occurs when calling abort[1].

void WasmEngine::DeleteCompileJobsOnContext(Handle<Context> context) {  

// Under the mutex get all jobs to delete. Then delete them without holding  

// the mutex, such that deletion can reenter the WasmEngine.  

std::vector<std::unique\_ptr<AsyncCompileJob>> jobs\_to\_delete;  

{  

base::MutexGuard guard(&mutex\_);  

for (auto it = async\_compile\_jobs\_.begin();  

it != async\_compile\_jobs\_.end();) {  

if (!it->first->context().is\_identical\_to(context)) {  

++it;  

continue;  

}  

jobs\_to\_delete.push\_back(std::move(it->second));  

it = async\_compile\_jobs\_.erase(it);  

}  

}  

}  

[0]<https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/wasm-engine.cc;drc=51bdde997e642b6e1dd971b361d41d7b92f19053;l=961>  

void AsyncStreamingProcessor::OnAbort() {  

TRACE\_STREAMING("Abort stream...\n");  

if (validate\_functions\_job\_handle\_) {  

validate\_functions\_job\_handle\_->Cancel();  

validate\_functions\_job\_handle\_.reset();  

}  

if (job\_->native\_module\_ && job\_->native\_module\_->wire\_bytes().empty()) { <---uaf here  

// Clean up the temporary cache entry.  

GetWasmEngine()->StreamingCompilationFailed(prefix\_hash\_);  

}  

// {Abort} invalidates the {AsyncCompileJob}.  

job\_->Abort();  

job\_ = nullptr;  

}  

[1]<https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/module-compiler.cc;drc=51bdde997e642b6e1dd971b361d41d7b92f19053;l=2926>

I don't have permission to see the issue in the CL above, so I'm not sure if it's a duplicate issue.  

BTW, I hope that the automatic closing feature of CF can be optimized. The experience does not feel very good for me:(.

**Additional Comments:**

\*\*Chrome version: \*\* 110.0.5478.4 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 318 B)
- [asan2.log](attachments/asan2.log) (text/plain, 26.6 KB)

## Timeline

### [Deleted User] (2022-12-24)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-12-26)

Thanks for filing another report and sorry for the inconvenience caused by CF (cc'ed some Smithy team members as FYI. Maybe CF can provide a reason when it auto closes a bug).

I'm able to reproduce with the --no-sandbox flag. Based on https://crbug.com/1400066, it is a bug introduced in M110 so adding FoundIn-110 label.

+clemensb@, could you take a look? This bug may provide a reliable way to reproduce the crash. Thanks!

[Monorail components: Blink>JavaScript>WebAssembly]

### [Deleted User] (2022-12-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-26)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-26)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-26)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-01-03)

Thanks for this report! This indeed illustrates the problem I was hunting after very well.

### ad...@google.com (2023-01-04)

xinghuliu@ hello. I'm trying to hunt down why this didn't reproduce on ClusterFuzz originally (when it was reported as https://crbug.com/chromium/1400122). Did you make any changes at all to crash.html, e.g. changing the "xxx"? Did it reproduce immediately? Did you have to retry? Did you find that you needed both --no-sandbox and --incognito to reproduce? Do you have any other hints?

### xi...@chromium.org (2023-01-04)

Re https://crbug.com/chromium/1403531#c8: I didn't make any changes to crash.html. --incognito alone doesn't reproduce. It reproduced with --incognito and --no-sandbox together. I didn't try --no-sandbox alone.

No it doesn't reproduce immediately. I notice that the PoC was continuously adding '?2' at the end of the URL and reloading the page until the page crashes. How fast it is reproduced depends on when the race condition actually gets triggered. It takes 5-10 seconds to reproduce from my redshell.

### gi...@appspot.gserviceaccount.com (2023-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/68047ec37fa5716528656a51927dda885691ff4a

commit 68047ec37fa5716528656a51927dda885691ff4a
Author: Clemens Backes <clemensb@chromium.org>
Date: Wed Jan 04 16:20:51 2023

[wasm][streaming] Avoid UAF after context disposal

After a call to {StreamingDecoder::NotifyCompilationEnded}, no method on
the {StreamingProcessor} should be called any more. We were still
calling the {OnAbort} method later.

To make the semantics a bit more clear, we rename
{NotifyCompilationEnded} to {NotifyCompilationDiscarded}.

We also remove the {stream_finished_} field and reset the processor
instead, which will result in a nullptr access if we try to illegally
call any further methods.

R=ahaas@chromium.org

Bug: chromium:1403531, chromium:1399790, chromium:1400066
Change-Id: I4caef3801dfe9d653125efbd7bc9b5d13ce30dc7
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4132966
Reviewed-by: Andreas Haas <ahaas@chromium.org>
Commit-Queue: Clemens Backes <clemensb@chromium.org>
Cr-Commit-Position: refs/heads/main@{#85114}

[modify] https://crrev.com/68047ec37fa5716528656a51927dda885691ff4a/src/wasm/streaming-decoder.cc
[modify] https://crrev.com/68047ec37fa5716528656a51927dda885691ff4a/src/wasm/sync-streaming-decoder.cc
[modify] https://crrev.com/68047ec37fa5716528656a51927dda885691ff4a/test/cctest/test-api.cc
[modify] https://crrev.com/68047ec37fa5716528656a51927dda885691ff4a/src/wasm/module-compiler.cc
[modify] https://crrev.com/68047ec37fa5716528656a51927dda885691ff4a/src/wasm/streaming-decoder.h
[modify] https://crrev.com/68047ec37fa5716528656a51927dda885691ff4a/test/cctest/cctest.status
[modify] https://crrev.com/68047ec37fa5716528656a51927dda885691ff4a/src/wasm/wasm-js.h
[modify] https://crrev.com/68047ec37fa5716528656a51927dda885691ff4a/src/wasm/wasm-js.cc


### cl...@chromium.org (2023-01-05)

This should be fixed. Let's merge it to all channels once this has some Canary coverage.
Hopefully this also fixes the two crash signatures of https://crbug.com/1399790 and https://crbug.com/1400066.

### cl...@chromium.org (2023-01-05)

To be precise: This only needs to be merged to the V8 10.0 branch.

### [Deleted User] (2023-01-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-05)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M110. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-06)

Merge approved: your change passed merge requirements and is auto-approved for M110. Please go ahead and merge the CL to branch 5481 (refs/branch-heads/5481) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/3157f2dba49a06a7519e8d28144e019406185af3

commit 3157f2dba49a06a7519e8d28144e019406185af3
Author: Clemens Backes <clemensb@chromium.org>
Date: Mon Jan 09 08:07:33 2023

Merged: [wasm][streaming] Avoid UAF after context disposal

After a call to {StreamingDecoder::NotifyCompilationEnded}, no method on
the {StreamingProcessor} should be called any more. We were still
calling the {OnAbort} method later.

To make the semantics a bit more clear, we rename
{NotifyCompilationEnded} to {NotifyCompilationDiscarded}.

We also remove the {stream_finished_} field and reset the processor
instead, which will result in a nullptr access if we try to illegally
call any further methods.

R=ahaas@chromium.org

(cherry picked from commit 68047ec37fa5716528656a51927dda885691ff4a)
Bug: chromium:1403531

Change-Id: I8709c4c604f9b17948ba57a98e822ccc897951cc
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4145821
Reviewed-by: Andreas Haas <ahaas@chromium.org>
Commit-Queue: Clemens Backes <clemensb@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.0@{#10}
Cr-Branched-From: 06097c6f0c5af54fd5d6965d37027efb72decd4f-refs/heads/11.0.226@{#1}
Cr-Branched-From: 6bf3344f5d9940de1ab253f1817dcb99c641c9d3-refs/heads/main@{#84857}

[modify] https://crrev.com/3157f2dba49a06a7519e8d28144e019406185af3/src/wasm/streaming-decoder.cc
[modify] https://crrev.com/3157f2dba49a06a7519e8d28144e019406185af3/src/wasm/sync-streaming-decoder.cc
[modify] https://crrev.com/3157f2dba49a06a7519e8d28144e019406185af3/test/cctest/test-api.cc
[modify] https://crrev.com/3157f2dba49a06a7519e8d28144e019406185af3/src/wasm/module-compiler.cc
[modify] https://crrev.com/3157f2dba49a06a7519e8d28144e019406185af3/src/wasm/streaming-decoder.h
[modify] https://crrev.com/3157f2dba49a06a7519e8d28144e019406185af3/test/cctest/cctest.status
[modify] https://crrev.com/3157f2dba49a06a7519e8d28144e019406185af3/src/wasm/wasm-js.h
[modify] https://crrev.com/3157f2dba49a06a7519e8d28144e019406185af3/src/wasm/wasm-js.cc


### [Deleted User] (2023-01-09)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-09)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6bade738eaae97dbb30df405c98e25c0cef1cbed

commit 6bade738eaae97dbb30df405c98e25c0cef1cbed
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Jan 09 19:13:29 2023

Roll v8 11.0 from 06097c6f0c5a to 172c32fa27f5 (17 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/06097c6f0c5a..172c32fa27f5

2023-01-09 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.9
2023-01-09 alexschulze@chromium.org [builtins] Warn only for invalid PGO profiles
2023-01-09 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.8
2023-01-09 leszeks@chromium.org [builtins] Update builtins PGO profiles for M110 (re-try)
2023-01-09 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.7
2023-01-09 panq@google.com [turbofan] Fix a bug of SignedBigInt64 in representation changer
2023-01-09 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.6
2023-01-09 clemensb@chromium.org Merged: [wasm][streaming] Avoid UAF after context disposal
2023-01-05 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.5
2023-01-05 sky@chromium.org moves use_libm_trig_functions flag to right spot
2023-01-03 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.4
2023-01-03 panq@google.com [turbofan] Fix bugs of BigInt constructor inlining
2022-12-21 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.3
2022-12-21 marja@chromium.org Merged: [rab/gsab] Fix ValueSerializer error handling
2022-12-15 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.2
2022-12-15 alexschulze@chromium.org [builtins] Update builtins PGO profiles for M110
2022-12-15 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.0.226.1

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-chromium-release-0
Please CC v8-waterfall-sheriff@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.0: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m110: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1400897,chromium:1402139,chromium:1403531,chromium:1403574,chromium:1404607
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I1161b3c3b29b0283f4928d0f95ef7af86dd08922
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4147748
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5481@{#182}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/6bade738eaae97dbb30df405c98e25c0cef1cbed/DEPS


### rz...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### rz...@google.com (2023-01-10)

Issue introduced in 110 (See https://crbug.com/chromium/1403531#c2).

### am...@google.com (2023-01-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-12)

Congratulations on another one, Cassidy Kim! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### am...@google.com (2023-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1403531?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062372)*

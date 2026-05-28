# Security: UAF in simple_devtools_protocol_client::SimpleDevToolsProtocolClient::DispatchProtocolMessageTask(

| Field | Value |
|-------|-------|
| **Issue ID** | [40063167](https://issues.chromium.org/issues/40063167) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Headless |
| **Platforms** | Android, Linux, Mac, Windows |
| **Reporter** | wh...@gmail.com |
| **Assignee** | kv...@chromium.org |
| **Created** | 2023-02-20 |
| **Bounty** | $4,000.00 |

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

It bug need "--headless" argument  

it was introducted from commit <https://chromium-review.googlesource.com/c/chromium/src/+/4026625>

I will do a vulnerability analysis as soon as possible.

**VERSION**  

Chrome Version: 112.0.5607.0 (Developer Build) (64-bit)

**REPRODUCTION CASE**

this bug found by my fuzzer, I can't repro it, only have asan log.

I using asan-linux-release-1107293, you can download from <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1107293.zip?generation=1668045906082534&alt=media>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- [fuzz-00084.html.2023-02-20-13-16-28.asan.log](attachments/fuzz-00084.html.2023-02-20-13-16-28.asan.log) (text/plain, 22.9 KB)
- deleted (application/octet-stream, 0 B)
- [patch.diff](attachments/patch.diff) (text/plain, 2.0 KB)

## Timeline

### [Deleted User] (2023-02-20)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-02-21)

details

[1] pass a unretained ptr to `HeadlessCommandHandler::OnTargetCrashed`. When target Inspector crashed as "headless_command_handler.cc(357)] Abnormal renderer termination" , `SimpleDevToolsProtocolClient::DispatchProtocolMessageTask(` will dispatch this message[2],  `HeadlessCommandHandler::OnTargetCrashed` handle it and finially delete self[3], then once new crashed message come in, it will trigger uaf bug[4]

```
void HeadlessCommandHandler::ExecuteCommands() {
  // Expose DevTools protocol to the target.
  base::Value::Dict params;
  params.Set("targetId", devtools_client_.GetTargetId());
  browser_devtools_client_.SendCommand("Target.exposeDevToolsProtocol",
                                       std::move(params));

  // Set up Inspector domain.
  devtools_client_.AddEventHandler(
      "Inspector.targetCrashed",
      base::BindRepeating(&HeadlessCommandHandler::OnTargetCrashed,
                          base::Unretained(this)));                                                       <-----------------------[1]
  devtools_client_.SendCommand("Inspector.enable");
```

```
void SimpleDevToolsProtocolClient::DispatchProtocolMessageTask(
    base::Value::Dict message) {
  VLOG(kVLogLevel) << "\n[CDP RECV] " << message.DebugString();

...

 // Try to locate the event specific handler first and if there is none,
  // check the domain events handler specified as 'Domain.*'.
  auto it = event_handler_map_.find(*event_name);                               <-------------------------[4]
  if (it == event_handler_map_.cend())
    return;

  // Use a snapshot of the event's handler list verifying each callback
  // before calling it since it could be removed by the previous callback.
  std::vector<EventCallback> handlers(it->second);
  bool first_callback = true;
  for (auto& callback : handlers) {
    if (first_callback || HasEventHandler(*event_name, callback)) {
      first_callback = false;
      callback.Run(message);                                          <------------------ [2]
    }
  }
}
```



```
void HeadlessCommandHandler::Done() {
  DCHECK(web_contents_);
  devtools_client_.DetachClient();
  browser_devtools_client_.DetachClient();

  DoneCallback done_callback(std::move(done_callback_));
  delete this;                                                                  <------------------[3]
  std::move(done_callback).Run();
}
```

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/headless/command_handler/headless_command_handler.cc;l=320?q=ess_command_handler.cc&ss=chromium%2Fchromium%2Fsrc
[2] https://source.chromium.org/chromium/chromium/src/+/main:components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.cc;l=167;drc=bdb02a472d649656cab763300f5364cc9eb6bfe6?q=simple_devtools_protocol_client.&ss=chromium%2Fchromium%2Fsrc
[3] https://source.chromium.org/chromium/chromium/src/+/main:components/headless/command_handler/headless_command_handler.cc;l=388;drc=bdb02a472d649656cab763300f5364cc9eb6bfe6?q=ess_command_handler.cc&ss=chromium%2Fchromium%2Fsrc

### wh...@gmail.com (2023-02-21)

please check

### wh...@gmail.com (2023-02-21)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-02-21)

The bug introduced commit is 3acd45eb60c0635754573b34c75977f0de943138

this commit impacted oldest release channel [1] :
dev: 110.0.5449.3  beta: 110.0.5481.30  stable: 110.0.5481.77

active release branches: all

[1] https://chromiumdash.appspot.com/commits?commit=3acd45eb60c0635754573b34c75977f0de943138&platform=Windows

### sr...@google.com (2023-02-21)

Thanks for the report!
kvitekp@, can you take a look? There's no reproducer for this bug, but the reporter has an ASAN trace and the analysis sounds reasonable.

[Monorail components: Internals>Headless]

### [Deleted User] (2023-02-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-21)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2023-02-22)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-02-22)

the bug is similar to https://crbug.com/chromium/1382993

### wh...@gmail.com (2023-02-24)

ping? any updates?

### gi...@appspot.gserviceaccount.com (2023-02-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3edf9ce1a7dd2e20d517ccb8c36ef2ac5c0bead4

commit 3edf9ce1a7dd2e20d517ccb8c36ef2ac5c0bead4
Author: Peter Kvitek <kvitekp@chromium.org>
Date: Sat Feb 25 00:33:56 2023

[devtools] Fixed potential UAF in simple CDP protocol

SimpleDevToolsProtocolClient posts task to itself, however since it does
not control its own lifecycle, it could be destroyed before the task is
dispatched.

Bug: 1417649
Change-Id: I92079214da01f4961bc66dba1bc436078adf1ce1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4291481
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Auto-Submit: Peter Kvitek <kvitekp@chromium.org>
Commit-Queue: Peter Kvitek <kvitekp@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1109904}

[modify] https://crrev.com/3edf9ce1a7dd2e20d517ccb8c36ef2ac5c0bead4/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.h
[modify] https://crrev.com/3edf9ce1a7dd2e20d517ccb8c36ef2ac5c0bead4/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client_unittest.cc
[modify] https://crrev.com/3edf9ce1a7dd2e20d517ccb8c36ef2ac5c0bead4/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.cc


### kv...@chromium.org (2023-02-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-26)

Requesting merge to stable M110 because latest trunk commit (1109904) appears to be after stable branch point (1084008).

Requesting merge to beta M111 because latest trunk commit (1109904) appears to be after beta branch point (1097615).

Requesting merge to dev M112 because latest trunk commit (1109904) appears to be after dev branch point (1109224).

Merge approved: your change passed merge requirements and is auto-approved for M112. Please go ahead and merge the CL to branch 5615 (refs/branch-heads/5615) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

Merge review required: M110 is already shipping to stable.

Merge review required: M111 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wh...@gmail.com (2023-02-27)

Hi, please add 
credit: Ganjiang Zhou(@refrain_areu) of ChaMd5-H1 team

### [Deleted User] (2023-02-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-27)

merge to 112 auto-approved, please merge this fix to branch 5615 

M111 and M110 approved, please merge this fix to branch 5563 asap, by 9am Pacific tomorrow, so this fix can be included in the M111 Stable cut. 
Please also merge this fix to branch 5481 so this fix can be included in M110/Extended

### gi...@appspot.gserviceaccount.com (2023-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d0e87369766692ae6a1c71af1a529ff99efb4915

commit d0e87369766692ae6a1c71af1a529ff99efb4915
Author: Peter Kvitek <kvitekp@chromium.org>
Date: Mon Feb 27 22:42:39 2023

[m110][devtools] Fixed potential UAF in simple CDP protocol

SimpleDevToolsProtocolClient posts task to itself, however since it does
not control its own lifecycle, it could be destroyed before the task is
dispatched.

(cherry picked from commit 3edf9ce1a7dd2e20d517ccb8c36ef2ac5c0bead4)

Bug: 1417649
Change-Id: I92079214da01f4961bc66dba1bc436078adf1ce1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4291481
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Auto-Submit: Peter Kvitek <kvitekp@chromium.org>
Commit-Queue: Peter Kvitek <kvitekp@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1109904}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4295724
Cr-Commit-Position: refs/branch-heads/5481@{#1300}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/d0e87369766692ae6a1c71af1a529ff99efb4915/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.h
[modify] https://crrev.com/d0e87369766692ae6a1c71af1a529ff99efb4915/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client_unittest.cc
[modify] https://crrev.com/d0e87369766692ae6a1c71af1a529ff99efb4915/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.cc


### gi...@appspot.gserviceaccount.com (2023-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4c27f2d50bea7cbae6bbf710a74b2fcc97a3d392

commit 4c27f2d50bea7cbae6bbf710a74b2fcc97a3d392
Author: Peter Kvitek <kvitekp@chromium.org>
Date: Mon Feb 27 22:51:58 2023

[m111][devtools] Fixed potential UAF in simple CDP protocol

SimpleDevToolsProtocolClient posts task to itself, however since it does
not control its own lifecycle, it could be destroyed before the task is
dispatched.

(cherry picked from commit 3edf9ce1a7dd2e20d517ccb8c36ef2ac5c0bead4)

Bug: 1417649
Change-Id: I92079214da01f4961bc66dba1bc436078adf1ce1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4291481
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Auto-Submit: Peter Kvitek <kvitekp@chromium.org>
Commit-Queue: Peter Kvitek <kvitekp@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1109904}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4296179
Cr-Commit-Position: refs/branch-heads/5563@{#875}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[modify] https://crrev.com/4c27f2d50bea7cbae6bbf710a74b2fcc97a3d392/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.h
[modify] https://crrev.com/4c27f2d50bea7cbae6bbf710a74b2fcc97a3d392/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client_unittest.cc
[modify] https://crrev.com/4c27f2d50bea7cbae6bbf710a74b2fcc97a3d392/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.cc


### gi...@appspot.gserviceaccount.com (2023-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1efa085c71fe70e76903cd031eb8523c8eb2840f

commit 1efa085c71fe70e76903cd031eb8523c8eb2840f
Author: Peter Kvitek <kvitekp@chromium.org>
Date: Mon Feb 27 23:01:04 2023

[m112][devtools] Fixed potential UAF in simple CDP protocol

SimpleDevToolsProtocolClient posts task to itself, however since it does
not control its own lifecycle, it could be destroyed before the task is
dispatched.

(cherry picked from commit 3edf9ce1a7dd2e20d517ccb8c36ef2ac5c0bead4)

Bug: 1417649
Change-Id: I92079214da01f4961bc66dba1bc436078adf1ce1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4291481
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Auto-Submit: Peter Kvitek <kvitekp@chromium.org>
Commit-Queue: Peter Kvitek <kvitekp@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1109904}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4295722
Cr-Commit-Position: refs/branch-heads/5615@{#39}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/1efa085c71fe70e76903cd031eb8523c8eb2840f/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.h
[modify] https://crrev.com/1efa085c71fe70e76903cd031eb8523c8eb2840f/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client_unittest.cc
[modify] https://crrev.com/1efa085c71fe70e76903cd031eb8523c8eb2840f/components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.cc


### am...@google.com (2023-03-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-02)

Congratulations, Ganjiang Zhou! The VRP Panel has decided to award you $2,000 for this report of a heavily mitigated security bug (that reachable only through devtools and reliant on crashing the devtools handler)  +1,000 bisect bonus and $1,000 patch bonus. Thank you for your efforts in discovering and reporting this issue to us! 

### wh...@gmail.com (2023-03-03)

Could I ask a question about bisect bonus?
From [1] 
"$1,000: For identifying the specific commit that introduced the bug
 $2,000: For identifying the specific commit that introduced the bug and verifying which active release branches (dev/beta/stable) are impacted at the time of reporting " 

In order to get $2k, it seems I did at https://crbug.com/chromium/1417649#c5,  commit that introduced the bug should be right. Is it "active release branches: all" wrong? or where is my wrong, how need I fix?



[1] https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules#scope-of-program



### wh...@gmail.com (2023-03-03)

Re https://crbug.com/chromium/1417649#c23: BTW "that reachable only through devtools", it could reache throuht --headless. When I am fuzzing dom, I add "--headless" to test my fuzzer, I run too much chrome instances with different "--user-data-dir", then it quickly crash, no user interaction required. So I found this bug.

### wh...@gmail.com (2023-03-03)

And this,
The bug that I think it should be that the system memory is exhausted and the related process crashes, to trigger bug. The bug is very similar to https://crbug.com/chromium/1382993, but different process crashes.

### am...@chromium.org (2023-03-03)

Hi Ganjiang, thanks for reaching out. 
So in ref to https://crbug.com/chromium/1417649#c24, the information wrt to active release channels you provided was "dev: 110.0.5449.3  beta: 110.0.5481.30  stable: 110.0.5481.77", so it was not clear by that information that current dev and beta are still impacted as current beta (and at that time) were version M111/beta and M112/dev. 
I know this seems nitpicky but $2,000 is a pretty high bonus for a bisection, so we are asking at it be complete and accurate, based on up to date information. This is important for understand if there is a regression or other change that resulted in this issue. 

>>> Re https://crbug.com/chromium/1417649#c23: BTW "that reachable only through devtools", it could reache throuht --headless. When I am fuzzing dom, I add "--headless" to test my fuzzer, I run too much chrome instances with different "--user-data-dir", then it quickly crash, no user interaction required. So I found this bug.
 
Fuzzers can detect issues that require user interaction. Based on this information presented this appears that it would only be reachable via devtools and also require crashing the devtools handler, which we are no sure how possible or attainable that is in a real world scenario. 
Without a reproducer we cannot confirm what you are asserting. 

re:https://crbug.com/chromium/1417649#c26:
While the issue you linked (https://crbug.com/chromium/1382993) does seem similar, as you mention the crash is in a different process, a process we don't believe is fully remote exploitable in the way presented and likely mitigated - thus the reward for a mitigated security issue. 

Another thing to mention here, is that the report you like was a high quality report - providing full testharness, POC, and a repro video. The issue was fully reproducible by based on the information provided, with the demonstration video to help support if we would have had difficulties reproducing it. 
Our reward structure is not simply based on class and impact of the bug being reported, but also based on the information provided being demonstrable evidence of exploitation and impact as well as actionable information. Please see our information about Report Quality in our policies and guidelines: https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules#report-quality




### am...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-03-03)

Thank you for your reply.

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1417649?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063167)*

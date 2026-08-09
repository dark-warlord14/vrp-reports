# D3D10Warp!JITCopyContext::ExecuteResourceCopy memory heap overflow based on Integer overflow in gpu

| Field | Value |
|-------|-------|
| **Issue ID** | [480548427](https://issues.chromium.org/issues/480548427) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU |
| **Platforms** | Windows |
| **Chrome Version** | 144.0.7559.0 |
| **CVE IDs** | CVE-2026-26178 |
| **Reporter** | do...@gmail.com |
| **Assignee** | ra...@microsoft.com |
| **Created** | 2026-02-02 |
| **Bounty** | $17,000.00 |

## Description

# Steps to reproduce the problem

1. download chromium latest version(144.0.7559.0) (<https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/1552469/>)
2. run chrome.exe in Windows 10 pro(19045.6809) with latest update in VMWare Fusion Virtual host :
   ./chrome
3. start up http server at poc directory:
   python3 -m http.server 4444
4. access main.html, main.html stopped because of alert;
   <http://ip:4444/main.html>
5. open chromium browser process manager to view the gpu process id;
6. open windbg debugger, attach the gpu process; "g" in windbg to continue process;
7. click ok in alert prompt
8. crash in windbg

# Problem Description

Hello,
This issue was reproduced in latest chromium and Electron app.It was heap-based integer overflow and make gpu process crash . Chromium call gl.texSubImage3D will call libglesv2!GL\_TexSubImage3DRobustANGLE -> D3D10Warp!JITCopyContext::ExecuteResourceCopy+0x6f , copy src heap buffer (allocated by js gl.texStorage3D) to the dst heap buffer (gl.texSubImage3D) based on width(0xc2) and heigth(0x541) and depth(0x404), but didn't compare size of dst buffer and size of src buffer . The size of src is 0xffcf6000, and the size of dst is 0x1000.

(1)Integer overflow

```
Integer overflow occur in function (D3D10Warp!ResourceShape::PreDistributeOriginal) which used for calculating size of heap buffer.

   There is a jump instruction (jz) based on r15b at loc_1800C10CE; When calculating size of source buffer ,r15b is 0 and the jz is taken. However when calculating size of destination buffer,r15b is 1 and the jz is not taken; rbx is height and add 1 (loc_1800C10D6). Maybe the addition is necessary from the 3D implementation, but this operation lead to integer overflow. So the size of source buffer is (width * height* depth) and the size of destination buffer is (width * (height+1)* depth). Why r15 register is different between two calculating? Getting arguments for some flag is 0x8 and 0x28 for two times of calculating (loc_1800C0D53)
  Another reason trigger integer overflow is register mismatch. Above calculating size of buffer used 64-bit register (rdi), however saving size of buffer used 32-bit register(edi). When above calculating size of buffer beyond maxium size of 32 bit regiter, this will result in integer overflow

```

（2）Heap overflow
at loc\_1800FB8BF call function
(D3D10Warp!JITCopyContext::ExecuteResourceCopy) to execte resource copy.
step in function (D3D10Warp!JITCopyContext::ExecuteResourceCopy) ,
This function may generate a JIT copy code in runtime , because address from backtrace of crash is not belong to any loaded module.
JIT code copy based on width and height and depth, which didn’t check size of source buffer and destination buffer

# Additional Comments

The Attachments:
(1) IDA packed for C:\Windows\System32\d3d10warp.dll for binary analysis
(2)poc files : main.html and kgpu.js
(3)reproduced video

# Summary

D3D10Warp!JITCopyContext::ExecuteResourceCopy memory heap overflow based on Integer overflow in gpu

# Custom Questions

#### Type of crash:

gpu process

#### Crash state:

Callstack
0:000> g

(2ca4.17e0): Access violation - code c0000005 (first chance)

First chance exceptions are reported before any exception handling.

This exception may be expected and handled.

00007df4b14e1123 0f1101 movups xmmword ptr [rcx],xmm0 ds:000002bb253ca000=????????????????????????????????

0:015> kb

# RetAddr : Args to Child : Call Site

00 00007ffd53ccb8c5 : 000002bb3097ff30 000002bb1a040000 000002bb2d2d4f40 0000000000000000 : 0x00007df4b14e1123

01 00007ffd53cb1e82 : 000002bb2d2d4f20 000002bb2213bfd0 000002bb3097ff30 000002bb00000000 : D3D10Warp!JITCopyContext::ExecuteResourceCopy+0x75
02 00007ffd53f1b050 : 000002bb2d2d4f20 8000000000000000 8000000000000000 000002bb2213bfd0 : D3D10Warp!Task\_Copy+0x132

03 00007ffd53f1d198 : 000002bb22141e20 000002bb2212fa80 000002bb2213bfd0 000002bb2cd1bf30 : D3D10Warp!Task::ExecuteTask+0x250
04 00007ffd5e213720 : 000000d3a23ffbc8 0000000000001f80 000002bb2214bf10 000002bb22141e20 : D3D10Warp!ThreadPool::WorkCallBack+0x128

05 00007ffd5e1fd79a : 0000000000000000 0000000000000000 000002bb22141e20 000002bb2777cff0 : ntdll!TppWorkpExecuteCallback+0x130
06 00007ffd5d7c7374 : 0000000000000000 0000000000000000 0000000000000000 0000000000000000 : ntdll!TppWorkerThread+0x68a

07 00007ffd5e1fcc91 : 0000000000000000 0000000000000000 0000000000000000 0000000000000000 : KERNEL32!BaseThreadInitThunk+0x14
08 0000000000000000 : 0000000000000000 0000000000000000 0000000000000000 0000000000000000 : ntdll!RtlUserThreadStart+0x21

#### Reporter credit:

Dongzhuo Zhao working with ADLab of Venustech

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [d3d10warp.dll.i64](attachments/d3d10warp.dll.i64) (application/octet-stream, 98.3 MB)
- [Repo 2026-02-02.mov](attachments/Repo 2026-02-02.mov) (video/quicktime, 45.9 MB)
- [main.html](attachments/main.html) (text/html, 4.1 KB)
- [kgpu.js](attachments/kgpu.js) (text/javascript, 2.6 KB)
- [ms_fix.png](attachments/ms_fix.png) (image/png, 343.7 KB)

## Timeline

### ja...@chromium.org (2026-02-03)

[security triage]

I'm not able to reproduce this but speculatively triaging it as S1 High as memory corruption in a sandboxed gpu process (on Windows).

I've added some team members who can better triage this.

### ja...@chromium.org (2026-02-03)

[security triage] preliminarily setting found in to extended stable (144).

### mp...@google.com (2026-02-03)

Geoff what are we doing about WARP bugs now that Swiftshader is deprecated? Based on [this doc](http://shortn/_BPknAijx80) we can have MS fix these?

### ch...@google.com (2026-02-03)

Setting milestone because of s0/s1 severity.

### do...@gmail.com (2026-02-06)

Hello,
     Have you reproduced this vulnerability? Please note that I trigger
this issue in windows 10 . I think if you follow the reproduction steps, It
will  be definitely reproduced .
     I reported this issue to MSRC at first, but they determined that this
issue orignated in the upstream Chromium code.

[image: image.png]

     I hope the information I provided is useful to you.


### ch...@google.com (2026-02-18)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ge...@chromium.org (2026-02-18)

Rafael, could you triage and forward this to the WARP folks?

### ra...@microsoft.com (2026-02-19)

There is an MSRC bug covering this. A fix is being created and will be serviced to earlier versions of Windows.

The root cause is integer overflow when texture sizes exceed 4GiB which causes small amounts of memory to be allocated, and subsequent bounds checks are based on the original resource sizes, leading to out-of-bounds reads or writes.

### ch...@google.com (2026-03-05)

rafael.cintron: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ra...@microsoft.com (2026-03-05)

@ge...@chromium.org, what do you suggest as the best resolution for the bug?

### ge...@chromium.org (2026-03-12)

If the fix will go out in a security update, we can accept that as the fix, IMO. I will mark the bug as ExternalDependency and close as fixed.

### ch...@google.com (2026-03-13)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [146, 147].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-03-15)

No action needed in Chrome, so we don't need merges.

### wf...@chromium.org (2026-03-18)

if this is an MS bug has MS issued a CVE for this?

### dr...@chromium.org (2026-03-18)

Let's leave this open until the bug is definitely fixed, otherwise we risk early disclosure.

### ch...@google.com (2026-03-20)

rafael.cintron: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-04-04)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### do...@gmail.com (2026-04-15)

Hello,
MS have been released fix for this issue and assigned CVE-2026-26178(
https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-26178)
[image: image.png]

<buganizer-system@google.com> 于2026年4月4日周六 15:56写道：

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/480548427
>
> *Changed*
> Chromium Labels:  Disable-Nags → Disable-Nags, Deadline-Exceeded
>
> *ch...@google.com <ch...@google.com> added comment #18
> <https://issues.chromium.org/issues/480548427#comment18>:*
>
> We commit ourselves to a 60 day deadline for fixing for s1 severity
> vulnerabilities, and have exceeded it here. If you're unable to look into
> this soon, could you please find another owner or remove yourself so that
> this gets back into the security triage queue?
>
> _______________________________
>
> *Reference Info: 480548427 D3D10Warp!JITCopyContext::ExecuteResourceCopy
> memory heap overflow based on Integer overflow in gpu*
> component:  Public Trackers > 1362134 > Chromium > Internals > GPU
> <https://issues.chromium.org/components/1456649>
> status:  Assigned
> reporter:  dongzhuozhaosec123@gmail.com
> assignee:  ra...@microsoft.com
> cc:  dongzhuozhaosec123@gmail.com, dr...@chromium.org, ge...@chromium.org,
> and 4 more
> collaborators:  se...@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P1
> severity:  S1
> found in:  144
> hotlist:  external_security_report
> <https://issues.chromium.org/hotlists/5433527>, reward-topanel
> <https://issues.chromium.org/hotlists/5432096>, Security_Impact-Extended
> <https://issues.chromium.org/hotlists/5432548>, Status_ExternalDependency
> <https://issues.chromium.org/hotlists/5438152>, Unconfirmed
> <https://issues.chromium.org/hotlists/5437934>
> retention:  Component default
> BuildNumber:  144.0.7559.0
> Chromium Labels:  Disable-Nags, Deadline-Exceeded
> Component Ancestor Tags:  Internals, Internals>GPU
> Component Tags:  Internals>GPU
> Fixed By Code Changes:  NA
> Merge:  Rejected-146, Rejected-147
> Milestone:  146
> OS:  Windows
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you have the following role(s) on the
> issue: cc, reporter, starred
> Unsubscribe from this issue
> <https://issues.chromium.org/issues/480548427?unsubscribe=true>.
>


### do...@gmail.com (2026-04-15)

MS have been released fix for this issue and assigned CVE-2026-26178(
https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-26178)

### do...@gmail.com (2026-04-22)

Since initial report with chrome(144.0.7559.0) (
https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/1552469/)
which is not canary version, now I send you the repo version with canary
version.
Repo Video in unpatched Windows 10 with chrome (149.0.7805.0 (Official
Build) canary (64-bit) (cohort: Clang-64) )
 chrome_canary_repo.mov
<https://drive.google.com/file/d/1Cw2cigUa1qIwsBzJG9j2FsBCPzYV_XJ1/view?usp=drive_web>

<buganizer-system@google.com> 于2026年4月17日周五 06:28写道：

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/480548427
>
> *Changed*
> hotlist (-):  Unconfirmed <https://issues.chromium.org/hotlists/5437934>
>
> _______________________________
>
> *Reference Info: 480548427 D3D10Warp!JITCopyContext::ExecuteResourceCopy
> memory heap overflow based on Integer overflow in gpu*
> component:  Public Trackers > 1362134 > Chromium > Internals > GPU
> <https://issues.chromium.org/components/1456649>
> status:  Assigned
> reporter:  dongzhuozhaosec123@gmail.com
> assignee:  ra...@microsoft.com
> cc:  ch...@google.com, dongzhuozhaosec123@gmail.com, dr...@chromium.org,
> and 5 more
> collaborators:  se...@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P1
> severity:  S1
> found in:  144
> hotlist:  external_security_report
> <https://issues.chromium.org/hotlists/5433527>, reward-topanel
> <https://issues.chromium.org/hotlists/5432096>, Security_Impact-Extended
> <https://issues.chromium.org/hotlists/5432548>, Status_ExternalDependency
> <https://issues.chromium.org/hotlists/5438152>
> retention:  Component default
> BuildNumber:  144.0.7559.0
> Chromium Labels:  Disable-Nags, Deadline-Exceeded
> Component Ancestor Tags:  Internals, Internals>GPU
> Component Tags:  Internals>GPU
> Fixed By Code Changes:  NA
> Merge:  Rejected-146, Rejected-147
> Milestone:  146
> OS:  Windows
>
>
> Generated by Google IssueTracker notification system.
>


### do...@gmail.com (2026-04-25)

deleted

### do...@gmail.com (2026-05-11)

deleted

### sp...@google.com (2026-05-19)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $17000.00 for this report.

Rationale for this decision:
Baseline with renderer bonus. Memory Corruption / RCE in a highly privileged process (e.g. GPU or network)


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### do...@gmail.com (2026-05-22)

🍻🍻🍻

On Wed, 20 May 2026 at 06:56, <buganizer-system@google.com> wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/480548427
>
> *Changed*
> vrp-reward:  <none> → 17000
>
> _______________________________
>
> *Reference Info: 480548427 D3D10Warp!JITCopyContext::ExecuteResourceCopy
> memory heap overflow based on Integer overflow in gpu*
> component:  Public Trackers > 1362134 > Chromium > Internals > GPU
> <https://issues.chromium.org/components/1456649>
> status:  Fixed
> reporter:  dongzhuozhaosec123@gmail.com
> assignee:  ra...@microsoft.com
> cc:  ch...@google.com, dongzhuozhaosec123@gmail.com, dr...@chromium.org,
> and 5 more
> collaborators:  se...@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P1
> severity:  S1
> found in:  144
> hotlist:  external_security_report
> <https://issues.chromium.org/hotlists/5433527>, reward-inprocess
> <https://issues.chromium.org/hotlists/5432630>, Security_Impact-Extended
> <https://issues.chromium.org/hotlists/5432548>, Status_ExternalDependency
> <https://issues.chromium.org/hotlists/5438152>
> retention:  Component default
> BuildNumber:  144.0.7559.0
> Chromium Labels:  Disable-Nags, Deadline-Exceeded
> Component Ancestor Tags:  Internals, Internals>GPU
> Component Tags:  Internals>GPU
> Fixed By Code Changes:  NA
> Merge:  Rejected-146, Rejected-147
> Milestone:  146
> OS:  Windows
> vrp-reward:  17000
>
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you have the following role(s) on the
> issue: cc, reporter, starred, subscribed
> Unsubscribe from this issue
> <https://issues.chromium.org/issues/480548427?unsubscribe=true>.
>


### ch...@google.com (2026-08-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/480548427)*

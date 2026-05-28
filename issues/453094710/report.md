# Out-of-bound read in the jmp table of ActiveMediaSessionController leads to sandbox escape.

| Field | Value |
|-------|-------|
| **Issue ID** | [453094710](https://issues.chromium.org/issues/453094710) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>Session |
| **Platforms** | Linux, Windows, ChromeOS |
| **Chrome Version** | 143.0.7475.11 |
| **Reporter** | bl...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2025-10-18 |
| **Bounty** | $250,000.00 |

## Description

# Steps to reproduce the problem

## Trigger the bug

1. git checkout -b dev\_7475 7a358025a3471995d126b3b5e286065ac3c56953
2. git apply `7475_patch_renderer_poc.diff`
3. gn gen out/Release --args="is\_debug=false symbol\_level=2 dcheck\_always\_on=false is\_component\_build=false"
4. autoninja -C out/Release chrome
5. Place `play.html` and `sample1.mp3` in the same directory, then start a HTTP server.
6. Trigger crash:
   - Access `play.html`
   - Click `start` button → Browser process crashes

## Exploitation

### Environment

- OS: 22.04.2

```
cat /proc/version
Linux version 6.8.0-85-generic (buildd@lcy02-amd64-024) (x86_64-linux-gnu-gcc-12 (Ubuntu 12.3.0-1ubuntu1~22.04.2) 12.3.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #85~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Fri Sep 19 16:18:59 UTC 2

```

- CPU: 13th Gen Intel(R) Core(TM) i9-13900K
- RAM: 128G

### Steps

1. sudo apt update && sudo apt upgrade
2. git checkout -b dev\_7475 7a358025a3471995d126b3b5e286065ac3c56953
3. git apply `7475_patch_renderer_exp.diff`
4. gn gen out/Release --args="is\_debug=false symbol\_level=2 dcheck\_always\_on=false is\_component\_build=false"
5. autoninja -C out/Release chrome
6. Place `play.html` and `sample1.mp3` in the same directory, then start a HTTP server.
7. Visit `play.html`, click `start` button and waiting.
8. With a runtime of ~10 minutes and ~80% success probability, this exploit executes `uname -a` in bash upon successful exploitation.

# Problem Description

[`MediaSessionAction action`](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/media/active_media_session_controller.cc;drc=3bf1d9f217305bc024a79c10c0030bef1fb86d7d;l=250) is transmitted from the renderer through Mojo, the transmission chain is:

```
MediaSessionServiceImpl => media_session_impl => media_controller => active_media_session_controller


```

1. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/media/session/media_session_service_impl.cc;drc=1f0de3303671c6c041930c7f4f8a9ad017a7f211;l=128>
2. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/media/session/media_session_impl.cc;drc=1cc7997baa714735aa78b08b94b64b02c22760ae;l=1600>
3. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/media/session/media_session_impl.cc;drc=3bf1d9f217305bc024a79c10c0030bef1fb86d7d;l=1882>
4. <https://source.chromium.org/chromium/chromium/src/+/main:services/media_session/media_controller.cc;drc=3bf1d9f217305bc024a79c10c0030bef1fb86d7d;l=287>
5. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/media/active_media_session_controller.cc;drc=3bf1d9f217305bc024a79c10c0030bef1fb86d7d;l=89>

In the compiled code of `ActiveMediaSessionController::MediaSessionActionToKeyCode`, a jmp table is used for the switch case statement. `action` is used for the offset to visit the jmp table, but without any value-checking:

```
0x000055555cc2e75b <+315>:   mov    (%r12),%eax   # rax is action, uesed for offset
0x000055555cc2e75f <+319>:   lea    -0x562bfb2(%rip),%rdx # jmp table 0x5555576027b4
=> 0x000055555cc2e766 <+326>:   movslq (%rdx,%rax,4),%rcx 
0x000055555cc2e76a <+330>:   add    %rdx,%rcx
0x000055555cc2e76d <+333>:   mov    $0xb3,%dx
0x000055555cc2e771 <+337>:   jmp    *%rcx

```

That mean if renderer can control any 4-bytes static value of chrome image memory, it can redirect execution to arbitrary addresses in chrome image memory.

There are 3 primary steps of the exploitation.

1. Achieve **arbitrary chrome image address execution**.
   [`next_request_id`](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/presentation/presentation_service_impl.cc;drc=d15fd76ecbf7fb17bbe4e2833c7537c120d4e045;l=43) increases by 1 if renderer calls `PresentationServiceImpl::StartPresentation` once.
   So if renderer let `rax * 4 + jmp_table_base` point to `&next_request_id`, and increase the value of `next_request_id` , it can redirect the execution of browser process.
2. Leak the chrome base address to bypass ASLR.
   The context when `jmp *%rcx`:
   
   ```
   (gdb) i r
   rcx            0x55555cb9aea1      93825116253857  // dst ip
   r12            0x215c01294d24      36679040191780 // actions.__begin_
   content::MediaKeysListenerManager *
   r15            0x215c01294d3c      36679040191804 // actions.__end_
   
   ```
   
   Firstly, perform a heap spray to let [BlobDataItem::bytes\_](https://source.chromium.org/chromium/chromium/src/+/main:storage/browser/blob/blob_data_item.cc;drc=3bf1d9f217305bc024a79c10c0030bef1fb86d7d;l=183) under `actions.__end_`, and redirect the execution to the code such as `mov %rcx,0x18(%r15); pop ... ret`. Then read the data of blob can get the chrome base.
3. Use some rops to bypass intel CET and control RDI/RSI/RDX and call execlp.

# Summary

Out-of-bound read in the jmp table of ActiveMediaSessionController leads to sandbox escape.

# Custom Questions

#### Type of crash:

browser

#### Crash state:

```
Thread 1 "chrome" received signal SIGSEGV, Segmentation fault.
content::ActiveMediaSessionController::MediaSessionActionsChanged (this=0x12bc00564840, actions=...) at ../../content/browser/media/active_media_session_controller.cc:89
89              MediaSessionActionToKeyCode(action);
(gdb) i r
rax            0x41414141          1094795585
rbx            0x12bc00564840      20598668806208
rcx            0x12bc00e613f8      20598678230008
rdx            0x5555576027b4      93825026500532
rsi            0x12bc00e613f8      20598678230008
rdi            0x12bc00e613fc      20598678230012
rbp            0x7fffffffc8c0      0x7fffffffc8c0
rsp            0x7fffffffc880      0x7fffffffc880
r8             0x1                 1
r9             0x0                 0
r10            0x7ffd0             524240
r11            0x0                 0
r12            0x12bc0358eecc      20598719311564
r13            0x12bc00564848      20598668806216
r14            0x12bc004937d0      20598667950032
r15            0x12bc0358eed0      20598719311568
rip            0x55555cc2e766      0x55555cc2e766 <content::ActiveMediaSessionController::MediaSessionActionsChanged(std::__Cr::vector<media_session::mojom::MediaSessionAction, std::__Cr::allocator<media_session::mojom::MediaSessionAction> > const&)+326>
(gdb) bt
#0  content::ActiveMediaSessionController::MediaSessionActionsChanged(std::__Cr::vector<media_session::mojom::MediaSessionAction, std::__Cr::allocator<media_session::mojom::MediaSessionAction> > const&)
    (this=0x12bc00564840, actions=<optimized out>) at ../../content/browser/media/active_media_session_controller.cc:89
#1  0x0000555559fc71c1 in media_session::mojom::MediaControllerObserverStubDispatch::Accept(media_session::mojom::MediaControllerObserver*, mojo::Message*) (impl=0x12bc00564840, message=0x7fffffffcc40)
    at gen/services/media_session/public/mojom/media_controller.mojom.cc:3006
#2  0x000055555f512f33 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) (this=0x12bc0006b600, message=0x7fffffffcc40)
    at ../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1060
#3  0x000055555f519dc0 in mojo::MessageDispatcher::Accept(mojo::Message*) (this=0x12bc0006b6e8, message=0x7fffffffcc40) at ../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43
#4  0x000055555f51476f in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) (this=<optimized out>, message=0x7fffffffcc40)
    at ../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:731
#5  0x000055555f51dbb1 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*)
    (this=this@entry=0x12bc00bb9a40, message_wrapper=message_wrapper@entry=0x7fffffffce00, client_call_behavior=client_call_behavior@entry=mojo::internal::MultiplexRouter::ALLOW_DIRECT_CLIENT_CALLS, current_task_runner=<optimized out>) at ../../mojo/public/cpp/bindings/lib/multiplex_router.cc:1164
#6  0x000055555f51d4e6 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) (this=0x12bc00bb9a40, message=<optimized out>) at ../../mojo/public/cpp/bindings/lib/multiplex_router.cc:767
#7  0x000055555f519dc0 in mojo::MessageDispatcher::Accept(mojo::Message*) (this=0x12bc00bb9a70, message=0x7fffffffcf60) at ../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43
#8  0x000055555f510c06 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) (this=this@entry=0x12bc00bb9aa0, handle=...) at ../../mojo/public/cpp/bindings/lib/connector.cc:561
#9  0x000055555f511355 in mojo::Connector::ReadAllAvailableMessages() (this=0x12bc00bb9aa0) at ../../mojo/public/cpp/bindings/lib/connector.cc:619
#10 0x000055555f5111a5 in mojo::Connector::OnHandleReadyInternal(unsigned int) (result=0, this=<optimized out>) at ../../mojo/public/cpp/bindings/lib/connector.cc:450
#11 mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) (this=0x12bc00bb9aa0, interface_name=0x5555570473b3 "media_session.mojom.MediaControllerObserver", result=0)
    at ../../mojo/public/cpp/bindings/lib/connector.cc:416

```
#### Reporter credit:

Hou(@bl1nnnk)

# Additional Data

Category: Security   

Chrome Channel: Dev   

Regression: N/A \

## Attachments

- [7475_patch_renderer_poc.diff](attachments/7475_patch_renderer_poc.diff) (text/x-diff, 706 B)
- [7475_patch_renderer_exp.diff](attachments/7475_patch_renderer_exp.diff) (text/x-diff, 33.7 KB)
- [play.html](attachments/play.html) (text/html, 2.6 KB)
- [sample1.mp3](attachments/sample1.mp3) (audio/mpeg, 1.9 MB)
- [exploit.mp4](attachments/exploit.mp4) (video/mp4, 285.6 MB)

## Timeline

### ja...@chromium.org (2025-10-20)

[security shepherd]

Thanks for the bug report, POC and writeup.

I'm working on reproducing the bug by applying the patch to M140 (Extended stable). In the mean time, I'll treat this as speculatively true and follow that triage procedure.

### ja...@chromium.org (2025-10-20)

Putting this in Blink > Media > Session as a starting component.

### ja...@chromium.org (2025-10-20)

[security shepherd]
Hi steimel, assigning this to you as a starting owner. Can you take a look and find a better owner if you aren't a good owner for this bug?

### ja...@chromium.org (2025-10-20)

[shepherd] I'm assigning this a severity of High (S1) based on "renderer sandbox escapes fall into this category as their impact is that of a critical severity bug, but they require the precondition of a compromised renderer."

<https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#toc-high-severity>

### ja...@chromium.org (2025-10-21)

[security shepherd] Setting found in to the current Dev milestone based on the initial report.

### ch...@google.com (2025-10-21)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-10-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2025-10-21)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2025-10-21)

Project: chromium/src  

Branch:  main  

Author:  Tommy Steimel [steimel@chromium.org](mailto:steimel@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7063465>

[Media Session] Verify media session action enum values from renderer

---


Expand for full commit details
```
     
    This CL ensures that media session action enum values coming from the 
    renderer are actually valid. This is necessary since the 
    MediaSessionAction enum is extensible, though we don't expect 
    non-standard values from Blink. 
     
    Bug: 453094710 
    Change-Id: I21539f346839b741f8496413335a5d9c2d133fc3 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7063465 
    Reviewed-by: Frank Liberato <liberato@chromium.org> 
    Commit-Queue: Tommy Steimel <steimel@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1533296}

```

---

Files:

- M `content/browser/media/session/media_session_service_impl.cc`

---

Hash: [097a55a74b8d89519026d90c6466b30c6433761a](https://chromiumdash.appspot.com/commit/097a55a74b8d89519026d90c6466b30c6433761a)  

Date: Tue Oct 21 23:21:06 2025


---

### st...@chromium.org (2025-10-21)

Thank you for the very detailed report!

### ch...@google.com (2025-10-29)

Security Merge Request Consideration: Not requesting merge to dev (M143) because latest trunk commit (1533296) appears to be prior to dev branch point (1536371). If this is incorrect please remove NA-143 from the 'Merge' field and add 143 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### wf...@chromium.org (2025-11-10)

[vrp panel here] hi reporter, if you would like this report to be considered "High-quality report with demonstration of RCE" can you provide a video or further steps to reproduce the bug as we were unable to reproduce this ourselves. With no evidence of this we will consider this as "High-quality report of demonstrated memory corruption"

### bl...@gmail.com (2025-11-11)

Hi team, I’ve uploaded a video demonstrating a working RCE for this issue. The exploit is not fully optimized, as I reported it immediately after confirming the vulnerability was exploitable.
Please let me know if any further details or artifacts are needed. Thank you.

### wf...@chromium.org (2025-11-11)

Thank you for your submission we will assess this at the next panel session.

### sp...@google.com (2025-11-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $250000.00 for this report.

Rationale for this decision:
High-quality report with demonstration of RCE in unsandboxed process. Congratulations, nice catch!


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### bl...@gmail.com (2025-11-14)

Thank you very much! I really appreciate the team’s efficiency and professionalism.

### bl...@gmail.com (2025-12-16)

Hi team, I'm glad to see that the issue has been fixed in the recent stable version. However, I was wondering why no CVE has been assigned for this issue. Could you please provide some insight?

### aw...@google.com (2025-12-19)

jdev@ mind looking into the CVE allocation please?

### bl...@gmail.com (2025-12-30)

Many products based on Chromium rely on CVEs to cherry-pick patches for vulnerability fixes. Without a CVE, they may remain vulnerable.

### bl...@gmail.com (2026-01-13)

May I share the patch and vulnerability with the community to help other products apply the fix?

### dr...@chromium.org (2026-01-13)

Please do not disclose details of the bug until it's made public. That should happen 14 weeks after the bug was fixed, which is about two weeks from now.

I can start to look into the CVE allocation in the meantime.

### dr...@chromium.org (2026-01-22)

Okay the lack of CVE is because we never confirmed this impacted Stable. I've just tested it in an M140 build and it does indeed apply. Updating FoundIn.

### ch...@google.com (2026-01-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### pu...@gmail.com (2026-02-05)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/453094710)*

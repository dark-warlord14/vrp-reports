# Security: Use After Free in PresentationConnectionCallbacks::OnSuccess

| Field | Value |
|-------|-------|
| **Issue ID** | [40053095](https://issues.chromium.org/issues/40053095) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>PresentationAPI |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2020-6550 |
| **Reporter** | lw...@gmail.com |
| **Assignee** | mf...@chromium.org |
| **Created** | 2020-08-15 |
| **Bounty** | $7,500.00 |

## Description

  Similar to CVE-2020-6550 (https://chromium-review.googlesource.com/c/chromium/src/+/2311620)，In function PresentationConnectionCallbacks::OnSuccess, Invoking Promise.resolve may trigger user callback. "connection_" can be freed in the callback and cause use-after-free.

  ```c++
  void PresentationConnectionCallbacks::OnSuccess(
      const mojom::blink::PresentationInfo& presentation_info,
      mojo::PendingRemote<mojom::blink::PresentationConnection> connection_remote,
      mojo::PendingReceiver<mojom::blink::PresentationConnection>
          connection_receiver) {
    // Reconnect to existing connection.
    if (connection_ && connection_->GetState() ==
                           mojom::blink::PresentationConnectionState::CLOSED) {
      connection_->DidChangeState(
          mojom::blink::PresentationConnectionState::CONNECTING);
    }
  
    // Create a new connection.
    if (!connection_ && request_) {
      connection_ = ControllerPresentationConnection::Take(
          resolver_.Get(), presentation_info, request_);
    }
  
    resolver_->Resolve(connection_); //***1***
    connection_->Init(std::move(connection_remote),
                      std::move(connection_receiver));
  }
  ```

  

  VERSION

  Operating System: I test it on Linux, but I think it affects other platforms too.
  Version:  Chromium dev  86.0.4229.0 (branch_base_position:796283)

  

  REPRODUCTION CASE

  1.Download chromium from (http://commondatastorage.googleapis.com/chromium-browser-ubsan/linux-release-vptr/ubsan-vptr-linux-release-796283.zip (prefer this version as it report symboled crash stack) or (http://commondatastorage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-796283.zip).

  2.it need an extra display connected to the machine to reproduce this bug.

  3.Include the attached files presentation-1.html, presentation-2.html in the same folder and serve it on local host. open  presentation-1.html in the chromium, and click the button in the page, it will then pop up dialog. Click the screen to present in the dialog and the crash happens. The crash state is attached as follows.

  

  FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
  Crash State:

  ```
  Received signal 11 SEGV_MAPERR 000000000000                                                                                                            
  #0 0x563df2c17779 base::debug::CollectStackTrace()                                                                                                     
  #1 0x563df2b18bf3 base::debug::StackTrace::StackTrace()                                                                                                
  #2 0x563df2c1713b base::debug::(anonymous namespace)::StackDumpSignalHandler()                                                                         
  #3 0x7fb56d1fddd0 (/usr/lib/libpthread-2.26.so+0x11dcf)                                                                                                
  #4 0x563dfbef9a83 blink::ControllerPresentationConnection::Init()                                                                                      
  #5 0x563dfbf1461e blink::PresentationConnectionCallbacks::OnSuccess()                                                                                  
  #6 0x563dfbf14265 blink::PresentationConnectionCallbacks::HandlePresentationResp                                                                       onse()
  #7 0x563dfbf13c9e base::internal::FunctorTraits<>::Invoke<>()
  #8 0x563df04fb6dc blink::mojom::blink::PresentationService_StartPresentation_ForwardToCallback::Accept()
  #9 0x563df2e07bd6 mojo::InterfaceEndpointClient::HandleValidatedMessage()
  #10 0x563df2e1953c mojo::internal::MultiplexRouter::ProcessIncomingMessage()
  #11 0x563df2e18346 mojo::internal::MultiplexRouter::Accept()
  #12 0x563df2e03789 mojo::Connector::DispatchMessage()
  #13 0x563df2e04f8c mojo::Connector::ReadAllAvailableMessages()
  #14 0x563df2e33842 mojo::SimpleWatcher::OnHandleReady()
  #15 0x563df2ba10d1 base::TaskAnnotator::RunTask()
  #16 0x563df2bc677c base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()
  #17 0x563df2bc5b8f base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
  #18 0x563df2b382eb base::MessagePumpDefault::Run()
  #19 0x563df2bc7e35 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
  #20 0x563df2b819c0 base::RunLoop::Run()
  #21 0x563dfd6f989c content::RendererMain()
  #22 0x563df21a126f content::RunZygote()
  #23 0x563df21a3684 content::ContentMainRunnerImpl::Run()
  #24 0x563df224f69a service_manager::Main()
  #25 0x563df21a0361 content::ContentMain()
  #26 0x563ded4dd47f ChromeMain
  #27 0x7fb565da3f4a __libc_start_main
  #28 0x563ded4c6c6a _start
    r8: 0000563dfa3a6a0d  r9: 000000000000000f r10: 0000563dfeac7710 r11: 0000563dfeac76e0
   r12: 8e38fa335280c207 r13: 000007d2456b05e8 r14: 9ddfea08eb382d69 r15: 000007d2456b04f8
    di: 000007d2456b0540  si: 34bafe4ed1ddb174  bp: 00007fffd0ed4490  bx: 0000563e01b2dd30
    dx: 34bafe4ed1ddb174  ax: 0000000000000000  cx: 0000000000000000  sp: 00007fffd0ed4410
    ip: 0000563dfbef9a83 efl: 0000000000010202 cgf: 002b000000000033 erf: 0000000000000004
   trp: 000000000000000e msk: 0000000000000000 cr2: 0000000000000000
  [end of stack trace]
  Calling _exit(1). Core file will not be generated.
  
  ```



## Attachments

- [presentation-1.html](attachments/presentation-1.html) (text/plain, 561 B)
- [presentation-2.html](attachments/presentation-2.html) (text/plain, 853 B)

## Timeline

### va...@chromium.org (2020-08-15)

Unable to reproduce with 768962, will try chromium-browser-ubsan/linux-release-vptr/ubsan-vptr-linux-release-796283.zip next

### va...@chromium.org (2020-08-15)

Can't reproduce withchromium-browser-ubsan/linux-release-vptr/ubsan-vptr-linux-release-796283.zip either probably because of

> it need an extra display connected to the machine to reproduce this bug.

[Monorail components: Blink>PresentationAPI]

### va...@chromium.org (2020-08-15)

Tentatively setting security label to Stable since I don't see any recent changes to the code in question here.

### [Deleted User] (2020-08-15)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-15)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ml...@google.com (2020-08-17)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/42a17e378ad7efbf57d47f3a7612d7c7cf95a907

commit 42a17e378ad7efbf57d47f3a7612d7c7cf95a907
Author: mark a. foltz <mfoltz@chromium.org>
Date: Tue Aug 18 22:02:07 2020

[Presentation API] Fix use-after-free.

This fixes a potential UAF in PresentationConnectionCallbacks::OnSuccess.

Bug: 1116706
Change-Id: I25fc55edf968f41bfedecbeb2054a5eae56d0de7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2361025
Reviewed-by: Mounir Lamouri <mlamouri@chromium.org>
Commit-Queue: mark a. foltz <mfoltz@chromium.org>
Cr-Commit-Position: refs/heads/master@{#799342}

[modify] https://crrev.com/42a17e378ad7efbf57d47f3a7612d7c7cf95a907/third_party/blink/renderer/modules/presentation/presentation_connection_callbacks.cc


### mf...@chromium.org (2020-08-18)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-20)

Sheriffbot will shortly add some merge requests here, so I'll pre-empt it. mfoltz@ would you consider this fix essentially risk-free? If so we'll merge to M85 for tomorrow's RC cut.

### [Deleted User] (2020-08-20)

This bug requires manual review: We are only 4 days from stable.
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

### mf...@chromium.org (2020-08-20)

Yes, this should be very low risk.

### ad...@google.com (2020-08-20)

OK, thanks, approving merge to M85, branch 4183 - please merge.

### sr...@google.com (2020-08-20)

Please complete your merge before 12pm PST friday 8/21. I will be cutting stable RC build tomorrow afternoon

### sr...@google.com (2020-08-21)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6fc5082ae2d34aaa1153f97dae066105adc977ec

commit 6fc5082ae2d34aaa1153f97dae066105adc977ec
Author: mark a. foltz <mfoltz@chromium.org>
Date: Fri Aug 21 05:51:35 2020

[Presentation API] Fix use-after-free.

This fixes a potential UAF in PresentationConnectionCallbacks::OnSuccess.

TBR=mlamouri@chromium.org

(cherry picked from commit 42a17e378ad7efbf57d47f3a7612d7c7cf95a907)

Bug: 1116706
Change-Id: I25fc55edf968f41bfedecbeb2054a5eae56d0de7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2361025
Reviewed-by: Mounir Lamouri <mlamouri@chromium.org>
Commit-Queue: mark a. foltz <mfoltz@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#799342}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2368426
Reviewed-by: mark a. foltz <mfoltz@chromium.org>
Cr-Commit-Position: refs/branch-heads/4183@{#1636}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/6fc5082ae2d34aaa1153f97dae066105adc977ec/third_party/blink/renderer/modules/presentation/presentation_connection_callbacks.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9e61716a59e8b81ca44e529d0fea857298d7d8c9

commit 9e61716a59e8b81ca44e529d0fea857298d7d8c9
Author: mark a. foltz <mfoltz@chromium.org>
Date: Fri Aug 21 18:24:41 2020

[Presentation API] Adds unit test for PresentationConnectionCallbacks

Followup from https://chromium-review.googlesource.com/c/chromium/src/+/2361025

Bug: 1116706
Change-Id: I337b41b74d9a74c825d6b83a25eab29891c83008
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2363705
Commit-Queue: mark a. foltz <mfoltz@chromium.org>
Reviewed-by: Mounir Lamouri <mlamouri@chromium.org>
Cr-Commit-Position: refs/heads/master@{#800650}

[modify] https://crrev.com/9e61716a59e8b81ca44e529d0fea857298d7d8c9/third_party/blink/renderer/modules/BUILD.gn
[modify] https://crrev.com/9e61716a59e8b81ca44e529d0fea857298d7d8c9/third_party/blink/renderer/modules/presentation/presentation_connection.h
[modify] https://crrev.com/9e61716a59e8b81ca44e529d0fea857298d7d8c9/third_party/blink/renderer/modules/presentation/presentation_connection_callbacks.h
[add] https://crrev.com/9e61716a59e8b81ca44e529d0fea857298d7d8c9/third_party/blink/renderer/modules/presentation/presentation_connection_callbacks_test.cc


### [Deleted User] (2020-08-21)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### lw...@gmail.com (2020-08-25)

Credit Info: Liu Wei of Tencent Security Xuanwu Lab. Thanks.

### ad...@google.com (2020-08-26)

lw17qhdz@gmail.com (or mfoltz@) - please could you confirm whether this presents itself as a null pointer dereference or an actual use-after-free? Thanks.

### lw...@gmail.com (2020-08-27)

The above crash is similar to this issue (https://bugs.chromium.org/p/chromium/issues/detail?id=1051748). The execution context is destroyed in the callback, then "ControllerPresentationConnection::Init" use it.

### ad...@google.com (2020-09-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-09-02)

Congratulations! The VRP panel has decided to award $7,500 for this issue.

### ad...@google.com (2020-09-03)

Someone from our finance team will be in touch.

### ad...@google.com (2020-09-03)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-09-08)

mfoltz@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1116706?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053095)*

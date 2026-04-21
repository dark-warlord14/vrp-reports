# use after poison write in mojo::InterfaceEndpointClient::NotifyError when deal with WebBundle

| Field | Value |
|-------|-------|
| **Issue ID** | [40055403](https://issues.chromium.org/issues/40055403) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Loader, Blink>Loader>WebPackaging |
| **Platforms** | Linux |
| **Reporter** | ne...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2021-04-01 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36

Steps to reproduce the problem:
OS:Ubuntu:
Chrome Version: Chromium 91.0.4465.0 gs://chromium-browser-asan/linux-release/asan-linux-release-868361.zip

./chrome --enable-experimental-web-platform-features --user-data-dir=/tmp/xx   http://localhost:8000/main2.html

This is same issue with https://bugs.chromium.org/p/chromium/issues/detail?id=1193451.
Because  @drubery said could not repro with my poc. So I made a little change with poc,and tested with latest canary. After few seconds can repro this issue.
Can you try this one again?
thanks.

The stack trace is a little diffrent with original one(chrome dev 91.0.4455.2)

What is the expected behavior?

What went wrong?
==1==ERROR: AddressSanitizer: use-after-poison on address 0x7eb5dec9d250 at pc 0x5559ed88f256 bp 0x7ffc0c6eee70 sp 0x7ffc0c6eee68
WRITE of size 8 at 0x7eb5dec9d250 thread T0 (chrome)
==1==WARNING: invalid path to external symbolizer!
==1==WARNING: Failed to use and restart external symbolizer!
error: unknown argument '--demangle=True'
    #0 0x5559ed88f255 in mojo::ReceiverSetState::Entry::DispatchFilter::WillDispatch(mojo::Message*) ./../../mojo/public/cpp/bindings/receiver_set.cc:126
    #1 0x5559ed88f255 in WillDispatch ./../../mojo/public/cpp/bindings/receiver_set.cc:50
    #2 0x5559ed88f255 in WillDispatch ./../../mojo/public/cpp/bindings/receiver_set.cc:28
    #3 0x5559ed88f255 in ?? ??:0
    #4 0x5559ed868322 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:46
    #5 0x5559ed868322 in ?? ??:0
    #6 0x5559ed873c26 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:955
    #7 0x5559ed873c26 in ?? ??:0
    #8 0x5559ed872318 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:622
    #9 0x5559ed872318 in ?? ??:0
    #10 0x5559ed868461 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43
    #11 0x5559ed868461 in ?? ??:0
    #12 0x5559ed855d11 in mojo::Connector::DispatchMessage(mojo::Message) ./../../mojo/public/cpp/bindings/lib/connector.cc:508
    #13 0x5559ed855d11 in ?? ??:0
    #14 0x5559ed8576f0 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:566
    #15 0x5559ed8576f0 in ?? ??:0
    #16 0x5559ed858a24 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector> >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:509
    #17 0x5559ed858a24 in MakeItSo<void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>> ./../../base/bind_internal.h:668
    #18 0x5559ed858a24 in RunImpl<void (mojo::Connector::*)(), std::tuple<base::WeakPtr<mojo::Connector> >, 0> ./../../base/bind_internal.h:721
    #19 0x5559ed858a24 in RunOnce ./../../base/bind_internal.h:690
    #20 0x5559ed858a24 in ?? ??:0
    #21 0x5559ebeb7af6 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/callback.h:101
    #22 0x5559ebeb7af6 in RunTask ./../../base/task/common/task_annotator.cc:173
    #23 0x5559ebeb7af6 in ?? ??:0
    #24 0x5559ebef2c17 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351
    #25 0x5559ebef2c17 in ?? ??:0
    #26 0x5559ebef2444 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264
    #27 0x5559ebef2444 in ?? ??:0
    #28 0x5559ebdb09d0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39
    #29 0x5559ebdb09d0 in ?? ??:0
    #30 0x5559ebef3d3c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:460
    #31 0x5559ebef3d3c in ?? ??:0
    #32 0x5559ebe37641 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:133
    #33 0x5559ebe37641 in ?? ??:0
    #34 0x555a009465e3 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:262
    #35 0x555a009465e3 in ?? ??:0
    #36 0x5559ebb87c24 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:572
    #37 0x5559ebb87c24 in ?? ??:0
    #38 0x5559ebb8ad7e in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:958
    #39 0x5559ebb8ad7e in ?? ??:0
    #40 0x5559ebb852a6 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:372
    #41 0x5559ebb852a6 in ?? ??:0
    #42 0x5559ebb857fc in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:398
    #43 0x5559ebb857fc in ?? ??:0
    #44 0x5559df62cfb7 in ChromeMain ./../../chrome/app/chrome_main.cc:141
    #45 0x5559df62cfb7 in ?? ??:0
error: unknown argument '--demangle=True'
    #46 0x7f48cbeeb0b2 in __libc_start_main ??:?
    #47 0x7f48cbeeb0b2 in ?? ??:0

Address 0x7eb5dec9d250 is a wild pointer inside of access range of size 0x000000000008.
SUMMARY: AddressSanitizer: use-after-poison (/home/test/asan-linux-release-868361/chrome+0x18e2f255)
Shadow bytes around the buggy address:
  0x0fd73bd8b9f0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd73bd8ba00: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd73bd8ba10: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd73bd8ba20: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd73bd8ba30: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x0fd73bd8ba40: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7[f7]f7 f7 f7 f7 f7
  0x0fd73bd8ba50: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd73bd8ba60: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd73bd8ba70: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd73bd8ba80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd73bd8ba90: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==1==ABORTING
Received signal 6

Did this work before? N/A 

Chrome version:  91.0.4465.0  Channel: dev
OS Version: 20.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [test.wbn](attachments/test.wbn) (application/octet-stream, 3.4 KB)
- [main3.html](attachments/main3.html) (text/plain, 376 B)
- [poc3.html](attachments/poc3.html) (text/plain, 164 B)

## Timeline

### [Deleted User] (2021-04-01)

[Empty comment from Monorail migration]

### ne...@gmail.com (2021-04-02)

Sorry,There was an error in the previous main2.html file, so I uploaded new one.

### ne...@gmail.com (2021-04-02)

[Empty comment from Monorail migration]

### ne...@gmail.com (2021-04-02)

I tested with Official Build non-asan version. And will repro very quickly.
Version 91.0.4455.2 (Official Build) dev (64-bit)

### dr...@chromium.org (2021-04-05)

This one reproduces, thanks!  It took closer to a minute for me, but it did get there. Seems like a pretty tight race condition. Due to the need for  --enable-experimental-web-platform-features, marking Security_Impact-None, and high severity.

kinuko@, kohei@ - can you take a look?

[Monorail components: Blink>Loader]

### [Deleted User] (2021-04-05)

[Empty comment from Monorail migration]

### ki...@chromium.org (2021-04-30)

This did slip under my radar to triage quickly.  ksakamoto@, hayato@ or horo@: Can any of you take a look?

Looks like there's a race condition that makes the use-after-poison happen in Web Bundle code.

[Monorail components: Blink>Loader>WebPackaging]

### de...@chromium.org (2021-04-30)

[Empty comment from Monorail migration]

### ho...@chromium.org (2021-04-30)

I think the root cause of this issue is that WebBundleLoader is using mojo::ReceiverSet.
We need to use HeapMojoReceiverSet in a garbage-collected object.

### ho...@chromium.org (2021-04-30)

Created https://chromium-review.googlesource.com/c/chromium/src/+/2862749/.

### ho...@chromium.org (2021-04-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ab64f8864cbc16976e6a7e0faed1cd9c07789947

commit ab64f8864cbc16976e6a7e0faed1cd9c07789947
Author: Tsuyoshi Horo <horo@chromium.org>
Date: Thu May 06 03:49:18 2021

Use HeapMojoReceiverSet in WebBundleLoader

Bug: 1194829
Change-Id: I3650897f5c8bf10de7616b707076cb7f1285d4a5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2862749
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Commit-Queue: Tsuyoshi Horo <horo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#879683}

[modify] https://crrev.com/ab64f8864cbc16976e6a7e0faed1cd9c07789947/third_party/blink/renderer/core/html/link_web_bundle.cc


### ho...@chromium.org (2021-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-10)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-05-12)

Congratulations! The VRP Panel has decided to award you $5000 for this report. Nice work! 

### am...@google.com (2021-05-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-08-17)

This issue was migrated from crbug.com/chromium/1194829?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Loader, Blink>Loader>WebPackaging]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055403)*

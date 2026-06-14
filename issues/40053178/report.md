# UAF in devtools

| Field | Value |
|-------|-------|
| **Issue ID** | [40053178](https://issues.chromium.org/issues/40053178) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2020-08-27 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36

Steps to reproduce the problem:
1. open chromium `./chrome`
2. open devtools and choose the `Sources` tab, then press `Pause script execution`(or press F8)
3. switch to `Console` tab and input anything, such as 1
4. close the devtools , UAF occurs.

What is the expected behavior?

What went wrong?
VERSION
Chrome Version: asan-linux-release-802102 (download from https://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=linux-release/)
Operating System:  Linux. Windows and Mac 

Note that I also test is on Windwos and Mac with latest chrome, crash occurs too.
Here is the ASAN log:

=================================================================
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x611000326d18 at pc 0x55da841dff76 bp 0x7ffdd50c37d0 sp 0x7ffdd50c37c8
READ of size 8 at 0x611000326d18 thread T0 (chrome)
==1==WARNING: invalid path to external symbolizer!
==1==WARNING: Failed to use and restart external symbolizer!
    #0 0x55da841dff75  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x120aff75)
    #1 0x55da841e04de  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x120b04de)
    #2 0x55da8431e161  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x121ee161)
    #3 0x55da841a9ff4  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x12079ff4)
    #4 0x55da843b9b0d  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x12289b0d)
    #5 0x55da842fd612  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x121cd612)
    #6 0x55da93ec8989  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x21d98989)
    #7 0x55da93ec815f  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x21d9815f)
    #8 0x55da825f7017  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x104c7017)
    #9 0x55da87aae934  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x1597e934)
    #10 0x55da87abaff6  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x1598aff6)
    #11 0x55da8942d002  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x172fd002)
    #12 0x55da89426284  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x172f6284)
    #13 0x55da87043c25  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x14f13c25)
    #14 0x55da8707c06f  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x14f4c06f)
    #15 0x55da8707b8ef  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x14f4b8ef)
    #16 0x55da86f78f00  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x14e48f00)
    #17 0x55da8707d3b6  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x14f4d3b6)
    #18 0x55da86ff124a  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x14ec124a)
    #19 0x55da9896d252  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x2683d252)
    #20 0x55da85e995bf  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x13d695bf)
    #21 0x55da85e9ca88  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x13d6ca88)
    #22 0x55da8602fadd  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x13effadd)
    #23 0x55da85e97a4f  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x13d67a4f)
    #24 0x55da7bd82893  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x9c52893)
    #25 0x7f0c235a90b2  (/lib/x86_64-linux-gnu/libc.so.6+0x270b2)

0x611000326d18 is located 24 bytes inside of 208-byte region [0x611000326d00,0x611000326dd0)
freed by thread T0 (chrome) here:
    #0 0x55da7bd805ed  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x9c505ed)
    #1 0x55da84209f26  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x120d9f26)
    #2 0x55da84208754  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x120d8754)
    #3 0x55da842eb43e  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x121bb43e)
    #4 0x55da842f8c86  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x121c8c86)
    #5 0x55da842f808c  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x121c808c)
    #6 0x55da842f8e8d  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x121c8e8d)
    #7 0x55da93ec6a5e  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x21d96a5e)
    #8 0x55da87ab1e7c  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x15981e7c)
    #9 0x55da8942be54  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x172fbe54)
    #10 0x55da8942c333  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x172fc333)
    #11 0x55da87043c25  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x14f13c25)
    #12 0x55da8707c06f  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x14f4c06f)
    #13 0x55da8707b8ef  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x14f4b8ef)
    #14 0x55da86f78f00  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x14e48f00)
    #15 0x55da8707d527  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x14f4d527)
    #16 0x55da86ff124a  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x14ec124a)
    #17 0x55da9158a7db  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x1f45a7db)
    #18 0x55da9340da32  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x212dda32)
    #19 0x55da842c4c36  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x12194c36)
    #20 0x55da82d92eaa  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x10c62eaa)
    #21 0x55da82d90426  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x10c60426)
    #22 0x55da83a79e37  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x11949e37)
    #23 0x55da84c67357  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x12b37357)
    #24 0x55da84ce6fe5  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x12bb6fe5)
    #25 0x55da84bfb534  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x12acb534)
    #26 0x55da84bf9079  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x12ac9079)
    #27 0x55da84bf8e57  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x12ac8e57)
    #28 0x55da82e42a2e  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x10d12a2e)
    #29 0x55da82e41800  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x10d11800)

previously allocated by thread T0 (chrome) here:
    #0 0x55da7bd7fd8d  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x9c4fd8d)
    #1 0x55da84208082  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x120d8082)
    #2 0x55da842fa4e6  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x121ca4e6)
    #3 0x55da841e10cb  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x120b10cb)
    #4 0x55da841e01af  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x120b01af)
    #5 0x55da843256fb  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x121f56fb)
    #6 0x55da841a7876  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x12077876)
    #7 0x55da843b9b0d  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x12289b0d)
    #8 0x55da842fd612  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x121cd612)
    #9 0x55da93ec8989  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x21d98989)
    #10 0x55da93ec815f  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x21d9815f)
    #11 0x55da825f7017  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x104c7017)
    #12 0x55da87aae934  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x1597e934)
    #13 0x55da87abaff6  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x1598aff6)
    #14 0x55da8942d002  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x172fd002)
    #15 0x55da89426284  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x172f6284)
    #16 0x55da87043c25  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x14f13c25)
    #17 0x55da8707c06f  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x14f4c06f)
    #18 0x55da8707b8ef  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x14f4b8ef)
    #19 0x55da86f78f00  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x14e48f00)
    #20 0x55da8707d3b6  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x14f4d3b6)
    #21 0x55da86ff124a  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x14ec124a)
    #22 0x55da9896d252  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x2683d252)
    #23 0x55da85e995bf  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x13d695bf)
    #24 0x55da85e9ca88  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x13d6ca88)
    #25 0x55da8602fadd  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x13effadd)
    #26 0x55da85e97a4f  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x13d67a4f)
    #27 0x55da7bd82893  (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x9c52893)
    #28 0x7f0c235a90b2  (/lib/x86_64-linux-gnu/libc.so.6+0x270b2)

SUMMARY: AddressSanitizer: heap-use-after-free (/home/krace/fuzz/chromium/src/out/asan-linux-release-802102/chrome+0x120aff75) 
Shadow bytes around the buggy address:
  0x0c228005cd50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c228005cd60: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x0c228005cd70: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c228005cd80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c228005cd90: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
=>0x0c228005cda0: fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c228005cdb0: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x0c228005cdc0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c228005cdd0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c228005cde0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c228005cdf0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

CREDIT INFORMATION
Reporter credit: Weipeng Jiang (@Krace) from Codesafe Team of Legendsec at Qi'anxin Group

Did this work before? N/A 

Chrome version: 84.0.4147.135  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- [test.mp4](attachments/test.mp4) (video/mp4, 1.2 MB)
- [asan-log.txt](attachments/asan-log.txt) (text/plain, 16.8 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### me...@gmail.com (2020-08-27)

Here is the asan log with llvm-symbolizer, I find that the problem maybe occurs in IPC 
`ipc/ipc_mojo_bootstrap.cc`



free:
```
...
    blink::DevToolsSession::Detach()
    ./../../third_party/blink/renderer/core/inspector/devtools_session.cc:185:15

    Run
    ./../../base/callback.h:99:12
    mojo::InterfaceEndpointClient::NotifyError(base::Optional<mojo::DisconnectReason> const&)
    ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:376:31

    IPC::(anonymous namespace)::ChannelAssociatedGroupController::NotifyEndpointOfError(IPC::(anonymous namespace)::ChannelAssociatedGroupController::Endpoint*, bool)
    ./../../ipc/ipc_mojo_bootstrap.cc:783:15

    IPC::(anonymous namespace)::ChannelAssociatedGroupController::NotifyEndpointOfErrorOnEndpointThread(unsigned int, IPC::(anonymous namespace)::ChannelAssociatedGroupController::Endpoint*)
    ./../../ipc/ipc_mojo_bootstrap.cc:803:5

    Run
    ./../../base/callback.h:99:12
    base::TaskAnnotator::RunTask(char const*, base::PendingTask*)
    ./../../base/task/common/task_annotator.cc:142:33
...
```
 777     if (endpoint->task_runner()->RunsTasksInCurrentSequence() && !force_async) {
 778       mojo::InterfaceEndpointClient* client = endpoint->client();
 779       base::Optional<mojo::DisconnectReason> reason(
 780           endpoint->disconnect_reason());
 781 
 782       base::AutoUnlock unlocker(lock_);
 783       client->NotifyError(reason);
 784     } 

 In line 783, it will unlocker and then call NotifyError, whcih will call `blink::DevToolsSession::Detach`
 that will free memory. 

==================

use:
```
...
    mojo::MessageDispatcher::Accept(mojo::Message*)
    ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:41:19

    IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnProxyThread(mojo::Message)
    ./../../ipc/ipc_mojo_bootstrap.cc:930:24

    Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>
    ./../../base/bind_internal.h:498:12
    MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>
    ./../../base/bind_internal.h:637:12
    RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__1::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0, 1>
    ./../../base/bind_internal.h:710:12
    base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*)
    ./../../base/bind_internal.h:679:12

    Run
    ./../../base/callback.h:99:12
    base::TaskAnnotator::RunTask(char const*, base::PendingTask*)
    ./../../base/task/common/task_annotator.cc:142:33
...
```
 927     bool result = false;
 928     {
 929       base::AutoUnlock unlocker(lock_);
 930       result = client->HandleIncomingMessage(&message);
 931     }

In line 930, it also unlocker and then call HandleIncomingMessage, which will use the freed memory.

So, I think this problem may be caused by race condition in multi thread.(Just a guess)

Hope this helps you guys:) 

### ts...@chromium.org (2020-08-27)

Sev medium due to the interaction required, otherwise might be considered high.

[Monorail components: Platform>DevTools]

### ha...@chromium.org (2020-08-27)

[Empty comment from Monorail migration]

### ha...@chromium.org (2020-08-27)

[Empty comment from Monorail migration]

### ha...@google.com (2020-08-28)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-28)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-28)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-09-10)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@gmail.com (2020-09-23)

hello, any update for this one ?

### me...@gmail.com (2020-09-24)

hi, here is some analysis, hope to help you.

### [Deleted User] (2020-09-25)

caseq: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2020-09-29)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/582de025d8a89ec7b5c839d4269159c5db25f44a

commit 582de025d8a89ec7b5c839d4269159c5db25f44a
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Wed Sep 30 00:12:24 2020

Do not pause on breaks while installing additional command line API

A break may cause the session disconnect (and therefore agents destruction)
on a nested message loop. The runtime agent code is generally prepared to
handle this during evaluate, but the code outside of it may be not. Besides,
having a break before the console API installed is generally not what
user wants or expects, so just disable all breaks while installing the API.

Bug: chromium:1122487
Change-Id: I1d40f5007f2e1e4ec07a50ef57988513d0309b7e
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2437383
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#70209}

[modify] https://crrev.com/582de025d8a89ec7b5c839d4269159c5db25f44a/src/api/api.cc
[modify] https://crrev.com/582de025d8a89ec7b5c839d4269159c5db25f44a/src/debug/debug-interface.h
[modify] https://crrev.com/582de025d8a89ec7b5c839d4269159c5db25f44a/src/inspector/injected-script.cc
[rename] https://crrev.com/582de025d8a89ec7b5c839d4269159c5db25f44a/test/inspector/debugger/destroy-in-break-program-expected.txt
[rename] https://crrev.com/582de025d8a89ec7b5c839d4269159c5db25f44a/test/inspector/debugger/destroy-in-break-program.js
[add] https://crrev.com/582de025d8a89ec7b5c839d4269159c5db25f44a/test/inspector/debugger/destroy-in-break-program2-expected.txt
[add] https://crrev.com/582de025d8a89ec7b5c839d4269159c5db25f44a/test/inspector/debugger/destroy-in-break-program2.js
[modify] https://crrev.com/582de025d8a89ec7b5c839d4269159c5db25f44a/test/inspector/inspector-test.cc
[modify] https://crrev.com/582de025d8a89ec7b5c839d4269159c5db25f44a/test/inspector/isolate-data.cc
[modify] https://crrev.com/582de025d8a89ec7b5c839d4269159c5db25f44a/test/inspector/isolate-data.h


### ca...@chromium.org (2020-10-01)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-01)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-05)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M86. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-05)

This bug requires manual review: We are only 0 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS),  pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2020-10-05)

While the fix should be fairly safe, I'm not sure if the severity of the bug meets the bar for merge -- it's a UAF in sandboxed code that requires a pretty elaborate scenario to trigger.  Adrian, WDYT?

### ad...@google.com (2020-10-07)

Yeah, no need to merge this, given it's entirely UI-driven.

### ad...@google.com (2020-10-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-07)

The VRP panel considers that this is probably not a security bug (given that the only known way to trigger it is through UI actions) but has decided to award $500 as a 'thank you' for being so helpful in your report here.

### me...@gmail.com (2020-10-08)

Thanks :)
BTW, is this eligible for a CVE?

### ad...@google.com (2020-10-08)

We've decided to keep it in the security queue, just in case there's some remote way to trigger this, so per our normal process yes this will be eligible for a CVE when the fix is released (looks like M87).

### ad...@google.com (2020-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-13)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-03-29)

merc.ouc@ - we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1122487?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053178)*

# uaf in device::FidoRequestHandlerBase::InitializeAuthenticatorAndDispatchRequest

| Field | Value |
|-------|-------|
| **Issue ID** | [40052296](https://issues.chromium.org/issues/40052296) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | ma...@google.com |
| **Created** | 2020-05-13 |
| **Bounty** | $20,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36

Steps to reproduce the problem:
Chromium 84.0.4127.0
Chromium 84.0.4144.0
1 python ./copy_mojo_js_bindings.py /path/to/chrome/.../out/asan/gen (copy all *.js file)
2 python3.6m -m http.server 8605
3 ./chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/nonexist  http://localhost:8605/crash.html

What is the expected behavior?

What went wrong?
==12057==ERROR: AddressSanitizer: heap-use-after-free on address 0x602000aca858 at pc 0x55c9d77501d5 bp 0x7ffe0eb87030 sp 0x7ffe0eb87028
READ of size 8 at 0x602000aca858 thread T0 (chrome)
    #0 0x55c9d77501d4 in reset buildtools/third_party/libc++/trunk/include/memory:2630:28
    #1 0x55c9d77501d4 in operator= buildtools/third_party/libc++/trunk/include/memory:2552:5
    #2 0x55c9d77501d4 in device::FidoRequestHandlerBase::InitializeAuthenticatorAndDispatchRequest(device::FidoRequestHandlerBase::AuthenticatorState*) device/fido/fido_request_handler_base.cc:357:30
    #3 0x55c9d39a7379 in Run base/callback.h:99:12
    #4 0x55c9d39a7379 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:142:33
    #5 0x55c9d39e10e1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:321:23
    #6 0x55c9d39e0a48 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:246:36
    #7 0x55c9d38e0670 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:443:48
    #8 0x55c9d39e2339 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:425:12
    #9 0x55c9d39584c6 in base::RunLoop::Run() base/run_loop.cc:124:14
    #10 0x55c9d2aff0fc in ChromeBrowserMainParts::MainMessageLoopRun(int*) chrome/browser/chrome_browser_main.cc:1683:15
    #11 0x55c9cc86fa22 in content::BrowserMainLoop::RunMainMessageLoopParts() content/browser/browser_main_loop.cc:1054:29
    #12 0x55c9cc875ed1 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:150:15
    #13 0x55c9cc867b3c in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:47:28
    #14 0x55c9d290836e in RunBrowserProcessMain content/app/content_main_runner_impl.cc:502:10
    #15 0x55c9d290836e in content::ContentMainRunnerImpl::RunServiceManager(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:944:10
    #16 0x55c9d29076a1 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:845:12
    #17 0x55c9d2a9ab05 in service_manager::Main(service_manager::MainParams const&) services/service_manager/embedder/main.cc:454:29
    #18 0x55c9d2902796 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:19:10
    #19 0x55c9c90a4c44 in ChromeMain chrome/app/chrome_main.cc:110:12
    #20 0x7f06c6948b96 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310

0x602000aca858 is located 8 bytes inside of 16-byte region [0x602000aca850,0x602000aca860)
freed by thread T0 (chrome) here:
    #0 0x55c9c90a22cd in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x55c9d7751be6 in operator() buildtools/third_party/libc++/trunk/include/memory:2378:5
    #2 0x55c9d7751be6 in reset buildtools/third_party/libc++/trunk/include/memory:2633:7
    #3 0x55c9d7751be6 in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:2587:19
    #4 0x55c9d7751be6 in device::FidoRequestHandlerBase::AuthenticatorAdded(device::FidoDiscoveryBase*, device::FidoAuthenticator*) device/fido/fido_request_handler_base.cc:343:1
    #5 0x55c9d7751158 in device::FidoRequestHandlerBase::DiscoveryStarted(device::FidoDiscoveryBase*, bool, std::__1::vector<device::FidoAuthenticator*, std::__1::allocator<device::FidoAuthenticator*> >) device/fido/fido_request_handler_base.cc:289:7
    #6 0x55c9d76d61ac in device::FidoDeviceDiscovery::NotifyDiscoveryStarted(bool) device/fido/fido_device_discovery.cc:49:15
    #7 0x55c9d39a7379 in Run base/callback.h:99:12
    #8 0x55c9d39a7379 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:142:33
    #9 0x55c9d39e10e1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:321:23
    #10 0x55c9d39e0a48 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:246:36
    #11 0x55c9d38e145c in HandleDispatch base/message_loop/message_pump_glib.cc:409:46
    #12 0x55c9d38e145c in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:122:43
    #13 0x7f06cbd54416 in g_main_context_dispatch (/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x4c416)

previously allocated by thread T0 (chrome) here:
    #0 0x55c9c90a1a6d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x55c9d775153b in make_unique<device::FidoRequestHandlerBase::AuthenticatorState, device::FidoAuthenticator *&> buildtools/third_party/libc++/trunk/include/memory:3043:28
    #2 0x55c9d775153b in device::FidoRequestHandlerBase::AuthenticatorAdded(device::FidoDiscoveryBase*, device::FidoAuthenticator*) device/fido/fido_request_handler_base.cc:302:7
    #3 0x55c9d7751158 in device::FidoRequestHandlerBase::DiscoveryStarted(device::FidoDiscoveryBase*, bool, std::__1::vector<device::FidoAuthenticator*, std::__1::allocator<device::FidoAuthenticator*> >) device/fido/fido_request_handler_base.cc:289:7
    #4 0x55c9d76d61ac in device::FidoDeviceDiscovery::NotifyDiscoveryStarted(bool) device/fido/fido_device_discovery.cc:49:15
    #5 0x55c9d39a7379 in Run base/callback.h:99:12
    #6 0x55c9d39a7379 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:142:33
    #7 0x55c9d39e10e1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:321:23
    #8 0x55c9d39e0a48 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:246:36
    #9 0x55c9d38e145c in HandleDispatch base/message_loop/message_pump_glib.cc:409:46
    #10 0x55c9d38e145c in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:122:43
    #11 0x7f06cbd54416 in g_main_context_dispatch (/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x4c416)

SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third_party/libc++/trunk/include/memory:2630:28 in reset
Shadow bytes around the buggy address:
  0x0c04801514b0: fa fa fd fd fa fa fd fa fa fa fd fd fa fa fd fd
  0x0c04801514c0: fa fa fd fd fa fa fd fa fa fa fa fa fa fa fa fa
  0x0c04801514d0: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c04801514e0: fa fa fd fa fa fa fd fd fa fa fa fa fa fa fd fd
  0x0c04801514f0: fa fa fd fa fa fa 00 fa fa fa fd fd fa fa 00 fa
=>0x0c0480151500: fa fa fd fd fa fa 00 00 fa fa fd[fd]fa fa fd fd
  0x0c0480151510: fa fa fd fd fa fa fa fa fa fa fd fd fa fa fd fa
  0x0c0480151520: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fa
  0x0c0480151530: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c0480151540: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fd
  0x0c0480151550: fa fa fa fa fa fa fd fd fa fa fd fd fa fa fd fa
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
==12057==ABORTING

Did this work before? N/A 

Chrome version: Chromium 84.0.4144.0  Channel: n/a
OS Version: 18.04
Flash Version:

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 110.7 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 508 B)
- [poc.zip](attachments/poc_53318680.zip) (application/octet-stream, 110.7 KB)
- [crash2.html](attachments/crash2.html) (text/plain, 2.0 KB)
- [authonticator-uaf-analysis.pdf](attachments/authonticator-uaf-analysis.pdf) (application/pdf, 1.0 MB)

## Timeline

### ct...@chromium.org (2020-05-13)

It looks like the poc.zip file is password-protected. Could you upload an unencrypted copy or share the password? Thanks.

### cd...@gmail.com (2020-05-13)

Sorry for my mistake.
I uploaded again with no password zip.

### [Deleted User] (2020-05-13)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-05-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5189863752663040.

### cl...@chromium.org (2020-05-13)

Testcase 5189863752663040 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5189863752663040.

### ct...@chromium.org (2020-05-13)

Adding some OWNERS and component to help investigate. I'll fiddle with Clusterfuzz more to get a working testcase.

Severity-High for memory corruption in browser that requires compromised renderer. Impact-Head, but this may affect prior milestones because it looks like the relevant bits of webauthn code were last touched in March (so are in M-83) or much earlier.

[Monorail components: Blink>WebAuthentication]

### ag...@chromium.org (2020-05-13)

Line lines appear to match file at 8dfaaffe3ccc, but I don't immediately see how the issue occurs: The trace says that the AuthenticatorState is getting freed at the end of  FidoRequestHandlerBase::AuthenticatorAdded, but it looks to me like it's unconditionally moved into active_authenticators_.

### ag...@chromium.org (2020-05-13)

(Ah, unless the emplace *didn't* move it because there's a duplicate Id in active_authenticators_?)

### ma...@google.com (2020-05-13)

I agree that's an issue, but I don't see how the POC would be triggering that? It's only creating a single authenticator right? Wouldn't AuthenticatorAdded() have to be invoked twice for that AuthenticatorState to get destroyed by the emplace() call?

Another issue is that, theoretically, AuthenticatorRemoved() could erase the AuthenticatorState from active_authenticators_ before InitializeAuthenticatorAndDispatchRequest() runs, I think? But I don't see that could be the cause here either.

### cd...@gmail.com (2020-05-14)

I modifed the POC, and now it is more stable. When [setInterval] is called about 2000 times (about 10 seconds)  in my local pc, it will crash.

### [Deleted User] (2020-05-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-05-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6113551633154048.

### ct...@chromium.org (2020-05-14)

Re #10: I think your PoC is fine, but thanks for the updated version. I'm just still trying to coerce clusterfuzz into running it correctly, so there may be some noise here while I work on that.

### cl...@chromium.org (2020-05-14)

Testcase 6113551633154048 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6113551633154048.

### cd...@gmail.com (2020-05-15)

We analyze the issue and find out the cause of UAF. The adding of authentication devices is accomplished by the function [FidoRequestHandlerBase:: AuthenticatorAdded], but when too many authentication devices are created, it triggers the reallocation of map container memory, resulting the release of internal objects.The attachment is the analysis document. I hope it  it helps.
Thansk~

### cd...@gmail.com (2020-05-18)

I found that my analysis was wrong--;. 
The cause of the uaf was not be the reallocation of the map. 
I  delete attachments that contain errors. 
If there are new discoveries, I will update it.
Sorry to bother you...

### cl...@chromium.org (2020-05-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5641931432984576.

### pb...@google.com (2020-05-18)

[Empty comment from Monorail migration]

### pb...@google.com (2020-05-18)

[Empty comment from Monorail migration]

### sr...@google.com (2020-05-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-05-18)

Testcase 5641931432984576 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5641931432984576.

### cl...@chromium.org (2020-05-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5698412098420736.

### cl...@chromium.org (2020-05-18)

Testcase 5698412098420736 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5698412098420736.

### cl...@chromium.org (2020-05-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5634421112242176.

### cl...@chromium.org (2020-05-19)

Testcase 5634421112242176 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5634421112242176.

### cd...@gmail.com (2020-05-19)

> Version: 84.0.4145.3 release
>
> OS: Windows 10 1909 18363.836

UAF may result when calling the function FidoRequestHandlerBase::AuthenticatorAdded for the addition of authentication device objects.

```c++
void FidoRequestHandlerBase::AuthenticatorAdded(
    FidoDiscoveryBase* discovery,
    FidoAuthenticator* authenticator) {
  DCHECK(authenticator &&
         !base::Contains(active_authenticators(), authenticator->GetId()));
  auto authenticator_state =
      std::make_unique<AuthenticatorState>(authenticator);
  auto* weak_authenticator_state = authenticator_state.get();
  active_authenticators_.emplace(authenticator->GetId(),
                                 std::move(authenticator_state));
//...
}
```

active_authenticators_ is a AuthenticatorMap.

```c++
using AuthenticatorMap =
    std::map<std::string, std::unique_ptr<AuthenticatorState>, std::less<>>;
```

Failure to add an element when its key conflicts with another element in the map.You can see how GetID gets key values here:

```c++
std::string VirtualFidoDevice::GetId() const {
  // Use our heap address to get a unique-ish number. (0xffe1 is a prime).
  return "VirtualFidoDevice-" + std::to_string((size_t)this % 0xffe1);
}
```

This can easily lead to repetition.

Since authenticator_state is unique_ptr, if the element added here fails, authenticator_state will be released at the end of the FidoRequestHandlerBase::AuthenticatorAdded().

And in FidoRequestHandlerBase::AuthenticatorAdded the original pointer of Authenticator_state is passed into the callback function FidoRequestHandlerBase::InitializeAuthenticatorAndDispatchRequest.

```c++
void FidoRequestHandlerBase::AuthenticatorAdded(
    FidoDiscoveryBase* discovery,
    FidoAuthenticator* authenticator) {
  DCHECK(authenticator &&
         !base::Contains(active_authenticators(), authenticator->GetId()));
  auto authenticator_state =
      std::make_unique<AuthenticatorState>(authenticator);
  auto* weak_authenticator_state = authenticator_state.get();
  //...

  if (!embedder_controls_dispatch) {
    // Post |InitializeAuthenticatorAndDispatchRequest| into its own task. This
    // avoids hairpinning, even if the authenticator immediately invokes the
    // request callback.
    VLOG(2)
        << "Request handler dispatching request to authenticator immediately.";
    base::SequencedTaskRunnerHandle::Get()->PostTask(
        FROM_HERE,
        base::BindOnce(
            &FidoRequestHandlerBase::InitializeAuthenticatorAndDispatchRequest,
            GetWeakPtr(), weak_authenticator_state));
  } else {
    VLOG(2) << "Embedder controls the dispatch.";
  }
//...
}
```

UAF will be triggered in the callback function.

```c++
void FidoRequestHandlerBase::InitializeAuthenticatorAndDispatchRequest(
    AuthenticatorState* authenticator_state) {
  authenticator_state->timer = std::make_unique<base::ElapsedTimer>();
  authenticator_state->authenticator->InitializeAuthenticator(base::BindOnce(
      &FidoRequestHandlerBase::DispatchRequest, weak_factory_.GetWeakPtr(),
      authenticator_state->authenticator));
}
```

Vulnerability will not be triggered when adding detection of the emplace return value to the FidoRequestHandlerBase::AuthenticatorAdded function. Here is the function that I patched:

```c++
void FidoRequestHandlerBase::AuthenticatorAdded(
    FidoDiscoveryBase* discovery,
    FidoAuthenticator* authenticator) {
  DCHECK(authenticator &&
         !base::Contains(active_authenticators(), authenticator->GetId()));
  auto authenticator_state =
      std::make_unique<AuthenticatorState>(authenticator);
  auto* weak_authenticator_state = authenticator_state.get();
  auto device_id = authenticator->GetId();
  auto result = active_authenticators_.emplace(device_id,
                                 std::move(authenticator_state));

  // If |observer_| exists, dispatching request to |authenticator| is
  // delegated to |observer_|. Else, dispatch request to |authenticator|
  // immediately.
  bool embedder_controls_dispatch = false;
  if (observer_) {
    embedder_controls_dispatch =
        observer_->EmbedderControlsAuthenticatorDispatch(*authenticator);
    observer_->FidoAuthenticatorAdded(*authenticator);
  }

  if (!embedder_controls_dispatch && result.second) {
    // Post |InitializeAuthenticatorAndDispatchRequest| into its own task. This
    // avoids hairpinning, even if the authenticator immediately invokes the
    // request callback.
    VLOG(2)
        << "Request handler dispatching request to authenticator immediately.";
    base::SequencedTaskRunnerHandle::Get()->PostTask(
        FROM_HERE,
        base::BindOnce(
            &FidoRequestHandlerBase::InitializeAuthenticatorAndDispatchRequest,
            GetWeakPtr(), weak_authenticator_state));
  } else {
    VLOG(2) << "Embedder controls the dispatch.";
  }

#if defined(OS_WIN)
  if (authenticator->IsWinNativeApiAuthenticator()) {
    DCHECK(transport_availability_info_.has_win_native_api_authenticator);
    transport_availability_info_.win_native_api_authenticator_id =
        authenticator->GetId();
    transport_availability_info_
        .win_native_ui_shows_resident_credential_notice =
        static_cast<WinWebAuthnApiAuthenticator*>(authenticator)
            ->ShowsPrivacyNotice();
  }
#endif  // defined(OS_WIN)
}
```

### sr...@google.com (2020-05-19)

we are doing stable promotion for M83 today,  based on the comments so far, I dont see this as RBS for M83,  Please let me know if anyone thinks this should block stable. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bdbf8ce8f546e6bc3e2c2fe7e68ac4ae6156c5b6

commit bdbf8ce8f546e6bc3e2c2fe7e68ac4ae6156c5b6
Author: Martin Kreichgauer <martinkr@google.com>
Date: Tue May 19 18:21:54 2020

fido: improve guards against adding authenticators with identical IDs

Make FidoRequestHandler::AuthenticatorAdded() return early when an
FidoAuthenticator is added whose ID matches that of a previously added
authenticator. The request handler  previously did not add the
duplicate authenticator into its |active_authenticators_| map, but then
attempted to dispatch its request to it (or rather to an invalid
reference).

Also better guard against authenticators being removed during
initialization by making the (asynchronously run)
InitializeAuthenticatorAndDispatchRequest() method look up the
AuthenticatorState for the authenticator to be initialized by its ID
rather than passing around AuthenticatorState pointers that may have
been freed by the time the method runs because the authenticator went
away.

Lastly, derive VirtualFidoDevice IDs randomly. It previously used its
instance pointer address for "randomness" which, aside from being weird,
could lead to re-use of IDs. (FidoAuthenticator ID reuse in itself
_should_ not be a problem, but certainly could lead to bugs if the rest
of the code is less than careful about it.)

Bug: 1082105
Change-Id: Ie4e3fd39c3360bf0131cdd6dd33b2be4dbb225a8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2203776
Commit-Queue: Martin Kreichgauer <martinkr@google.com>
Reviewed-by: Christopher Thompson <cthomp@chromium.org>
Reviewed-by: Adam Langley <agl@chromium.org>
Cr-Commit-Position: refs/heads/master@{#770190}

[modify] https://crrev.com/bdbf8ce8f546e6bc3e2c2fe7e68ac4ae6156c5b6/device/fido/fido_request_handler_base.cc
[modify] https://crrev.com/bdbf8ce8f546e6bc3e2c2fe7e68ac4ae6156c5b6/device/fido/fido_request_handler_base.h
[modify] https://crrev.com/bdbf8ce8f546e6bc3e2c2fe7e68ac4ae6156c5b6/device/fido/virtual_fido_device.cc
[modify] https://crrev.com/bdbf8ce8f546e6bc3e2c2fe7e68ac4ae6156c5b6/device/fido/virtual_fido_device.h


### ma...@google.com (2020-05-19)

So the CL that introduced the UAF landed in M83, and I can repro the POC there. 

After IM discussion with srinivassista, we agreed to merge the fix to 83 and re-spin, but not block stable. 

### ct...@chromium.org (2020-05-19)

Thanks! That assessment sounds good to me.

### ad...@chromium.org (2020-05-20)

Adjusting labels per https://crbug.com/chromium/1082105#c29. Did https://crbug.com/chromium/1082105#c28 fix this? If so, please mark as Fixed and Sheriffbot will add a bunch of merge request labels.

### cd...@gmail.com (2020-05-20)

Hi,
I found a similar code snippet, but the GUID is used as the first param here. 
Although UAF will not be triggered in general, but it may still need to fix.

content/browser/webauth/virtual_fido_discovery_factory.cc

VirtualAuthenticator* VirtualFidoDiscoveryFactory::CreateAuthenticator(
    device::ProtocolVersion protocol,
    device::FidoTransportProtocol transport,
    device::AuthenticatorAttachment attachment,
    bool has_resident_key,
    bool has_user_verification) {
  if (protocol == device::ProtocolVersion::kU2f &&
      !device::VirtualU2fDevice::IsTransportSupported(transport)) {
    return nullptr;
  }
  auto authenticator = std::make_unique<VirtualAuthenticator>(
      protocol, transport, attachment, has_resident_key, has_user_verification);
  auto* authenticator_ptr = authenticator.get();
  authenticators_.emplace(authenticator_ptr->unique_id(),
                          std::move(authenticator));



### ma...@google.com (2020-05-20)

[Empty comment from Monorail migration]

### ma...@google.com (2020-05-20)

https://crbug.com/chromium/1082105#c31: Yes, that's a fix. Is there value in reproing this on clusterfuzz still? The modified POC is stable in my tests, not totally sure why we can't repro it in clusterfuzz. But if that's normal procedure, I'm happy to try.

Re https://crbug.com/chromium/1082105#c32: Yeah, good catch. This isn't a bug yet, as you point out, because the insertion key is a fresh GUID for each VirtualAuthenticator. But I'll write a change to tighten that up, so it doesn't regress into the same bug as the one that https://crbug.com/chromium/1082105#c28 fixed.

### ad...@chromium.org (2020-05-20)

The benefits of reproing in ClusterFuzz:
1) It can identify the original regression CL, which in particular teaches us which branches we need to merge the fix back to (M83, M84?) - by means of setting the Security_Impact label correctly.
2) It can mark the bug as Verified now you've fixed it.

But if you're sure the problem was introduced in M83, and you're confident it's fixed, I don't think we need that.

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

Requesting merge to stable M83 because latest trunk commit (770190) appears to be after stable branch point (756066).

Requesting merge to beta M83 because latest trunk commit (770190) appears to be after beta branch point (756066).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-20)

This bug requires manual review: Request affecting a post-stable build
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
Owners: benmason@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-05-26)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-26)

The reporter has requested anonymity, so tagging with RV-SE.

### ma...@google.com (2020-05-26)

Re https://crbug.com/chromium/1082105#c38, per https://crbug.com/chromium/1082105#c29 we agreed that this qualifies for a post-stable merge to M83.

### ad...@google.com (2020-05-27)

Approving merge to M83, branch 4103, per https://crbug.com/chromium/1082105#c29, assuming this is looking good in Canary. This is at the more complex end of the range of changes that we merge to M83, so martinkr@ please do confirm that you think this is virtually risk-free to bypass normal bake time.

### na...@google.com (2020-05-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### sr...@google.com (2020-05-28)

Please complete the merge to M83 branch asap, as we will cut the re-spin RC tomorrow.

### ma...@google.com (2020-05-28)

I'm about to merge to M83. We will need an M84 merge as well, since the fix only landed in M85.



### ad...@google.com (2020-05-28)

Approving merge to M84, branch 4147.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/498ff740cb624a3337d4d30eff53d6656d96971d

commit 498ff740cb624a3337d4d30eff53d6656d96971d
Author: Martin Kreichgauer <martinkr@google.com>
Date: Thu May 28 20:30:22 2020

[m84] fido: improve guards against adding authenticators with identical IDs

Make FidoRequestHandler::AuthenticatorAdded() return early when an
FidoAuthenticator is added whose ID matches that of a previously added
authenticator. The request handler  previously did not add the
duplicate authenticator into its |active_authenticators_| map, but then
attempted to dispatch its request to it (or rather to an invalid
reference).

Also better guard against authenticators being removed during
initialization by making the (asynchronously run)
InitializeAuthenticatorAndDispatchRequest() method look up the
AuthenticatorState for the authenticator to be initialized by its ID
rather than passing around AuthenticatorState pointers that may have
been freed by the time the method runs because the authenticator went
away.

Lastly, derive VirtualFidoDevice IDs randomly. It previously used its
instance pointer address for "randomness" which, aside from being weird,
could lead to re-use of IDs. (FidoAuthenticator ID reuse in itself
_should_ not be a problem, but certainly could lead to bugs if the rest
of the code is less than careful about it.)

(cherry picked from commit bdbf8ce8f546e6bc3e2c2fe7e68ac4ae6156c5b6)

Bug: 1082105
Change-Id: Ie4e3fd39c3360bf0131cdd6dd33b2be4dbb225a8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2203776
Commit-Queue: Martin Kreichgauer <martinkr@google.com>
Reviewed-by: Christopher Thompson <cthomp@chromium.org>
Reviewed-by: Adam Langley <agl@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#770190}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2219925
Reviewed-by: Martin Kreichgauer <martinkr@google.com>
Cr-Commit-Position: refs/branch-heads/4147@{#324}
Cr-Branched-From: 16307825352720ae04d898f37efa5449ad68b606-refs/heads/master@{#768962}

[modify] https://crrev.com/498ff740cb624a3337d4d30eff53d6656d96971d/device/fido/fido_request_handler_base.cc
[modify] https://crrev.com/498ff740cb624a3337d4d30eff53d6656d96971d/device/fido/fido_request_handler_base.h
[modify] https://crrev.com/498ff740cb624a3337d4d30eff53d6656d96971d/device/fido/virtual_fido_device.cc
[modify] https://crrev.com/498ff740cb624a3337d4d30eff53d6656d96971d/device/fido/virtual_fido_device.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6e6b3096ffa9d054c9a3b4f59594ef840dd25545

commit 6e6b3096ffa9d054c9a3b4f59594ef840dd25545
Author: Martin Kreichgauer <martinkr@google.com>
Date: Thu May 28 20:31:12 2020

[m83] fido: improve guards against adding authenticators with identical IDs

Make FidoRequestHandler::AuthenticatorAdded() return early when an
FidoAuthenticator is added whose ID matches that of a previously added
authenticator. The request handler  previously did not add the
duplicate authenticator into its |active_authenticators_| map, but then
attempted to dispatch its request to it (or rather to an invalid
reference).

Also better guard against authenticators being removed during
initialization by making the (asynchronously run)
InitializeAuthenticatorAndDispatchRequest() method look up the
AuthenticatorState for the authenticator to be initialized by its ID
rather than passing around AuthenticatorState pointers that may have
been freed by the time the method runs because the authenticator went
away.

Lastly, derive VirtualFidoDevice IDs randomly. It previously used its
instance pointer address for "randomness" which, aside from being weird,
could lead to re-use of IDs. (FidoAuthenticator ID reuse in itself
_should_ not be a problem, but certainly could lead to bugs if the rest
of the code is less than careful about it.)

(cherry picked from commit bdbf8ce8f546e6bc3e2c2fe7e68ac4ae6156c5b6)

Bug: 1082105
Change-Id: Ie4e3fd39c3360bf0131cdd6dd33b2be4dbb225a8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2203776
Commit-Queue: Martin Kreichgauer <martinkr@google.com>
Reviewed-by: Christopher Thompson <cthomp@chromium.org>
Reviewed-by: Adam Langley <agl@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#770190}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2220073
Reviewed-by: Martin Kreichgauer <martinkr@google.com>
Cr-Commit-Position: refs/branch-heads/4103@{#629}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/6e6b3096ffa9d054c9a3b4f59594ef840dd25545/device/fido/fido_request_handler_base.cc
[modify] https://crrev.com/6e6b3096ffa9d054c9a3b4f59594ef840dd25545/device/fido/fido_request_handler_base.h
[modify] https://crrev.com/6e6b3096ffa9d054c9a3b4f59594ef840dd25545/device/fido/virtual_fido_device.cc
[modify] https://crrev.com/6e6b3096ffa9d054c9a3b4f59594ef840dd25545/device/fido/virtual_fido_device.h


### na...@google.com (2020-05-29)

Congrats! The Panel decided to award $20,000 for this report. 

### na...@google.com (2020-05-29)

[Empty comment from Monorail migration]

### ad...@google.com (2020-06-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-02)

[Empty comment from Monorail migration]

### ad...@google.com (2020-06-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-03)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-06-30)

martinkr@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### mm...@chromium.org (2020-07-07)

[Empty comment from Monorail migration]

### aw...@google.com (2020-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1082105?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052296)*

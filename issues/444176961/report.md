# use-after-poison in ContextInvalidationListener

| Field | Value |
|-------|-------|
| **Issue ID** | [444176961](https://issues.chromium.org/issues/444176961) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, ChromeOS |
| **Chrome Version** | 142.0.7405.2 |
| **Reporter** | vm...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2025-09-10 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. load extension poc.zip. (\*\*disable --no-sandbox \*\*; If it does not crash, try several times.)

# Problem Description

In the process of `UnloadExtension` when `extensions::APIBindingsSystem::WillReleaseContext(v8::Local<v8::Context>)` triggers context invalidation. During context invalidation, a `ContextInvalidationListener` attempts to access its base::OnceClosure callback after the callback has already been destroyed, resulting in a use-after-poison error when checking the callback's validity in `OnInvalidated()`.
This indicates a lifetime management issue where the callback object is destroyed before its associated `ContextInvalidationListener`, possibly due to incorrect destruction ordering or missing cleanup mechanisms during context release.

[1](https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/bindings/api_binding_util.h;drc=48d6f7175422b2c969c14258f9f8d5b196c28d18;l=55)
[2](https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/bindings/api_binding_util.cc;drc=48d6f7175422b2c969c14258f9f8d5b196c28d18;l=84)

fix: Ensure `ContextInvalidationListener`  unregisters itself or uses weak pointers to handle callback invalidation safely.

# Summary

use-after-poison in ContextInvalidationListener

# Custom Questions

#### Crash state:

```
=================================================================
==3775476==ERROR: AddressSanitizer: use-after-poison on address 0x7eac00559a58 at pc 0x615e5703021b bp 0x7ffe2d0cbbb0 sp 0x7ffe2d0cbba8
READ of size 8 at 0x7eac00559a58 thread T0 (chrome)
    #0 0x615e5703021a in operator bool base/memory/scoped_refptr.h:319:43
    #1 0x615e5703021a in is_null base/functional/callback_internal.h:140:34
    #2 0x615e5703021a in operator bool base/functional/callback_internal.h:141:44
    #3 0x615e5703021a in operator bool base/functional/callback.h:110:45
    #4 0x615e5703021a in OnInvalidated extensions/renderer/bindings/api_binding_util.cc:167:3
    #5 0x615e5703021a in extensions::binding::ContextInvalidationData::Invalidate() extensions/renderer/bindings/api_binding_util.cc:84:14
    #6 0x615e57036bb7 in extensions::APIBindingsSystem::WillReleaseContext(v8::Local<v8::Context>) extensions/renderer/bindings/api_bindings_system.cc:159:3
    #7 0x615e57138587 in extensions::NativeExtensionBindingsSystem::WillReleaseScriptContext(extensions::ScriptContext*) extensions/renderer/native_extension_bindings_system.cc:525:15
    #8 0x615e570c3ebf in Invoke<void (extensions::NativeExtensionBindingsSystem::*)(extensions::ScriptContext *), extensions::NativeExtensionBindingsSystem *, extensions::ScriptContext *> base/functional/bind_internal.h:730:12
    #9 0x615e570c3ebf in MakeItSo<void (extensions::NativeExtensionBindingsSystem::*const &)(extensions::ScriptContext *), const std::__Cr::tuple<base::internal::UnretainedWrapper<extensions::NativeExtensionBindingsSystem, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, extensions::ScriptContext *> base/functional/bind_internal.h:922:12
    #10 0x615e570c3ebf in RunImpl<void (extensions::NativeExtensionBindingsSystem::*const &)(extensions::ScriptContext *), const std::__Cr::tuple<base::internal::UnretainedWrapper<extensions::NativeExtensionBindingsSystem, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL> base/functional/bind_internal.h:1059:14
    #11 0x615e570c3ebf in base::internal::Invoker<base::internal::FunctorTraits<void (extensions::NativeExtensionBindingsSystem::* const&)(extensions::ScriptContext*), extensions::NativeExtensionBindingsSystem*>, base::internal::BindState<true, true, false, void (extensions::NativeExtensionBindingsSystem::*)(extensions::ScriptContext*), base::internal::UnretainedWrapper<extensions::NativeExtensionBindingsSystem, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (extensions::ScriptContext*)>::Run(base::internal::BindStateBase*, extensions::ScriptContext*) base/functional/bind_internal.h:979:12
    #12 0x615e57175949 in base::RepeatingCallback<void (extensions::ScriptContext*)>::Run(extensions::ScriptContext*) const & base/functional/callback.h:343:12
    #13 0x615e5717520b in ExecuteCallbackWithContext extensions/renderer/script_context_set.cc:202:14
    #14 0x615e5717520b in extensions::ScriptContextSet::ForEach(extensions::mojom::HostID const&, content::RenderFrame*, base::RepeatingCallback<void (extensions::ScriptContext*)> const&) extensions/renderer/script_context_set.cc:175:11
    #15 0x615e570b59a6 in extensions::Dispatcher::UnloadExtension(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&) extensions/renderer/dispatcher.cc:1185:24
    #16 0x615e4e2f1377 in extensions::mojom::RendererStubDispatch::Accept(extensions::mojom::Renderer*, mojo::Message*) gen/extensions/common/mojom/renderer.mojom.cc:2779:13
    #17 0x615e58c0e8a2 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1059:54
    #18 0x615e58c38fbb in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #19 0x615e58c15d88 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:731:20
    #20 0x615e5db96a4f in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ipc/ipc_mojo_bootstrap.cc:1202:24
    #21 0x615e5db9978c in Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> base/functional/bind_internal.h:730:12
    #22 0x615e5db9978c in MakeItSo<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> > base/functional/bind_internal.h:922:12
    #23 0x615e5db9978c in RunImpl<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, 0UL, 1UL, 2UL> base/functional/bind_internal.h:1059:14
    #24 0x615e5db9978c in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:972:12
    #25 0x615e3a86dbe9 in base::OnceCallback<void ()>::Run() && base/functional/callback.h:155:12
    #26 0x615e58f1a527 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:207:34
    #27 0x615e58fd8838 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:474:11)> base/task/common/task_annotator.h:104:5
    #28 0x615e58fd8838 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:472:23
    #29 0x615e58fd6756 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #30 0x615e58fd978a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #31 0x615e58d60e8b in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #32 0x615e58fdacad in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:647:12
    #33 0x615e58e61f2b in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #34 0x615e676787af in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:355:16
    #35 0x615e540becda in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:669:14
    #36 0x615e540c0e4d in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:772:12
    #37 0x615e540c468b in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1129:10
    #38 0x615e540bc3a4 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:346:36
    #39 0x615e540bc93c in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:359:10
    #40 0x615e3a157258 in ChromeMain chrome/app/chrome_main.cc:228:12
    #41 0x704becc2a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #42 0x704becc2a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #43 0x615e3a07a029 in _start (/home/xx/xx/src/chrome/chromium/src/out/asan/chrome+0x27d2d029) (BuildId: 2120e3b077da9166)

Address 0x7eac00559a58 is a wild pointer inside of access range of size 0x000000000008.
SUMMARY: AddressSanitizer: use-after-poison base/memory/scoped_refptr.h:319:43 in operator bool
Shadow bytes around the buggy address:
  0x7eac00559780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7eac00559800: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7eac00559880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7eac00559900: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7eac00559980: 00 00 00 00 00 00 00 00 00 00 00 00 00 f7 f7 f7
=>0x7eac00559a00: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7[f7]f7 f7 f7 f7
  0x7eac00559a80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7eac00559b00: 00 00 00 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7eac00559b80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7eac00559c00: f7 f7 f7 f7 f7 f7 00 00 00 00 00 00 00 00 00 00
  0x7eac00559c80: 00 00 00 00 00 00 00 00 00 00 f7 f7 f7 f7 f7 f7
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

NOTE: the stack trace above identifies the code that *accessed* the poisoned memory.
To identify the code that *poisoned* the memory, try the experimental setting ASAN_OPTIONS=poison_history_size=<size>.

==3775476==ADDITIONAL INFO

==3775476==Note: Please include this section with the ASan report.
Task trace:
    #0 0x615e5db8084c in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ipc/ipc_mojo_bootstrap.cc:1141:13


```
# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [poc.zip](attachments/poc.zip) (application/zip, 9.7 KB)
- [uap.mp4](attachments/uap.mp4) (video/mp4, 2.4 MB)
- [Screencast from 2025年09月23日 15时34分46秒.webm](attachments/Screencast from 2025年09月23日 15时34分46秒.webm) (application/octet-stream, 9.2 MB)
- [Screencast from 2025年09月23日 15时08分32秒.webm](attachments/Screencast from 2025年09月23日 15时08分32秒.webm) (application/octet-stream, 2.5 MB)
- [crashlog_CL](attachments/crashlog_CL) (application/octet-stream, 11.2 KB)
- [manifest.json](attachments/manifest.json) (application/json, 1.5 KB)
- [background.js](attachments/background.js) (text/javascript, 137 B)
- [main.html](attachments/main.html) (text/html, 55 B)
- [main.js](attachments/main.js) (text/javascript, 38.9 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [log-1522585](attachments/log-1522585) (application/octet-stream, 5.4 KB)
- [log-1549553](attachments/log-1549553) (application/octet-stream, 5.4 KB)
- [log-1562390](attachments/log-1562390) (application/octet-stream, 11.9 KB)
- [log-debug-1562437](attachments/log-debug-1562437) (application/octet-stream, 48.1 KB)
- [log-1576996](attachments/log-1576996) (application/octet-stream, 10.4 KB)
- [log-debug-1577024](attachments/log-debug-1577024) (application/octet-stream, 16.5 KB)

## Timeline

### sk...@google.com (2025-09-11)

Hi Devlin! Can you PTAL? I was not able to reproduce on my machine.

### vm...@gmail.com (2025-09-12)

> Hi Devlin! Can you PTAL? I was not able to reproduce on my machine.

I probably have a clue —I can repro it on two versions:

1. Directly `--load-extension` on asan-linux-release-1509401(142.0.7391.0)
2. If u r using a build version(142.0.7405.2), u need to goto `chrome://extensions/` and try to turn on the switch several times.

### pe...@google.com (2025-09-12)

Thank you for providing more feedback. Adding the requester to the CC list.

### pe...@google.com (2025-09-13)

The NextAction date has arrived: 2025-09-13
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### es...@chromium.org (2025-09-17)

Reporter: I can't reproduce this on an asan build of 142.0.7418.0. Is there any more information you can provide to help reproduce? Thanks.

### rd...@chromium.org (2025-09-17)

I also can't reproduce this. And, looking at the code, I don't quite see how this can happen, *assuming* we only invalidate each context once.

- When the context is invalidated, we'll run through the invalidation listeners and run the `on_invalidated_` callback if it's non-null.
- The only time `on_invalidated_` is run is via the context being invalidated.
- The context will be invalidated either by [`ContextInvalidationData`'s dtor](https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/bindings/api_binding_util.cc;l=61-64;drc=48d6f7175422b2c969c14258f9f8d5b196c28d18) (but only if the context is still valid) or by [ContextInvalidationData::Invalidate()](https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/bindings/api_binding_util.cc;l=79-85;drc=48d6f7175422b2c969c14258f9f8d5b196c28d18). Thus, only one of these should trigger. We also have some DCHECKs in place that ensure the context is valid when Invalidate() is being called (i.e., that we haven't called it twice) and we haven't, AFAIK, seen any reports for those failing (this isn't necessarily exhaustive evidence since DCHECKs are disabled for most users).

There is something that's "not great" here, which is that the ContextInvalidationListener [only removes itself](https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/bindings/api_binding_util.cc;l=158-164;drc=48d6f7175422b2c969c14258f9f8d5b196c28d18) as a listener if the context is still valid. This means that, if the context were already invalidated, we'll store a stale pointer in the listeners array. I don't think this causes any issues in practice because:
a) that will only happen if the context is already invalidated, and
b) we only call invalidate again in the dtor of the ContextInvalidationData if the context is still valid. So, there shouldn't be any way for that to trigger a UAF.

I'll still submit a CL to fix that, since it's a code smell and could be unsafe in the future (if we changed code around it), but I don't see how that would lead to a UAF today.

(And, the only place in which we use the ContextInvalidationListener is [here](https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/api/messaging/gin_port.cc;l=51-53;drc=48d6f7175422b2c969c14258f9f8d5b196c28d18), which already uses WeakPtrs, so it's not an issue of the callback itself being unsafe.)

### vm...@gmail.com (2025-09-23)

> Reporter: I can't reproduce this on an asan build of 142.0.7418.0. Is there any more information you can provide to help reproduce? Thanks.

HI, I still can reproduce this issue on Chromium 142.0.7430.0, and I'm uploading 2 ways (1.--load-extension with commandline; 2. goto chrome://extensions/ and try to turn on the switch) of reproducing the process. If you need further help for reproduing, I'm in the UTC+8 time zone, maybe we can set up a remote meeting.

### pe...@google.com (2025-09-23)

Thank you for providing more feedback. Adding the requester to the CC list.

### dx...@google.com (2025-09-23)

Project: chromium/src  

Branch:  main  

Author:  Devlin Cronin [rdevlin.cronin@chromium.org](mailto:rdevlin.cronin@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6961207>

[Extensions] Remove ContextInvalidationListener as listener in all cases

---


Expand for full commit details
```
     
    Currently, a ContextInvalidationListener removes itself as a listener 
    from the ContextInvalidationData only on destruction, and only if the 
    context is still valid. This means that if the context was invalidated 
    and then the listener is destroyed, it won't remove itself as a 
    listener, resulting in a stale pointer being stored in the 
    ContextInvalidationData. 
     
    In practice, this shouldn't be an issue, because we only access those 
    listeners when: 
    * The context is invalidated, or 
    * The ContextInvalidationData is destroyed *and* the context is still 
      valid. 
     
    So, since the only time this happens is when the context was 
    invalidated, this shouldn't be a problem, in practice. But, it's still 
    a code smell, and can be risky if that code ever changed. 
     
    Change this so that the ContextInvalidationListener is also removed 
    on context invalidation. 
     
    Bug: 444176961 
    Change-Id: Ifea756cd0b556401413e14e1ffb7a1829cfcc266 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6961207 
    Reviewed-by: Justin Lulejian <jlulejian@chromium.org> 
    Commit-Queue: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1519450}

```

---

Files:

- M `extensions/renderer/bindings/api_binding_util.cc`

---

Hash: [6791bdbf0a502efd52f761aad907506142cdb105](https://chromiumdash.appspot.com/commit/6791bdbf0a502efd52f761aad907506142cdb105)  

Date: Tue Sep 23 17:28:22 2025


---

### rd...@chromium.org (2025-09-23)

[#comment8](https://issues.chromium.org/issues/444176961#comment8): Can you share the gn args you're building with? And do you ever see this reproduce on a fresh user data dir? (It looks like you run it multiple times with the same dir before it crashes?) And it looks like you're just Ctrl-C killing it if it doesn't crash within a couple seconds; is that right?

Given this corresponds with v8 garbage collection, etc, it's entirely possible this is very timing- and resource-dependent, so we may or may not be able to reproduce on our hardware. And, as described in [#comment7](https://issues.chromium.org/issues/444176961#comment7), I'm not sure there's an exploitable issue (even though there *is* a potential dangling pointer). FWIW, I also have a CL at <https://chromium-review.googlesource.com/c/chromium/src/+/6961207> (just merged) that I think fixes the dangling pointer issue, so it may be worth re-testing with a version that includes that.

### wf...@chromium.org (2025-09-23)

Hi reporter, can you retest with the latest version after <https://chromium-review.googlesource.com/c/chromium/src/+/6961207> and see if you can still reproduce? Thanks!

### vm...@gmail.com (2025-09-24)

[#comment11](https://issues.chromium.org/issues/444176961#comment11): I'm using the release version of `gs://chromium-browser-asan/linux-release/asan-linux-release-1519090` in [#comment8](https://issues.chromium.org/issues/444176961#comment8). Yes, I have cleaned up the `--user-data-dir` as shown in the first video of [#comment8](https://issues.chromium.org/issues/444176961#comment8). I did both cleaned up the `--user-data-dir` and Ctrl-C killing the not reproduced round. And I can reproduce the issue on both my two PCs. Is there any chance you used the poc.zip instead of the `3` dir inside it?(load /path/to/poc/3 directly)

[#comment12](https://issues.chromium.org/issues/444176961#comment12): I've retested the CL but still got the crash. Attaching the crashlog\_CL.

### pe...@google.com (2025-09-24)

Thank you for providing more feedback. Adding the requester to the CC list.

### wf...@chromium.org (2025-09-24)

I think given the reporter has provided yet another stack trace that looks legitimate, despite nobody being able to repro, given reporter's track history of valid bugs, I have to assume this is a real bug, and it's sev-high because it's a renderer use-after-poison. I've left the bug assigned to you, devlin, but feel free to find someone else to look at it.

I am unsure of the regression range here - reporter if you are able to repro and bisect could you take a look to see if you can repro back to Chrome 140? There is a potential for a bisect bonus if you provide useful information here to help us.

### wf...@chromium.org (2025-09-24)

For now I am tagging foundin 140 but this is provisional hopefully the reporter can help us here!

### vm...@gmail.com (2025-09-25)

Yes, I'm able to repro on [Chromium 140.0.7312.0](javascript:void(0);).

### ch...@google.com (2025-09-25)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-10-08)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-23)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### th...@chromium.org (2025-10-23)

[secondary shepherd]

Reporter: Could you please upload the individual files for the POC instead of a zip file?

### vm...@gmail.com (2025-10-24)

```
.
├── background.js
├── js
│   ├── main.html
│   └── main.js
└── manifest.json


```

### th...@chromium.org (2025-10-24)

Thanks! There is a lot going on in main.js. Are you able to provide a minimized POC?

### vm...@gmail.com (2025-10-28)

Yeah, about that,, I normally would provide a minimized POC. The main.js I submitted is actually the minimized version after my attempts. It strikes a balance between size and reliability. I found that any further reduction of the code would compromise the reproducibility, making the issue intermittent and much harder to observe consistently.

### ch...@google.com (2025-11-07)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-10)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### ch...@google.com (2025-11-22)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 59 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ri...@google.com (2025-11-24)

[Secondary Shepherd] reporter@ Looks like the fix ([crrev.com/c/6961207](https://crrev.com/c/6961207)) was landed in M142, which might have rolled out after your last repro. Would you mind trying again with M142 at least.

### vm...@gmail.com (2025-11-25)

deleted

### vm...@gmail.com (2025-11-25)

Sure, the issue is reproducible in both asan-linux-release-1522585(142.0.7444.0) and asan-linux-release-1549553(144.0.7546.0). I am attaching the logs.

### ch...@google.com (2025-12-07)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 74 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### rd...@chromium.org (2025-12-20)

Sorry for the delay here.

I've taken another stab at this. Unfortunately, I'm still unable to reproduce, so it's difficult to verify what's happening. The code itself still seems like it should be safe at the //extensions layer, and it's pretty straightforward:

- A ContextInvalidationListener is notified when a context is invalidated [1](https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/bindings/api_binding_util.cc;l=82-83;drc=a02b50d6acbdb16adbe56ffc4d29935823631126)
- The ContextInvalidationListener is owned by a GinPort (in practice, this is the only consumer) [2](https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/api/messaging/gin_port.h;l=160-161;drc=f0821f47fc30afab8eeae78ea1d689480e0d5f6a)
- The ContextInvalidationListener will add and remove itself as an observer from ContextInvalidationData when it is created / destroyed (can't be a registered listener after it's destroyed) [3](https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/bindings/api_binding_util.cc;l=144-163;drc=a02b50d6acbdb16adbe56ffc4d29935823631126)
- The ContextInvalidationListener clears out its reference to ContextInvalidationData on invalidation, so it doesn't leave a dangling pointer. [4](https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/bindings/api_binding_util.cc;l=173;drc=a02b50d6acbdb16adbe56ffc4d29935823631126)
- The `on_invalidated_` callback is called *only* in OnInvalidated(), and the listener removes itself before invoking it -- so there should never be a use-after-move or use-after-free there. [5](https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/bindings/api_binding_util.cc;l=169-175;drc=a02b50d6acbdb16adbe56ffc4d29935823631126)

The only "weird" bit that still lingers is that we [create an invalidation data on Invalidate()](https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/bindings/api_binding_util.cc;l=120-125;drc=a02b50d6acbdb16adbe56ffc4d29935823631126). This is conceptually strange -- we're associating new data with a context that's about to go away. It *should*, in theory, be safe, because the gin::PerContextData is still around (otherwise, the [creation fails](https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/bindings/get_per_context_data.h;l=20-21;drc=f0821f47fc30afab8eeae78ea1d689480e0d5f6a)), and we're calling this from WillReleaseScriptContext -- i.e., the ScriptContext is still valid at this point. But, it's a bit strange, and there's maybe a chance that something could go awry if the gin::PerContextData is going to be destroyed (or is in the process of being destroyed?).

The reason we create the data in that case is because we consider "no invalidation data" to be [an indication of a valid context](https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/bindings/api_binding_util.cc;l=97;drc=a02b50d6acbdb16adbe56ffc4d29935823631126). As such, if we change that line, any checks that happen in after InvalidateContext() but before gin::PerContextData is cleaned up would be (erroneously) considered valid.

I have a CL that changes this flow by always instantiating an InvalidationData so that we can use its absence as an indication of an invalid context and thus bypass the need to create a new InvalidationData when invalidating the context. That will get rid of that code smell.

I also have a couple CLs that strengthen some of the CHECKs in this area.

Between those, we'll see if it fixes anything. I can't promise it will, since we've still been unable to reproduce locally. But, worth a shot.

### dx...@google.com (2025-12-22)

Project: chromium/src  

Branch:  main  

Author:  Devlin Cronin [rdevlin.cronin@chromium.org](mailto:rdevlin.cronin@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7281900>

[Extensions Bindings] Don't create invalidation data when invalidating

---


Expand for full commit details
```
     
    We track whether a given context is valid via an "invalidation data" 
    that's stored on the context via gin::PerContextData. Today, we lazily 
    create this data, and consider a context valid if it either has no 
    invalidation data or the invalidation data indicates the context is 
    still valid. 
     
    Unfortunately, because we consider "no invalidation data" (but still 
    gin::PerContextData) to be an indication of a valid state, we need to 
    *create* an invalidation data in InvalidateContext() if one hasn't 
    already been made. This is a bit weird, since we're adding a new 
    PerContextData to a context as it's being cleaned up. 
     
    Fix this code smell by always instantiating a ContextInvalidationData 
    entry for each new context. This way, we don't have to create a new 
    one during the context invalidation flow, and can treat absence of 
    invalidation data as a signal of an invalid context. 
     
    Bug: 444176961 
    Change-Id: I717e7dd74f3e0ef8b78a36a839174360a3b57a7f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7281900 
    Commit-Queue: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Reviewed-by: Tim <tjudkins@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1562006}

```

---

Files:

- M `extensions/renderer/bindings/api_binding_test.cc`
- M `extensions/renderer/bindings/api_binding_util.cc`
- M `extensions/renderer/bindings/api_binding_util.h`
- M `extensions/renderer/bindings/api_bindings_system.cc`
- M `extensions/renderer/bindings/api_bindings_system.h`
- M `extensions/renderer/native_extension_bindings_system.cc`

---

Hash: [5ec924bc3b4a65cd06fbb8385d6b2563d60c8197](https://chromiumdash.appspot.com/commit/5ec924bc3b4a65cd06fbb8385d6b2563d60c8197)  

Date: Mon Dec 22 23:19:35 2025


---

### dx...@google.com (2025-12-23)

Project: chromium/src  

Branch:  main  

Author:  Devlin Cronin [rdevlin.cronin@chromium.org](mailto:rdevlin.cronin@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7281715>

[Extensions Bindings] Upgrade a few DCHECKs to CHECKs

---


Expand for full commit details
```
     
    Upgrade some DCHECKs into CHECKs when dealing with context validity. 
     
    Bug: 444176961 
    Change-Id: Ib8827b02fe4293b013e2e8e7a28e2b76e242c1be 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7281715 
    Reviewed-by: Tim <tjudkins@chromium.org> 
    Commit-Queue: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1562022}

```

---

Files:

- M `extensions/renderer/bindings/api_binding_util.cc`

---

Hash: [5c577b0b78eccfeeca7c3a16da5b3f71962a82a6](https://chromiumdash.appspot.com/commit/5c577b0b78eccfeeca7c3a16da5b3f71962a82a6)  

Date: Tue Dec 23 00:22:36 2025


---

### dx...@google.com (2025-12-23)

Project: chromium/src  

Branch:  main  

Author:  Devlin Cronin [rdevlin.cronin@chromium.org](mailto:rdevlin.cronin@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7281997>

[Extensions Bindings] Make ContextInvalidationListeners Checked

---


Expand for full commit details
```
     
    Make ContextInvalidationListeners base::CheckedObservers for increased 
    safety. 
     
    Bug: 444176961 
    Change-Id: I753dd98107bd19b681b821cc8c7de0b7bc805134 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7281997 
    Reviewed-by: Tim <tjudkins@chromium.org> 
    Commit-Queue: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1562024}

```

---

Files:

- M `extensions/renderer/bindings/api_binding_util.cc`
- M `extensions/renderer/bindings/api_binding_util.h`

---

Hash: [d0bdcb90e4ca7869021910a36f77529aa8eec6c2](https://chromiumdash.appspot.com/commit/d0bdcb90e4ca7869021910a36f77529aa8eec6c2)  

Date: Tue Dec 23 00:34:25 2025


---

### rd...@chromium.org (2025-12-23)

The patches from [#comment32](https://issues.chromium.org/issues/444176961#comment32) have landed. I'll monitor to see if any of the newly-added CHECKs trigger (which would signal an issue). OP, if you can also test in a day or two (with a version higher than 145.0.7594.0), that would be great. Since none of us are able to repro (still unclear why), it's difficult for me to say if it's fixed.

Thank you for your patience!

### vm...@gmail.com (2025-12-24)

I've tested on 2 versions, a release(145.0.7596.0) and a debug(145.0.7597.0). It seems that the added CHECK did not trigger. The issue remains detectable by addresssanitizer, attaching logs.

### ch...@google.com (2026-01-07)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### vm...@gmail.com (2026-01-21)

deleted

### ch...@google.com (2026-01-22)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### rd...@chromium.org (2026-01-30)

Thanks for your continued patience.

- We've fixed a few other issues in the area that touch some related code. Unfortunately, since we've never been able to reproduce this on our end, we still can't verify. Can you try running one more time on the latest Chromium revisions?
- I have one final path I can explore tomorrow.

### vm...@gmail.com (2026-01-30)

I have tested it on the 2 latest versions. Logs attached.

### rd...@chromium.org (2026-02-03)

I've continued to look into this, but I'm not sure we're any closer to a solution.

I was finally able to, very sporadically, reproduce this and add some logs. But they are quite strange.

- The immediate trigger of the crash is that accessing the callback within invalidation listener fails. Interestingly, this is *any* access to the callback, not just *running* the callback. The first trigger is actually part of the DCHECK [here](https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/bindings/api_binding_util.cc;l=180;drc=1d1fcea6ebbc1c2c3d04ab5538c74f742c66444f) -- the DCHECK doesn't fail because even triggering that call is enough to cause the use-after-poison.
- With further testing, it looks like the whole ContextInvalidationListener is poisoned. Adding additional sentinel members and trying to access them triggers a similar crash.

This would all make sense, except... The ContextInvalidationListener is never destructed.

In the repro, there's only a single ContextInvalidationListener constructed for a single GinPort associated with the JS context for the extension's HTML page (not for the extension's background service worker). In the test, the extension gets unloaded, which triggers the destruction of its various JS contexts. The service worker context exits cleanly. The HTML context occasionally triggers the use-after-poison.

The main difference between when the use-after-poison occurs and when it does not appears to be whether the GinPort is destructed prior to context invalidation. If it is destructed, the ContextInvalidationListener is removed, and there is no crash. If it's not destructed, the use-after-poison occurs. This is interesting, because the extensions code here can accommodate either case.

It's not clear to me why the ContextInvalidationListener would be poisoned when the GinPort (which owns it) is not invalidated. I've verified that neither the dtor for the GinPort nor for the ContextInvalidationObserver have been called -- at least, as much as I can verify with a local build and logs.

There are a few situations in which this could theoretically happen:

1. There's a bug in ASAN's poisoning. This is possible, but it seems unlikely.
2. Something is trampling over the memory -- e.g., writing over arbitrary bytes and then they subsequently get poisoned. The GinPort's dtor doesn't get invoked because it wasn't freed, but the memory is otherwise poisoned by a different object that has occupied the same space. As above, I think this is relatively unlikely.
3. The memory associated with the ContextInvalidationListener is getting poisoned in another way. The most likely here seems to be if it were to be std::move()d or similar. This would result in the object never being destroyed, but the references to it in the ObserverList being unsafe (since they're stored by address). This would explain it, but...
   a) The use of the `context_invalidation_listener_` in GinPort is very sparse. It's never referenced outside of the ctor.
   b) I can't *see* anywhere where GinPort would be moved, and it doesn't supply a move constructor.
4. Something else?

jbroman@, I'm curious, do you have insights on whether 3) may somehow be happening? The GinPort is a gin::Wrappable<>, and I know we do strange things with that memory management...

### aj...@google.com (2026-02-03)

In one of the dupes I noted that this CL might have been related but I don't remember why - <https://chromium-review.googlesource.com/c/chromium/src/+/6961207>

### rd...@chromium.org (2026-02-03)

@ [#comment44](https://issues.chromium.org/issues/444176961#comment44): That was a CL that landed for this bug -- it was one of the early attempts to ensure the invalidation listeners were very deterministic and safe. It didn't solve the issue, though.

### rd...@chromium.org (2026-02-03)

It might also be helpful to figure out what the trace for poisoning the memory is, since the destructors for the objects are never invoked. This is theoretically possible, as noted in the ASAN output:

```
NOTE: the stack trace above identifies the code that *accessed* the poisoned memory.
To identify the code that *poisoned* the memory, try the experimental setting ASAN_OPTIONS=poison_history_size=<size>.

```

I tried using this on a local build, but I was unable to reproduce when I did. OP, any chance you're able to repro with that ASAN option? (Unfortunately, as well, it's not clear what size we'd need -- I think that refers to the size of the record, rather than the size of the memory, and we don't know how far back we'd need to go for the poisoning...)

### rd...@chromium.org (2026-02-03)

jbroman@ is busy, but maybe cbruni@ or ahaas@ have ideas? (Please see [comment#43](https://issues.chromium.org/issues/444176961#comment43))

### ah...@google.com (2026-02-04)

I believe I’ve identified the root cause of the crash. Since `GinPort` is an Oilpan-managed object, memory poisoning behaves differently than standard heap objects: the memory is poisoned as soon as the GC detects the object is unreachable, which occurs *prior* to the execution of the destructor.

Because `ContextInvalidationListener` is a member of `GinPort`, it is also managed by Oilpan. The pointer from `ContextInvalidationObserver` to the listener is not tracked by Oilpan; therefore, the memory is marked as unreachable and poisoned while that pointer is still active.

I have uploaded a fix at <https://crrev.com/c/7544878>.

The fix introduces a **prefinalizer** for `GinPort` to explicitly remove the `ContextInvalidationListener` from the `ContextInvalidationObserver` once the `GinPort` is detected as unreachable. This ensures the listener is no longer accessed after the memory has been poisoned.

I suspect this issue was introduced in <https://crrev.com/c/6734711>.

### rd...@chromium.org (2026-02-04)

Thank you for the analysis, @ahaas! That definitely explains it.

I'm curious, though -- is that desirable behavior? From a C++ memory safety perspective, it seems like this can lead to false positives (and it *seems* like that's the case here?). Even though the object is unreachable according to JS's GC, the C++ object is still valid, and thus accessing it's memory seems like it should still be (fundamentally) safe -- or does Oilpan immediately mark that memory as available for use in allocation of new objects?

(I'm curious, as well, how things like non-trivial destructors would work in this case -- if the memory is marked as poisoned, would an object's destructor that accesses its own members be considered a use-after-poison?)

### rd...@chromium.org (2026-02-04)

I'm also curious if this means it's likely an issue with other gin::Wrappables that we use in extension bindings -- there are a [decent number of them](https://source.chromium.org/search?q=%22public%20gin::wrappable%22%20f:extensions&sq=), none of which use things like Persistent<> or Member<> (can we even use those outside of blink?). Historically, I thought the old gin::Wrappable worked with these approaches, so this seems like something where we need to do work on each of these to ensure they are safe, if the memory poisoning *does* correspond to the point at which it is unsafe to use the object?

### dc...@chromium.org (2026-02-04)

> I'm curious, though -- is that desirable behavior? From a C++ memory safety perspective, it seems like this can lead to false positives (and it seems like that's the case here?). Even though the object is unreachable according to JS's GC, the C++ object is still valid, and thus accessing it's memory seems like it should still be (fundamentally) safe -- or does Oilpan immediately mark that memory as available for use in allocation of new objects?

Yes, the poisoning is intended behavior: once Oilpan finishes sweeping, all unreachable objects are *immediately* poisoned.

> (I'm curious, as well, how things like non-trivial destructors would work in this case -- if the memory is marked as poisoned, would an object's destructor that accesses its own members be considered a use-after-poison?)

When finalizers/destructors run, Oilpan temporarily unpoisons the object that is being finalized; however, finalization order is **non-deterministic**, and thus, it is a logical error to touch another Oilpan object in a destructor–any other Oilpan object may very well have been destroyed already.

You are technically correct that from a strict C++ perspective, the object is not destroyed, so there is no theoretical unsoundness to accessing the object's fields. However, it's very difficult to exist in such a state correctly–an object that is no longer reachable must stay that way, and if C++ code is using the poisoned object, it is very easy to accidentally end up in a state where a dead object ends up becoming reachable again–which would definitely cause memory safety issues.

### dx...@google.com (2026-02-04)

Project: chromium/src  

Branch:  main  

Author:  Andreas Haas [ahaas@chromium.org](mailto:ahaas@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7544878>

Migrate GinPort to use CppGC prefinalizers

---


Expand for full commit details
```
     
    GinPort is an Oilpan object, and as such, pointers to GinPort objects 
    should either be stored on the stack, where stack scanning finds them, 
    or in other Oilpan objects as Member<>, or as Persistent<>. If other 
    pointers point to GinPort objects, then these pointers have to be 
    invalidated latest in the GinPort prefinalizer. 
     
    GinPort, however, has a member of type ContextInvalidationListener, and 
    a pointer to that member is stored in a list of an observer. Since this 
    pointer is not known to Oilpan, it has to be invalidated. 
     
    This CL introduces a prefinalizer for GinPort that invalidates the 
    pointer to the ContextInvalidationListener in the list of its observer. 
     
    Bug: 444176961 
     
    Change-Id: I7011608df676cbb6339122134c6a07caac3bfbaa 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7544878 
    Commit-Queue: Andreas Haas <ahaas@chromium.org> 
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1579592}

```

---

Files:

- M `extensions/renderer/api/messaging/gin_port.cc`
- M `extensions/renderer/api/messaging/gin_port.h`
- M `extensions/renderer/bindings/api_binding_util.cc`
- M `extensions/renderer/bindings/api_binding_util.h`

---

Hash: [f5f5ddd31bdda07acf711c2929e2213bd2b7c182](https://chromiumdash.appspot.com/commit/f5f5ddd31bdda07acf711c2929e2213bd2b7c182)  

Date: Wed Feb 4 18:42:09 2026


---

### vm...@gmail.com (2026-02-06)

I've checked on two machines with version 146.0.7673.0 and can confirm the issue has been fixed. The CL works fine!

### rd...@chromium.org (2026-02-07)

Marking as fixed per [#comment52](https://issues.chromium.org/issues/444176961#comment52) and [#comment53](https://issues.chromium.org/issues/444176961#comment53). Thank you so much for all your patience and vigilance, OP! : )

### ch...@google.com (2026-02-07)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### rd...@chromium.org (2026-02-07)

I'm going to indicate "fixed by" all the CLs here, since some did affect lifetime in non-trivial ways and there might be merge conflicts.

### ch...@google.com (2026-02-07)

Security Merge Request Consideration: Requesting merge to stable (M144) because latest trunk commit (1579592) appears to be after stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to beta (M145) because latest trunk commit (1579592) appears to be after beta branch point (1568190).
Security Merge Request - Manual Review: Merge review required: M144 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M145 has already been cut for stable release.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144, 145].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-02-09)

I don't think we should merge this back. There are lots of small changes here which bear new stability risk, and this security bug seems to be exceptionally hard to reproduce and require a malicious extension. Rejecting the merges, but let me know if you disagree.

### dr...@chromium.org (2026-02-10)

It was pointed out to me offline that only <https://crrev.com/c/7544878> would need merge to M145, but we'd need the last four CLs in M144. I do still think the difficult reproducibility means it's not worth the merge to M145.

### sp...@google.com (2026-02-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Moderately mitigated (sandboxed) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### vm...@gmail.com (2026-03-12)

deleted

### vm...@gmail.com (2026-03-12)

deleted

### ch...@google.com (2026-05-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Moderately mitigated (sandboxed)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/444176961)*

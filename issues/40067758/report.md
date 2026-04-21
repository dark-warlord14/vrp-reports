# Security: Heap-use-after-free in HostResolverManager::Job::RunNextTask

| Field | Value |
|-------|-------|
| **Issue ID** | [40067758](https://issues.chromium.org/issues/40067758) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>DNS |
| **Platforms** | Android, Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2023-07-20 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. apply change.txt and compile chromium with ASAN
2. run `./chrome --user-data-dir=/tmp/noexist --no-sandbox`

This is a security bug in Network Service.  

The number in `change.txt` is obtained from `out/Debug/gen/services/network/public/mojom/system_dns_resolution.mojom-shared-message-ids.h` : `constexpr uint32_t kSystemDnsResolver_Resolve_Name = 1329788779;`. Please modify it according to your code repository.

**Problem Description:**  

Details are in Addition Comment.

**Additional Comments:**

1. Analysis

In some situations, `Schedule`[1] may delete `this`, which can lead to UAF when accessing member `resolver_` in `this` afterward.

```
  void RunNextTask() {  
    [...]  
    // Schedule insecure DnsTasks and HostResolverSystemTasks with the  
    // dispatcher.  
    if (!dispatched_ &&  
        (next_task == TaskType::DNS || next_task == TaskType::SYSTEM ||  
         next_task == TaskType::MDNS)) {  
      dispatched_ = true;  
      job_running_ = false;  
      Schedule(false);   // `Schedule` may delete `this` in some conditions.  
      DCHECK(is_running() || is_queued());  
  
      // Check for queue overflow.  
      PrioritizedDispatcher& dispatcher = \*resolver_->dispatcher_;  // Use of member `resolver_` will cause UAF  
      if (dispatcher.num_queued_jobs() > resolver_->max_queued_jobs_) {  
        Job\* evicted = static_cast<Job\*>(dispatcher.EvictOldestLowest());  
        DCHECK(evicted);  
        evicted->OnEvicted();  
      }  
      return;  
    }  
    [...]  
  }  

```

According to the ASAN log, we could get the following call stack: `Schedule` => `PrioritizedDispatcher::Add` => `PrioritizedDispatcher::Job::Start` => `RunNextTask` => `StartSystemTask` => `HostResolverSystemTask::Start` => `HostResolverSystemTask::StartLookupAttempt`[2]

`Schedule` will call `RunNextTask` again but `RunNextTask` will call `StartSystemTask`[2] this time. And finally it will call `HostResolverSystemTask::StartLookupAttempt`[2]. `HostResolverSystemTask::StartLookupAttempt` invokes the callback returned by `GetSystemDnsResolverOverride()`[3].

```
void HostResolverSystemTask::StartLookupAttempt() {  
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);  
  DCHECK(!was_completed());  
  ++attempt_number_;  
  
  net_log_.AddEventWithIntParams(  
      NetLogEventType::HOST_RESOLVER_MANAGER_ATTEMPT_STARTED, "attempt_number",  
      attempt_number_);  
  
  // If the results aren't received within a given time, RetryIfNotComplete  
  // will start a new attempt if none of the outstanding attempts have  
  // completed yet.  
  // Use a WeakPtr to avoid keeping the HostResolverSystemTask alive after  
  // completion or cancellation.  
  if (attempt_number_ <= params_.max_retry_attempts) {  
    base::SequencedTaskRunner::GetCurrentDefault()->PostDelayedTask(  
        FROM_HERE,  
        base::BindOnce(&HostResolverSystemTask::StartLookupAttempt,  
                       weak_ptr_factory_.GetWeakPtr()),  
        params_.unresponsive_delay \*  
            std::pow(params_.retry_factor, attempt_number_ - 1));  
  }  
  
  auto lookup_complete_cb =  
      base::BindOnce(&HostResolverSystemTask::OnLookupComplete,  
                     weak_ptr_factory_.GetWeakPtr(), attempt_number_);  
  
  // If a hook has been installed, call it instead of posting a resolution task  
  // to a worker thread.  
  if (GetSystemDnsResolverOverride()) {  
    GetSystemDnsResolverOverride().Run(hostname_, address_family_, flags_,   //  code goes here  
                                       std::move(lookup_complete_cb), network_);  
    // Do not add code below. `lookup_complete_cb` may have already deleted  
    // `this`.  
  } else {  
    base::OnceCallback<int(AddressList \* addrlist, int\* os_error)> resolve_cb =  
        base::BindOnce(&ResolveOnWorkerThread, params_.resolver_proc, hostname_,  
                       address_family_, flags_, network_);  
    PostSystemDnsResolutionTaskAndReply(std::move(resolve_cb),  
                                        std::move(lookup_complete_cb));  
  }  
}  

```
```
SystemDnsResolverOverrideCallback& GetSystemDnsResolverOverride() {  
  static base::NoDestructor<SystemDnsResolverOverrideCallback> dns_override;  
  
#if DCHECK_IS_ON()  
  if (\*dns_override) {  
    // This should only be called on the main thread, so DCHECK that it is.  
    // However, in unittests this may be called on different task environments  
    // in the same process so only bother sequence checking if an override  
    // exists.  
    static base::NoDestructor<base::SequenceCheckerImpl> sequence_checker;  
    base::ScopedValidateSequenceChecker scoped_validated_sequence_checker(  
        \*sequence_checker);  
  }  
#endif  
  
  return \*dns_override;  
}  

```

After exploring the reference, we could find that this callback is set here[4]: `base::BindRepeating(ResolveSystemDnsWithMojo, std::move(system_dns_override))`, so the callback is `ResolveSystemDnsWithMojo`[5].

`ResolveSystemDnsWithMojo` will send a mojo request to the browser with a `results_cb_with_default_invoke`. `results_cb_with_default_invoke` is a callback of type `mojo::WrapCallbackWithDefaultInvokeIfNotRun`, which means if `results_cb_with_default_invoke` is destructed before it has a change to run, it will be run with the default argument immediately!

```
void NetworkService::SetSystemDnsResolver(  
    mojo::PendingRemote<mojom::SystemDnsResolver> override_remote) {  
  CHECK(override_remote);  
  
  // Using a Remote (as opposed to a SharedRemote) is fine as system host  
  // resolver overrides should only be invoked on the main thread.  
  mojo::Remote<mojom::SystemDnsResolver> system_dns_override(  
      std::move(override_remote));  
  
  // Note that if this override replaces a currently existing override, it wil  
  // destruct the Remote<mojom::SystemDnsResolver> owned by the other override,  
  // which will cancel all ongoing DNS resolutions.  
  net::SetSystemDnsResolverOverride(base::BindRepeating(  // callback is set here  
      ResolveSystemDnsWithMojo, std::move(system_dns_override)));  
}  

```
```
void ResolveSystemDnsWithMojo(  
    const mojo::Remote<mojom::SystemDnsResolver>& system_dns_override,  
    const absl::optional<std::string>& hostname,  
    net::AddressFamily addr_family,  
    net::HostResolverFlags flags,  
    net::SystemDnsResultsCallback results_cb,  
    net::handles::NetworkHandle network) {  
  auto results_cb_with_default_invoke =  
      mojo::WrapCallbackWithDefaultInvokeIfNotRun(  
          std::move(results_cb), net::AddressList(), 0,  
          net::ERR_DNS_REQUEST_CANCELLED);  
  system_dns_override->Resolve(hostname, addr_family, flags, network,  
                               std::move(results_cb_with_default_invoke));  
}  

```

Normally, the `results_cb_with_default_invoke` will run after the browser endpoint replies to the NetworkService endpoint[6]. However, if we could destruct the `results_cb_with_default_invoke` before mojo request is sent, it will run directly. In other words, the execution order of this callback is advanced.  

There are two if conditions that could terminate `SendMessageWithResponder` before callback is moved, callback will be destructed if either of these two conditions is met. However, I haven't found a stable method to make this mojo interface return early, so I made some modifications. I determine whether to terminate this function early based on the name of the interface. You can see the `change.txt` for more info.

Finally, the callback invoked is `HostResolverSystemTask::OnLookupComplete` which is set by [2], and this callback will call: `OnSystemTaskComplete` => `CompleteRequests` => `RemoveJob` => delete `HostResolverManager::Job`.

```
bool InterfaceEndpointClient::SendMessageWithResponder(  
    Message\* message,  
    bool is_control_message,  
    SyncSendMode sync_send_mode,  
    std::unique_ptr<MessageReceiver> responder) {  
  CHECK(sequence_checker_.CalledOnValidSequence());  
  DCHECK(message->has_flag(Message::kFlagExpectsResponse));  
  DCHECK(!handle_.pending_association());  
  
  // Please see comments in Accept().  
  message->SerializeHandles(handle_.group_controller());  
  
  if (encountered_error_)  
    return false;  
  
  InitControllerIfNecessary();  
  
  // Reserve 0 in case we want it to convey special meaning in the future.  
  uint64_t request_id = next_request_id_++;  
  if (request_id == 0)  
    request_id = next_request_id_++;  
  
  message->set_request_id(request_id);  
  message->set_heap_profiler_tag(interface_name_);  
  
#if DCHECK_IS_ON()  
  // TODO(https://crbug.com/695289): Send |next_call_location_| in a control  
  // message before calling |SendMessage()| below.  
#endif  
  
  const uint32_t message_name = message->name();  
  const bool is_sync = message->has_flag(Message::kFlagIsSync);  
  const bool exclusive_wait =  
      message->has_flag(Message::kFlagNoInterrupt) ||  
      !SyncCallRestrictions::AreSyncCallInterruptsEnabled();  
  if (!controller_->SendMessage(message))  
    return false;  
  
  if (!is_control_message && idle_handler_)  
    ++num_unacked_messages_;  
  
  if (!is_sync || sync_send_mode == SyncSendMode::kForceAsync) {  
    if (is_sync) {  
      // This was forced to send async. Leave a placeholder in the map of  
      // expected sync responses so HandleValidatedMessage knows what to do.  
      sync_responses_.emplace(request_id, nullptr);  
      controller_->RegisterExternalSyncWaiter(request_id);  
    }  
    base::AutoLock lock(async_responders_lock_);  
    async_responders_.emplace(  
        request_id, PendingAsyncResponse{message_name, std::move(responder)});  
    return true;  
  }  
  
  SyncCallRestrictions::AssertSyncCallAllowed();  
  
  bool response_received = false;  
  sync_responses_.insert(std::make_pair(  
      request_id,  
      std::make_unique<SyncResponseInfo>(message_name, &response_received)));  
  
  base::WeakPtr<InterfaceEndpointClient> weak_self =  
      weak_ptr_factory_.GetWeakPtr();  
  if (exclusive_wait)  
    controller_->SyncWatchExclusive(request_id);  
  else  
    controller_->SyncWatch(response_received);  
  // Make sure that this instance hasn't been destroyed.  
  if (weak_self) {  
    DCHECK(base::Contains(sync_responses_, request_id));  
    auto iter = sync_responses_.find(request_id);  
    DCHECK_EQ(&response_received, iter->second->response_received);  
    if (response_received) {  
      std::ignore = responder->Accept(&iter->second->response);  
    } else {  
      DVLOG(1) << "Mojo sync call returns without receiving a response. "  
               << "Typcially it is because the interface has been "  
               << "disconnected.";  
    }  
    sync_responses_.erase(iter);  
  }  
  
  return true;  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:net/dns/host_resolver_manager.cc;l=2226;bpv=1;bpt=0;drc=9898b305169043c301f56acb4fa983579cd88ed7>  

[2] <https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:net/dns/host_resolver_system_task.cc;l=288;drc=402a9900e908141c002ac4fb1272a184b7c48978;bpv=1;bpt=0>  

[3] <https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:net/dns/host_resolver_system_task.cc;l=145;drc=402a9900e908141c002ac4fb1272a184b7c48978;bpv=0;bpt=0>  

[4] <https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:services/network/network_service.cc;l=597;drc=89fb0c37cd7eaac09a9ec102d1d83696e1c39f96;bpv=1;bpt=0>  

[5] <https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:services/network/network_service.cc;l=232;drc=89fb0c37cd7eaac09a9ec102d1d83696e1c39f96;bpv=1;bpt=0>  

[6] <https://source.chromium.org/chromium/chromium/src/+/main:mojo/public/cpp/bindings/lib/interface_endpoint_client.cc;l=609;drc=db49c3af22fbc8e4020c2b619a4eb262c6e58303;bpv=0;bpt=0>

2. Bisect

The vulnerability-related code was introduced in this commit.: c682ba3c41e0e5b554e82d10b395fb8c9cb64163  

<https://chromium-review.googlesource.com/c/chromium/src/+/1754187>

This bug affects Chrome Stable, Dev, Beta and Canary.

3. Suggested Patch

After calling `Schedule`, check if `this` is still alive.

```
diff --git a/net/dns/host_resolver_manager.cc b/net/dns/host_resolver_manager.cc  
index 5318e289e60e5..662ff7c0388e7 100644  
--- a/net/dns/host_resolver_manager.cc  
+++ b/net/dns/host_resolver_manager.cc  
@@ -2215,7 +2215,10 @@ class HostResolverManager::Job : public PrioritizedDispatcher::Job,  
          next_task == TaskType::MDNS)) {  
       dispatched_ = true;  
       job_running_ = false;  
+base::WeakPtr<Job> weak_ptr = weak_ptr_factory_.GetWeakPtr();  
       Schedule(false);  
+if(!weak_ptr)  
+    return;  
       DCHECK(is_running() || is_queued());  
   
       // Check for queue overflow.  

```

\*\*Chrome version: \*\* \*\*Channel: \*\* Stable

**OS:** Linux

## Attachments

- [change.txt](attachments/change.txt) (text/plain, 632 B)
- [asan.txt](attachments/asan.txt) (text/plain, 35.7 KB)
- [suggested_patch.txt](attachments/suggested_patch.txt) (text/plain, 588 B)
- [video.webm](attachments/video.webm) (video/webm, 924.6 KB)
- [1.png](attachments/1.png) (image/png, 25.8 KB)
- [video1.webm](attachments/video1.webm) (video/webm, 378.7 KB)

## Timeline

### [Deleted User] (2023-07-20)

[Empty comment from Monorail migration]

### rs...@chromium.org (2023-07-20)

I am not able to reproduce this:

==========
% git log -1 --oneline
a386629e602a2 (HEAD, origin/main, origin/HEAD) Roll bindgen 078fb77e82507c..97e29b49bebaba4d0

% cat out/linux-asan/args.gn   
dcheck_always_on = true
is_asan = true
is_component_build = false
is_debug = false
is_lsan = true
symbol_level = 1

% tail -7 out/linux-asan/gen/services/network/public/mojom/system_dns_resolution.mojom-shared-message-ids.h
constexpr uint32_t kSystemDnsResolver_Resolve_Name = 1132538028;

}  // namespace internal
}  // namespace mojom
}  // namespace network

#endif  // SERVICES_NETWORK_PUBLIC_MOJOM_SYSTEM_DNS_RESOLUTION_MOJOM_SHARED_MESSAGE_IDS_H_

% git diff
diff --git a/mojo/public/cpp/bindings/lib/interface_endpoint_client.cc b/mojo/public/cpp/bindings/lib/interface_endpoint_client.cc
index 7e4d699df3e8a..322d75cb6ed53 100644
--- a/mojo/public/cpp/bindings/lib/interface_endpoint_client.cc
+++ b/mojo/public/cpp/bindings/lib/interface_endpoint_client.cc
@@ -644,6 +644,10 @@ bool InterfaceEndpointClient::SendMessageWithResponder(
   if (!controller_->SendMessage(message))
     return false;
 
+  if (message_name == 1132538028) {
+    return false;
+  }
+
   if (!is_control_message && idle_handler_)
     ++num_unacked_messages_;
 
==========

I ran Chrome with the change applied as described in the report and demonstrated above but did not observe any crash.

It is also unclear to me what condition this applied patch is meant to replicate. It looks like it is causing the SystemDnsResolver.Resolve message to fail to be sent to the browser, but that seems like an impossible condition. Could you please elaborate on the purpose of the patch?

### me...@gmail.com (2023-07-21)

If you cannot reproduce it, please set your system's proxy to 'automate', It appears that function `StartSystemTask` will only be called in this particular situation, but I don't figure out the reason.

> It is also unclear to me what condition this applied patch is meant to replicate. It looks like it is causing the SystemDnsResolver.Resolve message to fail to be sent to the browser, but that seems like an impossible condition. 

Yes, it is a rare condition, and I have only encountered it once by chance during the fuzzing process. Therefore, I can only simulate this situation through the patch.


> Could you please elaborate on the purpose of the patch?

As I mentioned in https://crbug.com/chromium/1466415#c1, the purpose of this patch is to make the `InterfaceEndpointClient::SendMessageWithResponder` function return early, thereby destructing the `mojo::WrapCallbackWithDefaultInvokeIfNotRun` callback. Since this callback is moved into the `InterfaceEndpointClient::SendMessageWithResponder` function, if the `InterfaceEndpointClient::SendMessageWithResponder` function ends without performing any operations on the callback (like move callback to other function), the callback will also be destructed.

The `WrapCallbackWithDefaultInvokeIfNotRun` callback will run directly if it is destructed before it has a chance to run, so the callback will run directly rather than waiting for the reply of MOJO and run. 
The comments in the following code perfectly illustrate the impact of running this callback early. `this` will be released directly instead of waiting until the current function is executed done.


```[1]
  void RunNextTask() {
    [...]
    // Schedule insecure DnsTasks and HostResolverSystemTasks with the
    // dispatcher.
    if (!dispatched_ &&
        (next_task == TaskType::DNS || next_task == TaskType::SYSTEM ||
         next_task == TaskType::MDNS)) {
      dispatched_ = true;
      job_running_ = false;
      Schedule(false);   // `Schedule` will directly run the `mojo::WrapCallbackWithDefaultInvokeIfNotRun` callback, which will delete `this`.
      DCHECK(is_running() || is_queued());

      // Check for queue overflow.
      PrioritizedDispatcher& dispatcher = *resolver_->dispatcher_;  // Use of member `resolver` of `this` will cause UAF
      if (dispatcher.num_queued_jobs() > resolver_->max_queued_jobs_) {
        Job* evicted = static_cast<Job*>(dispatcher.EvictOldestLowest());
        DCHECK(evicted);
        evicted->OnEvicted();
      }
      return;
    }
    [...]
  }
```

### fl...@google.com (2023-07-21)

Thank you for explaining your patch further.

I've also tried to reproduce this without success.  Can you explain what exactly you mean by the suggestion to "set your system's proxy to 'automate'"?  Is this a Chrome setting, a gn setting, something else, how can I set it this way?

### me...@gmail.com (2023-07-21)

Oh I’m sorry. It’s a Ubuntu system’s setting. You need to change your operating system’s proxy:)

### fl...@google.com (2023-07-25)

I am on Ubuntu and the network proxy setting is already set to Automate.  Do you have any other ideas on how to reproduce this?  Or perhaps a simplified PoC (I'm a little worried the bug might be introduced by that kernel patch, rather than the ?  It'll be difficult to proceed unless we can reproduce.

### me...@gmail.com (2023-07-25)

I don't know why you can't reproduce it on your machine. I can easily reproduce this issue on my virtual machine using the patch, and according to the ASAN (AddressSanitizer) log, the vulnerability does indeed occur as described. And the patch is just to simulate a broken mojo request in browser side, the UAF occurs in network service.

### me...@gmail.com (2023-07-25)

In my virtual machine, after applying the above-mentioned patch, if the system proxy is set to automatic, this vulnerability will be triggered immediately.
And, here is my vm's configuration:

Distributor ID:	Ubuntu
Description:	Ubuntu 20.04.5 LTS
Release:	20.04
Codename:	focal
Linux ubuntu 5.15.0-56-generic #62~20.04.1-Ubuntu SMP Tue Nov 22 21:24:20 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux


### ma...@google.com (2023-07-27)

Even if this repros, the current patch blocks IPC from the network utility process to the browser process. Unless there is a way to make this trigger externally that doesn't already involve control of the browser process, then I don't think there is a security issue here. 

There may well be a bug here though, so reeling in component owners. 

DNS owners, could you PTAL? Any opinion on whether there is a security relevant issue here?

[Monorail components: Internals>Network>DNS]

### ad...@google.com (2023-07-27)

(I am a bot: this is an auto-cc on a security bug)

### ho...@chromium.org (2023-07-28)

mpdenton@
Could you please handle this issue?
I think it looks related to getaddrinfo() brokering work crbug.com/1320192 .

Thanks.

### mp...@chromium.org (2023-07-28)

I think https://chromium-review.googlesource.com/c/chromium/src/+/4570328 was supposed to fix this. I think this can only possibly happen once very briefly at shutdown since the only way to make the callback return synchronously (necessary to trigger this bug) is for the browser process to be dead or dying.

This code is in 1% stable on Linux.

I think the correct fix is to make sure we always post the response asynchronously instead of sometimes synchronously calling the callback.

### [Deleted User] (2023-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-28)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-28)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mp...@chromium.org (2023-07-29)

https://chromium-review.googlesource.com/c/chromium/src/+/4727671 is the fix. Verified with the reporter's PoC.

### gi...@appspot.gserviceaccount.com (2023-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4423494e32faffae215fb34b151d49ad619663d2

commit 4423494e32faffae215fb34b151d49ad619663d2
Author: Matthew Denton <mpdenton@chromium.org>
Date: Thu Aug 03 10:08:58 2023

HostResolverSystemTask::OnLookupComplete() should not run synchronously

HostResolverSystemTask::OnLookupComplete() can delete many objects and
no functions expect it to run synchronously when
HostResolverSystemTask::StartLookupAttempt() is called.

Bug: 1466415, 1449497
Change-Id: If17f62961ec46c85b21fe85b8e3c321dc10cdd15
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4727671
Reviewed-by: Tsuyoshi Horo <horo@chromium.org>
Commit-Queue: Matthew Denton <mpdenton@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1178936}

[modify] https://crrev.com/4423494e32faffae215fb34b151d49ad619663d2/services/network/network_service.cc
[modify] https://crrev.com/4423494e32faffae215fb34b151d49ad619663d2/net/dns/host_resolver_system_task.cc
[modify] https://crrev.com/4423494e32faffae215fb34b151d49ad619663d2/net/dns/host_resolver_system_task.h
[modify] https://crrev.com/4423494e32faffae215fb34b151d49ad619663d2/services/network/network_service_unittest.cc


### mp...@chromium.org (2023-08-03)

Reporter this above CL should work, can you verify?

### me...@gmail.com (2023-08-03)

I test this patch with `patch -p1 < 4423494.diff` and it works fine, good job:)

### mp...@chromium.org (2023-08-03)

Thanks!

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-03)

Requesting merge to beta M116 because latest trunk commit (1178936) appears to be after beta branch point (1160321).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-04)

Merge review required: M116 is already shipping to beta.

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
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mp...@chromium.org (2023-08-04)

1. Why does your merge fit within the merge criteria for these milestones?
Security issue in beta.

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/4727671

3. Have the changes been released and tested on canary?
This is Linux desktop only. I don't think there is another dev release before 116 stable cut. It might be fine for this merge to wait until stable cut, though I will be OOO next week and therefore someone else would have to do this merge.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
Yes this is behind the OutOfProcessSystemDnsResolution flag.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No

### am...@chromium.org (2023-08-04)

Thanks mpdenton@ -- yeah, last dev went out today and with Stable Cut on Tuesday, I'd like to let this get some bake time over the weekend and hopefully someone cc'ed here  (such as potentially horo@ since he reviewed this fix) can perform the merge on Monday afternoon Pacific Time (Tuesday morning JST) based on review and potential approval on Monday. 

### mp...@chromium.org (2023-08-05)

Okay thanks, assigning to horo@ for merge next week.

### am...@chromium.org (2023-08-07)

Hi horo@ -- thank you for taking on the merge for this fix. 
There do not appear to be any stability issues from over the weekend, since this fix landed on Canary last week. 

M116 merge approved for https://crrev.com/c/4727671 -- please merge this fix to branch 5845 at soonest / today (by morning Tuesday JST time) so this fix can be included in the M116 Stable cut -- thank you

### gi...@appspot.gserviceaccount.com (2023-08-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9169317aaa2a6acc52636f640ca8602ee6922f40

commit 9169317aaa2a6acc52636f640ca8602ee6922f40
Author: Tsuyoshi Horo <horo@chromium.org>
Date: Tue Aug 08 04:51:10 2023

[M116] HostResolverSystemTask::OnLookupComplete() should not run synchronously

HostResolverSystemTask::OnLookupComplete() can delete many objects and
no functions expect it to run synchronously when
HostResolverSystemTask::StartLookupAttempt() is called.

(cherry picked from commit 4423494e32faffae215fb34b151d49ad619663d2)

Bug: 1466415, 1449497
Change-Id: If17f62961ec46c85b21fe85b8e3c321dc10cdd15
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4727671
Reviewed-by: Tsuyoshi Horo <horo@chromium.org>
Commit-Queue: Matthew Denton <mpdenton@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1178936}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4756408
Reviewed-by: Kenichi Ishibashi <bashi@chromium.org>
Commit-Queue: Tsuyoshi Horo <horo@chromium.org>
Cr-Commit-Position: refs/branch-heads/5845@{#1248}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/9169317aaa2a6acc52636f640ca8602ee6922f40/services/network/network_service.cc
[modify] https://crrev.com/9169317aaa2a6acc52636f640ca8602ee6922f40/net/dns/host_resolver_system_task.cc
[modify] https://crrev.com/9169317aaa2a6acc52636f640ca8602ee6922f40/net/dns/host_resolver_system_task.h
[modify] https://crrev.com/9169317aaa2a6acc52636f640ca8602ee6922f40/services/network/network_service_unittest.cc


### am...@google.com (2023-08-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-10)

Congratulations on another one, Krace! The VRP Panel has decided to award you $3,000 for this report of a significantly mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us!

### me...@gmail.com (2023-08-10)

[Comment Deleted]

### am...@chromium.org (2023-08-10)

Apologies, once again, we are really off our game this week. It was supposed to be $2,000 for the bug report + $1,000 bisect bonus for a total of $3,000 reward. 
The bot/label was correct here, I flubbed up! 

### am...@chromium.org (2023-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1466415?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067758)*

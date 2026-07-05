# UAF in OnGpuControlReturnData

| Field | Value |
|-------|-------|
| **Issue ID** | [486505678](https://issues.chromium.org/issues/486505678) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | lo...@google.com |
| **Created** | 2026-02-22 |
| **Bounty** | $8,000.00 |

## Description

### SUMMARY

I accidentally run into this heap-use-after-free during fuzzing; I managed to reproduced it but failed using my fuzzer recorded steps. I think we might being able to identify issues by the asan crash stack, and I have briefly analyzed the crash stack.

### DETAILS

The UAF occurs when [`gpu::webgpu::WebGPUImplementation::OnGpuControlReturnData`](https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/client/webgpu_implementation.cc;l=316) is invoked on the IO thread after the WebGPU client / context provider has already been destroyed during **DedicatedWorker termination**. The immediate mechanism is that [`gpu::CommandBufferProxyImpl::OnReturnData`](https://source.chromium.org/chromium/chromium/src/+/main:gpu/ipc/client/command_buffer_proxy_impl.cc;l=739) forwards IPC “return data” to a raw `gpu_control_client_` pointer without a lifetime-safe indirection, so teardown on the worker thread can free the `WebGPUImplementation` while a queued return-data message is still dispatched on the IO thread.

The crash stack shows the UAF read originates from `gpu::webgpu::WebGPUImplementation::OnGpuControlReturnData` and is dispatched via the GPU IPC return-data plumbing:

In [`CommandBufferProxyImpl::OnReturnData`](https://source.chromium.org/chromium/chromium/src/+/main:gpu/ipc/client/command_buffer_proxy_impl.cc;l=739), the proxy forwards to `gpu_control_client_`:

```
void CommandBufferProxyImpl::OnReturnData(const std::vector<uint8_t>& data) {
  if (gpu_control_client_) {
    gpu_control_client_->OnGpuControlReturnData(data);
  }
}

```

During worker teardown, Blink’s WebGPU plumbing destroys the underlying graphics context provider asynchronously. The ASAN free stack indicates destruction via `viz::ContextProviderCommandBuffer` → `content::WebGraphicsContext3DProviderImpl` → `blink::WebGraphicsContext3DProviderWrapper` during [`blink::DawnControlClientHolder::Destroy`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/graphics/gpu/dawn_control_client_holder.cc;l=59).

`blink::DawnControlClientHolder::Destroy` posts a task which ultimately owns and destroys `context_provider_`:

```
if (context_provider_) {
  task_runner_->PostTask(
      FROM_HERE,
      base::BindOnce([](std::unique_ptr<WebGraphicsContext3DProviderWrapper>
                            context_provider) {},
                     std::move(context_provider_)));
}

```
### REPRODUCTION CASE

My fuzzer discovered this on the <https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1585188.zip> chromium on Linux. I failed to provide the reproduction case to reproduce it currently since it is quite flaky in my fuzzing machine.

The related flags fuzzer used is `--enable-unsafe-webgpu --enable-features=WebGPUExperimentalFeatures,WebGPUMapSyncOnWorkers,WebGPUService --no-sandbox`

Type of crash: renderer  

Crash State: UAF

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 32.7 KB)
- [poc.html](attachments/poc.html) (text/html, 2.3 KB)
- [poc.js](attachments/poc.js) (text/javascript, 2.6 KB)
- [asan_mac_1596779.txt](attachments/asan_mac_1596779.txt) (text/plain, 45.9 KB)
- [asan_mac_manual_build.txt](attachments/asan_mac_manual_build.txt) (text/plain, 47.7 KB)

## Timeline

### an...@chromium.org (2026-02-22)

lokokung@ can you PTAL? Please reroute if necessary.

### an...@chromium.org (2026-02-22)

Reporter, please do try to provide a PoC as well. Thanks.

### ch...@google.com (2026-02-23)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-23)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### lo...@google.com (2026-02-23)

The `WebGPUMapSyncOnWorkers` feature is experimental, users need to explicitly specify the flag to opt-in so it shouldn't currently have a security impact.

### an...@chromium.org (2026-02-23)

Thanks, added the Security\_Impact-None label.

### he...@gmail.com (2026-03-04)

Hi, I'm now have a stable reproduction and digging with the RCA now. Will attach the details and the poc ASAP when the detailed RCA is done.

### he...@gmail.com (2026-03-04)

### Summary

UAF in [`gpu::CommandBufferProxyImpl::OnReturnData`](https://source.chromium.org/chromium/chromium/src/+/main:gpu/ipc/client/command_buffer_proxy_impl.cc;l=739) when the raw `gpu_control_client_` pointer invoked after the WebGPUImplementation has been destroyed by worker.

### Details

GPU return-data callbacks are dispatched through a raw `GpuControlClient*` without lifetime fencing, while worker teardown can destroy the WebGPU client object on another thread. The first key issue is [`gpu::CommandBufferProxyImpl::OnReturnData`](https://source.chromium.org/chromium/chromium/src/+/main:gpu/ipc/client/command_buffer_proxy_impl.cc;l=739), which unconditionally forwards return data to `gpu_control_client_` if non-null.

From [`gpu::CommandBufferProxyImpl::OnReturnData`](https://source.chromium.org/chromium/chromium/src/+/main:gpu/ipc/client/command_buffer_proxy_impl.cc;l=739):

```
void CommandBufferProxyImpl::OnReturnData(const std::vector<uint8_t>& data) {
  if (gpu_control_client_) {
    gpu_control_client_->OnGpuControlReturnData(data);
  }
}

```

The WebGPU side client is [`gpu::webgpu::WebGPUImplementation::OnGpuControlReturnData`](https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/client/webgpu_implementation.cc;l=316), which dereferences object state (`lost_`, `dawn_wire_`) and handles returned Dawn commands. That is safe only while the `WebGPUImplementation` lifetime is guaranteed.

The teardown ordering creates a race window. In [`gpu::webgpu::WebGPUImplementation::~WebGPUImplementation`](https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/client/webgpu_implementation.cc;l=156), the derived destructor performs cleanup and `helper_->Finish()`. The `GpuControlClient` pointer is not cleared there. Instead, it is cleared later in the base destructor [`gpu::ImplementationBase::~ImplementationBase`](https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/client/implementation_base.cc;l=35).

[`gpu::webgpu::WebGPUImplementation::~WebGPUImplementation`](https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/client/webgpu_implementation.cc;l=156):

```
WebGPUImplementation::~WebGPUImplementation() {
  LoseContext();
  if (dawn_wire_) {
    dawn_wire_->FreeMappedResources(helper_);
  }
  helper_->Finish();
}

```

[`gpu::ImplementationBase::~ImplementationBase`](https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/client/implementation_base.cc;l=35):

```
ImplementationBase::~ImplementationBase() {
  gpu_control_->SetGpuControlClient(nullptr);
}

```

With worker teardown (`worker.terminate()` in the PoC), destruction runs through the worker shutdown path while return-data messages can still be delivered on the ChildIO path. Finally, `OnReturnData` observes a non-null stale client pointer and calls into freed `WebGPUImplementation`, producing UAF.

### Bisection

This issue is introduced by the commit <https://chromium-review.googlesource.com/c/chromium/src/+/7080760>, which makes the reply\_thread on the IO thread.

### Reproduction

Download the chrome from `https://storage.googleapis.com/chromium-browser-asan/mac-release-arm64/asan-mac-release-1592006.zip`. I can also reproduce it on the ToT arm Mac asan build with the commit `94452bdd15ffe772fde8b066e4fc017a6bc0b28d`.

Set up the http server e.g., `python3 -m http.server 8080` for both `poc.html` and `poc.js`

Run

```
./Chromium.app/Contents/MacOS/Chromium --enable-unsafe-webgpu --enable-experimental-web-platform-features http://localhost:8080/poc.html http://localhost:8080/poc.html http://localhost:8080/poc.html

```

You would observe the UAF shown in `asan.txt`. Sometimes you may observer the virtual function corruption crash with the ASAN.

### Suggested Fix

Stop dispatching return-data callbacks to a destructing WebGPUImplementation by clearing the GpuControlClient earlier in teardown. For example, we can clear the client pointer before any blocking work in [`gpu::webgpu::WebGPUImplementation::~WebGPUImplementation`](https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/client/webgpu_implementation.cc;l=156).

### dn...@google.com (2026-03-05)

[comment #6](https://issues.chromium.org/issues/486505678#comment6) says a non-standard flag must be used to expose the issue. Does that imply severity should be downgraded to S2?

### he...@gmail.com (2026-03-06)

Hi, since this is web-reachable, I think it should be the S1 severity, but with the Security-Impact\_None, according to the <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#toc-no-impact>.

Many thanks!

### cw...@chromium.org (2026-03-09)

In #9 the command line flag is `./Chromium.app/Contents/MacOS/Chromium --enable-unsafe-webgpu --enable-experimental-web-platform-features` so it seems like it should be reachable even without `WebGPUMapSyncOnWorkers`. Re-upping priority, Loko PTAL

### lo...@google.com (2026-03-10)

FWIW, I wasn't able reproduce the issue with the steps in [comment#9](https://issues.chromium.org/issues/486505678#comment9) with an ASAN build on my Mac nor with prebuilt, though I am not confident that I was running the ASAN build correctly? (I'm not sure if I set the correct ASAN\_OPTIONS to repro the issue.)

That said after looking at the stack trace and investigating, it definitely seems like the UAF is possible, hence the fix in <https://chromium-review.git.corp.google.com/c/chromium/src/+/7654876>. If OP could try to repro the issue either with that change patched in, or after a pre-built ASAN binary is built, that would be much appreciated. Or alternatively, if OP could provide more instructions on how they repro-ed the issue, i.e. what to set ASAN\_OPTIONS to and/or any other steps that may have been skipped above, I can try again.

### he...@gmail.com (2026-03-11)

Hi, I'm happy to re-run it on the pre-built ASAN binary after the change is land, in order to verify that the fix works. Appreciate for the quick fix.

FWIW, I just run the above poc on my Mac-mini (M4 chip, 16GB memory) and it stably reproduced the ASAN. The parameter in the poc.html such as the `iters` (make it larger), `keepAliveMs` (make it less) might need to be changed for the machine which have better CPUs performance. And attach the ASAN stack reproduced in my Mac-mini.

Many thanks!

### dx...@google.com (2026-03-20)

Project: chromium/src  

Branch:  main  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://chromium-review.googlesource.com/7654876>

[webgpu] Fix use-after-free in WebGPUImplementation during teardown

---


Expand for full commit details
```
     
    WebGPUImplementation receives IPC return data from the GPU process on 
    the IO thread via CommandBufferClientMessageFilter. During the 
    destruction of ContextProviderCommandBuffer, WebGPUImplementation (a 
    member) can be destroyed before the CommandBufferProxyImpl (another 
    member) is destroyed. This creates a race condition where the IO thread 
    may attempt to call into a partially or fully destroyed 
    WebGPUImplementation. 
     
    This CL introduces ShutdownClientMessageFilter() to 
    CommandBufferProxyImpl, which allows for an explicit, synchronous 
    shutdown of the IO thread filter. By calling this at the beginning of 
    the ContextProviderCommandBuffer destructor, we ensure that all 
    in-flight callbacks from the IO thread are completed and future 
    callbacks are blocked before any other members are destroyed. 
     
    Bug: 486505678 
    Change-Id: Ia9c40d996f232a094754846b19691ff5e877b7fd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7654876 
    Reviewed-by: Victor Miura <vmiura@chromium.org> 
    Commit-Queue: Loko Kung <lokokung@google.com> 
    Reviewed-by: Sunny Sachanandani <sunnyps@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1602875}

```

---

Files:

- M `gpu/ipc/client/command_buffer_proxy_impl.cc`
- M `gpu/ipc/client/command_buffer_proxy_impl.h`
- M `services/viz/public/cpp/gpu/context_provider_command_buffer.cc`

---

Hash: [245ab2ef25b526b0c3b820d6a856b01a016cee09](https://chromiumdash.appspot.com/commit/245ab2ef25b526b0c3b820d6a856b01a016cee09)  

Date: Fri Mar 20 22:26:17 2026


---

### he...@gmail.com (2026-03-21)

Thanks for the fix. I can verify the CL 7654876 works and indeed fix this issue on the ToT.

Thank you very much!

### dr...@chromium.org (2026-03-23)

No crashes in Canary, approved to merge to M146 and M147

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://chromium-review.googlesource.com/7694792>

[M147] [webgpu] Fix use-after-free in WebGPUImplementation during teardown

---


Expand for full commit details
```
     
    WebGPUImplementation receives IPC return data from the GPU process on 
    the IO thread via CommandBufferClientMessageFilter. During the 
    destruction of ContextProviderCommandBuffer, WebGPUImplementation (a 
    member) can be destroyed before the CommandBufferProxyImpl (another 
    member) is destroyed. This creates a race condition where the IO thread 
    may attempt to call into a partially or fully destroyed 
    WebGPUImplementation. 
     
    This CL introduces ShutdownClientMessageFilter() to 
    CommandBufferProxyImpl, which allows for an explicit, synchronous 
    shutdown of the IO thread filter. By calling this at the beginning of 
    the ContextProviderCommandBuffer destructor, we ensure that all 
    in-flight callbacks from the IO thread are completed and future 
    callbacks are blocked before any other members are destroyed. 
     
    (cherry picked from commit 245ab2ef25b526b0c3b820d6a856b01a016cee09) 
     
    Bug: 486505678 
    Change-Id: Ia9c40d996f232a094754846b19691ff5e877b7fd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7654876 
    Reviewed-by: Victor Miura <vmiura@chromium.org> 
    Commit-Queue: Loko Kung <lokokung@google.com> 
    Reviewed-by: Sunny Sachanandani <sunnyps@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1602875} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7694792 
    Commit-Queue: Victor Miura <vmiura@chromium.org> 
    Auto-Submit: Loko Kung <lokokung@google.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#1322} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `gpu/ipc/client/command_buffer_proxy_impl.cc`
- M `gpu/ipc/client/command_buffer_proxy_impl.h`
- M `services/viz/public/cpp/gpu/context_provider_command_buffer.cc`

---

Hash: [65f5882b2cefc3fc33f0afc761f3ce6d69601dd3](https://chromiumdash.appspot.com/commit/65f5882b2cefc3fc33f0afc761f3ce6d69601dd3)  

Date: Tue Mar 24 01:26:57 2026


---

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Lokbondo Kung [lokokung@google.com](mailto:lokokung@google.com)  

Link:    <https://chromium-review.googlesource.com/7694118>

[M146] [webgpu] Fix use-after-free in WebGPUImplementation during teardown

---


Expand for full commit details
```
     
    WebGPUImplementation receives IPC return data from the GPU process on 
    the IO thread via CommandBufferClientMessageFilter. During the 
    destruction of ContextProviderCommandBuffer, WebGPUImplementation (a 
    member) can be destroyed before the CommandBufferProxyImpl (another 
    member) is destroyed. This creates a race condition where the IO thread 
    may attempt to call into a partially or fully destroyed 
    WebGPUImplementation. 
     
    This CL introduces ShutdownClientMessageFilter() to 
    CommandBufferProxyImpl, which allows for an explicit, synchronous 
    shutdown of the IO thread filter. By calling this at the beginning of 
    the ContextProviderCommandBuffer destructor, we ensure that all 
    in-flight callbacks from the IO thread are completed and future 
    callbacks are blocked before any other members are destroyed. 
     
    (cherry picked from commit 245ab2ef25b526b0c3b820d6a856b01a016cee09) 
     
    Bug: 486505678 
    Change-Id: Ia9c40d996f232a094754846b19691ff5e877b7fd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7654876 
    Reviewed-by: Victor Miura <vmiura@chromium.org> 
    Commit-Queue: Loko Kung <lokokung@google.com> 
    Reviewed-by: Sunny Sachanandani <sunnyps@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1602875} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7694118 
    Auto-Submit: Loko Kung <lokokung@google.com> 
    Commit-Queue: Victor Miura <vmiura@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#3101} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `gpu/ipc/client/command_buffer_proxy_impl.cc`
- M `gpu/ipc/client/command_buffer_proxy_impl.h`
- M `services/viz/public/cpp/gpu/context_provider_command_buffer.cc`

---

Hash: [d0625af457d2e21103d3a5f35d476ba3c58138cd](https://chromiumdash.appspot.com/commit/d0625af457d2e21103d3a5f35d476ba3c58138cd)  

Date: Tue Mar 24 01:27:05 2026


---

### pe...@google.com (2026-03-24)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### qk...@google.com (2026-03-25)

Labeled `LTS-NotApplicable-144` and `LTS-NotApplicable-138` because M144 and M138 don't have the suspected CL[1].

[1] https://chromium-review.googlesource.com/c/chromium/src/+/7080760

### sp...@google.com (2026-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
Baseline. Renderer RCE / memory corruption in a sandboxed process with bisect


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/486505678)*

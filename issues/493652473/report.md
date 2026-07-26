# Use-after-free in DevToolsRendererChannel::ForceDetachWorkerSessions via duplicate ChildTargetCreated for dedicated workers

| Field | Value |
|-------|-------|
| **Issue ID** | [493652473](https://issues.chromium.org/issues/493652473) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | yy...@chromium.org |
| **Created** | 2026-03-18 |
| **Bounty** | $26,000.00 |

## Description

# Use-after-free in DevToolsRendererChannel::ForceDetachWorkerSessions via duplicate ChildTargetCreated for dedicated workers

## Summary

A compromised renderer can trigger a use-after-free in the browser process by sending duplicate `blink.mojom.DevToolsAgentHost.ChildTargetCreated` messages for the same dedicated worker token through different DevTools channels. The dedicated worker branch in `ChildTargetCreated` lacks the duplicate-token validation that the worklet branch enforces, allowing a single `DedicatedWorkerDevToolsAgentHost` to be inserted into multiple `child_targets_` sets while its `destroyed_callback_` is silently overwritten. When the host object is freed, one channel retains a dangling pointer. A subsequent frame navigation calls `ForceDetachWorkerSessions`, which dereferences this pointer in the browser process. The vulnerability affects all desktop platforms (Linux, Windows, macOS, ChromeOS) and requires only that the user opens DevTools (F12) on the compromised tab. Threat model: compromised renderer / sandbox escape.

## Bisect

Introducing Commit: `1598b6392def1a0d33fb485d78e463875e414655`

- Date: 2024-01-12
- Author: Andrey Kosyakov [caseq@chromium.org](mailto:caseq@chromium.org)
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/5185611>

## Root Cause

When a dedicated worker is created and DevTools is attached, the renderer sends a `ChildTargetCreated` IPC to the browser. The browser-side handler in `DevToolsRendererChannel::ChildTargetCreated` looks up the corresponding `DedicatedWorkerDevToolsAgentHost` by token, calls `ChildWorkerCreated` to register a destruction callback, rebinds the host's Mojo pipes via `SetRenderer`, and inserts the host's raw pointer into the channel's `child_targets_` set:

```
// content/browser/devtools/devtools_renderer_channel.cc:185-225
case blink::mojom::DevToolsExecutionContextType::kDedicatedWorker: {
  DedicatedWorkerDevToolsAgentHost* dedicated_worker_agent_host =
      WorkerDevToolsManager::GetInstance().GetDevToolsHostFromToken(
          devtools_worker_token);
  if (!dedicated_worker_agent_host)
    return;
  dedicated_worker_agent_host->ChildWorkerCreated(
      url, name,
      base::BindOnce(&DevToolsRendererChannel::ChildTargetDestroyed,
                     weak_factory_.GetWeakPtr()));
  agent_host = dedicated_worker_agent_host;
  break;
}
agent_host->SetRenderer(process_id_, std::move(worker_devtools_agent),
                        std::move(host_receiver));
child_targets_.insert(agent_host.get());

```

The worklet branch guards against duplicate tokens with an explicit check that calls `ReportBadMessage` and returns early. The dedicated worker branch has no such guard. `GetDevToolsHostFromToken` performs a global lookup by token with no validation of the caller's identity, so any channel in the same process can retrieve the same host object. `ChildWorkerCreated` unconditionally overwrites the single `destroyed_callback_` member:

```
// content/browser/devtools/worker_or_worklet_devtools_agent_host.cc:55-62
void WorkerOrWorkletDevToolsAgentHost::ChildWorkerCreated(
    const GURL& url, const std::string& name,
    base::OnceCallback<void(DevToolsAgentHostImpl*)> callback) {
  url_ = url;
  name_ = name;
  destroyed_callback_ = std::move(callback);
}

```

The `child_targets_` container uses `raw_ptr<WorkerOrWorkletDevToolsAgentHost, CtnExperimental>`, which maps to `kMayDangle` and disables Chromium's internal dangling-pointer detection.

The attack proceeds as follows. The compromised renderer creates a dedicated worker, causing the parent frame's DevTools channel to send the normal `ChildTargetCreated` with the worker's token. The browser inserts the host pointer into the frame channel's `child_targets_` and sets `destroyed_callback_` to point back at that channel. Meanwhile, the worker's own `DevToolsAgent` receives a `host_remote_` Mojo endpoint connected to the host's own `DevToolsRendererChannel`. Through this endpoint, the compromised renderer sends a second `ChildTargetCreated` carrying the same token but with throwaway Mojo pipe endpoints. The browser processes this on the host's channel, overwriting `destroyed_callback_` and rebinding the host's Mojo connection to the throwaway pipes. When the throwaway pipes are immediately destroyed on the renderer side, the browser's `agent_remote_` disconnect handler fires `Disconnected`, which invokes the overwritten callback, removing the host only from its own channel's `child_targets_`. The frame channel's `child_targets_` still holds the pointer. After the renderer terminates the worker, `WorkerDevToolsManager::WorkerDestroyed` erases the host from its `hosts_` map, dropping the last reference and freeing the object. On the next same-origin navigation of the frame, `ReadyToCommitNavigation` calls `ForceDetachWorkerSessions`, which iterates the frame channel's `child_targets_` and dereferences the freed host:

```
// content/browser/devtools/devtools_renderer_channel.cc:76-80
void DevToolsRendererChannel::ForceDetachWorkerSessions() {
  for (WorkerOrWorkletDevToolsAgentHost* host : child_targets_) {
    host->ForceDetachAllSessions();
  }
}

```

This virtual call reads the vtable pointer from freed memory, producing a heap-use-after-free in the browser process.

## Reproduce

Tested at commit `d0f83d769eeed` on macOS arm64 (also confirmed on Linux x86\_64) with an ASAN build:

```
is_asan = true
is_debug = false
is_component_build = true
dcheck_always_on = true

```

The PoC requires a renderer-side source modification (`patch.diff`) that replays the `ChildTargetCreated` IPC through the worker's own DevTools pipe, simulating a compromised renderer.

### 1. Apply patch and build

```
cd ~/chromium/src
git apply patch.diff
autoninja -C out/asan-release chrome

```
### 2. Start HTTP server

```
cd ~/issue_devtools_childtarget_uaf
python3 -m http.server 18035 &

```
### 3. Launch Chrome

- macOS:

```
ASAN_OPTIONS=detect_odr_violation=0 \
~/chromium/src/out/asan-release/Chromium.app/Contents/MacOS/Chromium \
  --enable-logging=stderr \
  http://localhost:18035/poc.html

```

- Linux:

```
ASAN_OPTIONS=detect_odr_violation=0 \
~/chromium/src/out/asan-release/chrome \
  --enable-logging=stderr \
  http://localhost:18035/poc.html

```
### 4. Trigger

Open DevTools on the tab (**F12** or **Cmd+Option+I**). The PoC page automatically creates a worker, triggers the duplicate IPC, terminates the worker, and navigates. The browser process crashes within 15 seconds.

```
=================================================================
==4176353==ERROR: AddressSanitizer: heap-use-after-free on address 0x7cfbb38b7980 at pc 0x7f8c16791b0a bp 0x7ffd8c1de3b0 sp 0x7ffd8c1de3a8
READ of size 8 at 0x7cfbb38b7980 thread T0 (chrome)
    #0 0x7f8c16791b09 in content::DevToolsRendererChannel::ForceDetachWorkerSessions() content/browser/devtools/devtools_renderer_channel.cc:81:11
    #1 0x7f8c169ecd9a in content::RenderFrameDevToolsAgentHost::ReadyToCommitNavigation(content::NavigationHandle*) content/browser/devtools/render_frame_devtools_agent_host.cc:510:25
    #2 0x7f8c1825a7b3 in void content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::*)(content::NavigationHandle*), content::NavigationHandle*&>(void (content::WebContentsObserver::*)(content::NavigationHandle*), content::NavigationHandle*&) content/browser/web_contents/web_contents_impl.h:1833:9
    #3 0x7f8c1825b75d in content::WebContentsImpl::ReadyToCommitNavigation(content::NavigationHandle*) content/browser/web_contents/web_contents_impl.cc:7431:14
    #4 0x7f8c178bcc95 in content::NavigationRequest::ReadyToCommitNavigation(bool) content/browser/renderer_host/navigation_request.cc:8990:20
    #5 0x7f8c178b3e03 in content::NavigationRequest::CommitNavigation() content/browser/renderer_host/navigation_request.cc:6716:3

0x7cfbb38b7980 is located 0 bytes inside of 648-byte region [0x7cfbb38b7980,0x7cfbb38b7c08)
freed by thread T0 (chrome) here:
    #0 0x55ace64339e2 in operator delete(void*, unsigned long)
    #1 0x7f8c16a2dcd5 in std::__Cr::__tree<...>::erase(...) base/memory/ref_counted.h:375:5
    #2 0x7f8c184c4614 in content::DedicatedWorkerHost::~DedicatedWorkerHost() content/browser/worker_host/dedicated_worker_host.cc:190:40
    #3 0x7f8c184c5652 in content::DedicatedWorkerHost::OnMojoDisconnect() content/browser/worker_host/dedicated_worker_host.cc:245:3

previously allocated by thread T0 (chrome) here:
    #0 0x55ace6432ddd in operator new(unsigned long)
    #1 0x7f8c16a2caac in base::MakeRefCounted<content::DedicatedWorkerDevToolsAgentHost, ...>(...) base/memory/scoped_refptr.h:151:12
    #2 0x7f8c16a2c689 in content::WorkerDevToolsManager::WorkerCreated(...) content/browser/devtools/worker_devtools_manager.cc:54:18

SUMMARY: AddressSanitizer: heap-use-after-free content/browser/devtools/devtools_renderer_channel.cc:81:11 in content::DevToolsRendererChannel::ForceDetachWorkerSessions()

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 1.3 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 3.0 KB)
- [asan.log](attachments/asan.log) (text/plain, 40.2 KB)
- [worker.js](attachments/worker.js) (text/javascript, 174 B)
- [patch_no_interaction.diff](attachments/patch_no_interaction.diff) (text/x-diff, 4.2 KB)
- [shared_worker.js](attachments/shared_worker.js) (text/javascript, 351 B)
- [poc_no_interaction.html](attachments/poc_no_interaction.html) (text/html, 4.0 KB)
- [asan_no_interaction.log](attachments/asan_no_interaction.log) (text/plain, 25.5 KB)

## Timeline

### ts...@google.com (2026-03-18)

Since a patch is required, DNR, but assigning per files implicated in attached symbolized ASAN trace.

### ts...@google.com (2026-03-18)

Assigning per suspect CL.

### wf...@chromium.org (2026-03-27)

user gesture requirement moves this from sev-high to sev-medium.

### ch...@google.com (2026-03-28)

Setting milestone because of s2 severity.

### aj...@google.com (2026-04-08)

A better repro of this report is available in [issue 500136078](https://issues.chromium.org/issues/500136078) - marking the bug as S1 as it turns out no user gesture is required.

### je...@gmail.com (2026-04-08)

Interesting, I'll also look into improving the reproducibility.

### yy...@chromium.org (2026-04-08)

I wrote https://chromium-review.googlesource.com/c/chromium/src/+/7736861 for crbug.com/500136078, which has been merged to this issue.

### je...@gmail.com (2026-04-08)

I've confirmed that this bug can be triggered **without any user interaction** (no DevTools / F12 required), which aligns with the S1 reassessment in [comment #6](https://issues.chromium.org/issues/493652473#comment6).

## Root cause (no-interaction variant)

The original PoC uses the frame's `DevToolsRendererChannel`, which only exists when DevTools is attached. However, **SharedWorker DevTools pipes are unconditionally connected** to the browser during worker startup via `OnReadyForInspection` (`web_shared_worker_impl.cc:350`), regardless of whether DevTools UI is open.

A compromised renderer can send forged `ChildTargetCreated` messages through the SharedWorker's `host_remote_` pipe, targeting a DedicatedWorker's token. Each message causes `SetRenderer()` with throwaway Mojo pipes on the `DedicatedWorkerDevToolsAgentHost`. When the throwaway pipes close, `Disconnected()` fires and calls `Release()`. Two such cycles underflow the reference count (constructor `AddRef()` is only called once), freeing the host object while `WorkerDevToolsManager::hosts_` still holds a `scoped_refptr` to it.

## Reproduce (no interaction)

Tested at the same commit (d0f83d769eeed) on Linux x86\_64 with the same ASAN build config:

```
is_asan = true
is_debug = false
is_component_build = true

```
### 1. Apply patch and build

```
cd ~/chromium/src
git apply patch_no_interaction.diff
autoninja -C out/asan-release chrome

```
### 2. Start HTTP server

```
cd ~/chromium/src/issue_devtools_childtarget_uaf_v2
python3 -m http.server 18035 &

```
### 3. Launch Chrome — no DevTools needed

```
ASAN_OPTIONS=detect_odr_violation=0 \
  ~/chromium/src/out/asan-release/chrome \
  --enable-logging=stderr \
  http://localhost:18035/poc_no_interaction.html

```

The browser process crashes within ~15 seconds with no user interaction:

```
==1052435==ERROR: AddressSanitizer: heap-use-after-free on address 0x7d145e3c8980
READ of size 1 at 0x7d145e3c8980 thread T0 (chrome)
    #0 in content::DedicatedWorkerDevToolsAgentHost::DisconnectIfNotCreated()
       content/browser/devtools/dedicated_worker_devtools_agent_host.cc:100:8
    #1 in content::WorkerDevToolsManager::WorkerDestroyed()
       content/browser/devtools/worker_devtools_manager.cc:75:15
    #2 in content::DedicatedWorkerHost::~DedicatedWorkerHost()
       content/browser/worker_host/dedicated_worker_host.cc:190:40
    #3 in content::DedicatedWorkerHost::OnMojoDisconnect()
       content/browser/worker_host/dedicated_worker_host.cc:245:3

freed by thread T0 (chrome) here:
    #0 in operator delete(void*, unsigned long)
    #1 in content::WorkerOrWorkletDevToolsAgentHost::Disconnected()
       base/memory/ref_counted.h:375:5

previously allocated by thread T0 (chrome) here:
    #0 in operator new(unsigned long)
    #1 in base::MakeRefCounted<content::DedicatedWorkerDevToolsAgentHost, ...>()
    #2 in content::WorkerDevToolsManager::WorkerCreated()
       content/browser/devtools/worker_devtools_manager.cc:54:18

SUMMARY: AddressSanitizer: heap-use-after-free
  content/browser/devtools/dedicated_worker_devtools_agent_host.cc:100:8
  in content::DedicatedWorkerDevToolsAgentHost::DisconnectIfNotCreated()

MiraclePtr Status: NOT PROTECTED
This crash is still exploitable with MiraclePtr.

```
## Attached files

- `poc_no_interaction.html` — main page (creates DedicatedWorker + SharedWorker, terminates DW to trigger UAF)
- `worker.js` / `shared_worker.js` — minimal worker scripts
- `patch_no_interaction.diff` — renderer-side patch simulating compromised renderer
- `asan_no_interaction.log` — full ASAN output

### dx...@google.com (2026-04-10)

Project: chromium/src  

Branch:  main  

Author:  Yoshisto Yanagisawa [yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7736861>

Prevent double initialization and Release() in DedicatedWorkerDevToolsAgentHost

---


Expand for full commit details
```
     
    A compromised renderer could trigger multiple ChildTargetCreated calls 
    for the same dedicated worker via a shared worker's DevTools interface. 
    Each call could establish a new mojo pipe, leading to multiple 
    SetRenderer() calls and subsequent multiple Release() calls on the host 
    object when the pipes were closed. This could underflow the reference 
    count and cause a Use-After-Free (UAF) in the browser process. 
     
    This CL fixes the issue in two ways: 
    1. It prevents multiple initializations of a 
       DedicatedWorkerDevToolsAgentHost in 
       DevToolsRendererChannel::ChildTargetCreated(). If the agent host 
       already has a renderer set, further requests for the same token are 
       ignored. 
    2. It introduces a flag (kWorkerOrWorkletAgentDoubleReleaseFix) 
       to ensure that the self-reference (AddRef() in constructor) is 
       only released once during Disconnected() in the base class 
       WorkerOrWorkletDevToolsAgentHost. 
     
    Additionally, a DCHECK in ChildTargetCreated is promoted to CHECK to 
    ensure that the token must correspond to an existing agent host. 
     
    The refcount fix is gated behind a feature flag to serve as a kill 
    switch for easier merging into older release branches. 
     
    Bug: 500136078, 493652473 
    Change-Id: Ib1a58b9a7f3f63f0362d40476f290645ee865c88 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7736861 
    Auto-Submit: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    Commit-Queue: Rakina Zata Amni <rakina@chromium.org> 
    Reviewed-by: Steven Holte <holte@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1612797}

```

---

Files:

- M `content/browser/bad_message.h`
- M `content/browser/devtools/dedicated_worker_devtools_agent_host.h`
- A `content/browser/devtools/devtools_refcount_unittest.cc`
- M `content/browser/devtools/devtools_renderer_channel.cc`
- M `content/browser/devtools/worker_or_worklet_devtools_agent_host.cc`
- M `content/browser/devtools/worker_or_worklet_devtools_agent_host.h`
- M `content/common/features.cc`
- M `content/common/features.h`
- M `content/test/BUILD.gn`
- M `tools/metrics/histograms/metadata/stability/enums.xml`

---

Hash: [5b7fd82e6c332f92840e8762cdaf218f009ddc3c](https://chromiumdash.appspot.com/commit/5b7fd82e6c332f92840e8762cdaf218f009ddc3c)  

Date: Fri Apr 10 12:59:37 2026


---

### al...@google.com (2026-04-13)

I think this was fixed by [yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org) in <https://crrev.com/c/7736861>. yyanagisawa@ could you please mark as fixed if everything you had in mind has landed?

### yy...@chromium.org (2026-04-13)

Sure.  I plan to fix this in 2 ways. 1. fixing the entrance at SharedWorker. 2. fixing double release in DedicatedWorker.  The previous change was for 2.  I am now working on 1.
I assume the similar issue may exist in ServiceWorker, and am now inspecting.

### yy...@chromium.org (2026-04-15)

All necessary CLs have been landed.

### yy...@chromium.org (2026-04-15)

https://issues.chromium.org/issues/500136078 is used as a tracking issue, and have not update this unfortunately.

### ch...@google.com (2026-04-15)

Requesting merge to M147 because latest trunk commit (1612797) appears to be after M147 branch point (1596535).

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M148 because latest trunk commit (1612797) appears to be after M148 branch point (1610480).

### ch...@google.com (2026-04-15)

**M147** merge request created. **Please update [crbug/502819720](https://crbug.com/502819720) to have this merge reviewed.**

### ch...@google.com (2026-04-15)

**M148** merge request created. **Please update [crbug/502819872](https://crbug.com/502819872) to have this merge reviewed.**

### dx...@google.com (2026-04-15)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Yoshisto Yanagisawa [yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7759170>

[M148] Prevent double initialization and Release() in DedicatedWorkerDevToolsAgentHost

---


Expand for full commit details
```
     
    Original change's description: 
    > Prevent double initialization and Release() in DedicatedWorkerDevToolsAgentHost 
    > 
    > A compromised renderer could trigger multiple ChildTargetCreated calls 
    > for the same dedicated worker via a shared worker's DevTools interface. 
    > Each call could establish a new mojo pipe, leading to multiple 
    > SetRenderer() calls and subsequent multiple Release() calls on the host 
    > object when the pipes were closed. This could underflow the reference 
    > count and cause a Use-After-Free (UAF) in the browser process. 
    > 
    > This CL fixes the issue in two ways: 
    > 1. It prevents multiple initializations of a 
    >    DedicatedWorkerDevToolsAgentHost in 
    >    DevToolsRendererChannel::ChildTargetCreated(). If the agent host 
    >    already has a renderer set, further requests for the same token are 
    >    ignored. 
    > 2. It introduces a flag (kWorkerOrWorkletAgentDoubleReleaseFix) 
    >    to ensure that the self-reference (AddRef() in constructor) is 
    >    only released once during Disconnected() in the base class 
    >    WorkerOrWorkletDevToolsAgentHost. 
    > 
    > Additionally, a DCHECK in ChildTargetCreated is promoted to CHECK to 
    > ensure that the token must correspond to an existing agent host. 
    > 
    > The refcount fix is gated behind a feature flag to serve as a kill 
    > switch for easier merging into older release branches. 
    > 
    > Bug: 500136078, 493652473 
    > Change-Id: Ib1a58b9a7f3f63f0362d40476f290645ee865c88 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7736861 
    > Auto-Submit: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    > Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    > Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    > Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    > Commit-Queue: Rakina Zata Amni <rakina@chromium.org> 
    > Reviewed-by: Steven Holte <holte@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1612797} 
     
    (cherry picked from commit 5b7fd82e6c332f92840e8762cdaf218f009ddc3c) 
     
    Bug: 502819872,500136078,493652473 
    Change-Id: Ib1a58b9a7f3f63f0362d40476f290645ee865c88 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7759170 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7778@{#670} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `content/browser/bad_message.h`
- M `content/browser/devtools/dedicated_worker_devtools_agent_host.h`
- A `content/browser/devtools/devtools_refcount_unittest.cc`
- M `content/browser/devtools/devtools_renderer_channel.cc`
- M `content/browser/devtools/worker_or_worklet_devtools_agent_host.cc`
- M `content/browser/devtools/worker_or_worklet_devtools_agent_host.h`
- M `content/common/features.cc`
- M `content/common/features.h`
- M `content/test/BUILD.gn`
- M `tools/metrics/histograms/metadata/stability/enums.xml`

---

Hash: [ae35dbbc4868714575c806de9686e9624c5bd288](https://chromiumdash.appspot.com/commit/ae35dbbc4868714575c806de9686e9624c5bd288)  

Date: Wed Apr 15 11:08:03 2026


---

### pe...@google.com (2026-04-15)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### yy...@chromium.org (2026-04-15)

1. Was this issue a regression for the milestone it was found in?

No.  I understand this is a structure issue that exist for a long time following the Microsoft Component Object Model (COM).  Since there were no smart pointer available, dereferencing by one self might be natural when the code was first implemented, which brought the double free issue today.

2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No.  As I mentioned in 1, it is long living issue.

### dx...@google.com (2026-04-16)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Yoshisto Yanagisawa [yyanagisawa@chromium.org](mailto:yyanagisawa@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7761455>

[M147] Prevent double initialization and Release() in DedicatedWorkerDevToolsAgentHost

---


Expand for full commit details
```
     
    Original change's description: 
    > Prevent double initialization and Release() in DedicatedWorkerDevToolsAgentHost 
    > 
    > A compromised renderer could trigger multiple ChildTargetCreated calls 
    > for the same dedicated worker via a shared worker's DevTools interface. 
    > Each call could establish a new mojo pipe, leading to multiple 
    > SetRenderer() calls and subsequent multiple Release() calls on the host 
    > object when the pipes were closed. This could underflow the reference 
    > count and cause a Use-After-Free (UAF) in the browser process. 
    > 
    > This CL fixes the issue in two ways: 
    > 1. It prevents multiple initializations of a 
    >    DedicatedWorkerDevToolsAgentHost in 
    >    DevToolsRendererChannel::ChildTargetCreated(). If the agent host 
    >    already has a renderer set, further requests for the same token are 
    >    ignored. 
    > 2. It introduces a flag (kWorkerOrWorkletAgentDoubleReleaseFix) 
    >    to ensure that the self-reference (AddRef() in constructor) is 
    >    only released once during Disconnected() in the base class 
    >    WorkerOrWorkletDevToolsAgentHost. 
    > 
    > Additionally, a DCHECK in ChildTargetCreated is promoted to CHECK to 
    > ensure that the token must correspond to an existing agent host. 
    > 
    > The refcount fix is gated behind a feature flag to serve as a kill 
    > switch for easier merging into older release branches. 
    > 
    > Bug: 500136078, 493652473 
    > Change-Id: Ib1a58b9a7f3f63f0362d40476f290645ee865c88 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7736861 
    > Auto-Submit: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    > Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    > Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    > Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    > Commit-Queue: Rakina Zata Amni <rakina@chromium.org> 
    > Reviewed-by: Steven Holte <holte@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1612797} 
     
    (cherry picked from commit 5b7fd82e6c332f92840e8762cdaf218f009ddc3c) 
     
    Bug: 502819720,500136078,493652473 
    Change-Id: Ib1a58b9a7f3f63f0362d40476f290645ee865c88 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7761455 
    Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    Reviewed-by: Steven Holte <holte@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#3011} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `content/browser/bad_message.h`
- M `content/browser/devtools/dedicated_worker_devtools_agent_host.h`
- A `content/browser/devtools/devtools_refcount_unittest.cc`
- M `content/browser/devtools/devtools_renderer_channel.cc`
- M `content/browser/devtools/worker_or_worklet_devtools_agent_host.cc`
- M `content/browser/devtools/worker_or_worklet_devtools_agent_host.h`
- M `content/common/features.cc`
- M `content/common/features.h`
- M `content/test/BUILD.gn`
- M `tools/metrics/histograms/metadata/stability/enums.xml`

---

Hash: [4bfc557c35035ff700ec3643e1ca827ce27fe33f](https://chromiumdash.appspot.com/commit/4bfc557c35035ff700ec3643e1ca827ce27fe33f)  

Date: Thu Apr 16 04:57:40 2026


---

### sp...@google.com (2026-04-24)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $26000.00 for this report.

Rationale for this decision:
Baseline with bisect. Renderer RCE / memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-05-07)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-05-07)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7805825?tab=checks>
2. Medium - There were some conflicts.
3. 147 and 148
4. Yes, the bug was introduced in 2024.

### dx...@google.com (2026-05-14)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Gyuyoung Kim [qkim@google.com](mailto:qkim@google.com)  

Link:    <https://chromium-review.googlesource.com/7805825>

[M144-LTS] Prevent double initialization and Release() in DedicatedWorkerDevToolsAgentHost

---


Expand for full commit details
```
     
    A compromised renderer could trigger multiple ChildTargetCreated calls 
    for the same dedicated worker via a shared worker's DevTools interface. 
    Each call could establish a new mojo pipe, leading to multiple 
    SetRenderer() calls and subsequent multiple Release() calls on the host 
    object when the pipes were closed. This could underflow the reference 
    count and cause a Use-After-Free (UAF) in the browser process. 
     
    This CL fixes the issue in two ways: 
    1. It prevents multiple initializations of a 
       DedicatedWorkerDevToolsAgentHost in 
       DevToolsRendererChannel::ChildTargetCreated(). If the agent host 
       already has a renderer set, further requests for the same token are 
       ignored. 
    2. It introduces a flag (kWorkerOrWorkletAgentDoubleReleaseFix) 
       to ensure that the self-reference (AddRef() in constructor) is 
       only released once during Disconnected() in the base class 
       WorkerOrWorkletDevToolsAgentHost. 
     
    Additionally, a DCHECK in ChildTargetCreated is promoted to CHECK to 
    ensure that the token must correspond to an existing agent host. 
     
    The refcount fix is gated behind a feature flag to serve as a kill 
    switch for easier merging into older release branches. 
     
    (cherry picked from commit 5b7fd82e6c332f92840e8762cdaf218f009ddc3c) 
     
    Bug: 500136078, 493652473 
    Change-Id: Ib1a58b9a7f3f63f0362d40476f290645ee865c88 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7736861 
    Auto-Submit: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    Commit-Queue: Rakina Zata Amni <rakina@chromium.org> 
    Reviewed-by: Steven Holte <holte@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1612797} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7805825 
    Reviewed-by: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Giovanni Pezzino <giovax@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4859} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `content/browser/bad_message.h`
- M `content/browser/devtools/dedicated_worker_devtools_agent_host.h`
- A `content/browser/devtools/devtools_refcount_unittest.cc`
- M `content/browser/devtools/devtools_renderer_channel.cc`
- M `content/browser/devtools/worker_or_worklet_devtools_agent_host.cc`
- M `content/browser/devtools/worker_or_worklet_devtools_agent_host.h`
- M `content/common/features.cc`
- M `content/common/features.h`
- M `content/test/BUILD.gn`
- M `tools/metrics/histograms/metadata/stability/enums.xml`

---

Hash: [e475837af64ac66503d555aa0438453f517d064e](https://chromiumdash.appspot.com/commit/e475837af64ac66503d555aa0438453f517d064e)  

Date: Thu May 14 04:36:52 2026


---

### ch...@google.com (2026-07-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493652473)*

# Browser-Process Heap Use-After-Free in FileSystemAccessWatcherManager

| Field | Value |
|-------|-------|
| **Issue ID** | [501115599](https://issues.chromium.org/issues/501115599) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | as...@gmail.com |
| **Assignee** | fe...@google.com |
| **Created** | 2026-04-10 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

A browser-process heap use-after-free (UAF) vulnerability exists in the File System Access API due to iterator/lifetime invalidation during change-delivery event dispatch.

`FileSystemAccessWatcherManager::OnRawChange(...)` iterates over its internal observation groups to notify them of changes. However, the resulting callback chain can synchronously destroy the active `FileSystemAccessObservationGroup`.

When an observed file root disappears or errors out, the following sequence occurs:

1. `OnRawChange()` calls `observation_group.NotifyOfChanges(...)`
2. `FileSystemAccessObserverObservation::OnChanges()` may call `HandleError()` when the observation root disappears.
3. `HandleError()` sends an errored event and calls `host_->RemoveObservation(this)`.
4. Removing the last observation triggers `watcher_manager_->RemoveObservationGroup(...)`.
5. This erases the group from the manager-owned map while `OnRawChange()` is still actively iterating over it.

When the callback chain finishes and control returns to `OnRawChange()`, the iterator or container state is invalid. The next operation inside the loop accesses freed memory, causing an immediate crash.

As indicated by the ASan log (`MiraclePtr Status: NOT PROTECTED`), no `raw_ptr<T>` access was detected for this specific memory operation. Consequently, this vulnerability is not mitigated by MiraclePtr and results in an exploitable browser-process Use-After-Free, which can potentially be leveraged by a compromised renderer or malicious web page to achieve sandbox escape/RCE.

**VERSION**

Chrome Version: Chromium 148.0.7763.0 (Official mac-arm64 ASan prebuilt)

Operating System: macOS arm64

**REPRODUCTION CASE**

*Please see the attached `poc.html` and `asan.log` files.*

1. Extract the provided files into a directory and serve them locally using a python web server:
   `python3 -m http.server 8001`
2. In another terminal, create a fresh profile directory and launch ASan Chromium:
   
   ```
   profile_dir=/tmp/fsa_obs_group_uaf_profile_final
   mkdir -p "$profile_dir"
   ASAN_OPTIONS='detect_odr_violation=0:abort_on_error=1:symbolize=1:external_symbolizer_path=/path/to/llvm-symbolizer:log_path=/tmp/fsa_obs_group_uaf_final' \
     open -n '/path/to/.asan_mac_arm64_run/Chromium.app' --args \
       --user-data-dir="$profile_dir" \
       --enable-blink-features=FileSystemObserver \
       --test-type \
       --no-first-run \
       --no-default-browser-check \
       'http://127.0.0.1:8001/poc.html?attempts=256&concurrency=16'
   
   ```
3. On the loaded page, click **Start**.
4. In the directory picker, choose any writable local directory.
5. The PoC will rapidly create, observe, and delete files to drive the `disappeared -> errored -> observation teardown` path at high concurrency. The browser process will quickly crash with a UAF.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: Browser Process

Crash State:

```
=================================================================
==63307==ERROR: AddressSanitizer: heap-use-after-free on address 0x6190006d1d40 at pc 0x000309218ea4 bp 0x00016d9bfff0 sp 0x00016d9bffe8

READ of size 4 at 0x6190006d1d40 thread T0 (Crash Stack):
    #0 0x000309218ea0 in content::FileSystemAccessWatcherManager::OnRawChange(...)
    #1 0x00030913b300 in content::FileSystemAccessChangeSource::NotifyOfChange(...)
    #2 0x00030a812238 in content::FileSystemAccessLocalPathWatcher::OnFilePathChanged(...)
    [... truncated sequence manager / run loop ...]

0x6190006d1d40 is located 704 bytes inside of 936-byte region[0x6190006d1a80,0x6190006d1e28)

freed by thread T0 here (Free Stack):
    #0 0x0001027d1074 in __asan_memmove
    #1 0x00030921a7c0 in content::FileSystemAccessWatcherManager::RemoveObserver(...)
    #2 0x0003091f0990 in content::FileSystemAccessObservationGroup::~FileSystemAccessObservationGroup()
    #3 0x000309224c50 in std::__Cr::__tree<...>::erase(...)
    #4 0x00030921af14 in content::FileSystemAccessWatcherManager::RemoveObservationGroup(...)
    #5 0x0003091f2d54 in base::ScopedObservation<...>::Reset()
    #6 0x0003091efe70 in content::FileSystemAccessObservationGroup::Observer::~Observer()
    #7 0x0003091fef58 in content::FileSystemAccessObserverObservation::~FileSystemAccessObserverObservation()
    #8 0x0003091ff178 in content::FileSystemAccessObserverObservation::~FileSystemAccessObserverObservation()
    #9 0x0003091fb598 in std::__Cr::vector<...>::erase(...)
    #10 0x0003091f75d8 in content::FileSystemAccessObserverHost::RemoveObservation(...)
    #11 0x0003091ffa38 in content::FileSystemAccessObserverObservation::HandleError()
    #12 0x0003091fe4a8 in content::FileSystemAccessObserverObservation::OnChanges(...)
    #13 0x000309201b94 in base::internal::Invoker<...>::Run(...)
    #14 0x0003091f0388 in base::RepeatingCallback<...>::Run(...)
    #15 0x0003091f1970 in content::FileSystemAccessObservationGroup::NotifyOfChanges(...)
    #16 0x000309217da8 in content::FileSystemAccessWatcherManager::OnRawChange(...)

==63307==ADDITIONAL INFO
MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.

```

**CREDIT INFORMATION**

Reporter credit: asjidkalam

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 39.7 KB)
- [poc.html](attachments/poc.html) (text/html, 4.9 KB)
- [FSA FileSystemAccessWatcherManager UAF PoC.mov](attachments/FSA FileSystemAccessWatcherManager UAF PoC.mov) (video/quicktime, 26.9 MB)

## Timeline

### as...@gmail.com (2026-04-10)

Attaching video PoC.

### fl...@google.com (2026-04-10)

I am able to reproduce with the PoC, thank you! (Note to whoever takes this bug on: I didn't actually need that enable blink feature flag to reproduce the reporter's issue. So it seems like this is a live issue in shipping Chrome builds.)

memmott@: I know it's been a while since you've touched this code, but it's been a while since anyone touched this code :) Could you own this or, if you're not the right person, can you reassign?

### ch...@google.com (2026-04-11)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-11)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### as...@gmail.com (2026-04-18)

Hi team,

Just following up, are there any updates on this issue or its current status?

Please let me know if additional repro details, testing, or clarification would be useful from my side.

### fe...@google.com (2026-05-01)

I think I am going to revert the CL that introduced RemoveObserver in the process of fixing [b/497429850](https://issues.chromium.org/issues/497429850). So that should take care of this.

### fe...@google.com (2026-05-08)

For the record, I could not repro this at 1662dfcb5d85dcdedd49c235a22f87448a04fe94 with the attached code.

### as...@gmail.com (2026-05-09)

Thanks for checking.

That makes sense. The issue was reproduced on Apr 11 against the ASAN build I reported with, but at **1662dfcb5d85dcdedd49c235a22f87448a04fe94** the relevant `OnRawChange()` signature now passes `FileSystemAccessWatchScope` by value, with a comment noting this avoids UAF when notifications synchronously destroy the source owning the original scope.

So I agree the attached PoC may no longer reproduce at **1662dfcb** because the specific reported path appears fixed by/before that revision. My understanding is that it was still valid at report time, since it was reproduced and treated as a live shipping issue then.

Please let me know if you need anything else from my side.

### dx...@google.com (2026-05-15)

Project: chromium/src  

Branch:  main  

Author:  Fergal Daly [fergal@chromium.org](mailto:fergal@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7805573>

Revert "[FSA] Quick fix UAF in FileSystemAccessBucketPathWatcher"

---


Expand for full commit details
```
     
    This reverts commit cfafd4297bbd2fad851e37fe145ab3eaf987dad6. 
     
    This was an attempted fix but the POC still reproduces and it causes 
    other UAFs. 
     
    Reverting it is a step towards landing a more comprehensive fix in 
    https://crrev.com/c/7805989/15 
     
    Bug: 497429850 
    Fixed: 501115599 
    Change-Id: I613c143bc0ae52ebf7103dcc0f8b3ccc5217fb8a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7805573 
    Commit-Queue: Fergal Daly <fergal@chromium.org> 
    Reviewed-by: Ming-Ying Chung <mych@chromium.org> 
    Reviewed-by: Kalvin Lee <kdlee@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1631136}

```

---

Files:

- M `content/browser/file_system_access/file_system_access_bucket_path_watcher.cc`
- M `content/browser/file_system_access/file_system_access_bucket_path_watcher.h`
- M `storage/browser/file_system/sandbox_file_system_backend_delegate.cc`
- M `storage/browser/file_system/sandbox_file_system_backend_delegate.h`
- M `storage/browser/file_system/sandbox_file_system_backend_delegate_unittest.cc`
- M `storage/browser/file_system/task_runner_bound_observer_list.h`

---

Hash: [61f666cc52225e0386741b772b4fc60e7777aef4](https://chromiumdash.appspot.com/commit/61f666cc52225e0386741b772b4fc60e7777aef4)  

Date: Fri May 15 07:55:34 2026


---

### ch...@google.com (2026-05-20)

Requesting merge to M148 because latest trunk commit is in 150.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M149 because latest trunk commit is in 150.

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514925814](https://crbug.com/514925814) to have this merge reviewed.**

### ch...@google.com (2026-05-20)

**M149** merge request created. **Please update [crbug/514929217](https://crbug.com/514929217) to have this merge reviewed.**

### fe...@google.com (2026-05-27)

I closed the M148 merge as that doesn't have the CL I'm reverting. The rest of the fix landed in <https://crrev.com/c/7805989> which I'm CPing in another bug.

### dx...@google.com (2026-05-27)

Project: chromium/src  

Branch:  refs/branch-heads/7827  

Author:  Fergal Daly [fergal@chromium.org](mailto:fergal@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7878605>

[M149] Revert "[FSA] Quick fix UAF in FileSystemAccessBucketPathWatcher"

---


Expand for full commit details
```
     
    Original change's description: 
    > Revert "[FSA] Quick fix UAF in FileSystemAccessBucketPathWatcher" 
    > 
    > This reverts commit cfafd4297bbd2fad851e37fe145ab3eaf987dad6. 
    > 
    > This was an attempted fix but the POC still reproduces and it causes 
    > other UAFs. 
    > 
    > Reverting it is a step towards landing a more comprehensive fix in 
    > https://crrev.com/c/7805989/15 
    > 
    > Bug: 497429850 
    > Fixed: 501115599 
    > Change-Id: I613c143bc0ae52ebf7103dcc0f8b3ccc5217fb8a 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7805573 
    > Commit-Queue: Fergal Daly <fergal@chromium.org> 
    > Reviewed-by: Ming-Ying Chung <mych@chromium.org> 
    > Reviewed-by: Kalvin Lee <kdlee@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1631136} 
     
    (cherry picked from commit 61f666cc52225e0386741b772b4fc60e7777aef4) 
     
    Bug: 514929217,497429850,501115599 
    Change-Id: I613c143bc0ae52ebf7103dcc0f8b3ccc5217fb8a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7878605 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7827@{#1840} 
    Cr-Branched-From: 9f3e9aaccba63bd2ec30334e45e0bfd07ebcc8f1-refs/heads/main@{#1625079}

```

---

Files:

- M `content/browser/file_system_access/file_system_access_bucket_path_watcher.cc`
- M `content/browser/file_system_access/file_system_access_bucket_path_watcher.h`
- M `storage/browser/file_system/sandbox_file_system_backend_delegate.cc`
- M `storage/browser/file_system/sandbox_file_system_backend_delegate.h`
- M `storage/browser/file_system/sandbox_file_system_backend_delegate_unittest.cc`
- M `storage/browser/file_system/task_runner_bound_observer_list.h`

---

Hash: [f72060ed133f01a64f8f3f1827673a15ed4d4c32](https://chromiumdash.appspot.com/commit/f72060ed133f01a64f8f3f1827673a15ed4d4c32)  

Date: Wed May 27 09:59:23 2026


---

### pe...@google.com (2026-05-27)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2026-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
Mildly Mitigated. Sandbox escape / Memory corruption in a non-sandboxed process.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### qk...@google.com (2026-07-09)

Add `LTS-NotApplicable-144` label because M144 doesn't have the suspected CL.

### ch...@google.com (2026-08-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/501115599)*

# Security: heap-use-after-free in ScopedResourceUsageQuery::NotifyObservers

| Field | Value |
|-------|-------|
| **Issue ID** | [327696052](https://issues.chromium.org/issues/327696052) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>PerformanceManager |
| **Platforms** | Linux, Mac |
| **Chrome Version** | 122.0.6261.94 |
| **Reporter** | zh...@gmail.com |
| **Assignee** | jo...@google.com |
| **Created** | 2024-03-01 |
| **Bounty** | $4,000.00 |

## Description

# Steps to reproduce the problem

1. In order to reproduce this vulnerability stably, we need to compile an asan chrome locally. The commit I chose to reproduce the vulnerability is:
   `git checkout 80a4b049ae9d4b5abea7333a661a1644f11b5a70`
2. `git apply trigger.diff` can trigger vulnerabilities more stably and conveniently
3. Start chrome like this: `./out/asan/Chromium.app/Contents/MacOS/Chromium --user-data-dir=/tmp/noexists1`.When this line of log is printed:`in ScopedResourceUsageQuery::NotifyObservers === === zh1x1an:`, UAF can be triggered by closing chromium.Triggering this vulnerability does not require enabling any additional features

# Problem Description

## RCA and Bisect here

The object: `performance_manager::metrics::PageResourceMonitor` that triggers the UAF vulnerability is created here [1]

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/performance_manager/chrome_browser_main_extra_parts_performance_manager.cc;l=206-207?q=chrome_browser_main_extra_parts_performance_manager.cc:207>

```
  graph->PassToGraph(
      std::make_unique<performance_manager::metrics::PageResourceMonitor>());

```

In the `GraphImpl` class, a `graph_owned_` is stored:

[2] <https://source.chromium.org/chromium/chromium/src/+/main:components/performance_manager/graph/graph_impl.h;l=281-285>

```
  // Graph-owned objects. For now we only expect O(10) clients, hence the
  // flat_map.
  OwnedObjects<GraphOwned,
               /* CallbackArgType = */ Graph*,
               &GraphOwned::OnPassedToGraph,
               &GraphOwned::OnTakenFromGraph>
      graph_owned_ GUARDED_BY_CONTEXT(sequence_checker_);

```

When Chrome starts, the `GraphImpl` object will be created and call `GraphImpl::PassToGraphImpl` [3], adding multiple objects (approximately more than 30) to `graph_owned_`, which will also add my latest at the position of [1] The `performance_manager::metrics::PageResourceMonitor` object mentioned at the beginning.

[3] <https://source.chromium.org/chromium/chromium/src/+/main:components/performance_manager/graph/graph_impl.cc;l=273-276;drc=f4a00cc248dd2dc8ec8759fb51620d47b5114090;bpv=0;bpt=1>

When chrome is closed, `graph_owned_.ReleaseObjects(this);` in `GraphImpl::TearDown` will be called to release all objects initially added.

[4] <https://source.chromium.org/chromium/chromium/src/+/main:components/performance_manager/graph/graph_impl.cc;l=193;drc=f4a00cc248dd2dc8ec8759fb51620d47b5114090;bpv=0;bpt=1>

The implementation of `ReleaseObjects` is as follows:

[5] <https://source.chromium.org/chromium/chromium/src/+/main:components/performance_manager/owned_objects.h;l=83-91;drc=f4a00cc248dd2dc8ec8759fb51620d47b5114090;bpv=1;bpt=1>

```
  // Releases all the objects owned by this container, invoking their
  // OnTakenFunctionPtr as they are released.
  template <typename... ArgTypes>
  void ReleaseObjects(ArgTypes... args) {
    // Release the last object first to be friendly with base::flat_set, which
    // is actually a std::vector.
    while (!objects_.empty())
      TakeObject(objects_.rbegin()->get(), std::forward<ArgTypes>(args)...);
  }

```

This will free `performance_manager::metrics::PageResourceMonitor`.

However, we can still use this object after it is released. Take a look at the code at this location [6]

[6] <https://source.chromium.org/chromium/chromium/src/+/main:components/performance_manager/resource_attribution/queries.cc;l=226-231?q=queries.cc:226>

```
void ScopedResourceUsageQuery::NotifyObservers(
    scoped_refptr<ObserverList> observer_list,
    const QueryResultMap& results) {
  observer_list->Notify(FROM_HERE, &QueryResultObserver::OnResourceUsageUpdated,
                        results);
}

```

When the battery status of the device is updated, such as unplugging the device, or restarting charging, etc., `ScopedResourceUsageQuery::NotifyObservers` will be called to notify observers of the change in status. However, at this time, `performance_manager::metrics::PageResourceMonitor` may have been released, eventually leading to UAF.

Triggering this vulnerability does not require any feature to be enabled. Since this is a UAF caused by a conditional race, I added sleep to the `trigger.diff` file to trigger this vulnerability more conveniently. As I mentioned in the reproduction steps, when the log in the `trigger.diff` file prints, if chrome is closed at that point, then the object is released, eventually successfully triggering the UAF at the `ScopedResourceUsageQuery::NotifyObservers` location.

I'll provide Bisect commit information later.

# Summary

Security: heap-use-after-free in ScopedResourceUsageQuery::NotifyObservers

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 48.4 KB)
- [trigger.diff](attachments/trigger.diff) (text/x-diff, 1.0 KB)
- [poc.mov](attachments/poc.mov) (video/quicktime, 13.2 MB)
- asan.txt (text/plain, 84.8 KB)
- [asan-122.txt](attachments/asan-122.txt) (text/plain, 76.9 KB)

## Timeline

### zh...@gmail.com (2024-03-01)

According to my previous analysis, bisect commit should be this:

https://chromium-review.googlesource.com/c/chromium/src/+/5024679

Vulnerability fix suggestions:

I think you can consider checking the survival of the `performance_manager::metrics::PageResourceMonitor` object first, and then calling `ScopedResourceUsageQuery::NotifyObservers` to notify observers of status updates.

If you have any other questions or findings, please let me know, thanks!

### zh...@gmail.com (2024-03-02)

To add, it is recommended to use MacOS to reproduce, because I have not tried to reproduce on other systems. So far, all I can 100% guarantee is that macos can definitely reproduce.


### ti...@chromium.org (2024-03-04)

[Security shepherd] Thanks for the report! It sounds reasonable.

> When chrome is closed

Memory corruption in the browser process is mitigated slightly by the requirement that Chrome must be shutting down. Setting High severity provisionally.

I will attempt to reproduce.

### ti...@chromium.org (2024-03-04)

Built Chrome with the patch, ran it, but lost the race to the sleep. Trying again.

### ti...@chromium.org (2024-03-04)

Reproduced successfully!

### ti...@chromium.org (2024-03-04)

ASAN log.

### ti...@chromium.org (2024-03-04)

This was at HEAD (commit 195be11b6b2f714bb9a38c5d749b78aa94135ac6).

### ti...@chromium.org (2024-03-04)

Trying to reproduce on 122: commit `2fe869e04f3d4a697f29e6324d4a4219e96d9d1c` (`refs/branch-heads/6261`)

### zh...@gmail.com (2024-03-04)

It looks good, asan log is exactly as expected.

### ti...@chromium.org (2024-03-04)

Reproduced! ASAN log attached.

### ti...@chromium.org (2024-03-04)

[Security shepherd] Assigning to fdoray@ for further triage. Here's a UaF in the browser process at shutdown - it reproduces consistently for me at HEAD and on Extended Stable with a patch to increase the race condition window. Can you please take it from here?

### pe...@google.com (2024-03-04)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-03-04)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### jo...@google.com (2024-03-04)

I'm back from vacation today, so I can take this on.

If PageResourceMonitor is freed, it should have removed itself from the observer list. It looks it relied on the destructor to free the ScopedResourceUsageQuery it owns, assuming that this would automatically clear the observer list, but since ScopedResourceUsageQuery uses ObserverListThreadSafe it can outlive the query object briefly.

> When the battery status of the device is updated, such as unplugging the device, or restarting charging, etc., ScopedResourceUsageQuery::NotifyObservers will be called to notify observers of the change in status.

ScopedResourceUsageQuery doesn't monitor battery status, it (currently) just measures CPU and/or memory usage of various Chrome objects on a timer.

I don't think the race condition is wide enough for this to be an S1 vulnerability. Although ScopedResourceUsageQuery is written to use sequence-agnostic observers, the PageResourceMonitor happens to be deleted on the PM sequence, which is the same sequence the measurements happen on. So the timeline here is:

1. Timer fires, causing an asynchronous measurement on the PM sequence.
2. Simultaneously to (1), browser shutdown begins on the main thread.
   1. This posts a task to the PM sequence to delete all GraphOwned objects. (The ThreadPool isn't shut down yet so tasks can still be posted.)
3. `QueryScheduler::OnResultsReceived` is called on the PM sequence with the measurement results.
   1. OnResultsReceived invokes its notification callback...
   2. ...which calls `ScopedResourceUsageQuery::NotifyObservers`...
   3. ...which calls `ObserverListThreadSafe::Notify`...
   4. ...which posts a task to the sequence that owns the observer list (which happens to also be the PM sequence).

At this point there are 3 references to the `ObserverListThreadSafe`, owned by `ScopedResourceUsageQuery`, `QueryScheduler`, and the queued notification task.

4. The task from (2.1) runs on the PM sequence to delete all the GraphOwned objects are deleted on the PM sequence. (The `ThreadPool` isn't shutdown yet so tasks will run.)
   1. `QueryScheduler` is deleted and drops its reference to the `ObserverListThreadSafe`. (Depending on the order of destruction this may happen at the end of step 4 instead, but it doesn't change anything.)
   2. `PageResourceMonitor`'s destructor deletes the `ScopedResourceUsageQuery`.
   3. `ScopedResourceUsageQuery`'s destructor posts a task to the PM sequence to call `QueryScheduler::RemoveScopedQuery`.
   4. `ScopedResourceUsageQuery` drops its reference to the `ObserverListThreadSafe`.
5. The notification task from (3.4) runs on the PM sequence (OOPS), then drops its reference to the `ObserverListThreadSafe`.
6. The `QueryScheduler::RemoveScopedQuery` task from (4.3) is up next on the PM sequence but is dropped because the `QueryScheduler` was deleted. (That's ok because it would just have the scheduler drop its reference to the `ObserverListThreadSafe`, which already happened in the destructor.

The problem happens because of the exact order that tasks (2.1) and (3.4) are posted. If `OnResultsReceived` had run before task (2.1) was posted, (3.4) would happen first and sucessfully deliver the notification before `PageResourceMonitor` is destroyed. And if it had been queued after task (2.1), `QueryScheduler` would be deleted when it was time to run it, so it would just be dropped and task (3.4) would never be posted.

To exploit this an attacker would need to place an object on the heap AFTER a measurement finishes (step 3) and AFTER shutdown begins (step 4), but before the task posted at step 3 runs. Even if they had an information leak to know when the measurement would finish, and a way to force browser shutdown, that's a very narrow window. The only way I can see to widen it is to flood the PM task sequence, but they would have to START the flood after task (2.1) is queued (so they don't delay it) and before task (3.4) is queued (so they DO delay it), which is just moving the narrow timing requirement to a different spot.

### jo...@google.com (2024-03-04)

Fix in review at <https://crrev.com/c/5341335>

### ti...@chromium.org (2024-03-05)

IIUC the fix makes it so that there step 4.2. instead becomes: "`PageResourceMonitor`'s destructor deletes the `ScopedQueryObservation`, which removes the `ScopedResourceUsageQuery` from `QueryScheduler`'s observer list synchronously.". This in turn means that when the task scheduled at 2.4. attempts to run, it does nothing instead? Or it gets cancelled outright before executing?

### ti...@chromium.org (2024-03-05)

The doc comment on `ObserverListThreadSafe` [1] states:

```
//    * If one sequence is notifying observers concurrently with an observer
//      removing itself from the observer list, the notifications will be
//      silently dropped.

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:base/observer_list_threadsafe.h;l=44-46;drc=7eda6612cc73c55d5c6e7febce7e6e827640dbef>

### ap...@google.com (2024-03-05)

Project: chromium/src
Branch: main

commit 255c8341c067b7191c9430cf39556c6f7660df56
Author: Joe Mason <joenotcharles@google.com>
Date:   Tue Mar 05 09:37:20 2024

    Use ScopedObservation in PageResourceMonitor
    
    This unregisters the observer in its destructor, preventing
    PageResourceMonitor from forgetting to unregister on shutdown.
    
    Bug: 327696052
    Change-Id: I9eca2aa32e42f1371a792326a07790c9cd9892d8
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5341335
    Auto-Submit: Joe Mason <joenotcharles@google.com>
    Reviewed-by: Titouan Rigoudy <titouan@chromium.org>
    Commit-Queue: Titouan Rigoudy <titouan@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1268334}

M       chrome/browser/performance_manager/metrics/page_resource_monitor.cc
M       chrome/browser/performance_manager/metrics/page_resource_monitor.h

https://chromium-review.googlesource.com/5341335


### jo...@google.com (2024-03-05)

> IIUC the fix makes it so that there step 4.2. instead becomes: "PageResourceMonitor's destructor deletes the ScopedQueryObservation, which removes the ScopedResourceUsageQuery from QueryScheduler's observer list synchronously.". This in turn means that when the task scheduled at 2.4. attempts to run, it does nothing instead? Or it gets cancelled outright before executing?

Silently dropped, which is guaranteed by `ObserverListThreadSafe` as you noted.

### zh...@gmail.com (2024-03-06)

Thanks for the quick fix and the very detailed analysis, it's very helpful, the fix is reasonable, learned a lot

### pe...@google.com (2024-03-06)

Requesting merge to stable (M122) because latest trunk commit (1268334) appears to be after stable branch point (1250580).
Requesting merge to beta (M123) because latest trunk commit (1268334) appears to be after beta branch point (1262506).
Merge review required: M122 is already shipping to stable.


Merge review required: M123 is already shipping to beta.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [122, 123].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### am...@chromium.org (2024-03-08)

There are no issues observed on Canary from this fix since it was landed
<https://crrev.com/c/5341335> approved for merge to M123 and M122
Please merge this fix to M123 Beta / branch 6312 and M122 Stable / branch 6261 at your earliest convenience so this fix can be included in the next respective updates.

Just a note for both joenotcharles@ and the Release Managers, M122 Stable cut for next week's Stable channel release is tomorrow at ~ 10am PST.
If this fix can be merged before then that would be great, but there is no rush needed here. Due to the timing of when this fix was landed, it was given the minimal bake time before approval. If this fix can be included in tomorrow's cut, great, but it's not necessary to hold Stable cut or rush merging this fix for it to be included.

If this misses M122 Stable release for next week, it will instead be shipped the first M123 Stable release the following week.
It should still be backmerged to M122 however, since M122 will be promoted to Extended Stable channel on 19 March.

### jo...@google.com (2024-03-08)

The patch doesn't cherry-pick cleanly to M122 because it uses an alias `resource_attribution::ScopedQueryObservation` that didn't exist yet in that branch.

### ap...@google.com (2024-03-09)

Project: chromium/src
Branch: refs/branch-heads/6312

commit cc990d1014c1b32aba943d0c5bb47fe4469d40fc
Author: Joe Mason <joenotcharles@google.com>
Date:   Fri Mar 08 23:59:44 2024

    Use ScopedObservation in PageResourceMonitor
    
    This unregisters the observer in its destructor, preventing
    PageResourceMonitor from forgetting to unregister on shutdown.
    
    (cherry picked from commit 255c8341c067b7191c9430cf39556c6f7660df56)
    
    Bug: 327696052
    Change-Id: I9eca2aa32e42f1371a792326a07790c9cd9892d8
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5341335
    Auto-Submit: Joe Mason <joenotcharles@google.com>
    Reviewed-by: Titouan Rigoudy <titouan@chromium.org>
    Commit-Queue: Titouan Rigoudy <titouan@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1268334}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5357035
    Commit-Queue: Joe Mason <joenotcharles@google.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6312@{#487}
    Cr-Branched-From: 6711dcdae48edaf98cbc6964f90fac85b7d9986e-refs/heads/main@{#1262506}

M       chrome/browser/performance_manager/metrics/page_resource_monitor.cc
M       chrome/browser/performance_manager/metrics/page_resource_monitor.h

https://chromium-review.googlesource.com/5357035


### jo...@google.com (2024-03-11)

Merge to M122 is in review at <https://crrev.com/c/5352142>

### ap...@google.com (2024-03-11)

Project: chromium/src
Branch: refs/branch-heads/6261

commit f18a44fedeb29764b2b5336c120fdd90ef1a3f5c
Author: Joe Mason <joenotcharles@google.com>
Date:   Mon Mar 11 21:37:15 2024

    Use ScopedObservation in PageResourceMonitor
    
    This unregisters the observer in its destructor, preventing
    PageResourceMonitor from forgetting to unregister on shutdown.
    
    (cherry picked from commit 255c8341c067b7191c9430cf39556c6f7660df56)
    
    Bug: 327696052
    Change-Id: I9eca2aa32e42f1371a792326a07790c9cd9892d8
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5341335
    Auto-Submit: Joe Mason <joenotcharles@google.com>
    Reviewed-by: Titouan Rigoudy <titouan@chromium.org>
    Commit-Queue: Titouan Rigoudy <titouan@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1268334}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5352142
    Reviewed-by: Prudhvikumar Bommana <pbommana@google.com>
    Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>
    Reviewed-by: Steven Luong <stluong@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6261@{#1057}
    Cr-Branched-From: 9755d9d81e4a8cb5b4f76b23b761457479dbb06b-refs/heads/main@{#1250580}

M       chrome/browser/performance_manager/metrics/page_resource_monitor.cc
M       chrome/browser/performance_manager/metrics/page_resource_monitor.h

https://chromium-review.googlesource.com/5352142


### am...@google.com (2024-03-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-14)

Congratulations! The Chrome VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security in a non-sandboxed process, mitigated by difficult to win race condition and shutdown, + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us!

### zh...@gmail.com (2024-03-15)

Thanks🫡🍻

### pe...@google.com (2024-06-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/327696052)*

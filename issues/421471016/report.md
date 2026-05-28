# UAF in StackSampler

| Field | Value |
|-------|-------|
| **Issue ID** | [421471016](https://issues.chromium.org/issues/421471016) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Metrics>SamplingProfiler |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 136.0.0.0 |
| **Reporter** | ha...@gmail.com |
| **Assignee** | th...@google.com |
| **Created** | 2025-05-31 |
| **Bounty** | $4,000.00 |

## Description

# Steps to reproduce the problem

Will attach details soon. See asan.txt for stack trace

# Problem Description

UAF in StackSampler

# Summary

UAF in StackSampler

# Custom Questions

#### Type of crash:

browser UAF

#### Crash state:

See asan.txt

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 93.0 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 93.0 KB)
- [fuzz_c5a39b1725b58e96ef18a1a0a1257893.html](attachments/fuzz_c5a39b1725b58e96ef18a1a0a1257893.html) (text/html, 107.6 KB)

## Timeline

### ha...@gmail.com (2025-05-31)

This UAF in StackSampler in found by the my webpage fuzzing accidentally. After analyzing the related ASAN trace, the root cause is clear and apparently shows the UAF is caused by the race condition for accessing the non\_native\_modules\_ between the sampling thread and the thread pool.

## Detail Analysis

StackSampler::WalkStack iters `non_native_modules_` (by `GetModuleForAddress`) to find out the actual module according to the address on a dedicated thread, while another persistent thread (i.e., sampling thread) periodically updates the `non_native_modules_` by calling `V8Unwinder::UpdateModules`. The main issue is that non\_native\_modules\_ is `std::flat_set`, which is iterated by `WalkStack` on one thread, while this `std::flat_set` is updated/moved on another sampling thread, causing the typical iter during move/free issue.

Firstly, we name two threads T1 and T2:

- T1: the sampling thread (created in <https://source.chromium.org/chromium/chromium/src/+/main:base/profiler/stack_sampling_profiler.cc;l=396-402;drc=103fe70ba39111be1ce8036a318c72c6cfed654b>)
- T2: the thread pool created by sampler (see below code for details, the T2 is actually the thread managed by `thread_pool_runner_`)

<https://source.chromium.org/chromium/chromium/src/+/main:base/profiler/stack_sampler.cc;l=103-111;drc=0dc30698370bcde67dda4f48b7ca19bf4c1dbc17>

```
void StackSampler::Initialize() {
  was_initialized_ = true;
  unwind_data_->Initialize(std::move(unwinders_factory_).Run());
  thread_pool_runner_ = base::ThreadPool::CreateSequencedTaskRunner({});

  // The thread pool might not start right away (or it may never start), so we
  // schedule a job and wait for it to become running before we schedule other
  // work.
  thread_pool_runner_->PostTaskAndReply(
      FROM_HERE, base::DoNothing(),
      base::BindOnce(&StackSampler::ThreadPoolRunning,
                     weak_ptr_factory_.GetWeakPtr()));
}

```

Secondly, we dive into the definition of `non_native_modules_` in `ModuleCache`, which is a `std::flat_set` of `std::unique_ptr<const Module>`.

<https://source.chromium.org/chromium/chromium/src/+/main:base/profiler/module_cache.h;l=176-185;drc=11b3fa7f7f9733dfecb31281808647dc17e2691c>

```
  // Set of non-native modules currently mapped into the address space, sorted
  // by base address. Represented as flat_set because std::set does not support
  // extracting move-only element types prior to C++17's
  // std::set<>::extract(). The non-native module insertion/removal patterns --
  // initial bulk insertion, then infrequent inserts/removals -- should work
  // reasonably well with the flat_set complexity guarantees. Separate from
  // native_modules_ to support preferential lookup of non-native modules
  // embedded in native modules; see comment on UpdateNonNativeModules().
  base::flat_set<std::unique_ptr<const Module>, ModuleAndAddressCompare>
      non_native_modules_;

```
#### Use Point [1]:

Thirdly, we delve into the `StackSampler::WalkStack` and `ModuleCache::GetModuleForAddress` to see how the `non_native_modules_` is accessed in the **USE POINT** (of the use-after-free) on thread T2.

The delayed task of &SamplingThread::RecordSampleTask will be posted on the sampling thread (T1). And it has the following call chain:
`SamplingThread::RecordSampleTask` (T1) -> `StackSamplingProfiler::SamplingThread::RecordSampleTask` (T1) -> `StackSampler::RecordStackFrames` (T1) -> `StackSampler::RecordStackFrames` (T1)

<https://source.chromium.org/chromium/chromium/src/+/main:base/profiler/stack_sampling_profiler.cc;l=662-666;drc=0dc30698370bcde67dda4f48b7ca19bf4c1dbc17>

```
  GetTaskRunnerOnSamplingThread()->PostDelayedTask(
      FROM_HERE,
      BindOnce(&SamplingThread::RecordSampleTask, Unretained(this),
               collection_id),
      initial_delay);

```

<https://source.chromium.org/chromium/chromium/src/+/main:base/profiler/stack_sampling_profiler.cc;l=737-742;drc=0dc30698370bcde67dda4f48b7ca19bf4c1dbc17>

[On Sampling Thread]

```
void StackSamplingProfiler::SamplingThread::RecordSampleTask(
    int collection_id) {
….
  collection->sampler->RecordStackFrames(
      stack_buffer_.get(), collection->thread_id,
      more_collections_remaining
          ? DoNothing()
          : BindOnce(&SamplingThread::RemoveCollectionTask, Unretained(this),
                     collection_id));

```

<https://source.chromium.org/chromium/chromium/src/+/main:base/profiler/stack_sampler.cc;l=262-276;drc=025a94257380eadfad2d705129e5863fca0bf89e>

[On Sampling Thread]

```
void StackSampler::RecordStackFrames(StackBuffer* stack_buffer,
                                     PlatformThreadId thread_id,
                                     base::OnceClosure done_callback) {
….
  if (thread_pool_ready_) {
    // Since `stack_buffer` needs to be the maximum stack size and be
    // preallocated it tends to be much larger than the actual stack size. So we
    // copy the stack here that is a smaller size before passing it over to the
    // worker. To allocate a `StackBuffer` for every sample not be good.
    std::unique_ptr<StackBuffer> cloned_stack =
        stack_copier_->CloneStack(*stack_buffer, &stack_top, &thread_context);
    thread_pool_runner_->PostTaskAndReplyWithResult(
        FROM_HERE,
        base::BindOnce(
            [](StackUnwindData* unwind_data,
               std::vector<UnwinderCapture> unwinders,
               RegisterContext thread_context,
               std::unique_ptr<StackBuffer> stack, uintptr_t stack_top) {
              return WalkStack(unwind_data->module_cache(), &thread_context,
                               stack_top, std::move(unwinders));
            },
            base::Unretained(unwind_data_.get()), std::move(unwinders),
            OwnedRef(thread_context), std::move(cloned_stack), stack_top),
        base::BindOnce(&StackSampler::UnwindComplete,
                       weak_ptr_factory_.GetWeakPtr(), timestamp,
                       std::move(done_callback)));
  } else {
    auto frames = WalkStack(unwind_data_->module_cache(), &thread_context,
                            stack_top, std::move(unwinders));
    UnwindComplete(timestamp, std::move(done_callback), std::move(frames));
  }

```

In ``StackSampler::RecordStackFrames`(T1), when`thread\_pool\_ready\_` is true, (i.e., the thread pool is ready), it will post a task to the thread pool (T2) to call `StackSampler::WalkStack`. Consequently, it calls `ModuleCache::GetExistingModuleForAddress` and finally calls `non\_native\_modules\_.find(address)` to iterate the `non\_native\_modules\_` on \*\* T2 \*\* in [1].

<https://source.chromium.org/chromium/chromium/src/+/main:base/profiler/stack_sampler.cc;l=345-347;drc=0dc30698370bcde67dda4f48b7ca19bf4c1dbc17>

[On T2]

```
// static
std::vector<Frame> StackSampler::WalkStack(
    ModuleCache* module_cache,
    RegisterContext* thread_context,
    uintptr_t stack_top,
    std::vector<UnwinderCapture> unwinders) {
  std::vector<Frame> stack;
  // Reserve enough memory for most stacks, to avoid repeated
  // allocations. Approximately 99.9% of recorded stacks are 128 frames or
  // fewer.
  stack.reserve(128);

  // Record the first frame from the context values.
  stack.emplace_back(RegisterContextInstructionPointer(thread_context),
                     module_cache->GetModuleForAddress( // Calls GetModuleForAddress from the module_cache
                         RegisterContextInstructionPointer(thread_context)));

```

<https://source.chromium.org/chromium/chromium/src/+/main:base/profiler/module_cache.cc;l=156;drc=025a94257380eadfad2d705129e5863fca0bf89e>

```
const ModuleCache::Module* ModuleCache::GetExistingModuleForAddress(
    uintptr_t address) const {
  const auto non_native_module_loc = non_native_modules_.find(address); // [1] iterate non_native_modules_ on T2, while this `non_native_modules_` is moved/freed on T1.

```
#### Free Point [2]:

In the free point, the `non_native_modules_` is moved/freed on the sampling thread (T1). It has the following call chain `SamplingThread::AddCollectionTask` -> `SamplingThread::RecordSampleTask` (T1) -> `StackSampler::RecordStackFrames` (T1) -> `V8Unwinder::UpdateModules` (T1) -> `ModuleCache::UpdateNonNativeModules` (T1) -> `non_native_modules_.insert`[2] (T1)

Therefore, the `non_native_modules_` is moved/freed on T1 in [2], while the `non_native_modules_` is iterated on T2 in [1], causing the use-after-free.

<https://source.chromium.org/chromium/chromium/src/+/main:base/profiler/stack_sampling_profiler.cc;l=662-666;drc=0dc30698370bcde67dda4f48b7ca19bf4c1dbc17>

```
void StackSamplingProfiler::SamplingThread::AddCollectionTask(
    std::unique_ptr<CollectionContext> collection) {
  DCHECK_EQ(GetThreadId(), PlatformThread::CurrentId());

  const int collection_id = collection->collection_id;
  const TimeDelta initial_delay = collection->params.initial_delay;

  collection->sampler->Initialize();

  active_collections_.insert(
      std::make_pair(collection_id, std::move(collection)));

  GetTaskRunnerOnSamplingThread()->PostDelayedTask(
      FROM_HERE,
      BindOnce(&SamplingThread::RecordSampleTask, Unretained(this),
               collection_id),
      initial_delay);

  // Another increment of "add events" serves to invalidate any pending
  // shutdown tasks that may have been initiated between the Add() and this
  // task running.
  {
    AutoLock lock(thread_execution_state_lock_);
    ++thread_execution_state_add_events_;
  }
}

```

<https://source.chromium.org/chromium/chromium/src/+/main:base/profiler/stack_sampling_profiler.cc;l=737-742;drc=0dc30698370bcde67dda4f48b7ca19bf4c1dbc17>

[On Sampling Thread]

```
void StackSamplingProfiler::SamplingThread::RecordSampleTask(
    int collection_id) {
  DCHECK_EQ(GetThreadId(), PlatformThread::CurrentId());

  auto found = active_collections_.find(collection_id);

  // The task won't be found if it has been stopped.
  if (found == active_collections_.end()) {
    return;
  }

  CollectionContext* collection = found->second.get();

  // If we are in the process of stopping just don't collect a stack
  // trace as that would cause further jobs to be scheduled.
  if (collection->stopping) {
    return;
  }

  // If this is the first sample, the collection params need to be filled.
  if (collection->sample_count == 0) {
    collection->profile_start_time = TimeTicks::Now();
    collection->next_sample_time = TimeTicks::Now();
  }

  bool more_collections_remaining =
      ++collection->sample_count < collection->params.samples_per_profile;
  // Record a single sample.
  collection->sampler->RecordStackFrames( // calls RecordStackFrames of sampler
      stack_buffer_.get(), collection->thread_id,
      more_collections_remaining
          ? DoNothing()
          : BindOnce(&SamplingThread::RemoveCollectionTask, Unretained(this),
                     collection_id));

```

<https://source.chromium.org/chromium/chromium/src/+/main:base/profiler/stack_sampler.cc;l=214-216;drc=0dc30698370bcde67dda4f48b7ca19bf4c1dbc17>

[On Sampling Thread]

```
void StackSampler::RecordStackFrames(StackBuffer* stack_buffer,
                                     PlatformThreadId thread_id,
                                     base::OnceClosure done_callback) {
…
  for (const auto& unwinder : unwinders) {
    GetUnwinder(unwinder)->UpdateModules(GetStateCapture(unwinder)); // calls UpdateModules of V8 Unwinder
  }


```

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/renderer/v8_unwinder.cc;l=245-246;drc=0dc30698370bcde67dda4f48b7ca19bf4c1dbc17>

[On Sampling Thread]

// Update the modules based on what was recorded in |code\_ranges\_|. The singular
// embedded code range was already added in in InitializeModules(). It is
// preserved by the algorithm below, which is why kNonEmbedded is
// unconditionally passed when creating new modules.
void V8Unwinder::UpdateModules(base::UnwinderStateCapture\* capture\_state) {
…
module\_cache()->UpdateNonNativeModules(defunct\_modules,
std::move(new\_modules));
}

<https://source.chromium.org/chromium/chromium/src/+/main:base/profiler/module_cache.cc;l=131-133;drc=0dc30698370bcde67dda4f48b7ca19bf4c1dbc17>
[On Sampling Thread]

```
void ModuleCache::UpdateNonNativeModules(
    const std::vector<const Module*>& defunct_modules,
    std::vector<std::unique_ptr<const Module>> new_modules) {

…


  // Insert the modules to be added. This operation is O((m + a) + a*log(a))
  // where m is the number of current modules and a is the number of modules to
  // be added.
  const size_t prior_non_native_modules_size = non_native_modules_.size();
  non_native_modules_.insert(std::make_move_iterator(new_modules.begin()), // [2] This is the point where the `non_native_modules_` is moved/freed on the sampling thread (T1).
                             std::make_move_iterator(new_modules.end()));

```
#### Conclusion

The UAF is caused by the race condition for accessing the `non_native_modules_` between the sampling thread (T1) and the thread pool (T2). The `non_native_modules_` is moved/freed on T1 in [2], while the `non_native_modules_` is iterated on T2 in [1], causing the use-after-free.

## Bisect

As per above analysis, this issue is initially introduced (i.e., the proposed thread pool) by the commit <https://chromium-review.googlesource.com/c/chromium/src/+/5704241> and later enabled by default by the commit <https://chromium-review.googlesource.com/c/chromium/src/+/5833662>

## Suggested Fix

There are two ways to fix this issue:

1. Disable the thread\_pool\_runner\_ and use sampling thread to perform the  `StackSampler::RecordStackFrames`.
2. Use a lock to protect the `non_native_modules_` when iterating it, as `thread_execution_state_lock_` does.

### nh...@chromium.org (2025-06-02)

Thanks for this report. It's unclear how to trigger this crash - are you able to provide a poc or steps to reproduce it?

dtapuska: I can't reproduce this issue based on the information provided, but if you can diagnose and fix the issue, please proceed accordingly. For triage purposes, I'm setting the severity to S0 based on this being memory corruption in the browser process, and setting it to all OSes. If you determine that there are specific conditions needed to trigger this crash or that it can only occur on certain platforms, that would be useful information for the Security Team.

### ch...@google.com (2025-06-03)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-06-03)

Setting Priority to P0 to match Severity s0. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dt...@chromium.org (2025-06-03)

Sending this over to the current owners of Stack Sampling Metrics. I don't necessarily have time for an involved fix and feel the OWNERs of the code in question should investigate it first. Sean let me know if you have concerns with that.

### am...@chromium.org (2025-06-03)

It looks like there is some actionable information missing here to consider this to be critical severity, we definitely need a reproducer/testcase/poc of some kind or steps to reproduce.
It also appears that the asan stack trace is missing the process command line data as part of the `additional info`.
I've downgraded this to high severity from critical in the meantime given that we cannot expect owning engineers to respond within the timeframe / SLO expected for Critical severity bugs without necessary actionable information to investigate this issue.

Setting this to needs-feedback, OP / reporter, at soonest, can you please provide:

- testcase / POC or repro steps
- full command line info
- and gn (args.gn) flags used to trigger this issue

### am...@chromium.org (2025-06-03)

spvm@ if you can investigate this in the interim based on the information provided, that would be excellent; however, we have requested more actionable information here before considering this a critical severity issue

### th...@google.com (2025-06-03)

Thank you for the bug report. Sean is OOO today so I'll take a look

### ha...@gmail.com (2025-06-04)

deleted

### ha...@gmail.com (2025-06-04)

redacted

### pe...@google.com (2025-06-04)

Thank you for providing more feedback. Adding the requester to the CC list.

### pe...@google.com (2025-06-04)

The NextAction date has arrived: 2025-06-04
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### th...@google.com (2025-06-04)

Should fix it: 
https://chromium-review.googlesource.com/c/chromium/src/+/6620528

### dx...@google.com (2025-06-05)

Project: chromium/src  

Branch: main  

Author: Thiabaud Engelbrecht [thiabaud@google.com](mailto:thiabaud@google.com)  

Link:      <https://chromium-review.googlesource.com/6620528>

[ssm] Fix race condition

---


Expand for full commit details
```
     
    This CL fixes a threading issue, by using locks to prevent racy access. 
     
    Bug: 421471016 
    Change-Id: If41796b9eb49aa3f27df175c6be198f47947c4c0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6620528 
    Reviewed-by: Jean-Philippe Gravel <jpgravel@chromium.org> 
    Commit-Queue: Thiabaud Engelbrecht <thiabaud@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1470083}

```

---

Files:

- M `base/profiler/module_cache.cc`
- M `base/profiler/module_cache.h`

---

Hash: e9e247c09b76dc6813c70d2c7007438c830bea56  

Date:  Thu Jun 5 18:18:54 2025


---

### ha...@gmail.com (2025-06-06)

deleted

### th...@google.com (2025-06-06)

Perfect, thanks for finding this!

### ch...@google.com (2025-06-07)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M136. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M137. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M138. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [136, 137, 138].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### sp...@google.com (2025-06-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
$3,000 for report of moderately mitigated memory corruption in a non-sandboxed process, mitigated by race and lower potential for reliable attacker control and exploitability + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-06-11)

Thank you for your efforts and reporting this issue to us!

### am...@chromium.org (2025-06-12)

no issues on Canary (post this fix landing) related to this code, please go ahead and merge <https://crrev.com/c/6620528> to M138 Beta / branch 7204 and M137 Stable / branch 7151

### ch...@google.com (2025-06-16)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-06-16)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2025-06-16)

Project: chromium/src  

Branch: refs/branch-heads/7151  

Author: Thiabaud Engelbrecht [thiabaud@google.com](mailto:thiabaud@google.com)  

Link:      <https://chromium-review.googlesource.com/6647090>

[ssm] Fix race condition

---


Expand for full commit details
```
     
    This CL fixes a threading issue, by using locks to prevent racy access. 
     
    (cherry picked from commit e9e247c09b76dc6813c70d2c7007438c830bea56) 
     
    Bug: 421471016 
    Change-Id: If41796b9eb49aa3f27df175c6be198f47947c4c0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6620528 
    Reviewed-by: Jean-Philippe Gravel <jpgravel@chromium.org> 
    Commit-Queue: Thiabaud Engelbrecht <thiabaud@google.com> 
    Cr-Original-Commit-Position: refs/heads/main@{#1470083} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6647090 
    Reviewed-by: Krishna Govind <govind@chromium.org> 
    Commit-Queue: Krishna Govind <govind@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7151@{#2340} 
    Cr-Branched-From: 8e0d32ed6e49a2415b16e5ed402957cac2349ce2-refs/heads/main@{#1453031}

```

---

Files:

- M `base/profiler/module_cache.cc`
- M `base/profiler/module_cache.h`

---

Hash: a41716a9f6074a035d4ccd247844b021b0bce090  

Date:  Mon Jun 16 17:57:22 2025


---

### pe...@google.com (2025-06-16)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2025-06-16)

Project: chromium/src  

Branch: refs/branch-heads/7204  

Author: Thiabaud Engelbrecht [thiabaud@google.com](mailto:thiabaud@google.com)  

Link:      <https://chromium-review.googlesource.com/6648464>

[ssm] Fix race condition

---


Expand for full commit details
```
     
    This CL fixes a threading issue, by using locks to prevent racy access. 
     
    (cherry picked from commit e9e247c09b76dc6813c70d2c7007438c830bea56) 
     
    Bug: 421471016 
    Change-Id: If41796b9eb49aa3f27df175c6be198f47947c4c0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6620528 
    Reviewed-by: Jean-Philippe Gravel <jpgravel@chromium.org> 
    Commit-Queue: Thiabaud Engelbrecht <thiabaud@google.com> 
    Cr-Original-Commit-Position: refs/heads/main@{#1470083} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6648464 
    Commit-Queue: Krishna Govind <govind@chromium.org> 
    Reviewed-by: Krishna Govind <govind@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7204@{#1400} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `base/profiler/module_cache.cc`
- M `base/profiler/module_cache.h`

---

Hash: 7206db266ffc62bd05a022edceea2b54c84a2732  

Date:  Mon Jun 16 19:01:44 2025


---

### pe...@google.com (2025-06-19)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-06-19)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6651573
2. Low - There were a few conflicts.
3. 137 and 138
4. Yes. According to the comment #2 Bisect, this bug was introduced by https://crrev.com/c/5704241 and https://crrev.com/c/5833662 which were merged last year. So this bug seems to happen on M132 as well.

### dx...@google.com (2025-06-25)

Project: chromium/src  

Branch: refs/branch-heads/6834  

Author: Thiabaud Engelbrecht [thiabaud@google.com](mailto:thiabaud@google.com)  

Link:      <https://chromium-review.googlesource.com/6651573>

[M132-LTS][ssm] Fix race condition

---


Expand for full commit details
```
     
    This CL fixes a threading issue, by using locks to prevent racy access. 
     
    (cherry picked from commit e9e247c09b76dc6813c70d2c7007438c830bea56) 
     
    Bug: 421471016 
    Change-Id: If41796b9eb49aa3f27df175c6be198f47947c4c0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6620528 
    Reviewed-by: Jean-Philippe Gravel <jpgravel@chromium.org> 
    Commit-Queue: Thiabaud Engelbrecht <thiabaud@google.com> 
    Cr-Original-Commit-Position: refs/heads/main@{#1470083} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6651573 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
    Reviewed-by: Sean Maher <spvm@chromium.org> 
    Owners-Override: Mohamed Omar <mohamedaomar@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Thiabaud Engelbrecht <thiabaud@google.com> 
    Cr-Commit-Position: refs/branch-heads/6834@{#5588} 
    Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `base/profiler/module_cache.cc`
- M `base/profiler/module_cache.h`

---

Hash: e6d8c998acd2e1b7191dcd2442f9ec1b5ba72eab  

Date:  Wed Jun 25 03:16:08 2025


---

### ch...@google.com (2025-09-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/421471016)*

# Security: UAP in JS Self-Profiling API

| Field | Value |
|-------|-------|
| **Issue ID** | [40055449](https://issues.chromium.org/issues/40055449) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>PerformanceAPIs |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ra...@gmail.com |
| **Assignee** | ac...@meta.com |
| **Created** | 2021-04-05 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

```
void ProfilerGroup::DispatchSampleBufferFullEvent() {  
  for (const auto& profiler : profilers_) {  
    profiler->DispatchEvent(  
        \*Event::Create(event_type_names::kSamplebufferfull)); // [0]  
  }  
}  

```
```
void ProfilerGroup::StopProfiler(ScriptState\* script_state,  
                                 Profiler\* profiler,  
                                 ScriptPromiseResolver\* resolver) {  
  DCHECK(cpu_profiler_);  
  DCHECK(!profiler->stopped());  
  
  v8::Local<v8::String> profiler_id =  
      V8String(isolate_, profiler->ProfilerId());  
  auto\* profile = cpu_profiler_->StopProfiling(profiler_id);  
  auto\* trace = ProfilerTraceBuilder::FromProfile(  
      script_state, profile, profiler->SourceOrigin(), profiler->TimeOrigin());  
  resolver->Resolve(trace);  
  
  if (profile)  
    profile->Delete();  
  
  profilers_.erase(profiler); // [1]  
  
  if (--num_active_profilers_ == 0)  
    TeardownV8Profiler();  
}  

```

when DispatchSampleBufferFullEvent, we can call user-defined code [0]

during iterating loop, |profilers\_| can be reallocated through profile.stop[1]

as result, cause Use after Poison

it is similar to this bug : <https://bugs.chromium.org/p/chromium/issues/detail?id=1108497>

it require "--enable-experimental-web-platform-features" flag  

**VERSION**  

Chrome Version: 91.0.4466.0 (Developer Build) (64-bit)

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Woojin Oh

## Attachments

- [index.html](attachments/index.html) (text/plain, 1.0 KB)
- [server.py](attachments/server.py) (text/plain, 754 B)

## Timeline

### [Deleted User] (2021-04-05)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-04-05)

Thanks for the report! This does appear to reproduce as described. npm@ - can you take a look?

[Monorail components: Blink>PerformanceAPIs]

### np...@chromium.org (2021-04-06)

Over to Andrew who owns this API

### gi...@appspot.gserviceaccount.com (2021-05-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c7fe9a804c8b7a250559c979df14dc72977b3328

commit c7fe9a804c8b7a250559c979df14dc72977b3328
Author: Nicolas Dubus <nicodubus@fb.com>
Date: Thu May 13 22:07:18 2021

Only fire DiscardedSamplesDelegate on Profiler object which has
reached sampleBufferFull status

R=npm@chromium.org

Bug: 1195722
Change-Id: I89162d997dd62472c3bbd170f07ccd30b3e8181c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2890449
Reviewed-by: Nicolás Peña Moreno <npm@chromium.org>
Commit-Queue: Nicolás Peña Moreno <npm@chromium.org>
Commit-Queue: Andrew Comminos <acomminos@fb.com>
Cr-Commit-Position: refs/heads/master@{#882715}

[modify] https://crrev.com/c7fe9a804c8b7a250559c979df14dc72977b3328/third_party/blink/renderer/core/timing/profiler_group.cc
[modify] https://crrev.com/c7fe9a804c8b7a250559c979df14dc72977b3328/third_party/blink/renderer/core/timing/profiler_group.h
[modify] https://crrev.com/c7fe9a804c8b7a250559c979df14dc72977b3328/third_party/blink/web_tests/wpt_internal/js-self-profiling/max-buffer-size.https.html


### ac...@meta.com (2021-05-27)

This should be fixed by #4, since the for loop does not continue to execute after JS is invoked.

### [Deleted User] (2021-05-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-28)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-10)

Congratulations, the VRP Panel has decided to award you $5,000 for this report. Nice work! 

### am...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-09-04)

This issue was migrated from crbug.com/chromium/1195722?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055449)*

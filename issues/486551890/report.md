# Debug check failed: Holder<To> v8::internal::TrustedCast(Holder<From>, SourceLocation) [To = v8::internal::SeqTwoByteString, From = v8::internal::String, Holder = v8::internal::Handl e] in src/json/json-parser.h, line 468

| Field | Value |
|-------|-------|
| **Issue ID** | [486551890](https://issues.chromium.org/issues/486551890) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@goodmanemail.com |
| **Assignee** | pt...@chromium.org |
| **Created** | 2026-02-22 |
| **Bounty** | $2,000.00 |

## Description

VULNERABILITY DETAILS
# Fatal error in ../../src/json/json-parser.h, line 468
# Debug check failed: Holder<To> v8::internal::TrustedCast(Holder<From>, SourceLocation) [To = v8::internal::SeqTwoByteString, From = v8::internal::String, Holder = v8::internal::Handle].   

Suspected GC creates small window for type confusion SeqTwoByteString -> ExternalTwoByteString 

VERSION
Tested on V8 4e31386ca3ee39753df98ff8c6bda1bb0487fcea

I am replicating with the below build args:
is_debug = false
is_asan = true
dcheck_always_on = true
v8_enable_slow_dchecks = true
v8_static_library = true
v8_enable_verify_heap = true
v8_enable_partition_alloc = false
v8_fuzzilli = true
sanitizer_coverage_flags = "trace-pc-guard"
target_cpu = "x64"

I am replicating with /home/alan/v8/v8/out/fuzzilli/d8 --expose-gc --expose-externalize-string --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --future --harmony --experimental-fuzzing --js-staging --wasm-staging --wasm-fast-api --expose-fast-api --wasm-test-streaming --minor-ms --harmony-struct --wasm-stack-switching-stack-size=265 --experimental-wasm-growable-stacks however based on my analysis I suspect that only --expose-externalize-string --expose-gc --fuzzing are needed.  Given the difficulty of replicating this its tricky to reduce the list further.

REPRODUCTION CASE
Two unminimized test cases are attached.

MY ANALYSIS
This is an extremely difficult to replicate crash.  It piqued my attention after the same crash was found in my Fuzzilli run twice in the same month.  Evidently sometimes extremely difficult to replicate crashes might be seen only once, but since this one happened twice in a month with very similar testcases I decided to pause my run and try to replicate it.  On a 56 core machine, running 56 concurrent terminals and --stress-runs=200000 I can typically replicate it in under 2 hours.  Based on analysis of the backtrace and the error message the JSON parser seems to be confusing SeqTwoByteString with ExternalTwoByteString.  In a debug build this is caught by a dcheck, in a release type build (which doesnt have debug checks) this will result in trying to read fields from memory that dont exist (I think because the two confused fields have different memory structures).  Since one of the fields that will be receiving garbage memory is a length field this might result in an invalid read or write.

The sequence to trigger the bug appears to be 1) create an externalized string 2) with slim timing margins a GC runs after the string->isseqtwobytesstring() fires. 3) You try to parse the string from 1, which tries to hit the handle of the now externalized string.  Therefore likely most of the test case is not tremendously interesting fluff however given how hard this is to replicate I've not tried to reduce it.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: Dcheck
Crash State: 
#0  __pthread_kill_implementation (no_tid=0, signo=6, threadid=<optimized out>) at ./nptl/pthread_kill.c:44
#1  __pthread_kill_internal (signo=6, threadid=<optimized out>) at ./nptl/pthread_kill.c:78
#2  __GI___pthread_kill (threadid=<optimized out>, signo=signo@entry=6) at ./nptl/pthread_kill.c:89
#3  0x00007ffff7c4527e in __GI_raise (sig=sig@entry=6) at ../sysdeps/posix/raise.c:26
#4  0x00007ffff7c288ff in __GI_abort () at ./stdlib/abort.c:79
#5  0x000055555839bae2 in Abort () at ../../src/base/platform/platform-posix.cc:808
#6  0x0000555558390b16 in V8_Fatal () at ../../src/base/logging.cc:232
#7  0x000055555838fbef in v8::base::(anonymous namespace)::DefaultDcheckHandler(char const*, int, char const*) () at ../../src/base/logging.cc:59
#8  0x0000555559d6391c in TrustedCast<v8::internal::SeqTwoByteString, v8::internal::String, v8::internal::Handle> () at ../../src/objects/casting.h:234
#9  0x0000555559d2fab4 in Cast<v8::internal::SeqTwoByteString, v8::internal::String, v8::internal::Handle> () at ../../src/objects/casting.h:327
#10 UpdatePointers () at ../../src/json/json-parser.h:468
#11 0x000055555962f040 in Invoke () at ../../src/heap/gc-callbacks.h:119
#12 InvokeGCEpilogueCallbacksInSafepoint () at ../../src/heap/local-heap.cc:476
#13 0x0000555559425c3d in operator() () at ../../src/heap/heap.cc:1138
#14 IterateLocalHeaps<(lambda at ../../src/heap/heap.cc:1137:13)> () at ../../src/heap/safepoint.h:43
#15 operator() () at ../../src/heap/heap.cc:1136
#16 IterateClientIsolates<(lambda at ../../src/heap/heap.cc:1135:60)> () at ../../src/heap/safepoint.h:202
#17 GarbageCollectionEpilogueInSafepoint () at ../../src/heap/heap.cc:1135
#18 0x000055555943be69 in PerformGarbageCollection () at ../../src/heap/heap.cc:2434
#19 0x00005555594c5a16 in operator() () at ../../src/heap/heap.cc:1661
#20 0x00005555594c4f93 in void heap::base::Stack::SetMarkerAndCallbackImpl<v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags, v8::internal::PerformHeapLimitCheck, v8::internal::PerformIneffectiveMarkCompactCheck)::$_1>(heap::base::Stack*, void*, void const*) ()
    at ../../src/heap/base/stack.h:180
#21 0x000055555d2c0453 in PushAllRegistersAndIterateStack ()
#22 0x000055555942b173 in SetMarkerIfNeededAndCallback<(lambda at ../../src/heap/heap.cc:1629:40)> () at ../../src/heap/base/stack.h:76
#23 CollectGarbage () at ../../src/heap/heap.cc:1629
#24 0x000055555942d78b in CollectAllGarbage () at ../../src/heap/heap.cc:1320
#25 0x000055555960cbd3 in RunInternal () at ../../src/heap/incremental-marking-job.cc:128
#26 0x00005555583a1756 in PumpMessageLoop () at ../../src/libplatform/default-platform.cc:173
#27 0x000055555800443c in ProcessMessages () at ../../src/d8/d8.cc:6668
#28 0x0000555557ff41dc in CompleteMessageLoop () at ../../src/d8/d8.cc:6724
#29 FinishExecuting () at ../../src/d8/d8.cc:6728
#30 0x0000555558003bb0 in RunMainIsolate () at ../../src/d8/d8.cc:6636
#31 0x00005555580027df in RunMain () at ../../src/d8/d8.cc:6541
#32 0x0000555558007415 in Main () at ../../src/d8/d8.cc:7403
#33 0x00007ffff7c2a1ca in __libc_start_call_main (main=main@entry=0x5555580096d0 <main>, argc=argc@entry=31, argv=argv@entry=0x7fffffffd998)
    at ../sysdeps/nptl/libc_start_call_main.h:58
#34 0x00007ffff7c2a28b in __libc_start_main_impl (main=0x5555580096d0 <main>, argc=31, argv=0x7fffffffd998, init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, 
    stack_end=0x7fffffffd988) at ../csu/libc-start.c:360
#35 0x0000555557e8302a in _start ()

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Alan Goodman

## Attachments

- [program_20260221160013_69ACA950-50D2-493C-B671-37C3AD2E37A8_flaky.js](attachments/program_20260221160013_69ACA950-50D2-493C-B671-37C3AD2E37A8_flaky.js) (text/javascript, 8.7 KB)
- [program_20260206093631_D65459B4-A831-4599-96B4-9FBFA57E42B5_flaky.js](attachments/program_20260206093631_D65459B4-A831-4599-96B4-9FBFA57E42B5_flaky.js) (text/javascript, 8.0 KB)

## Timeline

### an...@chromium.org (2026-02-22)

Hi, thank you for the report. We really do need a minimized PoC with minimal set of command-line switches to help us reproduce and test any fixes effectively.

ishell@ can you PTAL to see if the attached ASAN is usefuL?

### al...@goodmanemail.com (2026-02-22)

In theory; based on my analysis being correct a minimized is as follows:

```
function trigger() {
  const ext = this.externalizeString;
  ext("\u202Dpayload"); // needs to be non ascii i think
  gc();
  JSON.parse("\u202Dpayload");
}
new Worker(trigger, {type: "function"});

```

I didnt put it in the report because after half a million execs (and counting) this still hasnt replicated the crash. Therefore I suspect the other 'junk' in the original test cases is creating useful memory pressure (especially the bit where it allocates 2GB ram) which might be necessary to trigger the garbage collection, make the garbage collection take longer, do something else that enables the specific timing to trigger the confusion. Someone with more skill than me needs to look at this in my opinion. I cant see any commits in the git repo that might alter the behavior.

### pe...@google.com (2026-02-22)

Thank you for providing more feedback. Adding the requester to the CC list.

### al...@goodmanemail.com (2026-02-22)

After giving up with the minimal reproducer I spent some hours this afternoon attempting to reduce the amount of command line switches and sadly dont have anything concrete.

Looking at the backtrace the only command line switches that are in theory required would be --allow-natives-syntax --expose-externalize-string however despite trying millions of execs this isnt triggering the crash. This doesnt mean its not possible, it probably just means the test cases cant get lucky enough without some of the other switches. Since GC is involved I tried mucking about with adding --expose-gc and forcing GC at various points in the test case, without luck.

--allow-natives-syntax --fuzzing --jit-fuzzing --expose-externalize-string --wasm-staging --js-staging --future seems like a reasonable bet given the backtrace, but after ~700000 attempts no crash has triggered yet.

In terms of the test cases provided; they dont deterministically trigger the GC, therefore the reproduction requires luck of the GC triggering at just the right moment. My attempts to make the crash more deterministic by forcing GC were not succesful. The rest of the 'fluff' in the test cases will be needed for the GC to trigger; without them the GC wont be triggered. Neither of the test cases is enormous and given I've managed to obtain a backtrace I was hoping that this would be enough for you to at least take a look? As you can likely imagine; based upon the difficulty triggering the issue even obtaining a backtrace took me half a day.

### an...@chromium.org (2026-02-22)

Thanks, I'll provisionally assign this to the V8 shepherd.

### is...@chromium.org (2026-02-23)

Thank you for the report.

I didn't manage to reproduce the issue with the POCs provided.

Assigning to JSON folks to double check if concurrent string externalization could cause issues in JSON parser.

### ch...@google.com (2026-02-23)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-23)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pt...@chromium.org (2026-02-23)

This requires `--shared-string-table` (implied by `--harmony-struct` in the originally mentioned flags), so is not affecting a shipping configuration.  

Without a reliable repro it is tricky to understand what's going on (we shouldn't hit this `DCHECK`).

With `--shared-string-table`, externalization doesn't happen immediately, but during a full GC (without a stack).  

So the `JsonParser` sees a sequential string when invoked on a (shared) string that was externalized (in fact only marked for externalization during the next GC without stack).  

We install a GC callback to deal with the string potentially moving during GCs.  

The `DCHECK` failure is when we call this callback from GC, after apparently we transitioned the string to `External`.

And here is what's puzzling: If the `JsonParser` was still active at the time the GC is triggered, we would have a GC with stack and no transition is happening.

I will need to spend more time trying to create a reliable repro to debug this.

In any case this can only lead to an in-sandbox OOB read, so I am downgrading severity.

### al...@goodmanemail.com (2026-02-23)

Use care when interpreting the flags used in my repro - I am just re using what the fuzzer stated that it used however owing to the difficulty in reproducing the crash its extremely hard to narrow down the flags which need to be used. Most of the flags are likely not required.

The reasoning behind shared-string-table being required does make sense to me; I am simply saying be careful about jumping to any conclusions.

### ch...@google.com (2026-02-24)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### pt...@chromium.org (2026-02-24)

OK I know what's happening:  

My assumptions from yesterday were all right. The reason why we transition strings (although my assumptions was that we don't when we have a GC with stack) is that we have a GC on the main thread without a stack while the JsonParser runs on a worker thread.  

The concrete issue reported here is fixable. We can just check in the GC Epilogue callback if we have an `ExternalString` now and change `chars_may_relocate_` to `false` to now handle with an `ExternalString` source everywhere (the only thing tbd is unregistering the GC callback, which right now is not possible from another heap).

However there is another possible transition (not covered by this report) that is more problematic:
We could initially have an `ExternalString`, which we transition to a `ThinString` during GC (same requirements as above; JSON.parse running on a worker thread while the GC without stack is running on the main thread) if we internalize the source string with a string-table-hit (i.e. an internalized string with the same content already exists). The problem here is that we don't ever expect an indirect String as the `source_` in the Json parser (we unwrap indirect strings initially). Unfortunately we can't just update the `source_` in the GC callback, as we can't create `Handle`s at that point (we could patch the existing handle, but then we would require to record the slot in a remembered set somehow/somewhere).

Fixing this issue in general would require major updates in shared GC handling (e.g. one idea is to check if client heaps have a stack and only do transitions when *no* heap has a stack).  

Dealing with the possiblity of indirect strings everywhere in the json parser would be an alternative (which is most likely causing perf regressions and will only fix the issue in `JSON.parse`).

Since it is currently unlikely (or at least unsure) that `--shared-string-table` will ship (It was an initial requirement for the [shared structs proposal](https://github.com/tc39/proposal-structs?tab=readme-ov-file#shared-structs), but it is unlikely that this proposal will move forward), we decided to not fix this issue, but instead demote the flag to experimental.

Please note that your intial repro already requires experimental flags and is therefore not eligable for a VRP reward.
I was able to create a reliable reproducable repro, but not without using experimental features myself.

### al...@goodmanemail.com (2026-02-24)

Thanks for the detailed response.

Could you define which "experimental features" were used in the original/your new repros? I think you're saying --shared-string-table is needed, which at the time I made the report wasnt an experimental feature (I think). The older; larger; slower; repro doesnt use harmony-struct, but instead --shared-string-table directly. Admittedly there is a spam of other flags used in that repro (some experimental), but this is expected since I am running with argument randomization. Most of the flags wont be needed, but owing to the difficulty in reproducing my crashers its really tricky to reduce the list.

My thoughts that are from the list on that repro --jit-fuzzing --maglev-non-eager-inlining --turboshaft-verify-load-elimination --concurrent-recompilation-queue-length=58 --concurrent-recompilation-delay=89 --stress-flush-code --flush-bytecode only relate to compilation so are not needed. --wasm-staging --wasm-fast-api --expose-fast-api --wasm-test-streaming --wasm-inlining-ignore-call-counts --wasm-stack-switching-stack-size=70 --wasm-code-gc --stress-wasm-code-gc are all unrelated because they are wasm related. The remaining ones --fuzzing --experimental-fuzzing --omit-quit --future --harmony --js-staging --expose-gc relate to fuzzing knobs and stuff that enabled proposed features. --stress-scavenge=50 and --stress-compaction are GC related and I dont understand the importance of these for this issue.

### pt...@chromium.org (2026-02-25)

You mentioned yourself that you used `--harmony-struct` in your initial repro, which is experimental. I didn't verify which flags are required to run your poc.

I myself used `--harmony-struct` to create a reliable repro. It might be possible without, but it would definitely be harder.

### al...@goodmanemail.com (2026-02-25)

No, I replicated using the flags from the fuzzer, using the smaller/faster test case becuase that would be the most efficient way to replicate a test case that was clearly very difficult to replicate from the outset.

The older/longer/slower test case doesnt use harmany-struct and I would suggest doesnt need any experimental flags, just ones that at the time were potentially going to be in upcoming features. Both test cases were provided in comment 1. Which I think makes them VRP elligible?

### dx...@google.com (2026-02-25)

Project: v8/v8  

Branch:  main  

Author:  pthier [pthier@chromium.org](mailto:pthier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7607199>

Demote --shared-string-table to experimental

---


Expand for full commit details
```
     
    It is unclear at the moment if we are going to ship this feature. 
    We demote it to experimental for now. 
     
    In addition add a DCHECK to the JsonParser to document known issues 
    with --shared-string-table, that due to the uncertainty if the feature 
    will ever ship won't be fixed right now. 
     
    Bug: 486551890, 40096219 
    Change-Id: Idf6d507fa073493c79c041e18f99afdb0870ac20 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7607199 
    Commit-Queue: Patrick Thier <pthier@chromium.org> 
    Reviewed-by: Dominik Inführ <dinfuehr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105450}

```

---

Files:

- M `src/flags/flag-definitions.h`
- M `src/json/json-parser.cc`
- M `test/mjsunit/mjsunit.status`

---

Hash: [a3944c20ebb6ea04b6452c3dc37b343a37a65289](https://chromiumdash.appspot.com/commit/a3944c20ebb6ea04b6452c3dc37b343a37a65289)  

Date: Wed Feb 25 13:02:29 2026


---

### pt...@chromium.org (2026-02-25)

> No, I replicated using the flags from the fuzzer, using the smaller/faster test case becuase that would be the most efficient way to replicate a test case that was clearly very difficult to replicate from the outset.
> 
> The older/longer/slower test case doesnt use harmany-struct and I would suggest doesnt need any experimental flags, just ones that at the time were potentially going to be in upcoming features. Both test cases were provided in comment 1. Which I think makes them VRP elligible?

You reported using `--harmony-struct` in [comment #1](https://issues.chromium.org/issues/486551890#comment1). I didn't see any reproducible repro without using experimental features?  

Anyways this is not up to me to decide.

From my point of view this was a legit report that highlighted a real issue, even without a reproducible poc.

### al...@goodmanemail.com (2026-02-25)

Fair point, I didnt detail the flags needed for the second PoC in the original report. Both PoCs replicate for me - but with difficulty. As previously mentioned 56x terminals + 56 concurrent runs (on a 56 core box) with --stress-runs=lots replicates it in about 2 hours or ~1 million execs. Given what you've shared this makes sense as the PoCs dont call GC() deterministically so its relying on a heavy hint of luck. The second PoC doesnt need any experimental flags as far as I am aware, despite some being used by the fuzzer for that run as detailed in #16.

If you want / its appropriate for the VRP folks to triage this then care needed as status wontfix means it wont end up in their queue?

As some will be aware I've been active in fuzzing V8 for a while now; mainly as a hobby. My initial goal was to try and make it harder to find bugs in V8 through fuzzing, which I think I've achieved. More recently I've not earnt any bounties. 1 bounty pays for roughly a years worth of electricity so therefore I am keen to ensure none of my reports fall through the cracks in the systems as if I dont get a hit soon I will be forced to stop the continual fuzzing as it eats through vast amounts of power.

### pt...@chromium.org (2026-02-25)

> If you want / its appropriate for the VRP folks to triage this then care needed as status wontfix means it wont end up in their queue?

I clarified internally before I set the status, as I want to make sure that someone from VRP will look at this. The status shouldn't affect it. I also checked on previous issues and usually some automation kicks in to add the correct hotlist so someone from the VRP team will have a look. I will keep an eye on this issue that this automation process is triggered. Feel free to ping if nothing changes here in ~10 days.

As for the VRP itself: As I mentioned in [comment #18](https://issues.chromium.org/issues/486551890#comment18): this was a useful report and should be considered for VRP, as we wouldn't have found this issue otherwise.

Keep the fuzzers running :)

### dr...@chromium.org (2026-03-03)

Adding reward-topanel due to comment 18.

### al...@goodmanemail.com (2026-03-04)

Please could you define why this is marked as reward-ineligible?

To recap, the issue requires --shared-string-table which at the time of the report was not an experimental feature. One of the repros used --harmony-struct which is experimental, but this merely implied --shared-string-table. Repro with hash ending 7A8 replicates for me and as discussed in #14 probably does not need any experimental features enabled.

#10 confirms that this can lead to an OOB read which means there is security impact, since OOB read can be used to leak security relevant data.

### al...@goodmanemail.com (2026-03-17)

Please could I get an update? If this one is ineligible it would be nice to understand why as I believe this one is actually elligible.

### aj...@google.com (2026-03-19)

(for reassessment, see comments above)

### al...@goodmanemail.com (2026-04-14)

Please could I get an update on this one?

### ch...@google.com (2026-06-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/486551890)*

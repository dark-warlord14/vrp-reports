# Heap Buffer Overflow (READ) in TFLite + XNNPack via WebNN

| Field | Value |
|-------|-------|
| **Issue ID** | [484078869](https://issues.chromium.org/issues/484078869) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | to...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2026-02-12 |
| **Bounty** | $43,000.00 |

## Description

---

### Report description

Heap-buffer-overflow (READ of 4 bytes) in TFLite's mirror\_pad.cc:151

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/litert/src/tflite/kernels/mirror_pad.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

# TFLite MirrorPad heap-buffer-overflow (OOB Read) via WebNN pool2d ceil rounding + reflection pad

## Environment

Ubuntu + AMD processor (for completeness, shouldn't matter).

## Base Chromium revision

```
a0062e558d37e03d9129522e5a3c6c29946d8195 (2026-02-10)

```
## GN args

```
is_asan = true
is_debug = false
symbol_level = 1

```
## Build

```
cd chromium/src
gn gen out/asan_shell
autoninja -C out/asan_shell content_shell

```
## Running the PoC

WebNN is behind a feature flag. The GPU process is a separate process, so its ASAN errors don't appear on the main process stderr. Setting `ASAN_OPTIONS` with `log_path` captures per-process ASAN output to disk.

```
ASAN_OPTIONS="log_path=/tmp/asan_log:detect_leaks=0" ./out/asan_shell/content_shell --enable-features=WebMachineLearningNeuralNetwork file:///path/to/poc.html

```

The GPU process crashes during graph dispatch (inference). ASAN output is at `/tmp/asan_log.<gpu_pid>`. The poc.html file is included in this report.

## ASAN output

```
==473973==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x742245a1bdc8 at pc 0x62e8b4d5a284 bp 0x7181cbfb97d0 sp 0x7181cbfb97c8
READ of size 4 at 0x742245a1bdc8 thread T81
    #0 tflite::ops::builtin::mirror_pad::(anonymous namespace)::MirrorPadWorkerTask<float>::Run()
      third_party/tflite/src/tensorflow/lite/kernels/mirror_pad.cc:151:24
    #1 ruy::Thread::ThreadFuncImpl()
      third_party/ruy/src/ruy/thread_pool.cc:73:14

0x742245a1bdc8 is located 8 bytes after 23488-byte region [0x742245a16200,0x742245a1bdc0)
allocated by thread T71 (ThreadPoolForeg) here:
    #0 aligned_alloc
    #1 tflite::SimpleMemoryArena::Commit()
      third_party/tflite/src/tensorflow/lite/simple_memory_arena.cc:111:31
    #2 tflite::ArenaPlanner::ExecuteAllocations()
      third_party/tflite/src/tensorflow/lite/arena_planner.cc:433:32
    #3 tflite::Subgraph::PrepareOpsAndTensors()
      third_party/tflite/src/tensorflow/lite/core/subgraph.cc:1604:42
    #4 tflite::Subgraph::AllocateTensors()
      third_party/tflite/src/tensorflow/lite/core/subgraph.cc:1035:25

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/tflite/src/tensorflow/lite/kernels/mirror_pad.cc:151:24

```
## PoC graph structure

```
input [8,7,7,8]
  -> averagePool2d(window=[4,4], stride=[2,2], ceil) -> declared [8,3,3,8], actual [8,2,2,8]
  -> averagePool2d(window=[1,1], stride=[2,1], ceil) -> declared [8,2,3,8], actual [8,1,2,8]
  -> pad(begin=[2,1,2,2], end=[2,1,2,2], mode='reflection') -> OOB read

```

The reflection padding `[2,1,2,2]` is valid for the declared shape `[8,2,3,8]` (all padding < dim), but NOT for the actual shape `[8,1,2,8]` (padding 1 >= dim 1, padding 2 >= dim 2).

#### Impact analysis

## Affected platforms

Tested on Linux (x86\_64) with the TFLite+XNNPACK backend. The bug is in `graph_builder_tflite.cc` which is used on all platforms with the TFLite backend: Linux, Android (ARM64, x86/x64), and ChromeOS.

## Impact

- **Attack vector:** Any website, no user interaction required beyond navigation. WebNN is behind a feature flag (`WebMachineLearningNeuralNetwork`), which is not yet enabled by default, but eligible for VRP according to the [rules](https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules#chrome-fuzzer-program:~:text=Bugs%20in%20unlaunched,message%20at%20runtime.) and it is also in origin trial since Jan 31: <https://chromium-review.googlesource.com/c/chromium/src/+/7518276>.
- **Process:** GPU process. On Android, this is unsandboxed.
- **Primitive & Consequence:** OOB heap read.

---

### The cause

#### What version of Chrome have you found the security issue in?

147.0.7681.0 dev

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a non-sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Tobias Wienand

## Attachments

- [poc.html](attachments/poc.html) (text/html, 942 B)
- [asan.log](attachments/asan.log) (text/plain, 43.8 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5884652065587200.

### aj...@google.com (2026-02-12)

Confirm this repros on linux asan.

```
./out/Asan/chrome --no-sandbox --enable-features=WebMachineLearningNeuralNetwork ~/Downloads/poc.html 
...
==2458826==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7e1c640a7dc8 at pc 0x5627638c18e4 bp 0x7b7be7d17b90 sp 0x7b7be7d17b88
READ of size 4 at 0x7e1c640a7dc8 thread T82
    #0 0x5627638c18e3 in tflite::ops::builtin::mirror_pad::(anonymous namespace)::MirrorPadWorkerTask<float>::Run() third_party/tflite/src/tensorflow/lite/kernels/mirror_pad.cc:151:24
    #1 0x56273f034cd9 in ruy::Thread::ThreadFuncImpl() third_party/ruy/src/ruy/thread_pool.cc:73:14
    #2 0x56273f034fa6 in void* std::__Cr::__thread_proxy<std::__Cr::tuple<std::__Cr::unique_ptr<std::__Cr::__thread_struct, std::__Cr::default_delete<std::__Cr::__thread_struct>>, void (*)(ruy::Thread*), ruy::Thread*>>(void*) gen/third_party/libc++/src/include/__type_traits/invoke.h:90:27
    #3 0x56273cfbcc66 in asan_thread_start(void*) asan_interceptors.cpp


```

### re...@chromium.org (2026-02-12)

Junwei, please check the padding computation logic.

### aj...@google.com (2026-02-13)

Severity -> High as Android OT is being disabled.

### 24...@project.gserviceaccount.com (2026-02-13)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-02-13)

Detailed Report: https://clusterfuzz.com/testcase?key=5884652065587200

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 12
Crash Address: 0x79473f1cf548
Crash State:
  xnn_xx_copy_ukernel__scalar_memcpy
  xnn_compute_univector_strided
  pthreadpool_parallelize_1d_tile_1d_dynamic
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1483298:1483300

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5884652065587200

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ch...@google.com (2026-02-14)

Setting milestone because of s0/s1 severity.

### re...@chromium.org (2026-02-17)

Updating milestone because the WebNN OT is only enabled on M-146.

### re...@chromium.org (2026-02-19)

Reporter, is the difference between declared and actual shapes similar to the problem you reported in [issue 483971526](https://issues.chromium.org/issues/483971526), where WebNN computes rounding one way and TFLite computes it another way?

### to...@gmail.com (2026-02-19)

Yes, I just double checked and it seems to be the same root cause

### 24...@project.gserviceaccount.com (2026-02-20)

ClusterFuzz testcase 5884652065587200 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1587586:1587590

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-02-20)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-05-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/484078869)*

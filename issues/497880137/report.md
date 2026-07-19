# REFILE: Browser-Process UAF in FileSystemAccessChangeSource::DidInitialize (Reliability-Improved PoC)

| Field | Value |
|-------|-------|
| **Issue ID** | [497880137](https://issues.chromium.org/issues/497880137) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | as...@gmail.com |
| **Assignee** | fe...@chromium.org |
| **Created** | 2026-03-31 |
| **Bounty** | $10,000.00 |

## Description

**Reference**: This is a highly-reliable refile of Issue <https://issues.chromium.org/issues/497456775>.

**Why it was previously marked Not Reproducible**: The previous PoC relied on a single-shot race condition (Worker Termination vs. IO Thread Execution). Because thread scheduling timings differ across hardware (e.g., M-series vs. Intel, core counts), it missed the race window on the triage machine.

**The Fix**: I have created a new PoC that acts as a "reliability sweep". It programmatically sweeps through thousands of attempts using varying profiles of [attempts x fanout x concurrency] (e.g., 1024x24x8). This systematically exhausts the thread scheduler variations, effectively guaranteeing the Use-After-Free race window is hit across different hardware profiles.

A video demonstrating the reliable crash on the latest ASan build is attached.

---

**VULNERABILITY DETAILS**

**Class:** Browser-process heap-use-after-free / memory corruption.

**Impact:**
A compromised renderer or a malicious web page can trigger a browser-process UAF. Because the vulnerability bypasses MiraclePtr (`MiraclePtr Status: NOT PROTECTED`), this memory corruption can be exploited for an arbitrary memory read or controlled write in the browser process, leading to sandbox escape/RCE.

**Root Cause:**
The bug is in `content/browser/file_system_access/file_system_access_change_source.cc`, in `FileSystemAccessChangeSource::DidInitialize(...)`.

`DidInitialize()` moves `initialization_callbacks_` to a local stack variable because executing the callbacks may cause `this` to be deleted. However, it still reads `this->initialization_result_` from the member variable inside the callback loop:

```
  initialization_result_ = std::move(result);

  // Move the callbacks to the stack since they may cause |this| to be deleted.
  auto initialization_callbacks = std::move(initialization_callbacks_);
  initialization_callbacks_.clear();
  for (auto& callback : initialization_callbacks) {
    // If the first callback deleted |this|, the next iteration UAFs here:
    std::move(callback).Run(initialization_result_->Clone()); 
  }

```

If the first callback tears down the watcher and deletes the source, the second iteration dereferences freed object state through `this->initialization_result_`. The implicit `this` pointer is not protected by BRP/MiraclePtr in this specific execution context.

**VERSION**

Chrome Version: Chromium 148.0.7761.0 canary (official mac-arm64 ASan prebuilt; reproduced March 31, 2026)
Operating System: macOS 15.7.4 (24G517), arm64

**REPRODUCTION CASE**

*Please see the attached individual files:*

- `poc.html` (The reliability sweep driver)
- `poc.js`
- `worker.js`
- `asan.log` (ASan logs from the run)
- `FSA_UAF_POC.mov` (Video evidence of reproduction)

The PoC is a minimized, pure-web reproduction utilizing a reliability sweep:

1. Serve the PoC files from a local HTTP server (`python3 -m http.server 8000`).
2. Launch the ASan browser.
3. Click **Start**.
4. In the directory picker, choose any writable local directory.
5. The PoC will begin a staged sweep (Stage 1: 1024x24x8, Stage 2: 1024x32x8, Stage 3: 768x24x12).
6. The browser will crash with a heap-use-after-free during one of these stages.

**Exact Command Line from Repro (As recorded in `asan.log`):**

```
profile_dir=$(mktemp -d /tmp/fsa_profile.XXXXXX)

ASAN_OPTIONS="detect_odr_violation=0:abort_on_error=1:symbolize=1:external_symbolizer_path=/Users/asjidkalam/fuzzing/chrome_research/chromium/src/third_party/llvm-build/Release+Asserts/bin/llvm-symbolizer:log_path=/tmp/fsa_local_context_arm64_default_symbolized_asan" \
open -n "/Users/asjidkalam/fuzzing/chrome_research/chromium/src/.asan_mac_arm64_run/Chromium.app" --args \
  --user-data-dir="$profile_dir" \
  --window-size=1280,900 \
  --window-position=0,0 \
  --enable-blink-features=FileSystemObserver \
  --test-type \
  --no-first-run \
  --no-default-browser-check \
  "http://127.0.0.1:8000/fsa_change_source_default_web_vrp_bundle/poc.html"

```

**Notes:**

- **No flags required:** This repro does NOT use `--disable-features=PartitionAllocBackupRefPtr`.
- **Timing:** If the crash does not occur in Stage 1, please allow the sweep to continue through Stage 3.

**SUGGESTED PATCH**

Move/Clone the initialization result to a local stack variable before entering the callback loop to decouple it from the object's lifetime:

```
  auto initialization_callbacks = std::move(initialization_callbacks_);
  initialization_callbacks_.clear();
  auto result_clone = initialization_result_->Clone();
  for (auto& callback : initialization_callbacks) {
    std::move(callback).Run(result_clone->Clone());
  }

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: browser-process ASan heap-use-after-free

**Crash State:**

- Use path: `content::FileSystemAccessChangeSource::DidInitialize(...)`
- Callback path: `content::FileSystemAccessLocalPathWatcher::Initialize(...)`
- Free path: `content::FileSystemAccessWatcherManager::RemoveObserver(...)`
- Allocation path: `content::FileSystemAccessWatcherManager::CreateOwnedSourceForScope(...)`

**Summary from attached ASan log:**

- `ERROR: AddressSanitizer: heap-use-after-free`
- `SUMMARY: AddressSanitizer: heap-use-after-free ... in content::FileSystemAccessChangeSource::DidInitialize(...)`
- `MiraclePtr Status: NOT PROTECTED`

**CREDIT INFORMATION**

Reporter credit: asjidkalam

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 52.8 KB)
- [FSA_UAF_POC.mov](attachments/FSA_UAF_POC.mov) (video/quicktime, 39.1 MB)
- [poc.html](attachments/poc.html) (text/html, 2.5 KB)
- [poc.js](attachments/poc.js) (text/javascript, 10.6 KB)
- [worker.js](attachments/worker.js) (text/javascript, 753 B)

## Timeline

### xi...@chromium.org (2026-03-31)

Thanks for the report! Adding feature owners to take a look.

### ch...@google.com (2026-04-01)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-01)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-04-07)

Project: chromium/src  

Branch:  main  

Author:  Fergal Daly [fergal@chromium.org](mailto:fergal@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7728464>

Fix UAF in FileSystemAccessChangeSource.

---


Expand for full commit details
```
     
    `DidInitialize` calls any outstanding initialization callbacks but a 
    callback can delete this. The code guards against this in its access 
    of `initialization_callbacks_` but not `initialization_result_`. 
     
    This fix keeps a copy of the result on the stack. 
     
    This also adds a test which fails with ASAN before the fix is applied 
    and passes after. 
     
    The basic test code was written by Gemini. 
     
    Fixed: 497880137 
    Change-Id: I046831db23cb4b8e41964910e2aede9b1be0db7f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7728464 
    Auto-Submit: Fergal Daly <fergal@chromium.org> 
    Reviewed-by: Ming-Ying Chung <mych@chromium.org> 
    Commit-Queue: Ming-Ying Chung <mych@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1610499}

```

---

Files:

- M `content/browser/file_system_access/file_system_access_change_source.cc`
- A `content/browser/file_system_access/file_system_access_change_source_unittest.cc`
- M `content/test/BUILD.gn`

---

Hash: [c0390bcd64ba1fd6594fbc9f6246a1649662d683](https://chromiumdash.appspot.com/commit/c0390bcd64ba1fd6594fbc9f6246a1649662d683)  

Date: Tue Apr 7 02:49:06 2026


---

### ch...@google.com (2026-04-07)

Requesting merge to M146 because latest trunk commit (1610499) appears to be after M146 branch point (1582197).

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M147 because latest trunk commit (1610499) appears to be after M147 branch point (1596535).

### ch...@google.com (2026-04-07)

**M146** merge request created. **Please update [crbug/500247135](https://crbug.com/500247135) to have this merge reviewed.**

### ch...@google.com (2026-04-07)

**M147** merge request created. **Please update [crbug/500246902](https://crbug.com/500246902) to have this merge reviewed.**

### dx...@google.com (2026-04-13)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Fergal Daly [fergal@chromium.org](mailto:fergal@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7754020>

[M146] Fix UAF in FileSystemAccessChangeSource.

---


Expand for full commit details
```
     
    Original change's description: 
    > Fix UAF in FileSystemAccessChangeSource. 
    > 
    > `DidInitialize` calls any outstanding initialization callbacks but a 
    > callback can delete this. The code guards against this in its access 
    > of `initialization_callbacks_` but not `initialization_result_`. 
    > 
    > This fix keeps a copy of the result on the stack. 
    > 
    > This also adds a test which fails with ASAN before the fix is applied 
    > and passes after. 
    > 
    > The basic test code was written by Gemini. 
    > 
    > Fixed: 497880137 
    > Change-Id: I046831db23cb4b8e41964910e2aede9b1be0db7f 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7728464 
    > Auto-Submit: Fergal Daly <fergal@chromium.org> 
    > Reviewed-by: Ming-Ying Chung <mych@chromium.org> 
    > Commit-Queue: Ming-Ying Chung <mych@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1610499} 
     
    (cherry picked from commit c0390bcd64ba1fd6594fbc9f6246a1649662d683) 
     
    Bug: 500247135,497880137 
    Change-Id: I046831db23cb4b8e41964910e2aede9b1be0db7f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7754020 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Chrome Cherry Picker <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#3929} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `content/browser/file_system_access/file_system_access_change_source.cc`
- A `content/browser/file_system_access/file_system_access_change_source_unittest.cc`
- M `content/test/BUILD.gn`

---

Hash: [23865499a86aa3afc10f7ce06cf875448ba2ad9b](https://chromiumdash.appspot.com/commit/23865499a86aa3afc10f7ce06cf875448ba2ad9b)  

Date: Mon Apr 13 03:37:39 2026


---

### pe...@google.com (2026-04-13)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-04-14)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Fergal Daly [fergal@chromium.org](mailto:fergal@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7761642>

[M147] Fix UAF in FileSystemAccessChangeSource.

---


Expand for full commit details
```
     
    Original change's description: 
    > Fix UAF in FileSystemAccessChangeSource. 
    > 
    > `DidInitialize` calls any outstanding initialization callbacks but a 
    > callback can delete this. The code guards against this in its access 
    > of `initialization_callbacks_` but not `initialization_result_`. 
    > 
    > This fix keeps a copy of the result on the stack. 
    > 
    > This also adds a test which fails with ASAN before the fix is applied 
    > and passes after. 
    > 
    > The basic test code was written by Gemini. 
    > 
    > Fixed: 497880137 
    > Change-Id: I046831db23cb4b8e41964910e2aede9b1be0db7f 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7728464 
    > Auto-Submit: Fergal Daly <fergal@chromium.org> 
    > Reviewed-by: Ming-Ying Chung <mych@chromium.org> 
    > Commit-Queue: Ming-Ying Chung <mych@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1610499} 
     
    (cherry picked from commit c0390bcd64ba1fd6594fbc9f6246a1649662d683) 
     
    Bug: 500246902,497880137 
    Change-Id: I046831db23cb4b8e41964910e2aede9b1be0db7f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7761642 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#2882} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `content/browser/file_system_access/file_system_access_change_source.cc`
- A `content/browser/file_system_access/file_system_access_change_source_unittest.cc`
- M `content/test/BUILD.gn`

---

Hash: [17f91c4769bcde75fcefab16cc9e8b5eca65396d](https://chromiumdash.appspot.com/commit/17f91c4769bcde75fcefab16cc9e8b5eca65396d)  

Date: Tue Apr 14 08:51:02 2026


---

### ap...@google.com (2026-04-14)

Is this also going to be cherry-picked to M148? It'd be useful to get a clean cherry pick for [crbug.com/498745115](https://crbug.com/498745115).

### ch...@google.com (2026-04-15)

**M148** merge request created. **Please update [crbug/502733519](https://crbug.com/502733519) to have this merge reviewed.**

### fe...@chromium.org (2026-04-15)

I've added a request for M148.

### as...@gmail.com (2026-04-22)

Hello team, any update on this?

### dx...@google.com (2026-04-22)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Fergal Daly [fergal@chromium.org](mailto:fergal@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7775895>

[M148] Fix UAF in FileSystemAccessChangeSource.

---


Expand for full commit details
```
     
    Original change's description: 
    > Fix UAF in FileSystemAccessChangeSource. 
    > 
    > `DidInitialize` calls any outstanding initialization callbacks but a 
    > callback can delete this. The code guards against this in its access 
    > of `initialization_callbacks_` but not `initialization_result_`. 
    > 
    > This fix keeps a copy of the result on the stack. 
    > 
    > This also adds a test which fails with ASAN before the fix is applied 
    > and passes after. 
    > 
    > The basic test code was written by Gemini. 
    > 
    > Fixed: 497880137 
    > Change-Id: I046831db23cb4b8e41964910e2aede9b1be0db7f 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7728464 
    > Auto-Submit: Fergal Daly <fergal@chromium.org> 
    > Reviewed-by: Ming-Ying Chung <mych@chromium.org> 
    > Commit-Queue: Ming-Ying Chung <mych@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1610499} 
     
    (cherry picked from commit c0390bcd64ba1fd6594fbc9f6246a1649662d683) 
     
    Bug: 502733519,497880137 
    Change-Id: I046831db23cb4b8e41964910e2aede9b1be0db7f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7775895 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Andrew Paseltiner <apaseltiner@chromium.org> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7778@{#1378} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `content/browser/file_system_access/file_system_access_change_source.cc`
- A `content/browser/file_system_access/file_system_access_change_source_unittest.cc`
- M `content/test/BUILD.gn`

---

Hash: [479ea81ef35eec21a74de825e78e3252911c009e](https://chromiumdash.appspot.com/commit/479ea81ef35eec21a74de825e78e3252911c009e)  

Date: Wed Apr 22 14:35:32 2026


---

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
Mildly mitigated (non-sandboxed) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-05-19)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-05-20)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7849221>
2. Low. No Conflicts
3. 146, 147 and 148
4. Yes

### dx...@google.com (2026-06-11)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://chromium-review.googlesource.com/7849221>

[M144-LTS] Fix UAF in FileSystemAccessChangeSource.

---


Expand for full commit details
```
     
    `DidInitialize` calls any outstanding initialization callbacks but a 
    callback can delete this. The code guards against this in its access of 
    `initialization_callbacks_` but not `initialization_result_`. 
     
    This fix keeps a copy of the result on the stack. 
     
    This also adds a test which fails with ASAN before the fix is applied 
    and passes after. 
     
    The basic test code was written by Gemini. 
     
    (cherry picked from commit c0390bcd64ba1fd6594fbc9f6246a1649662d683) 
     
    Fixed: 497880137 
    Change-Id: I046831db23cb4b8e41964910e2aede9b1be0db7f 
    Fuchsia-Binary-Size: Cherry-pick to M144. 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7728464 
    Auto-Submit: Fergal Daly <fergal@chromium.org> 
    Reviewed-by: Ming-Ying Chung <mych@chromium.org> 
    Commit-Queue: Ming-Ying Chung <mych@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1610499} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7849221 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
    Reviewed-by: Fergal Daly <fergal@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#5003} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `content/browser/file_system_access/file_system_access_change_source.cc`
- A `content/browser/file_system_access/file_system_access_change_source_unittest.cc`
- M `content/test/BUILD.gn`

---

Hash: [aeac9d8bff6efdf67d624677674f213714546f79](https://chromiumdash.appspot.com/commit/aeac9d8bff6efdf67d624677674f213714546f79)  

Date: Thu Jun 11 15:30:12 2026


---

### ch...@google.com (2026-07-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/497880137)*

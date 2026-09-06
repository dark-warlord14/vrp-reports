# use-after-poison in ViewTransitionSupplement::OnTransitionCaptured

| Field | Value |
|-------|-------|
| **Issue ID** | [517168239](https://issues.chromium.org/issues/517168239) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>ViewTransitions |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | tr...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2026-05-27 |
| **Bounty** | $500.00 |

## Description

---

### Report description

use-after-poison in ViewTransitionSupplement::OnTransitionCaptured

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

Blink > ViewTransition

---

### The problem

#### Please describe the technical details of the vulnerability

# VULNERABILITY DETAILS

**Type:** use-after-poison (cppgc heap) / container invalidation during iteration
**Component:** Blink > ViewTransition
**Affected file:** `third_party/blink/renderer/core/view_transition/view_transition_supplement.cc`
**Affected function:** `ViewTransitionSupplement::OnTransitionCaptured` (line 346-357)
**Version:** Chromium 150.0.7847.0 (commit f3ab90db77d)
**Process:** Renderer
**MiraclePtr:** NOT PROTECTED (cppgc/Oilpan heap, not PartitionAlloc)
**User interaction:** Print dialog appears; triggers regardless of user choice (cancel/close/print)

**Variant of:** The $50K `LayerTreeHost::NotifyTransitionRequestsFinished` UAF (fixed by CL 6542846). Same bug class — nested RunLoop re-entrancy causing container invalidation during iteration. The cc-level fix (PostTask) does not prevent the blink-level re-entrancy.

## Root Cause Analysis

`OnTransitionCaptured()` iterates `captured_transitions_` (a `HeapVector<Member<ViewTransition>>`) using a range-for loop. For each transition it calls `OnCapturePhaseComplete()`, which synchronously invokes a JavaScript callback via `ViewTransition::ProcessCurrentState()` -> `DOMViewTransition::InvokeDOMChangeCallback()` -> `V8ViewTransitionCallback::Invoke()`.

If the JS callback triggers `window.print()`, the print preview path creates a nested RunLoop (`base::RunLoop{kNestableTasksAllowed}` at `print_render_frame_helper.cc:2702`). This nested RunLoop processes pending tasks, including compositor-originated `BeginMainFrame` tasks that run a full lifecycle update.

During the lifecycle update inside the nested RunLoop, newly created view transitions advance through their state machines (`kCaptureTagDiscovery` -> `kCaptureRequestPending` -> `kCapturing`), generating capture requests that are committed to the compositor. The compositor processes these immediately (due to `kDelayLayerTreeViewDeletionOnLocalSwap`, which is `FEATURE_ENABLED_BY_DEFAULT`) and posts completion callbacks back to the main thread.

These callbacks are processed during the same nested RunLoop, calling `OnTransitionCaptured()` re-entrantly. The re-entrant call executes `captured_transitions_.clear()` (line 356), which poisons the cppgc-managed HeapVector backing store. When the outer `OnTransitionCaptured()` resumes its range-for loop, it dereferences a `Member<ViewTransition>` pointer into poisoned memory.

**The developers were aware of this re-entrancy risk.** The same file contains `ForEachTransition()` (line 388-398) with the explicit comment: *"Local copy of the list, since the function may modify the transition map."* However, `OnTransitionCaptured()` has no such protection.

## Vulnerable Code

```
// view_transition_supplement.cc:346-357
void ViewTransitionSupplement::OnTransitionCaptured(ViewTransition* transition) {
  CHECK(transition);
  captured_transitions_.push_back(transition);           // [1]
  if (--in_flight_capture_requests_ == 0) {
    std::sort(captured_transitions_.begin(), ...);
    for (auto captured_transition : captured_transitions_) {  // [2] range-for
      captured_transition->OnCapturePhaseComplete();          // [3] -> JS -> print()
    }                                                         //     -> nested RunLoop
    captured_transitions_.clear();                            // [4] poisons memory
  }                                                           //     re-entrant [4]
}                                                             //     invalidates [2]

```

**Compare with the protected pattern in the same file:**

```
// view_transition_supplement.cc:388-398
void ViewTransitionSupplement::ForEachTransition(...) {
  // Local copy of the list, since the function may modify the transition map.
  HeapVector<Member<ViewTransition>> transitions;  // <-- local copy, SAFE
  // ... populate from element_transitions_ ...
  for (auto transition : transitions) {
    function(*transition);
  }
}

```
## Reproduction Steps

```
chrome --no-sandbox --user-data-dir=/tmp/test poc.html

```

Close/cancel/interact with the print dialog that appears. The crash triggers regardless of user choice.

**Note:** `--headless` will NOT work. The nested RunLoop only exists in the print preview path (`RequestPrintPreview`), which is disabled when `IsPrintPreviewEnabled()` returns false in headless mode.

## Trigger Chain

```
1. JS: 4x element.startViewTransition(callback)
   -> in_flight_capture_requests_ = 4
   -> 4 transitions enter kCapturing state

2. Compositor processes all 4 captures -> 4 PostTask'd callbacks fire sequentially:
   OnTransitionCaptured(A) -> push_back, counter 4->3
   OnTransitionCaptured(B) -> push_back, counter 3->2
   OnTransitionCaptured(C) -> push_back, counter 2->1
   OnTransitionCaptured(D) -> push_back, counter 1->0 -> ENTERS LOOP

3. Loop: OnCapturePhaseComplete(first) -> ProcessCurrentState() -> kCaptured
   -> InvokeDOMChangeCallback() -> V8 callback RUNS SYNCHRONOUSLY

4. JS callback:
   a. element5.startViewTransition(cb5)  -> in_flight_capture_requests_ = 1
      element6.startViewTransition(cb6)  -> in_flight_capture_requests_ = 2
   b. window.print()
      -> ScriptedPrint -> RequestPrintPreview(kScripted)
      -> base::RunLoop{kNestableTasksAllowed}.Run()  [line 2702]

5. DURING NESTED RUNLOOP:
   - BeginMainFrame -> lifecycle update -> RunViewTransitionStepsDuringMainFrame
   - Transitions E,F advance: kCaptureTagDiscovery -> kCapturing
   - PushPaintArtifactToCompositor -> capture requests committed
   - Impl processes captures immediately (kDelayLayerTreeViewDeletionOnLocalSwap)
   - PostTask chain: impl -> NotifyTransitionRequestsFinished [PostTask] -> callback

6. RE-ENTRANT OnTransitionCaptured(E): push_back(E), counter 2->1
   RE-ENTRANT OnTransitionCaptured(F): push_back(F), counter 1->0
   -> ENTERS INNER LOOP
   -> inner loop iterates captured_transitions_ [A,B,C,D,E,F]
   -> captured_transitions_.clear()  <<<--- POISONS MEMORY

7. Outer loop resumes -> dereferences Member<> into POISONED memory -> CRASH

```
## Prerequisites (all enabled by default)

- `ScopedViewTransitions`: runtime feature, `status: "stable"`
- `kDelayLayerTreeViewDeletionOnLocalSwap`: `FEATURE_ENABLED_BY_DEFAULT`
- No special flags required

## ASAN Report

```
==424011==ERROR: AddressSanitizer: use-after-poison on address 0x7edc02142c2c
READ of size 4 at 0x7edc02142c2c thread T0 (chrome)
    #0 in blink::ViewTransitionSupplement::OnTransitionCaptured
       v8/include/cppgc/member.h:59:55

Address 0x7edc02142c2c is a wild pointer inside of access range of size 0x000000000004.
SUMMARY: AddressSanitizer: use-after-poison v8/include/cppgc/member.h:59:55
         in blink::ViewTransitionSupplement::OnTransitionCaptured

Shadow byte: f7 (Poisoned by user)

Task trace:
    #0 cc::LayerTreeHost::NotifyTransitionRequestsFinished  cc/trees/layer_tree_host.cc:605
    #1 cc::ProxyImpl::NotifyTransitionRequestFinished       cc/trees/proxy_impl.cc:648

```
## Suggested Fix

Make a local copy before iterating, matching the existing `ForEachTransition` pattern:

```
void ViewTransitionSupplement::OnTransitionCaptured(ViewTransition* transition) {
  CHECK(transition);
  captured_transitions_.push_back(transition);
  if (--in_flight_capture_requests_ == 0) {
    std::sort(captured_transitions_.begin(), captured_transitions_.end(),
              CompareTransitions);
    // Local copy to prevent re-entrancy from invalidating the iteration.
    HeapVector<Member<ViewTransition>> local_copy(captured_transitions_);
    captured_transitions_.clear();
    for (auto captured_transition : local_copy) {
      captured_transition->OnCapturePhaseComplete();
    }
  }
}

```
## Files

- `poc.html` — Reproduction HTML
- `asan.txt` — Full ASAN report from Chromium 150.0.7847.0

#### Impact analysis

## Security Impact

**Severity:** High (Renderer Process Heap Corruption)

**Primitive:** use-after-poison on cppgc `HeapVector` backing store. After `captured_transitions_.clear()` poisons the memory, the outer loop dereferences `Member<ViewTransition>` pointers into attacker-influenced heap space. Because cppgc recycles backing store pages, a well-timed allocation between the inner `clear()` and the outer loop resumption can place attacker-controlled data at the poisoned address — converting the use-after-poison into a **controlled read/write on a fake `ViewTransition` object**.

**MiraclePtr / BackupRefPtr: NOT PROTECTED.** The `HeapVector<Member<ViewTransition>>` lives on the cppgc (Oilpan) managed heap, which is entirely outside PartitionAlloc's MiraclePtr coverage. There is no dangling pointer detection or use-after-free mitigation for this object type.

**Exploitation path:**

1. **Heap spray during nested RunLoop:** The nested RunLoop created by `window.print()` stays open for seconds (waiting for user interaction with print dialog). During this window, the attacker's JS callback can allocate arbitrary objects (ArrayBuffers, strings, TypedArrays) via the same cppgc allocator to reclaim the freed backing store.
2. **Type confusion via fake Member<>:** When the outer loop dereferences the reclaimed memory as a `Member<ViewTransition>`, the attacker controls the vtable pointer. Calling `OnCapturePhaseComplete()` on a fake object gives **arbitrary virtual call** — a standard vtable hijack primitive.
3. **RCE in renderer:** Arbitrary virtual call → stack pivot → ROP/JOP chain → arbitrary code execution within the renderer process sandbox.

**Attack surface:**

- Triggered from **any web page** via standard DOM APIs (`element.startViewTransition()` + `window.print()`)
- No special permissions, flags, or user gestures required beyond the print dialog appearing
- All prerequisites enabled by default in stable Chrome (`ScopedViewTransitions: "stable"`, `kDelayLayerTreeViewDeletionOnLocalSwap: FEATURE_ENABLED_BY_DEFAULT`)
- Works on all desktop platforms with print preview (Linux, Windows, macOS, ChromeOS)

**User interaction:** Minimal. The `window.print()` call opens a print dialog, but the UAF triggers **regardless of user choice** (cancel, close, or print). A phishing page could social-engineer the user with "Please print this receipt" to make the dialog appear expected. The corruption occurs during the nested RunLoop — before the user interacts with the dialog.

**Scope:** Renderer process only. Full exploitation requires combining with a sandbox escape for system-level impact. However, renderer-process RCE alone enables:

- Reading all cross-site data in the renderer (cookies, passwords in autofill, DOM content)
- Bypassing Site Isolation within the compromised renderer
- Serving as the first stage of a full exploit chain (renderer RCE → sandbox escape → system compromise)

---

### The cause

#### What version of Chrome have you found the security issue in?

Chromium 150.0.7847.0 (commit f3ab90db77d)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption

#### How would you like to be publicly acknowledged for your report?

Quac Tran

## Attachments

- [poc.html](attachments/poc.html) (text/html, 6.7 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 9.2 KB)

## Timeline

### xi...@chromium.org (2026-05-27)

[security shepherd] Great report! I'm able to reproduce. Assigning to the code author to take a look.

### tr...@gmail.com (2026-05-28)

Hello,

The vulnerability pattern was introduced by this CL: <https://chromium-review.googlesource.com/c/chromium/src/+/7101482>

### ch...@google.com (2026-05-28)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-05-28)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-05-28)

Project: chromium/src  

Branch:  main  

Author:  Kevin Ellis [kevers@google.com](mailto:kevers@google.com)  

Link:    <https://chromium-review.googlesource.com/7881960>

[vt] Fix use after capture in OnTransitionCaptured

---


Expand for full commit details
```
     
    Bug: 517168239 
    Change-Id: I2ae2b01ec9f87158cf4a4b604c4b901bc509e0c8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7881960 
    Commit-Queue: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1637664}

```

---

Files:

- M `third_party/blink/renderer/core/view_transition/view_transition_supplement.cc`

---

Hash: [e3c41472f7a775661fffabbbb71ca04c6793a555](https://chromiumdash.appspot.com/commit/e3c41472f7a775661fffabbbb71ca04c6793a555)  

Date: Thu May 28 13:43:36 2026


---

### ch...@google.com (2026-05-29)

Requesting merge to M148 because latest trunk commit is in 150.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M149 because latest trunk commit is in 150.

### ch...@google.com (2026-05-29)

**M148** merge request created. **Please update [crbug/517794258](https://crbug.com/517794258) to have this merge reviewed.**

### ch...@google.com (2026-05-29)

**M149** merge request created. **Please update [crbug/517793666](https://crbug.com/517793666) to have this merge reviewed.**

### dx...@google.com (2026-06-01)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Kevin Ellis [kevers@google.com](mailto:kevers@google.com)  

Link:    <https://chromium-review.googlesource.com/7886800>

[M148] [vt] Fix use after capture in OnTransitionCaptured

---


Expand for full commit details
```
     
    Original change's description: 
    > [vt] Fix use after capture in OnTransitionCaptured 
    > 
    > Bug: 517168239 
    > Change-Id: I2ae2b01ec9f87158cf4a4b604c4b901bc509e0c8 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7881960 
    > Commit-Queue: Vladimir Levin <vmpstr@chromium.org> 
    > Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1637664} 
     
    (cherry picked from commit e3c41472f7a775661fffabbbb71ca04c6793a555) 
     
    Bug: 517794258,517168239 
    Change-Id: I2ae2b01ec9f87158cf4a4b604c4b901bc509e0c8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7886800 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7778@{#4161} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `third_party/blink/renderer/core/view_transition/view_transition_supplement.cc`

---

Hash: [9190e0a6faf3398799b1e5affaa3b2d715da5e54](https://chromiumdash.appspot.com/commit/9190e0a6faf3398799b1e5affaa3b2d715da5e54)  

Date: Mon Jun 1 18:52:18 2026


---

### pe...@google.com (2026-06-01)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2026-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
ASAN Read. Other Processes - Renderer.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2026-06-05)

Project: chromium/src  

Branch:  refs/branch-heads/7827  

Author:  Kevin Ellis [kevers@google.com](mailto:kevers@google.com)  

Link:    <https://chromium-review.googlesource.com/7901387>

[vt] Fix use after capture in OnTransitionCaptured

---


Expand for full commit details
```
     
    (cherry picked from commit e3c41472f7a775661fffabbbb71ca04c6793a555) 
     
    Bug: 517168239, 517793666 
    Change-Id: I2ae2b01ec9f87158cf4a4b604c4b901bc509e0c8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7881960 
    Commit-Queue: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1637664} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7901387 
    Commit-Queue: Kevin Ellis <kevers@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7827@{#2530} 
    Cr-Branched-From: 9f3e9aaccba63bd2ec30334e45e0bfd07ebcc8f1-refs/heads/main@{#1625079}

```

---

Files:

- M `third_party/blink/renderer/core/view_transition/view_transition_supplement.cc`

---

Hash: [a5f4378c6bd26ae468836e445f2b1269f0076202](https://chromiumdash.appspot.com/commit/a5f4378c6bd26ae468836e445f2b1269f0076202)  

Date: Fri Jun 5 15:00:15 2026


---

### ch...@google.com (2026-07-14)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### pe...@google.com (2026-07-15)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-07-15)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/8084442
2. Low - There was no conflict.
3. 148 and 149
4. Yes.

### dx...@google.com (2026-07-17)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Kevin Ellis [kevers@google.com](mailto:kevers@google.com)  

Link:    <https://chromium-review.googlesource.com/8084442>

[M144-LTS][vt] Fix use after capture in OnTransitionCaptured

---


Expand for full commit details
```
[M144-LTS][vt] Fix use after capture in OnTransitionCaptured 
 
(cherry picked from commit e3c41472f7a775661fffabbbb71ca04c6793a555) 
 
Bug: 517168239 
Change-Id: I2ae2b01ec9f87158cf4a4b604c4b901bc509e0c8 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7881960 
Commit-Queue: Vladimir Levin <vmpstr@chromium.org> 
Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1637664} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/8084442 
Reviewed-by: Kevin Ellis <kevers@chromium.org> 
Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
Cr-Commit-Position: refs/branch-heads/7559@{#5114} 
Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `third_party/blink/renderer/core/view_transition/view_transition_supplement.cc`

---

Hash: [0f33e2544715776f4ee6bf64d931550accef24d5](https://chromiumdash.appspot.com/commit/0f33e2544715776f4ee6bf64d931550accef24d5)  

Date: Fri Jul 17 02:15:06 2026


---

### ch...@google.com (2026-09-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/517168239)*

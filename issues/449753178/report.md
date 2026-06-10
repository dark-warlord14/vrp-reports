# DCHECK failure in !value->properties().is_conversion() in maglev-interpreter-frame-state.h

| Field | Value |
|-------|-------|
| **Issue ID** | [449753178](https://issues.chromium.org/issues/449753178) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@googlemail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2025-10-06 |
| **Bounty** | $9,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5201735517667328

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_v8_arm64_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  !value->properties().is_conversion() in maglev-interpreter-frame-state.h
  void v8::internal::maglev::MaglevGraphBuilder::StoreRegister<v8::internal::magle
  v8::internal::maglev::ReduceResult v8::internal::maglev::MaglevGraphBuilder::Bui
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_v8_arm64_dbg&range=102940:102941

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5201735517667328

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### 24...@project.gserviceaccount.com (2025-10-06)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/f3a5565df877474e80a060f1dd1968b117f5b016 ([maglev] Constant-fold -0.0, *1.0 and /1.0

Bug: 431933185
Change-Id: I162bf4a551b870e1b57e9dbe7b2072935f879017
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7000251
Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
Reviewed-by: Victor Gomes <victorgomes@chromium.org>
Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
Cr-Commit-Position: refs/heads/main@{#102941}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### ch...@google.com (2025-10-07)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-10-07)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2025-10-07)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2025-10-08)

Project: v8/v8  

Branch:  main  

Author:  Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7021709>

[maglev] Correclty unwrap conversions in Float64 binop constant folding

---


Expand for full commit details
```
     
    Drive-by: move where constant folding is done so that's it applies 
    more often (since some places call 
    TryFoldFloat64BinaryOperationForToNumber with a constant for right 
    already, without going through the version that has 2 ValueNode 
    inputs). 
     
    Fixed: 449753178 
    Change-Id: I5d5c0f3855ddc628951ca7d9197a6f2c582e1bee 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7021709 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#103000}

```

---

Files:

- M `src/maglev/maglev-reducer-inl.h`
- A `test/mjsunit/maglev/regress-449753178.js`

---

Hash: [b50129859ef82030b8a1acb82ed73d680bafdc82](https://chromiumdash.appspot.com/commit/b50129859ef82030b8a1acb82ed73d680bafdc82)  

Date: Wed Oct 8 12:19:13 2025


---

### 24...@project.gserviceaccount.com (2025-10-09)

ClusterFuzz testcase 5201735517667328 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_v8_arm64_dbg&range=102999:103000

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### wf...@chromium.org (2025-10-17)

so cool to see this fuzzer still finding bugs!

### sp...@google.com (2025-10-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $9000.00 for this report.

Rationale for this decision:
baseline memory corruption in sandboxed process + fuzzer bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-01-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-01-15)

This issue is marked as a release blocker with no valid full version in the "Found In" field. Please add an appropriate full version (e.g. 139.0.5678.12).
This will be the version the issue is first found in.

This issue is marked as a release blocker and is in Fixed or Verified state, but with no valid full version in the "Verified In" field. Please add an appropriate full version (e.g. 139.0.5678.12).
This will be the version the issue is fixed in.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-15)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/449753178)*

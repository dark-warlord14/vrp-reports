# Security: Heap-buffer-overflow in v8::wasm

| Field | Value |
|-------|-------|
| **Issue ID** | [40088207](https://issues.chromium.org/issues/40088207) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | xi...@gmail.com |
| **Assignee** | ah...@chromium.org |
| **Created** | 2017-06-27 |
| **Bounty** | $1,000.00 |

## Description

This is working in the latest version with ASan.  

I'm using the pre-built ASan binary from  

<https://commondatastorage.googleapis.com/chromium-browser-asan/index.html>  

And ASan stacktrace comes from this version  

asan-win32-release-482506  

Linux version should has the same issue.

**VULNERABILITY DETAILS**  

The issue is quite simple so I didn't translate the stacktrace to source file.  

The issue is in function DecodeCodeSection() of module-decoder.cc,

```
  uint32_t size = consume_u32v("body size");  
  function->code_start_offset = pc_offset();  
  function->code_end_offset = pc_offset() + size;  
  if (verify_functions) {  
    ModuleBytesEnv module_env(module_.get(), nullptr,  
                              ModuleWireBytes(start_, end_));  
    VerifyFunctionBody(module_->signature_zone->allocator(),  
                       i + module_->num_imported_functions, &module_env,  
                       function);  
  }  

```

Where size comes from user input without sanity check.  

So the following VerifyFunctionBody will surely run out of the buffer boundary.

**VERSION**  

Chrome Version: [61.0.3142.0] + [dev]  

Operating System: [Windows 7, Service Pack 7]

**REPRODUCTION CASE**  

Open the attach test.html with ASan enabled.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State: [see link above: stacktrace.txt]

## Attachments

- [test.html](attachments/test.html) (text/plain, 242 B)
- [stacktrace.txt](attachments/stacktrace.txt) (text/plain, 4.5 KB)

## Timeline

### cl...@chromium.org (2017-06-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6656244629897216.

### cl...@chromium.org (2017-06-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5934685426548736.

### mm...@chromium.org (2017-06-27)

Thanks for your report!

I'm curious whether you found this bug via code audit or you tried to fuzz / analyze it in automated way?

[Monorail components: Blink>JavaScript>WebAssembly]

### xi...@gmail.com (2017-06-28)

Yes, this is found via code audit.

Frankly fuzzing is too difficult to me and my only way is code audit:(

### ah...@chromium.org (2017-06-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/a15030304ac030262f6a59e24d5833251fe4db8a

commit a15030304ac030262f6a59e24d5833251fe4db8a
Author: Andreas Haas <ahaas@chromium.org>
Date: Wed Jun 28 12:35:36 2017

[wasm] Check that a function body exists before verifying it.

R=clemensh@chromium.org
BUG=chromium:737069

Change-Id: Ic651c8e84eb8d3e1181355cf44aadf4c4009245b
Reviewed-on: https://chromium-review.googlesource.com/552145
Commit-Queue: Andreas Haas <ahaas@chromium.org>
Reviewed-by: Clemens Hammacher <clemensh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#46285}
[modify] https://crrev.com/a15030304ac030262f6a59e24d5833251fe4db8a/src/wasm/module-decoder.cc
[add] https://crrev.com/a15030304ac030262f6a59e24d5833251fe4db8a/test/mjsunit/regress/wasm/regression-737069.js


### sh...@chromium.org (2017-06-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-28)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ah...@chromium.org (2017-06-28)

[Empty comment from Monorail migration]

### mm...@chromium.org (2017-06-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-06-29)

ClusterFuzz has detected this issue as fixed in range 483124:483186.

Detailed report: https://clusterfuzz.com/testcase?key=5934685426548736

Job Type: windows_asan_chrome
Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x0e22bde4
Crash State:
  v8::internal::wasm::WasmDecoder::DecodeLocals
  v8::internal::wasm::WasmFullDecoder::Decode
  v8::internal::wasm::VerifyWasmCode
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Fixed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=483124:483186

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5934685426548736


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2017-06-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-06-29)

Detailed report: https://clusterfuzz.com/testcase?key=5934685426548736

Job Type: windows_asan_chrome
Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x0e22bde4
Crash State:
  v8::internal::wasm::WasmDecoder::DecodeLocals
  v8::internal::wasm::WasmFullDecoder::Decode
  v8::internal::wasm::VerifyWasmCode
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=449265:449291
Fixed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=483124:483186

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5934685426548736


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

The recommended severity is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.


### ah...@chromium.org (2017-06-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-30)

This bug requires manual review: M60 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), josafat@(ChromeOS), bustamante@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-06-30)

M59 is already at 100% and there are no respins planned. Please confirm if this bug warrants a respin. Please also list impacted OS. 

### ha...@chromium.org (2017-07-10)

Please merge to V8 6.0.

### bu...@chromium.org (2017-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/9d2da53097c4a37918b546cdae3309fb345318f2

commit 9d2da53097c4a37918b546cdae3309fb345318f2
Author: Andreas Haas <ahaas@google.com>
Date: Mon Jul 10 13:09:50 2017

Merged: [wasm] Check that a function body exists before verifying it.

There was a merge conflict, I had to do the changes again on the branch.
I did not remove the ok() check in the for loop, just to make the change
more conservative.

Revision: a15030304ac030262f6a59e24d5833251fe4db8a

BUG=chromium:737069
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=clemensh@chromium.org

Change-Id: I7fce9fe19fbf33a7b65fb01e8fb393f27029c8e7
Reviewed-on: https://chromium-review.googlesource.com/565290
Reviewed-by: Clemens Hammacher <clemensh@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.0@{#61}
Cr-Branched-From: 97dbf624a5eeffb3a8df36d24cdb2a883137385f-refs/heads/6.0.286@{#1}
Cr-Branched-From: 12e6f1cb5cd9616da7b9d4a7655c088778a6d415-refs/heads/master@{#45439}
[modify] https://crrev.com/9d2da53097c4a37918b546cdae3309fb345318f2/src/wasm/module-decoder.cc
[add] https://crrev.com/9d2da53097c4a37918b546cdae3309fb345318f2/test/mjsunit/regress/wasm/regression-737069.js


### ab...@chromium.org (2017-07-10)

Please merge this to M60 ASAP. branch:3112

### ah...@chromium.org (2017-07-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@google.com (2017-07-24)

Hi xilingggong@ - the VRP panel decided to award $1,000 for this bug, but they would re-consider for a higher amount if you could demonstrate that this could lead to memory corruption.  Thanks!

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-26)

[Empty comment from Monorail migration]

### xi...@gmail.com (2017-08-22)

Hi, will this issue receive a CVE?

### sh...@chromium.org (2017-10-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-10-05)

This issue was migrated from crbug.com/chromium/737069?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088207)*

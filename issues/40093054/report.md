# heap-use-after-free on sw::Renderer::finishRendering

| Field | Value |
|-------|-------|
| **Issue ID** | [40093054](https://issues.chromium.org/issues/40093054) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>GPU>Internals, Internals>GPU>SwiftShader |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | su...@chromium.org |
| **Created** | 2018-11-13 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
1. Download asan version asan-linux-release-606772
2. Run ./chrome.exe --disable-gpu poc.html

What is the expected behavior?

What went wrong?
Can get UAF stably

Did this work before? N/A 

Chrome version: 72.0.3607.0  Channel: stable
OS Version: 16.04
Flash Version:

## Attachments

- [utility.js](attachments/utility.js) (text/plain, 2.0 KB)
- [poc.html](attachments/poc.html) (text/plain, 998 B)
- [asan.log](attachments/asan.log) (text/plain, 14.9 KB)

## Timeline

### cl...@chromium.org (2018-11-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5223968438747136.

### cl...@chromium.org (2018-11-14)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>GPU>Internals Internals>GPU>SwiftShader]

### cl...@chromium.org (2018-11-14)

Detailed report: https://clusterfuzz.com/testcase?key=5223968438747136

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x6090016826cc
Crash State:
  sw::Renderer::finishRendering
  es2::Query::~Query
  gpu::gles2::AbstractIntegerQuery::Destroy
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=526747:526751

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5223968438747136

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### sh...@chromium.org (2018-11-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-14)

[Empty comment from Monorail migration]

### su...@chromium.org (2018-11-14)

[Empty comment from Monorail migration]

### dr...@chromium.org (2018-11-14)

Lowering the severity to Medium due to the need for the --disable-gpu flag.

Also assigning to sugoi@, as a third_party/swiftshader OWNER. Can you triage this to the right person?

### ca...@chromium.org (2018-11-14)

The --disable-gpu flag isn't strictly necessary. Chrome falls back to using SwiftShader when the GPU process crashes three times, which is easy to achieve. So any SwiftShader vulnerability affects all our users (see also https://googleprojectzero.blogspot.com/2018/10/heap-feng-shader-exploiting-swiftshader.html).

sugoi@ already has a fix.

### bu...@chromium.org (2018-11-14)

The following revision refers to this bug:
  https://swiftshader.googlesource.com/SwiftShader.git/+/3fc6893c8b24c0490ce90dc427b781732a98ff38

commit 3fc6893c8b24c0490ce90dc427b781732a98ff38
Author: Alexis Hetu <sugoi@google.com>
Date: Wed Nov 14 20:45:40 2018

Prevent glDeleteQueries from deleting a live Query

glDeleteQueries() instantly deletes all the es2::Query objects
passed as arguments to this function. If some of these queries
are still being used by the renderer, this will result in a use
after free error. To solve this issue, sw::Query is now a also
ref counted object.

https://crbug.com/chromium/904714

Change-Id: Ic1d5781bbf1724d8d07936fd49c8a172dc3d9fd4
Reviewed-on: https://swiftshader-review.googlesource.com/c/22548
Tested-by: Alexis Hétu <sugoi@google.com>
Reviewed-by: Nicolas Capens <nicolascapens@google.com>

[modify] https://crrev.com/3fc6893c8b24c0490ce90dc427b781732a98ff38/src/D3D9/Direct3DQuery9.cpp
[modify] https://crrev.com/3fc6893c8b24c0490ce90dc427b781732a98ff38/src/OpenGL/libGLESv2/Query.cpp
[modify] https://crrev.com/3fc6893c8b24c0490ce90dc427b781732a98ff38/src/Renderer/Renderer.cpp
[modify] https://crrev.com/3fc6893c8b24c0490ce90dc427b781732a98ff38/src/Renderer/Renderer.hpp


### cl...@chromium.org (2018-11-16)

ClusterFuzz has detected this issue as fixed in range 608433:608443.

Detailed report: https://clusterfuzz.com/testcase?key=5223968438747136

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x6090016826cc
Crash State:
  sw::Renderer::finishRendering
  es2::Query::~Query
  gpu::gles2::AbstractIntegerQuery::Destroy
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=526747:526751
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=608433:608443

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5223968438747136

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-11-16)

ClusterFuzz testcase 5223968438747136 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-11-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-12-03)

Hi cdsrc2016@ - $3,000 for this report, many thanks!

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-12-04)

awhalley@  Thanks for the reward!
cheers!

### aw...@google.com (2018-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-14)

This bug requires manual review: M72 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2018-12-14)

Seems like this is already in M72 branch so no merge needed?

### ab...@google.com (2018-12-20)

[Empty comment from Monorail migration]

### aw...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/904714?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>GPU>Internals, Internals>GPU>SwiftShader]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093054)*

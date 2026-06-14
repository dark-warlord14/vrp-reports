# [LangFuzz] Crash on Heap with Array access/length and invalid read

| Field | Value |
|-------|-------|
| **Issue ID** | [40078623](https://issues.chromium.org/issues/40078623) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ul...@chromium.org |
| **Created** | 2014-01-02 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0

Steps to reproduce the problem:
1. Run the following JS code in Chrome or d8:

function f(a,i) {
  return a[i];
}
f([1,2,3], "length");
f(3);
f([1,2,3], 3);
f(34359738368, 131072);

What is the expected behavior?
No crash.

What went wrong?
Tab crashed:

Program received signal SIGSEGV, Segmentation fault.
0x0000107cff856666 in ?? ()
(gdb) bt
#0  0x0000107cff856666 in ?? ()
[...]
(gdb) x /i $pc
=> 0x107cff856666:      mov    0xf(%rbx,%rdi,8),%rbx
(gdb) info reg rbx rdi
rbx            0x38c81df04101   62432146899201
rdi            0x20000  131072

Valgrind in d8 also doesn't show any more info (no symbols up to Invoke, could be jitted code that is crashing here).

Did this work before? Yes V8 Branch 3.22 does not reproduce the issue.

Chrome version: 33.0.1750.5  Channel: dev
OS Version: Ubuntu 12.04 LTS
Flash Version: Shockwave Flash 11.2 r202

## Timeline

### in...@chromium.org (2014-01-02)

[Empty comment from Monorail migration]

### ma...@chromium.org (2014-01-03)

Assign to current V8 sheriff.

### ul...@chromium.org (2014-01-03)

The crash happens in polymorphic keyed load IC.

We are using KeyedLoadFastElementStub for loading from heap-numbers and SMIs. Looks like there is a missing case for numbers either in KeyedLoadStubCompiler::CompileElementHandlers or its callers.

Assigning to Toon.

### cl...@chromium.org (2014-01-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-05)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5642278563479552

### mb...@chromium.org (2014-01-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5642278563479552

Uploader: mbarbella@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x1a3612304110
Crash State:
  - crash stack -
  NULL
Regressed: https://cluster-fuzz.appspot.com/revisions?range=235137:235454

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95L5wlD5UiO35Bn3qAXjAzstvGoTmJeYOCJCbY_3ik_qv4ejKer2SkVLbS58aRsGFJfu1s01JEzUoiXiy1-TMdh8AraOfeGyNnRzjRf0dxb3cGvtXdXQNhuiAlMiyapmqVe4OKRGcr3WVPkAEG4AEnSXWBs-w



### ia...@chromium.org (2014-01-07)

[Empty comment from Monorail migration]

### ul...@chromium.org (2014-01-07)

Uploaded a fix: https://codereview.chromium.org/121893003/

### in...@chromium.org (2014-01-09)

https://code.google.com/p/v8/source/detail?r=18484

### cl...@chromium.org (2014-01-09)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-01-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-09)

ClusterFuzz has detected this issue as fixed in range 243560:243575.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5642278563479552

Uploader: mbarbella@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x1a3612304110
Crash State:
  - crash stack -
  NULL
Regressed: https://cluster-fuzz.appspot.com/revisions?range=235137:235454
Fixed: https://cluster-fuzz.appspot.com/revisions?range=243560:243575

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95L5wlD5UiO35Bn3qAXjAzstvGoTmJeYOCJCbY_3ik_qv4ejKer2SkVLbS58aRsGFJfu1s01JEzUoiXiy1-TMdh8AraOfeGyNnRzjRf0dxb3cGvtXdXQNhuiAlMiyapmqVe4OKRGcr3WVPkAEG4AEnSXWBs-w

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### la...@google.com (2014-01-10)

[Empty comment from Monorail migration]

### ve...@chromium.org (2014-01-15)

[Empty comment from Monorail migration]

### ul...@chromium.org (2014-01-16)

Merged to V8 3.23 branch (M33): https://code.google.com/p/v8/source/detail?r=18637

### dh...@google.com (2014-01-16)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-14)

My apologies for the delay here - $3000 for this one. I'll start the payment process today.

### ti...@chromium.org (2014-04-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-17)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-04-18)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you (Ref #233619). Thanks again for your help!


### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/331416?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078623)*

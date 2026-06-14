# Crash in v8::internal::InnerPointerToCodeCache::GcSafeFindCodeForInnerPointer

| Field | Value |
|-------|-------|
| **Issue ID** | [40083887](https://issues.chromium.org/issues/40083887) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ad...@chromium.org |
| **Created** | 2016-03-17 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5403499919048704

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7fff7ea00030
Crash State:
  v8::internal::InnerPointerToCodeCache::GcSafeFindCodeForInnerPointer
  v8::internal::InnerPointerToCodeCache::GetCacheEntry
  v8::internal::StackFrame::ComputeType
  
Regressed: V8: r34731:34732

Minimized Testcase (6.24 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96jKhOUIwG2x-H_GpJD9SJccZ--XQxptO0q_s7KiG1_2e35NghPHPjAgofvCv7ve9a2fo8kPAH-Xp9Z8fP1vnvAMgBi9kSAW-1D9dEj3pjTQ089h2LYHuHWYT4WbVV6kEdKWPX62GKIcLOoNTXl4PiqiVqr8w

Filer: hablich

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### ha...@chromium.org (2016-03-17)

A flag removal resulting in a security problem? That is strange.

### cl...@chromium.org (2016-03-17)

[Empty comment from Monorail migration]

### ad...@chromium.org (2016-03-17)

Fairly certain this is not due to anything specific about the toString change; if the blamelist is correct, it's because that patch slightly changed heap layout.

Meanwhile, I'm having trouble actually running this reproduction: the fuzzer_with_launcher_script.zip claims to not be a valid zipfile.

### cl...@chromium.org (2016-03-17)

ClusterFuzz has detected this issue as fixed in range 34867:34868.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5403499919048704

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7fff7ea00030
Crash State:
  v8::internal::InnerPointerToCodeCache::GcSafeFindCodeForInnerPointer
  v8::internal::InnerPointerToCodeCache::GetCacheEntry
  v8::internal::StackFrame::ComputeType
  
Regressed: V8: r34731:34732
Fixed: V8: r34867:34868

Minimized Testcase (6.24 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96jKhOUIwG2x-H_GpJD9SJccZ--XQxptO0q_s7KiG1_2e35NghPHPjAgofvCv7ve9a2fo8kPAH-Xp9Z8fP1vnvAMgBi9kSAW-1D9dEj3pjTQ089h2LYHuHWYT4WbVV6kEdKWPX62GKIcLOoNTXl4PiqiVqr8w

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### ad...@chromium.org (2016-03-17)

Closing per #4

### cl...@chromium.org (2016-03-18)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ha...@chromium.org (2016-03-30)

This was introduced only to ToT so no merge needed. Am I missing something?

### ti...@google.com (2016-05-24)

#7: No, you're not missing anything. If there's no "Security_Impact" label, we assume that the impact is more significant than ToT (defence in depth!). Added the label and the milestone, so this should be good to go.

### sh...@chromium.org (2016-06-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@google.com (2016-06-30)

Congrats - $3,500 for this report. We'll add this to next week's payment run.

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/595656?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083887)*

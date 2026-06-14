# CSA_ASSERT failed: IsFastElementsKind(LoadElementsKind(array))

| Field | Value |
|-------|-------|
| **Issue ID** | [40092771](https://issues.chromium.org/issues/40092771) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2018-10-19 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest Debug build of d8 on ARM64

**VERSION**  

Chrome Version: v8 latest  

Operating System: Linux on ARM64

**REPRODUCTION CASE**

o0=[1.1,2.2,3.3];  

o0'push';  

o0'push';  

o0'push';  

o0'push';  

o0'push';  

o0'push';  

o0'push';  

o0'push';  

o0'push';  

o0'push';  

o0'push';  

o0'push';  

o0'push';  

o0.**defineSetter**(100,function() {});  

o0.sort();

Crash State:

abort: CSA\_ASSERT failed: IsFastElementsKind(LoadElementsKind(array)) [../../src/code-stub-assembler.cc:1556]

==== JS stack trace =========================================

```
0: ExitFrame [pc: 0x555d7a3708]  
1: StubFrame [pc: 0x555d83b1bc]  
2: StubFrame [pc: 0x555d8554b8]  

```

Security context: 0x00004e11b0b1 <JSObject>#0#  

3: sort [0x4e103869](this=0x007f9e18abf1 <JSArray[101]>#1#)  

4: /\* anonymous \*/ [0x4e1204c1] [report2.js:16] [bytecode=0x4e120279 offset=489](this=0x007f9e181521 <JSGlobal Object>#2#)  

5: InternalFrame [pc: 0x555d496f8c]  

6: EntryFrame [pc: 0x2a602160]

==== Details ================================================

[0]: ExitFrame [pc: 0x555d7a3708]  

[1]: StubFrame [pc: 0x555d83b1bc]  

[2]: StubFrame [pc: 0x555d8554b8]  

[3]: sort [0x4e103869](this=0x007f9e18abf1 <JSArray[101]>#1#) {  

// optimized frame  

--------- s o u r c e c o d e ---------  

<No Source>  

**-------------------------** ----------------  

}  

[4]: /\* anonymous \*/ [0x4e1204c1] [report2.js:16] [bytecode=0x4e120279 offset=489](this=0x007f9e181521 <JSGlobal Object>#2#) {  

// expression stack (top to bottom)  

[11] : 0x007f9e18abf1 <JSArray[101]>#1#  

[10] : 0  

[09] : 0x000051d004d9 <undefined>  

[08] : 0x007f9e18abf1 <JSArray[101]>#1#  

[07] : 12  

[06] : 0x00004e120009 <String[1]: A>  

[05] : 0x007f9e18abf1 <JSArray[101]>#1#  

[04] : 0x007f9e18b079 <JSFunction (sfi = 0x4e1200a1)>#3#  

[03] : 100  

[02] : 0x007f9e18abf1 <JSArray[101]>#1#  

[01] : 0x00004e103869 <JSFunction sort (sfi = 0x34d0eb01)>#4#  

[00] : 0x000051d004d9 <undefined>  

--------- s o u r c e c o d e ---------  

o0=[1.1,2.2,3.3];\x0ao0'push';\x0ao0'push';\x0ao0'push';\x0ao0'push';\x0ao0'push';\x0ao0'push';\x0ao0'push';\x0ao0[...

**-------------------------** ----------------  

}

[5]: InternalFrame [pc: 0x555d496f8c]  

[6]: EntryFrame [pc: 0x2a602160]  

==== Key ============================================

# #0# 0x4e11b0b1: 0x00004e11b0b1 <JSObject> #1# 0x7f9e18abf1: 0x007f9e18abf1 <JSArray[101]> #2# 0x7f9e181521: 0x007f9e181521 <JSGlobal Object> #3# 0x7f9e18b079: 0x007f9e18b079 <JSFunction (sfi = 0x4e1200a1)> #4# 0x4e103869: 0x00004e103869 <JSFunction sort (sfi = 0x34d0eb01)>

## Timeline

### cl...@chromium.org (2018-10-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5190315991105536.

### cl...@chromium.org (2018-10-19)

Detailed report: https://clusterfuzz.com/testcase?key=5190315991105536

Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: Ill
Crash Address: 0x7efe566a06d8
Crash State:
  v8::internal::__RT_impl_Runtime_AbortJS
  v8::internal::Runtime_AbortJS
  libv8.so
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=55002:55003

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5190315991105536

See https://github.com/google/clusterfuzz-tools for more information.

### cl...@chromium.org (2018-10-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5189804084690944.

### in...@chromium.org (2018-10-19)

Looks like i uploaded to the wrong job type, reuploading.

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2018-10-19)

Detailed report: <https://clusterfuzz.com/testcase?key=5189804084690944>

Job Type: linux\_asan\_d8\_v8\_arm64\_dbg  

Platform Id: linux

Crash Type: Ill  

Crash Address: 0x7f28948306d8  

Crash State:  

v8::internal::\_\_RT\_impl\_Runtime\_AbortJS  

v8::internal::Runtime\_AbortJS  

v8::internal::Simulator::DoRuntimeCall

Sanitizer: address (ASAN)

Reproducer Testcase: <https://clusterfuzz.com/download?testcase_id=5189804084690944>

No crash found using linux\_d8\_dbg job.

See <https://github.com/google/clusterfuzz-tools> for more information.

**Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days we've been seeing this crash frequently. If you are unable to reproduce this, please try a speculative fix based on the crash stacktrace in the report. The fix can be verified by looking at the crash statistics in the report, a day after the fix is deployed. We will auto-close the bug if the crash is not seen for 14 days.**

### cl...@chromium.org (2018-10-19)

Detailed report: <https://clusterfuzz.com/testcase?key=5189804084690944>

Job Type: linux\_asan\_d8\_v8\_arm64\_dbg  

Platform Id: linux

Crash Type: Ill  

Crash Address: 0x7f28948306d8  

Crash State:  

v8::internal::\_\_RT\_impl\_Runtime\_AbortJS  

v8::internal::Runtime\_AbortJS  

v8::internal::Simulator::DoRuntimeCall

Sanitizer: address (ASAN)

Reproducer Testcase: <https://clusterfuzz.com/download?testcase_id=5189804084690944>

Fully reproducible crash found using linux\_d8\_dbg job.

See <https://github.com/google/clusterfuzz-tools> for more information.

**Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days we've been seeing this crash frequently. If you are unable to reproduce this, please try a speculative fix based on the crash stacktrace in the report. The fix can be verified by looking at the crash statistics in the report, a day after the fix is deployed. We will auto-close the bug if the crash is not seen for 14 days.**

### cl...@chromium.org (2018-10-19)

Detailed report: <https://clusterfuzz.com/testcase?key=5190315991105536>

Job Type: linux\_asan\_d8\_dbg  

Platform Id: linux

Crash Type: Ill  

Crash Address: 0x7efe566a06d8  

Crash State:  

v8::internal::\_\_RT\_impl\_Runtime\_AbortJS  

v8::internal::Runtime\_AbortJS  

libv8.so

Sanitizer: address (ASAN)

Reproducer Testcase: <https://clusterfuzz.com/download?testcase_id=5190315991105536>

Fully reproducible crash found using linux\_d8\_dbg job.

See <https://github.com/google/clusterfuzz-tools> for more information.

**Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days we've been seeing this crash frequently. If you are unable to reproduce this, please try a speculative fix based on the crash stacktrace in the report. The fix can be verified by looking at the crash statistics in the report, a day after the fix is deployed. We will auto-close the bug if the crash is not seen for 14 days.**

### cl...@chromium.org (2018-10-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5727952749461504.

### in...@chromium.org (2018-10-20)

Can you please triage if this assert failure has any security implications.

### cl...@chromium.org (2018-10-20)

Testcase 5727952749461504 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5727952749461504.

### cl...@chromium.org (2018-10-22)

It's sad that ClusterFuzz merges this with other (unrelated) AbortJS crashes. Maybe we should change the way we generate CSA_ASSERTs.

Also, ClusterFuzz fails to generate a good regression range. From it's output it seems to be 55002:55004, which contains:
[array] Move Array.p.sort to Torque and use TimSort instead of QuickSort

### cl...@chromium.org (2018-10-22)

[Empty comment from Monorail migration]

### jg...@chromium.org (2018-10-22)

Taking this since since it looks related to Array.p.sort. Haven't been able to repro locally yet. The assertion failure is in CodeStubAssembler::LoadFastJSArrayLength but we don't know where it is called from.

### jg...@chromium.org (2018-10-22)

GetReceiverLengthProperty was buggy, always using .length_fast even though the JSArray may be slow.

https://cs.chromium.org/chromium/src/v8/third_party/v8/builtins/array-sort.tq?l=552&rcl=9958694f841a89cff68bdab0c2a5e13c052c68fd

This was recently fixed (presumably accidentally) by https://crrev.com/c/1281603, which replaced all .length_fast uses.

No backmerge necessary since this only happened within assertions.

### da...@chromium.org (2018-10-22)

Definitely not by accident. ;-) This seems to be the first documented instance of a bug that was implicitly fixed by rigorously applying Torque's strong typing (the fix removed an "UnsafeCast<>" which was indeed unsafe).

### sh...@chromium.org (2018-10-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-31)

Hi cloudfuzzer@ - the VRP panel decided to award $500 in this case as it was useful in helping us fix some infrastructure issues. Cheers!

### aw...@google.com (2018-10-31)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-11-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-01-28)

This issue was migrated from crbug.com/chromium/897110?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/906874]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092771)*

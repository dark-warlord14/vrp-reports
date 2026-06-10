# DCHECK failure in Handle<To> v8::internal::Cast(Handle<From>, const v8::SourceLocation &) [To = v8

| Field | Value |
|-------|-------|
| **Issue ID** | [374627491](https://issues.chromium.org/issues/374627491) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 132.0.0.0 |
| **Reporter** | dd...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2024-10-21 |
| **Bounty** | $7,000.00 |

## Description

# Steps to reproduce the problem

1. download d8-asan-linux-debug-v8-component-96641
2. unzip that
3. run d8 ./poc.js

# Problem Description

```
#
# Fatal error in ../../src/objects/objects.cc, line 353
# Debug check failed: Handle<To> v8::internal::Cast(Handle<From>, const v8::SourceLocation &) [To = v8::internal::JSReceiver, From = v8::internal::Object].
#
#
#
#FailureMessage Object: 0x7bc62e2f9c60
==== C stack trace ===============================

    ./google-cloud-sdk/d8-asan-linux-debug-v8-component-96641/d8(__interceptor_backtrace+0x46) [0x55cbd91b17a6]
    /root/google-cloud-sdk/d8-asan-linux-debug-v8-component-96641/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fc6317c8573]
    /root/google-cloud-sdk/d8-asan-linux-debug-v8-component-96641/libv8_libplatform.so(+0x3687a) [0x7fc63171c87a]
    /root/google-cloud-sdk/d8-asan-linux-debug-v8-component-96641/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x2a0) [0x7fc631792c80]
    /root/google-cloud-sdk/d8-asan-linux-debug-v8-component-96641/libv8_libbase.so(+0x56d3f) [0x7fc631791d3f]
    /root/google-cloud-sdk/d8-asan-linux-debug-v8-component-96641/libv8.so(v8::internal::Handle<v8::internal::JSReceiver> v8::internal::Cast<v8::internal::JSReceiver, v8::internal::Object>(v8::internal::Handle<v8::internal::Object>, v8::SourceLocation const&)+0x1b2) [0x7fc635ba53f2]
    /root/google-cloud-sdk/d8-asan-linux-debug-v8-component-96641/libv8.so(v8::internal::Object::ConvertToNumeric(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>)+0x1ba) [0x7fc637bd9dba]
    /root/google-cloud-sdk/d8-asan-linux-debug-v8-component-96641/libv8.so(v8::internal::Object::ToNumeric(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>)+0x3d1) [0x7fc635aacda1]
    /root/google-cloud-sdk/d8-asan-linux-debug-v8-component-96641/libv8.so(+0x6acfa0d) [0x7fc6382b3a0d]
    /root/google-cloud-sdk/d8-asan-linux-debug-v8-component-96641/libv8.so(v8::internal::Runtime_ToNumeric(int, unsigned long*, v8::internal::Isolate*)+0x1da) [0x7fc6382b315a]
    /root/google-cloud-sdk/d8-asan-linux-debug-v8-component-96641/libv8.so(+0x3a58afd) [0x7fc63523cafd]
AddressSanitizer:DEADLYSIGNAL
=================================================================
==1914346==ERROR: AddressSanitizer: TRAP on unknown address 0x000000000000 (pc 0x7fc6317c3690 bp 0x7ffe27e76810 sp 0x7ffe27e76810 T0)
SCARINESS: 10 (signal)
    #0 0x7fc6317c3690 in v8::base::OS::Abort() src/base/platform/platform-posix.cc:730:7
    #1 0x7fc631792c9b in V8_Fatal(char const*, int, char const*, ...) src/base/logging.cc:215:3
    #2 0x7fc631791d3e in v8::base::(anonymous namespace)::DefaultDcheckHandler(char const*, int, char const*) src/base/logging.cc:59:3
    #3 0x7fc635ba53f1 in v8::internal::Handle<v8::internal::JSReceiver> v8::internal::Cast<v8::internal::JSReceiver, v8::internal::Object>(v8::internal::Handle<v8::internal::Object>, v8::SourceLocation const&) src/handles/handles-inl.h:50:3
    #4 0x7fc637bd9db9 in v8::internal::Object::ConvertToNumeric(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>) src/objects/objects.cc:350:5
    #5 0x7fc635aacda0 in v8::internal::Object::ToNumeric(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>) src/objects/objects-inl.h:816:10
    #6 0x7fc6382b3a0c in v8::internal::__RT_impl_Runtime_ToNumeric(v8::internal::Arguments<(v8::internal::ArgumentsType)0>, v8::internal::Isolate*) src/runtime/runtime-object.cc:1231:3
    #7 0x7fc6382b3159 in v8::internal::Runtime_ToNumeric(int, unsigned long*, v8::internal::Isolate*) src/runtime/runtime-object.cc:1227:1
    #8 0x7fc63523cafc in Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc
    #9 0x7fc635454701 in Builtins_NonNumberToNumeric setup-isolate-deserialize.cc
    #10 0x7fc6358490d4 in Builtins_ShiftRightLogicalHandler setup-isolate-deserialize.cc
    #11 0x7fc634e5754e in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #12 0x7fc634e58162 in Builtins_InterpreterPushArgsThenFastConstructFunction setup-isolate-deserialize.cc
    #13 0x7fc63587725c in Builtins_ConstructHandler setup-isolate-deserialize.cc
    #14 0x7fc634e5754e in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc
    #15 0x7fc634e4e5db in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc
    #16 0x7fc634e4e31e in Builtins_JSEntry setup-isolate-deserialize.cc
    #17 0x7fc63659536a in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/simulator.h:191:12
    #18 0x7fc63659903c in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>) src/execution/execution.cc:517:10
    #19 0x7fc635a5b263 in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) src/api/api.cc:2140:7
    #20 0x55cbd927e335 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::ReportExceptions, v8::Global<v8::Value>*) 

```
# Summary

Type Confusion in ConvertToNumeric

# Custom Questions

#### Type of crash:

tab

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 425 B)

## Timeline

### ps...@google.com (2024-10-21)

Confirmed by cluster fuzz. https://clusterfuzz.com/testcase-detail/6327374975008768. Was unable to attach report to bug for some reason. But with confirmation, going to hand off to V8 Shepard. Setting provisional severity to S1 and P1

### sa...@google.com (2024-10-21)

Assigning to correct shepherd for this week.

### cl...@appspot.gserviceaccount.com (2024-10-21)

Detailed Report: https://clusterfuzz.com/testcase?key=6327374975008768

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  Handle<To> v8::internal::Cast(Handle<From>, const v8::SourceLocation &) [To = v8
  v8::internal::Handle<v8::internal::JSReceiver> v8::internal::Cast<v8::internal::
  v8::internal::Object::ConvertToNumeric
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=94372:94373

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6327374975008768

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2024-10-21)

Bisects to `ed01326 [tagged] Introduce a Union type by Leszek Swirski · 4 months ago`.

I'll try locally if it bisects further.

### le...@chromium.org (2024-10-21)

fwiw that CL split ConvertToNumberOrNumeric into ConvertToNumber and ConvertToNumeric, which is likely why this error bisects to that.

### 24...@project.gserviceaccount.com (2024-10-21)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### cl...@chromium.org (2024-10-21)

Hm, my bisection script first reproduced this error, then `Debug check failed: IsPrimitiveMap(*this) || instance_type() == WASM_NULL_TYPE`, and then `Debug check failed: (heap) != nullptr`.

Then we are at the beginning of 2023 and remoteexec stops working :/

### le...@chromium.org (2024-10-21)

Well the good news is that the value is a hole, and we're now reasonably ok with hole leaks as being well bottlenecked for security issues (cc cffsmith)

### pe...@google.com (2024-10-21)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-10-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### cl...@chromium.org (2024-10-21)

The latest bisection (for `Debug check failed: (heap) != nullptr`) results in <https://crrev.com/c/4521712> (`[interpreter] Enable TDZ elision by default`).

Before that, we get `ReferenceError: Must call super constructor in derived class before accessing 'this' or returning from derived constructor`.

### cl...@chromium.org (2024-10-22)

Shu, can you take this one?

TDZ seems to be "temporal dead zone", and from <https://crbug.com/42203665> I learned that this is the same as "hole elision" (quote: `TDZ elision (aka "hole elision" in the codebase)`).

So this seems highly related.

### pe...@google.com (2024-11-06)

syg: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dd...@gmail.com (2024-11-18)

Any update?

### sy...@chromium.org (2024-11-18)

Sorry I had missed this, taking a look.

### ap...@google.com (2024-11-19)

Project: v8/v8  

Branch: main  

Author: Shu-yu Guo <[syg@chromium.org](mailto:syg@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6032225>

[interpreter] Fix hole elision scope for switch jump tables

---


Expand for full commit details
```
[interpreter] Fix hole elision scope for switch jump tables 
 
Fixed: 374627491 
Change-Id: I7b6142b45295ba795a8ae8a90692fc09e704b65d 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6032225 
Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
Commit-Queue: Shu-yu Guo <syg@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#97274}

```

---

Files:

- M `src/interpreter/bytecode-generator.cc`
- A `test/mjsunit/regress/regress-374627491.js`

---

Hash: 5c3b50c26c50e68dbedf8ff991249e75e46ef06e  

Date:  Mon Nov 18 16:02:28 2024


---

### 24...@project.gserviceaccount.com (2024-11-20)

ClusterFuzz testcase 6327374975008768 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=97273:97274

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pe...@google.com (2024-11-20)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M132. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pe...@google.com (2024-11-20)

Merge review required: M132 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), alonbajayo (ChromeOS), srinivassista (Desktop)

### sy...@chromium.org (2024-11-20)

1. It is a security bug fix.
2. <https://chromium-review.googlesource.com/c/v8/v8/+/6032225>
3. Yes
4. No, not a new feature.
5. N/A
6. No manual verification needed.

### am...@chromium.org (2024-11-22)

<https://crrev.com/c/6032225> approved for merge to 132;

Please merge this fix to 13.2 at your convenience and by EOD 3 December, so this fix can be included in the next M132 beta update following the current release freeze

### ap...@google.com (2024-11-22)

Project: v8/v8  

Branch: refs/branch-heads/13.2  

Author: Shu-yu Guo <[syg@chromium.org](mailto:syg@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6042925>

Merged: [interpreter] Fix hole elision scope for switch jump tables

---


Expand for full commit details
```
Merged: [interpreter] Fix hole elision scope for switch jump tables 
 
(cherry picked from commit 5c3b50c26c50e68dbedf8ff991249e75e46ef06e) 
 
Change-Id: Id6bf2b62598b85a05c6cc7bd06b6cce673d7342a 
Bug: 374627491 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6042925 
Commit-Queue: Shu-yu Guo <syg@chromium.org> 
Commit-Queue: Rezvan Mahdavi Hezaveh <rezvan@chromium.org> 
Auto-Submit: Shu-yu Guo <syg@chromium.org> 
Reviewed-by: Rezvan Mahdavi Hezaveh <rezvan@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.2@{#18} 
Cr-Branched-From: 24068c59cedad9ee976ddc05431f5f497b1ebd71-refs/heads/13.2.152@{#1} 
Cr-Branched-From: 6054ba94db0969220be4f94dc1677fc4696bdc4f-refs/heads/main@{#97085}

```

---

Files:

- M `src/interpreter/bytecode-generator.cc`
- A `test/mjsunit/regress/regress-374627491.js`

---

Hash: 3c2d220ad025e2c532ea17289d8d29350f0b722a  

Date:  Mon Nov 18 16:02:28 2024


---

### dd...@gmail.com (2024-11-24)

According the impacts analysis of CF, this bug affect 'Extended\_Stable 130.0.6723.127' and 'Stable 131.0.6778.69'. So will this issue get CVE?

### pe...@google.com (2024-11-25)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sy...@chromium.org (2024-11-25)

For the LTS questions:

1. Yes. AFAICT this has been present since M114 (<https://chromiumdash.appspot.com/commit/da0bcffa3d0c86cb992250f160c32302e54fb557>)
2. No. See above.

### pe...@google.com (2024-11-26)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2024-11-26)

1. https://chromium-review.googlesource.com/c/v8/v8/+/6048230
2. Low, there are small conflicts.
3. 132.
4. Yes, as mentioned in the comment #26, the issue has been present since M114.

### pe...@google.com (2024-11-26)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2024-11-27)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
report of memory corruption in a sandboxed process / renderer


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-28)

Congratulations! Thank you for your efforts and reporting this issue to us.

### dd...@gmail.com (2024-11-28)

Thank you Amy. BTW, please answer the #c24, because the foundin of this issue seems not complete

### cl...@chromium.org (2024-11-28)

Ack, this is a pretty old bug. <https://crrev.com/c/4521712> landed in M-115, and <https://crrev.com/c/4405039> in M-114 (also see #c26).

### sr...@chromium.org (2024-12-02)

Please help complete your merges to M132 branch before 12pm PST tomorrow ( Tuesday Dec 3rd) so the change can be included in this weeks beta release. 

### go...@google.com (2024-12-02)

Please merge your change to M132 ASAP so we can take it in for this week's Beta release on Wedbesday, RC cut tomorrow at 10:00 AM PT.

Please see branch details here: https://chromiumdash.appspot.com/branches.

### ap...@google.com (2025-01-27)

Project: v8/v8  

Branch: refs/branch-heads/12.6  

Author: Gyuyoung Kim <[qkim@google.com](mailto:qkim@google.com)>  

Link:      <https://chromium-review.googlesource.com/6048230>

[M126-LTS][interpreter] Fix hole elision scope for switch jump tables

---


Expand for full commit details
```
[M126-LTS][interpreter] Fix hole elision scope for switch jump tables 
 
(cherry picked from commit 5c3b50c26c50e68dbedf8ff991249e75e46ef06e) 
 
Fixed: 374627491 
Change-Id: I7b6142b45295ba795a8ae8a90692fc09e704b65d 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6032225 
Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
Commit-Queue: Shu-yu Guo <syg@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#97274} 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6048230 
Reviewed-by: Shu-yu Guo <syg@chromium.org> 
Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
Cr-Commit-Position: refs/branch-heads/12.6@{#84} 
Cr-Branched-From: 3c9fa12db3183a6f4ea53d2675adb66ea1194529-refs/heads/12.6.228@{#2} 
Cr-Branched-From: 981bb15ba4dbf9e2381dfc94ec2c4af0b9c6a0b6-refs/heads/main@{#93835}

```

---

Files:

- M `src/interpreter/bytecode-generator.cc`
- A `test/mjsunit/regress/regress-374627491.js`

---

Hash: 7c5364450454daabe31f09768ad4afb898efc91d  

Date:  Tue Nov 26 07:30:41 2024


---

### ch...@google.com (2025-02-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/374627491)*

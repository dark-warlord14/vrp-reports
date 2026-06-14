# JS object corruption in WasmJs::InstallTypeReflection

| Field | Value |
|-------|-------|
| **Issue ID** | [331383939](https://issues.chromium.org/issues/331383939) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>API, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m-...@github.com |
| **Assignee** | ah...@chromium.org |
| **Created** | 2024-03-27 |
| **Bounty** | $10,000.00 |

## Description

VULNERABILITY DETAILS

In InstallConditionalFeatures, a check is in place to check that the `WebAssembly` object does not contain the `Function` property to avoid adding duplicate properties in the object:

```
void WasmJs::InstallConditionalFeatures(Isolate* isolate,
                                        Handle<NativeContext> context) {
    ...
    // Install Wasm type reflection features (if not already done).
    Handle<String> function_string = v8_str(isolate, "Function");
    if (!JSObject::HasRealNamedProperty(isolate, webassembly, function_string)
             .FromMaybe(true)) {
      InstallTypeReflection(isolate, context);
    }
  }
}
``` 
However, `InstallTypeReflection` also add properties in various other objects, and those are not checked:

```
void WasmJs::InstallTypeReflection(Isolate* isolate,
                                   Handle<NativeContext> context) {
  Handle<JSObject> webassembly(context->wasm_webassembly_object(), isolate);

#define INSTANCE_PROTO_HANDLE(Name) \
  handle(JSObject::cast(context->Name()->instance_prototype()), isolate)
  InstallFunc(isolate, INSTANCE_PROTO_HANDLE(wasm_table_constructor), "type",
              WebAssemblyTableType, 0, false, NONE,
              SideEffectType::kHasNoSideEffect);
  InstallFunc(isolate, INSTANCE_PROTO_HANDLE(wasm_memory_constructor), "type",
              WebAssemblyMemoryType, 0, false, NONE,
              SideEffectType::kHasNoSideEffect);
  InstallFunc(isolate, INSTANCE_PROTO_HANDLE(wasm_global_constructor), "type",
              WebAssemblyGlobalType, 0, false, NONE,
              SideEffectType::kHasNoSideEffect);
  InstallFunc(isolate, INSTANCE_PROTO_HANDLE(wasm_tag_constructor), "type",
              WebAssemblyTagType, 0);
#undef INSTANCE_PROTO_HANDLE
...
```

In the above, the `type` property is added to the `prototype` of `wasm_table_constructor` etc., without checking that the properties already exists. This leads to issues like 40056206 where duplicate properties are installed on objects.

Thank you very much for your help and please let me know if there is anything I can help. As with 40056206, the bug depends on origin trial and only affects Chrome version 123 onwards after the JSPI origin trial started.

VERSION
Chromium version 123.0.6312.58 stable
OS: Ubuntu 22.04 LTS 

REPRODUCTION CASE
To simulate origin trial token locally, apply the patch `trial-token.patch` to accept the token from the test cases. Then open `wasm_type.html` in Chrome. In a debug build, the renderer should crash with a `DCHECK` failure when duplicated properties are added.

CREDIT INFORMATION
Reporter credit: Man Yue Mo of GitHub Security Lab

## Attachments

- [trial-token.patch](attachments/trial-token.patch) (text/x-diff, 1.1 KB)
- [wasm_type.html](attachments/wasm_type.html) (text/html, 357 B)
- [wasm_poc.html](attachments/wasm_poc.html) (text/html, 4.9 KB)

## Timeline

### pa...@chromium.org (2024-03-27)

[security shepherd] I wasn't able to reproduce this. Setting severity and found-in provisionally. Assigning to clemensb@. This seems indeed related to [crbug.com/331358160](https://crbug.com/331358160). Not sure whether that's a dup or a different issue.

### cl...@chromium.org (2024-03-27)

Andreas, you fixed similar issues before, can you take this one?

### pe...@google.com (2024-03-28)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-03-28)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ah...@chromium.org (2024-04-02)

This issue is only relevant for M123 and later, because only M123 introduces the origin trial that can trigger this issue.

### ap...@google.com (2024-04-03)

Project: v8/v8
Branch: main

commit 292c5a8536ae0a70ac59d8ea8b3bdcceac44e8a5
Author: Andreas Haas <ahaas@chromium.org>
Date:   Tue Apr 02 13:53:10 2024

    [wasm] Check for all new fields before calling InstallTypeReflection
    
    The origin trial of JSPI can enable the type reflection proposal after
    some JavaScript code has already been executed. This JavaScript code can
    already add the fields to objects that would be added by the type
    reflection proposal. Therefore, if any of these fields already exists,
    the type reflection proposal cannot be activated.
    
    With this CL we check for all fields that get added with the type
    reflection proposal, and don't add any fields if one of them exists
    already.
    
    R=fgm@chromium.org
    
    Bug: 331383939
    Change-Id: I551f4aebf5429fd08b79435723100a4e93bba715
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5412655
    Reviewed-by: Francis McCabe <fgm@chromium.org>
    Commit-Queue: Andreas Haas <ahaas@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#93126}

M       src/wasm/wasm-js.cc

https://chromium-review.googlesource.com/5412655


### pe...@google.com (2024-04-03)

This is sufficiently serious that it should be merged to stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M123. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to beta. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M124. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### m-...@github.com (2024-04-03)

The issue can be exploited by using `CloneObjectIC` to create an object that has inconsistent `Map` and `PropertyArray` (more specifically, a `target` object with an inconsistent `UnusedPropertyField` in `Map` and `PropertyArray` size if the `source` object has a duplicate property) The attached test case demonstrates this to gain arbitrary read and write in the v8 heap, which is readily exploitable on 32 bit Chrome (that is still used on Android devices with <= 4GB ram), on 64 bit platforms, the sandbox escape fixed here: <https://source.chromium.org/chromium/_/chromium/v8/v8.git/+/80dad0bec2061ae0620895da97dfc1bf89b100f9> can be used to gain code execution. The `importedTargets` array in a WebAssembly instance can be used to gain control of the instruction pointer (and also leaks the address of the Builtin function `kWasmToJsWrapperAsm`. This should be sufficient to gain code execution. The test case will print out the addresses of some objects, and then crash by setting the instruction pointer to an invalid location. Control of instruction pointer can be verified by attaching a debugger.

The bug only affects version 123 onwards and should only be a problem when origin trial is active. It was probably introduced in this commit: <https://source.chromium.org/chromium/_/chromium/v8/v8.git/+/cf70bd3b911510bdba8a657c3805a221a908f55b>

### pe...@google.com (2024-04-04)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=331383939&entry.958145677=Android, Fuchsia, Linux, Mac, Windows, Lacros, ChromeOS&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript>API, Blink>JavaScript>WebAssembly&entry.975983575=ahaas@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

### pe...@google.com (2024-04-04)

Merge review required: M124 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

### pe...@google.com (2024-04-04)

Merge review required: M123 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

### am...@chromium.org (2024-04-08)

<https://crrev.com/c/5412655> approved for merge to M124, please merge this fix to 12.4 by 10am Pacific time tomorrow (Tuesday 9 April) so this fix can be included in tomorrow's M124 Stable Cut for release next week

The final M123 Stable release is being cut right now, so no merge to M123 is needed at this time

### fg...@chromium.org (2024-04-08)

Ack.

### go...@google.com (2024-04-08)

Please merge your change to M124 latest by 10:00 AM PT tomorrow, Tuesday, April 9th so it can be picked up by Early Stable release.

Branch Details: https://chromiumdash.appspot.com/branches



### cl...@chromium.org (2024-04-09)

Andreas is out today, I prepared the merge to 12.4: https://crrev.com/c/5438115

### cl...@chromium.org (2024-04-09)

Jakob, do you think we should also merge https://crrev.com/c/5423130?

### cl...@chromium.org (2024-04-09)

Actually, that would / should be merged as part of https://crbug.com/331358160 I think...

### ap...@google.com (2024-04-09)

Project: v8/v8
Branch: refs/branch-heads/12.4

commit 2bfdfc882d737a5e94e021e88a95232707fd241e
Author: Andreas Haas <ahaas@chromium.org>
Date:   Tue Apr 02 13:53:10 2024

    Merged: [wasm] Check for all new fields before calling InstallTypeReflection
    
    The origin trial of JSPI can enable the type reflection proposal after
    some JavaScript code has already been executed. This JavaScript code can
    already add the fields to objects that would be added by the type
    reflection proposal. Therefore, if any of these fields already exists,
    the type reflection proposal cannot be activated.
    
    With this CL we check for all fields that get added with the type
    reflection proposal, and don't add any fields if one of them exists
    already.
    
    R=fgm@chromium.org
    
    (cherry picked from commit 292c5a8536ae0a70ac59d8ea8b3bdcceac44e8a5)
    Bug: 331383939
    
    Change-Id: I10040761a0479b8c7d5253eeaf9179a8fa08d3d0
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5438115
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Clemens Backes <clemensb@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.4@{#18}
    Cr-Branched-From: 309640da62fae0485c7e4f64829627c92d53b35d-refs/heads/12.4.254@{#1}
    Cr-Branched-From: 5dc24701432278556a9829d27c532f974643e6df-refs/heads/main@{#92862}

M       src/wasm/wasm-js.cc

https://chromium-review.googlesource.com/5438115


### pe...@google.com (2024-04-09)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### vo...@google.com (2024-04-09)

Not applicable to M120 LTS since the bug depends on the origin trial started in M123.

### am...@google.com (2024-04-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-11)

Congratulations on another one, Man Yue Mo! The Chrome VRP Panel has decided to award you $10,000 for this high quality report of memory corruption in a sandboxed process. Thank you for your efforts in discovering and reporting this issue to us -- nice work!

### m-...@github.com (2024-04-12)

amyressler@ Thanks. I'd like to donate the reward please. Thank you very much for your help.

### am...@chromium.org (2024-04-13)

Thanks for letting me know! I'll get back to you off-bug later next week with donation information.

### pe...@google.com (2024-07-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/331383939)*

# Insufficient fix for CVE-2021-30561

| Field | Value |
|-------|-------|
| **Issue ID** | [331358160](https://issues.chromium.org/issues/331358160) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>API, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2021-30561 |
| **Reporter** | m-...@github.com |
| **Assignee** | ah...@chromium.org |
| **Created** | 2024-03-27 |
| **Bounty** | $20,000.00 |

## Description

VULNERABILITY DETAILS
It appears that mechanisms introduced to prevent issues like 40056206 (CVE-2021-30561) is insufficient. In `InstallConditionalFeatures`, a check is introduced to check that the `webassembly` object does not have the relevant property before adding it to the object:

```
void WasmJs::InstallConditionalFeatures(Isolate* isolate,
                                        Handle<NativeContext> context) {
  ...
  MaybeHandle<Object> maybe_wasm =
      JSReceiver::GetProperty(isolate, global, "WebAssembly");    //<-------- 1.
  ...
  if (isolate->IsWasmJSPIEnabled(context)) {
    isolate->WasmInitJSPIFeature();

    Handle<String> suspender_string = v8_str(isolate, "Suspender");
    if (!JSObject::HasRealNamedProperty(isolate, webassembly, suspender_string)   //<----- 2.
             .FromMaybe(true)) {
      InstallSuspenderConstructor(isolate, context);
    }

    // Install Wasm type reflection features (if not already done).
    Handle<String> function_string = v8_str(isolate, "Function");
    if (!JSObject::HasRealNamedProperty(isolate, webassembly, function_string)
             .FromMaybe(true)) {
      InstallTypeReflection(isolate, context);
    }
  }
}

```

In the above, the object that is used in the check is the global property `WebAssembly` (1. and 2.) However, when the property is installed using `InstallSuspenderConstructor`, the object that is used is `context->wasm_webassembly_object()` (3.), which may not be the same as the `WebAssembly` global property.

```
void WasmJs::InstallSuspenderConstructor(Isolate* isolate,
                                         Handle<NativeContext> context) {
  Handle<JSObject> webassembly(context->wasm_webassembly_object(), isolate);    //<------ 3.
  Handle<JSFunction> suspender_constructor = InstallConstructorFunc(
      isolate, webassembly, "Suspender", WebAssemblySuspender);
  context->set_wasm_suspender_constructor(*suspender_constructor);
  SetupConstructor(isolate, suspender_constructor, WASM_SUSPENDER_OBJECT_TYPE,
                   WasmSuspenderObject::kHeaderSize, "WebAssembly.Suspender");
}

```

By first setting the `Suspender` property on the `WebAssembly` object and then set the global `WebAssembly` to a different object, the property name check will be performed on the newly assigned `WebAssembly` object while the property will be added in the `context->wasm_assembly_object()`, which already had a `Suspender` object. This then creates a corrupted object with a duplicated `Suspender` property. This also affects the `InstallTypeReflection` function when the `Function` property is installed.

This is somewhat related to 331383939 though with a rather different root cause, so I opened a different ticket, but please feel to merge the issues if you see fit.

Thank you very much for your help and please let me know if there is anything I can help. As with 40056206, the bug depends on origin trial and only affects Chrome version 123 onwards after the JSPI origin trial started.

VERSION
Chromium version 123.0.6312.58
OS: Ubuntu 22.04 LTS

REPRODUCTION CASE
To simulate origin trial token locally, apply the patch `trial-token.patch` to accept the token from the test cases. Then open `wasm_suspender.html` in Chrome. In a debug build, the renderer should crash with a `DCHECK` failure when duplicated properties are added.

CREDIT INFORMATION
Reporter credit: Man Yue Mo of GitHub Security Lab

## Attachments

- [trial-token.patch](attachments/trial-token.patch) (text/x-diff, 1.1 KB)
- [wasm_suspender.html](attachments/wasm_suspender.html) (text/html, 418 B)

## Timeline

### pa...@chromium.org (2024-03-27)

[security shepherd] I wasn't able to reproduce this. Setting severity and found-in provisionally. Assigning to clemensb@. This seems indeed related to [crbug.com/331383939](https://crbug.com/331383939). Not sure whether that's a dup or a different issue.

### cl...@chromium.org (2024-03-27)

Andreas, you fixed similar issues before, can you take this one?

### pe...@google.com (2024-03-28)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-03-28)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-04-03)

Project: v8/v8
Branch: main

commit c63e4c4954f38f68b69993c7f20bef6055d79ac4
Author: Andreas Haas <ahaas@chromium.org>
Date:   Wed Apr 03 10:43:30 2024

    [wasm] Correctly lookup WebAssembly object in InstallConditionalFeatures
    
    The WebAssembly object was looked up partly from the NativeContext.
    However, after user code has been executed, the WebAssembly object has
    to be retrieved with a JavaScript property lookup, because the
    WebAssembly object may have been replaced or augmented by user code.
    
    Drive-by change: I added a regression test for a similar issue where I
    forgot to add the test to the CL.
    
    Bug: 331358160
    Change-Id: Iec81830afee3352a53a27f2658408f55d62a840c
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5419093
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
    Commit-Queue: Andreas Haas <ahaas@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#93138}

M       src/wasm/wasm-js.cc
M       src/wasm/wasm-js.h
A       test/mjsunit/regress/wasm/regress-331358160.js
A       test/mjsunit/regress/wasm/regress-331383939.js

https://chromium-review.googlesource.com/5419093


### m-...@github.com (2024-04-03)

It seems that the fix for the "Function" path may not be correct. `CanInstallTypeReflection` now checks the `webassembly` object from the `context`, but `InstallTypeReflection` now installs function on the `webassembly` object that passed to it, which comes from the global `WebAssembly` property. So it looks like the problem still exists on this path, but the other way round. So if you first cache the `WebAssembly` global property, then overwrite it with something that already has the `Function` property, and then install conditional properties, you probably still have the same problem. e.g.

```
var wa = WebAssembly;
WebAssembly = {Function : 1};
d8.test.enableJSPI();
d8.test.installConditionalFeatures();

```

I'd suggest passing the `webassembly` argument to `CanInstallTypeReflection` and test that to ensure the same object that has the properties installed is also the one that is tested.

### pe...@google.com (2024-04-03)

This is sufficiently serious that it should be merged to extended stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M122. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
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


### ap...@google.com (2024-04-03)

Project: v8/v8
Branch: main

commit 49ba787fca9bd98daa1c1f4c36f0038d5640b6b2
Author: Shu-yu Guo <syg@chromium.org>
Date:   Wed Apr 03 14:01:52 2024

    [maglev] Parenthesize && inside || to quell gcc warning
    
    Bug: 331358160
    Change-Id: I307024dc5740c74d9e6ff0ce80765de4f9e27476
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5419867
    Reviewed-by: Adam Klein <adamk@chromium.org>
    Commit-Queue: Adam Klein <adamk@chromium.org>
    Auto-Submit: Shu-yu Guo <syg@chromium.org>
    Commit-Queue: Shu-yu Guo <syg@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#93149}

M       src/maglev/maglev-phi-representation-selector.cc

https://chromium-review.googlesource.com/5419867


### pe...@google.com (2024-04-04)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=331358160&entry.958145677=Android, Fuchsia, Linux, Mac, Windows, Lacros, ChromeOS&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript>API, Blink>JavaScript>WebAssembly&entry.975983575=ahaas@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

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

### pe...@google.com (2024-04-04)

Merge review required: M122 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), pbommana (Desktop)

### am...@chromium.org (2024-04-04)

Thanks for the quick work on this one ahaas@ and syg@
Since these fixes just landed on Chromium earlier this morning, I'm going to them get a bit more bake time before merge review.

### ah...@chromium.org (2024-04-05)

There is no need to merge to M122, because the origin trial only starts with M123. 

I think syg@'s CL referenced the wrong issue by accident. A final fix is still missing, I'm landing it now.

### cl...@chromium.org (2024-04-09)

Amy, please consider this for backmerge; the fix in https://crbug.com/331383939 is insufficient otherwise.

### am...@chromium.org (2024-04-09)

<https://crrev.com/c/5419867> has been approved for merge to M124, please merge this fix ASAP so this fix can be included in the M124 Stable Cut happening today

### ah...@chromium.org (2024-04-10)

The fix mentioned in #15 landed in https://chromium-review.googlesource.com/c/v8/v8/+/5423130, but for some reason it did not get added here automatically. I guess #17 meant that this CL should be merged back.

### cl...@chromium.org (2024-04-10)

The CLs to backmerge should actually be <https://crrev.com/c/5419093> and <https://crrev.com/c/5423130>.

### ap...@google.com (2024-04-11)

Project: v8/v8
Branch: refs/branch-heads/12.4

commit 5ec0b0e485dd06594c6f61e318ebea721493a832
Author: Andreas Haas <ahaas@google.com>
Date:   Thu Apr 11 12:16:05 2024

    Merged: Squashed multiple commits.
    
    Merged: [wasm] Correctly lookup WebAssembly object in InstallConditionalFeatures
    Revision: c63e4c4954f38f68b69993c7f20bef6055d79ac4
    
    Merged: [wasm] Don't load WebAssembly object in CanInstallTypeReflection
    Revision: 38e23f3a5d07022def739030d877ea224dd7952d
    
    BUG=331358160
    R=clemensb@chromium.org
    
    Change-Id: I8ba7b04d6151dafdc298715aa499b7408cd4cef3
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5447009
    Reviewed-by: Clemens Backes <clemensb@chromium.org>
    Commit-Queue: Andreas Haas <ahaas@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.4@{#22}
    Cr-Branched-From: 309640da62fae0485c7e4f64829627c92d53b35d-refs/heads/12.4.254@{#1}
    Cr-Branched-From: 5dc24701432278556a9829d27c532f974643e6df-refs/heads/main@{#92862}

M       src/wasm/wasm-js.cc
M       src/wasm/wasm-js.h

https://chromium-review.googlesource.com/5447009


### pe...@google.com (2024-04-11)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### am...@google.com (2024-04-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-11)

Congratulations Man Yue Mo! The Chrome VRP Panel has decided to award you $20,000 for this report of V8 renderer memory corruption impacting Chrome for some time (<https://g.co/chrome/vrp/#rewards-for-v8-bugs-in-stable-channel-and-older-versions>). Thank you for your efforts in discovering and reporting this issue to us -- great work!

### m-...@github.com (2024-04-12)

amyressler@ Thanks. I'd like to donate the reward please. Thank you very much for your help.

### am...@chromium.org (2024-04-13)

Thanks for letting us know! I'll get back to you off bug later next week with donation information.

### rz...@google.com (2024-04-15)

Labelling as not applicable for M120-LTS based on [comment #15](https://issues.chromium.org/issues/331358160#comment15)

### pe...@google.com (2024-04-15)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pe...@google.com (2024-07-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/331358160)*

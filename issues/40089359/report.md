# Security: V8:Use After Free Leads to Remote Code Execution

| Field | Value |
|-------|-------|
| **Issue ID** | [40089359](https://issues.chromium.org/issues/40089359) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | so...@gmail.com |
| **Assignee** | gd...@chromium.org |
| **Created** | 2017-10-20 |
| **Bounty** | $7,500.00 |

## Description


VULNERABILITY DETAILS
This is a Use After Free Vul in V8.It can cause RCE in the Chrome renderer process.More information please see the html file.It is a full exploit to open "calc.exe"
 without sandbox.

VERSION
Chrome Version: 62.0.3202.62 Stable (32bit)
Operating System: [Windows 10 1703 64bit] 8G Memory

REPRODUCTION CASE
Please see the attach file.PASS:MobilePPPP200000Zzz
Note:This is a vul I prepare for the Mobile Pwn2Own.But I prefer to report to you.

1.Open the chrome with --no-sandbox.
2.Open the html file.
3.calc.exe will spawn out.(May be need to try serveral times)

The Patch I will report soon.


## Attachments

- [hello_chrome_3.zip](attachments/hello_chrome_3.zip) (application/octet-stream, 2.3 KB)
- [poc.zip](attachments/poc.zip) (application/octet-stream, 553 B)
- [lx_clip1508495189568_lx.jpg](attachments/lx_clip1508495189568_lx.jpg) (image/jpeg, 28.9 KB)

## Timeline

### so...@gmail.com (2017-10-20)

Here is the PoC file.It works on the 62.0.3202.62 Stable Version(32bit or 64bit).
And the Mobile Pwn2Own will come soon.May be we need to repair this quickly:)

### so...@gmail.com (2017-10-20)

It can works on the latest source code build and latest chrome Canary too.(When I sumbit is 6.4.63 and 64.0.3244.0)

As I think the patch,we should always updated the wasm_context when we call the |memory.grow| function.This is more safer.

In the function |WasmMemoryObject::Grow|:
...
if (memory_object->has_instances()) {
...
Handle<WasmInstanceObject> instance(WasmInstanceObject::cast(elem),
                                          isolate);
SetInstanceMemory(isolate, instance, new_buffer);
...

if the jit function is asmjs,|if (memory_object->has_instances())| return false,it will go continue and not update the wasm_context.


### cl...@chromium.org (2017-10-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5984217585680384.

### ke...@chromium.org (2017-10-20)

Thanks for the report and the clean repro. I have verified a use-after-free in JIT.

Flagging to go into the v8 triage queue.

[Monorail components: Blink>JavaScript]

### so...@gmail.com (2017-10-20)

The root problem in the function |InstanceBuilder::Build|,if the function mode is asmjs,the following code:

 if (module_->has_memory && !instance->has_memory_object()) {
    Handle<WasmMemoryObject> memory_object = WasmMemoryObject::New(
        isolate_,
        instance->has_memory_buffer() ? handle(instance->memory_buffer())
                                      : Handle<JSArrayBuffer>::null(),
        module_->maximum_pages != 0 ? module_->maximum_pages : -1);
    instance->set_memory_object(*memory_object);
  }

will new a WasmMemoryObject |memory_obj1|,and then:

if (instance->has_memory_object()) {
    Handle<WasmMemoryObject> memory(instance->memory_object(), isolate_);
    WasmMemoryObject::AddInstance(isolate_, memory, instance);
  }

memory_obj1 will add the instance.But in the  function |WasmMemoryObject::Grow|:
the WasmMemoryObject memory_obj2 is not the same with memory_obj1,is the JSObject |memory = new WebAssembly.Memory({initial:200});|(in the PoC).So the memory_obj2 will not have a instance,|if (memory_object->has_instances())| return false.

If we transfer a WasmMemoryObject's ArrayBuffer to asmjs module,I think the instance should use the same WasmMemoryObject which transfered from JS when we build the instance.

### ha...@chromium.org (2017-10-20)

Assigning to titzer for further investigation.

[Monorail components: -Blink>JavaScript Blink>JavaScript>WebAssembly]

### ha...@chromium.org (2017-10-20)

[Empty comment from Monorail migration]

### ti...@chromium.org (2017-10-20)

Hi soulchen, thanks for the report.

Re: c5.

We cannot have the asm.js module share the same WasmMemoryObject, since that would violate JavaScript semantics (i.e. it would appear to JS code that the underlying ArrayBuffer would have its length grow--which it cannot, in normal JS).

I think the solution is to make sure that attempting to grow a memory whose underlying buffer has been shared with asm.js results in -1 (i.e. the grow operation fails).



### ti...@chromium.org (2017-10-20)

So this means, concretely:

1. The buffer underlying a WebAssembly.Memory cannot be neutered by any outside operation (e.g. postMessage()).

2. If an array buffer is used as the memory for asm.js (which currently is the only operation that makes an array buffer non-neuterable) any associated WebAssembly.Memory becomes non-growable.

3. WebAssembly.Memory checks if the underlying buffer has been subject to conditions in (2) and the grow operation fails.

For this I think we probably need to add another bit to JSArrayBuffer.

### ti...@chromium.org (2017-10-20)

Also,

3b: WebAssembly.Memory.grow actually does neuter the old buffer (again, subject to the constraints of 2, which causes the operation to fail first).

### so...@gmail.com (2017-10-20)

Re: c8.

As you meaning,not only the asm.js module,but also all the TypedArray operations(etc:new Uint32Array(memory.buffer);) would violate JavaScript semantics,too.

But on the another hand,in the other browsers(Edge,Safari),attempting to grow a memory whose underlying buffer has been shared with asm.js will success.There is no standard in the ECMAScript(I am not sure) that we can't grow that.

Will it causes some correctness BUG？

### so...@gmail.com (2017-10-20)

My meaning is,

if we |new Uint32Array(memory.buffer);|(not in the asm.js),and if we can grow the memory.buffer,it would violate JavaScript semantics,too?

### ti...@chromium.org (2017-10-20)

Correct. A JavaScript ArrayBuffer cannot change its length, except that the length can be set to zero by an operation that "detachs" the buffer--such as transferring it to a worker via postMessage(). (In V8 we use the term "neuter" instead of "detach").

### br...@chromium.org (2017-10-21)

Deepti has a tentative fix for this issue here:
https://chromium-review.googlesource.com/c/v8/v8/+/731844

This sort of breaks correct behavior in that grow will act like it's out of memory (RangeError) if the buffer has been handed to asm.js, though this strictly spec compliant in that we're just claiming to be unable to grow due to a resource constraint.

Longer term we maybe should consider doing something closer to how this worked pre-asm->wasm, where we make the asm.js code generate the neutering checks, but this fix will be easier to cherry-pick cleanly as it doesn't change code-gen.

I'm starting a separate item on the process for landing this change, stay tuned.


### br...@chromium.org (2017-10-21)

Pre-emptively requesting merge to various branches.


### sh...@chromium.org (2017-10-21)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-10-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-22)

Your change meets the bar and is auto-approved for M63. Please go ahead and merge the CL to branch 3239 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), gkihumba@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-10-22)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-10-23)

We are targeting an M62 respin on Wednesday 10/25. It's currently at 5% rollout. Do you think we'll have a fix ready, tested before Tuesday 4PM PDT?

### so...@gmail.com (2017-10-23)

Please credit me as "Zhao Qixun(@S0rryMybad) of Qihoo 360 Vulcan Team".

And can I get a [$7500+$1337] luckly bounty number for this case?This is a full exploit in the renderer process.I feel the number 1337 is very cool.

### go...@chromium.org (2017-10-23)

Please merge your change to M63 branch 3239 before 11:30 AM Monday (10/23), so we can take it in for M63 Dev/Beta release. Thank you.

### sh...@chromium.org (2017-10-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/5f960dfc06a7c95af69e2b09f772b2280168469b

commit 5f960dfc06a7c95af69e2b09f772b2280168469b
Author: Deepti Gandluri <gdeepti@chromium.org>
Date: Mon Oct 23 15:49:03 2017

[wasm] Fix Memory.grow when shared with asm.js modules

If the buffer associated with WebAssembly.Memory is used as memory
for asm.js modules, throw a range error on Memory.Grow.

Bug: chromium:776677
Change-Id: Iebcd7797fa7724002dd8073d1dbaeb98f080d316
Reviewed-on: https://chromium-review.googlesource.com/731844
Commit-Queue: Deepti Gandluri <gdeepti@chromium.org>
Reviewed-by: Brad Nelson <bradnelson@chromium.org>
Reviewed-by: Ben Titzer <titzer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#48837}
[modify] https://crrev.com/5f960dfc06a7c95af69e2b09f772b2280168469b/src/asmjs/asm-js.cc
[modify] https://crrev.com/5f960dfc06a7c95af69e2b09f772b2280168469b/src/objects-printer.cc
[modify] https://crrev.com/5f960dfc06a7c95af69e2b09f772b2280168469b/src/objects/js-array-inl.h
[modify] https://crrev.com/5f960dfc06a7c95af69e2b09f772b2280168469b/src/objects/js-array.h
[modify] https://crrev.com/5f960dfc06a7c95af69e2b09f772b2280168469b/src/wasm/module-compiler.cc
[modify] https://crrev.com/5f960dfc06a7c95af69e2b09f772b2280168469b/src/wasm/wasm-js.cc
[modify] https://crrev.com/5f960dfc06a7c95af69e2b09f772b2280168469b/src/wasm/wasm-memory.cc
[modify] https://crrev.com/5f960dfc06a7c95af69e2b09f772b2280168469b/src/wasm/wasm-objects.cc
[add] https://crrev.com/5f960dfc06a7c95af69e2b09f772b2280168469b/test/mjsunit/regress/wasm/regress-776677.js


### go...@chromium.org (2017-10-23)

This got auto approved at #18 but change landed in trunk this morning at #24. I'm planning to cut M63 Dev RC soon for release tomorrow (plan is to promote same build to Beta on Thursday). 

hablich@/awhalley@, should we take this merge in to M63 without canary coverage?

### ha...@chromium.org (2017-10-23)

No, one beta push can survive without it.

### ha...@chromium.org (2017-10-23)

It has not even rolled into chromium yet 

### gd...@chromium.org (2017-10-23)

abdulsyed@, Fix has landed on trunk, Can this be approved for the M62 respin? 

### aw...@google.com (2017-10-23)

soulchen8650@ - let's see what the panel thinks :-)

### go...@chromium.org (2017-10-23)

Adding back "Merge-Request-63" label as we're waiting on Canary coverage per https://crbug.com/chromium/776677#c27.

### ab...@chromium.org (2017-10-23)

hi gdeepti@ thanks for the fix! I'm a bit hesitant in merging to M62 until we have tested this in Canary tomorrow. This will roll-out in tonight's canary results. Can we please review it tomorrow to confirm?

Can you please comment on how safe (eg: chances of introducing new regressions) this merge is overall?

### sh...@chromium.org (2017-10-24)

Your change meets the bar and is auto-approved for M63. Please go ahead and merge the CL to branch 3239 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), gkihumba@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gd...@chromium.org (2017-10-25)

abdulsyed@, Sure, this should be out in canary now.

Regarding safety, this fix is very conservative - i.e. it changes the behavior for WebAssembly.Memory when it's used by asm.js modules, and grown, so it should be a pretty narrow subset. Also, the introduces a RangeError on Grow so I think if there are cases that are currently using - this is a better way for them to be handled.

### ab...@chromium.org (2017-10-25)

Approving merge to M62. Branch:3202

### go...@chromium.org (2017-10-25)

Please merge you change to M63 branch 3239 by 4:00 PM PT, tomorrow (Wednesday). Thank you.

### ha...@chromium.org (2017-10-25)

Merge to M62 is fine but please check the Canary data for 64.0.3249.0 before you do it. 64.0.3249.0 is the first Canary that has this fix.

### ab...@chromium.org (2017-10-25)

Chatted with ahwalley@ and cmasso@. And we agreed that let's not merge this to M62 yet.  It's important to have this bake in canary for a few days, and it just landed in Canary today. Secondly, we should have fix for Android/Desktop go out together. Right now, Android release is today (and doesn't contain fix) and desktop is tomorrow. So let's let it bake a few more days and we can consider for a future respin. 

### sh...@chromium.org (2017-10-25)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/a94ca13d44ca30c2e8c770370f89a3a7b41b782a

commit a94ca13d44ca30c2e8c770370f89a3a7b41b782a
Author: Deepti Gandluri <gdeepti@chromium.org>
Date: Wed Oct 25 21:18:17 2017

Merged: [wasm] Fix Memory.grow when shared with asm.js modules

Revision: 5f960dfc06a7c95af69e2b09f772b2280168469b

BUG=chromium:776677
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=bradnelson@chromium.org

Change-Id: I497968fef319dc12fadb311a054168da01281bb0
Reviewed-on: https://chromium-review.googlesource.com/737518
Reviewed-by: Eric Holk <eholk@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.3@{#42}
Cr-Branched-From: 094a7c93dcdcd921de3883ba4674b7e1a0feffbe-refs/heads/6.3.292@{#1}
Cr-Branched-From: 18b8fbb528a8021e04a029e06eafee50b918bce0-refs/heads/master@{#48432}
[modify] https://crrev.com/a94ca13d44ca30c2e8c770370f89a3a7b41b782a/src/asmjs/asm-js.cc
[modify] https://crrev.com/a94ca13d44ca30c2e8c770370f89a3a7b41b782a/src/objects-inl.h
[modify] https://crrev.com/a94ca13d44ca30c2e8c770370f89a3a7b41b782a/src/objects-printer.cc
[modify] https://crrev.com/a94ca13d44ca30c2e8c770370f89a3a7b41b782a/src/objects.h
[modify] https://crrev.com/a94ca13d44ca30c2e8c770370f89a3a7b41b782a/src/wasm/module-compiler.cc
[modify] https://crrev.com/a94ca13d44ca30c2e8c770370f89a3a7b41b782a/src/wasm/wasm-js.cc
[modify] https://crrev.com/a94ca13d44ca30c2e8c770370f89a3a7b41b782a/src/wasm/wasm-memory.cc
[modify] https://crrev.com/a94ca13d44ca30c2e8c770370f89a3a7b41b782a/src/wasm/wasm-objects.cc
[add] https://crrev.com/a94ca13d44ca30c2e8c770370f89a3a7b41b782a/test/mjsunit/regress/wasm/regress-776677.js


### go...@chromium.org (2017-10-26)

Per https://crbug.com/chromium/776677#c39, this is already merged to M63. So removing "Merge-Approved-63" label. Thank you.

### aw...@chromium.org (2017-10-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-10-26)

Hello soulchen8650@ The VRP panel decided to award $7,500 for this report - very many thanks!  I'm afraid they didn't see the 'je ne sais quoi' needed to award the $1337 bonus in this case :-(

### aw...@chromium.org (2017-10-26)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-10-31)

Approving merge to M62. We don't have a respin planned yet for Desktop; but since this has baked in Canary/Dev for over a week, approving this for a merge. Branch:3202

### cm...@chromium.org (2017-11-01)

We are planning a respin on Android tomorrow. please make sure to merge this into branch 3202 by 5PM today. Also, please confirm here that the fix for this issue is safe enough to be merged in 62 at this point and will not make the current issue any worse in the worst case scenario.

### bu...@chromium.org (2017-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/ffaf1ba04665da34ca4e65d86b5fb15336928db0

commit ffaf1ba04665da34ca4e65d86b5fb15336928db0
Author: Adam Klein <adamk@chromium.org>
Date: Thu Nov 02 01:07:54 2017

Merged: [wasm] Fix Memory.grow when shared with asm.js modules

Revision: 5f960dfc06a7c95af69e2b09f772b2280168469b

LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=gdeepti@chromium.org

Bug: chromium:776677
Change-Id: I2fe2892c95724f9fa43941a0120336d218dd8d71
Reviewed-on: https://chromium-review.googlesource.com/749822
Reviewed-by: Deepti Gandluri <gdeepti@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.2@{#78}
Cr-Branched-From: efa2ac4129d30c7c72e84c16af3d20b44829f990-refs/heads/6.2.414@{#1}
Cr-Branched-From: a861ebb762a60bf5cc2a274faee3620abfb06311-refs/heads/master@{#47693}
[modify] https://crrev.com/ffaf1ba04665da34ca4e65d86b5fb15336928db0/src/asmjs/asm-js.cc
[modify] https://crrev.com/ffaf1ba04665da34ca4e65d86b5fb15336928db0/src/objects-inl.h
[modify] https://crrev.com/ffaf1ba04665da34ca4e65d86b5fb15336928db0/src/objects-printer.cc
[modify] https://crrev.com/ffaf1ba04665da34ca4e65d86b5fb15336928db0/src/objects.h
[modify] https://crrev.com/ffaf1ba04665da34ca4e65d86b5fb15336928db0/src/wasm/module-compiler.cc
[modify] https://crrev.com/ffaf1ba04665da34ca4e65d86b5fb15336928db0/src/wasm/wasm-js.cc
[modify] https://crrev.com/ffaf1ba04665da34ca4e65d86b5fb15336928db0/src/wasm/wasm-module.cc
[modify] https://crrev.com/ffaf1ba04665da34ca4e65d86b5fb15336928db0/src/wasm/wasm-objects.cc
[add] https://crrev.com/ffaf1ba04665da34ca4e65d86b5fb15336928db0/test/mjsunit/regress/wasm/regress-776677.js


### ab...@chromium.org (2017-11-02)

Merged to 6.2

### bu...@chromium.org (2017-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/90b181f2b268abfc785896795e7abab1691af8f5

commit 90b181f2b268abfc785896795e7abab1691af8f5
Author: Michael Achenbach <machenbach@chromium.org>
Date: Thu Nov 02 09:14:38 2017

Revert "Merged: [wasm] Fix Memory.grow when shared with asm.js modules"

This reverts commit ffaf1ba04665da34ca4e65d86b5fb15336928db0.

Reason for revert: Failures on branch bots:
https://build.chromium.org/p/client.v8.branches/builders/V8%20Linux%20-%20stable%20branch%20-%20debug/builds/316

Original change's description:
> Merged: [wasm] Fix Memory.grow when shared with asm.js modules
> 
> Revision: 5f960dfc06a7c95af69e2b09f772b2280168469b
> 
> LOG=N
> NOTRY=true
> NOPRESUBMIT=true
> NOTREECHECKS=true
> R=​gdeepti@chromium.org
> 
> Bug: chromium:776677
> Change-Id: I2fe2892c95724f9fa43941a0120336d218dd8d71
> Reviewed-on: https://chromium-review.googlesource.com/749822
> Reviewed-by: Deepti Gandluri <gdeepti@chromium.org>
> Cr-Commit-Position: refs/branch-heads/6.2@{#78}
> Cr-Branched-From: efa2ac4129d30c7c72e84c16af3d20b44829f990-refs/heads/6.2.414@{#1}
> Cr-Branched-From: a861ebb762a60bf5cc2a274faee3620abfb06311-refs/heads/master@{#47693}

TBR=adamk@chromium.org,gdeepti@chromium.org

Change-Id: If74f21da2817125ba5a476593cfb746033de7fc6
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:776677
Reviewed-on: https://chromium-review.googlesource.com/750841
Reviewed-by: Michael Achenbach <machenbach@chromium.org>
Commit-Queue: Michael Achenbach <machenbach@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.2@{#80}
Cr-Branched-From: efa2ac4129d30c7c72e84c16af3d20b44829f990-refs/heads/6.2.414@{#1}
Cr-Branched-From: a861ebb762a60bf5cc2a274faee3620abfb06311-refs/heads/master@{#47693}
[modify] https://crrev.com/90b181f2b268abfc785896795e7abab1691af8f5/src/asmjs/asm-js.cc
[modify] https://crrev.com/90b181f2b268abfc785896795e7abab1691af8f5/src/objects-inl.h
[modify] https://crrev.com/90b181f2b268abfc785896795e7abab1691af8f5/src/objects-printer.cc
[modify] https://crrev.com/90b181f2b268abfc785896795e7abab1691af8f5/src/objects.h
[modify] https://crrev.com/90b181f2b268abfc785896795e7abab1691af8f5/src/wasm/module-compiler.cc
[modify] https://crrev.com/90b181f2b268abfc785896795e7abab1691af8f5/src/wasm/wasm-js.cc
[modify] https://crrev.com/90b181f2b268abfc785896795e7abab1691af8f5/src/wasm/wasm-module.cc
[modify] https://crrev.com/90b181f2b268abfc785896795e7abab1691af8f5/src/wasm/wasm-objects.cc
[delete] https://crrev.com/db62a2c81e0554c51069a3e92e295e0150b019ad/test/mjsunit/regress/wasm/regress-776677.js


### ma...@chromium.org (2017-11-02)

Merge led to test failures and needed to be reverted. Please merge again with a fix.

### aw...@chromium.org (2017-11-02)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-11-02)

Re #49: Does this need to be reverted on M63 branch as well? 

### ab...@chromium.org (2017-11-02)

Can you please comment on how this revert will affect today's M62 Stable candidate?

### gd...@chromium.org (2017-11-02)

There was a refactoring change post 6.2 that this fix merges on top of that causes the  the test failure. This does not need to be reverted on M63. 

As for today's M62 stable candidate, there either needs to be an additional fix with the merge, or the merge needs to be reverted from the candidate. This is not OK to use as is.


### go...@chromium.org (2017-11-02)

Thank you gdeepti@.
 Just to be clear, for M63, this doesn't need to be reverted and additional fix/merge is not needed either, correct?

### gd...@chromium.org (2017-11-02)

Govind@, nothing more is needed for M63. 

### go...@chromium.org (2017-11-02)

Thank you gdeepti@ for confirmation.

### ab...@google.com (2017-11-03)

Deepti - can you please confirm if this is properly now merged in M62 and no test failures?

### bu...@chromium.org (2017-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/32cb1bcc3251a8a8335eca114bbaee76b2d18b0d

commit 32cb1bcc3251a8a8335eca114bbaee76b2d18b0d
Author: Deepti Gandluri <gdeepti@chromium.org>
Date: Fri Nov 03 18:06:04 2017

Merged: [wasm] Fix Memory.grow when shared with asm.js modules

Revision: 5f960dfc06a7c95af69e2b09f772b2280168469b

BUG=chromium:776677
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=adamk@chromium.org, bradnelson@chromium.org

Change-Id: I6b1709a9809237219cb75bebc4d08f07c43a3b7e
Reviewed-on: https://chromium-review.googlesource.com/752195
Reviewed-by: Mircea Trofin <mtrofin@chromium.org>
Commit-Queue: Deepti Gandluri <gdeepti@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.2@{#82}
Cr-Branched-From: efa2ac4129d30c7c72e84c16af3d20b44829f990-refs/heads/6.2.414@{#1}
Cr-Branched-From: a861ebb762a60bf5cc2a274faee3620abfb06311-refs/heads/master@{#47693}
[modify] https://crrev.com/32cb1bcc3251a8a8335eca114bbaee76b2d18b0d/src/asmjs/asm-js.cc
[modify] https://crrev.com/32cb1bcc3251a8a8335eca114bbaee76b2d18b0d/src/objects-inl.h
[modify] https://crrev.com/32cb1bcc3251a8a8335eca114bbaee76b2d18b0d/src/objects-printer.cc
[modify] https://crrev.com/32cb1bcc3251a8a8335eca114bbaee76b2d18b0d/src/objects.h
[modify] https://crrev.com/32cb1bcc3251a8a8335eca114bbaee76b2d18b0d/src/wasm/module-compiler.cc
[modify] https://crrev.com/32cb1bcc3251a8a8335eca114bbaee76b2d18b0d/src/wasm/wasm-js.cc
[modify] https://crrev.com/32cb1bcc3251a8a8335eca114bbaee76b2d18b0d/src/wasm/wasm-module.cc
[modify] https://crrev.com/32cb1bcc3251a8a8335eca114bbaee76b2d18b0d/src/wasm/wasm-objects.cc
[add] https://crrev.com/32cb1bcc3251a8a8335eca114bbaee76b2d18b0d/test/mjsunit/regress/wasm/regress-776677.js


### ab...@chromium.org (2017-11-03)

https://chromium.googlesource.com/v8/v8.git/+/32cb1bcc3251a8a8335eca114bbaee76b2d18b0d
Merged - removing label. 

### gd...@chromium.org (2017-11-03)

abdulsyed@, the v8 tests for this change, and the v8-autoroll after the merge are all clean. 

### ha...@chromium.org (2017-11-17)

61 is already deprecated.

### of...@google.com (2017-11-27)

Node 8 (V8 6.1) backport: https://github.com/nodejs/node/pull/17354

### sh...@chromium.org (2018-01-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### lo...@redblink.com (2019-04-05)

always update the wasm_context when we call the |memory.grow| function. This is a more safer option.
Thanks
Security Advisor @ WPHH
https://secure.wphackedhelp.com/blog/

### is...@google.com (2019-04-05)

This issue was migrated from crbug.com/chromium/776677?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089359)*

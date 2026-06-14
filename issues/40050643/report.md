# Security: Missing HasPrototypeSlot() check in ConstructorBuiltinsbAssembler::EmitFastNewObject() results in out-of-bound read.

| Field | Value |
|-------|-------|
| **Issue ID** | [40050643](https://issues.chromium.org/issues/40050643) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pi...@arm.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2019-11-08 |
| **Bounty** | $3,000.00 |

## Description

V8 Version: 8.0.0 dev (hash 2daa1138e3f568e011fc1ee90e394dfa77fa8e4b) but we're not sure when the issue started.

We have a fast path to construct an object which reads a JSFunction's prototype_or_initial_map slot without first checking that the JSFunction indeeds has one:

```
TNode<JSObject> ConstructorBuiltinsAssembler::EmitFastNewObject(
    SloppyTNode<Context> context, SloppyTNode<JSFunction> target,
    SloppyTNode<JSReceiver> new_target, Label* call_runtime) {
  // Verify that the new target is a JSFunction.
  Label fast(this), end(this);
  GotoIf(HasInstanceType(new_target, JS_FUNCTION_TYPE), &fast);
  Goto(call_runtime);

  BIND(&fast);

  // Load the initial map and verify that it's in fact a map.
  TNode<Object> initial_map_or_proto =
      LoadObjectField(new_target, JSFunction::kPrototypeOrInitialMapOffset);
  ...
}
```

The LoadObjectField() results in an out-of-bound read as a result, since the optional slot is at the end of the object: https://cs.chromium.org/chromium/src/v8/src/objects/js-objects.h?l=1163&rcl=2daa1138e3f568e011fc1ee90e394dfa77fa8e4b

I've adapted the regression test from similar issues in the past [0][1], giving us the following reproducer:

```
(function JSCreate() {
  function f(arg) {
    const o = Reflect.construct(Object, arguments, Proxy);
    o.foo = arg;
  }
  f(0);
})();
```
[0]: https://bugs.chromium.org/p/chromium/issues/detail?id=939316
[1]: https://bugs.chromium.org/p/chromium/issues/detail?id=907714

Now in order to catch the error, we can add an assertion that ensure `new_target` has the optional slot:

```
TNode<JSObject> ConstructorBuiltinsAssembler::EmitFastNewObject(
    SloppyTNode<Context> context, SloppyTNode<JSFunction> target,
    SloppyTNode<JSReceiver> new_target, Label* call_runtime) {
  // Verify that the new target is a JSFunction.
  Label fast(this), end(this);
  GotoIf(HasInstanceType(new_target, JS_FUNCTION_TYPE), &fast);
  Goto(call_runtime);

  BIND(&fast);

  CSA_ASSERT(this, HasPrototypeSlot(CAST(new_target)));

  // Load the initial map and verify that it's in fact a map.
  TNode<Object> initial_map_or_proto =
      LoadObjectField(new_target, JSFunction::kPrototypeOrInitialMapOffset);
  ...
}
```

And with a V8 build with x64.optdebug, we can show case the problem:

```
$ /out.gn/x64.optdebug/d8 regress.js
abort: CSA_ASSERT failed: HasPrototypeSlot(CAST(new_target)) [../../src/builtins/builtins-constructor-gen.cc:189]

==== JS stack trace =========================================

    0: ExitFrame [pc: 0x7f7aabb19360]
    1: StubFrame [pc: 0x7f7aab8a1d6d]
Security context: 0x02683aa1ad59 <JSObject>#0#
    2: new Object(aka Object) [0x2683aa02199](this=0x3f96738c0591 <the_hole>,0)
    3: ConstructFrame [pc: 0x7f7aab8a1081]
    4: f [0x2221b98cb3e1] [../regress.js:3] [bytecode=0x2683aa1f039 offset=37](this=0x2221b98c15b9 <JSGlobal Object>#1#,0)
    5: JSCreate [0x2221b98cb389] [../regress.js:6] [bytecode=0x2683aa1ee89 offset=13](this=0x2221b98c15b9 <JSGlobal Object>#1#)
    6: /* anonymous */ [0x2683aa1eee9] [../regress.js:7] [bytecode=0x2683aa1edb1 offset=10](this=0x2221b98c15b9 <JSGlobal Object>#1#)
    7: InternalFrame [pc: 0x7f7aab8a83fa]
    8: EntryFrame [pc: 0x7f7aab8a81d8]

...
```

Finally, we've actually found this bug using a work-in-progress prototype implementation of a "JS Address Sanitizer" on 64-bit Arm. And running all the V8 tests with it on. It works similarly to LLVM's HWASAN: https://clang.llvm.org/docs/HardwareAssistedAddressSanitizerDesign.html . The prototype isn't ready to be published yet, but you can find more information and discussion about it on here: https://docs.google.com/document/d/1Y4x7VmkN74jEgvqv2QnMgindLEKN3fo9-qHv-YV1Fa

It's my first time submitting a potential security issue, hopefully this is enough information!

Thanks,
Pierre


## Timeline

### cl...@chromium.org (2019-11-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5649570323103744.

### me...@chromium.org (2019-11-08)

>Finally, we've actually found this bug using a work-in-progress prototype implementation of a "JS Address Sanitizer" on 64-bit Arm.

Very interesting! Thanks

### me...@chromium.org (2019-11-08)

What were the GN options you used to build d8?

### cl...@chromium.org (2019-11-08)

Testcase 5649570323103744 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5649570323103744.

### pi...@arm.com (2019-11-11)

> What were the GN options you used to build d8?

I just used the default x64.optdebug config, which gives us this:

```
is_debug = true
target_cpu = "x64"
v8_enable_backtrace = true
v8_enable_slow_dchecks = true
```

But any version with runtime assertions on should be OK.

Note that by default everything will look fine, in order to outline the problem, you need to add a CSA_ASSERT as such:

```
diff --git a/src/builtins/builtins-constructor-gen.cc b/src/builtins/builtins-constructor-gen.cc
index 38159ee3b2..c9b655a4f4 100644
--- a/src/builtins/builtins-constructor-gen.cc
+++ b/src/builtins/builtins-constructor-gen.cc
@@ -186,6 +186,8 @@ TNode<JSObject> ConstructorBuiltinsAssembler::EmitFastNewObject(
 
   BIND(&fast);
 
+  CSA_ASSERT(this, HasPrototypeSlot(CAST(new_target)));
+
   // Load the initial map and verify that it's in fact a map.
   TNode<Object> initial_map_or_proto =
       LoadObjectField(new_target, JSFunction::kPrototypeOrInitialMapOffset);
```

This shows that we are accessing the slot at `kPrototyepOrInitialMapOffset` when in that the object does not have one, and this is in fact one word past the object.

Hope this helps!

Thanks,
Pierre

### ve...@chromium.org (2019-11-11)

Thanks Pierre, your written up information is clear enough for me to know where the bug was (and where it was introduced).
When talking to ishell about this he wondered whether we couldn't get the same kind of coverage for our tests by modifying the ARM simulator to perform the same kind of bounds checks? That would have been useful to catch this bug much earlier...

### me...@chromium.org (2019-11-11)

ishell@ or verawest@ What do you think is the severity of this issue?

### cl...@chromium.org (2019-11-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5392911097004032.

### sh...@chromium.org (2019-11-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-11-11)

Testcase 5392911097004032 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5392911097004032.

### pi...@arm.com (2019-11-11)

Using the simulator to perform bounds check is interesting, maybe it would be possible to have every load and store check the map of the object, get its size and make sure the access is in bound. I *believe* that's something Jakob Kummerow said he experimented with in the past.

Alternatively, the ways to do this that I know of are either a HWASAN/memory tagging approach as I'm prototyping (I'm working on answers and investigations on all the comments on this by the way, thank you for looking at it!) or a generic address sanitizer approach.

We could implement an address sanitizer more-or-less like clang does, by adding "red zones" in between each objects, probably as filler objects so the GC can safely skip over them. And then we can record where these zones are and check if a pointer points to a red zone before derefencing. We could then do this check in the Arm simulator or in the code generator directly to cover the native case. We could also instrument C++ memory accesses on the heap, by doing a check in the various loads and stores here: https://cs.chromium.org/chromium/src/v8/src/objects/tagged-field-inl.h?q=tagged-fiel&sq=package:chromium&g=0&l=58

The main advantage of using a memory tagging approach though is that with hardware support, the memory and cpu overhead can potentially be small enough for use in the wild, as we do not need red zones anymore, although we have to align objects to 16 bytes.

### is...@chromium.org (2019-11-12)

[Empty comment from Monorail migration]

### is...@chromium.org (2019-11-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-13)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/20f6f21cae129d156329285fee3242a60ba6d567

commit 20f6f21cae129d156329285fee3242a60ba6d567
Author: Igor Sheludko <ishell@chromium.org>
Date: Thu Nov 14 15:34:41 2019

[builtins] Ensure constructor has a prototype slot

Drive-by-cleanup: simplify related helper functions in CSA.

Bug: chromium:1022855
Change-Id: Icb15e6a35275708af313ec5776e92be4b6ce2524
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1910939
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/master@{#64961}

[modify] https://crrev.com/20f6f21cae129d156329285fee3242a60ba6d567/src/builtins/builtins-constructor-gen.cc
[modify] https://crrev.com/20f6f21cae129d156329285fee3242a60ba6d567/src/builtins/cast.tq
[modify] https://crrev.com/20f6f21cae129d156329285fee3242a60ba6d567/src/codegen/code-stub-assembler.cc
[modify] https://crrev.com/20f6f21cae129d156329285fee3242a60ba6d567/src/codegen/code-stub-assembler.h
[modify] https://crrev.com/20f6f21cae129d156329285fee3242a60ba6d567/src/diagnostics/objects-debug.cc
[modify] https://crrev.com/20f6f21cae129d156329285fee3242a60ba6d567/src/objects/js-objects.tq


### is...@chromium.org (2019-11-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-15)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-18)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-18)

ishell@ re https://crbug.com/chromium/1022855#c13 can you explain why this is Security_Severity-Low? An OOB read in the renderer process would normally be Medium (per https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md). I'll change to Medium now so that it goes through all the right merge processes, but feel free to put back down to Low if there are special circumstances.

### ve...@chromium.org (2019-12-19)

Igor marked this as low based on how difficult it is to mount an attack, not because of the scope once an attack is successfully mounted. Making it medium sgtm.

### na...@google.com (2019-12-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-19)

Congrats! The Panel decided to reward $3,000 for this report!

### na...@google.com (2019-12-19)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-08)

Unfortunately since you are a contributor to V8 you are not eligible for a reward.  

### ad...@google.com (2020-01-28)

pierre.langlois@arm.com, how would you like to be credited in the release notes?

### pi...@arm.com (2020-01-29)

By name and affiliation would be good, such as "Pierre Langlois from Arm".

Thank you!
Pierre

### ad...@google.com (2020-02-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/1022855?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050643)*

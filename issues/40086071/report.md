# Security: Universal XSS by polluting private scripts with named properties

| Field | Value |
|-------|-------|
| **Issue ID** | [40086071](https://issues.chromium.org/issues/40086071) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bindings |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ha...@chromium.org |
| **Created** | 2016-11-24 |
| **Bounty** | $8,000.00 |

## Description

**VULNERABILITY DETAILS**  

When a private script method is invoked, a ScriptForbiddenScope::AllowUserAgentScript scope is set up to allow running the internal script. It is possible to exploit this scope to execute user code here:

---

## static v8::Local[v8::Value](javascript:void(0);) compileAndRunPrivateScript(ScriptState\* scriptState, String scriptClassName, const char\* source, size\_t size) { (...) v8::Local[v8::Context](javascript:void(0);) context = scriptState->context(); v8::Local[v8::Object](javascript:void(0);) global = context->Global(); v8::Local[v8::Value](javascript:void(0);) privateScriptController = global->Get(context, v8String(isolate, "privateScriptController")) .ToLocalChecked(); RELEASE\_ASSERT(privateScriptController->IsUndefined() || privateScriptController->IsObject()); if (privateScriptController->IsObject()) { v8::Local[v8::Object](javascript:void(0);) privateScriptControllerObject = privateScriptController.As[v8::Object](javascript:void(0);)(); v8::Local[v8::Value](javascript:void(0);) importFunctionValue = privateScriptControllerObject->Get(context, v8String(isolate, "import")) .ToLocalChecked(); (...) }

Even though the context belongs to a private script isolated world, |global->Get(context, v8String(isolate, "privateScriptController"))| can return a DOM node if there's one named "privateScriptController". If the node is a plugin element then |privateScriptControllerObject->Get(context, v8String(isolate, "import"))| will run an interceptor. This allows an attacker to run script in the middle of node adoption and corrupt the DOM tree.

**VERSION**  

Chrome 54.0.2840.99 (Stable)  

Chrome 55.0.2883.59 (Beta)  

Chrome 56.0.2924.3 (Dev)  

Chromium 57.0.2932.0 (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 1.6 KB)

## Timeline

### do...@chromium.org (2016-11-24)

V8 sheriffs: please triage this urgently, thanks!

[Monorail components: Blink>JavaScript]

### jo...@chromium.org (2016-11-25)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript Blink>Bindings]

### ha...@chromium.org (2016-11-25)

yukishiino: Do you have any idea on how to fix this? We somehow need to make sure that global->Get("privateScriptController") returns the PrivateScriptController object in PrivateScriptRunner.js without being hijacked by named properties of the window object...



### yu...@chromium.org (2016-11-25)

Why don't we use a v8::PrivateProperty to store the instance of PrivateScriptController?  Is there any reason that we cannot use v8::PrivateProperty?

Another option is to fix the order of named properties look-up, and to make the property unconfigurable.  The latest spec says that own properties must have priority over named properties.


### sh...@chromium.org (2016-11-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-25)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-11-25)

> Why don't we use a v8::PrivateProperty to store the instance of PrivateScriptController?  Is there any reason that we cannot use v8::PrivateProperty?

The problem is that the property is set by PrivateScriptController.js and then used by PrivateScriptController.cpp. There's no easy way to share the PrivateProperty between .js and .cpp (although it's doable by somehow passing an object between .js and .cpp).



### ma...@gmail.com (2016-11-25)

> The latest spec says that own properties must have priority over named properties.

And they do, the problem here is that there's no own property if the privateScriptController property hasn't been set yet.

Please see https://codereview.chromium.org/2529163002 for a potential fix. If the idea looks good, I'll add a test etc.

### ha...@chromium.org (2016-11-26)

LGTMed the fix, thanks!!


### yu...@chromium.org (2016-11-28)

The fix looks good.

re: #7

We knew the filepath to PrivateScriptController.js and ran it from Blink, then we can get the return value (the value evaluated at last) of PrivateScriptController.js, right?

In pseudo code, we can do the following, I thought.
    v8::Local<v8::Value> privateScriptController = compileAndRun("PrivateScriptController.js");
    V8PrivateProperty::createSymbol("Window#PrivateScriptController").set(window, privateScriptController);


### bu...@chromium.org (2016-11-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c093b7a74ddce32dd3b0e0be60f31becc6ce32f9

commit c093b7a74ddce32dd3b0e0be60f31becc6ce32f9
Author: marius.mlynski <marius.mlynski@gmail.com>
Date: Mon Nov 28 10:18:01 2016

Don't touch the prototype chain to get the private script controller.

Prior to this patch, private scripts attempted to get the
"privateScriptController" property off the global object without verifying if
the property actually exists on the global. If the property hasn't been set yet,
this operation could descend into the prototype chain and potentially return
a named property from the WindowProperties object, leading to release asserts
and general confusion.

BUG=668552

Review-Url: https://codereview.chromium.org/2529163002
Cr-Commit-Position: refs/heads/master@{#434627}

[add] https://crrev.com/c093b7a74ddce32dd3b0e0be60f31becc6ce32f9/third_party/WebKit/LayoutTests/fast/dom/marquee-named-property-crash-expected.txt
[add] https://crrev.com/c093b7a74ddce32dd3b0e0be60f31becc6ce32f9/third_party/WebKit/LayoutTests/fast/dom/marquee-named-property-crash.html
[modify] https://crrev.com/c093b7a74ddce32dd3b0e0be60f31becc6ce32f9/third_party/WebKit/Source/bindings/core/v8/PrivateScriptRunner.cpp
[modify] https://crrev.com/c093b7a74ddce32dd3b0e0be60f31becc6ce32f9/third_party/WebKit/Source/bindings/core/v8/PrivateScriptRunner.js


### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-10)

haraken: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2016-12-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-11)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-13)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-12-13)

Your change meets the bar and is auto-approved for M56 (branch: 2924)

### bu...@chromium.org (2016-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/267649a3f59fc0beec78d95dfc283cdb367da6b9

commit 267649a3f59fc0beec78d95dfc283cdb367da6b9
Author: Kentaro Hara <haraken@chromium.org>
Date: Wed Dec 14 01:44:11 2016

Don't touch the prototype chain to get the private script controller.

Prior to this patch, private scripts attempted to get the
"privateScriptController" property off the global object without verifying if
the property actually exists on the global. If the property hasn't been set yet,
this operation could descend into the prototype chain and potentially return
a named property from the WindowProperties object, leading to release asserts
and general confusion.

BUG=668552

Review-Url: https://codereview.chromium.org/2529163002
Cr-Commit-Position: refs/heads/master@{#434627}
(cherry picked from commit c093b7a74ddce32dd3b0e0be60f31becc6ce32f9)

Review-Url: https://codereview.chromium.org/2574523004 .
Cr-Commit-Position: refs/branch-heads/2924@{#485}
Cr-Branched-From: 3a87aecc31cd1ffe751dd72c04e5a96a1fc8108a-refs/heads/master@{#433059}

[add] https://crrev.com/267649a3f59fc0beec78d95dfc283cdb367da6b9/third_party/WebKit/LayoutTests/fast/dom/marquee-named-property-crash-expected.txt
[add] https://crrev.com/267649a3f59fc0beec78d95dfc283cdb367da6b9/third_party/WebKit/LayoutTests/fast/dom/marquee-named-property-crash.html
[modify] https://crrev.com/267649a3f59fc0beec78d95dfc283cdb367da6b9/third_party/WebKit/Source/bindings/core/v8/PrivateScriptRunner.cpp
[modify] https://crrev.com/267649a3f59fc0beec78d95dfc283cdb367da6b9/third_party/WebKit/Source/bindings/core/v8/PrivateScriptRunner.js


### aw...@chromium.org (2016-12-16)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-16)

Congratulations, $7,500 for this!

### aw...@google.com (2016-12-19)

[Empty comment from Monorail migration]

### mm...@chromium.org (2016-12-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-12)

+$500 for the patch - thanks!

### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/668552?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086071)*

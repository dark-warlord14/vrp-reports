# Security: `String` not isolated from global in ReadableStream.js, allowing out-of-order JavaScript execution

| Field | Value |
|-------|-------|
| **Issue ID** | [40088598](https://issues.chromium.org/issues/40088598) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P4 |
| **Component** | Blink>Network>StreamsAPI |
| **Reporter** | sk...@chromium.org |
| **Assignee** | ri...@chromium.org |
| **Created** | 2017-08-03 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS
The code in core/streams/ReadableStream.js makes copies of many global JavaScript functions it wants to use, in order to prevent them being manipulated by JavaScript running on the web-page, as this could otherwise affect its functioning. Unfortunately, the code does not make a copy of the `String` function/constructor, but does end up using it. JavaScript running in the web-page can change the global `String` to either cause an exception in the `ReadableStream` constructor, or execute arbitrary JavaScript in the middle of object construction.

The `ReadableStream` constructor is called from blink։։ReadableStreamOperations։։CreateReadableStream (https://chromium.googlesource.com/chromium/src/+/master/third_party/WebKit/Source/core/streams/ReadableStreamOperations.cpp#25). This code uses `V8ScriptRunner::CallExtraOrCrash`, which will terminate the process if the script throws an exception. By setting `String` to something that is not a function (e.g. the number 0), an exception can be triggered in this code and the renderer can be crashed.

However, I do not believe this code was designed to handle arbitrary JavaScript execution in the constructor. By setting `String` to an arbitrary function, this function can be executed during the constructor. This may be abused to trigger reentrancy or object life-time issues, by deliberately calling methods out-of-order or deleting objects. Note that I was not able to find any examples of such issues, but I did not invest a lot of time looking for them.

VERSION
Chrome Version: 60.0.3112.90 stable (This issue affects everything up to 62.0.3175.2 Canary)
Operating System: [Windows 10.0.14393 & .15063]

REPRODUCTION CASE
// Trigger arbitrary Javascript execution
String = function () { alert("Hello, world!"); };
fetch("?");

// Trigger an assertion failure using a different vector
String=0;
new Response("?");

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab (this crashes the renderer process)
Crash State: See attached BugId report
Client ID (if relevant): n/a


## Attachments

- [repro.html](attachments/repro.html) (text/plain, 233 B)
- [Assert f35.6a4 @ chrome.exe!chrome_child.dll!blink։։ReadableStreamOperations։։CreateReadableStream.html](attachments/Assert f35.6a4 @ chrome.exe!chrome_child.dll!blink։։ReadableStreamOperations։։CreateReadableStream.html) (text/plain, 1.1 MB)

## Timeline

### cl...@chromium.org (2017-08-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5018863459893248.

### el...@chromium.org (2017-08-03)

ricea@, can you PTAL?

[Monorail components: Blink>Network>StreamsAPI]

### cl...@chromium.org (2017-08-03)

Detailed report: https://clusterfuzz.com/testcase?key=5018863459893248

Job Type: linux_asan_chrome_mp
Crash Type: Abrt
Crash Address: 0x03e900000001
Crash State:
  blink::ReportFatalErrorInMainThread
  v8::V8::ToLocalEmpty
  blink::ReadableStreamOperations::CreateReadableStream
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=476918:476983

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5018863459893248


See https://github.com/google/clusterfuzz-tools for more information.

### ri...@chromium.org (2017-08-04)

Good find. I have a fix under review at https://chromium-review.googlesource.com/c/601668.

I have been trying to think of a comprehensive way to find these issues but I haven't come up with anything yet.

### ri...@chromium.org (2017-08-04)

I worked out how to undefine everything on the global object. In the process I discovered that we were also failing to use a copy of Boolean: https://chromium-review.googlesource.com/c/601610.

### ri...@chromium.org (2017-08-04)

+tyoshino who is reviewing my CLs.

### bu...@chromium.org (2017-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/be5214ee56f8f91275210e297b961a5b836d94a3

commit be5214ee56f8f91275210e297b961a5b836d94a3
Author: Adam Rice <ricea@chromium.org>
Date: Fri Aug 04 09:21:08 2017

Make a copy of String function in ReadableStream

The ReadableStream constructor uses the String function. However, the
implementation was failing to take a copy of the function. This meant
that the version from the Javascript environment was used. If it had
been modified then it could result in incorrect behaviour.

Use a copy of the original value of the String function in
ReadableStream.

This change also includes a regression test.

BUG=752177

Change-Id: I52f36244a9d87131219958837e3cee00a8fc5fb4
Reviewed-on: https://chromium-review.googlesource.com/601668
Reviewed-by: Takeshi Yoshino <tyoshino@chromium.org>
Commit-Queue: Adam Rice <ricea@chromium.org>
Cr-Commit-Position: refs/heads/master@{#491973}
[add] https://crrev.com/be5214ee56f8f91275210e297b961a5b836d94a3/third_party/WebKit/LayoutTests/http/tests/streams/chromium/bad-string-constructor.html
[modify] https://crrev.com/be5214ee56f8f91275210e297b961a5b836d94a3/third_party/WebKit/Source/core/streams/ReadableStream.js


### bu...@chromium.org (2017-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/35b930495b526df8a7e04eefef76de0ff36497c4

commit 35b930495b526df8a7e04eefef76de0ff36497c4
Author: Adam Rice <ricea@chromium.org>
Date: Fri Aug 04 10:19:05 2017

Use a copy of Boolean in ReadableStream

ReadableStream.prototype.pipeTo was using the global Boolean
function. Use a copy of the original value instead to avoid problems
when it is overwritten.

This change also adds a test that ReadableStream and WritableStream
still work when all global objects have been set to undefined.

Bug: 752177
Change-Id: I09c7fb139610c2c9c3bc8780c59615361d8beb55
Reviewed-on: https://chromium-review.googlesource.com/601610
Reviewed-by: Takeshi Yoshino <tyoshino@chromium.org>
Commit-Queue: Adam Rice <ricea@chromium.org>
Cr-Commit-Position: refs/heads/master@{#491985}
[add] https://crrev.com/35b930495b526df8a7e04eefef76de0ff36497c4/third_party/WebKit/LayoutTests/http/tests/streams/chromium/touching-global-object-expected.txt
[add] https://crrev.com/35b930495b526df8a7e04eefef76de0ff36497c4/third_party/WebKit/LayoutTests/http/tests/streams/chromium/touching-global-object.html
[modify] https://crrev.com/35b930495b526df8a7e04eefef76de0ff36497c4/third_party/WebKit/Source/core/streams/ReadableStream.js


### cl...@chromium.org (2017-08-05)

ClusterFuzz has detected this issue as fixed in range 491739:492052.

Detailed report: https://clusterfuzz.com/testcase?key=5018863459893248

Job Type: linux_asan_chrome_mp
Crash Type: Abrt
Crash Address: 0x03e900000001
Crash State:
  blink::ReportFatalErrorInMainThread
  v8::V8::ToLocalEmpty
  blink::ReadableStreamOperations::CreateReadableStream
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=476918:476983
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=491739:492052

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5018863459893248


See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-08-05)

ClusterFuzz testcase 5018863459893248 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-08-05)

[Empty comment from Monorail migration]

### sk...@chromium.org (2017-08-11)

[Comment Deleted]

### sk...@chromium.org (2017-08-11)

I was wondering if this bug was going to get `reward-topanel` and `Security_Severity-XXX` labels.

### mb...@chromium.org (2017-08-11)

Adding reward-topanel now so we don't miss it. I'm not immediately sure of the severity, so hopefully someone else can chime in on that, but worst case the reward panel can figure it out.

### ri...@chromium.org (2017-08-13)

As far as I know, there are currently three paths to get to the buggy code:

1. new ReadableStream()
2. new Response()
3. fetch()

I am 99.9% sure the first one is not exploitable, because the attacker cannot get a reference to the ReadableStream object until the constructor has completed, at which point it is too late to exploit re-entrancy.

new Response() is probably also not exploitable for the same reason, although in this case you can cause a renderer crash as seen above.

fetch() is the most risky one, although there is no known exploit apart from the obvious renderer crash.

I have added yhirano@ who is more familiar with the implementation and so better able to assess risk.

Even if it wasn't exploitable now, it might have become exploitable as more users of ReadableStream were added, so it was definitely a valuable find.

### sk...@chromium.org (2017-08-15)

I come up with a relatively naive way of detecting this type of bug using regular expressions:
1) Enumerate all global properties in Chrome using `Object.getOwnPropertyNames(window);`, then for each such global name `<global-name>`:.
2) Scan all `.js` files for `/function\s*\(global\s*,\s*binding\s*,\s*v8\)\s*\{/` and filter out files that do not match to get a list of files that could contain this issue.
3) scan all remaining files for `/\b<global-name>\(/` and filter out those that do not match to get a list of files that use this global as a function.
4) scan all remaining files for `/\bconst\s+<global-name>\s*=\s*global\.<global-name>\s*;/` and filter out those that DO match to get a list of files that do not make a copy of the global function.

I ran the above recursively in `\third_party\WebKit\Source` and it found the `String` issue I reported and the `Boolean` issue reported in https://crbug.com/chromium/752177#c5. It found a few other things that were false positives.

There are a number of reasons why a bug might slip through this test; such as the code using different argument variable names (which would incorrectly filter it out in step 2). Also, this does not detect reading/writing global properties, or accessing members of global objects.

Ideally, one would write/reuse a JavaScript parser to indisputably detect where globals are used in the code: there should not be any, as all `globals` should be copied into variables from the `global` argument.


### sk...@chromium.org (2017-08-15)

FYI: I play around with the regular expression for step 3 to try to detect reading from/writing to a global variable, but found no additional bugs. I was using `/(\b<global-name>\s*\(|\b<global-name>\s*[\+\-\%\*\&\|\!\<\>\=]|[\+\-\%\*\&\|\!\<\>\=]\s*<global-name>\b|\b<global-name>\.)/`; it results in many false positives for `Object`.


I also looked for code accessing members of global objects: such a bug would follow this pattern:

  const SomeGlobal = global.SomeGlobal;
  ...
  if (SomeGlobal.property1) ...
  ...or...
  SomeGlobal.property2 = Value;
  ...or...
  SomeGlobal.method(...);

I used the regular expression `/\bconst\s+(\w+)\s*=\s*global(\.\w+)+\s*;[\s\S]*\b\1\.\w+/` but did not find anything useful.

There's another potential risk with automatic type conversion: `.toString ` and `.valueOf` may get called in such cases. It could potentially be possible for an attacker to overwrite these methods and execute code when the conversion happens.

### ri...@chromium.org (2017-08-15)

#17 Interesting. So accidentally using the == operator could be a security problem.

### sk...@chromium.org (2017-08-16)

Simply reading a global is enough:

// malicious webpage:
  Object.defineProperty(window, "SomeGlobal", {get: function() { alert(1); }});

// vulnerable chrome script:
  var a = SomeGlobal; // an alert will be shown

(You can copy+paste the above into an inspector to test this.)

### bu...@chromium.org (2017-08-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4623f9599a0aa9a97d1ffe6fc6c0667af98fafff

commit 4623f9599a0aa9a97d1ffe6fc6c0667af98fafff
Author: Adam Rice <ricea@chromium.org>
Date: Thu Aug 17 11:03:23 2017

Streams global tests: poison implicit conversions

Add implementations of toString and valueOf to the String and Array
prototypes that throw exceptions. This should cause code that contains
implicit conversions to fail.

This change did not find any bugs in the current implementation.

BUG=752177

Change-Id: If38a9bb83aeb42ab55e801d3e3dee48e9e352aca
Reviewed-on: https://chromium-review.googlesource.com/615855
Reviewed-by: Takeshi Yoshino <tyoshino@chromium.org>
Commit-Queue: Adam Rice <ricea@chromium.org>
Cr-Commit-Position: refs/heads/master@{#495134}
[modify] https://crrev.com/4623f9599a0aa9a97d1ffe6fc6c0667af98fafff/third_party/WebKit/LayoutTests/http/tests/streams/chromium/touching-global-object.html


### aw...@chromium.org (2017-08-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-08-28)

Nice one! The VRP Panel decided to award $1,000 for this bug.

### sk...@chromium.org (2017-08-28)

I'm sorry to hear that. I was under the impression that a potentially exploitable security issue in the release build with a proper write-up would be rewarded higher.

I was hoping to contribute directly to Chrome more but the rewards I have been getting suggest that this is not economically viable. I will have to go back to fuzzing release builds only and reporting what I find through ZDI/iDefense.


### aw...@chromium.org (2017-08-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-11-11)

This issue was migrated from crbug.com/chromium/752177?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088598)*

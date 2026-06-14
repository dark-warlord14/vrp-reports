# Security: type confusion trigger DCHECK fail in ReadableStreamBytesConsumer::OnFulfilled::Call

| Field | Value |
|-------|-------|
| **Issue ID** | [40091312](https://issues.chromium.org/issues/40091312) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Network>FetchAPI, Blink>Network>StreamsAPI |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | yh...@chromium.org |
| **Created** | 2018-05-07 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

the argument v passed to the Function ReadableStreamBytesConsumer::OnFulfilled::Call May be not a js object.  

ScriptValue Call(ScriptValue v) override {  

bool done;  

v8::Local[v8::Value](javascript:void(0);) item = v.V8Value();  

DCHECK(item->IsObject()); ------>this check will be fail under certain circumstances  

v8::Local[v8::Value](javascript:void(0);) value =  

V8UnpackIteratorResult(v.GetScriptState(), item.As[v8::Object](javascript:void(0);)(), &done)------------> this line will cause type confusion when convert item to an object.  

.ToLocalChecked();  

if (done) {  

consumer\_->OnReadDone();  

return v;  

}  

if (!value->IsUint8Array()) {  

consumer\_->OnRejected();  

return ScriptValue();  

}  

consumer\_->OnRead(V8Uint8Array::ToImpl(value.As[v8::Object](javascript:void(0);)()));  

return v;  

}

**VERSION**  

Chrome Version: [66.0.3359.139]  

Operating System: [All]

**REPRODUCTION CASE**  

load the attached poc.html in a debugger version chrome and you'll see the crash as follows.

[32192:32225:0507/182630.740682:FATAL:readable\_stream\_bytes\_consumer.cc(36)] Check failed: item->IsObject().

Program received signal SIGTRAP, Trace/breakpoint trap.  

[Switching to Thread 0x7fffb91cd700 (LWP 32225)]  

base::debug::(anonymous namespace)::DebugBreak () at ../../base/debug/debugger\_posix.cc:239  

239 }  

(gdb) bt  

#0 base::debug::(anonymous namespace)::DebugBreak () at ../../base/debug/debugger\_posix.cc:239  

#1 0x00007ffff7ad7a88 in base::debug::BreakDebugger () at ../../base/debug/debugger\_posix.cc:258  

#2 0x00007ffff7875d34 in logging::LogMessage::~LogMessage (this=0x7fffb91c96a0) at ../../base/logging.cc:855  

#3 0x00007fffe7fac6a6 in blink::ReadableStreamBytesConsumer::OnFulfilled::Call (this=0x19fd50194140, v=...)  

at ../../third\_party/blink/renderer/core/fetch/readable\_stream\_bytes\_consumer.cc:36  

#4 0x00007fffe75d2e54 in blink::ScriptFunction::CallCallback (args=...) at ../../third\_party/blink/renderer/bindings/core/v8/script\_function.cc:32  

#5 0x00007fffea009953 in v8::internal::FunctionCallbackArguments::Call (this=<optimized out>, handler=<optimized out>) at ../../v8/src/api-arguments-inl.h:94  

#6 0x00007fffea007c4e in v8::internal::(anonymous namespace)::HandleApiCallHelper<false> (isolate=<optimized out>, function=..., new\_target=..., fun\_data=..., receiver=..., args=...)  

at ../../v8/src/builtins/builtins-api.cc:108  

#7 0x00007fffea005f39 in v8::internal::Builtin\_Impl\_HandleApiCall (args=..., isolate=<optimized out>) at ../../v8/src/builtins/builtins-api.cc:138  

#8 0x00007fffea00597d in v8::internal::Builtin\_HandleApiCall (args\_length=<optimized out>, args\_object=<optimized out>, isolate=<optimized out>)  

at ../../v8/src/builtins/builtins-api.cc:126  

#9 0x000022e397d10f19 in ?? ()  

#10 0x000022e397d10e81 in ?? ()  

#11 0x00007fffb91c9e10 in ?? ()  

#12 0x0000000000000006 in ?? ()  

#13 0x00007fffb91c9e80 in ?? ()  

#14 0x00007fffeaadf12b in v8\_Default\_embedded\_blob\_ () from /home/ggong/ssd1/chromium/src/out/Debug/./libv8.so  

#15 0x0000136c3ce826c1 in ?? ()  

#16 0x000028e057edd909 in ?? ()  

#17 0x0000000600000000 in ?? ()  

#18 0x0000136c3ce827d1 in ?? ()  

#19 0x0000000100000000 in ?? ()  

#20 0x00000dc66d807491 in ?? ()  

#21 0x00000dc66d81a941 in ?? ()  

#22 0x00000dc66d81a479 in ?? ()  

#23 0x0000000000000016 in ?? ()  

#24 0x00007fffb91c9ed8 in ?? ()  

#25 0x00007fffeaa563f0 in v8\_Default\_embedded\_blob\_ () from /home/ggong/ssd1/chromium/src/out/Debug/./libv8.so  

#26 0x00000dc66d81ad99 in ?? ()  

#27 0x00007ffff7b9cb38 in base::trace\_event::TraceLog::GetInstance()::instance () from /home/ggong/ssd1/chromium/src/out/Debug/./libbase.so  

#28 0x0000000000000002 in ?? ()  

#29 0x00000dc66d81a941 in ?? ()  

#30 0x00000dc66d81a479 in ?? ()  

#31 0x0000000000000000 in ?? ()

the patch is simple, attached as patch.diff

diff --git a/third\_party/blink/renderer/core/fetch/readable\_stream\_bytes\_consumer.cc b/third\_party/blink/renderer/core/fetch/readable\_stream\_bytes\_consumer.cc  

index abf67b3..ec7eaec 100644  

--- a/third\_party/blink/renderer/core/fetch/readable\_stream\_bytes\_consumer.cc  

+++ b/third\_party/blink/renderer/core/fetch/readable\_stream\_bytes\_consumer.cc  

@@ -33,7 +33,10 @@ class ReadableStreamBytesConsumer::OnFulfilled final : public ScriptFunction {  

ScriptValue Call(ScriptValue v) override {  

bool done;  

v8::Local[v8::Value](javascript:void(0);) item = v.V8Value();

- DCHECK(item->IsObject());

- if (!item->IsObject()) {
- ```
   consumer_->OnRejected();  
  
  ```
- ```
   return ScriptValue();  
  
  ```
- }  
  
  v8::Local[v8::Value](javascript:void(0);) value =  
  
  V8UnpackIteratorResult(v.GetScriptState(), item.As[v8::Object](javascript:void(0);)(), &done)  
  
  .ToLocalChecked();

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 954 B)
- [patch.diff](attachments/patch.diff) (application/octet-stream, 828 B)

## Timeline

### cl...@chromium.org (2018-05-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6488298034561024.

### ts...@chromium.org (2018-05-07)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript Blink>Network>FetchAPI]

### ts...@chromium.org (2018-05-07)

Assigning per OWNERs file.

### ts...@chromium.org (2018-05-07)

[Empty comment from Monorail migration]

### yh...@chromium.org (2018-05-08)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript Blink>Network>StreamsAPI]

### yh...@chromium.org (2018-05-08)

[Empty comment from Monorail migration]

### yh...@chromium.org (2018-05-08)

[Empty comment from Monorail migration]

### yh...@chromium.org (2018-05-08)

[Comment Deleted]

### yh...@chromium.org (2018-05-08)

wpt-style poc:

promise_test(async () => {
  const hello = new TextEncoder('utf-8').encode('hello');
  const bye = new TextEncoder('utf-8').encode('bye');
  const rs = new ReadableStream({
    start(controller) {
      controller.enqueue(hello);
      controller.close();
    }
  });
  const resp = new Response(rs);
  Object.prototype.then = (f1, f2) => {
    delete Object.prototype.then;
    f1({done: false, value: bye});
  };
  const text = await resp.text();
  assert_equals(text, 'hello');
}, '...');


### ri...@chromium.org (2018-05-08)

Unfortunately, our ReadableStream implementation is behaving according to the standard. CreateIterResultObject() in the ECMAScript standard explicitly creates an object using Object.prototype: https://tc39.github.io/ecma262/#sec-createiterresultobject

I'd like to change this, because I think it breaks the guarantee that the internals of pipeTo() are invisible to Javascript. I will file an issue against the Streams Standard once we have resolved this issue.

This means the DCHECK() is wrong: there's no guarantee that we get an object here.

I am going to check the Fetch Standard to see whether our behaviour is standard there.

### ri...@chromium.org (2018-05-08)

The Fetch Standard is fine (our behaviour is wrong). The relevant step is:

> * When read is fulfilled with a value that matches with neither of the above patterns, reject promise with a TypeError.

### yh...@chromium.org (2018-05-08)

Ok, then I will fix that in core/fetch. Thanks!

### yh...@chromium.org (2018-05-08)

tsepez@, is this really Security_Severity-High? Do we need to merge the fix to stable?

### bu...@chromium.org (2018-05-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7712d138374a92c4d2f3b05cdc86d1a7a523702b

commit 7712d138374a92c4d2f3b05cdc86d1a7a523702b
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Tue May 08 10:55:08 2018

ReadableStreamBytesConsumer should check read results

ReadableStreamBytesConsumer expected that the results from
ReadableStreamReaderDefaultRead should be Promise<Object> because that
is provided from ReadableStream provided by blink, but it's possible to
inject arbitrary values with the promise assimilation.

This CL adds additional checks for such injection.

Bug: 840320
Change-Id: I7b3c6a8bfcf563dd860b133ff0295dd7a5d5fea5
Reviewed-on: https://chromium-review.googlesource.com/1049413
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Adam Rice <ricea@chromium.org>
Cr-Commit-Position: refs/heads/master@{#556751}
[add] https://crrev.com/7712d138374a92c4d2f3b05cdc86d1a7a523702b/third_party/WebKit/LayoutTests/external/wpt/fetch/api/response/response-stream-with-broken-then.any.js
[modify] https://crrev.com/7712d138374a92c4d2f3b05cdc86d1a7a523702b/third_party/blink/renderer/core/fetch/readable_stream_bytes_consumer.cc


### yh...@chromium.org (2018-05-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-14)

[Empty comment from Monorail migration]

### aw...@google.com (2018-05-14)

[Empty comment from Monorail migration]

### yh...@chromium.org (2018-05-16)

+tsepez@ for #13

### aw...@google.com (2018-05-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-16)

This bug requires manual review: We are only 12 days from stable.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-05-16)

+awhalley@ for M67 merge review (CL listed at #14 landed in trunk on May 8th)

### aw...@google.com (2018-05-17)

govind@ - good for 67

### go...@chromium.org (2018-05-17)

Approving merge to M67 branch 3396 based on https://crbug.com/chromium/840320#c22. Pls merge ASAP. Thank you.

### bu...@chromium.org (2018-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e20fa6ea657a39d9697c167c3b4c6809b5dbc2e3

commit e20fa6ea657a39d9697c167c3b4c6809b5dbc2e3
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Thu May 17 04:08:39 2018

ReadableStreamBytesConsumer should check read results

ReadableStreamBytesConsumer expected that the results from
ReadableStreamReaderDefaultRead should be Promise<Object> because that
is provided from ReadableStream provided by blink, but it's possible to
inject arbitrary values with the promise assimilation.

This CL adds additional checks for such injection.

TBR=yhirano@chromium.org

(cherry picked from commit 7712d138374a92c4d2f3b05cdc86d1a7a523702b)

Bug: 840320
Change-Id: I7b3c6a8bfcf563dd860b133ff0295dd7a5d5fea5
Reviewed-on: https://chromium-review.googlesource.com/1049413
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Adam Rice <ricea@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#556751}
Reviewed-on: https://chromium-review.googlesource.com/1062992
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/branch-heads/3396@{#620}
Cr-Branched-From: 9ef2aa869bc7bc0c089e255d698cca6e47d6b038-refs/heads/master@{#550428}
[add] https://crrev.com/e20fa6ea657a39d9697c167c3b4c6809b5dbc2e3/third_party/WebKit/LayoutTests/external/wpt/fetch/api/response/response-stream-with-broken-then.any.js
[modify] https://crrev.com/e20fa6ea657a39d9697c167c3b4c6809b5dbc2e3/third_party/blink/renderer/core/fetch/readable_stream_bytes_consumer.cc


### aw...@chromium.org (2018-05-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-05-21)

Thanks higongguang@ - the VRP panel decided to award $5,000 for this report :-)

### aw...@chromium.org (2018-05-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### ri...@chromium.org (2018-05-30)

Can you let me know when this becomes public? I want to address the issue in the streams standard.

### aw...@google.com (2018-05-30)

Hi ricea@ - since it's fixed in 67 which went stable yesterday we could open it up early, as getting it looked at in the standard would be great. We can open it up next week once 67 has gone to 100% and folk have had a chance to upgrade.

### ri...@chromium.org (2018-06-13)

[Empty comment from Monorail migration]

### ri...@chromium.org (2018-06-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/840320?no_tracker_redirect=1

[Multiple monorail components: Blink>Network>FetchAPI, Blink>Network>StreamsAPI]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091312)*

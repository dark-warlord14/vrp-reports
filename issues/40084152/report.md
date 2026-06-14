# Security: Universal XSS using iterables

| Field | Value |
|-------|-------|
| **Issue ID** | [40084152](https://issues.chromium.org/issues/40084152) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bindings |
| **Reporter** | ma...@gmail.com |
| **Assignee** | jl...@opera.com |
| **Created** | 2016-04-22 |
| **Bounty** | $7,500.00 |

## Description

## **VULNERABILITY DETAILS** From /third\_party/WebKit/Source/bindings/core/v8/Iterable.h:

```
void forEachForBinding(...)  
{  
    (...)  
    v8::Local<v8::Object> creationContext(scriptState->context()->Global());  
    v8::Local<v8::Function> v8Callback(callback.v8Value().As<v8::Function>());  
    v8::Local<v8::Value> v8ThisArg(thisArg.v8Value());  
    v8::Local<v8::Value> args[3];  

    args[2] = thisValue.v8Value();  

    while (true) {  
        KeyType key;  
        ValueType value;  

        if (!source->next(scriptState, key, value, exceptionState))  
            return;  
        (...)  
        args[0] = toV8(value, creationContext, isolate);  
        args[1] = toV8(key, creationContext, isolate);  
        (...)  
        v8::Local<v8::Value> result;  
        if (!V8ScriptRunner::callFunction(v8Callback, scriptState->getExecutionContext(), v8ThisArg, 3, args, isolate).ToLocal(&result)) {  
            exceptionState.rethrowV8Exception(tryCatch.Exception());  
            return;  
        }  
    }  
}  

```

---

This code doesn't consider that the callback can change the security characteristics of the object used as a creation context. This may lead to cross-origin object leaks.

**VERSION**  

Chrome 50.0.2661.87 (Stable)  

Chrome 51.0.2704.22 (Beta)  

Chrome 51.0.2704.19 (Dev)  

Chromium 52.0.2716.0 (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 1.1 KB)

## Timeline

### va...@chromium.org (2016-04-22)

[Empty comment from Monorail migration]

[Monorail components: Blink>Bindings]

### va...@chromium.org (2016-04-22)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-04-22)

dcheng@ -- could you please take a look and assign it to the appropriate owner? Thanks!

### dc...@chromium.org (2016-04-22)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-04-22)

[Empty comment from Monorail migration]

### jl...@opera.com (2016-04-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-04-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0cd7a9f853e3cb7c035b4ab9e07a503552267f9d

commit 0cd7a9f853e3cb7c035b4ab9e07a503552267f9d
Author: jl <jl@opera.com>
Date: Tue Apr 26 15:22:47 2016

Use correct creation context during Iterable.forEach iteration

Use |thisValue| instead of |scriptState->context()->Global()|, since this
is simpler and since Global() actually returns a WindowProxy object that
may change and become incorrect to use as creation context depending on
what the callback function does.

BUG=605910

Review URL: https://codereview.chromium.org/1918763002

Cr-Commit-Position: refs/heads/master@{#389785}

[add] https://crrev.com/0cd7a9f853e3cb7c035b4ab9e07a503552267f9d/third_party/WebKit/LayoutTests/fast/css/fontfaceset-cross-frame.html
[modify] https://crrev.com/0cd7a9f853e3cb7c035b4ab9e07a503552267f9d/third_party/WebKit/Source/bindings/core/v8/Iterable.h


### jl...@opera.com (2016-04-27)

This fix ought to be merged to stabilization branches, I assume? It's quite trivial and should be safe to merge.

Note that I'm quite unfamiliar with the proper way of handling such issues, so all advise and/or help is very appreciated.

### yu...@chromium.org (2016-04-27)

We've confirmed that the fix works fine on ToT.
Requesting merge to M50 and M51.

### ti...@google.com (2016-04-27)

[Automated comment] Request affecting a post-stable build (M50), manual review required.

### ti...@google.com (2016-04-27)

Your change meets the bar and is auto-approved for M51 (branch: 2704)

### ti...@google.com (2016-04-27)

Your change meets the bar and is auto-approved for M51 (branch: 2704)

### cl...@chromium.org (2016-04-27)

[Empty comment from Monorail migration]

### yu...@chromium.org (2016-04-28)

jl@, you can now merge the CL to M51.
The branch number is 2704.  Please use the drover to merge the CL.
http://dev.chromium.org/developers/how-tos/drover

Let us know if you have any trouble.

FYI just in case:
http://dev.chromium.org/developers/the-zen-of-merge-requests


### bu...@chromium.org (2016-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4fdeff55d9188e4490e71305f38ee0e62d0b50c6

commit 4fdeff55d9188e4490e71305f38ee0e62d0b50c6
Author: Jens Widell <jl@opera.com>
Date: Thu Apr 28 06:12:40 2016

Use correct creation context during Iterable.forEach iteration

Use |thisValue| instead of |scriptState->context()->Global()|, since this
is simpler and since Global() actually returns a WindowProxy object that
may change and become incorrect to use as creation context depending on
what the callback function does.

BUG=605910

Review URL: https://codereview.chromium.org/1918763002

Cr-Commit-Position: refs/heads/master@{#389785}
(cherry picked from commit 0cd7a9f853e3cb7c035b4ab9e07a503552267f9d)

Review URL: https://codereview.chromium.org/1927063002 .

Cr-Commit-Position: refs/branch-heads/2704@{#283}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[add] https://crrev.com/4fdeff55d9188e4490e71305f38ee0e62d0b50c6/third_party/WebKit/LayoutTests/fast/css/fontfaceset-cross-frame.html
[modify] https://crrev.com/4fdeff55d9188e4490e71305f38ee0e62d0b50c6/third_party/WebKit/Source/bindings/core/v8/Iterable.h


### go...@chromium.org (2016-05-06)

Approving merge to M50 branch 2661, based on https://crbug.com/chromium/605910#c9 and also it is in Beta already. Please merge asap (latest before 1:00 PM PST Monday), so we can take it for next week Stable refresh release. Thank you.

### bu...@chromium.org (2016-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cfb182b8d5cdc104ba1e9c09125c918b00e850bb

commit cfb182b8d5cdc104ba1e9c09125c918b00e850bb
Author: Jens Widell <jl@opera.com>
Date: Mon May 09 06:47:57 2016

Use correct creation context during Iterable.forEach iteration

Use |thisValue| instead of |scriptState->context()->Global()|, since this
is simpler and since Global() actually returns a WindowProxy object that
may change and become incorrect to use as creation context depending on
what the callback function does.

BUG=605910

Review URL: https://codereview.chromium.org/1918763002

Cr-Commit-Position: refs/heads/master@{#389785}
(cherry picked from commit 0cd7a9f853e3cb7c035b4ab9e07a503552267f9d)

Review URL: https://codereview.chromium.org/1960013002 .

Cr-Commit-Position: refs/branch-heads/2661@{#671}
Cr-Branched-From: ef6f6ae5e4c96622286b563658d5cd62a6cf1197-refs/heads/master@{#378081}

[add] https://crrev.com/cfb182b8d5cdc104ba1e9c09125c918b00e850bb/third_party/WebKit/LayoutTests/fast/css/fontfaceset-cross-frame.html
[modify] https://crrev.com/cfb182b8d5cdc104ba1e9c09125c918b00e850bb/third_party/WebKit/Source/bindings/core/v8/Iterable.h


### ti...@google.com (2016-05-09)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-05-09)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-05-10)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-12)

...and another $7,500 for this report. Thanks again for a great report and POC.

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/605910?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084152)*

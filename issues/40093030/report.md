# Security: Type confusion in blink::GetTypeExtension

| Field | Value |
|-------|-------|
| **Issue ID** | [40093030](https://issues.chromium.org/issues/40093030) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | pe...@chromium.org |
| **Created** | 2018-11-11 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

<https://cs.chromium.org/chromium/src/third_party/blink/renderer/core/dom/document.cc?rcl=c1582e69def506093836a7cc6ba1e9c77c3b7a69&l=951>  

AtomicString GetTypeExtension(Document\* document,  

const StringOrDictionary& string\_or\_options,  

ExceptionState& exception\_state) {  

if (string\_or\_options.IsNull())  

return AtomicString();

if (string\_or\_options.IsString()) {  

UseCounter::Count(document,  

WebFeature::kDocumentCreateElement2ndArgStringHandling);  

return AtomicString(string\_or\_options.GetAsString());  

}

if (string\_or\_options.IsDictionary()) {  

Dictionary dict = string\_or\_options.GetAsDictionary();  

v8::Local[v8::Value](javascript:void(0);) value;  

if (dict.HasProperty("is", exception\_state) && dict.Get("is", value)) {  

return ToCoreAtomicString(v8::Local[v8::String](javascript:void(0);)::Cast(value));  

}  

}

return AtomicString();  

}

GetTypeExtension() casts the "is" field of the dictionary to |v8::String| without a prior type check.

**VERSION**  

Google Chrome 72.0.3607.0 (Official Build) canary (32-bit) (cohort: Clang-32)  

Google Chrome 72.0.3602.2 (Official Build) dev (64-bit) (cohort: Dev)  

The bug has been introduced by commit c89bf1db1e841d6bc9fbf34eb005747d153c1b26.

**REPRODUCTION CASE**

<script>
document.createElement("a", {is: 0x41414141});
</script>

This repro case shows leaked heap content:

<script>
alert(document.createElement("a",{is: []}).outerHTML);
</script>

Externalize() gets called on the fake string object, so it should be possible to turn the bug into memory corruption.

## Attachments

- [crash.log](attachments/crash.log) (text/plain, 2.1 KB)

## Timeline

### ke...@chromium.org (2018-11-12)

Thanks for the report!

peria@: Can you please look at this security regression? It looks like a straightforward fix.

[Monorail components: Blink>DOM]

### pe...@chromium.org (2018-11-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6a1db25d6a3e63d19d3591af858f6389fe23b7ee

commit 6a1db25d6a3e63d19d3591af858f6389fe23b7ee
Author: Hitoshi Yoshida <peria@chromium.org>
Date: Fri Nov 16 04:59:24 2018

document: Use ElementCreationOptions in Document.createElement()

We used (DOMString or Dictionary) type for |option| parameter,
but this CL replaces it with (DOMString or ElementCreationOpitons)
as the spec defined.


Bug: 904241
Change-Id: I9416af83168e7c1f7456ffdbd3141fa97b510706
Reviewed-on: https://chromium-review.googlesource.com/c/1333094
Commit-Queue: Hitoshi Yoshida <peria@chromium.org>
Reviewed-by: Yuki Shiino <yukishiino@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#608668}
[modify] https://crrev.com/6a1db25d6a3e63d19d3591af858f6389fe23b7ee/third_party/blink/renderer/bindings/core/v8/BUILD.gn
[modify] https://crrev.com/6a1db25d6a3e63d19d3591af858f6389fe23b7ee/third_party/blink/renderer/bindings/core/v8/v0_custom_element_constructor_builder.cc
[modify] https://crrev.com/6a1db25d6a3e63d19d3591af858f6389fe23b7ee/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/6a1db25d6a3e63d19d3591af858f6389fe23b7ee/third_party/blink/renderer/core/dom/document.h
[modify] https://crrev.com/6a1db25d6a3e63d19d3591af858f6389fe23b7ee/third_party/blink/renderer/core/dom/document.idl
[modify] https://crrev.com/6a1db25d6a3e63d19d3591af858f6389fe23b7ee/third_party/blink/renderer/core/html/custom/custom_element_upgrade_sorter_test.cc


### bu...@chromium.org (2018-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/97597a979e142cfe6f85e924ab6934afd1e39577

commit 97597a979e142cfe6f85e924ab6934afd1e39577
Author: Findit <findit-for-me@appspot.gserviceaccount.com>
Date: Fri Nov 16 05:33:26 2018

Revert "document: Use ElementCreationOptions in Document.createElement()"

This reverts commit 6a1db25d6a3e63d19d3591af858f6389fe23b7ee.

Reason for revert:

Findit (https://goo.gl/kROfz5) identified CL at revision 608668 as the
culprit for failures in the build cycles as shown on:
https://findit-for-me.appspot.com/waterfall/culprit?key=ag9zfmZpbmRpdC1mb3ItbWVyRAsSDVdmU3VzcGVjdGVkQ0wiMWNocm9taXVtLzZhMWRiMjVkNmEzZTYzZDE5ZDM1OTFhZjg1OGY2Mzg5ZmUyM2I3ZWUM

Sample Failed Build: https://ci.chromium.org/buildbot/chromium/android-rel/4452

Sample Failed Step: compile

Original change's description:
> document: Use ElementCreationOptions in Document.createElement()
> 
> We used (DOMString or Dictionary) type for |option| parameter,
> but this CL replaces it with (DOMString or ElementCreationOpitons)
> as the spec defined.
> 
> 
> Bug: 904241
> Change-Id: I9416af83168e7c1f7456ffdbd3141fa97b510706
> Reviewed-on: https://chromium-review.googlesource.com/c/1333094
> Commit-Queue: Hitoshi Yoshida <peria@chromium.org>
> Reviewed-by: Yuki Shiino <yukishiino@chromium.org>
> Reviewed-by: Kentaro Hara <haraken@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#608668}

Change-Id: I2e851f9c54e1327f7a0b62446ac8b24c7e7371e8
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 904241
Reviewed-on: https://chromium-review.googlesource.com/c/1339360
Cr-Commit-Position: refs/heads/master@{#608672}
[modify] https://crrev.com/97597a979e142cfe6f85e924ab6934afd1e39577/third_party/blink/renderer/bindings/core/v8/BUILD.gn
[modify] https://crrev.com/97597a979e142cfe6f85e924ab6934afd1e39577/third_party/blink/renderer/bindings/core/v8/v0_custom_element_constructor_builder.cc
[modify] https://crrev.com/97597a979e142cfe6f85e924ab6934afd1e39577/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/97597a979e142cfe6f85e924ab6934afd1e39577/third_party/blink/renderer/core/dom/document.h
[modify] https://crrev.com/97597a979e142cfe6f85e924ab6934afd1e39577/third_party/blink/renderer/core/dom/document.idl
[modify] https://crrev.com/97597a979e142cfe6f85e924ab6934afd1e39577/third_party/blink/renderer/core/html/custom/custom_element_upgrade_sorter_test.cc


### bu...@chromium.org (2018-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e3e4d7e3fd63be642f0dd27c4f6978e4b1447c5e

commit e3e4d7e3fd63be642f0dd27c4f6978e4b1447c5e
Author: Hitoshi Yoshida <peria@chromium.org>
Date: Fri Nov 16 08:54:41 2018

Reland "document: Use ElementCreationOptions in Document.createElement()"

This is a reland of 6a1db25d6a3e63d19d3591af858f6389fe23b7ee
with fixing the build error.

Original change's description:
> document: Use ElementCreationOptions in Document.createElement()
>
> We used (DOMString or Dictionary) type for |option| parameter,
> but this CL replaces it with (DOMString or ElementCreationOpitons)
> as the spec defined.
>
>
> Bug: 904241
> Change-Id: I9416af83168e7c1f7456ffdbd3141fa97b510706
> Reviewed-on: https://chromium-review.googlesource.com/c/1333094
> Commit-Queue: Hitoshi Yoshida <peria@chromium.org>
> Reviewed-by: Yuki Shiino <yukishiino@chromium.org>
> Reviewed-by: Kentaro Hara <haraken@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#608668}

Bug: 904241
Change-Id: I2ea645814ea80f9989dab93574e70e473b72a10a
Reviewed-on: https://chromium-review.googlesource.com/c/1339499
Reviewed-by: Yuki Shiino <yukishiino@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Hitoshi Yoshida <peria@chromium.org>
Cr-Commit-Position: refs/heads/master@{#608699}
[modify] https://crrev.com/e3e4d7e3fd63be642f0dd27c4f6978e4b1447c5e/third_party/blink/renderer/bindings/core/v8/BUILD.gn
[modify] https://crrev.com/e3e4d7e3fd63be642f0dd27c4f6978e4b1447c5e/third_party/blink/renderer/bindings/core/v8/v0_custom_element_constructor_builder.cc
[modify] https://crrev.com/e3e4d7e3fd63be642f0dd27c4f6978e4b1447c5e/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/e3e4d7e3fd63be642f0dd27c4f6978e4b1447c5e/third_party/blink/renderer/core/dom/document.h
[modify] https://crrev.com/e3e4d7e3fd63be642f0dd27c4f6978e4b1447c5e/third_party/blink/renderer/core/dom/document.idl
[modify] https://crrev.com/e3e4d7e3fd63be642f0dd27c4f6978e4b1447c5e/third_party/blink/renderer/core/html/custom/custom_element_upgrade_sorter_test.cc


### pe...@chromium.org (2018-11-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-12-07)

Nice bug! Many thanks, and $5,000 :-)

### aw...@google.com (2018-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-02-22)

This issue was migrated from crbug.com/chromium/904241?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093030)*

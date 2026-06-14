# Security: OOB Write in ReduceRegExpPrototypeTest

| Field | Value |
|-------|-------|
| **Issue ID** | [40050685](https://issues.chromium.org/issues/40050685) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2019-11-14 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

From <https://cs.chromium.org/chromium/src/v8/src/compiler/js-call-reducer.cc?l=7055&rcl=4636c1f0b8ea41d3d8dfe415f16f1022dd194545>

ReduceRegExpPrototypeTest don't check that the receiver's map is equal to the native context's initial regexp map, so any regexp with untouched 'exec' method will pass the check.

JS call 'RegExpPrototypeTest' will be lowered to 'RegExpTest', and it will be further lowered to a callable node which calls Builtins::kRegExpPrototypeTestFast. (<https://cs.chromium.org/chromium/src/v8/src/compiler/js-generic-lowering.cc?l=472&rcl=4636c1f0b8ea41d3d8dfe415f16f1022dd194545>)

RegExpPrototypeTestFast assumes that the regexp has initial map and read/write lastIndex field directly with specific offset, and thus cause OOB write.

This bug should affect the current stable version of Chrome.

**VERSION**  

Chrome Version: 78.0.3904.97 Stable (Official Build) (64-bit)

**REPRODUCTION CASE**  

Put the two poc files in the same directory.

d8 --allow-natives-syntax --expose-gc poc.js

What does poc file do:

1. Allocate some regexp, shrink the instance size by removing lastIndex from in-object property to ProperyArray.
2. Trigger GC to move regexp(s) to oldspace, expecting one of them lies at the bottom of a page.
3. When the jited code tries to access lastIndex field of regexp, it will crash due to access violation.

I only tested the poc on debug build d8 7.9.265 Linux x64, crash may not happen if you run the poc on other version of d8 because of the uncertainty behavior of GC process.

## Attachments

- [worker.js](attachments/worker.js) (text/plain, 5.4 KB)
- [poc.js](attachments/poc.js) (text/plain, 284 B)

## Timeline

### jt...@gmail.com (2019-11-14)

[Comment Deleted]

### do...@chromium.org (2019-11-14)

+CC V8 sheriffs for triage.

[Monorail components: Blink>JavaScript]

### ha...@chromium.org (2019-11-14)

To Jgruber@ because regex

### sh...@chromium.org (2019-11-15)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jg...@chromium.org (2019-11-18)

Sigurd would you like to take this / do you have time? If not I can take a look.

[Monorail components: Blink>JavaScript>Compiler]

### jg...@chromium.org (2019-11-18)

[Empty comment from Monorail migration]

### si...@chromium.org (2019-11-18)

[Empty comment from Monorail migration]

### jg...@chromium.org (2019-11-18)

The reducer should match IsFastRegExpPermissive (which among other things verifies the object's map). Without this it's very possible to pass in unexpected object shapes, from which we then attempt to read lastIndex at a possibly incorrect location.

Introduced in https://chromium-review.googlesource.com/1074654.

### jg...@chromium.org (2019-11-19)

As described above, there are indeed two separate OOB accesses past the end of the current object:

1. in ReduceRegExpPrototypeTest while checking validity of lastIndex, and
2. in the RegExpPrototypeTestFast builtin if step 1 can be tricked to pass the test.

### jg...@chromium.org (2019-11-19)

Minimized repro:

```
function f() {
  return r.test("abc");
}

function to_dict(o) {
  r.a = 42;
  r.b = 42;
  delete r.a;
}

function to_fast(o) {
  const obj = {};
  const obj2 = {};
  delete o.a;
  obj.__proto__ = o;
  obj[0] = 1;
  obj.__proto__ = obj2;
  delete obj[0];
  return o;
}

// Shrink the instance size by first transitioning to dictionary properties,
// then back to fast properties.
const r = /./;
to_dict(r);
to_fast(r);

%PrepareFunctionForOptimization(f);
assertTrue(f());
%OptimizeFunctionOnNextCall(f);
assertTrue(f());
```

After to_fast, the instance size is 48 whereas the initial JSRegExp map has an instance size of 56. The optimized version of f attempts to read lastIndex OOB.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/aecd84376c10622d9ad434adeb8090b23ba88fa4

commit aecd84376c10622d9ad434adeb8090b23ba88fa4
Author: Jakob Gruber <jgruber@chromium.org>
Date: Tue Nov 19 14:21:12 2019

[compiler] Fix RegExpPrototypeTest reduction

This reduction relies on a known object layout of the regexp instance
in order to access the lastIndex field through a statically-determined
offset. Prior to this CL, we checked only for instance types, not for
the map, and thus it was possible to read garbage from either inside
or outside the current object.

Bug: chromium:1024758,v8:7779
Change-Id: I1eec8220797f443bdf3d05804e54f33b21fa2f00
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1924353
Reviewed-by: Georg Neis <neis@chromium.org>
Reviewed-by: Sigurd Schneider <sigurds@chromium.org>
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/heads/master@{#65039}

[modify] https://crrev.com/aecd84376c10622d9ad434adeb8090b23ba88fa4/src/compiler/heap-refs.h
[modify] https://crrev.com/aecd84376c10622d9ad434adeb8090b23ba88fa4/src/compiler/js-call-reducer.cc
[modify] https://crrev.com/aecd84376c10622d9ad434adeb8090b23ba88fa4/src/compiler/map-inference.cc
[modify] https://crrev.com/aecd84376c10622d9ad434adeb8090b23ba88fa4/src/compiler/map-inference.h
[add] https://crrev.com/aecd84376c10622d9ad434adeb8090b23ba88fa4/test/mjsunit/regress/regress-crbug-1024758.js


### jg...@chromium.org (2019-11-19)

NextAction to check back for canary coverage.

### sh...@chromium.org (2019-11-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-19)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M78. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M79. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-19)

This bug requires manual review: M79's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-11-19)

jgruber@ pls confirm canary coverage for this CL for a merge to M-79. 

With respect to merge to M78 , can you ptal and see if this is indeed needed for M78 or can it wait until M-79 to roll out?

+adetaylor@

### ad...@chromium.org (2019-11-19)

From my side the only urgency here is the normal urgency to release this soon due to patch gappers. It's still a while till first stable release of M79 so it would be great to get this out in any future M78 stable refresh, but there is no extra special need which would merit a special release.

### go...@chromium.org (2019-11-19)

Per #13, we're waiting on canary coverage, change at #12 landed today, not in canary yet. So will wait for M79 merge review.

### bm...@chromium.org (2019-11-20)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-11-25)

How is the change looking in canary? Is it safe to merge to M79 now?

### jg...@chromium.org (2019-11-25)

Canary is looking good.

### go...@chromium.org (2019-11-25)

Approving merge to M79 branch 3945 based on https://crbug.com/chromium/1024758#c22. Please merge ASAP so we can pick it up for tomorrow's beta release. Thank you.

### go...@chromium.org (2019-11-25)

Please merge your change to M79 branch 3945 before 12:30 PM PT today so we can pick it up for tomorrow's beta release. Thank you.

### ad...@chromium.org (2019-11-25)

I'm handling this merge at govind's request. CCing hablich for visibility.

### ad...@chromium.org (2019-11-25)

Merged to M79 in 25509b1be0f66bc765df19e8207d28168b482722 (not idea why Bugdroid didn't notice)

### na...@google.com (2019-12-02)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-12-03)

We're not planning any further M78 releases. So rejecting merge to M78. 

### na...@google.com (2019-12-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-05)

Congrats! The Panel decided to reward $7,500 for this high quality report!

### na...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-12-05)

jgruber@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-06)

jtrrodant@gmail.com - how would you like to be credited in the Chrome release notes? (Thanks again for the report!)

### jt...@gmail.com (2019-12-06)

Re #34:
Thank You !
Credit info: Rong Jian and Guang Gong of Alpha Lab, Qihoo 360.

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1024758?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Compiler]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050685)*

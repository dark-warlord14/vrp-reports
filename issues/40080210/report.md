# V8 Runtime_ArrayConcat uninitialized memory leak

| Field | Value |
|-------|-------|
| **Issue ID** | [40080210](https://issues.chromium.org/issues/40080210) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | ju...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2014-08-13 |
| **Bounty** | $4,500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36

Steps to reproduce the problem:
Runtime_ArrayConcat fast double case allocates an uninitialized array:

  Handle<FixedArrayBase> storage =
      isolate->factory()->NewFixedDoubleArray(estimate_result_length);

If concat later encounters a hole, it bails out leaving the rest of the array uninitialized:

  if (elements->is_the_hole(i)) {
    failure = true;
    break;
  }

Attacker can read out this memory. Repro is attached, you might have to hit F5 a few times to see anything interesting. Tested on 36.0.1985.125 and 38.0.2120.0.

Proposed patch is attached.

What is the expected behavior?

What went wrong?

Did this work before? N/A 

Chrome version: 36.0.1985.125  Channel: stable
OS Version: 
Flash Version: Shockwave Flash 14.0 r0

## Attachments

- [leak.html](attachments/leak.html) (text/html, 855 B)
- [leak.patch](attachments/leak.patch) (application/octet-stream, 2.9 KB)

## Timeline

### mb...@chromium.org (2014-08-13)

Thanks for the report, Juri!

Could someone from the cc list please help find an owner for this?

### cl...@chromium.org (2014-08-13)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=6688780355371008

### cl...@chromium.org (2014-08-13)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5821337487540224

### mb...@chromium.org (2014-08-13)

earthdok@, kcc@: MSan doesn't seem to be catching this case. Any idea what might be going on here?

### cl...@chromium.org (2014-08-14)

[Empty comment from Monorail migration]

### ju...@gmail.com (2014-08-14)

#4: Perhaps because the buffer is in JS heap, not allocated by malloc.

### ju...@gmail.com (2014-08-14)

The patch has a semantics change. This code

arr = [];
arr[1] = 0.5;
arr.concat(0.5);

returns []. That's because concat stops with hole at index 0. With the patch it will return [undefined, 0.5, 0.5], similar to what concat currently returns for integer and object elements.

### jk...@chromium.org (2014-08-14)

Awesome bug. Thanks for the report. I'm on it.

### js...@chromium.org (2014-08-14)

Hey Juri, Good to see you!

### kc...@chromium.org (2014-08-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/external/v8.git/+/dacca11cb9b7bfa831ae8f2ce159df155f9885e2

commit dacca11cb9b7bfa831ae8f2ce159df155f9885e2
Author: jkummerow@chromium.org <jkummerow@chromium.org@ce2b1a6d-e550-0410-aec6-3dcde31c8c00>
Date: Mon Aug 18 08:51:35 2014

Correctly handle holes when concat()ing double arrays

BUG=chromium:403409
LOG=y
R=verwaest@chromium.org

Review URL: https://codereview.chromium.org/468863003

git-svn-id: https://v8.googlecode.com/svn/branches/bleeding_edge@23144 ce2b1a6d-e550-0410-aec6-3dcde31c8c00



### in...@chromium.org (2014-08-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-18)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### mb...@chromium.org (2014-08-19)

[Empty comment from Monorail migration]

### [Deleted User] (2014-08-20)

#6 - Would it make sense, then, to annotate Heap::AllocateRaw() to poison the allocated memory when running under MSan?

### jk...@chromium.org (2014-08-20)

@15 - Might be worth pursuing, but it's likely not trivial, because MSan might not detect some valid initialization paths, so manual unpoisoning might be needed (generated memmove comes to mind, which is used for copying objects; there could be other code paths).
Also, this wouldn't cover all cases, as we also allocate from generated code.

### [Deleted User] (2014-08-20)

Do those concerns remain valid if we use an instrumented arm64 emulator, as we currently do with MSan?

### [Deleted User] (2014-08-21)

Added the annotations in https://codereview.chromium.org/480763003/. Pasting Jakob's comment here for posterity:

> Considering that MSan is only run with simulators, this approach shouldn't
introduce false positives due to missing unpoisoning.

> The other caveat I mentioned on the bug is still valid, though: fast inline
allocation from generated code isn't covered by this. But some coverage is
better than no coverage, so this limitation is not a blocker.

### in...@chromium.org (2014-09-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2014-09-03)

build is being cut tonight, so punting to m38 per recommendation from inferno@

### [Deleted User] (2014-09-04)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-24)

jkummerow@ - please merge to M38 (branch 2125)

### ma...@google.com (2014-09-26)

Please process the merge approval if you haven't.

### ti...@chromium.org (2014-09-29)

jkummerow - can you please merge this to branch 2125 ASAP?

### jk...@chromium.org (2014-09-29)

version: 3.28.71.14
branch: 3.28
revision: 24296

### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-07)

Congratulations (again!) - $4500 for this report, comprised of

$4000 for Top-Tier Information Leak + exploit
+$500 for the patch

### ju...@gmail.com (2014-10-07)

:)

I probably shouldn't get the +$500 though. jkummerow wrote a different patch, mine missed the case where prototype chain has elements.

#9: Hey Justin, thanks!

### cl...@chromium.org (2014-11-24)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-01)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/403409?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080210)*

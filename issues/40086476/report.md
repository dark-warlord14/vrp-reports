# Security: Spoofing location object by overriding Symbol.toPrimitive

| Field | Value |
|-------|-------|
| **Issue ID** | [40086476](https://issues.chromium.org/issues/40086476) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Bindings, Blink>HTML |
| **Reporter** | ma...@gmail.com |
| **Assignee** | yu...@chromium.org |
| **Created** | 2017-01-12 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

Chrome allows to spoof the location object by overriding `Object.prototype[Symbol.toPrimitive]`.

You can test this behavior from the following code:

Object.prototype[Symbol.toPrimitive]=function(){return "[https://www.google.com/"}](https://www.google.com/%22%7D)  

alert(location)//returns <https://www.google.com/>

also this works:

location[Symbol.toPrimitive]=function(){return "[https://www.google.com/"}](https://www.google.com/%22%7D)  

alert(location)//returns <https://www.google.com/>

The following PoC shows that an attacker might be able to get victim's secret data using this behavior:  

<https://l0.cm/chrome_location_spoofing_symbol_toPrimitive.html>

FYI, Firefox has `Symbol.toPrimitive`. But it does not have this behavior.  

I think that the location object should return always correct current URL.

**VERSION**  

57.0.2979.1（Official Build）

## Timeline

### el...@chromium.org (2017-01-12)

[Empty comment from Monorail migration]

### aa...@google.com (2017-01-17)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### aa...@google.com (2017-01-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### ha...@chromium.org (2017-01-20)

[Empty comment from Monorail migration]

### ad...@chromium.org (2017-01-20)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript Blink>Bindings Blink>HTML]

### sh...@chromium.org (2017-01-26)

yukishiino: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/34bee46b0be6afc06f254ec0debd4b868443a649

commit 34bee46b0be6afc06f254ec0debd4b868443a649
Author: yukishiino <yukishiino@chromium.org>
Date: Fri Jan 27 07:29:15 2017

Exposes Symbol.toPrimitive in C++ APIs as Symbol::GetToPrimitive.

As Blink needs to set Symbol.toPrimitive, exposes the symbol in C++ APIs
as Symbol::GetToPrimitive.

BUG=chromium:680409

Review-Url: https://codereview.chromium.org/2657933003
Cr-Commit-Position: refs/heads/master@{#42724}

[modify] https://crrev.com/34bee46b0be6afc06f254ec0debd4b868443a649/include/v8.h
[modify] https://crrev.com/34bee46b0be6afc06f254ec0debd4b868443a649/src/api.cc


### bu...@chromium.org (2017-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1f959adce3efa86d7d9560f9642c6ae816f8d81c

commit 1f959adce3efa86d7d9560f9642c6ae816f8d81c
Author: yukishiino <yukishiino@chromium.org>
Date: Mon Jan 30 16:06:13 2017

binding: Sets location[Symbol.toPrimitive].

Let the location objects have Symbol.toPrimitive property
as an unconfiguable own property, so that author scripts
cannot inject nor overwrite it.

BUG=680409

Review-Url: https://codereview.chromium.org/2656973002
Cr-Commit-Position: refs/heads/master@{#446991}

[add] https://crrev.com/1f959adce3efa86d7d9560f9642c6ae816f8d81c/third_party/WebKit/LayoutTests/fast/dom/location-toprimitive.html
[modify] https://crrev.com/1f959adce3efa86d7d9560f9642c6ae816f8d81c/third_party/WebKit/Source/bindings/templates/interface_base.cpp.tmpl


### yu...@chromium.org (2017-01-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-07)

Your change meets the bar and is auto-approved for M57. Please go ahead and merge the CL to branch 2987 manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-02-07)

If possible, please merge your change to M57 branch 2987 before 5:00 PM PT today,Tuesday (02/07/17) so we can pick it up for next Beta release. Thank you.

### go...@chromium.org (2017-02-09)

Please merge your change to M57 branch 2987 before 5:00 PM PT, Friday 02/10 (sooner the better please) so we can take it in for next week beta release. Thank you.

### yu...@chromium.org (2017-02-09)

Sorry for the late response, I was OOO.

My fix (https://crrev.com/2656973002) depends on another CL in V8 repository (https://crrev.com/2657933003).  So, I cannot simply merge the fix to M57 branch 2987.  (If merged, it breaks the build.)

What should I do?  I think our options are:
a) make M57 include a newer version of V8, and merge my fix.
b) merge my preparation CL in V8 directly into M57 (is this really okay or possible?), and merge my fix.
c) do not merge


### go...@chromium.org (2017-02-09)

[Comment Deleted]

### go...@chromium.org (2017-02-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-02-10)

Hi yukishiino@. I'd really rather not wait until M58 to take this fix if at all possible.

I believe we've done something similar to b) in the past in the Chromium repro, providing the prerequisite change is small and low risk (which this one seems to be). If they can be merged independently that would be my suggestion, as the diffs between what's currently in 57 and the prerequisite change are pretty substantial.

### aw...@chromium.org (2017-02-10)

[Empty comment from Monorail migration]

### yu...@chromium.org (2017-02-13)

+cc: jochen@,

Could you let me know how to merge a CL into V8 branch 5.7 and auto-roll?

I vaguely guess that I need to do the following but I don't know exact steps nor command lines.
step 1) Merge https://crrev.com/2657933003 into V8 branch 5.7
step 2) Increment the minor version of V8
step 3) Roll the updated V8 into Chromium
Is there any detailed guideline?


### jo...@chromium.org (2017-02-13)

Use tools/release/merge_to_branch.py -r hablich@chronium.org --branch 5.7 <hash> in a V8 checkout

### bu...@chromium.org (2017-02-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/d84f2b2b7ee3cb94afd1d539e5ebdbaa29e5b26c

commit d84f2b2b7ee3cb94afd1d539e5ebdbaa29e5b26c
Author: yukishiino <yukishiino@chromium.org>
Date: Mon Feb 13 12:34:32 2017

Merged: Exposes Symbol.toPrimitive in C++ APIs as Symbol::GetToPrimitive.

Revision: 34bee46b0be6afc06f254ec0debd4b868443a649

BUG=chromium:680409
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=hablich@chronium.org

Review-Url: https://codereview.chromium.org/2692823002
Cr-Commit-Position: refs/branch-heads/5.7@{#98}
Cr-Branched-From: 975e9a320b6eaf9f12280c35df98e013beb8f041-refs/heads/5.7.492@{#1}
Cr-Branched-From: 8d76f0e3465a84bbf0bceab114900fbe75844e1f-refs/heads/master@{#42426}

[modify] https://crrev.com/d84f2b2b7ee3cb94afd1d539e5ebdbaa29e5b26c/include/v8.h
[modify] https://crrev.com/d84f2b2b7ee3cb94afd1d539e5ebdbaa29e5b26c/src/api.cc


### bu...@chromium.org (2017-02-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/601b6bfa2b363e4c1acc4ab599f30ccde43b8a06

commit 601b6bfa2b363e4c1acc4ab599f30ccde43b8a06
Author: Yuki Shiino <yukishiino@chromium.org>
Date: Mon Feb 13 12:48:21 2017

binding: Sets location[Symbol.toPrimitive].

Let the location objects have Symbol.toPrimitive property
as an unconfiguable own property, so that author scripts
cannot inject nor overwrite it.

BUG=680409

Review-Url: https://codereview.chromium.org/2656973002
Cr-Commit-Position: refs/heads/master@{#446991}
(cherry picked from commit 1f959adce3efa86d7d9560f9642c6ae816f8d81c)

Review-Url: https://codereview.chromium.org/2692873002 .
Cr-Commit-Position: refs/branch-heads/2987@{#472}
Cr-Branched-From: ad51088c0e8776e8dcd963dbe752c4035ba6dab6-refs/heads/master@{#444943}

[add] https://crrev.com/601b6bfa2b363e4c1acc4ab599f30ccde43b8a06/third_party/WebKit/LayoutTests/fast/dom/location-toprimitive.html
[modify] https://crrev.com/601b6bfa2b363e4c1acc4ab599f30ccde43b8a06/third_party/WebKit/Source/bindings/templates/interface_base.cpp.tmpl


### yu...@chromium.org (2017-02-13)

Thank you guys all for helping me.  I've merged the fix into M57 (2987).

### aw...@chromium.org (2017-02-13)

Excellent, thanks!

### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-13)

Thanks for the report yukishiino@!  The panel decided to award $500.

### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### yu...@chromium.org (2017-02-14)

re #31: Just in case, I'm not the reporter.

### aw...@google.com (2017-02-14)

Yep, sorry. Thanks masatokinugawa@!

### aw...@chromium.org (2017-02-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/680409?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Bindings, Blink>HTML]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086476)*

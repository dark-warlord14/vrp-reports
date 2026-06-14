# Security: OOB Access in V8 

| Field | Value |
|-------|-------|
| **Issue ID** | [40096142](https://issues.chromium.org/issues/40096142) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | si...@chromium.org |
| **Created** | 2019-08-29 |
| **Bounty** | $10,000.00 |

## Description

(filed on behalf of the reporter)

The bug:

We know that, the size of JSFunctin object in v8 is not fixed. it may contain the field PrototypeOrInitialMap or not. But the macro [GetDerivedMap](https://cs.chromium.org/chromium/src/v8/src/builtins/base.tq?rcl=568f3984d3ead0863deb3e84eec4c0ccd33a4936&l=372) in base.tq doesn't check this situation and accesses PrototypeOrInitialMap directly, which results in OOB access.

```tq
macro GetDerivedMap(implicit context: Context)(
    target: JSFunction, newTarget: JSReceiver): Map {
  try {
    const constructor = Cast<JSFunction>(newTarget) otherwise SlowPath;
    const map =
        Cast<Map>(constructor.prototype_or_initial_map) otherwise SlowPath; *** oob access occurs here
    if (LoadConstructorOrBackPointer(map) != target) { ***[1]***
      goto SlowPath;
    }

    return map;
  }
  label SlowPath {
    return runtime::GetDerivedMap(context, target, newTarget);
  }
}
```

How to exploit

To trigger the oob access, we have to find a constructor without prototype_or_initial_map, it seems like the Proxy function is the only selection. The bug can be triggered by the following simple code

```JavaScript
var malformedTypedArray = Reflect.construct(Uint8Array, [4], Proxy)
```

But if the above JavaScript is run in chrome simply, nothing will happen although the OOB access has already occurred. it's because that after loading prototype_or_initial_map, the value will be treat as a map, its constructor is loaded and compared with target(in position [1]),and in most situations, this value is a legal map but it's constructor is not the same as the target, so execution flow will bail out to slow path, every things is normal. if the oob accessed prototype_or_initial_map isn't a map, execution flow will bail out to slow path too while it's cast to map failed.
So here is the exploit strategy:

1. free the object below the Proxy function.

2. reoccupy the free space with an object whose map's(named map x) constructor is Uint8Array, So the fast path will continue. the wrong map will be returned.

3. win some races to free the map x before it's linked to root objects.

4. reoccupy the freed space with a map whose constructor is Uint32Array, so we can get a malformed typed array, its map is Uint32Array, but its layout especially its element is Uin8Array, it's easy to get arbitrary read and write with this malformaed object.



## Timeline

### aw...@google.com (2019-08-29)

[Empty comment from Monorail migration]

### aw...@google.com (2019-08-29)

[Empty comment from Monorail migration]

### aw...@google.com (2019-08-29)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### aw...@google.com (2019-08-29)

[Empty comment from Monorail migration]

### aw...@google.com (2019-08-29)

To the V8 US timezone sheriff. Hi fgm@. This was part of a full chain exploit, but responsibly disclosed so it's not an emergency, but would be good to get it routed to the right engineer quickly. Cheers!

### ct...@chromium.org (2019-08-29)

Note that this is also connected to https://crbug.com/chromium/999311.

cc'ing the engineers who are on the CL that created the TQ port of GetDerivedMap, specifically nicohartmann@ (https://chromium-review.googlesource.com/c/v8/v8/+/1609804). Do you think adding a check here would be a reasonable initial fix?

[Monorail components: Blink>JavaScript>Runtime]

### ct...@chromium.org (2019-08-29)

[Empty comment from Monorail migration]

### aw...@google.com (2019-08-29)

[Empty comment from Monorail migration]

### ct...@chromium.org (2019-08-29)

Assigning this to sigurds@ since it appears nicohartmann@ was an intern and is no longer active.

### aw...@google.com (2019-08-30)

[Empty comment from Monorail migration]

### si...@chromium.org (2019-08-30)

[Empty comment from Monorail migration]

### ha...@chromium.org (2019-08-30)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/bdcc7502cb01bcf1bd3300573be6c1352b8cfd72

commit bdcc7502cb01bcf1bd3300573be6c1352b8cfd72
Author: Sigurd Schneider <sigurds@chromium.org>
Date: Fri Aug 30 09:37:23 2019

[torque] Check for prototype before loading it

Add a missing check for a prototype to GetDerivedMap.

Bug: chromium:999310
Change-Id: I99c342a53e3b95bb7b624ff14c1c40576ee629df
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1776092
Auto-Submit: Sigurd Schneider <sigurds@chromium.org>
Commit-Queue: Tobias Tebbi <tebbi@chromium.org>
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/master@{#63473}

[modify] https://crrev.com/bdcc7502cb01bcf1bd3300573be6c1352b8cfd72/src/builtins/base.tq
[modify] https://crrev.com/bdcc7502cb01bcf1bd3300573be6c1352b8cfd72/src/codegen/code-stub-assembler.cc
[modify] https://crrev.com/bdcc7502cb01bcf1bd3300573be6c1352b8cfd72/src/codegen/code-stub-assembler.h


### si...@chromium.org (2019-08-30)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-08-30)

sigurds@, thank you for the fix. Please merge the change listed at #13 to current canary branch 3898 so we can trigger new canary from same branch. Thank you.

### si...@chromium.org (2019-08-30)

I merged to Version 7.8.231.1
https://chromium-review.googlesource.com/c/v8/v8/+/1778290
and updated canary branch 3898 accordingly.

### sh...@chromium.org (2019-08-30)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-08-30)

Thank you sigurds@. New canary version #78.0.3898.1 in trigger queue with merge listed at #16. Please verify the bug when new canary becomes available. 

### sh...@chromium.org (2019-08-30)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M76. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M77. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-30)

This bug requires manual review: We are only 10 days from stable.
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
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-08-30)

Rejecting merge to M76 based on meeting with TPMs.

Please update bug with canary result  before we approve merge to M77.

+benmason@ & +lakpamarthy@ (M77 Release TPMs)


### na...@google.com (2019-09-03)

[Empty comment from Monorail migration]

### la...@chromium.org (2019-09-03)

sigurds@ - can you update the bug with a response to C#20 so we can consider for M77? Would be good to get this change into tomorrow's Beta.

### si...@chromium.org (2019-09-03)

1. Does your merge fit within the Merge Decision Guidelines? 
  Yes.
2. Links to the CLs you are requesting to merge.
  https://chromium-review.googlesource.com/c/v8/v8/+/1776092
3. Has the change landed and been verified on master/ToT?
  There was no exploit provided, only a general description of how to construct one. 
  There is no simple way to write a deterministic repro.
  We verified locally that the fix is working.
4. Why are these changes required in this milestone after branch?
  This CL fixes a security vulnerability.
5. Is this a new feature?
  No.
6. If it is a new feature, is it behind a flag using finch?
  n/a

### la...@chromium.org (2019-09-03)

merge approved for M77 branch 3865

### si...@chromium.org (2019-09-03)

Landed: https://chromium.googlesource.com/v8/v8/+/3e2dda91f7f2284423814696095c8ac3480d9ba3

### si...@chromium.org (2019-09-03)

Also merged to M77 branch head: https://chromium-review.googlesource.com/c/v8/v8/+/1782823

### la...@google.com (2019-09-03)

This request for M77 merge is already approved. Please land your changes into M77 branch (3865) today. We are one week away from Stable and doing the final Beta tomorrow.

### la...@google.com (2019-09-03)

Dropping the Merge-Approved-77 label as the change has landed to M77 V8 branch head

### aw...@google.com (2019-09-05)

[Empty comment from Monorail migration]

### aw...@google.com (2019-09-05)

For reference the internal tracking bug with some more details is b/140174798

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-09-16)

Congrats! The Panel decided to reward $10,000 for this report! 

### pa...@chromium.org (2019-09-16)

[Comment Deleted]

### na...@google.com (2019-09-16)

[Empty comment from Monorail migration]

### hi...@gmail.com (2019-11-22)

Hi, Can we keep this bug private? please don't remove Restrict-View-SecurityNotify, I want to disclose it myself, thanks.

### ad...@google.com (2019-11-22)

Restrict-View-SecurityEmbargo will ensure this stays private.

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-02-20)

[Empty comment from Monorail migration]

### aw...@google.com (2020-07-07)

Remove allpublic from bugs that have Restrict-View-SecurityEmbargo

### aw...@google.com (2020-07-08)

higongguang@ - Confirming we're now OK to open this bug publically?

### hi...@gmail.com (2020-07-09)

awhalley@  I want to delay it until I finish the BLACKHAT USA 2020 presentation

### aw...@google.com (2020-07-09)

Sounds good. Setting a Next Action of 2020-10-05 to open up after Blackhat.

### aw...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### si...@chromium.org (2021-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2021-04-26)

This issue was migrated from crbug.com/chromium/999310?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Runtime]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096142)*

# Security: Heap-use-after-free in AutofillAgent::FillFieldWithValue

| Field | Value |
|-------|-------|
| **Issue ID** | [40084205](https://issues.chromium.org/issues/40084205) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **CVE IDs** | CVE-2016-1690 |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | va...@chromium.org |
| **Created** | 2016-04-29 |
| **Bounty** | $1,000.00 |

## Description

Chrome version: 50.0.2661.75

Open the attached PoC (uaf-autofill-auto.html) and follow its instructions to trigger the UAF.
Basically:
1. Save a password in Autofill.
2. Refresh the page
3. Switch to another window/tab and back, OR click anywhere in the page (not necessarily the frame containing the form field).

https://chromium.googlesource.com/chromium/src/+/4f6b038b0bc4589d9f021debda64c160c1ca3c5c/components/autofill/content/renderer/autofill_agent.cc#773
void AutofillAgent::FillFieldWithValue(const base::string16& value,
                                       WebInputElement* node) {
  base::AutoReset<bool> auto_reset(&ignore_text_changes_, true);
  node->setEditingValue(value.substr(0, node->maxLength()));
  // ^^^ This triggers the input event from the web page.
  // When the web page removes the frame, then the RenderFrameObserver
  // (the superclass of AutofillAgent) is destructed and therefore
  // ignore_text_changes_ points to invalid memory.
  // When auto_reset goes out of scope, we have a UAF.

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [asan-autofill-suggestion-list-50.0.2661.94.log](attachments/asan-autofill-suggestion-list-50.0.2661.94.log) (text/plain, 20.0 KB)
- [uaf-autofill-suggestion-list.html](attachments/uaf-autofill-suggestion-list.html) (text/plain, 983 B)

## Timeline

### rs...@chromium.org (2016-05-02)

vabr: Can you please take a look?

### is...@chromium.org (2016-05-02)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-05-02)

The initial report listed the incorrect test case and stack trace (namely for https://crbug.com/chromium/608101).

I've now attached the stack trace and test case for this bug.

### va...@chromium.org (2016-05-03)

Thanks a lot for this report and the great analysis!

I'll need to think a bit about what to do in general to avoid UAF in AutofillAgent and PasswordAutofillAgent when they use setValue or setEditingValue.

### va...@chromium.org (2016-05-03)

On a suggestion from dvadym@, I'm going to try to make the agents delete themselves with a delay, posting a task to do so.

### va...@chromium.org (2016-05-03)

https://codereview.chromium.org/1943873002/ is in progress, once the bots are happy, I'll send it out for review.

### bu...@chromium.org (2016-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a8755e432460c9412291c0ae4dd887babb3fa506

commit a8755e432460c9412291c0ae4dd887babb3fa506
Author: vabr <vabr@chromium.org>
Date: Tue May 03 15:04:05 2016

Postpone deletion of (Password)AutofillAgent

Currently, the two agent classes delete themselves immediately on destruction
of the RenderFrame they are observing. This CL postpones the deletion to a
separately posted task, to avoid the situation when the agent is deleted while
still having methods in progress lower on the stack.

BUG=608100

Review-Url: https://codereview.chromium.org/1943873002
Cr-Commit-Position: refs/heads/master@{#391236}

[modify] https://crrev.com/a8755e432460c9412291c0ae4dd887babb3fa506/components/autofill/content/renderer/autofill_agent.cc
[modify] https://crrev.com/a8755e432460c9412291c0ae4dd887babb3fa506/components/autofill/content/renderer/autofill_agent.h
[modify] https://crrev.com/a8755e432460c9412291c0ae4dd887babb3fa506/components/autofill/content/renderer/password_autofill_agent.cc
[modify] https://crrev.com/a8755e432460c9412291c0ae4dd887babb3fa506/components/autofill/content/renderer/password_autofill_agent.h


### va...@chromium.org (2016-05-03)

I'll request the merges once this bakes in the Canary.

However, due to holidays I'll only be able to do that next week.
If there is any hurry, people are welcome to do the merge earlier, once approved.

### va...@chromium.org (2016-05-03)

(And by "do the merge" I mean "request and merge". :))

### va...@chromium.org (2016-05-04)

As https://crbug.com/chromium/609007 shows, I forgot about other tasks posted before the deletion but executed after the frame destruction. Fixing that at the moment, but I believe it is prudent to wait with the merge request until next week in any case, to check for other crashes.

### bu...@chromium.org (2016-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/50bf9075cac0e5d69f5adfc0763968d5afa1734b

commit 50bf9075cac0e5d69f5adfc0763968d5afa1734b
Author: vabr <vabr@chromium.org>
Date: Wed May 04 09:13:51 2016

Revert of Postpone deletion of (Password)AutofillAgent (patchset #1 id:1 of https://codereview.chromium.org/1943873002/ )

Reason for revert:
This fix is not complete, I need to also handle disabling the LegacyAutofillAgent.

Because the final fix is going to be merged, I prefer to have the complete solution in one CL. Therefore I am reverting this partial fix, and will reintroduce it in a new CL. Sorry for the noise.

BUG=609010, 609007, 608100, 608101

Original issue's description:
> Postpone deletion of (Password)AutofillAgent
>
> Currently, the two agent classes delete themselves immediately on destruction
> of the RenderFrame they are observing. This CL postpones the deletion to a
> separately posted task, to avoid the situation when the agent is deleted while
> still having methods in progress lower on the stack.
>
> BUG=608100
>
> Committed: https://crrev.com/a8755e432460c9412291c0ae4dd887babb3fa506
> Cr-Commit-Position: refs/heads/master@{#391236}

TBR=mathp@chromium.org,dvadym@chromium.org
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=608100

Review-Url: https://codereview.chromium.org/1951813002
Cr-Commit-Position: refs/heads/master@{#391465}

[modify] https://crrev.com/50bf9075cac0e5d69f5adfc0763968d5afa1734b/components/autofill/content/renderer/autofill_agent.cc
[modify] https://crrev.com/50bf9075cac0e5d69f5adfc0763968d5afa1734b/components/autofill/content/renderer/autofill_agent.h
[modify] https://crrev.com/50bf9075cac0e5d69f5adfc0763968d5afa1734b/components/autofill/content/renderer/password_autofill_agent.cc
[modify] https://crrev.com/50bf9075cac0e5d69f5adfc0763968d5afa1734b/components/autofill/content/renderer/password_autofill_agent.h


### bu...@chromium.org (2016-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9de81f45c73a8f9f215fc234a6adfe087b0eab74

commit 9de81f45c73a8f9f215fc234a6adfe087b0eab74
Author: vabr <vabr@chromium.org>
Date: Wed May 04 10:48:04 2016

Remove WeakPtrFactory from PasswordAutofillAgent

Unlike in AutofillAgent, the factory is no longer used in PAA.

R=dvadym@chromium.org
BUG=609010,609007,608100,608101,433486

Review-Url: https://codereview.chromium.org/1945723003
Cr-Commit-Position: refs/heads/master@{#391475}

[modify] https://crrev.com/9de81f45c73a8f9f215fc234a6adfe087b0eab74/components/autofill/content/renderer/password_autofill_agent.cc
[modify] https://crrev.com/9de81f45c73a8f9f215fc234a6adfe087b0eab74/components/autofill/content/renderer/password_autofill_agent.h


### bu...@chromium.org (2016-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d62bc3e6e2c3be6bbb01fa325e3389f089974017

commit d62bc3e6e2c3be6bbb01fa325e3389f089974017
Author: vabr <vabr@chromium.org>
Date: Wed May 04 15:58:52 2016

Destroy (Password)AutofillAgent safely

AutofillAgent and related code often edits field values. Those edits may trigger JavaScript capable of deleting the associated frame. Currently, AutofillAgent and related classes are RenderFrameObservers and delete themselves on the frame deletion. This results in use-after-free if the deletion happens up in the stack and there is still the method which changed the field value down on the stack.

Therefore this CL postpones deletion by sending a DeleteSoon task on the frame destruction. The CL also changes a couple of places relying on render frame being alive if the observer is alive to handle a null frame gratefully.

R=dvadym@chromium.org
BUG=609010,609007,608100,608101

Review-Url: https://codereview.chromium.org/1946143002
Cr-Commit-Position: refs/heads/master@{#391524}

[modify] https://crrev.com/d62bc3e6e2c3be6bbb01fa325e3389f089974017/components/autofill/content/renderer/autofill_agent.cc
[modify] https://crrev.com/d62bc3e6e2c3be6bbb01fa325e3389f089974017/components/autofill/content/renderer/autofill_agent.h
[modify] https://crrev.com/d62bc3e6e2c3be6bbb01fa325e3389f089974017/components/autofill/content/renderer/form_autofill_util.cc
[modify] https://crrev.com/d62bc3e6e2c3be6bbb01fa325e3389f089974017/components/autofill/content/renderer/password_autofill_agent.cc
[modify] https://crrev.com/d62bc3e6e2c3be6bbb01fa325e3389f089974017/components/autofill/content/renderer/password_autofill_agent.h
[modify] https://crrev.com/d62bc3e6e2c3be6bbb01fa325e3389f089974017/components/autofill/content/renderer/password_generation_agent.cc
[modify] https://crrev.com/d62bc3e6e2c3be6bbb01fa325e3389f089974017/components/autofill/content/renderer/password_generation_agent.h


### va...@chromium.org (2016-05-09)

Requesting merge of r391524 to 51 (branch 2704). The patch has been sitting on ToT for 4 days, hit Canary and caused no crashes or bugreports as far as I could find.

### va...@chromium.org (2016-05-09)

Requesting merge of r391524 to 50 (branch 2661). The patch has been sitting on ToT for 4 days, hit Canary and caused no crashes or bugreports as far as I could find.

### ti...@google.com (2016-05-09)

[Automated comment] Request affecting a post-stable build (M50), manual review required.

### ti...@google.com (2016-05-09)

Your change meets the bar and is auto-approved for M51 (branch: 2704)

### bu...@chromium.org (2016-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7e112c1563632f57cfa1c4fa964987f823da17fa

commit 7e112c1563632f57cfa1c4fa964987f823da17fa
Author: Vaclav Brozek <vabr@chromium.org>
Date: Mon May 09 07:18:24 2016

Destroy (Password)AutofillAgent safely

AutofillAgent and related code often edits field values. Those edits may trigger JavaScript capable of deleting the associated frame. Currently, AutofillAgent and related classes are RenderFrameObservers and delete themselves on the frame deletion. This results in use-after-free if the deletion happens up in the stack and there is still the method which changed the field value down on the stack.

Therefore this CL postpones deletion by sending a DeleteSoon task on the frame destruction. The CL also changes a couple of places relying on render frame being alive if the observer is alive to handle a null frame gratefully.

R=dvadym@chromium.org
BUG=609010,609007,608100,608101

Review-Url: https://codereview.chromium.org/1946143002
Cr-Commit-Position: refs/heads/master@{#391524}
(cherry picked from commit d62bc3e6e2c3be6bbb01fa325e3389f089974017)

Review URL: https://codereview.chromium.org/1960023002 .

Cr-Commit-Position: refs/branch-heads/2704@{#441}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/7e112c1563632f57cfa1c4fa964987f823da17fa/components/autofill/content/renderer/autofill_agent.cc
[modify] https://crrev.com/7e112c1563632f57cfa1c4fa964987f823da17fa/components/autofill/content/renderer/autofill_agent.h
[modify] https://crrev.com/7e112c1563632f57cfa1c4fa964987f823da17fa/components/autofill/content/renderer/form_autofill_util.cc
[modify] https://crrev.com/7e112c1563632f57cfa1c4fa964987f823da17fa/components/autofill/content/renderer/password_autofill_agent.cc
[modify] https://crrev.com/7e112c1563632f57cfa1c4fa964987f823da17fa/components/autofill/content/renderer/password_autofill_agent.h
[modify] https://crrev.com/7e112c1563632f57cfa1c4fa964987f823da17fa/components/autofill/content/renderer/password_generation_agent.cc
[modify] https://crrev.com/7e112c1563632f57cfa1c4fa964987f823da17fa/components/autofill/content/renderer/password_generation_agent.h


### cl...@chromium.org (2016-05-09)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-05-09)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-09)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-25)

Updating to Medium severity due to the amount of user interaction required.

### ti...@google.com (2016-05-26)

Rob - another $1,000 here. Woohoo!

Panel notes: Reduced amount due to amount of user interaction required. CVE-ID is CVE-2016-1690.

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-15)

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

### ku...@gmail.com (2017-01-06)

[Comment Deleted]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### ma...@chromium.org (2018-07-03)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-03)

This issue was migrated from crbug.com/chromium/608100?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/608101]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084205)*

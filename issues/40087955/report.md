# Security: IndexedDB OpenCursor UaF

| Field | Value |
|-------|-------|
| **Issue ID** | [40087955](https://issues.chromium.org/issues/40087955) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>IndexedDB |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ne...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2017-06-02 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

In content/browser/indexed\_db/indexed\_db\_database.cc, leveldb::Status IndexedDBDatabase::OpenCursorOperation creates a cursor and passes ownership of it to an instance of IndexedDBCallbacks, which itself takes ::indexed\_db::mojom::CallbacksAssociatedPtrInfo callbacks\_info which is provided by the renderer. If callbacks\_info is invalid, the IndexedDBCallbacks leaves callbacks\_ uninitialized. Before passing ownership of the cursor, it stores a raw pointer to the cursor in the transaction.

The unique\_ptr owning the cursor makes its way to IndexedDBCallbacks::IOThreadHelper::SendSuccessCursor, where it is finally added to the dispatcher. But if the IndexedDBCallbacks doesn't have a callbacks\_ or dispatcher\_host\_, the ownership is not passed and so the cursor gets destructed. A UaF occurs when the raw pointer to the cursor is accessed as accessed as part of the transaction.

I'm not sure if this requires a renderer patch, as there may be another way to destroy the dispatcher host or cause the mojo binding to fail before the callback occurs, but this should sufficient to show the issue.

**VERSION**  

Chrome Version: 58.0 Stable  

Operating System: All

**REPRODUCTION CASE**  

Apply the attached renderer patch and open cursor.html. Close the browser or refresh to see the ASAN error.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan.log

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 13.7 KB)
- [no_callback.patch](attachments/no_callback.patch) (application/octet-stream, 826 B)
- [cursor.html](attachments/cursor.html) (text/plain, 274 B)
- [fix.patch](attachments/fix.patch) (application/octet-stream, 940 B)

## Timeline

### ne...@gmail.com (2017-06-02)

I think we can fix this by ensuring that the cursor removes itself from the transaction when IndexedDBCursor is destructed, rather than when CursorImpl (that we return before constructing) is destructed. See the attached patch.

### el...@chromium.org (2017-06-02)

[Empty comment from Monorail migration]

[Monorail components: Blink>Storage>IndexedDB]

### mb...@chromium.org (2017-06-05)

jsbell: Would you mind taking a look at this or reassigning?

### js...@chromium.org (2017-06-05)

dmurph@ - please take a look

### dm...@chromium.org (2017-06-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-06-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d007b8b750851fe1b375c463009ea3b24e5c021d

commit d007b8b750851fe1b375c463009ea3b24e5c021d
Author: Daniel Murphy <dmurph@chromium.org>
Date: Wed Jun 07 01:24:31 2017

[IndexedDB] Fix Cursor UAF

If the connection is closed before we return a cursor, it dies in
IndexedDBCallbacks::IOThreadHelper::SendSuccessCursor. It's deleted on
the correct thread, but we also need to makes sure to remove it from its
transaction.

To make things simpler, we have the cursor remove itself from its
transaction on destruction.

R: pwnall@chromium.org
Bug: 728887
Change-Id: I8c76e6195c2490137a05213e47c635d12f4d3dd2
Reviewed-on: https://chromium-review.googlesource.com/526284
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/heads/master@{#477504}
[modify] https://crrev.com/d007b8b750851fe1b375c463009ea3b24e5c021d/content/browser/indexed_db/cursor_impl.cc
[modify] https://crrev.com/d007b8b750851fe1b375c463009ea3b24e5c021d/content/browser/indexed_db/indexed_db_cursor.cc
[modify] https://crrev.com/d007b8b750851fe1b375c463009ea3b24e5c021d/content/browser/indexed_db/indexed_db_cursor.h


### dm...@chromium.org (2017-06-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-07)

Your change meets the bar and is auto-approved for M60. Please go ahead and merge the CL to branch 3112 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), josafat@(ChromeOS), bustamante@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-06-07)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-06-07)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-06-07)

+awhalley@ for security review. 

### ab...@chromium.org (2017-06-08)

Thanks for confirming - can you please confirm if both changes are safe merges, and if they are tested/verified in canary?

### sh...@chromium.org (2017-06-08)

[Empty comment from Monorail migration]

### dm...@chromium.org (2017-06-08)

I strongly believe the change is safe - it should be in canary today. I think it is safe to merge.

### ab...@chromium.org (2017-06-08)

Per discussion with awhalley@, since this is not baked in canary, dev, or beta yet - we will not consider this for Monday's M59 respin. Per the usual process, merges should be baked in beta prior to coming to stable.

### aw...@chromium.org (2017-06-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-06-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-06-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/51bbaf611b628c9396f573435bb0a9289434923f

commit 51bbaf611b628c9396f573435bb0a9289434923f
Author: Daniel Murphy <dmurph@chromium.org>
Date: Mon Jun 12 18:40:02 2017

[IndexedDB] Fix Cursor UAF

If the connection is closed before we return a cursor, it dies in
IndexedDBCallbacks::IOThreadHelper::SendSuccessCursor. It's deleted on
the correct thread, but we also need to makes sure to remove it from its
transaction.

To make things simpler, we have the cursor remove itself from its
transaction on destruction.

TBR=dmurph@chromium.org

(cherry picked from commit d007b8b750851fe1b375c463009ea3b24e5c021d)

R: pwnall@chromium.org
Bug: 728887
Change-Id: I8c76e6195c2490137a05213e47c635d12f4d3dd2
Reviewed-on: https://chromium-review.googlesource.com/526284
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#477504}
Reviewed-on: https://chromium-review.googlesource.com/531774
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/branch-heads/3112@{#308}
Cr-Branched-From: b6460e24cf59f429d69de255538d0fc7a425ccf9-refs/heads/master@{#474897}
[modify] https://crrev.com/51bbaf611b628c9396f573435bb0a9289434923f/content/browser/indexed_db/cursor_impl.cc
[modify] https://crrev.com/51bbaf611b628c9396f573435bb0a9289434923f/content/browser/indexed_db/indexed_db_cursor.cc
[modify] https://crrev.com/51bbaf611b628c9396f573435bb0a9289434923f/content/browser/indexed_db/indexed_db_cursor.h


### aw...@chromium.org (2017-06-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-27)

Congratulations nedwilliamson@! The VRP panel decided to award $1,000 for this report :-)

### ne...@gmail.com (2017-06-27)

Thanks! Though I thought because this was a use-after-free in the browser process it would be considered a sandbox escape. I was able to reliably crash the browser in my testing but didn't get register control yet (the object is smaller so spraying on the IDB thread isn't as reliable as my other bug, at least using the same spray technique). If there's something I can do to improve the report please let me know!

### aw...@chromium.org (2017-06-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-28)

Hi nedwilliamson@ - I'm terribly sorry, we made a mistake and the reward was too low by a decimal order of magnitude!  Thank you for raising the fact you thought it was a bit low :-D  I've managed to get the value changed with our finance folk so it shouldn't delay payment.

### ne...@gmail.com (2017-06-28)

awhalley@: Wow, thanks! I just wanted to make sure I wasn't missing any useful information in the report. Thanks again for the generous reward! :-)

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/728887?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087955)*

# UAF in indexeddb database

| Field | Value |
|-------|-------|
| **Issue ID** | [40055100](https://issues.chromium.org/issues/40055100) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>IndexedDB |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | su...@gmail.com |
| **Assignee** | ro...@google.com |
| **Created** | 2021-03-08 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36

Steps to reproduce the problem:
1.git apply git.patch
2.ninja -C out/asan chrome
3.out/asan/chrome --user-data-dir=/tmp/xxxx "http://192.168.0.14:8000/indexed.html"
4、wait for your browser crash

What is the expected behavior?

What went wrong?
1、IndexedDBDispatcherHost::CreateCursorBinding hold the raw_pointer of cursor_impl [1].
2、cursor_impl will be stored in receivers_ through  cursor_receivers_.Add [2] =>AddImpl [3]=>receivers_.insert(std::make_pair(id, std::move(entry)));[6].
3、id in insert function is from next_receiver_id_++;[4].
4、The type of next_receiver_id_ is size_t.In 32bits .The maxium of it's value is 4294967296.If next_receiver_id_ overflow we can get a same id to make receivers_.insert fail so the unique_ptr cursor_impl will be freed.
5、Then using the raw_pointer cursor_impl_ptr to call the function cursor_impl_ptr->OnRemoveBinding()[5] will cause a UAF bug in browser.

However,if we insert to receivers_ 4294967296 times  will cause OOM,but in my poc,I hold the id 0.Then insert 0x500 times to receivers_. Remove the 0x500 id and repeate this operation.Finally It will overflow next_receiver_id_ and trigger the  uaf in browser!

POC is just for proof.It can be work in 64bits patched chrome and  POC can be improved to run quicker when in 32 bits.

mojo::PendingAssociatedRemote<blink::mojom::IDBCursor>
IndexedDBDispatcherHost::CreateCursorBinding(
    const url::Origin& origin,
    std::unique_ptr<IndexedDBCursor> cursor) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
  auto cursor_impl = std::make_unique<CursorImpl>(std::move(cursor), origin,this, IDBTaskRunner());
  auto* cursor_impl_ptr = cursor_impl.get();  [1]
  mojo::PendingAssociatedRemote<blink::mojom::IDBCursor> remote;
  mojo::ReceiverId receiver_id = cursor_receivers_.Add(
      std::move(cursor_impl), remote.InitWithNewEndpointAndPassReceiver());[2]
  cursor_impl_ptr->OnRemoveBinding(
      base::BindOnce(&IndexedDBDispatcherHost::RemoveCursorBinding,
                     weak_factory_.GetWeakPtr(), receiver_id));[5]
  return remote;
}

  ReceiverId Add( 
      ImplPointerType impl,
      PendingType receiver,
      scoped_refptr<base::SequencedTaskRunner> task_runner = nullptr) {
    static_assert(!ContextTraits::SupportsContext(),
                  "Context value required for non-void context type.");
    return AddImpl(std::move(impl), std::move(receiver), false,
                   std::move(task_runner));[3]
  }

ReceiverId AddImpl(ImplPointerType impl,
                     PendingType receiver,
                     Context context,
                     scoped_refptr<base::SequencedTaskRunner> task_runner) {
    DCHECK(receiver.is_valid());
    ReceiverId id = next_receiver_id_++;[4]
    DCHECK_GE(next_receiver_id_, 0u);
    auto entry =
        std::make_unique<Entry>(std::move(impl), std::move(receiver), this, id,
                                std::move(context), std::move(task_runner));
    receivers_.insert(std::make_pair(id, std::move(entry)));[6]
    return id;
  }

Did this work before? N/A 

Chrome version: 89.0.4389.82  Channel: stable
OS Version: 
Flash Version: 

patch suggestion:
  check the ReceiverId returned by cursor_receivers_.Add in IndexedDBDispatcherHost::CreateCursorBinding to avoid it overflow.

koocola(@alo_cook) and Nan Wang(@eternalsakura13) of 360 Alpha Lab

## Attachments

- [git.patch](attachments/git.patch) (text/plain, 1.4 KB)
- [asan.log](attachments/asan.log) (text/plain, 9.9 KB)
- [indexed.html](attachments/indexed.html) (text/plain, 1.8 KB)
- [indexed.html](attachments/indexed.html) (text/plain, 1.8 KB)

## Timeline

### [Deleted User] (2021-03-08)

[Empty comment from Monorail migration]

### su...@gmail.com (2021-03-08)

To trigger the bug quicker ,I patched receiver_set.h and indexed_db_dispatcher_host.cc  in browser.Just to make next_receiver_id increase quicker.It will not influence the browsers logic.

### do...@chromium.org (2021-03-09)

I'm not sure if it's possible in practice to overflow this ID, but perhaps we should be checking that it doesn't overflow before assigning the next one as a defensive measure?

[Monorail components: Blink>Storage>IndexedDB]

### do...@chromium.org (2021-03-09)

[Empty comment from Monorail migration]

### su...@gmail.com (2021-03-09)

[Comment Deleted]

### su...@gmail.com (2021-03-09)

[Comment Deleted]

### su...@gmail.com (2021-03-09)

[Comment Deleted]

### su...@gmail.com (2021-03-09)

[Comment Deleted]

### su...@gmail.com (2021-03-09)

Yes,I think it should be checked.
This bug is almost same pattern like https://bugs.chromium.org/p/chromium/issues/detail?id=925864 .
But this bug in indexedDB can crash the browser process without a compromised render in 32bits.
According to the rate that I test on my virtual machine with asan version ,this bug need nearly 3 days to trigger in 32bits with the following poc which i imroved now.I think it could be quicker in a compromised render process  with release version and real machine.

### pw...@chromium.org (2021-03-09)

If I'm understanding this correctly, the report aim to trigger an integer overflow in mojo::ReceiverSet. Assigning rockot@ because I think individual Chrome features should be able to assume that primitives like ReceiverSet work.

I'm personally skeptical about the exploit. backdoor_addid() seems to be used to advance a counter by 2**52-1. I think we're assuming that a 64-bit ID space cannot be exhausted quickly enough, and backdoor_addid() seems to cut down the space from 64 to 12 bits. That being said, I'd rather let qualified folks take a look.

### su...@gmail.com (2021-03-09)

in 32bits chrome，size_t is 32bits.So like https://bugs.chromium.org/p/chromium/issues/detail?id=925864 .
It’s possibly to trigger.

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/668cf831e91210d4f23e815e07ff1421f3ee9747

commit 668cf831e91210d4f23e815e07ff1421f3ee9747
Author: Ken Rockot <rockot@google.com>
Date: Tue Mar 23 21:13:00 2021

Never fail in ReceiverSet::Add

Because of how UniqueReceiverSet is implemented and used, it is
dangerous to allow Add() to fail: callers reasonably assume that added
objects are still alive immediately after the Add() call.

This changes ReceiverId to a uint64 and simply CHECK-fails on
insert collision.

This fundamentally increases binary size of 32-bit builds, because
a widely used 32-bit data type is expanding to 64 bits for the sake
of security and stability. It is effectively unavoidable for now, and
also just barely above the tolerable threshold.

A follow-up (but less backwards-mergeable) change should be able to
reduce binary size beyond this increase by consolidating shared
code among ReceiverSet template instantiations.

Fixed: 1185732
Change-Id: I9acf6aaaa36e10fdce5aa49a890173caddc13c52
Binary-Size: Unavoidable (see above)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2778871
Commit-Queue: Ken Rockot <rockot@google.com>
Auto-Submit: Ken Rockot <rockot@google.com>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Cr-Commit-Position: refs/heads/master@{#865815}

[modify] https://crrev.com/668cf831e91210d4f23e815e07ff1421f3ee9747/mojo/public/cpp/bindings/receiver_set.h


### [Deleted User] (2021-03-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-24)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-31)

Congratulations superjoe817@! The VRP Panel has decided to award you $5000 for this report. A member of our finance team will be in touch soon to arrange payment. In the meantime, please inform us how you would like to be credited for this issue, such as the name or handle you would like us to use. Nice work!  

### su...@gmail.com (2021-04-01)

koocola(@alo_cook) and Nan Wang(@eternalsakura13) of 360 Alpha Lab.
Thank you!

### am...@google.com (2021-04-02)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-06)

I think this is more than 'Low' severity. This seems to give a browser process UaF which would be Critical. Without the patches, on a 32-bit machine, it seems this would take 3 days to trigger (from https://crbug.com/chromium/1185732#c9) which is long but not inconceivable. I'm going to bump this to Medium, which I suspect means we'll end up merging to a security refresh of M90.

### ad...@google.com (2021-04-06)

Sheriffbot would make a merge request anyway, so shortcutting the process.

### [Deleted User] (2021-04-06)

This bug requires manual review: We are only 6 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-06)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-04-06)

Approving merge to M90, branch 4430. (We don't yet have answers to https://crbug.com/chromium/1185732#c23, but the CL description explicitly says it's designed for backmerging). rockot@ - please merge unless you have any concerns about stability or performance - ideally before 1pm when the M90 stable RC will be cut.

### ad...@google.com (2021-04-06)

M90 merge CL: https://chromium-review.googlesource.com/c/chromium/src/+/2806696

### [Deleted User] (2021-04-06)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2021-04-06)

Please merge your change to M90 branch 4430 so it can be included in M90 Stable promotion, cutting Stable RC today @3:30 PM PT. Thank you.

### gi...@appspot.gserviceaccount.com (2021-04-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6b7e2800a473a496b407e9d4667fb9b73078a666

commit 6b7e2800a473a496b407e9d4667fb9b73078a666
Author: Ken Rockot <rockot@google.com>
Date: Tue Apr 06 21:08:25 2021

Never fail in ReceiverSet::Add

Because of how UniqueReceiverSet is implemented and used, it is
dangerous to allow Add() to fail: callers reasonably assume that added
objects are still alive immediately after the Add() call.

This changes ReceiverId to a uint64 and simply CHECK-fails on
insert collision.

This fundamentally increases binary size of 32-bit builds, because
a widely used 32-bit data type is expanding to 64 bits for the sake
of security and stability. It is effectively unavoidable for now, and
also just barely above the tolerable threshold.

A follow-up (but less backwards-mergeable) change should be able to
reduce binary size beyond this increase by consolidating shared
code among ReceiverSet template instantiations.

(cherry picked from commit 668cf831e91210d4f23e815e07ff1421f3ee9747)

Fixed: 1185732
Change-Id: I9acf6aaaa36e10fdce5aa49a890173caddc13c52
Binary-Size: Unavoidable (see above)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2778871
Commit-Queue: Ken Rockot <rockot@google.com>
Auto-Submit: Ken Rockot <rockot@google.com>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#865815}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2806696
Reviewed-by: Ken Rockot <rockot@google.com>
Reviewed-by: Adrian Taylor <adetaylor@chromium.org>
Commit-Queue: Adrian Taylor <adetaylor@chromium.org>
Cr-Commit-Position: refs/branch-heads/4430@{#1102}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/6b7e2800a473a496b407e9d4667fb9b73078a666/mojo/public/cpp/bindings/receiver_set.h


### ad...@google.com (2021-04-07)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### ja...@google.com (2021-04-12)

[Empty comment from Monorail migration]

### gi...@google.com (2021-04-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/df981dc4d6068439085cfee5609e23d2b21940c0

commit df981dc4d6068439085cfee5609e23d2b21940c0
Author: Ken Rockot <rockot@google.com>
Date: Fri Apr 16 19:00:43 2021

Never fail in ReceiverSet::Add

Because of how UniqueReceiverSet is implemented and used, it is
dangerous to allow Add() to fail: callers reasonably assume that added
objects are still alive immediately after the Add() call.

This changes ReceiverId to a uint64 and simply CHECK-fails on
insert collision.

This fundamentally increases binary size of 32-bit builds, because
a widely used 32-bit data type is expanding to 64 bits for the sake
of security and stability. It is effectively unavoidable for now, and
also just barely above the tolerable threshold.

A follow-up (but less backwards-mergeable) change should be able to
reduce binary size beyond this increase by consolidating shared
code among ReceiverSet template instantiations.

(cherry picked from commit 668cf831e91210d4f23e815e07ff1421f3ee9747)

Fixed: 1185732
Change-Id: I9acf6aaaa36e10fdce5aa49a890173caddc13c52
Binary-Size: Unavoidable (see above)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2778871
Commit-Queue: Ken Rockot <rockot@google.com>
Auto-Submit: Ken Rockot <rockot@google.com>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#865815}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2822154
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1610}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/df981dc4d6068439085cfee5609e23d2b21940c0/mojo/public/cpp/bindings/receiver_set.h


### ja...@google.com (2021-04-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-07-26)

Hello koocola and Nan Wang- we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1185732?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1185731]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055100)*

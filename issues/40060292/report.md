# Security: Heap-use-after-free in user_notes::FrameUserNoteChanges::Apply (Annotation - deleting a note that was just created in another tab causes crash)

| Field | Value |
|-------|-------|
| **Issue ID** | [40060292](https://issues.chromium.org/issues/40060292) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Creation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | gu...@google.com |
| **Created** | 2022-07-15 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. download asan-linux-release-1024589.zip and unzip
2. start a http server at the folder of poc.html
3. run `./chrome --enable-features=UserNotes,UnifiedSidePanel http://127.0.0.1:8605/poc.html` and enable popup
4. right click to `add a note`, when new tab popup, delete the note in new tab.  
   
   Or you could just manually dup the poc.html to trigger this without popup.

**Problem Description:**  

I will provide the analysis ASAP:)  

you can see the ASAN log and video for more info.

**Additional Comments:**

\*\*Chrome version: \*\* 103.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 45.9 KB)
- [poc.webm](attachments/poc.webm) (video/webm, 512.0 KB)
- [poc.html](attachments/poc.html) (text/plain, 106 B)

## Timeline

### [Deleted User] (2022-07-15)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-07-17)

+gujen, can you please take a look?

Reporter: do you mind providing the poc? Or will any file do in this case?

Marking None security impact as this is in a disabled feature. Marking Medium severity as it is a UaF in the browser process, but requires a bit of unusual setup at this point.

[Monorail components: UI>Browser>Creation]

### me...@gmail.com (2022-07-18)

Sorry, I forgot to attach the poc.html.

### gu...@google.com (2022-07-18)

[Empty comment from Monorail migration]

### gu...@google.com (2022-07-18)

[Empty comment from Monorail migration]

### me...@gmail.com (2022-07-19)

In function `FrameUserNoteChanges::Apply`[1], it uses `base::BarrierClosure`[2] to bind the callback (3).

```
void FrameUserNoteChanges::Apply(base::OnceClosure callback) {
 [...]
  base::RepeatingClosure barrier =
      base::BarrierClosure(notes_added_.size(), std::move(callback)); // => (3) bind callback here
  for (const base::UnguessableToken& note_id : notes_added_) {
    const UserNote* note = service_->GetNoteModel(note_id);
    DCHECK(note);

    std::unique_ptr<UserNoteInstance> instance_unique =
        MakeNoteInstance(note, manager);
    manager->AddNoteInstance(std::move(instance_unique), barrier);
  }
}
```

The callback passed to Apply is `UserNoteService::OnFrameChangesApplied`[3], [4], it will erase the changes_id and the corresponding `FrameUserNoteChanges`.(1)

```
// 
void UserNoteService::OnNoteModelsFetched(
    const IdSet& new_notes,
    std::vector<std::unique_ptr<FrameUserNoteChanges>> note_changes,
    std::vector<std::unique_ptr<UserNote>> notes) {
[...]
  for (std::unique_ptr<FrameUserNoteChanges>& diff : note_changes) {
    FrameUserNoteChanges* diff_raw = diff.get();
    note_changes_in_progress_.emplace(diff->id(), std::move(diff));
    diff_raw->Apply(base::BindOnce(&UserNoteService::OnFrameChangesApplied,
                                   weak_ptr_factory_.GetWeakPtr(),
                                   diff_raw->id()));
  }
}
void UserNoteService::OnFrameChangesApplied(base::UnguessableToken change_id) {
  const auto& changes_it = note_changes_in_progress_.find(change_id);
  DCHECK(changes_it != note_changes_in_progress_.end());

  // If this set of changes was for a page that's in an active tab, notify the
  // UI to reload the notes it's displaying.
  const std::unique_ptr<FrameUserNoteChanges>& frame_changes =
      changes_it->second;
  if (delegate_->IsFrameInActiveTab(frame_changes->render_frame_host())) {
    UserNotesUI* ui =
        delegate_->GetUICoordinatorForFrame(frame_changes->render_frame_host());
    DCHECK(ui);
    ui->Invalidate();
  }

  note_changes_in_progress_.erase(changes_it); // =>(1)  FrameUserNoteChanges erased here
}
```


And, if the first arg of `base::BarrierClosure` is zero, it will run the callback directly(2).
```
RepeatingClosure BarrierClosure(size_t num_callbacks_left,
                                OnceClosure done_closure) {
  if (num_callbacks_left == 0) {  // =>(1)
    std::move(done_closure).Run();
    return BindRepeating(&ShouldNeverRun);
  }

  return BindRepeating(&BarrierInfo::Run,
                       std::make_unique<BarrierInfo>(num_callbacks_left,
                                                     std::move(done_closure)));
}
```

So, if we delete the note, the size of `notes_added_` in (3) is zero, So the callback `OnFrameChangesApplied` will be called directly, which will erase the `FrameUserNoteChanges` from the map and delete it. When `notes_added_` is used to enter the for loop, UAF occurs.

To trigger this code path(call `UserNoteService::OnNoteModelsFetched`), you could dup the same tab that has been added any notes OR you could just refresh the tab that has any notes. So the poc could be simplified by refreshing the tab and don't need to open another same tab.






[1] https://source.chromium.org/chromium/chromium/src/+/main:components/user_notes/browser/frame_user_note_changes.cc;l=70;bpv=1;bpt=1
[2] https://source.chromium.org/chromium/chromium/src/+/main:base/barrier_closure.cc;l=46;drc=55569b5e8638661badee35006ae794d9363d76d6
[3] https://source.chromium.org/chromium/chromium/src/+/main:components/user_notes/browser/user_note_service.cc;l=486;drc=7e048e714f1e0545827e47d5f4802b3c86f2269d;bpv=1;bpt=1
[4] https://source.chromium.org/chromium/chromium/src/+/main:components/user_notes/browser/user_note_service.cc;l=480;drc=7e048e714f1e0545827e47d5f4802b3c86f2269d

### gu...@google.com (2022-07-19)

Thanks for the thorough investigation! I plan to take a look today

### gu...@google.com (2022-07-19)

For some reason I am unable to repro this. Even when notes_added_.size() == 0 in the FrameUserNoteChanges, somehow everything works just fine for me on Windows. These two unit tests [1] [2] also exercise this exact code path (notes_added_.size() == 0) on all platforms and they pass just fine.

I guess it doesn't hurt to add an explicit check for notes_added_.empty() and invoke the callback and return before the for loop, but since I don't have a repro I'm not able to confirm this fixes the issue you're seeing. I'll send a CL shortly!

[1]
https://source.chromium.org/chromium/chromium/src/+/main:components/user_notes/browser/frame_user_note_changes_unittest.cc;l=118

[2]
https://source.chromium.org/chromium/chromium/src/+/main:components/user_notes/browser/frame_user_note_changes_unittest.cc;l=150

### me...@gmail.com (2022-07-20)

Hi gujen@, I don't test this issue on Windows. But I test this patch (check for the empty of notes_added_) on Ubuntu , it can surely prevent the UAF. Hope this could help you :)

```
diff --git a/components/user_notes/browser/frame_user_note_changes.cc b/components/user_notes/browser/frame_user_note_changes.cc
index d8c5abd33bf8..dfc0630b445f 100644
--- a/components/user_notes/browser/frame_user_note_changes.cc
+++ b/components/user_notes/browser/frame_user_note_changes.cc
@@ -66,6 +66,9 @@ void FrameUserNoteChanges::Apply(base::OnceClosure callback) {
   // awaited, because the order in which notes are shown in the Notes UI depends
   // on the order of the corresponding highlights in the page. Use a barrier
   // closure to wait until all note highlights have been created in the page.
+if(notes_added_.empty()){
+   return;
+}
   base::RepeatingClosure barrier =
       base::BarrierClosure(notes_added_.size(), std::move(callback));
   for (const base::UnguessableToken& note_id : notes_added_) {
```

### gi...@appspot.gserviceaccount.com (2022-07-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3a4e66049b05ce80abd090fdf023c0210696a917

commit 3a4e66049b05ce80abd090fdf023c0210696a917
Author: Guillaume Jenkins <gujen@google.com>
Date: Wed Jul 20 15:02:41 2022

[Notes] Tentatively fix crash in FrameUserNoteChanges::Apply

When there's a note change in a page with only modified and / or
deleted notes (notes_added_.size() == 0), FrameUserNoteChanges::Apply
crashes. This is because the callback it's passed destroys the
FrameUserNoteChanges instance, and when there are no added notes in the
change, the BarrierClosure used by Apply immediately invokes the
callback. By the time the next line (the loop) attempts to iterate
notes_added_, the instance has already been destroyed.

The fix is simply to return early if there are no added notes.
Unfortunately I cannot repro the crash in my dev environment, so this
fix cannot be verified. However, this code path is covered by unit tests
(which oddly also weren't affected by the crash).

Bug: 1344814
Change-Id: I56398a26cc60f740e86b7fe4ba93648b125c15ef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3777280
Reviewed-by: David Bokan <bokan@chromium.org>
Commit-Queue: David Bokan <bokan@chromium.org>
Auto-Submit: Guillaume Jenkins <gujen@google.com>
Commit-Queue: Guillaume Jenkins <gujen@google.com>
Cr-Commit-Position: refs/heads/main@{#1026249}

[modify] https://crrev.com/3a4e66049b05ce80abd090fdf023c0210696a917/components/user_notes/browser/frame_user_note_changes.cc


### gu...@google.com (2022-07-20)

Added the early return (while still invoking the callback), I believe that should fix the issue. Thanks again!

### [Deleted User] (2022-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-20)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-11)

Congratulations on another one! The VRP Panel has decided to award you $3,000 for this report. The reward amount was based on this issue being mitigated by not being remote exploitable and the user interaction required. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-10-26)

This issue was migrated from crbug.com/chromium/1344814?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060292)*

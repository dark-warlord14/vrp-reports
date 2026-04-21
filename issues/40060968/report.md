# Security: Heap-use-after-free in UserNoteService::OnNoteCreationDone

| Field | Value |
|-------|-------|
| **Issue ID** | [40060968](https://issues.chromium.org/issues/40060968) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Creation |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | gu...@google.com |
| **Created** | 2022-09-14 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**

1. apply the change.diff and compile chromium with ASAN
2. start a http server at the folder of poc.html
3. run `./chrome --user-data-dir=/tmp/noexist --enable-features=UnifiedSidePanel,UserNotes http://127.0.0.1:8605/poc.html`
4. right click to `add a note`, then click `Add` at side panel.

**Problem Description:**  

Function `UserNoteService::OnNoteCreationDone`[1] will pass a raw ptr `note`(1) to `UpdateNote`, `UpdateNote` will use AsyncCall to call `UserNoteDatabase::UpdateNote`[2]. AsyncCall will run `UserNoteDatabase::UpdateNote` on a separate thread, but the `note` could be free on the main thread. So if we could free `note` first, then run the `UserNoteDatabase::UpdateNote`, UAF occurs.  

Note that this race is hard to trigger, so I patch the code to let `UserNoteDatabase::UpdateNote` to sleep some while to make it stable.

```
void UserNoteService::OnNoteCreationDone(const base::UnguessableToken& id,  
                                         const std::u16string& note_content) {  
  DCHECK(IsUserNotesEnabled());  
  
  // Retrieve the partial note from the creation map and send it to the storage  
  // layer so it can officially be created and persisted. This will trigger a  
  // note change event, which will cause the service to propagate this new note  
  // to all relevant pages via `FrameUserNoteChanges::Apply()`. The partial  
  // model will be cleaned up from the creation map as part of that process.  
  const auto& creation_entry_it = creation_map_.find(id);  
  DCHECK(creation_entry_it != creation_map_.end())  
      << "Attempted to complete the creation of a note that doesn't exist";  
  const UserNote\* note = creation_entry_it->second.model.get(); // -> (1) raw ptr `note`   
  if (!note)  
    return;  
  storage_->UpdateNote(note, note_content, /\*is_creation=\*/true);  
}  

```
```
void UserNoteStorageImpl::UpdateNote(const UserNote\* model,  
                                     std::u16string note_body_text,  
                                     bool is_creation) {  
  database_.AsyncCall(&UserNoteDatabase::UpdateNote)  
      .WithArgs(model, note_body_text, is_creation)  
      .Then(base::BindOnce(&UserNoteStorageImpl::OnNotesChanged,  
                           weak_factory_.GetWeakPtr()));  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/user_notes/browser/user_note_service.cc;l=244;drc=8ba1bad80dc22235693a0dd41fe55c0fd2dbdabd;bpv=0;bpt=0>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:components/user_notes/storage/user_note_storage_impl.cc;l=63;drc=8ba1bad80dc22235693a0dd41fe55c0fd2dbdabd;bpv=0;bpt=0>

**Additional Comments:**

\*\*Chrome version: \*\* \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [poc.html](attachments/poc.html) (text/plain, 183 B)

## Timeline

### [Deleted User] (2022-09-14)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-09-14)

I'm delighted to see that the patch merely introduces a sleep(), thus making the condition more likely, rather than changing logic in unpredictable ways.



[Monorail components: UI>Browser>Creation]

### [Deleted User] (2022-09-14)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gu...@google.com (2022-09-21)

I need to set a Security_Impact label in order to mark the status as Started. I chose Impact-None to match the other recent UAF UserNote bugs. Note that this code is behind a disabled flag that isn't exposed in chrome://flags yet.

### gu...@google.com (2022-09-27)

[Empty comment from Monorail migration]

### gu...@google.com (2022-09-27)

[Empty comment from Monorail migration]

### gu...@google.com (2022-09-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b9d30f1da7c5975ec3fbee52dce92d02b57a77a8

commit b9d30f1da7c5975ec3fbee52dce92d02b57a77a8
Author: Guillaume Jenkins <gujen@google.com>
Date: Tue Oct 04 14:42:53 2022

[UserNotes] Fix UAF in OnNoteCreationDone

UserNoteService was passing a UserNote pointer to the storage layer,
which was making async calls on a separate sequence and dereferencing
the pointer there. This was a potential UAF if the UserNote was
destroyed in the service while the async call was running on the
sequence.

Ideally, the fix would have been to pass a WeakPtr and validate it on
the sequence, but UserNote already has a WeakPtrFactory that creates
SafeRefs for the UserNoteInstance objects, so it is already bound to the
main thread. As such, any WeakPtr it produces cannot be dereferenced on
another sequence.

The proposed fix is thus to create a clone of the UserNote, and pass
that to the storage layer and its sequence. Because AsyncCall() uses
the move constructor to forward args to the other sequence, and the
move constructor of UserNote has been deleted by its WeakPtrFactory,
the clone needs to be a unique_ptr. An alternative would have been to
pass the values of the UserNote properties as function parameters, but
there are up to 8, which would have made the code hard to read and maintain.

Bug: 1363583
Change-Id: I96fed460901cced5148f0c0fb44a7fc21b7618a2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3910071
Reviewed-by: Yuheng Huang <yuhengh@chromium.org>
Commit-Queue: Guillaume Jenkins <gujen@google.com>
Cr-Commit-Position: refs/heads/main@{#1054708}

[modify] https://crrev.com/b9d30f1da7c5975ec3fbee52dce92d02b57a77a8/components/user_notes/storage/user_note_database.h
[modify] https://crrev.com/b9d30f1da7c5975ec3fbee52dce92d02b57a77a8/components/user_notes/storage/user_note_storage_impl.cc
[modify] https://crrev.com/b9d30f1da7c5975ec3fbee52dce92d02b57a77a8/components/user_notes/storage/user_note_database_unittest.cc
[modify] https://crrev.com/b9d30f1da7c5975ec3fbee52dce92d02b57a77a8/components/user_notes/model/user_note_target.h
[modify] https://crrev.com/b9d30f1da7c5975ec3fbee52dce92d02b57a77a8/components/user_notes/model/user_note.h
[modify] https://crrev.com/b9d30f1da7c5975ec3fbee52dce92d02b57a77a8/components/user_notes/storage/user_note_database.cc
[modify] https://crrev.com/b9d30f1da7c5975ec3fbee52dce92d02b57a77a8/components/user_notes/model/user_note.cc
[modify] https://crrev.com/b9d30f1da7c5975ec3fbee52dce92d02b57a77a8/components/user_notes/model/user_note_metadata.h


### gu...@google.com (2022-10-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-14)

Congratulations, Weipeng Jiang! The VRP Panel has decided to award you $5,000 for this report of a mildly mitigated security bug. Thank you for your efforts in finding and reporting this issue to us! 

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-01-10)

This issue was migrated from crbug.com/chromium/1363583?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060968)*

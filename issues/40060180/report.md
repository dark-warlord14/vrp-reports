# Security: Heap-use-after-free in UserNoteUICoordinator::Invalidate

| Field | Value |
|-------|-------|
| **Issue ID** | [40060180](https://issues.chromium.org/issues/40060180) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>SidePanel |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2022-07-06 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**

1. start server at the dir of poc.html `python -m SimpleHTTPServer 8605`
2. run `./chrome --enable-features=UserNotes,UnifiedSidePanel --user-data-dir=/tmp/noexist http://127.0.0.1:8605/poc.html`
3. open side panel, switch the combobox to `Notes` then close side panel.
4. wait until UAF occurs.

**Problem Description:**  

`UserNoteUICoordinator::scroll_view_`[1] is a child view of sied panel root\_view, when we close the side panel, the root\_view will be freed and `scroll_view_` could also be freed. But when we close tab or change tab, the Oberver will notify `UserNoteUICoordinator` to call `OnTabStripModelChanged` and it will call `Invalidate`[2], which will use the freed `scroll_view`. UAF.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/side_panel/user_note/user_note_ui_coordinator.cc;l=269;drc=fef630b303c530a6d0fcae0f626efd1201654815>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/side_panel/user_note/user_note_ui_coordinator.cc;l=256;drc=fef630b303c530a6d0fcae0f626efd1201654815>

**Additional Comments:**

\*\*Chrome version: \*\* 102.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 16.2 KB)
- [poc.html](attachments/poc.html) (text/plain, 75 B)
- [poc.webm](attachments/poc.webm) (video/webm, 715.5 KB)

## Timeline

### [Deleted User] (2022-07-06)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-07-06)

This would be a critical sev bug, UAF in the browser process, however it's behind a flag, so there's no need to spin up a new stable version. Downgrading it to high sev.
Security impact None as it's behind a flag, but this should be blocking experiments of launch of SidePanel.

[Monorail components: UI>Browser>TopChrome>SidePanel]

### da...@chromium.org (2022-07-06)

dfriend@ could you please triage?

### ad...@google.com (2022-07-06)

(auto-cc on security bug)

### me...@gmail.com (2022-07-14)

[Comment Deleted]

### me...@gmail.com (2022-07-21)

[Comment Deleted]

### me...@gmail.com (2022-07-28)

[Comment Deleted]

### df...@chromium.org (2022-07-28)

Sorry was out on vacation and then with Covid.

Caroline, this appears to be a side panel issue; can you forward it to the owner?

### co...@chromium.org (2022-07-28)

[Empty comment from Monorail migration]

### gu...@google.com (2022-07-29)

Reassigning to Cheick, who implemented Invalidate()

### gu...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### gu...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### me...@gmail.com (2022-08-19)

[Comment Deleted]

### sr...@google.com (2022-08-22)

[Empty comment from Monorail migration]

### ch...@google.com (2022-08-22)

CL is waiting for approval https://chromium-review.googlesource.com/c/chromium/src/+/3806419

### gi...@appspot.gserviceaccount.com (2022-09-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8666472ecfe5616afec254dd90c1511671968414

commit 8666472ecfe5616afec254dd90c1511671968414
Author: Cheick Cisse <cheickcisse@google.com>
Date: Tue Sep 06 15:32:28 2022

[Note] Fix heap-use_after_free in UserNoteUiCoordinator

This CL uses SidePanelViewStateObserver to observe when the side panel closes and clean up scroll_view_.

Bug: 1342163
Change-Id: I31f7930e1a9246806df68e16ca34d44f0ce40bea
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3806419
Commit-Queue: Cheick Cisse <cheickcisse@google.com>
Reviewed-by: Caroline Rising <corising@chromium.org>
Reviewed-by: Sebastien Seguin-Gagnon <sebsg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1043452}

[modify] https://crrev.com/8666472ecfe5616afec254dd90c1511671968414/components/user_notes/browser/user_note_service.cc
[modify] https://crrev.com/8666472ecfe5616afec254dd90c1511671968414/chrome/browser/ui/views/side_panel/user_note/user_note_ui_coordinator.cc
[modify] https://crrev.com/8666472ecfe5616afec254dd90c1511671968414/chrome/browser/ui/views/side_panel/user_note/user_note_ui_coordinator.h
[modify] https://crrev.com/8666472ecfe5616afec254dd90c1511671968414/components/user_notes/interfaces/user_notes_ui.h
[modify] https://crrev.com/8666472ecfe5616afec254dd90c1511671968414/components/user_notes/browser/user_note_service_unittest.cc
[modify] https://crrev.com/8666472ecfe5616afec254dd90c1511671968414/chrome/browser/ui/views/side_panel/user_note/user_note_ui_coordinator_unittest.cc
[modify] https://crrev.com/8666472ecfe5616afec254dd90c1511671968414/chrome/browser/user_notes/user_note_service_delegate_impl_unittest.cc


### ma...@chromium.org (2022-09-07)

[Empty comment from Monorail migration]

### ch...@google.com (2022-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-09-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-22)

Congratulations! The VRP Panel has decided to award you $7,000 for this report of this mildly mitigated (https://g.co/chrome/vrp) security bug. Thank you for your efforts in reporting this issue to us - nice work! 

### am...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-12-14)

This issue was migrated from crbug.com/chromium/1342163?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1348113, crbug.com/chromium/1354929, crbug.com/chromium/1360065]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060180)*

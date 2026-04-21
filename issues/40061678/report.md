# Security: heap-use-after-free in observer_list.h triggered via Notes/Annotation feature

| Field | Value |
|-------|-------|
| **Issue ID** | [40061678](https://issues.chromium.org/issues/40061678) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>SidePanel |
| **Platforms** | Linux, Mac, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | co...@chromium.org |
| **Created** | 2022-11-10 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Closing a window with Notes/Annotation feature open seems to cause a UAF in certain conditions. I'm having trouble reproducing a second time, but providing ASan stack trace and potential repro steps since that should have enough info to start analysis. Based on stack trace, may not be specific to Notes feature but uncertain about this analysis.

Reproduced with flags: --enable-features=UserNotes,UnifiedSidePanel

Based on a tip from collaborating researcher Vitor Torres, I was poking around with Notes/Annotation feature because UserNoteUICoordinator::InvalidateIfVisible() does not appear to be consistently called in certain circumstances:  

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/side_panel/user_note/user_note_ui_coordinator.cc;l=236;drc=1e6c1a39cbbc1dcad6e7828661d74d76463465ed>

It's conditionally called in these two places of interest:

\* UserNoteUICoordinator::OnTabStripModelChanged()  

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/side_panel/user_note/user_note_ui_coordinator.cc;l=362;drc=1e6c1a39cbbc1dcad6e7828661d74d76463465ed>

```
if (!selection.active_tab_changed() || tab_strip_model->closing_all())  
    return;  
  
  InvalidateIfVisible();  

```

\* UserNoteService::OnNoteMetadataFetchedForNavigation()  

<https://source.chromium.org/chromium/chromium/src/+/main:components/user_notes/browser/user_note_service.cc;l=425;drc=1e6c1a39cbbc1dcad6e7828661d74d76463465ed>

```
  if (!rfh) {  
    // The navigated frame is no longer valid.  
    return;  
  }  
  
  if (delegate_->IsFrameInActiveTab(rfh)) {  
    UserNotesUI\* ui = delegate_->GetUICoordinatorForFrame(rfh);  
    DCHECK(ui);  
  
    // TODO(crbug.com/1313967): For now, always invalidate the UI if the tab is  
    // in the foreground. This is to fix edge cases around back/forward  
    // navigations, where the Page (and attached UserNoteManager) is kept alive  
    // in the BFCache. If the notes didn't change on disk by the time the user  
    // does a back/forward navigation, InvalidateIfVisible() will never get  
    // called because there won't be any diff between the instances in the Page  
    // and the notes on disk. Ideally, InvalidateIfVisible() should only be  
    // called if this is a back/forward navigation and the notes didn't change,  
    // but there's no way to know whether the notes changed until further down  
    // the callback stack. Since InvalidateIfVisible() is cheap enough, always  
    // calling it here is considered an acceptable fix for now.  
    ui->InvalidateIfVisible();  
    // [...]  
  }  

```

Since the view wouldn't be invalidated using the UserNoteUICoordinator::OnTabStripModelChanged() path if all tabs were closing in a window, I tried that, and eventually triggered the UAF in less than two minutes. I'm not sure if this analysis is relevant, but it's what led me to try the repro steps.

Hopefully I can repro again soon with more specific steps.

**VERSION**  

Chrome Version: ASan build 1069279 (asan-win32-release\_x64-1069279)  

Operating System: Windows 10 Version 21H2 (Build 19044.2006)

**REPRODUCTION CASE**  

Inexact repro steps for now, since I was only able to repro once:

1. Open browser with --enable-features=UserNotes,UnifiedSidePanel
2. Right-click any page and select "Add a note" to open side panel with Notes view
3. Open new window
4. ???
5. Close new window to trigger UAF

Between steps 3 and 5, might be one or more of the following (or something completely different within Notes):  

\* In new window, add a note  

\* In new window, add a note, cancel, and add a note again  

\* In new window, create second tab, then add a note  

\* In new window, add note, then create second tab

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com> and Vitor Torres <https://github.com/vtorres/>

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 21.2 KB)
- [Notes-CHECK-asan.log](attachments/Notes-CHECK-asan.log) (text/plain, 7.7 KB)
- [Notes-CHECK-repro.mp4](attachments/Notes-CHECK-repro.mp4) (video/mp4, 1.3 MB)

## Timeline

### al...@alesandroortiz.com (2022-11-10)

Please CC collaborating researcher vitortorresvt@gmail.com when possible.

### [Deleted User] (2022-11-10)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-11-10)

This seems related to the UAF and is what triggered our investigation.

Using different repro steps (see below), Vitor was able to hit this CHECK which was added in https://source.chromium.org/chromium/chromium/src/+/12993351a415619a445a836ca8a94a6310569dbd to prevent double-observation:

[FATAL:scoped_observation.h(114)] Check failed: source_ == nullptr (000012DC54057400 vs. nullptr)
Backtrace:
        base::debug::CollectStackTrace [0x00007FF976DB83F2+18] (C:\b\s\w\ir\cache\builder\src\base\debug\stack_trace_win.cc:329)
        base::debug::StackTrace::StackTrace [0x00007FF9798729FA+26] (C:\b\s\w\ir\cache\builder\src\base\debug\stack_trace.cc:218)
        logging::LogMessage::~LogMessage [0x00007FF976C1F583+691] (C:\b\s\w\ir\cache\builder\src\base\logging.cc:719)
        logging::LogMessage::~LogMessage [0x00007FF976C23470+16] (C:\b\s\w\ir\cache\builder\src\base\logging.cc:712)
        base::ScopedObservation<views::View,views::ViewObserver>::Observe [0x00007FF97573627D+345] (C:\b\s\w\ir\cache\builder\src\base\scoped_observation.h:114)
        UserNoteUICoordinator::StartNoteCreation [0x00007FF98750EDFB+147] (C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\side_panel\user_note\user_note_ui_coordinator.cc:192)

See asan-CHECK.log for full stack trace.

Repro steps:
1. Open browser with --enable-features=UserNotes,UnifiedSidePanel
2. Right-click any page and select "Add a note" to open side panel with Notes view
3. Click cancel on the newly created note
4. Repeat steps 2+3 until CHECK is hit (should be on the third "Add a note" interaction)

Attached video of CHECK repro. If this is unrelated, let us know and we can file separate bug.

### al...@alesandroortiz.com (2022-11-10)

For https://crbug.com/chromium/1382969#c3 CHECK:

Hits this CHECK: https://source.chromium.org/chromium/chromium/src/+/main:base/scoped_observation.h;l=114;drc=8fdfb672b5f96dd3725dfd962363ba3ab7aa515e
Observe() call made within UserNoteUICoordinator::StartNoteCreation(): https://source.chromium.org/chromium/chromium/src/+/HEAD:chrome/browser/ui/views/side_panel/user_note/user_note_ui_coordinator.cc;l=191;drc=1e6c1a39cbbc1dcad6e7828661d74d76463465ed

### wf...@chromium.org (2022-11-10)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-11-10)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>TopChrome>SidePanel]

### wf...@chromium.org (2022-11-10)

Thanks for your report. I can hit the check in #3, but have not yet managed to hit the UAF.

### wf...@chromium.org (2022-11-10)

I'm assigning to gujen@google.com to help repro here. I still am unable to repro any UAF but am hitting the CHECK. Without a repro for the UAF it might be hard for us to understand the impact on user safety.

### gu...@google.com (2022-11-10)

+cheickcisse, who wrote the UI code of Notes, and +yuhengh, who is reworking the notes logic.

The Notes UI is in the process of being rewritten to WebUI. Because it is fully behind a disabled flag, and because there is no plan to release it to users until the WebUI rewrite has happened, and because there is no conclusive repro for this, I propose to wait until we either find a consistent repro or the code is removed in favor of the new WebUI code.

Yuheng, do you have an ETA on the WebUI rewrite?

### wf...@chromium.org (2022-11-10)

okay thanks, since this is flagged and not being trialed I'm marking it security_impact-none but hard to know the severity without a repro.

### yu...@chromium.org (2022-11-10)

@gujen
The WebUI rewrite is actively being worked on right now and the ETA early next year.
The Notes backend is also being worked on leveraging power bookmarks backend so I don't think this bug is going to affect the new notes project. Wait until the code is removed seems like the best thing to do here.

### wf...@chromium.org (2022-11-10)

okay out of the abundance of caution I'm going to leave this as High (as there is a UAF stack from the reporter) but impact=none. It would be useful to mark this bug as a blocker for the Notes launch, then we can verify that it's fixed by the time it launches, as the security sheriff probably won't look at this bug as it's impact-none. Can you add that bug link? Thanks.

### ad...@google.com (2022-11-10)

(auto-cc on security bug)

### yu...@chromium.org (2022-11-10)

We don't have a launch bug yet, I will take the bug and update information according when we have it.

### [Deleted User] (2022-11-12)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-11-14)

Thanks for triage so far.

If I understand correctly, the UAF won't be investigated further unless there's a more reliable reproduction case?

Re: https://crbug.com/chromium/1382969#c3, I'm also able to hit that CHECK with these repro steps:
1. Open browser with --enable-features=UserNotes,UnifiedSidePanel
2. Right-click any page and select "Add a note" to open side panel with Notes view
3. Reload page: this can be done by page with JS or by user manually
4. Repeat steps 2+3 until CHECK is hit (should be on the third "Add a note" interaction)

### yu...@chromium.org (2022-11-15)

The current code path will be deprecated soon, before the feature is shipped to any real users.  So even if we have a reliable reproduction case I don't think it's worth fixing, thanks.

### al...@alesandroortiz.com (2022-11-15)

Fair enough, thanks for clarification.

### al...@alesandroortiz.com (2022-11-15)

Quick update: Was able to get consistent repro with same stack trace on a much older ASan build, but there it's a null read. Will try to get a consistent UAF shortly either on that version or another ASan build that's between 995515 and 1069279.

This seems very similar to https://crbug.com/chromium/1320181 (that was for the ReadAnything feature).

### am...@chromium.org (2022-11-16)

[security marshal] Hi yuhengh@ what is the timeline / ETA for this code path to be deprecated and removed? 

general note for future check-ins: this issue should remain open until that time. 





### an...@chromium.org (2022-12-06)

[security marshal] Hi yuhengh@! Just following up on the previous comment. Any update on the deprecation timeline? Thanks!

### yu...@chromium.org (2022-12-06)

We are planning to launch the new Notes in M112, but I think the old frontend should be deprecated way before that. @corising is working on the new frontend. Do you know when it will replace the old frontend?

### an...@chromium.org (2022-12-12)

Hi corising@, could you provide an update on the frontend work? Thanks!

### an...@chromium.org (2022-12-19)

Friendly ping from the security marshal. corising@, yuhengh@ any update on the deprecation of the old frontend?

### co...@chromium.org (2022-12-20)

We are planning to start deprecating the old frontend shortly after landing changes:
https://chromium-review.googlesource.com/c/chromium/src/+/4069245
https://chromium-review.googlesource.com/c/chromium/src/+/4059975

### ja...@chromium.org (2023-02-02)

Hi corising@ and yuhengh@, I can see that the two changes from https://crbug.com/chromium/1382969#c25 have landed. Have you made progress on deprecating the affected UI?

Thanks for the update.

### co...@chromium.org (2023-02-02)

Yes this code is no longer run as of https://chromium-review.googlesource.com/c/chromium/src/+/4059975 and was removed as of https://chromium-review.googlesource.com/c/chromium/src/+/4188350. Marking this as fixed

### [Deleted User] (2023-02-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-03)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-09)

Congratulations! The VRP Panel has decided to award you $1,000 for this report of a very heavily mitigated security bug. Thank you for the solid quality report and your efforts in reporting this issue to us!

### am...@google.com (2023-02-11)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-02-18)

Thanks for the reward and for providing updates here. I'll continue looking at Notes this year with the refactored code.

### [Deleted User] (2023-05-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-05-13)

This issue was migrated from crbug.com/chromium/1382969?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061678)*

# TaskManager fails to keep Profile alive leading to UAF in CreateNativeWidget

| Field | Value |
|-------|-------|
| **Issue ID** | [40056556](https://issues.chromium.org/issues/40056556) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Profiles, UI>TaskManager |
| **Platforms** | Windows |
| **Reporter** | wx...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2021-07-15 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36

Steps to reproduce the problem:
1.lanch chromium and open task window.
2.open anathor profile window, close the current profile window.
3.right click task window, browser crash

my chromium version is 3f011eda583817f209cc2d064eba276a7926537b

What is the expected behavior?

What went wrong?
browser crash

Did this work before? N/A 

Chrome version: 91.0.4472.124  Channel: stable
OS Version: 10.0

## Attachments

- [uaf.txt](attachments/uaf.txt) (text/plain, 24.3 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 8.2 MB)

## Timeline

### [Deleted User] (2021-07-15)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-07-15)

[Empty comment from Monorail migration]

### jd...@chromium.org (2021-07-16)

I'm unable to reproduce this. Are you able to reproduce it reliably on Canary, or just in Chrome stable?

### wx...@gmail.com (2021-07-16)

I try it from lateset chromium,(its version is 3f011eda583817f209cc2d064eba276a7926537b) I will try to download a asan version of Canary

### [Deleted User] (2021-07-16)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wx...@gmail.com (2021-07-16)

I can reproduce in asan-win32-release_x64-899809.

### do...@chromium.org (2021-07-21)

+some views folks, can you take a look at this?

[Monorail components: Blink>ViewSource Internals>Views]

### pb...@chromium.org (2021-07-21)

AIUI this is not a views question:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/native_widget_factory.cc;l=52;drc=2e3beeadb7a48af2c3dd58e0ec22085fc988636b

This is a UAF because profile has already been destroyed.

Part of the destroy stack has:
    #15 0x7ff8d5982904 in ProfileManager::RemoveKeepAlive(class Profile const *, enum ProfileKeepAliveOrigin) E:\work\fuzz\chromium_src\src\chrome\browser\profiles\profile_manager.cc:1388:3

Maybe the TaskManager needs to keep the profile alive, or close urgently at this point, idk.

[Monorail components: -Blink>ViewSource -Internals>Views UI>Browser>Profiles UI>TaskManager]

### pb...@chromium.org (2021-07-21)

-> nicolaso@ as this relates to DestroyProfileOnBrowserClose

updating the cl description to my rough understanding

### ni...@chromium.org (2021-07-21)

Thanks for the bug report, I'll get started right away

> Maybe the TaskManager needs to keep the profile alive

I think the bug is more general than this, unfortunately. It's due to SetThemeForProfileWindow(), and a now-incorrect assumption described in the comment here: https://crgo.dev/c/b/ui/views/native_widget_factory.cc;l=48-52;drc=43e2faaae6d1ef18762e1f8e5082fd2a59399abe

Seems like we want to to SetThemeForProfileWindow(nullptr) when the Profile is destroyed, or use a WeakPtr-like pointer to the Profile.

### ni...@chromium.org (2021-07-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-07-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/51ab2b4b4702040ee12288d03fbc073d766c071f

commit 51ab2b4b4702040ee12288d03fbc073d766c071f
Author: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Date: Wed Jul 21 23:02:27 2021

[Views] Fix UaF caused by TaskManagerView

TaskManagerView could stay visible even after the Profile* was
destroyed, and creating a ContextMenu tried to use its
ThemeProfileForWindow.

Make ThemeProfileForWindow reset to nullptr when the Profile* is
destoryed to avoid the use-after-free.

Bug: 1229625
Change-Id: I4451df05de11fbf8fd6ffde86521a1d0e5a9f667
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3041368
Commit-Queue: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Commit-Position: refs/heads/master@{#904095}

[modify] https://crrev.com/51ab2b4b4702040ee12288d03fbc073d766c071f/chrome/browser/ui/views/theme_profile_key.cc


### ni...@chromium.org (2021-07-21)

Marking fixed

### [Deleted User] (2021-07-21)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and Security_Impact labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues Impact guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jd...@chromium.org (2021-07-21)

Sorry for the missing labels.

This is a UaF in the browser process. That'd be very bad (critical) if it were web accessible, but it requires substantial and unnatural user interaction. What's more, I'm not convinced it's remotely controllable, since it's over in the task manager. And it's further tricky because all of the first profile's windows had to be closed so as to trigger this. To me, that doesn't sound exploitable.

That said, I'd appreciate it if adetaylor@ actually made the call on severity.

### [Deleted User] (2021-07-21)

[Empty comment from Monorail migration]

### ni...@chromium.org (2021-07-22)

Also, this bug is behind a flag (DestroyProfileOnBrowserClose) which is disabled on Beta and Stable.

I may end up pushing it a small portion of the Beta population in M93, though, so maybe it's still worth merging.

### ad...@chromium.org (2021-07-22)

Re https://crbug.com/chromium/1229625#c15

I agree this is mitigated down from Critical to High severity by the unusual UI interaction. Arguably the UI interaction is so obscure that this is mitigated to 'medium' but as a matter of policy we tend to mitigate stuff down by only one notch, so marking as High.

Re https://crbug.com/chromium/1229625#c17, hm, if the earliest version where real users could be affected is M93, then I'll label this as FoundIn-93, and I do agree we should probably merge it. Adding a merge request for consideration.

### [Deleted User] (2021-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-22)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-22)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-22)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-07-23)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-07-28)

The VRP Panel has decided to award you $1,000 for this report. Thank you so much for reporting this issue! 

### am...@google.com (2021-07-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-21)

[Empty comment from Monorail migration]

### jo...@chromium.org (2021-09-22)

Did this get merged to M93?

### vo...@google.com (2021-09-23)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-09-27)

Re https://crbug.com/chromium/1229625#c29, no, and it looks like a sheriffbot bug: https://crbug.com/chromium/1253642.

### rz...@google.com (2021-10-05)

[Empty comment from Monorail migration]

### gi...@google.com (2021-10-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4a4f2093bba6131f6e856ba7da253cad2e5ea115

commit 4a4f2093bba6131f6e856ba7da253cad2e5ea115
Author: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Date: Wed Oct 06 14:38:13 2021

[M90-LTS][Views] Fix UaF caused by TaskManagerView

TaskManagerView could stay visible even after the Profile* was
destroyed, and creating a ContextMenu tried to use its
ThemeProfileForWindow.

Make ThemeProfileForWindow reset to nullptr when the Profile* is
destoryed to avoid the use-after-free.

M90 merge issues:
  The lts branch is missing a change to allow unique_ptr as arguments
  of SetProperty:
   https://chromium-review.googlesource.com/c/chromium/src/+/3016342)
  Changed the SetProperty call on SetThemeProfileForWindow
  to use a raw pointer.

(cherry picked from commit 51ab2b4b4702040ee12288d03fbc073d766c071f)
(cherry picked from commit 112d20b81e418e216df2280c4cd99a20a095b23a)

Bug: 1229625
Change-Id: I4451df05de11fbf8fd6ffde86521a1d0e5a9f667
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3041368
Commit-Queue: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#904095}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3173227
Reviewed-by: Jana Grill <janagrill@google.com>
Reviewed-by: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1637}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/4a4f2093bba6131f6e856ba7da253cad2e5ea115/chrome/browser/ui/views/theme_profile_key.cc


### rz...@google.com (2021-10-06)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1229625?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Profiles, UI>TaskManager]
[Monorail mergedwith: crbug.com/chromium/1231963]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056556)*

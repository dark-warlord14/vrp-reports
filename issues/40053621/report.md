# Security: Use-after-free in MediaStreamCaptureIndicator::WebContentsDeviceUsage::AddDevices()

| Field | Value |
|-------|-------|
| **Issue ID** | [40053621](https://issues.chromium.org/issues/40053621) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>MediaStream, UI>Browser>MediaCapture |
| **Platforms** | Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2020-10-14 |
| **Bounty** | $10,000.00 |

## Description

Chrome Version: 88.0.4292.0 (Official Build) canary (x86_64)
Operating System: MacOS

1. Open PoC.html
2. Open a new tab
3. In poc.html page select "Chrome tab" in the pop-up dialog box, then try to share the new tab
4. Close the shared tab 
5. Try to cancel the print dialog


Received signal 11 SEGV_MAPERR fffffffd5524cd33
#0 0x555b692020b9 base::debug::CollectStackTrace()
#1 0x555b691774e3 base::debug::StackTrace::StackTrace()
#2 0x555b69201c5b base::debug::(anonymous namespace)::StackDumpSignalHandler()
#3 0x7fd89ee023c0 (/usr/lib/x86_64-linux-gnu/libpthread-2.31.so+0x153bf)
#4 0x555b6954d69e MediaStreamCaptureIndicator::WebContentsDeviceUsage::AddDevices()
#5 0x555b6954fa9b MediaStreamCaptureIndicator::UIDelegate::OnStarted()
#6 0x555b6bf1284c TabSharingUIViews::CreateTabCaptureIndicator()
#7 0x555b6bf1247c TabSharingUIViews::OnStarted()
#8 0x555b6954fadc MediaStreamCaptureIndicator::UIDelegate::OnStarted()
#9 0x555b679ce862 content::MediaStreamUIProxy::Core::OnStarted()
#10 0x555b691ea6a6 base::(anonymous namespace)::PostTaskAndReplyRelay::RunTaskAndPostReply()
#11 0x555b691ea899 base::internal::Invoker<>::RunOnce()
#12 0x555b691c4836 base::TaskAnnotator::RunTask()
#13 0x555b691d557d base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()
#14 0x555b691d5278 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#15 0x555b6918c157 base::(anonymous namespace)::WorkSourceDispatch()
#16 0x7fd89ecaafbd g_main_context_dispatch
#17 0x7fd89ecab240 (/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.6400.2+0x5223f)
#18 0x7fd89ecab2e3 g_main_context_iteration
#19 0x555b6918bf12 base::MessagePumpGlib::Run()
#20 0x555b691d5b9d base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#21 0x555b691ac5ce base::RunLoop::Run()
#22 0x555b694f24b3 ChromeBrowserMainParts::MainMessageLoopRun()
#23 0x555b67712395 content::BrowserMainLoop::RunMainMessageLoopParts()
#24 0x555b677142a2 content::BrowserMainRunnerImpl::Run()
#25 0x555b6770f698 content::BrowserMain()
#26 0x555b691221fc content::ContentMainRunnerImpl::RunServiceManager()
#27 0x555b69121dee content::ContentMainRunnerImpl::Run()
#28 0x555b6911f206 content::RunContentProcess()
#29 0x555b6911fbec content::ContentMain()
#30 0x555b669054ca ChromeMain
#31 0x7fd89d64b0b3 __libc_start_main
#32 0x555b669052ea _start
  r8: 0000000000000000  r9: 00007fd88e7526c0 r10: 0000000000000000 r11: 0000000000000286
 r12: 00003524097990f0 r13: 000035240b47af50 r14: 00003524097990f0 r15: 000035240b47af50
  di: 0000352409ff9800  si: 0000000000000002  bp: 00007fff988c0c30  bx: 000035240983a9a0
  dx: 0000000000000001  ax: 0000352409ff9800  cx: fffffffd5524cb03  sp: 00007fff988c0b90
  ip: 0000555b6954d69e efl: 0000000000010206 cgf: 002b000000000033 erf: 0000000000000005
 trp: 000000000000000e msk: 0000000000000000 cr2: fffffffd5524cd33


## Attachments

- [screen.mov](attachments/screen.mov) (video/quicktime, 8.7 MB)
- [poc.html](attachments/poc.html) (text/plain, 98 B)
- [poc.html](attachments/poc_53358606.html) (text/plain, 89 B)

## Timeline

### pa...@chromium.org (2020-10-15)

guidou, could you please take a look, or pass this to someone else knowledgeable? Thanks!

Although this is a UAF in the browser, it seems to require significant and unlikely user interaction, so I don't think it's at the usual degree of severity for browser UAFs.

### ch...@gmail.com (2020-10-15)

[Empty comment from Monorail migration]

### pa...@chromium.org (2020-10-15)

[Empty comment from Monorail migration]

[Monorail components: Blink>MediaStream UI>Browser>TabCapture]

### pa...@chromium.org (2020-10-15)

[Empty comment from Monorail migration]

### pa...@chromium.org (2020-10-15)

[Empty comment from Monorail migration]

### ch...@gmail.com (2020-10-15)

Chrome stable 86 has the same issue, so it's not a regression.

### ch...@gmail.com (2020-10-23)

[Comment Deleted]

### ch...@gmail.com (2020-10-23)

Reproduced this on a recent ASAN build. Here's the relevant part of the log:

==8732==ERROR: AddressSanitizer: heap-use-after-free on address 0x61d0003a6898 at pc 0x00011d90ead8 bp 0x7fff56fe3430 sp 0x7fff56fe3428
READ of size 8 at 0x61d0003a6898 thread T0
    #0 0x11d90ead7 in content::WebContentsImpl::AddObserver(content::WebContentsObserver*) vector:1524
    #1 0x12513efa7 in MediaStreamCaptureIndicator::RegisterMediaStream(content::WebContents*, std::__1::vector<blink::MediaStreamDevice, std::__1::allocator<blink::MediaStreamDevice> > const&, std::__1::unique_ptr<MediaStreamUI, std::__1::default_delete<MediaStreamUI> >) media_stream_capture_indicator.cc:135
    #2 0x131af7bae in TabSharingUIViews::CreateTabCaptureIndicator() tab_sharing_ui_views.cc:306
    #3 0x131af74bb in TabSharingUIViews::OnStarted(base::OnceCallback<void ()>, base::RepeatingCallback<void (content::DesktopMediaID const&)>) tab_sharing_ui_views.cc:148
    #4 0x125144119 in MediaStreamCaptureIndicator::UIDelegate::OnStarted(base::OnceCallback<void ()>, base::RepeatingCallback<void (content::DesktopMediaID const&)>) media_stream_capture_indicator.cc:214
    #5 0x11d1e313f in content::MediaStreamUIProxy::Core::OnStarted(long*, bool) media_stream_ui_proxy.cc:144

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### gu...@chromium.org (2020-11-02)

agpalak@: Can you take a look?

### ch...@gmail.com (2020-11-03)

Browser process UAFs are usually critical severity but as this requires a user interaction, so I think this is probably high severity as https://crbug.com/chromium/1135018.

### ag...@chromium.org (2020-11-03)

[Empty comment from Monorail migration]

### ke...@chromium.org (2020-11-03)

Sev-High sounds reasonable based on precedent and our severity guidelines.

### [Deleted User] (2020-11-04)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ag...@chromium.org (2020-11-16)

[Empty comment from Monorail migration]

### gu...@chromium.org (2020-11-16)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/629f75862b63e95c5f4651a15c8523949c5f98a3

commit 629f75862b63e95c5f4651a15c8523949c5f98a3
Author: Guido Urdaneta <guidou@chromium.org>
Date: Wed Nov 18 13:15:06 2020

[TabSharing] Stop capturing when the captured tab is destroyed

This CL prevents the creation of a TabSharing UI for tabs that
are destroyed before the UI is even started.

Bug: 1138683
Change-Id: I4849b2b78e6e3a5efebe590d0d0e532e231285fb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2545164
Reviewed-by: Marina Ciocea <marinaciocea@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/heads/master@{#828689}

[modify] https://crrev.com/629f75862b63e95c5f4651a15c8523949c5f98a3/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc
[modify] https://crrev.com/629f75862b63e95c5f4651a15c8523949c5f98a3/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.h


### gu...@chromium.org (2020-11-18)

[Empty comment from Monorail migration]

### gu...@chromium.org (2020-11-18)

[Empty comment from Monorail migration]

### gu...@chromium.org (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-19)

Your change meets the bar and is auto-approved for M88. Please go ahead and merge the CL to branch 4324 (refs/branch-heads/4324) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b5c7c7c8371a3759aaad5c40a81c337544340b80

commit b5c7c7c8371a3759aaad5c40a81c337544340b80
Author: Guido Urdaneta <guidou@chromium.org>
Date: Thu Nov 19 16:31:19 2020

[TabSharing] Stop capturing when the captured tab is destroyed

This CL prevents the creation of a TabSharing UI for tabs that
are destroyed before the UI is even started.

(cherry picked from commit 629f75862b63e95c5f4651a15c8523949c5f98a3)

Bug: 1138683
Change-Id: I4849b2b78e6e3a5efebe590d0d0e532e231285fb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2545164
Reviewed-by: Marina Ciocea <marinaciocea@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#828689}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2550381
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#152}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/b5c7c7c8371a3759aaad5c40a81c337544340b80/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc
[modify] https://crrev.com/b5c7c7c8371a3759aaad5c40a81c337544340b80/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.h


### gu...@chromium.org (2020-11-19)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-19)

This bug requires manual review: Request affecting a post-stable build
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
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-11-19)

Approving merge to M87, branch 4280. Please wait for a day of Canary data before merging.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/848bfc355226259f298516932214f9dad56111ba

commit 848bfc355226259f298516932214f9dad56111ba
Author: Guido Urdaneta <guidou@chromium.org>
Date: Mon Nov 23 06:26:59 2020

[TabSharing] Stop capturing when the captured tab is destroyed

This CL prevents the creation of a TabSharing UI for tabs that
are destroyed before the UI is even started.

(cherry picked from commit 629f75862b63e95c5f4651a15c8523949c5f98a3)

Bug: 1138683
Change-Id: I4849b2b78e6e3a5efebe590d0d0e532e231285fb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2545164
Reviewed-by: Marina Ciocea <marinaciocea@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#828689}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2552863
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#1549}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/848bfc355226259f298516932214f9dad56111ba/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc
[modify] https://crrev.com/848bfc355226259f298516932214f9dad56111ba/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.h


### ad...@google.com (2020-12-02)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-02)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-03)

Congratulations, the VRP panel has awarded $10,000 for this bug.

### ad...@google.com (2020-12-04)

[Empty comment from Monorail migration]

### as...@google.com (2020-12-08)

ketakid@, could you please take a look at the merge to LTS?

### ke...@google.com (2020-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8379fcfae60e06d46b332f220027b02cc9c4f451

commit 8379fcfae60e06d46b332f220027b02cc9c4f451
Author: Guido Urdaneta <guidou@chromium.org>
Date: Wed Dec 16 18:43:29 2020

[TabSharing] Stop capturing when the captured tab is destroyed

This CL prevents the creation of a TabSharing UI for tabs that
are destroyed before the UI is even started.

(cherry picked from commit 629f75862b63e95c5f4651a15c8523949c5f98a3)

Bug: 1138683
Change-Id: I4849b2b78e6e3a5efebe590d0d0e532e231285fb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2545164
Reviewed-by: Marina Ciocea <marinaciocea@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#828689}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2587056
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1490}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/8379fcfae60e06d46b332f220027b02cc9c4f451/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc
[modify] https://crrev.com/8379fcfae60e06d46b332f220027b02cc9c4f451/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.h


### [Deleted User] (2020-12-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mf...@chromium.org (2021-03-22)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>MediaCapture]

### mf...@chromium.org (2021-03-22)

[Empty comment from Monorail migration]

[Monorail components: -UI>Browser>TabCapture]

### am...@chromium.org (2021-03-29)

Hi, chromium.khalil@ - we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### ch...@gmail.com (2021-03-29)

Yeah yeah! no problem!

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1138683?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>MediaStream, UI>Browser>MediaCapture]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053621)*
